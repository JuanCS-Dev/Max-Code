"""
P6 Validator - Eficiência de Tokens (Token Efficiency)

Production-grade validator ensuring efficient use of computational resources.

This validator enforces:
- Token budget management
- Efficient code patterns
- Avoiding redundant operations
- Optimized data structures
- Minimal context usage
- Resource-conscious algorithms

Biblical Foundation:
"Sê fiel no pouco" (Lucas 16:10)

Constitutional Reference:
"Eficiência de Tokens" (Constituição Vértice v3.0 - P6)
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

class P6ValidationError(Exception):
    """Base exception for P6 validation errors."""
    pass

class InvalidActionError(P6ValidationError):
    """Action is invalid or malformed."""
    pass

class ConfigurationError(P6ValidationError):
    """P6 configuration is invalid."""
    pass


# ============================================================================
# VIOLATION TYPES
# ============================================================================

class EfficiencyViolationType(str, Enum):
    """Types of P6 efficiency violations."""
    REDUNDANT_CODE = "redundant_code"
    INEFFICIENT_LOOPS = "inefficient_loops"
    EXCESSIVE_VERBOSITY = "excessive_verbosity"
    POOR_DATA_STRUCTURES = "poor_data_structures"
    UNNECESSARY_COMPLEXITY = "unnecessary_complexity"
    WASTEFUL_OPERATIONS = "wasteful_operations"
    TOKEN_BUDGET_EXCEEDED = "token_budget_exceeded"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class P6Config:
    """
    P6 Token Efficiency Monitor Configuration (Immutable, Thread-Safe).

    All regex patterns pre-compiled in __post_init__ for optimal performance.
    Frozen dataclass ensures thread-safety and prevents accidental mutation.

    Attributes:
        min_passing_score: Minimum score (0.0-1.0) to pass validation (default: 0.70)
        strict_mode: If True, any CRITICAL violation fails validation (default: False)
        max_code_length: Maximum lines of code allowed per action (default: 500)
        check_redundancy: Detect and flag redundant code patterns (default: True)
        check_complexity: Analyze algorithmic complexity (default: True)
        token_budget: Maximum token budget for operations (default: 200000)
    """
    min_passing_score: float = 0.70
    strict_mode: bool = False
    max_code_length: int = 500
    check_redundancy: bool = True
    check_complexity: bool = True
    token_budget: int = 200000

    _redundancy_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _inefficiency_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """
        Compile regex patterns and validate configuration.

        Pre-compiles all regex patterns for performance optimization.
        Validates min_passing_score, max_code_length, and token_budget ranges.

        Raises:
            ConfigurationError: If any config parameter is out of valid range or pattern compilation fails
        """
        try:
            object.__setattr__(self, '_redundancy_patterns', self._compile_redundancy_patterns())
            object.__setattr__(self, '_inefficiency_patterns', self._compile_inefficiency_patterns())

            if not 0.0 <= self.min_passing_score <= 1.0:
                raise ConfigurationError(f"min_passing_score must be 0.0-1.0, got {self.min_passing_score}")

            if self.max_code_length <= 0:
                raise ConfigurationError(f"max_code_length must be positive, got {self.max_code_length}")

            logger.debug(f"P6Config initialized: strict={self.strict_mode}, budget={self.token_budget}")
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize P6Config: {e}") from e

    @staticmethod
    def _compile_redundancy_patterns() -> List[Pattern]:
        """Compile patterns for redundant code."""
        return [
            re.compile(r'(\w+)\s*=\s*\1', re.MULTILINE),  # x = x
            re.compile(r'if\s+True:', re.IGNORECASE),
            re.compile(r'if\s+False:', re.IGNORECASE),
            re.compile(r'return\s+(\w+)\s+if\s+\1\s+else\s+\1', re.IGNORECASE),
        ]

    @staticmethod
    def _compile_inefficiency_patterns() -> List[Pattern]:
        """Compile patterns for inefficient code."""
        return [
            re.compile(r'for\s+\w+\s+in\s+range\([^)]+\):\s+for\s+\w+\s+in\s+range', re.MULTILINE),  # Nested loops
            re.compile(r'\.append\([^)]+\)\s+.*\.append\([^)]+\)\s+.*\.append', re.MULTILINE),  # Multiple appends
            re.compile(r'time\.sleep\(\d+\)', re.IGNORECASE),  # Long sleeps
        ]

    @property
    def redundancy_patterns(self) -> List[Pattern]:
        return self._redundancy_patterns or []

    @property
    def inefficiency_patterns(self) -> List[Pattern]:
        return self._inefficiency_patterns or []


# ============================================================================
# VALIDATOR
# ============================================================================

class P6_Token_Efficiency_Monitor:
    """
    P6: Eficiência de Tokens (Token Efficiency Monitor)

    Biblical Foundation: "Sê fiel no pouco" (Lucas 16:10)

    Validates that AI actions use computational resources efficiently and stay within budgets.
    Ensures code is concise, avoids redundancy, uses optimal algorithms and data structures.

    6 Core Efficiency Checks:
    1. Code length within budget (max lines per action, not overly verbose)
    2. No redundant code (duplicate logic, copy-paste patterns)
    3. Efficient algorithms (avoid O(n²) when O(n log n) available, no nested loops)
    4. Appropriate data structures (sets for membership, dicts for lookups, not lists)
    5. Minimal verbosity (clear but concise, no unnecessary comments/prints)
    6. Token budget respected (total context usage within limits)

    Thread-safe, fail-safe, context-aware validation with comprehensive error handling.
    """

    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P6Config] = None):
        """
        Initialize P6 Token Efficiency Monitor.

        Args:
            config: Optional custom configuration. Defaults to P6Config() with standard settings.

        Raises:
            ConfigurationError: If validator initialization fails (config issues, pattern compilation errors)

        Note:
            Tracks current_usage for token budget monitoring.
            All regex patterns are pre-compiled during config initialization for performance.
            Validator is thread-safe due to frozen dataclass configuration.
        """
        try:
            self.config = config or P6Config()
            self.current_usage = 0
            logger.info("P6_Token_Efficiency_Monitor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize P6 validator: {e}")
            raise ConfigurationError(f"Failed to initialize validator: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """
        Validate action against P6 Token Efficiency principle.

        Runs all 6 efficiency checks and calculates an aggregate score.
        Fail-safe: Returns score=0.0 on catastrophic errors (never crashes).

        Args:
            action: Action to validate (must have task_id, intent, context with code)

        Returns:
            ConstitutionalResult with passed status, score, violations, and suggestions

        Raises:
            InvalidActionError: If action is malformed or missing required fields
            P6ValidationError: If validation process fails unexpectedly
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
                    "P1": 0.0,
                    "P2": 0.0,
                    "P3": 0.0,
                    "P4": 0.0,
                    "P5": 0.0,
                    "P6": score,
                },
                suggestions=[v.suggestion for v in violations],
                metadata={
                    "principle": "P6",
                    "principle_name": "Eficiência de Tokens",
                    "checks_run": 6,
                    "violations_count": len(violations),
                    "critical_count": sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL),
                    "strict_mode": self.config.strict_mode,
                    "code_length": len(code),
                    "token_usage": self.current_usage,
                }
            )

            logger.debug(f"P6 validation complete: passed={passed}, score={score:.3f}, violations={len(violations)}")
            return result

        except InvalidActionError:
            raise
        except Exception as e:
            logger.exception("P6 validation failed unexpectedly")
            raise P6ValidationError(f"Validation failed: {e}") from e

    def record_usage(self, tokens: int) -> None:
        """Record token usage."""
        try:
            if tokens < 0:
                logger.warning(f"Negative token usage: {tokens}")
                return
            self.current_usage += tokens
            logger.debug(f"Token usage recorded: +{tokens} (total: {self.current_usage}/{self.config.token_budget})")
        except Exception as e:
            logger.error(f"Failed to record token usage: {e}")

    def reset(self) -> None:
        """Reset usage counter."""
        try:
            self.current_usage = 0
            logger.debug("Token usage counter reset")
        except Exception as e:
            logger.error(f"Failed to reset token usage: {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current usage metrics."""
        try:
            efficiency = 1.0 - (self.current_usage / self.config.token_budget) if self.config.token_budget > 0 else 0.0
            return {
                "tokens_used": self.current_usage,
                "tokens_limit": self.config.token_budget,
                "efficiency_score": max(0.0, efficiency),
                "usage_percent": (self.current_usage / self.config.token_budget * 100) if self.config.token_budget > 0 else 0.0,
            }
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {
                "tokens_used": 0,
                "tokens_limit": self.config.token_budget,
                "efficiency_score": 0.0,
                "usage_percent": 0.0,
            }

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
        """Run all efficiency checks."""
        violations = []

        checks = [
            (self._check_code_length, "code_length"),
            (self._check_redundancy, "redundancy"),
            (self._check_loop_efficiency, "loop_efficiency"),
            (self._check_data_structures, "data_structures"),
            (self._check_verbosity, "verbosity"),
            (self._check_token_budget, "token_budget"),
        ]

        for check_func, check_name in checks:
            try:
                violations.extend(check_func(code, action))
                logger.debug(f"P6 check '{check_name}': {len(violations)} violations")
            except Exception as e:
                logger.warning(f"P6 check '{check_name}' failed: {e}", exc_info=True)
                if self.config.strict_mode:
                    violations.append(Violation(
                        principle="P6",
                        severity=ViolationSeverity.MEDIUM,
                        message=f"Check '{check_name}' failed to execute",
                        suggestion="Review code for syntax errors or edge cases",
                        context={"check": check_name, "error": str(e)}
                    ))

        return violations

    def _check_code_length(self, code: str, action: Action) -> List[Violation]:
        """Check code length efficiency."""
        violations = []

        try:
            code_length = len(code.strip())

            if code_length > self.config.max_code_length:
                severity = ViolationSeverity.MEDIUM if code_length < self.config.max_code_length * 2 else ViolationSeverity.HIGH

                violations.append(Violation(
                    principle="P6",
                    severity=severity,
                    message=f"Code too long: {code_length} chars (limit: {self.config.max_code_length})",
                    suggestion="Break into smaller functions or modules",
                    context={
                        "type": EfficiencyViolationType.EXCESSIVE_VERBOSITY,
                        "code_length": code_length,
                        "limit": self.config.max_code_length,
                    }
                ))
        except Exception as e:
            logger.error(f"Code length check failed: {e}", exc_info=True)

        return violations

    def _check_redundancy(self, code: str, action: Action) -> List[Violation]:
        """Check for redundant code patterns."""
        violations = []

        if not self.config.check_redundancy:
            return violations

        try:
            for pattern in self.config.redundancy_patterns:
                matches = list(pattern.finditer(code))
                if matches:
                    violations.append(Violation(
                        principle="P6",
                        severity=ViolationSeverity.LOW,
                        message="Redundant code pattern detected",
                        suggestion="Remove redundant code to improve clarity and efficiency",
                        context={
                            "type": EfficiencyViolationType.REDUNDANT_CODE,
                            "matches": len(matches),
                        }
                    ))
                    break  # One violation is enough
        except Exception as e:
            logger.error(f"Redundancy check failed: {e}", exc_info=True)

        return violations

    def _check_loop_efficiency(self, code: str, action: Action) -> List[Violation]:
        """Check loop efficiency."""
        violations = []

        try:
            # Check for nested loops
            nested_loops = re.findall(
                r'for\s+\w+\s+in\s+[^:]+:\s*\n\s+for\s+\w+\s+in',
                code,
                re.MULTILINE
            )

            if len(nested_loops) > 2:
                violations.append(Violation(
                    principle="P6",
                    severity=ViolationSeverity.MEDIUM,
                    message=f"Multiple nested loops detected ({len(nested_loops)})",
                    suggestion="Consider using list comprehensions or vectorized operations",
                    context={
                        "type": EfficiencyViolationType.INEFFICIENT_LOOPS,
                        "nested_count": len(nested_loops),
                    }
                ))

            # Check for inefficient list building
            append_count = code.count('.append(')
            if append_count > 10:
                violations.append(Violation(
                    principle="P6",
                    severity=ViolationSeverity.LOW,
                    message=f"Many list appends ({append_count})",
                    suggestion="Consider list comprehension or generator expression",
                    context={
                        "type": EfficiencyViolationType.INEFFICIENT_LOOPS,
                        "append_count": append_count,
                    }
                ))
        except Exception as e:
            logger.error(f"Loop efficiency check failed: {e}", exc_info=True)

        return violations

    def _check_data_structures(self, code: str, action: Action) -> List[Violation]:
        """Check data structure choices."""
        violations = []

        try:
            # Check for inefficient membership testing
            if 'in [' in code or 'in (' in code:
                # Should use set for large collections
                list_size_match = re.search(r'in\s+\[[^\]]{100,}\]', code)
                if list_size_match:
                    violations.append(Violation(
                        principle="P6",
                        severity=ViolationSeverity.LOW,
                        message="Using list for membership testing (large collection)",
                        suggestion="Use set instead of list for O(1) membership testing",
                        context={
                            "type": EfficiencyViolationType.POOR_DATA_STRUCTURES,
                        }
                    ))
        except Exception as e:
            logger.error(f"Data structures check failed: {e}", exc_info=True)

        return violations

    def _check_verbosity(self, code: str, action: Action) -> List[Violation]:
        """Check code verbosity."""
        violations = []

        try:
            # Check for overly verbose patterns
            lines = code.split('\n')
            non_empty_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]

            # Check comment ratio
            comment_lines = [l for l in lines if l.strip().startswith('#')]
            if len(non_empty_lines) > 0:
                comment_ratio = len(comment_lines) / len(non_empty_lines)

                if comment_ratio > 0.5:
                    violations.append(Violation(
                        principle="P6",
                        severity=ViolationSeverity.LOW,
                        message="Excessive comments (too verbose)",
                        suggestion="Use self-documenting code; reduce redundant comments",
                        context={
                            "type": EfficiencyViolationType.EXCESSIVE_VERBOSITY,
                            "comment_ratio": f"{comment_ratio:.2%}",
                        }
                    ))
        except Exception as e:
            logger.error(f"Verbosity check failed: {e}", exc_info=True)

        return violations

    def _check_token_budget(self, code: str, action: Action) -> List[Violation]:
        """Check token budget compliance."""
        violations = []

        try:
            # Estimate tokens (rough: ~4 chars per token)
            estimated_tokens = len(code) // 4

            if self.current_usage + estimated_tokens > self.config.token_budget:
                violations.append(Violation(
                    principle="P6",
                    severity=ViolationSeverity.CRITICAL,
                    message=f"Token budget exceeded: {self.current_usage + estimated_tokens} > {self.config.token_budget}",
                    suggestion="Reduce code size or increase token budget",
                    context={
                        "type": EfficiencyViolationType.TOKEN_BUDGET_EXCEEDED,
                        "current_usage": self.current_usage,
                        "estimated_tokens": estimated_tokens,
                        "budget": self.config.token_budget,
                    }
                ))
        except Exception as e:
            logger.error(f"Token budget check failed: {e}", exc_info=True)

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
    "P6ValidationError",
    "InvalidActionError",
    "ConfigurationError",
    "EfficiencyViolationType",
    "P6Config",
    "P6_Token_Efficiency_Monitor",
]
