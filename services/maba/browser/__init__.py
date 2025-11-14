"""MABA Browser Automation Package.

Day 3: Playwright-based browser automation with session management.
"""
from .controller import (
    BrowserController,
    BrowserControllerError,
    SessionNotFoundError,
    SessionLimitError,
    NavigationError,
    ElementNotFoundError,
)

__all__ = [
    "BrowserController",
    "BrowserControllerError",
    "SessionNotFoundError",
    "SessionLimitError",
    "NavigationError",
    "ElementNotFoundError",
]
