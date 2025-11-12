"""E2E Tests for 'max-code logs' command"""
import pytest


class TestLogsE2E:
    """End-to-end tests for logs command"""
    
    @pytest.mark.e2e
    def test_logs_help(self, invoke_command):
        """Test: logs --help"""
        result = invoke_command("logs", ["--help"])
        assert result.exit_code == 0
        assert "logs" in result.output.lower()
    
    @pytest.mark.e2e
    def test_logs_invalid_service(self, invoke_command):
        """Test: logs with invalid service"""
        result = invoke_command("logs", ["nonexistent"])
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "service" in result.output.lower()
    
    @pytest.mark.e2e
    def test_logs_default_offline(self, invoke_command):
        """Test: logs command when service offline"""
        result = invoke_command("logs", ["core"])
        # Should handle gracefully
        assert "traceback" not in result.output.lower()
