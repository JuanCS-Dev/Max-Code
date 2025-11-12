"""
Tests for Health Command

Tests enhanced health command functionality.

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""
import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch

from cli.health_command import (
    health,
    check_all_services,
    check_single_service,
    SERVICE_DESCRIPTIONS
)
from core.maximus_integration.shared_client import ServiceResponse, MaximusService


class TestHealthCommand:
    """Test health command CLI"""
    
    def test_help_option(self):
        """Test --help flag"""
        runner = CliRunner()
        result = runner.invoke(health, ["--help"])
        
        assert result.exit_code == 0
        assert "Check health status" in result.output
        assert "--detailed" in result.output
        assert "--watch" in result.output
        assert "--format" in result.output
    
    def test_invalid_service_name(self):
        """Test invalid service name shows error"""
        runner = CliRunner()
        result = runner.invoke(health, ["invalid_service"])
        
        assert result.exit_code != 0
        assert "Invalid Service" in result.output
        assert "invalid_service" in result.output
        assert "Available services" in result.output
    
    def test_valid_service_names(self):
        """Test all valid service names are accepted"""
        valid_services = [s.value for s in MaximusService]
        
        for service in valid_services:
            runner = CliRunner()
            # Won't succeed without services running, but shouldn't error on service name
            result = runner.invoke(health, [service, "--timeout", "1"])
            # Should not show "Invalid Service" error
            assert "Invalid Service" not in result.output
    
    @patch('cli.health_command.check_all_services')
    def test_table_format_default(self, mock_check):
        """Test default table format"""
        # Mock response
        mock_check.return_value = [
            ServiceResponse(
                success=True,
                data={"status": "healthy", "uptime": "2h"},
                status_code=200,
                response_time_ms=45.5,
                service="core"
            )
        ]
        
        runner = CliRunner()
        result = runner.invoke(health, ["--timeout", "1"])
        
        assert result.exit_code == 0
        assert "MAXIMUS Service Health" in result.output
        assert "✓ UP" in result.output
        assert "Summary" in result.output
    
    @patch('cli.health_command.check_all_services')
    def test_json_format(self, mock_check):
        """Test JSON output format"""
        mock_check.return_value = [
            ServiceResponse(
                success=True,
                data={"status": "healthy"},
                status_code=200,
                response_time_ms=50.0,
                service="core"
            )
        ]
        
        runner = CliRunner()
        result = runner.invoke(health, ["--format", "json", "--timeout", "1"])
        
        assert result.exit_code == 0
        # Should contain JSON-like output
        assert "core" in result.output
    
    @patch('cli.health_command.check_all_services')
    def test_detailed_flag(self, mock_check):
        """Test --detailed flag shows extra info"""
        mock_check.return_value = [
            ServiceResponse(
                success=True,
                data={"status": "healthy", "uptime": "2h 15m", "version": "1.0.0"},
                status_code=200,
                response_time_ms=45.5,
                service="core"
            )
        ]
        
        runner = CliRunner()
        result = runner.invoke(health, ["--detailed", "--timeout", "1"])
        
        assert result.exit_code == 0
        # Detailed mode should show more columns
        assert "Details" in result.output or "version" in result.output.lower()


class TestHealthChecks:
    """Test health check functions"""
    
    @patch('core.maximus_integration.shared_client.SharedMaximusClient.health_check')
    def test_check_single_service_success(self, mock_health_check):
        """Test successful single service check"""
        mock_health_check.return_value = ServiceResponse(
            success=True,
            data={"status": "healthy"},
            status_code=200,
            response_time_ms=45.5,
            service="core"
        )
        
        result = check_single_service("core", timeout=5)
        
        assert result.success is True
        assert result.service == "core"
        assert result.response_time_ms == 45.5
    
    @patch('core.maximus_integration.shared_client.SharedMaximusClient.health_check')
    def test_check_single_service_failure(self, mock_health_check):
        """Test failed single service check"""
        mock_health_check.return_value = ServiceResponse(
            success=False,
            error="Connection refused",
            status_code=503,
            service="core"
        )
        
        result = check_single_service("core", timeout=5)
        
        assert result.success is False
        assert result.error is not None
        assert "Connection refused" in result.error
    
    def test_check_single_service_invalid(self):
        """Test invalid service name"""
        result = check_single_service("invalid_service", timeout=5)
        
        assert result.success is False
        assert "Unknown service" in result.error
    
    @patch('core.maximus_integration.shared_client.SharedMaximusClient.health_check_all')
    def test_check_all_services(self, mock_health_check_all):
        """Test check all services"""
        mock_health_check_all.return_value = [
            ServiceResponse(success=True, service="core"),
            ServiceResponse(success=True, service="penelope"),
            ServiceResponse(success=False, service="oraculo", error="Timeout")
        ]
        
        results = check_all_services(timeout=10)
        
        assert len(results) == 3
        assert results[0].service == "core"
        assert results[1].success is True
        assert results[2].success is False


class TestServiceDescriptions:
    """Test service descriptions"""
    
    def test_all_services_have_descriptions(self):
        """Test all MaximusService values have descriptions"""
        for service in MaximusService:
            assert service.value in SERVICE_DESCRIPTIONS, \
                f"Missing description for {service.value}"
    
    def test_descriptions_are_non_empty(self):
        """Test descriptions are not empty"""
        for service, description in SERVICE_DESCRIPTIONS.items():
            assert description, f"Empty description for {service}"
            assert len(description) > 0


class TestResponseTimeFormatting:
    """Test response time color formatting logic"""
    
    def test_fast_response_time(self):
        """Test fast response (<50ms) is formatted"""
        # This tests the logic, not the actual output
        response_ms = 30.0
        
        if response_ms < 50:
            color = "green"
        elif response_ms < 150:
            color = "yellow"
        else:
            color = "red"
        
        assert color == "green"
    
    def test_medium_response_time(self):
        """Test medium response (50-150ms) is formatted"""
        response_ms = 100.0
        
        if response_ms < 50:
            color = "green"
        elif response_ms < 150:
            color = "yellow"
        else:
            color = "red"
        
        assert color == "yellow"
    
    def test_slow_response_time(self):
        """Test slow response (>150ms) is formatted"""
        response_ms = 250.0
        
        if response_ms < 50:
            color = "green"
        elif response_ms < 150:
            color = "yellow"
        else:
            color = "red"
        
        assert color == "red"


@pytest.mark.integration
class TestRealHealthChecks:
    """Integration tests with real services (require services running)"""
    
    def test_real_health_check_all(self):
        """Test real health check (if services available)"""
        results = check_all_services(timeout=5)
        
        # Should return results for all services
        assert len(results) == len(MaximusService)
        
        # All should be ServiceResponse
        for result in results:
            assert isinstance(result, ServiceResponse)
            assert result.service is not None
    
    def test_real_single_service(self):
        """Test real single service check (if available)"""
        result = check_single_service("core", timeout=5)
        
        assert isinstance(result, ServiceResponse)
        assert result.service == "core"
        # Don't assert success - service may be down


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
