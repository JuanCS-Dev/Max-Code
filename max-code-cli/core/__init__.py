"""
Max-Code CLI Core

Core integration and orchestration layer.
"""

from core.integration_manager import IntegrationManager, IntegrationMode, get_integration_manager

__all__ = [
    "IntegrationManager",
    "IntegrationMode",
    "get_integration_manager",
]
