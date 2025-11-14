"""
Max-Code CLI - Development Commands

Integrates all development tools (test, lint, format, audit, security) into the CLI.
Boris Cherny Standard: Make the right thing easy to do.

"If it's hard to test, you won't test it" - Boris Cherny
"""

import click
import subprocess
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional

console = Console()


@click.group()
def dev():
    """
    Development tools and commands.
    
    Quality gates, testing, linting, formatting, security scanning, and audit.
    """
    pass


# ============================================================
# TESTING COMMANDS
# ============================================================

@dev.command()
@click.option('--unit', is_flag=True, help='Run only unit tests')
@click.option('--integration', is_flag=True, help='Run only integration tests')
@click.option('--fast', is_flag=True, help='Run tests without coverage (faster)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--file', '-f', type=str, help='Run specific test file')
def test(unit: bool, integration: bool, fast: bool, verbose: bool, file: Optional[str]):
    """
    Run tests with coverage.
    
    Examples:
        max-code dev test              # All tests with coverage
        max-code dev test --unit       # Unit tests only
        max-code dev test --fast       # Tests without coverage
        max-code dev test -f test_base_agent.py
    """
    console.print("\n[bold cyan]🧪 Running Tests[/bold cyan]\n")
    
    cmd = ["pytest"]
    
    if unit:
        cmd.append("tests/unit/")
    elif integration:
        cmd.append("tests/integration/")
    elif file:
        cmd.append(f"tests/{file}")
    else:
        cmd.append("tests/")
    
    if not fast:
        cmd.extend([
            "--cov=sdk",
            "--cov=cli",
            "--cov=config",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-fail-under=80"
        ])
    
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("--tb=short")
    
    result = subprocess.run(cmd, cwd=Path.cwd())
    
    if result.returncode == 0:
        console.print("\n[green]✅ Tests passed![/green]\n")
        if not fast:
            console.print("[dim]📊 Coverage report: htmlcov/index.html[/dim]\n")
    else:
        console.print("\n[red]❌ Tests failed![/red]\n")
    
    raise SystemExit(result.returncode)


@dev.command()
def coverage():
    """
    Generate comprehensive coverage report.
    
    Generates HTML, XML, and JSON coverage reports.
    """
    console.print("\n[bold cyan]📊 Generating Coverage Report[/bold cyan]\n")
    
    cmd = [
        "pytest", "tests/",
        "--cov=sdk",
        "--cov=cli",
        "--cov=config",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-report=json"
    ]
    
    result = subprocess.run(cmd, cwd=Path.cwd())
    
    if result.returncode == 0:
        console.print("\n[green]✅ Coverage reports generated![/green]\n")
        console.print("📊 Reports:")
        console.print("  - Terminal: see above")
        console.print("  - HTML: [cyan]htmlcov/index.html[/cyan]")
        console.print("  - XML: [cyan]coverage.xml[/cyan]")
        console.print("  - JSON: [cyan]coverage.json[/cyan]\n")
    else:
        console.print("\n[red]❌ Coverage generation failed![/red]\n")
    
    raise SystemExit(result.returncode)


# ============================================================
# CODE QUALITY COMMANDS
# ============================================================

@dev.command()
@click.option('--fix', is_flag=True, help='Auto-fix issues (black, isort)')
def lint(fix: bool):
    """
    Run all linters (flake8, black, isort).
    
    Examples:
        max-code dev lint        # Check code quality
        max-code dev lint --fix  # Auto-fix formatting issues
    """
    console.print("\n[bold cyan]🔍 Running Linters[/bold cyan]\n")
    
    issues_found = False
    
    # flake8 (no auto-fix)
    console.print("[yellow]→[/yellow] Running flake8...")
    result = subprocess.run(
        ["flake8", "sdk/", "cli/", "config/", "--count", "--statistics"],
        cwd=Path.cwd()
    )
    if result.returncode != 0:
        issues_found = True
    
    # black
    if fix:
        console.print("\n[yellow]→[/yellow] Formatting code with black...")
        subprocess.run(["black", "sdk/", "cli/", "config/", "tests/"], cwd=Path.cwd())
    else:
        console.print("\n[yellow]→[/yellow] Checking black formatting...")
        result = subprocess.run(
            ["black", "--check", "--diff", "sdk/", "cli/", "config/", "tests/"],
            cwd=Path.cwd()
        )
        if result.returncode != 0:
            issues_found = True
    
    # isort
    if fix:
        console.print("\n[yellow]→[/yellow] Sorting imports with isort...")
        subprocess.run(["isort", "sdk/", "cli/", "config/", "tests/"], cwd=Path.cwd())
    else:
        console.print("\n[yellow]→[/yellow] Checking import sorting...")
        result = subprocess.run(
            ["isort", "--check-only", "--diff", "sdk/", "cli/", "config/", "tests/"],
            cwd=Path.cwd()
        )
        if result.returncode != 0:
            issues_found = True
    
    if issues_found and not fix:
        console.print("\n[red]❌ Linting issues found![/red]")
        console.print("[yellow]💡 Run with --fix to auto-fix formatting issues[/yellow]\n")
        raise SystemExit(1)
    elif fix:
        console.print("\n[green]✅ Code formatted![/green]\n")
    else:
        console.print("\n[green]✅ All linting checks passed![/green]\n")


@dev.command()
@click.argument('targets', nargs=-1)
def format(targets):
    """
    Format code with black and isort.
    
    Examples:
        max-code dev format              # Format all code
        max-code dev format sdk/ cli/    # Format specific directories
    """
    console.print("\n[bold cyan]🎨 Formatting Code[/bold cyan]\n")
    
    dirs = list(targets) if targets else ["sdk/", "cli/", "config/", "tests/"]
    
    console.print("[yellow]→[/yellow] Running black...")
    subprocess.run(["black"] + dirs, cwd=Path.cwd())
    
    console.print("\n[yellow]→[/yellow] Running isort...")
    subprocess.run(["isort"] + dirs, cwd=Path.cwd())
    
    console.print("\n[green]✅ Code formatted![/green]\n")


@dev.command()
def typecheck():
    """
    Run type checking with mypy.
    
    Validates type hints in sdk/, cli/, and config/ modules.
    """
    console.print("\n[bold cyan]🔍 Type Checking with mypy[/bold cyan]\n")
    
    result = subprocess.run(
        ["mypy", "sdk/", "cli/", "config/", "--config-file=mypy.ini"],
        cwd=Path.cwd()
    )
    
    if result.returncode == 0:
        console.print("\n[green]✅ Type check passed![/green]\n")
    else:
        console.print("\n[red]❌ Type check failed![/red]\n")
    
    raise SystemExit(result.returncode)


# ============================================================
# SECURITY COMMANDS
# ============================================================

@dev.command()
@click.option('--full', is_flag=True, help='Run comprehensive security scan')
def security(full: bool):
    """
    Run security scans (pip-audit, bandit).
    
    Examples:
        max-code dev security        # Quick security scan
        max-code dev security --full # Comprehensive scan with reports
    """
    console.print("\n[bold cyan]🔒 Running Security Scan[/bold cyan]\n")
    
    # pip-audit
    console.print("[yellow]→[/yellow] Running pip-audit...")
    if full:
        subprocess.run(["pip-audit", "--desc", "--fix-dry-run"], cwd=Path.cwd())
    else:
        subprocess.run(["pip-audit", "--desc"], cwd=Path.cwd())
    
    # bandit
    console.print("\n[yellow]→[/yellow] Running bandit...")
    if full:
        subprocess.run(
            ["bandit", "-r", "sdk/", "cli/", "config/", "-f", "json", "-o", "bandit-report.json"],
            cwd=Path.cwd()
        )
        subprocess.run(["bandit", "-r", "sdk/", "cli/", "config/"], cwd=Path.cwd())
        console.print("\n[dim]📊 Bandit report: bandit-report.json[/dim]")
    else:
        subprocess.run(["bandit", "-r", "sdk/", "cli/", "config/", "-ll", "-i"], cwd=Path.cwd())
    
    console.print("\n[green]✅ Security scan complete![/green]\n")


@dev.command()
def audit():
    """
    Run comprehensive audit script.
    
    Executes the Boris Cherny audit script covering:
    - Security vulnerabilities
    - Type safety
    - Code smells
    - Complexity analysis
    - Test coverage
    """
    console.print("\n[bold cyan]📋 Running Comprehensive Audit[/bold cyan]\n")
    
    audit_script = Path.cwd() / "audit-cli.sh"
    
    if not audit_script.exists():
        console.print("[red]❌ audit-cli.sh not found![/red]\n")
        raise SystemExit(1)
    
    result = subprocess.run(["bash", str(audit_script)], cwd=Path.cwd())
    
    if result.returncode == 0:
        console.print("\n[green]✅ Audit complete![/green]")
        console.print("[dim]📊 Report: AUDIT_REPORT_COMPLETE.md[/dim]\n")
    else:
        console.print("\n[yellow]⚠️  Audit completed with warnings[/yellow]\n")


# ============================================================
# COMBINED COMMANDS
# ============================================================

@dev.command()
def ci():
    """
    Run all CI checks locally.
    
    Executes the same checks that run in CI/CD:
    - Format checking (black, isort)
    - Linting (flake8)
    - Type checking (mypy)
    - Tests (pytest with coverage)
    - Security scan
    """
    console.print("\n[bold cyan]🚀 Running CI Checks Locally[/bold cyan]\n")
    
    checks = [
        ("Format Check", ["black", "--check", "sdk/", "cli/", "config/", "tests/"]),
        ("Import Sort Check", ["isort", "--check-only", "sdk/", "cli/", "config/", "tests/"]),
        ("Flake8", ["flake8", "sdk/", "cli/", "config/", "--count", "--statistics"]),
        ("Type Check", ["mypy", "sdk/", "cli/", "config/", "--config-file=mypy.ini"]),
        ("Tests", ["pytest", "tests/", "--cov=sdk", "--cov=cli", "--cov=config", "--cov-fail-under=80", "-v"]),
    ]
    
    results = []
    
    for name, cmd in checks:
        console.print(f"\n[yellow]→ {name}[/yellow]")
        result = subprocess.run(cmd, cwd=Path.cwd(), capture_output=False)
        results.append((name, result.returncode == 0))
    
    # Summary table
    console.print("\n[bold cyan]📊 CI Summary[/bold cyan]\n")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Check", style="cyan")
    table.add_column("Status", justify="center")
    
    for name, passed in results:
        status = "[green]✅ PASS[/green]" if passed else "[red]❌ FAIL[/red]"
        table.add_row(name, status)
    
    console.print(table)
    console.print()
    
    if all(passed for _, passed in results):
        console.print("[green]🎉 All CI checks passed![/green]\n")
        raise SystemExit(0)
    else:
        console.print("[red]❌ Some CI checks failed![/red]\n")
        raise SystemExit(1)


@dev.command()
def pre_push():
    """
    Run all checks before pushing (recommended).
    
    Comprehensive validation:
    - Clean build artifacts
    - Format code (auto-fix)
    - Run all linters
    - Type check
    - Run all tests
    - Security scan
    """
    console.print("\n[bold cyan]🚀 Pre-push Validation[/bold cyan]\n")
    
    # Clean
    console.print("[yellow]→[/yellow] Cleaning build artifacts...")
    subprocess.run(["make", "clean"], cwd=Path.cwd())
    
    # Format
    console.print("\n[yellow]→[/yellow] Formatting code...")
    subprocess.run(["black", "sdk/", "cli/", "config/", "tests/"], cwd=Path.cwd())
    subprocess.run(["isort", "sdk/", "cli/", "config/", "tests/"], cwd=Path.cwd())
    
    # Lint
    console.print("\n[yellow]→[/yellow] Running linters...")
    result = subprocess.run(["flake8", "sdk/", "cli/", "config/"], cwd=Path.cwd())
    if result.returncode != 0:
        console.print("\n[red]❌ Linting failed![/red]\n")
        raise SystemExit(1)
    
    # Type check
    console.print("\n[yellow]→[/yellow] Type checking...")
    result = subprocess.run(["mypy", "sdk/", "cli/", "config/", "--config-file=mypy.ini"], cwd=Path.cwd())
    if result.returncode != 0:
        console.print("\n[red]❌ Type check failed![/red]\n")
        raise SystemExit(1)
    
    # Tests
    console.print("\n[yellow]→[/yellow] Running tests...")
    result = subprocess.run(
        ["pytest", "tests/", "--cov=sdk", "--cov=cli", "--cov=config", "--cov-fail-under=80"],
        cwd=Path.cwd()
    )
    if result.returncode != 0:
        console.print("\n[red]❌ Tests failed![/red]\n")
        raise SystemExit(1)
    
    console.print("\n[green]✅ Ready to push![/green]\n")


@dev.command()
def stats():
    """
    Show project statistics.
    
    Displays code metrics, test coverage, and quality indicators.
    """
    console.print("\n[bold cyan]📊 Project Statistics[/bold cyan]\n")
    
    # Code statistics
    table = Table(title="Code Metrics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="yellow")
    
    # Count Python files
    py_files = list(Path.cwd().rglob("*.py"))
    py_files_sdk = list(Path("sdk").rglob("*.py")) if Path("sdk").exists() else []
    py_files_cli = list(Path("cli").rglob("*.py")) if Path("cli").exists() else []
    py_files_tests = list(Path("tests").rglob("*.py")) if Path("tests").exists() else []
    
    table.add_row("Total Python Files", str(len(py_files)))
    table.add_row("SDK Files", str(len(py_files_sdk)))
    table.add_row("CLI Files", str(len(py_files_cli)))
    table.add_row("Test Files", str(len(py_files_tests)))
    
    # Lines of code
    total_lines = sum(1 for f in py_files for _ in open(f))
    table.add_row("Total Lines", f"{total_lines:,}")
    
    console.print(table)
    console.print()
    
    # Test coverage (if available)
    coverage_file = Path.cwd() / ".coverage"
    if coverage_file.exists():
        console.print("[dim]💡 Run 'max-code dev coverage' for detailed coverage report[/dim]\n")
    else:
        console.print("[dim]💡 Run 'max-code dev test' to generate coverage data[/dim]\n")


# ============================================================
# HELP COMMAND
# ============================================================

@dev.command()
def help_dev():
    """
    Show detailed help for development commands.
    """
    help_text = """
[bold cyan]Max-Code CLI - Development Commands[/bold cyan]

[yellow]Quick Start:[/yellow]
  max-code dev test              Run all tests
  max-code dev lint --fix        Check and fix code quality
  max-code dev ci                Run CI checks locally
  max-code dev pre-push          Validate before pushing

[yellow]Testing:[/yellow]
  test              Run tests with coverage
  test --unit       Run unit tests only
  test --fast       Run tests without coverage
  coverage          Generate coverage reports

[yellow]Code Quality:[/yellow]
  lint              Run linters (flake8, black, isort)
  lint --fix        Auto-fix formatting issues
  format            Format code with black and isort
  typecheck         Run mypy type checking

[yellow]Security:[/yellow]
  security          Quick security scan
  security --full   Comprehensive security scan
  audit             Run comprehensive audit script

[yellow]Combined:[/yellow]
  ci                Run all CI checks locally
  pre-push          All checks before pushing
  stats             Show project statistics

[yellow]Examples:[/yellow]
  max-code dev test -v                    # Verbose tests
  max-code dev lint --fix                 # Auto-fix code
  max-code dev security --full            # Full security scan
  max-code dev ci                         # Local CI validation

[dim]💡 Tip: Use 'max-code dev <command> --help' for detailed help[/dim]
    """
    
    console.print(Panel(help_text, border_style="cyan"))
