"""Unit tests for PENELOPE PageAnalyzer.

Day 5 Audit: Comprehensive tests for analyzer validation and functionality.

Author: Vértice Platform Team
License: Proprietary
"""
import base64
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from penelope_integration.analyzer import PageAnalyzer, _safe_truncate_html


class TestSafeTruncateHtml:
    """Test HTML truncation helper."""

    def test_no_truncation_needed(self):
        """Test that short HTML is not truncated."""
        html = "<div>Hello</div>"
        result = _safe_truncate_html(html, 1000)
        assert result == html

    def test_truncates_at_tag_boundary(self):
        """Test that HTML is truncated at tag boundary."""
        html = "<div>Hello</div><p>World</p><span>Test</span>"
        result = _safe_truncate_html(html, 25)
        # Should truncate after </div> or </p>
        assert result.endswith(">")
        assert "<" not in result[-10:-1]  # No opening tags at end

    def test_handles_no_tags(self):
        """Test truncation with plain text."""
        text = "A" * 1000
        result = _safe_truncate_html(text, 100)
        assert len(result) <= 100


class TestPageAnalyzerInit:
    """Test PageAnalyzer initialization."""

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        analyzer = PageAnalyzer(api_key="test-key")
        assert analyzer.api_key == "test-key"
        assert analyzer.client is not None

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict("os.environ", {}, clear=True):
            analyzer = PageAnalyzer()
            assert analyzer.api_key is None
            assert analyzer.client is None

    def test_init_with_env_api_key(self):
        """Test initialization with environment variable."""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "env-key"}):
            analyzer = PageAnalyzer()
            assert analyzer.api_key == "env-key"


class TestPageAnalyzerValidation:
    """Test input validation for PageAnalyzer methods."""

    @pytest.fixture
    def mock_analyzer(self):
        """Create analyzer with mocked client."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()
        return analyzer

    @pytest.mark.asyncio
    async def test_analyze_screenshot_requires_screenshot(self, mock_analyzer):
        """Test that analyze_screenshot validates screenshot."""
        with pytest.raises(ValueError, match="Screenshot is required"):
            await mock_analyzer.analyze_screenshot(
                screenshot_b64="",
                url="https://test.com"
            )

    @pytest.mark.asyncio
    async def test_analyze_screenshot_requires_url(self, mock_analyzer):
        """Test that analyze_screenshot validates URL."""
        with pytest.raises(ValueError, match="URL is required"):
            await mock_analyzer.analyze_screenshot(
                screenshot_b64="base64data",
                url=""
            )

    @pytest.mark.asyncio
    async def test_analyze_screenshot_requires_client(self):
        """Test that analyze_screenshot requires API client."""
        analyzer = PageAnalyzer()  # No API key
        with pytest.raises(ValueError, match="Anthropic API key not configured"):
            await analyzer.analyze_screenshot(
                screenshot_b64="base64data",
                url="https://test.com"
            )

    @pytest.mark.asyncio
    async def test_analyze_html_structure_requires_html(self, mock_analyzer):
        """Test that analyze_html_structure validates HTML."""
        with pytest.raises(ValueError, match="HTML content is required"):
            await mock_analyzer.analyze_html_structure(
                html="",
                url="https://test.com"
            )

    @pytest.mark.asyncio
    async def test_suggest_selectors_requires_html(self, mock_analyzer):
        """Test that suggest_selectors validates HTML."""
        with pytest.raises(ValueError, match="HTML content is required"):
            await mock_analyzer.suggest_selectors(
                html="",
                element_description="button"
            )

    @pytest.mark.asyncio
    async def test_suggest_selectors_requires_description(self, mock_analyzer):
        """Test that suggest_selectors validates element description."""
        with pytest.raises(ValueError, match="Element description is required"):
            await mock_analyzer.suggest_selectors(
                html="<div>Test</div>",
                element_description=""
            )

    @pytest.mark.asyncio
    async def test_extract_with_llm_requires_html(self, mock_analyzer):
        """Test that extract_with_llm validates HTML."""
        with pytest.raises(ValueError, match="HTML content is required"):
            await mock_analyzer.extract_with_llm(
                html="",
                schema={"title": "Page title"}
            )

    @pytest.mark.asyncio
    async def test_extract_with_llm_requires_schema(self, mock_analyzer):
        """Test that extract_with_llm validates schema."""
        with pytest.raises(ValueError, match="Valid schema dictionary is required"):
            await mock_analyzer.extract_with_llm(
                html="<div>Test</div>",
                schema=None
            )


class TestPageAnalyzerFunctionality:
    """Test PageAnalyzer core functionality."""

    @pytest.fixture
    def mock_analyzer(self):
        """Create analyzer with mocked client."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()
        return analyzer

    @pytest.mark.asyncio
    async def test_analyze_screenshot_success(self, mock_analyzer):
        """Test successful screenshot analysis."""
        # Mock Claude response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is a login page with email and password fields.")]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        result = await mock_analyzer.analyze_screenshot(
            screenshot_b64="base64encodedimage",
            url="https://example.com/login"
        )

        assert "analysis" in result
        assert result["model"] == "claude-sonnet-4-5"
        assert result["url"] == "https://example.com/login"
        assert result["confidence"] == 0.9

    @pytest.mark.asyncio
    async def test_suggest_selectors_success(self, mock_analyzer):
        """Test successful selector suggestions."""
        # Mock Claude response with selectors
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="button.submit\nbutton[type='submit']\n#submit-btn")]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        result = await mock_analyzer.suggest_selectors(
            html="<button class='submit' type='submit' id='submit-btn'>Submit</button>",
            element_description="submit button"
        )

        assert isinstance(result, list)
        assert len(result) == 3
        assert "button.submit" in result
        assert "button[type='submit']" in result
        assert "#submit-btn" in result

    @pytest.mark.asyncio
    async def test_suggest_selectors_filters_comments_not_id_selectors(self, mock_analyzer):
        """Test that CSS ID selectors are NOT filtered out (bug fix)."""
        # Mock Claude response with both comments and CSS ID selectors
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="""# This is a comment
#login-btn
#user-id
# Another comment
button.login""")]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        result = await mock_analyzer.suggest_selectors(
            html="<button id='login-btn'>Login</button>",
            element_description="login button"
        )

        # Should include CSS ID selectors but not comment lines
        assert "#login-btn" in result
        assert "#user-id" in result
        assert "button.login" in result
        # Comments should be filtered
        assert "# This is a comment" not in result
        assert "# Another comment" not in result

    @pytest.mark.asyncio
    async def test_extract_with_llm_direct_json(self, mock_analyzer):
        """Test LLM extraction with direct JSON response."""
        # Mock Claude response with JSON
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"title": "Test Product", "price": "$99.99"}')]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        result = await mock_analyzer.extract_with_llm(
            html="<h1>Test Product</h1><span class='price'>$99.99</span>",
            schema={"title": "Product title", "price": "Product price"}
        )

        assert result == {"title": "Test Product", "price": "$99.99"}

    @pytest.mark.asyncio
    async def test_extract_with_llm_json_in_markdown(self, mock_analyzer):
        """Test LLM extraction with JSON in markdown code block."""
        # Mock Claude response with JSON in code block
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='```json\n{"title": "Test", "price": "$50"}\n```')]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        result = await mock_analyzer.extract_with_llm(
            html="<h1>Test</h1>",
            schema={"title": "Title", "price": "Price"}
        )

        assert result == {"title": "Test", "price": "$50"}

    @pytest.mark.asyncio
    async def test_extract_with_llm_json_embedded(self, mock_analyzer):
        """Test LLM extraction with JSON embedded in text."""
        # Mock Claude response with JSON embedded
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='Here is the data: {"title": "Item", "price": "$10"} as requested.')]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        result = await mock_analyzer.extract_with_llm(
            html="<div>Item - $10</div>",
            schema={"title": "Title", "price": "Price"}
        )

        assert result == {"title": "Item", "price": "$10"}

    @pytest.mark.asyncio
    async def test_extract_with_llm_no_json_raises(self, mock_analyzer):
        """Test LLM extraction fails when no JSON found."""
        # Mock Claude response without JSON
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="No JSON here, just text")]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        with pytest.raises(ValueError, match="Could not parse JSON"):
            await mock_analyzer.extract_with_llm(
                html="<div>Test</div>",
                schema={"title": "Title"}
            )

    @pytest.mark.asyncio
    async def test_close_closes_client(self, mock_analyzer):
        """Test that close() closes the client."""
        await mock_analyzer.close()
        mock_analyzer.client.close.assert_called_once()


class TestPageAnalyzerHtmlTruncation:
    """Test HTML truncation in analyzer methods."""

    @pytest.fixture
    def mock_analyzer(self):
        """Create analyzer with mocked client."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="analysis")]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)
        return analyzer

    @pytest.mark.asyncio
    async def test_analyze_html_structure_truncates_safely(self, mock_analyzer):
        """Test HTML structure analysis truncates at tag boundary."""
        # Create HTML longer than 50000 chars
        large_html = "<div>" + "x" * 60000 + "</div>"

        await mock_analyzer.analyze_html_structure(
            html=large_html,
            url="https://test.com"
        )

        # Check that the call was made
        assert mock_analyzer.client.messages.create.called
        call_args = mock_analyzer.client.messages.create.call_args
        prompt = call_args[1]["messages"][0]["content"]

        # Truncated HTML should be in the prompt and should end with >
        assert len(prompt) < len(large_html)

    @pytest.mark.asyncio
    async def test_suggest_selectors_truncates_safely(self, mock_analyzer):
        """Test selector suggestion truncates HTML safely."""
        large_html = "<button>" + "x" * 40000 + "</button>"

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="button")]
        mock_analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        await mock_analyzer.suggest_selectors(
            html=large_html,
            element_description="button"
        )

        assert mock_analyzer.client.messages.create.called
