"""
Rich UI Components Library - Gemini CLI Style

Complementary components for max-code-cli UI system.
Works alongside existing ui/formatter.py, ui/banner.py, ui/dashboard.py.

Biblical Foundation:
"E tudo quanto fizerdes, fazei-o de todo o coração"
(Colossenses 3:23)
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn
)
from rich.spinner import Spinner
from rich.console import Group
from rich.syntax import Syntax
from typing import List, Dict, Callable, Any, Optional
import time


# Color palette (aligned with existing ui/colors.py)
COLORS = {
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "info": "cyan",
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "blue",
    "border": "cyan",
    "header": "bold cyan",
    "subtitle": "bold white",
    "body": "white",
    "dim": "dim white",
    "prompt": "bold cyan",
}


def show_thinking_stream(activities: List[str], delay: float = 0.8):
    """
    Show thinking/processing stream with spinner (Gemini-like)
    
    Args:
        activities: List of activity descriptions
        delay: Delay between activities (seconds)
    
    Example:
        show_thinking_stream([
            "Connecting to MAXIMUS Core",
            "Fetching health metrics",
            "Processing results"
        ])
    """
    console = Console()
    
    with Live(console=console, refresh_per_second=4) as live:
        for i, activity in enumerate(activities):
            lines = []
            
            # Header
            lines.append(Text("💭 Thinking...", style="bold yellow"))
            lines.append(Text())
            
            # Completed activities
            for prev_activity in activities[:i]:
                lines.append(Text(f"  ✓ {prev_activity}", style="dim green"))
            
            # Current activity (with spinner)
            spinner_text = Text(f"  {activity}", style="cyan")
            lines.append(Spinner("dots", text=spinner_text, style="cyan"))
            
            # Pending activities
            for future_activity in activities[i+1:]:
                lines.append(Text(f"  ○ {future_activity}", style="dim white"))
            
            # Render
            group = Group(*lines)
            panel = Panel(
                group,
                border_style="yellow",
                padding=(1, 2),
                title="[bold yellow]Processing",
                title_align="left"
            )
            
            live.update(panel)
            time.sleep(delay)
    
    # Success
    console.print(Panel(
        Text("✓ Complete!", style="bold green"),
        border_style="green",
        padding=(0, 2)
    ))


def show_results_box(
    title: str,
    sections: Dict[str, Any],
    status: str = "success"
):
    """
    Show results in rich formatted box
    
    Args:
        title: Box title
        sections: Dict of {section_name: content}
        status: "success", "warning", "error"
    
    Example:
        show_results_box(
            "Health Status",
            {
                "Summary": "8/8 services healthy",
                "Details": table_object
            },
            status="success"
        )
    """
    console = Console()
    
    # Colors by status
    border_color = COLORS.get(status, "white")
    
    # Icons
    icons = {
        "success": "✓",
        "warning": "⚠",
        "error": "✗"
    }
    icon = icons.get(status, "•")
    
    # Build content
    content_parts = []
    
    for section_name, section_content in sections.items():
        # Section header
        content_parts.append(Text(f"\n{section_name}", style=f"bold {border_color}"))
        content_parts.append(Text("─" * 50, style="dim"))
        
        # Section content
        if isinstance(section_content, (Table, Panel, Group)):
            content_parts.append(section_content)
        elif isinstance(section_content, str):
            content_parts.append(Text(section_content))
        else:
            content_parts.append(Text(str(section_content)))
    
    # Render
    group = Group(*content_parts)
    panel = Panel(
        group,
        title=f"[bold {border_color}]{icon} {title}",
        border_style=border_color,
        padding=(1, 2),
        expand=True
    )
    
    console.print(panel)


def show_error(
    error_title: str,
    error_msg: str,
    suggestions: Optional[List[str]] = None,
    context: Optional[Dict] = None
):
    """
    Show error with compassionate messaging
    
    Args:
        error_title: Error title
        error_msg: Error message
        suggestions: List of suggestions to fix
        context: Additional context dict
    
    Example:
        show_error(
            "Connection Failed",
            "Could not connect to MAXIMUS Core",
            suggestions=[
                "Check if service is running: docker ps",
                "Verify URL in ~/.max-code/config.yaml"
            ],
            context={"service": "core", "url": "localhost:8153"}
        )
    """
    console = Console()
    
    # Build content
    content = []
    
    # Error message
    content.append(Text(f"❌ {error_msg}\n", style="bold red"))
    
    # Context
    if context:
        content.append(Text("\nContext:", style="bold white"))
        for key, value in context.items():
            content.append(Text(f"  • {key}: {value}", style="dim white"))
        content.append(Text())
    
    # Suggestions
    if suggestions:
        content.append(Text("\n💡 Try this:", style="bold yellow"))
        for i, suggestion in enumerate(suggestions, 1):
            content.append(Text(f"  {i}. {suggestion}", style="yellow"))
    
    # Help reference
    content.append(Text("\n" + "─" * 50, style="dim"))
    content.append(Text("Need help? Run: max-code <command> --help", style="dim cyan"))
    
    # Render
    group = Group(*content)
    panel = Panel(
        group,
        title=f"[bold red]Error: {error_title}",
        border_style="red",
        padding=(1, 2)
    )
    
    console.print(panel)


def show_progress_operation(task_name: str, steps: List[tuple[str, Callable]]):
    """
    Show progress bar for multi-step operation
    
    Args:
        task_name: Overall task name
        steps: List of (step_name, step_function) tuples
    
    Returns:
        List of results from each step
    
    Example:
        results = show_progress_operation("Analysis", [
            ("Loading data", load_func),
            ("Processing", process_func),
            ("Saving", save_func)
        ])
    """
    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        
        main_task = progress.add_task(
            f"[cyan]{task_name}",
            total=len(steps)
        )
        
        results = []
        for step_name, step_func in steps:
            # Update description
            progress.update(
                main_task,
                description=f"[cyan]{task_name}: {step_name}"
            )
            
            # Execute step
            result = step_func()
            results.append(result)
            
            # Advance
            progress.advance(main_task)
        
        return results


def stream_logs_display(log_lines: List[str], max_lines: int = 50):
    """
    Display log lines with auto-scroll (for static logs)
    
    Args:
        log_lines: List of log line strings
        max_lines: Maximum visible lines
    
    Example:
        stream_logs_display(["[INFO] Starting", "[DEBUG] Loaded"])
    """
    console = Console()
    
    # Take last N lines
    visible_lines = log_lines[-max_lines:] if len(log_lines) > max_lines else log_lines
    
    # Header
    console.print(Panel(
        f"[bold cyan]📜 Logs[/bold cyan]\n"
        f"Showing {len(visible_lines)} of {len(log_lines)} lines",
        border_style="cyan"
    ))
    console.print()
    
    # Print lines
    for line in visible_lines:
        console.print(line)


def create_table(
    title: str,
    columns: List[tuple[str, str, str]],
    rows: List[List[str]],
    **kwargs
) -> Table:
    """
    Create styled table
    
    Args:
        title: Table title
        columns: List of (name, justify, style) tuples
        rows: List of row data
        **kwargs: Additional Table() arguments
    
    Returns:
        Rich Table object
    
    Example:
        table = create_table(
            "MAXIMUS Services",
            [("Name", "left", "bold"), ("Status", "center", ""), ("Uptime", "right", "dim")],
            [["Core", "✓ OK", "2h 15m"], ["Penelope", "✓ OK", "2h 15m"]]
        )
    """
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        title=f"[bold cyan]{title}",
        **kwargs
    )
    
    # Add columns
    for col_name, justify, style in columns:
        table.add_column(col_name, justify=justify, style=style)
    
    # Add rows
    for row in rows:
        table.add_row(*row)
    
    return table


def format_json(data: dict, theme: str = "monokai") -> Syntax:
    """
    Format dict as syntax-highlighted JSON
    
    Args:
        data: Dict to format
        theme: Pygments theme
    
    Returns:
        Rich Syntax object
    """
    import json
    json_str = json.dumps(data, indent=2, sort_keys=False)
    return Syntax(json_str, "json", theme=theme, line_numbers=True)


def format_yaml(data: dict, theme: str = "monokai") -> Syntax:
    """
    Format dict as syntax-highlighted YAML
    
    Args:
        data: Dict to format
        theme: Pygments theme
    
    Returns:
        Rich Syntax object
    """
    try:
        import yaml
        yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
        return Syntax(yaml_str, "yaml", theme=theme, line_numbers=True)
    except ImportError:
        # Fallback to JSON if PyYAML not installed
        return format_json(data, theme)


def confirm_action(prompt: str, default: bool = False) -> bool:
    """
    Ask user for confirmation
    
    Args:
        prompt: Confirmation prompt
        default: Default value
    
    Returns:
        True if confirmed, False otherwise
    
    Example:
        if confirm_action("Restart all services?"):
            restart_services()
    """
    console = Console()
    
    default_str = "Y/n" if default else "y/N"
    response = console.input(f"[bold yellow]{prompt}[/bold yellow] [{default_str}] ")
    
    if not response:
        return default
    
    return response.lower() in ["y", "yes"]


def show_service_status(
    service_name: str,
    status: str,
    details: Optional[Dict[str, Any]] = None
):
    """
    Show detailed service status panel
    
    Args:
        service_name: Name of the service
        status: Status string ("healthy", "degraded", "offline")
        details: Additional details dict
    
    Example:
        show_service_status(
            "MAXIMUS Core",
            "healthy",
            {"uptime": "2h 15m", "memory": "256 MB", "cpu": "12%"}
        )
    """
    console = Console()
    
    # Status colors
    status_colors = {
        "healthy": "green",
        "degraded": "yellow",
        "offline": "red",
        "unknown": "dim white"
    }
    
    status_icons = {
        "healthy": "✓",
        "degraded": "⚠",
        "offline": "✗",
        "unknown": "?"
    }
    
    color = status_colors.get(status.lower(), "white")
    icon = status_icons.get(status.lower(), "•")
    
    # Build content
    content = []
    content.append(Text(f"{icon} {service_name}", style=f"bold {color}"))
    content.append(Text(f"Status: {status.upper()}", style=color))
    
    if details:
        content.append(Text())
        for key, value in details.items():
            content.append(Text(f"{key}: {value}", style="dim white"))
    
    # Render
    group = Group(*content)
    panel = Panel(
        group,
        border_style=color,
        padding=(1, 2)
    )
    
    console.print(panel)


# Export public API
__all__ = [
    "show_thinking_stream",
    "show_results_box",
    "show_error",
    "show_progress_operation",
    "stream_logs_display",
    "create_table",
    "format_json",
    "format_yaml",
    "confirm_action",
    "show_service_status",
    "COLORS"
]
