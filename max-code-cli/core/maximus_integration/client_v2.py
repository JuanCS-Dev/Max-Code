"""
MaximusClient SDK v2.0 - Refactored using Anthropic SDK Best Practices

Improvements over v1:
1. Resource-based architecture (Anthropic pattern)
2. Proper HTTP client management with context managers
3. Type-safe request/response using Pydantic
4. Sync/Async support
5. Matches ACTUAL backend API (from OpenAPI schema)
6. Inherits from BaseMaximusClient (shared logic)

Biblical Foundation:
"Porque com sabedoria se edifica a casa, e com a inteligência ela se firma"
(Provérbios 24:3)
"""

from typing import Dict, Any, List, Optional, AsyncIterator
from pydantic import BaseModel, Field
from enum import Enum
from contextlib import asynccontextmanager
import logging
import asyncio

from config.settings import get_settings
from .base_client import (
    BaseMaximusClient,
    BaseSyncMaximusClient,
    BaseMaximusError,
    BaseMaximusConnectionError,
    BaseMaximusAPIError,
    BaseMaximusTimeoutError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# EXCEPTIONS (MAXIMUS-specific, inherit from base)
# ============================================================================

class MaximusError(BaseMaximusError):
    """Base exception for all Maximus SDK errors"""
    pass


class MaximusConnectionError(BaseMaximusConnectionError, MaximusError):
    """Raised when connection to backend fails"""
    pass


class MaximusAPIError(BaseMaximusAPIError, MaximusError):
    """Raised when API returns error response"""
    pass


class MaximusTimeoutError(BaseMaximusTimeoutError, MaximusError):
    """Raised when request exceeds timeout"""
    pass


# ============================================================================
# MODELS (Pydantic for type safety)
# ============================================================================

class TIGMetrics(BaseModel):
    """TIG Fabric metrics"""
    node_count: int
    edge_count: int
    density: float
    avg_clustering_coefficient: float
    avg_path_length: float
    algebraic_connectivity: float
    effective_connectivity_index: float
    has_feed_forward_bottlenecks: bool
    bottleneck_locations: List[Any]
    min_path_redundancy: int
    avg_latency_us: float
    max_latency_us: float
    total_bandwidth_gbps: float
    last_update: float


class ConsciousnessState(BaseModel):
    """Consciousness state from /api/consciousness/state (REAL SCHEMA)"""
    timestamp: str
    esgt_active: bool
    arousal_level: float = Field(..., ge=0.0, le=1.0)
    arousal_classification: str  # "relaxed", "alert", etc.
    tig_metrics: TIGMetrics
    recent_events_count: int
    system_health: str  # "HEALTHY", "DEGRADED", etc.


class ArousalLevel(BaseModel):
    """Arousal level (REAL SCHEMA)"""
    arousal: float = Field(..., ge=0.0, le=1.0)
    level: str  # "relaxed", "alert", "focused", etc.
    baseline: float = Field(..., ge=0.0, le=1.0)
    need_contribution: float
    temporal_contribution: float
    timestamp: str


class SafetyStatus(BaseModel):
    """Safety system status"""
    enabled: bool
    violations_count: int
    emergency_shutdown_available: bool


class QueryRequest(BaseModel):
    """Request for /query endpoint"""
    query: str
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = 4096


class QueryResponse(BaseModel):
    """Response from /query endpoint (REAL SCHEMA)"""
    final_response: str
    confidence_score: float
    processing_time_seconds: float
    timestamp: str
    raw_reasoning_output: Dict[str, Any]
    tool_execution_results: List[Any]
    reflection_notes: str


class GovernanceDecision(BaseModel):
    """HITL decision from governance queue"""
    decision_id: str
    action_type: str
    description: str
    risk_level: str
    timestamp: str
    requires_approval: bool
    operator_id: Optional[str] = None


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    message: Optional[str] = None
    components: Optional[Dict[str, Any]] = None


# ============================================================================
# RESOURCES (Anthropic pattern: organize by domain)
# ============================================================================

class ConsciousnessResource:
    """
    Consciousness API resource.

    Provides access to:
    - Arousal management
    - ESGT event handling
    - Safety monitoring
    - Reactive fabric orchestration
    """

    def __init__(self, client: 'MaximusClient'):
        self._client = client

    async def get_state(self) -> ConsciousnessState:
        """Get current consciousness state"""
        response = await self._client._request("GET", "/api/consciousness/state")
        return ConsciousnessState(**response)

    async def get_arousal(self) -> ArousalLevel:
        """Get current arousal level"""
        response = await self._client._request("GET", "/api/consciousness/arousal")
        return ArousalLevel(**response)

    async def adjust_arousal(self, target_level: float) -> ArousalLevel:
        """Adjust arousal to target level (0.0-1.0)"""
        response = await self._client._request(
            "POST",
            "/api/consciousness/arousal/adjust",
            json={"target_level": target_level}
        )
        return ArousalLevel(**response)

    async def get_safety_status(self) -> SafetyStatus:
        """Get safety system status"""
        response = await self._client._request("GET", "/api/consciousness/safety/status")
        return SafetyStatus(**response)

    async def trigger_esgt(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger ESGT event"""
        return await self._client._request(
            "POST",
            "/api/consciousness/esgt/trigger",
            json={"event_type": event_type, "data": data}
        )

    async def get_esgt_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent ESGT events"""
        response = await self._client._request(
            "GET",
            "/api/consciousness/esgt/events",
            params={"limit": limit}
        )
        return response.get("events", [])

    async def get_metrics(self) -> Dict[str, Any]:
        """Get consciousness metrics"""
        return await self._client._request("GET", "/api/consciousness/metrics")

    async def emergency_shutdown(self, reason: str) -> Dict[str, Any]:
        """Trigger emergency safety shutdown"""
        return await self._client._request(
            "POST",
            "/api/consciousness/safety/emergency-shutdown",
            json={"reason": reason}
        )


class GovernanceResource:
    """
    Governance API resource (HITL - Human-in-the-Loop).

    Provides access to:
    - Pending decisions queue
    - Decision approvals/rejections
    - Operator sessions
    - SSE streaming of governance events
    """

    def __init__(self, client: 'MaximusClient'):
        self._client = client

    async def get_pending(self, operator_id: Optional[str] = None) -> List[GovernanceDecision]:
        """Get pending decisions"""
        params = {"operator_id": operator_id} if operator_id else {}
        response = await self._client._request(
            "GET",
            "/api/v1/governance/pending",
            params=params
        )
        return [GovernanceDecision(**d) for d in response.get("decisions", [])]

    async def get_decision(self, decision_id: str) -> GovernanceDecision:
        """Get specific decision"""
        response = await self._client._request("GET", f"/api/v1/governance/decision/{decision_id}")
        return GovernanceDecision(**response)

    async def approve(self, decision_id: str, operator_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Approve a decision"""
        return await self._client._request(
            "POST",
            f"/api/v1/governance/decision/{decision_id}/approve",
            json={"operator_id": operator_id, "reason": reason}
        )

    async def reject(self, decision_id: str, operator_id: str, reason: str) -> Dict[str, Any]:
        """Reject a decision"""
        return await self._client._request(
            "POST",
            f"/api/v1/governance/decision/{decision_id}/reject",
            json={"operator_id": operator_id, "reason": reason}
        )

    async def escalate(self, decision_id: str, operator_id: str, reason: str) -> Dict[str, Any]:
        """Escalate a decision"""
        return await self._client._request(
            "POST",
            f"/api/v1/governance/decision/{decision_id}/escalate",
            json={"operator_id": operator_id, "reason": reason}
        )

    async def create_session(
        self,
        operator_id: str,
        operator_name: str,
        operator_role: str = "soc_operator",
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create operator session"""
        payload = {
            "operator_id": operator_id,
            "operator_name": operator_name,
            "operator_role": operator_role,
        }
        if ip_address:
            payload["ip_address"] = ip_address
        if user_agent:
            payload["user_agent"] = user_agent

        return await self._client._request(
            "POST",
            "/api/v1/governance/session/create",
            json=payload
        )

    async def get_session_stats(self, operator_id: str) -> Dict[str, Any]:
        """Get operator session statistics"""
        return await self._client._request(
            "GET",
            f"/api/v1/governance/session/{operator_id}/stats"
        )

    async def stream_events(self, operator_id: str, session_id: str) -> AsyncIterator[Dict[str, Any]]:
        """
        Stream governance events via SSE.

        Example:
            async for event in client.governance.stream_events(operator_id, session_id):
                print(f"New decision: {event}")
        """
        async with self._client._http_client.stream(
            "GET",
            f"{self._client.base_url}/api/v1/governance/stream/{operator_id}",
            params={"session_id": session_id},
            timeout=None  # SSE streams don't timeout
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    import json
                    yield json.loads(line[6:])


# ============================================================================
# MAIN CLIENT (Anthropic pattern)
# ============================================================================

class MaximusClient(BaseMaximusClient):
    """
    Async client for MAXIMUS AI backend (v2.0 - Anthropic pattern).

    Improvements over v1:
    - Resource-based API (consciousness, governance)
    - Proper async/await with context managers
    - Type-safe requests/responses (Pydantic)
    - Matches ACTUAL backend API (not fictitious)
    - Follows Anthropic SDK best practices
    - Inherits shared logic from BaseMaximusClient

    Example:
        async with MaximusClient() as client:
            # Health check
            health = await client.health()
            print(f"Status: {health.status}")

            # Query endpoint (natural language)
            response = await client.query("Analyze this code for issues")
            print(response.answer)

            # Consciousness API
            state = await client.consciousness.get_state()
            print(f"Arousal: {state.arousal_level}")

            # Governance API
            decisions = await client.governance.get_pending()
            for decision in decisions:
                await client.governance.approve(decision.decision_id, "operator1")
    """

    def _get_default_base_url(self) -> str:
        """Get default MAXIMUS Core URL from settings"""
        settings = get_settings()
        return settings.maximus.core_url.rstrip('/')

    def _get_api_key_env_var(self) -> str:
        """Get API key environment variable name"""
        return "MAXIMUS_API_KEY"

    def _get_connection_error_class(self):
        """Get MAXIMUS-specific connection error class"""
        return MaximusConnectionError

    def _get_api_error_class(self):
        """Get MAXIMUS-specific API error class"""
        return MaximusAPIError

    def _get_timeout_error_class(self):
        """Get MAXIMUS-specific timeout error class"""
        return MaximusTimeoutError

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        api_key: Optional[str] = None,
    ):
        """
        Initialize Maximus client.

        Args:
            base_url: Backend URL (default: from settings)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Max retry attempts (default: 3)
            api_key: API key for authentication (optional)
        """
        settings = get_settings()

        # Set base_url using settings if not provided
        if base_url is None:
            base_url = settings.maximus.core_url.rstrip('/')

        # Set timeout using settings if not provided
        if timeout is None:
            timeout = settings.maximus.timeout_seconds

        # Initialize base class
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            api_key=api_key,
        )

        # Resources (Anthropic pattern)
        self.consciousness = ConsciousnessResource(self)
        self.governance = GovernanceResource(self)

    # _request() method inherited from BaseMaximusClient - no duplication! ✅

    # ========================================================================
    # TOP-LEVEL METHODS (Not resource-specific)
    # ========================================================================

    async def health(self) -> HealthCheck:
        """
        Check backend health.

        Returns:
            HealthCheck with status and components

        Example:
            health = await client.health()
            if health.status == "healthy":
                print("✓ Backend is online")
        """
        response = await self._request("GET", "/health")  # Inherited from base class
        return HealthCheck(**response)

    async def query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
    ) -> QueryResponse:
        """
        Process natural language query.

        This is the main endpoint for general AI queries.
        Use this for:
        - Code analysis
        - Systemic impact analysis (instead of /api/v1/mape-k/analyze)
        - Ethical reviews (instead of /api/v1/ethical/review)
        - Edge case prediction (instead of /api/v1/predictive-coding/edge-cases)

        Args:
            query: Natural language query
            context: Optional context (code, project info, etc.)
            max_tokens: Maximum response tokens

        Returns:
            QueryResponse with answer and metadata

        Example:
            # Systemic analysis (replaces old analyze_systemic_impact)
            response = await client.query(
                "Analyze the systemic impact of changing the authentication system",
                context={"codebase": "...", "change": "..."}
            )

            # Ethical review (replaces old ethical_review)
            response = await client.query(
                "Perform ethical review of this feature using Kantian and Virtue ethics",
                context={"feature": "user tracking"}
            )
        """
        request = QueryRequest(query=query, context=context, max_tokens=max_tokens)
        response = await self._request("POST", "/query", json=request.dict())
        return QueryResponse(**response)


# ============================================================================
# SYNCHRONOUS CLIENT (Optional - for non-async codebases)
# ============================================================================

class SyncMaximusClient:
    """
    Synchronous wrapper around MaximusClient.

    Use this if your codebase doesn't support async/await.
    For async code, use MaximusClient directly.

    Example:
        with SyncMaximusClient() as client:
            health = client.health()
            response = client.query("Analyze this code")
    """

    def __init__(self, **kwargs):
        import asyncio
        self._async_client = MaximusClient(**kwargs)
        self._loop = asyncio.new_event_loop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._loop.run_until_complete(self._async_client.close())
        self._loop.close()

    def health(self) -> HealthCheck:
        return self._loop.run_until_complete(self._async_client.health())

    def query(self, query: str, **kwargs) -> QueryResponse:
        return self._loop.run_until_complete(self._async_client.query(query, **kwargs))

    # Delegate to resources
    @property
    def consciousness(self):
        return self._async_client.consciousness

    @property
    def governance(self):
        return self._async_client.governance


# ============================================================================
# CONVENIENCE FUNCTION (Anthropic pattern)
# ============================================================================

@asynccontextmanager
async def create_client(**kwargs) -> MaximusClient:
    """
    Create and manage Maximus client lifecycle.

    Example:
        async with create_client() as client:
            health = await client.health()
    """
    client = MaximusClient(**kwargs)
    try:
        yield client
    finally:
        await client.close()
