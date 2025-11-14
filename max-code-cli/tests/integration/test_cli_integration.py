"""
Integration Tests for Max-Code CLI

Tests the complete CLI workflow including dev commands.
Boris Cherny Standard: Integration tests for critical paths.
"""

import pytest
import subprocess
from pathlib import Path
import sys

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def run_cli_command(args: list) -> tuple:
    """
    Run a CLI command and return (returncode, stdout, stderr).
    
    Args:
        args: Command arguments (e.g., ['dev', 'test', '--help'])
    
    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    # Run via Python module
    cmd = [sys.executable, "-m", "cli.main"] + args
    result = subprocess.run(
        cmd,
        cwd=Path(__file__).parent.parent.parent,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


# ============================================================
# BASIC CLI TESTS
# ============================================================

@pytest.mark.integration
class TestCLIBasics:
    """Test basic CLI functionality."""
    
    def test_cli_help(self):
        """Test that CLI --help works."""
        returncode, stdout, stderr = run_cli_command(["--help"])
        assert returncode == 0
        assert "Max-Code CLI" in stdout or "Usage" in stdout
    
    def test_cli_version(self):
        """Test that CLI --version works."""
        returncode, stdout, stderr = run_cli_command(["--version"])
        assert returncode == 0
        # Should show version info


# ============================================================
# DEV COMMANDS TESTS
# ============================================================

@pytest.mark.integration
class TestDevCommands:
    """Test dev command group."""
    
    def test_dev_help(self):
        """Test that dev --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "--help"])
        assert returncode == 0
        assert "Development tools" in stdout or "dev" in stdout
    
    def test_dev_test_help(self):
        """Test that dev test --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "test", "--help"])
        assert returncode == 0
        assert "test" in stdout.lower()
    
    def test_dev_lint_help(self):
        """Test that dev lint --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "lint", "--help"])
        assert returncode == 0
        assert "lint" in stdout.lower()
    
    def test_dev_format_help(self):
        """Test that dev format --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "format", "--help"])
        assert returncode == 0
        assert "format" in stdout.lower()
    
    def test_dev_typecheck_help(self):
        """Test that dev typecheck --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "typecheck", "--help"])
        assert returncode == 0
        assert "type" in stdout.lower()
    
    def test_dev_security_help(self):
        """Test that dev security --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "security", "--help"])
        assert returncode == 0
        assert "security" in stdout.lower()
    
    def test_dev_audit_help(self):
        """Test that dev audit --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "audit", "--help"])
        assert returncode == 0
        assert "audit" in stdout.lower()
    
    def test_dev_coverage_help(self):
        """Test that dev coverage --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "coverage", "--help"])
        assert returncode == 0
        assert "coverage" in stdout.lower()
    
    def test_dev_ci_help(self):
        """Test that dev ci --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "ci", "--help"])
        assert returncode == 0
        assert "ci" in stdout.lower()
    
    def test_dev_stats_help(self):
        """Test that dev stats --help works."""
        returncode, stdout, stderr = run_cli_command(["dev", "stats", "--help"])
        assert returncode == 0
        assert "stats" in stdout.lower()


# ============================================================
# COMMAND AVAILABILITY
# ============================================================

@pytest.mark.integration
def test_all_dev_commands_available():
    """Test that all dev commands are registered and available."""
    expected_commands = [
        "test",
        "coverage",
        "lint",
        "format",
        "typecheck",
        "security",
        "audit",
        "ci",
        "pre-push",
        "stats",
        "help-dev"
    ]
    
    returncode, stdout, stderr = run_cli_command(["dev", "--help"])
    assert returncode == 0
    
    # Check that each command appears in help text
    for cmd in expected_commands:
        # Commands might appear with hyphens or underscores
        assert cmd in stdout or cmd.replace("-", "_") in stdout or cmd.replace("_", "-") in stdout, \
            f"Command '{cmd}' not found in dev --help output"


# ============================================================
# MAKEFILE INTEGRATION
# ============================================================

@pytest.mark.integration
class TestMakefileIntegration:
    """Test that Makefile commands work."""
    
    def test_makefile_exists(self):
        """Test that Makefile exists."""
        makefile = Path(__file__).parent.parent.parent / "Makefile"
        assert makefile.exists(), "Makefile not found"
    
    def test_makefile_help(self):
        """Test that make help works."""
        result = subprocess.run(
            ["make", "help"],
            cwd=Path(__file__).parent.parent.parent,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Max-Code CLI" in result.stdout


# ============================================================
# CI/CD INTEGRATION
# ============================================================

@pytest.mark.integration
class TestCICDIntegration:
    """Test CI/CD pipeline integration."""
    
    def test_github_workflow_exists(self):
        """Test that GitHub Actions workflow exists."""
        workflow = Path(__file__).parent.parent.parent.parent / ".github" / "workflows" / "ci.yml"
        assert workflow.exists(), "GitHub Actions workflow not found"
    
    def test_pre_commit_config_exists(self):
        """Test that pre-commit config exists."""
        config = Path(__file__).parent.parent.parent.parent / ".pre-commit-config.yaml"
        assert config.exists(), "Pre-commit config not found"
    
    def test_coverage_config_exists(self):
        """Test that coverage config exists."""
        config = Path(__file__).parent.parent.parent / ".coveragerc"
        assert config.exists(), "Coverage config not found"


# ============================================================
# BORIS CHERNY COMPLIANCE
# ============================================================

@pytest.mark.integration
def test_boris_cherny_compliance():
    """
    Meta-test: Verify Boris Cherny standards compliance.
    
    Checks:
    - Type safety configuration (mypy.ini)
    - Testing configuration (pytest.ini)
    - Structured logging (config/logging_config.py)
    - Security requirements (requirements.secure.txt)
    """
    base_path = Path(__file__).parent.parent.parent
    
    # Type safety
    assert (base_path / "mypy.ini").exists(), "mypy.ini not found"
    
    # Testing
    assert (base_path / "pytest.ini").exists(), "pytest.ini not found"
    
    # Logging
    assert (base_path / "config" / "logging_config.py").exists(), "logging_config.py not found"
    
    # Security
    assert (base_path / "requirements.secure.txt").exists(), "requirements.secure.txt not found"
    
    # Documentation
    assert (base_path / "PHASE_4_SUMMARY.md").exists(), "Phase 4 summary not found"


# ============================================================
# COVERAGE TARGET
# ============================================================

# Target: Integration tests verify critical user workflows
# These tests ensure:
# - CLI commands are registered correctly
# - Help text is available for all commands
# - Configuration files exist
# - CI/CD infrastructure is in place
# - Boris Cherny standards are enforced
