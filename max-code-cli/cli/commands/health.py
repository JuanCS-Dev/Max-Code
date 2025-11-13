"""
Health Check Command - MAXIMUS Services Monitor

Command: max-code health [--detailed]

Features:
- Real-time service health monitoring
- Latency measurement
- Circuit breaker status
- Beautiful Rich UI table
- Detailed error reporting
"""

import click
import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.health_check import HealthChecker, ServiceStatus, MAXIMUS_SERVICES


console = Console()


def create_health_table(health_map: dict, detailed: bool = False) -> Table:
    """
    Create beautiful Rich table for health check results

    Args:
        health_map: Dict mapping service_id to ServiceHealth
        detailed: Show detailed information

    Returns:
        Rich Table object
    """
    table = Table(
        title="🏥 MAXIMUS Services Health Check",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        title_style="bold magenta",
    )

    # Columns
    table.add_column("Service", style="bold", width=20)
    table.add_column("Port", justify="center", width=8)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Latency", justify="right", width=10)

    if detailed:
        table.add_column("Circuit Breaker", justify="center", width=15)
        table.add_column("Version", justify="center", width=10)
        table.add_column("Uptime", justify="right", width=10)

    table.add_column("Description", width=30)

    # Add rows
    for service_id, health in health_map.items():
        config = MAXIMUS_SERVICES[service_id]

        # Status icon and color
        if health.status == ServiceStatus.HEALTHY:
            status_icon = "✅"
            status_color = "green"
        elif health.status == ServiceStatus.DEGRADED:
            status_icon = "⚠️"
            status_color = "yellow"
        elif health.status == ServiceStatus.DOWN:
            status_icon = "❌"
            status_color = "red"
        else:
            status_icon = "❓"
            status_color = "white"

        # Latency
        latency_str = f"{health.latency_ms:.2f}ms" if health.latency_ms else "-"
        latency_color = "green" if health.latency_ms and health.latency_ms < 50 else "yellow" if health.latency_ms and health.latency_ms < 200 else "red" if health.latency_ms else "dim"

        # Description (with error if DOWN)
        description = config["description"]
        if health.status == ServiceStatus.DOWN and health.error:
            description = f"{description}\n[dim red]{health.error}[/dim red]"

        # Build row
        row = [
            health.name,
            str(health.port),
            f"{status_icon} [{status_color}]{health.status.value.upper()}[/{status_color}]",
            f"[{latency_color}]{latency_str}[/{latency_color}]",
        ]

        if detailed:
            row.extend([
                health.circuit_breaker_state or "-",
                health.version or "-",
                f"{health.uptime_seconds}s" if health.uptime_seconds else "-",
            ])

        row.append(description)

        table.add_row(*row)

    return table


def create_summary_panel(summary: dict) -> Panel:
    """
    Create summary panel with statistics

    Args:
        summary: Summary dict from HealthChecker.get_summary()

    Returns:
        Rich Panel object
    """
    # Status emoji
    status_emoji = "✅" if summary["all_healthy"] else "⚠️" if summary["degraded"] > 0 else "❌"

    # Summary text
    summary_lines = [
        f"[bold]Total Services:[/bold] {summary['total']}",
        f"[green]Healthy:[/green] {summary['healthy']}",
    ]

    if summary["degraded"] > 0:
        summary_lines.append(f"[yellow]Degraded:[/yellow] {summary['degraded']}")

    if summary["down"] > 0:
        summary_lines.append(f"[red]Down:[/red] {summary['down']}")

    if summary["avg_latency_ms"]:
        latency_color = "green" if summary["avg_latency_ms"] < 50 else "yellow" if summary["avg_latency_ms"] < 200 else "red"
        summary_lines.append(f"[bold]Avg Latency:[/bold] [{latency_color}]{summary['avg_latency_ms']:.2f}ms[/{latency_color}]")

    # Critical services down
    if summary["critical_down"]:
        summary_lines.append("")
        summary_lines.append(f"[bold red]⚠️  Critical Services Down:[/bold red]")
        for service_name in summary["critical_down"]:
            summary_lines.append(f"   • {service_name}")

    summary_text = "\n".join(summary_lines)

    return Panel(
        summary_text,
        title=f"{status_emoji} Summary",
        border_style="cyan" if summary["all_healthy"] else "yellow" if summary["degraded"] > 0 else "red",
        box=box.ROUNDED,
    )


@click.command()
@click.option('--detailed', is_flag=True, help='Show detailed information (circuit breaker, version, uptime)')
@click.option('--services', multiple=True, help='Check specific services only (can be used multiple times)')
def health(detailed: bool, services: tuple):
    """
    Check health of MAXIMUS services

    Examples:
        max-code health                          # Check all services
        max-code health --detailed               # Show detailed info
        max-code health --services maximus_core  # Check specific service
    """
    try:
        # Run async health check
        health_map, summary = asyncio.run(run_health_check(list(services) if services else None))

        # Display results
        console.print()
        table = create_health_table(health_map, detailed=detailed)
        console.print(table)
        console.print()

        summary_panel = create_summary_panel(summary)
        console.print(summary_panel)
        console.print()

        # Exit code
        if not summary["all_healthy"]:
            if summary["critical_down"]:
                console.print("[bold red]⚠️  Critical services are down! System may not function correctly.[/bold red]\n")
                sys.exit(2)  # Critical failure
            else:
                console.print("[yellow]⚠️  Some non-critical services are down.[/yellow]\n")
                sys.exit(1)  # Non-critical failure
        else:
            console.print("[bold green]✅ All services are healthy![/bold green]\n")
            sys.exit(0)  # Success

    except Exception as e:
        console.print(f"\n[bold red]❌ Error running health check:[/bold red] {str(e)}\n")
        sys.exit(3)


async def run_health_check(services: list = None):
    """
    Run health check asynchronously

    Args:
        services: Optional list of service IDs to check

    Returns:
        Tuple of (health_map, summary)
    """
    checker = HealthChecker(timeout=5.0, retries=1)
    health_map = await checker.check_all_services(services=services)
    summary = checker.get_summary(health_map)
    return health_map, summary


if __name__ == "__main__":
    health()
