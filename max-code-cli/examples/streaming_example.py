"""
Example: Streaming System - AsyncIterator-based Streaming

Demonstrates Anthropic SDK-style streaming following FASE 2.4 implementation.

Features:
- AsyncIterator streaming patterns
- Bidirectional communication
- Real-time progress tracking
- Token-by-token delivery

Run: python examples/streaming_example.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, '.')

from core.streaming import (
    StreamingAgent,
    StreamCollector,
    StreamConfig,
    StreamChunk,
    BidirectionalStreamClient,
    StreamingConversation,
    stream_to_text,
    stream_with_callback,
    stream_and_print,
)


# ============================================================================
# EXAMPLE 1: Basic streaming
# ============================================================================

async def example_basic_streaming():
    """Basic streaming example"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Streaming")
    print("=" * 70)

    agent = StreamingAgent()

    print("Streaming response:\n")
    print(">>> ", end="", flush=True)

    async for chunk in agent.execute_streaming("Hello! Tell me about streaming."):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")


# ============================================================================
# EXAMPLE 2: Collect complete result
# ============================================================================

async def example_collect_result():
    """Collect complete streaming result"""
    print("=" * 70)
    print("EXAMPLE 2: Collect Complete Result")
    print("=" * 70)

    agent = StreamingAgent()

    result = await agent.execute_and_collect("What is the capital of France?")

    print(f"✅ Complete message received")
    print(f"\n📝 Content:\n{result.message.content}\n")
    print(f"📊 Statistics:")
    print(f"   - Input tokens: {result.message.input_tokens}")
    print(f"   - Output tokens: {result.message.output_tokens}")
    print(f"   - Total chunks: {result.total_chunks}")
    print(f"   - Duration: {result.total_time:.2f}s")
    print(f"   - Success: {result.success}")
    print()


# ============================================================================
# EXAMPLE 3: Progress tracking
# ============================================================================

async def example_progress_tracking():
    """Track streaming progress"""
    print("=" * 70)
    print("EXAMPLE 3: Progress Tracking")
    print("=" * 70)

    agent = StreamingAgent()
    collector = StreamCollector()

    print("Streaming with progress tracking:\n")

    async for chunk in agent.execute_streaming("Explain quantum computing briefly."):
        collector.add_chunk(chunk)

        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")
    print(f"📊 Progress Stats:")
    progress = collector.progress
    print(f"   - Chunks: {progress.chunks_received}")
    print(f"   - Tokens: {progress.tokens_generated}")
    print(f"   - Chars: {progress.chars_generated}")
    print(f"   - Time: {progress.elapsed_time:.2f}s")
    print(f"   - Tokens/sec: {progress.tokens_per_second:.1f}")
    print(f"   - Chars/sec: {progress.chars_per_second:.1f}")
    print(f"   - Complete: {progress.is_complete}")
    print()


# ============================================================================
# EXAMPLE 4: Chunk callback
# ============================================================================

async def example_chunk_callback():
    """Use callback for each chunk"""
    print("=" * 70)
    print("EXAMPLE 4: Chunk Callback")
    print("=" * 70)

    agent = StreamingAgent()

    chunk_count = 0
    text_chunks = 0

    def on_chunk(chunk: StreamChunk):
        nonlocal chunk_count, text_chunks
        chunk_count += 1
        if chunk.text:
            text_chunks += 1

    print("Streaming with callback:\n")
    print(">>> ", end="", flush=True)

    result = await agent.execute_and_collect(
        "List 3 programming languages.",
        on_chunk=on_chunk
    )

    print(result.message.content)
    print(f"\n📊 Callback Stats:")
    print(f"   - Total chunks: {chunk_count}")
    print(f"   - Text chunks: {text_chunks}")
    print()


# ============================================================================
# EXAMPLE 5: Bidirectional streaming
# ============================================================================

async def example_bidirectional():
    """Bidirectional streaming"""
    print("=" * 70)
    print("EXAMPLE 5: Bidirectional Streaming")
    print("=" * 70)

    client = BidirectionalStreamClient()

    async with client.session():
        print("Session established\n")

        # Query 1
        print("Query 1: What is AI?")
        print(">>> ", end="", flush=True)

        async for chunk in client.query("What is AI in one sentence?"):
            if chunk.text:
                print(chunk.text, end="", flush=True)

        print("\n")

        # Query 2
        print("Query 2: What is ML?")
        print(">>> ", end="", flush=True)

        async for chunk in client.query("What is ML in one sentence?"):
            if chunk.text:
                print(chunk.text, end="", flush=True)

        print("\n")

    print("Session closed\n")


# ============================================================================
# EXAMPLE 6: Streaming conversation
# ============================================================================

async def example_conversation():
    """Multi-turn streaming conversation"""
    print("=" * 70)
    print("EXAMPLE 6: Streaming Conversation")
    print("=" * 70)

    conversation = StreamingConversation()

    messages = [
        "Hello!",
        "What's 2+2?",
        "Thanks!",
    ]

    for i, msg in enumerate(messages, 1):
        print(f"\n[Turn {i}] User: {msg}")
        print("Assistant: ", end="", flush=True)

        response = await conversation.send_message(msg)
        print(response.content)

    print(f"\n📝 Conversation history: {len(conversation.get_history())} messages")
    print()


# ============================================================================
# EXAMPLE 7: Stream utilities
# ============================================================================

async def example_utilities():
    """Demonstrate utility functions"""
    print("=" * 70)
    print("EXAMPLE 7: Stream Utilities")
    print("=" * 70)

    agent = StreamingAgent()

    # stream_to_text
    print("1️⃣  stream_to_text():")
    print("   ", end="", flush=True)

    text = await stream_to_text(agent.execute_streaming("Say hello!"))
    print(text)

    # stream_with_callback
    print("\n2️⃣  stream_with_callback():")

    chunks = []

    def track_chunk(chunk):
        chunks.append(chunk)

    print("   ", end="", flush=True)

    result = await stream_with_callback(
        agent.execute_streaming("Count to 3."),
        track_chunk
    )
    print(result.message.content)
    print(f"   Tracked {len(chunks)} chunks")

    # stream_and_print
    print("\n3️⃣  stream_and_print():")
    print("   ", end="", flush=True)

    text = await stream_and_print("What is Python?")

    print()


# ============================================================================
# EXAMPLE 8: Custom config
# ============================================================================

async def example_custom_config():
    """Use custom streaming config"""
    print("=" * 70)
    print("EXAMPLE 8: Custom Configuration")
    print("=" * 70)

    config = StreamConfig(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        temperature=0.7,
        show_progress=True,
        show_tokens=True,
    )

    agent = StreamingAgent(config)

    print(f"Config:")
    print(f"   - Model: {config.model}")
    print(f"   - Max tokens: {config.max_tokens}")
    print(f"   - Temperature: {config.temperature}")

    print("\nStreaming response:\n>>> ", end="", flush=True)

    result = await agent.execute_and_collect("Explain recursion briefly.")

    print(result.message.content)
    print()


# ============================================================================
# EXAMPLE 9: Error handling
# ============================================================================

async def example_error_handling():
    """Handle streaming errors"""
    print("=" * 70)
    print("EXAMPLE 9: Error Handling")
    print("=" * 70)

    agent = StreamingAgent()

    try:
        collector = StreamCollector()

        async for chunk in agent.execute_streaming("Test error handling"):
            collector.add_chunk(chunk)

            if chunk.is_error:
                print(f"❌ Error detected: {chunk.data.get('message')}")
                break

            if chunk.text:
                print(chunk.text, end="", flush=True)

        if collector.progress.error:
            print(f"\n⚠️  Stream error: {collector.progress.error}")
        else:
            print("\n✅ Stream completed successfully")

    except Exception as e:
        print(f"❌ Exception: {e}")

    print()


# ============================================================================
# EXAMPLE 10: Performance comparison
# ============================================================================

async def example_performance():
    """Compare streaming vs non-streaming performance"""
    print("=" * 70)
    print("EXAMPLE 10: Performance Comparison")
    print("=" * 70)

    agent = StreamingAgent()
    prompt = "Explain the benefits of streaming responses."

    # Streaming
    print("1️⃣  Streaming mode:")
    import time
    start = time.time()

    result = await agent.execute_and_collect(prompt)

    streaming_time = time.time() - start

    print(f"   Time to first token: ~0.05s (simulated)")
    print(f"   Total time: {streaming_time:.2f}s")
    print(f"   Tokens/sec: {result.message.output_tokens / streaming_time:.1f}")

    # Note: In real implementation, streaming shows tokens immediately
    # while non-streaming waits for complete response

    print("\n2️⃣  Benefits of streaming:")
    print("   ✅ Faster perceived response time")
    print("   ✅ Better UX (see progress in real-time)")
    print("   ✅ Can process tokens as they arrive")
    print("   ✅ Lower latency to first token")
    print()


# ============================================================================
# MAIN: Run all examples
# ============================================================================

async def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 14 + "STREAMING EXAMPLES - FASE 2.4" + " " * 25 + "║")
    print("║" + " " * 10 + "Anthropic SDK-style AsyncIterator Streaming" + " " * 16 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    # Run examples
    await example_basic_streaming()
    await example_collect_result()
    await example_progress_tracking()
    await example_chunk_callback()
    await example_bidirectional()
    await example_conversation()
    await example_utilities()
    await example_custom_config()
    await example_error_handling()
    await example_performance()

    print("=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)
    print()

    print("📊 SUMMARY:")
    print("   - AsyncIterator streaming (Anthropic SDK pattern)")
    print("   - Bidirectional communication")
    print("   - Real-time progress tracking")
    print("   - Token-by-token delivery")
    print("   - Conversation management")
    print("   - Comprehensive statistics")
    print()


if __name__ == "__main__":
    asyncio.run(main())
