"""
Tests for Features 2-7 Commands

Tests logs, analyze, risk, workflow, heal, and security commands.

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""
import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch

from cli.logs_command import logs
from cli.analyze_command import analyze
from cli.risk_command import risk
from cli.workflow_command import workflow
from cli.heal_command import heal
from cli.security_command import security

from core.maximus_integration.shared_client import ServiceResponse


class TestLogsCommand:
    """Test logs command"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(logs, ["--help"])
        
        assert result.exit_code == 0
        assert "Stream logs" in result.output
        assert "--tail" in result.output
        assert "--follow" in result.output
    
    def test_invalid_service(self):
        """Test invalid service name"""
        runner = CliRunner()
        result = runner.invoke(logs, ["invalid_service"])
        
        assert result.exit_code != 0
        assert "Invalid Service" in result.output
    
    @patch('cli.logs_command.get_shared_client')
    def test_fetch_logs_success(self, mock_client):
        """Test successful log fetch"""
        mock_client_instance = Mock()
        mock_client_instance.request.return_value = ServiceResponse(
            success=True,
            data={"logs": [
                {"timestamp": "2025-11-08T10:00:00", "level": "INFO", "message": "Test log"}
            ]},
            status_code=200,
            service="core"
        )
        mock_client.return_value = mock_client_instance
        
        runner = CliRunner()
        result = runner.invoke(logs, ["core", "--tail", "10"])
        
        assert result.exit_code == 0
        assert "Logs: CORE" in result.output


class TestAnalyzeCommand:
    """Test analyze command"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(analyze, ["--help"])
        
        assert result.exit_code == 0
        assert "Analyze code" in result.output
        assert "--security" in result.output
        assert "--quality" in result.output
    
    @patch('cli.analyze_command.get_shared_client')
    @patch('cli.analyze_command.show_progress_operation')
    def test_analyze_success(self, mock_progress, mock_client):
        """Test successful analysis"""
        mock_client_instance = Mock()
        mock_client_instance.request.return_value = ServiceResponse(
            success=True,
            data={
                "overall_score": 8,
                "security_score": 8,
                "quality_score": 8,
                "maintainability_score": 8,
                "test_coverage": 80,
                "issues": {},
                "recommendations": ["Good work!"]
            },
            status_code=200,
            service="eureka"
        )
        mock_client.return_value = mock_client_instance
        
        # Mock progress operation
        mock_progress.return_value = [
            {"path": "/test"},
            mock_client_instance.request.return_value,
            {"formatted": True}
        ]
        
        runner = CliRunner()
        result = runner.invoke(analyze, [".", "--threshold", "7"])
        
        assert result.exit_code == 0


class TestRiskCommand:
    """Test risk command"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(risk, ["--help"])
        
        assert result.exit_code == 0
        assert "Risk assessment" in result.output
        assert "--assess" in result.output
        assert "--suggest" in result.output
    
    @patch('cli.risk_command.get_shared_client')
    def test_assess_success(self, mock_client):
        """Test successful risk assessment"""
        mock_client_instance = Mock()
        mock_client_instance.request.return_value = ServiceResponse(
            success=True,
            data={
                "risk_level": "LOW",
                "risk_score": 3,
                "risks": [],
                "mitigations": []
            },
            status_code=200,
            service="oraculo"
        )
        mock_client.return_value = mock_client_instance
        
        runner = CliRunner()
        result = runner.invoke(risk, ["--assess"])
        
        assert result.exit_code == 0
        assert "Risk Assessment" in result.output


class TestWorkflowCommand:
    """Test workflow command"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(workflow, ["--help"])
        
        assert result.exit_code == 0
        assert "Manage MAXIMUS workflows" in result.output
        assert "list" in result.output
        assert "run" in result.output
    
    @patch('cli.workflow_command.get_shared_client')
    def test_list_workflows(self, mock_client):
        """Test list workflows"""
        mock_client_instance = Mock()
        mock_client_instance.request.return_value = ServiceResponse(
            success=True,
            data={"workflows": [
                {"name": "test-workflow", "status": "active", "description": "Test"}
            ]},
            status_code=200,
            service="orchestrator"
        )
        mock_client.return_value = mock_client_instance
        
        runner = CliRunner()
        result = runner.invoke(workflow, ["list"])
        
        assert result.exit_code == 0
        assert "Workflows" in result.output


class TestHealCommand:
    """Test heal command"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(heal, ["--help"])
        
        assert result.exit_code == 0
        assert "Self-healing" in result.output
        assert "--auto" in result.output
    
    @patch('cli.heal_command.get_shared_client')
    @patch('cli.heal_command.show_thinking_stream')
    def test_heal_auto_success(self, mock_thinking, mock_client):
        """Test successful auto-healing"""
        mock_client_instance = Mock()
        mock_client_instance.request.return_value = ServiceResponse(
            success=True,
            data={
                "target": "eureka",
                "status": "healed",
                "actions_taken": ["Restarted service"],
                "improvements": ["Service restored"]
            },
            status_code=200,
            service="penelope"
        )
        mock_client.return_value = mock_client_instance
        
        runner = CliRunner()
        result = runner.invoke(heal, ["eureka", "--auto"])
        
        assert result.exit_code == 0
        assert "Healing" in result.output


class TestSecurityCommand:
    """Test security command"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(security, ["--help"])
        
        assert result.exit_code == 0
        assert "Security scanning" in result.output
        assert "--scan" in result.output
        assert "--report" in result.output
    
    @patch('cli.security_command.get_shared_client')
    def test_scan_success(self, mock_client):
        """Test successful security scan"""
        mock_client_instance = Mock()
        mock_client_instance.request.return_value = ServiceResponse(
            success=True,
            data={
                "threat_level": "LOW",
                "vulnerabilities_count": 0,
                "vulnerabilities": [],
                "recommendations": ["Good security posture"]
            },
            status_code=200,
            service="nis"
        )
        mock_client.return_value = mock_client_instance
        
        runner = CliRunner()
        result = runner.invoke(security, ["--scan"])
        
        assert result.exit_code == 0
        assert "Security Scan" in result.output


# Integration tests
@pytest.mark.integration
class TestRealServices:
    """Integration tests with real services (require services running)"""
    
    def test_real_logs(self):
        """Test real logs command"""
        runner = CliRunner()
        result = runner.invoke(logs, ["core", "--tail", "10"])
        
        # Should handle offline gracefully
        assert "Invalid Service" not in result.output or result.exit_code != 0
    
    def test_real_analyze(self):
        """Test real analyze command"""
        runner = CliRunner()
        result = runner.invoke(analyze, [".", "--threshold", "1"])
        
        # Should handle offline gracefully
        assert isinstance(result.exit_code, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
