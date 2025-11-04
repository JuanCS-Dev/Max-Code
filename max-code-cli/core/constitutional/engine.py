"""
Constitutional Engine

Core engine for Constitutional AI validation of actions against P1-P6 principles.

This module orchestrates validation across all 6 constitutional principles.

Biblical Foundation:
"Os céus proclamam a glória de Deus e o firmamento anuncia a obra das suas mãos"
(Salmos 19:1)
"""

from typing import Dict, Optional
from .models import Action, ConstitutionalResult, create_clean_result

# Re-export models for convenience
from .models import (
    Action,
    ActionType,
    ConstitutionalResult,
    Violation,
    ViolationSeverity,
)


class ConstitutionalEngine:
    """
    Constitutional Engine - Validates actions against P1-P6 principles.

    This is currently a STUB that will be fully implemented in future phases.
    For now, it provides a minimal interface for Guardians to work with.

    Future implementation will include:
    - Full P1-P6 validator integration
    - Detailed violation detection
    - Scoring algorithms
    - Historical tracking
    """

    def __init__(self):
        """Initialize Constitutional Engine"""
        self.principles_active = True

        # Mock validators (will be real in future)
        self.validators = {
            'P1': self._mock_validator(),
            'P2': self._mock_validator(),
            'P3': self._mock_validator(),
            'P4': self._mock_validator(),
            'P5': self._mock_validator(),
            'P6': self._mock_validator(),
        }

    def _mock_validator(self):
        """Create mock validator for testing"""
        class MockValidator:
            def validate(self, action):
                # Always returns clean for now
                return create_clean_result(score=0.95)

        return MockValidator()

    def execute_action(self, action: Action) -> ConstitutionalResult:
        """
        Execute constitutional validation on an action.

        Args:
            action: Action to validate

        Returns:
            ConstitutionalResult with validation results

        Note:
            This is a STUB implementation. Always returns positive result.
            Future versions will do real validation.
        """
        # STUB: Always return clean result for now
        # Real implementation will validate against all P1-P6 principles
        return create_clean_result(score=0.95)

    def evaluate_all_principles(self, data: dict) -> ConstitutionalResult:
        """
        Evaluate data against all principles (legacy method).

        Args:
            data: Data to evaluate

        Returns:
            ConstitutionalResult

        Note:
            This method is kept for backward compatibility.
            Prefer execute_action() for new code.
        """
        # Convert dict to Action if needed
        if isinstance(data, dict):
            from .models import ActionType
            action = Action(
                task_id=data.get("task_id", "unknown"),
                action_type=ActionType.CODE_GENERATION,  # Default
                intent=data.get("intent", "unknown"),
                context=data.get("context", {}),
                constitutional_context=data.get("constitutional_context", {})
            )
            return self.execute_action(action)
        else:
            return create_clean_result(score=0.85)


# ============================================================================
# SINGLETON
# ============================================================================

_global_engine: Optional[ConstitutionalEngine] = None


def get_constitutional_engine() -> ConstitutionalEngine:
    """
    Get global Constitutional Engine instance (singleton).

    Returns:
        ConstitutionalEngine instance
    """
    global _global_engine
    if _global_engine is None:
        _global_engine = ConstitutionalEngine()
    return _global_engine


def reset_constitutional_engine():
    """Reset global engine (useful for testing)"""
    global _global_engine
    _global_engine = None


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Engine
    "ConstitutionalEngine",
    "get_constitutional_engine",
    "reset_constitutional_engine",
    # Models (re-exported)
    "Action",
    "ActionType",
    "ConstitutionalResult",
    "Violation",
    "ViolationSeverity",
]
