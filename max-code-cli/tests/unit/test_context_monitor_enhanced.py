"""
Enhanced tests for context monitor with user prompt functionality

Tests the new interactive user prompt and auto-approval features.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from core.context.monitor import AutoCompactionMonitor
from core.context.types import (
    ConversationContext,
    Message,
    MessageRole,
    CompactionConfig,
    CompactionStrategy,
)


@pytest.fixture
def sample_context():
    """Create sample context for testing"""
    messages = [
        Message(role=MessageRole.SYSTEM, content="You are a helpful assistant"),
        Message(role=MessageRole.USER, content="Hello"),
        Message(role=MessageRole.ASSISTANT, content="Hi there!"),
    ]
    return ConversationContext(messages=messages, max_tokens=1000)


@pytest.fixture
def monitor(sample_context):
    """Create monitor instance"""
    config = CompactionConfig(
        strategy=CompactionStrategy.SELECTIVE,
        compact_threshold=0.8,
        target_ratio=0.7,
    )
    return AutoCompactionMonitor(
        context=sample_context,
        config=config,
        require_confirmation=True,
    )


class TestUserPrompt:
    """Test interactive user prompt functionality"""

    @patch('sys.stdin.isatty', return_value=False)
    def test_non_interactive_auto_approves(self, mock_isatty, monitor):
        """Non-interactive mode should auto-approve"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is True

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', return_value='y')
    def test_interactive_user_approves(self, mock_input, mock_isatty, monitor):
        """Interactive mode with 'y' should approve"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is True
        assert mock_input.called

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', return_value='yes')
    def test_interactive_user_approves_full_yes(self, mock_input, mock_isatty, monitor):
        """Interactive mode with 'yes' should approve"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is True

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', return_value='')
    def test_interactive_empty_response_approves(self, mock_input, mock_isatty, monitor):
        """Interactive mode with empty (Enter) should approve"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is True

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', return_value='n')
    def test_interactive_user_declines(self, mock_input, mock_isatty, monitor):
        """Interactive mode with 'n' should decline"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is False

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', return_value='no')
    def test_interactive_user_declines_full_no(self, mock_input, mock_isatty, monitor):
        """Interactive mode with 'no' should decline"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is False

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', side_effect=EOFError())
    def test_eof_error_auto_approves(self, mock_input, mock_isatty, monitor):
        """EOFError should auto-approve as fallback"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is True

    @patch('sys.stdin.isatty', return_value=True)
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_keyboard_interrupt_auto_approves(self, mock_input, mock_isatty, monitor):
        """KeyboardInterrupt should auto-approve as fallback"""
        import asyncio
        result = asyncio.run(monitor._request_confirmation())
        assert result is True


class TestMonitorStatistics:
    """Test monitor statistics and reporting"""

    def test_repr_shows_usage(self, monitor):
        """__repr__ should show usage percentage"""
        repr_str = repr(monitor)
        assert "ContextMonitor" in repr_str or "AutoCompactionMonitor" in repr_str
        assert "%" in repr_str
        assert "tokens" in repr_str

    def test_get_stats_includes_context(self, monitor):
        """get_stats should include context information"""
        stats = monitor.get_stats()
        assert "current_usage" in stats
        assert "max_tokens" in stats
        assert "usage_percent" in stats
        assert isinstance(stats["current_usage"], int)

    def test_usage_tracking(self, monitor, sample_context):
        """Monitor should track usage accurately"""
        usage = monitor.get_current_usage()
        assert usage > 0

        usage_percent = monitor.get_usage_percent()
        assert 0 <= usage_percent <= 100


class TestAutoCompaction:
    """Test auto-compaction triggers"""

    def test_should_compact_triggers_at_threshold(self, sample_context):
        """Should compact when threshold is reached"""
        config = CompactionConfig(
            strategy=CompactionStrategy.SELECTIVE,
            compact_threshold=0.01,  # Very low threshold
            target_ratio=0.7,
        )
        monitor = AutoCompactionMonitor(
            context=sample_context,
            config=config,
            require_confirmation=False,
        )

        # Should trigger compaction
        assert monitor.should_compact()

    def test_should_not_compact_below_threshold(self, sample_context):
        """Should not compact when below threshold"""
        config = CompactionConfig(
            strategy=CompactionStrategy.SELECTIVE,
            compact_threshold=0.99,  # Very high threshold
            target_ratio=0.7,
        )
        monitor = AutoCompactionMonitor(
            context=sample_context,
            config=config,
            require_confirmation=False,
        )

        # Should not trigger compaction
        assert not monitor.should_compact()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
