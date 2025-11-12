"""E2E Tests for 'max-code security' command"""
import pytest


class TestSecurityE2E:
    @pytest.mark.e2e
    def test_security_help(self, invoke_command):
        result = invoke_command("security", ["--help"])
        assert result.exit_code == 0
    
    @pytest.mark.e2e
    def test_security_scan_offline(self, invoke_command):
        result = invoke_command("security", ["--scan"])
        assert "traceback" not in result.output.lower()
