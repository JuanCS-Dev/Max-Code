"""Unit tests for database models.

Day 4: Comprehensive testing of SQLAlchemy models.

Tests cover:
- Model creation and validation
- to_dict() serialization
- Relationships and cascades
- URL hashing for cognitive map
- Timestamps and defaults

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import select

from db.models import (
    BrowserSession,
    BrowserAction,
    CognitiveMapPage,
    NavigationPath,
)


# ============================================================================
# BROWSER SESSION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestBrowserSession:
    """Test BrowserSession model."""

    async def test_create_browser_session(self, db_session):
        """Test creating a browser session with all fields."""
        session = BrowserSession(
            status="active",
            browser_type="chromium",
            viewport_width=1920,
            viewport_height=1080,
            user_agent="Mozilla/5.0 Test",
            context_data={"locale": "en-US"},
            metadata={"test": True},
        )
        db_session.add(session)
        await db_session.commit()

        assert session.id is not None
        assert session.created_at is not None
        assert session.last_active is not None
        assert session.status == "active"
        assert session.browser_type == "chromium"

    async def test_browser_session_defaults(self, db_session):
        """Test default values for browser session."""
        session = BrowserSession()
        db_session.add(session)
        await db_session.commit()

        assert session.status == "active"
        assert session.browser_type == "chromium"
        assert session.closed_at is None

    async def test_browser_session_to_dict(self, db_session):
        """Test to_dict() serialization."""
        session = BrowserSession(
            status="active",
            browser_type="firefox",
            viewport_width=1280,
            viewport_height=720,
        )
        db_session.add(session)
        await db_session.commit()

        data = session.to_dict()

        assert isinstance(data, dict)
        assert data["status"] == "active"
        assert data["browser_type"] == "firefox"
        assert data["viewport_width"] == 1280
        assert "id" in data
        assert "created_at" in data

    async def test_browser_session_relationship_cascade(self, db_session):
        """Test that deleting session cascades to actions."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        # Add action
        action = BrowserAction(
            session_id=session.id,
            action_type="navigate",
            url="https://test.com",
            success=True,
        )
        db_session.add(action)
        await db_session.commit()

        # Verify action exists
        result = await db_session.execute(
            select(BrowserAction).where(BrowserAction.session_id == session.id)
        )
        assert result.scalar_one_or_none() is not None

        # Delete session
        await db_session.delete(session)
        await db_session.commit()

        # Verify action was cascaded
        result = await db_session.execute(
            select(BrowserAction).where(BrowserAction.session_id == session.id)
        )
        assert result.scalar_one_or_none() is None


# ============================================================================
# BROWSER ACTION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestBrowserAction:
    """Test BrowserAction model."""

    async def test_create_browser_action(self, db_session):
        """Test creating a browser action."""
        # First create session
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        action = BrowserAction(
            session_id=session.id,
            action_type="click",
            url="https://example.com",
            selector="button.submit",
            parameters={"button": "left"},
            success=True,
            duration_ms=250,
            metadata={"test": True},
        )
        db_session.add(action)
        await db_session.commit()

        assert action.id is not None
        assert action.created_at is not None
        assert action.action_type == "click"
        assert action.success is True

    async def test_browser_action_failure(self, db_session):
        """Test recording failed action."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        action = BrowserAction(
            session_id=session.id,
            action_type="click",
            url="https://example.com",
            selector="nonexistent",
            success=False,
            error_message="Element not found",
            error_type="ElementNotFoundError",
        )
        db_session.add(action)
        await db_session.commit()

        assert action.success is False
        assert action.error_message is not None
        assert "not found" in action.error_message.lower()

    async def test_browser_action_to_dict(self, db_session):
        """Test to_dict() serialization."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        action = BrowserAction(
            session_id=session.id,
            action_type="navigate",
            url="https://test.com",
            success=True,
            duration_ms=1500,
        )
        db_session.add(action)
        await db_session.commit()

        data = action.to_dict()

        assert isinstance(data, dict)
        assert data["action_type"] == "navigate"
        assert data["url"] == "https://test.com"
        assert data["success"] is True
        assert data["duration_ms"] == 1500


# ============================================================================
# COGNITIVE MAP PAGE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestCognitiveMapPage:
    """Test CognitiveMapPage model."""

    async def test_create_cognitive_map_page(self, db_session):
        """Test creating a cognitive map page."""
        url = "https://example.com"
        page = CognitiveMapPage(
            url=url,
            url_hash=CognitiveMapPage.hash_url(url),
            title="Example Domain",
            domain="example.com",
            visited_count=1,
            importance_score=50.0,
            elements_snapshot={"title": "Example", "selectors": {}},
        )
        db_session.add(page)
        await db_session.commit()

        assert page.id is not None
        assert page.url_hash is not None
        assert page.visited_count == 1
        assert page.importance_score == 50.0

    async def test_url_hash_uniqueness(self, db_session):
        """Test that URL hash must be unique."""
        url = "https://example.com"
        url_hash = CognitiveMapPage.hash_url(url)

        page1 = CognitiveMapPage(url=url, url_hash=url_hash, domain="example.com")
        db_session.add(page1)
        await db_session.commit()

        # Try to create duplicate
        page2 = CognitiveMapPage(url=url, url_hash=url_hash, domain="example.com")
        db_session.add(page2)

        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()

    async def test_url_hash_generation(self):
        """Test hash_url() static method."""
        url1 = "https://example.com"
        url2 = "https://example.com"
        url3 = "https://different.com"

        hash1 = CognitiveMapPage.hash_url(url1)
        hash2 = CognitiveMapPage.hash_url(url2)
        hash3 = CognitiveMapPage.hash_url(url3)

        # Same URL = same hash
        assert hash1 == hash2

        # Different URL = different hash
        assert hash1 != hash3

        # Hash length (SHA256 = 64 hex chars)
        assert len(hash1) == 64

    async def test_cognitive_map_page_timestamps(self, db_session):
        """Test timestamp fields."""
        page = CognitiveMapPage(
            url="https://test.com",
            url_hash=CognitiveMapPage.hash_url("https://test.com"),
            domain="test.com",
        )
        db_session.add(page)
        await db_session.commit()

        assert page.first_visited is not None
        assert page.last_visited is not None
        assert page.created_at is not None
        assert page.updated_at is not None

    async def test_cognitive_map_page_to_dict(self, db_session):
        """Test to_dict() serialization."""
        page = CognitiveMapPage(
            url="https://example.com",
            url_hash=CognitiveMapPage.hash_url("https://example.com"),
            title="Example",
            domain="example.com",
            visited_count=5,
            importance_score=75.0,
        )
        db_session.add(page)
        await db_session.commit()

        data = page.to_dict()

        assert isinstance(data, dict)
        assert data["url"] == "https://example.com"
        assert data["title"] == "Example"
        assert data["visited_count"] == 5
        assert data["importance_score"] == 75.0


# ============================================================================
# NAVIGATION PATH TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestNavigationPath:
    """Test NavigationPath model."""

    async def test_create_navigation_path(self, db_session):
        """Test creating a navigation path."""
        from_hash = CognitiveMapPage.hash_url("https://example.com")
        to_hash = CognitiveMapPage.hash_url("https://test.com")

        path = NavigationPath(
            from_url_hash=from_hash,
            to_url_hash=to_hash,
            action_sequence=[
                {"action": "click", "selector": "a.link"},
                {"action": "wait", "duration_ms": 1000},
            ],
            success_count=5,
            failure_count=1,
            confidence_score=0.83,
            avg_duration_ms=2500,
        )
        db_session.add(path)
        await db_session.commit()

        assert path.id is not None
        assert path.success_count == 5
        assert path.failure_count == 1
        assert path.confidence_score == 0.83

    async def test_navigation_path_uniqueness(self, db_session):
        """Test unique constraint on from/to URL hashes."""
        from_hash = CognitiveMapPage.hash_url("https://example.com")
        to_hash = CognitiveMapPage.hash_url("https://test.com")

        path1 = NavigationPath(
            from_url_hash=from_hash,
            to_url_hash=to_hash,
            action_sequence=[],
        )
        db_session.add(path1)
        await db_session.commit()

        # Try to create duplicate path
        path2 = NavigationPath(
            from_url_hash=from_hash,
            to_url_hash=to_hash,
            action_sequence=[],
        )
        db_session.add(path2)

        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()

    async def test_navigation_path_to_dict(self, db_session):
        """Test to_dict() serialization."""
        from_hash = CognitiveMapPage.hash_url("https://example.com")
        to_hash = CognitiveMapPage.hash_url("https://test.com")

        path = NavigationPath(
            from_url_hash=from_hash,
            to_url_hash=to_hash,
            action_sequence=[{"action": "click"}],
            success_count=10,
            confidence_score=0.9,
        )
        db_session.add(path)
        await db_session.commit()

        data = path.to_dict()

        assert isinstance(data, dict)
        assert data["from_url_hash"] == from_hash
        assert data["to_url_hash"] == to_hash
        assert data["success_count"] == 10
        assert data["confidence_score"] == 0.9
        assert "action_sequence" in data
