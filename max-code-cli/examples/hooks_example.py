"""
Example: Hooks System - Lifecycle Event Management

Demonstrates Anthropic SDK-style lifecycle hooks following FASE 2.2 implementation.

Based on Claude Code hooks (2025):
- 8 lifecycle events
- Blocking support (PreToolUse)
- Shell command execution
- Environment variable injection

Run: python examples/hooks_example.py
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '.')

from core.hooks import (
    HookEvent,
    HookPayload,
    HookResult,
    HookDefinition,
    HookConfig,
    SessionSource,
    HookManager,
    get_hook_manager,
    HookExecutor,
)


# ============================================================================
# EXAMPLE 1: Load hooks from settings.json (Anthropic format)
# ============================================================================

async def example_load_config():
    """Load hook configuration from settings.json"""
    print("=" * 70)
    print("EXAMPLE 1: Load Hooks from settings.json")
    print("=" * 70)

    manager = get_hook_manager()
    config_path = Path("examples/hooks_settings.json")

    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return

    manager.load_config(config_path)

    print(f"✅ Loaded {manager.get_hook_count()} hooks from {config_path}")
    print()

    # List all hooks
    for event in HookEvent:
        hooks = manager.list_hooks(event)
        if hooks:
            print(f"📌 {event}: {len(hooks)} hook(s)")
            for hook in hooks:
                print(f"   - Matcher: {hook.matcher}")
                print(f"     Command: {hook.command[:60]}...")
    print()


# ============================================================================
# EXAMPLE 2: Programmatic hook registration (without settings.json)
# ============================================================================

async def example_programmatic_registration():
    """Register hooks programmatically"""
    print("=" * 70)
    print("EXAMPLE 2: Programmatic Hook Registration")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()  # Clear existing hooks

    # Register PreToolUse hook
    hook1 = manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="Bash",
        command="echo 'PreToolUse: Bash command detected'",
    )
    print(f"✅ Registered: {hook1.event} / {hook1.matcher}")

    # Register PostToolUse hook (all tools)
    hook2 = manager.register_hook(
        event=HookEvent.POST_TOOL_USE,
        matcher="*",
        command="echo 'PostToolUse: Tool execution completed'",
    )
    print(f"✅ Registered: {hook2.event} / {hook2.matcher}")

    # Register SessionStart hook
    hook3 = manager.register_hook(
        event=HookEvent.SESSION_START,
        matcher="*",
        command="echo 'SessionStart: Session initialized'",
    )
    print(f"✅ Registered: {hook3.event} / {hook3.matcher}")

    print(f"\n📋 Total hooks registered: {manager.get_hook_count()}")
    print()


# ============================================================================
# EXAMPLE 3: PreToolUse - Blocking behavior
# ============================================================================

async def example_pretool_blocking():
    """Demonstrate PreToolUse blocking"""
    print("=" * 70)
    print("EXAMPLE 3: PreToolUse Blocking")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()

    # Register blocking hook (exit code != 0)
    manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="Bash",
        command="echo 'BLOCKED: Bash commands are not allowed' >&2 && exit 1",
    )

    # Create payload
    payload = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Bash",
        tool_input={"command": "rm -rf /"},
    )

    # Trigger hook
    result = await manager.trigger(HookEvent.PRE_TOOL_USE, payload, tool_name="Bash")

    print(f"🔒 Execution allowed: {result.allow_execution}")
    print(f"💬 Feedback: {result.feedback}")

    if not result.allow_execution:
        print("✅ Hook successfully blocked dangerous command!")

    print()


# ============================================================================
# EXAMPLE 4: PreToolUse - Allowing execution
# ============================================================================

async def example_pretool_allow():
    """Demonstrate PreToolUse allowing execution"""
    print("=" * 70)
    print("EXAMPLE 4: PreToolUse Allow Execution")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()

    # Register allowing hook (exit code 0)
    manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="Edit",
        command="echo 'PreToolUse: Edit command validated' && exit 0",
    )

    # Create payload
    payload = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Edit",
        tool_input={"file_path": "/tmp/test.txt", "content": "Hello"},
    )

    # Trigger hook
    result = await manager.trigger(HookEvent.PRE_TOOL_USE, payload, tool_name="Edit")

    print(f"✅ Execution allowed: {result.allow_execution}")
    print(f"💬 Feedback: {result.feedback}")
    print()


# ============================================================================
# EXAMPLE 5: PostToolUse - Non-blocking execution
# ============================================================================

async def example_posttool():
    """Demonstrate PostToolUse (non-blocking)"""
    print("=" * 70)
    print("EXAMPLE 5: PostToolUse (Non-Blocking)")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()

    # Register PostToolUse hook
    manager.register_hook(
        event=HookEvent.POST_TOOL_USE,
        matcher="*",
        command="echo 'PostToolUse: Tool execution logged'",
    )

    # Create payload
    payload = HookPayload(
        event=HookEvent.POST_TOOL_USE,
        tool_name="Read",
        tool_input={"file_path": "/tmp/test.txt"},
        tool_response={"content": "File contents..."},
    )

    # Trigger hook
    result = await manager.trigger(HookEvent.POST_TOOL_USE, payload, tool_name="Read")

    print(f"✅ Hook executed: {result.success}")
    print(f"💬 Feedback: {result.feedback}")
    print()


# ============================================================================
# EXAMPLE 6: Environment variable injection
# ============================================================================

async def example_env_injection():
    """Demonstrate environment variable injection"""
    print("=" * 70)
    print("EXAMPLE 6: Environment Variable Injection")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()

    # Register hook that uses env vars
    manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="*",
        command="echo \"Event: $HOOK_EVENT | Tool: $TOOL_NAME | Time: $HOOK_TIMESTAMP\"",
    )

    # Create payload with tool input
    payload = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Grep",
        tool_input={
            "pattern": "TODO",
            "path": "/home/user/project",
        },
    )

    # Trigger hook
    result = await manager.trigger(HookEvent.PRE_TOOL_USE, payload, tool_name="Grep")

    print(f"💬 Feedback (env vars injected):")
    print(f"   {result.feedback}")
    print()


# ============================================================================
# EXAMPLE 7: All 8 lifecycle events
# ============================================================================

async def example_all_events():
    """Demonstrate all 8 lifecycle events"""
    print("=" * 70)
    print("EXAMPLE 7: All 8 Lifecycle Events")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()

    # Register hook for each event
    events = [
        HookEvent.PRE_TOOL_USE,
        HookEvent.POST_TOOL_USE,
        HookEvent.USER_PROMPT_SUBMIT,
        HookEvent.NOTIFICATION,
        HookEvent.STOP,
        HookEvent.SUBAGENT_STOP,
        HookEvent.PRE_COMPACT,
        HookEvent.SESSION_START,
        HookEvent.SESSION_END,
    ]

    for event in events:
        manager.register_hook(
            event=event,
            matcher="*",
            command=f"echo '[{event}] Event triggered'",
        )

    print(f"✅ Registered hooks for all {len(events)} events\n")

    # Trigger each event
    print("📌 Triggering events:\n")

    # 1. SessionStart
    payload1 = HookPayload(
        event=HookEvent.SESSION_START,
        source=SessionSource.STARTUP,
        session_info={"user": "claude", "mode": "cli"},
    )
    result = await manager.trigger(HookEvent.SESSION_START, payload1)
    print(f"   {HookEvent.SESSION_START}: {result.feedback}")

    # 2. UserPromptSubmit
    payload2 = HookPayload(
        event=HookEvent.USER_PROMPT_SUBMIT,
        user_prompt="Help me refactor this code",
    )
    result = await manager.trigger(HookEvent.USER_PROMPT_SUBMIT, payload2)
    print(f"   {HookEvent.USER_PROMPT_SUBMIT}: {result.feedback}")

    # 3. PreToolUse
    payload3 = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Read",
        tool_input={"file_path": "/tmp/test.py"},
    )
    result = await manager.trigger(HookEvent.PRE_TOOL_USE, payload3, tool_name="Read")
    print(f"   {HookEvent.PRE_TOOL_USE}: {result.feedback}")

    # 4. PostToolUse
    payload4 = HookPayload(
        event=HookEvent.POST_TOOL_USE,
        tool_name="Read",
        tool_response={"content": "def hello(): pass"},
    )
    result = await manager.trigger(HookEvent.POST_TOOL_USE, payload4, tool_name="Read")
    print(f"   {HookEvent.POST_TOOL_USE}: {result.feedback}")

    # 5. Notification
    payload5 = HookPayload(
        event=HookEvent.NOTIFICATION,
        notification_message="Analysis complete",
    )
    result = await manager.trigger(HookEvent.NOTIFICATION, payload5)
    print(f"   {HookEvent.NOTIFICATION}: {result.feedback}")

    # 6. PreCompact
    payload6 = HookPayload(
        event=HookEvent.PRE_COMPACT,
        context_usage=0.78,
        context_limit=200000,
    )
    result = await manager.trigger(HookEvent.PRE_COMPACT, payload6)
    print(f"   {HookEvent.PRE_COMPACT}: {result.feedback}")

    # 7. Stop
    payload7 = HookPayload(event=HookEvent.STOP)
    result = await manager.trigger(HookEvent.STOP, payload7)
    print(f"   {HookEvent.STOP}: {result.feedback}")

    # 8. SessionEnd
    payload8 = HookPayload(event=HookEvent.SESSION_END)
    result = await manager.trigger(HookEvent.SESSION_END, payload8)
    print(f"   {HookEvent.SESSION_END}: {result.feedback}")

    print()


# ============================================================================
# EXAMPLE 8: Multiple hooks aggregation
# ============================================================================

async def example_multiple_hooks():
    """Demonstrate multiple hooks for same event"""
    print("=" * 70)
    print("EXAMPLE 8: Multiple Hooks Aggregation")
    print("=" * 70)

    manager = get_hook_manager()
    manager.clear()

    # Register 3 hooks for PreToolUse
    manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="Bash",
        command="echo 'Hook 1: Validation passed' && exit 0",
    )

    manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="Bash",
        command="echo 'Hook 2: Security check passed' && exit 0",
    )

    manager.register_hook(
        event=HookEvent.PRE_TOOL_USE,
        matcher="Bash",
        command="echo 'Hook 3: Logging command' && exit 0",
    )

    print(f"✅ Registered 3 hooks for PreToolUse/Bash\n")

    # Create payload
    payload = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Bash",
        tool_input={"command": "ls -la"},
    )

    # Trigger all hooks
    result = await manager.trigger(HookEvent.PRE_TOOL_USE, payload, tool_name="Bash")

    print(f"✅ All hooks executed")
    print(f"🔓 Execution allowed: {result.allow_execution}")
    print(f"💬 Aggregated feedback:")
    if result.feedback:
        for line in result.feedback.split('\n'):
            print(f"   - {line}")
    print()


# ============================================================================
# EXAMPLE 9: Hook executor direct usage
# ============================================================================

async def example_executor_direct():
    """Demonstrate direct HookExecutor usage"""
    print("=" * 70)
    print("EXAMPLE 9: Direct HookExecutor Usage")
    print("=" * 70)

    executor = HookExecutor(timeout=10)

    # Test 1: Successful command
    print("Test 1: Successful command (exit 0)")
    payload1 = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Test",
    )
    result1 = executor.execute("echo 'Success!' && exit 0", payload1)
    print(f"  ✅ Success: {result1.success}")
    print(f"  🔓 Allow: {result1.allow_execution}")
    print(f"  💬 Output: {result1.feedback}")
    print()

    # Test 2: Failing command (exit 1)
    print("Test 2: Failing command (exit 1)")
    payload2 = HookPayload(
        event=HookEvent.PRE_TOOL_USE,
        tool_name="Test",
    )
    result2 = executor.execute("echo 'Blocked!' >&2 && exit 1", payload2)
    print(f"  ✅ Success: {result2.success}")
    print(f"  🔒 Allow: {result2.allow_execution}")
    print(f"  💬 Output: {result2.feedback}")
    print()


# ============================================================================
# MAIN: Run all examples
# ============================================================================

async def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "HOOKS SYSTEM EXAMPLES - FASE 2.2" + " " * 21 + "║")
    print("║" + " " * 12 + "Anthropic SDK-style Lifecycle Hooks" + " " * 21 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    # Run examples
    await example_load_config()
    await example_programmatic_registration()
    await example_pretool_blocking()
    await example_pretool_allow()
    await example_posttool()
    await example_env_injection()
    await example_all_events()
    await example_multiple_hooks()
    await example_executor_direct()

    print("=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)
    print()

    # Summary
    manager = get_hook_manager()
    print("📊 SUMMARY:")
    print(f"   - Total hooks registered: {manager.get_hook_count()}")
    print(f"   - Hook system enabled: {manager.is_enabled()}")
    print(f"   - Supported events: {len(HookEvent)} lifecycle events")
    print()


if __name__ == "__main__":
    asyncio.run(main())
