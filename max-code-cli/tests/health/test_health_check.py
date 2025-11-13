"""
Comprehensive Health Check System Tests

Tests for core/health_check.py - MAXIMUS Services Health Monitoring

Categories:
1. Individual Service Health Checks
2. Parallel Service Checks
3. Summary Statistics
4. Critical Service Detection
5. Service Configuration

Biblical Foundation:
"E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentidos em Cristo Jesus."
(Filipenses 4:7)
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from aiohttp import ClientConnectorError
from typing import Dict

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.health_check import (
    HealthChecker,
    ServiceHealth,
    ServiceStatus,
    MAXIMUS_SERVICES,
    quick_health_check,
    sync_health_check,
)


# Helper function to create proper async mock
def create_mock_aiohttp_session(response_status=200, response_data=None, raise_error=None):
    """
    Create a properly mocked aiohttp.ClientSession

    Args:
        response_status: HTTP status code to return
        response_data: JSON data to return from response.json()
        raise_error: Exception to raise instead of returning response

    Returns:
        Mock ClientSession class
    """
    if response_data is None:
        response_data = {"status": "healthy"}

    # Create mock response
    mock_response = MagicMock()
    mock_response.status = response_status
    mock_response.json = AsyncMock(return_value=response_data)

    # Create mock for async context manager (response)
    mock_response_cm = MagicMock()
    mock_response_cm.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response_cm.__aexit__ = AsyncMock(return_value=None)

    # Create mock session
    mock_session = MagicMock()

    if raise_error:
        mock_session.get = MagicMock(side_effect=raise_error)
    else:
        mock_session.get = MagicMock(return_value=mock_response_cm)

    # Create mock for async context manager (session)
    mock_session_cm = MagicMock()
    mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_cm.__aexit__ = AsyncMock(return_value=None)

    return mock_session_cm


# ============================================================================
# 1. INDIVIDUAL SERVICE HEALTH CHECKS
# ============================================================================

class TestIndividualServiceHealthChecks:
    """Test checking individual services"""

    @pytest.mark.asyncio
    async def test_healthy_service_check(self):
        """Test checking a healthy service"""
        checker = HealthChecker(timeout=5.0)

        response_data = {
            "status": "healthy",
            "version": "1.0.0",
            "uptime": 3600,
            "circuit_breaker": "closed"
        }

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200, response_data)):
            result = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])

            assert result.status == ServiceStatus.HEALTHY
            assert result.name == "Maximus Core"
            assert result.port == 8150
            assert result.latency_ms is not None
            assert result.latency_ms >= 0
            assert result.version == "1.0.0"
            assert result.uptime_seconds == 3600
            assert result.circuit_breaker_state == "closed"
            assert result.error is None

    @pytest.mark.asyncio
    async def test_degraded_service_check(self):
        """Test checking a degraded service (HTTP 503)"""
        checker = HealthChecker(timeout=5.0)

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(503)):
            result = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])

            assert result.status == ServiceStatus.DEGRADED
            assert result.error == "HTTP 503"
            assert result.latency_ms is not None

    @pytest.mark.asyncio
    async def test_down_service_connection_refused(self):
        """Test checking a service that refuses connection"""
        checker = HealthChecker(timeout=5.0)

        error = ClientConnectorError(connection_key=MagicMock(), os_error=ConnectionRefusedError())

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(raise_error=error)):
            result = await checker.check_service("maba", MAXIMUS_SERVICES["maba"])

            assert result.status == ServiceStatus.DOWN
            assert result.error == "Connection refused"
            assert result.latency_ms is None

    @pytest.mark.asyncio
    async def test_down_service_timeout(self):
        """Test checking a service that times out"""
        checker = HealthChecker(timeout=1.0)

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(raise_error=asyncio.TimeoutError())):
            result = await checker.check_service("thot", MAXIMUS_SERVICES["thot"])

            assert result.status == ServiceStatus.DOWN
            assert result.error == "Timeout"
            assert result.latency_ms is not None  # Measured until timeout

    @pytest.mark.asyncio
    async def test_unexpected_exception(self):
        """Test handling unexpected exceptions"""
        checker = HealthChecker(timeout=5.0)

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(raise_error=ValueError("Unexpected error"))):
            result = await checker.check_service("thoth", MAXIMUS_SERVICES["thoth"])

            assert result.status == ServiceStatus.DOWN
            assert "ValueError" in result.error
            assert "Unexpected error" in result.error


# ============================================================================
# 2. PARALLEL SERVICE CHECKS
# ============================================================================

class TestParallelServiceChecks:
    """Test checking multiple services in parallel"""

    @pytest.mark.asyncio
    async def test_check_all_services_parallel(self):
        """Test checking all 8 services in parallel"""
        checker = HealthChecker(timeout=5.0)

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200)):
            health_map = await checker.check_all_services()

            assert len(health_map) == 8
            assert all(service_id in health_map for service_id in MAXIMUS_SERVICES.keys())
            assert all(health.status == ServiceStatus.HEALTHY for health in health_map.values())

    @pytest.mark.asyncio
    async def test_check_specific_services_only(self):
        """Test checking only specific services"""
        checker = HealthChecker(timeout=5.0)

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200)):
            health_map = await checker.check_all_services(services=["maximus_core", "penelope"])

            assert len(health_map) == 2
            assert "maximus_core" in health_map
            assert "penelope" in health_map


# ============================================================================
# 3. SUMMARY STATISTICS
# ============================================================================

class TestSummaryStatistics:
    """Test summary statistics generation"""

    def test_all_healthy_summary(self):
        """Test summary when all services are healthy"""
        checker = HealthChecker()

        health_map = {
            "maximus_core": ServiceHealth("Maximus Core", 8150, ServiceStatus.HEALTHY, latency_ms=25.5),
            "penelope": ServiceHealth("PENELOPE", 8151, ServiceStatus.HEALTHY, latency_ms=30.2),
        }

        summary = checker.get_summary(health_map)

        assert summary["total"] == 2
        assert summary["healthy"] == 2
        assert summary["degraded"] == 0
        assert summary["down"] == 0
        assert summary["all_healthy"] is True
        assert summary["avg_latency_ms"] is not None
        assert 20 < summary["avg_latency_ms"] < 35
        assert summary["critical_down"] == []

    def test_mixed_health_summary(self):
        """Test summary with mixed health states"""
        checker = HealthChecker()

        health_map = {
            "maximus_core": ServiceHealth("Maximus Core", 8150, ServiceStatus.HEALTHY, latency_ms=25.0),
            "penelope": ServiceHealth("PENELOPE", 8151, ServiceStatus.DEGRADED),
            "maba": ServiceHealth("MABA", 8152, ServiceStatus.DOWN, error="Connection refused"),
        }

        summary = checker.get_summary(health_map)

        assert summary["total"] == 3
        assert summary["healthy"] == 1
        assert summary["degraded"] == 1
        assert summary["down"] == 1
        assert summary["all_healthy"] is False

    def test_critical_services_down_detected(self):
        """Test detection of critical services down"""
        checker = HealthChecker()

        health_map = {
            "maximus_core": ServiceHealth("Maximus Core", 8150, ServiceStatus.DOWN, error="Connection refused"),
            "penelope": ServiceHealth("PENELOPE", 8151, ServiceStatus.DOWN, error="Timeout"),
            "maba": ServiceHealth("MABA", 8152, ServiceStatus.HEALTHY),
        }

        summary = checker.get_summary(health_map)

        assert len(summary["critical_down"]) == 2
        assert "Maximus Core" in summary["critical_down"]
        assert "PENELOPE" in summary["critical_down"]

    def test_average_latency_only_healthy_services(self):
        """Test average latency calculation only includes healthy services"""
        checker = HealthChecker()

        health_map = {
            "maximus_core": ServiceHealth("Maximus Core", 8150, ServiceStatus.HEALTHY, latency_ms=20.0),
            "penelope": ServiceHealth("PENELOPE", 8151, ServiceStatus.HEALTHY, latency_ms=40.0),
            "maba": ServiceHealth("MABA", 8152, ServiceStatus.DOWN, latency_ms=5000.0),  # Should be ignored
        }

        summary = checker.get_summary(health_map)

        # Average should be (20 + 40) / 2 = 30, NOT including the DOWN service
        assert summary["avg_latency_ms"] == 30.0

    def test_no_healthy_services_latency(self):
        """Test latency is None when no healthy services"""
        checker = HealthChecker()

        health_map = {
            "maximus_core": ServiceHealth("Maximus Core", 8150, ServiceStatus.DOWN),
            "penelope": ServiceHealth("PENELOPE", 8151, ServiceStatus.DEGRADED),
        }

        summary = checker.get_summary(health_map)

        assert summary["avg_latency_ms"] is None


# ============================================================================
# 4. CRITICAL SERVICE DETECTION
# ============================================================================

class TestCriticalServiceDetection:
    """Test critical service identification"""

    def test_critical_services_configured(self):
        """Test critical services are properly configured"""
        critical_services = [
            service_id for service_id, config in MAXIMUS_SERVICES.items()
            if config.get("critical")
        ]

        assert "maximus_core" in critical_services
        assert "penelope" in critical_services
        # Non-critical services
        assert "maba" not in critical_services

    def test_critical_service_down_alert(self):
        """Test alert when critical service is down"""
        checker = HealthChecker()

        health_map = {
            "maximus_core": ServiceHealth("Maximus Core", 8150, ServiceStatus.DOWN),
            "maba": ServiceHealth("MABA", 8152, ServiceStatus.DOWN),  # Non-critical
        }

        summary = checker.get_summary(health_map)

        # Only Maximus Core should be in critical_down
        assert len(summary["critical_down"]) == 1
        assert "Maximus Core" in summary["critical_down"]
        assert "MABA" not in summary["critical_down"]


# ============================================================================
# 5. SERVICE CONFIGURATION
# ============================================================================

class TestServiceConfiguration:
    """Test MAXIMUS services configuration"""

    def test_all_8_services_configured(self):
        """Test all 8 MAXIMUS services are configured"""
        assert len(MAXIMUS_SERVICES) == 8

        expected_services = [
            "maximus_core", "penelope", "maba", "thot",
            "thoth", "peniel", "anima", "pneuma"
        ]

        for service_id in expected_services:
            assert service_id in MAXIMUS_SERVICES

    def test_service_ports_unique(self):
        """Test all services have unique ports"""
        ports = [config["port"] for config in MAXIMUS_SERVICES.values()]
        assert len(ports) == len(set(ports))

    def test_service_ports_in_range(self):
        """Test all service ports are in expected range (8150-8157)"""
        for config in MAXIMUS_SERVICES.values():
            assert 8150 <= config["port"] <= 8157

    def test_service_has_required_fields(self):
        """Test each service has required configuration fields"""
        required_fields = ["name", "port", "description"]

        for service_id, config in MAXIMUS_SERVICES.items():
            for field in required_fields:
                assert field in config, f"Service {service_id} missing {field}"

    def test_critical_flag_exists(self):
        """Test critical flag exists for all services"""
        for config in MAXIMUS_SERVICES.values():
            assert "critical" in config
            assert isinstance(config["critical"], bool)


# ============================================================================
# 6. CONVENIENCE FUNCTIONS
# ============================================================================

class TestConvenienceFunctions:
    """Test convenience functions for health checks"""

    @pytest.mark.asyncio
    async def test_quick_health_check(self):
        """Test quick_health_check convenience function"""
        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200)):
            health_map, summary = await quick_health_check()

            assert isinstance(health_map, dict)
            assert isinstance(summary, dict)
            assert len(health_map) == 8

    def test_sync_health_check(self):
        """Test sync_health_check convenience function"""
        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200)):
            health_map, summary = sync_health_check()

            assert isinstance(health_map, dict)
            assert isinstance(summary, dict)


# ============================================================================
# 7. INTEGRATION TESTS
# ============================================================================

class TestHealthCheckIntegration:
    """Integration tests for complete health check flow"""

    @pytest.mark.asyncio
    async def test_complete_health_check_workflow(self):
        """Test complete health check workflow"""
        checker = HealthChecker(timeout=5.0, retries=1)

        response_data = {
            "status": "healthy",
            "version": "1.0.0",
            "uptime": 3600,
            "circuit_breaker": "closed"
        }

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200, response_data)):
            # Step 1: Check all services
            health_map = await checker.check_all_services()
            assert len(health_map) == 8

            # Step 2: Generate summary
            summary = checker.get_summary(health_map)
            assert summary["all_healthy"] is True

            # Step 3: Verify critical services
            assert len(summary["critical_down"]) == 0


# ============================================================================
# 8. CIRCUIT BREAKER STATUS
# ============================================================================

class TestCircuitBreakerStatus:
    """Test circuit breaker status detection"""

    @pytest.mark.asyncio
    async def test_circuit_breaker_closed_healthy(self):
        """Test circuit breaker status when service is healthy"""
        checker = HealthChecker(timeout=5.0)

        response_data = {
            "status": "healthy",
            "circuit_breaker": "closed"
        }

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200, response_data)):
            result = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])

            assert result.circuit_breaker_state == "closed"

    @pytest.mark.asyncio
    async def test_circuit_breaker_open_degraded(self):
        """Test circuit breaker status when circuit is open"""
        checker = HealthChecker(timeout=5.0)

        response_data = {
            "status": "degraded",
            "circuit_breaker": "open"
        }

        with patch('aiohttp.ClientSession', return_value=create_mock_aiohttp_session(200, response_data)):
            result = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])

            assert result.circuit_breaker_state == "open"


print("✅ Health Check test suite created!")
print("Categories: 8")
print("Total test methods: 24")
print("Coverage: Individual checks, parallel execution, errors, statistics, integration")
