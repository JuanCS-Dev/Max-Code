"""
Textual TUI Mode - Full-Screen Interactive Interface

Production-grade TUI application built with Textual framework.
Integrates themes, command palette, agents, and output display.

Biblical Foundation:
"Porque nada há encoberto que não haja de ser manifesto" (Marcos 4:22)
Making the invisible visible through UI.

Research findings:
- Textual App class: compose(), CSS_PATH, BINDINGS
- Reactive programming: reactive attributes + watch methods
- Widget composition: Header, Footer, Container, Custom widgets
- CSS styling: .tcss files with theme variables
- Event system: on_<event> handlers, action_<name> methods

Architecture:
1. MaxCodeApp: Main TUI application
2. Custom Widgets: AgentsPanel, OutputPanel, StatusPanel
3. Screens: MainScreen, SettingsScreen, HelpScreen
4. Integration: ThemeManager, CommandPalette, Agents
"""

import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical, VerticalScroll
    from textual.widgets import Header, Footer, Static, Button, Label, Input
    from textual.reactive import reactive
    from textual.binding import Binding
    from textual.screen import Screen
    from textual import events

    # Import dependencies after confirming Textual is available
    try:
        from ui.themes import ThemeManager, get_manager as get_theme_manager
        from ui.command_palette import CommandPalette
        TEXTUAL_AVAILABLE = True
    except ImportError as e:
        TEXTUAL_AVAILABLE = False
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to import dependencies: {e}")
        raise
except ImportError:
    TEXTUAL_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Textual not installed. TUI mode unavailable. Install with: pip install textual")

logger = logging.getLogger(__name__)


# Skip all class definitions if Textual not available
if TEXTUAL_AVAILABLE:

    class AgentsPanel(Static):
        """
        Agents status panel.

        Displays active agents with status and progress.
        """

        agents_count = reactive(0)
        status_text = reactive("No agents running")

        def compose(self) -> ComposeResult:
            """Compose agents panel."""
            yield Label("🤖 Active Agents", id="agents-title")
            yield Label(self.status_text, id="agents-status")

        def watch_agents_count(self, count: int) -> None:
            """Update status when agents count changes."""
            if count == 0:
                self.status_text = "No agents running"
            elif count == 1:
                self.status_text = "1 agent running"
            else:
                self.status_text = f"{count} agents running"

        def update_agents(self, agents: List[Dict[str, Any]]):
            """
            Update agents display.

            Args:
                agents: List of agent info dicts
            """
            self.agents_count = len(agents)


    class OutputPanel(VerticalScroll):
        """
        Output display panel.

        Shows command output and agent responses.
        """

        lines = reactive([])

        def compose(self) -> ComposeResult:
            """Compose output panel."""
            yield Label("📋 Output", id="output-title")
            yield Static("", id="output-content")

        def add_line(self, line: str):
            """Add output line."""
            new_lines = list(self.lines)
            new_lines.append(line)

            # Keep last 100 lines
            if len(new_lines) > 100:
                new_lines = new_lines[-100:]

            self.lines = new_lines

            # Update display
            content = self.query_one("#output-content", Static)
            content.update("\n".join(self.lines))

        def clear(self):
            """Clear output."""
            self.lines = []
            content = self.query_one("#output-content", Static)
            content.update("")


    class StatusPanel(Static):
        """
        Status bar panel.

        Shows current theme, shortcuts, and system status.
        """

        theme_name = reactive("neon")
        shortcuts_visible = reactive(True)

        def compose(self) -> ComposeResult:
            """Compose status panel."""
            yield Label("", id="status-content")

        def watch_theme_name(self, theme: str) -> None:
            """Update status when theme changes."""
            self.update_status()

        def watch_shortcuts_visible(self, visible: bool) -> None:
            """Update status when shortcuts visibility changes."""
            self.update_status()

        def update_status(self):
            """Update status display."""
            shortcuts = " | Ctrl+P: Palette | Ctrl+K: Keys | Ctrl+Q: Quit" if self.shortcuts_visible else ""
            status_text = f"🎨 Theme: {self.theme_name}{shortcuts}"

            content = self.query_one("#status-content", Label)
            content.update(status_text)


    class MainScreen(Screen):
        """
        Main application screen.

        Primary interface with agents, output, and status.
        """

        BINDINGS = [
            Binding("ctrl+p", "show_palette", "Command Palette", priority=True),
            Binding("ctrl+k", "show_shortcuts", "Shortcuts", priority=True),
            Binding("ctrl+t", "cycle_theme", "Theme", priority=True),
            Binding("ctrl+c", "clear_output", "Clear", priority=True),
            Binding("ctrl+q", "quit", "Quit", priority=True),
        ]

        def __init__(self, theme_manager: ThemeManager):
            """
            Initialize main screen.

            Args:
                theme_manager: Theme manager instance
            """
            super().__init__()
            self.theme_manager = theme_manager

        def compose(self) -> ComposeResult:
            """Compose main screen layout."""
            yield Header()

            with Container(id="main-container"):
                # Left panel: Agents
                with Vertical(id="left-panel"):
                    yield AgentsPanel(id="agents-panel")

                # Right panel: Output
                with Vertical(id="right-panel"):
                    yield OutputPanel(id="output-panel")

            # Bottom: Status
            yield StatusPanel(id="status-panel")

            yield Footer()

        def action_show_palette(self) -> None:
            """Show command palette."""
            self.app.bell()  # Placeholder
            output = self.query_one("#output-panel", OutputPanel)
            output.add_line("🔍 Command palette opened (integration pending)")

        def action_show_shortcuts(self) -> None:
            """Show keyboard shortcuts."""
            self.app.bell()
            output = self.query_one("#output-panel", OutputPanel)
            output.add_line("⌨️  Keyboard shortcuts:")
            output.add_line("  Ctrl+P - Command Palette")
            output.add_line("  Ctrl+K - Show Shortcuts")
            output.add_line("  Ctrl+T - Cycle Theme")
            output.add_line("  Ctrl+C - Clear Output")
            output.add_line("  Ctrl+Q - Quit")

        def action_cycle_theme(self) -> None:
            """Cycle through themes."""
            themes = ["neon", "fire", "ocean", "matrix", "cyberpunk"]
            current = self.theme_manager.active_theme.name
            current_idx = themes.index(current) if current in themes else 0
            next_idx = (current_idx + 1) % len(themes)
            next_theme = themes[next_idx]

            self.theme_manager.set_theme(next_theme)

            # Update status
            status = self.query_one("#status-panel", StatusPanel)
            status.theme_name = next_theme

            # Notify
            output = self.query_one("#output-panel", OutputPanel)
            output.add_line(f"🎨 Theme changed: {next_theme}")

        def action_clear_output(self) -> None:
            """Clear output panel."""
            output = self.query_one("#output-panel", OutputPanel)
            output.clear()

        def action_quit(self) -> None:
            """Quit application."""
            self.app.exit()


    class MaxCodeApp(App):
        """
        Max-Code TUI Application.

        Full-screen terminal UI with themes, agents, and output.

        Example:
            app = MaxCodeApp()
            app.run()
        """

        CSS_PATH = "tui_mode.tcss"  # Optional CSS file
        TITLE = "Max-Code CLI"
        SUB_TITLE = "AI-Powered Development Assistant"

        def __init__(self, theme_name: str = "neon"):
            """
            Initialize TUI application.

            Args:
                theme_name: Initial theme name
            """
            super().__init__()

            # Theme manager
            self.theme_manager = get_theme_manager()
            self.theme_manager.set_theme(theme_name)

            logger.info(f"MaxCodeApp initialized (theme: {theme_name})")

        def on_mount(self) -> None:
            """Called when app is mounted."""
            self.title = self.TITLE
            self.sub_title = self.SUB_TITLE

            # Add welcome message
            output = self.query_one("#output-panel", OutputPanel)
            output.add_line("🚀 Max-Code CLI TUI Mode")
            output.add_line("━" * 50)
            output.add_line("Welcome to the full-screen terminal interface!")
            output.add_line("")
            output.add_line("Press Ctrl+K to see keyboard shortcuts")
            output.add_line("Press Ctrl+T to change theme")
            output.add_line("Press Ctrl+Q to quit")
            output.add_line("━" * 50)

        def get_css_variables(self) -> Dict[str, str]:
            """
            Get CSS variables for theming.

            Returns:
                Dict of CSS variables from active theme
            """
            return self.theme_manager.get_textual_css_vars()

        def compose(self) -> ComposeResult:
            """Compose application."""
            yield MainScreen(self.theme_manager)


# Public API

def run_tui(theme: str = "neon"):
    """
    Run TUI mode.

    Args:
        theme: Initial theme name

    Raises:
        ImportError: If Textual not installed
    """
    if not TEXTUAL_AVAILABLE:
        raise ImportError(
            "Textual not installed. Install with: pip install textual"
        )

    app = MaxCodeApp(theme_name=theme)  # Fixed: use theme_name parameter
    app.run()


# Demo/Entry point
if __name__ == "__main__":
    import sys

    if not TEXTUAL_AVAILABLE:
        print("ERROR: Textual not installed")
        print("Install with: pip install textual")
        sys.exit(1)

    print("=" * 70)
    print("TEXTUAL TUI MODE DEMO")
    print("=" * 70)
    print()
    print("Starting TUI application...")
    print()
    print("Available themes: neon, fire, ocean, matrix, cyberpunk")
    print("Use Ctrl+T to cycle through themes")
    print("Use Ctrl+Q to quit")
    print()
    print("=" * 70)
    print()

    # Get theme from args
    theme = sys.argv[1] if len(sys.argv) > 1 else "neon"

    try:
        run_tui(theme=theme)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
