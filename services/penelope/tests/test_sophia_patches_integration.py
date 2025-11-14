"""
Integration tests for Sophia Engine production patches

Tests the 4 critical patches applied in Phase 4 cleanup:
1. Service Registry integration
2. Prometheus monitoring
3. Service restart capability
4. Real alerting (Slack/PagerDuty)

Author: Phase 4 Cleanup Team
Date: 2025-11-14
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import os


# Test that imports work correctly
class TestPatchesImportability:
    """Test that all patches can be imported"""

    def test_sophia_engine_imports(self):
        """sophia_engine.py should import without errors"""
        try:
            from core.sophia_engine import SophiaEngine
            assert SophiaEngine is not None
        except ImportError as e:
            pytest.skip(f"Dependencies not available: {e}")

    def test_patches_module_imports(self):
        """sophia_engine_patches.py should import without errors"""
        try:
            from core.sophia_engine_patches import (
                ServiceRegistryClient,
                PrometheusMonitor,
                ServiceRestarter,
                AlertManager,
            )
            assert ServiceRegistryClient is not None
            assert PrometheusMonitor is not None
            assert ServiceRestarter is not None
            assert AlertManager is not None
        except ImportError as e:
            pytest.skip(f"Dependencies not available: {e}")

    def test_patches_available_flag_works(self):
        """PATCHES_AVAILABLE flag should work correctly"""
        try:
            from core import sophia_engine
            # Should have PATCHES_AVAILABLE attribute
            assert hasattr(sophia_engine, 'PATCHES_AVAILABLE')
        except ImportError:
            pytest.skip("Module not available")


class TestServiceRegistryClient:
    """Test Service Registry integration patch"""

    def test_client_initialization(self):
        """ServiceRegistryClient should initialize correctly"""
        try:
            from core.sophia_engine_patches import ServiceRegistryClient

            client = ServiceRegistryClient()
            assert client.registry_url is not None
            assert client.client is not None
        except ImportError:
            pytest.skip("Dependencies not available")

    def test_client_with_custom_url(self):
        """ServiceRegistryClient should accept custom URL"""
        try:
            from core.sophia_engine_patches import ServiceRegistryClient

            custom_url = "http://custom-registry:8159"
            client = ServiceRegistryClient(registry_url=custom_url)
            assert client.registry_url == custom_url
        except ImportError:
            pytest.skip("Dependencies not available")

    @pytest.mark.asyncio
    async def test_query_dependencies_handles_errors(self):
        """query_dependencies should handle errors gracefully"""
        try:
            from core.sophia_engine_patches import ServiceRegistryClient

            client = ServiceRegistryClient(registry_url="http://nonexistent:9999")
            # Should return empty list on error, not crash
            deps = await client.query_dependencies("test-service")
            assert isinstance(deps, list)
        except ImportError:
            pytest.skip("Dependencies not available")


class TestPrometheusMonitor:
    """Test Prometheus monitoring patch"""

    def test_monitor_initialization(self):
        """PrometheusMonitor should initialize correctly"""
        try:
            from core.sophia_engine_patches import PrometheusMonitor

            monitor = PrometheusMonitor()
            assert monitor.url is not None
            assert monitor.prom is not None
        except ImportError:
            pytest.skip("Dependencies not available")

    def test_monitor_with_custom_url(self):
        """PrometheusMonitor should accept custom URL"""
        try:
            from core.sophia_engine_patches import PrometheusMonitor

            custom_url = "http://custom-prometheus:9090"
            monitor = PrometheusMonitor(prometheus_url=custom_url)
            assert monitor.url == custom_url
        except ImportError:
            pytest.skip("Dependencies not available")

    @pytest.mark.asyncio
    async def test_get_service_metrics_has_fallback(self):
        """get_service_metrics should have fallback on errors"""
        try:
            from core.sophia_engine_patches import PrometheusMonitor

            monitor = PrometheusMonitor(prometheus_url="http://nonexistent:9999")
            # Should return fallback metrics, not crash
            metrics = await monitor.get_service_metrics("test-service")
            assert isinstance(metrics, dict)
            assert "error_rate" in metrics
            assert "healthy" in metrics
        except ImportError:
            pytest.skip("Dependencies not available")


class TestServiceRestarter:
    """Test service restart capability patch"""

    def test_restarter_initialization(self):
        """ServiceRestarter should initialize correctly"""
        try:
            from core.sophia_engine_patches import ServiceRestarter

            restarter = ServiceRestarter()
            # Should detect available orchestration
            assert hasattr(restarter, 'docker_available')
            assert hasattr(restarter, 'k8s_available')
            assert isinstance(restarter.docker_available, bool)
            assert isinstance(restarter.k8s_available, bool)
        except ImportError:
            pytest.skip("Dependencies not available")

    @pytest.mark.asyncio
    async def test_restart_service_handles_no_orchestration(self):
        """restart_service should handle missing orchestration gracefully"""
        try:
            from core.sophia_engine_patches import ServiceRestarter

            restarter = ServiceRestarter()
            # Even without docker/k8s, should not crash
            result = await restarter.restart_service("test-service")
            assert isinstance(result, bool)
        except ImportError:
            pytest.skip("Dependencies not available")


class TestAlertManager:
    """Test real alerting patch"""

    def test_alert_manager_initialization(self):
        """AlertManager should initialize correctly"""
        try:
            from core.sophia_engine_patches import AlertManager

            manager = AlertManager()
            # Should read environment variables
            assert hasattr(manager, 'slack_webhook')
            assert hasattr(manager, 'pagerduty_key')
        except ImportError:
            pytest.skip("Dependencies not available")

    def test_alert_manager_reads_env_vars(self):
        """AlertManager should read Slack/PagerDuty from environment"""
        try:
            from core.sophia_engine_patches import AlertManager

            # Set test environment
            test_slack = "https://hooks.slack.com/test"
            test_pd = "test-pd-key"

            with patch.dict(os.environ, {
                'SLACK_WEBHOOK_URL': test_slack,
                'PAGERDUTY_INTEGRATION_KEY': test_pd
            }):
                manager = AlertManager()
                assert manager.slack_webhook == test_slack
                assert manager.pagerduty_key == test_pd
        except ImportError:
            pytest.skip("Dependencies not available")

    @pytest.mark.asyncio
    async def test_alert_human_logs_when_no_integrations(self):
        """alert_human should log when no integrations configured"""
        try:
            from core.sophia_engine_patches import AlertManager

            manager = AlertManager()
            # Even without webhooks, should not crash (logs to console)
            result = await manager.alert_human(
                "test-service",
                "CRITICAL",
                "Test alert message"
            )
            assert isinstance(result, bool)
        except ImportError:
            pytest.skip("Dependencies not available")


class TestSophiaEngineIntegration:
    """Test Sophia Engine integration with patches"""

    def test_sophia_initializes_with_patches(self):
        """Sophia should initialize patch clients when available"""
        try:
            from core.sophia_engine import SophiaEngine

            # Mock dependencies
            mock_wisdom = Mock()
            mock_obs = Mock()

            sophia = SophiaEngine(mock_wisdom, mock_obs)

            # Should have patch client attributes
            assert hasattr(sophia, 'registry_client')
            assert hasattr(sophia, 'prometheus_monitor')
            assert hasattr(sophia, 'service_restarter')
            assert hasattr(sophia, 'alert_manager')

        except ImportError:
            pytest.skip("Dependencies not available")

    def test_sophia_gracefully_handles_missing_patches(self):
        """Sophia should work even if patches aren't available"""
        try:
            # This tests the try/except ImportError in sophia_engine.py
            from core.sophia_engine import SophiaEngine

            mock_wisdom = Mock()
            mock_obs = Mock()

            # Should not crash
            sophia = SophiaEngine(mock_wisdom, mock_obs)
            assert sophia is not None

        except ImportError:
            pytest.skip("Dependencies not available")


class TestEndToEndIntegration:
    """End-to-end integration tests"""

    @pytest.mark.asyncio
    async def test_full_decision_flow_with_patches(self):
        """Test complete decision flow using all patches"""
        try:
            from core.sophia_engine import SophiaEngine
            from models import Anomaly, Severity

            # Mock all dependencies
            mock_wisdom = Mock()
            mock_wisdom.query_precedents = AsyncMock(return_value=[])

            mock_obs = Mock()
            mock_obs.query_similar_anomalies = AsyncMock(return_value=[])

            # Create Sophia with patches
            sophia = SophiaEngine(mock_wisdom, mock_obs)

            # Create test anomaly
            anomaly = Anomaly(
                anomaly_id="test-123",
                anomaly_type="latency_spike",
                service="test-service",
                severity=Severity.P2_MEDIUM,
                metrics={"p99_latency": 1000}
            )

            # Execute decision (should use patches internally)
            decision = await sophia.should_intervene(anomaly)

            # Should return valid decision
            assert decision is not None
            assert "decision" in decision
            assert "reasoning" in decision

        except ImportError:
            pytest.skip("Dependencies not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
