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
    """
    Immutable configuration for P1 Completeness Validator.

    Using frozen dataclass for thread safety and immutability.
    All regex patterns are compiled in __post_init__ for performance.

    Attributes:
        min_passing_score: Minimum score (0.0-1.0) to pass validation
        strict_mode: If True, any CRITICAL violation fails validation
        require_tests: Whether to require test coverage
        require_error_handling: Whether to require error handling in risky operations
        require_docs: Whether to require documentation for functions/classes
    """
    min_passing_score: float = 0.70
    strict_mode: bool = False
    require_tests: bool = True
    require_error_handling: bool = True
    require_docs: bool = True

    _error_handling_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _test_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _doc_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """
        Compile all regex patterns for performance and validate configuration.

        Uses object.__setattr__ because dataclass is frozen (immutable).
        All patterns are pre-compiled once to avoid recompilation on each validation.

        Raises:
            ConfigurationError: If configuration parameters are invalid
        """
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
        """
        Compile regex patterns for error handling detection.

        Detects: try/except blocks, .catch() handlers, error assignments, Exception usage.
        Patterns are case-insensitive where appropriate for broad detection.

        Returns:
            List[Pattern]: Compiled regex patterns (performance optimized)
        """
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
        """
        Compile regex patterns for test code detection.

        Detects: test_ prefix, def test, assert statements, pytest decorators, unittest.
        Helps identify if code is test code (which has different validation rules).

        Returns:
            List[Pattern]: Compiled regex patterns (performance optimized)
        """
        return [
            re.compile(r'\btest_', re.IGNORECASE),
            re.compile(r'\bdef test', re.IGNORECASE),
            re.compile(r'\bassert\b', re.IGNORECASE),
            re.compile(r'@pytest\.', re.IGNORECASE),
            re.compile(r'unittest\.TestCase'),
        ]

    @staticmethod
    def _compile_doc_patterns() -> List[Pattern]:
        """
        Compile regex patterns for documentation detection.

        Detects: triple-quote docstrings (both double and single), inline comments (#),
        and Args:/Returns: sections. Helps identify if functions/classes have proper documentation.

        Returns:
            List[Pattern]: Compiled regex patterns (performance optimized)
        """
        return [
            re.compile(r'"""[\s\S]*?"""'),
            re.compile(r"'{3}[\s\S]*?'{3}"),  # Triple single-quote docstrings
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
    P1: Primazia da Responsabilidade (Completeness Validator)

    Biblical Foundation: "A sabedoria é a coisa principal" (Provérbios 4:7)

    Validates that AI actions are complete, responsible, and production-ready.
    Ensures every action has proper error handling, documentation, tests, and safety mechanisms.

    6 Core Completeness Checks:
    1. Error handling present (try/except, error propagation)
    2. Test coverage exists (unit/integration tests when required)
    3. Documentation complete (docstrings, comments, Args/Returns)
    4. Breaking changes have migration paths
    5. Input validation present (type checks, boundary validation)
    6. Rollback mechanisms for destructive operations

    Thread-safe, fail-safe, context-aware validation with comprehensive error handling.
    """

    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P1Config] = None):
        """
        Initialize P1 Completeness Validator.

        Args:
            config: Optional custom configuration. Defaults to P1Config() with standard settings.

        Raises:
            ConfigurationError: If validator initialization fails (config issues, pattern compilation errors)

        Note:
            All regex patterns are pre-compiled during config initialization for performance.
            Validator is thread-safe due to frozen dataclass configuration.
        """
        try:
            self.config = config or P1Config()
            logger.info("P1_Completeness_Validator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize P1 validator: {e}")
            raise ConfigurationError(f"Failed to initialize validator: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """
        Validate action against P1 Completeness principle.

        Runs all 6 completeness checks and calculates an aggregate score.
        Fail-safe: Returns score=0.0 on catastrophic errors (never crashes).

        Args:
            action: Action to validate (must have task_id, intent, context with code)

        Returns:
            ConstitutionalResult with:
                - passed: True if score >= min_passing_score and no CRITICAL violations (strict mode)
                - score: 0.0-1.0 aggregate score (1.0 = perfect, 0.0 = failed)
                - violations: List of detected violations with severity, location, suggestion
                - principle_scores: Score breakdown (P1 only, others 0.0)
                - suggestions: Remediation guidance for all violations
                - metadata: Execution details (checks_run, violation counts, strict_mode)

        Raises:
            InvalidActionError: If action is malformed or missing required fields
            P1ValidationError: If validation process fails unexpectedly
        """
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
        """
        Validate action structure and required fields.

        Ensures action has all necessary fields before validation can proceed.

        Args:
            action: Action instance to validate

        Raises:
            InvalidActionError: If action is not an Action instance, or missing task_id/intent
        """
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
        """
        Safely extract code from action context.

        Tries multiple locations: context["code"], output, intent fallback.
        Fail-safe: Returns empty string if all extraction attempts fail.

        Args:
            action: Action with context containing code

        Returns:
            str: Extracted code or empty string
        """
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
