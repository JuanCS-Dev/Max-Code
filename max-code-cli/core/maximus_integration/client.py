"""
MaximusClient SDK

Main client for communicating with MAXIMUS AI backend.
Handles all REST API calls to MAXIMUS Core and TRINITY services.

v2.1: Refactored to use centralized settings (FASE 3.3)

Biblical Foundation:
"Porque com sabedoria se edifica a casa, e com a inteligência ela se firma"
(Provérbios 24:3)
"""

import asyncio
import aiohttp
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from config.settings import get_settings
from config.logging_config import get_logger

logger = get_logger(__name__)


# ============================================================================
# EXCEPTIONS
# ============================================================================

class MaximusOfflineError(Exception):
    """Raised when MAXIMUS backend is offline"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MaximusTimeoutError(Exception):
    """Raised when MAXIMUS call exceeds timeout"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MaximusAPIError(Exception):
    """Raised when MAXIMUS API returns error"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SystemicAnalysis:
    """Result from MAXIMUS systemic impact analysis"""
    systemic_risk_score: float  # 0.0 (low) to 1.0 (high)
    side_effects: List[str]
    mitigation_strategies: List[str]
    affected_components: List[str]
    confidence: float
    reasoning: str


class EthicalFramework(str, Enum):
    """Ethical reasoning frameworks"""
    KANTIAN = "kantian"
    VIRTUE = "virtue"
    CONSEQUENTIALIST = "consequentialist"
    PRINCIPLISM = "principlism"


@dataclass
class EthicalVerdict:
    """Result from MAXIMUS ethical review"""
    kantian_score: float  # 0-100
    virtue_score: float  # 0-100
    consequentialist_score: float  # 0-100
    principlism_score: float  # 0-100
    verdict: str  # "APPROVED" | "REJECTED" | "CONDITIONAL"
    reasoning: str
    issues: List[str]
    recommendations: List[str]


class EdgeCaseSeverity(str, Enum):
    """Edge case severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class EdgeCase:
    """Predicted edge case from MAXIMUS"""
    scenario: str
    probability: float  # 0.0 to 1.0
    severity: EdgeCaseSeverity
    suggested_test: str
    reasoning: str


@dataclass
class FixOption:
    """Healing fix option"""
    description: str
    code: str
    confidence: float
    side_effects: List[str]


@dataclass
class HealingSuggestion:
    """Result from PENELOPE healing"""
    root_cause: str
    fix_suggestions: List[FixOption]
    confidence: float
    analysis: str


@dataclass
class SearchResult:
    """MABA search result"""
    title: str
    url: str
    snippet: str
    relevance: float


@dataclass
class MABASearchResult:
    """Result from MABA search"""
    results: List[SearchResult]
    confidence: float
    query_understanding: str


@dataclass
class Narrative:
    """Result from NIS narrative generation"""
    story: str
    key_insights: List[str]
    visualization_data: Dict[str, Any]
    confidence: float


# ============================================================================
# MAXIMUS CLIENT
# ============================================================================

class MaximusClient:
    """
    Main SDK for MAXIMUS AI backend communication.

    This client provides methods for:
    - Systemic impact analysis (MAPE-K)
    - Ethical reasoning (4 frameworks)
    - Edge case prediction (Predictive Coding)
    - Code healing (PENELOPE)
    - Web search (MABA)
    - Narrative generation (NIS)

    Example:
        client = MaximusClient(base_url="http://localhost:8153")

        # Check health
        if await client.health_check():
            # Analyze systemic impact
            analysis = await client.analyze_systemic_impact(
                action={"type": "code_change", "file": "auth.py"},
                context={"codebase": "..."}
            )
            logger.info(f"Systemic risk: {analysis.systemic_risk_score}")
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        backoff_factor: float = 1.5,
        auth_token: Optional[str] = None,
    ):
        """
        Initialize MAXIMUS client.

        Args:
            base_url: MAXIMUS Core base URL (default: from settings)
            timeout: Request timeout in seconds (default: from settings)
            max_retries: Maximum retry attempts (default: from settings)
            backoff_factor: Exponential backoff factor (default: 1.5)
            auth_token: OAuth token for authentication (default: from env CLAUDE_CODE_OAUTH_TOKEN)
        """
        # Load settings
        settings = get_settings()

        # Use provided values or fallback to settings
        self.base_url = (base_url or settings.maximus.core_url).rstrip("/")
        self.timeout = timeout if timeout is not None else float(settings.maximus.timeout_seconds)
        self.max_retries = max_retries if max_retries is not None else settings.maximus.max_retries
        self.backoff_factor = backoff_factor

        # Auth token (API key only - OAuth removed)
        if auth_token:
            self.auth_token = auth_token
        else:
            # Try to get from settings (which reads from env)
            self.auth_token = settings.claude.api_key

        # TRINITY service URLs (from settings)
        self.penelope_url = settings.maximus.penelope_url.rstrip("/")
        self.maba_url = settings.maximus.maba_url.rstrip("/")
        self.nis_url = settings.maximus.nis_url.rstrip("/")

        # Session (reuse connection pool)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self):
        """Close client session"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(
        self,
        method: str,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc)
            url: Full URL
            json: JSON payload
            retry_count: Current retry attempt

        Returns:
            Response JSON

        Raises:
            MaximusOfflineError: If MAXIMUS is offline
            MaximusTimeoutError: If request times out
            MaximusAPIError: If API returns error
        """
        session = await self._get_session()

        # Build headers
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        try:
            start_time = time.time()

            async with session.request(method, url, json=json, headers=headers) as response:
                latency = (time.time() - start_time) * 1000  # ms

                if response.status == 200:
                    data = await response.json()
                    return {"data": data, "latency_ms": latency}

                elif response.status >= 500:
                    # Server error - retry
                    if retry_count < self.max_retries:
                        await asyncio.sleep(self.backoff_factor ** retry_count)
                        return await self._request(method, url, json, retry_count + 1)
                    else:
                        raise MaximusAPIError(
                            f"MAXIMUS API error {response.status}: {await response.text()}"
                        )

                else:
                    # Client error - don't retry
                    raise MaximusAPIError(
                        f"MAXIMUS API error {response.status}: {await response.text()}"
                    )

        except asyncio.TimeoutError:
            if retry_count < self.max_retries:
                await asyncio.sleep(self.backoff_factor ** retry_count)
                return await self._request(method, url, json, retry_count + 1)
            else:
                raise MaximusTimeoutError(f"Request to {url} timed out after {self.timeout}s")

        except aiohttp.ClientConnectorError:
            raise MaximusOfflineError(f"Cannot connect to MAXIMUS at {url}")

    # ========================================================================
    # HEALTH CHECK
    # ========================================================================

    async def health_check(self) -> bool:
        """
        Check if MAXIMUS is online and healthy.

        Returns:
            True if MAXIMUS is healthy, False otherwise

        Example:
            if await client.health_check():
                logger.info("✓ MAXIMUS is online")
            else:
                logger.warning("✗ MAXIMUS is offline")
        """
        try:
            response = await self._request("GET", f"{self.base_url}/api/v1/health")
            return response["data"].get("status") == "healthy"
        except (MaximusOfflineError, MaximusTimeoutError, MaximusAPIError):
            return False

    # ========================================================================
    # SYSTEMIC ANALYSIS (MAPE-K)
    # ========================================================================

    async def analyze_systemic_impact(
        self,
        action: Dict[str, Any],
        context: Dict[str, Any],
    ) -> SystemicAnalysis:
        """
        Analyze systemic impact of an action using MAXIMUS MAPE-K loop.

        This calls MAXIMUS Core to perform deep systemic analysis,
        considering side effects, dependencies, and ripple effects.

        Args:
            action: Action to analyze (e.g., {"type": "code_change", "file": "auth.py"})
            context: Context information (codebase, dependencies, etc)

        Returns:
            SystemicAnalysis with risk score, side effects, and mitigations

        Example:
            analysis = await client.analyze_systemic_impact(
                action={"type": "refactor", "module": "authentication"},
                context={"dependencies": ["user_service", "session_manager"]}
            )

            if analysis.systemic_risk_score > 0.7:
                logger.warning(f"⚠️ High systemic risk: {analysis.reasoning}")
                for mitigation in analysis.mitigation_strategies:
                    logger.info(f"  → {mitigation}")
        """
        payload = {"action": action, "context": context}

        response = await self._request(
            "POST",
            f"{self.base_url}/api/v1/analyze",
            json=payload
        )

        data = response["data"]

        return SystemicAnalysis(
            systemic_risk_score=data["systemic_risk_score"],
            side_effects=data["side_effects"],
            mitigation_strategies=data["mitigation_strategies"],
            affected_components=data["affected_components"],
            confidence=data["confidence"],
            reasoning=data["reasoning"],
        )

    # ========================================================================
    # ETHICAL REVIEW
    # ========================================================================

    async def ethical_review(
        self,
        code: str,
        context: Dict[str, Any],
    ) -> EthicalVerdict:
        """
        Perform ethical review using MAXIMUS 4 ethical frameworks.

        MAXIMUS evaluates code through 4 lenses:
        1. Kantian: Universal principles (duty-based)
        2. Virtue Ethics: Character and intentions
        3. Consequentialist: Outcomes and impacts
        4. Principlism: Bioethical principles (autonomy, beneficence, etc)

        Args:
            code: Code to review
            context: Context (purpose, affected users, etc)

        Returns:
            EthicalVerdict with scores and verdict

        Example:
            verdict = await client.ethical_review(
                code=auth_code,
                context={"purpose": "user authentication", "stores_pii": True}
            )

            if verdict.verdict == "REJECTED":
                logger.error(f"❌ Ethical violation: {verdict.reasoning}")
                for issue in verdict.issues:
                    logger.info(f"  → {issue}")
        """
        payload = {"code": code, "context": context}

        response = await self._request(
            "POST",
            f"{self.base_url}/api/v1/ethical_review",
            json=payload
        )

        data = response["data"]

        return EthicalVerdict(
            kantian_score=data["kantian_score"],
            virtue_score=data["virtue_score"],
            consequentialist_score=data["consequentialist_score"],
            principlism_score=data["principlism_score"],
            verdict=data["verdict"],
            reasoning=data["reasoning"],
            issues=data["issues"],
            recommendations=data["recommendations"],
        )

    # ========================================================================
    # EDGE CASE PREDICTION (PREDICTIVE CODING)
    # ========================================================================

    async def predict_edge_cases(
        self,
        function_code: str,
        test_suite: List[str],
    ) -> List[EdgeCase]:
        """
        Predict edge cases using MAXIMUS Predictive Coding Network.

        MAXIMUS uses Karl Friston's free energy minimization to predict
        scenarios not covered by current test suite.

        Args:
            function_code: Function to analyze
            test_suite: Existing test cases

        Returns:
            List of predicted edge cases sorted by severity

        Example:
            edge_cases = await client.predict_edge_cases(
                function_code=authenticate_function,
                test_suite=existing_tests
            )

            for edge_case in edge_cases:
                if edge_case.severity in ["HIGH", "CRITICAL"]:
                    logger.warning(f"⚠️ {edge_case.scenario} (p={edge_case.probability:.2f})")
                    logger.info(f"   Suggested test: {edge_case.suggested_test}")
        """
        payload = {"function_code": function_code, "test_suite": test_suite}

        response = await self._request(
            "POST",
            f"{self.base_url}/api/v1/predict_edge_cases",
            json=payload
        )

        data = response["data"]

        edge_cases = [
            EdgeCase(
                scenario=ec["scenario"],
                probability=ec["probability"],
                severity=EdgeCaseSeverity(ec["severity"]),
                suggested_test=ec["suggested_test"],
                reasoning=ec["reasoning"],
            )
            for ec in data["edge_cases"]
        ]

        # Sort by severity (CRITICAL > HIGH > MEDIUM > LOW)
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        edge_cases.sort(key=lambda ec: (severity_order[ec.severity.value], -ec.probability))

        return edge_cases

    # ========================================================================
    # CODE HEALING (PENELOPE)
    # ========================================================================

    async def heal_code(
        self,
        broken_code: str,
        error_trace: str,
        context: Dict[str, Any],
    ) -> HealingSuggestion:
        """
        Get healing suggestions from PENELOPE service.

        PENELOPE performs root cause analysis and suggests fixes.

        Args:
            broken_code: Code with bug
            error_trace: Error trace/stack trace
            context: Context (codebase, dependencies)

        Returns:
            HealingSuggestion with root cause and fix options

        Example:
            healing = await client.heal_code(
                broken_code=buggy_code,
                error_trace=stack_trace,
                context={"codebase": "..."}
            )

            logger.info(f"Root cause: {healing.root_cause}")
            for fix in healing.fix_suggestions:
                logger.info(f"Fix (confidence {fix.confidence:.2f}): {fix.description}")
        """
        payload = {
            "broken_code": broken_code,
            "error_trace": error_trace,
            "context": context,
        }

        response = await self._request(
            "POST",
            f"{self.penelope_url}/api/v1/heal",
            json=payload
        )

        data = response["data"]

        fix_suggestions = [
            FixOption(
                description=fix["description"],
                code=fix["code"],
                confidence=fix["confidence"],
                side_effects=fix["side_effects"],
            )
            for fix in data["fix_suggestions"]
        ]

        return HealingSuggestion(
            root_cause=data["root_cause"],
            fix_suggestions=fix_suggestions,
            confidence=data["confidence"],
            analysis=data["analysis"],
        )

    # ========================================================================
    # WEB SEARCH (MABA)
    # ========================================================================

    async def search_web(
        self,
        query: str,
        context: str,
    ) -> MABASearchResult:
        """
        Search web using MABA (Multi-Agent Browser Assistant).

        Args:
            query: Search query
            context: Context for query understanding

        Returns:
            MABASearchResult with search results

        Example:
            results = await client.search_web(
                query="OAuth 2.0 PKCE best practices",
                context="Implementing secure authentication"
            )

            for result in results.results:
                logger.info(f"{result.title}: {result.url}")
        """
        payload = {"query": query, "context": context}

        response = await self._request(
            "POST",
            f"{self.maba_url}/api/v1/search",
            json=payload
        )

        data = response["data"]

        search_results = [
            SearchResult(
                title=r["title"],
                url=r["url"],
                snippet=r["snippet"],
                relevance=r["relevance"],
            )
            for r in data["results"]
        ]

        return MABASearchResult(
            results=search_results,
            confidence=data["confidence"],
            query_understanding=data["query_understanding"],
        )

    # ========================================================================
    # NARRATIVE GENERATION (NIS)
    # ========================================================================

    async def generate_narrative(
        self,
        code_changes: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> Narrative:
        """
        Generate narrative using NIS (Narrative Intelligence System).

        NIS creates human-readable stories explaining code changes.

        Args:
            code_changes: List of code changes
            context: Context (project, purpose)

        Returns:
            Narrative with story and insights

        Example:
            narrative = await client.generate_narrative(
                code_changes=[
                    {"file": "auth.py", "type": "refactor", "lines": 50}
                ],
                context={"project": "user_service"}
            )

            print(narrative.story)
            for insight in narrative.key_insights:
                logger.info(f"💡 {insight}")
        """
        payload = {"code_changes": code_changes, "context": context}

        response = await self._request(
            "POST",
            f"{self.nis_url}/api/v1/narrative",
            json=payload
        )

        data = response["data"]

        return Narrative(
            story=data["story"],
            key_insights=data["key_insights"],
            visualization_data=data["visualization_data"],
            confidence=data["confidence"],
        )


# ============================================================================
# CONTEXT MANAGER SUPPORT
# ============================================================================

class MaximusClientContext:
    """Context manager for MaximusClient (auto-close session)"""

    def __init__(self, **kwargs):
        self.client = MaximusClient(**kwargs)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

async def create_maximus_client(
    base_url: str = "http://localhost:8153",
    **kwargs
) -> MaximusClient:
    """
    Create MaximusClient instance.

    Example:
        async with create_maximus_client() as client:
            if await client.health_check():
                analysis = await client.analyze_systemic_impact(...)
    """
    return MaximusClientContext(base_url=base_url, **kwargs)
