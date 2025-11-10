"""
Claude Streaming Adapter - Bridge between Claude API and Thinking Display

Integrates Anthropic Claude API streaming with enhanced thinking display.

Features:
- Automatic thinking/output detection
- Tool use tracking
- Extended thinking mode support
- Performance metrics

Biblical Foundation:
"E o que de mim, entre muitas testemunhas, ouviste, confia-o a homens fiéis,
que sejam idôneos para também ensinarem os outros" (2 Timóteo 2:2)
Faithful transmission - from API to display.

Soli Deo Gloria
"""

import asyncio
import os
from typing import AsyncIterator, Optional, Dict, Any, List
from anthropic import AsyncAnthropic, Anthropic
from anthropic.types import (
    MessageStreamEvent,
    ContentBlockDeltaEvent,
    MessageDeltaEvent,
    MessageStopEvent,
)

from .types import StreamChunk, StreamEventType
from .thinking_display import (
    EnhancedThinkingDisplay,
    ThinkingPhase,
    ThinkingDisplayConfig,
)


class ClaudeStreamAdapter:
    """
    Adapter for Claude API streaming with thinking display.
    
    Bridges Anthropic SDK streaming events to our thinking display system.
    Automatically detects thinking vs output, tracks tool use, and manages display.
    
    Features:
    - Auto-detects extended thinking blocks
    - Separates reasoning from output
    - Tracks tool invocations
    - Real-time metrics
    
    Usage:
        adapter = ClaudeStreamAdapter()
        async for chunk in adapter.stream_with_thinking(
            prompt="Create a hello world function",
            agent_name="code"
        ):
            # Chunk is displayed automatically
            pass
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
    ):
        """
        Initialize adapter.
        
        Args:
            api_key: Anthropic API key (from env if None)
            model: Claude model to use
            max_tokens: Maximum tokens
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        
        # Create clients
        self.client = AsyncAnthropic(api_key=self.api_key)
        self.sync_client = Anthropic(api_key=self.api_key)
    
    async def stream_with_thinking(
        self,
        prompt: str,
        agent_name: str = "assistant",
        system: Optional[str] = None,
        display_config: Optional[ThinkingDisplayConfig] = None,
        **kwargs
    ) -> AsyncIterator[StreamChunk]:
        """
        Stream Claude response with enhanced thinking display.
        
        Args:
            prompt: User prompt
            agent_name: Name of agent (for display styling)
            system: System prompt
            display_config: Display configuration
            **kwargs: Additional Claude API parameters
        
        Yields:
            StreamChunk objects
        
        Example:
            async for chunk in adapter.stream_with_thinking(
                "Create hello world",
                agent_name="code",
                system="You are a code generator."
            ):
                # Automatic thinking display
                if chunk.text:
                    print(chunk.text, end="")
        """
        # Build messages
        messages = [{"role": "user", "content": prompt}]
        
        # Add extended thinking instruction to system prompt
        if system:
            system = self._enhance_system_prompt(system)
        else:
            system = self._get_default_system_prompt(agent_name)
        
        # Create display
        async with EnhancedThinkingDisplay(
            agent_name=agent_name,
            config=display_config,
        ) as display:
            
            display.add_thinking_step(
                ThinkingPhase.INITIALIZING,
                "Connecting to Claude API..."
            )
            await display.update()
            
            # State tracking
            in_thinking_block = False
            thinking_buffer = []
            output_buffer = []
            
            try:
                # Stream from Claude
                async with self.client.messages.stream(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=messages,
                    system=system,
                    **kwargs
                ) as stream:
                    
                    display.add_thinking_step(
                        ThinkingPhase.ANALYZING,
                        "Processing request..."
                    )
                    display.complete_thinking_step()
                    await display.update()
                    
                    async for event in stream:
                        chunk = self._convert_event_to_chunk(event)
                        
                        if chunk:
                            # Update display progress
                            display.update_progress(chunk)
                            
                            # Handle content
                            if chunk.text:
                                # Detect thinking vs output
                                is_thinking = self._is_thinking_content(chunk.text)
                                
                                if is_thinking and not in_thinking_block:
                                    # Entering thinking block
                                    in_thinking_block = True
                                    display.add_thinking_step(
                                        ThinkingPhase.PLANNING,
                                        "Reasoning about approach..."
                                    )
                                    thinking_buffer.append(chunk.text)
                                
                                elif is_thinking and in_thinking_block:
                                    # Continuing thinking
                                    thinking_buffer.append(chunk.text)
                                    
                                    # Update thinking display periodically
                                    thinking_text = "".join(thinking_buffer)
                                    if len(thinking_text) % 50 < 10:  # Update every ~50 chars
                                        lines = thinking_text.split('\n')
                                        if lines:
                                            last_line = lines[-1][:80]
                                            display.thinking_steps[-1].description = last_line
                                
                                elif not is_thinking and in_thinking_block:
                                    # Exiting thinking block
                                    in_thinking_block = False
                                    display.complete_thinking_step()
                                    display.add_thinking_step(
                                        ThinkingPhase.EXECUTING,
                                        "Generating output..."
                                    )
                                    output_buffer.append(chunk.text)
                                
                                else:
                                    # Regular output
                                    output_buffer.append(chunk.text)
                                    display.add_output(chunk.text)
                            
                            # Yield chunk
                            await display.update()
                            yield chunk
                    
                    # Complete
                    display.add_thinking_step(
                        ThinkingPhase.COMPLETING,
                        "Response complete"
                    )
                    display.complete_thinking_step()
                    await display.update()
            
            except Exception as e:
                display.add_thinking_step(
                    ThinkingPhase.ERROR,
                    f"Error: {str(e)}"
                )
                display.complete_thinking_step()
                await display.update()
                raise
    
    def _convert_event_to_chunk(self, event: MessageStreamEvent) -> Optional[StreamChunk]:
        """Convert Anthropic event to StreamChunk"""
        if isinstance(event, ContentBlockDeltaEvent):
            # Text delta
            if hasattr(event.delta, 'text'):
                return StreamChunk(
                    event_type=StreamEventType.CONTENT_BLOCK_DELTA,
                    data={"delta": {"text": event.delta.text}},
                )
        
        elif isinstance(event, MessageDeltaEvent):
            # Message delta (usage updates)
            return StreamChunk(
                event_type=StreamEventType.MESSAGE_DELTA,
                data={
                    "delta": event.delta.model_dump() if hasattr(event.delta, 'model_dump') else {},
                    "usage": event.usage.model_dump() if hasattr(event, 'usage') and event.usage else {},
                },
            )
        
        elif isinstance(event, MessageStopEvent):
            # Stream complete
            return StreamChunk(
                event_type=StreamEventType.MESSAGE_STOP,
                data={},
            )
        
        return None
    
    def _is_thinking_content(self, text: str) -> bool:
        """
        Heuristic to detect thinking vs output content.
        
        Thinking indicators:
        - Starts with analysis keywords
        - Contains reasoning markers
        - Has planning language
        """
        text_lower = text.lower().strip()
        
        # Strong thinking indicators
        thinking_starters = [
            "i need to",
            "first, i",
            "let me",
            "i'll",
            "i will",
            "i should",
            "the approach is",
            "my plan is",
            "step 1:",
            "step 2:",
        ]
        
        # Reasoning keywords
        reasoning_keywords = [
            "analyzing",
            "considering",
            "thinking",
            "planning",
            "evaluating",
            "reasoning",
            "determining",
            "assessing",
        ]
        
        # Check starters
        for starter in thinking_starters:
            if text_lower.startswith(starter):
                return True
        
        # Check keywords (needs multiple matches)
        keyword_matches = sum(1 for kw in reasoning_keywords if kw in text_lower)
        if keyword_matches >= 2:
            return True
        
        return False
    
    def _enhance_system_prompt(self, system: str) -> str:
        """Add extended thinking instruction to system prompt"""
        thinking_instruction = """

IMPORTANT: Show your thinking process BEFORE providing your final answer.

Structure your response as:
1. First, explain your reasoning, analysis, and approach
2. Then, provide your final output/code/answer

Example:
```
I need to analyze the requirements...
The approach will be to...
Key considerations: ...

[Then provide actual output]
```
"""
        return system + thinking_instruction
    
    def _get_default_system_prompt(self, agent_name: str) -> str:
        """Get default system prompt for agent"""
        base = f"""You are {agent_name.upper()}, an expert AI assistant.

You are operating under the VÉRTICE CONSTITUTION v3.0, which mandates:
- P1: Complete, functional code (no TODOs, placeholders)
- P2: Validate APIs before using (no hallucinations)
- P3: Critical thinking (challenge flawed assumptions)
- P4: Traceability (cite sources)
- P5: Systemic awareness (consider impact)
- P6: Token efficiency (diagnose before fixing)

Show your thinking process BEFORE providing output.
"""
        return base


class ClaudeAgentIntegration:
    """
    Integration layer for agents to use Claude streaming.
    
    Provides simple interface for agents to get streaming with thinking display.
    
    Usage in agent:
        integration = ClaudeAgentIntegration()
        result = await integration.execute_with_thinking(
            prompt="Generate code",
            agent_name="code",
        )
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize integration"""
        self.adapter = ClaudeStreamAdapter(api_key=api_key)
    
    async def execute_with_thinking(
        self,
        prompt: str,
        agent_name: str = "assistant",
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Execute prompt with thinking display, return complete text.
        
        Args:
            prompt: User prompt
            agent_name: Agent name
            system: System prompt
            **kwargs: Additional parameters
        
        Returns:
            Complete response text
        """
        output_parts = []
        
        async for chunk in self.adapter.stream_with_thinking(
            prompt=prompt,
            agent_name=agent_name,
            system=system,
            **kwargs
        ):
            if chunk.text:
                output_parts.append(chunk.text)
        
        return "".join(output_parts)
    
    def execute_with_thinking_sync(
        self,
        prompt: str,
        agent_name: str = "assistant",
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Sync wrapper for execute_with_thinking.
        
        Args:
            prompt: User prompt
            agent_name: Agent name
            system: System prompt
            **kwargs: Additional parameters
        
        Returns:
            Complete response text
        """
        return asyncio.run(
            self.execute_with_thinking(
                prompt=prompt,
                agent_name=agent_name,
                system=system,
                **kwargs
            )
        )


# Export
__all__ = [
    'ClaudeStreamAdapter',
    'ClaudeAgentIntegration',
]
