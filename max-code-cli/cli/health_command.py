# -*- coding: utf-8 -*-
"""Health Check Command - Enhanced with Foundation Components

Verifies connectivity to all MAXIMUS services.
Tests circuit breaker, retry logic, and service availability.

Enhanced Features:
- SharedMaximusClient integration
- Rich UI components (Gemini-style)
- Watch mode support
- JSON/YAML output
- Detailed metrics

Biblical Foundation:
"E disse-lhes: Ide por todo o mundo, pregai o evangelho a toda criatura."
(Marcos 16:15)
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
import time
from typing import Optional, List, Dict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Foundation imports
from core.maximus_integration.shared_client import (
    get_shared_client,
    MaximusService,
    ServiceResponse
)
from ui.components import (
    create_table,
    show_results_box,
    show_error,
    format_json,
    format_yaml,
    COLORS
)
from config.settings import get_settings

console = Console()


# Service descriptions (enhanced metadata)
SERVICE_DESCRIPTIONS = {
    "core": "Consciousness & Safety",
    "penelope": "7 Fruits & Healing",
    "maba": "Browser Agent",
    "nis": "Narrative Intelligence",
    "orchestrator": "Workflow Coordination",
    "eureka": "Insights & Discovery",
    "oraculo": "Predictions",
    "atlas": "Context & Environment"
}


def check_all_services(timeout: int = 10) -> List[ServiceResponse]:
    """Check health of all MAXIMUS services"""
    client = get_shared_client()
    return client.health_check_all(timeout=timeout)


def check_single_service(service_name: str, timeout: int = 10) -> ServiceResponse:
    """Check health of single service"""
    client = get_shared_client()
    
    try:
        service_enum = MaximusService(service_name.lower())
    except ValueError:
        return ServiceResponse(
            success=False,
            error=f"Unknown service: {service_name}",
            service=service_name
        )
    
    return client.health_check(service_enum, timeout=timeout)


def display_table_format(results: List[ServiceResponse], detailed: bool):
    """Display results as rich table"""
    # Summary stats
    total = len(results)
    healthy = sum(1 for r in results if r.success)
    unhealthy = total - healthy
    
    # Average response time
    response_times = [r.response_time_ms for r in results if r.response_time_ms]
    avg_response = sum(response_times) / len(response_times) if response_times else 0
    
    # Build table
    columns = [
        ("Service", "left", "bold white"),
        ("Status", "center", ""),
        ("Response Time", "right", ""),
        ("Description", "left", "")
    ]
    
    if detailed:
        columns.append(("Details", "left", "dim"))
    
    rows = []
    
    # Add rows
    for result in sorted(results, key=lambda x: x.service or ""):
        service = result.service or "unknown"
        
        # Status display
        if result.success:
            status_display = "✓ UP"
            style = "green"
        else:
            status_display = "✗ DOWN"
            style = "red"
        
        # Response time display
        if result.response_time_ms:
            response_ms = result.response_time_ms
            if response_ms < 50:
                response_display = f"{response_ms:.0f}ms"
                response_style = "green"
            elif response_ms < 150:
                response_display = f"{response_ms:.0f}ms"
                response_style = "yellow"
            else:
                response_display = f"{response_ms:.0f}ms"
                response_style = "red"
        else:
            response_display = "-"
            response_style = "dim"
        
        # Description
        description = SERVICE_DESCRIPTIONS.get(service, "Unknown service")
        
        # Build row
        row = [
            service.upper(),
            f"[{style}]{status_display}[/{style}]",
            f"[{response_style}]{response_display}[/{response_style}]",
            f"[dim]{description}[/dim]"
        ]
        
        if detailed and result.data:
            # Show additional details
            details_parts = []
            if "uptime" in result.data:
                details_parts.append(f"Uptime: {result.data['uptime']}")
            if "version" in result.data:
                details_parts.append(f"v{result.data['version']}")
            if "memory" in result.data:
                details_parts.append(f"Mem: {result.data['memory']}")
            
            details_str = " | ".join(details_parts) if details_parts else "-"
            row.append(details_str)
        elif detailed:
            row.append(result.error[:50] if result.error else "-")
        
        rows.append(row)
    
    # Create and print table
    table = create_table(
        "🏥 MAXIMUS Service Health",
        columns,
        rows
    )
    
    console.print(table)
    
    # Summary
    console.print()
    summary = f"[bold white]Summary:[/bold white] {healthy}/{total} healthy"
    if unhealthy > 0:
        summary += f" | [yellow]{unhealthy} issues[/yellow]"
    if avg_response:
        summary += f" | Avg response: {avg_response:.1f}ms"
    console.print(summary)
    
    # Contextual next steps
    if unhealthy > 0:
        console.print("\n[bold yellow]💡 Next steps:[/bold yellow]")
        console.print("  • Check logs: [cyan]max-code logs <service>[/cyan]")
        console.print("  • View details: [cyan]max-code health <service> --detailed[/cyan]")
        console.print("  • Monitor: [cyan]max-code health --watch[/cyan]")
    
    # Circuit breaker info
    console.print("\n[dim]Circuit Breaker: 3 retries with exponential backoff | Timeout: 30s default[/dim]")


def display_json_format(results: List[ServiceResponse]):
    """Display results as JSON"""
    data = {}
    for result in results:
        service = result.service or "unknown"
        data[service] = {
            "success": result.success,
            "status": "healthy" if result.success else "unhealthy",
            "response_time_ms": result.response_time_ms,
            "data": result.data,
            "error": result.error
        }
    
    syntax = format_json(data)
    console.print(syntax)


def display_yaml_format(results: List[ServiceResponse]):
    """Display results as YAML"""
    data = {}
    for result in results:
        service = result.service or "unknown"
        data[service] = {
            "success": result.success,
            "status": "healthy" if result.success else "unhealthy",
            "response_time_ms": result.response_time_ms,
            "data": result.data,
            "error": result.error
        }
    
    syntax = format_yaml(data)
    console.print(syntax)


def watch_mode(
    service_filter: Optional[str],
    detailed: bool,
    timeout: int,
    interval: int = 5
):
    """Watch mode with auto-refresh"""
    console.print("[bold cyan]🔍 Watch Mode[/bold cyan] (press Ctrl+C to stop)\n")
    
    try:
        while True:
            # Clear screen
            console.clear()
            
            # Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            console.print(f"[bold cyan]Last update: {timestamp}[/bold cyan]\n")
            
            # Fetch and display
            if service_filter:
                results = [check_single_service(service_filter, timeout)]
            else:
                results = check_all_services(timeout)
            
            display_table_format(results, detailed)
            
            # Wait
            time.sleep(interval)
    
    except KeyboardInterrupt:
        console.print("\n\n[bold green]✓ Stopped monitoring[/bold green]")


@click.command(name="health")
@click.argument("service", required=False, default=None)
@click.option("--detailed", "-d", is_flag=True, help="Show detailed metrics")
@click.option("--watch", "-w", is_flag=True, help="Watch mode (refresh every 5s)")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json", "yaml"]),
    default="table",
    help="Output format"
)
@click.option("--timeout", type=int, default=10, help="Request timeout in seconds")
@click.option("--interval", type=int, default=5, help="Watch mode refresh interval")
def health(
    service: Optional[str],
    detailed: bool,
    watch: bool,
    output_format: str,
    timeout: int,
    interval: int
):
    """Check health status of MAXIMUS services
    
    Examples:
    
        \b
        max-code health              # All services
        max-code health core         # Specific service
        max-code health --watch      # Monitor mode
        max-code health --format json  # JSON output
    """
    # Validate service name if provided
    if service:
        valid_services = [s.value for s in MaximusService]
        if service.lower() not in valid_services:
            show_error(
                "Invalid Service",
                f"Service '{service}' not found",
                suggestions=[
                    f"Available services: {', '.join(valid_services)}",
                    "Run 'max-code health' to check all services"
                ],
                context={"requested": service}
            )
            raise click.Abort()
    
    # Watch mode
    if watch:
        watch_mode(service, detailed, timeout, interval)
        return
    
    # Header
    console.print("\n[bold cyan]🏥 MAXIMUS Services Health Check[/bold cyan]\n")
    
    # Fetch data
    with console.status("[bold green]Checking services...") as status:
        if service:
            results = [check_single_service(service, timeout)]
        else:
            results = check_all_services(timeout)
    
    # Success indicator
    console.print("[bold green]✓ Health check complete!\n")
    
    # Display based on format
    if output_format == "json":
        display_json_format(results)
    elif output_format == "yaml":
        display_yaml_format(results)
    else:
        display_table_format(results, detailed)
    
    console.print()


if __name__ == "__main__":
    health()
