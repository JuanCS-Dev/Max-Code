"""
MAXIMUS Core Service Client

Interfaces with MAXIMUS Core for:
- Consciousness system (ESGT ignition, TIG, MMEI, MCEA)
- Predictive coding (5-layer hierarchy)
- Neuromodulation (DA, ACh, NE, 5-HT)
- Skill learning (Hybrid RL)
- Attention system
- Ethical AI stack

PRODUCTION IMPLEMENTATION
"""

from typing import Dict, Any, Optional
from integration.base_client import BaseServiceClient, ServiceResponse


class MaximusClient(BaseServiceClient):
    """
    Client for MAXIMUS Core Service.

    The heart of the AI system - provides consciousness, prediction,
    and neuromodulation capabilities.
    """

    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize MAXIMUS Core client.

        Args:
            base_url: MAXIMUS Core service URL
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        super().__init__(base_url, "MAXIMUS Core", timeout, max_retries)

    # ========================================================================
    # CONSCIOUSNESS SYSTEM
    # ========================================================================

    def get_consciousness_state(self) -> ServiceResponse:
        """
        Get current complete consciousness state.

        Returns:
            ServiceResponse with:
            - timestamp: Current time
            - esgt_active: Whether ESGT is active
            - arousal_level: Current arousal (0-1)
            - arousal_classification: Arousal level name
            - tig_metrics: TIG fabric metrics
            - recent_events_count: Number of recent events
            - system_health: Overall health status
        """
        return self.get("/api/consciousness/state")

    def trigger_esgt_event(self, salience: Dict[str, float], context: Optional[Dict[str, Any]] = None) -> ServiceResponse:
        """
        Manually trigger ESGT ignition event.

        Args:
            salience: Dict with 'novelty', 'relevance', 'urgency' (0-1)
            context: Additional context for the event

        Returns:
            ServiceResponse with ignition result
        """
        payload = {
            "novelty": salience.get("novelty", 0.5),
            "relevance": salience.get("relevance", 0.5),
            "urgency": salience.get("urgency", 0.5),
            "context": context or {}
        }
        return self.post("/api/consciousness/trigger", json=payload)

    # ========================================================================
    # PREDICTIVE CODING
    # ========================================================================

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> ServiceResponse:
        """
        Process query through MAXIMUS integrated system.

        Args:
            query: Natural language query
            context: Additional context

        Returns:
            ServiceResponse with processed result
        """
        payload = {
            "query": query,
            "context": context or {}
        }
        return self.post("/api/process", json=payload)

    # ========================================================================
    # NEUROMODULATION
    # ========================================================================

    def adjust_arousal(self, delta: float, duration: float = 5.0, source: str = "cli") -> ServiceResponse:
        """
        Adjust arousal level for neuromodulation.

        Args:
            delta: Arousal change (-0.5 to +0.5)
            duration: Duration in seconds
            source: Source identifier

        Returns:
            ServiceResponse with new arousal state
        """
        payload = {
            "delta": max(-0.5, min(0.5, delta)),
            "duration_seconds": duration,
            "source": source
        }
        return self.post("/api/consciousness/arousal", json=payload)

    def get_arousal_level(self) -> ServiceResponse:
        """
        Get current arousal level.

        Returns:
            ServiceResponse with arousal metrics
        """
        response = self.get_consciousness_state()
        if response.success and response.data:
            arousal_data = {
                "arousal_level": response.data.get("arousal_level"),
                "classification": response.data.get("arousal_classification"),
                "timestamp": response.data.get("timestamp")
            }
            return ServiceResponse(success=True, data=arousal_data)
        return response

    # ========================================================================
    # EVENT HISTORY
    # ========================================================================

    def get_recent_events(self, limit: int = 10) -> ServiceResponse:
        """
        Get recent consciousness events.

        Args:
            limit: Maximum number of events

        Returns:
            ServiceResponse with event history
        """
        return self.get(f"/api/consciousness/events?limit={limit}")

    def get_event_by_id(self, event_id: str) -> ServiceResponse:
        """
        Get specific consciousness event by ID.

        Args:
            event_id: Event identifier

        Returns:
            ServiceResponse with event details
        """
        return self.get(f"/api/consciousness/events/{event_id}")

    # ========================================================================
    # SAFETY & MONITORING
    # ========================================================================

    def get_safety_status(self) -> ServiceResponse:
        """
        Get safety protocol status.

        Returns:
            ServiceResponse with safety metrics
        """
        return self.get("/api/consciousness/safety/status")

    def get_metrics(self) -> ServiceResponse:
        """
        Get Prometheus metrics.

        Returns:
            ServiceResponse with metrics data
        """
        return self.get("/metrics")

    # ========================================================================
    # INTEGRATION HELPER
    # ========================================================================

    def is_conscious(self) -> bool:
        """
        Check if consciousness system is active.

        Returns:
            True if ESGT is active
        """
        response = self.get_consciousness_state()
        if response.success and response.data:
            return response.data.get("esgt_active", False)
        return False

    def get_consciousness_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Get consciousness metrics summary.

        Returns:
            Dictionary with key metrics or None
        """
        response = self.get_consciousness_state()
        if response.success and response.data:
            return {
                "esgt_active": response.data.get("esgt_active"),
                "arousal_level": response.data.get("arousal_level"),
                "arousal_class": response.data.get("arousal_classification"),
                "events_count": response.data.get("recent_events_count"),
                "health": response.data.get("system_health"),
                "timestamp": response.data.get("timestamp")
            }
        return None
