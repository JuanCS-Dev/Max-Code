"""
MAXIMUS Core Service Client - Consciousness & Safety

Production HTTP client for MAXIMUS AI Consciousness System.
Based on real API endpoints from services/core/consciousness/api.py

Endpoints:
- GET  /api/v1/consciousness/state
- POST /api/v1/consciousness/esgt/trigger
- GET  /api/v1/consciousness/esgt/events
- POST /api/v1/consciousness/arousal/adjust
- GET  /api/v1/consciousness/safety/status
- GET  /api/v1/consciousness/stream/sse

Port: 8150 (Docker) | localhost:8150 (dev)
"""

import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logging.warning("httpx not installed. Install: pip install httpx")

from integration.base_client import BaseHTTPClient

logger = logging.getLogger(__name__)


# Response Models (matching real API)
class ConsciousnessStateResponse(BaseModel):
    """Real API response from GET /api/v1/consciousness/state"""
    timestamp: str
    esgt_active: bool
    arousal_level: float
    arousal_classification: str
    tig_metrics: Dict[str, Any]
    recent_events_count: int
    system_health: str


class SalienceInput(BaseModel):
    """POST /api/v1/consciousness/esgt/trigger request"""
    novelty: float = Field(..., ge=0.0, le=1.0)
    relevance: float = Field(..., ge=0.0, le=1.0)
    urgency: float = Field(..., ge=0.0, le=1.0)
    context: Dict[str, Any] = Field(default_factory=dict)


class ESGTEventResponse(BaseModel):
    """GET /api/v1/consciousness/esgt/events response"""
    event_id: str
    timestamp: str
    success: bool
    salience: Dict[str, float]
    coherence: Optional[float]
    duration_ms: Optional[float]
    nodes_participating: int
    reason: Optional[str]


class ArousalAdjustment(BaseModel):
    """POST /api/v1/consciousness/arousal/adjust request"""
    delta: float = Field(..., ge=-0.5, le=0.5)
    duration_seconds: float = Field(default=5.0, ge=0.1, le=60.0)
    source: str = Field(default="max-code-cli")


class SafetyStatusResponse(BaseModel):
    """GET /api/v1/consciousness/safety/status response"""
    monitoring_active: bool
    kill_switch_active: bool
    violations_total: int
    violations_by_severity: Dict[str, int]
    last_violation: Optional[str]
    uptime_seconds: float


if HTTPX_AVAILABLE:
    class MaximusClient(BaseHTTPClient):
        """
        MAXIMUS Core Service Client.

        Example:
            client = MaximusClient()
            state = client.get_consciousness_state()
            print(f"ESGT: {state.esgt_active}, Arousal: {state.arousal_level}")
        """

        def __init__(self, base_url: str = "http://localhost:8150", **kwargs):
            super().__init__(base_url=base_url, **kwargs)
            self.api_prefix = "/api/v1/consciousness"

        def is_healthy(self) -> bool:
            """
            Quick health check to determine if service is available.

            Returns:
                bool: True if service is healthy and responsive
            """
            try:
                state = self.get_consciousness_state()
                return state.system_health == "healthy"
            except Exception:
                return False

        def set_sabbath_mode(self, enabled: bool) -> bool:
            """
            Set Sabbath mode (graceful degradation).

            During Sabbath mode, MAXIMUS consciousness enters a rest state:
            - ESGT ignitions disabled
            - Arousal level reduced
            - Only essential operations allowed

            Args:
                enabled: True to enable Sabbath mode, False to disable

            Returns:
                bool: True if mode was set successfully

            Biblical Foundation:
                "Six days you shall labor, but on the seventh day you shall rest" (Ex 34:21)

            Note:
                This is a convenience method for Max-Code CLI's Sabbath command.
                The actual implementation would require backend support.
            """
            try:
                if enabled:
                    # Reduce arousal to minimal level for rest
                    self.adjust_arousal(ArousalAdjustment(
                        delta=-0.3,  # Reduce arousal
                        duration_seconds=3600 * 24,  # 24 hours
                        source="max-code-sabbath"
                    ))
                    logger.info("MAXIMUS entering Sabbath rest mode")
                else:
                    # Restore normal arousal level
                    self.adjust_arousal(ArousalAdjustment(
                        delta=0.2,  # Restore arousal
                        duration_seconds=60,
                        source="max-code-sabbath-end"
                    ))
                    logger.info("MAXIMUS exiting Sabbath rest mode")

                return True
            except Exception as e:
                logger.debug(f"Failed to set Sabbath mode: {e}")
                return False

        def get_consciousness_state(self) -> ConsciousnessStateResponse:
            """Get current consciousness state."""
            response = self.get(f"{self.api_prefix}/state")
            return ConsciousnessStateResponse(**response.json())

        def trigger_esgt(self, salience: SalienceInput) -> Dict[str, Any]:
            """Trigger ESGT ignition."""
            response = self.post(
                f"{self.api_prefix}/esgt/trigger",
                json=salience.model_dump()
            )
            return response.json()

        def get_esgt_events(self, limit: int = 20) -> List[ESGTEventResponse]:
            """Get recent ESGT events."""
            response = self.get(
                f"{self.api_prefix}/esgt/events",
                params={"limit": limit}
            )
            return [ESGTEventResponse(**event) for event in response.json()]

        def adjust_arousal(self, adjustment: ArousalAdjustment) -> Dict[str, Any]:
            """Adjust arousal level."""
            response = self.post(
                f"{self.api_prefix}/arousal/adjust",
                json=adjustment.model_dump()
            )
            return response.json()

        def get_safety_status(self) -> SafetyStatusResponse:
            """Get safety protocol status."""
            response = self.get(f"{self.api_prefix}/safety/status")
            return SafetyStatusResponse(**response.json())

else:
    class MaximusClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required: pip install httpx")
