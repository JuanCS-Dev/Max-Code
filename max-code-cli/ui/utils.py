"""
UI Utilities

Helper functions for UI components, color schemes, and formatting.
"""

from typing import Dict, Optional
from rich.console import Console
from rich.theme import Theme


# Color Schemes
COLOR_SCHEMES = {
    "maximus": {
        "primary": "cyan",
        "secondary": "magenta",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "blue",
        "muted": "bright_black",
        "consciousness": "magenta",
        "agent": "cyan",
        "code": "yellow",
    },
    "cyberpunk": {
        "primary": "bright_magenta",
        "secondary": "bright_cyan",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "info": "bright_blue",
        "muted": "bright_black",
        "consciousness": "bright_magenta",
        "agent": "bright_cyan",
        "code": "bright_yellow",
    },
    "matrix": {
        "primary": "green",
        "secondary": "bright_green",
        "success": "bright_green",
        "warning": "yellow",
        "error": "red",
        "info": "green",
        "muted": "bright_black",
        "consciousness": "bright_green",
        "agent": "green",
        "code": "bright_green",
    },
}


def get_theme(scheme: str = "maximus") -> Theme:
    """
    Get Rich theme for specified color scheme.

    Args:
        scheme: Color scheme name

    Returns:
        Rich Theme object
    """
    colors = COLOR_SCHEMES.get(scheme, COLOR_SCHEMES["maximus"])

    return Theme({
        "info": colors["info"],
        "warning": colors["warning"],
        "error": colors["error"],
        "success": colors["success"],
        "primary": colors["primary"],
        "secondary": colors["secondary"],
        "muted": colors["muted"],
        "consciousness": colors["consciousness"],
        "agent": colors["agent"],
        "code": colors["code"],
    })


def get_console(scheme: str = "maximus", no_color: bool = False) -> Console:
    """
    Get configured Console instance.

    Args:
        scheme: Color scheme name
        no_color: Disable colors

    Returns:
        Console instance
    """
    if no_color:
        return Console(no_color=True)

    theme = get_theme(scheme)
    return Console(theme=theme)


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human-readable string.

    Args:
        bytes_value: Number of bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_value)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """
    Format duration into human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "1m 30s")
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def truncate_text(text: str, max_length: int = 80, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def status_icon(status: str) -> str:
    """
    Get icon for status.

    Args:
        status: Status string

    Returns:
        Icon character
    """
    icons = {
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ",
        "running": "▶",
        "pending": "⏳",
        "completed": "✓",
        "failed": "✗",
    }
    return icons.get(status.lower(), "•")


def agent_icon(agent_name: str) -> str:
    """
    Get icon for agent.

    Args:
        agent_name: Agent name

    Returns:
        Icon character
    """
    icons = {
        "sophia": "🏛",
        "code": "⚙",
        "test": "🧪",
        "review": "🔍",
        "guardian": "🛡",
    }
    return icons.get(agent_name.lower(), "🤖")


def consciousness_icon(level: str) -> str:
    """
    Get icon for consciousness level.

    Args:
        level: Consciousness level

    Returns:
        Icon character
    """
    icons = {
        "inactive": "○",
        "active": "◉",
        "ignited": "⦿",
        "peak": "◉",
    }
    return icons.get(level.lower(), "○")


def print_header(console: Console, title: str, subtitle: Optional[str] = None) -> None:
    """
    Print styled header.

    Args:
        console: Rich Console instance
        title: Header title
        subtitle: Optional subtitle
    """
    console.print(f"\n[bold primary]{title}[/bold primary]")
    if subtitle:
        console.print(f"[muted]{subtitle}[/muted]")
    console.print()


def print_section(console: Console, title: str) -> None:
    """
    Print section header.

    Args:
        console: Rich Console instance
        title: Section title
    """
    console.print(f"\n[bold secondary]{title}[/bold secondary]")


def print_success(console: Console, message: str) -> None:
    """
    Print success message.

    Args:
        console: Rich Console instance
        message: Success message
    """
    console.print(f"[success]{status_icon('success')}[/success] {message}")


def print_error(console: Console, message: str) -> None:
    """
    Print error message.

    Args:
        console: Rich Console instance
        message: Error message
    """
    console.print(f"[error]{status_icon('error')}[/error] {message}")


def print_warning(console: Console, message: str) -> None:
    """
    Print warning message.

    Args:
        console: Rich Console instance
        message: Warning message
    """
    console.print(f"[warning]{status_icon('warning')}[/warning] {message}")


def print_info(console: Console, message: str) -> None:
    """
    Print info message.

    Args:
        console: Rich Console instance
        message: Info message
    """
    console.print(f"[info]{status_icon('info')}[/info] {message}")


def create_box(content: str, title: Optional[str] = None,
               border_style: str = "cyan") -> str:
    """
    Create a boxed text display.

    Args:
        content: Content to box
        title: Optional title
        border_style: Border color style

    Returns:
        Boxed text string
    """
    from rich.panel import Panel
    from rich.console import Console
    from io import StringIO

    console = Console(file=StringIO(), force_terminal=True)
    panel = Panel(content, title=title, border_style=border_style)

    with console.capture() as capture:
        console.print(panel)

    return capture.get()


def create_divider(char: str = "─", length: int = 80,
                   style: str = "muted") -> str:
    """
    Create a text divider.

    Args:
        char: Character to use
        length: Divider length
        style: Rich style

    Returns:
        Divider string
    """
    return f"[{style}]{char * length}[/{style}]"


# Export commonly used console instance
console = get_console()
