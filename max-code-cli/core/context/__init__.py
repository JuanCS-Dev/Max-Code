"""
Context Management System - Auto-compaction and monitoring

Anthropic SDK-style context management with:
- Auto-compaction at configurable threshold (default: 75%)
- Multiple compaction strategies (LLM summary, truncate, selective, rolling window)
- Context monitoring and token tracking
- Integration with hooks system (PreCompact events)

Biblical Foundation:
"Porque qual de vós, querendo edificar uma torre, não se assenta primeiro a fazer
as contas dos gastos?" (Lucas 14:28)
Count the cost - manage resources wisely.

Features:
- ✅ Context monitoring (track token usage)
- ✅ Auto-compaction at threshold (default: 75%)
- ✅ 4 compaction strategies (LLM, Truncate, Selective, Rolling Window)
- ✅ PreCompact hook integration
- ✅ Configurable threshold and target ratio
- ✅ Statistics tracking (tokens saved, compression ratio, etc.)
- ✅ Manual compaction trigger

Example:
    >>> from core.context import CompactionManager, CompactionConfig
    >>> from core.context import ConversationContext, Message, MessageRole
    >>>
    >>> # Create context
    >>> context = ConversationContext(max_tokens=200000)
    >>>
    >>> # Create manager with config
    >>> config = CompactionConfig(
    ...     compact_threshold=0.75,  # Compact at 75%
    ...     target_ratio=0.50,       # Compress to 50%
    ...     strategy=CompactionStrategy.LLM_SUMMARY,
    ...     auto_compact=True,
    ... )
    >>>
    >>> manager = CompactionManager(context, config)
    >>>
    >>> # Add messages (auto-compacts when threshold reached)
    >>> message = Message(role=MessageRole.USER, content="Hello")
    >>> await manager.add_message(message)
    >>>
    >>> # Or manually trigger
    >>> result = await manager.compact_now()
    >>> print(f"Saved {result.tokens_saved} tokens")
"""

from .types import (
    Message,
    MessageRole,
    ConversationContext,
    CompactionStrategy,
    CompactionResult,
    CompactionConfig,
)

from .strategies import (
    BaseCompactionStrategy,
    TruncateStrategy,
    SelectiveStrategy,
    RollingWindowStrategy,
    LLMSummaryStrategy,
    get_strategy,
)

from .monitor import (
    ContextMonitor,
    AutoCompactionMonitor,
)

from .compactor import (
    ContextCompactor,
    CompactionManager,
)

__all__ = [
    # Types
    'Message',
    'MessageRole',
    'ConversationContext',
    'CompactionStrategy',
    'CompactionResult',
    'CompactionConfig',

    # Strategies
    'BaseCompactionStrategy',
    'TruncateStrategy',
    'SelectiveStrategy',
    'RollingWindowStrategy',
    'LLMSummaryStrategy',
    'get_strategy',

    # Monitor
    'ContextMonitor',
    'AutoCompactionMonitor',

    # Compactor
    'ContextCompactor',
    'CompactionManager',
]

__version__ = '2.0.0'  # FASE 2.3: Context Compaction System
