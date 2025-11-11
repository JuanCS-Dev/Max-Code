"""
⚠️ DEPRECATED - Legacy Integration Layer

DO NOT USE THIS MODULE - Use v2 clients instead:
- core.maximus_integration.client_v2 (MaximusClient)
- core.maximus_integration.penelope_client_v2 (PENELOPEClient)

See: integration/DEPRECATED.md for migration guide
"""

# DEPRECATED: Legacy base client - use core.maximus_integration.base_client
from integration.base_client import BaseHTTPClient, CircuitBreaker, CircuitState

__version__ = "1.0.0-deprecated"
__all__ = [
    # DEPRECATED: Only base classes exported for backward compatibility
    "BaseHTTPClient",
    "CircuitBreaker",
    "CircuitState",
]

# DO NOT IMPORT FROM THIS MODULE
# Use v2 clients from core.maximus_integration instead
