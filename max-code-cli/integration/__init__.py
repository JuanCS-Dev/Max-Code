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

from integration.base_client import BaseServiceClient, ServiceResponse, ServiceHealth
from integration.maximus_client import MaximusClient
from integration.penelope_client import PenelopeClient
from integration.orchestrator_client import OrchestratorClient
from integration.oraculo_client import OraculoClient
from integration.atlas_client import AtlasClient

__version__ = "1.0.0"
__all__ = [
    # Base classes
    "BaseServiceClient",
    "ServiceResponse",
    "ServiceHealth",

    # Service clients
    "MaximusClient",
    "PenelopeClient",
    "OrchestratorClient",
    "OraculoClient",
    "AtlasClient",
]
