"""
Context Monitor - Track context usage and trigger compaction

Monitors token usage and triggers compaction when threshold is reached.
Compatible with Anthropic Claude Code patterns (2025).

Biblical Foundation:
"Vigia, pois, porque não sabeis a que hora há de vir o vosso Senhor" (Mateus 24:42)
Watch vigilantly - monitor before limits are reached.
"""

import logging
import asyncio
from typing import Optional, Callable, Awaitable
from datetime import datetime

from .types import (
    ConversationContext,
    CompactionConfig,
    CompactionResult,
    Message,
)

logger = logging.getLogger(__name__)


class ContextMonitor:
    """
    Monitor context usage and trigger compaction.

    Tracks token usage and alerts when threshold is reached.
    Integrates with auto-compaction system.
    """

    def __init__(
        self,
        context: ConversationContext,
        config: CompactionConfig,
        on_threshold_reached: Optional[
            Callable[[ConversationContext], Awaitable[bool]]
        ] = None,
    ):
        """
        Initialize monitor.

        Args:
            context: Conversation context to monitor
            config: Compaction configuration
            on_threshold_reached: Callback when threshold reached (returns True to compact)
        """
        self.context = context
        self.config = config
        self.on_threshold_reached = on_threshold_reached

        # Monitoring state
        self.threshold_reached = False
        self.last_check_time = datetime.now()
        self.check_count = 0

        # Statistics
        self.peak_usage = 0.0
        self.threshold_crossings = 0

        logger.info(
            f"ContextMonitor initialized: max={context.max_tokens} tokens, "
            f"threshold={config.compact_threshold * 100}%"
        )

    def get_current_usage(self) -> int:
        """Get current token usage"""
        return self.context.get_token_count()

    def get_usage_ratio(self) -> float:
        """Get usage ratio (0.0 to 1.0)"""
        return self.context.get_usage_ratio()

    def get_usage_percent(self) -> float:
        """Get usage percentage (0.0 to 100.0)"""
        return self.context.get_usage_percent()

    def get_remaining_tokens(self) -> int:
        """Get remaining token capacity"""
        return self.context.max_tokens - self.get_current_usage()

    def should_compact(self) -> bool:
        """
        Check if compaction should trigger.

        Returns:
            True if usage >= threshold
        """
        ratio = self.get_usage_ratio()
        return ratio >= self.config.compact_threshold

    def can_add_tokens(self, token_count: int) -> bool:
        """
        Check if adding tokens would exceed threshold.

        Args:
            token_count: Number of tokens to add

        Returns:
            True if addition won't exceed threshold
        """
        projected_usage = self.get_current_usage() + token_count
        projected_ratio = projected_usage / self.context.max_tokens
        return projected_ratio < self.config.compact_threshold

    async def check_and_trigger(self) -> Optional[bool]:
        """
        Check threshold and trigger callback if needed.

        Returns:
            True if compaction requested, False if declined, None if not needed
        """
        self.check_count += 1
        self.last_check_time = datetime.now()

        # Update peak usage
        current_ratio = self.get_usage_ratio()
        if current_ratio > self.peak_usage:
            self.peak_usage = current_ratio

        # Check threshold
        if self.should_compact():
            if not self.threshold_reached:
                # First time crossing threshold
                self.threshold_reached = True
                self.threshold_crossings += 1

                logger.warning(
                    f"Context threshold reached: {self.get_usage_percent():.1f}% "
                    f"({self.get_current_usage()}/{self.context.max_tokens} tokens)"
                )

            # Trigger callback if configured
            if self.on_threshold_reached:
                should_compact = await self.on_threshold_reached(self.context)
                return should_compact

            return True  # Default: compact when threshold reached

        else:
            # Below threshold
            if self.threshold_reached:
                # Crossed back below threshold (after compaction)
                logger.info(
                    f"Context usage back below threshold: {self.get_usage_percent():.1f}%"
                )
                self.threshold_reached = False

            return None  # No action needed

    def add_message(self, message: Message):
        """
        Add message to context and update tracking.

        Args:
            message: Message to add
        """
        self.context.add_message(message)

        # Log if approaching threshold
        ratio = self.get_usage_ratio()
        if ratio >= self.config.compact_threshold * 0.90:  # 90% of threshold
            logger.info(
                f"Context approaching threshold: {self.get_usage_percent():.1f}%"
            )

    def reset_after_compaction(self, result: CompactionResult):
        """
        Reset monitor state after compaction.

        Args:
            result: Compaction result
        """
        # Update context reference
        self.context = result.compacted_context

        # Reset threshold flag
        self.threshold_reached = False

        logger.info(
            f"Monitor reset after compaction: "
            f"{result.compacted_token_count} tokens "
            f"({self.get_usage_percent():.1f}%)"
        )

    def get_stats(self) -> dict:
        """
        Get monitoring statistics.

        Returns:
            Dictionary with stats
        """
        return {
            "current_usage": self.get_current_usage(),
            "usage_percent": self.get_usage_percent(),
            "max_tokens": self.context.max_tokens,
            "remaining_tokens": self.get_remaining_tokens(),
            "threshold": self.config.compact_threshold * 100,
            "threshold_reached": self.threshold_reached,
            "peak_usage_percent": self.peak_usage * 100,
            "threshold_crossings": self.threshold_crossings,
            "check_count": self.check_count,
            "last_check": self.last_check_time.isoformat(),
            "message_count": len(self.context.messages),
        }

    def __repr__(self) -> str:
        return (
            f"<ContextMonitor: {self.get_usage_percent():.1f}% "
            f"({self.get_current_usage()}/{self.context.max_tokens} tokens)>"
        )


class AutoCompactionMonitor(ContextMonitor):
    """
    Enhanced monitor with automatic compaction triggering.

    Extends ContextMonitor with auto-compaction capability.
    Integrates with hooks system for PreCompact events.
    """

    def __init__(
        self,
        context: ConversationContext,
        config: CompactionConfig,
        compactor: Optional["ContextCompactor"] = None,  # Forward reference
        hook_manager: Optional[any] = None,
    ):
        """
        Initialize auto-compaction monitor.

        Args:
            context: Conversation context
            config: Compaction configuration
            compactor: Optional compactor instance
            hook_manager: Optional hook manager for PreCompact events
        """
        super().__init__(context, config)

        self.compactor = compactor
        self.hook_manager = hook_manager

        # Auto-compaction state
        self.auto_compact_enabled = config.auto_compact
        self.compaction_count = 0
        self.last_compaction_time: Optional[datetime] = None

        logger.info(
            f"AutoCompactionMonitor initialized: "
            f"auto_compact={self.auto_compact_enabled}"
        )

    async def auto_compact_if_needed(self) -> Optional[CompactionResult]:
        """
        Automatically compact if threshold reached.

        Returns:
            CompactionResult if compaction occurred, None otherwise
        """
        if not self.auto_compact_enabled:
            return None

        if not self.should_compact():
            return None

        logger.info("Auto-compaction triggered")

        # Trigger PreCompact hook if configured
        if self.config.trigger_precompact_hook and self.hook_manager:
            await self._trigger_precompact_hook()

        # Require confirmation if configured
        if self.config.require_confirmation:
            confirmed = await self._request_confirmation()
            if not confirmed:
                logger.info("Auto-compaction declined by user")
                return None

        # Perform compaction
        if self.compactor is None:
            logger.error("No compactor configured for auto-compaction")
            return None

        result = await self.compactor.compact(self.context)

        # Update state
        self.compaction_count += 1
        self.last_compaction_time = datetime.now()
        self.reset_after_compaction(result)

        logger.info(
            f"Auto-compaction #{self.compaction_count} complete: "
            f"{result.original_token_count} → {result.compacted_token_count} tokens"
        )

        return result

    async def _trigger_precompact_hook(self):
        """Trigger PreCompact hook"""
        try:
            from core.hooks import HookEvent, HookPayload

            payload = HookPayload(
                event=HookEvent.PRE_COMPACT,
                context_usage=self.get_usage_ratio(),
                context_limit=self.context.max_tokens,
            )

            await self.hook_manager.trigger(HookEvent.PRE_COMPACT, payload)

        except Exception as e:
            logger.warning(f"Failed to trigger PreCompact hook: {e}")

    async def _request_confirmation(self) -> bool:
        """
        Request user confirmation for compaction.

        Returns:
            True if user confirms
        """
        # TODO: Implement user prompt
        # For now, auto-approve
        logger.info("User confirmation required (auto-approved for now)")
        return True

    def enable_auto_compact(self):
        """Enable automatic compaction"""
        self.auto_compact_enabled = True
        logger.info("Auto-compaction enabled")

    def disable_auto_compact(self):
        """Disable automatic compaction"""
        self.auto_compact_enabled = False
        logger.info("Auto-compaction disabled")

    def get_stats(self) -> dict:
        """Get monitoring statistics with compaction info"""
        stats = super().get_stats()
        stats.update(
            {
                "auto_compact_enabled": self.auto_compact_enabled,
                "compaction_count": self.compaction_count,
                "last_compaction": (
                    self.last_compaction_time.isoformat()
                    if self.last_compaction_time
                    else None
                ),
            }
        )
        return stats
