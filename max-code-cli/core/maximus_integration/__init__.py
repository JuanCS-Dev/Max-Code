"""
MAXIMUS AI Integration Layer

This module provides integration between Max-Code CLI and MAXIMUS AI backend,
enabling hybrid decision-making that combines:
- Max-Code: Constitutional code generation (processing layer)
- MAXIMUS: Bio-inspired cognitive analysis (noble AI layer)

Components:
- MaximusClient: Main SDK for MAXIMUS API calls
- DecisionFusion: Merge decisions from both systems
- FallbackSystem: Graceful degradation when MAXIMUS offline
- PENELOPE/MABA/NIS Clients: TRINITY service integration

Usage:
    from core.maximus_integration import MaximusClient, DecisionFusion

    client = MaximusClient()
    fusion = DecisionFusion()

    # Check health
    if await client.health_check():
        # Hybrid mode
        maximus_analysis = await client.analyze_systemic_impact(action, context)
        decision = fusion.fuse(maxcode_decision, maximus_analysis)
    else:
        # Standalone mode
        decision = maxcode_decision
"""

from .client import (
    MaximusClient,
    SystemicAnalysis,
    EthicalVerdict,
    EthicalFramework,
    EdgeCase,
    EdgeCaseSeverity,
    FixOption,
    HealingSuggestion,
    SearchResult,
    MABASearchResult,
    Narrative,
    MaximusOfflineError,
    MaximusTimeoutError,
    MaximusAPIError,
)

from .decision_fusion import (
    DecisionFusion,
    FusedDecision,
    FusionMethod,
)

from .fallback import (
    FallbackSystem,
    FallbackResult,
    FallbackMode,
)

from .penelope_client import PENELOPEClient
from .maba_client import MABAClient
from .nis_client import NISClient
from .cache import MaximusCache

__all__ = [
    # Main client
    "MaximusClient",
    "SystemicAnalysis",
    "EthicalVerdict",
    "EthicalFramework",
    "EdgeCase",
    "EdgeCaseSeverity",
    "FixOption",
    "HealingSuggestion",
    "SearchResult",
    "MABASearchResult",
    "Narrative",
    "MaximusOfflineError",
    "MaximusTimeoutError",
    "MaximusAPIError",
    # Decision fusion
    "DecisionFusion",
    "FusedDecision",
    "FusionMethod",
    # Fallback
    "FallbackSystem",
    "FallbackResult",
    "FallbackMode",
    # TRINITY clients
    "PENELOPEClient",
    "MABAClient",
    "NISClient",
    # Cache
    "MaximusCache",
]

__version__ = "2.0.0"
