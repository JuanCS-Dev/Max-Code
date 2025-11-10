"""Consciousness Checker - GWT metrics (Claude)"""
import logging
from dataclasses import dataclass
from typing import Dict, Optional
from .backend_client import MaximusClient

logger = logging.getLogger(__name__)

@dataclass
class ConsciousnessReport:
    aware: bool
    gw_broadcast_score: float
    integration_score: float
    self_model_score: float
    narrative_coherence: float
    overall_score: float
    analysis: str

class ConsciousnessChecker:
    """Check code awareness using Global Workspace Theory"""
    def __init__(self, client=None):
        self.client = client or MaximusClient()
        self._owns_client = client is None
    
    async def check_awareness(self, code: str) -> ConsciousnessReport:
        """Check consciousness metrics (Claude Extended Thinking)"""
        result = await self.client.call_service("consciousness-core", {
            "code": code, "metrics": ["gw_broadcast", "integration", "self_model", "narrative"], "extended_thinking": True
        })
        return ConsciousnessReport(
            aware=result.get("aware", False),
            gw_broadcast_score=result.get("gw_broadcast", 0.0),
            integration_score=result.get("integration", 0.0),
            self_model_score=result.get("self_model", 0.0),
            narrative_coherence=result.get("narrative", 0.0),
            overall_score=result.get("overall_score", 0.0),
            analysis=result.get("analysis", "")
        )
    
    async def close(self):
        if self._owns_client: await self.client.close()
