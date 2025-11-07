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
    """Custom auto-completion for max-code commands."""

    # Available commands
    COMMANDS = [
        "/help", "/exit", "/quit", "/clear",
        "/status", "/agents", "/constitutional",
        "/memory", "/metrics", "/theme",
        "/dashboard", "/consciousness",
        "/sophia", "/dormir",
    ]

    # EPL emojis (popular ones)
    EMOJIS = [
        "👑", "🧠", "🏥", "🎯", "📖",  # Agents
        "🌳", "🔍", "💻", "🧪", "🔧", "📝", "🚀",  # Actions
        "🔴", "🟢", "🔄", "✅", "❌", "⚠️", "🔥",  # States
        "🔒", "🐛", "✨", "💡", "🏆", "📊", "🏛️", "⚖️",  # Concepts
    ]

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()

        # Command completion
        if word.startswith("/"):
            for cmd in self.COMMANDS:
                if cmd.startswith(word):
                    yield Completion(cmd, start_position=-len(word))

        # Emoji completion (if starts with emoji or after space)
        else:
            for emoji in self.EMOJIS:
                if word in emoji or word == "":
                    yield Completion(emoji, start_position=-len(word))


def get_prompt_message() -> HTML:
    """Get formatted prompt message with colors."""
    return HTML('<ansigreen><b>max-code></b></ansigreen> ')


def print_welcome():
    """Print welcome message."""
    settings = get_settings()

    welcome_text = f"""
# Max-Code Interactive Shell

**Version:** {settings.version}
**Model:** {settings.claude.model}
**Environment:** {settings.environment}

## Quick Start

- Type commands in **natural language** or use **EPL** (Emoji Protocol Language)
- Press `Tab` for auto-completion
- Press `↑/↓` for command history
- Special commands start with `/`

## Examples

```bash
# Natural language
analyze the authentication module

# EPL (Emoji Protocol Language)
🌳📊🔒  # Tree of Thoughts to analyze security
🐛🔒  # Fix bug in security

# Mixed
Fix 🐛 in auth module

# Special commands
/help        # Show help
/agents      # Show agent dashboard
/status      # System status
/exit        # Exit shell
```

## EPL Vocabulary (Quick Reference)

**Agents:** 👑 Sophia | 🧠 MAXIMUS | 🏥 PENELOPE
**Actions:** 🌳 ToT | 🔍 Search | 💻 Code | 🧪 Test | 🔧 Fix
**States:** 🔴 RED | 🟢 GREEN | 🔄 REFACTOR | ✅ Success

Type `/help epl` for complete vocabulary.

---

*"Wisdom is supreme; therefore get wisdom." (Proverbs 4:7)*
    """

    md = Markdown(welcome_text)
    console.print(Panel(md, title="🚀 Welcome", border_style="cyan", expand=False))
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

    else:
        console.print(f"[yellow]⚠️  Unknown command: {cmd}[/yellow]")
        console.print("[dim]Type /help for available commands[/dim]\n")
        return False


def process_command(user_input: str):
    """
    Process user command (natural language, EPL, or regular).

    Sends to Claude Pro Max for processing.
    """
    from core.llm import chat_with_claude

    # Check if EPL
    has_emoji = any(char for char in user_input if ord(char) > 0x1F300)

    if has_emoji:
        console.print("[dim]🧠 EPL detected, parsing...[/dim]")
        # TODO FASE 2: Translate EPL to natural language
        # For now, send as-is

    console.print("[dim]🔄 Processing with Claude Pro Max...[/dim]\n")

    # Call Claude using Pro Max subscription
    result = chat_with_claude(user_input)

    if result and result.get("success"):
        # Display response
        response = result["response"]

        # Format as markdown panel
        from rich.panel import Panel
        from rich.markdown import Markdown

        md = Markdown(response)
        console.print(Panel(
            md,
            title=f"[cyan]Claude Pro Max[/cyan] [dim]({result['billing']})[/dim]",
            border_style="green",
            expand=True
        ))
    else:
        console.print("[red]❌ Failed to get response from Claude[/red]")
        console.print("[dim]Make sure 'claude' CLI is installed and authenticated[/dim]")
        console.print("[dim]Run: claude login[/dim]")

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
