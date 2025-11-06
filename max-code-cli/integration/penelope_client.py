"""
PENELOPE Service Client - 7 Fruits, Healing & Wisdom

Production HTTP client for PENELOPE Autonomous Healing System.
Based on real API endpoints from services/penelope/api/routes.py

Endpoints:
- GET  /api/v1/penelope/fruits/status       # 9 Frutos do Espírito status
- GET  /api/v1/penelope/virtues/metrics     # 3 Virtudes Teológicas métricas
- GET  /api/v1/penelope/healing/history     # Histórico de healing
- POST /api/v1/penelope/diagnose            # Diagnosticar anomalia
- GET  /api/v1/penelope/patches             # Lista de patches
- GET  /api/v1/penelope/wisdom              # Consultar Wisdom Base

Port: 8151 (Docker) | localhost:8151 (dev)
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
class FruitStatus(BaseModel):
    """Individual fruit status."""
    name: str
    score: float
    description: str
    metric: str
    status: str
    last_updated: str


class FruitsStatusResponse(BaseModel):
    """GET /api/v1/penelope/fruits/status response."""
    fruits: Dict[str, FruitStatus]
    overall_score: float
    healthy_fruits: int
    total_fruits: int
    biblical_reference: str
    last_updated: str


class VirtueMetrics(BaseModel):
    """Individual virtue metrics."""
    name: str
    score: float
    metrics: Dict[str, Any]
    biblical_reference: str
    status: str


class VirtuesMetricsResponse(BaseModel):
    """GET /api/v1/penelope/virtues/metrics response."""
    virtues: Dict[str, VirtueMetrics]
    overall_score: float
    theological_reference: str
    governance_framework: str
    last_updated: str


class HealingEvent(BaseModel):
    """Individual healing event."""
    event_id: str
    timestamp: str
    anomaly_type: str
    affected_service: str
    severity: str
    action_taken: str
    patch_applied: Optional[str]
    outcome: str
    resolution_time_seconds: int
    sophia_confidence: float


class HealingHistoryResponse(BaseModel):
    """GET /api/v1/penelope/healing/history response."""
    events: List[HealingEvent]
    total: int
    limit: int
    offset: int
    has_more: bool


class DiagnoseRequest(BaseModel):
    """POST /api/v1/penelope/diagnose request."""
    anomaly_id: str = Field(..., description="Unique anomaly identifier")
    anomaly_type: str = Field(..., description="Type of anomaly (e.g., latency_spike)")
    affected_service: str = Field(..., description="Service experiencing anomaly")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Relevant metrics")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class Precedent(BaseModel):
    """Historical precedent from Wisdom Base."""
    case_id: str
    similarity: float
    outcome: str
    patch_applied: str
    lessons_learned: str


class CausalChainStep(BaseModel):
    """Step in causal chain analysis."""
    step: int
    description: str
    confidence: float


class DiagnoseResponse(BaseModel):
    """POST /api/v1/penelope/diagnose response."""
    diagnosis_id: str
    anomaly_id: str
    root_cause: str
    confidence: float
    severity: str
    causal_chain: List[CausalChainStep]
    sophia_recommendation: str
    intervention_level: int
    precedents: List[Precedent]
    estimated_resolution_time_minutes: int
    biblical_wisdom: str
    diagnosed_at: str


class Patch(BaseModel):
    """Healing patch metadata."""
    patch_id: str
    diagnosis_id: str
    status: str
    patch_size_lines: int
    mansidao_score: float
    confidence: float
    affected_files: List[str]
    summary: str
    created_at: str
    deployed_at: Optional[str]
    failure_reason: Optional[str] = None


class PatchesResponse(BaseModel):
    """GET /api/v1/penelope/patches response."""
    patches: List[Patch]
    total: int
    filtered_by_status: Optional[str]
    limit: int


class WisdomPrecedent(BaseModel):
    """Precedent from Wisdom Base query."""
    case_id: str
    anomaly_type: str
    service: str
    patch_applied: str
    outcome: str
    lessons_learned: str
    similarity: float
    date: str


class WisdomBaseResponse(BaseModel):
    """GET /api/v1/penelope/wisdom response."""
    precedents: List[WisdomPrecedent]
    total_found: int
    query: Dict[str, Any]
    wisdom_note: str


if HTTPX_AVAILABLE:
    class PenelopeClient(BaseHTTPClient):
        """
        PENELOPE Service Client - Autonomous Healing.

        Example:
            client = PenelopeClient()
            fruits = client.get_fruits_status()
            print(f"Overall score: {fruits.overall_score}")
            print(f"Healthy fruits: {fruits.healthy_fruits}/{fruits.total_fruits}")
        """

        def __init__(self, base_url: str = "http://localhost:8151", **kwargs):
            super().__init__(base_url=base_url, **kwargs)
            self.api_prefix = "/api/v1/penelope"

        def get_fruits_status(self) -> FruitsStatusResponse:
            """
            Get status of 9 Fruits of the Spirit (Galatians 5:22-23).

            Returns:
                FruitsStatusResponse with all 9 fruits metrics
            """
            response = self.get(f"{self.api_prefix}/fruits/status")
            return FruitsStatusResponse(**response.json())

        def get_virtues_metrics(self) -> VirtuesMetricsResponse:
            """
            Get metrics for 3 Theological Virtues (1 Corinthians 13:13).

            Returns:
                VirtuesMetricsResponse with Sophia, Praotes, Tapeinophrosyne metrics
            """
            response = self.get(f"{self.api_prefix}/virtues/metrics")
            return VirtuesMetricsResponse(**response.json())

        def get_healing_history(
            self,
            limit: int = 50,
            offset: int = 0,
            severity: Optional[str] = None
        ) -> HealingHistoryResponse:
            """
            Get healing intervention history.

            Args:
                limit: Maximum number of events (1-500)
                offset: Pagination offset
                severity: Filter by severity (P0, P1, P2, P3)

            Returns:
                HealingHistoryResponse with paginated events
            """
            params = {"limit": limit, "offset": offset}
            if severity:
                params["severity"] = severity

            response = self.get(f"{self.api_prefix}/healing/history", params=params)
            return HealingHistoryResponse(**response.json())

        def diagnose_anomaly(self, diagnosis_request: DiagnoseRequest) -> DiagnoseResponse:
            """
            Diagnose anomaly and get intervention recommendation.

            Integrates with:
            - Sophia Engine: Decides whether to intervene
            - Causal AI: Identifies root cause
            - Wisdom Base: Searches historical precedents

            Args:
                diagnosis_request: Anomaly data

            Returns:
                DiagnoseResponse with root cause and recommendation
            """
            response = self.post(
                f"{self.api_prefix}/diagnose",
                json=diagnosis_request.model_dump()
            )
            return DiagnoseResponse(**response.json())

        def get_patches(
            self,
            status_filter: Optional[str] = None,
            limit: int = 20
        ) -> PatchesResponse:
            """
            Get list of generated healing patches.

            Args:
                status_filter: Filter by status (pending, validated, deployed, failed)
                limit: Maximum number of patches (1-100)

            Returns:
                PatchesResponse with patch metadata
            """
            params = {"limit": limit}
            if status_filter:
                params["status_filter"] = status_filter

            response = self.get(f"{self.api_prefix}/patches", params=params)
            return PatchesResponse(**response.json())

        def query_wisdom_base(
            self,
            anomaly_type: str,
            service: Optional[str] = None,
            similarity_threshold: float = 0.8
        ) -> WisdomBaseResponse:
            """
            Query Wisdom Base for historical precedents.

            Args:
                anomaly_type: Type of anomaly to search
                service: Filter by specific service (optional)
                similarity_threshold: Minimum similarity threshold (0.0-1.0)

            Returns:
                WisdomBaseResponse with similar historical cases
            """
            params = {
                "anomaly_type": anomaly_type,
                "similarity_threshold": similarity_threshold
            }
            if service:
                params["service"] = service

            response = self.get(f"{self.api_prefix}/wisdom", params=params)
            return WisdomBaseResponse(**response.json())

else:
    class PenelopeClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required: pip install httpx")
