"""
Keyboard Shortcuts System

Global keybindings for max-code CLI.
Based on prompt_toolkit KeyBindings.

Biblical Foundation:
"Tudo tem o seu tempo determinado" (Eclesiastes 3:1)
Efficiency through shortcuts.

Research findings:
- prompt_toolkit KeyBindings: @bindings.add("c-p") for Ctrl+P
- run_in_terminal(): execute without mixing prompt output
- Filter instances: conditional activation
- Event.app: access to application state

Architecture:
1. KeyBinding registry with categories
2. Global shortcuts (Ctrl+P, Ctrl+K, Ctrl+Q, etc.)
3. Conditional activation via filters
4. Help display with all shortcuts
"""

import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.filters import Condition

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ui.constants import NERD_ICONS, NEON_PALETTE

logger = logging.getLogger(__name__)


class ShortcutCategory(str, Enum):
    """Shortcut categories."""
    GLOBAL = "global"        # Global shortcuts (always available)
    NAVIGATION = "navigation"  # Navigation
    EDIT = "edit"            # Editing
    AGENT = "agent"          # Agent operations
    GIT = "git"              # Git operations
    UI = "ui"                # UI operations
    DEBUG = "debug"          # Debug operations


@dataclass
class KeyShortcut:
    """
    Keyboard shortcut definition.

    Attributes:
        key: Key combination (e.g., "c-p", "c-s-k")
        description: Shortcut description
        category: Shortcut category
        handler: Callback function
        filter_fn: Optional condition for activation
        enabled: Whether shortcut is currently enabled
    """
    key: str
    description: str
    category: ShortcutCategory
    handler: Callable
    filter_fn: Optional[Callable[[], bool]] = None
    enabled: bool = True

    def __post_init__(self):
        """Validate shortcut after initialization."""
        if not callable(self.handler):
            raise ValueError(f"Shortcut handler must be callable: {self.key}")

    def display_key(self) -> str:
        """Format key for display."""
        # Convert prompt_toolkit format to readable format
        key = self.key.replace("c-", "Ctrl+").replace("s-", "Shift+").replace("m-", "Alt+")
        return key.upper()


class KeybindingsManager:
    """
    Keyboard shortcuts manager.

    Manages global keybindings using prompt_toolkit.

    Example:
        manager = KeybindingsManager()

        # Register shortcut
        manager.register_shortcut(KeyShortcut(
            key="c-p",
            description="Open command palette",
            category=ShortcutCategory.GLOBAL,
            handler=lambda event: print("Opening palette...")
        ))

        # Get bindings for prompt
        bindings = manager.get_bindings()
        session = PromptSession(key_bindings=bindings)
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize keybindings manager.

        Args:
            console: Rich Console instance
        """
        self.console = console or Console()
        self.shortcuts: Dict[str, KeyShortcut] = {}
        self._bindings: Optional[KeyBindings] = None

        logger.info("KeybindingsManager initialized")

    def register_shortcut(self, shortcut: KeyShortcut):
        """
        Register keyboard shortcut.

        Args:
            shortcut: KeyShortcut to register
        """
        if shortcut.key in self.shortcuts:
            logger.warning(f"Overwriting existing shortcut: {shortcut.key}")

        self.shortcuts[shortcut.key] = shortcut
        self._bindings = None  # Invalidate cached bindings
        logger.debug(f"Shortcut registered: {shortcut.key}")

    def register_shortcuts(self, shortcuts: List[KeyShortcut]):
        """Register multiple shortcuts."""
        for shortcut in shortcuts:
            self.register_shortcut(shortcut)

    def unregister_shortcut(self, key: str):
        """Unregister shortcut."""
        self.shortcuts.pop(key, None)
        self._bindings = None
        logger.debug(f"Shortcut unregistered: {key}")

    def get_shortcut(self, key: str) -> Optional[KeyShortcut]:
        """Get shortcut by key."""
        return self.shortcuts.get(key)

    def list_shortcuts(
        self,
        category: Optional[ShortcutCategory] = None,
        enabled_only: bool = True
    ) -> List[KeyShortcut]:
        """
        List shortcuts.

        Args:
            category: Filter by category
            enabled_only: Only enabled shortcuts

        Returns:
            List of shortcuts
        """
        shortcuts = list(self.shortcuts.values())

        if category:
            shortcuts = [s for s in shortcuts if s.category == category]

        if enabled_only:
            shortcuts = [s for s in shortcuts if s.enabled]

        return shortcuts

    def get_bindings(self) -> KeyBindings:
        """
        Get prompt_toolkit KeyBindings.

        Returns:
            KeyBindings instance with all registered shortcuts
        """
        if self._bindings is not None:
            return self._bindings

        bindings = KeyBindings()

        for key, shortcut in self.shortcuts.items():
            if not shortcut.enabled:
                continue

            # Create filter if provided
            filter_condition = None
            if shortcut.filter_fn:
                filter_condition = Condition(shortcut.filter_fn)

            # Register binding
            @bindings.add(key, filter=filter_condition)
            def _handler(event, s=shortcut):
                """Execute shortcut handler."""
                try:
                    # Use run_in_terminal to prevent output mixing
                    def execute():
                        s.handler(event)

                    run_in_terminal(execute)
                except Exception as e:
                    logger.error(f"Shortcut execution failed: {s.key}", exc_info=True)

        self._bindings = bindings
        logger.debug(f"Built KeyBindings with {len(self.shortcuts)} shortcuts")
        return bindings

    def show_help(self):
        """Display shortcuts help."""
        # Group by category
        by_category: Dict[ShortcutCategory, List[KeyShortcut]] = {}
        for shortcut in self.list_shortcuts(enabled_only=True):
            if shortcut.category not in by_category:
                by_category[shortcut.category] = []
            by_category[shortcut.category].append(shortcut)

        # Create help table
        table = Table(
            title=f"{NERD_ICONS.get('key', '')} Keyboard Shortcuts",
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Key", style="yellow", width=15)
        table.add_column("Description", style="white")
        table.add_column("Category", style="dim", width=12)

        # Add rows by category
        for category in ShortcutCategory:
            if category not in by_category:
                continue

            shortcuts = by_category[category]
            for shortcut in sorted(shortcuts, key=lambda s: s.key):
                table.add_row(
                    shortcut.display_key(),
                    shortcut.description,
                    category.value
                )

        # Display
        panel = Panel(
            table,
            border_style=NEON_PALETTE['primary'],
            padding=(1, 2)
        )

        self.console.print(panel)


class GlobalShortcuts:
    """
    Global shortcuts registry.

    Singleton pattern for centralized shortcut management.
    """

    _instance = None
    _manager: Optional[KeybindingsManager] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._manager is None:
            self._manager = KeybindingsManager()

    @property
    def manager(self) -> KeybindingsManager:
        """Get keybindings manager instance."""
        return self._manager

    def register(self, shortcut: KeyShortcut):
        """Register shortcut globally."""
        self._manager.register_shortcut(shortcut)

    def get_bindings(self) -> KeyBindings:
        """Get global keybindings."""
        return self._manager.get_bindings()


# Global shortcuts instance
_shortcuts = GlobalShortcuts()


def get_manager() -> KeybindingsManager:
    """Get global keybindings manager."""
    return _shortcuts.manager


def register_shortcut(shortcut: KeyShortcut):
    """Register shortcut in global registry."""
    _shortcuts.register(shortcut)


def get_bindings() -> KeyBindings:
    """Get global keybindings."""
    return _shortcuts.get_bindings()


def show_shortcuts_help():
    """Show global shortcuts help."""
    _shortcuts.manager.show_help()


# ============================================================================
# DEFAULT SHORTCUTS
# ============================================================================

def register_default_shortcuts(
    on_palette: Optional[Callable] = None,
    on_shortcuts: Optional[Callable] = None,
    on_quit: Optional[Callable] = None,
    on_help: Optional[Callable] = None
):
    """
    Register default shortcuts.

    Args:
        on_palette: Command palette handler (Ctrl+P)
        on_shortcuts: Shortcuts help handler (Ctrl+K)
        on_quit: Quit handler (Ctrl+Q)
        on_help: Help handler (Ctrl+H)
    """
    manager = get_manager()

    shortcuts = []

    # Ctrl+P - Command Palette
    if on_palette:
        shortcuts.append(KeyShortcut(
            key="c-p",
            description="Open Command Palette",
            category=ShortcutCategory.GLOBAL,
            handler=on_palette
        ))

    # Ctrl+K - Keyboard Shortcuts
    if on_shortcuts:
        shortcuts.append(KeyShortcut(
            key="c-k",
            description="Show Keyboard Shortcuts",
            category=ShortcutCategory.GLOBAL,
            handler=on_shortcuts
        ))

    # Ctrl+Q - Quit
    if on_quit:
        shortcuts.append(KeyShortcut(
            key="c-q",
            description="Quit Application",
            category=ShortcutCategory.GLOBAL,
            handler=on_quit
        ))

    # Ctrl+H - Help
    if on_help:
        shortcuts.append(KeyShortcut(
            key="c-h",
            description="Show Help",
            category=ShortcutCategory.GLOBAL,
            handler=on_help
        ))

    # Ctrl+D - EOF (built-in, just document)
    shortcuts.append(KeyShortcut(
        key="c-d",
        description="Exit (EOF)",
        category=ShortcutCategory.GLOBAL,
        handler=lambda e: None,  # Built-in
        enabled=False  # Don't register (built-in)
    ))

    # Ctrl+C - Interrupt (built-in, just document)
    shortcuts.append(KeyShortcut(
        key="c-c",
        description="Cancel/Interrupt",
        category=ShortcutCategory.GLOBAL,
        handler=lambda e: None,  # Built-in
        enabled=False  # Don't register (built-in)
    ))

    manager.register_shortcuts(shortcuts)
    logger.info(f"Registered {len([s for s in shortcuts if s.enabled])} default shortcuts")


# Demo code
if __name__ == "__main__":
    print("=" * 70)
    print("KEYBOARD SHORTCUTS DEMO")
    print("=" * 70)
    print()

    # Create manager
    manager = KeybindingsManager()

    # Sample shortcuts
    shortcuts = [
        KeyShortcut(
            key="c-p",
            description="Open Command Palette",
            category=ShortcutCategory.GLOBAL,
            handler=lambda e: print("󰀫 Opening command palette...")
        ),
        KeyShortcut(
            key="c-k",
            description="Show Keyboard Shortcuts",
            category=ShortcutCategory.GLOBAL,
            handler=lambda e: print(" Showing shortcuts help...")
        ),
        KeyShortcut(
            key="c-s",
            description="Call Sophia Agent",
            category=ShortcutCategory.AGENT,
            handler=lambda e: print("󰉋 Calling Sophia...")
        ),
        KeyShortcut(
            key="c-g",
            description="Git Status",
            category=ShortcutCategory.GIT,
            handler=lambda e: print(" Git status")
        ),
        KeyShortcut(
            key="c-q",
            description="Quit Application",
            category=ShortcutCategory.GLOBAL,
            handler=lambda e: print("👋 Quitting...")
        ),
        KeyShortcut(
            key="c-h",
            description="Show Help",
            category=ShortcutCategory.GLOBAL,
            handler=lambda e: print("ℹ Help")
        ),
    ]

    # Register all shortcuts
    manager.register_shortcuts(shortcuts)

    print(f"Registered {len(manager.shortcuts)} shortcuts")
    print()

    # Show help
    manager.show_help()

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print()
    print("NOTE: To use these shortcuts, integrate with PromptSession:")
    print("  session = PromptSession(key_bindings=manager.get_bindings())")
