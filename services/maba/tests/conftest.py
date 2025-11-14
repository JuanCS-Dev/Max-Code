"""Pytest configuration and shared fixtures.

Day 4: Test infrastructure for MABA service.

Fixtures provided:
- Database: test_db, db_session
- Browser: mock_browser, browser_session
- Cognitive Map: cognitive_map_service
- API: test_client, authenticated_client
- Test Data: faker, sample_urls, sample_actions

Author: Vértice Platform Team
License: Proprietary
"""
import asyncio
import os
import sys
from datetime import datetime, timedelta
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import Base
from db.models import BrowserAction, BrowserSession, CognitiveMapPage, NavigationPath

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

# Use in-memory SQLite for tests (fast, isolated)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Faker instance for test data
fake = Faker()
Faker.seed(42)  # Deterministic test data


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Set test environment variables
    os.environ["ENV"] = "test"
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "WARNING"  # Reduce noise in tests

    # Disable external connections during tests
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["NEO4J_URI"] = "bolt://localhost:7687"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create test database engine with in-memory SQLite.

    Uses StaticPool to maintain single connection for in-memory database.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session.

    Automatically rolls back after each test for isolation.
    """
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def db_with_sample_data(db_session: AsyncSession) -> AsyncSession:
    """Database session pre-populated with sample data."""
    # Create sample browser sessions
    session1 = BrowserSession(
        status="active",
        browser_type="chromium",
        viewport_width=1920,
        viewport_height=1080,
    )
    session2 = BrowserSession(
        status="closed",
        browser_type="firefox",
        viewport_width=1280,
        viewport_height=720,
    )
    db_session.add_all([session1, session2])
    await db_session.flush()

    # Create sample cognitive map pages
    page1 = CognitiveMapPage(
        url="https://example.com",
        url_hash=CognitiveMapPage.hash_url("https://example.com"),
        title="Example Domain",
        domain="example.com",
        visited_count=5,
        importance_score=75.0,
        elements_snapshot={"title": "Example Domain", "selectors": {}},
    )
    page2 = CognitiveMapPage(
        url="https://test.com",
        url_hash=CognitiveMapPage.hash_url("https://test.com"),
        title="Test Site",
        domain="test.com",
        visited_count=2,
        importance_score=40.0,
    )
    db_session.add_all([page1, page2])
    await db_session.flush()

    # Create sample browser actions
    action1 = BrowserAction(
        session_id=session1.id,
        action_type="navigate",
        url="https://example.com",
        success=True,
        duration_ms=1500,
    )
    action2 = BrowserAction(
        session_id=session1.id,
        action_type="click",
        url="https://example.com",
        selector="button.submit",
        success=True,
        duration_ms=250,
    )
    db_session.add_all([action1, action2])

    # Create sample navigation path
    nav_path = NavigationPath(
        from_url_hash=CognitiveMapPage.hash_url("https://example.com"),
        to_url_hash=CognitiveMapPage.hash_url("https://test.com"),
        action_sequence=[
            {"action": "click", "selector": "a.link"},
            {"action": "wait", "duration_ms": 1000},
        ],
        success_count=3,
        failure_count=1,
        confidence_score=0.75,
    )
    db_session.add(nav_path)

    await db_session.commit()
    return db_session


# ============================================================================
# BROWSER CONTROLLER FIXTURES
# ============================================================================

@pytest.fixture
def mock_playwright():
    """Mock Playwright instance."""
    mock = AsyncMock()
    mock.chromium.launch = AsyncMock(return_value=AsyncMock())
    mock.firefox.launch = AsyncMock(return_value=AsyncMock())
    mock.webkit.launch = AsyncMock(return_value=AsyncMock())
    return mock


@pytest.fixture
def mock_browser():
    """Mock browser instance with typical methods."""
    browser = AsyncMock()

    # Mock context
    context = AsyncMock()
    page = AsyncMock()

    # Setup page methods
    page.goto = AsyncMock()
    page.click = AsyncMock()
    page.fill = AsyncMock()
    page.type = AsyncMock()
    page.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
    page.evaluate = AsyncMock(return_value={"title": "Test Page"})
    page.query_selector = AsyncMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Test Page")

    context.new_page = AsyncMock(return_value=page)
    context.close = AsyncMock()

    browser.new_context = AsyncMock(return_value=context)
    browser.close = AsyncMock()

    return browser


@pytest.fixture
def mock_browser_controller(mock_browser, db_session):
    """Mock BrowserController with pre-configured behavior."""
    from browser.controller import BrowserController

    controller = BrowserController()
    controller.playwright = AsyncMock()
    controller.browsers = {"chromium": mock_browser}
    controller._running = True
    controller.db_session = db_session

    return controller


# ============================================================================
# COGNITIVE MAP FIXTURES
# ============================================================================

@pytest.fixture
def cognitive_map_service(db_session):
    """Create CognitiveMapService instance with test database."""
    from cognitive_map.service import CognitiveMapService
    return CognitiveMapService(db_session)


# ============================================================================
# API CLIENT FIXTURES
# ============================================================================

@pytest.fixture
def test_app():
    """Create FastAPI test application."""
    from main import app
    return app


@pytest.fixture
def test_client(test_app):
    """Create synchronous test client."""
    return TestClient(test_app)


@pytest.fixture
async def async_client(test_app):
    """Create async test client for async endpoints."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


@pytest.fixture
def auth_token():
    """Generate test JWT token."""
    import jwt
    from datetime import datetime, timedelta

    payload = {
        "sub": "test_user",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }

    # Use test secret
    secret = os.getenv("JWT_SECRET", "test_secret_key")
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


@pytest.fixture
def auth_headers(auth_token):
    """HTTP headers with authentication token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
async def authenticated_client(async_client, auth_headers):
    """Async client with authentication headers."""
    async_client.headers.update(auth_headers)
    return async_client


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_urls():
    """Generate sample URLs for testing."""
    return [
        "https://example.com",
        "https://test.com",
        "https://demo.org",
        "https://sample.io",
        "https://localhost:3000",
    ]


@pytest.fixture
def sample_selectors():
    """Common CSS selectors for testing."""
    return {
        "button": "button.submit",
        "input": "input[type='text']",
        "link": "a.nav-link",
        "form": "form#main-form",
        "div": "div.container",
    }


@pytest.fixture
def sample_browser_session():
    """Sample browser session data."""
    return {
        "viewport_width": 1920,
        "viewport_height": 1080,
        "user_agent": "Mozilla/5.0 Test Agent",
        "browser_type": "chromium",
    }


@pytest.fixture
def sample_navigation_request():
    """Sample navigation request data."""
    return {
        "url": "https://example.com",
        "wait_until": "networkidle",
        "timeout_ms": 30000,
    }


@pytest.fixture
def sample_click_request():
    """Sample click request data."""
    return {
        "selector": "button.submit",
        "timeout_ms": 5000,
    }


@pytest.fixture
def sample_type_request():
    """Sample type request data."""
    return {
        "selector": "input[name='username']",
        "text": "test_user",
        "delay_ms": 50,
    }


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def faker_instance():
    """Faker instance for generating test data."""
    return fake


@pytest.fixture
def freezer(monkeypatch):
    """Freeze time for consistent testing."""
    frozen_time = datetime(2025, 11, 14, 12, 0, 0)

    class FrozenDateTime:
        @classmethod
        def utcnow(cls):
            return frozen_time

        @classmethod
        def now(cls, tz=None):
            return frozen_time

    monkeypatch.setattr("datetime.datetime", FrozenDateTime)
    return frozen_time


@pytest.fixture
async def cleanup():
    """Cleanup helper for async resources."""
    resources = []

    def register(resource):
        resources.append(resource)

    yield register

    # Cleanup all registered resources
    for resource in resources:
        if hasattr(resource, "close"):
            if asyncio.iscoroutinefunction(resource.close):
                await resource.close()
            else:
                resource.close()


# ============================================================================
# PERFORMANCE FIXTURES
# ============================================================================

@pytest.fixture
def benchmark_config():
    """Configuration for performance benchmarks."""
    return {
        "iterations": 100,
        "warmup": 10,
        "max_time": 5.0,  # seconds
        "min_rounds": 5,
    }


@pytest.fixture
def performance_thresholds():
    """Performance thresholds for different operations."""
    return {
        "db_query": 0.1,  # 100ms
        "browser_navigate": 5.0,  # 5 seconds
        "browser_click": 1.0,  # 1 second
        "cognitive_map_learn": 0.5,  # 500ms
        "api_request": 0.2,  # 200ms
    }
