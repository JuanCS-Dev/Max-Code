"""
Context Types - Message and context management types

Type definitions for context compaction system following Anthropic SDK patterns.

Biblical Foundation:
"Porque qual de vós, querendo edificar uma torre, não se assenta primeiro a fazer
as contas dos gastos?" (Lucas 14:28)
Count the cost - manage resources wisely.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message roles in conversation"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class CompactionStrategy(str, Enum):
    """
    Compaction strategies for context management.

    Based on Anthropic Claude Code patterns (2025).
    """
    # LLM-based summarization (best quality, uses tokens)
    LLM_SUMMARY = "llm_summary"

    # Simple truncation (fast, no token cost)
    TRUNCATE = "truncate"

    # Keep important messages only (system, recent, tool results)
    SELECTIVE = "selective"

    # Rolling window (keep last N messages)
    ROLLING_WINDOW = "rolling_window"

    # No compaction
    NONE = "none"


@dataclass
class Message:
    """
    Conversation message.

    Compatible with Anthropic Messages API format.
    """
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    # Optional metadata
    name: Optional[str] = None  # Tool name for tool messages
    tool_use_id: Optional[str] = None  # Tool call ID
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Token estimation (for context tracking)
    estimated_tokens: Optional[int] = None

    def estimate_tokens(self) -> int:
        """
        Estimate token count for this message.

        Rough heuristic: ~4 characters per token (English).
        More accurate: use tiktoken or Anthropic's API.
        """
        if self.estimated_tokens is not None:
            return self.estimated_tokens

        # Simple heuristic
        char_count = len(self.content)
        if self.name:
            char_count += len(self.name)

        # ~4 chars per token + overhead
        estimated = (char_count // 4) + 10
        self.estimated_tokens = estimated
        return estimated

    def to_dict(self) -> Dict[str, Any]:
        """Convert to Anthropic API format"""
        result = {
            "role": self.role,
            "content": self.content,
        }

        if self.name:
            result["name"] = self.name
        if self.tool_use_id:
            result["tool_use_id"] = self.tool_use_id

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create from Anthropic API format"""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            name=data.get("name"),
            tool_use_id=data.get("tool_use_id"),
        )


@dataclass
class ConversationContext:
    """
    Full conversation context with token tracking.

    Manages messages and monitors token usage.
    """
    messages: List[Message] = field(default_factory=list)
    max_tokens: int = 200000  # Default: Claude Sonnet 4.5 limit
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: Message):
        """Add message to context"""
        self.messages.append(message)

    def get_token_count(self) -> int:
        """Get total token count"""
        return sum(msg.estimate_tokens() for msg in self.messages)

    def get_usage_ratio(self) -> float:
        """Get usage as ratio (0.0 to 1.0)"""
        return self.get_token_count() / self.max_tokens

    def get_usage_percent(self) -> float:
        """Get usage as percentage (0.0 to 100.0)"""
        return self.get_usage_ratio() * 100

    def get_last_n_messages(self, n: int) -> List[Message]:
        """Get last N messages"""
        return self.messages[-n:] if n > 0 else []

    def get_system_messages(self) -> List[Message]:
        """Get all system messages"""
        return [msg for msg in self.messages if msg.role == MessageRole.SYSTEM]

    def to_api_format(self) -> List[Dict[str, Any]]:
        """Convert to Anthropic API format"""
        return [msg.to_dict() for msg in self.messages]


@dataclass
class CompactionResult:
    """
    Result from context compaction.

    Contains compacted context and metadata about the operation.
    """
    compacted_context: ConversationContext
    strategy_used: CompactionStrategy

    # Statistics
    original_token_count: int
    compacted_token_count: int
    messages_removed: int
    messages_summarized: int

    # Timing
    compaction_time: float  # seconds
    timestamp: datetime = field(default_factory=datetime.now)

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def compression_ratio(self) -> float:
        """Get compression ratio (compacted / original)"""
        if self.original_token_count == 0:
            return 0.0
        return self.compacted_token_count / self.original_token_count

    @property
    def tokens_saved(self) -> int:
        """Get number of tokens saved"""
        return self.original_token_count - self.compacted_token_count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "strategy": self.strategy_used,
            "original_tokens": self.original_token_count,
            "compacted_tokens": self.compacted_token_count,
            "messages_removed": self.messages_removed,
            "messages_summarized": self.messages_summarized,
            "compression_ratio": self.compression_ratio,
            "tokens_saved": self.tokens_saved,
            "compaction_time": self.compaction_time,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class CompactionConfig:
    """
    Configuration for context compaction.

    Based on Anthropic Claude Code defaults (2025).
    """
    # Trigger threshold (0.0 to 1.0)
    compact_threshold: float = 0.75  # Compact at 75%

    # Target ratio after compaction (0.0 to 1.0)
    target_ratio: float = 0.50  # Compress to 50%

    # Strategy to use
    strategy: CompactionStrategy = CompactionStrategy.LLM_SUMMARY

    # Preservation settings
    preserve_system_messages: bool = True  # Always keep system prompts
    preserve_recent_count: int = 10  # Keep last N messages untouched

    # Auto-compaction
    auto_compact: bool = True  # Auto-trigger when threshold reached

    # Hook integration
    trigger_precompact_hook: bool = True  # Trigger PreCompact hook

    # Manual confirmation
    require_confirmation: bool = False  # Ask user before compaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "compact_threshold": self.compact_threshold,
            "target_ratio": self.target_ratio,
            "strategy": self.strategy,
            "preserve_system_messages": self.preserve_system_messages,
            "preserve_recent_count": self.preserve_recent_count,
            "auto_compact": self.auto_compact,
            "trigger_precompact_hook": self.trigger_precompact_hook,
            "require_confirmation": self.require_confirmation,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompactionConfig":
        """Create from dictionary"""
        return cls(
            compact_threshold=data.get("compact_threshold", 0.75),
            target_ratio=data.get("target_ratio", 0.50),
            strategy=CompactionStrategy(data.get("strategy", "llm_summary")),
            preserve_system_messages=data.get("preserve_system_messages", True),
            preserve_recent_count=data.get("preserve_recent_count", 10),
            auto_compact=data.get("auto_compact", True),
            trigger_precompact_hook=data.get("trigger_precompact_hook", True),
            require_confirmation=data.get("require_confirmation", False),
        )
