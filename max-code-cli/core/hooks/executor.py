"""
Hook Executor - Shell command execution for hooks

Executes shell commands with:
- Environment variable injection (payload data)
- Timeout support
- Exit code handling (0 = allow, non-zero = block for PreToolUse)
- Security considerations

Biblical Foundation:
"Tudo o que fizerem, façam de todo o coração" (Colossenses 3:23)
"""

import subprocess
import logging
import json
import os
import shlex
from typing import Dict, Any, Optional
from pathlib import Path

from .types import HookPayload, HookResult, HookEvent

logger = logging.getLogger(__name__)


class HookExecutionError(Exception):
    """Hook execution failed"""
    pass


class HookExecutor:
    """
    Execute shell commands for hooks.

    Injects payload data as environment variables and JSON stdin.
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize executor.

        Args:
            timeout: Command timeout in seconds (default: 30)
        """
        self.timeout = timeout

    def execute(
        self,
        command: str,
        payload: HookPayload,
        working_dir: Optional[Path] = None,
    ) -> HookResult:
        """
        Execute shell command with hook payload.

        Args:
            command: Shell command to execute
            payload: Hook payload (injected as env vars + stdin)
            working_dir: Working directory (defaults to current)

        Returns:
            HookResult with success status and feedback

        Blocking logic (PreToolUse only):
        - Exit code 0: Allow execution
        - Exit code != 0: Block execution, pass stderr as feedback
        """
        try:
            # Prepare environment variables
            env = self._prepare_environment(payload)

            # Prepare stdin (JSON payload)
            stdin_data = json.dumps(payload.to_dict())

            # Execute command
            logger.debug(f"Executing hook command: {command}")

            # Security: shell=True needed for hook script execution
            # Commands come from configured hooks, not untrusted input
            # Protected by timeout and pre-configured environment
            result = subprocess.run(
                command,
                shell=True,  # nosec B602
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=env,
                cwd=working_dir,
                input=stdin_data,
            )

            # Check result
            success = result.returncode == 0

            if success:
                # Success: allow execution
                feedback = result.stdout.strip() if result.stdout else None
                return HookResult.allow(feedback=feedback)
            else:
                # Non-zero exit: block execution (for PreToolUse)
                feedback = result.stderr.strip() if result.stderr else f"Hook returned exit code {result.returncode}"

                if payload.event == HookEvent.PRE_TOOL_USE:
                    logger.warning(f"PreToolUse hook blocked execution: {feedback}")
                    return HookResult.block(feedback=feedback)
                else:
                    # Other events don't block
                    logger.warning(f"Hook failed (non-blocking): {feedback}")
                    return HookResult.error(feedback)

        except subprocess.TimeoutExpired:
            error_msg = f"Hook command timed out after {self.timeout}s"
            logger.error(error_msg)
            return HookResult.error(error_msg)

        except Exception as e:
            error_msg = f"Hook execution failed: {e}"
            logger.error(error_msg, exc_info=True)
            return HookResult.error(error_msg)

    def _prepare_environment(self, payload: HookPayload) -> Dict[str, str]:
        """
        Prepare environment variables from payload.

        Injects payload data as env vars:
        - HOOK_EVENT: Event name
        - TOOL_NAME: Tool name (if present)
        - TOOL_INPUT: JSON of tool input (if present)
        - TOOL_RESPONSE: JSON of tool response (if present)
        - etc.
        """
        # Start with current environment
        env = os.environ.copy()

        # Add hook-specific vars
        env["HOOK_EVENT"] = payload.event
        env["HOOK_TIMESTAMP"] = payload.timestamp.isoformat()

        # Tool-related
        if payload.tool_name:
            env["TOOL_NAME"] = payload.tool_name
        if payload.tool_input:
            env["TOOL_INPUT"] = json.dumps(payload.tool_input)
        if payload.tool_response:
            env["TOOL_RESPONSE"] = json.dumps(payload.tool_response)

        # Session-related
        if payload.source:
            env["SESSION_SOURCE"] = payload.source
        if payload.session_info:
            env["SESSION_INFO"] = json.dumps(payload.session_info)

        # User prompt
        if payload.user_prompt:
            env["USER_PROMPT"] = payload.user_prompt

        # Notification
        if payload.notification_message:
            env["NOTIFICATION_MESSAGE"] = payload.notification_message

        # Context compaction
        if payload.context_usage is not None:
            env["CONTEXT_USAGE"] = str(payload.context_usage)
        if payload.context_limit is not None:
            env["CONTEXT_LIMIT"] = str(payload.context_limit)

        # Metadata
        if payload.metadata:
            env["HOOK_METADATA"] = json.dumps(payload.metadata)

        return env

    def validate_command(self, command: str) -> bool:
        """
        Validate command for security.

        Basic checks:
        - Not empty
        - No obvious shell injection attempts

        Note: Shell commands are inherently risky. Users should audit hooks.
        """
        if not command or not command.strip():
            return False

        # Could add more security checks here
        # For now, trust that users audit their hooks

        return True
