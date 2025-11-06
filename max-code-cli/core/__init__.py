"""
Max-Code CLI Core

Core integration and orchestration layer.
"""

from core.integration_manager import IntegrationManager, IntegrationMode, ServiceHealth, get_integration_manager

__all__ = [
    "IntegrationManager",
    "IntegrationMode",
    "ServiceHealth",
    "get_integration_manager",
]
