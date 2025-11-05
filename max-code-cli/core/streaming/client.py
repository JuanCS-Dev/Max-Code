"""
Bidirectional Streaming Client - Two-way streaming communication

Implements Anthropic SDK-style bidirectional streaming patterns.

Biblical Foundation:
"Assim como a água reflete o rosto, o coração reflete quem somos" (Provérbios 27:19)
Two-way reflection - bidirectional communication.
"""

import asyncio
import logging
from typing import AsyncIterator, Optional, Any
from datetime import datetime
from contextlib import asynccontextmanager

from .types import (
    StreamChunk,
    StreamMessage,
    StreamConfig,
    StreamEventType,
)
from .agent import StreamingAgent, StreamCollector

logger = logging.getLogger(__name__)


class BidirectionalStreamClient:
    """
    Bidirectional streaming client.

    Supports:
    - Sending streaming input
    - Receiving streaming output
    - Full-duplex communication
    """

    def __init__(
        self,
        config: Optional[StreamConfig] = None,
        llm_client: Optional[Any] = None,
    ):
        """
        Initialize bidirectional client.

        Args:
            config: Streaming configuration
            llm_client: Optional LLM client
        """
        self.config = config or StreamConfig()
        self.llm_client = llm_client
        self.agent = StreamingAgent(config, llm_client)

        # Connection state
        self._connected = False
        self._input_queue: asyncio.Queue = asyncio.Queue()
        self._output_queue: asyncio.Queue = asyncio.Queue()

        logger.info("BidirectionalStreamClient initialized")

    async def connect(self):
        """Establish connection"""
        self._connected = True
        logger.info("Client connected")

    async def disconnect(self):
        """Close connection"""
        self._connected = False
        logger.info("Client disconnected")

    async def send(self, message: str):
        """
        Send message to input stream.

        Args:
            message: Message to send
        """
        if not self._connected:
            raise RuntimeError("Client not connected")

        await self._input_queue.put(message)
        logger.debug(f"Sent message: {len(message)} chars")

    async def receive(self) -> AsyncIterator[StreamChunk]:
        """
        Receive streaming output.

        Yields:
            StreamChunk objects
        """
        if not self._connected:
            raise RuntimeError("Client not connected")

        while self._connected or not self._output_queue.empty():
            try:
                chunk = await asyncio.wait_for(
                    self._output_queue.get(), timeout=1.0
                )
                yield chunk

                # Stop if final chunk
                if chunk.is_final:
                    break

            except asyncio.TimeoutError:
                continue

    async def query(self, message: str) -> AsyncIterator[StreamChunk]:
        """
        Send query and receive streaming response.

        Args:
            message: Query message

        Yields:
            StreamChunk objects
        """
        if not self._connected:
            await self.connect()

        # Stream response
        async for chunk in self.agent.execute_streaming(message):
            yield chunk

    async def interactive_session(
        self, input_stream: AsyncIterator[str]
    ) -> AsyncIterator[StreamChunk]:
        """
        Interactive bidirectional session.

        Args:
            input_stream: Stream of input messages

        Yields:
            StreamChunk objects from responses
        """
        if not self._connected:
            await self.connect()

        async for user_input in input_stream:
            logger.info(f"Processing input: {len(user_input)} chars")

            # Stream response for this input
            async for chunk in self.agent.execute_streaming(user_input):
                yield chunk

    @asynccontextmanager
    async def session(self):
        """
        Context manager for streaming session.

        Usage:
            async with client.session():
                await client.send("Hello")
                async for chunk in client.receive():
                    print(chunk.text)
        """
        await self.connect()
        try:
            yield self
        finally:
            await self.disconnect()


class StreamingConversation:
    """
    High-level conversation manager with streaming.

    Manages full conversation with streaming responses.
    """

    def __init__(
        self,
        config: Optional[StreamConfig] = None,
        llm_client: Optional[Any] = None,
    ):
        """
        Initialize conversation.

        Args:
            config: Streaming configuration
            llm_client: Optional LLM client
        """
        self.config = config or StreamConfig()
        self.client = BidirectionalStreamClient(config, llm_client)

        # Conversation history
        self.messages: list[StreamMessage] = []

        logger.info("StreamingConversation initialized")

    async def send_message(
        self, content: str, on_chunk: Optional[Any] = None
    ) -> StreamMessage:
        """
        Send message and receive streaming response.

        Args:
            content: Message content
            on_chunk: Optional callback for each chunk

        Returns:
            Complete StreamMessage
        """
        # Add user message
        user_msg = StreamMessage(role="user", content=content)
        user_msg.finalize()
        self.messages.append(user_msg)

        # Stream assistant response
        collector = StreamCollector()

        async for chunk in self.client.query(content):
            if on_chunk:
                on_chunk(chunk)
            collector.add_chunk(chunk)

        # Add assistant message
        self.messages.append(collector.message)

        return collector.message

    async def stream_response(self, content: str) -> AsyncIterator[StreamChunk]:
        """
        Send message and stream response chunks.

        Args:
            content: Message content

        Yields:
            StreamChunk objects
        """
        # Add user message
        user_msg = StreamMessage(role="user", content=content)
        user_msg.finalize()
        self.messages.append(user_msg)

        # Stream response
        collector = StreamCollector()

        async for chunk in self.client.query(content):
            collector.add_chunk(chunk)
            yield chunk

        # Add assistant message to history
        self.messages.append(collector.message)

    def get_history(self) -> list[StreamMessage]:
        """Get conversation history"""
        return self.messages.copy()

    def clear_history(self):
        """Clear conversation history"""
        self.messages.clear()
        logger.info("Conversation history cleared")


# Utility functions

async def stream_conversation(
    messages: list[str],
    config: Optional[StreamConfig] = None,
) -> list[StreamMessage]:
    """
    Stream a sequence of messages through conversation.

    Args:
        messages: List of user messages
        config: Streaming configuration

    Returns:
        List of all messages (user + assistant)
    """
    conversation = StreamingConversation(config)

    all_messages = []

    for msg in messages:
        response = await conversation.send_message(msg)
        all_messages.extend([
            StreamMessage(role="user", content=msg),
            response,
        ])

    return all_messages


async def stream_and_print(
    prompt: str,
    config: Optional[StreamConfig] = None,
) -> str:
    """
    Stream response and print in real-time.

    Args:
        prompt: User prompt
        config: Streaming configuration

    Returns:
        Complete response text
    """
    agent = StreamingAgent(config)
    text_parts = []

    async for chunk in agent.execute_streaming(prompt):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            text_parts.append(chunk.text)

    print()  # Newline at end
    return "".join(text_parts)
