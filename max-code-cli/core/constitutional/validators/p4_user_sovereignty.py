"""
P4 Validator - Soberania do Usuário

Validates compliance with P4: User Sovereignty principle.

This validator ensures that AI actions respect user control, consent, and privacy.

Biblical Foundation:
"Tudo me é lícito, mas nem tudo convém" (1 Coríntios 10:23)
"Aquele que vos chama é fiel" (1 Tessalonicenses 5:24)

PRINCÍPIO P4 - SOBERANIA DO USUÁRIO:
- User consent for external API calls
- Confirmation prompts for destructive operations
- Privacy controls and data protection
- No automated actions without user approval
- Transparency in AI actions
"""

import logging
import re
import ast
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


class P4ValidationError(Exception):
    """Base exception for P4 validation errors."""
    pass


class InvalidActionError(P4ValidationError):
    """Action is invalid or malformed."""
    pass


class ConfigurationError(P4ValidationError):
    """P4 configuration is invalid."""
    pass


# ============================================================================
# VIOLATION TYPES
# ============================================================================


class SovereigntyViolationType(str, Enum):
    """Types of P4 sovereignty violations."""
    MISSING_CONSENT = "missing_consent"
    NO_CONFIRMATION = "no_confirmation"
    PRIVACY_LEAK = "privacy_leak"
    UNAUTHORIZED_ACTION = "unauthorized_action"
    NO_USER_CONTROL = "no_user_control"
    AUTOMATED_DESTRUCTIVE = "automated_destructive"
    MISSING_APPROVAL = "missing_approval"
    FORCED_ACTION = "forced_action"


# ============================================================================
# CONFIGURATION
# ============================================================================


@dataclass(frozen=True)
class P4Config:
    """
    Immutable configuration for P4 User Sovereignty Validator.

    Using frozen dataclass for thread safety and immutability.
    All regex patterns are compiled in __post_init__ for performance.
    """
    min_passing_score: float = 0.70
    strict_mode: bool = False
    require_confirmation_for_destructive: bool = True
    require_consent_for_external: bool = True
    allow_automated_safe_actions: bool = True

    # Pre-compiled regex patterns (private, set in __post_init__)
    _destructive_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _external_api_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _privacy_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _consent_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)
    _confirmation_patterns: Optional[List[Pattern]] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """
        Compile all regex patterns for performance.
        Validate configuration parameters.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        try:
            # Compile patterns (performance optimization)
            object.__setattr__(self, '_destructive_patterns', self._compile_destructive_patterns())
            object.__setattr__(self, '_external_api_patterns', self._compile_external_api_patterns())
            object.__setattr__(self, '_privacy_patterns', self._compile_privacy_patterns())
            object.__setattr__(self, '_consent_patterns', self._compile_consent_patterns())
            object.__setattr__(self, '_confirmation_patterns', self._compile_confirmation_patterns())

            # Validate configuration bounds
            if not 0.0 <= self.min_passing_score <= 1.0:
                raise ConfigurationError(
                    f"min_passing_score must be between 0.0 and 1.0, got {self.min_passing_score}"
                )

            logger.debug(f"P4Config initialized: strict_mode={self.strict_mode}, min_score={self.min_passing_score}")

        except re.error as e:
            raise ConfigurationError(f"Failed to compile regex patterns: {e}") from e
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize P4Config: {e}") from e

    @staticmethod
    def _compile_destructive_patterns() -> List[Pattern]:
        """Compile patterns for destructive operations."""
        patterns = [
            r'\brm\b',
            r'\bunlink\b',
            r'\bremove\b',
            r'\bdelete\b',
            r'\bdrop\b',
            r'\btruncate\b',
            r'\bpurge\b',
            r'\bwipe\b',
            r'\berase\b',
            r'\bshutil\.rmtree\b',
            r'\bos\.remove\b',
            r'\bos\.unlink\b',
            r'\bos\.rmdir\b',
            r'\bpathlib\.Path\.unlink\b',
            r'\bgit\s+push\s+--force\b',
            r'\bgit\s+reset\s+--hard\b',
            r'\bgit\s+clean\s+-fd\b',
            r'\.drop\(\)',  # pandas/database drop
            r'DELETE\s+FROM\s+',  # SQL DELETE
            r'DROP\s+(TABLE|DATABASE)',  # SQL DROP
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]

    @staticmethod
    def _compile_external_api_patterns() -> List[Pattern]:
        """Compile patterns for external API calls."""
        patterns = [
            r'requests\.(get|post|put|delete|patch)',
            r'urllib\.request',
            r'http\.client',
            r'httpx\.',
            r'aiohttp\.',
            r'fetch\(',
            r'axios\.',
            r'@app\.route',
            r'@api\.route',
            r'anthropic\.Anthropic\(',
            r'openai\.',
            r'OpenAI\(',
            r'claude\.',
            r'gpt-',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]

    @staticmethod
    def _compile_privacy_patterns() -> List[Pattern]:
        """Compile patterns for privacy concerns."""
        patterns = [
            r'\bpassword\s*=',
            r'\bemail\s*=',
            r'\bphone\s*=',
            r'\bssn\s*=',
            r'\bcredit_card\s*=',
            r'\bapi_key\s*=',
            r'\btoken\s*=',
            r'\bprivate_key\s*=',
            r'user_data',
            r'personal_info',
            r'sensitive_data',
            r'\.telemetry',
            r'\.tracking',
            r'\.analytics',
            r'send_to_server',
            r'upload_data',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]

    @staticmethod
    def _compile_consent_patterns() -> List[Pattern]:
        """Compile patterns indicating consent mechanisms."""
        patterns = [
            r'user_consent',
            r'get_consent',
            r'ask_permission',
            r'request_approval',
            r'user_approved',
            r'has_permission',
            r'check_authorization',
            r'if\s+consent',
            r'if\s+approved',
            r'AskUserQuestion',
            r'input\(',
            r'prompt\(',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]

    @staticmethod
    def _compile_confirmation_patterns() -> List[Pattern]:
        """Compile patterns indicating confirmation prompts."""
        patterns = [
            r'confirm',
            r'are\s+you\s+sure',
            r'proceed\?',
            r'continue\?',
            r'yes/no',
            r'y/n',
            r'AskUserQuestion',
            r'input\(["\'].*confirm',
            r'input\(["\'].*sure',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]

    @property
    def destructive_patterns(self) -> List[Pattern]:
        """Get compiled destructive operation patterns."""
        return self._destructive_patterns or []

    @property
    def external_api_patterns(self) -> List[Pattern]:
        """Get compiled external API patterns."""
        return self._external_api_patterns or []

    @property
    def privacy_patterns(self) -> List[Pattern]:
        """Get compiled privacy patterns."""
        return self._privacy_patterns or []

    @property
    def consent_patterns(self) -> List[Pattern]:
        """Get compiled consent patterns."""
        return self._consent_patterns or []

    @property
    def confirmation_patterns(self) -> List[Pattern]:
        """Get compiled confirmation patterns."""
        return self._confirmation_patterns or []


# ============================================================================
# VALIDATOR
# ============================================================================


class P4_User_Sovereignty_Validator:
    """
    P4 User Sovereignty Validator

    Validates that AI actions respect user control, consent, and privacy.

    CHECKS:
    1. Destructive operations require confirmation
    2. External API calls require consent
    3. Privacy-sensitive data handling
    4. No unauthorized automated actions
    5. User control mechanisms present
    6. Forced actions detection

    Implements enterprise patterns:
    - Comprehensive error handling
    - Fail-safe mechanisms
    - Cascade failure prevention
    - Thread-safe configuration
    - Performance optimization (compiled regex)
    - Security (context-aware validation)
    """

    # Severity weights for score calculation
    SEVERITY_WEIGHTS = {
        ViolationSeverity.CRITICAL: 1.0,
        ViolationSeverity.HIGH: 0.20,
        ViolationSeverity.MEDIUM: 0.10,
        ViolationSeverity.LOW: 0.05,
    }

    def __init__(self, config: Optional[P4Config] = None):
        """
        Initialize P4 validator.

        Args:
            config: Optional P4Config instance. Defaults to P4Config().
        """
        try:
            self.config = config or P4Config()
            logger.info("P4_User_Sovereignty_Validator initialized")
        except Exception as e:
            logger.error(f"Failed to initialize P4 validator: {e}")
            raise ConfigurationError(f"Failed to initialize validator: {e}") from e

    def validate(self, action: Action) -> ConstitutionalResult:
        """
        Validate action against P4 User Sovereignty principle.

        Args:
            action: Action to validate

        Returns:
            ConstitutionalResult with pass/fail, score, and violations

        Raises:
            InvalidActionError: If action is malformed
            P4ValidationError: If validation fails unexpectedly
        """
        try:
            # Validate action structure
            self._validate_action(action)

            # Extract code safely
            code = self._extract_code_safe(action)

            # Run all sovereignty checks
            violations = self._run_all_checks(code, action)

            # Calculate score robustly
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
                    "P3": 0.0,
                    "P4": score,  # This validator only scores P4
                    "P5": 0.0,
                    "P6": 0.0,
                },
                suggestions=[v.suggestion for v in violations],
                metadata={
                    "principle": "P4",
                    "total_violations": len(violations),
                    "critical_violations": sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL),
                    "high_violations": sum(1 for v in violations if v.severity == ViolationSeverity.HIGH),
                    "config": {
                        "strict_mode": self.config.strict_mode,
                        "require_confirmation": self.config.require_confirmation_for_destructive,
                        "require_consent": self.config.require_consent_for_external,
                    }
                }
            )

            logger.debug(
                f"P4 validation complete: passed={passed}, score={score:.3f}, "
                f"violations={len(violations)}"
            )

            return result

        except InvalidActionError:
            # Re-raise validation errors
            raise
        except Exception as e:
            # Log and wrap unexpected errors
            logger.exception("P4 validation failed unexpectedly")
            raise P4ValidationError(f"Validation failed: {e}") from e

    def _validate_action(self, action: Action) -> None:
        """
        Validate action structure.

        Args:
            action: Action to validate

        Raises:
            InvalidActionError: If action is invalid
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
        Safely extract code from action.

        Args:
            action: Action containing code

        Returns:
            Code string (empty if not found)
        """
        try:
            # Try multiple context keys
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
        """
        Run all sovereignty checks.

        Implements cascade failure prevention: if one check fails,
        continue with remaining checks.

        Args:
            code: Code to check
            action: Original action (for context)

        Returns:
            List of violations (may be empty)
        """
        violations = []

        # Define all checks
        checks = [
            (self._check_destructive_without_confirmation, "destructive_confirmation"),
            (self._check_external_without_consent, "external_consent"),
            (self._check_privacy_violations, "privacy"),
            (self._check_unauthorized_automation, "unauthorized_automation"),
            (self._check_missing_user_control, "user_control"),
            (self._check_forced_actions, "forced_actions"),
        ]

        # Run each check with error isolation
        for check_func, check_name in checks:
            try:
                check_violations = check_func(code, action)
                violations.extend(check_violations)
                logger.debug(f"P4 check '{check_name}': {len(check_violations)} violations")
            except Exception as e:
                # Log but continue with other checks
                logger.warning(f"P4 check '{check_name}' failed: {e}", exc_info=True)
                # Add a violation for the failed check in strict mode
                if self.config.strict_mode:
                    violations.append(Violation(
                        principle="P4",
                        severity=ViolationSeverity.MEDIUM,
                        message=f"Check '{check_name}' failed to execute",
                        suggestion="Review code for syntax errors or edge cases",
                        context={"check": check_name, "error": str(e)}
                    ))

        return violations

    def _check_destructive_without_confirmation(self, code: str, action: Action) -> List[Violation]:
        """
        Check for destructive operations without confirmation.

        DESTRUCTIVE OPERATIONS:
        - File deletion (rm, unlink, remove)
        - Database drops
        - Force pushes
        - Directory removal

        Args:
            code: Code to check
            action: Action context

        Returns:
            List of violations
        """
        violations = []

        if not self.config.require_confirmation_for_destructive:
            return violations

        try:
            # Check if code contains destructive operations
            has_destructive = False
            destructive_matches = []

            for pattern in self.config.destructive_patterns:
                try:
                    matches = list(pattern.finditer(code))
                    if matches:
                        has_destructive = True
                        destructive_matches.extend([m.group() for m in matches])
                except re.error as e:
                    logger.error(f"Regex error in destructive check: {e}")

            if not has_destructive:
                return violations

            # Check if confirmation mechanism is present
            has_confirmation = False
            for pattern in self.config.confirmation_patterns:
                try:
                    if pattern.search(code):
                        has_confirmation = True
                        break
                except re.error as e:
                    logger.error(f"Regex error in confirmation check: {e}")

            # Check action context for approval
            context_has_approval = (
                action.context.get("user_approved", False) or
                action.context.get("confirmed", False) or
                action.constitutional_context.get("user_consent", False)
            )

            if not has_confirmation and not context_has_approval:
                violations.append(Violation(
                    principle="P4",
                    severity=ViolationSeverity.CRITICAL,
                    message="Destructive operation without user confirmation",
                    suggestion=(
                        "Add confirmation prompt before destructive operations: "
                        "AskUserQuestion or check action.context['user_approved']"
                    ),
                    context={
                        "type": SovereigntyViolationType.NO_CONFIRMATION,
                        "destructive_operations": destructive_matches[:5],  # Limit to 5
                        "has_confirmation": has_confirmation,
                        "has_approval": context_has_approval,
                    }
                ))

        except Exception as e:
            logger.error(f"Destructive check failed: {e}", exc_info=True)

        return violations

    def _check_external_without_consent(self, code: str, action: Action) -> List[Violation]:
        """
        Check for external API calls without consent.

        EXTERNAL CALLS:
        - HTTP requests
        - External API calls (OpenAI, Anthropic, etc.)
        - Database connections

        Args:
            code: Code to check
            action: Action context

        Returns:
            List of violations
        """
        violations = []

        if not self.config.require_consent_for_external:
            return violations

        try:
            # Check if code contains external API calls
            has_external = False
            external_matches = []

            for pattern in self.config.external_api_patterns:
                try:
                    matches = list(pattern.finditer(code))
                    if matches:
                        has_external = True
                        external_matches.extend([m.group() for m in matches])
                except re.error as e:
                    logger.error(f"Regex error in external API check: {e}")

            if not has_external:
                return violations

            # Check if consent mechanism is present
            has_consent = False
            for pattern in self.config.consent_patterns:
                try:
                    if pattern.search(code):
                        has_consent = True
                        break
                except re.error as e:
                    logger.error(f"Regex error in consent check: {e}")

            # Check action context for consent
            context_has_consent = (
                action.context.get("user_consent", False) or
                action.context.get("external_approved", False) or
                action.constitutional_context.get("api_consent", False)
            )

            if not has_consent and not context_has_consent:
                violations.append(Violation(
                    principle="P4",
                    severity=ViolationSeverity.HIGH,
                    message="External API call without user consent",
                    suggestion=(
                        "Request consent before external calls: "
                        "AskUserQuestion or check action.context['user_consent']"
                    ),
                    context={
                        "type": SovereigntyViolationType.MISSING_CONSENT,
                        "external_calls": external_matches[:5],  # Limit to 5
                        "has_consent": has_consent,
                        "has_approval": context_has_consent,
                    }
                ))

        except Exception as e:
            logger.error(f"External consent check failed: {e}", exc_info=True)

        return violations

    def _check_privacy_violations(self, code: str, action: Action) -> List[Violation]:
        """
        Check for privacy violations.

        PRIVACY CONCERNS:
        - Handling sensitive data without safeguards
        - Logging passwords/tokens
        - Telemetry without consent

        Args:
            code: Code to check
            action: Action context

        Returns:
            List of violations
        """
        violations = []

        try:
            for pattern in self.config.privacy_patterns:
                try:
                    for match in pattern.finditer(code):
                        # Check if there's consent for privacy-sensitive operations
                        has_privacy_consent = (
                            action.context.get("privacy_consent", False) or
                            action.constitutional_context.get("data_consent", False)
                        )

                        if not has_privacy_consent:
                            violations.append(Violation(
                                principle="P4",
                                severity=ViolationSeverity.HIGH,
                                message="Privacy-sensitive data handling without consent",
                                suggestion="Request explicit consent for handling sensitive data",
                                context={
                                    "type": SovereigntyViolationType.PRIVACY_LEAK,
                                    "matched": match.group()[:50],  # Limit length
                                }
                            ))
                            break  # One violation per pattern is enough

                except re.error as e:
                    logger.error(f"Regex error in privacy check: {e}")

        except Exception as e:
            logger.error(f"Privacy check failed: {e}", exc_info=True)

        return violations

    def _check_unauthorized_automation(self, code: str, action: Action) -> List[Violation]:
        """
        Check for unauthorized automated actions.

        AUTOMATED ACTIONS that need approval:
        - Git commits/pushes
        - File modifications
        - System commands

        Args:
            code: Code to check
            action: Action context

        Returns:
            List of violations
        """
        violations = []

        try:
            # Patterns for automated actions
            automation_patterns = [
                r'git\s+commit',
                r'git\s+push',
                r'subprocess\.',
                r'os\.system',
                r'exec\(',
                r'eval\(',
            ]

            for pattern_str in automation_patterns:
                try:
                    pattern = re.compile(pattern_str, re.IGNORECASE)
                    if pattern.search(code):
                        # Check if automation is authorized
                        has_automation_approval = (
                            action.context.get("automation_approved", False) or
                            action.constitutional_context.get("auto_consent", False) or
                            (self.config.allow_automated_safe_actions and
                             action.action_type in [ActionType.READ, ActionType.ANALYZE])
                        )

                        if not has_automation_approval:
                            violations.append(Violation(
                                principle="P4",
                                severity=ViolationSeverity.MEDIUM,
                                message="Automated action without authorization",
                                suggestion="Request user approval for automated actions",
                                context={
                                    "type": SovereigntyViolationType.UNAUTHORIZED_ACTION,
                                    "pattern": pattern_str,
                                }
                            ))
                            break  # One violation is enough

                except re.error as e:
                    logger.error(f"Regex error in automation check: {e}")

        except Exception as e:
            logger.error(f"Automation check failed: {e}", exc_info=True)

        return violations

    def _check_missing_user_control(self, code: str, action: Action) -> List[Violation]:
        """
        Check for missing user control mechanisms.

        USER CONTROL includes:
        - Ability to cancel operations
        - Progress visibility
        - Undo mechanisms

        Args:
            code: Code to check
            action: Action context

        Returns:
            List of violations
        """
        violations = []

        try:
            # For long-running or complex operations, check for control mechanisms
            is_complex = (
                len(code) > 500 or
                action.action_type in [ActionType.EXECUTE, ActionType.MODIFY] or
                any(keyword in code.lower() for keyword in ['loop', 'while', 'for'])
            )

            if is_complex:
                # Check for control mechanisms
                control_patterns = [
                    r'cancel',
                    r'abort',
                    r'stop',
                    r'interrupt',
                    r'undo',
                    r'rollback',
                    r'progress',
                    r'status',
                ]

                has_control = False
                for pattern_str in control_patterns:
                    try:
                        if re.search(pattern_str, code, re.IGNORECASE):
                            has_control = True
                            break
                    except re.error as e:
                        logger.error(f"Regex error in control check: {e}")

                # Check context for control flags
                context_has_control = (
                    action.context.get("cancellable", False) or
                    action.context.get("has_progress", False) or
                    action.constitutional_context.get("user_control", False)
                )

                if not has_control and not context_has_control:
                    violations.append(Violation(
                        principle="P4",
                        severity=ViolationSeverity.MEDIUM,
                        message="Complex operation lacks user control mechanisms",
                        suggestion="Add cancel/undo capability or progress visibility",
                        context={
                            "type": SovereigntyViolationType.NO_USER_CONTROL,
                            "code_length": len(code),
                            "action_type": str(action.action_type),
                        }
                    ))

        except Exception as e:
            logger.error(f"User control check failed: {e}", exc_info=True)

        return violations

    def _check_forced_actions(self, code: str, action: Action) -> List[Violation]:
        """
        Check for forced actions (no opt-out).

        FORCED ACTIONS:
        - No way to decline
        - Automatic execution without choice
        - Hidden side effects

        Args:
            code: Code to check
            action: Action context

        Returns:
            List of violations
        """
        violations = []

        try:
            # AST-based detection of forced actions
            try:
                tree = ast.parse(code)

                # Look for functions that don't check user input
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check if function has side effects without user checks
                        has_side_effects = False
                        has_user_check = False

                        for child in ast.walk(node):
                            # Side effects: file writes, API calls, etc.
                            if isinstance(child, ast.Call):
                                func_name = self._get_func_name(child)
                                if any(keyword in func_name.lower() for keyword in
                                      ['write', 'delete', 'send', 'post', 'commit']):
                                    has_side_effects = True

                            # User checks: if statements checking approval
                            if isinstance(child, ast.If):
                                test_str = ast.unparse(child.test) if hasattr(ast, 'unparse') else ""
                                if any(keyword in test_str.lower() for keyword in
                                      ['approved', 'consent', 'confirm', 'allow']):
                                    has_user_check = True

                        if has_side_effects and not has_user_check:
                            violations.append(Violation(
                                principle="P4",
                                severity=ViolationSeverity.MEDIUM,
                                message=f"Function '{node.name}' has side effects without user check",
                                suggestion="Add user approval check before executing side effects",
                                context={
                                    "type": SovereigntyViolationType.FORCED_ACTION,
                                    "function": node.name,
                                    "line": node.lineno,
                                }
                            ))

            except SyntaxError:
                # Not valid Python, skip AST analysis
                logger.debug("Code is not valid Python, skipping AST analysis")

        except Exception as e:
            logger.error(f"Forced actions check failed: {e}", exc_info=True)

        return violations

    def _get_func_name(self, call_node: ast.Call) -> str:
        """
        Safely extract function name from Call node.

        Args:
            call_node: AST Call node

        Returns:
            Function name (empty string if not extractable)
        """
        try:
            if isinstance(call_node.func, ast.Name):
                return call_node.func.id
            elif isinstance(call_node.func, ast.Attribute):
                return call_node.func.attr
            else:
                return ""
        except Exception as e:
            logger.debug(f"Failed to extract function name: {e}")
            return ""

    def _calculate_score_robust(self, violations: List[Violation]) -> float:
        """
        Calculate score with robust error handling.

        Score = 1.0 - (weighted sum of violations)

        Args:
            violations: List of violations

        Returns:
            Score between 0.0 and 1.0 (0.0 on error)
        """
        try:
            if not violations:
                return 1.0

            # Calculate weighted penalty
            penalty = 0.0
            for violation in violations:
                try:
                    weight = self.SEVERITY_WEIGHTS.get(violation.severity, 0.05)
                    penalty += weight
                except Exception as e:
                    logger.warning(f"Failed to process violation {violation}: {e}")

            # Score = 1.0 - penalty (clamped to [0.0, 1.0])
            score = max(0.0, min(1.0, 1.0 - penalty))

            logger.debug(f"Calculated score: {score:.3f} (penalty={penalty:.3f})")
            return score

        except Exception as e:
            logger.error(f"Score calculation failed: {e}", exc_info=True)
            return 0.0  # Fail-safe: return worst score on error

    def _determine_passed(self, score: float, violations: List[Violation]) -> bool:
        """
        Determine if validation passed.

        PASS CONDITIONS:
        - Score >= min_passing_score
        - No CRITICAL violations (in strict mode)

        Args:
            score: Calculated score
            violations: List of violations

        Returns:
            True if passed, False otherwise
        """
        try:
            # Check score threshold
            score_passed = score >= self.config.min_passing_score

            # In strict mode, no CRITICAL violations allowed
            if self.config.strict_mode:
                has_critical = any(
                    v.severity == ViolationSeverity.CRITICAL
                    for v in violations
                )
                if has_critical:
                    logger.debug("Failed due to CRITICAL violations in strict mode")
                    return False

            logger.debug(f"Validation passed: {score_passed} (score={score:.3f})")
            return score_passed

        except Exception as e:
            logger.error(f"Pass determination failed: {e}", exc_info=True)
            return False  # Fail-safe: return False on error


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    "P4ValidationError",
    "InvalidActionError",
    "ConfigurationError",
    "SovereigntyViolationType",
    "P4Config",
    "P4_User_Sovereignty_Validator",
]
