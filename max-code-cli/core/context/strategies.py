"""
Compaction Strategies - Different approaches to context compression

Implements multiple strategies for reducing context size while preserving
important information.

Biblical Foundation:
"O sábio entesourou o conhecimento" (Provérbios 10:14)
Wisdom preserves knowledge - compress without losing essence.
"""

import logging
from typing import List, Optional
from abc import ABC, abstractmethod

from .types import (
    Message,
    MessageRole,
    ConversationContext,
    CompactionStrategy,
    CompactionConfig,
)

logger = logging.getLogger(__name__)


class BaseCompactionStrategy(ABC):
    """
    Base class for compaction strategies.

    Each strategy implements a different approach to reducing context size.
    """

    def __init__(self, config: CompactionConfig):
        """
        Initialize strategy.

        Args:
            config: Compaction configuration
        """
        self.config = config

    @abstractmethod
    def compact(
        self,
        context: ConversationContext,
        target_tokens: Optional[int] = None,
    ) -> ConversationContext:
        """
        Compact context to target size.

        Args:
            context: Original conversation context
            target_tokens: Target token count (optional, uses config if None)

        Returns:
            Compacted conversation context
        """
        pass

    def _calculate_target_tokens(self, context: ConversationContext) -> int:
        """Calculate target token count based on config"""
        current_tokens = context.get_token_count()
        target_tokens = int(current_tokens * self.config.target_ratio)
        return target_tokens

    def _preserve_system_messages(
        self, messages: List[Message]
    ) -> tuple[List[Message], List[Message]]:
        """
        Separate system messages from others.

        Returns:
            (system_messages, other_messages)
        """
        system = [msg for msg in messages if msg.role == MessageRole.SYSTEM]
        others = [msg for msg in messages if msg.role != MessageRole.SYSTEM]
        return system, others

    def _preserve_recent_messages(
        self, messages: List[Message], count: int
    ) -> tuple[List[Message], List[Message]]:
        """
        Separate recent messages from older ones.

        Returns:
            (recent_messages, older_messages)
        """
        if count <= 0:
            return [], messages

        recent = messages[-count:] if len(messages) > count else messages
        older = messages[:-count] if len(messages) > count else []
        return recent, older


class TruncateStrategy(BaseCompactionStrategy):
    """
    Simple truncation strategy.

    Removes oldest messages until target is reached.
    Fast, no token cost, but loses information.
    """

    def compact(
        self,
        context: ConversationContext,
        target_tokens: Optional[int] = None,
    ) -> ConversationContext:
        """Truncate oldest messages"""
        if target_tokens is None:
            target_tokens = self._calculate_target_tokens(context)

        logger.info(f"Truncating context to {target_tokens} tokens")

        # Preserve system messages
        system_msgs, other_msgs = self._preserve_system_messages(context.messages)

        # Preserve recent messages
        recent_msgs, older_msgs = self._preserve_recent_messages(
            other_msgs, self.config.preserve_recent_count
        )

        # Build compacted messages
        compacted_messages = system_msgs.copy()

        # Add recent messages (always preserved)
        compacted_messages.extend(recent_msgs)

        # Calculate current token count
        current_tokens = sum(msg.estimate_tokens() for msg in compacted_messages)

        # If still over target, remove from recent (start from oldest recent)
        if current_tokens > target_tokens:
            logger.warning(
                f"Even after truncation, context is {current_tokens} tokens "
                f"(target: {target_tokens}). Removing from recent messages."
            )

            # Remove messages from the beginning of recent_msgs
            final_messages = system_msgs.copy()
            remaining_tokens = target_tokens - sum(
                msg.estimate_tokens() for msg in system_msgs
            )

            for msg in reversed(recent_msgs):
                msg_tokens = msg.estimate_tokens()
                if remaining_tokens >= msg_tokens:
                    final_messages.insert(len(system_msgs), msg)
                    remaining_tokens -= msg_tokens

            compacted_messages = final_messages

        # Create compacted context
        compacted = ConversationContext(
            messages=compacted_messages,
            max_tokens=context.max_tokens,
            metadata=context.metadata.copy(),
        )

        logger.info(
            f"Truncated from {context.get_token_count()} to "
            f"{compacted.get_token_count()} tokens"
        )

        return compacted


class SelectiveStrategy(BaseCompactionStrategy):
    """
    Selective preservation strategy.

    Keeps:
    - All system messages
    - Recent messages
    - Tool results (important outputs)

    Removes:
    - Older user/assistant exchanges
    """

    def compact(
        self,
        context: ConversationContext,
        target_tokens: Optional[int] = None,
    ) -> ConversationContext:
        """Selectively preserve important messages"""
        if target_tokens is None:
            target_tokens = self._calculate_target_tokens(context)

        logger.info(f"Selectively compacting context to {target_tokens} tokens")

        # Categorize messages
        system_msgs = []
        recent_msgs = []
        tool_msgs = []
        other_msgs = []

        # Recent threshold
        recent_count = self.config.preserve_recent_count
        recent_start_idx = max(0, len(context.messages) - recent_count)

        for idx, msg in enumerate(context.messages):
            if msg.role == MessageRole.SYSTEM:
                system_msgs.append(msg)
            elif idx >= recent_start_idx:
                recent_msgs.append(msg)
            elif msg.role == MessageRole.TOOL:
                tool_msgs.append(msg)
            else:
                other_msgs.append(msg)

        # Build compacted messages (priority order)
        compacted_messages = []

        # 1. System messages (highest priority)
        compacted_messages.extend(system_msgs)

        # 2. Recent messages (second priority)
        compacted_messages.extend(recent_msgs)

        # 3. Tool messages (third priority, if space allows)
        current_tokens = sum(msg.estimate_tokens() for msg in compacted_messages)
        remaining_tokens = target_tokens - current_tokens

        for msg in reversed(tool_msgs):  # Most recent tool messages first
            msg_tokens = msg.estimate_tokens()
            if remaining_tokens >= msg_tokens:
                # Insert before recent messages
                compacted_messages.insert(len(system_msgs), msg)
                remaining_tokens -= msg_tokens

        # Create compacted context
        compacted = ConversationContext(
            messages=compacted_messages,
            max_tokens=context.max_tokens,
            metadata=context.metadata.copy(),
        )

        logger.info(
            f"Selective compaction: {context.get_token_count()} → "
            f"{compacted.get_token_count()} tokens "
            f"(kept {len(compacted_messages)}/{len(context.messages)} messages)"
        )

        return compacted


class RollingWindowStrategy(BaseCompactionStrategy):
    """
    Rolling window strategy.

    Keeps last N messages in a sliding window.
    Simple, predictable, preserves recent conversation flow.
    """

    def compact(
        self,
        context: ConversationContext,
        target_tokens: Optional[int] = None,
    ) -> ConversationContext:
        """Keep last N messages"""
        if target_tokens is None:
            target_tokens = self._calculate_target_tokens(context)

        logger.info(f"Rolling window compaction to {target_tokens} tokens")

        # Always preserve system messages
        system_msgs, other_msgs = self._preserve_system_messages(context.messages)

        # Calculate how many messages we can keep
        system_tokens = sum(msg.estimate_tokens() for msg in system_msgs)
        remaining_tokens = target_tokens - system_tokens

        # Add messages from most recent, working backwards
        window_msgs = []
        for msg in reversed(other_msgs):
            msg_tokens = msg.estimate_tokens()
            if remaining_tokens >= msg_tokens:
                window_msgs.insert(0, msg)
                remaining_tokens -= msg_tokens
            else:
                break

        # Build compacted messages
        compacted_messages = system_msgs + window_msgs

        # Create compacted context
        compacted = ConversationContext(
            messages=compacted_messages,
            max_tokens=context.max_tokens,
            metadata=context.metadata.copy(),
        )

        logger.info(
            f"Rolling window: kept {len(window_msgs)} messages "
            f"({compacted.get_token_count()} tokens)"
        )

        return compacted


class LLMSummaryStrategy(BaseCompactionStrategy):
    """
    LLM-based summarization strategy.

    Uses LLM to summarize older messages into condensed form.
    Best quality, but uses tokens for summarization.

    Strategy:
    - Keep system messages (first 20%)
    - Summarize middle messages (60%)
    - Keep recent messages (last 20%)
    """

    def __init__(self, config: CompactionConfig, llm_client=None):
        """
        Initialize strategy.

        Args:
            config: Compaction configuration
            llm_client: Optional LLM client for summarization
        """
        super().__init__(config)
        self.llm_client = llm_client

    def compact(
        self,
        context: ConversationContext,
        target_tokens: Optional[int] = None,
    ) -> ConversationContext:
        """Summarize using LLM"""
        if target_tokens is None:
            target_tokens = self._calculate_target_tokens(context)

        logger.info(f"LLM summarization to {target_tokens} tokens")

        # Split messages into sections
        system_msgs, other_msgs = self._preserve_system_messages(context.messages)

        # Calculate split points (20% recent, rest for summarization)
        total_msgs = len(other_msgs)
        recent_count = max(
            self.config.preserve_recent_count, int(total_msgs * 0.20)
        )

        recent_msgs = other_msgs[-recent_count:] if recent_count > 0 else []
        middle_msgs = other_msgs[:-recent_count] if recent_count > 0 else other_msgs

        # If no LLM client, fall back to selective strategy
        if self.llm_client is None:
            logger.warning(
                "No LLM client provided, falling back to selective strategy"
            )
            fallback = SelectiveStrategy(self.config)
            return fallback.compact(context, target_tokens)

        # Summarize middle messages with LLM
        if middle_msgs:
            try:
                summary_text = self._summarize_with_llm(middle_msgs)
                logger.info(f"LLM generated summary of {len(middle_msgs)} messages")
            except Exception as e:
                logger.warning(f"LLM summarization failed: {e}, using placeholder")
                summary_text = self._create_summary_placeholder(middle_msgs)

            summary_msg = Message(
                role=MessageRole.SYSTEM,
                content=summary_text,
                metadata={"type": "summary", "message_count": len(middle_msgs)},
            )

            compacted_messages = system_msgs + [summary_msg] + recent_msgs
        else:
            compacted_messages = system_msgs + recent_msgs

        # Create compacted context
        compacted = ConversationContext(
            messages=compacted_messages,
            max_tokens=context.max_tokens,
            metadata=context.metadata.copy(),
        )

        logger.info(
            f"LLM summary: {len(context.messages)} → {len(compacted_messages)} messages "
            f"({context.get_token_count()} → {compacted.get_token_count()} tokens)"
        )

        return compacted

    def _summarize_with_llm(self, messages: List[Message]) -> str:
        """Generate real LLM-based summary of conversation history"""
        # Build prompt for summarization
        conversation_text = "\n\n".join([
            f"[{msg.role.value}]: {msg.content[:500]}"  # Truncate long messages
            for msg in messages
        ])

        summarization_prompt = f"""Please provide a concise summary of the following conversation history.
Focus on key decisions, important information, and context that would be helpful for continuing the conversation.
Keep the summary brief but informative (2-4 sentences).

Conversation to summarize:
{conversation_text}

Summary:"""

        # Call LLM for summarization
        try:
            response = self.llm_client.messages.create(
                model="claude-3-haiku-20240307",  # Use fast model for summarization
                max_tokens=200,  # Brief summary
                messages=[{"role": "user", "content": summarization_prompt}]
            )

            summary = response.content[0].text if response.content else ""
            return f"[Context Summary]: {summary}"

        except Exception as e:
            logger.error(f"LLM summarization error: {e}")
            # Fallback to placeholder if LLM fails
            return self._create_summary_placeholder(messages)

    def _create_summary_placeholder(self, messages: List[Message]) -> str:
        """Create placeholder summary (fallback when LLM unavailable)"""
        user_msgs = sum(1 for msg in messages if msg.role == MessageRole.USER)
        assistant_msgs = sum(
            1 for msg in messages if msg.role == MessageRole.ASSISTANT
        )
        tool_msgs = sum(1 for msg in messages if msg.role == MessageRole.TOOL)

        return (
            f"[Context Summary: Previous conversation included "
            f"{user_msgs} user messages, {assistant_msgs} assistant responses, "
            f"and {tool_msgs} tool executions. "
            f"Total messages summarized: {len(messages)}]"
        )


# Strategy factory
def get_strategy(
    strategy: CompactionStrategy, config: CompactionConfig, llm_client=None
) -> BaseCompactionStrategy:
    """
    Get compaction strategy instance.

    Args:
        strategy: Strategy type
        config: Compaction config
        llm_client: Optional LLM client (for LLM_SUMMARY)

    Returns:
        Strategy instance
    """
    strategies = {
        CompactionStrategy.TRUNCATE: TruncateStrategy,
        CompactionStrategy.SELECTIVE: SelectiveStrategy,
        CompactionStrategy.ROLLING_WINDOW: RollingWindowStrategy,
        CompactionStrategy.LLM_SUMMARY: LLMSummaryStrategy,
    }

    strategy_class = strategies.get(strategy)
    if strategy_class is None:
        logger.warning(f"Unknown strategy {strategy}, using SELECTIVE")
        strategy_class = SelectiveStrategy

    if strategy == CompactionStrategy.LLM_SUMMARY:
        return strategy_class(config, llm_client)

    return strategy_class(config)
