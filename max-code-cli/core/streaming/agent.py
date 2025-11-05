"""
Streaming Agent - AsyncIterator-based agent execution

Implements Anthropic SDK-style streaming patterns for agent responses.

Biblical Foundation:
"E havia um rio cujas correntes alegram a cidade de Deus" (Salmos 46:4)
Rivers of living water - continuous, life-giving flow.
"""

import asyncio
import logging
from typing import AsyncIterator, Optional, Callable, Any
from datetime import datetime

from .types import (
    StreamChunk,
    StreamMessage,
    StreamConfig,
    StreamProgress,
    StreamResult,
    StreamEventType,
)

logger = logging.getLogger(__name__)


class StreamingAgent:
    """
    Agent with streaming response support.

    Yields chunks as they arrive, compatible with Anthropic SDK patterns.
    """

    def __init__(
        self,
        config: Optional[StreamConfig] = None,
        llm_client: Optional[Any] = None,
    ):
        """
        Initialize streaming agent.

        Args:
            config: Streaming configuration
            llm_client: Optional LLM client for actual streaming
        """
        self.config = config or StreamConfig()
        self.llm_client = llm_client

        logger.info(f"StreamingAgent initialized: model={self.config.model}")

    async def execute_streaming(
        self,
        prompt: str,
        on_chunk: Optional[Callable[[StreamChunk], None]] = None,
    ) -> AsyncIterator[StreamChunk]:
        """
        Execute prompt with streaming response.

        Yields chunks as they arrive from LLM.

        Args:
            prompt: User prompt
            on_chunk: Optional callback for each chunk

        Yields:
            StreamChunk objects
        """
        logger.info(f"Starting streaming execution: {len(prompt)} chars")

        try:
            # If LLM client provided, use real streaming
            if self.llm_client:
                async for chunk in self._stream_from_llm(prompt):
                    if on_chunk:
                        on_chunk(chunk)
                    yield chunk

            else:
                # Mock streaming for demo/testing
                async for chunk in self._mock_stream(prompt):
                    if on_chunk:
                        on_chunk(chunk)
                    yield chunk

        except Exception as e:
            logger.error(f"Streaming failed: {e}", exc_info=True)
            # Yield error chunk
            yield StreamChunk(
                event_type=StreamEventType.ERROR,
                data={"message": str(e)},
            )

    async def execute_and_collect(
        self,
        prompt: str,
        on_chunk: Optional[Callable[[StreamChunk], None]] = None,
    ) -> StreamResult:
        """
        Execute and collect full streaming result.

        Args:
            prompt: User prompt
            on_chunk: Optional callback for each chunk

        Returns:
            StreamResult with complete message and statistics
        """
        message = StreamMessage(model=self.config.model)
        progress = StreamProgress()

        chunk_count = 0
        start_time = datetime.now()

        async for chunk in self.execute_streaming(prompt, on_chunk):
            chunk_count += 1
            progress.update_chunk(chunk)

            # Build message from chunks
            if chunk.text:
                message.append_text(chunk.text)

            # Handle final chunk
            if chunk.is_final:
                stop_reason = chunk.data.get("stop_reason")
                message.finalize(stop_reason)

            # Handle token usage
            if "usage" in chunk.data:
                usage = chunk.data["usage"]
                message.input_tokens = usage.get("input_tokens", 0)
                message.output_tokens = usage.get("output_tokens", 0)

        total_time = (datetime.now() - start_time).total_seconds()

        return StreamResult(
            message=message,
            progress=progress,
            total_chunks=chunk_count,
            total_time=total_time,
        )

    async def _stream_from_llm(self, prompt: str) -> AsyncIterator[StreamChunk]:
        """
        Stream from actual LLM client.

        TODO: Implement real Anthropic API streaming.
        """
        # Placeholder for real LLM streaming
        # This would use self.llm_client to stream from Anthropic API

        raise NotImplementedError(
            "Real LLM streaming not implemented. Use mock streaming for now."
        )

    async def _mock_stream(self, prompt: str) -> AsyncIterator[StreamChunk]:
        """
        Mock streaming for demo/testing.

        Simulates realistic streaming behavior.
        """
        # Message start
        yield StreamChunk(
            event_type=StreamEventType.MESSAGE_START,
            data={
                "message": {
                    "role": "assistant",
                    "model": self.config.model,
                }
            },
        )

        await asyncio.sleep(0.05)

        # Content block start
        yield StreamChunk(
            event_type=StreamEventType.CONTENT_BLOCK_START,
            data={"index": 0, "type": "text"},
        )

        await asyncio.sleep(0.05)

        # Stream text in chunks
        response_text = self._generate_mock_response(prompt)

        # Split into words for realistic streaming
        words = response_text.split()

        for i, word in enumerate(words):
            text = word + (" " if i < len(words) - 1 else "")

            yield StreamChunk(
                event_type=StreamEventType.CONTENT_BLOCK_DELTA,
                data={"delta": {"text": text}},
            )

            # Simulate network delay
            await asyncio.sleep(0.02)

        # Content block stop
        yield StreamChunk(
            event_type=StreamEventType.CONTENT_BLOCK_STOP,
            data={"index": 0},
        )

        await asyncio.sleep(0.05)

        # Message stop with usage
        yield StreamChunk(
            event_type=StreamEventType.MESSAGE_STOP,
            data={
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": len(prompt) // 4,  # Rough estimate
                    "output_tokens": len(response_text) // 4,
                },
            },
        )

    def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock response based on prompt"""
        # Simple mock response
        return (
            f"This is a streamed response to your prompt. "
            f"Your prompt was {len(prompt)} characters long. "
            f"In a real implementation, this would use the Anthropic API "
            f"to stream the actual response from Claude. "
            f"The streaming system supports real-time token-by-token delivery "
            f"with progress tracking and comprehensive statistics."
        )


class StreamCollector:
    """
    Utility to collect and accumulate streaming chunks.

    Simplifies working with streaming responses.
    """

    def __init__(self):
        """Initialize collector"""
        self.chunks: list[StreamChunk] = []
        self.message = StreamMessage()
        self.progress = StreamProgress()

    def add_chunk(self, chunk: StreamChunk):
        """Add chunk to collector"""
        self.chunks.append(chunk)
        self.progress.update_chunk(chunk)

        # Build message
        if chunk.text:
            self.message.append_text(chunk.text)

        if chunk.is_final:
            self.message.finalize(chunk.data.get("stop_reason"))

        if "usage" in chunk.data:
            usage = chunk.data["usage"]
            self.message.input_tokens = usage.get("input_tokens", 0)
            self.message.output_tokens = usage.get("output_tokens", 0)

    async def collect_stream(
        self, stream: AsyncIterator[StreamChunk]
    ) -> StreamResult:
        """
        Collect all chunks from stream.

        Args:
            stream: Async iterator of chunks

        Returns:
            StreamResult with complete message
        """
        start_time = datetime.now()

        async for chunk in stream:
            self.add_chunk(chunk)

        total_time = (datetime.now() - start_time).total_seconds()

        return StreamResult(
            message=self.message,
            progress=self.progress,
            total_chunks=len(self.chunks),
            total_time=total_time,
        )

    def get_text(self) -> str:
        """Get accumulated text"""
        return self.message.content

    def is_complete(self) -> bool:
        """Check if stream is complete"""
        return self.progress.is_complete


async def stream_to_text(stream: AsyncIterator[StreamChunk]) -> str:
    """
    Collect stream into complete text.

    Convenience function for simple text extraction.

    Args:
        stream: Async iterator of chunks

    Returns:
        Complete text from stream
    """
    collector = StreamCollector()
    await collector.collect_stream(stream)
    return collector.get_text()


async def stream_with_callback(
    stream: AsyncIterator[StreamChunk],
    on_chunk: Callable[[StreamChunk], None],
) -> StreamResult:
    """
    Process stream with callback for each chunk.

    Args:
        stream: Async iterator of chunks
        on_chunk: Callback function

    Returns:
        StreamResult
    """
    collector = StreamCollector()

    async for chunk in stream:
        on_chunk(chunk)
        collector.add_chunk(chunk)

    return StreamResult(
        message=collector.message,
        progress=collector.progress,
        total_chunks=len(collector.chunks),
        total_time=collector.progress.elapsed_time,
    )
