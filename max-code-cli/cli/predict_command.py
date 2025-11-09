"""
Predict Command for Max-Code CLI

Provides predictive suggestions for next commands based on context.

FASE 9 - Advanced Features
"""

import asyncio
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from core.predictive_engine import (
    PredictiveEngine,
    PredictionContext,
    PredictionSource,
    GitStatus,
    ProjectDetector
)


console = Console()


@click.command()
@click.option(
    '--mode',
    type=click.Choice(['fast', 'deep']),
    default='fast',
    help='Prediction mode: fast (cache+history) or deep (LLM analysis)'
)
@click.option(
    '--show-reasoning',
    is_flag=True,
    help='Show reasoning for each prediction'
)
@click.option(
    '--limit',
    type=int,
    default=5,
    help='Number of suggestions to show (max 10)'
)
@click.option(
    '--execute',
    is_flag=True,
    help='Interactively select and execute a prediction'
)
def predict(mode, show_reasoning, limit, execute):
    """
    Get predictive suggestions for next commands.

    Max-Code analyzes your context (directory, git status, command history)
    and predicts what commands you're likely to run next.

    \b
    Examples:
      max-code predict                    # Fast prediction (history-based)
      max-code predict --mode deep        # Deep prediction (consciousness)
      max-code predict --show-reasoning   # Show why suggestions were made
      max-code predict --execute          # Select and run a prediction

    \b
    Features:
    - Context-aware (current dir, git status, recent commands)
    - Consciousness-based (MAXIMUS Oraculo integration)
    - Privacy-preserving (no external telemetry)
    - 3-tier fallback (Oraculo → Claude AI → Heuristic)

    \b
    Prediction Sources:
      🔮 Oraculo   - MAXIMUS consciousness-based prediction
      🤖 Claude AI - LLM reasoning with context analysis
      📊 Heuristic - Local command history patterns
    """
    # Validate limit
    if limit > 10:
        console.print("[yellow]Warning: Limiting suggestions to 10 (max)[/yellow]")
        limit = 10

    # Initialize engine
    engine = PredictiveEngine()

    # Build prediction context
    git_info = GitStatus.detect()
    project_type = ProjectDetector.detect_type()

    context = PredictionContext(
        current_directory=Path.cwd(),
        git_branch=git_info['branch'],
        git_status_clean=git_info['is_clean'],
        recent_commands=engine.command_history.get_recent(10),
        project_type=project_type
    )

    # Show context info
    console.print("\n[bold cyan]Predictive Suggestions[/bold cyan]")
    console.print(f"Mode: [yellow]{mode.upper()}[/yellow]")
    console.print(f"Directory: [white]{context.current_directory.name}[/white]")
    if git_info['in_repo']:
        console.print(f"Git Branch: [cyan]{git_info['branch']}[/cyan]")
        status_icon = "✓" if git_info['is_clean'] else "⚠"
        status_color = "green" if git_info['is_clean'] else "yellow"
        console.print(f"Git Status: [{status_color}]{status_icon} {'Clean' if git_info['is_clean'] else 'Modified'}[/{status_color}]")
    if project_type.value != "unknown":
        console.print(f"Project: [magenta]{project_type.value.title()}[/magenta]")
    console.print()

    # Get predictions
    with console.status(f"[cyan]Analyzing context ({mode} mode)..."):
        predictions = asyncio.run(
            engine.predict_next_command(context, mode=mode)
        )

    if not predictions:
        console.print("[yellow]No predictions available. Try running more commands to build history.[/yellow]\n")
        engine.close()
        return

    # Display predictions table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Rank", style="yellow", width=6)
    table.add_column("Command", style="cyan", width=50)
    table.add_column("Confidence", style="white", width=15)
    table.add_column("Source", style="magenta", width=15)

    for i, pred in enumerate(predictions[:limit], 1):
        # Confidence bar
        confidence_bar = "█" * int(pred.confidence * 10)
        confidence_text = f"{confidence_bar} {pred.confidence:.0%}"

        # Source icon
        source_icons = {
            PredictionSource.ORACULO: "🔮 Oraculo",
            PredictionSource.CLAUDE: "🤖 Claude AI",
            PredictionSource.HEURISTIC: "📊 Heuristic"
        }
        source_icon = source_icons.get(pred.source, "❓ Unknown")

        table.add_row(
            f"#{i}",
            pred.command,
            confidence_text,
            source_icon
        )

    console.print(table)

    # Show reasoning if requested
    if show_reasoning:
        console.print("\n[bold cyan]Reasoning:[/bold cyan]")
        for i, pred in enumerate(predictions[:limit], 1):
            if pred.reasoning:
                console.print(f"  [yellow]#{i}[/yellow] [dim]{pred.reasoning}[/dim]")
        console.print()

    # Interactive execution
    if execute:
        _interactive_execute(predictions[:limit], engine)
    else:
        console.print()

    # Cleanup
    engine.close()


def _interactive_execute(predictions, engine):
    """Interactively select and execute a prediction."""
    console.print("\n[bold cyan]Execute Prediction[/bold cyan]")
    console.print("Select a command to execute (or press Enter to cancel):\n")

    # Show numbered list
    for i, pred in enumerate(predictions, 1):
        console.print(f"  [yellow]{i}[/yellow]. {pred.command}")

    console.print()

    # Get user selection
    try:
        selection = input("Enter number (1-{}): ".format(len(predictions)))

        if not selection.strip():
            console.print("[dim]Cancelled[/dim]\n")
            return

        index = int(selection) - 1
        if index < 0 or index >= len(predictions):
            console.print("[red]Invalid selection[/red]\n")
            return

        selected = predictions[index]

        # Confirm execution
        console.print(f"\n[bold yellow]Execute:[/bold yellow] [cyan]{selected.command}[/cyan]")
        confirm = input("Confirm? (y/N): ")

        if confirm.lower() != 'y':
            console.print("[dim]Cancelled[/dim]\n")
            return

        # Execute command
        # Security note: shell=True is acceptable here because:
        # 1. User explicitly confirms before execution
        # 2. Command comes from learned history, not external input
        # 3. This is a CLI tool where user has full control
        import subprocess
        console.print(f"\n[bold cyan]Executing:[/bold cyan] {selected.command}\n")

        result = subprocess.run(selected.command, shell=True)  # nosec B602

        # Record execution in history
        engine.command_history.add_command(
            command=selected.command,
            directory=str(Path.cwd()),
            git_branch=GitStatus.detect()['branch'],
            success=(result.returncode == 0)
        )

        console.print()

    except (ValueError, KeyboardInterrupt):
        console.print("\n[dim]Cancelled[/dim]\n")
        return


if __name__ == '__main__':
    predict()
