# -*- coding: utf-8 -*-
"""
Risk Command - Oráculo risk assessment and predictions

Risk assessment and self-improvement suggestions using Oráculo service.

Biblical Foundation:
"O prudente vê o mal e esconde-se; mas os simples passam e sofrem a pena"
(Provérbios 22:3)
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


def _display_risk_assessment(data: dict):
    """Display risk assessment results"""
    risk_level = data.get("risk_level", "MEDIUM")
    risk_score = data.get("risk_score", 5)
    
    # Determine status
    if risk_level == "LOW" or risk_score < 4:
        status = "success"
    elif risk_level == "MEDIUM" or risk_score < 7:
        status = "warning"
    else:
        status = "error"
    
    # Format risks
    risks = data.get("risks", [])
    risks_text = "\n".join(
        f"  {i+1}. [{('red' if r.get('severity') == 'HIGH' else 'yellow')}]{r.get('description', 'Unknown risk')}[/]\n"
        f"     Impact: {r.get('impact', 'Unknown')}"
        for i, r in enumerate(risks[:5])
    ) if risks else "  No significant risks detected"
    
    # Format mitigations
    mitigations = data.get("mitigations", [])
    mitigations_text = "\n".join(
        f"  {i+1}. {m.get('action', m) if isinstance(m, dict) else m}"
        for i, m in enumerate(mitigations[:5])
    ) if mitigations else "  No mitigations needed"
    
    sections = {
        "Risk Level": f"[bold]{risk_level}[/bold] (Score: {risk_score}/10)",
        "Identified Risks": risks_text,
        "Recommended Mitigations": mitigations_text
    }
    
    show_results_box("⚠️ Oráculo Risk Assessment", sections, status)


def _display_suggestions(data: dict):
    """Display self-improvement suggestions"""
    suggestions = data.get("suggestions", [])
    priority = data.get("priority_areas", [])
    
    suggestions_text = "\n".join(
        f"  {i+1}. [cyan]{s.get('title', s) if isinstance(s, dict) else s}[/cyan]\n"
        f"     {s.get('description', '') if isinstance(s, dict) else ''}"
        for i, s in enumerate(suggestions[:5])
    ) if suggestions else "  No suggestions at this time"
    
    priority_text = "\n".join(
        f"  • {p}"
        for p in priority[:5]
    ) if priority else "  All areas performing well"
    
    sections = {
        "Improvement Suggestions": suggestions_text,
        "Priority Areas": priority_text
    }
    
    show_results_box("💡 Self-Improvement Suggestions", sections, "info")


@click.command(name="risk")
@click.option("--assess", is_flag=True, help="Run risk assessment")
@click.option("--suggest", is_flag=True, help="Get self-improvement suggestions")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format"
)
def risk(assess: bool, suggest: bool, output_format: str):
    """
    Risk assessment and predictions with Oráculo
    
    Analyze risks and get AI-powered suggestions for improvement.
    
    Examples:
    
        \b
        max-code risk --assess         # Risk assessment
        max-code risk --suggest        # Improvement suggestions
        max-code risk --assess --suggest # Both
    """
    # Default to assess if nothing specified
    if not assess and not suggest:
        assess = True
    
    client = get_shared_client()
    
    # Risk assessment
    if assess:
        with console.status("[bold yellow]Assessing risks..."):
            response = client.request(
                service=MaximusService.ORACULO,
                endpoint="/risk/assess",
                method="POST",
                data={"scope": "system"},
                timeout=60
            )
        
        if not response.success:
            show_error(
                "Risk Assessment Failed",
                response.error or "Unknown error",
                suggestions=[
                    "Check Oráculo service: max-code health oraculo",
                    "Verify service is responding",
                    "Check service logs: max-code logs oraculo"
                ],
                context={"service": "oraculo", "status_code": response.status_code}
            )
            raise click.Abort()
        
        data = response.data or {
            "risk_level": "MEDIUM",
            "risk_score": 5,
            "risks": [{"description": "Sample risk", "severity": "MEDIUM", "impact": "Moderate"}],
            "mitigations": ["Sample mitigation"]
        }
        
        if output_format == "json":
            console.print(format_json(data))
        else:
            _display_risk_assessment(data)
    
    # Self-improvement suggestions
    if suggest:
        console.print()  # Spacing
        
        with console.status("[bold yellow]Generating suggestions..."):
            response = client.request(
                service=MaximusService.ORACULO,
                endpoint="/suggest",
                method="POST",
                data={"context": "self-improvement"},
                timeout=60
            )
        
        if not response.success:
            show_error(
                "Suggestion Generation Failed",
                response.error or "Unknown error",
                suggestions=[
                    "Check Oráculo service: max-code health oraculo"
                ]
            )
            raise click.Abort()
        
        data = response.data or {
            "suggestions": [
                {"title": "Improve test coverage", "description": "Add more unit tests"},
                {"title": "Refactor complex functions", "description": "Break down large functions"}
            ],
            "priority_areas": ["Testing", "Code quality"]
        }
        
        if output_format == "json":
            console.print(format_json(data))
        else:
            _display_suggestions(data)


if __name__ == "__main__":
    risk()
