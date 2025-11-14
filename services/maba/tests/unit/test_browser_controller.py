"""Unit tests for BrowserController.

Day 4: Testing browser automation with mocked Playwright.

Tests use mocked browsers to avoid needing real Playwright installation.

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import uuid

from browser.controller import (
    BrowserController,
    SessionNotFoundError,
    SessionLimitError,
)


@pytest.mark.unit
@pytest.mark.browser
class TestBrowserControllerInitialization:
    """Test BrowserController initialization."""

    async def test_initialize(self, mock_playwright):
        """Test controller initialization."""
        controller = BrowserController()

        with patch("browser.controller.async_playwright") as mock_async_pw:
            mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)
            
            await controller.initialize()

            assert controller.playwright is not None
            assert controller._running is True

    async def test_shutdown(self, mock_browser_controller):
        """Test controller shutdown."""
        await mock_browser_controller.shutdown()

        assert mock_browser_controller._running is False


@pytest.mark.unit
@pytest.mark.browser
class TestBrowserSessions:
    """Test browser session management."""

    async def test_create_session(self, mock_browser_controller):
        """Test creating a browser session."""
        result = await mock_browser_controller.create_session(
            browser_type="chromium",
            viewport_width=1920,
            viewport_height=1080,
        )

        assert "session_id" in result
        assert "status" in result
        assert result["status"] == "created"

    async def test_session_limit(self, mock_browser_controller):
        """Test session limit enforcement."""
        mock_browser_controller.max_sessions = 2

        # Create max sessions
        await mock_browser_controller.create_session()
        await mock_browser_controller.create_session()

        # Should raise when exceeding limit
        with pytest.raises(SessionLimitError):
            await mock_browser_controller.create_session()

    async def test_close_session(self, mock_browser_controller):
        """Test closing a session."""
        result = await mock_browser_controller.create_session()
        session_id = result["session_id"]

        close_result = await mock_browser_controller.close_session(session_id)

        assert close_result["status"] == "closed"

    async def test_close_nonexistent_session(self, mock_browser_controller):
        """Test closing a session that doesn't exist."""
        fake_id = str(uuid.uuid4())

        with pytest.raises(SessionNotFoundError):
            await mock_browser_controller.close_session(fake_id)


@pytest.mark.unit
@pytest.mark.browser
class TestBrowserActions:
    """Test browser actions."""

    async def test_navigate(self, mock_browser_controller):
        """Test navigation action."""
        session = await mock_browser_controller.create_session()
        session_id = session["session_id"]

        result = await mock_browser_controller.navigate(
            session_id=session_id,
            url="https://example.com",
            wait_until="networkidle",
        )

        assert result["status"] == "success"
        assert result["url"] == "https://example.com"

    async def test_click(self, mock_browser_controller):
        """Test click action."""
        session = await mock_browser_controller.create_session()
        session_id = session["session_id"]

        result = await mock_browser_controller.click(
            session_id=session_id,
            selector="button.submit",
        )

        assert result["status"] == "success"

    async def test_type_text(self, mock_browser_controller):
        """Test typing text."""
        session = await mock_browser_controller.create_session()
        session_id = session["session_id"]

        result = await mock_browser_controller.type_text(
            session_id=session_id,
            selector="input[name='username']",
            text="test_user",
        )

        assert result["status"] == "success"

    async def test_screenshot(self, mock_browser_controller):
        """Test screenshot capture."""
        session = await mock_browser_controller.create_session()
        session_id = session["session_id"]

        result = await mock_browser_controller.screenshot(
            session_id=session_id,
            full_page=False,
        )

        assert result["status"] == "success"
        assert "screenshot" in result

    async def test_extract_data(self, mock_browser_controller):
        """Test data extraction."""
        session = await mock_browser_controller.create_session()
        session_id = session["session_id"]

        result = await mock_browser_controller.extract_data(
            session_id=session_id,
            selectors={"title": "h1", "content": "p"},
        )

        assert result["status"] == "success"


@pytest.mark.unit
@pytest.mark.browser
class TestBrowserHealth:
    """Test browser health checks."""

    async def test_health_check(self, mock_browser_controller):
        """Test health check returns status."""
        health = await mock_browser_controller.health_check()

        assert "status" in health
        assert "active_sessions" in health
        assert isinstance(health["active_sessions"], int)
