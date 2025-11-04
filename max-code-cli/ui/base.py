"""
Max-Code CLI UI Base Classes

Base classes and utility functions shared across all UI components.
Eliminates code duplication and ensures consistency.

Usage:
    from ui.base import BaseDisplay, score_to_color, render_progress_bar
"""

from rich.console import Console
from typing import Optional
from ui.constants import (
    SCORE_THRESHOLDS,
    PROGRESS_CHARS,
    STATUS_COLORS,
    STATUS_SYMBOLS,
)
from ui.types import ScoreType, PercentageType, ColorType


class BaseDisplay:
    """
    Base class for all display components.

    Provides common functionality:
    - Console management
    - Score-to-color mapping
    - Progress bar rendering
    - Status formatting
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize display component.

        Args:
            console: Optional Rich console instance
        """
        self.console = console or Console()

    # ========================================================================
    # COLOR UTILITIES
    # ========================================================================

    def score_to_color(self, score: ScoreType) -> ColorType:
        """
        Map score (0-10) to color.

        Args:
            score: Score value (0-10)

        Returns:
            Color name for Rich
        """
        if score >= SCORE_THRESHOLDS['excellent']:
            return "green"
        elif score >= SCORE_THRESHOLDS['good']:
            return "yellow"
        elif score >= SCORE_THRESHOLDS['fair']:
            return "orange3"
        else:
            return "red"

    def percentage_to_color(self, percentage: PercentageType) -> ColorType:
        """
        Map percentage (0-100) to color.

        Args:
            percentage: Percentage value (0-100)

        Returns:
            Color name for Rich
        """
        # Convert to 0-10 scale
        score = percentage / 10
        return self.score_to_color(score)

    # ========================================================================
    # PROGRESS BAR RENDERING
    # ========================================================================

    def render_progress_bar(
        self,
        percentage: PercentageType,
        width: int = 10,
        color: Optional[ColorType] = None,
        auto_color: bool = True
    ) -> str:
        """
        Render progress bar.

        Args:
            percentage: Progress percentage (0-100)
            width: Bar width in characters
            color: Bar color (overrides auto_color)
            auto_color: Use color based on percentage

        Returns:
            Formatted progress bar string
        """
        filled = int((percentage / 100) * width)
        empty = width - filled

        # Determine color
        if color is None and auto_color:
            color = self.percentage_to_color(percentage)
        elif color is None:
            color = 'cyan'

        filled_char = PROGRESS_CHARS['filled']
        empty_char = PROGRESS_CHARS['empty']

        bar = f"[{color}]{filled_char * filled}[/{color}][dim]{empty_char * empty}[/dim]"
        return bar

    def render_horizontal_bar(
        self,
        percentage: PercentageType,
        width: int = 30,
        color: Optional[ColorType] = None,
        auto_color: bool = True
    ) -> str:
        """
        Render horizontal bar chart.

        Args:
            percentage: Progress percentage (0-100)
            width: Bar width in characters
            color: Bar color (overrides auto_color)
            auto_color: Use color based on percentage

        Returns:
            Formatted horizontal bar string
        """
        filled = int((percentage / 100) * width)
        empty = width - filled

        # Determine color
        if color is None and auto_color:
            color = self.percentage_to_color(percentage)
        elif color is None:
            color = 'cyan'

        filled_char = PROGRESS_CHARS['horizontal_filled']
        empty_char = PROGRESS_CHARS['horizontal_empty']

        bar = f"[{color}]{filled_char * filled}[/{color}][dim]{empty_char * empty}[/dim]"
        return bar

    # ========================================================================
    # STATUS FORMATTING
    # ========================================================================

    def format_status(self, status: str) -> str:
        """
        Format status with color and symbol.

        Args:
            status: Status string (e.g., 'active', 'completed')

        Returns:
            Formatted status string
        """
        status_lower = status.lower()
        color = STATUS_COLORS.get(status_lower, 'white')
        symbol = STATUS_SYMBOLS.get(status_lower, '○')

        return f"[{color}]{symbol} {status.upper()}[/{color}]"

    # ========================================================================
    # TEXT UTILITIES
    # ========================================================================

    def truncate_text(self, text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate text to maximum length.

        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    def format_duration(self, seconds: float) -> str:
        """
        Format duration in seconds to human-readable string.

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration (e.g., "1.5s", "2m 30s", "1h 15m")
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            return f"{hours}h {remaining_minutes}m"

    def format_bytes(self, bytes_value: float) -> str:
        """
        Format bytes to human-readable string.

        Args:
            bytes_value: Size in bytes

        Returns:
            Formatted size (e.g., "1.5 MB", "500 KB")
        """
        if bytes_value < 1024:
            return f"{bytes_value:.0f} B"
        elif bytes_value < 1024 * 1024:
            return f"{bytes_value / 1024:.1f} KB"
        elif bytes_value < 1024 * 1024 * 1024:
            return f"{bytes_value / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes_value / (1024 * 1024 * 1024):.1f} GB"


# ============================================================================
# STANDALONE UTILITY FUNCTIONS
# ============================================================================

def score_to_color(score: ScoreType) -> ColorType:
    """
    Standalone function to map score to color.

    Args:
        score: Score value (0-10)

    Returns:
        Color name for Rich
    """
    if score >= SCORE_THRESHOLDS['excellent']:
        return "green"
    elif score >= SCORE_THRESHOLDS['good']:
        return "yellow"
    elif score >= SCORE_THRESHOLDS['fair']:
        return "orange3"
    else:
        return "red"


def render_progress_bar(
    percentage: PercentageType,
    width: int = 10,
    color: Optional[ColorType] = None
) -> str:
    """
    Standalone function to render progress bar.

    Args:
        percentage: Progress percentage (0-100)
        width: Bar width in characters
        color: Bar color (if None, uses percentage-based color)

    Returns:
        Formatted progress bar string
    """
    filled = int((percentage / 100) * width)
    empty = width - filled

    if color is None:
        color = score_to_color(percentage / 10)

    filled_char = PROGRESS_CHARS['filled']
    empty_char = PROGRESS_CHARS['empty']

    bar = f"[{color}]{filled_char * filled}[/{color}][dim]{empty_char * empty}[/dim]"
    return bar


def format_status(status: str) -> str:
    """
    Standalone function to format status.

    Args:
        status: Status string

    Returns:
        Formatted status string with color and symbol
    """
    status_lower = status.lower()
    color = STATUS_COLORS.get(status_lower, 'white')
    symbol = STATUS_SYMBOLS.get(status_lower, '○')

    return f"[{color}]{symbol} {status.upper()}[/{color}]"


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'BaseDisplay',
    'score_to_color',
    'render_progress_bar',
    'format_status',
]
