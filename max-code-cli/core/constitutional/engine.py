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

# Import REAL validators P1-P6
from .validators.p1_completeness import P1_Completeness_Validator
from .validators.p2_api_validator import P2_API_Validator
from .validators.p3_truth import P3_Truth_Validator
from .validators.p4_user_sovereignty import P4_User_Sovereignty_Validator
from .validators.p5_systemic import P5_Systemic_Analyzer
from .validators.p6_token_efficiency import P6_Token_Efficiency_Monitor


class ConstitutionalEngine:
    """
    Constitutional Engine - Validates actions against P1-P6 principles.

    PRODUCTION-GRADE: Now using REAL validators (4,033 lines of implementation).

    Features:
    - P1: Completeness (complete implementations, tests, error handling)
    - P2: API Transparency (clear contracts, documentation)
    - P3: Truth (factual accuracy, no hallucinations)
    - P4: User Sovereignty (user control, consent, privacy)
    - P5: Systemic Analysis (holistic thinking, consequences)
    - P6: Token Efficiency (resource optimization, performance)
    """

    def __init__(self):
        """Initialize Constitutional Engine with REAL P1-P6 validators"""
        self.principles_active = True

        # REAL validators (substituiu mocks)
        self.validators = {
            'P1': P1_Completeness_Validator(),
            'P2': P2_API_Validator(),
            'P3': P3_Truth_Validator(),
            'P4': P4_User_Sovereignty_Validator(),
            'P5': P5_Systemic_Analyzer(),
            'P6': P6_Token_Efficiency_Monitor(),
        }

    def execute_action(self, action: Action) -> ConstitutionalResult:
        """
        Execute constitutional validation on an action.

        PRODUCTION: Runs ALL P1-P6 validators and aggregates results.

        Args:
            action: Action to validate

        Returns:
            ConstitutionalResult with validation results from all 6 principles

        Validation Flow:
            1. Run all 6 validators in sequence
            2. Collect all violations
            3. Calculate aggregate score
            4. Determine if action passes (score >= 0.6)
        """
        all_violations = []
        principle_scores = {}

        # Run ALL 6 validators
        for principle_id, validator in self.validators.items():
            try:
                result = validator.validate(action)
                principle_scores[principle_id] = result.score
                all_violations.extend(result.violations)
            except Exception as e:
                # Fail-safe: If validator crashes, count as violation
                principle_scores[principle_id] = 0.0
                all_violations.append(
                    Violation(
                        principle=principle_id,
                        severity=ViolationSeverity.CRITICAL,
                        message=f"Validator {principle_id} crashed: {type(e).__name__}",
                        suggestion=f"Fix validator {principle_id} implementation",
                        context={"error": str(e)}
                    )
                )

        # Calculate aggregate score (average of all 6 principles)
        aggregate_score = sum(principle_scores.values()) / len(principle_scores) if principle_scores else 0.0

        # Determine if passed (threshold: 0.6)
        passed = aggregate_score >= 0.6 and len([v for v in all_violations if v.severity == ViolationSeverity.CRITICAL]) == 0

        # Collect suggestions from violations
        suggestions = [v.suggestion for v in all_violations if v.suggestion] if all_violations else []

        # Build metadata
        from datetime import datetime
        metadata = {
            'validation_timestamp': datetime.utcnow().isoformat() + 'Z',
            'validator_version': '3.1.0',
            'engine_mode': 'production',
            'total_violations': len(all_violations),
            'critical_violations': len([v for v in all_violations if v.severity == ViolationSeverity.CRITICAL]),
            'threshold': 0.6,
        }

        return ConstitutionalResult(
            passed=passed,
            score=aggregate_score,
            principle_scores=principle_scores,
            violations=all_violations,
            suggestions=suggestions,
            metadata=metadata
        )

    def evaluate_all_principles(self, data: dict) -> ConstitutionalResult:
        """
        Evaluate data against all principles (legacy method).

        Args:
            data: Data to evaluate (Guardian format or direct Action fields)

        Returns:
            ConstitutionalResult

        Note:
            This method is kept for backward compatibility with Guardian.
            Handles both Guardian format (code at top level) and Action format.
            Prefer execute_action() for new code.
        """
        # Convert dict to Action if needed
        if isinstance(data, dict):
            from .models import ActionType

            # Map action_type string to ActionType enum
            action_type_str = data.get("action_type", "code_generation")
            try:
                if hasattr(ActionType, action_type_str.upper()):
                    action_type = ActionType[action_type_str.upper()]
                else:
                    # Try direct match
                    action_type = ActionType(action_type_str)
            except (KeyError, ValueError):
                action_type = ActionType.CODE_GENERATION

            # Build context - if 'code' is at top level (Guardian format), move to context
            context = data.get("context", {})
            if "code" in data and "code" not in context:
                context["code"] = data["code"]

            # Extract description/intent with fallbacks
            intent = (
                data.get("intent") or
                data.get("description") or
                context.get("description") or
                "Constitutional validation check"
            ).strip() or "Constitutional validation check"

            action = Action(
                task_id=data.get("task_id", "guardian_action"),
                action_type=action_type,
                intent=intent,
                context=context,
                constitutional_context=data.get("constitutional_context", data.get("parameters", {}))
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
