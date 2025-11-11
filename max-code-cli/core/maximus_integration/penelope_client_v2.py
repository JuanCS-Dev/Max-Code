"""
PENELOPE Client SDK v2.0 - Refactored using Anthropic SDK Best Practices

PENELOPE (Παράκλησις - Paraklesis): Sistema de Cura de Código baseado nos 7 Frutos
do Espírito e 3 Virtudes Teológicas.

Improvements over v1:
1. Resource-based architecture (Anthropic pattern)
2. Proper HTTP client management with context managers
3. Type-safe request/response using Pydantic
4. Sync/Async support
5. Matches ACTUAL backend API (from OpenAPI schema)

Biblical Foundation:
"Mas o fruto do Espírito é: amor, alegria, paz, paciência, bondade,
fidelidade, mansidão, domínio próprio. Contra estas coisas não há lei."
(Gálatas 5:22-23)

"Agora, pois, permanecem a fé, a esperança e o amor, estes três;
porém o maior destes é o amor."
(1 Coríntios 13:13)
"""

import httpx
from typing import Dict, Any, List, Optional, AsyncIterator
from pydantic import BaseModel, Field
from enum import Enum
from contextlib import asynccontextmanager
from datetime import datetime
import logging

from config.settings import get_settings

logger = logging.getLogger(__name__)


# ============================================================================
# EXCEPTIONS (Following Anthropic pattern)
# ============================================================================

class PENELOPEError(Exception):
    """Base exception for all PENELOPE SDK errors"""
    pass


class PENELOPEConnectionError(PENELOPEError):
    """Raised when connection to PENELOPE backend fails"""
    pass


class PENELOPEAPIError(PENELOPEError):
    """Raised when API returns error response"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class PENELOPETimeoutError(PENELOPEError):
    """Raised when request exceeds timeout"""
    pass


# ============================================================================
# MODELS (Pydantic for type safety)
# ============================================================================

class FruitStatus(str, Enum):
    """Status dos Frutos do Espírito"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class Fruit(BaseModel):
    """Individual Fruit of the Spirit"""
    name: str  # e.g., "Amor (Ἀγάπη)"
    score: float = Field(..., ge=0.0, le=1.0)
    description: str
    metric: str
    status: FruitStatus
    last_updated: str


class FruitsStatus(BaseModel):
    """Status dos 7 Frutos do Espírito (REAL SCHEMA)"""
    fruits: Dict[str, Fruit]
    overall_score: float = Field(..., ge=0.0, le=1.0)
    healthy_fruits: int
    total_fruits: int
    biblical_reference: str  # "Gálatas 5:22-23"
    last_updated: str


class VirtueMetrics(BaseModel):
    """Metrics for a theological virtue"""
    # Dynamic fields - varies by virtue
    pass


class Virtue(BaseModel):
    """Individual Theological Virtue (Sophia, Praotes, Tapeinophrosyne)"""
    name: str
    score: float = Field(..., ge=0.0, le=1.0)
    metrics: Dict[str, Any]  # Varies by virtue
    biblical_reference: str
    status: str


class VirtuesMetrics(BaseModel):
    """Métricas das 3 Virtudes Teológicas (REAL SCHEMA)"""
    virtues: Dict[str, Virtue]
    overall_score: float = Field(..., ge=0.0, le=1.0)
    theological_reference: str  # "1 Coríntios 13:13"
    governance_framework: str  # "7 Biblical Articles"
    last_updated: str


class DiagnoseRequest(BaseModel):
    """Request for code diagnosis"""
    code: str
    language: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class DiagnoseResponse(BaseModel):
    """Response from code diagnosis"""
    diagnosis_id: str
    issues: List[Dict[str, Any]]
    severity: str
    recommendations: List[str]
    healing_patches: Optional[List[str]] = None
    confidence: float
    timestamp: str


class HealingPatch(BaseModel):
    """Healing patch for code (REAL SCHEMA)"""
    patch_id: str
    diagnosis_id: str
    status: str  # "deployed", "validated", "failed"
    patch_size_lines: int
    mansidao_score: float  # Mansidão (Gentleness) score
    confidence: float
    affected_files: List[str]
    summary: str
    created_at: str
    deployed_at: Optional[str] = None
    failure_reason: Optional[str] = None


class HealingEvent(BaseModel):
    """Individual healing event"""
    event_id: str
    timestamp: str
    anomaly_type: str
    affected_service: str
    severity: str  # P0, P1, P2
    action_taken: str  # "intervene", "observe", "escalate"
    patch_applied: Optional[str] = None
    outcome: str  # "success", "self_healed", "human_intervention"
    resolution_time_seconds: int
    sophia_confidence: float


class HealingHistory(BaseModel):
    """History of healing operations (REAL SCHEMA)"""
    events: List[HealingEvent]
    total: int
    limit: int
    offset: int
    has_more: bool


class WisdomQuery(BaseModel):
    """Query to PENELOPE wisdom base"""
    query: str
    context: Optional[Dict[str, Any]] = None


class WisdomResponse(BaseModel):
    """Response from wisdom base"""
    answer: str
    precedents: List[Dict[str, Any]]
    biblical_references: List[str]
    confidence: float
    timestamp: str


class AudioSynthesizeRequest(BaseModel):
    """Request to synthesize audio (voice of PENELOPE)"""
    text: str
    voice: Optional[str] = "penelope"  # Greek feminine voice
    speed: Optional[float] = 1.0


class AudioSynthesizeResponse(BaseModel):
    """Response from audio synthesis"""
    audio_url: str
    duration_seconds: float
    format: str
    timestamp: str


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    components: Dict[str, str]
    virtues_status: Dict[str, str]
    sabbath_mode: bool
    timestamp: str


# ============================================================================
# RESOURCES (Anthropic pattern: organize by domain)
# ============================================================================

class HealingResource:
    """
    Healing API resource.

    Provides access to:
    - Code diagnosis (identify issues)
    - Healing patches (automated fixes)
    - Healing history (audit trail)
    """

    def __init__(self, client: 'PENELOPEClient'):
        self._client = client

    async def diagnose(
        self,
        code: str,
        language: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> DiagnoseResponse:
        """
        Diagnose code issues using PENELOPE wisdom.

        Args:
            code: Source code to diagnose
            language: Programming language (auto-detect if None)
            context: Additional context (project info, etc.)

        Returns:
            DiagnoseResponse with issues and recommendations

        Example:
            diagnosis = await client.healing.diagnose(
                code="def foo(): return bar",
                language="python"
            )
            print(f"Found {len(diagnosis.issues)} issues")
        """
        request = DiagnoseRequest(code=code, language=language, context=context)
        response = await self._client._request(
            "POST",
            "/api/v1/penelope/diagnose",
            json=request.dict(exclude_none=True)
        )
        return DiagnoseResponse(**response)

    async def get_patches(self, diagnosis_id: Optional[str] = None) -> List[HealingPatch]:
        """
        Get available healing patches.

        Args:
            diagnosis_id: Filter by specific diagnosis (optional)

        Returns:
            List of available healing patches
        """
        params = {"diagnosis_id": diagnosis_id} if diagnosis_id else {}
        response = await self._client._request(
            "GET",
            "/api/v1/penelope/patches",
            params=params
        )
        return [HealingPatch(**p) for p in response.get("patches", [])]

    async def get_history(
        self,
        limit: int = 100,
        status: Optional[str] = None
    ) -> HealingHistory:
        """
        Get healing history.

        Args:
            limit: Max number of entries to return
            status: Filter by status (successful/failed/all)

        Returns:
            HealingHistory with past healing operations
        """
        params = {"limit": limit}
        if status:
            params["status"] = status

        response = await self._client._request(
            "GET",
            "/api/v1/penelope/healing/history",
            params=params
        )
        return HealingHistory(**response)


class SpiritualResource:
    """
    Spiritual Metrics API resource.

    Provides access to:
    - 7 Fruits of the Spirit status
    - 3 Theological Virtues metrics
    - Biblical governance framework
    """

    def __init__(self, client: 'PENELOPEClient'):
        self._client = client

    async def get_fruits_status(self) -> FruitsStatus:
        """
        Get status of the 7 Fruits of the Spirit.

        Returns:
            FruitsStatus with all 9 fruits:
            - Amor (Ἀγάπη) - Love
            - Alegria (Χαρά) - Joy
            - Paz (Εἰρήνη) - Peace
            - Paciência (Μακροθυμία) - Patience
            - Bondade (Χρηστότης) - Kindness
            - Fidelidade (Πίστις) - Faithfulness
            - Mansidão (Πραότης) - Gentleness
            - Domínio Próprio (Ἐγκράτεια) - Self-control
            - Gentileza (Ἀγαθωσύνη) - Goodness

        Example:
            fruits = await client.spiritual.get_fruits_status()
            print(f"Overall score: {fruits.overall_score}")
            for name, fruit in fruits.fruits.items():
                print(f"{fruit.name}: {fruit.score:.2f} ({fruit.status})")
        """
        response = await self._client._request("GET", "/api/v1/penelope/fruits/status")
        return FruitsStatus(**response)

    async def get_virtues_metrics(self) -> VirtuesMetrics:
        """
        Get metrics for the 3 Theological Virtues.

        Returns:
            VirtuesMetrics with:
            - Sophia (Σοφία) - Wisdom
            - Praotes (Πραότης) - Gentleness
            - Tapeinophrosyne (Ταπεινοφροσύνη) - Humility

        Example:
            virtues = await client.spiritual.get_virtues_metrics()
            print(f"Overall virtue score: {virtues.overall_score}")

            sophia = virtues.virtues['sophia']
            print(f"Wisdom interventions: {sophia.metrics['interventions_approved']}")
        """
        response = await self._client._request("GET", "/api/v1/penelope/virtues/metrics")
        return VirtuesMetrics(**response)


class WisdomResource:
    """
    Wisdom API resource.

    Provides access to:
    - PENELOPE wisdom base (precedents, best practices)
    - Biblical references
    - Architectural guidance
    """

    def __init__(self, client: 'PENELOPEClient'):
        self._client = client

    async def query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> WisdomResponse:
        """
        Query PENELOPE wisdom base.

        Args:
            query: Wisdom query (e.g., "How to handle authentication?")
            context: Optional context

        Returns:
            WisdomResponse with answer, precedents, and biblical references

        Example:
            wisdom = await client.wisdom.query(
                "How should I handle user authentication securely?"
            )
            print(wisdom.answer)
            print(f"Biblical reference: {wisdom.biblical_references}")
        """
        request = WisdomQuery(query=query, context=context)
        response = await self._client._request(
            "GET",
            "/api/v1/penelope/wisdom",
            params={"q": query}
        )
        return WisdomResponse(**response)


class AudioResource:
    """
    Audio API resource.

    Provides access to:
    - Audio synthesis (PENELOPE's voice)
    - Text-to-speech with Greek feminine voice
    """

    def __init__(self, client: 'PENELOPEClient'):
        self._client = client

    async def synthesize(
        self,
        text: str,
        voice: str = "penelope",
        speed: float = 1.0
    ) -> AudioSynthesizeResponse:
        """
        Synthesize audio from text (PENELOPE's voice).

        Args:
            text: Text to synthesize
            voice: Voice model (default: "penelope")
            speed: Speech speed (0.5 - 2.0)

        Returns:
            AudioSynthesizeResponse with audio URL

        Example:
            audio = await client.audio.synthesize(
                "Παράκλησις - The Comforter brings healing"
            )
            print(f"Audio ready: {audio.audio_url}")
        """
        request = AudioSynthesizeRequest(text=text, voice=voice, speed=speed)
        response = await self._client._request(
            "POST",
            "/api/v1/penelope/audio/synthesize",
            json=request.dict()
        )
        return AudioSynthesizeResponse(**response)


# ============================================================================
# MAIN CLIENT (Anthropic pattern)
# ============================================================================

class PENELOPEClient:
    """
    Async client for PENELOPE AI backend (v2.0 - Anthropic pattern).

    PENELOPE (Παράκλησις - Paraklesis): The Comforter
    Sistema de Cura de Código baseado nos 7 Frutos do Espírito e 3 Virtudes.

    Improvements over v1:
    - Resource-based API (healing, spiritual, wisdom, audio)
    - Proper async/await with context managers
    - Type-safe requests/responses (Pydantic)
    - Matches ACTUAL backend API (not fictitious)
    - Follows Anthropic SDK best practices

    Example:
        async with PENELOPEClient() as client:
            # Health check
            health = await client.health()
            print(f"Status: {health.status}")

            # Code diagnosis
            diagnosis = await client.healing.diagnose(
                code="def foo(): return bar",
                language="python"
            )

            # Spiritual metrics
            fruits = await client.spiritual.get_fruits_status()
            print(f"Overall fruit score: {fruits.overall_score}")

            # Wisdom query
            wisdom = await client.wisdom.query("How to handle errors?")
            print(wisdom.answer)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        api_key: Optional[str] = None,
    ):
        """
        Initialize PENELOPE client.

        Args:
            base_url: Backend URL (default: from settings)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Max retry attempts (default: 3)
            api_key: API key for authentication (optional)
        """
        settings = get_settings()

        self.base_url = (base_url or settings.maximus.penelope_url).rstrip('/')
        self.timeout = timeout or settings.maximus.timeout_seconds
        self.max_retries = max_retries
        self.api_key = api_key

        # HTTP client (httpx with connection pooling)
        self._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            headers={"User-Agent": "MaxCodeCLI/2.0-PENELOPE"},
        )

        # Resources (Anthropic pattern)
        self.healing = HealingResource(self)
        self.spiritual = SpiritualResource(self)
        self.wisdom = WisdomResource(self)
        self.audio = AudioResource(self)

    async def __aenter__(self):
        """Context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        await self.close()

    async def close(self):
        """Close HTTP client"""
        await self._http_client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
        retries: int = 0,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retries.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., "/health")
            json: Request body (for POST/PUT)
            params: Query parameters
            retries: Current retry count

        Returns:
            Response JSON data

        Raises:
            PENELOPEConnectionError: Connection failed
            PENELOPEAPIError: API returned error
            PENELOPETimeoutError: Request timed out
        """
        url = f"{self.base_url}{path}"

        try:
            response = await self._http_client.request(
                method,
                url,
                json=json,
                params=params,
            )

            # Raise for 4xx/5xx
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise PENELOPEAPIError(
                    f"API error: {response.status_code} {response.reason_phrase}",
                    status_code=response.status_code,
                    response=error_data
                )

            return response.json()

        except httpx.TimeoutException as e:
            if retries < self.max_retries:
                logger.warning(f"Request timeout, retry {retries + 1}/{self.max_retries}")
                return await self._request(method, path, json=json, params=params, retries=retries + 1)
            raise PENELOPETimeoutError(f"Request timed out after {self.max_retries} retries") from e

        except httpx.ConnectError as e:
            if retries < self.max_retries:
                logger.warning(f"Connection failed, retry {retries + 1}/{self.max_retries}")
                return await self._request(method, path, json=json, params=params, retries=retries + 1)
            raise PENELOPEConnectionError(f"Failed to connect to {self.base_url}") from e

        except PENELOPEAPIError:
            raise  # Don't retry on API errors

    # ========================================================================
    # TOP-LEVEL METHODS (Not resource-specific)
    # ========================================================================

    async def health(self) -> HealthCheck:
        """
        Check PENELOPE backend health.

        Returns:
            HealthCheck with status and components

        Example:
            health = await client.health()
            if health.status == "healthy":
                print("✓ PENELOPE is online")
                print(f"Sabbath mode: {health.sabbath_mode}")
        """
        response = await self._request("GET", "/health")
        return HealthCheck(**response)


# ============================================================================
# SYNCHRONOUS CLIENT (Optional - for non-async codebases)
# ============================================================================

class SyncPENELOPEClient:
    """
    Synchronous wrapper around PENELOPEClient.

    Use this if your codebase doesn't support async/await.
    For async code, use PENELOPEClient directly.

    Example:
        with SyncPENELOPEClient() as client:
            health = client.health()
            diagnosis = client.healing.diagnose(code="...")
    """

    def __init__(self, **kwargs):
        import asyncio
        self._async_client = PENELOPEClient(**kwargs)
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

    # Delegate to resources
    @property
    def healing(self):
        return self._async_client.healing

    @property
    def spiritual(self):
        return self._async_client.spiritual

    @property
    def wisdom(self):
        return self._async_client.wisdom

    @property
    def audio(self):
        return self._async_client.audio


# ============================================================================
# CONVENIENCE FUNCTION (Anthropic pattern)
# ============================================================================

@asynccontextmanager
async def create_client(**kwargs) -> PENELOPEClient:
    """
    Create and manage PENELOPE client lifecycle.

    Example:
        async with create_client() as client:
            health = await client.health()
    """
    client = PENELOPEClient(**kwargs)
    try:
        yield client
    finally:
        await client.close()
