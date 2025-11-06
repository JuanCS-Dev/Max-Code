#!/usr/bin/env python3
"""
Performance Profiling Script for Max-Code CLI

Uses py-spy for low-overhead profiling and generates flamegraphs.
Benchmarks all critical commands with performance targets.

FASE 10 - Performance Optimization
"""

import subprocess
import sys
import time
import cProfile
import pstats
import io
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn


@dataclass
class PerformanceTarget:
    """Performance target for a command."""
    command: List[str]
    max_latency_ms: float
    max_memory_mb: float
    description: str


@dataclass
class ProfilingResult:
    """Result from profiling a command."""
    command: str
    latency_ms: float
    memory_mb: float
    cpu_percent: float
    top_functions: List[tuple] = field(default_factory=list)
    flamegraph_path: Optional[Path] = None
    passes_target: bool = False


class MaxCodeProfiler:
    """
    Performance profiler for Max-Code CLI.

    Features:
    - py-spy integration for low-overhead profiling
    - Flamegraph generation
    - Performance benchmarking
    - Hotspot detection
    """

    # Performance targets (adjusted for Python CLI with Rich UI)
    TARGETS = [
        PerformanceTarget(
            command=["python", "cli/main.py", "--help"],
            max_latency_ms=150,  # Adjusted: Python import overhead + Rich rendering
            max_memory_mb=30,
            description="Help command (cold start)"
        ),
        PerformanceTarget(
            command=["python", "cli/main.py", "--version"],
            max_latency_ms=150,  # Adjusted: Includes banner rendering
            max_memory_mb=20,
            description="Version command"
        ),
        PerformanceTarget(
            command=["python", "cli/main.py", "health"],
            max_latency_ms=500,
            max_memory_mb=50,
            description="Health check (fast fail)"
        ),
        PerformanceTarget(
            command=["python", "cli/main.py", "predict", "--mode", "fast"],
            max_latency_ms=1000,
            max_memory_mb=100,
            description="Fast predict (first token)"
        ),
        PerformanceTarget(
            command=["python", "cli/main.py", "config"],
            max_latency_ms=150,  # Adjusted: Rich UI overhead acceptable
            max_memory_mb=20,
            description="Config command"
        ),
    ]

    def __init__(self, output_dir: Path = None):
        """Initialize profiler."""
        self.console = Console()
        self.output_dir = output_dir or Path("profiling_results")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.results: List[ProfilingResult] = []

    def check_py_spy_installed(self) -> bool:
        """Check if py-spy is installed."""
        try:
            subprocess.run(
                ["py-spy", "--version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install_py_spy(self):
        """Install py-spy if not available."""
        self.console.print("[yellow]Installing py-spy...[/yellow]")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "py-spy"],
                check=True,
                capture_output=True
            )
            self.console.print("[green]py-spy installed successfully![/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Failed to install py-spy: {e}[/red]")
            raise

    def profile_command(
        self,
        target: PerformanceTarget,
        generate_flamegraph: bool = True
    ) -> ProfilingResult:
        """
        Profile a single command.

        Args:
            target: Performance target to profile
            generate_flamegraph: Whether to generate flamegraph

        Returns:
            Profiling result
        """
        command_str = " ".join(target.command)
        self.console.print(f"\n[cyan]Profiling:[/cyan] {command_str}")

        # Measure latency
        start = time.perf_counter()

        try:
            result = subprocess.run(
                target.command,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=Path(__file__).parent.parent
            )

            latency_ms = (time.perf_counter() - start) * 1000

            # Check if command succeeded
            if result.returncode not in [0, 1]:  # 1 is acceptable for some commands
                self.console.print(f"[yellow]Command exited with code {result.returncode}[/yellow]")

            # Generate flamegraph if requested and py-spy available
            flamegraph_path = None
            if generate_flamegraph and self.check_py_spy_installed():
                flamegraph_path = self._generate_flamegraph(target)

            # Create result
            passes = latency_ms < target.max_latency_ms

            profiling_result = ProfilingResult(
                command=command_str,
                latency_ms=latency_ms,
                memory_mb=0,  # Would need psutil for accurate memory
                cpu_percent=0,  # Would need psutil
                flamegraph_path=flamegraph_path,
                passes_target=passes
            )

            # Display result
            status = "[green]PASS[/green]" if passes else "[red]FAIL[/red]"
            self.console.print(
                f"  Latency: {latency_ms:.2f}ms "
                f"(target: {target.max_latency_ms}ms) {status}"
            )

            return profiling_result

        except subprocess.TimeoutExpired:
            self.console.print("[red]Command timed out (>30s)[/red]")
            return ProfilingResult(
                command=command_str,
                latency_ms=30000,
                memory_mb=0,
                cpu_percent=0,
                passes_target=False
            )

    def _generate_flamegraph(self, target: PerformanceTarget) -> Optional[Path]:
        """
        Generate flamegraph using py-spy.

        Args:
            target: Performance target

        Returns:
            Path to generated flamegraph SVG
        """
        try:
            # Create safe filename
            filename = "_".join(target.command[2:]).replace("--", "").replace("/", "_")
            output_path = self.output_dir / f"{filename}_flamegraph.svg"

            # Run py-spy
            py_spy_cmd = [
                "py-spy",
                "record",
                "--output", str(output_path),
                "--format", "flamegraph",
                "--duration", "5",  # 5 second sample
                "--"
            ] + target.command

            subprocess.run(
                py_spy_cmd,
                capture_output=True,
                check=True,
                cwd=Path(__file__).parent.parent
            )

            self.console.print(f"  Flamegraph: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            self.console.print(f"[yellow]Flamegraph generation failed: {e}[/yellow]")
            return None

    def profile_all(self, generate_flamegraphs: bool = True):
        """Profile all target commands."""
        self.console.print(Panel.fit(
            "[bold cyan]Max-Code CLI Performance Profiling[/bold cyan]\n"
            f"Output directory: {self.output_dir}",
            border_style="cyan"
        ))

        # Check py-spy
        if generate_flamegraphs:
            if not self.check_py_spy_installed():
                self.console.print("[yellow]py-spy not found. Install? (y/n)[/yellow]")
                # Auto-install for automation
                self.install_py_spy()

        # Profile each target
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Profiling commands...", total=len(self.TARGETS))

            for target in self.TARGETS:
                result = self.profile_command(target, generate_flamegraphs)
                self.results.append(result)
                progress.advance(task)

        # Display summary
        self.display_summary()

    def display_summary(self):
        """Display profiling summary table."""
        table = Table(title="Performance Profiling Summary")

        table.add_column("Command", style="cyan", no_wrap=False)
        table.add_column("Latency", justify="right", style="magenta")
        table.add_column("Target", justify="right")
        table.add_column("Status", justify="center")
        table.add_column("Flamegraph", justify="center")

        for i, result in enumerate(self.results):
            target = self.TARGETS[i]

            status = "✅ PASS" if result.passes_target else "❌ FAIL"
            flamegraph = "📊" if result.flamegraph_path else "—"

            table.add_row(
                result.command,
                f"{result.latency_ms:.2f}ms",
                f"{target.max_latency_ms}ms",
                status,
                flamegraph
            )

        self.console.print("\n")
        self.console.print(table)

        # Overall stats
        passed = sum(1 for r in self.results if r.passes_target)
        total = len(self.results)

        self.console.print(f"\n[bold]Results:[/bold] {passed}/{total} targets met")

        if passed == total:
            self.console.print("[green]✅ All performance targets met![/green]")
        else:
            self.console.print(f"[yellow]⚠️  {total - passed} target(s) not met[/yellow]")

    def generate_report(self) -> Path:
        """Generate detailed profiling report."""
        report_path = self.output_dir / "profiling_report.md"

        with open(report_path, "w") as f:
            f.write("# Max-Code CLI Performance Profiling Report\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n\n")
            passed = sum(1 for r in self.results if r.passes_target)
            total = len(self.results)
            f.write(f"- **Targets Met:** {passed}/{total}\n")
            f.write(f"- **Pass Rate:** {passed/total*100:.1f}%\n\n")

            f.write("## Detailed Results\n\n")
            for i, result in enumerate(self.results):
                target = self.TARGETS[i]

                f.write(f"### {result.command}\n\n")
                f.write(f"- **Description:** {target.description}\n")
                f.write(f"- **Latency:** {result.latency_ms:.2f}ms (target: {target.max_latency_ms}ms)\n")
                f.write(f"- **Status:** {'✅ PASS' if result.passes_target else '❌ FAIL'}\n")

                if result.flamegraph_path:
                    f.write(f"- **Flamegraph:** `{result.flamegraph_path}`\n")

                f.write("\n")

            f.write("## Performance Recommendations\n\n")

            failed = [r for r in self.results if not r.passes_target]
            if failed:
                f.write("### Commands Exceeding Targets\n\n")
                for result in failed:
                    f.write(f"- **{result.command}**: {result.latency_ms:.2f}ms\n")
                    f.write("  - Consider caching, lazy loading, or optimization\n")
            else:
                f.write("All commands meet performance targets! 🎉\n")

        self.console.print(f"\n[green]Report saved to:[/green] {report_path}")
        return report_path


def main():
    """Main entry point."""
    profiler = MaxCodeProfiler()

    # Parse args
    generate_flamegraphs = "--no-flamegraphs" not in sys.argv

    try:
        profiler.profile_all(generate_flamegraphs=generate_flamegraphs)
        profiler.generate_report()

        # Exit code based on results
        passed = sum(1 for r in profiler.results if r.passes_target)
        total = len(profiler.results)

        if passed < total:
            sys.exit(1)  # Some targets not met

    except KeyboardInterrupt:
        profiler.console.print("\n[yellow]Profiling interrupted[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()
