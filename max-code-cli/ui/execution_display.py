"""
Real-time Execution Display

Rich-based UI for execution progress tracking with:
- Overall progress bar
- Task status table
- Real-time updates
- Summary statistics
- ETA calculation

Biblical Foundation:
"Tudo faço com boa ordem" (1 Coríntios 14:40)

Soli Deo Gloria
"""
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.layout import Layout
from rich.console import Group
from typing import Optional, Dict
from datetime import datetime

from core.task_models import Task, EnhancedExecutionPlan


class ExecutionDisplay:
    """
    Real-time UI for execution progress
    
    Shows:
    - Overall progress
    - Current task status
    - Completed/failed counts
    - ETA
    
    Examples:
        >>> with ExecutionDisplay(plan) as display:
        ...     for task in tasks:
        ...         display.update_task_status(task, "running")
        ...         # ... execute ...
        ...         display.update_task_status(task, "completed")
    """
    
    def __init__(self, plan: EnhancedExecutionPlan, console: Optional[Console] = None):
        """
        Initialize execution display
        
        Args:
            plan: ExecutionPlan to display
            console: Rich console (optional)
        """
        self.plan = plan
        self.console = console or Console()
        
        self.start_time = datetime.now()
        self.task_statuses: Dict[str, str] = {}
        self.completed_count = 0
        self.failed_count = 0
        
        self.live = None
        self.progress = None
        self.overall_task_id = None
    
    def __enter__(self):
        """Start live display"""
        # Create progress bar
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        )
        
        # Add overall progress task
        self.overall_task_id = self.progress.add_task(
            "[cyan]Overall Progress",
            total=len(self.plan.tasks)
        )
        
        # Start live display
        self.live = Live(
            self._render(),
            console=self.console,
            refresh_per_second=4
        )
        self.live.__enter__()
        
        return self
    
    def __exit__(self, *args):
        """Stop live display"""
        if self.live:
            self.live.__exit__(*args)
    
    def update_task_status(self, task: Task, status: str):
        """
        Update task status
        
        Args:
            task: Task being updated
            status: New status ("running", "completed", "failed", "retrying")
        
        Examples:
            >>> display.update_task_status(task, "running")
            >>> display.update_task_status(task, "completed")
        """
        self.task_statuses[task.id] = status
        
        if status == "completed":
            self.completed_count += 1
            if self.progress and self.overall_task_id is not None:
                self.progress.update(self.overall_task_id, advance=1)
        
        elif status == "failed":
            self.failed_count += 1
            if self.progress and self.overall_task_id is not None:
                self.progress.update(self.overall_task_id, advance=1)
        
        # Re-render
        if self.live:
            self.live.update(self._render())
    
    def _render(self):
        """Render current state"""
        # Build display components
        components = []
        
        # Header with goal
        header = Panel(
            Text(f"🎯 {self.plan.goal}", style="bold cyan"),
            border_style="cyan"
        )
        components.append(header)
        
        # Progress bar
        if self.progress:
            components.append(self.progress)
        
        # Current tasks table
        components.append(self._render_tasks_table())
        
        # Summary
        components.append(self._render_summary())
        
        return Group(*components)
    
    def _render_tasks_table(self) -> Table:
        """Render tasks status table"""
        table = Table(
            title="Task Status",
            border_style="cyan",
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("#", width=4, style="dim")
        table.add_column("Task", style="white")
        table.add_column("Status", width=15)
        
        # Show all tasks
        for i, task in enumerate(self.plan.tasks, 1):
            status = self.task_statuses.get(task.id, "pending")
            
            # Status icon and color
            if status == "completed":
                status_text = Text("✓ Completed", style="green")
            elif status == "failed":
                status_text = Text("✗ Failed", style="red")
            elif status == "running":
                status_text = Text("⚙ Running", style="yellow")
            elif status.startswith("retrying"):
                status_text = Text(f"🔄 {status}", style="yellow")
            else:
                status_text = Text("⏸ Pending", style="dim")
            
            table.add_row(
                str(i),
                task.description[:60],
                status_text
            )
        
        return table
    
    def _render_summary(self) -> Panel:
        """Render execution summary"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
        
        total = len(self.plan.tasks)
        remaining = total - self.completed_count - self.failed_count
        
        # Calculate ETA
        if self.completed_count > 0:
            avg_time = elapsed / self.completed_count
            eta_seconds = avg_time * remaining
            eta_str = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
        else:
            eta_str = "Calculating..."
        
        summary = Text()
        summary.append("📊 Summary\n\n", style="bold white")
        summary.append(f"Completed:  {self.completed_count}/{total}\n", style="green")
        summary.append(f"Failed:     {self.failed_count}/{total}\n", style="red" if self.failed_count > 0 else "dim")
        summary.append(f"Remaining:  {remaining}/{total}\n", style="yellow")
        summary.append(f"\nElapsed:    {elapsed_str}\n")
        summary.append(f"ETA:        {eta_str}\n")
        
        return Panel(summary, border_style="cyan", padding=(1, 2))
    
    def get_stats(self) -> Dict[str, any]:
        """
        Get current statistics
        
        Returns:
            Dict with statistics
        
        Examples:
            >>> stats = display.get_stats()
            >>> print(f"Progress: {stats['progress']:.1f}%")
        """
        total = len(self.plan.tasks)
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_tasks": total,
            "completed": self.completed_count,
            "failed": self.failed_count,
            "remaining": total - self.completed_count - self.failed_count,
            "progress": (self.completed_count / total * 100) if total > 0 else 0,
            "elapsed_seconds": elapsed
        }


class SimpleDisplay:
    """
    Simple non-interactive display for testing or logging
    
    Examples:
        >>> display = SimpleDisplay(plan)
        >>> display.update_task_status(task, "running")
        [RUNNING] Task 1: Read file
        >>> display.update_task_status(task, "completed")
        [COMPLETED] Task 1: Read file
    """
    
    def __init__(self, plan: EnhancedExecutionPlan):
        """
        Initialize simple display
        
        Args:
            plan: ExecutionPlan to display
        """
        self.plan = plan
        self.start_time = datetime.now()
        self.completed_count = 0
        self.failed_count = 0
    
    def __enter__(self):
        """Start display"""
        print(f"\n🎯 Starting: {self.plan.goal}")
        print(f"📋 Total tasks: {len(self.plan.tasks)}\n")
        return self
    
    def __exit__(self, *args):
        """Stop display"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n✅ Execution completed in {elapsed:.1f}s")
        print(f"   Completed: {self.completed_count}")
        print(f"   Failed: {self.failed_count}")
    
    def update_task_status(self, task: Task, status: str):
        """
        Update task status
        
        Args:
            task: Task being updated
            status: New status
        """
        # Status icon
        if status == "completed":
            icon = "✓"
            self.completed_count += 1
        elif status == "failed":
            icon = "✗"
            self.failed_count += 1
        elif status == "running":
            icon = "⚙"
        elif status.startswith("retrying"):
            icon = "🔄"
        else:
            icon = "⏸"
        
        print(f"{icon} [{status.upper()}] {task.id}: {task.description[:60]}")
    
    def get_stats(self) -> Dict[str, any]:
        """Get current statistics"""
        total = len(self.plan.tasks)
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_tasks": total,
            "completed": self.completed_count,
            "failed": self.failed_count,
            "remaining": total - self.completed_count - self.failed_count,
            "progress": (self.completed_count / total * 100) if total > 0 else 0,
            "elapsed_seconds": elapsed
        }
