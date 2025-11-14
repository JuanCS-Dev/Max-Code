"""
Pytest Configuration and Shared Fixtures

Global fixtures available to all tests.
Boris Cherny Standard: Clean, reusable test infrastructure.
"""

import pytest
import sys
import os
from pathlib import Path
from typing import Generator, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================
# PYTEST HOOKS
# ============================================================

def pytest_configure(config: Any) -> None:
    """Configure pytest session."""
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests (>1 second)")


# ============================================================
# SHARED FIXTURES
# ============================================================

@pytest.fixture
def sample_task_description() -> str:
    """Sample task description for testing."""
    return "Generate a REST API endpoint for user management"


@pytest.fixture
def sample_task_parameters() -> dict:
    """Sample task parameters for testing."""
    return {
        "framework": "fastapi",
        "include_tests": True,
    }
