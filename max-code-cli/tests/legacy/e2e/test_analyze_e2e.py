"""E2E Tests for 'max-code analyze' command"""
import pytest


class TestAnalyzeE2E:
    @pytest.mark.e2e
    def test_analyze_help(self, invoke_command):
        result = invoke_command("analyze", ["--help"])
        assert result.exit_code == 0
    
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_analyze_sample_code(self, invoke_command, sample_code_path):
        result = invoke_command("analyze", [str(sample_code_path)])
        assert "traceback" not in result.output.lower()
