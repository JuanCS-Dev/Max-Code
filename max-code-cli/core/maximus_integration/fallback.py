"""
Fallback System

Graceful degradation when MAXIMUS AI is offline or timing out.

Strategies:
1. User Prompt: Ask user if continue without MAXIMUS
2. Auto Fallback: Continue automatically (for non-critical tasks)
3. Fail Fast: Block action (for critical tasks)

Biblical Foundation:
"Os pensamentos do diligente tendem só à abundância, porém os de todo apressado, tão-somente à penúria."
(Provérbios 21:5)
"""

import asyncio
import time
from typing import Any, Callable, Optional, Dict
from dataclasses import dataclass
from enum import Enum
from config.logging_config import get_logger

logger = get_logger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class FallbackMode(str, Enum):
    """Fallback execution modes"""
    HYBRID = "hybrid"          # MAXIMUS online (preferred)
    STANDALONE = "standalone"  # MAXIMUS offline (fallback)
    FAILED = "failed"          # User rejected standalone mode


class FallbackStrategy(str, Enum):
    """Fallback strategies"""
    ASK_USER = "ask_user"            # Prompt user for decision
    AUTO_FALLBACK = "auto_fallback"  # Continue automatically
    FAIL_FAST = "fail_fast"          # Block action


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class FallbackResult:
    """Result from fallback execution"""
    result: Any
    mode: FallbackMode
    latency_ms: float
    maximus_available: bool
    user_approved_fallback: Optional[bool] = None
    warnings: list = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class FallbackMetrics:
    """Metrics for fallback system"""
    total_executions: int = 0
    hybrid_executions: int = 0
    standalone_executions: int = 0
    failed_executions: int = 0
    user_approvals: int = 0
    user_rejections: int = 0
    avg_maximus_latency_ms: float = 0.0
    avg_fallback_latency_ms: float = 0.0


# ============================================================================
# FALLBACK SYSTEM
# ============================================================================

class FallbackSystem:
    """
    Manages graceful degradation when MAXIMUS is offline.

    The fallback system ensures Max-Code can always execute,
    even when MAXIMUS (noble AI layer) is unavailable.

    Usage:
        fallback = FallbackSystem()

        # Execute with fallback
        result = await fallback.execute_with_fallback(
            primary_fn=lambda: call_maximus(...),
            fallback_fn=lambda: maxcode_only(...),
            task_critical=False
        )

        if result.mode == FallbackMode.HYBRID:
            logger.info("✓ MAXIMUS contributed")
        else:
            logger.warning("⚠️ Standalone mode (MAXIMUS offline)")
    """

    def __init__(
        self,
        default_strategy: FallbackStrategy = FallbackStrategy.ASK_USER,
        timeout_threshold: float = 2.0,
        max_retries: int = 1,
    ):
        """
        Initialize Fallback System.

        Args:
            default_strategy: Default fallback strategy
            timeout_threshold: Timeout threshold in seconds (default: 2.0)
            max_retries: Maximum retry attempts for MAXIMUS calls (default: 1)
        """
        self.default_strategy = default_strategy
        self.timeout_threshold = timeout_threshold
        self.max_retries = max_retries
        self.metrics = FallbackMetrics()

    # ========================================================================
    # MAIN EXECUTION METHOD
    # ========================================================================

    async def execute_with_fallback(
        self,
        primary_fn: Callable,
        fallback_fn: Callable,
        task_critical: bool = False,
        strategy: Optional[FallbackStrategy] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> FallbackResult:
        """
        Execute with fallback support.

        Args:
            primary_fn: Primary function (calls MAXIMUS)
            fallback_fn: Fallback function (Max-Code only)
            task_critical: Is this task critical? (affects strategy)
            strategy: Fallback strategy (uses default if None)
            context: Context for user prompts

        Returns:
            FallbackResult with execution result and mode

        Example:
            result = await fallback.execute_with_fallback(
                primary_fn=lambda: client.analyze_systemic_impact(...),
                fallback_fn=lambda: basic_systemic_check(...),
                task_critical=True
            )
        """
        strategy = strategy or self.default_strategy
        context = context or {}

        start_time = time.time()

        # Try primary (MAXIMUS)
        try:
            primary_result = await self._execute_with_timeout(
                primary_fn,
                timeout=self.timeout_threshold
            )

            latency_ms = (time.time() - start_time) * 1000

            # Success - hybrid mode
            self.metrics.total_executions += 1
            self.metrics.hybrid_executions += 1
            self.metrics.avg_maximus_latency_ms = self._update_avg(
                self.metrics.avg_maximus_latency_ms,
                latency_ms,
                self.metrics.hybrid_executions
            )

            return FallbackResult(
                result=primary_result,
                mode=FallbackMode.HYBRID,
                latency_ms=latency_ms,
                maximus_available=True,
                warnings=[],
            )

        except (asyncio.TimeoutError, ConnectionError, Exception) as e:
            # Primary failed - apply fallback strategy
            logger.warning(f"⚠️  MAXIMUS unavailable: {type(e).__name__}")
            if strategy == FallbackStrategy.FAIL_FAST and task_critical:
                # Fail fast for critical tasks
                self.metrics.total_executions += 1
                self.metrics.failed_executions += 1

                return FallbackResult(
                    result=None,
                    mode=FallbackMode.FAILED,
                    latency_ms=(time.time() - start_time) * 1000,
                    maximus_available=False,
                    warnings=["Critical task blocked - MAXIMUS required but offline"],
                )

            elif strategy == FallbackStrategy.ASK_USER:
                # Ask user
                user_approved = self._ask_user_continue(context)

                if not user_approved:
                    self.metrics.total_executions += 1
                    self.metrics.failed_executions += 1
                    self.metrics.user_rejections += 1

                    return FallbackResult(
                        result=None,
                        mode=FallbackMode.FAILED,
                        latency_ms=(time.time() - start_time) * 1000,
                        maximus_available=False,
                        user_approved_fallback=False,
                        warnings=["User rejected standalone mode"],
                    )

                # User approved - continue with fallback
                self.metrics.user_approvals += 1

            # Execute fallback (AUTO_FALLBACK or user approved ASK_USER)
            fallback_start = time.time()
            fallback_result = await fallback_fn()
            fallback_latency = (time.time() - fallback_start) * 1000

            total_latency = (time.time() - start_time) * 1000

            self.metrics.total_executions += 1
            self.metrics.standalone_executions += 1
            self.metrics.avg_fallback_latency_ms = self._update_avg(
                self.metrics.avg_fallback_latency_ms,
                fallback_latency,
                self.metrics.standalone_executions
            )

            return FallbackResult(
                result=fallback_result,
                mode=FallbackMode.STANDALONE,
                latency_ms=total_latency,
                maximus_available=False,
                user_approved_fallback=True if strategy == FallbackStrategy.ASK_USER else None,
                warnings=[
                    "MAXIMUS offline - using standalone Max-Code",
                    f"Fallback latency: {fallback_latency:.0f}ms"
                ],
            )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    async def _execute_with_timeout(
        self,
        fn: Callable,
        timeout: float,
    ) -> Any:
        """Execute function with timeout"""
        return await asyncio.wait_for(fn(), timeout=timeout)

    def _ask_user_continue(self, context: Dict[str, Any]) -> bool:
        """
        Ask user if they want to continue without MAXIMUS.

        This is a simple console prompt. In UI mode, this would be
        a modal dialog.
        """
        task_desc = context.get("task_description", "this task")

        print("\n" + "="*60)
        logger.warning("⚠️  MAXIMUS AI is offline")
        print("="*60)
        logger.info(f"\nTask: {task_desc}")
        logger.info("\nOptions:")
        logger.info("  1. Continue WITHOUT MAXIMUS (standalone Max-Code)")
        logger.info("     → Lower quality (no systemic/ethical analysis)")
        logger.info("     → Faster execution")
        logger.info("\n  2. Cancel and retry later")
        logger.info("     → Wait for MAXIMUS to come back online")
        print("="*60)

        while True:
            choice = input("\nContinue without MAXIMUS? [y/N]: ").strip().lower()

            if choice in ["y", "yes"]:
                logger.info("✓ Continuing in standalone mode...\n")
                return True
            elif choice in ["n", "no", ""]:
                logger.info("✗ Task cancelled. Please retry when MAXIMUS is online.\n")
                return False
            else:
                logger.info("Invalid choice. Please enter 'y' or 'n'.")
    def _update_avg(self, current_avg: float, new_value: float, count: int) -> float:
        """Update running average"""
        if count == 0:
            return new_value
        return ((current_avg * (count - 1)) + new_value) / count

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_metrics(self) -> FallbackMetrics:
        """Get fallback metrics"""
        return self.metrics

    def print_metrics(self):
        """Print fallback metrics (console)"""
        m = self.metrics

        print("\n" + "="*60)
        logger.info("Fallback System Metrics")
        print("="*60)
        logger.info(f"Total Executions:      {m.total_executions}")
        logger.info(f"  ✓ Hybrid:            {m.hybrid_executions} ({self._pct(m.hybrid_executions, m.total_executions)})")
        logger.info(f"  ⚠ Standalone:        {m.standalone_executions} ({self._pct(m.standalone_executions, m.total_executions)})")
        logger.error(f"  ✗ Failed:            {m.failed_executions} ({self._pct(m.failed_executions, m.total_executions)})")
        print()
        logger.info(f"User Decisions:")
        logger.info(f"  Approvals:           {m.user_approvals}")
        logger.info(f"  Rejections:          {m.user_rejections}")
        print()
        logger.info(f"Latency:")
        logger.info(f"  MAXIMUS (avg):       {m.avg_maximus_latency_ms:.0f}ms")
        logger.info(f"  Fallback (avg):      {m.avg_fallback_latency_ms:.0f}ms")
        print("="*60 + "\n")

    def _pct(self, part: int, total: int) -> str:
        """Calculate percentage"""
        if total == 0:
            return "0%"
        return f"{(part / total * 100):.1f}%"

    def reset_metrics(self):
        """Reset metrics"""
        self.metrics = FallbackMetrics()


# ============================================================================
# CONTEXT MANAGER
# ============================================================================

class FallbackContext:
    """
    Context manager for automatic fallback.

    Example:
        async with FallbackContext(maximus_client) as fb:
            if fb.maximus_available:
                # Hybrid mode
                result = await maximus_client.analyze(...)
            else:
                # Standalone mode
                result = maxcode_only(...)
    """

    def __init__(self, maximus_client, timeout: float = 2.0):
        self.maximus_client = maximus_client
        self.timeout = timeout
        self.maximus_available = False

    async def __aenter__(self):
        """Check MAXIMUS availability on enter"""
        try:
            self.maximus_available = await asyncio.wait_for(
                self.maximus_client.health_check(),
                timeout=self.timeout
            )
        except (asyncio.TimeoutError, Exception):
            self.maximus_available = False

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up on exit (no cleanup needed for FallbackContext)"""
        return False  # Don't suppress exceptions


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

async def with_fallback(
    primary_fn: Callable,
    fallback_fn: Callable,
    ask_user: bool = True,
) -> FallbackResult:
    """
    Execute with fallback (convenience function).

    Example:
        result = await with_fallback(
            primary_fn=lambda: client.analyze(...),
            fallback_fn=lambda: maxcode_only(...),
            ask_user=True
        )
    """
    fallback = FallbackSystem(
        default_strategy=FallbackStrategy.ASK_USER if ask_user else FallbackStrategy.AUTO_FALLBACK
    )

    return await fallback.execute_with_fallback(primary_fn, fallback_fn)


async def check_maximus_or_warn(maximus_client) -> bool:
    """
    Check MAXIMUS health and warn if offline.

    Returns:
        True if online, False if offline

    Example:
        if await check_maximus_or_warn(client):
            # Hybrid mode
        else:
            # Standalone mode
    """
    try:
        online = await asyncio.wait_for(
            maximus_client.health_check(),
            timeout=2.0
        )

        if online:
            logger.info("✓ MAXIMUS online - hybrid mode enabled")
            return True
        else:
            logger.warning("⚠️  MAXIMUS offline - standalone mode")
            return False

    except (asyncio.TimeoutError, Exception) as e:
        logger.error(f"⚠️  MAXIMUS check failed: {type(e).__name__}")
        logger.info("   Continuing in standalone mode...")
        return False
