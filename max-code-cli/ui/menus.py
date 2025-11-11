"""
Max-Code CLI Interactive Menus

Beautiful interactive menus with:
- Selection menus with arrow key navigation
- Configuration editors
- Command palette with fuzzy search
- Multi-select support
- Perfect alignment (TOC-approved! 🎯)

Usage:
    from ui.menus import SelectionMenu, ConfigMenu, CommandPalette

    menu = SelectionMenu()
    choice = menu.select(options, title="Select Agent")
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
import re


@dataclass
class MenuItem:
    """Menu item with label and value."""
    label: str
    value: Any
    description: Optional[str] = None
    color: str = "white"


@dataclass
class Command:
    """Command for command palette."""
    name: str
    description: str
    shortcut: Optional[str] = None
    callback: Optional[Callable] = None
    category: str = "general"


class SelectionMenu:
    """
    Interactive selection menu.

    Features:
    - Beautiful display with colors
    - Keyboard-style navigation simulation
    - Search/filter
    - Multi-select option
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize selection menu."""
        self.console = console or Console()

    def select(
        self,
        items: List[MenuItem],
        title: str = "Select Option",
        prompt_text: str = "Choose",
        allow_cancel: bool = True
    ) -> Optional[MenuItem]:
        """
        Show selection menu.

        Args:
            items: List of menu items
            title: Menu title
            prompt_text: Prompt text
            allow_cancel: Allow cancellation

        Returns:
            Selected MenuItem or None if cancelled
        """
        # Display menu
        self._display_menu(items, title)

        # Get user choice (simplified - in real implementation would use arrow keys)
        self.console.print()
        choices_text = ", ".join([f"[cyan]{i+1}[/cyan]={item.label}" for i, item in enumerate(items)])

        if allow_cancel:
            choices_text += ", [dim]0=Cancel[/dim]"

        self.console.print(f"[cyan]❯[/cyan] {prompt_text}: {choices_text}")

        while True:
            try:
                choice_input = Prompt.ask("Enter choice", console=self.console)
                choice = int(choice_input)

                if choice == 0 and allow_cancel:
                    return None

                if 1 <= choice <= len(items):
                    selected = items[choice - 1]
                    self.console.print(f"[green]✓[/green] Selected: [cyan]{selected.label}[/cyan]")
                    return selected
                else:
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
            except (ValueError, KeyboardInterrupt):
                if allow_cancel:
                    self.console.print("[yellow]Cancelled.[/yellow]")
                    return None
                else:
                    self.console.print("[red]Invalid input. Please enter a number.[/red]")

    def select_multiple(
        self,
        items: List[MenuItem],
        title: str = "Select Options",
        min_choices: int = 1,
        max_choices: Optional[int] = None
    ) -> List[MenuItem]:
        """
        Show multi-select menu.

        Args:
            items: List of menu items
            title: Menu title
            min_choices: Minimum selections required
            max_choices: Maximum selections allowed

        Returns:
            List of selected MenuItems
        """
        self._display_menu(items, title)

        self.console.print()
        self.console.print(f"[cyan]❯[/cyan] Select {min_choices}-{max_choices or 'multiple'} options")
        self.console.print("[dim]Enter numbers separated by commas (e.g., 1,3,5)[/dim]")

        while True:
            try:
                choice_input = Prompt.ask("Enter choices", console=self.console)
                choices = [int(c.strip()) for c in choice_input.split(',')]

                # Validate choices
                if len(choices) < min_choices:
                    self.console.print(f"[red]Please select at least {min_choices} options.[/red]")
                    continue

                if max_choices and len(choices) > max_choices:
                    self.console.print(f"[red]Please select at most {max_choices} options.[/red]")
                    continue

                if not all(1 <= c <= len(items) for c in choices):
                    self.console.print("[red]Invalid choice number(s).[/red]")
                    continue

                selected = [items[c - 1] for c in choices]
                self.console.print(f"[green]✓[/green] Selected: {', '.join([f'[cyan]{s.label}[/cyan]' for s in selected])}")
                return selected

            except (ValueError, KeyboardInterrupt):
                self.console.print("[yellow]Cancelled.[/yellow]")
                return []

    def _display_menu(self, items: List[MenuItem], title: str):
        """Display menu items in a table."""
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 2),
            expand=False,
        )

        table.add_column("#", style="cyan", width=5, justify="right")
        table.add_column("Option", style="white", width=30)
        table.add_column("Description", style="dim", width=40)

        for i, item in enumerate(items, 1):
            description = item.description or ""
            table.add_row(
                str(i),
                f"[{item.color}]{item.label}[/{item.color}]",
                description
            )

        self.console.print(table)


class ConfigMenu:
    """
    Interactive configuration menu.

    Features:
    - Edit configuration values inline
    - Type validation
    - Save/cancel
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize config menu."""
        self.console = console or Console()

    def edit_config(
        self,
        config: Dict[str, Any],
        title: str = "Configuration",
        descriptions: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Edit configuration interactively.

        Args:
            config: Configuration dictionary
            title: Menu title
            descriptions: Optional descriptions for each config key

        Returns:
            Updated config dict or None if cancelled
        """
        descriptions = descriptions or {}
        new_config = config.copy()

        while True:
            # Display current config
            self._display_config(new_config, title, descriptions)

            self.console.print()
            self.console.print("[cyan]❯[/cyan] Options:")
            self.console.print("  [cyan]1-N[/cyan] = Edit value")
            self.console.print("  [green]s[/green] = Save and exit")
            self.console.print("  [red]c[/red] = Cancel")

            choice = Prompt.ask("\nChoice", console=self.console).lower()

            if choice == 's':
                self.console.print("[green]✓[/green] Configuration saved!")
                return new_config
            elif choice == 'c':
                self.console.print("[yellow]Cancelled. No changes saved.[/yellow]")
                return None
            else:
                try:
                    idx = int(choice) - 1
                    keys = list(new_config.keys())
                    if 0 <= idx < len(keys):
                        key = keys[idx]
                        self._edit_value(new_config, key)
                    else:
                        self.console.print("[red]Invalid choice.[/red]")
                except ValueError:
                    self.console.print("[red]Invalid input.[/red]")

    def _display_config(self, config: Dict[str, Any], title: str, descriptions: Dict[str, str]):
        """Display configuration table."""
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 2),
            expand=False,
        )

        table.add_column("#", style="cyan", width=5, justify="right")
        table.add_column("Key", style="white", width=25)
        table.add_column("Value", style="green", width=25)
        table.add_column("Description", style="dim", width=35)

        for i, (key, value) in enumerate(config.items(), 1):
            description = descriptions.get(key, "")
            value_str = str(value)
            if len(value_str) > 23:
                value_str = value_str[:20] + "..."

            table.add_row(str(i), key, value_str, description)

        self.console.print(table)

    def _edit_value(self, config: Dict[str, Any], key: str):
        """Edit a single configuration value."""
        current_value = config[key]
        value_type = type(current_value)

        self.console.print(f"\n[cyan]Editing:[/cyan] {key}")
        self.console.print(f"[dim]Current value:[/dim] {current_value}")
        self.console.print(f"[dim]Type:[/dim] {value_type.__name__}")

        new_value = Prompt.ask("New value", default=str(current_value), console=self.console)

        # Type conversion
        try:
            if value_type == bool:
                config[key] = new_value.lower() in ('true', 'yes', '1', 'on')
            elif value_type == int:
                config[key] = int(new_value)
            elif value_type == float:
                config[key] = float(new_value)
            else:
                config[key] = new_value

            self.console.print(f"[green]✓[/green] Updated {key} = {config[key]}")
        except ValueError:
            self.console.print(f"[red]✗[/red] Invalid value for type {value_type.__name__}")


class CommandPalette:
    """
    Fuzzy-search command palette.

    Features:
    - Fuzzy search
    - Command descriptions
    - Keyboard shortcuts
    - Recent commands
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize command palette."""
        self.console = console or Console()
        self.recent_commands: List[Command] = []

    def show(
        self,
        commands: List[Command],
        title: str = "Command Palette",
        max_results: int = 10
    ) -> Optional[Command]:
        """
        Show command palette with search.

        Args:
            commands: List of available commands
            title: Palette title
            max_results: Maximum search results to display

        Returns:
            Selected Command or None if cancelled
        """
        while True:
            self.console.print()
            self.console.print(f"╔{'═' * 78}╗")
            self.console.print(f"║ [bold cyan]{title:^76}[/bold cyan] ║")
            self.console.print(f"╚{'═' * 78}╝")

            search_query = Prompt.ask(
                "\n[cyan]❯[/cyan] Search command (or 'q' to quit)",
                console=self.console
            )

            if search_query.lower() in ('q', 'quit', 'exit'):
                return None

            # Fuzzy search
            results = self._fuzzy_search(commands, search_query, max_results)

            if not results:
                self.console.print("[yellow]No commands found.[/yellow]")
                continue

            # Display results
            self._display_commands(results)

            # Select
            self.console.print()
            choice_input = Prompt.ask(
                "Enter number to execute (or Enter to search again)",
                default="",
                console=self.console
            )

            if not choice_input:
                continue

            try:
                idx = int(choice_input) - 1
                if 0 <= idx < len(results):
                    selected = results[idx]
                    self._add_to_recent(selected)
                    self.console.print(f"[green]✓[/green] Executing: [cyan]{selected.name}[/cyan]")
                    return selected
                else:
                    self.console.print("[red]Invalid choice.[/red]")
            except ValueError:
                self.console.print("[red]Invalid input.[/red]")

    def _fuzzy_search(self, commands: List[Command], query: str, max_results: int) -> List[Command]:
        """Perform fuzzy search on commands."""
        if not query:
            return commands[:max_results]

        query_lower = query.lower()
        results = []

        for cmd in commands:
            # Simple fuzzy match: check if all query chars appear in order
            name_lower = cmd.name.lower()
            desc_lower = cmd.description.lower()

            # Exact match in name (highest priority)
            if query_lower in name_lower:
                results.append((3, cmd))
            # Exact match in description
            elif query_lower in desc_lower:
                results.append((2, cmd))
            # Fuzzy match
            elif self._fuzzy_match(query_lower, name_lower):
                results.append((1, cmd))

        # Sort by priority (score) and return top results
        results.sort(key=lambda x: -x[0])
        return [cmd for _, cmd in results[:max_results]]

    def _fuzzy_match(self, query: str, text: str) -> bool:
        """Check if query characters appear in text in order."""
        query_idx = 0
        for char in text:
            if query_idx < len(query) and char == query[query_idx]:
                query_idx += 1
        return query_idx == len(query)

    def _display_commands(self, commands: List[Command]):
        """Display command results."""
        table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 2),
            expand=False,
        )

        table.add_column("#", style="cyan", width=5, justify="right")
        table.add_column("Command", style="white", width=25)
        table.add_column("Description", style="dim", width=40)
        table.add_column("Shortcut", style="yellow", width=10)

        for i, cmd in enumerate(commands, 1):
            shortcut = cmd.shortcut or ""
            table.add_row(
                str(i),
                f"[cyan]{cmd.name}[/cyan]",
                cmd.description,
                shortcut
            )

        self.console.print(table)

    def _add_to_recent(self, command: Command):
        """Add command to recent history."""
        if command in self.recent_commands:
            self.recent_commands.remove(command)
        self.recent_commands.insert(0, command)
        self.recent_commands = self.recent_commands[:5]  # Keep last 5


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("MAX-CODE CLI INTERACTIVE MENUS DEMONSTRATION")
    print("=" * 80 + "\n")

    console = Console()

    # Demo 1: Selection Menu
    print("1. SELECTION MENU:")
    selection_menu = SelectionMenu(console)

    agents = [
        MenuItem("Sophia", "sophia", "Architecture and planning", "gold1"),
        MenuItem("Code", "code", "Code generation and implementation", "blue"),
        MenuItem("Test", "test", "Testing and validation", "green"),
        MenuItem("Review", "review", "Code review and quality", "orange3"),
        MenuItem("Guardian", "guardian", "Security and compliance", "bright_red"),
    ]

    selected = selection_menu.select(agents, title="Select Agent", prompt_text="Choose agent")
    if selected:
        console.print(f"\n[green]You selected:[/green] {selected.label} ({selected.value})\n")

    # Demo 2: Multi-Select Menu
    print("\n2. MULTI-SELECT MENU:")
    features = [
        MenuItem("Constitutional AI", "constitutional", "P1-P6 principles"),
        MenuItem("Multi-Agent System", "agents", "Sophia, Code, Test, Review"),
        MenuItem("Tree of Thoughts", "tot", "Advanced reasoning"),
        MenuItem("NLP Shell", "nlp", "Natural language processing"),
    ]

    selected_features = selection_menu.select_multiple(
        features,
        title="Select Features to Enable",
        min_choices=1,
        max_choices=3
    )
    if selected_features:
        console.print(f"\n[green]Selected features:[/green] {', '.join([f.label for f in selected_features])}\n")

    # Demo 3: Config Menu
    print("\n3. CONFIGURATION MENU:")
    config_menu = ConfigMenu(console)

    config = {
        "model": "claude-3-5-haiku-20241022",
        "temperature": 0.7,
        "max_tokens": 4096,
        "debug_mode": False,
    }

    descriptions = {
        "model": "AI model to use",
        "temperature": "Sampling temperature (0-1)",
        "max_tokens": "Maximum tokens per response",
        "debug_mode": "Enable debug logging",
    }

    new_config = config_menu.edit_config(config, title="Max-Code Configuration", descriptions=descriptions)
    if new_config:
        console.print(f"\n[green]Updated configuration:[/green]")
        for key, value in new_config.items():
            console.print(f"  {key}: {value}")

    # Demo 4: Command Palette
    print("\n4. COMMAND PALETTE:")
    palette = CommandPalette(console)

    commands = [
        Command("analyze", "Analyze code with Constitutional AI", "Ctrl+A", category="analysis"),
        Command("generate", "Generate code with multi-agents", "Ctrl+G", category="generation"),
        Command("test", "Run tests with EPL integration", "Ctrl+T", category="testing"),
        Command("review", "Review code against principles", "Ctrl+R", category="review"),
        Command("config", "Edit configuration", "Ctrl+,", category="settings"),
        Command("help", "Show help documentation", "F1", category="help"),
    ]

    selected_cmd = palette.show(commands, title="Command Palette")
    if selected_cmd:
        console.print(f"\n[green]Would execute:[/green] {selected_cmd.name}")
        if selected_cmd.callback:
            selected_cmd.callback()

    print("\n" + "=" * 80)
    print("INTERACTIVE MENUS DEMO COMPLETE - Perfect Alignment! 🎯")
    print("=" * 80 + "\n")
