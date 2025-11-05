"""
Hooks Framework - Anthropic SDK-style lifecycle hooks

Based on Claude Code hooks (2025):
- 8 lifecycle events
- Blocking support (PreToolUse)
- Shell command execution
- Environment variable injection

Biblical Foundation:
"Há tempo de nascer e tempo de morrer" (Eclesiastes 3:2)
Lifecycle management with deterministic control.

Features:
- PreToolUse (can block)
- PostToolUse
- UserPromptSubmit
- Notification
- Stop / SubagentStop
- PreCompact
- SessionStart / SessionEnd

Example:
    >>> from core.hooks import get_hook_manager, HookEvent, HookPayload
    >>>
    >>> manager = get_hook_manager()
    >>> manager.register_hook(
    ...     event=HookEvent.PRE_TOOL_USE,
    ...     matcher="Bash",
    ...     command="echo 'Running bash command' >> ~/log.txt"
    ... )
    >>>
    >>> payload = HookPayload(
    ...     event=HookEvent.PRE_TOOL_USE,
    ...     tool_name="Bash",
    ...     tool_input={"command": "ls -la"}
    ... )
    >>>
    >>> result = await manager.trigger(HookEvent.PRE_TOOL_USE, payload, tool_name="Bash")
    >>> if not result.allow_execution:
    ...     print(f"Blocked: {result.feedback}")
"""

from .types import (
    HookEvent,
    HookPayload,
    HookResult,
    HookDefinition,
    HookConfig,
    SessionSource,
)

from .executor import (
    HookExecutor,
    HookExecutionError,
)

from .manager import (
    HookManager,
    get_hook_manager,
    HookManagerError,
    HookConfigNotFoundError,
)

__all__ = [
    # Types
    'HookEvent',
    'HookPayload',
    'HookResult',
    'HookDefinition',
    'HookConfig',
    'SessionSource',

    # Executor
    'HookExecutor',
    'HookExecutionError',

    # Manager
    'HookManager',
    'get_hook_manager',
    'HookManagerError',
    'HookConfigNotFoundError',
]

__version__ = '2.0.0'  # FASE 2.2: Hooks System
