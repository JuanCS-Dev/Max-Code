"""
Safety Module - Split from safety.py for maintainability

BACKWARDS COMPATIBLE: All imports work as before
"""

# Import everything from submodules
from .violations import (
    ThreatLevel, SafetyLevel, SafetyViolationType, ViolationType,
    _ViolationTypeAdapter, SafetyViolation
)
from .config import ShutdownReason, SafetyThresholds
from .monitoring import ThresholdMonitor, AnomalyDetector
from .incidents import IncidentReport, StateSnapshot, KillSwitch
from .protocol import ConsciousnessSafetyProtocol

__all__ = [
    "ThreatLevel", "SafetyLevel", "SafetyViolationType", "ViolationType",
    "_ViolationTypeAdapter", "SafetyViolation", "ShutdownReason",
    "SafetyThresholds", "ThresholdMonitor", "AnomalyDetector",
    "IncidentReport", "StateSnapshot", "KillSwitch",
    "ConsciousnessSafetyProtocol"
]
