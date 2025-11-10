"""E2E Tests for 'max-code workflow' command"""
import pytest


class TestWorkflowE2E:
    @pytest.mark.e2e
    def test_workflow_help(self, invoke_command):
        result = invoke_command("workflow", ["--help"])
        assert result.exit_code == 0
    
    @pytest.mark.e2e
    def test_workflow_list_offline(self, invoke_command):
        result = invoke_command("workflow", ["list"])
        assert "traceback" not in result.output.lower()
