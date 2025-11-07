"""
MAXIMUS SHELL - Status Bar System v3.0
Persistent bottom status bar for Constitutional AI monitoring.

Features:
- P1-P6 Constitutional Principles status (with colors + icons)
- Current agent indicator
- Token usage with visual progress
- Model information (Claude Sonnet 4.5)
- Session time tracking
- Auto-refresh on updates
- Beautiful neon accents

"Watch and pray so that you will not fall into temptation.
The spirit is willing, but the flesh is weak."
(Matthew 26:41)

Visual Layout:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ∞P1 ⚡P2 ♥P3 ◆P4 ✦P5 ⚙P6 │ 🤖 CodeAgent │ 🧠 Sonnet 4.5 │ ⚡ 2.4K/200K ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.text import Text
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class StatusBarState:
    """
    State container for status bar information.

    Tracks all dynamic elements that need to be displayed.
    """
    # Constitutional Principles (P1-P6) - active states
    principles: Dict[str, bool] = field(default_factory=lambda: {
        'P1': True, 'P2': True, 'P3': True,
        'P4': True, 'P5': True, 'P6': True
    })

    # Current agent
    active_agent: Optional[str] = None
    agent_status: str = "idle"  # idle, thinking, active

    # Model information
    model_name: str = "Claude Sonnet 4.5"
    model_version: str = "20250929"

    # Token usage
    tokens_used: int = 0
    tokens_limit: int = 200000

    # Session info
    session_start: float = field(default_factory=time.time)
    session_id: Optional[str] = None

    # Context info
    current_file: Optional[str] = None
    git_branch: Optional[str] = None


class StatusBar:
    """
    Persistent status bar for MAXIMUS SHELL.

    Displays Constitutional AI status, agent info, and system metrics
    in a beautiful bottom bar with neon accents.

    Usage:
        status = StatusBar()
        status.update(active_agent="CodeAgent", tokens_used=2400)
        status.render()  # One-time render

        # Or use live mode
        with status.live():
            # Status bar updates automatically
            status.update(tokens_used=3000)
    """

    # Unicode icons for Constitutional Principles (terminal-safe)
    PRINCIPLE_ICONS = {
        'P1': '∞',   # Transcendence
        'P2': '⚡',  # Reasoning
        'P3': '♥',   # Care
        'P4': '◆',   # Wisdom
        'P5': '✦',   # Beauty
        'P6': '⚙',   # Autonomy
    }

    # Agent status icons
    AGENT_ICONS = {
        'idle': '🤖',
        'thinking': '🧠',
        'active': '⚡',
    }

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize status bar.

        Args:
            console: Rich Console instance (creates new if None)
        """
        self.console = console or Console()
        self.state = StatusBarState()
        self._live = None

    def update(
        self,
        active_agent: Optional[str] = None,
        agent_status: Optional[str] = None,
        tokens_used: Optional[int] = None,
        principles: Optional[Dict[str, bool]] = None,
        current_file: Optional[str] = None,
        git_branch: Optional[str] = None,
        **kwargs
    ):
        """
        Update status bar state.

        Args:
            active_agent: Name of currently active agent
            agent_status: Agent status (idle/thinking/active)
            tokens_used: Current token usage
            principles: P1-P6 active states
            current_file: Current file being edited
            git_branch: Current git branch
            **kwargs: Additional state updates
        """
        if active_agent is not None:
            self.state.active_agent = active_agent
        if agent_status is not None:
            self.state.agent_status = agent_status
        if tokens_used is not None:
            self.state.tokens_used = tokens_used
        if principles is not None:
            self.state.principles.update(principles)
        if current_file is not None:
            self.state.current_file = current_file
        if git_branch is not None:
            self.state.git_branch = git_branch

        # Update any additional state
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)

        # Refresh display if in live mode
        if self._live:
            self._live.update(self._build_status_bar())

    def _build_principles_section(self) -> Text:
        """
        Build Constitutional Principles status display.

        Returns:
            Rich Text with colored P1-P6 indicators
        """
        from ui.colors import ColorPalette

        palette = ColorPalette()
        principle_colors = {
            'P1': palette.P1_TRANSCENDENCE,
            'P2': palette.P2_REASONING,
            'P3': palette.P3_CARE,
            'P4': palette.P4_WISDOM,
            'P5': palette.P5_BEAUTY,
            'P6': palette.P6_AUTONOMY,
        }

        text = Text()
        for i, (code, active) in enumerate(self.state.principles.items()):
            if i > 0:
                text.append(" ", style="dim")

            icon = self.PRINCIPLE_ICONS.get(code, '●')
            color = principle_colors.get(code, "#808080")

            if active:
                # Active: colored icon + code
                text.append(f"{icon}{code}", style=f"bold {color}")
            else:
                # Inactive: dimmed
                text.append(f"{icon}{code}", style="dim")

        return text

    def _build_agent_section(self) -> Text:
        """
        Build agent status display.

        Returns:
            Rich Text with agent name and status icon
        """
        from ui.colors import ColorPalette

        palette = ColorPalette()
        text = Text()

        if self.state.active_agent:
            # Status icon
            icon = self.AGENT_ICONS.get(self.state.agent_status, '🤖')
            text.append(f"{icon} ", style="")

            # Agent name with color based on status
            if self.state.agent_status == 'active':
                color = palette.AGENT_ACTIVE
            elif self.state.agent_status == 'thinking':
                color = palette.AGENT_THINKING
            else:
                color = palette.AGENT_IDLE

            text.append(self.state.active_agent, style=f"bold {color}")
        else:
            text.append("🤖 Ready", style="dim")

        return text

    def _build_model_section(self) -> Text:
        """
        Build model information display.

        Returns:
            Rich Text with model name
        """
        from ui.colors import ColorPalette

        palette = ColorPalette()
        text = Text()

        text.append("🧠 ", style="")
        text.append(self.state.model_name, style=f"{palette.INFO}")

        return text

    def _build_tokens_section(self) -> Text:
        """
        Build token usage display with visual indicator.

        Returns:
            Rich Text with token count and percentage
        """
        from ui.colors import ColorPalette

        palette = ColorPalette()
        text = Text()

        # Calculate usage percentage
        usage_pct = (self.state.tokens_used / self.state.tokens_limit) * 100

        # Choose color based on usage
        if usage_pct < 50:
            color = palette.SUCCESS
        elif usage_pct < 80:
            color = palette.WARNING
        else:
            color = palette.ERROR

        # Format token numbers (e.g., 2.4K, 15.3K, 200K)
        used_str = self._format_token_count(self.state.tokens_used)
        limit_str = self._format_token_count(self.state.tokens_limit)

        text.append("⚡ ", style="")
        text.append(f"{used_str}/{limit_str}", style=f"bold {color}")
        text.append(f" ({usage_pct:.0f}%)", style="dim")

        return text

    def _format_token_count(self, count: int) -> str:
        """Format token count with K suffix (e.g., 2400 → 2.4K)."""
        if count >= 1000:
            return f"{count / 1000:.1f}K"
        return str(count)

    def _build_context_section(self) -> Optional[Text]:
        """
        Build context information (file, git branch).

        Returns:
            Rich Text with context info, or None if no context
        """
        from ui.colors import ColorPalette

        palette = ColorPalette()
        parts = []

        if self.state.git_branch:
            parts.append(f"⎇ {self.state.git_branch}")

        if self.state.current_file:
            # Truncate long file paths
            file_display = self.state.current_file
            if len(file_display) > 30:
                file_display = "..." + file_display[-27:]
            parts.append(f"📄 {file_display}")

        if not parts:
            return None

        text = Text()
        text.append(" │ ".join(parts), style="dim")
        return text

    def _build_session_section(self) -> Text:
        """
        Build session time display.

        Returns:
            Rich Text with elapsed session time
        """
        elapsed = time.time() - self.state.session_start
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        text = Text()
        text.append(f"⏱ {minutes:02d}:{seconds:02d}", style="dim")

        return text

    def _build_status_bar(self) -> Table:
        """
        Build the complete status bar as a Rich Table.

        Returns:
            Rich Table configured as status bar
        """
        from ui.colors import ColorPalette

        palette = ColorPalette()

        # Create table with no headers
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left")    # Principles
        table.add_column(justify="left")    # Agent
        table.add_column(justify="left")    # Model
        table.add_column(justify="right")   # Tokens
        table.add_column(justify="right")   # Session

        # Build sections
        principles = self._build_principles_section()
        agent = self._build_agent_section()
        model = self._build_model_section()
        tokens = self._build_tokens_section()
        session = self._build_session_section()

        # Add context if available
        context = self._build_context_section()

        # Assemble row
        if context:
            # With context: Principles │ Agent │ Model │ Context │ Tokens │ Session
            table.add_row(
                principles,
                agent,
                model,
                context,
                tokens,
                session
            )
        else:
            # Without context: Principles │ Agent │ Model │ Tokens │ Session
            table.add_row(
                principles,
                agent,
                model,
                tokens,
                session
            )

        return table

    def render(self):
        """Render status bar once (non-live mode)."""
        self.console.print(self._build_status_bar())

    def live(self):
        """
        Start live mode for automatic updates.

        Returns:
            Live context manager

        Usage:
            with status.live():
                # Make updates
                status.update(tokens_used=3000)
                time.sleep(1)
        """
        if self._live is None:
            self._live = Live(
                self._build_status_bar(),
                console=self.console,
                refresh_per_second=1
            )
        return self._live

    def stop(self):
        """Stop live mode."""
        if self._live:
            self._live.stop()
            self._live = None


# ═══════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

_status_bar_instance = None

def get_status_bar(console: Optional[Console] = None) -> StatusBar:
    """Get singleton status bar instance."""
    global _status_bar_instance
    if _status_bar_instance is None:
        _status_bar_instance = StatusBar(console=console)
    return _status_bar_instance


# ═══════════════════════════════════════════════════════════════════════════
# DEMO / TESTING
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import time
    from rich.console import Console

    console = Console()
    status = StatusBar(console=console)

    console.print("\n" + "=" * 70)
    console.print("MAXIMUS SHELL - STATUS BAR DEMONSTRATION")
    console.print("=" * 70 + "\n")

    # Test 1: Static render
    console.print("1. STATIC STATUS BAR (Initial state):")
    status.render()
    console.print()

    time.sleep(1)

    # Test 2: With agent active
    console.print("2. WITH AGENT ACTIVE:")
    status.update(
        active_agent="CodeAgent",
        agent_status="thinking",
        tokens_used=2400
    )
    status.render()
    console.print()

    time.sleep(1)

    # Test 3: With context
    console.print("3. WITH CONTEXT INFO:")
    status.update(
        git_branch="feature/maximus-shell",
        current_file="ui/status_bar.py"
    )
    status.render()
    console.print()

    time.sleep(1)

    # Test 4: High token usage
    console.print("4. HIGH TOKEN USAGE WARNING:")
    status.update(
        tokens_used=165000,
        agent_status="active"
    )
    status.render()
    console.print()

    time.sleep(1)

    # Test 5: Live mode demonstration
    console.print("5. LIVE MODE (5 seconds, auto-updating):")
    console.print("   Watch the session timer and token count increment...\n")

    with status.live():
        for i in range(5):
            status.update(tokens_used=165000 + (i * 1000))
            time.sleep(1)

    console.print("\n" + "=" * 70)
    console.print("DEMO COMPLETE - Status bar ready for MAXIMUS SHELL")
    console.print("=" * 70 + "\n")
