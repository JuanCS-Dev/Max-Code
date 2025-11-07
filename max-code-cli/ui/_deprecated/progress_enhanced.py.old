"""
Enhanced Progress Bars - With Gradient Support

Combines Rich Progress with terminaltexteffects gradients.
Based on research: Rich BarColumn + custom gradient styling.

Biblical Foundation:
"Porque não temos aqui cidade permanente, mas buscamos a futura" (Hebreus 13:14)
Progress toward a goal.

Research findings:
- Rich BarColumn: complete_style, finished_style (solid colors)
- Textual: native gradient support (requires TUI mode)
- terminaltexteffects: gradient generation (we have this!)
- Solution: Rich structure + effects.py gradient overlay
"""

import logging
from typing import Optional, List, Callable, Any
from datetime import datetime

from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    SpinnerColumn,
    TaskID
)
from rich.table import Column
from rich.text import Text

from ui.constants import NEON_GRADIENT, NERD_ICONS, AGENT_SPINNERS

logger = logging.getLogger(__name__)


class GradientBarColumn(BarColumn):
    """
    Enhanced BarColumn with gradient color support.

    Uses color interpolation to create gradient effect.
    Based on progress percentage: 0% (red) → 50% (yellow) → 100% (green)
    """

    def __init__(
        self,
        bar_width: Optional[int] = 40,
        gradient_colors: Optional[List[str]] = None,
        **kwargs
    ):
        """
        Initialize gradient bar column.

        Args:
            bar_width: Width of progress bar
            gradient_colors: List of hex colors for gradient (default: red→yellow→green)
            **kwargs: Additional BarColumn arguments
        """
        # Default gradient: red → yellow → green (traffic light)
        self.gradient_colors = gradient_colors or ['#FF0040', '#FFD700', '#00FF00']

        super().__init__(bar_width=bar_width, **kwargs)

    def _get_color_for_progress(self, progress: float) -> str:
        """
        Get color for current progress (0.0 to 1.0).

        Interpolates between gradient colors based on progress.

        Args:
            progress: Progress value (0.0 to 1.0)

        Returns:
            Hex color string
        """
        if progress <= 0:
            return self.gradient_colors[0]
        if progress >= 1:
            return self.gradient_colors[-1]

        # Find which segment we're in
        num_segments = len(self.gradient_colors) - 1
        segment = progress * num_segments
        segment_index = int(segment)
        segment_progress = segment - segment_index

        # Ensure we don't go out of bounds
        if segment_index >= num_segments:
            return self.gradient_colors[-1]

        # Interpolate between two colors
        color1 = self.gradient_colors[segment_index]
        color2 = self.gradient_colors[segment_index + 1]

        return self._interpolate_color(color1, color2, segment_progress)

    def _interpolate_color(self, color1: str, color2: str, t: float) -> str:
        """
        Interpolate between two hex colors.

        Args:
            color1: Start color (hex)
            color2: End color (hex)
            t: Interpolation factor (0.0 to 1.0)

        Returns:
            Interpolated hex color
        """
        # Parse hex colors
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        # Interpolate
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)

        return f"#{r:02x}{g:02x}{b:02x}"

    def render(self, task):
        """Render bar with gradient color."""
        # Calculate progress
        if task.total:
            progress = task.completed / task.total
        else:
            progress = 0

        # Get color for current progress
        color = self._get_color_for_progress(progress)

        # Update complete_style with gradient color
        self.complete_style = color
        self.finished_style = color

        # Render using parent method
        return super().render(task)


class NeonProgress(Progress):
    """
    Enhanced Progress with neon gradient colors.

    Uses official NEON_GRADIENT palette.

    Example:
        progress = NeonProgress()
        task = progress.add_task("Processing", total=100)

        with progress:
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.1)
    """

    def __init__(self, *args, **kwargs):
        """Initialize neon progress with gradient bar."""
        # Use NEON_GRADIENT colors
        gradient_colors = NEON_GRADIENT  # ['#0FFF50', '#00F0FF', '#0080FF', '#FFFF00']

        # Default columns if not provided
        if not args:
            args = (
                TextColumn("[progress.description]{task.description}"),
                GradientBarColumn(gradient_colors=gradient_colors),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            )

        super().__init__(*args, **kwargs)


class AgentProgress:
    """
    Progress tracking for multiple agents.

    Each agent gets its own progress bar with custom spinner and icon.

    Example:
        progress = AgentProgress()
        progress.add_agent("Sophia", "Analyzing", icon="󰉋")
        progress.add_agent("Code", "Generating", icon="")

        with progress.live():
            progress.update_agent("Sophia", 50)
            time.sleep(2)
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize agent progress tracker.

        Args:
            console: Rich Console instance
        """
        self.console = console or Console()

        # Create progress with custom columns
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.fields[icon]}[/bold]", justify="right"),
            TextColumn("[bold cyan]{task.description}"),
            GradientBarColumn(bar_width=30),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console
        )

        self.agents: dict = {}  # agent_name -> task_id

        logger.info("AgentProgress initialized")

    def add_agent(
        self,
        name: str,
        description: str,
        total: float = 100,
        icon: Optional[str] = None
    ) -> TaskID:
        """
        Add agent to progress tracker.

        Args:
            name: Agent name
            description: Task description
            total: Total progress units
            icon: Nerd Font icon (auto-detected from AGENT_SPINNERS if None)

        Returns:
            Task ID
        """
        # Auto-detect icon from AGENT_SPINNERS
        if icon is None:
            agent_key = name.lower()
            spinner_data = AGENT_SPINNERS.get(agent_key)
            if spinner_data:
                icon = spinner_data[0]  # Get icon from tuple
            else:
                icon = NERD_ICONS.get('agent_sophia', '🤖')

        # Create task
        task_id = self.progress.add_task(
            description,
            total=total,
            icon=icon
        )

        self.agents[name] = task_id
        logger.debug(f"Agent added: {name} (icon: {icon})")

        return task_id

    def update_agent(
        self,
        name: str,
        advance: Optional[float] = None,
        completed: Optional[float] = None,
        description: Optional[str] = None
    ):
        """
        Update agent progress.

        Args:
            name: Agent name
            advance: Amount to advance (relative)
            completed: Set completed value (absolute)
            description: Update description
        """
        task_id = self.agents.get(name)
        if task_id is None:
            logger.warning(f"Agent not found: {name}")
            return

        self.progress.update(
            task_id,
            advance=advance,
            completed=completed,
            description=description
        )

    def remove_agent(self, name: str):
        """Remove agent from progress tracker."""
        task_id = self.agents.pop(name, None)
        if task_id:
            self.progress.remove_task(task_id)
            logger.debug(f"Agent removed: {name}")

    def live(self):
        """Return progress context manager for live updates."""
        return self.progress

    def stop(self):
        """Stop progress display."""
        self.progress.stop()


# Convenience functions
def create_neon_progress() -> NeonProgress:
    """Create NeonProgress instance."""
    return NeonProgress()


def create_agent_progress(console: Optional[Console] = None) -> AgentProgress:
    """Create AgentProgress instance."""
    return AgentProgress(console=console)


# Demo code
if __name__ == "__main__":
    import time

    print("=" * 70)
    print("ENHANCED PROGRESS BARS DEMO")
    print("=" * 70)
    print()

    # Demo 1: Neon gradient progress
    print("1. NEON GRADIENT PROGRESS BAR:")
    print()

    progress = create_neon_progress()
    task = progress.add_task("Processing files", total=100)

    with progress:
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)

    print()
    print("-" * 70)
    print()

    # Demo 2: Multiple agents with icons
    print("2. MULTIPLE AGENT PROGRESS:")
    print()

    agent_progress = create_agent_progress()

    agent_progress.add_agent("Sophia", "Analyzing codebase", icon="󰉋")
    agent_progress.add_agent("Code", "Generating code", icon="")
    agent_progress.add_agent("Test", "Running tests", icon="󰙨")

    with agent_progress.live():
        # Sophia completes first
        for i in range(100):
            agent_progress.update_agent("Sophia", advance=1)
            time.sleep(0.01)

        # Code and Test in parallel
        for i in range(100):
            agent_progress.update_agent("Code", advance=1)
            agent_progress.update_agent("Test", advance=0.8)
            time.sleep(0.01)

        # Test finishes
        for i in range(20):
            agent_progress.update_agent("Test", advance=1)
            time.sleep(0.01)

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
