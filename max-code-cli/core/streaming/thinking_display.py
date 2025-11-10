"""
Enhanced Thinking Display - World-Class Visual Feedback System

Real-time thinking process visualization with:
- Agent-specific thinking patterns
- Multi-phase reasoning display
- Tool use tracking
- Performance metrics
- Beautiful Rich-based UI

Biblical Foundation:
"Porque, como ele imagina em sua alma, assim é" (Provérbios 23:7)
As a mind thinks, so it displays.

Soli Deo Gloria
"""

import asyncio
import time
from typing import Optional, List, Dict, Any, AsyncIterator, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich.markdown import Markdown

from .types import StreamChunk, StreamEventType, StreamProgress


class ThinkingPhase(str, Enum):
    """Phases of thinking process"""
    INITIALIZING = "initializing"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    VALIDATING = "validating"
    COMPLETING = "completing"
    ERROR = "error"


@dataclass
class ThinkingStep:
    """Single step in thinking process"""
    phase: ThinkingPhase
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    completed: bool = False
    result: Optional[str] = None
    error: Optional[str] = None
    
    @property
    def duration(self) -> float:
        """Duration in seconds"""
        return (datetime.now() - self.timestamp).total_seconds()
    
    def complete(self, result: Optional[str] = None):
        """Mark step as completed"""
        self.completed = True
        self.result = result
    
    def fail(self, error: str):
        """Mark step as failed"""
        self.completed = True
        self.error = error
        self.phase = ThinkingPhase.ERROR


@dataclass
class ToolUse:
    """Tool usage tracking"""
    tool_name: str
    input_params: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    completed: bool = False
    output: Optional[Any] = None
    error: Optional[str] = None
    
    @property
    def duration(self) -> float:
        """Duration in seconds"""
        return (datetime.now() - self.timestamp).total_seconds()
    
    def complete(self, output: Any):
        """Mark tool use as completed"""
        self.completed = True
        self.output = output
    
    def fail(self, error: str):
        """Mark tool use as failed"""
        self.completed = True
        self.error = error


class ThinkingDisplayConfig:
    """Configuration for thinking display"""
    
    def __init__(
        self,
        # Visual settings
        show_thinking: bool = True,
        show_tools: bool = True,
        show_metrics: bool = True,
        show_code_preview: bool = True,
        
        # Timing
        refresh_rate: float = 10.0,
        animation_speed: float = 1.0,
        
        # Content
        max_thinking_lines: int = 10,
        max_tool_history: int = 5,
        max_output_lines: int = 20,
        
        # Colors (agent-specific)
        agent_colors: Optional[Dict[str, str]] = None,
    ):
        """Initialize configuration"""
        self.show_thinking = show_thinking
        self.show_tools = show_tools
        self.show_metrics = show_metrics
        self.show_code_preview = show_code_preview
        
        self.refresh_rate = refresh_rate
        self.animation_speed = animation_speed
        
        self.max_thinking_lines = max_thinking_lines
        self.max_tool_history = max_tool_history
        self.max_output_lines = max_output_lines
        
        self.agent_colors = agent_colors or {
            'code': 'cyan',
            'test': 'green',
            'fix': 'yellow',
            'review': 'magenta',
            'docs': 'blue',
            'architect': 'gold1',
            'default': 'white',
        }
    
    def get_agent_color(self, agent_name: str) -> str:
        """Get color for agent"""
        return self.agent_colors.get(agent_name.lower(), self.agent_colors['default'])


class EnhancedThinkingDisplay:
    """
    World-class thinking display with real-time updates.
    
    Features:
    - Multi-phase thinking visualization
    - Tool use tracking with parameters
    - Performance metrics (tokens/sec, time)
    - Code/output preview
    - Agent-specific styling
    - Smooth animations
    - Error handling with details
    
    Usage:
        async with EnhancedThinkingDisplay(agent_name="code") as display:
            display.add_thinking_step(ThinkingPhase.ANALYZING, "Reading codebase...")
            await display.update()
            
            display.add_tool_use("read_file", {"path": "main.py"})
            await display.update()
            
            display.complete_tool_use("read_file", "File content...")
            display.add_output("Generated code...")
            await display.update()
    """
    
    def __init__(
        self,
        agent_name: str = "assistant",
        console: Optional[Console] = None,
        config: Optional[ThinkingDisplayConfig] = None,
    ):
        """
        Initialize thinking display.
        
        Args:
            agent_name: Name of agent (for styling)
            console: Rich console (created if None)
            config: Display configuration
        """
        self.agent_name = agent_name
        self.console = console or Console()
        self.config = config or ThinkingDisplayConfig()
        
        # State
        self.thinking_steps: List[ThinkingStep] = []
        self.tool_uses: List[ToolUse] = []
        self.output_lines: List[str] = []
        self.code_blocks: List[tuple[str, str]] = []  # (language, code)
        
        # Progress tracking
        self.progress = StreamProgress()
        self.start_time = datetime.now()
        
        # UI components
        self.live: Optional[Live] = None
        self.current_phase = ThinkingPhase.INITIALIZING
        
        # Agent color
        self.agent_color = self.config.get_agent_color(agent_name)
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.start()
        return self
    
    async def __aexit__(self, *args):
        """Async context manager exit"""
        await self.stop()
    
    def __enter__(self):
        """Sync context manager entry"""
        self.start()
        return self
    
    def __exit__(self, *args):
        """Sync context manager exit"""
        self.stop_sync()
    
    def start(self):
        """Start live display"""
        if not self.config.show_thinking:
            return
        
        self.live = Live(
            console=self.console,
            refresh_per_second=self.config.refresh_rate,
            transient=False,
        )
        self.live.__enter__()
        self._render()
    
    async def stop(self):
        """Stop live display (async)"""
        if self.live:
            self.current_phase = ThinkingPhase.COMPLETING
            self._render()
            await asyncio.sleep(0.5)  # Final render
            self.live.__exit__(None, None, None)
            self.live = None
    
    def stop_sync(self):
        """Stop live display (sync)"""
        if self.live:
            self.current_phase = ThinkingPhase.COMPLETING
            self._render()
            time.sleep(0.5)
            self.live.__exit__(None, None, None)
            self.live = None
    
    def add_thinking_step(self, phase: ThinkingPhase, description: str):
        """
        Add thinking step.
        
        Args:
            phase: Thinking phase
            description: Step description
        """
        step = ThinkingStep(phase=phase, description=description)
        self.thinking_steps.append(step)
        self.current_phase = phase
    
    def complete_thinking_step(self, result: Optional[str] = None):
        """Complete current thinking step"""
        if self.thinking_steps:
            self.thinking_steps[-1].complete(result)
    
    def add_tool_use(self, tool_name: str, input_params: Dict[str, Any]):
        """
        Add tool use.
        
        Args:
            tool_name: Name of tool
            input_params: Tool input parameters
        """
        tool = ToolUse(tool_name=tool_name, input_params=input_params)
        self.tool_uses.append(tool)
    
    def complete_tool_use(self, tool_name: str, output: Any):
        """
        Complete tool use.
        
        Args:
            tool_name: Name of tool
            output: Tool output
        """
        for tool in reversed(self.tool_uses):
            if tool.tool_name == tool_name and not tool.completed:
                tool.complete(output)
                break
    
    def fail_tool_use(self, tool_name: str, error: str):
        """Mark tool use as failed"""
        for tool in reversed(self.tool_uses):
            if tool.tool_name == tool_name and not tool.completed:
                tool.fail(error)
                break
    
    def add_output(self, text: str):
        """Add output text"""
        self.output_lines.append(text)
    
    def add_code(self, code: str, language: str = "python"):
        """Add code block"""
        self.code_blocks.append((language, code))
    
    def update_progress(self, chunk: StreamChunk):
        """Update progress from stream chunk"""
        self.progress.update_chunk(chunk)
    
    async def update(self):
        """Update display (async)"""
        if self.live:
            self._render()
            await asyncio.sleep(0.01)  # Yield control
    
    def update_sync(self):
        """Update display (sync)"""
        if self.live:
            self._render()
    
    def _render(self):
        """Render current state"""
        if not self.live:
            return
        
        # Build display components
        components = []
        
        # Header with agent name and phase
        components.append(self._render_header())
        
        # Thinking steps (if enabled)
        if self.config.show_thinking and self.thinking_steps:
            components.append(Text())  # Spacer
            components.append(self._render_thinking_steps())
        
        # Tool uses (if enabled)
        if self.config.show_tools and self.tool_uses:
            components.append(Text())
            components.append(self._render_tool_uses())
        
        # Metrics (if enabled)
        if self.config.show_metrics:
            components.append(Text())
            components.append(self._render_metrics())
        
        # Output preview
        if self.output_lines:
            components.append(Text())
            components.append(self._render_output())
        
        # Code preview
        if self.config.show_code_preview and self.code_blocks:
            components.append(Text())
            components.append(self._render_code_preview())
        
        # Wrap in panel
        group = Group(*components)
        panel = Panel(
            group,
            title=f"[bold {self.agent_color}]⚡ {self.agent_name.upper()} AGENT",
            border_style=self.agent_color,
            padding=(1, 2),
        )
        
        self.live.update(panel)
    
    def _render_header(self) -> Text:
        """Render header with phase and status"""
        # Phase emoji
        phase_emoji = {
            ThinkingPhase.INITIALIZING: "🔄",
            ThinkingPhase.ANALYZING: "🔍",
            ThinkingPhase.PLANNING: "📋",
            ThinkingPhase.EXECUTING: "⚡",
            ThinkingPhase.VALIDATING: "✓",
            ThinkingPhase.COMPLETING: "✅",
            ThinkingPhase.ERROR: "❌",
        }
        
        emoji = phase_emoji.get(self.current_phase, "●")
        
        # Build header
        header = Text()
        header.append(f"{emoji} ", style="bold")
        header.append(f"{self.current_phase.value.upper()}", style=f"bold {self.agent_color}")
        
        # Add elapsed time
        elapsed = (datetime.now() - self.start_time).total_seconds()
        header.append(f" • {elapsed:.1f}s", style="dim")
        
        return header
    
    def _render_thinking_steps(self) -> Group:
        """Render thinking steps"""
        lines = []
        lines.append(Text("💭 Thinking Process:", style="bold yellow"))
        lines.append(Text())
        
        # Show last N steps
        visible_steps = self.thinking_steps[-self.config.max_thinking_lines:]
        
        for step in visible_steps:
            # Status icon
            if step.error:
                icon = "✗"
                color = "red"
            elif step.completed:
                icon = "✓"
                color = "green"
            else:
                icon = "●"
                color = "yellow"
            
            # Format line
            line = Text()
            line.append(f"  {icon} ", style=f"{color}")
            line.append(step.description, style=f"dim {color}" if step.completed else color)
            
            # Add duration if completed
            if step.completed:
                line.append(f" ({step.duration:.1f}s)", style="dim")
            
            lines.append(line)
        
        return Group(*lines)
    
    def _render_tool_uses(self) -> Group:
        """Render tool uses"""
        lines = []
        lines.append(Text("🔧 Tool Usage:", style="bold cyan"))
        lines.append(Text())
        
        # Show last N tools
        visible_tools = self.tool_uses[-self.config.max_tool_history:]
        
        for tool in visible_tools:
            # Status
            if tool.error:
                status = "✗"
                color = "red"
            elif tool.completed:
                status = "✓"
                color = "green"
            else:
                status = Spinner("dots", style="cyan")
                color = "cyan"
            
            # Tool name
            line = Text()
            if isinstance(status, str):
                line.append(f"  {status} ", style=color)
            else:
                # Can't embed spinner in Text, use symbol
                line.append(f"  ⚙ ", style=color)
            
            line.append(f"{tool.tool_name}", style=f"bold {color}")
            
            # Parameters (abbreviated)
            if tool.input_params:
                params_str = str(tool.input_params)[:50]
                if len(str(tool.input_params)) > 50:
                    params_str += "..."
                line.append(f" {params_str}", style=f"dim {color}")
            
            # Duration if completed
            if tool.completed:
                line.append(f" ({tool.duration:.1f}s)", style="dim")
            
            lines.append(line)
        
        return Group(*lines)
    
    def _render_metrics(self) -> Table:
        """Render performance metrics"""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="dim")
        table.add_column(style="cyan")
        
        table.add_row("Tokens:", f"{self.progress.tokens_generated}")
        table.add_row("Speed:", f"{self.progress.tokens_per_second:.1f} tok/s")
        table.add_row("Chunks:", f"{self.progress.chunks_received}")
        
        return table
    
    def _render_output(self) -> Group:
        """Render output preview"""
        lines = []
        lines.append(Text("📝 Output:", style="bold green"))
        lines.append(Text())
        
        # Show last N lines
        visible_lines = self.output_lines[-self.config.max_output_lines:]
        
        for line in visible_lines:
            text = Text(f"  {line[:100]}", style="white")
            if len(line) > 100:
                text.append("...", style="dim")
            lines.append(text)
        
        return Group(*lines)
    
    def _render_code_preview(self) -> Syntax:
        """Render code preview"""
        if not self.code_blocks:
            return Text()
        
        # Show last code block
        language, code = self.code_blocks[-1]
        
        # Truncate if too long
        lines = code.split('\n')
        if len(lines) > 15:
            code = '\n'.join(lines[:15]) + "\n# ... (truncated)"
        
        return Syntax(
            code,
            language,
            theme="monokai",
            line_numbers=True,
            word_wrap=True,
        )


async def stream_with_thinking(
    stream: AsyncIterator[StreamChunk],
    agent_name: str = "assistant",
    console: Optional[Console] = None,
    on_chunk: Optional[Callable[[StreamChunk], None]] = None,
) -> str:
    """
    Stream response with enhanced thinking display.
    
    High-level convenience function that handles thinking display automatically.
    
    Args:
        stream: Async stream of chunks
        agent_name: Name of agent
        console: Rich console
        on_chunk: Optional callback for each chunk
    
    Returns:
        Complete output text
    
    Example:
        output = await stream_with_thinking(
            agent.execute_streaming("Create hello world"),
            agent_name="code",
        )
    """
    output_text = []
    
    async with EnhancedThinkingDisplay(agent_name, console) as display:
        display.add_thinking_step(ThinkingPhase.INITIALIZING, "Starting agent...")
        await display.update()
        
        async for chunk in stream:
            # Update progress
            display.update_progress(chunk)
            
            # Handle chunk
            if chunk.text:
                output_text.append(chunk.text)
                display.add_output(chunk.text)
            
            # Callback
            if on_chunk:
                on_chunk(chunk)
            
            # Update display
            await display.update()
        
        display.add_thinking_step(ThinkingPhase.COMPLETING, "Finalizing response...")
        await display.update()
    
    return "".join(output_text)


# Export
__all__ = [
    'ThinkingPhase',
    'ThinkingStep',
    'ToolUse',
    'ThinkingDisplayConfig',
    'EnhancedThinkingDisplay',
    'stream_with_thinking',
]
