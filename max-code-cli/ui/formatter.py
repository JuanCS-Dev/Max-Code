"""
Max-Code CLI Output Formatter

Beautiful, consistent output formatting with:
- Semantic colors (success, error, warning, info)
- Constitutional principles colors
- Agent-specific colors
- Syntax highlighting
- Tables and panels
- Markdown rendering
- Perfect alignment (TOC-friendly! 🎯)

Usage:
    from ui.formatter import MaxCodeFormatter

    fmt = MaxCodeFormatter()
    fmt.print_success("Operation completed")
    fmt.print_error("Connection failed", "Check network settings")
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Optional, Dict, List, Any
import json


class MaxCodeFormatter:
    """
    Handles all output formatting for Max-Code CLI.

    Features:
    - Semantic color coding
    - Constitutional principles coloring
    - Agent-specific styling
    - Code syntax highlighting
    - Table formatting
    - Markdown rendering
    - Perfect alignment
    """

    # Semantic colors (universal standards)
    SEMANTIC_COLORS = {
        'success': 'green',
        'error': 'red',
        'warning': 'yellow',
        'info': 'cyan',
        'debug': 'dim white',
    }

    # Semantic symbols
    SEMANTIC_SYMBOLS = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ',
        'debug': '⚙',
    }

    # Constitutional principles (P1-P6)
    CONSTITUTIONAL_COLORS = {
        'p1': 'violet',          # Transcendence
        'p2': 'blue',            # Reasoning
        'p3': 'green',           # Care
        'p4': 'yellow',          # Wisdom
        'p5': 'magenta',         # Beauty
        'p6': 'cyan',            # Autonomy
    }

    CONSTITUTIONAL_NAMES = {
        'p1': 'Transcendence',
        'p2': 'Reasoning',
        'p3': 'Care',
        'p4': 'Wisdom',
        'p5': 'Beauty',
        'p6': 'Autonomy',
    }

    # Agent colors
    AGENT_COLORS = {
        'sophia': 'gold1',       # Architect
        'code': 'blue',          # Developer
        'test': 'green',         # Validator
        'review': 'orange3',     # Auditor
        'fix': 'red',            # Debugger
        'docs': 'purple',        # Writer
        'explore': 'cyan',       # Researcher
        'guardian': 'bright_red',# Guardian System
        'sleep': 'deep_sky_blue1', # Sleep Agent
    }

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize formatter.

        Args:
            console: Rich Console instance (creates new if None)
        """
        self.console = console or Console()

    # ========================================================================
    # SEMANTIC MESSAGES (perfectly aligned)
    # ========================================================================

    def print_success(self, message: str):
        """
        Print success message with perfect alignment.

        Args:
            message: Success message to display
        """
        symbol = self.SEMANTIC_SYMBOLS['success']
        color = self.SEMANTIC_COLORS['success']
        self.console.print(f"[{color}]{symbol}[/{color}] {message}")

    def print_error(self, message: str, details: Optional[str] = None):
        """
        Print error message with optional details (aligned).

        Args:
            message: Error message
            details: Optional detailed explanation
        """
        symbol = self.SEMANTIC_SYMBOLS['error']
        color = self.SEMANTIC_COLORS['error']
        self.console.print(f"[{color}]{symbol} Error:[/{color}] {message}")

        if details:
            # Indent details for perfect alignment
            self.console.print(f"  [{color}]→[/{color}] [dim]{details}[/dim]")

    def print_warning(self, message: str):
        """
        Print warning message (aligned).

        Args:
            message: Warning message
        """
        symbol = self.SEMANTIC_SYMBOLS['warning']
        color = self.SEMANTIC_COLORS['warning']
        self.console.print(f"[{color}]{symbol} Warning:[/{color}] {message}")

    def print_info(self, message: str):
        """
        Print info message (aligned).

        Args:
            message: Info message
        """
        symbol = self.SEMANTIC_SYMBOLS['info']
        color = self.SEMANTIC_COLORS['info']
        self.console.print(f"[{color}]{symbol} Info:[/{color}] {message}")

    def print_debug(self, message: str):
        """
        Print debug message (aligned, dimmed).

        Args:
            message: Debug message
        """
        symbol = self.SEMANTIC_SYMBOLS['debug']
        color = self.SEMANTIC_COLORS['debug']
        self.console.print(f"[{color}]{symbol} Debug:[/{color}] [dim]{message}[/dim]")

    # ========================================================================
    # CODE & SYNTAX HIGHLIGHTING
    # ========================================================================

    def print_code(
        self,
        code: str,
        language: str = "python",
        line_numbers: bool = True,
        theme: str = "monokai"
    ):
        """
        Print syntax-highlighted code (perfectly formatted).

        Args:
            code: Source code to display
            language: Programming language
            line_numbers: Show line numbers
            theme: Color theme for syntax highlighting
        """
        syntax = Syntax(
            code.strip(),  # Remove leading/trailing whitespace
            language,
            theme=theme,
            line_numbers=line_numbers,
            word_wrap=False,
            indent_guides=True,  # Beautiful indent guides!
        )
        self.console.print(syntax)

    def print_markdown(self, md_text: str):
        """
        Print formatted markdown (aligned).

        Args:
            md_text: Markdown text to render
        """
        md = Markdown(md_text.strip())
        self.console.print(md)

    def print_json(self, data: Any, indent: int = 2):
        """
        Print formatted JSON (perfectly indented).

        Args:
            data: Data to serialize as JSON
            indent: Indentation level
        """
        json_text = json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)
        self.print_code(json_text, "json", line_numbers=False)

    # ========================================================================
    # TABLES (perfectly aligned columns)
    # ========================================================================

    def print_table(
        self,
        data: List[Dict],
        title: Optional[str] = None,
        columns: Optional[List[str]] = None
    ):
        """
        Print perfectly aligned table.

        Args:
            data: List of dictionaries (one per row)
            title: Optional table title
            columns: Specific columns to display (auto-detect if None)
        """
        if not data:
            self.print_warning("No data to display")
            return

        # Auto-detect columns if not provided
        if columns is None:
            columns = list(data[0].keys())

        # Create table with perfect alignment
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),  # Perfect padding
        )

        # Add columns
        for col in columns:
            table.add_column(col, style="white", no_wrap=False)

        # Add rows
        for row in data:
            table.add_row(*[str(row.get(col, "")) for col in columns])

        self.console.print(table)

    # ========================================================================
    # PANELS (beautifully bordered)
    # ========================================================================

    def print_panel(
        self,
        content: str,
        title: Optional[str] = None,
        border_style: str = "cyan",
        padding: tuple = (1, 2)
    ):
        """
        Print content in a beautiful panel (perfect borders).

        Args:
            content: Panel content
            title: Optional title
            border_style: Border color
            padding: (vertical, horizontal) padding
        """
        self.console.print(Panel(
            content.strip(),
            title=title,
            border_style=border_style,
            padding=padding,
        ))

    # ========================================================================
    # CONSTITUTIONAL PRINCIPLES (perfectly aligned)
    # ========================================================================

    def print_constitutional_status(self, principles: Dict[str, bool]):
        """
        Print constitutional principles status (perfectly aligned).

        Args:
            principles: Dict of principle status (e.g., {'p1': True, 'p2': False})
        """
        table = Table(
            title="Constitutional Principles",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 2),
        )

        table.add_column("Principle", style="cyan", width=15)
        table.add_column("Name", style="white", width=20)
        table.add_column("Status", style="white", width=10, justify="center")

        for p_key in ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']:
            color = self.CONSTITUTIONAL_COLORS[p_key]
            name = self.CONSTITUTIONAL_NAMES[p_key]
            status = principles.get(p_key, True)

            symbol = "✓" if status else "✗"
            status_text = "[green]Active[/green]" if status else "[red]Inactive[/red]"

            table.add_row(
                f"[{color}]{p_key.upper()}[/{color}]",
                name,
                f"{symbol} {status_text}"
            )

        self.console.print(table)

    # ========================================================================
    # AGENT MESSAGES (color-coded, aligned)
    # ========================================================================

    def print_agent_message(
        self,
        agent: str,
        message: str,
        action: Optional[str] = None
    ):
        """
        Print agent message with perfect alignment and color.

        Args:
            agent: Agent name (sophia, code, test, etc.)
            message: Message from agent
            action: Optional action description
        """
        agent_lower = agent.lower()
        color = self.AGENT_COLORS.get(agent_lower, 'white')

        if action:
            self.console.print(
                f"[{color}]{agent}:[/{color}] [{color}]{action}[/{color}] - {message}"
            )
        else:
            self.console.print(f"[{color}]{agent}:[/{color}] {message}")

    # ========================================================================
    # PROGRESS MESSAGES (aligned)
    # ========================================================================

    def print_step(self, step_num: int, total_steps: int, message: str):
        """
        Print step progress (perfectly aligned).

        Args:
            step_num: Current step number
            total_steps: Total number of steps
            message: Step description
        """
        self.console.print(
            f"[cyan]Step {step_num}/{total_steps}:[/cyan] {message}"
        )

    # ========================================================================
    # DIVIDERS (perfect width)
    # ========================================================================

    def print_divider(self, text: Optional[str] = None, style: str = "cyan"):
        """
        Print a divider line (perfectly centered).

        Args:
            text: Optional centered text
            style: Line color
        """
        if text:
            self.console.rule(f"[{style}]{text}[/{style}]")
        else:
            self.console.rule(style=style)

    # ========================================================================
    # SPECIAL FORMATTING
    # ========================================================================

    def print_gradient_text(self, text: str):
        """
        Print text with neon green → blue gradient.

        Args:
            text: Text to display with gradient
        """
        from rich_gradient import Gradient
        self.console.print(Gradient(text, colors=['#0FFF50', '#00F0FF', '#0080FF']))


# Convenience functions
def success(message: str, console: Optional[Console] = None):
    """Quick success message."""
    fmt = MaxCodeFormatter(console=console)
    fmt.print_success(message)


def error(message: str, details: Optional[str] = None, console: Optional[Console] = None):
    """Quick error message."""
    fmt = MaxCodeFormatter(console=console)
    fmt.print_error(message, details)


def warning(message: str, console: Optional[Console] = None):
    """Quick warning message."""
    fmt = MaxCodeFormatter(console=console)
    fmt.print_warning(message)


def info(message: str, console: Optional[Console] = None):
    """Quick info message."""
    fmt = MaxCodeFormatter(console=console)
    fmt.print_info(message)


# Demo/test code
if __name__ == "__main__":
    print("=" * 70)
    print("MAX-CODE CLI FORMATTER DEMONSTRATION")
    print("=" * 70)
    print()

    fmt = MaxCodeFormatter()

    # Test 1: Semantic messages (perfectly aligned)
    print("1. SEMANTIC MESSAGES (Perfect Alignment):")
    fmt.print_success("CLI initialized successfully")
    fmt.print_error("Connection failed", "Check your network settings")
    fmt.print_warning("Context limit approaching 90%")
    fmt.print_info("Using Claude Sonnet 4.5")
    fmt.print_debug("Debug mode enabled")
    print()

    # Test 2: Code highlighting
    print("2. CODE SYNTAX HIGHLIGHTING:")
    code = """
def hello_maxcode():
    print("Hello, Max-Code CLI!")
    return "Constitutional AI at work"
    """
    fmt.print_code(code, "python")
    print()

    # Test 3: Table (perfectly aligned columns)
    print("3. PERFECTLY ALIGNED TABLE:")
    agents_data = [
        {'Agent': 'Sophia', 'Role': 'Architect', 'Status': 'Active', 'Tasks': '3'},
        {'Agent': 'Code', 'Role': 'Developer', 'Status': 'Idle', 'Tasks': '0'},
        {'Agent': 'Test', 'Role': 'Validator', 'Status': 'Active', 'Tasks': '1'},
        {'Agent': 'Review', 'Role': 'Auditor', 'Status': 'Active', 'Tasks': '2'},
    ]
    fmt.print_table(agents_data, title="Agent Overview")
    print()

    # Test 4: Constitutional principles
    print("4. CONSTITUTIONAL PRINCIPLES STATUS:")
    principles = {
        'p1': True,
        'p2': True,
        'p3': True,
        'p4': True,
        'p5': True,
        'p6': True,
    }
    fmt.print_constitutional_status(principles)
    print()

    # Test 5: Agent messages (color-coded, aligned)
    print("5. AGENT MESSAGES (Color-Coded & Aligned):")
    fmt.print_agent_message("Sophia", "System architecture looks solid", "Analyzing")
    fmt.print_agent_message("Code", "Implementing new features", "Working")
    fmt.print_agent_message("Test", "All tests passing", "Validating")
    fmt.print_agent_message("Guardian", "No constitutional violations detected", "Monitoring")
    print()

    # Test 6: Dividers
    print("6. PERFECTLY CENTERED DIVIDERS:")
    fmt.print_divider("Section Break")
    fmt.print_divider()
    print()

    # Test 7: Gradient text
    print("7. GRADIENT TEXT (Neon Green → Blue):")
    fmt.print_gradient_text("MAX-CODE CONSTITUTIONAL AI")
    print()

    print("=" * 70)
    print("FORMATTER DEMO COMPLETE - Everything Perfectly Aligned! 🎯")
    print("=" * 70)
