"""Unit tests for PENELOPE Client.

Day 5 Audit: Comprehensive tests for client validation and functionality.

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from penelope_integration.client import PenelopeClient


class TestPenelopeClientInit:
    """Test PenelopeClient initialization."""

    def test_init_with_url(self):
        """Test initialization with custom URL."""
        client = PenelopeClient(penelope_url="http://custom:8000")
        assert client.penelope_url == "http://custom:8000"

    def test_init_with_default_url(self):
        """Test initialization with default URL."""
        with patch.dict("os.environ", {}, clear=True):
            client = PenelopeClient()
            assert "vertice-penelope-service" in client.penelope_url

    def test_init_with_env_url(self):
        """Test initialization with environment variable URL."""
        with patch.dict("os.environ", {"PENELOPE_URL": "http://env:9000"}):
            client = PenelopeClient()
            assert client.penelope_url == "http://env:9000"

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = PenelopeClient(api_key="test-key")
        assert client.api_key == "test-key"

    def test_init_sets_auth_header(self):
        """Test that API key sets Authorization header."""
        client = PenelopeClient(api_key="test-key")
        # Client should have Authorization header
        assert "Authorization" in client.client.headers
        assert client.client.headers["Authorization"] == "Bearer test-key"


class TestPenelopeClientValidation:
    """Test input validation for PenelopeClient methods."""

    @pytest.fixture
    def mock_client(self):
        """Create client with mocked HTTP client."""
        client = PenelopeClient()
        client.client = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_suggest_action_requires_url(self, mock_client):
        """Test that suggest_action validates current_url."""
        with pytest.raises(ValueError, match="current_url is required"):
            await mock_client.suggest_action(
                current_url="",
                goal="test goal"
            )

    @pytest.mark.asyncio
    async def test_suggest_action_requires_goal(self, mock_client):
        """Test that suggest_action validates goal."""
        with pytest.raises(ValueError, match="goal is required"):
            await mock_client.suggest_action(
                current_url="https://test.com",
                goal=""
            )

    @pytest.mark.asyncio
    async def test_auto_heal_requires_failed_action(self, mock_client):
        """Test that auto_heal validates failed_action."""
        with pytest.raises(ValueError, match="failed_action must be a dictionary"):
            await mock_client.auto_heal(
                failed_action=None,
                error_message="error"
            )

    @pytest.mark.asyncio
    async def test_auto_heal_requires_dict_failed_action(self, mock_client):
        """Test that auto_heal requires dict for failed_action."""
        with pytest.raises(ValueError, match="failed_action must be a dictionary"):
            await mock_client.auto_heal(
                failed_action="not a dict",
                error_message="error"
            )

    @pytest.mark.asyncio
    async def test_auto_heal_requires_error_message(self, mock_client):
        """Test that auto_heal validates error_message."""
        with pytest.raises(ValueError, match="error_message is required"):
            await mock_client.auto_heal(
                failed_action={"action": "click"},
                error_message=""
            )

    @pytest.mark.asyncio
    async def test_extract_structured_data_requires_html(self, mock_client):
        """Test that extract_structured_data validates html."""
        with pytest.raises(ValueError, match="html is required"):
            await mock_client.extract_structured_data(
                html="",
                url="https://test.com",
                schema={"title": "Title"}
            )

    @pytest.mark.asyncio
    async def test_extract_structured_data_requires_url(self, mock_client):
        """Test that extract_structured_data validates url."""
        with pytest.raises(ValueError, match="url is required"):
            await mock_client.extract_structured_data(
                html="<div>Test</div>",
                url="",
                schema={"title": "Title"}
            )

    @pytest.mark.asyncio
    async def test_extract_structured_data_requires_schema(self, mock_client):
        """Test that extract_structured_data validates schema."""
        with pytest.raises(ValueError, match="schema must be a dictionary"):
            await mock_client.extract_structured_data(
                html="<div>Test</div>",
                url="https://test.com",
                schema=None
            )


class TestPenelopeClientFunctionality:
    """Test PenelopeClient core functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create client with mocked HTTP client."""
        client = PenelopeClient()
        client.client = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_analyze_page_success(self, mock_client):
        """Test successful page analysis."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "analysis": "Login page detected",
            "confidence": 0.95
        }
        mock_client.client.post = AsyncMock(return_value=mock_response)

        result = await mock_client.analyze_page(
            html="<form><input name='email'></form>",
            url="https://example.com/login",
            analysis_type="form"
        )

        assert result["analysis"] == "Login page detected"
        assert result["confidence"] == 0.95
        mock_client.client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_suggest_action_success(self, mock_client):
        """Test successful action suggestion."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "action": "click",
            "selector": "button.login",
            "reasoning": "Login button found",
            "confidence": 0.9
        }
        mock_client.client.post = AsyncMock(return_value=mock_response)

        result = await mock_client.suggest_action(
            current_url="https://example.com",
            goal="login to account",
            page_html="<button class='login'>Login</button>"
        )

        assert result["action"] == "click"
        assert result["selector"] == "button.login"
        assert result["confidence"] == 0.9

    @pytest.mark.asyncio
    async def test_auto_heal_success(self, mock_client):
        """Test successful auto-healing."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "healed": True,
            "alternative_action": {
                "action": "click",
                "selector": "button[type='submit']",
                "reasoning": "Alternative selector found"
            },
            "confidence": 0.85
        }
        mock_client.client.post = AsyncMock(return_value=mock_response)

        result = await mock_client.auto_heal(
            failed_action={"action": "click", "selector": "button.missing"},
            error_message="Element not found",
            page_html="<button type='submit'>Submit</button>"
        )

        assert result["healed"] is True
        assert result["alternative_action"]["selector"] == "button[type='submit']"

    @pytest.mark.asyncio
    async def test_auto_heal_failed(self, mock_client):
        """Test auto-healing when healing fails."""
        # Mock HTTP response indicating healing failed
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "healed": False,
            "reason": "No alternative found"
        }
        mock_client.client.post = AsyncMock(return_value=mock_response)

        result = await mock_client.auto_heal(
            failed_action={"action": "click", "selector": "button.missing"},
            error_message="Element not found"
        )

        assert result["healed"] is False

    @pytest.mark.asyncio
    async def test_extract_structured_data_success(self, mock_client):
        """Test successful structured data extraction."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "title": "Product Name",
            "price": "$99.99",
            "availability": "In stock"
        }
        mock_client.client.post = AsyncMock(return_value=mock_response)

        result = await mock_client.extract_structured_data(
            html="<h1>Product Name</h1><span>$99.99</span>",
            url="https://example.com/product",
            schema={
                "title": "Product title",
                "price": "Product price",
                "availability": "Stock status"
            }
        )

        assert result["title"] == "Product Name"
        assert result["price"] == "$99.99"

    @pytest.mark.asyncio
    async def test_health_check_success(self, mock_client):
        """Test successful health check."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "healthy",
            "version": "1.0.0"
        }
        mock_client.client.get = AsyncMock(return_value=mock_response)

        result = await mock_client.health_check()

        assert result["status"] == "healthy"
        mock_client.client.get.assert_called_once_with("/health")

    @pytest.mark.asyncio
    async def test_http_error_handling(self, mock_client):
        """Test that HTTP errors are propagated."""
        # Mock HTTP error
        mock_client.client.post = AsyncMock(
            side_effect=httpx.HTTPError("Connection failed")
        )

        with pytest.raises(httpx.HTTPError):
            await mock_client.suggest_action(
                current_url="https://test.com",
                goal="test"
            )

    @pytest.mark.asyncio
    async def test_close_closes_client(self, mock_client):
        """Test that close() closes the HTTP client."""
        await mock_client.close()
        mock_client.client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager usage."""
        async with PenelopeClient() as client:
            assert client is not None

        # Client should be closed after context


class TestPenelopeClientPayloads:
    """Test that correct payloads are sent to PENELOPE service."""

    @pytest.fixture
    def mock_client(self):
        """Create client with mocked HTTP client."""
        client = PenelopeClient()
        client.client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        client.client.post = AsyncMock(return_value=mock_response)
        return client

    @pytest.mark.asyncio
    async def test_suggest_action_payload(self, mock_client):
        """Test suggest_action sends correct payload."""
        await mock_client.suggest_action(
            current_url="https://test.com",
            goal="test goal",
            page_html="<div>Test</div>",
            screenshot="screenshot_data",
            previous_actions=[{"action": "navigate"}]
        )

        # Check payload
        call_args = mock_client.client.post.call_args
        payload = call_args[1]["json"]

        assert payload["current_url"] == "https://test.com"
        assert payload["goal"] == "test goal"
        assert payload["page_html"] == "<div>Test</div>"
        assert payload["screenshot"] == "screenshot_data"
        assert len(payload["previous_actions"]) == 1

    @pytest.mark.asyncio
    async def test_auto_heal_payload(self, mock_client):
        """Test auto_heal sends correct payload."""
        failed_action = {"action": "click", "selector": "button"}

        await mock_client.auto_heal(
            failed_action=failed_action,
            error_message="Element not found",
            page_html="<div>Test</div>",
            screenshot="screenshot"
        )

        # Check payload
        call_args = mock_client.client.post.call_args
        payload = call_args[1]["json"]

        assert payload["failed_action"] == failed_action
        assert payload["error_message"] == "Element not found"
        assert payload["page_html"] == "<div>Test</div>"
