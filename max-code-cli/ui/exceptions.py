"""
Max-Code CLI UI Exceptions

Custom exception hierarchy for UI components.
Provides clear, actionable error messages.

Usage:
    from ui.exceptions import UIError, InvalidConfigError

    raise InvalidConfigError("Temperature must be 0-1", suggestion="Use 0.7")
"""

from typing import Optional


class UIError(Exception):
    """Base exception for all UI errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        """
        Initialize UI error.

        Args:
            message: Error message
            suggestion: Optional suggestion for fixing the error
        """
        self.message = message
        self.suggestion = suggestion
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format error message with suggestion."""
        if self.suggestion:
            return f"{self.message}\nSuggestion: {self.suggestion}"
        return self.message


class InvalidInputError(UIError):
    """Raised when user input is invalid."""
    pass


class InvalidConfigError(UIError):
    """Raised when configuration is invalid."""
    pass


class RenderError(UIError):
    """Raised when rendering fails."""
    pass


class EmptyDataError(UIError):
    """Raised when required data is empty."""
    pass


class TerminalError(UIError):
    """Raised when terminal operations fail."""
    pass


class ImportError(UIError):
    """Raised when required dependencies are missing."""
    pass


__all__ = [
    'UIError',
    'InvalidInputError',
    'InvalidConfigError',
    'RenderError',
    'EmptyDataError',
    'TerminalError',
    'ImportError',
]
