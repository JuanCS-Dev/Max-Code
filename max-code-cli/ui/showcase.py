"""
UI Showcase - Demo all Max-Code CLI UI components

This script demonstrates all UI components in action with realistic scenarios.
"""

import time
from rich.console import Console
from rich.panel import Panel

from ui.banner_vcli_style import show_banner
from ui.formatter import MaxCodeFormatter
from ui.progress import ProgressTracker, TaskProgress
from ui.agent_display import AgentActivityDisplay, AgentState, AgentStatus
from ui.tree_of_thoughts import TreeOfThoughts, ThoughtNode, ThoughtStatus
from ui.streaming import StreamingDisplay
from ui.validation import ValidationDisplay, ValidationLevel
from ui.exceptions import ExceptionDisplay
from ui.utils import print_header, print_success, print_info, console


def showcase_banner():
    """Demo banner display."""
    print_header(console, "1. Banner Display", "Stylized ASCII art banner")
    show_banner()
    time.sleep(2)


def showcase_formatter():
    """Demo formatter."""
    print_header(console, "2. Message Formatter", "Styled message display")

    formatter = MaxCodeFormatter()

    formatter.system("System initialized successfully")
    formatter.info("Loading configuration from .env file")
    formatter.success("Configuration loaded: development profile")
    formatter.warning("Claude API key not set (optional for testing)")
    formatter.error("Failed to connect to MAXIMUS Core service")

    console.print()
    time.sleep(2)


def showcase_progress():
    """Demo progress tracking."""
    print_header(console, "3. Progress Tracking", "Multi-task progress with live updates")

    tracker = ProgressTracker(total_tasks=4)

    tracker.add_task("analyze", "Analyzing codebase", total_steps=100)
    tracker.add_task("test", "Running test suite", total_steps=50)
    tracker.add_task("build", "Building project", total_steps=75)
    tracker.add_task("deploy", "Deploying to production", total_steps=25)

    with tracker:
        # Simulate progress
        for i in range(100):
            tracker.update_task("analyze", advance=1)
            time.sleep(0.02)

        tracker.complete_task("analyze", "Analyzed 1,234 files")

        for i in range(50):
            tracker.update_task("test", advance=1)
            time.sleep(0.02)

        tracker.complete_task("test", "48/48 tests passed")

        for i in range(75):
            tracker.update_task("build", advance=1)
            time.sleep(0.01)

        tracker.complete_task("build", "Build successful")

        for i in range(25):
            tracker.update_task("deploy", advance=1)
            time.sleep(0.03)

        tracker.complete_task("deploy", "Deployed to production")

    console.print()
    time.sleep(1)


def showcase_agents():
    """Demo agent activity display."""
    print_header(console, "4. Multi-Agent System", "Real-time agent activity dashboard")

    display = AgentActivityDisplay()

    # Register agents
    display.register_agent("sophia", "Architect", "System design and planning")
    display.register_agent("code", "Developer", "Code generation and refactoring")
    display.register_agent("test", "QA Engineer", "Testing and validation")
    display.register_agent("review", "Reviewer", "Code quality review")
    display.register_agent("guardian", "Ethics", "Constitutional AI oversight")

    with display:
        # Sophia planning
        display.update_agent("sophia", AgentStatus.ACTIVE, "Analyzing requirements")
        time.sleep(1)
        display.update_agent("sophia", AgentStatus.ACTIVE, "Designing architecture")
        time.sleep(1)
        display.update_agent("sophia", AgentStatus.COMPLETED, "Architecture complete")

        # Code implementing
        display.update_agent("code", AgentStatus.ACTIVE, "Generating REST API")
        time.sleep(1)
        display.update_agent("code", AgentStatus.ACTIVE, "Adding authentication")
        time.sleep(1)
        display.update_agent("code", AgentStatus.COMPLETED, "Implementation complete")

        # Test testing
        display.update_agent("test", AgentStatus.ACTIVE, "Writing unit tests")
        time.sleep(1)
        display.update_agent("test", AgentStatus.ACTIVE, "Running test suite")
        time.sleep(1)
        display.update_agent("test", AgentStatus.COMPLETED, "All tests passed")

        # Review reviewing
        display.update_agent("review", AgentStatus.ACTIVE, "Checking code quality")
        time.sleep(1)
        display.update_agent("review", AgentStatus.COMPLETED, "Quality approved")

        # Guardian monitoring
        display.update_agent("guardian", AgentStatus.ACTIVE, "Ethical validation")
        time.sleep(1)
        display.update_agent("guardian", AgentStatus.COMPLETED, "Constitutional compliance ✓")

        time.sleep(1)

    console.print()
    time.sleep(1)


def showcase_tree_of_thoughts():
    """Demo Tree of Thoughts."""
    print_header(console, "5. Tree of Thoughts", "Advanced reasoning visualization")

    tree = TreeOfThoughts(max_depth=3)

    with tree:
        # Root thought
        root = tree.add_thought(
            "Design authentication system",
            "How should we implement secure user authentication?"
        )
        time.sleep(0.5)

        # Branch 1: JWT
        jwt = tree.add_thought(
            "Use JWT tokens",
            "Stateless authentication with JSON Web Tokens",
            parent_id=root,
            score=0.8
        )
        time.sleep(0.5)

        tree.add_thought(
            "Store in httpOnly cookies",
            "Secure client-side storage",
            parent_id=jwt,
            score=0.9,
            status=ThoughtStatus.SELECTED
        )
        time.sleep(0.5)

        tree.add_thought(
            "Use localStorage",
            "Simpler but less secure",
            parent_id=jwt,
            score=0.4,
            status=ThoughtStatus.REJECTED
        )
        time.sleep(0.5)

        # Branch 2: Sessions
        session = tree.add_thought(
            "Use server sessions",
            "Traditional session-based auth",
            parent_id=root,
            score=0.6
        )
        time.sleep(0.5)

        tree.add_thought(
            "Redis session store",
            "Fast distributed sessions",
            parent_id=session,
            score=0.7
        )
        time.sleep(0.5)

        # Branch 3: OAuth
        oauth = tree.add_thought(
            "OAuth 2.0",
            "Third-party authentication",
            parent_id=root,
            score=0.7
        )
        time.sleep(0.5)

        tree.add_thought(
            "Google + GitHub",
            "Support multiple providers",
            parent_id=oauth,
            score=0.8
        )
        time.sleep(0.5)

        time.sleep(2)

    console.print()
    time.sleep(1)


def showcase_streaming():
    """Demo streaming display."""
    print_header(console, "6. Streaming Responses", "Live AI response streaming")

    display = StreamingDisplay(show_thinking=True)

    message = """
    I'll help you implement user authentication. Here's my approach:

    First, let's use JWT tokens for stateless authentication. This approach offers:
    - Scalability: No server-side session storage required
    - Security: Cryptographically signed tokens
    - Portability: Works across different domains

    Implementation steps:
    1. Create user registration endpoint
    2. Hash passwords with bcrypt
    3. Generate JWT on successful login
    4. Validate JWT on protected routes
    5. Implement refresh token rotation

    Let me generate the code for you...
    """

    display.start_streaming()

    for char in message:
        display.stream_chunk(char)
        time.sleep(0.01)

    display.end_streaming()

    console.print()
    time.sleep(1)


def showcase_validation():
    """Demo validation display."""
    print_header(console, "7. Validation & Quality Checks", "Code quality and security validation")

    display = ValidationDisplay()

    checks = [
        ("Code Quality", ValidationLevel.SUCCESS, "All quality metrics passed"),
        ("Security Scan", ValidationLevel.SUCCESS, "No vulnerabilities found"),
        ("Type Checking", ValidationLevel.WARNING, "2 type hints missing"),
        ("Test Coverage", ValidationLevel.SUCCESS, "Coverage: 87%"),
        ("Documentation", ValidationLevel.WARNING, "3 functions missing docstrings"),
        ("Performance", ValidationLevel.SUCCESS, "All benchmarks passed"),
    ]

    display.start_validation("Running quality checks")

    for name, level, message in checks:
        display.add_check(name, level, message)
        time.sleep(0.3)

    display.complete_validation()

    console.print()
    time.sleep(1)


def showcase_exceptions():
    """Demo exception display."""
    print_header(console, "8. Exception Handling", "User-friendly error display")

    display = ExceptionDisplay()

    try:
        # Simulate an error
        raise ValueError("Invalid configuration: ANTHROPIC_API_KEY not set")
    except Exception as e:
        display.show_exception(
            e,
            context="Initializing Claude API client",
            suggestions=[
                "Set ANTHROPIC_API_KEY in .env file",
                "Run: max-code init --profile development",
                "Get API key from: https://console.anthropic.com/",
            ]
        )

    console.print()
    time.sleep(2)


def main():
    """Run full UI showcase."""
    console.print("\n[bold cyan]═" * 40)
    console.print("[bold cyan]MAX-CODE CLI - UI COMPONENT SHOWCASE")
    console.print("[bold cyan]═" * 40 + "[/bold cyan]\n")

    time.sleep(1)

    showcase_banner()
    showcase_formatter()
    showcase_progress()
    showcase_agents()
    showcase_tree_of_thoughts()
    showcase_streaming()
    showcase_validation()
    showcase_exceptions()

    console.print("\n[bold green]✓ All UI components showcased successfully![/bold green]")
    console.print("[bold cyan]═" * 40 + "[/bold cyan]\n")


if __name__ == "__main__":
    main()
