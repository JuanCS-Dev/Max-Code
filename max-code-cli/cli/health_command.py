#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Check Command - MAXIMUS Services Monitoring

Verifica conectividade e saúde dos 8 serviços MAXIMUS em tempo real.

Features:
- Beautiful Rich UI with tables
- Real-time latency measurement
- Circuit breaker status
- Watch mode (auto-refresh)
- JSON/YAML output
- Critical service alerts
- Graceful degradation detection

Biblical Foundation:
"E disse-lhes: Ide por todo o mundo, pregai o evangelho a toda criatura."
(Marcos 16:15)
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import typer
import asyncio
import time
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich import box
from rich.text import Text

from core.health_check import HealthChecker, ServiceStatus, MAXIMUS_SERVICES

console = Console()
app = typer.Typer(help="🏥 MAXIMUS Services Health Check")


def create_health_table(health_map: dict, detailed: bool = False) -> Table:
    """
    Create beautiful Rich table with health status

    Args:
        health_map: Dict of service_id -> ServiceHealth
        detailed: Show detailed metrics

    Returns:
        Rich Table
    """
    table = Table(
        title="🏥 MAXIMUS Services Health Check",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
    )

    # Columns
    table.add_column("Service", style="bold white", width=20)
    table.add_column("Port", justify="center", style="dim", width=6)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Latency", justify="right", width=10)
    table.add_column("Description", style="dim", width=30)

    if detailed:
        table.add_column("Details", style="dim italic", width=25)

    # Sort by port for consistent ordering
    sorted_services = sorted(
        health_map.items(),
        key=lambda x: MAXIMUS_SERVICES[x[0]]["port"]
    )

    # Add rows
    for service_id, health in sorted_services:
        config = MAXIMUS_SERVICES[service_id]

        # Status styling
        if health.status == ServiceStatus.HEALTHY:
            status_text = Text("✅ UP", style="bold green")
            latency_style = "green" if health.latency_ms and health.latency_ms < 50 else "yellow"
        elif health.status == ServiceStatus.DEGRADED:
            status_text = Text("⚠️  DEGRADED", style="bold yellow")
            latency_style = "yellow"
        else:
            status_text = Text("❌ DOWN", style="bold red")
            latency_style = "red"

        # Latency display
        if health.latency_ms:
            latency_text = Text(f"{health.latency_ms:.0f}ms", style=latency_style)
        else:
            latency_text = Text("-", style="dim")

        # Description
        description = config["description"]
        if config.get("critical"):
            description += " [CRITICAL]"

        # Build row
        row = [
            health.name,
            str(health.port),
            status_text,
            latency_text,
            description,
        ]

        # Detailed info
        if detailed:
            details_parts = []
            if health.version:
                details_parts.append(f"v{health.version}")
            if health.uptime_seconds:
                uptime_hrs = health.uptime_seconds / 3600
                details_parts.append(f"Uptime: {uptime_hrs:.1f}h")
            if health.circuit_breaker_state:
                details_parts.append(f"CB: {health.circuit_breaker_state}")
            if health.error:
                details_parts.append(f"Error: {health.error[:20]}")

            details_str = " | ".join(details_parts) if details_parts else "-"
            row.append(details_str)

        table.add_row(*row)

    return table


def create_summary_panel(summary: dict) -> Panel:
    """
    Create summary panel with statistics

    Args:
        summary: Summary dict from HealthChecker

    Returns:
        Rich Panel
    """
    total = summary["total"]
    healthy = summary["healthy"]
    degraded = summary["degraded"]
    down = summary["down"]
    avg_latency = summary.get("avg_latency_ms")
    critical_down = summary.get("critical_down", [])

    # Build summary text
    lines = []

    # Health ratio
    health_ratio = f"{healthy}/{total}"
    if healthy == total:
        health_style = "bold green"
        health_emoji = "✅"
    elif healthy > total / 2:
        health_style = "bold yellow"
        health_emoji = "⚠️"
    else:
        health_style = "bold red"
        health_emoji = "❌"

    lines.append(
        Text.assemble(
            (health_emoji + " Services: ", "bold"),
            (health_ratio, health_style),
            (" healthy", "dim"),
        )
    )

    # Breakdown
    if degraded > 0:
        lines.append(Text(f"  ⚠️  {degraded} degraded", style="yellow"))
    if down > 0:
        lines.append(Text(f"  ❌ {down} down", style="red"))

    # Average latency
    if avg_latency:
        latency_style = "green" if avg_latency < 50 else "yellow" if avg_latency < 100 else "red"
        lines.append(
            Text.assemble(
                ("⚡ Avg Latency: ", "bold"),
                (f"{avg_latency:.1f}ms", latency_style),
            )
        )

    # Critical services
    if critical_down:
        lines.append(Text(""))
        lines.append(Text("🚨 CRITICAL SERVICES DOWN:", style="bold red"))
        for service in critical_down:
            lines.append(Text(f"  • {service}", style="red"))

    # Circuit breaker info
    lines.append(Text(""))
    lines.append(
        Text(
            "🔄 Circuit Breaker: 3 retries | 30s timeout | Exponential backoff",
            style="dim italic",
        )
    )

    # Combine lines
    summary_text = Text("\n").join(lines)

    # Panel styling based on health
    if critical_down:
        border_style = "red"
        title = "📊 Summary [CRITICAL ALERT]"
    elif healthy == total:
        border_style = "green"
        title = "📊 Summary [ALL HEALTHY]"
    else:
        border_style = "yellow"
        title = "📊 Summary [DEGRADED]"

    return Panel(
        summary_text,
        title=title,
        border_style=border_style,
        box=box.ROUNDED,
    )


def create_next_steps_panel(summary: dict) -> Optional[Panel]:
    """
    Create panel with suggested next steps

    Args:
        summary: Summary dict

    Returns:
        Rich Panel or None if all healthy
    """
    if summary["all_healthy"]:
        return None

    suggestions = []

    if summary["down"] > 0:
        suggestions.append("🔍 Check service logs: [cyan]docker logs <service>[/cyan]")
        suggestions.append("🔄 Restart services: [cyan]docker-compose restart[/cyan]")

    if summary["critical_down"]:
        suggestions.append("🚨 Critical services down - system degraded")
        suggestions.append("📞 Alert team: [cyan]max-code alert --critical[/cyan]")

    if summary.get("avg_latency_ms", 0) > 100:
        suggestions.append("⚡ High latency detected - check system load")

    suggestions.append("")
    suggestions.append("💡 More options:")
    suggestions.append("  • [cyan]max-code health --watch[/cyan] - Monitor continuously")
    suggestions.append("  • [cyan]max-code health <service> --detailed[/cyan] - Detailed view")
    suggestions.append("  • [cyan]max-code logs <service>[/cyan] - View service logs")

    text = "\n".join(suggestions)

    return Panel(
        text,
        title="💡 Recommended Actions",
        border_style="yellow",
        box=box.ROUNDED,
    )


@app.command()
def health(
    service: Optional[str] = typer.Argument(None, help="Specific service to check (optional)"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed metrics"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch mode (refresh every 5s)"),
    interval: int = typer.Option(5, "--interval", "-i", help="Watch mode refresh interval (seconds)"),
    timeout: float = typer.Option(5.0, "--timeout", "-t", help="Health check timeout (seconds)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """
    🏥 Check health status of MAXIMUS services

    Examples:

        max-code health                    # All services
        max-code health --detailed         # With details
        max-code health --watch            # Monitor mode
        max-code health maximus_core       # Single service
        max-code health --json             # JSON output
    """
    # Validate service name
    if service:
        if service not in MAXIMUS_SERVICES:
            console.print(
                f"\n[red]❌ Unknown service: {service}[/red]\n",
                style="bold",
            )
            console.print("[yellow]Available services:[/yellow]")
            for svc_id, config in MAXIMUS_SERVICES.items():
                console.print(f"  • {svc_id} - {config['name']} ({config['description']})")
            console.print()
            raise typer.Exit(1)

    # Watch mode
    if watch:
        watch_mode_impl(service, detailed, interval, timeout)
        return

    # Single check
    async def run_check():
        checker = HealthChecker(timeout=timeout)
        if service:
            # Single service
            config = MAXIMUS_SERVICES[service]
            health_result = await checker.check_service(service, config)
            return {service: health_result}, None
        else:
            # All services
            health_map = await checker.check_all_services()
            summary = checker.get_summary(health_map)
            return health_map, summary

    # Execute check
    console.print()
    with console.status("[bold green]Checking services...", spinner="dots"):
        health_map, summary = asyncio.run(run_check())

    # JSON output
    if json_output:
        import json
        output = {}
        for svc_id, health in health_map.items():
            output[svc_id] = {
                "name": health.name,
                "port": health.port,
                "status": health.status.value,
                "latency_ms": health.latency_ms,
                "error": health.error,
                "circuit_breaker": health.circuit_breaker_state,
                "version": health.version,
                "uptime_seconds": health.uptime_seconds,
            }
        if summary:
            output["_summary"] = summary
        console.print_json(json.dumps(output, indent=2))
        console.print()
        return

    # Display results
    console.print()
    table = create_health_table(health_map, detailed)
    console.print(table)

    if summary:
        console.print()
        summary_panel = create_summary_panel(summary)
        console.print(summary_panel)

        # Next steps (if needed)
        next_steps = create_next_steps_panel(summary)
        if next_steps:
            console.print()
            console.print(next_steps)

    console.print()


def watch_mode_impl(
    service: Optional[str],
    detailed: bool,
    interval: int,
    timeout: float,
):
    """
    Watch mode with live updates

    Args:
        service: Optional specific service
        detailed: Show detailed metrics
        interval: Refresh interval in seconds
        timeout: Health check timeout
    """
    console.print("\n[bold cyan]🔍 Watch Mode[/bold cyan] (press Ctrl+C to stop)\n")

    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                # Run check
                async def run_check():
                    checker = HealthChecker(timeout=timeout)
                    if service:
                        config = MAXIMUS_SERVICES[service]
                        health_result = await checker.check_service(service, config)
                        return {service: health_result}, None
                    else:
                        health_map = await checker.check_all_services()
                        summary = checker.get_summary(health_map)
                        return health_map, summary

                health_map, summary = asyncio.run(run_check())

                # Build display
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header = Text(f"Last update: {timestamp}", style="bold cyan")

                table = create_health_table(health_map, detailed)

                # Combine elements
                from rich.console import Group
                elements = [header, Text(""), table]

                if summary:
                    summary_panel = create_summary_panel(summary)
                    elements.extend([Text(""), summary_panel])

                display = Group(*elements)
                live.update(display)

                # Wait
                time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n\n[bold green]✓ Stopped monitoring[/bold green]\n")


if __name__ == "__main__":
    app()
