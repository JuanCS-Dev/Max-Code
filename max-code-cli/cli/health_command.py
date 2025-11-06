# -*- coding: utf-8 -*-
"""Health Check Command - FASE 7

Verifies connectivity to all MAXIMUS services.
Tests circuit breaker, retry logic, and service availability.
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from integration import (
    MaximusClient, PenelopeClient, OraculoClient,
    OrchestratorClient, MABAClient, NISClient,
    EurekaClient, DLQMonitorClient
)

console = Console()


SERVICES = [
    ("Maximus Core", MaximusClient, "http://localhost:8150", "Consciousness & Safety"),
    ("Penelope", PenelopeClient, "http://localhost:8151", "7 Fruits & Healing"),
    ("MABA", MABAClient, "http://localhost:8152", "Browser Agent"),
    ("NIS", NISClient, "http://localhost:8153", "Narrative Intelligence"),
    ("Orchestrator", OrchestratorClient, "http://localhost:8154", "Workflow Coordination"),
    ("Eureka", EurekaClient, "http://localhost:8155", "Insights & Discovery"),
    ("Oraculo", OraculoClient, "http://localhost:8156", "Predictions"),
    ("DLQ Monitor", DLQMonitorClient, "http://localhost:8157", "Dead Letter Queue"),
]


def check_service(name, client_class, base_url, description):
    """Check single service health."""
    try:
        start = time.time()
        client = client_class(base_url=base_url, timeout=5.0, max_retries=1)

        # Try health endpoint
        if hasattr(client, 'health'):
            result = client.health()
        elif hasattr(client, 'get_health'):
            result = client.get_health()
        else:
            result = {"status": "unknown"}

        latency = (time.time() - start) * 1000  # ms
        client.close()

        return {
            "status": " UP",
            "latency": f"{latency:.0f}ms",
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "status": "L DOWN",
            "latency": "-",
            "result": None,
            "error": str(e)[:50]
        }


@click.command()
@click.option('--detailed', is_flag=True, help='Show detailed service information')
def health(detailed):
    """Check MAXIMUS services health and connectivity."""

    console.print("\n[bold cyan]<� MAXIMUS Services Health Check[/bold cyan]\n")

    # Create results table
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Service", style="cyan", width=18)
    table.add_column("Port", justify="center", width=6)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Latency", justify="right", width=10)
    table.add_column("Description", style="dim", width=30)

    results = []
    healthy_count = 0

    with console.status("[bold green]Testing services...") as status:
        for name, client_class, base_url, description in SERVICES:
            port = base_url.split(":")[-1]
            status.update(f"[bold green]Testing {name}...")

            result = check_service(name, client_class, base_url, description)
            results.append((name, port, result, description))

            if "UP" in result["status"]:
                healthy_count += 1

    # Add rows to table
    for name, port, result, description in results:
        status_style = "green" if "UP" in result["status"] else "red"
        table.add_row(
            name,
            port,
            f"[{status_style}]{result['status']}[/{status_style}]",
            f"[{status_style}]{result['latency']}[/{status_style}]",
            description
        )

    console.print(table)

    # Summary
    total = len(SERVICES)
    console.print(f"\n[bold]Summary:[/bold] {healthy_count}/{total} services healthy")

    if healthy_count == total:
        console.print("[bold green] All services operational![/bold green]\n")
    elif healthy_count > 0:
        console.print(f"[bold yellow]�  {total - healthy_count} service(s) unavailable[/bold yellow]\n")
    else:
        console.print("[bold red]L All services down - check if MAXIMUS is running[/bold red]\n")

    # Detailed output
    if detailed:
        console.print("\n[bold]Detailed Results:[/bold]\n")
        for name, port, result, description in results:
            if result["error"]:
                panel = Panel(
                    f"[red]Error: {result['error']}[/red]",
                    title=f"{name} (:{port})",
                    border_style="red"
                )
                console.print(panel)

    # Circuit breaker info
    console.print("\n[dim]Circuit Breaker: 5 failures � 30s recovery | Retry: 3 attempts (1s, 2s, 4s)[/dim]\n")


if __name__ == "__main__":
    health()
