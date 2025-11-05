"""
PENELOPE Client

Client for PENELOPE (Self-Healing Service) - Port 8150.

PENELOPE performs:
- Root cause analysis
- Code healing suggestions
- Error recovery strategies

Named after Penelope from Greek mythology (weaver, symbolizing healing/mending).

v2.1: Refactored to use centralized settings (FASE 3.3)
"""

import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from config.settings import get_settings


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class HealingContext:
    """Context for healing request"""
    codebase: Optional[str] = None
    dependencies: Optional[List[str]] = None
    recent_changes: Optional[List[Dict[str, Any]]] = None
    error_history: Optional[List[str]] = None


@dataclass
class FixOption:
    """A single fix option"""
    description: str
    code: str
    confidence: float  # 0.0 to 1.0
    side_effects: List[str]
    explanation: str


@dataclass
class RootCause:
    """Root cause analysis"""
    primary_cause: str
    contributing_factors: List[str]
    confidence: float
    evidence: List[str]


@dataclass
class HealingSuggestion:
    """Complete healing suggestion from PENELOPE"""
    root_cause: RootCause
    fix_options: List[FixOption]
    prevention_strategies: List[str]
    confidence: float
    analysis: str


# ============================================================================
# PENELOPE CLIENT
# ============================================================================

class PENELOPEClient:
    """
    Client for PENELOPE Self-Healing Service.

    PENELOPE specializes in:
    - Analyzing bugs and errors
    - Identifying root causes
    - Suggesting fixes with confidence scores
    - Providing prevention strategies

    Example:
        client = PENELOPEClient(url="http://localhost:8150")

        healing = await client.heal(
            broken_code=buggy_code,
            error_trace=stack_trace,
            context=HealingContext(codebase="...")
        )

        print(f"Root cause: {healing.root_cause.primary_cause}")
        for fix in healing.fix_options:
            print(f"Fix (confidence {fix.confidence:.2f}): {fix.description}")
    """

    def __init__(
        self,
        url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        """
        Initialize PENELOPE client.

        Args:
            url: PENELOPE service URL (default: from settings)
            timeout: Request timeout in seconds (default: from settings)
        """
        # Load settings
        settings = get_settings()

        # Use provided values or fallback to settings
        self.url = (url or settings.maximus.penelope_url).rstrip("/")
        self.timeout = timeout if timeout is not None else float(settings.maximus.timeout_seconds)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self):
        """Close client session"""
        if self._session and not self._session.closed:
            await self._session.close()

    # ========================================================================
    # HEAL CODE
    # ========================================================================

    async def heal(
        self,
        broken_code: str,
        error_trace: str,
        context: Optional[HealingContext] = None,
    ) -> HealingSuggestion:
        """
        Request code healing from PENELOPE.

        Args:
            broken_code: Code with bug
            error_trace: Error trace/stack trace
            context: Optional context (codebase, dependencies, etc)

        Returns:
            HealingSuggestion with root cause and fix options

        Example:
            healing = await client.heal(
                broken_code=\"\"\"
                def authenticate(user, password):
                    if user.password = password:  # BUG: = instead of ==
                        return True
                    return False
                \"\"\",
                error_trace="SyntaxError: invalid syntax",
                context=HealingContext(codebase="auth_module")
            )

            print(healing.root_cause.primary_cause)
            # "Assignment operator (=) used instead of comparison (==)"

            best_fix = healing.fix_options[0]
            print(best_fix.code)
            # "if user.password == password:"
        """
        context = context or HealingContext()

        payload = {
            "broken_code": broken_code,
            "error_trace": error_trace,
            "context": {
                "codebase": context.codebase,
                "dependencies": context.dependencies or [],
                "recent_changes": context.recent_changes or [],
                "error_history": context.error_history or [],
            },
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/heal", json=payload) as response:
            if response.status != 200:
                raise Exception(f"PENELOPE error {response.status}: {await response.text()}")

            data = await response.json()

            # Parse root cause
            root_cause_data = data["root_cause"]
            root_cause = RootCause(
                primary_cause=root_cause_data["primary_cause"],
                contributing_factors=root_cause_data["contributing_factors"],
                confidence=root_cause_data["confidence"],
                evidence=root_cause_data["evidence"],
            )

            # Parse fix options
            fix_options = [
                FixOption(
                    description=fix["description"],
                    code=fix["code"],
                    confidence=fix["confidence"],
                    side_effects=fix["side_effects"],
                    explanation=fix["explanation"],
                )
                for fix in data["fix_options"]
            ]

            # Sort by confidence
            fix_options.sort(key=lambda f: f.confidence, reverse=True)

            return HealingSuggestion(
                root_cause=root_cause,
                fix_options=fix_options,
                prevention_strategies=data["prevention_strategies"],
                confidence=data["confidence"],
                analysis=data["analysis"],
            )

    # ========================================================================
    # ANALYZE ROOT CAUSE
    # ========================================================================

    async def analyze_root_cause(
        self,
        error_trace: str,
        context: Optional[HealingContext] = None,
    ) -> RootCause:
        """
        Analyze root cause without generating fixes.

        Faster than full heal() when you only need root cause analysis.

        Args:
            error_trace: Error trace
            context: Optional context

        Returns:
            RootCause analysis
        """
        context = context or HealingContext()

        payload = {
            "error_trace": error_trace,
            "context": {
                "codebase": context.codebase,
                "dependencies": context.dependencies or [],
                "error_history": context.error_history or [],
            },
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/root_cause", json=payload) as response:
            if response.status != 200:
                raise Exception(f"PENELOPE error {response.status}: {await response.text()}")

            data = await response.json()

            return RootCause(
                primary_cause=data["primary_cause"],
                contributing_factors=data["contributing_factors"],
                confidence=data["confidence"],
                evidence=data["evidence"],
            )

    # ========================================================================
    # HEALTH CHECK
    # ========================================================================

    async def health_check(self) -> bool:
        """
        Check if PENELOPE is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            session = await self._get_session()
            async with session.get(f"{self.url}/api/v1/health") as response:
                return response.status == 200
        except Exception:
            return False


# ============================================================================
# CONTEXT MANAGER
# ============================================================================

class PENELOPEClientContext:
    """Context manager for PENELOPE client"""

    def __init__(self, **kwargs):
        self.client = PENELOPEClient(**kwargs)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
