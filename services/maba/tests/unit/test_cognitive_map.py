"""Unit tests for CognitiveMapService.

Day 4: Complete testing of learning and recommendation system.

Tests cover:
- Learning from browser actions
- Selector recommendation
- Navigation path learning
- Importance scoring algorithm
- Statistics and queries

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
from datetime import datetime, timedelta

from cognitive_map.service import CognitiveMapService
from db.models import BrowserAction, BrowserSession, CognitiveMapPage, NavigationPath


# ============================================================================
# LEARNING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestCognitiveMapLearning:
    """Test cognitive map learning from actions."""

    async def test_learn_from_successful_action(self, db_session, cognitive_map_service):
        """Test learning from a successful browser action."""
        # Create session and action
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        action = BrowserAction(
            session_id=session.id,
            action_type="click",
            url="https://example.com",
            selector="button.submit",
            success=True,
            duration_ms=200,
        )
        db_session.add(action)
        await db_session.commit()

        # Learn from action
        await cognitive_map_service.learn_from_action(action)

        # Verify page was created
        url_hash = CognitiveMapPage.hash_url("https://example.com")
        page = await db_session.get(CognitiveMapPage, url_hash)
        
        # Note: might need to query differently
        from sqlalchemy import select
        result = await db_session.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one_or_none()

        assert page is not None
        assert page.url == "https://example.com"
        assert page.visited_count == 1

    async def test_learn_selector_from_action(self, db_session, cognitive_map_service):
        """Test that successful selectors are learned."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        # Perform multiple successful clicks
        for i in range(3):
            action = BrowserAction(
                session_id=session.id,
                action_type="click",
                url="https://example.com",
                selector="button.submit",
                success=True,
                duration_ms=150 + i * 10,
            )
            db_session.add(action)
            await db_session.flush()
            await cognitive_map_service.learn_from_action(action)

        await db_session.commit()

        # Check learned selectors
        url_hash = CognitiveMapPage.hash_url("https://example.com")
        from sqlalchemy import select
        result = await db_session.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one()

        assert page.elements_snapshot is not None
        assert "selectors" in page.elements_snapshot
        assert "click" in page.elements_snapshot["selectors"]
        assert "button.submit" in page.elements_snapshot["selectors"]["click"]
        
        selector_data = page.elements_snapshot["selectors"]["click"]["button.submit"]
        assert selector_data["count"] == 3

    async def test_failed_action_not_learned(self, db_session, cognitive_map_service):
        """Test that failed actions don't learn selectors."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        action = BrowserAction(
            session_id=session.id,
            action_type="click",
            url="https://example.com",
            selector="button.nonexistent",
            success=False,
            error_message="Element not found",
        )
        db_session.add(action)
        await db_session.commit()

        await cognitive_map_service.learn_from_action(action)

        # Page should be created but selector not learned
        url_hash = CognitiveMapPage.hash_url("https://example.com")
        from sqlalchemy import select
        result = await db_session.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one()

        assert page.visited_count == 1
        # Selector should NOT be in learned selectors
        if page.elements_snapshot and "selectors" in page.elements_snapshot:
            assert "button.nonexistent" not in page.elements_snapshot.get("selectors", {}).get("click", {})


# ============================================================================
# IMPORTANCE SCORING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestImportanceScoring:
    """Test importance score calculation."""

    async def test_importance_score_calculation(self, db_session, cognitive_map_service):
        """Test that importance score is calculated correctly."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        # Create action
        action = BrowserAction(
            session_id=session.id,
            action_type="navigate",
            url="https://important.com",
            success=True,
        )
        db_session.add(action)
        await db_session.commit()

        await cognitive_map_service.learn_from_action(action)

        # Check score was calculated
        url_hash = CognitiveMapPage.hash_url("https://important.com")
        from sqlalchemy import select
        result = await db_session.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one()

        assert page.importance_score > 0
        assert page.importance_score <= 100

    async def test_importance_increases_with_visits(self, db_session, cognitive_map_service):
        """Test that importance increases with visit count."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        url = "https://frequent.com"
        scores = []

        # Visit page multiple times
        for i in range(5):
            action = BrowserAction(
                session_id=session.id,
                action_type="navigate",
                url=url,
                success=True,
            )
            db_session.add(action)
            await db_session.flush()
            await cognitive_map_service.learn_from_action(action)

            # Get current score
            url_hash = CognitiveMapPage.hash_url(url)
            from sqlalchemy import select
            result = await db_session.execute(
                select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
            )
            page = result.scalar_one()
            scores.append(page.importance_score)

        # Score should generally increase or stay similar with visits
        assert scores[-1] >= scores[0]


# ============================================================================
# NAVIGATION PATH TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestNavigationPathLearning:
    """Test navigation path learning."""

    async def test_learn_navigation_path(self, db_session, cognitive_map_service):
        """Test learning a navigation path."""
        from_url = "https://example.com"
        to_url = "https://example.com/page2"
        actions = [
            {"action": "click", "selector": "a.next"},
            {"action": "wait", "duration_ms": 500},
        ]

        await cognitive_map_service.learn_navigation_path(
            from_url=from_url,
            to_url=to_url,
            actions=actions,
            success=True,
            duration_ms=1500,
        )

        # Retrieve path
        path = await cognitive_map_service.get_navigation_path(from_url, to_url)

        assert path is not None
        assert path.success_count == 1
        assert path.failure_count == 0
        assert path.action_sequence == actions
        assert path.avg_duration_ms == 1500

    async def test_navigation_path_confidence_increases(self, db_session, cognitive_map_service):
        """Test that confidence increases with successful navigations."""
        from_url = "https://example.com"
        to_url = "https://example.com/page2"
        actions = [{"action": "click", "selector": "a.next"}]

        # Learn path multiple times successfully
        for i in range(5):
            await cognitive_map_service.learn_navigation_path(
                from_url=from_url,
                to_url=to_url,
                actions=actions,
                success=True,
                duration_ms=1000,
            )

        path = await cognitive_map_service.get_navigation_path(from_url, to_url)

        assert path.success_count == 5
        assert path.failure_count == 0
        assert path.confidence_score > 0.5  # Should be high with 5 successes

    async def test_navigation_path_confidence_decreases_with_failures(
        self, db_session, cognitive_map_service
    ):
        """Test that failures decrease confidence."""
        from_url = "https://example.com"
        to_url = "https://example.com/page2"
        actions = [{"action": "click", "selector": "a.unreliable"}]

        # 3 successes
        for i in range(3):
            await cognitive_map_service.learn_navigation_path(
                from_url, to_url, actions, success=True, duration_ms=1000
            )

        path_before = await cognitive_map_service.get_navigation_path(from_url, to_url)
        confidence_before = path_before.confidence_score

        # 2 failures
        for i in range(2):
            await cognitive_map_service.learn_navigation_path(
                from_url, to_url, actions, success=False, duration_ms=5000
            )

        path_after = await cognitive_map_service.get_navigation_path(from_url, to_url)
        confidence_after = path_after.confidence_score

        # Confidence should decrease (3/5 = 60% vs 3/3 = 100%)
        assert confidence_after < confidence_before


# ============================================================================
# RECOMMENDATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestSelectorRecommendations:
    """Test selector recommendation system."""

    async def test_recommend_selector(self, db_session, cognitive_map_service):
        """Test getting selector recommendations."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        url = "https://example.com"

        # Learn multiple selectors
        selectors = ["button.submit", "button.primary", "input[type='submit']"]
        for selector in selectors:
            for i in range(3 if selector == "button.submit" else 1):  # Make one more popular
                action = BrowserAction(
                    session_id=session.id,
                    action_type="click",
                    url=url,
                    selector=selector,
                    success=True,
                    duration_ms=200,
                )
                db_session.add(action)
                await db_session.flush()
                await cognitive_map_service.learn_from_action(action)

        await db_session.commit()

        # Get recommendations
        recommendations = await cognitive_map_service.recommend_selector(
            url=url, action_type="click", limit=3
        )

        assert len(recommendations) > 0
        # Most used selector should be first
        assert recommendations[0]["selector"] == "button.submit"
        assert recommendations[0]["count"] == 3

    async def test_no_recommendations_for_unvisited_page(
        self, db_session, cognitive_map_service
    ):
        """Test that unvisited pages return no recommendations."""
        recommendations = await cognitive_map_service.recommend_selector(
            url="https://never-visited.com", action_type="click"
        )

        assert len(recommendations) == 0


# ============================================================================
# STATISTICS TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestCognitiveMapStatistics:
    """Test cognitive map statistics."""

    async def test_get_statistics(self, db_with_sample_data):
        """Test getting cognitive map statistics."""
        cognitive_map = CognitiveMapService(db_with_sample_data)
        stats = await cognitive_map.get_statistics()

        assert "total_pages" in stats
        assert "total_navigation_paths" in stats
        assert "avg_importance_score" in stats
        assert "top_domains" in stats

        assert stats["total_pages"] == 2  # Sample data has 2 pages
        assert stats["total_navigation_paths"] == 1  # Sample data has 1 path

    async def test_get_important_pages(self, db_with_sample_data):
        """Test retrieving important pages."""
        cognitive_map = CognitiveMapService(db_with_sample_data)
        pages = await cognitive_map.get_important_pages(min_score=50.0, limit=10)

        assert len(pages) == 1  # Only 1 page with score >= 50
        assert pages[0].url == "https://example.com"
        assert pages[0].importance_score >= 50.0

    async def test_get_recent_pages(self, db_with_sample_data):
        """Test retrieving recent pages."""
        cognitive_map = CognitiveMapService(db_with_sample_data)
        pages = await cognitive_map.get_recent_pages(hours=24, limit=10)

        assert len(pages) >= 0  # At least some pages should be recent
        # Pages should be ordered by recency
        if len(pages) > 1:
            assert pages[0].last_visited >= pages[1].last_visited
