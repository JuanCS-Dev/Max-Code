"""
P2 Validator - Transparência Radical (API Transparency)

Production-grade validator ensuring API transparency and clear communication.

This validator enforces:
- Clear API contracts (input/output specifications)
- Proper status codes and error messages
- API versioning
- Rate limiting disclosure
- Authentication requirements transparency
- Deprecation warnings

Biblical Foundation:
"A verdade vos libertará" (João 8:32)

Constitutional Reference:
"Transparência Radical" (Constituição Vértice v3.0 - P2)
"""

import re
import json
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

class P2ValidationError(Exception):
    """Base exception for P2 validation errors."""
    pass

class InvalidActionError(P2ValidationError):
    """Action is invalid or malformed."""
    pass

class ConfigurationError(P2ValidationError):
    """P2 configuration is invalid."""
    pass


# ============================================================================
# VIOLATION TYPES
# ============================================================================

class TransparencyViolationType(str, Enum):
    """Types of P2 transparency violations."""
    MISSING_API_CONTRACT = "missing_api_contract"
    UNCLEAR_ERROR_MESSAGES = "unclear_error_messages"
    NO_VERSIONING = "no_versioning"
    HIDDEN_RATE_LIMITS = "hidden_rate_limits"
    UNDOCUMENTED_AUTH = "undocumented_auth"
    NO_DEPRECATION_WARNING = "no_deprecation_warning"
    OPAQUE_BEHAVIOR = "opaque_behavior"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class P2Config:
    """Immutable configuration for P2 Transparency Validator."""
    min_passing_score: float = 0.70
    strict_mode: bool = False
    require_api_contracts: bool = True
    require_error_details: bool = True
    require_versioning: bool = True

    _api_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _error_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _version_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compile regex patterns and validate config."""
        try:
            object.__setattr__(self, '_api_patterns', self._compile_api_patterns())
            object.__setattr__(self, '_error_patterns', self._compile_error_patterns())
            object.__setattr__(self, '_version_patterns', self._compile_version_patterns())

            if not 0.0 <= self.min_passing_score <= 1.0:
                raise ConfigurationError(f"min_passing_score must be 0.0-1.0, got {self.min_passing_score}")

            logger.debug(f"P2Config initialized: strict={self.strict_mode}, min_score={self.min_passing_score}")
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize P2Config: {e}") from e

    @staticmethod
    def _compile_api_patterns() -> List[Pattern]:
        """Compile patterns for API definitions."""
        return [
            re.compile(r'@app\.route', re.IGNORECASE),
            re.compile(r'@api\.(get|post|put|delete)', re.IGNORECASE),
            re.compile(r'def\s+\w+\(.*request', re.IGNORECASE),
            re.compile(r'FastAPI|Flask|Django', re.IGNORECASE),
            re.compile(r'router\.(get|post|put|delete)', re.IGNORECASE),
        ]

    @staticmethod
    def _compile_error_patterns() -> List[Pattern]:
        """Compile patterns for error handling."""
        return [
            re.compile(r'raise\s+\w+Error\(', re.IGNORECASE),
            re.compile(r'return\s+\{[^}]*"error"', re.IGNORECASE),
            re.compile(r'HTTPException', re.IGNORECASE),
            re.compile(r'status_code\s*=', re.IGNORECASE),
        ]

    @staticmethod
    def _compile_version_patterns() -> List[Pattern]:
        """Compile patterns for versioning."""
        return [
            re.compile(r'/v\d+/', re.IGNORECASE),
            re.compile(r'version\s*=', re.IGNORECASE),
            re.compile(r'__version__', re.IGNORECASE),
            re.compile(r'API_VERSION', re.IGNORECASE),
        ]

    @property
    def api_patterns(self) -> List[Pattern]:
        return self._api_patterns or []

    @property
    def error_patterns(self) -> List[Pattern]:
        return self._error_patterns or []

    @property
    def version_patterns(self) -> List[Pattern]:
        return self._version_patterns or []


# ============================================================================
# VALIDATOR
# ============================================================================

class P2_API_Validator:
    """
    P2 Transparency Validator

    Validates that AI actions maintain API transparency.

    CHECKS:
    1. API contracts clearly defined
    2. Error messages are descriptive
    3. Versioning present
    4. Rate limits documented
    5. Authentication requirements clear
    6. Deprecation warnings for old APIs
    """

    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P2Config] = None):
        """Initialize P2 validator."""
        try:
            self.config = config or P2Config()
            logger.info("P2_API_Validator initialized")
        except Exception as e:
            logger.error(f"Failed to initialize P2 validator: {e}")
            raise ConfigurationError(f"Failed to initialize validator: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """Validate action against P2 Transparency principle."""
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
                    "P2": score,
                    "P3": 0.0,
                    "P4": 0.0,
                    "P5": 0.0,
                    "P6": 0.0,
                },
                suggestions=[v.suggestion for v in violations],
                metadata={
                    "principle": "P2",
                    "principle_name": "Transparência Radical",
                    "checks_run": 6,
                    "violations_count": len(violations),
                    "critical_count": sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL),
                    "strict_mode": self.config.strict_mode,
                }
            )

            logger.debug(f"P2 validation complete: passed={passed}, score={score:.3f}, violations={len(violations)}")
            return result

        except InvalidActionError:
            raise
        except Exception as e:
            logger.exception("P2 validation failed unexpectedly")
            raise P2ValidationError(f"Validation failed: {e}") from e

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
        """Run all transparency checks."""
        violations = []

        checks = [
            (self._check_api_contracts, "api_contracts"),
            (self._check_error_messages, "error_messages"),
            (self._check_versioning, "versioning"),
            (self._check_rate_limits, "rate_limits"),
            (self._check_authentication, "authentication"),
            (self._check_deprecation, "deprecation"),
        ]

        for check_func, check_name in checks:
            try:
                violations.extend(check_func(code, action))
                logger.debug(f"P2 check '{check_name}': {len(violations)} violations")
            except Exception as e:
                logger.warning(f"P2 check '{check_name}' failed: {e}", exc_info=True)
                if self.config.strict_mode:
                    violations.append(Violation(
                        principle="P2",
                        severity=ViolationSeverity.MEDIUM,
                        message=f"Check '{check_name}' failed to execute",
                        suggestion="Review code for syntax errors or edge cases",
                        context={"check": check_name, "error": str(e)}
                    ))

        return violations

    def _check_api_contracts(self, code: str, action: Action) -> List[Violation]:
        """Check for clear API contracts."""
        violations = []

        if not self.config.require_api_contracts:
            return violations

        try:
            # Check if this is API code
            is_api = any(pattern.search(code) for pattern in self.config.api_patterns)

            if is_api:
                # Check for input/output specifications
                has_type_hints = bool(re.search(r'def\s+\w+\([^)]*:\s*\w+', code))
                has_response_model = 'response_model' in code.lower()
                has_docstring = '"""' in code or "'''" in code

                if not (has_type_hints or has_response_model or has_docstring):
                    violations.append(Violation(
                        principle="P2",
                        severity=ViolationSeverity.HIGH,
                        message="API endpoint lacks clear contract (input/output spec)",
                        suggestion="Add type hints, response_model, or comprehensive docstring",
                        context={
                            "type": TransparencyViolationType.MISSING_API_CONTRACT,
                            "has_type_hints": has_type_hints,
                            "has_response_model": has_response_model,
                        }
                    ))
        except Exception as e:
            logger.error(f"API contracts check failed: {e}", exc_info=True)

        return violations

    def _check_error_messages(self, code: str, action: Action) -> List[Violation]:
        """Check for descriptive error messages."""
        violations = []

        if not self.config.require_error_details:
            return violations

        try:
            # Check for error handling
            has_errors = any(pattern.search(code) for pattern in self.config.error_patterns)

            if has_errors:
                # Check for generic/unclear error messages
                generic_errors = [
                    r'raise\s+\w+Error\(\s*\)',  # Empty error
                    r'"error":\s*"error"',  # Generic "error" message
                    r'return\s+None\s*#\s*error',  # Silent failure
                ]

                has_generic = any(re.search(p, code, re.IGNORECASE) for p in generic_errors)

                if has_generic:
                    violations.append(Violation(
                        principle="P2",
                        severity=ViolationSeverity.MEDIUM,
                        message="Error messages are unclear or generic",
                        suggestion="Provide specific error messages with context and actionable guidance",
                        context={
                            "type": TransparencyViolationType.UNCLEAR_ERROR_MESSAGES,
                            "has_generic": has_generic,
                        }
                    ))
        except Exception as e:
            logger.error(f"Error messages check failed: {e}", exc_info=True)

        return violations

    def _check_versioning(self, code: str, action: Action) -> List[Violation]:
        """Check for API versioning."""
        violations = []

        if not self.config.require_versioning:
            return violations

        try:
            # Check if this is API code
            is_api = any(pattern.search(code) for pattern in self.config.api_patterns)

            if is_api:
                # Check for versioning
                has_version = any(pattern.search(code) for pattern in self.config.version_patterns)

                if not has_version:
                    violations.append(Violation(
                        principle="P2",
                        severity=ViolationSeverity.MEDIUM,
                        message="API lacks versioning",
                        suggestion="Add version to API path (/v1/) or include API_VERSION constant",
                        context={
                            "type": TransparencyViolationType.NO_VERSIONING,
                            "is_api": is_api,
                        }
                    ))
        except Exception as e:
            logger.error(f"Versioning check failed: {e}", exc_info=True)

        return violations

    def _check_rate_limits(self, code: str, action: Action) -> List[Violation]:
        """Check for rate limit transparency."""
        violations = []

        try:
            # Check if this is API code
            is_api = any(pattern.search(code) for pattern in self.config.api_patterns)

            if is_api:
                # Check for rate limiting
                has_rate_limit = bool(re.search(r'rate_limit|RateLimit|throttle|limiter', code, re.IGNORECASE))

                if has_rate_limit:
                    # Check if limits are documented
                    has_limit_docs = bool(re.search(r'(limit|max_requests|per_second|per_minute)', code, re.IGNORECASE))

                    if not has_limit_docs:
                        violations.append(Violation(
                            principle="P2",
                            severity=ViolationSeverity.LOW,
                            message="Rate limits exist but are not clearly documented",
                            suggestion="Document rate limits in API docstring or response headers",
                            context={
                                "type": TransparencyViolationType.HIDDEN_RATE_LIMITS,
                                "has_rate_limit": has_rate_limit,
                            }
                        ))
        except Exception as e:
            logger.error(f"Rate limits check failed: {e}", exc_info=True)

        return violations

    def _check_authentication(self, code: str, action: Action) -> List[Violation]:
        """Check for authentication transparency."""
        violations = []

        try:
            # Check for authentication requirements
            has_auth = bool(re.search(r'@require|@auth|authenticate|authorization|bearer|token', code, re.IGNORECASE))

            if has_auth:
                # Check if auth is documented
                has_auth_docs = bool(re.search(r'(auth|token|bearer|api[_-]?key).*required', code, re.IGNORECASE))

                if not has_auth_docs:
                    violations.append(Violation(
                        principle="P2",
                        severity=ViolationSeverity.MEDIUM,
                        message="Authentication required but not clearly documented",
                        suggestion="Document authentication requirements in API docstring",
                        context={
                            "type": TransparencyViolationType.UNDOCUMENTED_AUTH,
                            "has_auth": has_auth,
                        }
                    ))
        except Exception as e:
            logger.error(f"Authentication check failed: {e}", exc_info=True)

        return violations

    def _check_deprecation(self, code: str, action: Action) -> List[Violation]:
        """Check for deprecation warnings."""
        violations = []

        try:
            # Check for deprecated patterns
            has_deprecated = bool(re.search(r'@deprecated|DeprecationWarning|deprecated\s*=\s*True', code, re.IGNORECASE))

            if 'delete' in action.intent.lower() or 'remove' in action.intent.lower():
                if not has_deprecated:
                    violations.append(Violation(
                        principle="P2",
                        severity=ViolationSeverity.LOW,
                        message="Removing/deprecating functionality without warning",
                        suggestion="Add @deprecated decorator or DeprecationWarning before removal",
                        context={
                            "type": TransparencyViolationType.NO_DEPRECATION_WARNING,
                            "intent": action.intent,
                        }
                    ))
        except Exception as e:
            logger.error(f"Deprecation check failed: {e}", exc_info=True)

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
    "P2ValidationError",
    "InvalidActionError",
    "ConfigurationError",
    "TransparencyViolationType",
    "P2Config",
    "P2_API_Validator",
]
