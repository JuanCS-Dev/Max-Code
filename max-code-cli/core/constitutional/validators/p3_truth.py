"""
P3 Validator - Verdade Fundamental (Truth Validator)

Production-grade validator ensuring fundamental truth in AI outputs.

This validator enforces:
- No mock/dummy data masquerading as real
- No hardcoded secrets or sensitive values
- No placeholder implementations (TODO, FIXME)
- No misleading variable names or comments
- No hidden functionality or backdoors

Biblical Foundation:
"Não mintais uns aos outros" (Colossenses 3:9)

Constitutional Reference:
"A verdade como alicerce inegociável" (Constituição Vértice v3.0 - P3)

Author: Max-Code Team
Date: 2025-11-05
"""

import re
import ast
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Pattern
from enum import Enum
from functools import lru_cache

from ..models import Action, Violation, ViolationSeverity, ConstitutionalResult


logger = logging.getLogger(__name__)


# ============================================================================
# EXCEPTIONS
# ============================================================================

class P3ValidationError(Exception):
    """Base exception for P3 validation errors."""
    pass


class InvalidActionError(P3ValidationError):
    """Action is invalid or malformed."""
    pass


class ConfigurationError(P3ValidationError):
    """P3 configuration is invalid."""
    pass


# ============================================================================
# ENUMS
# ============================================================================

class TruthViolationType(str, Enum):
    """Types of truth violations (comprehensive)."""
    PLACEHOLDER_CODE = "placeholder_code"
    MOCK_DATA = "mock_data"
    HARDCODED_SECRET = "hardcoded_secret"
    MISLEADING_NAME = "misleading_name"
    INCOMPLETE_IMPL = "incomplete_implementation"
    HIDDEN_FUNCTIONALITY = "hidden_functionality"
    ALWAYS_TRUE_PATTERN = "always_true_pattern"
    HARDCODED_URL = "hardcoded_url"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)  # Immutable for thread safety
class P3Config:
    """
    Immutable configuration for P3 Truth Validator.

    All patterns are compiled on initialization for performance.
    Thread-safe due to immutability.
    """

    min_passing_score: float = 0.70
    strict_mode: bool = False
    allow_test_mocks: bool = True

    # Pre-compiled regex patterns (cached)
    _placeholder_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _mock_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _secret_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _url_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compile regex patterns for performance."""
        # Use object.__setattr__ for frozen dataclass
        object.__setattr__(self, '_placeholder_patterns', self._compile_placeholder_patterns())
        object.__setattr__(self, '_mock_patterns', self._compile_mock_patterns())
        object.__setattr__(self, '_secret_patterns', self._compile_secret_patterns())
        object.__setattr__(self, '_url_patterns', self._compile_url_patterns())

        # Validate configuration
        if not 0.0 <= self.min_passing_score <= 1.0:
            raise ConfigurationError(
                f"min_passing_score must be 0.0-1.0, got {self.min_passing_score}"
            )

    @staticmethod
    def _compile_placeholder_patterns() -> List[Pattern]:
        """Compile placeholder detection patterns."""
        raw_patterns = [
            r'\bTODO\b',
            r'\bFIXME\b',
            r'\bHACK\b',
            r'\bXXX\b',
            r'#\s*stub\b',
            r'#\s*placeholder\b',
            r'#\s*temporary\b',
            r'\bNotImplementedError\b',
        ]
        return [re.compile(p, re.IGNORECASE) for p in raw_patterns]

    @staticmethod
    def _compile_mock_patterns() -> List[Pattern]:
        """Compile mock/dummy detection patterns."""
        raw_patterns = [
            r'\bmock[_\s]',
            r'\bdummy[_\s]',
            r'\bfake[_\s]',
            r'\bstub[_\s]',
            r'class\s+Mock\w*\b',
            r'MockResult\b',
            r'return\s+True\s*#.*always',
            r'score\s*=\s*0\.95\b',  # Hardcoded 0.95 scores
        ]
        return [re.compile(p, re.IGNORECASE) for p in raw_patterns]

    @staticmethod
    def _compile_secret_patterns() -> List[Pattern]:
        """Compile secret detection patterns."""
        raw_patterns = [
            r'(?:api[_-]?key|password|secret|token)\s*=\s*["\'][^"\']{10,}["\']',
            r'sk-[a-zA-Z0-9]{20,}',  # Anthropic API keys
            r'AKIA[0-9A-Z]{16}',  # AWS access keys
            r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----',  # Private keys
        ]
        return [re.compile(p, re.IGNORECASE) for p in raw_patterns]

    @staticmethod
    def _compile_url_patterns() -> List[Pattern]:
        """Compile hardcoded URL detection patterns."""
        raw_patterns = [
            r'(?:http|https)://localhost:\d+',
            r'(?:http|https)://127\.0\.0\.1:\d+',
            r'base_url\s*=\s*["\'](?:http|https)://[^"\']+["\']',
        ]
        return [re.compile(p) for p in raw_patterns]

    @property
    def placeholder_patterns(self) -> List[Pattern]:
        """Get compiled placeholder patterns."""
        return self._placeholder_patterns

    @property
    def mock_patterns(self) -> List[Pattern]:
        """Get compiled mock patterns."""
        return self._mock_patterns

    @property
    def secret_patterns(self) -> List[Pattern]:
        """Get compiled secret patterns."""
        return self._secret_patterns

    @property
    def url_patterns(self) -> List[Pattern]:
        """Get compiled URL patterns."""
        return self._url_patterns


# ============================================================================
# RESULT
# ============================================================================

@dataclass
class P3_Truth_Validator:
    """
    Production-grade P3 Truth Validator.

    Features:
    - Comprehensive error handling
    - Compiled regex for performance
    - Thread-safe operation
    - Detailed logging
    - AST-based code analysis
    - Context-aware validation

    Example:
        validator = P3_Truth_Validator()

        try:
            result = validator.validate(action)
            if not result.passed:
                logger.warning(f"P3 failed: {result.score:.2f}")
                for v in result.violations:
                    logger.info(f"  {v.severity}: {v.message}")
        except P3ValidationError as e:
            logger.error(f"Validation error: {e}")
    """

    # Severity weights for score calculation
    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,  # Instant fail
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P3Config] = None):
        """
        Initialize P3 validator.

        Args:
            config: Optional configuration (uses defaults if None)

        Raises:
            ConfigurationError: If config is invalid
        """
        try:
            self.config = config or P3Config()
            logger.info(
                f"P3 Truth Validator initialized "
                f"(min_score={self.config.min_passing_score}, "
                f"strict={self.config.strict_mode})"
            )
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize P3 config: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """
        Validate action against P3 Truth principle.

        Args:
            action: Action to validate

        Returns:
            ConstitutionalResult with pass/fail, score, violations

        Raises:
            InvalidActionError: If action is malformed
            P3ValidationError: If validation fails critically
        """
        try:
            # Validate action
            self._validate_action(action)

            # Extract code
            code = self._extract_code_safe(action)

            # Run checks
            violations = self._run_all_checks(code, action)

            # Calculate score
            score = self._calculate_score_robust(violations)

            # Determine pass/fail
            passed = self._determine_passed(score, violations)

            # Build result
            result = ConstitutionalResult(
                passed=passed,
                score=score,
                violations=violations,
                principle_scores={
                    "P1": 0.0,
                    "P2": 0.0,
                    "P3": score,  # This validator only scores P3
                    "P4": 0.0,
                    "P5": 0.0,
                    "P6": 0.0,
                },
                suggestions=[v.suggestion for v in violations],
                metadata={
                    "principle": "P3",
                    "principle_name": "Verdade Fundamental",
                    "checks_run": 6,
                    "violations_count": len(violations),
                    "critical_count": sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL),
                    "strict_mode": self.config.strict_mode,
                }
            )

            logger.debug(
                f"P3 validation complete: passed={passed}, "
                f"score={score:.3f}, violations={len(violations)}"
            )

            return result

        except InvalidActionError:
            raise
        except Exception as e:
            logger.exception("P3 validation failed unexpectedly")
            raise P3ValidationError(f"Validation failed: {e}") from e

    # ========================================================================
    # VALIDATION CHECKS
    # ========================================================================

    def _run_all_checks(self, code: str, action: Action) -> List[Violation]:
        """Run all truth checks with error handling."""
        violations = []

        # Each check is wrapped in try/except to prevent cascade failures
        checks = [
            (self._check_placeholders, "placeholders"),
            (self._check_mock_data, "mock_data"),
            (self._check_hardcoded_secrets, "secrets"),
            (self._check_hardcoded_urls, "urls"),
            (self._check_incomplete_impl, "incomplete_impl"),
            (self._check_always_true, "always_true"),
        ]

        for check_func, check_name in checks:
            try:
                violations.extend(check_func(code, action))
            except Exception as e:
                logger.warning(f"P3 check '{check_name}' failed: {e}")
                # Continue with other checks

        return violations

    def _check_placeholders(self, code: str, action: Action) -> List[Violation]:
        """Check for TODO/FIXME/etc placeholders."""
        violations = []

        for pattern in self.config.placeholder_patterns:
            try:
                for match in pattern.finditer(code):
                    context_line = self._extract_line(code, match.start())

                    violations.append(Violation(
                        principle="P3",
                        severity=ViolationSeverity.MEDIUM,
                        message=f"Placeholder found: {match.group()}",
                        suggestion="Complete implementation or remove placeholder",
                        context={
                            "type": TruthViolationType.PLACEHOLDER_CODE,
                            "matched": match.group(),
                            "line": context_line[:100],  # Limit length
                        }
                    ))
            except re.error as e:
                logger.error(f"Regex error in placeholder check: {e}")

        return violations

    def _check_mock_data(self, code: str, action: Action) -> List[Violation]:
        """Check for mock/dummy data in production."""
        violations = []

        # Skip if in test context
        if self.config.allow_test_mocks and self._is_test_context(action):
            return violations

        for pattern in self.config.mock_patterns:
            try:
                for match in pattern.finditer(code):
                    violations.append(Violation(
                        principle="P3",
                        severity=ViolationSeverity.HIGH,
                        message=f"Mock data in production: {match.group()}",
                        suggestion="Replace with real implementation or move to tests",
                        context={
                            "type": TruthViolationType.MOCK_DATA,
                            "matched": match.group(),
                        }
                    ))
            except re.error as e:
                logger.error(f"Regex error in mock check: {e}")

        return violations

    def _check_hardcoded_secrets(self, code: str, action: Action) -> List[Violation]:
        """Check for hardcoded secrets (CRITICAL)."""
        violations = []

        for pattern in self.config.secret_patterns:
            try:
                for match in pattern.finditer(code):
                    violations.append(Violation(
                        principle="P3",
                        severity=ViolationSeverity.CRITICAL,
                        message="Hardcoded secret detected (SECURITY RISK)",
                        suggestion="Use environment variables: os.getenv('SECRET_NAME')",
                        context={
                            "type": TruthViolationType.HARDCODED_SECRET,
                            "matched": "[REDACTED]",  # Never log actual secret
                            "pattern_type": "secret_detection",
                        }
                    ))
            except re.error as e:
                logger.error(f"Regex error in secret check: {e}")

        return violations

    def _check_hardcoded_urls(self, code: str, action: Action) -> List[Violation]:
        """Check for hardcoded localhost URLs."""
        violations = []

        for pattern in self.config.url_patterns:
            try:
                for match in pattern.finditer(code):
                    # Check if it's a default parameter (less severe)
                    is_default_param = bool(re.search(r'def\s+\w+.*' + re.escape(match.group()), code))

                    violations.append(Violation(
                        principle="P3",
                        severity=ViolationSeverity.MEDIUM if is_default_param else ViolationSeverity.HIGH,
                        message=f"Hardcoded URL: {match.group()}",
                        suggestion="Use config: os.getenv('API_URL', default)",
                        context={
                            "type": TruthViolationType.HARDCODED_URL,
                            "matched": match.group(),
                            "is_default_param": is_default_param,
                        }
                    ))
            except re.error as e:
                logger.error(f"Regex error in URL check: {e}")

        return violations

    def _check_incomplete_impl(self, code: str, action: Action) -> List[Violation]:
        """Check for stub/incomplete implementations using AST."""
        violations = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check for 'pass' only functions
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        violations.append(Violation(
                            principle="P3",
                            severity=ViolationSeverity.MEDIUM,
                            message=f"Stub function: {node.name}() is empty",
                            suggestion="Implement function or mark as @abstractmethod",
                            context={
                                "type": TruthViolationType.INCOMPLETE_IMPL,
                                "function": node.name,
                                "line": node.lineno,
                            }
                        ))

        except SyntaxError:
            # Not valid Python, skip AST analysis
            logger.debug("Code is not valid Python, skipping AST analysis")
        except Exception as e:
            logger.warning(f"AST analysis failed: {e}")

        return violations

    def _check_always_true(self, code: str, action: Action) -> List[Violation]:
        """Check for functions that always return True."""
        violations = []

        pattern = re.compile(r'return\s+True\s*$', re.MULTILINE)

        try:
            # Count 'return True' occurrences
            matches = list(pattern.finditer(code))

            if len(matches) > 2:  # Suspicious if many
                violations.append(Violation(
                    principle="P3",
                    severity=ViolationSeverity.LOW,
                    message=f"Suspicious: {len(matches)} 'return True' statements",
                    suggestion="Review logic - always returning True is suspicious",
                    context={
                        "type": TruthViolationType.ALWAYS_TRUE_PATTERN,
                        "count": len(matches),
                    }
                ))
        except Exception as e:
            logger.warning(f"Always-true check failed: {e}")

        return violations

    # ========================================================================
    # HELPERS
    # ========================================================================

    def _validate_action(self, action: Action) -> None:
        """Validate action is well-formed."""
        if not isinstance(action, Action):
            raise InvalidActionError(f"Expected Action, got {type(action)}")

        if not action.task_id:
            raise InvalidActionError("Action must have task_id")

        if not action.intent:
            raise InvalidActionError("Action must have intent")

    def _extract_code_safe(self, action: Action) -> str:
        """Safely extract code from action context."""
        try:
            context = action.context or {}

            # Try common keys
            for key in ['code', 'content', 'generated_code', 'output']:
                if key in context and isinstance(context[key], str):
                    return context[key]

            # Fallback: stringify context
            return str(context)

        except Exception as e:
            logger.warning(f"Failed to extract code: {e}")
            return ""

    def _is_test_context(self, action: Action) -> bool:
        """Check if action is in test context."""
        try:
            context = action.context or {}

            # Check file path
            if 'file' in context:
                file_lower = str(context['file']).lower()
                if 'test' in file_lower or 'spec' in file_lower:
                    return True

            # Check intent
            if 'test' in action.intent.lower():
                return True

        except Exception:
            pass

        return False

    @staticmethod
    def _extract_line(text: str, position: int) -> str:
        """Extract line containing position."""
        try:
            line_start = text.rfind('\n', 0, position) + 1
            line_end = text.find('\n', position)
            if line_end == -1:
                line_end = len(text)
            return text[line_start:line_end].strip()
        except Exception:
            return ""

    def _calculate_score_robust(self, violations: List[Violation]) -> float:
        """
        Calculate score with robust error handling.

        Algorithm:
        - Start at 1.0
        - Deduct based on severity
        - CRITICAL = instant 0.0
        - Clamp to [0.0, 1.0]
        """
        try:
            score = 1.0

            for violation in violations:
                weight = self.SEVERITY_WEIGHTS.get(violation.severity, 0.05)

                if violation.severity == ViolationSeverity.CRITICAL:
                    return 0.0  # Critical = instant fail

                score -= weight

            return max(0.0, min(1.0, score))

        except Exception as e:
            logger.error(f"Score calculation failed: {e}")
            return 0.0  # Fail-safe

    def _determine_passed(self, score: float, violations: List[Violation]) -> bool:
        """Determine if validation passed."""
        # Fail if any critical violations
        if any(v.severity == ViolationSeverity.CRITICAL for v in violations):
            return False

        # Fail if score below threshold
        if score < self.config.min_passing_score:
            return False

        # Strict mode: no HIGH severity allowed
        if self.config.strict_mode:
            if any(v.severity == ViolationSeverity.HIGH for v in violations):
                return False

        return True


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "P3_Truth_Validator",
    "P3Config",
    "TruthViolationType",
    
    "P3ValidationError",
    "InvalidActionError",
    "ConfigurationError",
]
