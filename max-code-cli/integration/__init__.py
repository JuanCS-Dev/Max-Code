"""
MAXIMUS AI Integration Layer

Connects Max-Code CLI with MAXIMUS backend services:
- MAXIMUS Core (consciousness, predictive coding, neuromodulation)
- Penelope (NLP, healing, 7 Biblical Articles)
- Orchestrator (workflow coordination)
- Oraculo (prediction, forecasting)
- Atlas (context, environment)

All clients are production-ready with real implementations!
"""

from integration.base_client import BaseHTTPClient, CircuitBreaker, CircuitState
from integration.maximus_client import MaximusClient
from integration.penelope_client import PenelopeClient
from integration.oraculo_client import OraculoClient

__version__ = "1.0.0"
__all__ = [
    # Base classes
    "BaseHTTPClient",
    "CircuitBreaker",
    "CircuitState",

    # Service clients (FASE 6 - 3/8 implemented)
    "MaximusClient",
    "PenelopeClient",
    "OraculoClient",

    # TODO FASE 7+:
    # "OrchestratorClient",
    # "MABAClient",
    # "NISClient",
    # "EurekaClient",
]
