"""Unit tests for PENELOPE AutoHealer.

Day 5 Audit: Comprehensive tests for auto-healing validation and functionality.

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from penelope_integration.auto_healing import AutoHealer
from penelope_integration.analyzer import PageAnalyzer
from penelope_integration.client import PenelopeClient


class TestAutoHealerInit:
    """Test AutoHealer initialization."""

    def test_init_with_components(self):
        """Test initialization with provided components."""
        analyzer = MagicMock()
        penelope_client = MagicMock()

        healer = AutoHealer(
            analyzer=analyzer,
            penelope_client=penelope_client,
            max_heal_attempts=5
        )

        assert healer.analyzer == analyzer
        assert healer.penelope_client == penelope_client
        assert healer.max_heal_attempts == 5

    def test_init_creates_default_analyzer(self):
        """Test that default analyzer is created if not provided."""
        with patch("penelope_integration.auto_healing.PageAnalyzer") as MockAnalyzer:
            healer = AutoHealer(api_key="test-key")

            # Should create PageAnalyzer with api_key
            MockAnalyzer.assert_called_once_with(api_key="test-key")

    def test_init_with_max_history_size(self):
        """Test initialization with custom history size."""
        healer = AutoHealer(max_history_size=50)
        assert healer.max_history_size == 50

    def test_init_default_history_size(self):
        """Test default history size."""
        healer = AutoHealer()
        assert healer.max_history_size == 100


class TestAutoHealerMemoryManagement:
    """Test AutoHealer memory leak prevention."""

    @pytest.fixture
    def mock_healer(self):
        """Create healer with mocked components."""
        analyzer = AsyncMock()
        analyzer.suggest_selectors = AsyncMock(return_value=["button.alt"])

        healer = AutoHealer(
            analyzer=analyzer,
            max_history_size=5  # Small size for testing
        )
        return healer

    @pytest.mark.asyncio
    async def test_healing_history_trimmed(self, mock_healer):
        """Test that healing history is trimmed when exceeding max size."""
        # Add more entries than max_history_size
        for i in range(10):
            await mock_healer.heal_failed_action(
                failed_action={"action": "click", "selector": f"button{i}"},
                error_message="Element not found",
                page_html="<div>Test</div>"
            )

        # History should be trimmed to max_history_size
        assert len(mock_healer.healing_history) <= mock_healer.max_history_size

    @pytest.mark.asyncio
    async def test_healing_history_keeps_recent(self, mock_healer):
        """Test that most recent entries are kept when trimming."""
        # Add 10 entries
        for i in range(10):
            await mock_healer.heal_failed_action(
                failed_action={"action": "click", "selector": f"button{i}"},
                error_message="Element not found",
                page_html="<div>Test</div>"
            )

        # The most recent entries should be kept
        # Last entry should be button9
        last_entry = mock_healer.healing_history[-1]
        assert "button9" in str(last_entry["failed_action"])


class TestAutoHealerMaxAttempts:
    """Test AutoHealer max attempts enforcement."""

    @pytest.fixture
    def mock_healer(self):
        """Create healer with mocked components."""
        analyzer = AsyncMock()
        healer = AutoHealer(analyzer=analyzer, max_heal_attempts=3)
        return healer

    @pytest.mark.asyncio
    async def test_max_attempts_enforced(self, mock_healer):
        """Test that healing stops after max attempts."""
        result = await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element not found",
            page_html="<div>Test</div>",
            attempt=4  # Exceeds max_heal_attempts
        )

        # Should return None when max attempts exceeded
        assert result is None

    @pytest.mark.asyncio
    async def test_within_max_attempts(self, mock_healer):
        """Test that healing proceeds within max attempts."""
        mock_healer.analyzer.suggest_selectors = AsyncMock(return_value=["button.alt"])

        result = await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element not found",
            page_html="<div>Test</div>",
            attempt=2  # Within max_heal_attempts
        )

        # Should return a healed action
        assert result is not None


class TestAutoHealerStrategies:
    """Test AutoHealer healing strategies."""

    @pytest.fixture
    def mock_healer(self):
        """Create healer with mocked components."""
        analyzer = AsyncMock()
        analyzer.suggest_selectors = AsyncMock(return_value=["button.alternative"])

        healer = AutoHealer(analyzer=analyzer)
        return healer

    @pytest.mark.asyncio
    async def test_element_not_found_strategy(self, mock_healer):
        """Test healing strategy for element not found errors."""
        result = await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button.missing"},
            error_message="Element not found",
            page_html="<button class='alternative'>Click</button>"
        )

        assert result is not None
        assert result["action"] == "click"
        assert result["selector"] == "button.alternative"
        assert result["healing_strategy"] == "alternative_selector"

    @pytest.mark.asyncio
    async def test_element_not_clickable_strategy(self, mock_healer):
        """Test healing strategy for element not clickable errors."""
        result = await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element is not clickable",
            page_html="<button>Click</button>"
        )

        assert result is not None
        assert result["action"] == "wait"
        assert result["healing_strategy"] == "wait_before_action"
        assert "then_retry" in result

    @pytest.mark.asyncio
    async def test_element_not_visible_strategy(self, mock_healer):
        """Test healing strategy for element not visible errors."""
        result = await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element not visible",
            page_html="<button>Click</button>"
        )

        assert result is not None
        assert result["action"] == "scroll"
        assert result["healing_strategy"] == "scroll_to_element"
        assert "then_retry" in result

    @pytest.mark.asyncio
    async def test_timeout_error_strategy(self, mock_healer):
        """Test healing strategy for timeout errors."""
        result = await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Timeout waiting for element",
            page_html="<button>Click</button>"
        )

        # Timeout should use alternative selector strategy
        assert result is not None
        assert result["healing_strategy"] == "alternative_selector"


class TestAutoHealerPenelopeIntegration:
    """Test AutoHealer integration with PENELOPE service."""

    @pytest.fixture
    def mock_healer_with_penelope(self):
        """Create healer with mocked PENELOPE client."""
        analyzer = AsyncMock()
        penelope_client = AsyncMock()

        healer = AutoHealer(
            analyzer=analyzer,
            penelope_client=penelope_client
        )
        return healer

    @pytest.mark.asyncio
    async def test_uses_penelope_first(self, mock_healer_with_penelope):
        """Test that PENELOPE service is tried first."""
        # Mock PENELOPE successful healing
        mock_healer_with_penelope.penelope_client.auto_heal = AsyncMock(
            return_value={
                "healed": True,
                "alternative_action": {"action": "click", "selector": "button.healed"}
            }
        )

        result = await mock_healer_with_penelope.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element not found",
            page_html="<div>Test</div>"
        )

        # Should use PENELOPE result
        assert result is not None
        # PENELOPE should have been called
        mock_healer_with_penelope.penelope_client.auto_heal.assert_called_once()

    @pytest.mark.asyncio
    async def test_fallback_to_local_on_penelope_failure(self, mock_healer_with_penelope):
        """Test fallback to local healing when PENELOPE fails."""
        # Mock PENELOPE failure
        mock_healer_with_penelope.penelope_client.auto_heal = AsyncMock(
            side_effect=Exception("PENELOPE unavailable")
        )

        # Mock local healing success
        mock_healer_with_penelope.analyzer.suggest_selectors = AsyncMock(
            return_value=["button.local"]
        )

        result = await mock_healer_with_penelope.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element not found",
            page_html="<button class='local'>Click</button>"
        )

        # Should fall back to local healing
        assert result is not None
        assert result["selector"] == "button.local"


class TestAutoHealerElementDescription:
    """Test AutoHealer element description inference."""

    def test_infer_submit_button(self):
        """Test inferring submit button description."""
        healer = AutoHealer()
        description = healer._infer_element_description("click", "button.submit-form")
        assert "submit" in description.lower()

    def test_infer_login_button(self):
        """Test inferring login button description."""
        healer = AutoHealer()
        description = healer._infer_element_description("click", "a.login-link")
        assert "login" in description.lower()

    def test_infer_generic_button(self):
        """Test inferring generic button description."""
        healer = AutoHealer()
        description = healer._infer_element_description("click", "button.primary")
        assert "button" in description.lower()

    def test_infer_input_field(self):
        """Test inferring input field description."""
        healer = AutoHealer()
        description = healer._infer_element_description("type", "input.email")
        assert "input" in description.lower()


class TestAutoHealerStatistics:
    """Test AutoHealer healing statistics."""

    @pytest.fixture
    def mock_healer(self):
        """Create healer with mocked components."""
        analyzer = AsyncMock()
        healer = AutoHealer(analyzer=analyzer)
        return healer

    @pytest.mark.asyncio
    async def test_healing_stats_empty(self, mock_healer):
        """Test stats when no healing attempts."""
        stats = mock_healer.get_healing_stats()

        assert stats["total_attempts"] == 0
        assert stats["successful"] == 0
        assert stats["failed"] == 0
        assert stats["success_rate"] == 0.0

    @pytest.mark.asyncio
    async def test_healing_stats_with_attempts(self, mock_healer):
        """Test stats with healing attempts."""
        # Mock successful healing
        mock_healer.analyzer.suggest_selectors = AsyncMock(return_value=["button.alt"])

        # Perform 3 successful healings
        for i in range(3):
            await mock_healer.heal_failed_action(
                failed_action={"action": "click", "selector": f"button{i}"},
                error_message="Element not found",
                page_html="<button class='alt'>Click</button>"
            )

        # Perform 1 failed healing (no HTML provided)
        await mock_healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="Element not found",
            page_html=None  # Will fail
        )

        stats = mock_healer.get_healing_stats()

        assert stats["total_attempts"] == 4
        assert stats["successful"] == 3
        assert stats["failed"] == 1
        assert stats["success_rate"] == 0.75


class TestAutoHealerClose:
    """Test AutoHealer cleanup."""

    @pytest.mark.asyncio
    async def test_close_closes_components(self):
        """Test that close() closes analyzer and client."""
        analyzer = AsyncMock()
        penelope_client = AsyncMock()

        healer = AutoHealer(
            analyzer=analyzer,
            penelope_client=penelope_client
        )

        await healer.close()

        # Both should be closed
        analyzer.close.assert_called_once()
        penelope_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_handles_none_client(self):
        """Test that close() handles None client gracefully."""
        analyzer = AsyncMock()

        healer = AutoHealer(
            analyzer=analyzer,
            penelope_client=None
        )

        # Should not raise error
        await healer.close()
        analyzer.close.assert_called_once()
