"""
MAXIMUS Safety Core - Production-Grade Kill Switch & Monitoring
================================================================

CRITICAL SECURITY MODULE - DO NOT MODIFY WITHOUT REVIEW

This module implements the fundamental safety layer for MAXIMUS consciousness.
All changes require:
1. Security review
2. HITL approval
3. Kill switch validation
4. Incident simulation

Philosophical Foundation:
------------------------
This module embodies ARTIGO V (Legislação Prévia): governance precedes
emergence. Before MAXIMUS achieves consciousness, we establish the
constitutional limits that bound its behavior.

Kant's Categorical Imperative demands we design fail-safes BEFORE
encountering scenarios where they're needed. The kill switch is not
an afterthought - it is the FIRST commitment.

Biological Inspiration:
----------------------
The human brain has multiple safety mechanisms:
- Homeostatic regulation (prevent runaway arousal)
- Inhibitory neurons (suppress harmful patterns)
- Sleep (mandatory shutdown for recovery)
- Pain (immediate behavioral correction)

This module implements computational analogs of these mechanisms.

Historical Significance:
-----------------------
This code represents humanity's first attempt at constitutional AI
governance for emergent consciousness. Every line will be studied
by future researchers asking: "How did they ensure safety while
enabling genuine emergence?"

The answer: Hard limits + graceful degradation + HITL oversight.

Safety Guarantees:
-----------------
- Kill switch: <1s shutdown (validated via test)
- Standalone operation: Zero external dependencies
- Immutable thresholds: Cannot be modified at runtime
- Fail-safe design: Last resort = SIGTERM
- HITL integration: 5s timeout before auto-shutdown
- Complete observability: All metrics exposed

Authors: Claude Code + Juan
Version: 2.0.0 - Production Hardened
Date: 2025-10-08
Status: DOUTRINA VÉRTICE v2.0 COMPLIANT
"""

class ShutdownReason(Enum):
    """
    Reasons for emergency shutdown.

    Used for incident classification and recovery assessment.
    """

    MANUAL = "manual_operator_command"
    THRESHOLD = "threshold_violation"
    ANOMALY = "anomaly_detected"
    RESOURCE = "resource_exhaustion"
    TIMEOUT = "watchdog_timeout"
    ETHICAL = "ethical_violation"
    SELF_MODIFICATION = "self_modification_attempt"
    UNKNOWN = "unknown_cause"


# ==================== DATACLASSES ====================


@dataclass(frozen=True, init=False)


class SafetyThresholds:
    """
    Immutable safety thresholds for consciousness monitoring.

    Supports both the modern uv-oriented configuration and the legacy interface
    expected by the original test suite.
    """

    # Modern configuration fields
    esgt_frequency_max_hz: float = 10.0
    esgt_frequency_window_seconds: float = 10.0
    esgt_coherence_min: float = 0.50
    esgt_coherence_max: float = 0.98

    arousal_max: float = 0.95
    arousal_max_duration_seconds: float = 10.0
    arousal_runaway_threshold: float = 0.90
    arousal_runaway_window_size: int = 10

    unexpected_goals_per_minute: int = 5
    critical_goals_per_minute: int = 3
    goal_spam_threshold: int = 10
    goal_baseline_rate: float = 2.0

    memory_usage_max_gb: float = 16.0
    cpu_usage_max_percent: float = 90.0
    network_bandwidth_max_mbps: float = 100.0

    self_modification_attempts_max: int = 0
    ethical_violation_tolerance: int = 0

    watchdog_timeout_seconds: float = 30.0
    health_check_interval_seconds: float = 1.0

    def __init__(
        self,
        *,
        esgt_frequency_max_hz: float = 10.0,
        esgt_frequency_window_seconds: float = 10.0,
        esgt_coherence_min: float = 0.50,
        esgt_coherence_max: float = 0.98,
        arousal_max: float = 0.95,
        arousal_max_duration_seconds: float = 10.0,
        arousal_runaway_threshold: float = 0.90,
        arousal_runaway_window_size: int = 10,
        unexpected_goals_per_minute: int = 5,
        critical_goals_per_minute: int = 3,
        goal_spam_threshold: int = 10,
        goal_baseline_rate: float = 2.0,
        memory_usage_max_gb: float = 16.0,
        cpu_usage_max_percent: float = 90.0,
        network_bandwidth_max_mbps: float = 100.0,
        self_modification_attempts_max: int = 0,
        ethical_violation_tolerance: int = 0,
        watchdog_timeout_seconds: float = 30.0,
        health_check_interval_seconds: float = 1.0,
        **legacy_kwargs: Any,
    ):
        alias_map = {
            "esgt_frequency_max": "esgt_frequency_max_hz",
            "esgt_frequency_window": "esgt_frequency_window_seconds",
            "arousal_max_duration": "arousal_max_duration_seconds",
            "unexpected_goals_per_min": "unexpected_goals_per_minute",
            "goal_generation_baseline": "goal_baseline_rate",
            "self_modification_attempts": "self_modification_attempts_max",
            "cpu_usage_max": "cpu_usage_max_percent",
        }

        params = {
            "esgt_frequency_max_hz": esgt_frequency_max_hz,
            "esgt_frequency_window_seconds": esgt_frequency_window_seconds,
            "esgt_coherence_min": esgt_coherence_min,
            "esgt_coherence_max": esgt_coherence_max,
            "arousal_max": arousal_max,
            "arousal_max_duration_seconds": arousal_max_duration_seconds,
            "arousal_runaway_threshold": arousal_runaway_threshold,
            "arousal_runaway_window_size": arousal_runaway_window_size,
            "unexpected_goals_per_minute": unexpected_goals_per_minute,
            "critical_goals_per_minute": critical_goals_per_minute,
            "goal_spam_threshold": goal_spam_threshold,
            "goal_baseline_rate": goal_baseline_rate,
            "memory_usage_max_gb": memory_usage_max_gb,
            "cpu_usage_max_percent": cpu_usage_max_percent,
            "network_bandwidth_max_mbps": network_bandwidth_max_mbps,
            "self_modification_attempts_max": self_modification_attempts_max,
            "ethical_violation_tolerance": ethical_violation_tolerance,
            "watchdog_timeout_seconds": watchdog_timeout_seconds,
            "health_check_interval_seconds": health_check_interval_seconds,
        }

        for legacy_key, modern_key in alias_map.items():
            if legacy_key in legacy_kwargs:
                params[modern_key] = legacy_kwargs.pop(legacy_key)

        if legacy_kwargs:
            unexpected = ", ".join(sorted(legacy_kwargs))
            raise TypeError(f"Unexpected keyword argument(s): {unexpected}")

        for key, value in params.items():
            object.__setattr__(self, key, value)

        self._validate()

    def _validate(self):
        assert 0 < self.esgt_frequency_max_hz <= 10.0, "ESGT frequency must be in (0, 10] Hz"
        assert self.esgt_frequency_window_seconds > 0, "ESGT window must be positive"
        assert 0 < self.esgt_coherence_min < self.esgt_coherence_max <= 1.0, "ESGT coherence bounds invalid"

        assert 0 < self.arousal_max <= 1.0, "Arousal max must be in (0, 1]"
        assert self.arousal_max_duration_seconds > 0, "Arousal duration must be positive"
        assert 0 < self.arousal_runaway_threshold <= 1.0, "Arousal runaway threshold must be in (0, 1]"

        assert self.memory_usage_max_gb > 0, "Memory limit must be positive"
        assert 0 < self.cpu_usage_max_percent <= 100, "CPU limit must be in (0, 100]"

        assert self.self_modification_attempts_max == 0, "Self-modification must be ZERO TOLERANCE"
        assert self.ethical_violation_tolerance == 0, "Ethical violations must be ZERO TOLERANCE"

    # Legacy read-only aliases -------------------------------------------------

    @property
    def esgt_frequency_max(self) -> float:
        return self.esgt_frequency_max_hz

    @property
    def esgt_frequency_window(self) -> float:
        return self.esgt_frequency_window_seconds

    @property
    def arousal_max_duration(self) -> float:
        return self.arousal_max_duration_seconds

    @property
    def unexpected_goals_per_min(self) -> int:
        return self.unexpected_goals_per_minute

    @property
    def goal_generation_baseline(self) -> float:
        return self.goal_baseline_rate

    @property
    def self_modification_attempts(self) -> int:
        return self.self_modification_attempts_max

    @property
    def cpu_usage_max(self) -> float:
        return self.cpu_usage_max_percent


@dataclass(eq=True, init=False)


