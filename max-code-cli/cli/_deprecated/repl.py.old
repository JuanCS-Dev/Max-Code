"""
Max-Code CLI - Interactive REPL

Professional shell with prompt_toolkit integration.
Supports natural language, EPL (Emoji Protocol Language), and special commands.

Biblical Foundation:
"Let your speech always be gracious" (Colossians 4:6)
"""

import sys
from pathlib import Path
from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.formatted_text import HTML
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from config.settings import get_settings

console = Console()


class MaxCodeCompleter(Completer):
    """Modern auto-completion with command hints and EPL support."""

    # All available commands with descriptions
    COMMANDS = {
        "/help": "Show help",
        "/exit": "Exit shell",
        "/quit": "Exit shell",
        "/clear": "Clear screen",
        "/status": "System configuration",
        "/health": "Service health",
        "/agents": "Agent dashboard",
        "/constitutional": "P1-P6 status",
        "/dashboard": "Live multi-panel",
        "/theme": "Change theme",
        "/tui": "Full-screen mode",
        "/epl": "EPL vocabulary",
    }

    # EPL emojis with meanings
    EPL_EMOJIS = {
        "👑": "Sophia (Architect)",
        "🧠": "MAXIMUS (Systemic)",
        "🏥": "Penelope (Healing)",
        "🌳": "Tree of Thoughts",
        "🔍": "Explore/Search",
        "💻": "Code Generation",
        "🧪": "Test/TDD",
        "🔧": "Fix/Repair",
        "🔴": "RED (Failing)",
        "🟢": "GREEN (Passing)",
        "✅": "Success/Done",
        "🐛": "Bug/Error",
    }

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()

        # Command completion with descriptions
        if word.startswith("/"):
            for cmd, desc in self.COMMANDS.items():
                if cmd.startswith(word):
                    yield Completion(
                        cmd,
                        start_position=-len(word),
                        display_meta=desc
                    )

        # EPL emoji completion with meanings
        elif len(word) == 0 or any(c > '\u1F300' for c in word):
            for emoji, meaning in self.EPL_EMOJIS.items():
                yield Completion(
                    emoji,
                    start_position=-len(word),
                    display_meta=meaning
                )


def get_prompt_message() -> HTML:
    """Get formatted prompt message with colors and emoji."""
    # Use rocket emoji + colored prompt
    return HTML('<ansigreen><b>🚀 max-code></b></ansigreen> ')


def print_welcome():
    """Print magnificent welcome banner with MaxCodeBanner."""
    from ui.banner import MaxCodeBanner
    from config.settings import get_settings

    settings = get_settings()

    # Show magnificent banner with gradient, P1-P6, optional effects
    banner = MaxCodeBanner()
    banner.show(
        version=settings.version,
        context={
            'model': settings.claude.model,
            'environment': settings.environment,
            'mode': 'REPL Interactive Shell'
        },
        style='default',
        effect=None,  # Set to 'beams' for cinematic startup
        show_verse=True
    )

    # Minimal hint - Gemini style
    console.print()
    console.print("[dim]Type /help to see available commands[/dim]", justify="center")
    console.print("[dim]Tab for completion • ↑↓ for history[/dim]", justify="center")
    console.print()


def print_help(topic: Optional[str] = None):
    """Print help information."""

    if topic == "epl":
        help_text = """
# EPL (Emoji Protocol Language) - Complete Vocabulary

## Agents (5)
- 👑 Sophia (Architect)
- 🧠 MAXIMUS (Systemic Analysis)
- 🏥 PENELOPE (Code Healing)
- 🎯 MABA (Bias Detection)
- 📖 NIS (Narrative Intelligence)

## Actions (7)
- 🌳 Tree of Thoughts (ToT)
- 🔍 Explore/Search
- 💻 Code Generation
- 🧪 Test/TDD
- 🔧 Fix/Repair
- 📝 Documentation
- 🚀 Deploy/Launch

## States (7)
- 🔴 RED (TDD - Tests Failing)
- 🟢 GREEN (TDD - Tests Passing)
- 🔄 REFACTOR
- ✅ Success/Done/Approved
- ❌ Fail/Rejected/Error
- ⚠️ Warning/Attention
- 🔥 Urgent/Hot/Critical

## Concepts (8)
- 🔒 Security/Authentication
- 🐛 Bug/Error/Issue
- ✨ Feature/New
- 💡 Idea/Option
- 🏆 Winner/Best
- 📊 Analysis/Metrics
- 🏛️ Constitutional Review (P1-P6)
- ⚖️ Ethical Review

## Operators
- `→` then / flow / leads to
- `+` and / combine / with
- `|` or / alternative
- `!` not / negate

## Examples
```
🔴→🟢→🔄          # TDD cycle
👑:🌳→💡💡💡→🏆   # Sophia: ToT → 3 ideas → pick best
🐛→🏥→🔧→🧪→✅   # Bug → PENELOPE → Fix → Test → Success
🌳📊🔒            # Tree of Thoughts to analyze security
```

See docs/EPL_GUIDE.md for complete grammar and examples.
        """
    else:
        help_text = """
# Max-Code Commands

## Chat & Generation
- `chat <prompt>` - AI chat with Constitutional AI
- `analyze <file>` - Code analysis
- `generate <description>` - Code generation

## Constitutional AI
- `/constitutional` - P1-P6 dashboard
- `/guardian` - Guardian status

## Agents
- `/agents` - Agent dashboard (live)
- `/sophia <task>` - Sophia architect
- `/dormir` - Sleep agent (end-of-day)

## MAXIMUS Integration
- `/consciousness` - ESGT consciousness state
- `/penelope <request>` - PENELOPE healing
- `/orchestrator` - MAPE-K monitoring
- `/predict <task>` - Oraculo predictions
- `/context` - Atlas context

## System
- `/status` - System status
- `/memory` - Memory state
- `/metrics` - LEI, FPC, CRS metrics
- `/health` - Service health check

## UI/UX
- `/dashboard` - Multi-panel dashboard
- `/palette` - Command palette (Ctrl+P)
- `/theme <name>` - Switch theme (neon, fire, ocean, matrix, cyberpunk)
- `/tui` - Full-screen TUI mode

## EPL
- `/epl vocab` - Emoji vocabulary
- `/epl progress` - Learning progress

## REPL Commands
- `/help [topic]` - Show help (topics: epl)
- `/clear` - Clear screen
- `/exit` or `/quit` - Exit shell
- `Ctrl+C` - Interrupt current command
- `Ctrl+D` - Exit shell

## Examples
```bash
# Natural language
max-code> implement JWT authentication with refresh tokens

# EPL
max-code> 🌳📊🔒

# Special commands
max-code> /agents
max-code> /constitutional
max-code> /sophia design REST API
max-code> /help epl
```
        """

    md = Markdown(help_text)
    console.print(Panel(md, title="📚 Help", border_style="blue", expand=False))
    console.print()


def process_special_command(command: str) -> bool:
    """
    Process special commands starting with /.

    Returns:
        True if should exit, False otherwise
    """
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    if cmd in ["/exit", "/quit"]:
        console.print("\n[cyan]👋 Goodbye! May your code be bug-free.[/cyan]\n")
        return True

    elif cmd == "/clear":
        console.clear()
        return False

    elif cmd == "/help":
        print_help(topic=arg)
        return False

    elif cmd == "/status":
        from cli.main import config as config_cmd
        config_cmd.callback()
        return False

    elif cmd == "/health":
        from cli.main import health
        health.callback()
        return False

    # === AGENTS (Live Dashboard) ===
    elif cmd == "/agents":
        from ui.agents import AgentDisplay, Agent, AgentStatus
        display = AgentDisplay()

        # TODO: Get real agents from system
        # For now, show available agents
        agents = [
            Agent("Sophia", "Architect", AgentStatus.IDLE, "", 0, 0, 0, 0),
            Agent("MAXIMUS", "Systemic", AgentStatus.IDLE, "", 0, 0, 0, 0),
            Agent("Penelope", "Healing", AgentStatus.IDLE, "", 0, 0, 0, 0),
            Agent("Guardian", "Safety", AgentStatus.IDLE, "", 0, 0, 0, 0),
        ]

        console.print()
        display.show_dashboard(agents, title="🤖 Available Agents")
        console.print()
        return False

    # === CONSTITUTIONAL (P1-P6 Status) ===
    elif cmd == "/constitutional":
        from ui.tree_of_thoughts import TreeOfThoughtsDisplay
        from core.constitutional.models import Action, ActionType
        from core.constitutional.engine import get_constitutional_engine

        console.print("\n[bold cyan]📜 Constitutional AI Status[/bold cyan]\n")

        # Get constitutional engine and show status
        engine = get_constitutional_engine()

        # Create demo action to show validation
        action = Action(
            task_id="demo",
            action_type=ActionType.CODE_GENERATION,
            intent="Demo constitutional status",
            context={}
        )

        result = engine.execute_action(action)

        # Display using ToT display
        tot_display = TreeOfThoughtsDisplay()
        tot_display.show_constitutional_analysis(result)
        console.print()
        return False

    # === DASHBOARD (Multi-panel Live) ===
    elif cmd == "/dashboard":
        from ui.dashboard import create_dashboard
        import time

        console.print("\n[cyan]📊 Live Dashboard[/cyan]")
        console.print("[dim]Press Ctrl+C to exit[/dim]\n")

        dashboard = create_dashboard()

        # Add demo data
        dashboard.agents.add_agent("Sophia", "Analyzing", 75.0, "󰉋")
        dashboard.agents.add_agent("MAXIMUS", "Processing", 40.0, "")
        dashboard.output.add_line("✓ System ready", "green")
        dashboard.output.add_line("→ Monitoring...", "cyan")

        try:
            with dashboard.live(refresh_per_second=10):
                time.sleep(10)
        except KeyboardInterrupt:
            console.print("\n[dim]Dashboard closed[/dim]\n")

        return False

    # === THEME (Change theme) ===
    elif cmd == "/theme":
        from ui.themes import get_manager, set_theme

        if not arg:
            # Show available themes
            manager = get_manager()
            console.print("\n[bold cyan]🎨 Available Themes:[/bold cyan]\n")
            manager.show_themes(console)
            console.print()
        else:
            # Change theme
            try:
                set_theme(arg)
                console.print(f"\n[green]✓[/green] Theme changed to: [cyan]{arg}[/cyan]\n")
            except ValueError as e:
                console.print(f"\n[red]✗[/red] Invalid theme: {arg}\n")
                console.print("[dim]Use /theme to see available themes[/dim]\n")
        return False

    # === TUI (Full-screen mode) ===
    elif cmd == "/tui":
        from ui.tui_mode import run_tui

        console.print("\n[cyan]🖥️  Launching TUI mode...[/cyan]")
        console.print("[dim]Press Ctrl+C to exit[/dim]\n")

        try:
            run_tui(theme="neon")
        except ImportError:
            console.print("[red]✗[/red] TUI mode requires textual")
            console.print("[dim]Install: pip install textual[/dim]\n")
        except KeyboardInterrupt:
            console.print("\n[dim]TUI mode closed[/dim]\n")

        return False

    # === EPL VOCAB ===
    elif cmd == "/epl":
        if arg == "vocab":
            from core.epl.vocabulary import EMOJI_VOCABULARY

            console.print("\n[bold cyan]📚 EPL Vocabulary (Top 10):[/bold cyan]\n")
            for emoji, defn in list(EMOJI_VOCABULARY.items())[:10]:
                console.print(f"  {emoji}  [cyan]{defn.primary_meaning}[/cyan]  [dim]({defn.category.value})[/dim]")

            console.print(f"\n[dim]...and {len(EMOJI_VOCABULARY) - 10} more. See docs/EPL_GUIDE.md[/dim]\n")
        else:
            console.print("\n[yellow]Usage:[/yellow] /epl vocab\n")
        return False

    else:
        console.print(f"\n[yellow]✗[/yellow] Unknown command: [red]{cmd}[/red]")
        console.print("[dim]Type /help for available commands[/dim]\n")
        return False


def process_command(user_input: str):
    """
    Process user command (natural language or EPL).

    Sends to Claude Pro Max for processing.
    """
    from core.llm import chat_with_claude

    # Check if EPL (contains emojis)
    has_emoji = any(char for char in user_input if ord(char) > 0x1F300)

    if has_emoji:
        # EPL detected - try to translate
        try:
            from core.epl.parser import EPLParser
            from core.epl.translator import EPLTranslator

            parser = EPLParser()
            translator = EPLTranslator()

            # Parse EPL
            ast = parser.parse(user_input)

            # Translate to natural language
            natural = translator.translate(ast)

            # Show translation (clean, minimal)
            console.print(f"\n[dim]EPL:[/dim] {user_input}")
            console.print(f"[dim]→[/dim]   [cyan]{natural}[/cyan]\n")

            # Use translated version for Claude
            user_input = natural

        except Exception as e:
            # EPL parsing failed, send as-is
            console.print(f"[dim]⚠ EPL parse failed, sending as-is[/dim]\n")

    # Show clean processing indicator
    console.print("[dim]Processing...[/dim]")

    # Call Claude using Pro Max subscription
    result = chat_with_claude(user_input)

    if result and result.get("success"):
        # Display response with clean formatting
        response = result["response"]

        from rich.panel import Panel
        from rich.markdown import Markdown

        md = Markdown(response)
        console.print(Panel(
            md,
            title=f"[cyan]Claude[/cyan] [dim]• Pro Max • {result['billing']}[/dim]",
            border_style="cyan",
            expand=True,
            padding=(1, 2)
        ))
    else:
        console.print("\n[red]✗[/red] No response from Claude")
        console.print("[dim]Ensure 'claude' CLI is authenticated: claude login[/dim]")

    console.print()


def start_repl():
    """Start the interactive REPL shell."""
    settings = get_settings()

    # Setup history file
    history_file = settings.config_dir / ".max-code-history"

    # Create prompt session
    session = PromptSession(
        history=FileHistory(str(history_file)),
        auto_suggest=AutoSuggestFromHistory(),
        completer=MaxCodeCompleter(),
        enable_history_search=True,
        vi_mode=False,  # Emacs mode (Ctrl+A, Ctrl+E, etc)
    )

    # Print welcome
    print_welcome()

    # Quick check if Claude CLI is available (non-blocking, no test call)
    from core.llm import check_claude_cli_available
    from pathlib import Path

    cli_available = check_claude_cli_available()
    credentials_exist = (Path.home() / ".claude" / ".credentials.json").exists()

    if not cli_available:
        console.print("[yellow]⚠ Warning:[/yellow] [red]'claude' command not found[/red]")
        console.print("[dim]Install: npm install -g @anthropic-ai/claude-code[/dim]")
        console.print("[dim]Then run: claude login[/dim]")
        console.print()
    elif not credentials_exist:
        console.print("[yellow]⚠ Warning:[/yellow] [red]Not authenticated[/red]")
        console.print("[dim]Run: [bold]claude login[/bold][/dim]")
        console.print()

    # Main REPL loop
    while True:
        try:
            # Get user input
            user_input = session.prompt(get_prompt_message()).strip()

            # Skip empty input
            if not user_input:
                continue

            # Process special commands
            if user_input.startswith("/"):
                should_exit = process_special_command(user_input)
                if should_exit:
                    break
                continue

            # Process regular command
            process_command(user_input)

        except KeyboardInterrupt:
            # Ctrl+C - just print newline and continue
            console.print()
            continue

        except EOFError:
            # Ctrl+D - exit gracefully
            console.print("\n[cyan]👋 Goodbye![/cyan]\n")
            break

        except Exception as e:
            # Unexpected error
            console.print(f"[red]❌ Error: {e}[/red]")
            console.print("[dim]Type /help for assistance[/dim]\n")


if __name__ == "__main__":
    start_repl()
