"""
Streaming Types - AsyncIterator patterns for streaming responses

Type definitions for streaming system following Anthropic SDK patterns.

Biblical Foundation:
"Aquele que crê em mim, como diz a Escritura, rios de água viva correrão do seu ventre" (João 7:38)
Living streams - continuous flow of responses.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, AsyncIterator, Literal
from datetime import datetime
from enum import Enum


class StreamEventType(str, Enum):
    """
    Streaming event types.

    Based on Anthropic SDK streaming events (2025).
    """
    # Message lifecycle
    MESSAGE_START = "message_start"
    MESSAGE_DELTA = "message_delta"
    MESSAGE_STOP = "message_stop"

    # Content streaming
    CONTENT_BLOCK_START = "content_block_start"
    CONTENT_BLOCK_DELTA = "content_block_delta"
    CONTENT_BLOCK_STOP = "content_block_stop"

    # Tool use
    TOOL_USE_START = "tool_use_start"
    TOOL_USE_DELTA = "tool_use_delta"
    TOOL_USE_STOP = "tool_use_stop"

    # Token usage
    TOKEN_COUNT = "token_count"

    # Errors
    ERROR = "error"

    # Progress
    PROGRESS = "progress"


@dataclass
class StreamChunk:
    """
    Single chunk from streaming response.

    Compatible with Anthropic Messages API streaming format.
    """
    event_type: StreamEventType
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    # Content extraction helpers
    @property
    def text(self) -> Optional[str]:
        """Extract text content from chunk"""
        if self.event_type == StreamEventType.CONTENT_BLOCK_DELTA:
            return self.data.get("delta", {}).get("text")
        elif self.event_type == StreamEventType.MESSAGE_DELTA:
            return self.data.get("delta", {}).get("content")
        return None

    @property
    def is_final(self) -> bool:
        """Check if this is a final chunk"""
        return self.event_type in (
            StreamEventType.MESSAGE_STOP,
            StreamEventType.CONTENT_BLOCK_STOP,
            StreamEventType.TOOL_USE_STOP,
        )

    @property
    def is_error(self) -> bool:
        """Check if this is an error chunk"""
        return self.event_type == StreamEventType.ERROR

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class StreamMessage:
    """
    Accumulated message from stream.

    Builds complete message from chunks.
    """
    role: str = "assistant"
    content: str = ""

    # Metadata
    model: Optional[str] = None
    stop_reason: Optional[str] = None
    stop_sequence: Optional[str] = None

    # Token usage
    input_tokens: int = 0
    output_tokens: int = 0

    # Tool use
    tool_uses: list = field(default_factory=list)

    # Timing
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    @property
    def is_complete(self) -> bool:
        """Check if message is complete"""
        return self.end_time is not None

    @property
    def duration(self) -> float:
        """Get message duration in seconds"""
        if self.end_time is None:
            return (datetime.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()

    def append_text(self, text: str):
        """Append text to content"""
        self.content += text

    def finalize(self, stop_reason: Optional[str] = None):
        """Mark message as complete"""
        self.end_time = datetime.now()
        if stop_reason:
            self.stop_reason = stop_reason

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "role": self.role,
            "content": self.content,
            "model": self.model,
            "stop_reason": self.stop_reason,
            "stop_sequence": self.stop_sequence,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "tool_uses": self.tool_uses,
            "duration": self.duration,
            "is_complete": self.is_complete,
        }


@dataclass
class StreamConfig:
    """
    Configuration for streaming.

    Controls streaming behavior and UI updates.
    """
    # Model settings
    model: str = "claude-3-5-haiku-20241022"
    max_tokens: int = 4096
    temperature: float = 1.0

    # Streaming settings
    stream_timeout: float = 60.0  # seconds
    chunk_size: int = 1024  # bytes

    # UI settings
    show_progress: bool = True
    show_tokens: bool = True
    update_interval: float = 0.1  # seconds

    # Buffer settings
    buffer_chunks: bool = False
    buffer_size: int = 10

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream_timeout": self.stream_timeout,
            "chunk_size": self.chunk_size,
            "show_progress": self.show_progress,
            "show_tokens": self.show_tokens,
            "update_interval": self.update_interval,
            "buffer_chunks": self.buffer_chunks,
            "buffer_size": self.buffer_size,
        }


@dataclass
class StreamProgress:
    """
    Progress tracking for streaming operations.

    Tracks tokens, timing, and completion status.
    """
    # Counts
    chunks_received: int = 0
    tokens_generated: int = 0
    chars_generated: int = 0

    # Timing
    start_time: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)

    # Status
    is_complete: bool = False
    error: Optional[str] = None

    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        return (datetime.now() - self.start_time).total_seconds()

    @property
    def tokens_per_second(self) -> float:
        """Calculate tokens per second"""
        elapsed = self.elapsed_time
        return self.tokens_generated / elapsed if elapsed > 0 else 0.0

    @property
    def chars_per_second(self) -> float:
        """Calculate characters per second"""
        elapsed = self.elapsed_time
        return self.chars_generated / elapsed if elapsed > 0 else 0.0

    def update_chunk(self, chunk: StreamChunk):
        """Update progress from chunk"""
        self.chunks_received += 1
        self.last_update = datetime.now()

        # Update text counts
        if chunk.text:
            self.chars_generated += len(chunk.text)
            # Rough token estimate: ~4 chars per token
            self.tokens_generated = self.chars_generated // 4

        # Update token counts from metadata
        if "usage" in chunk.data:
            usage = chunk.data["usage"]
            self.tokens_generated = usage.get("output_tokens", self.tokens_generated)

        # Check completion
        if chunk.is_final:
            self.is_complete = True

        # Check error
        if chunk.is_error:
            self.error = chunk.data.get("message", "Unknown error")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "chunks_received": self.chunks_received,
            "tokens_generated": self.tokens_generated,
            "chars_generated": self.chars_generated,
            "elapsed_time": self.elapsed_time,
            "tokens_per_second": self.tokens_per_second,
            "chars_per_second": self.chars_per_second,
            "is_complete": self.is_complete,
            "error": self.error,
        }


@dataclass
class StreamResult:
    """
    Complete result from streaming operation.

    Contains final message and statistics.
    """
    message: StreamMessage
    progress: StreamProgress

    # Statistics
    total_chunks: int = 0
    total_time: float = 0.0

    @property
    def success(self) -> bool:
        """Check if stream completed successfully"""
        return self.progress.is_complete and self.progress.error is None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "message": self.message.to_dict(),
            "progress": self.progress.to_dict(),
            "total_chunks": self.total_chunks,
            "total_time": self.total_time,
            "success": self.success,
        }
