"""
Max-Code CLI Progress Indicators

Beautiful progress tracking with:
- Elegant spinners (yaspin)
- Progress bars (Rich Progress)
- Multi-progress for parallel operations
- Agent activity tracking
- Task status display
- Perfect alignment (TOC-approved! 🎯)

Usage:
    from ui.progress import MaxCodeProgress

    progress = MaxCodeProgress()

    # Simple spinner
    with progress.spinner("Processing..."):
        do_work()

    # Progress bar
    with progress.bar(total=100) as bar:
        for i in range(100):
            bar.advance(1)
"""

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
)
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Optional, Dict, List, Callable
from contextlib import contextmanager
import time


class MaxCodeProgress:
    """
    Handles all progress indicators for Max-Code CLI.

    Features:
    - Elegant spinners
    - Beautiful progress bars
    - Multi-progress (parallel tasks)
    - Agent activity tracking
    - Perfect alignment
    - Constitutional colors
    """

    # Spinner styles (yaspin-compatible)
    SPINNER_STYLES = {
        'default': '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏',  # Dots (elegant)
        'dots': '⣾⣽⣻⢿⡿⣟⣯⣷',          # Braille dots
        'line': '-\\|/',                   # Simple line
        'arrow': '←↖↑↗→↘↓↙',              # Rotating arrow
        'pulse': '⣾⣽⣻⢿⡿⣟⣯⣷',          # Pulsing
        'bounce': '⠁⠂⠄⡀⢀⠠⠐⠈',         # Bouncing
    }

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

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize progress handler.

        Args:
            console: Rich Console instance (creates new if None)
        """
        self.console = console or Console()
        self._current_tasks: Dict[str, any] = {}

    # ========================================================================
    # SPINNERS (elegant loading indicators)
    # ========================================================================

    @contextmanager
    def spinner(
        self,
        message: str,
        style: str = 'default',
        color: str = 'cyan'
    ):
        """
        Show elegant spinner during operation.

        Args:
            message: Message to display
            style: Spinner style (default, dots, line, arrow, pulse, bounce)
            color: Spinner color

        Usage:
            with progress.spinner("Loading..."):
                do_work()
        """
        # Create spinner text
        spinner_text = Text()
        spinner_text.append("⠋", style=color)
        spinner_text.append(f" {message}", style="white")

        # Use Rich's built-in spinner via Live
        from rich.spinner import Spinner
        spinner = Spinner("dots", text=message, style=color)

        with Live(spinner, console=self.console, refresh_per_second=10):
            try:
                yield
            finally:
                pass

        # Show completion
        self.console.print(f"[{color}]✓[/{color}] {message}")

    @contextmanager
    def agent_spinner(
        self,
        agent: str,
        message: str,
        action: str = "Working"
    ):
        """
        Show agent-specific spinner with color.

        Args:
            agent: Agent name (sophia, code, test, etc.)
            message: Task description
            action: Action verb (Working, Analyzing, Testing, etc.)

        Usage:
            with progress.agent_spinner("sophia", "Analyzing architecture"):
                analyze()
        """
        agent_lower = agent.lower()
        color = self.AGENT_COLORS.get(agent_lower, 'cyan')

        from rich.spinner import Spinner
        spinner = Spinner(
            "dots",
            text=f"[{color}]{agent}:[/{color}] [{color}]{action}[/{color}] - {message}",
            style=color
        )

        with Live(spinner, console=self.console, refresh_per_second=10):
            try:
                yield
            finally:
                pass

        # Show completion
        self.console.print(
            f"[{color}]✓[/{color}] [{color}]{agent}:[/{color}] {message}"
        )

    # ========================================================================
    # PROGRESS BARS (beautiful, aligned)
    # ========================================================================

    @contextmanager
    def bar(
        self,
        total: int,
        description: str = "Progress",
        transient: bool = False
    ):
        """
        Show beautiful progress bar.

        Args:
            total: Total number of items
            description: Task description
            transient: Remove bar when done

        Usage:
            with progress.bar(total=100, description="Processing") as bar:
                for i in range(100):
                    do_work(i)
                    bar.advance(1)
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(complete_style="cyan", finished_style="green"),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            console=self.console,
            transient=transient,
        )

        with progress:
            task = progress.add_task(description, total=total)

            class ProgressWrapper:
                def advance(self, amount: float = 1):
                    progress.advance(task, amount)

                def update(self, completed: int):
                    progress.update(task, completed=completed)

            yield ProgressWrapper()

    # ========================================================================
    # MULTI-PROGRESS (parallel operations)
    # ========================================================================

    @contextmanager
    def multi_progress(self, tasks: List[Dict[str, any]]):
        """
        Show multiple progress bars for parallel operations.

        Args:
            tasks: List of task dicts with 'name', 'total', 'color'

        Usage:
            tasks = [
                {'name': 'Download', 'total': 100, 'color': 'cyan'},
                {'name': 'Process', 'total': 50, 'color': 'green'},
            ]

            with progress.multi_progress(tasks) as bars:
                bars['Download'].advance(10)
                bars['Process'].advance(5)
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console,
        )

        with progress:
            # Create all tasks
            task_ids = {}
            for task_def in tasks:
                name = task_def['name']
                total = task_def['total']
                color = task_def.get('color', 'cyan')

                task_id = progress.add_task(
                    f"[{color}]{name}[/{color}]",
                    total=total
                )
                task_ids[name] = task_id

            # Wrapper for easy access
            class MultiProgressWrapper:
                def __init__(self, progress_obj, task_ids):
                    self.progress = progress_obj
                    self.task_ids = task_ids

                def __getitem__(self, task_name: str):
                    task_id = self.task_ids[task_name]

                    class TaskWrapper:
                        def __init__(self, progress, task_id):
                            self.progress = progress
                            self.task_id = task_id

                        def advance(self, amount: float = 1):
                            self.progress.advance(self.task_id, amount)

                        def update(self, completed: int):
                            self.progress.update(self.task_id, completed=completed)

                    return TaskWrapper(self.progress, task_id)

            yield MultiProgressWrapper(progress, task_ids)

    # ========================================================================
    # AGENT ACTIVITY TRACKING (visual timeline)
    # ========================================================================

    def show_agent_activity(
        self,
        agents: List[Dict[str, any]],
        title: str = "Agent Activity"
    ):
        """
        Show beautiful agent activity table.

        Args:
            agents: List of agent dicts with 'name', 'status', 'task', 'progress'
            title: Table title

        Example:
            agents = [
                {
                    'name': 'Sophia',
                    'status': 'active',
                    'task': 'Architecture analysis',
                    'progress': 75
                },
                {
                    'name': 'Code',
                    'status': 'idle',
                    'task': 'Waiting for specs',
                    'progress': 0
                },
            ]

            progress.show_agent_activity(agents)
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 2),
        )

        table.add_column("Agent", style="white", width=12)
        table.add_column("Status", style="white", width=10, justify="center")
        table.add_column("Task", style="white", width=35)
        table.add_column("Progress", style="white", width=15, justify="right")

        for agent_info in agents:
            name = agent_info['name']
            status = agent_info['status']
            task = agent_info['task']
            progress_val = agent_info.get('progress', 0)

            # Agent color
            agent_lower = name.lower()
            color = self.AGENT_COLORS.get(agent_lower, 'cyan')

            # Status symbol and color
            if status == 'active':
                status_text = "[green]● Active[/green]"
            elif status == 'idle':
                status_text = "[dim]○ Idle[/dim]"
            elif status == 'completed':
                status_text = "[cyan]✓ Done[/cyan]"
            else:
                status_text = "[yellow]⚠ Unknown[/yellow]"

            # Progress bar
            bar_width = 10
            filled = int((progress_val / 100) * bar_width)
            empty = bar_width - filled
            progress_bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim] {progress_val}%"

            table.add_row(
                f"[{color}]{name}[/{color}]",
                status_text,
                task,
                progress_bar
            )

        self.console.print(table)

    # ========================================================================
    # TASK STATUS DISPLAY (perfect alignment)
    # ========================================================================

    def show_task_status(
        self,
        tasks: List[Dict[str, any]],
        title: str = "Task Status"
    ):
        """
        Show beautiful task status panel.

        Args:
            tasks: List of task dicts with 'name', 'status', 'duration'
            title: Panel title

        Example:
            tasks = [
                {'name': 'Load config', 'status': 'completed', 'duration': '0.5s'},
                {'name': 'Initialize', 'status': 'completed', 'duration': '1.2s'},
                {'name': 'Process data', 'status': 'in_progress', 'duration': '...'},
                {'name': 'Generate report', 'status': 'pending', 'duration': '-'},
            ]

            progress.show_task_status(tasks)
        """
        lines = []

        for task_info in tasks:
            name = task_info['name']
            status = task_info['status']
            duration = task_info.get('duration', '-')

            # Status symbol and color
            if status == 'completed':
                symbol = "[green]✓[/green]"
            elif status == 'in_progress':
                symbol = "[cyan]⟳[/cyan]"
            elif status == 'pending':
                symbol = "[dim]○[/dim]"
            elif status == 'failed':
                symbol = "[red]✗[/red]"
            else:
                symbol = "[yellow]?[/yellow]"

            # Format line (perfectly aligned)
            lines.append(f"{symbol} {name:<30} [{duration:>8}]")

        content = "\n".join(lines)

        self.console.print(Panel(
            content,
            title=title,
            border_style="cyan",
            padding=(1, 2),
        ))

    # ========================================================================
    # STEP PROGRESS (numbered steps)
    # ========================================================================

    def show_step(
        self,
        current: int,
        total: int,
        description: str,
        status: str = "in_progress"
    ):
        """
        Show step progress indicator.

        Args:
            current: Current step number
            total: Total number of steps
            description: Step description
            status: Step status (in_progress, completed, failed)
        """
        # Status symbol
        if status == 'completed':
            symbol = "[green]✓[/green]"
        elif status == 'in_progress':
            symbol = "[cyan]⟳[/cyan]"
        elif status == 'failed':
            symbol = "[red]✗[/red]"
        else:
            symbol = "[dim]○[/dim]"

        # Progress percentage
        percent = int((current / total) * 100)

        self.console.print(
            f"{symbol} [cyan]Step {current}/{total}[/cyan] "
            f"[dim]({percent}%)[/dim] - {description}"
        )


# Convenience functions
def spinner(message: str, console: Optional[Console] = None):
    """Quick spinner context manager."""
    progress = MaxCodeProgress(console=console)
    return progress.spinner(message)


def bar(total: int, description: str = "Progress", console: Optional[Console] = None):
    """Quick progress bar context manager."""
    progress = MaxCodeProgress(console=console)
    return progress.bar(total, description)


# Demo/test code
if __name__ == "__main__":
    import time

    print("=" * 70)
    print("MAX-CODE CLI PROGRESS INDICATORS DEMONSTRATION")
    print("=" * 70)
    print()

    progress = MaxCodeProgress()

    # Test 1: Simple spinner
    print("1. SIMPLE SPINNER:")
    with progress.spinner("Loading configuration..."):
        time.sleep(2)
    print()

    # Test 2: Agent spinner
    print("2. AGENT SPINNER:")
    with progress.agent_spinner("sophia", "Analyzing architecture", "Analyzing"):
        time.sleep(2)
    print()

    # Test 3: Progress bar
    print("3. PROGRESS BAR:")
    with progress.bar(total=50, description="Processing files") as bar:
        for i in range(50):
            time.sleep(0.05)
            bar.advance(1)
    print()

    # Test 4: Multi-progress (parallel operations)
    print("4. MULTI-PROGRESS (Parallel Operations):")
    tasks = [
        {'name': 'Download', 'total': 100, 'color': 'cyan'},
        {'name': 'Process', 'total': 80, 'color': 'green'},
        {'name': 'Upload', 'total': 60, 'color': 'yellow'},
    ]

    with progress.multi_progress(tasks) as bars:
        for i in range(100):
            if i < 100:
                bars['Download'].advance(1)
            if i < 80:
                bars['Process'].advance(1)
            if i < 60:
                bars['Upload'].advance(1)
            time.sleep(0.03)
    print()

    # Test 5: Agent activity
    print("5. AGENT ACTIVITY:")
    agents = [
        {'name': 'Sophia', 'status': 'active', 'task': 'Architecture analysis', 'progress': 75},
        {'name': 'Code', 'status': 'active', 'task': 'Implementing features', 'progress': 50},
        {'name': 'Test', 'status': 'idle', 'task': 'Waiting for code', 'progress': 0},
        {'name': 'Review', 'status': 'completed', 'task': 'Code review done', 'progress': 100},
    ]
    progress.show_agent_activity(agents)
    print()

    # Test 6: Task status
    print("6. TASK STATUS:")
    tasks = [
        {'name': 'Load configuration', 'status': 'completed', 'duration': '0.5s'},
        {'name': 'Initialize system', 'status': 'completed', 'duration': '1.2s'},
        {'name': 'Process data', 'status': 'in_progress', 'duration': '...'},
        {'name': 'Generate report', 'status': 'pending', 'duration': '-'},
    ]
    progress.show_task_status(tasks)
    print()

    # Test 7: Step progress
    print("7. STEP PROGRESS:")
    progress.show_step(1, 5, "Initializing environment", "completed")
    progress.show_step(2, 5, "Loading dependencies", "completed")
    progress.show_step(3, 5, "Processing data", "in_progress")
    progress.show_step(4, 5, "Generating output", "pending")
    progress.show_step(5, 5, "Cleanup", "pending")
    print()

    print("=" * 70)
    print("PROGRESS INDICATORS DEMO COMPLETE - Everything Perfectly Aligned! 🎯")
    print("=" * 70)
