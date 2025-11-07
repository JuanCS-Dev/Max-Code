"""
Dashboard Multi-Panel - Professional CLI Layout

Inspired by k9s, lazygit, and Warp terminal.
Uses Rich Layout for responsive multi-panel display.

Biblical Foundation:
"Porque Deus não é Deus de confusão, senão de paz" (1 Coríntios 14:33)
Order and clarity in presentation.

Architecture (based on research):
┌─────────────────────────────────────────┐
│ HEADER (fixed 3 rows)                   │
├──────────────┬──────────────────────────┤
│ AGENTS       │ OUTPUT                   │
│ (ratio 1)    │ (ratio 2)                │
│              │                          │
├──────────────┴──────────────────────────┤
│ FOOTER (fixed 1 row)                    │
└─────────────────────────────────────────┘
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text

from ui.constants import NEON_PALETTE, NERD_ICONS

logger = logging.getLogger(__name__)


class DashboardPanel:
    """
    Base class for dashboard panels.

    Each panel is responsible for rendering its content.
    """

    def __init__(self, title: str):
        self.title = title
        self._content: Optional[RenderableType] = None

    def update(self, content: RenderableType):
        """Update panel content."""
        self._content = content

    def render(self) -> RenderableType:
        """Render panel as Rich renderable."""
        if self._content is None:
            return Panel(
                Text("No data", style="dim"),
                title=self.title,
                border_style="dim"
            )

        return Panel(
            self._content,
            title=self.title,
            border_style="cyan"
        )


class HeaderPanel(DashboardPanel):
    """
    Header panel - Shows banner, version, status.

    Fixed height: 3 rows
    """

    def __init__(self):
        super().__init__("MAX-CODE")

    def render(self) -> RenderableType:
        """Render header with gradient colors."""
        if self._content:
            return self._content

        # Default header
        from rich_gradient import Gradient

        header_text = Text()
        header_text.append("MAX-CODE ", style="bold")
        header_text.append("v3.0 ", style="dim")
        header_text.append(f"{NERD_ICONS.get('cpu', '⚡')} ", style="cyan")
        header_text.append("Constitutional AI Framework", style="italic")

        return Panel(
            header_text,
            border_style="cyan",
            padding=(0, 2)
        )


class AgentsPanel(DashboardPanel):
    """
    Agents panel - Shows active agents with spinners.

    Flexible height, ratio 1 (1/3 of body width)
    """

    def __init__(self):
        super().__init__(f"{NERD_ICONS.get('agent_sophia', '🤖')} Agents")
        self.agents: Dict[str, Dict[str, Any]] = {}

    def add_agent(self, name: str, status: str, progress: float = 0.0, icon: str = "●"):
        """Add or update agent."""
        self.agents[name] = {
            'status': status,
            'progress': progress,
            'icon': icon
        }

    def remove_agent(self, name: str):
        """Remove agent."""
        self.agents.pop(name, None)

    def render(self) -> RenderableType:
        """Render agents table."""
        if not self.agents:
            return Panel(
                Text("No active agents", style="dim"),
                title=self.title,
                border_style="dim"
            )

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Icon", style="cyan", width=3)
        table.add_column("Agent", style="bold")
        table.add_column("Progress", justify="right", width=8)

        for name, data in self.agents.items():
            # Progress bar visual
            progress_pct = int(data['progress'])
            bar_length = 5
            filled = int((progress_pct / 100) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)

            table.add_row(
                data['icon'],
                name,
                f"{bar} {progress_pct}%"
            )

        return Panel(
            table,
            title=self.title,
            border_style="cyan"
        )


class OutputPanel(DashboardPanel):
    """
    Output panel - Shows live command output.

    Flexible height, ratio 2 (2/3 of body width)
    """

    def __init__(self):
        super().__init__(f"{NERD_ICONS.get('file', '📄')} Output")
        self.lines: list = []
        self.max_lines: int = 20

    def add_line(self, line: str, style: str = ""):
        """Add line to output."""
        self.lines.append((line, style))

        # Keep only last max_lines
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]

    def clear(self):
        """Clear output."""
        self.lines = []

    def render(self) -> RenderableType:
        """Render output lines."""
        if not self.lines:
            return Panel(
                Text("Waiting for output...", style="dim"),
                title=self.title,
                border_style="dim"
            )

        text = Text()
        for line, style in self.lines:
            text.append(line + "\n", style=style)

        return Panel(
            text,
            title=self.title,
            border_style="cyan"
        )


class FooterPanel(DashboardPanel):
    """
    Footer panel - Shows constitutional principles status + help.

    Fixed height: 1 row
    """

    def __init__(self):
        super().__init__("")

    def render(self) -> RenderableType:
        """Render footer with P1-P6 status."""
        from ui.constants import CONSTITUTIONAL_PRINCIPLES

        status_parts = []

        # P1-P6 indicators
        for code, name, color, _ in CONSTITUTIONAL_PRINCIPLES:
            icon = NERD_ICONS.get(code.lower(), '●')
            status_parts.append(f"[{color}]{icon}[/{color}] {code}")

        # Help indicator
        status_parts.append(f"[dim]Press[/dim] [cyan]?[/cyan] [dim]for help[/dim]")

        status_line = "  ".join(status_parts)

        return Panel(
            Text.from_markup(status_line, justify="center"),
            border_style="cyan",
            padding=(0, 1)
        )


class MaxCodeDashboard:
    """
    Main dashboard controller.

    Manages layout and live updates.

    Example:
        dashboard = MaxCodeDashboard()
        dashboard.agents.add_agent("Sophia", "Analyzing", 75.0, "󰉋")
        dashboard.output.add_line("Processing file.py", "green")

        with dashboard.live():
            time.sleep(5)
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize dashboard.

        Args:
            console: Rich Console instance (creates new if None)
        """
        self.console = console or Console()

        # Create panels
        self.header = HeaderPanel()
        self.agents = AgentsPanel()
        self.output = OutputPanel()
        self.footer = FooterPanel()

        # Create layout (based on research: k9s, lazygit)
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),    # Fixed: 3 rows
            Layout(name="body"),               # Flexible
            Layout(name="footer", size=3)      # Fixed: 3 rows (P1-P6 + help)
        )

        # Split body into agents (1/3) and output (2/3)
        self.layout["body"].split_row(
            Layout(name="agents", ratio=1),
            Layout(name="output", ratio=2)
        )

        logger.info("MaxCodeDashboard initialized")

    def update_layout(self):
        """Update layout with current panel content."""
        self.layout["header"].update(self.header.render())
        self.layout["agents"].update(self.agents.render())
        self.layout["output"].update(self.output.render())
        self.layout["footer"].update(self.footer.render())

    def live(self, refresh_per_second: int = 10, screen: bool = False):
        """
        Return Live context manager for real-time updates.

        Args:
            refresh_per_second: Update frequency
            screen: Use alternate screen buffer (full-screen)

        Returns:
            Live context manager

        Example:
            with dashboard.live():
                dashboard.agents.add_agent("Code", "Working", 50.0)
                time.sleep(2)
        """
        self.update_layout()
        return Live(
            self.layout,
            console=self.console,
            refresh_per_second=refresh_per_second,
            screen=screen
        )

    def render_static(self):
        """Render dashboard once (non-live mode)."""
        self.update_layout()
        self.console.print(self.layout)


# Convenience function
def create_dashboard(console: Optional[Console] = None) -> MaxCodeDashboard:
    """
    Create dashboard instance.

    Args:
        console: Rich Console instance

    Returns:
        MaxCodeDashboard instance
    """
    return MaxCodeDashboard(console=console)


# Demo code
if __name__ == "__main__":
    import time

    print("=" * 70)
    print("MAX-CODE DASHBOARD DEMO")
    print("=" * 70)
    print()

    dashboard = create_dashboard()

    # Add some agents
    dashboard.agents.add_agent("Sophia", "Analyzing", 75.0, "󰉋")
    dashboard.agents.add_agent("Code", "Generating", 40.0, "")
    dashboard.agents.add_agent("Test", "Testing", 90.0, "󰙨")

    # Add some output
    dashboard.output.add_line("✓ Loaded configuration", "green")
    dashboard.output.add_line("→ Analyzing codebase...", "cyan")
    dashboard.output.add_line("✓ Found 15 files", "green")
    dashboard.output.add_line("→ Running tests...", "cyan")

    print("Starting live dashboard (5 seconds)...")

    with dashboard.live(refresh_per_second=10):
        time.sleep(5)

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


# Alias for simpler imports in repl_enhanced.py
Dashboard = MaxCodeDashboard
