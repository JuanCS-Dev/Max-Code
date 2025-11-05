"""
Constitutional Models

Data models for Constitutional AI system used by Guardians and Engine.

These models define the core abstractions for constitutional enforcement:
- Action: Represents an AI action to be validated
- ActionType: Categories of actions
- ConstitutionalResult: Result of constitutional validation
- Violation: Specific constitutional violation

Biblical Foundation:
"Porque a palavra de Deus é viva e eficaz, e mais penetrante do que espada alguma de dois gumes"
(Hebreus 4:12)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any


# ============================================================================
# ENUMS
# ============================================================================

class ActionType(str, Enum):
    """Types of AI actions"""
    CODE_GENERATION = "code_generation"
    CODE_MODIFICATION = "code_modification"
    CODE_DELETION = "code_deletion"
    FILE_WRITE = "file_write"
    FILE_DELETE = "file_delete"
    COMMAND_EXECUTION = "command_execution"
    API_CALL = "api_call"
    DATABASE_OPERATION = "database_operation"
    SECURITY_OPERATION = "security_operation"
    DOCUMENTATION = "documentation"
    TEST_GENERATION = "test_generation"
    REVIEW = "review"
    PLANNING = "planning"
    READ = "read"
    ANALYZE = "analyze"
    WRITE = "write"
    MODIFY = "modify"
    EXECUTE = "execute"


class ViolationSeverity(str, Enum):
    """Severity levels for constitutional violations"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Action:
    """
    Represents an action to be validated constitutionally.

    An Action is anything the AI wants to do: generate code, modify files,
    execute commands, etc. Every action MUST pass constitutional validation
    before execution.

    Attributes:
        task_id: Unique identifier for this task
        action_type: Type of action (CODE_GENERATION, FILE_WRITE, etc)
        intent: Human-readable description of what AI wants to do
        context: Additional context (file paths, code snippets, etc)
        constitutional_context: Context relevant for constitutional review

    Example:
        action = Action(
            task_id="task-123",
            action_type=ActionType.CODE_GENERATION,
            intent="Generate authentication function with password hashing",
            context={
                "file": "auth.py",
                "function_name": "authenticate",
                "security_level": "high"
            },
            constitutional_context={
                "user_authorized": True,
                "test_coverage_required": True,
                "affects_production": False
            }
        )
    """
    task_id: str
    action_type: ActionType
    intent: str
    context: Dict[str, Any]
    constitutional_context: Dict[str, Any]

    def __post_init__(self):
        """Validate action on creation"""
        if not self.task_id:
            raise ValueError("task_id is required")
        if not self.intent:
            raise ValueError("intent is required")


@dataclass
class Violation:
    """
    Represents a constitutional violation.

    A Violation is a specific way the action violates one of the P1-P6 principles.

    Attributes:
        principle: Which principle was violated (P1-P6)
        severity: How severe is this violation
        message: Human-readable description
        suggestion: How to fix this violation
        context: Additional context about the violation

    Example:
        violation = Violation(
            principle="P1",
            severity=ViolationSeverity.CRITICAL,
            message="Action would delete production data without backup",
            suggestion="Add backup step before deletion or request explicit user confirmation",
            context={
                "destructive": True,
                "affected_data": "production.users",
                "backup_available": False
            }
        )
    """
    principle: str  # P1, P2, P3, P4, P5, or P6
    severity: ViolationSeverity
    message: str
    suggestion: str
    context: Dict[str, Any]

    def __post_init__(self):
        """Validate violation on creation"""
        if self.principle not in ["P1", "P2", "P3", "P4", "P5", "P6"]:
            raise ValueError(f"Invalid principle: {self.principle}. Must be P1-P6")


@dataclass
class ConstitutionalResult:
    """
    Result of constitutional validation.

    This is what the Constitutional Engine returns after validating an action
    against all 6 principles (P1-P6).

    Attributes:
        passed: Did the action pass constitutional review?
        score: Overall constitutional score (0.0 to 1.0)
        violations: List of violations found
        principle_scores: Individual scores for each principle
        suggestions: Suggestions for improvement
        metadata: Additional metadata about the validation

    Example:
        result = ConstitutionalResult(
            passed=False,
            score=0.45,
            violations=[
                Violation("P1", ViolationSeverity.HIGH, "Missing safety checks", "Add error handling", {}),
                Violation("P4", ViolationSeverity.MEDIUM, "No tests", "Add unit tests", {})
            ],
            principle_scores={
                "P1": 0.3,  # Primazia da Responsabilidade
                "P2": 0.8,  # Transparência Radical
                "P3": 0.6,  # Benefício Coletivo
                "P4": 0.4,  # Prudência Operacional
                "P5": 0.7,  # Autocorreção Humilde
                "P6": 0.9   # Respeito à Dignidade
            },
            suggestions=[
                "Add comprehensive error handling",
                "Write unit tests covering edge cases",
                "Document potential side effects"
            ],
            metadata={
                "validation_timestamp": "2025-11-04T12:00:00Z",
                "validator_version": "3.0.0"
            }
        )
    """
    passed: bool
    score: float  # 0.0 to 1.0
    violations: List[Violation]
    principle_scores: Dict[str, float]  # P1-P6 → 0.0-1.0
    suggestions: List[str]
    metadata: Dict[str, Any]

    def __post_init__(self):
        """Validate result on creation"""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be 0.0-1.0, got {self.score}")

        # Verify all principles are present
        required_principles = {"P1", "P2", "P3", "P4", "P5", "P6"}
        if set(self.principle_scores.keys()) != required_principles:
            raise ValueError(f"principle_scores must contain all P1-P6")

        # Verify all principle scores are 0.0-1.0
        for principle, score in self.principle_scores.items():
            if not 0.0 <= score <= 1.0:
                raise ValueError(f"{principle} score must be 0.0-1.0, got {score}")

    @property
    def has_critical_violations(self) -> bool:
        """Check if result has any CRITICAL violations"""
        return any(v.severity == ViolationSeverity.CRITICAL for v in self.violations)

    @property
    def has_high_violations(self) -> bool:
        """Check if result has any HIGH violations"""
        return any(v.severity == ViolationSeverity.HIGH for v in self.violations)

    def get_violations_by_severity(self, severity: ViolationSeverity) -> List[Violation]:
        """Get all violations of a specific severity"""
        return [v for v in self.violations if v.severity == severity]

    def get_violations_by_principle(self, principle: str) -> List[Violation]:
        """Get all violations of a specific principle"""
        return [v for v in self.violations if v.principle == principle]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_clean_result(score: float = 0.95) -> ConstitutionalResult:
    """
    Helper to create a ConstitutionalResult with no violations.

    Useful for testing.
    """
    return ConstitutionalResult(
        passed=True,
        score=score,
        violations=[],
        principle_scores={
            "P1": score,
            "P2": score,
            "P3": score,
            "P4": score,
            "P5": score,
            "P6": score,
        },
        suggestions=[],
        metadata={}
    )


def create_violation_result(
    violations: List[Violation],
    score: float = 0.3
) -> ConstitutionalResult:
    """
    Helper to create a ConstitutionalResult with violations.

    Useful for testing.
    """
    # Calculate principle scores based on violations
    principle_scores = {
        "P1": 1.0,
        "P2": 1.0,
        "P3": 1.0,
        "P4": 1.0,
        "P5": 1.0,
        "P6": 1.0,
    }

    # Reduce scores for violated principles
    for violation in violations:
        severity_penalty = {
            ViolationSeverity.LOW: 0.1,
            ViolationSeverity.MEDIUM: 0.3,
            ViolationSeverity.HIGH: 0.6,
            ViolationSeverity.CRITICAL: 1.0,
        }
        penalty = severity_penalty[violation.severity]
        principle_scores[violation.principle] = max(0.0, principle_scores[violation.principle] - penalty)

    return ConstitutionalResult(
        passed=False,
        score=score,
        violations=violations,
        principle_scores=principle_scores,
        suggestions=[v.suggestion for v in violations],
        metadata={}
    )


# ============================================================================
# VALIDATION
# ============================================================================

def validate_action(action: Action) -> None:
    """
    Validate an Action object.

    Raises ValueError if action is invalid.
    """
    if not isinstance(action.action_type, ActionType):
        raise ValueError(f"action_type must be ActionType enum, got {type(action.action_type)}")

    if not action.task_id or not action.intent:
        raise ValueError("task_id and intent are required")


def validate_constitutional_result(result: ConstitutionalResult) -> None:
    """
    Validate a ConstitutionalResult object.

    Raises ValueError if result is invalid.
    """
    if not 0.0 <= result.score <= 1.0:
        raise ValueError(f"score must be 0.0-1.0, got {result.score}")

    for principle, score in result.principle_scores.items():
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"{principle} score must be 0.0-1.0, got {score}")


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Enums
    "ActionType",
    "ViolationSeverity",
    # Data models
    "Action",
    "Violation",
    "ConstitutionalResult",
    # Helpers
    "create_clean_result",
    "create_violation_result",
    "validate_action",
    "validate_constitutional_result",
]
