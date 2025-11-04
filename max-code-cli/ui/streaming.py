"""
Max-Code CLI Streaming Output System

Beautiful real-time streaming with:
- Word-by-word streaming text
- Live log viewer with filtering
- Multi-stream progress updates
- Smooth animations without flicker
- Perfect alignment (TOC-approved! 🎯)

Usage:
    from ui.streaming import StreamingDisplay, LiveLogViewer, ProgressStream

    stream = StreamingDisplay()
    stream.stream_text(text_generator)
"""

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.layout import Layout
from typing import Generator, List, Dict, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import time
import re


class LogLevel(Enum):
    """Log level types."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class LogEntry:
    """Single log entry."""
    timestamp: datetime
    level: LogLevel
    message: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class StreamUpdate:
    """Progress stream update."""
    stream_id: str
    description: str
    current: int
    total: int
    status: str = "active"  # active/completed/failed
    metadata: Optional[Dict[str, Any]] = None


class StreamingDisplay:
    """
    Real-time streaming text display.

    Features:
    - Word-by-word streaming
    - Syntax highlighting
    - Markdown rendering
    - Smooth animations
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize streaming display."""
        self.console = console or Console()

    def stream_text(
        self,
        text_generator: Generator[str, None, None],
        prefix: str = "",
        style: str = "white",
        delay: float = 0.03
    ):
        """
        Stream text word-by-word.

        Args:
            text_generator: Generator yielding text chunks
            prefix: Optional prefix (e.g., "Agent: ")
            style: Text style
            delay: Delay between chunks (seconds)
        """
        if prefix:
            self.console.print(f"[bold {style}]{prefix}[/bold {style}]", end="")

        for chunk in text_generator:
            self.console.print(f"[{style}]{chunk}[/{style}]", end="")
            time.sleep(delay)

        self.console.print()  # Newline at end

    def stream_markdown(
        self,
        markdown_generator: Generator[str, None, None],
        title: Optional[str] = None
    ):
        """
        Stream markdown content with live rendering.

        Args:
            markdown_generator: Generator yielding markdown chunks
            title: Optional panel title
        """
        accumulated = ""

        with Live(console=self.console, refresh_per_second=10) as live:
            for chunk in markdown_generator:
                accumulated += chunk

                # Render accumulated markdown
                md = Markdown(accumulated)

                if title:
                    panel = Panel(md, title=title, border_style="cyan")
                    live.update(panel)
                else:
                    live.update(md)

                time.sleep(0.05)

    def stream_code(
        self,
        code_generator: Generator[str, None, None],
        language: str = "python",
        title: Optional[str] = None,
        theme: str = "monokai"
    ):
        """
        Stream code with syntax highlighting.

        Args:
            code_generator: Generator yielding code chunks
            language: Programming language
            title: Optional panel title
            theme: Syntax theme
        """
        accumulated = ""

        with Live(console=self.console, refresh_per_second=10) as live:
            for chunk in code_generator:
                accumulated += chunk

                # Render with syntax highlighting
                syntax = Syntax(accumulated, language, theme=theme, line_numbers=True)

                if title:
                    panel = Panel(syntax, title=title, border_style="cyan")
                    live.update(panel)
                else:
                    live.update(syntax)

                time.sleep(0.05)

    def stream_agent_response(
        self,
        agent_name: str,
        response_generator: Generator[str, None, None],
        agent_color: str = "cyan"
    ):
        """
        Stream agent response with agent branding.

        Args:
            agent_name: Name of agent
            response_generator: Generator yielding response chunks
            agent_color: Agent's brand color
        """
        # Agent header
        self.console.print(f"\n[bold {agent_color}]═══ {agent_name.upper()} ═══[/bold {agent_color}]")

        # Stream response
        accumulated = ""
        for chunk in response_generator:
            accumulated += chunk
            self.console.print(f"[{agent_color}]{chunk}[/{agent_color}]", end="")
            time.sleep(0.03)

        self.console.print()  # Newline
        self.console.print(f"[bold {agent_color}]{'═' * (len(agent_name) + 10)}[/bold {agent_color}]\n")


class LiveLogViewer:
    """
    Real-time log viewer with filtering.

    Features:
    - Auto-scroll
    - Color coding by level
    - Filtering by level/source
    - Search capability
    """

    # Log level colors
    LEVEL_COLORS = {
        LogLevel.DEBUG: "dim white",
        LogLevel.INFO: "cyan",
        LogLevel.WARNING: "yellow",
        LogLevel.ERROR: "red",
        LogLevel.CRITICAL: "bold red",
    }

    # Log level symbols
    LEVEL_SYMBOLS = {
        LogLevel.DEBUG: "⚙",
        LogLevel.INFO: "ℹ",
        LogLevel.WARNING: "⚠",
        LogLevel.ERROR: "✗",
        LogLevel.CRITICAL: "🔥",
    }

    def __init__(self, console: Optional[Console] = None):
        """Initialize log viewer."""
        self.console = console or Console()

    def view_logs(
        self,
        log_generator: Generator[LogEntry, None, None],
        title: str = "LIVE LOGS",
        max_lines: int = 20,
        filter_level: Optional[LogLevel] = None,
        filter_source: Optional[str] = None
    ):
        """
        Display logs in real-time with filtering.

        Args:
            log_generator: Generator yielding log entries
            title: Log viewer title
            max_lines: Maximum visible lines
            filter_level: Filter by log level (minimum)
            filter_source: Filter by source name
        """
        log_buffer = []

        with Live(console=self.console, refresh_per_second=4) as live:
            for log_entry in log_generator:
                # Apply filters
                if filter_level and self._should_filter_level(log_entry.level, filter_level):
                    continue

                if filter_source and log_entry.source != filter_source:
                    continue

                # Add to buffer
                log_buffer.append(log_entry)

                # Keep only max_lines
                if len(log_buffer) > max_lines:
                    log_buffer.pop(0)

                # Render logs
                live.update(self._render_logs(log_buffer, title))

    def view_logs_table(
        self,
        log_generator: Generator[LogEntry, None, None],
        title: str = "LIVE LOGS",
        max_rows: int = 15
    ):
        """
        Display logs in table format.

        Args:
            log_generator: Generator yielding log entries
            title: Table title
            max_rows: Maximum visible rows
        """
        log_buffer = []

        with Live(console=self.console, refresh_per_second=4) as live:
            for log_entry in log_generator:
                log_buffer.append(log_entry)

                # Keep only max_rows
                if len(log_buffer) > max_rows:
                    log_buffer.pop(0)

                # Render table
                live.update(self._render_log_table(log_buffer, title))

    def _render_logs(self, logs: List[LogEntry], title: str) -> Panel:
        """Render logs as panel."""
        lines = []

        for log in logs:
            # Format timestamp
            time_str = log.timestamp.strftime("%H:%M:%S")

            # Get level color and symbol
            color = self.LEVEL_COLORS[log.level]
            symbol = self.LEVEL_SYMBOLS[log.level]

            # Source (if available)
            source_str = f"[{log.source}]" if log.source else ""

            # Build line
            line = f"[dim]{time_str}[/dim] [{color}]{symbol}[/{color}] {source_str} {log.message}"
            lines.append(line)

        content = "\n".join(lines) if lines else "[dim]No logs yet...[/dim]"

        return Panel(
            content,
            title=title,
            border_style="cyan",
            padding=(1, 2),
        )

    def _render_log_table(self, logs: List[LogEntry], title: str) -> Table:
        """Render logs as table."""
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Time", style="dim", width=10)
        table.add_column("Level", style="white", width=10, justify="center")
        table.add_column("Source", style="cyan", width=12)
        table.add_column("Message", style="white", width=50)

        for log in logs:
            # Format timestamp
            time_str = log.timestamp.strftime("%H:%M:%S")

            # Level with color and symbol
            color = self.LEVEL_COLORS[log.level]
            symbol = self.LEVEL_SYMBOLS[log.level]
            level_display = f"[{color}]{symbol} {log.level.value.upper()}[/{color}]"

            # Source
            source = log.source or ""

            # Message (truncate if needed)
            message = log.message[:48] + "..." if len(log.message) > 50 else log.message

            table.add_row(time_str, level_display, source, message)

        return table

    def _should_filter_level(self, entry_level: LogLevel, min_level: LogLevel) -> bool:
        """Check if log should be filtered based on level."""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4,
        }
        return level_order[entry_level] < level_order[min_level]


class ProgressStream:
    """
    Streaming progress updates for multiple concurrent operations.

    Features:
    - Multiple concurrent streams
    - Updates without flicker
    - Percentage and ETA
    - Status indicators
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize progress stream."""
        self.console = console or Console()

    def stream_progress(
        self,
        update_generator: Generator[StreamUpdate, None, None],
        title: str = "PROGRESS"
    ):
        """
        Display multiple progress streams.

        Args:
            update_generator: Generator yielding stream updates
            title: Progress title
        """
        streams = {}  # stream_id -> StreamUpdate

        with Live(console=self.console, refresh_per_second=10) as live:
            for update in update_generator:
                # Update stream state
                streams[update.stream_id] = update

                # Render all streams
                live.update(self._render_streams(streams, title))

    def stream_progress_bars(
        self,
        update_generator: Generator[StreamUpdate, None, None],
        title: str = "PROGRESS"
    ):
        """
        Display progress with Rich progress bars.

        Args:
            update_generator: Generator yielding stream updates
            title: Progress title
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=self.console,
        )

        tasks = {}  # stream_id -> task_id

        with progress:
            for update in update_generator:
                # Create task if new
                if update.stream_id not in tasks:
                    task_id = progress.add_task(update.description, total=update.total)
                    tasks[update.stream_id] = task_id
                else:
                    task_id = tasks[update.stream_id]

                # Update progress
                progress.update(
                    task_id,
                    completed=update.current,
                    description=update.description
                )

                # Mark as complete if done
                if update.current >= update.total or update.status == "completed":
                    progress.update(task_id, completed=update.total)

    def _render_streams(self, streams: Dict[str, StreamUpdate], title: str) -> Table:
        """Render progress streams as table."""
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Stream", style="white", width=25)
        table.add_column("Progress", style="white", width=35, justify="right")
        table.add_column("Status", style="white", width=12, justify="center")

        for stream_id, update in streams.items():
            # Stream name
            stream_name = update.description

            # Progress bar
            percentage = (update.current / update.total * 100) if update.total > 0 else 0
            progress_bar = self._render_progress_bar(percentage)
            progress_display = f"{progress_bar} {update.current}/{update.total}"

            # Status
            status_color = self._get_status_color(update.status)
            status_symbol = self._get_status_symbol(update.status)
            status_display = f"[{status_color}]{status_symbol} {update.status.upper()}[/{status_color}]"

            table.add_row(stream_name, progress_display, status_display)

        return table

    def _render_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Render progress bar."""
        filled = int((percentage / 100) * width)
        empty = width - filled

        # Color based on percentage
        if percentage >= 100:
            color = "green"
        elif percentage >= 75:
            color = "cyan"
        elif percentage >= 50:
            color = "yellow"
        else:
            color = "orange3"

        bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
        return bar

    def _get_status_color(self, status: str) -> str:
        """Get color for status."""
        status_colors = {
            'active': 'cyan',
            'completed': 'green',
            'failed': 'red',
            'pending': 'yellow',
        }
        return status_colors.get(status.lower(), 'white')

    def _get_status_symbol(self, status: str) -> str:
        """Get symbol for status."""
        status_symbols = {
            'active': '●',
            'completed': '✓',
            'failed': '✗',
            'pending': '○',
        }
        return status_symbols.get(status.lower(), '○')


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("MAX-CODE CLI STREAMING OUTPUT DEMONSTRATION")
    print("=" * 80 + "\n")

    console = Console()

    # Demo 1: Streaming Text
    print("1. STREAMING TEXT:")
    stream = StreamingDisplay(console)

    def text_generator():
        text = "Max-Code CLI provides beautiful real-time streaming output with smooth animations."
        words = text.split()
        for word in words:
            yield word + " "
            time.sleep(0.1)

    stream.stream_text(text_generator(), prefix="Output: ", style="cyan")
    print()

    time.sleep(2)

    # Demo 2: Streaming Agent Response
    print("\n2. STREAMING AGENT RESPONSE:")

    def agent_response_generator():
        response = "I've analyzed your codebase and found several optimization opportunities. First, we can improve the database query performance by adding proper indexes. Second, the API response time can be reduced by implementing caching."
        words = response.split()
        for word in words:
            yield word + " "

    stream.stream_agent_response("Sophia", agent_response_generator(), agent_color="gold1")

    time.sleep(2)

    # Demo 3: Live Log Viewer
    print("\n3. LIVE LOG VIEWER:")
    log_viewer = LiveLogViewer(console)

    def log_generator():
        logs = [
            LogEntry(datetime.now(), LogLevel.INFO, "Starting analysis...", "Sophia"),
            LogEntry(datetime.now(), LogLevel.DEBUG, "Loading configuration", "System"),
            LogEntry(datetime.now(), LogLevel.INFO, "Analyzing 150 files", "Code"),
            LogEntry(datetime.now(), LogLevel.WARNING, "Deprecated API detected", "Review"),
            LogEntry(datetime.now(), LogLevel.INFO, "Tests passed: 45/50", "Test"),
            LogEntry(datetime.now(), LogLevel.ERROR, "Type error in module.py:123", "Test"),
            LogEntry(datetime.now(), LogLevel.INFO, "Generating report...", "Review"),
            LogEntry(datetime.now(), LogLevel.INFO, "Analysis complete!", "Sophia"),
        ]

        for log in logs:
            yield log
            time.sleep(0.5)

    log_viewer.view_logs_table(log_generator(), title="ANALYSIS LOGS")
    print()

    time.sleep(2)

    # Demo 4: Progress Streams
    print("\n4. MULTI-STREAM PROGRESS:")
    progress_stream = ProgressStream(console)

    def progress_generator():
        # Initialize streams
        streams = {
            'download': {'current': 0, 'total': 100},
            'process': {'current': 0, 'total': 80},
            'analyze': {'current': 0, 'total': 60},
        }

        # Simulate progress
        for i in range(100):
            # Update download
            if streams['download']['current'] < streams['download']['total']:
                streams['download']['current'] += 2
                yield StreamUpdate(
                    'download',
                    'Downloading dependencies',
                    streams['download']['current'],
                    streams['download']['total'],
                    'active' if streams['download']['current'] < streams['download']['total'] else 'completed'
                )

            # Update process (slower)
            if streams['process']['current'] < streams['process']['total'] and i % 2 == 0:
                streams['process']['current'] += 2
                yield StreamUpdate(
                    'process',
                    'Processing files',
                    streams['process']['current'],
                    streams['process']['total'],
                    'active' if streams['process']['current'] < streams['process']['total'] else 'completed'
                )

            # Update analyze (slowest)
            if streams['analyze']['current'] < streams['analyze']['total'] and i % 3 == 0:
                streams['analyze']['current'] += 2
                yield StreamUpdate(
                    'analyze',
                    'Analyzing code',
                    streams['analyze']['current'],
                    streams['analyze']['total'],
                    'active' if streams['analyze']['current'] < streams['analyze']['total'] else 'completed'
                )

            time.sleep(0.1)

    progress_stream.stream_progress(progress_generator(), title="CONCURRENT OPERATIONS")
    print()

    print("=" * 80)
    print("STREAMING OUTPUT DEMO COMPLETE - Perfect Alignment! 🎯")
    print("=" * 80 + "\n")
