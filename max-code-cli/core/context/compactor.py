"""
Context Compactor - Main compaction engine

Orchestrates context compaction using different strategies.
Integrates with monitoring and hooks systems.

Biblical Foundation:
"Ajunta o que sobejou dos pedaços, para que nada se perca" (João 6:12)
Gather what remains - preserve essence, discard excess.
"""

import logging
import time
from typing import Optional
from datetime import datetime

from .types import (
    ConversationContext,
    CompactionConfig,
    CompactionResult,
    CompactionStrategy,
)
from .strategies import get_strategy, BaseCompactionStrategy

logger = logging.getLogger(__name__)


class ContextCompactor:
    """
    Main context compaction engine.

    Orchestrates compaction using configured strategy.
    Tracks statistics and integrates with hooks.
    """

    def __init__(
        self,
        config: Optional[CompactionConfig] = None,
        llm_client: Optional[any] = None,
    ):
        """
        Initialize compactor.

        Args:
            config: Compaction configuration (uses defaults if None)
            llm_client: Optional LLM client for summarization
        """
        self.config = config or CompactionConfig()
        self.llm_client = llm_client

        # Strategy instance (lazy-loaded)
        self._strategy: Optional[BaseCompactionStrategy] = None

        # Statistics
        self.total_compactions = 0
        self.total_tokens_saved = 0
        self.total_time_spent = 0.0

        logger.info(
            f"ContextCompactor initialized: "
            f"strategy={self.config.strategy}, "
            f"threshold={self.config.compact_threshold * 100}%"
        )

    @property
    def strategy(self) -> BaseCompactionStrategy:
        """Get strategy instance (lazy-loaded)"""
        if self._strategy is None:
            self._strategy = get_strategy(
                self.config.strategy, self.config, self.llm_client
            )
        return self._strategy

    async def compact(
        self,
        context: ConversationContext,
        target_tokens: Optional[int] = None,
        strategy_override: Optional[CompactionStrategy] = None,
    ) -> CompactionResult:
        """
        Compact conversation context.

        Args:
            context: Original conversation context
            target_tokens: Optional target token count (uses config if None)
            strategy_override: Optional strategy override

        Returns:
            CompactionResult with compacted context and statistics
        """
        start_time = time.time()

        original_token_count = context.get_token_count()
        original_message_count = len(context.messages)

        logger.info(
            f"Starting compaction: {original_token_count} tokens, "
            f"{original_message_count} messages"
        )

        # Use override strategy if provided
        if strategy_override:
            strategy = get_strategy(strategy_override, self.config, self.llm_client)
        else:
            strategy = self.strategy

        # Perform compaction
        try:
            compacted_context = strategy.compact(context, target_tokens)

        except Exception as e:
            logger.error(f"Compaction failed: {e}", exc_info=True)
            raise

        # Calculate statistics
        compacted_token_count = compacted_context.get_token_count()
        compacted_message_count = len(compacted_context.messages)

        messages_removed = original_message_count - compacted_message_count

        # Track messages summarized (from summary metadata if LLM strategy was used)
        messages_summarized = 0
        for msg in compacted_context.messages:
            if msg.metadata.get("type") == "summary":
                messages_summarized = msg.metadata.get("message_count", 0)
                break  # Only one summary per compaction

        compaction_time = time.time() - start_time

        # Create result
        result = CompactionResult(
            compacted_context=compacted_context,
            strategy_used=strategy_override or self.config.strategy,
            original_token_count=original_token_count,
            compacted_token_count=compacted_token_count,
            messages_removed=messages_removed,
            messages_summarized=messages_summarized,
            compaction_time=compaction_time,
        )

        # Update statistics
        self.total_compactions += 1
        self.total_tokens_saved += result.tokens_saved
        self.total_time_spent += compaction_time

        logger.info(
            f"Compaction complete: "
            f"{original_token_count} → {compacted_token_count} tokens "
            f"({result.compression_ratio * 100:.1f}% retained), "
            f"{messages_removed} messages removed, "
            f"{compaction_time:.2f}s"
        )

        return result

    def update_config(self, config: CompactionConfig):
        """
        Update compaction configuration.

        Args:
            config: New configuration
        """
        self.config = config
        self._strategy = None  # Reset strategy to use new config

        logger.info(f"Configuration updated: strategy={config.strategy}")

    def update_strategy(self, strategy: CompactionStrategy):
        """
        Update compaction strategy.

        Args:
            strategy: New strategy
        """
        self.config.strategy = strategy
        self._strategy = None  # Reset strategy instance

        logger.info(f"Strategy updated: {strategy}")

    def get_stats(self) -> dict:
        """
        Get compaction statistics.

        Returns:
            Dictionary with statistics
        """
        avg_time = (
            self.total_time_spent / self.total_compactions
            if self.total_compactions > 0
            else 0.0
        )
        avg_tokens_saved = (
            self.total_tokens_saved / self.total_compactions
            if self.total_compactions > 0
            else 0
        )

        return {
            "total_compactions": self.total_compactions,
            "total_tokens_saved": self.total_tokens_saved,
            "total_time_spent": self.total_time_spent,
            "avg_compaction_time": avg_time,
            "avg_tokens_saved": avg_tokens_saved,
            "current_strategy": self.config.strategy,
            "threshold": self.config.compact_threshold * 100,
            "target_ratio": self.config.target_ratio * 100,
        }

    def __repr__(self) -> str:
        """String representation with strategy and stats"""
        return (
            f"<ContextCompactor: {self.config.strategy}, "
            f"{self.total_compactions} compactions>"
        )


class CompactionManager:
    """
    High-level compaction manager.

    Integrates monitor, compactor, and hooks for complete
    auto-compaction workflow.
    """

    def __init__(
        self,
        context: ConversationContext,
        config: Optional[CompactionConfig] = None,
        llm_client: Optional[any] = None,
        hook_manager: Optional[any] = None,
    ):
        """
        Initialize compaction manager.

        Args:
            context: Conversation context
            config: Compaction configuration
            llm_client: Optional LLM client
            hook_manager: Optional hook manager
        """
        from .monitor import AutoCompactionMonitor

        self.config = config or CompactionConfig()
        self.context = context

        # Components
        self.compactor = ContextCompactor(self.config, llm_client)
        self.monitor = AutoCompactionMonitor(
            context, self.config, self.compactor, hook_manager
        )

        logger.info("CompactionManager initialized")

    async def add_message(self, message):
        """
        Add message and check for auto-compaction.

        Args:
            message: Message to add

        Returns:
            CompactionResult if compaction occurred, None otherwise
        """
        # Add message to context
        self.monitor.add_message(message)

        # Check if compaction needed
        result = await self.monitor.auto_compact_if_needed()

        if result:
            # Update context reference
            self.context = result.compacted_context

        return result

    async def compact_now(
        self, strategy_override: Optional[CompactionStrategy] = None
    ) -> CompactionResult:
        """
        Manually trigger compaction.

        Args:
            strategy_override: Optional strategy override

        Returns:
            CompactionResult
        """
        result = await self.compactor.compact(
            self.context, strategy_override=strategy_override
        )

        # Update monitor
        self.monitor.reset_after_compaction(result)

        # Update context reference
        self.context = result.compacted_context

        return result

    def get_usage_stats(self) -> dict:
        """Get combined usage and compaction statistics"""
        return {
            "monitor": self.monitor.get_stats(),
            "compactor": self.compactor.get_stats(),
        }

    def enable_auto_compact(self):
        """Enable automatic compaction"""
        self.monitor.enable_auto_compact()

    def disable_auto_compact(self):
        """Disable automatic compaction"""
        self.monitor.disable_auto_compact()

    def __repr__(self) -> str:
        """String representation with usage and compaction stats"""
        return (
            f"<CompactionManager: {self.monitor.get_usage_percent():.1f}% usage, "
            f"{self.compactor.total_compactions} compactions>"
        )
