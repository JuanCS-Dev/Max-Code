"""
E2E Test Fixtures and Configuration

Provides shared fixtures for end-to-end workflow testing.
Focuses on realistic user scenarios and environment isolation.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Create Click CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """
    Isolate Max-Code configuration to temporary directory.

    Prevents tests from polluting user's actual ~/.max-code directory.
    """
    config_dir = tmp_path / ".max-code"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Override home directory for this test
    monkeypatch.setenv("HOME", str(tmp_path))

    yield config_dir

    # Cleanup handled by tmp_path fixture


@pytest.fixture
def mock_git_repo(tmp_path):
    """
    Create a mock git repository for testing.

    Returns:
        Path to mock git repository with initialized git
    """
    repo_dir = tmp_path / "test-project"
    repo_dir.mkdir(parents=True, exist_ok=True)

    # Initialize git
    import subprocess
    subprocess.run(
        ["git", "init"],
        cwd=repo_dir,
        capture_output=True,
        check=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_dir,
        capture_output=True,
        check=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        capture_output=True,
        check=True
    )

    # Create initial commit
    readme = repo_dir / "README.md"
    readme.write_text("# Test Project\n")

    subprocess.run(
        ["git", "add", "."],
        cwd=repo_dir,
        capture_output=True,
        check=True
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=repo_dir,
        capture_output=True,
        check=True
    )

    return repo_dir


@pytest.fixture
def python_project(mock_git_repo):
    """
    Create a realistic Python project structure.

    Returns:
        Path to Python project with pyproject.toml, src/, tests/, etc.
    """
    # Create pyproject.toml
    pyproject = mock_git_repo / "pyproject.toml"
    pyproject.write_text("""
[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test project for E2E testing"

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0"
""")

    # Create src directory
    src_dir = mock_git_repo / "src" / "test_project"
    src_dir.mkdir(parents=True, exist_ok=True)

    init_file = src_dir / "__init__.py"
    init_file.write_text('"""Test project."""\n\n__version__ = "0.1.0"\n')

    main_file = src_dir / "main.py"
    main_file.write_text("""
def hello(name: str) -> str:
    \"\"\"Greet someone.\"\"\"
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(hello("World"))
""")

    # Create tests directory
    tests_dir = mock_git_repo / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    test_file = tests_dir / "test_main.py"
    test_file.write_text("""
from test_project.main import hello

def test_hello():
    assert hello("World") == "Hello, World!"
""")

    return mock_git_repo


@pytest.fixture
def mock_maximus_services(monkeypatch):
    """
    Mock MAXIMUS service responses for offline testing.

    Returns health check and prediction responses without actual services.
    """
    from unittest.mock import MagicMock

    # Mock service health checks
    def mock_health_check(*args, **kwargs):
        return {
            "status": "healthy",
            "latency_ms": 25,
            "service": "mock"
        }

    # Mock prediction responses
    def mock_predict(*args, **kwargs):
        return [
            {"command": "git status", "confidence": 0.95},
            {"command": "git add .", "confidence": 0.85},
            {"command": "git commit -m 'Update'", "confidence": 0.75}
        ]

    # Apply mocks
    # (We'll integrate these when services are called)

    yield {
        "health_check": mock_health_check,
        "predict": mock_predict
    }


@pytest.fixture
def performance_tracker():
    """
    Track performance metrics during E2E tests.

    Yields a tracker that records command execution times.
    """
    class PerformanceTracker:
        def __init__(self):
            self.timings = []

        def record(self, command: str, duration_ms: float):
            """Record command execution time."""
            self.timings.append({
                "command": command,
                "duration_ms": duration_ms
            })

        def get_avg(self, command: str = None) -> float:
            """Get average execution time."""
            if command:
                filtered = [t["duration_ms"] for t in self.timings if t["command"] == command]
                return sum(filtered) / len(filtered) if filtered else 0
            else:
                return sum(t["duration_ms"] for t in self.timings) / len(self.timings) if self.timings else 0

        def assert_performance(self, command: str, max_ms: float):
            """Assert command met performance target."""
            avg = self.get_avg(command)
            assert avg < max_ms, f"{command} took {avg:.2f}ms (expected < {max_ms}ms)"

    return PerformanceTracker()


@pytest.fixture(autouse=True)
def fast_fail_unavailable_services(monkeypatch):
    """
    Configure fast failure for unavailable services in E2E tests.

    Prevents tests from hanging on network timeouts.
    """
    # Reduce timeout for service health checks
    monkeypatch.setenv("MAXIMUS_HEALTH_TIMEOUT", "1")  # 1 second timeout
    monkeypatch.setenv("MAXIMUS_PREDICT_TIMEOUT", "2")  # 2 second timeout

    yield
