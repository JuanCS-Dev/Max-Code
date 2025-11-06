"""
Learn Command for Max-Code CLI

Adaptive learning and user behavior analytics (GDPR-compliant).

FASE 9 - Advanced Features
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.adaptive_learning import AdaptiveLearningSystem, LearningConfig


console = Console()


@click.group()
def learn():
    """
    Adaptive learning and user behavior analytics.

    Max-Code learns from your command usage patterns to provide better
    predictions and personalized recommendations.

    \b
    Privacy-First Design:
    - All data stored locally (no external servers)
    - Explicit opt-in required
    - GDPR compliant (export, delete, opt-out)
    - No telemetry without consent

    \b
    Examples:
      max-code learn enable              # Enable learning mode
      max-code learn insights            # Show learning insights
      max-code learn export data.json    # Export all data (GDPR)
      max-code learn reset               # Delete all data (GDPR)
    """
    pass


@learn.command()
@click.option('--auto', is_flag=True, help='Enable automatic learning (record all commands)')
@click.option('--no-maximus', is_flag=True, help='Disable feedback to MAXIMUS services')
def enable(auto, no_maximus):
    """
    Enable learning mode.

    Learning mode tracks your command usage to improve predictions and
    provide personalized recommendations.

    \b
    Privacy Notice:
    - All data stored locally in ~/.max-code/learning.db
    - No data sent to external servers (except MAXIMUS if enabled)
    - You can export or delete your data anytime
    - GDPR compliant (Articles 13, 17, 20, 21)
    """
    config = LearningConfig.load()

    # Show privacy notice if first time
    if not config.enabled:
        console.print("\n[bold cyan]Privacy Notice[/bold cyan]\n")
        console.print("Max-Code Learning Mode collects usage data to improve predictions.")
        console.print()
        console.print("[bold yellow]What we collect (locally):[/bold yellow]")
        console.print("  • Command execution history")
        console.print("  • Success/failure status")
        console.print("  • Execution context (directory, git branch)")
        console.print("  • Optional user ratings (1-5 stars)")
        console.print()
        console.print("[bold yellow]What we DON'T collect:[/bold yellow]")
        console.print("  • File contents or code")
        console.print("  • API keys or secrets")
        console.print("  • Personal identifiable information (PII)")
        console.print()
        console.print("[bold green]Your rights (GDPR):[/bold green]")
        console.print("  • Right to access: max-code learn export")
        console.print("  • Right to erasure: max-code learn reset")
        console.print("  • Right to object: max-code learn disable")
        console.print()

        # Get consent
        if not click.confirm("Do you consent to local data collection?", default=False):
            console.print("\n[yellow]Learning mode not enabled.[/yellow]")
            console.print("You can enable it later with: [cyan]max-code learn enable[/cyan]\n")
            return

    # Update config
    config.enabled = True
    config.auto_record = auto
    config.send_feedback_to_maximus = not no_maximus
    config.save()

    # Success message
    console.print("\n[green]✓[/green] Learning mode enabled")

    if auto:
        console.print("[green]✓[/green] Auto-recording enabled (all commands)")
    else:
        console.print("[yellow]→[/yellow] Manual recording only")

    if config.send_feedback_to_maximus:
        console.print("[green]✓[/green] MAXIMUS feedback enabled (neuromodulation)")
    else:
        console.print("[yellow]→[/yellow] MAXIMUS feedback disabled")

    console.print()
    console.print("[dim]All data stored locally: ~/.max-code/learning.db[/dim]")
    console.print("[dim]Privacy-preserving: No external telemetry[/dim]")
    console.print()


@learn.command()
def disable():
    """
    Disable learning mode.

    Stops collecting new data. Existing data is preserved unless you reset.
    """
    config = LearningConfig.load()

    if not config.enabled:
        console.print("\n[yellow]Learning mode is already disabled.[/yellow]\n")
        return

    config.enabled = False
    config.save()

    console.print("\n[green]✓[/green] Learning mode disabled")
    console.print()
    console.print("[dim]Existing data preserved. Use 'max-code learn reset' to delete.[/dim]")
    console.print()


@learn.command()
def insights():
    """
    Show learning insights and recommendations.

    Displays analytics about your command usage patterns, success rates,
    and personalized recommendations.
    """
    system = AdaptiveLearningSystem()
    config = LearningConfig.load()

    if not config.enabled:
        console.print("\n[yellow]⚠ Learning mode is disabled.[/yellow]")
        console.print("Enable with: [cyan]max-code learn enable[/cyan]\n")

    # Get statistics
    stats = system.get_statistics()

    if stats["total_executions"] == 0:
        console.print("\n[yellow]No learning data available yet.[/yellow]")
        console.print("Start using Max-Code commands to build your learning profile.")
        console.print()
        return

    # Get insights
    insights = system.get_learning_insights()

    # Display header
    console.print("\n[bold cyan]Learning Insights[/bold cyan]")
    console.print(f"[dim]Based on {stats['total_executions']} command executions[/dim]\n")

    # Most used commands
    if insights.most_used_commands:
        console.print("[bold yellow]Most Used Commands:[/bold yellow]")
        table = Table(show_header=False, box=None)
        table.add_column("Rank", style="yellow", width=4)
        table.add_column("Command", style="cyan", width=50)
        table.add_column("Count", style="white", width=10)

        for i, (cmd, count) in enumerate(insights.most_used_commands[:5], 1):
            table.add_row(f"{i}.", cmd, f"{count}x")

        console.print(table)
        console.print()

    # Success rates
    if insights.success_rate_by_command:
        console.print("[bold yellow]Success Rates:[/bold yellow]")
        table = Table(show_header=False, box=None)
        table.add_column("Command", style="cyan", width=50)
        table.add_column("Success Rate", style="white", width=20)

        for cmd, rate in list(insights.success_rate_by_command.items())[:5]:
            color = "green" if rate > 0.8 else "yellow" if rate > 0.5 else "red"
            bar = "█" * int(rate * 10)
            table.add_row(cmd, f"[{color}]{bar} {rate:.0%}[/{color}]")

        console.print(table)
        console.print()

    # Error patterns
    if insights.error_patterns:
        console.print("[bold red]Common Errors:[/bold red]")
        for error in insights.error_patterns[:3]:
            console.print(
                f"  [red]•[/red] {error['command']} "
                f"({error['failures']} failures / {error['total_attempts']} attempts)"
            )
        console.print()

    # Time patterns
    if insights.time_patterns:
        console.print("[bold yellow]Usage by Time of Day:[/bold yellow]")
        max_count = max(insights.time_patterns.values())
        for hour, count in sorted(insights.time_patterns.items())[:8]:
            bar_length = int((count / max_count) * 20) if max_count > 0 else 0
            bar = "▓" * bar_length + "░" * (20 - bar_length)
            console.print(f"  {hour} [{bar}] {count}")
        console.print()

    # Recommendations
    if insights.recommendations:
        console.print("[bold cyan]Recommendations:[/bold cyan]")
        for i, rec in enumerate(insights.recommendations, 1):
            console.print(f"  [cyan]{i}.[/cyan] {rec}")
        console.print()

    # Statistics summary
    console.print("[bold yellow]Statistics:[/bold yellow]")
    console.print(f"  • Total executions: [white]{stats['total_executions']}[/white]")
    console.print(f"  • Unique commands: [white]{stats['unique_commands']}[/white]")
    console.print(f"  • Total errors: [white]{stats['error_count']}[/white]")
    console.print()


@learn.command()
@click.argument('output_file', type=click.Path())
def export(output_file):
    """
    Export all learning data to JSON file.

    GDPR Article 20: Right to data portability

    \b
    Example:
      max-code learn export my-data.json
    """
    system = AdaptiveLearningSystem()

    output_path = Path(output_file)

    # Confirm if file exists
    if output_path.exists():
        if not click.confirm(f"File {output_file} exists. Overwrite?", default=False):
            console.print("\n[yellow]Export cancelled.[/yellow]\n")
            return

    # Export data
    console.print(f"\n[cyan]Exporting learning data to {output_file}...[/cyan]")

    try:
        count = system.export_data(output_path)

        console.print(f"\n[green]✓[/green] Exported {count} records")
        console.print(f"[green]✓[/green] File saved to: [white]{output_path.absolute()}[/white]")
        console.print()
        console.print("[dim]This data was collected locally on your device.[/dim]")
        console.print("[dim]No external servers have access to this information.[/dim]")
        console.print()

    except Exception as e:
        console.print(f"\n[red]✗ Export failed: {e}[/red]\n")


@learn.command()
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def reset(confirm):
    """
    Reset all learned data.

    GDPR Article 17: Right to erasure (Right to be forgotten)

    \b
    Warning: This action cannot be undone!

    \b
    Example:
      max-code learn reset --confirm
    """
    system = AdaptiveLearningSystem()

    # Get statistics before reset
    stats = system.get_statistics()

    if stats["total_executions"] == 0:
        console.print("\n[yellow]No data to reset.[/yellow]\n")
        return

    # Confirm action
    if not confirm:
        console.print(f"\n[bold yellow]⚠ Warning: This will delete {stats['total_executions']} execution records![/bold yellow]\n")
        console.print("This action cannot be undone.\n")

        if not click.confirm("Are you sure you want to delete all learning data?", default=False):
            console.print("\n[yellow]Reset cancelled.[/yellow]\n")
            return

    # Reset data
    console.print("\n[cyan]Deleting all learning data...[/cyan]")

    try:
        system.reset()

        console.print("\n[green]✓[/green] All learning data deleted")
        console.print(f"[green]✓[/green] Removed {stats['total_executions']} records")
        console.print()
        console.print("[dim]Your right to erasure has been exercised (GDPR Article 17).[/dim]")
        console.print()

    except Exception as e:
        console.print(f"\n[red]✗ Reset failed: {e}[/red]\n")


@learn.command()
def status():
    """
    Show learning mode status and configuration.
    """
    system = AdaptiveLearningSystem()
    config = LearningConfig.load()
    stats = system.get_statistics()

    console.print("\n[bold cyan]Learning Mode Status[/bold cyan]\n")

    # Status
    status_color = "green" if config.enabled else "yellow"
    status_text = "ENABLED" if config.enabled else "DISABLED"
    console.print(f"Status: [{status_color}]{status_text}[/{status_color}]")

    if config.enabled:
        console.print(f"Auto-record: [{'green' if config.auto_record else 'yellow'}]{'✓ Yes' if config.auto_record else '✗ No'}[/{'green' if config.auto_record else 'yellow'}]")
        console.print(f"MAXIMUS feedback: [{'green' if config.send_feedback_to_maximus else 'yellow'}]{'✓ Yes' if config.send_feedback_to_maximus else '✗ No'}[/{'green' if config.send_feedback_to_maximus else 'yellow'}]")

    console.print()

    # Statistics
    console.print("[bold yellow]Statistics:[/bold yellow]")
    console.print(f"  Total executions: [white]{stats['total_executions']}[/white]")
    console.print(f"  Unique commands: [white]{stats['unique_commands']}[/white]")
    console.print(f"  Total errors: [white]{stats['error_count']}[/white]")

    if stats['most_used']:
        top_cmd = stats['most_used'][0]
        console.print(f"  Most used: [cyan]{top_cmd[0]}[/cyan] ({top_cmd[1]}x)")

    console.print()

    # Storage
    db_path = Path.home() / ".max-code" / "learning.db"
    if db_path.exists():
        size_kb = db_path.stat().st_size / 1024
        console.print(f"[dim]Database: {db_path} ({size_kb:.1f} KB)[/dim]")
    else:
        console.print("[dim]Database: Not created yet[/dim]")

    console.print()

    # GDPR notice
    if config.enabled:
        console.print("[bold green]GDPR Compliance:[/bold green]")
        console.print("  • Right to access: [cyan]max-code learn export[/cyan]")
        console.print("  • Right to erasure: [cyan]max-code learn reset[/cyan]")
        console.print("  • Right to object: [cyan]max-code learn disable[/cyan]")
        console.print()


if __name__ == '__main__':
    learn()
