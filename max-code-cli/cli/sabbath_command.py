"""
Sabbath Command for Max-Code CLI

Sabbath mode management for rest and reflection (Biblical observance).

FASE 9 - Advanced Features
"""

import click
from rich.console import Console
from rich.panel import Panel

from core.sabbath_manager import SabbathManager, SabbathTradition


console = Console()


@click.group()
def sabbath():
    """
    Sabbath mode management for rest and reflection.

    Respects Biblical principles of rest with graceful service degradation.

    \b
    Biblical Foundation:
    - Exodus 20:8-11 (4th Commandment)
    - Leviticus 23:3 (Day of rest)
    - Isaiah 58:13-14 (Call the Sabbath a delight)

    \b
    Examples:
      max-code sabbath configure --tradition jewish    # Jewish Sabbath
      max-code sabbath configure --tradition christian # Christian Sabbath
      max-code sabbath enable                          # Manually enable
      max-code sabbath status                          # Check status

    \b
    During Sabbath Mode:
    - Essential commands work (health, status, config)
    - Non-essential commands disabled (predict, learn)
    - MAXIMUS consciousness in rest state
    - Graceful degradation for all features
    """
    pass


@sabbath.command()
@click.option(
    '--tradition',
    type=click.Choice(['jewish', 'christian', 'custom']),
    default='jewish',
    help='Sabbath tradition (default: jewish)'
)
@click.option(
    '--timezone',
    default='UTC',
    help='Timezone for scheduling (e.g., America/New_York, Europe/London)'
)
@click.option(
    '--auto',
    is_flag=True,
    help='Auto-enable based on schedule'
)
@click.option(
    '--latitude',
    type=float,
    default=32.0853,
    help='Latitude for sunset calculation (default: Jerusalem)'
)
@click.option(
    '--longitude',
    type=float,
    default=34.7818,
    help='Longitude for sunset calculation (default: Jerusalem)'
)
def configure(tradition, timezone, auto, latitude, longitude):
    """
    Configure Sabbath mode settings.

    Sets up automated Sabbath mode based on your tradition and location.

    \b
    Traditions:
      jewish    - Friday sunset → Saturday sunset (Biblical)
      christian - Sunday 00:00 → 23:59 (First day of week)
      custom    - User-defined schedule

    \b
    Biblical Reference:
      Jewish: "From evening to evening you shall observe your sabbath" (Lev 23:32)
      Christian: "On the first day of the week" (Acts 20:7)

    \b
    Examples:
      # Jewish Sabbath in New York
      max-code sabbath configure --tradition jewish --timezone America/New_York

      # Christian Sabbath in London
      max-code sabbath configure --tradition christian --timezone Europe/London

      # Auto-enable
      max-code sabbath configure --tradition jewish --auto
    """
    manager = SabbathManager()

    console.print("\n[bold cyan]Sabbath Configuration[/bold cyan]\n")

    # Calculate next Sabbath
    tradition_enum = SabbathTradition(tradition)

    try:
        start, end = manager.calculate_sabbath_window(
            tradition_enum,
            timezone,
            latitude,
            longitude
        )

        # Display configuration
        console.print(f"Tradition: [yellow]{tradition.title()}[/yellow]")
        console.print(f"Timezone: [white]{timezone}[/white]")

        if tradition == "jewish":
            console.print(f"Location: [white]Lat {latitude}, Lon {longitude}[/white]")
            console.print("[dim]Sunset times calculated using astronomy[/dim]")

        console.print()
        console.print(f"Next Sabbath: [cyan]{start.strftime('%A, %B %d, %Y at %H:%M %Z')}[/cyan]")
        console.print(f"Ends: [cyan]{end.strftime('%A, %B %d, %Y at %H:%M %Z')}[/cyan]")

        duration_hours = (end - start).total_seconds() / 3600
        console.print(f"Duration: [white]{duration_hours:.1f} hours[/white]")

        console.print()

        # Schedule auto-sabbath if requested
        if auto:
            manager.schedule_auto_sabbath(
                tradition_enum,
                timezone,
                latitude,
                longitude
            )
            console.print()
        else:
            console.print("[dim]Auto-enable not configured. Use --auto to enable automatic Sabbath mode.[/dim]")
            console.print()

        # Biblical wisdom
        if tradition == "jewish":
            console.print(Panel(
                "[italic]Remember the Sabbath day, to keep it holy.[/italic]\n"
                "— Exodus 20:8",
                border_style="cyan",
                title="[bold]Biblical Foundation[/bold]"
            ))
        elif tradition == "christian":
            console.print(Panel(
                "[italic]On the first day of the week, we came together to break bread.[/italic]\n"
                "— Acts 20:7",
                border_style="cyan",
                title="[bold]Biblical Foundation[/bold]"
            ))

        console.print()

    except Exception as e:
        console.print(f"\n[red]✗ Configuration failed: {e}[/red]\n")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@sabbath.command()
def enable():
    """
    Manually enable Sabbath mode.

    Enters graceful degradation mode regardless of schedule.

    \b
    Effects:
    - Disables non-essential commands (predict, learn)
    - MAXIMUS consciousness enters rest state
    - Minimal UI mode active
    - Essential commands remain available

    \b
    Biblical Principle:
    "Six days you shall labor, but on the seventh day you shall rest" (Ex 34:21)
    """
    manager = SabbathManager()

    console.print()
    manager.enable_sabbath_mode()


@sabbath.command()
def disable():
    """
    Manually disable Sabbath mode.

    Exits graceful degradation and restores full functionality.
    """
    manager = SabbathManager()

    console.print()
    manager.disable_sabbath_mode()


@sabbath.command()
def status():
    """
    Show Sabbath mode status.

    Displays current status, next scheduled Sabbath, and configuration.
    """
    manager = SabbathManager()
    status = manager.get_status()

    console.print("\n[bold cyan]Sabbath Mode Status[/bold cyan]\n")

    # Active status
    if status.is_active:
        console.print(f"Status: [green]ACTIVE[/green]")
        if status.end_time:
            console.print(f"Ends: [cyan]{status.end_time.strftime('%Y-%m-%d %H:%M %Z')}[/cyan]")

        console.print()
        console.print("[bold yellow]During Sabbath:[/bold yellow]")
        console.print("  [green]✓[/green] Essential commands (health, status, config)")
        console.print("  [red]✗[/red] Non-essential commands (predict, learn)")
        console.print("  [yellow]⚠[/yellow] MAXIMUS consciousness in rest state")
        console.print()
        console.print("[dim]Isaiah 58:13 - 'Call the Sabbath a delight'[/dim]")

    else:
        console.print(f"Status: [yellow]INACTIVE[/yellow]")

        if status.next_sabbath:
            console.print(f"Next Sabbath: [cyan]{status.next_sabbath.strftime('%A, %B %d at %H:%M %Z')}[/cyan]")

    console.print()

    # Configuration
    if status.tradition:
        console.print("[bold yellow]Configuration:[/bold yellow]")
        console.print(f"  Tradition: [white]{status.tradition.value.title()}[/white]")
        console.print(f"  Auto-schedule: [{'green' if status.is_scheduled else 'yellow'}]{'✓ Enabled' if status.is_scheduled else '✗ Disabled'}[/{'green' if status.is_scheduled else 'yellow'}]")
    else:
        console.print("[yellow]No Sabbath schedule configured.[/yellow]")
        console.print("Use: [cyan]max-code sabbath configure[/cyan]")

    console.print()


if __name__ == '__main__':
    sabbath()
