"""
P.P.B.P.R Command - Automated Research-to-Plan Methodology

Prompt → Paper → Blueprint → Plan → Refine

Constitutional AI v3.0 aligned command that automates the complete
research and planning workflow using hybrid Gemini + Claude architecture.
"""

import typer
import asyncio
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich import box

from core.ppbpr.orchestrator import PPBPROrchestrator
from config.settings import get_settings
from config.logging_config import get_logger

app = typer.Typer(help="P.P.B.P.R Methodology - Automated Research Pipeline")
console = Console()
logger = get_logger(__name__)


def create_banner():
    """Create P.P.B.P.R banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║        P.P.B.P.R METHODOLOGY AUTOMATION v1.0             ║
║   Prompt → Paper → Blueprint → Plan → Refine             ║
╚═══════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, border_style="cyan", box=box.HEAVY))


@app.command()
def run(
    prompt: str = typer.Argument(
        ...,
        help="Detailed idea or requirement to research and plan"
    ),
    depth: str = typer.Option(
        "comprehensive",
        "--depth",
        "-d",
        help="Research depth: basic, moderate, comprehensive"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for deliverables"
    ),
    format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help="Output format: markdown, json"
    ),
    skip_validation: bool = typer.Option(
        False,
        "--skip-validation",
        help="Skip constitutional validation (not recommended)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output"
    )
):
    """
    Execute P.P.B.P.R methodology on a topic

    EXAMPLES:

        \b
        # Comprehensive research on OAuth 2.0
        max-code ppbpr "OAuth 2.0 implementation for microservices"

        \b
        # Quick research with custom output
        max-code ppbpr "Redis caching strategies" --depth basic --output ./research

        \b
        # Full pipeline with JSON output
        max-code ppbpr "CI/CD pipeline with Docker" --format json
    """
    # Validate depth
    valid_depths = ["basic", "moderate", "comprehensive"]
    if depth not in valid_depths:
        console.print(f"[red]❌ Invalid depth: {depth}[/red]")
        console.print(f"   Valid options: {', '.join(valid_depths)}")
        raise typer.Exit(1)

    # Show banner
    create_banner()

    # Load settings
    settings = get_settings()

    # Check Gemini API key
    if not settings.gemini.api_key:
        console.print("\n[red]❌ Error: GEMINI_API_KEY not configured[/red]")
        console.print("\n[yellow]To fix:[/yellow]")
        console.print("1. Get API key from: https://ai.google.dev/")
        console.print("2. Add to .env file: GEMINI_API_KEY=your_key_here")
        console.print("3. Or export: export GEMINI_API_KEY=your_key_here")
        raise typer.Exit(1)

    # Set output directory
    if output_dir is None:
        output_dir = settings.ppbpr.output_dir

    # Show configuration
    config_table = Table(show_header=False, box=box.SIMPLE)
    config_table.add_row("[cyan]Prompt:[/cyan]", prompt[:80] + "..." if len(prompt) > 80 else prompt)
    config_table.add_row("[cyan]Depth:[/cyan]", depth)
    config_table.add_row("[cyan]Output:[/cyan]", str(output_dir))
    config_table.add_row("[cyan]Format:[/cyan]", format)
    config_table.add_row("[cyan]Validation:[/cyan]", "Disabled" if skip_validation else "Enabled (P1-P6)")

    console.print("\n")
    console.print(config_table)
    console.print("\n")

    # Initialize orchestrator
    orchestrator = PPBPROrchestrator(
        enable_quality_gates=True,
        enable_constitutional=not skip_validation
    )

    # Run P.P.B.P.R workflow
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:

            task = progress.add_task(
                "[cyan]Running P.P.B.P.R workflow...",
                total=5
            )

            # Execute workflow
            deliverable = asyncio.run(
                orchestrator.run(prompt=prompt, research_depth=depth)
            )

            progress.update(task, completed=5)

        # Display results
        console.print("\n")
        console.print("╔═══════════════════════════════════════════════╗")
        console.print("║         P.P.B.P.R DELIVERABLE READY           ║")
        console.print("╚═══════════════════════════════════════════════╝")
        console.print("\n")

        # Results table
        results_table = Table(show_header=True, box=box.ROUNDED)
        results_table.add_column("Metric", style="cyan")
        results_table.add_column("Value", style="green")

        results_table.add_row(
            "📄 Paper",
            f"{len(deliverable.paper.split())} words"
        )
        results_table.add_row(
            "🔗 Sources",
            f"{len(deliverable.research.sources)} references"
        )
        results_table.add_row(
            "🏗️  Blueprint",
            deliverable.blueprint.get("approach", "N/A")[:50]
        )
        results_table.add_row(
            "📋 Plan",
            f"{len(deliverable.plan.get('phases', []))} phases, {len(deliverable.plan.get('tasks', []))} tasks"
        )
        results_table.add_row(
            "📊 Quality Score",
            f"{deliverable.quality_score:.2f} / 1.00"
        )
        results_table.add_row(
            "⏱️  Execution Time",
            f"{deliverable.execution_time_seconds:.1f}s"
        )

        console.print(results_table)
        console.print("\n")

        # Constitutional report
        if not skip_validation:
            const_passed = sum(deliverable.constitutional_report.values())
            const_total = len(deliverable.constitutional_report)

            if const_passed == const_total:
                console.print(f"[green]✅ Constitutional Validation: {const_passed}/{const_total} passed[/green]")
            else:
                console.print(f"[yellow]⚠️  Constitutional Validation: {const_passed}/{const_total} passed[/yellow]")
                failed = [k for k, v in deliverable.constitutional_report.items() if not v]
                console.print(f"   Failed: {', '.join(failed)}")

            console.print("\n")

        # Save deliverables
        try:
            deliverable.save_to_file(output_dir=output_dir, format=format)

            console.print(f"[green]✅ Deliverables saved to:[/green] {output_dir}")
            console.print("\n[cyan]Next steps:[/cyan]")
            console.print(f"1. Review paper: {output_dir}/paper_*.md")
            console.print(f"2. Review blueprint: {output_dir}/blueprint_*.md")
            console.print(f"3. Review plan: {output_dir}/plan_*.md")

            if verbose:
                console.print("\n[dim]--- Paper Preview ---[/dim]")
                console.print(deliverable.paper[:500] + "...")

        except Exception as e:
            console.print(f"\n[yellow]⚠️  Warning: Could not save deliverables: {e}[/yellow]")

        console.print("\n[green]🎉 P.P.B.P.R Complete![/green]")
        console.print("\n[dim]Soli Deo Gloria 🙏[/dim]\n")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  P.P.B.P.R interrupted by user[/yellow]")
        raise typer.Exit(130)

    except Exception as e:
        console.print(f"\n\n[red]❌ P.P.B.P.R failed: {e}[/red]")
        if verbose:
            import traceback
            console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)


@app.command()
def info():
    """Show P.P.B.P.R methodology information"""

    create_banner()

    info_text = """
[cyan]P.P.B.P.R Methodology[/cyan] - Automated Research-to-Plan Pipeline

[bold]What it does:[/bold]
Automates your successful manual methodology for project planning:

[cyan]1. PROMPT[/cyan] - You provide a detailed idea/requirement
[cyan]2. PAPER[/cyan] - Gemini conducts PhD-level research with Google Search grounding
[cyan]3. BLUEPRINT[/cyan] - Claude + Sophia design system architecture
[cyan]4. PLAN[/cyan] - PlanAgent creates implementation roadmap
[cyan]5. REFINE[/cyan] - Constitutional AI validation (P1-P6)

[bold]Research Depths:[/bold]
• [green]basic[/green] - Quick overview (2K words, 1+ sources)
• [yellow]moderate[/yellow] - Balanced analysis (5K words, 2+ sources)
• [cyan]comprehensive[/cyan] - Deep research (10K words, 3+ sources)

[bold]Quality Gates:[/bold]
• QG1 - Research quality (sources, depth)
• QG2 - Paper structure (sections, citations)
• QG3 - Constitutional validation (P1-P6)
• QG4 - Plan completeness (phases, tasks)
• QG5 - Final validation (all principles)

[bold]Constitutional AI Framework:[/bold]
• P1 - Zero Trust (validation at each step)
• P2 - Completude (100% functional outputs)
• P3 - Visão Sistêmica (holistic analysis)
• P4 - Obrigação da Verdade (honest assessment)
• P5 - Soberania da Intenção (user intent paramount)
• P6 - Antifragilidade (iterative improvement)

[bold]Cost:[/bold]
~$0.025 per run (Gemini Flash: $0.15/M tokens)

[bold]Examples:[/bold]
max-code ppbpr "OAuth 2.0 for microservices"
max-code ppbpr "Redis caching strategies" --depth basic
max-code ppbpr "CI/CD pipeline" --format json --output ./research
    """

    console.print(Panel(info_text, title="P.P.B.P.R Info", border_style="cyan"))
    console.print("\n[dim]For more info: /ppbpr --help[/dim]\n")


@app.command()
def test():
    """Test P.P.B.P.R system with a simple query"""

    console.print("\n[cyan]🧪 Testing P.P.B.P.R System[/cyan]\n")

    # Simple test query
    test_prompt = "Best practices for Python async programming"

    console.print(f"Test Query: [yellow]{test_prompt}[/yellow]")
    console.print("Depth: [yellow]basic[/yellow]")
    console.print("\nRunning...\n")

    try:
        # Use the run command with basic depth
        ctx = typer.Context(run)
        ctx.invoke(
            run,
            prompt=test_prompt,
            depth="basic",
            output_dir=Path("./outputs/ppbpr/test"),
            format="markdown",
            skip_validation=False,
            verbose=False
        )

        console.print("\n[green]✅ Test completed successfully![/green]")

    except Exception as e:
        console.print(f"\n[red]❌ Test failed: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
