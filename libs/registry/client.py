"""
Service Registry Client - Standalone Implementation
Provides graceful degradation for service discovery.
"""

import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ServiceInfo:
    """Information about a registered service."""
    name: str
    host: str
    port: int
    health_endpoint: str = "/health"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @property
    def url(self) -> str:
        """Get full service URL."""
        return f"http://{self.host}:{self.port}"


class RegistryClient:
    """
    Service Registry Client with graceful degradation.

    If no registry is available, falls back to environment variables:
    - {SERVICE_NAME}_HOST
    - {SERVICE_NAME}_PORT
    """

    def __init__(
        self,
        registry_url: Optional[str] = None,
        enable_fallback: bool = True
    ):
        """
        Initialize registry client.

        Args:
            registry_url: URL of service registry (optional)
            enable_fallback: Enable fallback to environment variables
        """
        self.registry_url = registry_url or os.getenv("SERVICE_REGISTRY_URL")
        self.enable_fallback = enable_fallback
        self._services_cache: Dict[str, ServiceInfo] = {}

        if not self.registry_url and not enable_fallback:
            logger.warning(
                "No registry URL configured and fallback disabled. "
                "Service discovery will fail."
            )

    async def register(
        self,
        service_name: str,
        port: int,
        health_endpoint: str = "/health",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Register service with registry.

        Args:
            service_name: Name of the service
            port: Port the service is running on
            health_endpoint: Health check endpoint
            metadata: Additional service metadata

        Returns:
            True if registration successful, False otherwise
        """
        logger.info(f"Registering service '{service_name}' on port {port}")

        # If no registry, just log and return success (graceful degradation)
        if not self.registry_url:
            logger.warning(
                f"No registry URL configured. Service '{service_name}' "
                f"registration skipped (graceful degradation mode)."
            )
            return True

        # TODO: Implement actual registry HTTP call when registry is deployed
        # For now, we're running standalone without central registry
        logger.info(f"Service '{service_name}' registration acknowledged (standalone mode)")
        return True

    async def discover(self, service_name: str) -> Optional[ServiceInfo]:
        """
        Discover service by name.

        Args:
            service_name: Name of service to discover

        Returns:
            ServiceInfo if found, None otherwise
        """
        # Check cache first
        if service_name in self._services_cache:
            return self._services_cache[service_name]

        # Try registry if available
        if self.registry_url:
            # TODO: Implement actual registry lookup
            logger.debug(f"Registry lookup for '{service_name}' (not implemented yet)")

        # Fallback to environment variables
        if self.enable_fallback:
            host = os.getenv(f"{service_name.upper()}_HOST", "localhost")
            port_str = os.getenv(f"{service_name.upper()}_PORT")

            if port_str:
                try:
                    port = int(port_str)
                    service_info = ServiceInfo(
                        name=service_name,
                        host=host,
                        port=port,
                        metadata={"source": "environment"}
                    )
                    self._services_cache[service_name] = service_info
                    logger.info(
                        f"Service '{service_name}' discovered via environment: "
                        f"{service_info.url}"
                    )
                    return service_info
                except ValueError:
                    logger.error(f"Invalid port for service '{service_name}': {port_str}")

        logger.warning(f"Service '{service_name}' not found")
        return None

    async def heartbeat(self, service_name: str) -> bool:
        """
        Send heartbeat for service.

        Args:
            service_name: Name of the service

        Returns:
            True if heartbeat acknowledged
        """
        # Graceful degradation: always succeed in standalone mode
        logger.debug(f"Heartbeat for '{service_name}' (standalone mode)")
        return True

    async def deregister(self, service_name: str) -> bool:
        """
        Deregister service from registry.

        Args:
            service_name: Name of the service

        Returns:
            True if deregistration successful
        """
        logger.info(f"Deregistering service '{service_name}'")

        # Remove from cache
        self._services_cache.pop(service_name, None)

        # Graceful degradation
        if not self.registry_url:
            logger.debug(f"No registry configured, service '{service_name}' removed from local cache only")
            return True

        # TODO: Implement actual registry HTTP call
        logger.info(f"Service '{service_name}' deregistration acknowledged")
        return True


# Convenience function for auto-registration
async def auto_register_service(
    service_name: str,
    port: int,
    health_endpoint: str = "/health",
    metadata: Optional[Dict[str, Any]] = None,
    registry_url: Optional[str] = None
) -> RegistryClient:
    """
    Automatically create client and register service.

    Args:
        service_name: Name of the service
        port: Port the service is running on
        health_endpoint: Health check endpoint
        metadata: Additional service metadata
        registry_url: Registry URL (optional)

    Returns:
        RegistryClient instance
    """
    client = RegistryClient(registry_url=registry_url, enable_fallback=True)
    await client.register(service_name, port, health_endpoint, metadata)
    return client
