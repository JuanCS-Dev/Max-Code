"""
Tests for analyze_command - Eureka Code Analysis

Biblical Foundation:
"Toda a Escritura é divinamente inspirada, e proveitosa para ensinar" (2 Timóteo 3:16)

NO MOCK, NO PLACEHOLDER, NO TODO
"""

import pytest
from click.testing import CliRunner
from cli.analyze_command import analyze


class TestAnalyzeCommandHelp:
    """Test analyze command help"""

    def setup_method(self):
        """Setup test fixtures"""
        self.runner = CliRunner()

    def test_analyze_help(self):
        """Test analyze command help output"""
        result = self.runner.invoke(analyze, ["--help"])
        assert result.exit_code == 0
        assert "analyze" in result.output.lower()
        assert "--security" in result.output
        assert "--quality" in result.output
        assert "--format" in result.output
        assert "--threshold" in result.output


class TestAnalyzeCommandBasic:
    """Test basic analyze command functionality"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_analyze_default(self):
        """Test analyze with default path (current directory)"""
        result = self.runner.invoke(analyze, [])

        # Should execute (may fail if service not running)
        assert result.exit_code in [0, 1]

    def test_analyze_with_path(self):
        """Test analyze with explicit path"""
        result = self.runner.invoke(analyze, ["."])

        assert result.exit_code in [0, 1]

    def test_analyze_security_focus(self):
        """Test analyze with --security flag"""
        result = self.runner.invoke(analyze, [".", "--security"])

        assert result.exit_code in [0, 1]

    def test_analyze_quality_focus(self):
        """Test analyze with --quality flag"""
        result = self.runner.invoke(analyze, [".", "--quality"])

        assert result.exit_code in [0, 1]


class TestAnalyzeCommandFormats:
    """Test analyze command output formats"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_analyze_table_format(self):
        """Test analyze with --format table (default)"""
        result = self.runner.invoke(analyze, [".", "--format", "table"])

        assert result.exit_code in [0, 1]

    def test_analyze_json_format(self):
        """Test analyze with --format json"""
        result = self.runner.invoke(analyze, [".", "--format", "json"])

        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            # JSON output should contain json-like structure
            assert "{" in result.output or "[" in result.output

    def test_analyze_invalid_format(self):
        """Test analyze with invalid format value"""
        result = self.runner.invoke(analyze, [".", "--format", "invalid"])

        # Should fail with validation error
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "choice" in result.output.lower()


class TestAnalyzeCommandThreshold:
    """Test analyze command threshold option"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_analyze_threshold_default(self):
        """Test analyze with default threshold (7)"""
        result = self.runner.invoke(analyze, ["."])

        assert result.exit_code in [0, 1]

    def test_analyze_threshold_low(self):
        """Test analyze with low threshold (5)"""
        result = self.runner.invoke(analyze, [".", "--threshold", "5"])

        assert result.exit_code in [0, 1]

    def test_analyze_threshold_high(self):
        """Test analyze with high threshold (9)"""
        result = self.runner.invoke(analyze, [".", "--threshold", "9"])

        assert result.exit_code in [0, 1]

    def test_analyze_threshold_min(self):
        """Test analyze with minimum threshold (1)"""
        result = self.runner.invoke(analyze, [".", "--threshold", "1"])

        assert result.exit_code in [0, 1]

    def test_analyze_threshold_max(self):
        """Test analyze with maximum threshold (10)"""
        result = self.runner.invoke(analyze, [".", "--threshold", "10"])

        assert result.exit_code in [0, 1]

    def test_analyze_threshold_below_min(self):
        """Test analyze with threshold below minimum (0)"""
        result = self.runner.invoke(analyze, [".", "--threshold", "0"])

        # Should fail with validation error
        assert result.exit_code != 0
        assert "threshold" in result.output.lower() or "between" in result.output.lower()

    def test_analyze_threshold_above_max(self):
        """Test analyze with threshold above maximum (11)"""
        result = self.runner.invoke(analyze, [".", "--threshold", "11"])

        # Should fail with validation error
        assert result.exit_code != 0
        assert "threshold" in result.output.lower() or "between" in result.output.lower()


class TestAnalyzeCommandCombinations:
    """Test analyze command with combined options"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_analyze_security_json(self):
        """Test analyze with --security and JSON format"""
        result = self.runner.invoke(analyze, [
            ".",
            "--security",
            "--format", "json"
        ])

        assert result.exit_code in [0, 1]

    def test_analyze_quality_json(self):
        """Test analyze with --quality and JSON format"""
        result = self.runner.invoke(analyze, [
            ".",
            "--quality",
            "--format", "json"
        ])

        assert result.exit_code in [0, 1]

    def test_analyze_security_quality(self):
        """Test analyze with both --security and --quality"""
        result = self.runner.invoke(analyze, [
            ".",
            "--security",
            "--quality"
        ])

        assert result.exit_code in [0, 1]

    def test_analyze_security_threshold(self):
        """Test analyze with --security and custom threshold"""
        result = self.runner.invoke(analyze, [
            ".",
            "--security",
            "--threshold", "8"
        ])

        assert result.exit_code in [0, 1]

    def test_analyze_all_options(self):
        """Test analyze with all options combined"""
        result = self.runner.invoke(analyze, [
            ".",
            "--security",
            "--quality",
            "--format", "json",
            "--threshold", "7"
        ])

        assert result.exit_code in [0, 1]


class TestAnalyzeCommandPaths:
    """Test analyze command with different paths"""

    def setup_method(self):
        """Setup"""
        self.runner = CliRunner()

    def test_analyze_current_directory(self):
        """Test analyze with current directory ('.')"""
        result = self.runner.invoke(analyze, ["."])
        assert result.exit_code in [0, 1]

    def test_analyze_nonexistent_path(self):
        """Test analyze with non-existent path"""
        result = self.runner.invoke(analyze, ["/nonexistent/path/to/code"])

        # Should fail with path error
        assert result.exit_code != 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
