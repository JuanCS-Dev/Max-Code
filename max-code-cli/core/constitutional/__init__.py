"""Constitutional Core - P1-P6 Validation System"""

from .engine import ConstitutionalEngine
from .models import (
    Action,
    ActionType,
    ConstitutionalResult,
    Violation,
    ViolationSeverity,
)

# Alias for compatibility with DETER-AGENT Guardian
ConstitutionalVerdict = ConstitutionalResult

__all__ = [
    'ConstitutionalEngine',
    'ConstitutionalVerdict',
    'Action',
    'ActionType',
    'ConstitutionalResult',
    'Violation',
    'ViolationSeverity',
]
