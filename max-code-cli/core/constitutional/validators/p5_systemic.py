"""
P5 Validator - Impacto Sistêmico

Production-grade validator ensuring systemic thinking and holistic impact analysis.

This validator enforces:
- Cross-component impact analysis
- Dependency chain validation
- Side effect detection
- Integration point checks
- Backward compatibility
- System-wide consistency

Biblical Foundation:
"Todas as coisas cooperam para o bem" (Romanos 8:28)

Constitutional Reference:
"Impacto Sistêmico" (Constituição Vértice v3.0 - P5)
"""

import re
import ast
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Pattern, Set
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

class P5ValidationError(Exception):
    """Base exception for P5 validation errors."""
    pass

class InvalidActionError(P5ValidationError):
    """Action is invalid or malformed."""
    pass

class ConfigurationError(P5ValidationError):
    """P5 configuration is invalid."""
    pass


# ============================================================================
# VIOLATION TYPES
# ============================================================================

class SystemicViolationType(str, Enum):
    """Types of P5 systemic violations."""
    MISSING_IMPACT_ANALYSIS = "missing_impact_analysis"
    BROKEN_DEPENDENCIES = "broken_dependencies"
    UNHANDLED_SIDE_EFFECTS = "unhandled_side_effects"
    INTEGRATION_RISK = "integration_risk"
    BACKWARD_INCOMPATIBLE = "backward_incompatible"
    INCONSISTENT_STATE = "inconsistent_state"
    CASCADE_FAILURE_RISK = "cascade_failure_risk"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class P5Config:
    """Immutable configuration for P5 Systemic Validator."""
    min_passing_score: float = 0.70
    strict_mode: bool = False
    require_impact_analysis: bool = True
    check_dependencies: bool = True
    check_side_effects: bool = True

    _import_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _mutation_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _integration_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compile regex patterns and validate config."""
        try:
            object.__setattr__(self, '_import_patterns', self._compile_import_patterns())
            object.__setattr__(self, '_mutation_patterns', self._compile_mutation_patterns())
            object.__setattr__(self, '_integration_patterns', self._compile_integration_patterns())

            if not 0.0 <= self.min_passing_score <= 1.0:
                raise ConfigurationError(f"min_passing_score must be 0.0-1.0, got {self.min_passing_score}")

            logger.debug(f"P5Config initialized: strict={self.strict_mode}, min_score={self.min_passing_score}")
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize P5Config: {e}") from e

    @staticmethod
    def _compile_import_patterns() -> List[Pattern]:
        """Compile patterns for imports/dependencies."""
        return [
            re.compile(r'^import\s+(\w+)', re.MULTILINE),
            re.compile(r'^from\s+(\w+)', re.MULTILINE),
            re.compile(r'require\(["\']([^"\']+)', re.IGNORECASE),
        ]

    @staticmethod
    def _compile_mutation_patterns() -> List[Pattern]:
        """Compile patterns for state mutations."""
        return [
            re.compile(r'\w+\s*=\s*', re.MULTILINE),
            re.compile(r'\.append\(', re.IGNORECASE),
            re.compile(r'\.update\(', re.IGNORECASE),
            re.compile(r'\.set\(', re.IGNORECASE),
            re.compile(r'global\s+\w+', re.IGNORECASE),
        ]

    @staticmethod
    def _compile_integration_patterns() -> List[Pattern]:
        """Compile patterns for integration points."""
        return [
            re.compile(r'@app\.route|@api\.|router\.', re.IGNORECASE),
            re.compile(r'requests\.(get|post|put|delete)', re.IGNORECASE),
            re.compile(r'database\.|db\.|session\.', re.IGNORECASE),
            re.compile(r'redis\.|cache\.|queue\.', re.IGNORECASE),
        ]

    @property
    def import_patterns(self) -> List[Pattern]:
        return self._import_patterns or []

    @property
    def mutation_patterns(self) -> List[Pattern]:
        return self._mutation_patterns or []

    @property
    def integration_patterns(self) -> List[Pattern]:
        return self._integration_patterns or []


# ============================================================================
# VALIDATOR
# ============================================================================

class P5_Systemic_Analyzer:
    """
    P5 Systemic Validator

    Validates that AI actions consider systemic impact.

    CHECKS:
    1. Impact analysis for changes
    2. Dependency chain validation
    3. Side effect detection
    4. Integration point safety
    5. Backward compatibility
    6. State consistency
    """

    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P5Config] = None):
        """Initialize P5 validator."""
        try:
            self.config = config or P5Config()
            logger.info("P5_Systemic_Analyzer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize P5 validator: {e}")
            raise ConfigurationError(f"Failed to initialize validator: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """Validate action against P5 Systemic principle."""
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
                    "P5": score,
                    "P6": 0.0,
                },
                suggestions=[v.suggestion for v in violations],
                metadata={
                    "principle": "P5",
                    "principle_name": "Impacto Sistêmico",
                    "checks_run": 6,
                    "violations_count": len(violations),
                    "critical_count": sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL),
                    "strict_mode": self.config.strict_mode,
                }
            )

            logger.debug(f"P5 validation complete: passed={passed}, score={score:.3f}, violations={len(violations)}")
            return result

        except InvalidActionError:
            raise
        except Exception as e:
            logger.exception("P5 validation failed unexpectedly")
            raise P5ValidationError(f"Validation failed: {e}") from e

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
        """Run all systemic checks."""
        violations = []

        checks = [
            (self._check_impact_analysis, "impact_analysis"),
            (self._check_dependencies, "dependencies"),
            (self._check_side_effects, "side_effects"),
            (self._check_integration_points, "integration_points"),
            (self._check_backward_compatibility, "backward_compatibility"),
            (self._check_state_consistency, "state_consistency"),
        ]

        for check_func, check_name in checks:
            try:
                violations.extend(check_func(code, action))
                logger.debug(f"P5 check '{check_name}': {len(violations)} violations")
            except Exception as e:
                logger.warning(f"P5 check '{check_name}' failed: {e}", exc_info=True)
                if self.config.strict_mode:
                    violations.append(Violation(
                        principle="P5",
                        severity=ViolationSeverity.MEDIUM,
                        message=f"Check '{check_name}' failed to execute",
                        suggestion="Review code for syntax errors or edge cases",
                        context={"check": check_name, "error": str(e)}
                    ))

        return violations

    def _check_impact_analysis(self, code: str, action: Action) -> List[Violation]:
        """Check for impact analysis."""
        violations = []

        if not self.config.require_impact_analysis:
            return violations

        try:
            # For significant changes, require impact documentation
            is_significant = (
                action.action_type in [ActionType.CODE_MODIFICATION, ActionType.FILE_DELETE] or
                len(code.strip()) > 200
            )

            if is_significant:
                has_impact_docs = (
                    action.context.get("impact_analysis", False) or
                    action.constitutional_context.get("impact_documented", False) or
                    bool(re.search(r'impact|affects|changes|modifies', action.intent, re.IGNORECASE))
                )

                if not has_impact_docs:
                    violations.append(Violation(
                        principle="P5",
                        severity=ViolationSeverity.MEDIUM,
                        message="Significant change without impact analysis",
                        suggestion="Document what components/systems are affected by this change",
                        context={
                            "type": SystemicViolationType.MISSING_IMPACT_ANALYSIS,
                            "code_length": len(code),
                        }
                    ))
        except Exception as e:
            logger.error(f"Impact analysis check failed: {e}", exc_info=True)

        return violations

    def _check_dependencies(self, code: str, action: Action) -> List[Violation]:
        """Check dependency management."""
        violations = []

        if not self.config.check_dependencies:
            return violations

        try:
            # Extract imports
            imports: Set[str] = set()
            for pattern in self.config.import_patterns:
                for match in pattern.finditer(code):
                    if match.groups():
                        imports.add(match.group(1))

            # Check for risky/heavy dependencies
            risky_deps = ['os', 'subprocess', 'eval', 'exec']
            found_risky = [dep for dep in risky_deps if dep in imports or dep in code]

            if found_risky:
                violations.append(Violation(
                    principle="P5",
                    severity=ViolationSeverity.HIGH,
                    message=f"Risky dependencies detected: {', '.join(found_risky)}",
                    suggestion="Review necessity of risky dependencies, add safety checks",
                    context={
                        "type": SystemicViolationType.BROKEN_DEPENDENCIES,
                        "risky_deps": found_risky,
                    }
                ))
        except Exception as e:
            logger.error(f"Dependencies check failed: {e}", exc_info=True)

        return violations

    def _check_side_effects(self, code: str, action: Action) -> List[Violation]:
        """Check for unhandled side effects."""
        violations = []

        if not self.config.check_side_effects:
            return violations

        try:
            # Detect mutations
            mutations = []
            for pattern in self.config.mutation_patterns:
                mutations.extend(pattern.findall(code))

            # Check for global state mutations
            has_global = bool(re.search(r'global\s+\w+', code, re.IGNORECASE))

            if has_global:
                violations.append(Violation(
                    principle="P5",
                    severity=ViolationSeverity.HIGH,
                    message="Global state mutation detected",
                    suggestion="Avoid global state; use dependency injection or context managers",
                    context={
                        "type": SystemicViolationType.UNHANDLED_SIDE_EFFECTS,
                        "has_global": has_global,
                    }
                ))
        except Exception as e:
            logger.error(f"Side effects check failed: {e}", exc_info=True)

        return violations

    def _check_integration_points(self, code: str, action: Action) -> List[Violation]:
        """Check integration point safety."""
        violations = []

        try:
            # Detect integration points
            integrations = []
            for pattern in self.config.integration_patterns:
                if pattern.search(code):
                    integrations.append(pattern.pattern)

            if integrations:
                # Check for error handling at integration points
                has_error_handling = bool(re.search(r'try:|except:|catch\(', code, re.IGNORECASE))

                if not has_error_handling:
                    violations.append(Violation(
                        principle="P5",
                        severity=ViolationSeverity.HIGH,
                        message="Integration points without error handling",
                        suggestion="Add try/except blocks for all external integrations",
                        context={
                            "type": SystemicViolationType.INTEGRATION_RISK,
                            "integration_count": len(integrations),
                        }
                    ))
        except Exception as e:
            logger.error(f"Integration points check failed: {e}", exc_info=True)

        return violations

    def _check_backward_compatibility(self, code: str, action: Action) -> List[Violation]:
        """Check backward compatibility."""
        violations = []

        try:
            # Check for breaking changes
            breaking_keywords = ['remove', 'delete', 'drop', 'deprecated']
            is_breaking = any(kw in action.intent.lower() for kw in breaking_keywords)

            if is_breaking:
                # Check for versioning or deprecation warnings
                has_version_handling = bool(re.search(
                    r'version|deprecated|migration|backward.*compat',
                    code,
                    re.IGNORECASE
                ))

                if not has_version_handling:
                    violations.append(Violation(
                        principle="P5",
                        severity=ViolationSeverity.HIGH,
                        message="Breaking change without compatibility layer",
                        suggestion="Add deprecation warnings, version checks, or migration path",
                        context={
                            "type": SystemicViolationType.BACKWARD_INCOMPATIBLE,
                            "intent": action.intent,
                        }
                    ))
        except Exception as e:
            logger.error(f"Backward compatibility check failed: {e}", exc_info=True)

        return violations

    def _check_state_consistency(self, code: str, action: Action) -> List[Violation]:
        """Check state consistency."""
        violations = []

        try:
            # Check for transaction boundaries
            has_transactions = bool(re.search(
                r'transaction|commit|rollback|atomic|BEGIN|COMMIT',
                code,
                re.IGNORECASE
            ))

            # Check for state mutations
            has_mutations = any(pattern.search(code) for pattern in self.config.mutation_patterns)

            # Database operations should use transactions
            has_db = bool(re.search(r'database|db\.|INSERT|UPDATE|DELETE', code, re.IGNORECASE))

            if has_db and has_mutations and not has_transactions:
                violations.append(Violation(
                    principle="P5",
                    severity=ViolationSeverity.MEDIUM,
                    message="Database operations without transaction boundaries",
                    suggestion="Wrap related database operations in transactions for consistency",
                    context={
                        "type": SystemicViolationType.INCONSISTENT_STATE,
                        "has_db": has_db,
                        "has_mutations": has_mutations,
                    }
                ))
        except Exception as e:
            logger.error(f"State consistency check failed: {e}", exc_info=True)

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
    "P5ValidationError",
    "InvalidActionError",
    "ConfigurationError",
    "SystemicViolationType",
    "P5Config",
    "P5_Systemic_Analyzer",
]
