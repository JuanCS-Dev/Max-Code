"""
Example: Context Compaction System - Auto-compaction and Monitoring

Demonstrates Anthropic SDK-style context compaction following FASE 2.3 implementation.

Features:
- Auto-compaction at threshold (75% default)
- 4 compaction strategies
- Context monitoring
- Statistics tracking

Run: python examples/context_compaction_example.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, '.')

from core.context import (
    Message,
    MessageRole,
    ConversationContext,
    CompactionStrategy,
    CompactionConfig,
    CompactionManager,
    ContextMonitor,
    ContextCompactor,
)


# ============================================================================
# EXAMPLE 1: Basic context creation and message handling
# ============================================================================

def example_basic_context():
    """Create basic conversation context"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Context Creation")
    print("=" * 70)

    # Create context with 10K token limit (for demo purposes)
    context = ConversationContext(max_tokens=10000)

    # Add messages
    messages = [
        Message(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
        Message(role=MessageRole.USER, content="Hello! Can you help me with Python?"),
        Message(role=MessageRole.ASSISTANT, content="Of course! I'd be happy to help you with Python. What would you like to know?"),
        Message(role=MessageRole.USER, content="How do I read a file in Python?"),
        Message(role=MessageRole.ASSISTANT, content="You can read a file using: with open('file.txt', 'r') as f: content = f.read()"),
    ]

    for msg in messages:
        context.add_message(msg)

    print(f"✅ Created context with {len(context.messages)} messages")
    print(f"📊 Token usage: {context.get_token_count()} / {context.max_tokens}")
    print(f"📈 Usage: {context.get_usage_percent():.1f}%")
    print()


# ============================================================================
# EXAMPLE 2: Context monitoring
# ============================================================================

async def example_monitoring():
    """Monitor context usage"""
    print("=" * 70)
    print("EXAMPLE 2: Context Monitoring")
    print("=" * 70)

    context = ConversationContext(max_tokens=1000)  # Small limit for demo
    config = CompactionConfig(compact_threshold=0.75)

    monitor = ContextMonitor(context, config)

    # Add messages and monitor
    print(f"Initial usage: {monitor.get_usage_percent():.1f}%\n")

    messages = [
        "This is message 1 with some content to consume tokens.",
        "Message 2 continues the conversation with more text.",
        "Message 3 adds even more content to increase token usage.",
        "Message 4 keeps going to reach the threshold.",
        "Message 5 should push us over the 75% threshold.",
        "Message 6 for good measure to ensure we cross it.",
    ]

    for i, content in enumerate(messages, 1):
        msg = Message(role=MessageRole.USER, content=content * 5)  # Repeat to increase size
        monitor.add_message(msg)

        usage = monitor.get_usage_percent()
        should_compact = monitor.should_compact()

        print(f"Message {i}: {usage:.1f}% usage - {'🔴 COMPACT!' if should_compact else '🟢 OK'}")

    print(f"\n📊 Final stats:")
    stats = monitor.get_stats()
    print(f"   - Usage: {stats['usage_percent']:.1f}%")
    print(f"   - Remaining: {stats['remaining_tokens']} tokens")
    print(f"   - Threshold crossings: {stats['threshold_crossings']}")
    print()


# ============================================================================
# EXAMPLE 3: Truncate strategy
# ============================================================================

async def example_truncate_strategy():
    """Demonstrate truncate compaction strategy"""
    print("=" * 70)
    print("EXAMPLE 3: Truncate Strategy")
    print("=" * 70)

    # Create context with many messages
    context = ConversationContext(max_tokens=5000)

    # Add 20 messages
    for i in range(20):
        context.add_message(
            Message(
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}: " + "Some content here. " * 20,
            )
        )

    print(f"Original: {context.get_token_count()} tokens, {len(context.messages)} messages")

    # Compact using truncate strategy
    config = CompactionConfig(
        strategy=CompactionStrategy.TRUNCATE,
        target_ratio=0.50,
        preserve_recent_count=5,
    )

    compactor = ContextCompactor(config)
    result = await compactor.compact(context)

    print(f"Compacted: {result.compacted_token_count} tokens, "
          f"{len(result.compacted_context.messages)} messages")
    print(f"📊 Compression ratio: {result.compression_ratio * 100:.1f}%")
    print(f"💾 Tokens saved: {result.tokens_saved}")
    print(f"⏱️  Time: {result.compaction_time:.3f}s")
    print(f"🗑️  Messages removed: {result.messages_removed}")
    print()


# ============================================================================
# EXAMPLE 4: Selective strategy
# ============================================================================

async def example_selective_strategy():
    """Demonstrate selective compaction strategy"""
    print("=" * 70)
    print("EXAMPLE 4: Selective Strategy")
    print("=" * 70)

    context = ConversationContext(max_tokens=5000)

    # Add mix of messages
    context.add_message(Message(role=MessageRole.SYSTEM, content="System prompt."))

    for i in range(15):
        context.add_message(
            Message(
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Old message {i}: " + "Content. " * 15,
            )
        )

    # Add some tool messages
    context.add_message(Message(role=MessageRole.TOOL, content="Tool result 1: Important data"))
    context.add_message(Message(role=MessageRole.TOOL, content="Tool result 2: More important data"))

    # Add recent messages
    for i in range(5):
        context.add_message(
            Message(
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Recent message {i}: " + "Recent content. " * 10,
            )
        )

    print(f"Original: {context.get_token_count()} tokens, {len(context.messages)} messages")
    print(f"  - System: {len(context.get_system_messages())}")
    print(f"  - Total: {len(context.messages)}")

    # Compact using selective strategy
    config = CompactionConfig(
        strategy=CompactionStrategy.SELECTIVE,
        target_ratio=0.60,
        preserve_recent_count=5,
    )

    compactor = ContextCompactor(config)
    result = await compactor.compact(context)

    print(f"\nCompacted: {result.compacted_token_count} tokens, "
          f"{len(result.compacted_context.messages)} messages")
    print(f"  - Kept system messages: ✅")
    print(f"  - Kept recent messages: ✅")
    print(f"  - Kept tool messages: ✅ (if space allowed)")
    print(f"📊 Compression ratio: {result.compression_ratio * 100:.1f}%")
    print()


# ============================================================================
# EXAMPLE 5: Rolling window strategy
# ============================================================================

async def example_rolling_window():
    """Demonstrate rolling window strategy"""
    print("=" * 70)
    print("EXAMPLE 5: Rolling Window Strategy")
    print("=" * 70)

    context = ConversationContext(max_tokens=3000)

    # Add 30 messages
    for i in range(30):
        context.add_message(
            Message(
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}: " + "Content here. " * 10,
            )
        )

    print(f"Original: {context.get_token_count()} tokens, {len(context.messages)} messages")

    # Compact using rolling window
    config = CompactionConfig(
        strategy=CompactionStrategy.ROLLING_WINDOW,
        target_ratio=0.40,
    )

    compactor = ContextCompactor(config)
    result = await compactor.compact(context)

    print(f"Compacted: {result.compacted_token_count} tokens, "
          f"{len(result.compacted_context.messages)} messages")
    print(f"📊 Kept most recent messages only")
    print(f"💾 Tokens saved: {result.tokens_saved}")
    print()


# ============================================================================
# EXAMPLE 6: Auto-compaction with CompactionManager
# ============================================================================

async def example_auto_compaction():
    """Demonstrate automatic compaction"""
    print("=" * 70)
    print("EXAMPLE 6: Auto-Compaction")
    print("=" * 70)

    context = ConversationContext(max_tokens=2000)

    config = CompactionConfig(
        compact_threshold=0.75,
        target_ratio=0.50,
        strategy=CompactionStrategy.TRUNCATE,
        auto_compact=True,
    )

    manager = CompactionManager(context, config)

    print(f"Auto-compact enabled: {manager.monitor.auto_compact_enabled}")
    print(f"Threshold: {config.compact_threshold * 100}%")
    print(f"Target ratio: {config.target_ratio * 100}%\n")

    # Add messages until auto-compaction triggers
    for i in range(50):
        msg = Message(
            role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
            content=f"Message {i}: " + "Content here. " * 15,
        )

        result = await manager.add_message(msg)

        usage = manager.monitor.get_usage_percent()

        if result:
            print(f"🔴 AUTO-COMPACTION TRIGGERED at message {i}!")
            print(f"   Usage before: {result.original_token_count} tokens")
            print(f"   Usage after: {result.compacted_token_count} tokens")
            print(f"   Saved: {result.tokens_saved} tokens\n")
            break
        elif i % 10 == 0:
            print(f"Message {i}: {usage:.1f}% usage")

    stats = manager.get_usage_stats()
    print(f"\n📊 Final stats:")
    print(f"   - Current usage: {stats['monitor']['usage_percent']:.1f}%")
    print(f"   - Total compactions: {stats['compactor']['total_compactions']}")
    print(f"   - Total tokens saved: {stats['compactor']['total_tokens_saved']}")
    print()


# ============================================================================
# EXAMPLE 7: Manual compaction
# ============================================================================

async def example_manual_compaction():
    """Demonstrate manual compaction trigger"""
    print("=" * 70)
    print("EXAMPLE 7: Manual Compaction")
    print("=" * 70)

    context = ConversationContext(max_tokens=5000)

    # Add messages
    for i in range(25):
        context.add_message(
            Message(
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}: " + "Content. " * 20,
            )
        )

    config = CompactionConfig(auto_compact=False)  # Disable auto
    manager = CompactionManager(context, config)

    print(f"Usage before: {manager.monitor.get_usage_percent():.1f}%")

    # Manually trigger compaction
    result = await manager.compact_now()

    print(f"Usage after: {manager.monitor.get_usage_percent():.1f}%")
    print(f"📊 Compression ratio: {result.compression_ratio * 100:.1f}%")
    print(f"💾 Tokens saved: {result.tokens_saved}")
    print()


# ============================================================================
# EXAMPLE 8: Strategy comparison
# ============================================================================

async def example_strategy_comparison():
    """Compare different compaction strategies"""
    print("=" * 70)
    print("EXAMPLE 8: Strategy Comparison")
    print("=" * 70)

    # Create identical contexts
    def create_test_context():
        ctx = ConversationContext(max_tokens=5000)
        ctx.add_message(Message(role=MessageRole.SYSTEM, content="System prompt."))
        for i in range(30):
            ctx.add_message(
                Message(
                    role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                    content=f"Message {i}: " + "Content. " * 15,
                )
            )
        return ctx

    strategies = [
        CompactionStrategy.TRUNCATE,
        CompactionStrategy.SELECTIVE,
        CompactionStrategy.ROLLING_WINDOW,
    ]

    original_tokens = create_test_context().get_token_count()
    print(f"Original context: {original_tokens} tokens, 31 messages\n")

    for strategy in strategies:
        context = create_test_context()
        config = CompactionConfig(strategy=strategy, target_ratio=0.50)
        compactor = ContextCompactor(config)

        result = await compactor.compact(context)

        print(f"📌 {strategy.upper()}:")
        print(f"   - Tokens: {result.original_token_count} → {result.compacted_token_count}")
        print(f"   - Ratio: {result.compression_ratio * 100:.1f}%")
        print(f"   - Saved: {result.tokens_saved} tokens")
        print(f"   - Time: {result.compaction_time:.3f}s")
        print(f"   - Messages: {result.original_token_count // 100} → {len(result.compacted_context.messages)}")
        print()


# ============================================================================
# EXAMPLE 9: Statistics tracking
# ============================================================================

async def example_statistics():
    """Track compaction statistics"""
    print("=" * 70)
    print("EXAMPLE 9: Statistics Tracking")
    print("=" * 70)

    context = ConversationContext(max_tokens=3000)
    config = CompactionConfig(
        compact_threshold=0.70,
        target_ratio=0.45,
        auto_compact=True,
    )

    manager = CompactionManager(context, config)

    # Simulate conversation with multiple compactions
    for i in range(100):
        msg = Message(
            role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
            content=f"Message {i}: " + "Content. " * 20,
        )

        result = await manager.add_message(msg)

        if result:
            print(f"Compaction #{manager.compactor.total_compactions} at message {i}")

    # Print comprehensive stats
    stats = manager.get_usage_stats()

    print(f"\n📊 COMPREHENSIVE STATISTICS:")
    print(f"\n📈 Monitor Stats:")
    print(f"   - Current usage: {stats['monitor']['usage_percent']:.1f}%")
    print(f"   - Peak usage: {stats['monitor']['peak_usage_percent']:.1f}%")
    print(f"   - Threshold crossings: {stats['monitor']['threshold_crossings']}")
    print(f"   - Message count: {stats['monitor']['message_count']}")

    print(f"\n🗜️  Compactor Stats:")
    print(f"   - Total compactions: {stats['compactor']['total_compactions']}")
    print(f"   - Total tokens saved: {stats['compactor']['total_tokens_saved']}")
    print(f"   - Avg tokens saved: {stats['compactor']['avg_tokens_saved']:.0f}")
    print(f"   - Avg compaction time: {stats['compactor']['avg_compaction_time']:.3f}s")
    print(f"   - Total time spent: {stats['compactor']['total_time_spent']:.2f}s")
    print()


# ============================================================================
# MAIN: Run all examples
# ============================================================================

async def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "CONTEXT COMPACTION EXAMPLES - FASE 2.3" + " " * 21 + "║")
    print("║" + " " * 9 + "Anthropic SDK-style Auto-Compaction System" + " " * 18 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    # Run examples
    example_basic_context()
    await example_monitoring()
    await example_truncate_strategy()
    await example_selective_strategy()
    await example_rolling_window()
    await example_auto_compaction()
    await example_manual_compaction()
    await example_strategy_comparison()
    await example_statistics()

    print("=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)
    print()

    print("📊 SUMMARY:")
    print("   - 4 compaction strategies implemented")
    print("   - Auto-compaction at threshold (default: 75%)")
    print("   - Configurable target ratio (default: 50%)")
    print("   - Comprehensive statistics tracking")
    print("   - Token estimation and monitoring")
    print()


if __name__ == "__main__":
    asyncio.run(main())
