"""
Max-Code CLI Agent Display System

Beautiful agent activity visualization with:
- Real-time status dashboard
- Activity timeline
- Communication flow
- Workload distribution
- Perfect alignment (TOC-approved! 🎯)

Usage:
    from ui.agents import AgentDisplay

    display = AgentDisplay()
    display.show_dashboard(agents)
"""

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich_gradient import Gradient
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime


class AgentStatus(Enum):
    """Agent status states."""
    ACTIVE = "active"
    IDLE = "idle"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"


@dataclass
class Agent:
    """Agent information."""
    name: str
    role: str
    status: AgentStatus
    current_task: str = ""
    progress: float = 0.0  # 0-100
    time_elapsed: float = 0.0  # seconds
    cpu_usage: float = 0.0  # 0-100
    memory_usage: float = 0.0  # MB


@dataclass
class AgentEvent:
    """Agent activity event."""
    timestamp: datetime
    agent_name: str
    action: str
    duration: Optional[float] = None  # seconds


@dataclass
class AgentMessage:
    """Inter-agent communication message."""
    sender: str
    receiver: str
    message_type: str
    status: str  # sent/received/acknowledged
    timestamp: datetime


class AgentDisplay:
    """
    Comprehensive agent activity visualization.

    Features:
    - Real-time dashboard
    - Activity timeline
    - Communication flow
    - Workload distribution
    """

    # Agent colors (matching formatter)
    AGENT_COLORS = {
        'sophia': 'gold1',
        'code': 'blue',
        'test': 'green',
        'review': 'orange3',
        'fix': 'red',
        'docs': 'purple',
        'explore': 'cyan',
        'guardian': 'bright_red',
        'sleep': 'deep_sky_blue1',
    }

    # Status colors and symbols
    STATUS_CONFIG = {
        AgentStatus.ACTIVE: ('green', '●', 'Active'),
        AgentStatus.IDLE: ('dim', '○', 'Idle'),
        AgentStatus.COMPLETED: ('cyan', '✓', 'Done'),
        AgentStatus.FAILED: ('red', '✗', 'Failed'),
        AgentStatus.WAITING: ('yellow', '⟳', 'Waiting'),
    }

    def __init__(self, console: Optional[Console] = None):
        """Initialize agent display."""
        self.console = console or Console()

    # ========================================================================
    # AGENT DASHBOARD (Real-time status)
    # ========================================================================

    def show_dashboard(self, agents: List[Agent], title: str = "AGENT DASHBOARD"):
        """
        Display real-time agent dashboard.

        Args:
            agents: List of agents with current status
            title: Dashboard title

        Raises:
            EmptyDataError: If agents list is empty
            InvalidInputError: If agents list is invalid
        """
        # Validate input
        from ui.validation import validate_items
        from ui.exceptions import EmptyDataError

        try:
            validate_items(agents, min_items=1, item_name="agents")
        except EmptyDataError:
            # Show empty state instead of crashing
            self.console.print(f"\n[dim]No agents to display[/dim]\n")
            return

        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        # Add columns
        table.add_column("Agent", style="white", width=12)
        table.add_column("Status", style="white", width=12, justify="center")
        table.add_column("Task", style="white", width=35)
        table.add_column("Progress", style="white", width=20, justify="right")

        # Add agent rows
        for agent in agents:
            try:
                # Validate agent data
                if not agent.name:
                    agent.name = "Unknown"

                # Clamp progress to valid range
                progress = max(0.0, min(100.0, agent.progress))

                # Agent name with color
                agent_lower = agent.name.lower()
                color = self.AGENT_COLORS.get(agent_lower, 'white')
                agent_name = f"[{color}]{agent.name}[/{color}]"

                # Status with symbol (handle invalid status gracefully)
                if agent.status in self.STATUS_CONFIG:
                    status_color, status_symbol, status_text = self.STATUS_CONFIG[agent.status]
                else:
                    status_color, status_symbol, status_text = ('dim', '?', 'Unknown')
                status_display = f"[{status_color}]{status_symbol}[/{status_color}] {status_text}"

                # Progress bar
                progress_bar = self._render_progress_bar(
                    progress,
                    width=10,
                    color=color
                )
                progress_display = f"{progress_bar} {progress:.0f}%"

                # Task (truncate if too long, handle None)
                task = agent.current_task or ""
                task_display = task[:33] + "..." if len(task) > 35 else task

                table.add_row(
                    agent_name,
                    status_display,
                    task_display,
                    progress_display
                )

            except Exception as e:
                # Log error but continue rendering other agents
                self.console.print(f"[dim red]Warning: Failed to render agent {getattr(agent, 'name', 'unknown')}: {e}[/dim red]", style="dim")
                continue

        self.console.print(table)

    def show_dashboard_live(self, agents_generator, refresh_rate: float = 0.5):
        """
        Display live-updating agent dashboard.

        Args:
            agents_generator: Generator yielding List[Agent]
            refresh_rate: Refresh rate in seconds
        """
        with Live(self._generate_dashboard_table([]), console=self.console, refresh_per_second=1/refresh_rate) as live:
            for agents in agents_generator:
                live.update(self._generate_dashboard_table(agents))

    def _generate_dashboard_table(self, agents: List[Agent]) -> Table:
        """Generate dashboard table (for live updates)."""
        table = Table(
            title="AGENT DASHBOARD",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Agent", style="white", width=12)
        table.add_column("Status", style="white", width=12, justify="center")
        table.add_column("Task", style="white", width=35)
        table.add_column("Progress", style="white", width=20, justify="right")

        for agent in agents:
            agent_lower = agent.name.lower()
            color = self.AGENT_COLORS.get(agent_lower, 'white')
            agent_name = f"[{color}]{agent.name}[/{color}]"

            status_color, status_symbol, status_text = self.STATUS_CONFIG[agent.status]
            status_display = f"[{status_color}]{status_symbol}[/{status_color}] {status_text}"

            progress_bar = self._render_progress_bar(agent.progress, width=10, color=color)
            progress_display = f"{progress_bar} {agent.progress:.0f}%"

            task_display = agent.current_task[:33] + "..." if len(agent.current_task) > 35 else agent.current_task

            table.add_row(agent_name, status_display, task_display, progress_display)

        return table

    # ========================================================================
    # AGENT TIMELINE (Activity history)
    # ========================================================================

    def show_timeline(self, events: List[AgentEvent], title: str = "AGENT TIMELINE", max_events: int = 10):
        """
        Display agent activity timeline.

        Args:
            events: List of agent events
            title: Timeline title
            max_events: Maximum events to display
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Time", style="dim", width=10)
        table.add_column("Agent", style="white", width=12)
        table.add_column("Action", style="white", width=45)

        # Show most recent events first
        recent_events = events[-max_events:] if len(events) > max_events else events

        for event in reversed(recent_events):
            # Format timestamp
            time_str = event.timestamp.strftime("%H:%M:%S")

            # Agent name with color
            agent_lower = event.agent_name.lower()
            color = self.AGENT_COLORS.get(agent_lower, 'white')
            agent_name = f"[{color}]{event.agent_name}[/{color}]"

            # Action with duration
            if event.duration:
                action_display = f"{event.action} [dim]({event.duration:.1f}s)[/dim]"
            else:
                action_display = event.action

            table.add_row(time_str, agent_name, action_display)

        self.console.print(table)

    # ========================================================================
    # AGENT COMMUNICATION FLOW
    # ========================================================================

    def show_communication(self, messages: List[AgentMessage], title: str = "AGENT COMMUNICATION FLOW"):
        """
        Display inter-agent communication flow.

        Args:
            messages: List of agent messages
            title: Flow title
        """
        panel_content = []

        for msg in messages:
            # Sender with color
            sender_lower = msg.sender.lower()
            sender_color = self.AGENT_COLORS.get(sender_lower, 'white')
            sender = f"[{sender_color}]{msg.sender}[/{sender_color}]"

            # Receiver with color
            receiver_lower = msg.receiver.lower()
            receiver_color = self.AGENT_COLORS.get(receiver_lower, 'white')
            receiver = f"[{receiver_color}]{msg.receiver}[/{receiver_color}]"

            # Status symbol
            if msg.status == 'received':
                status = "[green]✓ Received[/green]"
            elif msg.status == 'sent':
                status = "[yellow]⟳ Processing[/yellow]"
            elif msg.status == 'acknowledged':
                status = "[cyan]✓ Acknowledged[/cyan]"
            else:
                status = "[dim]○ Pending[/dim]"

            # Build message line
            line = f"{sender} ──[{msg.message_type}]──> {receiver}  {status}"
            panel_content.append(line)

        content = "\n".join(panel_content) if panel_content else "[dim]No messages[/dim]"

        panel = Panel(
            content,
            title=title,
            border_style="cyan",
            padding=(1, 2),
        )

        self.console.print(panel)

    # ========================================================================
    # AGENT WORKLOAD DISTRIBUTION
    # ========================================================================

    def show_workload(self, agents: List[Agent], title: str = "AGENT WORKLOAD"):
        """
        Display agent workload distribution.

        Args:
            agents: List of agents
            title: Workload title
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Agent", style="white", width=12)
        table.add_column("Tasks", style="white", width=8, justify="center")
        table.add_column("CPU", style="white", width=20, justify="right")
        table.add_column("Memory", style="white", width=20, justify="right")

        for agent in agents:
            # Agent name with color
            agent_lower = agent.name.lower()
            color = self.AGENT_COLORS.get(agent_lower, 'white')
            agent_name = f"[{color}]{agent.name}[/{color}]"

            # Task count (1 if active, 0 if idle)
            task_count = "1" if agent.status == AgentStatus.ACTIVE else "0"

            # CPU usage bar
            cpu_bar = self._render_progress_bar(agent.cpu_usage, width=8, color='yellow')
            cpu_display = f"{cpu_bar} {agent.cpu_usage:.0f}%"

            # Memory usage
            memory_display = f"{agent.memory_usage:.1f} MB"

            table.add_row(agent_name, task_count, cpu_display, memory_display)

        self.console.print(table)

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _render_progress_bar(self, percentage: float, width: int = 10, color: str = 'cyan') -> str:
        """
        Render a progress bar.

        Args:
            percentage: Progress percentage (0-100)
            width: Bar width in characters
            color: Bar color

        Returns:
            Formatted progress bar string
        """
        filled = int((percentage / 100) * width)
        empty = width - filled
        bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
        return bar


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("MAX-CODE CLI AGENT DISPLAY DEMONSTRATION")
    print("=" * 80 + "\n")

    display = AgentDisplay()

    # Demo 1: Agent Dashboard
    print("1. AGENT DASHBOARD:")
    agents = [
        Agent("Sophia", "Architect", AgentStatus.ACTIVE, "Architecture analysis", 75, 15.5, 23.5, 42.3),
        Agent("Code", "Developer", AgentStatus.ACTIVE, "Implementing REST API endpoints", 50, 8.2, 18.2, 38.1),
        Agent("Test", "Validator", AgentStatus.IDLE, "Waiting for code completion", 0, 0, 2.1, 15.4),
        Agent("Review", "Auditor", AgentStatus.COMPLETED, "Code review complete", 100, 12.3, 5.2, 28.7),
        Agent("Guardian", "Security", AgentStatus.ACTIVE, "Security validation", 85, 6.8, 15.3, 32.5),
    ]
    display.show_dashboard(agents)
    print()

    time.sleep(2)

    # Demo 2: Agent Timeline
    print("2. AGENT TIMELINE:")
    events = [
        AgentEvent(datetime.now(), "Sophia", "Started architecture analysis"),
        AgentEvent(datetime.now(), "Code", "Implementing features"),
        AgentEvent(datetime.now(), "Test", "Writing unit tests"),
        AgentEvent(datetime.now(), "Sophia", "Completed analysis", 15.5),
        AgentEvent(datetime.now(), "Review", "Code review in progress"),
        AgentEvent(datetime.now(), "Guardian", "Security check initiated"),
    ]
    display.show_timeline(events)
    print()

    time.sleep(2)

    # Demo 3: Agent Communication
    print("3. AGENT COMMUNICATION FLOW:")
    messages = [
        AgentMessage("Sophia", "Code", "request", "received", datetime.now()),
        AgentMessage("Code", "Test", "update", "sent", datetime.now()),
        AgentMessage("Test", "Review", "result", "sent", datetime.now()),
        AgentMessage("Review", "Sophia", "approve", "acknowledged", datetime.now()),
    ]
    display.show_communication(messages)
    print()

    time.sleep(2)

    # Demo 4: Agent Workload
    print("4. AGENT WORKLOAD:")
    display.show_workload(agents)
    print()

    print("=" * 80)
    print("AGENT DISPLAY DEMO COMPLETE - Perfect Alignment! 🎯")
    print("=" * 80 + "\n")
