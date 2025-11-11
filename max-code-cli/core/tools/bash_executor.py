"""
Bash Executor Tool - Execução Segura de Comandos Shell

Design Philosophy (Boris Principle):
"Um comando bash é uma interface com o sistema. Deve ser tratado
com o mesmo cuidado que uma transação financeira ou uma operação
cirúrgica: validado, monitorado, e reversível quando possível."

Princípios:
1. Zero Trust - Validar TUDO antes de executar
2. Fail Safe - Default para seguro, não conveniente
3. Observability - Log completo de todas operações
4. Graceful Degradation - Falhar elegantemente

Soli Deo Gloria 🙏
"""

import subprocess
import shlex
import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import re

from core.tools.types import ToolResult, ToolResultType, ToolContent
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class CommandValidationResult:
    """Resultado de validação de comando"""
    safe: bool
    reason: Optional[str] = None
    risk_level: str = "low"  # low, medium, high, critical
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ExecutionResult:
    """Resultado detalhado de execução"""
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    timestamp: str
    safe: bool


class CommandValidator:
    """
    Validador de comandos bash.

    Baseado em Security Best Practices:
    - OWASP Command Injection Prevention
    - CIS Benchmark for Linux
    - NIST Cybersecurity Framework
    """

    # Comandos perigosos que devem ser bloqueados
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf\s+/',           # rm -rf /
        r'mkfs\.',                  # Format filesystem
        r'dd\s+if=',               # Disk destroyer
        r':\(\)\{.*:\|:&\s*\};:',  # Fork bomb
        r'>\s*/dev/sd[a-z]',       # Write to disk directly
        r'chmod\s+777',            # Insecure permissions
        r'curl.*\|.*sh',           # Pipe to shell (risky)
        r'wget.*\|.*sh',           # Pipe to shell (risky)
        r'/etc/passwd',            # Access sensitive files
        r'/etc/shadow',            # Access sensitive files
    ]

    # Comandos que requerem confirmação
    REQUIRES_CONFIRMATION = [
        r'rm\s+-r',                # Recursive delete
        r'git\s+push\s+.*--force', # Force push
        r'docker\s+rm',            # Remove container
        r'npm\s+uninstall',        # Uninstall package
    ]

    # Comandos permitidos (whitelist para modo strict)
    SAFE_COMMANDS = [
        'ls', 'cat', 'echo', 'pwd', 'whoami', 'date',
        'git status', 'git diff', 'git log', 'git branch',
        'npm --version', 'node --version', 'python --version',
        'pip list', 'pip show', 'pytest --version'
    ]

    def validate(self, command: str, strict: bool = False) -> CommandValidationResult:
        """
        Validar comando bash.

        Args:
            command: Comando a validar
            strict: Modo strict (apenas whitelist)

        Returns:
            CommandValidationResult
        """
        command = command.strip()

        # Empty command
        if not command:
            return CommandValidationResult(
                safe=False,
                reason="Empty command",
                risk_level="low"
            )

        # Strict mode: apenas whitelist
        if strict:
            if command not in self.SAFE_COMMANDS:
                return CommandValidationResult(
                    safe=False,
                    reason=f"Command not in whitelist (strict mode)",
                    risk_level="medium",
                    suggestions=self.SAFE_COMMANDS[:5]
                )

        # Check dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return CommandValidationResult(
                    safe=False,
                    reason=f"Dangerous command blocked: matches pattern '{pattern}'",
                    risk_level="critical",
                    suggestions=[
                        "Review command for safety",
                        "Use safer alternatives",
                        "Run in sandboxed environment"
                    ]
                )

        # Check if requires confirmation
        for pattern in self.REQUIRES_CONFIRMATION:
            if re.search(pattern, command, re.IGNORECASE):
                return CommandValidationResult(
                    safe=True,  # Safe but needs confirmation
                    reason=f"Command requires confirmation: matches pattern '{pattern}'",
                    risk_level="high",
                    suggestions=["Confirm before executing"]
                )

        # Command injection check
        if self._has_injection_risk(command):
            return CommandValidationResult(
                safe=False,
                reason="Potential command injection detected",
                risk_level="high",
                suggestions=[
                    "Avoid special characters: ; | & $ ` \\ \" '",
                    "Use proper escaping",
                    "Consider using dedicated tools"
                ]
            )

        # All checks passed
        return CommandValidationResult(
            safe=True,
            risk_level="low"
        )

    def _has_injection_risk(self, command: str) -> bool:
        """Detectar risco de command injection"""
        # Caracteres suspeitos para injection
        injection_chars = [';', '|', '&', '$(', '`', '\n', '\r']

        # Permitir alguns casos legítimos
        # Example: git commit -m "message with ; in it" é OK
        # Example: echo "test" | grep "test" pode ser OK

        # Por enquanto, detecção simples
        # TODO: Melhorar com parsing mais sofisticado

        suspicious_count = sum(1 for char in injection_chars if char in command)

        # Se tem muitos caracteres suspeitos, provável injection
        return suspicious_count > 2


class BashExecutor:
    """
    Bash Command Executor with Safety Guarantees.

    Features:
    - Command validation (dangerous pattern detection)
    - Timeout enforcement (prevent hanging)
    - Output capture (stdout + stderr)
    - Exit code handling
    - Execution time tracking
    - Comprehensive logging

    Usage:
        executor = BashExecutor()
        result = executor.execute("ls -la")

        if result.type == "success":
            print(result.content[0].text)
    """

    def __init__(self,
                 default_timeout: int = 30,
                 strict_mode: bool = False,
                 log_commands: bool = True):
        """
        Initialize bash executor.

        Args:
            default_timeout: Default timeout in seconds (default: 30)
            strict_mode: Enable strict validation (whitelist only)
            log_commands: Log all executed commands
        """
        self.default_timeout = default_timeout
        self.strict_mode = strict_mode
        self.log_commands = log_commands
        self.validator = CommandValidator()

        # Execution history (for debugging)
        self.execution_history: List[ExecutionResult] = []

        logger.info(f"BashExecutor initialized (timeout={default_timeout}s, strict={strict_mode})")

    def execute(self,
                command: str,
                timeout: Optional[int] = None,
                cwd: Optional[str] = None,
                env: Optional[Dict[str, str]] = None,
                require_confirmation: bool = False) -> ToolResult:
        """
        Execute bash command safely.

        Args:
            command: Bash command to execute
            timeout: Timeout in seconds (None = use default)
            cwd: Working directory (None = current)
            env: Environment variables (None = inherit)
            require_confirmation: Whether to require user confirmation

        Returns:
            ToolResult with execution results

        Examples:
            >>> executor = BashExecutor()
            >>> result = executor.execute("echo 'hello'")
            >>> print(result.content[0].text)
            'hello'

            >>> result = executor.execute("sleep 100", timeout=1)
            >>> print(result.type)  # "error" (timeout)
        """
        start_time = datetime.now()

        # Use default timeout if not specified
        if timeout is None:
            timeout = self.default_timeout

        # Log command
        if self.log_commands:
            logger.info(f"Executing command: {command}")

        # Validate command
        validation = self.validator.validate(command, strict=self.strict_mode)

        if not validation.safe:
            logger.error(f"Command validation failed: {validation.reason}")
            return ToolResult.error(
                f"🚫 Command blocked: {validation.reason}\n\n"
                f"Risk level: {validation.risk_level}\n"
                f"Suggestions:\n" + "\n".join(f"  - {s}" for s in validation.suggestions),
                validation_failed=True,
                risk_level=validation.risk_level
            )

        # Check if requires confirmation
        if validation.risk_level == "high" and not require_confirmation:
            return ToolResult.error(
                f"⚠️  Command requires confirmation: {validation.reason}\n\n"
                f"This command may have significant effects. "
                f"Please review carefully before proceeding.",
                requires_confirmation=True
            )

        # Execute command
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=env
            )

            # Calculate execution time
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Store execution result
            exec_result = ExecutionResult(
                command=command,
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_ms=duration_ms,
                timestamp=datetime.now().isoformat(),
                safe=True
            )
            self.execution_history.append(exec_result)

            # Log result
            logger.info(f"Command completed (exit_code={result.returncode}, duration={duration_ms:.2f}ms)")

            # Return appropriate result
            if result.returncode == 0:
                # Success
                output = result.stdout if result.stdout else "(no output)"

                return ToolResult.success(
                    output,
                    exit_code=result.returncode,
                    duration_ms=duration_ms,
                    stderr=result.stderr if result.stderr else None
                )
            else:
                # Non-zero exit code (command failed)
                error_msg = result.stderr if result.stderr else "(no error message)"

                return ToolResult.error(
                    f"❌ Command failed (exit code {result.returncode}):\n\n{error_msg}",
                    exit_code=result.returncode,
                    stdout=result.stdout if result.stdout else None,
                    duration_ms=duration_ms
                )

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s")
            return ToolResult.error(
                f"⏱️  Command timed out after {timeout} seconds.\n\n"
                f"Consider:\n"
                f"  - Increasing timeout\n"
                f"  - Running command in background\n"
                f"  - Breaking into smaller operations",
                timeout=True,
                timeout_seconds=timeout
            )

        except Exception as e:
            logger.exception(f"Execution error: {e}")
            return ToolResult.error(
                f"💥 Execution error: {str(e)}\n\n"
                f"This is an unexpected error. Please check:\n"
                f"  - Command syntax\n"
                f"  - System resources\n"
                f"  - Permissions",
                exception=str(e),
                exception_type=type(e).__name__
            )

    def get_history(self, limit: int = 10) -> List[ExecutionResult]:
        """Get recent execution history"""
        return self.execution_history[-limit:]

    def clear_history(self):
        """Clear execution history"""
        self.execution_history.clear()
        logger.info("Execution history cleared")


# Convenience function for quick execution
def execute_bash(command: str, timeout: int = 30) -> ToolResult:
    """
    Quick bash execution (convenience function).

    Args:
        command: Bash command
        timeout: Timeout in seconds

    Returns:
        ToolResult
    """
    executor = BashExecutor(default_timeout=timeout)
    return executor.execute(command)


if __name__ == "__main__":
    # Self-test
    print("🧪 BashExecutor Self-Test\n")

    executor = BashExecutor()

    # Test 1: Safe command
    print("Test 1: Safe command (echo)")
    result = executor.execute("echo 'Hello, Boris!'")
    print(f"  Status: {result.type}")
    print(f"  Output: {result.content[0].text if result.content else 'N/A'}\n")

    # Test 2: Dangerous command (blocked)
    print("Test 2: Dangerous command (rm -rf /)")
    result = executor.execute("rm -rf /")
    print(f"  Status: {result.type}")
    print(f"  Message: {result.content[0].text if result.content else 'N/A'}\n")

    # Test 3: Timeout
    print("Test 3: Timeout (sleep 10 with 1s timeout)")
    result = executor.execute("sleep 10", timeout=1)
    print(f"  Status: {result.type}")
    print(f"  Message: {result.content[0].text[:100] if result.content else 'N/A'}...\n")

    # Test 4: Non-existent command
    print("Test 4: Non-existent command")
    result = executor.execute("command_that_does_not_exist_12345")
    print(f"  Status: {result.type}")
    print(f"  Exit code: {result.metadata.get('exit_code', 'N/A')}\n")

    print("✅ Self-test complete!")
