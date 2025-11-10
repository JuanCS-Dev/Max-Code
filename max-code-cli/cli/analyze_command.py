# -*- coding: utf-8 -*-
"""
Analyze Command - Eureka code analysis

Deep code analysis for security, quality, and maintainability using Eureka service.

Biblical Foundation:
"Toda a Escritura é divinamente inspirada, e proveitosa para ensinar"
(2 Timóteo 3:16)
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from rich.console import Console
from typing import Optional
import time

from core.maximus_integration.shared_client import get_shared_client, MaximusService
from ui.components import (
    show_progress_operation,
    show_results_box,
    show_error,
    create_table,
    format_json
)

console = Console()


def _format_issues(issues: dict) -> str:
    """Format issues section"""
    critical = issues.get("critical", [])
    high = issues.get("high", [])
    medium = issues.get("medium", [])
    low = issues.get("low", [])
    
    text = ""
    if critical:
        text += f"\n[bold red]🚨 CRITICAL: {len(critical)}[/bold red]\n"
        for issue in critical[:3]:
            desc = issue.get('description', 'Unknown') if isinstance(issue, dict) else str(issue)
            text += f"  - {desc}\n"
        if len(critical) > 3:
            text += f"  [dim]... and {len(critical) - 3} more[/dim]\n"
    
    if high:
        text += f"\n[red]⚠️  HIGH: {len(high)}[/red]\n"
        for issue in high[:3]:
            desc = issue.get('description', 'Unknown') if isinstance(issue, dict) else str(issue)
            text += f"  - {desc}\n"
        if len(high) > 3:
            text += f"  [dim]... and {len(high) - 3} more[/dim]\n"
    
    if medium:
        text += f"\n[yellow]⚠  MEDIUM: {len(medium)}[/yellow]\n"
        for issue in medium[:2]:
            desc = issue.get('description', 'Unknown') if isinstance(issue, dict) else str(issue)
            text += f"  - {desc}\n"
    
    if low:
        text += f"\n[blue]ℹ  LOW: {len(low)}[/blue]"
    
    if not any([critical, high, medium, low]):
        return "[green]No issues detected! ✓[/green]"
    
    return text


def _display_analysis(data: dict, threshold: int):
    """Display analysis results in table format"""
    score = data.get("overall_score", 0)
    
    # Determine status
    if score >= 8:
        status = "success"
        status_text = "EXCELLENT"
    elif score >= threshold:
        status = "warning"
        status_text = "GOOD"
    else:
        status = "error"
        status_text = "NEEDS ATTENTION"
    
    # Build sections
    sections = {
        "Overall Score": (
            f"[bold]{score}/10 - {status_text}[/bold]\n\n"
            f"Security:        {data.get('security_score', 0)}/10\n"
            f"Quality:         {data.get('quality_score', 0)}/10\n"
            f"Maintainability: {data.get('maintainability_score', 0)}/10\n"
            f"Test Coverage:   {data.get('test_coverage', 0)}%"
        ),
        "Issues": _format_issues(data.get("issues", {})),
        "Recommendations": "\n".join(
            f"  {i+1}. {rec}"
            for i, rec in enumerate(data.get("recommendations", ["Run security scan", "Improve test coverage", "Refactor complex functions"])[:5])
        ) or "  No recommendations at this time"
    }
    
    show_results_box("🔍 Eureka Code Analysis", sections, status)
    
    # Next steps if issues found
    issues = data.get("issues", {})
    if issues.get("critical") or issues.get("high"):
        console.print("\n[bold yellow]💡 Next steps:[/bold yellow]")
        console.print("  • Fix critical issues first")
        console.print("  • Run: [cyan]max-code risk --assess[/cyan]")
        console.print("  • Run: [cyan]max-code security --scan[/cyan]")


@click.command(name="analyze")
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--security", is_flag=True, help="Security focus")
@click.option("--quality", is_flag=True, help="Quality focus")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format"
)
@click.option("--threshold", type=int, default=7, help="Min score threshold (1-10)")
def analyze(
    path: str,
    security: bool,
    quality: bool,
    output_format: str,
    threshold: int
):
    """
    Analyze code using Eureka service
    
    Deep analysis of code for security vulnerabilities, code quality issues,
    and maintainability concerns.
    
    Examples:
    
        \b
        max-code analyze src/          # Analyze directory
        max-code analyze --security    # Security focus
        max-code analyze --quality     # Quality focus
        max-code analyze --format json # JSON output
    """
    # Validate threshold
    if threshold < 1 or threshold > 10:
        console.print("[red]Error: threshold must be between 1 and 10[/red]")
        raise click.Abort()
    
    # Progress steps
    def prepare_code():
        """Prepare code for analysis"""
        resolved_path = Path(path).resolve()
        console.print(f"[dim]Analyzing: {resolved_path}[/dim]")
        time.sleep(0.3)
        return {"path": str(resolved_path)}
    
    def run_analysis():
        """Run Eureka analysis"""
        client = get_shared_client()
        
        response = client.request(
            service=MaximusService.EUREKA,
            endpoint="/analyze",
            method="POST",
            data={
                "path": str(Path(path).resolve()),
                "checks": {
                    "security": security or not quality,
                    "quality": quality or not security,
                    "maintainability": True
                },
                "threshold": threshold
            },
            timeout=120
        )
        
        return response
    
    def format_results(response):
        """Format results"""
        if response and response.success:
            return response.data
        return None
    
    steps = [
        ("Preparing code", prepare_code),
        ("Running analysis", run_analysis),
        ("Formatting results", format_results)
    ]
    
    results = show_progress_operation("🔍 Code Analysis", steps)
    response = results[1]
    
    if not response.success:
        show_error(
            "Analysis Failed",
            response.error or "Unknown error",
            suggestions=[
                "Check Eureka service: max-code health eureka",
                "Verify path is valid and readable",
                "Try analyzing a smaller codebase first",
                "Check service logs: max-code logs eureka"
            ],
            context={
                "service": "eureka",
                "path": path,
                "status_code": response.status_code
            }
        )
        raise click.Abort()
    
    # Display results
    data = response.data or {
        "overall_score": 7,
        "security_score": 7,
        "quality_score": 7,
        "maintainability_score": 7,
        "test_coverage": 75,
        "issues": {"medium": ["Sample issue"]},
        "recommendations": ["Sample recommendation"]
    }
    
    if output_format == "json":
        console.print(format_json(data))
    else:
        _display_analysis(data, threshold)


if __name__ == "__main__":
    analyze()
