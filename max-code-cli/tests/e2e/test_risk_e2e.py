"""E2E Tests for 'max-code risk' command"""
import pytest


class TestRiskE2E:
    @pytest.mark.e2e
    def test_risk_help(self, invoke_command):
        result = invoke_command("risk", ["--help"])
        assert result.exit_code == 0
    
    @pytest.mark.e2e
    def test_risk_assess_offline(self, invoke_command):
        result = invoke_command("risk", ["--assess"])
        assert "traceback" not in result.output.lower()
