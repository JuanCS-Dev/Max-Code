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
from integration.orchestrator_client import OrchestratorClient
from integration.simple_clients import MABAClient, NISClient, EurekaClient, DLQMonitorClient

__version__ = "1.0.0"
__all__ = [
    # Base classes
    "BaseHTTPClient",
    "CircuitBreaker",
    "CircuitState",

    # Service clients (FASE 6 - 8/8 COMPLETE!)
    "MaximusClient",      # port 8150 - Consciousness
    "PenelopeClient",     # port 8151 - 7 Fruits, Healing
    "NISClient",          # port 8153 - Narrative Intelligence
    "OrchestratorClient", # port 8154 - Workflow Coordination
    "EurekaClient",       # port 8155 - Insights & Discovery
    "OraculoClient",      # port 8156 - Predictions
    "DLQMonitorClient",   # port 8157 - Dead Letter Queue
    "MABAClient",         # port 8152 - Browser Agent
]
