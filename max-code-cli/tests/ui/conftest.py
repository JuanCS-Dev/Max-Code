"""
Pytest configuration for UI tests

Provides fixtures and markers for UI testing:
- slow: Tests that involve actual animations (may take seconds)
- benchmark: Performance tests
"""

import pytest


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "slow: Tests that involve actual animations and may be slow"
    )
    config.addinivalue_line(
        "markers", "benchmark: Performance benchmark tests"
    )
