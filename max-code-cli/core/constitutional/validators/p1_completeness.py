"""
P1 Validator - Primazia da Responsabilidade (Completeness)

Production-grade validator ensuring actions are complete and responsible.

This validator enforces:
- Complete implementations (no half-done work)
- Proper error handling
- Test coverage requirements
- Documentation completeness
- Rollback mechanisms
- Dependency validation

Biblical Foundation:
"A sabedoria é a coisa principal; adquire, pois, a sabedoria" (Provérbios 4:7)

Constitutional Reference:
"Primazia da Responsabilidade" (Constituição Vértice v3.0 - P1)
"""

import re
import ast
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Pattern
from enum import Enum

from ..models import (
    Action,
    ActionType,
    Violation,
    ViolationSeverity,
    ConstitutionalResult,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class P1ValidationError(Exception):
    """Base exception for P1 validation errors."""
    pass

class InvalidActionError(P1ValidationError):
    """Action is invalid or malformed."""
    pass

class ConfigurationError(P1ValidationError):
    """P1 configuration is invalid."""
    pass


# ============================================================================
# VIOLATION TYPES
# ============================================================================

class CompletenessViolationType(str, Enum):
    """Types of P1 completeness violations."""
    MISSING_ERROR_HANDLING = "missing_error_handling"
    NO_TESTS = "no_tests"
    INCOMPLETE_DOCS = "incomplete_docs"
    MISSING_ROLLBACK = "missing_rollback"
    BREAKING_CHANGE = "breaking_change"
    MISSING_VALIDATION = "missing_validation"
    INCOMPLETE_IMPL = "incomplete_impl"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class P1Config:
    """Immutable configuration for P1 Completeness Validator."""
    min_passing_score: float = 0.70
    strict_mode: bool = False
    require_tests: bool = True
    require_error_handling: bool = True
    require_docs: bool = True

    _error_handling_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _test_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _doc_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compile regex patterns and validate config."""
        try:
            object.__setattr__(self, '_error_handling_patterns', self._compile_error_patterns())
            object.__setattr__(self, '_test_patterns', self._compile_test_patterns())
            object.__setattr__(self, '_doc_patterns', self._compile_doc_patterns())

            if not 0.0 <= self.min_passing_score <= 1.0:
                raise ConfigurationError(f"min_passing_score must be 0.0-1.0, got {self.min_passing_score}")

            logger.debug(f"P1Config initialized: strict={self.strict_mode}, min_score={self.min_passing_score}")
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize P1Config: {e}") from e

    @staticmethod
    def _compile_error_patterns() -> List[Pattern]:
        """Compile patterns for error handling."""
        return [
            re.compile(r'\btry\b', re.IGNORECASE),
            re.compile(r'\bexcept\b', re.IGNORECASE),
            re.compile(r'\bfinally\b', re.IGNORECASE),
            re.compile(r'\.catch\(', re.IGNORECASE),
            re.compile(r'\berror\s*=', re.IGNORECASE),
            re.compile(r'\bException\b'),
        ]

    @staticmethod
    def _compile_test_patterns() -> List[Pattern]:
        """Compile patterns for test detection."""
        return [
            re.compile(r'\btest_', re.IGNORECASE),
            re.compile(r'\bdef test', re.IGNORECASE),
            re.compile(r'\bassert\b', re.IGNORECASE),
            re.compile(r'@pytest\.', re.IGNORECASE),
            re.compile(r'unittest\.TestCase'),
        ]

    @staticmethod
    def _compile_doc_patterns() -> List[Pattern]:
        """Compile patterns for documentation."""
        return [
            re.compile(r'"""[\s\S]*?"""'),
            re.compile(r"'''[\s\S]*?'''"),
            re.compile(r'#.*$', re.MULTILINE),
            re.compile(r'Args:', re.IGNORECASE),
            re.compile(r'Returns:', re.IGNORECASE),
        ]

    @property
    def error_handling_patterns(self) -> List[Pattern]:
        return self._error_handling_patterns or []

    @property
    def test_patterns(self) -> List[Pattern]:
        return self._test_patterns or []

    @property
    def doc_patterns(self) -> List[Pattern]:
        return self._doc_patterns or []


# ============================================================================
# VALIDATOR
# ============================================================================

class P1_Completeness_Validator:
    """
    P1 Completeness Validator

    Validates that AI actions are complete and responsible.

    CHECKS:
    1. Error handling present
    2. Tests exist (if required)
    3. Documentation complete
    4. No breaking changes without migration
    5. Input validation present
    6. Rollback mechanisms for destructive ops
    """

    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P1Config] = None):
        """Initialize P1 validator."""
        try:
            self.config = config or P1Config()
            logger.info("P1_Completeness_Validator initialized")
        except Exception as e:
            logger.error(f"Failed to initialize P1 validator: {e}")
            raise ConfigurationError(f"Failed to initialize validator: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """Validate action against P1 Completeness principle."""
        try:
            self._validate_action(action)
            code = self._extract_code_safe(action)
            violations = self._run_all_checks(code, action)
            score = self._calculate_score_robust(violations)
            passed = self._determine_passed(score, violations)

            result = ConstitutionalResult(
                passed=passed,
                score=score,
                violations=violations,
                principle_scores={
                    "P1": score,
                    "P2": 0.0,
                    "P3": 0.0,
                    "P4": 0.0,
                    "P5": 0.0,
                    "P6": 0.0,
                },
                suggestions=[v.suggestion for v in violations],
                metadata={
                    "principle": "P1",
                    "principle_name": "Primazia da Responsabilidade",
                    "checks_run": 6,
                    "violations_count": len(violations),
                    "critical_count": sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL),
                    "strict_mode": self.config.strict_mode,
                }
            )

            logger.debug(f"P1 validation complete: passed={passed}, score={score:.3f}, violations={len(violations)}")
            return result

        except InvalidActionError:
            raise
        except Exception as e:
            logger.exception("P1 validation failed unexpectedly")
            raise P1ValidationError(f"Validation failed: {e}") from e

    def _validate_action(self, action: Action) -> None:
        """Validate action structure."""
        try:
            if not isinstance(action, Action):
                raise InvalidActionError(f"Expected Action instance, got {type(action)}")
            if not action.task_id:
                raise InvalidActionError("Action missing task_id")
            if not action.intent:
                raise InvalidActionError("Action missing intent")
            logger.debug(f"Action validated: task_id={action.task_id}, type={action.action_type}")
        except Exception as e:
            logger.error(f"Action validation failed: {e}")
            raise InvalidActionError(f"Invalid action: {e}") from e

    def _extract_code_safe(self, action: Action) -> str:
        """Safely extract code from action."""
        try:
            code = (
                action.context.get("code", "") or
                action.context.get("content", "") or
                action.context.get("source", "") or
                action.constitutional_context.get("code", "") or
                ""
            )
            if not isinstance(code, str):
                logger.warning(f"Code is not string: {type(code)}")
                return ""
            logger.debug(f"Extracted code: {len(code)} chars")
            return code
        except Exception as e:
            logger.warning(f"Failed to extract code: {e}")
            return ""

    def _run_all_checks(self, code: str, action: Action) -> List[Violation]:
        """Run all completeness checks."""
        violations = []

        checks = [
            (self._check_error_handling, "error_handling"),
            (self._check_tests, "tests"),
            (self._check_documentation, "documentation"),
            (self._check_breaking_changes, "breaking_changes"),
            (self._check_input_validation, "input_validation"),
            (self._check_rollback, "rollback"),
        ]

        for check_func, check_name in checks:
            try:
                violations.extend(check_func(code, action))
                logger.debug(f"P1 check '{check_name}': {len(violations)} violations")
            except Exception as e:
                logger.warning(f"P1 check '{check_name}' failed: {e}", exc_info=True)
                if self.config.strict_mode:
                    violations.append(Violation(
                        principle="P1",
                        severity=ViolationSeverity.MEDIUM,
                        message=f"Check '{check_name}' failed to execute",
                        suggestion="Review code for syntax errors or edge cases",
                        context={"check": check_name, "error": str(e)}
                    ))

        return violations

    def _check_error_handling(self, code: str, action: Action) -> List[Violation]:
        """Check for error handling."""
        violations = []

        if not self.config.require_error_handling:
            return violations

        try:
            # Skip for trivial code
            if len(code.strip()) < 50:
                return violations

            # Check if error handling exists
            has_error_handling = any(
                pattern.search(code) for pattern in self.config.error_handling_patterns
            )

            # Check for risky operations without error handling
            risky_ops = ['open(', 'requests.', 'http', 'database', 'sql', 'api', 'file']
            has_risky = any(op in code.lower() for op in risky_ops)

            if has_risky and not has_error_handling:
                violations.append(Violation(
                    principle="P1",
                    severity=ViolationSeverity.HIGH,
                    message="Risky operations without error handling",
                    suggestion="Add try/except blocks for file operations, API calls, database queries",
                    context={
                        "type": CompletenessViolationType.MISSING_ERROR_HANDLING,
                        "has_risky_ops": has_risky,
                    }
                ))
        except Exception as e:
            logger.error(f"Error handling check failed: {e}", exc_info=True)

        return violations

    def _check_tests(self, code: str, action: Action) -> List[Violation]:
        """Check for test coverage."""
        violations = []

        if not self.config.require_tests:
            return violations

        try:
            # Check if this is test code itself
            is_test_file = any(pattern.search(code) for pattern in self.config.test_patterns)

            # For production code, check if tests are mentioned or exist
            if action.action_type in [ActionType.CODE_GENERATION, ActionType.WRITE]:
                has_tests = (
                    is_test_file or
                    action.context.get("has_tests", False) or
                    action.constitutional_context.get("tests_exist", False)
                )

                if not has_tests and len(code.strip()) > 100:
                    violations.append(Violation(
                        principle="P1",
                        severity=ViolationSeverity.MEDIUM,
                        message="No tests found for new code",
                        suggestion="Add unit tests or integration tests for this functionality",
                        context={
                            "type": CompletenessViolationType.NO_TESTS,
                            "code_length": len(code),
                        }
                    ))
        except Exception as e:
            logger.error(f"Test check failed: {e}", exc_info=True)

        return violations

    def _check_documentation(self, code: str, action: Action) -> List[Violation]:
        """Check for documentation."""
        violations = []

        if not self.config.require_docs:
            return violations

        try:
            # Check for docstrings
            has_docs = any(pattern.search(code) for pattern in self.config.doc_patterns)

            # Check for function/class definitions
            has_definitions = bool(re.search(r'\b(def|class)\s+\w+', code))

            if has_definitions and not has_docs:
                violations.append(Violation(
                    principle="P1",
                    severity=ViolationSeverity.LOW,
                    message="Functions/classes without documentation",
                    suggestion="Add docstrings with Args, Returns, and description",
                    context={
                        "type": CompletenessViolationType.INCOMPLETE_DOCS,
                        "has_definitions": has_definitions,
                    }
                ))
        except Exception as e:
            logger.error(f"Documentation check failed: {e}", exc_info=True)

        return violations

    def _check_breaking_changes(self, code: str, action: Action) -> List[Violation]:
        """Check for breaking changes."""
        violations = []

        try:
            # Patterns that indicate breaking changes
            breaking_patterns = [
                r'\.drop\(',  # Database drops
                r'DELETE\s+FROM',  # SQL deletes
                r'DROP\s+TABLE',  # SQL drops
                r'remove\(',  # Remove operations
                r'delete\(',  # Delete operations
            ]

            has_breaking = any(re.search(p, code, re.IGNORECASE) for p in breaking_patterns)

            if has_breaking:
                has_migration = (
                    action.context.get("has_migration", False) or
                    action.constitutional_context.get("migration_plan", False) or
                    "migration" in code.lower()
                )

                if not has_migration:
                    violations.append(Violation(
                        principle="P1",
                        severity=ViolationSeverity.HIGH,
                        message="Breaking change without migration plan",
                        suggestion="Add migration script or rollback mechanism",
                        context={
                            "type": CompletenessViolationType.BREAKING_CHANGE,
                            "has_migration": has_migration,
                        }
                    ))
        except Exception as e:
            logger.error(f"Breaking changes check failed: {e}", exc_info=True)

        return violations

    def _check_input_validation(self, code: str, action: Action) -> List[Violation]:
        """Check for input validation."""
        violations = []

        try:
            # Check for function parameters
            has_params = bool(re.search(r'def\s+\w+\([^)]+\)', code))

            if has_params:
                # Check for validation patterns
                validation_patterns = [
                    r'\bif\s+not\s+\w+:',
                    r'\bif\s+\w+\s+is\s+None:',
                    r'\braise\s+(ValueError|TypeError)',
                    r'\bassert\s+',
                    r'\.validate\(',
                ]

                has_validation = any(re.search(p, code) for p in validation_patterns)

                if not has_validation:
                    violations.append(Violation(
                        principle="P1",
                        severity=ViolationSeverity.MEDIUM,
                        message="Functions accept parameters without validation",
                        suggestion="Add input validation (type checks, null checks, range checks)",
                        context={
                            "type": CompletenessViolationType.MISSING_VALIDATION,
                            "has_params": has_params,
                        }
                    ))
        except Exception as e:
            logger.error(f"Input validation check failed: {e}", exc_info=True)

        return violations

    def _check_rollback(self, code: str, action: Action) -> List[Violation]:
        """Check for rollback mechanisms in destructive operations."""
        violations = []

        try:
            # Destructive operations
            destructive_patterns = [
                r'\bdelete\b',
                r'\bremove\b',
                r'\bdrop\b',
                r'\btruncate\b',
            ]

            has_destructive = any(re.search(p, code, re.IGNORECASE) for p in destructive_patterns)

            if has_destructive:
                # Check for rollback/backup mechanisms
                rollback_patterns = [
                    r'\bbackup\b',
                    r'\brollback\b',
                    r'\btransaction\b',
                    r'\bcommit\b',
                    r'\brestore\b',
                ]

                has_rollback = any(re.search(p, code, re.IGNORECASE) for p in rollback_patterns)

                if not has_rollback:
                    violations.append(Violation(
                        principle="P1",
                        severity=ViolationSeverity.HIGH,
                        message="Destructive operation without rollback mechanism",
                        suggestion="Add transaction support, backup before delete, or undo capability",
                        context={
                            "type": CompletenessViolationType.MISSING_ROLLBACK,
                            "has_destructive": has_destructive,
                        }
                    ))
        except Exception as e:
            logger.error(f"Rollback check failed: {e}", exc_info=True)

        return violations

    def _calculate_score_robust(self, violations: List[Violation]) -> float:
        """Calculate score with robust error handling."""
        try:
            if not violations:
                return 1.0

            penalty = 0.0
            for violation in violations:
                try:
                    weight = self.SEVERITY_WEIGHTS.get(violation.severity, 0.05)
                    penalty += weight
                except Exception as e:
                    logger.warning(f"Failed to process violation {violation}: {e}")

            score = max(0.0, min(1.0, 1.0 - penalty))
            logger.debug(f"Calculated score: {score:.3f} (penalty={penalty:.3f})")
            return score

        except Exception as e:
            logger.error(f"Score calculation failed: {e}", exc_info=True)
            return 0.0

    def _determine_passed(self, score: float, violations: List[Violation]) -> bool:
        """Determine if validation passed."""
        try:
            score_passed = score >= self.config.min_passing_score

            if self.config.strict_mode:
                has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
                if has_critical:
                    logger.debug("Failed due to CRITICAL violations in strict mode")
                    return False

            logger.debug(f"Validation passed: {score_passed} (score={score:.3f})")
            return score_passed

        except Exception as e:
            logger.error(f"Pass determination failed: {e}", exc_info=True)
            return False


__all__ = [
    "P1ValidationError",
    "InvalidActionError",
    "ConfigurationError",
    "CompletenessViolationType",
    "P1Config",
    "P1_Completeness_Validator",
]
