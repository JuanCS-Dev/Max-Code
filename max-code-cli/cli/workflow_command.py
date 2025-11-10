# -*- coding: utf-8 -*-
"""
Workflow Command - Orchestrator workflow management

Manage and execute MAXIMUS AI workflows using Orchestrator service.

Biblical Foundation:
"Tudo tem o seu tempo determinado, e há tempo para todo o propósito debaixo do céu"
(Eclesiastes 3:1)
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from rich.console import Console
from typing import Optional

from core.maximus_integration.shared_client import get_shared_client, MaximusService
from ui.components import (
    show_results_box,
    show_error,
    create_table,
    format_json,
    confirm_action
)

console = Console()


def _display_workflows(workflows: list):
    """Display workflows as table"""
    if not workflows:
        console.print("[yellow]No workflows found[/yellow]")
        return
    
    # Create table
    rows = []
    for wf in workflows:
        name = wf.get("name", "Unknown")
        status = wf.get("status", "Unknown")
        description = wf.get("description", "-")
        
        # Status color
        if status == "active":
            status_display = "[green]Active[/green]"
        elif status == "paused":
            status_display = "[yellow]Paused[/yellow]"
        else:
            status_display = "[dim]Inactive[/dim]"
        
        rows.append([name, status_display, description[:50]])
    
    table = create_table(
        "🔄 MAXIMUS Workflows",
        [
            ("Name", "left", "bold white"),
            ("Status", "center", ""),
            ("Description", "left", "dim")
        ],
        rows
    )
    
    console.print(table)


def _display_workflow_status(status_data: dict):
    """Display workflow execution status"""
    workflow_name = status_data.get("workflow", "Unknown")
    status = status_data.get("status", "Unknown")
    progress = status_data.get("progress", 0)
    
    # Status determination
    if status == "completed":
        status_type = "success"
        status_text = "COMPLETED"
    elif status == "running":
        status_type = "info"
        status_text = "RUNNING"
    elif status == "failed":
        status_type = "error"
        status_text = "FAILED"
    else:
        status_type = "warning"
        status_text = status.upper()
    
    # Format steps
    steps = status_data.get("steps", [])
    steps_text = "\n".join(
        f"  {i+1}. [{('green' if s.get('status') == 'completed' else 'yellow' if s.get('status') == 'running' else 'dim')}]"
        f"{s.get('name', 'Unknown step')} - {s.get('status', 'pending')}[/]"
        for i, s in enumerate(steps)
    ) if steps else "  No step information available"
    
    sections = {
        "Workflow": f"[bold]{workflow_name}[/bold]",
        "Status": f"{status_text} ({progress}%)",
        "Steps": steps_text
    }
    
    show_results_box("🔄 Workflow Status", sections, status_type)


@click.command(name="workflow")
@click.argument(
    "action",
    type=click.Choice(["list", "run", "status", "stop"], case_sensitive=False)
)
@click.argument("workflow_name", required=False)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format"
)
def workflow(
    action: str,
    workflow_name: Optional[str],
    output_format: str
):
    """
    Manage MAXIMUS workflows
    
    Control workflow execution and monitoring via Orchestrator service.
    
    Examples:
    
        \b
        max-code workflow list                # List workflows
        max-code workflow run analysis        # Run workflow
        max-code workflow status analysis     # Check status
        max-code workflow stop analysis       # Stop workflow
    """
    client = get_shared_client()
    action = action.lower()
    
    # List workflows
    if action == "list":
        with console.status("[bold yellow]Fetching workflows..."):
            response = client.request(
                service=MaximusService.ORCHESTRATOR,
                endpoint="/workflows",
                timeout=30
            )
        
        if not response.success:
            show_error(
                "Failed to List Workflows",
                response.error or "Unknown error",
                suggestions=[
                    "Check Orchestrator: max-code health orchestrator",
                    "Verify service is responding"
                ]
            )
            raise click.Abort()
        
        workflows = response.data.get("workflows", []) if response.data else []
        
        if output_format == "json":
            console.print(format_json({"workflows": workflows}))
        else:
            _display_workflows(workflows)
    
    # Run workflow
    elif action == "run":
        if not workflow_name:
            console.print("[red]Error: workflow name required for 'run' action[/red]")
            raise click.Abort()
        
        # Confirm
        if not confirm_action(f"Run workflow '{workflow_name}'?", default=True):
            console.print("[yellow]Cancelled[/yellow]")
            return
        
        with console.status(f"[bold yellow]Starting workflow '{workflow_name}'..."):
            response = client.request(
                service=MaximusService.ORCHESTRATOR,
                endpoint=f"/workflows/{workflow_name}/run",
                method="POST",
                timeout=60
            )
        
        if not response.success:
            show_error(
                "Failed to Run Workflow",
                response.error or "Unknown error",
                suggestions=[
                    f"Verify workflow '{workflow_name}' exists",
                    "Check orchestrator logs: max-code logs orchestrator"
                ]
            )
            raise click.Abort()
        
        console.print(f"[green]✓ Workflow '{workflow_name}' started successfully[/green]")
        console.print(f"\n[dim]Check status with: max-code workflow status {workflow_name}[/dim]")
    
    # Check status
    elif action == "status":
        if not workflow_name:
            console.print("[red]Error: workflow name required for 'status' action[/red]")
            raise click.Abort()
        
        with console.status(f"[bold yellow]Checking workflow status..."):
            response = client.request(
                service=MaximusService.ORCHESTRATOR,
                endpoint=f"/workflows/{workflow_name}/status",
                timeout=30
            )
        
        if not response.success:
            show_error(
                "Failed to Get Status",
                response.error or "Unknown error"
            )
            raise click.Abort()
        
        status_data = response.data or {
            "workflow": workflow_name,
            "status": "unknown",
            "progress": 0,
            "steps": []
        }
        
        if output_format == "json":
            console.print(format_json(status_data))
        else:
            _display_workflow_status(status_data)
    
    # Stop workflow
    elif action == "stop":
        if not workflow_name:
            console.print("[red]Error: workflow name required for 'stop' action[/red]")
            raise click.Abort()
        
        if not confirm_action(f"Stop workflow '{workflow_name}'?", default=False):
            console.print("[yellow]Cancelled[/yellow]")
            return
        
        with console.status(f"[bold yellow]Stopping workflow..."):
            response = client.request(
                service=MaximusService.ORCHESTRATOR,
                endpoint=f"/workflows/{workflow_name}/stop",
                method="POST",
                timeout=30
            )
        
        if not response.success:
            show_error(
                "Failed to Stop Workflow",
                response.error or "Unknown error"
            )
            raise click.Abort()
        
        console.print(f"[green]✓ Workflow '{workflow_name}' stopped[/green]")


if __name__ == "__main__":
    workflow()
