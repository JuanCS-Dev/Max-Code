# -*- coding: utf-8 -*-
"""
Logs Command - Stream logs from MAXIMUS services

Stream and display logs from any MAXIMUS service with filtering and follow mode.

Biblical Foundation:
"Examinai as Escrituras, porque vós cuidais ter nelas a vida eterna"
(João 5:39)
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
import time
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from core.maximus_integration.shared_client import (
    get_shared_client,
    MaximusService
)
from ui.components import show_error

console = Console()


def _validate_service(service_name: str) -> bool:
    """Validate service name"""
    valid_services = [s.value for s in MaximusService]
    return service_name.lower() in valid_services


def _print_log_line(console: Console, log_entry: dict):
    """Print single log line with styling"""
    timestamp = log_entry.get("timestamp", "")
    level = log_entry.get("level", "INFO")
    message = log_entry.get("message", "")
    
    # Color by level
    level_colors = {
        "DEBUG": "dim blue",
        "INFO": "white",
        "WARN": "yellow",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold red"
    }
    color = level_colors.get(level.upper(), "white")
    
    console.print(
        f"[dim]{timestamp}[/dim] "
        f"[{color}]{level:8s}[/{color}] "
        f"{message}"
    )


def _fetch_logs_static(
    service: str,
    tail: int,
    level: Optional[str],
    since: Optional[str]
):
    """Fetch static log snapshot"""
    client = get_shared_client()
    
    with console.status("[bold yellow]Fetching logs..."):
        # Build params
        params = {"tail": tail}
        if level:
            params["level"] = level
        if since:
            params["since"] = since
        
        try:
            service_enum = MaximusService(service.lower())
        except ValueError:
            show_error(
                "Invalid Service",
                f"Service '{service}' not found",
                suggestions=[
                    f"Available: {', '.join([s.value for s in MaximusService])}"
                ]
            )
            raise click.Abort()
        
        response = client.request(
            service=service_enum,
            endpoint="/logs",
            params=params,
            timeout=30
        )
    
    if not response.success:
        show_error(
            "Failed to Fetch Logs",
            response.error or "Unknown error",
            suggestions=[
                f"Check if service is running: max-code health {service}",
                "Verify service supports /logs endpoint",
                "Check service URL configuration"
            ],
            context={"service": service, "status_code": response.status_code}
        )
        raise click.Abort()
    
    # Display logs
    logs = response.data.get("logs", []) if response.data else []
    
    # Header
    console.print(Panel(
        f"[bold cyan]📜 Logs: {service.upper()}[/bold cyan]\n"
        f"Lines: {len(logs)} | Level: {level or 'ALL'}",
        border_style="cyan"
    ))
    console.print()
    
    # Print each log line
    if logs:
        for log_entry in logs:
            _print_log_line(console, log_entry)
    else:
        console.print("[dim]No logs found[/dim]")
    
    # Footer
    console.print(f"\n[dim]Showing last {len(logs)} lines[/dim]")
    if len(logs) >= tail:
        console.print(f"[dim](Use --tail {tail*2} to see more)[/dim]")


def _stream_logs_live(
    service: str,
    level: Optional[str],
    since: Optional[str]
):
    """Stream logs in real-time"""
    console.print(Panel(
        f"[bold cyan]📜 Live Logs: {service.upper()}[/bold cyan]\n"
        "[dim](Press Ctrl+C to stop)[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    client = get_shared_client()
    
    try:
        service_enum = MaximusService(service.lower())
    except ValueError:
        show_error(
            "Invalid Service",
            f"Service '{service}' not found"
        )
        raise click.Abort()
    
    try:
        # Polling loop (simulated streaming)
        last_timestamp = since or datetime.now().isoformat()
        
        console.print("[dim]Starting log stream...[/dim]\n")
        
        while True:
            params = {"level": level, "since": last_timestamp}
            
            response = client.request(
                service=service_enum,
                endpoint="/logs/stream",
                params=params,
                timeout=10
            )
            
            if response.success and response.data:
                logs = response.data.get("logs", [])
                for log_entry in logs:
                    _print_log_line(console, log_entry)
                    # Update last timestamp
                    if "timestamp" in log_entry:
                        last_timestamp = log_entry["timestamp"]
            elif not response.success:
                # Service offline, show error but don't crash
                console.print(f"[dim red]Connection lost... retrying...[/dim red]")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        console.print("\n[bold green]✓ Stopped streaming[/bold green]")


@click.command(name="logs")
@click.argument("service", required=True)
@click.option("--tail", "-n", type=int, default=100, help="Number of lines")
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@click.option(
    "--level",
    type=click.Choice(["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    help="Filter by log level"
)
@click.option("--since", help="Show logs since timestamp (ISO format)")
def logs(
    service: str,
    tail: int,
    follow: bool,
    level: Optional[str],
    since: Optional[str]
):
    """
    Stream logs from MAXIMUS service
    
    Examples:
    
        \b
        max-code logs eureka              # Last 100 lines
        max-code logs eureka --tail 50    # Last 50 lines
        max-code logs eureka --follow     # Live streaming
        max-code logs eureka --level ERROR  # Only errors
    """
    # Validate service
    if not _validate_service(service):
        valid_services = [s.value for s in MaximusService]
        show_error(
            "Invalid Service",
            f"Service '{service}' not found",
            suggestions=[
                f"Available services: {', '.join(valid_services)}",
                "Run 'max-code health' to see all services"
            ],
            context={"requested": service}
        )
        raise click.Abort()
    
    # Fetch or stream
    if follow:
        _stream_logs_live(service, level, since)
    else:
        _fetch_logs_static(service, tail, level, since)


if __name__ == "__main__":
    logs()
