"""
Agent Spinners - Customized per Agent with Nerd Fonts

Based on research:
- Rich Spinner + Live for multiple spinners
- SpinnerColumn with custom styles
- Nerd Fonts icons from AGENT_SPINNERS (ui/constants.py)

Biblical Foundation:
"Esperei com paciência no Senhor, e ele se inclinou para mim" (Salmos 40:1)
Patience in waiting.

Research findings:
- Rich supports 70+ built-in spinners
- SpinnerColumn: custom spinner per task
- 2025 update: custom spinner frames support
- yaspin: alternative for custom frames (not needed, Rich sufficient)
"""

import logging
from typing import Optional, Dict, Any
from enum import Enum

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
from rich.text import Text

from ui.constants import AGENT_SPINNERS, NERD_ICONS

logger = logging.getLogger(__name__)


class SpinnerType(str, Enum):
    """Built-in Rich spinner types (most popular)."""
    DOTS = "dots"
    LINE = "line"
    DOTS_SCROLLING = "dots12"
    BOUNCINGBAR = "bouncingBar"
    AESTHETIC = "aesthetic"
    CLOCK = "clock"
    EARTH = "earth"
    MOON = "moon"
    RUNNER = "runner"
    PONG = "pong"


class AgentSpinner:
    """
    Single agent spinner with custom icon and style.

    Combines Rich Spinner with Nerd Fonts icon from AGENT_SPINNERS.

    Example:
        spinner = AgentSpinner(
            agent_name="Sophia",
            status="Analyzing codebase",
            icon="󰉋",
            color="gold1"
        )
        console.print(spinner.render())
    """

    def __init__(
        self,
        agent_name: str,
        status: str,
        icon: Optional[str] = None,
        color: Optional[str] = None,
        spinner_type: SpinnerType = SpinnerType.DOTS
    ):
        """
        Initialize agent spinner.

        Args:
            agent_name: Agent name (e.g., "Sophia", "Code")
            status: Current status text
            icon: Nerd Font icon (auto-detected from AGENT_SPINNERS if None)
            color: Spinner color (auto-detected from AGENT_SPINNERS if None)
            spinner_type: Spinner animation type
        """
        self.agent_name = agent_name
        self.status = status
        self.spinner_type = spinner_type

        # Auto-detect icon and color from AGENT_SPINNERS
        agent_key = agent_name.lower()
        spinner_data = AGENT_SPINNERS.get(agent_key)

        if spinner_data:
            self.icon = icon or spinner_data[0]  # Icon
            self.color = color or spinner_data[1]  # Color
        else:
            self.icon = icon or NERD_ICONS.get('agent_sophia', '🤖')
            self.color = color or "cyan"

        logger.debug(f"AgentSpinner created: {agent_name} ({self.icon})")

    def update_status(self, status: str):
        """Update status text."""
        self.status = status

    def render(self) -> Text:
        """
        Render spinner as Rich Text with icon.

        Returns:
            Rich Text with spinner, icon, agent name, and status
        """
        text = Text()

        # Icon
        text.append(f"{self.icon} ", style=f"bold {self.color}")

        # Agent name
        text.append(f"{self.agent_name}: ", style=f"bold {self.color}")

        # Status
        text.append(self.status, style="dim")

        return text


class MultiSpinnerDisplay:
    """
    Display multiple agent spinners simultaneously.

    Uses Rich Live + Table for real-time updates.

    Example:
        display = MultiSpinnerDisplay()
        display.add_agent("Sophia", "Analyzing", icon="󰉋")
        display.add_agent("Code", "Generating", icon="")

        with display.live():
            time.sleep(3)
            display.update_status("Sophia", "Analysis complete")
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        title: Optional[str] = None,
        spinner_type: SpinnerType = SpinnerType.DOTS
    ):
        """
        Initialize multi-spinner display.

        Args:
            console: Rich Console instance
            title: Optional title for display
            spinner_type: Spinner animation type for all agents
        """
        self.console = console or Console()
        self.title = title or f"{NERD_ICONS.get('agent_sophia', '🤖')} Active Agents"
        self.spinner_type = spinner_type

        self.agents: Dict[str, AgentSpinner] = {}
        self._live: Optional[Live] = None

        logger.info("MultiSpinnerDisplay initialized")

    def add_agent(
        self,
        agent_name: str,
        status: str,
        icon: Optional[str] = None,
        color: Optional[str] = None
    ):
        """
        Add agent to display.

        Args:
            agent_name: Agent name
            status: Initial status
            icon: Nerd Font icon (auto-detected if None)
            color: Spinner color (auto-detected if None)
        """
        spinner = AgentSpinner(
            agent_name=agent_name,
            status=status,
            icon=icon,
            color=color,
            spinner_type=self.spinner_type
        )

        self.agents[agent_name] = spinner
        logger.debug(f"Agent added to display: {agent_name}")

    def remove_agent(self, agent_name: str):
        """Remove agent from display."""
        self.agents.pop(agent_name, None)
        logger.debug(f"Agent removed from display: {agent_name}")

    def update_status(self, agent_name: str, status: str):
        """
        Update agent status.

        Args:
            agent_name: Agent name
            status: New status text
        """
        spinner = self.agents.get(agent_name)
        if spinner:
            spinner.update_status(status)
        else:
            logger.warning(f"Agent not found: {agent_name}")

    def _render_table(self) -> Table:
        """Render agents as Rich Table."""
        table = Table(
            title=self.title,
            show_header=False,
            box=None,
            padding=(0, 2)
        )

        # Add columns
        table.add_column("Spinner", width=3, justify="center")
        table.add_column("Agent", style="cyan")

        # Add each agent with spinner
        for agent_name, spinner in self.agents.items():
            # Create spinner
            spinner_obj = Spinner(
                self.spinner_type.value,
                style=spinner.color
            )

            # Get agent text
            agent_text = spinner.render()

            # Add row with spinner as separate column
            table.add_row(spinner_obj, agent_text)

        return table

    def live(
        self,
        refresh_per_second: int = 10,
        screen: bool = False
    ) -> Live:
        """
        Create Live context manager for real-time updates.

        Args:
            refresh_per_second: Update frequency
            screen: Use alternate screen buffer

        Returns:
            Live context manager

        Example:
            with display.live():
                time.sleep(5)
        """
        self._live = Live(
            self._render_table(),
            console=self.console,
            refresh_per_second=refresh_per_second,
            screen=screen,
            transient=False
        )

        # Auto-update table in Live
        def update():
            if self._live:
                self._live.update(self._render_table())

        # Store update function
        self._update_fn = update

        return self._live

    def refresh(self):
        """Manually refresh display (when using live context)."""
        if self._live and hasattr(self, '_update_fn'):
            self._update_fn()


# Convenience functions
def create_multi_spinner(
    console: Optional[Console] = None,
    title: Optional[str] = None,
    spinner_type: SpinnerType = SpinnerType.DOTS
) -> MultiSpinnerDisplay:
    """
    Create MultiSpinnerDisplay instance.

    Args:
        console: Rich Console instance
        title: Display title
        spinner_type: Spinner animation type

    Returns:
        MultiSpinnerDisplay instance
    """
    return MultiSpinnerDisplay(
        console=console,
        title=title,
        spinner_type=spinner_type
    )


# Demo code
if __name__ == "__main__":
    import time

    print("=" * 70)
    print("AGENT SPINNERS DEMO")
    print("=" * 70)
    print()

    # Demo 1: Single spinner
    print("1. SINGLE AGENT SPINNER:")
    print()

    spinner = AgentSpinner("Sophia", "Analyzing codebase", icon="󰉋")
    console = Console()

    for i in range(3):
        console.print(spinner.render())
        time.sleep(0.5)

    print()
    print("-" * 70)
    print()

    # Demo 2: Multiple agents with live updates
    print("2. MULTIPLE AGENT SPINNERS (Live):")
    print()

    display = create_multi_spinner(
        title=f"{NERD_ICONS.get('agent_sophia', '🤖')} Active Agents",
        spinner_type=SpinnerType.DOTS
    )

    # Add agents (icons auto-detected from AGENT_SPINNERS)
    display.add_agent("Sophia", "Initializing...")
    display.add_agent("Code", "Waiting...")
    display.add_agent("Test", "Waiting...")

    with display.live(refresh_per_second=10):
        time.sleep(1)

        # Sophia starts
        display.update_status("Sophia", "Analyzing codebase")
        display.refresh()
        time.sleep(2)

        # Code starts
        display.update_status("Code", "Generating functions")
        display.refresh()
        time.sleep(2)

        # Test starts
        display.update_status("Test", "Running tests")
        display.refresh()
        time.sleep(2)

        # Sophia completes
        display.update_status("Sophia", "✓ Analysis complete")
        display.refresh()
        time.sleep(1)

        # Code completes
        display.update_status("Code", "✓ Generation complete")
        display.refresh()
        time.sleep(1)

        # Test completes
        display.update_status("Test", "✓ All tests passed")
        display.refresh()
        time.sleep(1)

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
