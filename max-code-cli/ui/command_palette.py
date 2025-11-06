"""
Command Palette - Fuzzy Search for Commands

Inspired by VSCode Command Palette (Ctrl+Shift+P).
Fuzzy search with prompt_toolkit + FuzzyCompleter.

Biblical Foundation:
"Peça, e lhe será dado; busque, e encontrará" (Mateus 7:7)
Searching and finding.

Research findings:
- prompt_toolkit: FuzzyCompleter + custom Completer class
- Pattern: get_completions() yields Completion objects
- KeyBindings: @bindings.add("c-p") for Ctrl+P
- run_in_terminal(): prevent output mixing

Architecture:
1. CommandCompleter: yields Command objects with fuzzy matching
2. CommandPalette: PromptSession with FuzzyCompleter
3. Command registry: dict of {name: Command}
"""

import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal

from rich.console import Console
from rich.text import Text

from ui.constants import NERD_ICONS, NEON_PALETTE

logger = logging.getLogger(__name__)


class CommandCategory(str, Enum):
    """Command categories for organization."""
    AGENT = "agent"          # Agent operations
    FILE = "file"            # File operations
    GIT = "git"              # Git operations
    UI = "ui"                # UI operations
    SYSTEM = "system"        # System operations
    DEBUG = "debug"          # Debug operations
    HELP = "help"            # Help/docs


@dataclass
class Command:
    """
    Command definition.

    Attributes:
        name: Command name (unique identifier)
        title: Display title
        description: Command description
        category: Command category
        icon: Nerd Font icon
        handler: Callback function
        shortcut: Optional keyboard shortcut
        enabled: Whether command is currently enabled
    """
    name: str
    title: str
    description: str
    category: CommandCategory
    icon: str
    handler: Callable
    shortcut: Optional[str] = None
    enabled: bool = True

    def __post_init__(self):
        """Validate command after initialization."""
        if not callable(self.handler):
            raise ValueError(f"Command handler must be callable: {self.name}")

    def display_text(self) -> str:
        """Get display text for completion menu."""
        shortcut_text = f" [{self.shortcut}]" if self.shortcut else ""
        return f"{self.icon} {self.title}{shortcut_text} - {self.description}"

    def execute(self, *args, **kwargs):
        """Execute command handler."""
        try:
            return self.handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"Command execution failed: {self.name}", exc_info=True)
            raise


class CommandCompleter(Completer):
    """
    Custom completer for commands with fuzzy matching.

    Based on prompt_toolkit pattern:
    1. get_completions() yields Completion objects
    2. Extract user input via document.get_word_before_cursor()
    3. Match against command registry
    """

    def __init__(self, commands: Dict[str, Command]):
        """
        Initialize command completer.

        Args:
            commands: Command registry {name: Command}
        """
        self.commands = commands
        logger.debug(f"CommandCompleter initialized with {len(commands)} commands")

    def get_completions(self, document: Document, complete_event):
        """
        Yield completions based on user input.

        Args:
            document: Current document state
            complete_event: Completion event

        Yields:
            Completion objects for matching commands
        """
        word = document.text_before_cursor.lower()

        # Filter enabled commands
        enabled_commands = {
            name: cmd for name, cmd in self.commands.items()
            if cmd.enabled
        }

        # Yield all enabled commands (FuzzyCompleter will handle matching)
        for name, cmd in enabled_commands.items():
            # Create styled completion text
            display_text = cmd.display_text()

            yield Completion(
                text=name,
                start_position=-len(document.text_before_cursor),
                display=display_text,
                display_meta=f"[{cmd.category.value}]"
            )


class CommandPalette:
    """
    Command Palette with fuzzy search.

    VSCode-style command palette using prompt_toolkit.

    Example:
        palette = CommandPalette()

        # Register commands
        palette.register_command(Command(
            name="agents.list",
            title="List Agents",
            description="Show all active agents",
            category=CommandCategory.AGENT,
            icon="󰉋",
            handler=lambda: print("Listing agents...")
        ))

        # Show palette
        command = palette.show()
        if command:
            command.execute()
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        title: str = "Command Palette"
    ):
        """
        Initialize command palette.

        Args:
            console: Rich Console instance
            title: Palette title
        """
        self.console = console or Console()
        self.title = title
        self.commands: Dict[str, Command] = {}

        # Create completer
        self.completer = CommandCompleter(self.commands)
        self.fuzzy_completer = FuzzyCompleter(self.completer)

        # Create prompt session
        self.session = PromptSession(
            completer=self.fuzzy_completer,
            complete_while_typing=True,
            mouse_support=True
        )

        logger.info("CommandPalette initialized")

    def register_command(self, command: Command):
        """
        Register command in palette.

        Args:
            command: Command to register
        """
        if command.name in self.commands:
            logger.warning(f"Overwriting existing command: {command.name}")

        self.commands[command.name] = command
        logger.debug(f"Command registered: {command.name}")

    def register_commands(self, commands: List[Command]):
        """Register multiple commands."""
        for cmd in commands:
            self.register_command(cmd)

    def unregister_command(self, name: str):
        """Unregister command."""
        self.commands.pop(name, None)
        logger.debug(f"Command unregistered: {name}")

    def get_command(self, name: str) -> Optional[Command]:
        """Get command by name."""
        return self.commands.get(name)

    def list_commands(
        self,
        category: Optional[CommandCategory] = None,
        enabled_only: bool = True
    ) -> List[Command]:
        """
        List commands.

        Args:
            category: Filter by category
            enabled_only: Only enabled commands

        Returns:
            List of commands
        """
        commands = list(self.commands.values())

        if category:
            commands = [c for c in commands if c.category == category]

        if enabled_only:
            commands = [c for c in commands if c.enabled]

        return commands

    def show(self) -> Optional[Command]:
        """
        Show command palette and return selected command.

        Returns:
            Selected Command or None if cancelled
        """
        try:
            # Update completer with current commands
            self.completer.commands = self.commands

            # Show prompt
            self.console.print(
                f"\n{NERD_ICONS.get('sparkles', '✨')} {self.title}",
                style=f"bold {NEON_PALETTE['primary']}"
            )
            self.console.print("Type to search, ↓↑ to navigate, Enter to select, Ctrl+C to cancel\n")

            result = self.session.prompt(
                HTML("<b>></b> "),
                default=""
            )

            if result and result in self.commands:
                return self.commands[result]

            return None

        except KeyboardInterrupt:
            self.console.print("\nCancelled", style="dim")
            return None
        except EOFError:
            return None


class GlobalCommandRegistry:
    """
    Global registry for commands.

    Singleton pattern for centralized command management.
    """

    _instance = None
    _palette: Optional[CommandPalette] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._palette is None:
            self._palette = CommandPalette()

    @property
    def palette(self) -> CommandPalette:
        """Get command palette instance."""
        return self._palette

    def register(self, command: Command):
        """Register command globally."""
        self._palette.register_command(command)

    def execute(self, name: str, *args, **kwargs):
        """Execute command by name."""
        cmd = self._palette.get_command(name)
        if cmd:
            return cmd.execute(*args, **kwargs)
        else:
            logger.warning(f"Command not found: {name}")


# Global registry instance
_registry = GlobalCommandRegistry()


def get_palette() -> CommandPalette:
    """Get global command palette instance."""
    return _registry.palette


def register_command(command: Command):
    """Register command in global registry."""
    _registry.register(command)


def execute_command(name: str, *args, **kwargs):
    """Execute command from global registry."""
    return _registry.execute(name, *args, **kwargs)


# Demo code
if __name__ == "__main__":
    import time

    print("=" * 70)
    print("COMMAND PALETTE DEMO")
    print("=" * 70)
    print()

    # Create palette
    palette = CommandPalette(title=f"{NERD_ICONS.get('sparkles', '✨')} Command Palette")

    # Sample commands
    commands = [
        Command(
            name="agents.list",
            title="List Active Agents",
            description="Show all currently active agents",
            category=CommandCategory.AGENT,
            icon=NERD_ICONS.get('agent_sophia', '󰉋'),
            handler=lambda: print("📋 Listing agents: Sophia, Code, Test"),
            shortcut="Ctrl+A"
        ),
        Command(
            name="agents.sophia",
            title="Call Sophia",
            description="Invoke Sophia (Architect Agent)",
            category=CommandCategory.AGENT,
            icon=NERD_ICONS.get('agent_sophia', '󰉋'),
            handler=lambda: print("󰉋 Sophia: Analyzing codebase..."),
            shortcut="Ctrl+S"
        ),
        Command(
            name="git.status",
            title="Git Status",
            description="Show git repository status",
            category=CommandCategory.GIT,
            icon=NERD_ICONS.get('git', ''),
            handler=lambda: print(" Git status: 5 files modified")
        ),
        Command(
            name="git.commit",
            title="Git Commit",
            description="Create new git commit",
            category=CommandCategory.GIT,
            icon=NERD_ICONS.get('git_commit', ''),
            handler=lambda: print(" Creating commit...")
        ),
        Command(
            name="file.open",
            title="Open File",
            description="Open file in editor",
            category=CommandCategory.FILE,
            icon=NERD_ICONS.get('file', ''),
            handler=lambda: print(" Opening file...")
        ),
        Command(
            name="system.help",
            title="Show Help",
            description="Display help documentation",
            category=CommandCategory.HELP,
            icon=NERD_ICONS.get('info', ''),
            handler=lambda: print("ℹ Help: Type commands to search...")
        ),
    ]

    # Register all commands
    palette.register_commands(commands)

    print(f"Registered {len(commands)} commands")
    print()

    # Show command palette
    selected = palette.show()

    if selected:
        print()
        print(f"✓ Selected: {selected.title}")
        print(f"  Executing: {selected.name}")
        print()

        # Execute command
        selected.execute()
    else:
        print("\n✗ No command selected")

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
