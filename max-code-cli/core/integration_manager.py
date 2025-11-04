"""
Integration Manager

Manages MAXIMUS service connections with graceful degradation.
Works in 3 modes:
1. FULL - All MAXIMUS services available
2. PARTIAL - Some services available
3. STANDALONE - No services, direct Claude API only

This allows CLI to work even when MAXIMUS backend is not running.
"""

from typing import Dict, Any, Optional
from enum import Enum
import logging

from config.settings import get_settings
from integration import (
    MaximusClient,
    PenelopeClient,
    OrchestratorClient,
    OraculoClient,
    AtlasClient,
    ServiceHealth
)


class IntegrationMode(str, Enum):
    """Integration mode."""
    FULL = "full"           # All services available
    PARTIAL = "partial"     # Some services available
    STANDALONE = "standalone"  # No services, Claude API only


class IntegrationManager:
    """
    Manages MAXIMUS service integrations with graceful degradation.

    Features:
    - Automatic service discovery
    - Health monitoring
    - Graceful fallback to standalone mode
    - Connection pooling
    """

    def __init__(self):
        """Initialize integration manager."""
        self.logger = logging.getLogger(__name__)
        self.settings = get_settings()

        # Initialize clients
        self.maximus: Optional[MaximusClient] = None
        self.penelope: Optional[PenelopeClient] = None
        self.orchestrator: Optional[OrchestratorClient] = None
        self.oraculo: Optional[OraculoClient] = None
        self.atlas: Optional[AtlasClient] = None

        # Service availability
        self.service_health: Dict[str, ServiceHealth] = {}
        self.mode: IntegrationMode = IntegrationMode.STANDALONE

        # Initialize
        self._initialize_clients()
        self._check_service_health()

    def _initialize_clients(self):
        """Initialize service clients."""
        try:
            self.maximus = MaximusClient(
                self.settings.maximus.core_url,
                timeout=self.settings.maximus.timeout_seconds,
                max_retries=self.settings.maximus.max_retries
            )
            self.logger.debug("MaximusClient initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize MaximusClient: {e}")

        try:
            self.penelope = PenelopeClient(
                self.settings.maximus.penelope_url,
                timeout=self.settings.maximus.timeout_seconds,
                max_retries=self.settings.maximus.max_retries
            )
            self.logger.debug("PenelopeClient initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize PenelopeClient: {e}")

        try:
            self.orchestrator = OrchestratorClient(
                self.settings.maximus.orchestrator_url,
                timeout=self.settings.maximus.timeout_seconds,
                max_retries=self.settings.maximus.max_retries
            )
            self.logger.debug("OrchestratorClient initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize OrchestratorClient: {e}")

        try:
            self.oraculo = OraculoClient(
                self.settings.maximus.oraculo_url,
                timeout=self.settings.maximus.timeout_seconds,
                max_retries=self.settings.maximus.max_retries
            )
            self.logger.debug("OraculoClient initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize OraculoClient: {e}")

        try:
            self.atlas = AtlasClient(
                self.settings.maximus.atlas_url,
                timeout=self.settings.maximus.timeout_seconds,
                max_retries=self.settings.maximus.max_retries
            )
            self.logger.debug("AtlasClient initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize AtlasClient: {e}")

    def _check_service_health(self):
        """Check health of all services."""
        services = {
            "maximus": self.maximus,
            "penelope": self.penelope,
            "orchestrator": self.orchestrator,
            "oraculo": self.oraculo,
            "atlas": self.atlas
        }

        healthy_count = 0
        for name, client in services.items():
            if client:
                try:
                    health = client.health_check()
                    self.service_health[name] = health
                    if health == ServiceHealth.HEALTHY:
                        healthy_count += 1
                        self.logger.info(f"{name} service: HEALTHY")
                    else:
                        self.logger.warning(f"{name} service: {health.value}")
                except Exception as e:
                    self.service_health[name] = ServiceHealth.UNKNOWN
                    self.logger.error(f"{name} health check failed: {e}")
            else:
                self.service_health[name] = ServiceHealth.UNKNOWN

        # Determine mode
        total_services = len(services)
        if healthy_count == total_services:
            self.mode = IntegrationMode.FULL
            self.logger.info("Integration Mode: FULL (all services available)")
        elif healthy_count > 0:
            self.mode = IntegrationMode.PARTIAL
            self.logger.info(f"Integration Mode: PARTIAL ({healthy_count}/{total_services} services available)")
        else:
            self.mode = IntegrationMode.STANDALONE
            self.logger.info("Integration Mode: STANDALONE (no services available, using Claude API directly)")

    def get_mode(self) -> IntegrationMode:
        """Get current integration mode."""
        return self.mode

    def is_service_available(self, service_name: str) -> bool:
        """
        Check if service is available.

        Args:
            service_name: Service name (maximus, penelope, etc.)

        Returns:
            True if service is healthy
        """
        health = self.service_health.get(service_name, ServiceHealth.UNKNOWN)
        return health == ServiceHealth.HEALTHY

    def get_consciousness_state(self) -> Optional[Dict[str, Any]]:
        """
        Get consciousness state if available.

        Returns:
            Consciousness metrics or None if unavailable
        """
        if not self.is_service_available("maximus"):
            return None

        try:
            response = self.maximus.get_consciousness_state()
            if response.success:
                return response.data
        except Exception as e:
            self.logger.error(f"Failed to get consciousness state: {e}")

        return None

    def evaluate_ethics(self, action_description: str) -> Optional[Dict[str, Any]]:
        """
        Evaluate action against 7 Biblical Articles.

        Args:
            action_description: Description of action

        Returns:
            Ethics evaluation or None if unavailable
        """
        if not self.is_service_available("penelope"):
            return None

        try:
            action = {"description": action_description}
            response = self.penelope.evaluate_against_articles(action)
            if response.success:
                return response.data
        except Exception as e:
            self.logger.error(f"Failed to evaluate ethics: {e}")

        return None

    def is_sabbath(self) -> bool:
        """
        Check if Sabbath mode is active.

        Returns:
            True if Sabbath, False otherwise (default to False if unavailable)
        """
        if not self.is_service_available("penelope"):
            return False

        try:
            return self.penelope.is_sabbath()
        except Exception as e:
            self.logger.error(f"Failed to check Sabbath: {e}")
            return False

    def get_service_summary(self) -> Dict[str, Any]:
        """
        Get summary of all services.

        Returns:
            Dictionary with service status
        """
        return {
            "mode": self.mode.value,
            "services": {
                name: health.value
                for name, health in self.service_health.items()
            },
            "claude_api_available": bool(self.settings.claude.api_key),
            "features": {
                "consciousness": self.is_service_available("maximus"),
                "ethics": self.is_service_available("penelope"),
                "orchestration": self.is_service_available("orchestrator"),
                "prediction": self.is_service_available("oraculo"),
                "context": self.is_service_available("atlas"),
            }
        }

    def close(self):
        """Close all service connections."""
        clients = [
            self.maximus,
            self.penelope,
            self.orchestrator,
            self.oraculo,
            self.atlas
        ]

        for client in clients:
            if client:
                try:
                    client.close()
                except Exception as e:
                    self.logger.error(f"Error closing client: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Singleton instance
_integration_manager: Optional[IntegrationManager] = None


def get_integration_manager() -> IntegrationManager:
    """
    Get singleton integration manager.

    Returns:
        IntegrationManager instance
    """
    global _integration_manager
    if _integration_manager is None:
        _integration_manager = IntegrationManager()
    return _integration_manager
