"""
B.P.R CLI Command - Blueprint → Plan → Refine

Takes user's research paper and generates:
1. BLUEPRINT - Architecture design (Sophia/ArchitectAgent)
2. PLAN - Implementation roadmap (PlanAgent)
3. REFINE - Constitutional AI validation (P1-P6)

Constitutional AI v3.0 Compliant
"""

import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.markdown import Markdown
import sys

from core.bpr.orchestrator import BPROrchestrator
from config.settings import get_settings
from config.logging_config import get_logger

logger = get_logger(__name__)
console = Console()

# Create Typer app for B.P.R commands
app = typer.Typer(
    name="bpr",
    help="B.P.R Methodology: Blueprint → Plan → Refine (User provides research paper)",
    add_completion=False
)


@app.command()
def run(
    prompt: str = typer.Argument(
        ...,
        help="Brief description of your project/idea (for context)"
    ),
    paper: Optional[Path] = typer.Option(
        None,
        "--paper",
        "-p",
        help="Path to your research paper file (Markdown, text, etc.)",
        exists=True,
        readable=True
    ),
    paper_text: Optional[str] = typer.Option(
        None,
        "--paper-text",
        help="Research paper content as string (alternative to --paper)"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for deliverables (default: ./outputs/bpr/)"
    ),
    format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help="Output format: markdown or json"
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
        help="Verbose output with detailed progress"
    )
):
    """
    Execute B.P.R methodology on your research paper

    Takes your research paper and generates:
    - Architecture Blueprint (via Sophia/ArchitectAgent)
    - Implementation Plan (via PlanAgent)
    - Constitutional Validation Report (P1-P6)

    Examples:

        # Using paper file
        max-code bpr run "Medical diagnostic AI" --paper ./research.md

        # Using paper text directly
        max-code bpr run "Constitutional AI v3.0" --paper-text "..."

        # With custom output
        max-code bpr run "ML platform" --paper ./ml-research.md --output ./outputs/ml
    """

    # Validate inputs
    if not paper and not paper_text:
        console.print("[red]❌ Error: Must provide either --paper <file> or --paper-text <content>[/red]")
        raise typer.Exit(code=1)

    if paper and paper_text:
        console.print("[yellow]⚠️  Warning: Both --paper and --paper-text provided. Using --paper file.[/yellow]")
        paper_text = None

    # Load paper from file if provided
    paper_content = None
    if paper:
        try:
            with open(paper, 'r', encoding='utf-8') as f:
                paper_content = f.read()

            if verbose:
                console.print(f"[green]✅ Loaded paper from: {paper}[/green]")
                console.print(f"[dim]   Paper length: {len(paper_content.split())} words[/dim]")
        except Exception as e:
            console.print(f"[red]❌ Error reading paper file: {e}[/red]")
            raise typer.Exit(code=1)
    else:
        paper_content = paper_text

    # Validate paper content
    if not paper_content or len(paper_content.strip()) < 100:
        console.print("[red]❌ Error: Paper content too short (minimum 100 characters)[/red]")
        raise typer.Exit(code=1)

    # Configuration
    settings = get_settings()
    output_path = output_dir or settings.ppbpr.output_dir / "bpr"

    # Display header
    console.print(Panel.fit(
        "[bold cyan]B.P.R Methodology Automation[/bold cyan]\n"
        "[dim]Blueprint → Plan → Refine[/dim]\n\n"
        f"[yellow]Prompt:[/yellow] {prompt[:80]}{'...' if len(prompt) > 80 else ''}\n"
        f"[yellow]Paper:[/yellow] {len(paper_content.split())} words\n"
        f"[yellow]Output:[/yellow] {output_path}\n"
        f"[yellow]Constitutional Validation:[/yellow] {'Enabled ✅' if not skip_validation else 'Disabled ⚠️'}",
        title="🏗️  B.P.R Orchestrator",
        border_style="cyan"
    ))

    # Initialize orchestrator
    orchestrator = BPROrchestrator(
        enable_constitutional=not skip_validation
    )

    # Execute B.P.R workflow
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False
        ) as progress:

            task = progress.add_task("[cyan]Running B.P.R workflow...", total=3)

            if verbose:
                console.print("\n[bold]Starting B.P.R execution...[/bold]\n")

            # Run B.P.R
            deliverable = asyncio.run(
                orchestrator.run(
                    paper=paper_content,
                    prompt=prompt,
                    paper_file=paper
                )
            )

            progress.update(task, completed=3)

        # Display results
        console.print("\n[bold green]✅ B.P.R Complete![/bold green]\n")

        # Results table
        results_table = Table(title="📊 B.P.R Results", show_header=True, header_style="bold cyan")
        results_table.add_column("Metric", style="yellow")
        results_table.add_column("Value", style="green")

        results_table.add_row("Execution Time", f"{deliverable.execution_time_seconds:.1f}s")
        results_table.add_row("Paper Length", f"{len(deliverable.paper.split())} words")
        results_table.add_row("Blueprint Components", str(len(deliverable.blueprint.get('components', []))))
        results_table.add_row("Plan Phases", str(len(deliverable.plan.get('phases', []))))
        results_table.add_row("Plan Tasks", str(len(deliverable.plan.get('tasks', []))))
        results_table.add_row("Quality Score", f"{deliverable.quality_score:.2f}")

        console.print(results_table)

        # Constitutional report
        if not skip_validation:
            console.print("\n[bold]📜 Constitutional AI Report (P1-P6)[/bold]\n")

            constitutional_table = Table(show_header=True, header_style="bold cyan")
            constitutional_table.add_column("Principle", style="yellow")
            constitutional_table.add_column("Status", style="green")

            for principle, passed in deliverable.constitutional_report.items():
                status = "✅ PASS" if passed else "❌ FAIL"
                status_style = "green" if passed else "red"
                constitutional_table.add_row(principle.replace("_", " ").title(), f"[{status_style}]{status}[/{status_style}]")

            console.print(constitutional_table)

            all_passed = all(deliverable.constitutional_report.values())
            if all_passed:
                console.print("\n[bold green]✅ All constitutional principles validated[/bold green]")
            else:
                failed = [k for k, v in deliverable.constitutional_report.items() if not v]
                console.print(f"\n[bold red]⚠️  Constitutional validation failed: {', '.join(failed)}[/bold red]")

        # Save deliverables
        console.print(f"\n[cyan]💾 Saving deliverables to: {output_path}[/cyan]")

        deliverable.save_to_file(
            output_dir=output_path,
            format=format
        )

        console.print(f"\n[bold green]✅ Deliverables saved successfully![/bold green]")
        console.print(f"[dim]   Check {output_path} for blueprint and plan files[/dim]\n")

        # Quality warning
        if deliverable.quality_score < 0.6:
            console.print(Panel(
                f"[yellow]⚠️  Quality score is below optimal threshold (0.60)[/yellow]\n\n"
                f"Current score: {deliverable.quality_score:.2f}\n\n"
                "This may indicate:\n"
                "- Paper needs more detail\n"
                "- Blueprint generation had low confidence\n"
                "- Plan lacks sufficient tasks/phases\n\n"
                "Consider:\n"
                "- Expanding your research paper\n"
                "- Reviewing blueprint and plan outputs\n"
                "- Running B.P.R again with refined inputs",
                title="Quality Advisory",
                border_style="yellow"
            ))

        # Verbose output
        if verbose:
            console.print("\n[bold]📋 Blueprint Preview[/bold]")
            console.print(f"[dim]{str(deliverable.blueprint)[:500]}...[/dim]\n")

            console.print("[bold]📋 Plan Preview[/bold]")
            console.print(f"[dim]{str(deliverable.plan)[:500]}...[/dim]\n")

    except Exception as e:
        logger.error(f"B.P.R execution failed: {e}", exc_info=True)
        console.print(f"\n[bold red]❌ B.P.R execution failed:[/bold red]\n")
        console.print(f"[red]{str(e)}[/red]\n")

        if verbose:
            import traceback
            console.print("[dim]Full traceback:[/dim]")
            console.print(f"[dim]{traceback.format_exc()}[/dim]")

        raise typer.Exit(code=1)


@app.command()
def info():
    """
    Show information about B.P.R methodology
    """
    info_text = """
# B.P.R Methodology - Blueprint → Plan → Refine

**Automated architecture and planning from YOUR research paper.**

## Workflow

1. **YOU provide:** Research paper (20+ pages, scientifically grounded)
2. **System generates:**
   - **BLUEPRINT** - Architecture design (via Sophia/ArchitectAgent)
   - **PLAN** - Implementation roadmap (via PlanAgent)
   - **REFINE** - Constitutional AI validation (P1-P6)

## Why B.P.R?

- **You keep creative control:** Research and writing stay in your hands
- **Automate mechanical work:** Blueprint and planning automated
- **Scientific foundation:** Your research provides the "lastro científico"
- **Fast execution:** < 1 minute typical (no external API calls for blueprint/plan)

## Difference from P.P.B.P.R

| Aspect | P.P.B.P.R | B.P.R |
|--------|-----------|-------|
| Research | Automated (Gemini) | **You provide** |
| Paper | Automated (Gemini) | **You provide** |
| Blueprint | Automated (Sophia) | Automated (Sophia) |
| Plan | Automated (PlanAgent) | Automated (PlanAgent) |
| Refine | Automated (Constitutional AI) | Automated (Constitutional AI) |

**Use B.P.R when:** You enjoy research and want control over paper quality
**Use P.P.B.P.R when:** You want full end-to-end automation

## Usage Example

```bash
# Basic usage
max-code bpr run "Medical diagnostic AI" --paper ./research.md

# With custom output
max-code bpr run "Constitutional AI v3.0" --paper ./constitutional-research.md --output ./outputs/constitutional

# JSON format
max-code bpr run "ML platform" --paper ./ml.md --format json
```

## Constitutional AI Compliance

All B.P.R outputs are validated against Constitutional AI v3.0 principles:
- **P1** - Zero Trust (validation at each step)
- **P2** - Completude (100% functional outputs)
- **P3** - Visão Sistêmica (holistic analysis)
- **P4** - Obrigação da Verdade (honest limitations)
- **P5** - Soberania da Intenção (your intent paramount)
- **P6** - Antifragilidade (iterative improvement)

## Next Steps

After B.P.R generates blueprint and plan:
1. Review architecture design
2. Validate implementation roadmap
3. Use `max-code predict` to implement features
4. Iterate and refine based on feedback

---

**Soli Deo Gloria!** 🙏
"""

    console.print(Panel(
        Markdown(info_text),
        title="ℹ️  B.P.R Information",
        border_style="cyan",
        expand=False
    ))


@app.command()
def test():
    """
    Run a simple B.P.R test with sample data
    """
    console.print("[cyan]🧪 Running B.P.R test...[/cyan]\n")

    # Sample paper (minimal)
    sample_paper = """
# Constitutional AI Implementation Research

## Executive Summary

Constitutional AI is a framework for building AI systems with built-in ethical
guardrails and value alignment. This research explores implementation patterns
for production AI applications with P1-P6 constitutional principles.

## Technical Analysis

The framework consists of six foundational principles:
- P1: Zero Trust, Maximum Validation
- P2: Completude Não-Negociável
- P3: Visão Sistêmica Obrigatória
- P4: Obrigação da Verdade
- P5: Soberania da Intenção
- P6: Antifragilidade por Design

## Implementation Recommendations

For production systems:
1. Implement validation gates at each decision point
2. Design for 100% completeness - no partial outputs
3. Maintain holistic system awareness across components
4. Build truth obligation into agent prompts
5. Preserve user intent through transformation pipeline
6. Create systems that improve under stress

## Architecture Considerations

- Multi-agent orchestration with constitutional validation
- Quality gates (QG1-QG5) for sequential workflows
- Context retention scoring (CRS ≥ 0.85)
- First-pass correctness tracking (FPC ≥ 80%)
- Lazy execution detection and prevention (LEI ≤ 1.0)

## Conclusion

Constitutional AI provides a robust framework for building trustworthy AI systems.
Key success factors include rigorous validation, complete implementations, and
continuous monitoring of constitutional adherence.
"""

    sample_prompt = "Constitutional AI v3.0 implementation for multi-agent systems"

    console.print(f"[yellow]Prompt:[/yellow] {sample_prompt}")
    console.print(f"[yellow]Paper:[/yellow] {len(sample_paper.split())} words (sample)\n")

    try:
        orchestrator = BPROrchestrator()

        console.print("[cyan]Executing B.P.R...[/cyan]\n")

        deliverable = asyncio.run(
            orchestrator.run(
                paper=sample_paper,
                prompt=sample_prompt
            )
        )

        console.print("[bold green]✅ Test Complete![/bold green]\n")

        # Results
        results_table = Table(title="📊 Test Results", show_header=True, header_style="bold cyan")
        results_table.add_column("Metric", style="yellow")
        results_table.add_column("Value", style="green")

        results_table.add_row("Execution Time", f"{deliverable.execution_time_seconds:.1f}s")
        results_table.add_row("Quality Score", f"{deliverable.quality_score:.2f}")
        results_table.add_row("Blueprint Components", str(len(deliverable.blueprint.get('components', []))))
        results_table.add_row("Plan Phases", str(len(deliverable.plan.get('phases', []))))
        results_table.add_row("Constitutional Validation", "✅ PASS" if all(deliverable.constitutional_report.values()) else "❌ FAIL")

        console.print(results_table)
        console.print("\n[green]✅ B.P.R system operational![/green]\n")

    except Exception as e:
        console.print(f"[red]❌ Test failed: {e}[/red]\n")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
