"""
Streaming System - AsyncIterator-based streaming responses

Anthropic SDK-style streaming support with:
- AsyncIterator streaming patterns
- Bidirectional communication
- Real-time progress tracking
- Token-by-token delivery
- Comprehensive statistics

Biblical Foundation:
"Aquele que crê em mim, como diz a Escritura, rios de água viva correrão do seu ventre" (João 7:38)
Living streams - continuous flow of responses.

Features:
- ✅ AsyncIterator streaming (Anthropic SDK pattern)
- ✅ StreamingAgent for async execution
- ✅ Bidirectional streaming client
- ✅ Progress tracking and statistics
- ✅ Chunk-by-chunk delivery
- ✅ StreamCollector utility
- ✅ Conversation management

Example:
    >>> from core.streaming import StreamingAgent, StreamConfig
    >>>
    >>> # Create streaming agent
    >>> agent = StreamingAgent(StreamConfig(model="claude-sonnet-4-5-20250929"))
    >>>
    >>> # Stream response
    >>> async for chunk in agent.execute_streaming("Hello!"):
    ...     if chunk.text:
    ...         print(chunk.text, end="", flush=True)
    >>>
    >>> # Or collect complete result
    >>> result = await agent.execute_and_collect("Hello!")
    >>> print(result.message.content)
    >>> print(f"Tokens: {result.message.output_tokens}")
"""

from .types import (
    StreamEventType,
    StreamChunk,
    StreamMessage,
    StreamConfig,
    StreamProgress,
    StreamResult,
)

from .agent import (
    StreamingAgent,
    StreamCollector,
    stream_to_text,
    stream_with_callback,
)

from .client import (
    BidirectionalStreamClient,
    StreamingConversation,
    stream_conversation,
    stream_and_print,
)

__all__ = [
    # Types
    'StreamEventType',
    'StreamChunk',
    'StreamMessage',
    'StreamConfig',
    'StreamProgress',
    'StreamResult',

    # Agent
    'StreamingAgent',
    'StreamCollector',
    'stream_to_text',
    'stream_with_callback',

    # Client
    'BidirectionalStreamClient',
    'StreamingConversation',
    'stream_conversation',
    'stream_and_print',
]

__version__ = '2.0.0'  # FASE 2.4: Streaming Support
