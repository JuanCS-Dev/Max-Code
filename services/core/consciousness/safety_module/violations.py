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

class ThreatLevel(Enum):
    """
    Threat severity levels for safety violations.

    NONE: No threat detected (normal operation)
    LOW: Minor deviation, log only
    MEDIUM: Significant deviation, alert HITL
    HIGH: Dangerous state, initiate graceful degradation
    CRITICAL: Imminent danger, trigger kill switch
    """

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"




class SafetyLevel(Enum):
    """
    Legacy safety severity levels (backward compatibility).

    Maps the historical four-level scale to the modern five-level ThreatLevel.
    """

    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

    @classmethod
    def from_threat(cls, threat_level: ThreatLevel) -> "SafetyLevel":
        """Convert a modern threat level into the legacy severity scale."""
        mapping = {
            ThreatLevel.NONE: cls.NORMAL,
            ThreatLevel.LOW: cls.WARNING,
            ThreatLevel.MEDIUM: cls.WARNING,
            ThreatLevel.HIGH: cls.CRITICAL,
            ThreatLevel.CRITICAL: cls.EMERGENCY,
        }
        return mapping[threat_level]

    def to_threat(self) -> ThreatLevel:
        """Convert the legacy severity scale back to a modern threat level."""
        mapping = {
            SafetyLevel.NORMAL: ThreatLevel.NONE,
            SafetyLevel.WARNING: ThreatLevel.LOW,
            SafetyLevel.CRITICAL: ThreatLevel.HIGH,
            SafetyLevel.EMERGENCY: ThreatLevel.CRITICAL,
        }
        return mapping[self]




class SafetyViolationType(Enum):
    """
    Types of safety violations.

    Each violation type maps to specific thresholds and response protocols.
    """

    THRESHOLD_EXCEEDED = "threshold_exceeded"
    ANOMALY_DETECTED = "anomaly_detected"
    SELF_MODIFICATION = "self_modification_attempt"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    UNEXPECTED_BEHAVIOR = "unexpected_behavior"
    CONSCIOUSNESS_RUNAWAY = "consciousness_runaway"
    ETHICAL_VIOLATION = "ethical_violation"
    GOAL_SPAM = "goal_spam"
    AROUSAL_RUNAWAY = "arousal_runaway"
    COHERENCE_COLLAPSE = "coherence_collapse"




class ViolationType(Enum):
    """
    Legacy safety violation types (backward compatibility).

    These map directly onto the modern SafetyViolationType enum.
    """

    ESGT_FREQUENCY_EXCEEDED = "esgt_frequency_exceeded"
    AROUSAL_SUSTAINED_HIGH = "arousal_sustained_high"
    UNEXPECTED_GOALS = "unexpected_goals"
    SELF_MODIFICATION = "self_modification"
    MEMORY_OVERFLOW = "memory_overflow"
    CPU_SATURATION = "cpu_saturation"
    ETHICAL_VIOLATION = "ethical_violation"
    UNKNOWN_BEHAVIOR = "unknown_behavior"

    def to_modern(self) -> SafetyViolationType:
        """Translate the legacy violation enum to the modern equivalent."""
        return _LEGACY_TO_MODERN_VIOLATION[self]


_LEGACY_TO_MODERN_VIOLATION = {
    ViolationType.ESGT_FREQUENCY_EXCEEDED: SafetyViolationType.THRESHOLD_EXCEEDED,
    ViolationType.AROUSAL_SUSTAINED_HIGH: SafetyViolationType.AROUSAL_RUNAWAY,
    ViolationType.UNEXPECTED_GOALS: SafetyViolationType.GOAL_SPAM,
    ViolationType.SELF_MODIFICATION: SafetyViolationType.SELF_MODIFICATION,
    ViolationType.MEMORY_OVERFLOW: SafetyViolationType.RESOURCE_EXHAUSTION,
    ViolationType.CPU_SATURATION: SafetyViolationType.RESOURCE_EXHAUSTION,
    ViolationType.ETHICAL_VIOLATION: SafetyViolationType.ETHICAL_VIOLATION,
    ViolationType.UNKNOWN_BEHAVIOR: SafetyViolationType.UNEXPECTED_BEHAVIOR,
}

_MODERN_TO_LEGACY_VIOLATION: dict[SafetyViolationType, ViolationType] = {}
for legacy, modern in _LEGACY_TO_MODERN_VIOLATION.items():
    # Preserve the first mapping for modern types that aggregate multiple legacy enums.
    _MODERN_TO_LEGACY_VIOLATION.setdefault(modern, legacy)




class _ViolationTypeAdapter:
    """Adapter that allows equality across legacy and modern violation enums."""

    __slots__ = ("modern", "legacy")

    def __init__(self, modern: SafetyViolationType, legacy: ViolationType):
        self.modern = modern
        self.legacy = legacy

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _ViolationTypeAdapter):
            return self.modern is other.modern
        if isinstance(other, SafetyViolationType):
            return self.modern is other
        if isinstance(other, ViolationType):
            return self.legacy is other
        if isinstance(other, str):
            return other in {self.modern.value, self.legacy.value, self.modern.name, self.legacy.name}
        return False

    def __hash__(self) -> int:
        return hash(self.modern)

    def __repr__(self) -> str:
        return f"{self.modern}"

    @property
    def value(self) -> str:
        return self.modern.value

    @property
    def name(self) -> str:
        return self.modern.name




class SafetyViolationType(Enum):
    """
    Types of safety violations.

    Each violation type maps to specific thresholds and response protocols.
    """

    THRESHOLD_EXCEEDED = "threshold_exceeded"
    ANOMALY_DETECTED = "anomaly_detected"
    SELF_MODIFICATION = "self_modification_attempt"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    UNEXPECTED_BEHAVIOR = "unexpected_behavior"
    CONSCIOUSNESS_RUNAWAY = "consciousness_runaway"
    ETHICAL_VIOLATION = "ethical_violation"
    GOAL_SPAM = "goal_spam"
    AROUSAL_RUNAWAY = "arousal_runaway"
    COHERENCE_COLLAPSE = "coherence_collapse"




