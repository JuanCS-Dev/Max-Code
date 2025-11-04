"""
Max-Code CLI Visual Demo

Shows ALL visual features in action:
- Magnificent banner with gradient (ISOMETRIC1 font)
- Perfect alignment everywhere
- Constitutional principles
- Agent messages
- Progress indicators (spinners, bars, multi-progress)
- Tables, panels, code highlighting
- Everything beautifully aligned (TOC-approved! 🎯)

Run with:
    python3 ui/demo.py
"""

import sys
import time
from rich.console import Console

# Force TTY mode for demo
console = Console(force_terminal=True)

# Import our beautiful UI components
sys.path.insert(0, '.')
from ui.banner import MaxCodeBanner
from ui.formatter import MaxCodeFormatter
from ui.progress import MaxCodeProgress


def demo_banner():
    """Demo the magnificent banner."""
    console.print("\n[bold cyan]═" * 35)
    console.print("[bold cyan]DEMO 1: MAGNIFICENT BANNER[/bold cyan]")
    console.print("[bold cyan]═" * 35 + "\n")

    banner = MaxCodeBanner(console=console)

    # Force banner display for demo
    banner._should_show = True

    # Show default style (ISOMETRIC1 - filled blocks)
    console.print("[yellow]Style: DEFAULT (ISOMETRIC1 - Filled 3D Blocks)[/yellow]")
    banner.show(
        version="3.0",
        context={
            'model': 'Claude Sonnet 4.5',
            'session': 'demo_abc123'
        },
        style='default'
    )


def demo_formatter():
    """Demo the perfect formatter."""
    console.print("\n[bold cyan]═" * 35)
    console.print("[bold cyan]DEMO 2: PERFECT FORMATTING[/bold cyan]")
    console.print("[bold cyan]═" * 35 + "\n")

    fmt = MaxCodeFormatter(console=console)

    # Semantic messages
    console.print("[yellow]Semantic Messages (Perfect Alignment):[/yellow]\n")
    fmt.print_success("All systems operational")
    fmt.print_error("Database connection lost", "Retrying in 5 seconds")
    fmt.print_warning("Memory usage at 85%")
    fmt.print_info("Processing 1,250 requests/second")
    fmt.print_debug("Cache hit ratio: 94.2%")

    time.sleep(2)

    # Divider
    fmt.print_divider("Agent Status")

    # Agent messages
    console.print("\n[yellow]Agent Messages (Color-Coded):[/yellow]\n")
    fmt.print_agent_message("Sophia", "Architecture analysis complete", "Analyzing")
    fmt.print_agent_message("Code", "Implementing REST API endpoints", "Working")
    fmt.print_agent_message("Test", "Running integration test suite", "Testing")
    fmt.print_agent_message("Review", "Code review in progress", "Reviewing")
    fmt.print_agent_message("Guardian", "All checks passed", "Monitoring")

    time.sleep(2)

    # Table
    fmt.print_divider("System Metrics")
    console.print()

    metrics_data = [
        {'Metric': 'CPU Usage', 'Value': '23%', 'Status': 'Normal', 'Trend': '↓'},
        {'Metric': 'Memory', 'Value': '4.2 GB', 'Status': 'Normal', 'Trend': '→'},
        {'Metric': 'Network', 'Value': '145 MB/s', 'Status': 'High', 'Trend': '↑'},
        {'Metric': 'Disk I/O', 'Value': '89 MB/s', 'Status': 'Normal', 'Trend': '→'},
    ]
    fmt.print_table(metrics_data, title="Real-Time System Metrics")

    time.sleep(2)

    # Constitutional principles
    console.print()
    fmt.print_divider("Constitutional Status")
    console.print()

    principles = {
        'p1': True,
        'p2': True,
        'p3': True,
        'p4': True,
        'p5': True,
        'p6': True,
    }
    fmt.print_constitutional_status(principles)

    time.sleep(2)

    # Code highlighting
    console.print()
    fmt.print_divider("Code Syntax Highlighting")
    console.print()

    code = """
from ui.banner import MaxCodeBanner
from ui.formatter import MaxCodeFormatter

# Initialize beautiful UI
banner = MaxCodeBanner()
formatter = MaxCodeFormatter()

# Show magnificent banner
banner.show(version="3.0", style="default")

# Print perfectly aligned messages
formatter.print_success("Max-Code CLI initialized")
formatter.print_info("Constitutional AI Framework ready")
    """

    fmt.print_code(code, "python")

    time.sleep(2)

    # Gradient text
    console.print()
    fmt.print_divider("Gradient Text")
    console.print()

    fmt.print_gradient_text("MAX-CODE CONSTITUTIONAL AI")
    fmt.print_gradient_text("Neon Green → Cyan → Blue Gradient")


def demo_progress():
    """Demo progress indicators."""
    console.print("\n[bold cyan]═" * 35)
    console.print("[bold cyan]DEMO 3: PROGRESS INDICATORS[/bold cyan]")
    console.print("[bold cyan]═" * 35 + "\n")

    progress = MaxCodeProgress(console=console)

    # Spinner
    console.print("[yellow]1. Agent Spinner:[/yellow]\n")
    with progress.agent_spinner("Sophia", "Analyzing architecture", "Analyzing"):
        time.sleep(2)
    console.print()

    # Progress bar
    console.print("[yellow]2. Progress Bar:[/yellow]\n")
    with progress.bar(total=40, description="Processing files") as bar:
        for i in range(40):
            time.sleep(0.05)
            bar.advance(1)
    console.print()

    # Agent activity
    console.print("[yellow]3. Agent Activity:[/yellow]\n")
    agents = [
        {'name': 'Sophia', 'status': 'active', 'task': 'Architecture analysis', 'progress': 75},
        {'name': 'Code', 'status': 'active', 'task': 'Implementing features', 'progress': 50},
        {'name': 'Test', 'status': 'idle', 'task': 'Waiting for code', 'progress': 0},
        {'name': 'Guardian', 'status': 'completed', 'task': 'Security check done', 'progress': 100},
    ]
    progress.show_agent_activity(agents)
    console.print()

    # Task status
    console.print("[yellow]4. Task Status:[/yellow]\n")
    tasks = [
        {'name': 'Load configuration', 'status': 'completed', 'duration': '0.5s'},
        {'name': 'Initialize system', 'status': 'completed', 'duration': '1.2s'},
        {'name': 'Process data', 'status': 'in_progress', 'duration': '...'},
        {'name': 'Generate report', 'status': 'pending', 'duration': '-'},
    ]
    progress.show_task_status(tasks)


def demo_agents():
    """Demo agent visualization."""
    console.print("\n[bold cyan]═" * 35)
    console.print("[bold cyan]DEMO 4: AGENT MESSAGES[/bold cyan]")
    console.print("[bold cyan]═" * 35 + "\n")

    fmt = MaxCodeFormatter(console=console)

    # Agent activity timeline
    console.print("[yellow]Agent Activity Timeline:[/yellow]\n")

    activities = [
        ("Sophia", "Planning system architecture", 0.8),
        ("Code", "Implementing UI components", 1.0),
        ("Test", "Writing unit tests", 0.8),
        ("Review", "Reviewing code quality", 0.8),
        ("Guardian", "Validating constitutional compliance", 0.8),
    ]

    for agent, action, duration in activities:
        fmt.print_agent_message(agent, action, "Working")
        time.sleep(duration)

    console.print()
    fmt.print_success("All agents completed their tasks")


def demo_complete():
    """Show completion message."""
    console.print("\n[bold cyan]═" * 35)
    console.print("[bold cyan]DEMO COMPLETE[/bold cyan]")
    console.print("[bold cyan]═" * 35 + "\n")

    fmt = MaxCodeFormatter(console=console)

    fmt.print_panel(
        """
Max-Code CLI UI/UX Demo Complete! 🎨

Features Demonstrated:
  ✓ Magnificent ASCII banner with gradient (ISOMETRIC1)
  ✓ Perfect alignment (TOC-friendly!)
  ✓ Color-coded semantic messages
  ✓ Constitutional principles display
  ✓ Progress indicators (spinners, bars, multi-progress)
  ✓ Agent activity visualization
  ✓ Beautiful tables and panels
  ✓ Syntax-highlighted code
  ✓ Gradient text effects

Everything is:
  • Perfectly aligned 🎯
  • Beautifully colored 🌈
  • Production-ready ⚡
  • TOC-approved 😄
        """,
        title="✨ Demo Summary ✨",
        border_style="cyan"
    )

    console.print()
    fmt.print_gradient_text("MAX-CODE CLI - A VISUAL MASTERPIECE")
    console.print()


def main():
    """Run complete visual demo."""
    try:
        # Demo 1: Banner
        demo_banner()

        time.sleep(2)

        # Demo 2: Formatter
        demo_formatter()

        time.sleep(2)

        # Demo 3: Progress Indicators
        demo_progress()

        time.sleep(2)

        # Demo 4: Agent Messages
        demo_agents()

        time.sleep(1)

        # Complete
        demo_complete()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n\n[red]Error in demo: {e}[/red]")


if __name__ == "__main__":
    main()
