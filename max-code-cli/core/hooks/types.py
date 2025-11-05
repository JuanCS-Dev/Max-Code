"""
Hook Types - Type definitions for lifecycle hooks system

Based on Anthropic Claude Code hooks (2025):
- 8 lifecycle events (PreToolUse, PostToolUse, SessionStart, etc.)
- Blocking support (PreToolUse can block execution)
- Payload structure for each event

Biblical Foundation:
"Há tempo de nascer e tempo de morrer" (Eclesiastes 3:2)
Lifecycle management - deterministic execution.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime


class HookEvent(str, Enum):
    """
    Lifecycle hook events.

    Based on Anthropic Claude Code hooks (8 events).
    """
    # Pre/Post tool execution
    PRE_TOOL_USE = "PreToolUse"              # Before tool calls (CAN BLOCK)
    POST_TOOL_USE = "PostToolUse"            # After tool calls

    # User interaction
    USER_PROMPT_SUBMIT = "UserPromptSubmit"  # When user submits prompt

    # Agent lifecycle
    NOTIFICATION = "Notification"            # When Claude sends notifications
    STOP = "Stop"                            # When Claude finishes responding
    SUBAGENT_STOP = "SubagentStop"          # When subagent Task finishes

    # Context management
    PRE_COMPACT = "PreCompact"              # Before context compaction

    # Session lifecycle
    SESSION_START = "SessionStart"          # Session start or resume
    SESSION_END = "SessionEnd"              # Session termination


class SessionSource(str, Enum):
    """Session start sources"""
    STARTUP = "startup"
    RESUME = "resume"
    CLEAR = "clear"


@dataclass
class HookPayload:
    """
    Payload passed to hook handlers.

    Different events have different payload structures.
    """
    event: HookEvent
    timestamp: datetime = field(default_factory=datetime.now)

    # Tool-related (PreToolUse, PostToolUse)
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_response: Optional[Dict[str, Any]] = None

    # Session-related (SessionStart)
    source: Optional[SessionSource] = None
    session_info: Optional[Dict[str, Any]] = None

    # User interaction (UserPromptSubmit)
    user_prompt: Optional[str] = None

    # Notification
    notification_message: Optional[str] = None

    # Context compaction (PreCompact)
    context_usage: Optional[float] = None
    context_limit: Optional[int] = None

    # Generic metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            "event": self.event,
            "timestamp": self.timestamp.isoformat(),
        }

        # Add non-None fields
        if self.tool_name:
            result["tool_name"] = self.tool_name
        if self.tool_input:
            result["tool_input"] = self.tool_input
        if self.tool_response:
            result["tool_response"] = self.tool_response
        if self.source:
            result["source"] = self.source
        if self.session_info:
            result["session_info"] = self.session_info
        if self.user_prompt:
            result["user_prompt"] = self.user_prompt
        if self.notification_message:
            result["notification_message"] = self.notification_message
        if self.context_usage is not None:
            result["context_usage"] = self.context_usage
        if self.context_limit is not None:
            result["context_limit"] = self.context_limit
        if self.metadata:
            result["metadata"] = self.metadata

        return result


@dataclass
class HookResult:
    """
    Result from hook execution.

    For blocking hooks (PreToolUse), allow_execution determines if tool runs.
    """
    success: bool
    allow_execution: bool = True  # Only used for PreToolUse
    feedback: Optional[str] = None  # Feedback to LLM if blocked
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def allow(cls, feedback: Optional[str] = None) -> "HookResult":
        """Create result that allows execution"""
        return cls(success=True, allow_execution=True, feedback=feedback)

    @classmethod
    def block(cls, feedback: str) -> "HookResult":
        """Create result that blocks execution"""
        return cls(success=True, allow_execution=False, feedback=feedback)

    @classmethod
    def error(cls, error_message: str) -> "HookResult":
        """Create error result (allows execution by default)"""
        return cls(success=False, allow_execution=True, feedback=error_message)


@dataclass
class HookDefinition:
    """
    Hook definition from configuration.

    Matches Anthropic settings.json format:
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Running bash' >> log.txt"
        }
      ]
    }
    """
    event: HookEvent
    matcher: str  # Tool name pattern ("Bash", "Edit|Write", "*")
    command: str  # Shell command to execute
    type: str = "command"  # Always "command" for now
    enabled: bool = True

    def matches_tool(self, tool_name: str) -> bool:
        """
        Check if hook matches tool name.

        Supports:
        - Exact match: "Bash"
        - Multiple tools: "Edit|Write"
        - All tools: "*"
        """
        if self.matcher == "*":
            return True

        if "|" in self.matcher:
            # Multiple tools: "Edit|Write"
            patterns = [p.strip() for p in self.matcher.split("|")]
            return tool_name in patterns

        # Exact match
        return self.matcher == tool_name


@dataclass
class HookConfig:
    """
    Complete hook configuration.

    Loaded from ~/.max-code/settings.json or project .max-code/settings.json
    """
    hooks: Dict[HookEvent, List[HookDefinition]] = field(default_factory=dict)

    def add_hook(self, hook: HookDefinition):
        """Add hook to configuration"""
        if hook.event not in self.hooks:
            self.hooks[hook.event] = []
        self.hooks[hook.event].append(hook)

    def get_hooks(self, event: HookEvent) -> List[HookDefinition]:
        """Get all hooks for an event"""
        return self.hooks.get(event, [])

    def get_matching_hooks(self, event: HookEvent, tool_name: Optional[str] = None) -> List[HookDefinition]:
        """
        Get hooks matching event and tool name.

        Args:
            event: Hook event
            tool_name: Tool name (only for PreToolUse/PostToolUse)

        Returns:
            List of matching enabled hooks
        """
        event_hooks = self.get_hooks(event)

        if tool_name is None:
            # Non-tool events: return all enabled hooks
            return [h for h in event_hooks if h.enabled]

        # Tool events: filter by matcher
        return [h for h in event_hooks if h.enabled and h.matches_tool(tool_name)]

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "HookConfig":
        """
        Load configuration from dictionary.

        Expected format (Anthropic settings.json):
        {
          "hooks": {
            "PreToolUse": [
              {
                "matcher": "Bash",
                "hooks": [
                  {
                    "type": "command",
                    "command": "echo 'Running bash' >> log.txt"
                  }
                ]
              }
            ]
          }
        }
        """
        config = cls()

        hooks_dict = config_dict.get("hooks", {})

        for event_name, event_configs in hooks_dict.items():
            try:
                event = HookEvent(event_name)
            except ValueError:
                continue  # Skip unknown events

            for event_config in event_configs:
                matcher = event_config.get("matcher", "*")

                for hook_def in event_config.get("hooks", []):
                    hook = HookDefinition(
                        event=event,
                        matcher=matcher,
                        command=hook_def.get("command", ""),
                        type=hook_def.get("type", "command"),
                        enabled=hook_def.get("enabled", True),
                    )
                    config.add_hook(hook)

        return config
