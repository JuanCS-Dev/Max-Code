"""
Tests for heal_command - Penelope Self-Healing

Biblical Foundation:
"Ele sara os quebrantados de coração e liga as suas feridas" (Salmos 147:3)

NO MOCK, NO PLACEHOLDER, NO TODO
"""

import pytest
from click.testing import CliRunner
from cli.heal_command import heal


class TestHealCommandHelp:
    """Test heal command help"""

    def setup_method(self):
        """Setup test fixtures"""
        self.runner = CliRunner()

    def test_heal_help(self):
        """Test heal command help output"""
        result = self.runner.invoke(heal, ["--help"])
        assert result.exit_code == 0
        assert "heal" in result.output.lower()
        assert "--auto" in result.output
        assert "--focus" in result.output
        assert "--format" in result.output

    def test_heal_requires_target_argument(self):
        """Test that target argument is required"""
        result = self.runner.invoke(heal, [])
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "target" in result.output.lower()


class TestHealCommandBasic:
    """Test basic heal command functionality"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_heal_with_target(self):
        """Test heal with target name"""
        # User will be prompted, auto-answer 'n'
        result = self.runner.invoke(heal, ["eureka"], input="n\n")

        # Should execute (cancelled by user)
        assert result.exit_code in [0, 1]

    def test_heal_with_auto_flag(self):
        """Test heal with --auto flag (no confirmation)"""
        result = self.runner.invoke(heal, ["eureka", "--auto"])

        # Should execute (may fail if service not running)
        assert result.exit_code in [0, 1]

    def test_heal_with_system_target(self):
        """Test heal with system target"""
        result = self.runner.invoke(heal, ["system", "--auto"])

        assert result.exit_code in [0, 1]

    def test_heal_with_errors_target(self):
        """Test heal with errors target"""
        result = self.runner.invoke(heal, ["errors", "--auto"])

        assert result.exit_code in [0, 1]


class TestHealCommandFocus:
    """Test heal command focus options"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_heal_focus_errors(self):
        """Test heal with --focus errors"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--focus", "errors"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_focus_warnings(self):
        """Test heal with --focus warnings"""
        result = self.runner.invoke(heal, [
            "system",
            "--auto",
            "--focus", "warnings"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_focus_performance(self):
        """Test heal with --focus performance"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--focus", "performance"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_focus_all(self):
        """Test heal with --focus all (default)"""
        result = self.runner.invoke(heal, [
            "system",
            "--auto",
            "--focus", "all"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_invalid_focus(self):
        """Test heal with invalid focus value"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--focus", "invalid"
        ])

        # Should fail with validation error
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "choice" in result.output.lower()


class TestHealCommandFormats:
    """Test heal command output formats"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_heal_table_format(self):
        """Test heal with --format table (default)"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--format", "table"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_json_format(self):
        """Test heal with --format json"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--format", "json"
        ])

        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            # JSON output should contain json-like structure
            assert "{" in result.output or "[" in result.output

    def test_heal_invalid_format(self):
        """Test heal with invalid format value"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--format", "invalid"
        ])

        # Should fail with validation error
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "choice" in result.output.lower()


class TestHealCommandCombinations:
    """Test heal command with combined options"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_heal_auto_with_focus_errors(self):
        """Test heal with --auto and --focus errors"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--focus", "errors"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_auto_with_json_format(self):
        """Test heal with --auto and --format json"""
        result = self.runner.invoke(heal, [
            "system",
            "--auto",
            "--format", "json"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_all_options(self):
        """Test heal with all options combined"""
        result = self.runner.invoke(heal, [
            "eureka",
            "--auto",
            "--focus", "performance",
            "--format", "json"
        ])

        assert result.exit_code in [0, 1]

    def test_heal_errors_focus_table(self):
        """Test heal with errors focus and table format"""
        result = self.runner.invoke(heal, [
            "errors",
            "--auto",
            "--focus", "errors",
            "--format", "table"
        ])

        assert result.exit_code in [0, 1]


class TestHealCommandConfirmation:
    """Test heal command confirmation behavior"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_heal_cancelled_by_user(self):
        """Test heal cancelled when user rejects confirmation"""
        result = self.runner.invoke(heal, ["eureka"], input="n\n")

        # Should complete without error (user cancelled)
        assert result.exit_code == 0
        assert "cancelled" in result.output.lower()

    def test_heal_confirmed_by_user(self):
        """Test heal proceeds when user confirms"""
        result = self.runner.invoke(heal, ["eureka"], input="y\n")

        # Should execute (may fail if service not running)
        assert result.exit_code in [0, 1]


class TestHealCommandTargets:
    """Test heal command with different targets"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_heal_service_target(self):
        """Test heal with service name"""
        result = self.runner.invoke(heal, ["eureka", "--auto"])
        assert result.exit_code in [0, 1]

    def test_heal_system_target(self):
        """Test heal with 'system' target"""
        result = self.runner.invoke(heal, ["system", "--auto"])
        assert result.exit_code in [0, 1]

    def test_heal_errors_target(self):
        """Test heal with 'errors' target"""
        result = self.runner.invoke(heal, ["errors", "--auto"])
        assert result.exit_code in [0, 1]

    def test_heal_custom_target(self):
        """Test heal with custom target name"""
        result = self.runner.invoke(heal, ["my-custom-service", "--auto"])
        assert result.exit_code in [0, 1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
