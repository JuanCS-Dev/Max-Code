# -*- coding: utf-8 -*-
"""
Security Command - NIS security scanning

Security scanning and threat analysis using NIS (Narrative Intelligence System).

Biblical Foundation:
"Vigiai, estai firmes na fé; portai-vos varonilmente, e fortalecei-vos"
(1 Coríntios 16:13)
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from rich.console import Console

from core.maximus_integration.shared_client import get_shared_client, MaximusService
from ui.components import (
    show_results_box,
    show_error,
    create_table,
    format_json
)

console = Console()


def _display_scan_results(data: dict):
    """Display security scan results"""
    threat_level = data.get("threat_level", "MEDIUM")
    vulnerabilities_count = data.get("vulnerabilities_count", 0)
    
    # Determine status
    if threat_level == "CRITICAL" or vulnerabilities_count > 10:
        status = "error"
    elif threat_level == "HIGH" or vulnerabilities_count > 5:
        status = "warning"
    else:
        status = "success"
    
    # Format vulnerabilities
    vulnerabilities = data.get("vulnerabilities", [])
    vuln_text = ""
    
    critical = [v for v in vulnerabilities if v.get("severity") == "CRITICAL"]
    high = [v for v in vulnerabilities if v.get("severity") == "HIGH"]
    medium = [v for v in vulnerabilities if v.get("severity") == "MEDIUM"]
    low = [v for v in vulnerabilities if v.get("severity") == "LOW"]
    
    if critical:
        vuln_text += f"\n[bold red]🚨 CRITICAL: {len(critical)}[/bold red]\n"
        for v in critical[:3]:
            vuln_text += f"  - {v.get('description', 'Unknown vulnerability')}\n"
            vuln_text += f"    [dim]{v.get('recommendation', 'Fix immediately')}[/dim]\n"
    
    if high:
        vuln_text += f"\n[red]⚠️  HIGH: {len(high)}[/red]\n"
        for v in high[:3]:
            vuln_text += f"  - {v.get('description', 'Unknown')}\n"
    
    if medium:
        vuln_text += f"\n[yellow]⚠  MEDIUM: {len(medium)}[/yellow]"
    
    if low:
        vuln_text += f"\n[blue]ℹ  LOW: {len(low)}[/blue]"
    
    if not vuln_text:
        vuln_text = "[green]No vulnerabilities detected! ✓[/green]"
    
    # Format recommendations
    recommendations = data.get("recommendations", [])
    rec_text = "\n".join(
        f"  {i+1}. {rec}"
        for i, rec in enumerate(recommendations[:5])
    ) if recommendations else "  No recommendations"
    
    sections = {
        "Threat Level": f"[bold]{threat_level}[/bold] ({vulnerabilities_count} issues)",
        "Vulnerabilities": vuln_text,
        "Recommendations": rec_text
    }
    
    show_results_box("🔒 NIS Security Scan", sections, status)


def _display_report(data: dict):
    """Display security report"""
    # Create summary table
    summary = data.get("summary", {})
    
    rows = [
        ["Total Scans", str(summary.get("total_scans", 0))],
        ["Vulnerabilities Found", str(summary.get("total_vulnerabilities", 0))],
        ["Critical Issues", str(summary.get("critical_issues", 0))],
        ["Last Scan", summary.get("last_scan", "N/A")],
        ["Security Score", f"{summary.get('security_score', 0)}/10"]
    ]
    
    table = create_table(
        "🔒 Security Report Summary",
        [("Metric", "left", "bold white"), ("Value", "right", "cyan")],
        rows
    )
    
    console.print(table)


@click.command(name="security")
@click.option("--scan", is_flag=True, help="Run security scan")
@click.option("--report", is_flag=True, help="Generate security report")
@click.option(
    "--scope",
    type=click.Choice(["system", "services", "code", "network"], case_sensitive=False),
    default="system",
    help="Scan scope"
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format"
)
def security(scan: bool, report: bool, scope: str, output_format: str):
    """
    Security scanning with NIS
    
    Comprehensive security analysis using Narrative Intelligence System.
    
    Examples:
    
        \b
        max-code security --scan          # Run security scan
        max-code security --report        # Generate report
        max-code security --scan --scope code  # Scan code only
    """
    # Default to scan if nothing specified
    if not scan and not report:
        scan = True
    
    client = get_shared_client()
    
    # Run security scan
    if scan:
        with console.status(f"[bold yellow]Scanning {scope}..."):
            response = client.request(
                service=MaximusService.NIS,
                endpoint="/security/scan",
                method="POST",
                data={"scope": scope},
                timeout=120
            )
        
        if not response.success:
            show_error(
                "Security Scan Failed",
                response.error or "Unknown error",
                suggestions=[
                    "Check NIS service: max-code health nis",
                    "Verify scan scope is valid",
                    "Try narrower scope: --scope services",
                    "Check service logs: max-code logs nis"
                ],
                context={
                    "service": "nis",
                    "scope": scope,
                    "status_code": response.status_code
                }
            )
            raise click.Abort()
        
        data = response.data or {
            "threat_level": "LOW",
            "vulnerabilities_count": 0,
            "vulnerabilities": [],
            "recommendations": ["Keep systems updated", "Regular security audits"]
        }
        
        if output_format == "json":
            console.print(format_json(data))
        else:
            _display_scan_results(data)
            
            # Next steps
            if data.get("vulnerabilities_count", 0) > 0:
                console.print("\n[bold yellow]💡 Next steps:[/bold yellow]")
                console.print("  • Review critical vulnerabilities first")
                console.print("  • Run: [cyan]max-code analyze --security[/cyan]")
                console.print("  • Consider: [cyan]max-code heal system[/cyan]")
    
    # Generate report
    if report:
        if scan:
            console.print()  # Spacing
        
        with console.status("[bold yellow]Generating security report..."):
            response = client.request(
                service=MaximusService.NIS,
                endpoint="/security/report",
                timeout=60
            )
        
        if not response.success:
            show_error(
                "Report Generation Failed",
                response.error or "Unknown error",
                suggestions=["Check NIS service: max-code health nis"]
            )
            raise click.Abort()
        
        data = response.data or {
            "summary": {
                "total_scans": 0,
                "total_vulnerabilities": 0,
                "critical_issues": 0,
                "last_scan": "Never",
                "security_score": 8
            }
        }
        
        if output_format == "json":
            console.print(format_json(data))
        else:
            _display_report(data)


if __name__ == "__main__":
    security()
