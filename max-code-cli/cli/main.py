"""
Max-Code CLI - Main Command Entry Point

Integrates Click framework with rich UI components and MAXIMUS AI.
"""

import click
from pathlib import Path
from rich.console import Console

from config.settings import get_settings
from config.profiles import Profile, ProfileManager, init_profile_wizard
from ui.banner import MaxCodeBanner
from ui.formatter import MaxCodeFormatter

console = Console()
formatter = MaxCodeFormatter()


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.option('--no-banner', is_flag=True, help='Disable banner display')
@click.pass_context
def cli(ctx, version, no_banner):
    """
    Max-Code CLI - AI-Powered Development Assistant

    Powered by Claude API and MAXIMUS AI Backend.
    Constitutional AI v3.0 with Multi-Agent System.
    """
    settings = get_settings()

    # Show banner unless disabled
    if not no_banner and not settings.ui.no_banner:
        banner = MaxCodeBanner(console=console)
        banner.show(
            version=settings.version,
            context={
                'model': settings.claude.model,
            },
            style=settings.ui.banner_style if hasattr(settings.ui, 'banner_style') else 'default',
            effect=None,  # Effects opcional (pode adicionar depois)
            show_verse=True  # Verses habilitados por padrão
        )

    # Show version if requested
    if version:
        console.print(f"\n[bold cyan]{settings.app_name}[/bold cyan] [yellow]v{settings.version}[/yellow]")
        console.print(f"Environment: [green]{settings.environment}[/green]")
        console.print(f"Claude Model: [magenta]{settings.claude.model}[/magenta]\n")
        ctx.exit()

    # Start Enhanced REPL if no command provided (FASE 1 - Interactive Shell)
    if ctx.invoked_subcommand is None:
        from cli.repl_enhanced import start_enhanced_repl
        start_enhanced_repl()


@cli.command()
@click.option('--profile', type=click.Choice(['development', 'production', 'local']),
              help='Configuration profile to use')
@click.option('--interactive', is_flag=True, help='Interactive profile selection')
def init(profile, interactive):
    """
    Initialize Max-Code CLI configuration.

    Creates configuration directory and .env file with selected profile.
    """
    console.print("\n[bold cyan]Max-Code CLI - Initialization[/bold cyan]\n")

    manager = ProfileManager()

    # Interactive wizard
    if interactive:
        selected_profile = init_profile_wizard()
    elif profile:
        selected_profile = Profile(profile)
    else:
        # Default to development
        selected_profile = Profile.DEVELOPMENT
        console.print("[yellow]No profile specified, using 'development'[/yellow]")

    # Initialize profile
    manager.initialize_profile(selected_profile)

    # Success message
    console.print(f"\n[green]✓[/green] Profile '[cyan]{selected_profile.value}[/cyan]' initialized")
    console.print(f"[green]✓[/green] Configuration written to: [white]{manager.get_env_file_path()}[/white]")

    # Next steps
    console.print("\n[bold yellow]Next Steps:[/bold yellow]")
    console.print("1. Add your Claude API key to the .env file:")
    console.print(f"   [white]{manager.get_env_file_path()}[/white]")
    console.print("2. Set ANTHROPIC_API_KEY=your_key_here")
    console.print("3. Run: [cyan]max-code --help[/cyan]")
    console.print()


@cli.command()
def setup():
    """
    One-time setup for Max-Code CLI.

    Creates configuration directory and guides through API key setup.

    This command:
    1. Creates configuration directory
    2. Checks for existing API key
    3. Guides through API key setup

    Example:
      max-code setup
    """
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]       MAX-CODE CLI - FIRST TIME SETUP               [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")

    settings = get_settings()

    # Check existing API key
    console.print("[bold yellow]Step 1:[/bold yellow] Checking API key...")

    if settings.claude.api_key:
        console.print("[green]✓[/green] API key configured!\n")
        console.print("[bold green]Setup complete! You're ready to use max-code.[/bold green]\n")

        console.print("[bold yellow]Try these commands:[/bold yellow]")
        console.print("  [cyan]max-code shell[/cyan]        # Enhanced REPL")
        console.print("  [cyan]max-code chat[/cyan]         # Chat with Claude")
        console.print("  [cyan]max-code health[/cyan]       # Check services\n")

    else:
        console.print("[yellow]⚠[/yellow]  No API key found.\n")

        console.print("[bold yellow]Step 2:[/bold yellow] Set your Claude API key...")
        console.print("\nTo use Max-Code, set your Anthropic API key:\n")

        console.print("[bold]Option 1:[/bold] Environment Variable")
        console.print("  [white]export ANTHROPIC_API_KEY=\"sk-ant-api...\"[/white]\n")

        console.print("[bold]Option 2:[/bold] Add to .env file")
        console.print(f"  Edit: [white]{settings.config_dir}/.env[/white]")
        console.print("  Add: [white]ANTHROPIC_API_KEY=sk-ant-api...[/white]\n")

        console.print("[bold yellow]Get your API key:[/bold yellow]")
        console.print("  https://console.anthropic.com/settings/keys\n")


@cli.command()
def config():
    """
    Show current configuration.

    Displays all settings, validates configuration, and shows status.
    """
    settings = get_settings()

    console.print("\n[bold cyan]Max-Code CLI - Configuration[/bold cyan]\n")

    # Application
    console.print("[bold yellow]Application:[/bold yellow]")
    console.print(f"  Name: [white]{settings.app_name}[/white]")
    console.print(f"  Version: [white]{settings.version}[/white]")
    console.print(f"  Environment: [white]{settings.environment}[/white]")
    console.print()

    # Claude API
    console.print("[bold yellow]Claude API:[/bold yellow]")
    console.print(f"  Model: [white]{settings.claude.model}[/white]")
    console.print(f"  Temperature: [white]{settings.claude.temperature}[/white]")
    console.print(f"  Max Tokens: [white]{settings.claude.max_tokens}[/white]")
    api_key_status = "[green]✓ Set[/green]" if settings.claude.api_key else "[red]✗ Not Set[/red]"
    console.print(f"  API Key: {api_key_status}")
    console.print()

    # MAXIMUS Services
    console.print("[bold yellow]MAXIMUS Services:[/bold yellow]")
    console.print(f"  Core: [white]{settings.maximus.core_url}[/white]")
    console.print(f"  Penelope: [white]{settings.maximus.penelope_url}[/white]")
    console.print(f"  Orchestrator: [white]{settings.maximus.orchestrator_url}[/white]")
    console.print(f"  Oraculo: [white]{settings.maximus.oraculo_url}[/white]")
    console.print(f"  Atlas: [white]{settings.maximus.atlas_url}[/white]")
    console.print()

    # Features
    console.print("[bold yellow]Features:[/bold yellow]")
    console.print(f"  Consciousness: {_bool_status(settings.maximus.enable_consciousness)}")
    console.print(f"  Prediction: {_bool_status(settings.maximus.enable_prediction)}")
    console.print(f"  Neuromodulation: {_bool_status(settings.maximus.enable_neuromodulation)}")
    console.print(f"  Constitutional AI: {_bool_status(settings.enable_constitutional_ai)}")
    console.print(f"  Multi-Agent: {_bool_status(settings.enable_multi_agent)}")
    console.print(f"  Tree of Thoughts: {_bool_status(settings.enable_tree_of_thoughts)}")
    console.print()

    # UI
    console.print("[bold yellow]UI/UX:[/bold yellow]")
    console.print(f"  Banner Style: [white]{settings.ui.banner_style}[/white]")
    console.print(f"  Show Progress: {_bool_status(settings.ui.show_progress)}")
    console.print(f"  Show Agents: {_bool_status(settings.ui.show_agent_activity)}")
    console.print(f"  Show Consciousness: {_bool_status(settings.ui.show_consciousness)}")
    console.print(f"  Verbose: {_bool_status(settings.ui.verbose)}")
    console.print()

    # Logging
    console.print("[bold yellow]Logging:[/bold yellow]")
    console.print(f"  Level: [white]{settings.logging.log_level}[/white]")
    console.print(f"  Format: [white]{settings.logging.log_format}[/white]")
    console.print(f"  Tracing: {_bool_status(settings.logging.enable_tracing)}")
    console.print()

    # Validation
    is_valid, errors = settings.validate_configuration()
    if is_valid:
        console.print("[bold green]✓ Configuration Valid[/bold green]\n")
    else:
        console.print("[bold red]✗ Configuration Issues:[/bold red]")
        for error in errors:
            console.print(f"  [red]•[/red] {error}")
        console.print()


@cli.command()
@click.argument('profile', type=click.Choice(['development', 'production', 'local']))
def profile(profile):
    """
    Switch to a different configuration profile.

    Available profiles:
    - development: Local dev with all features enabled
    - production: Optimized for deployment
    - local: Standalone without MAXIMUS backend
    """
    manager = ProfileManager()
    selected_profile = Profile(profile)

    console.print(f"\n[bold cyan]Switching to profile: [yellow]{profile}[/yellow][/bold cyan]\n")

    # Get profile config
    config = manager.get_profile_config(selected_profile)
    console.print(f"[white]{config.description}[/white]\n")

    # Set profile
    manager.set_profile(selected_profile)

    console.print(f"[green]✓[/green] Profile activated: [cyan]{profile}[/cyan]")
    console.print(f"[green]✓[/green] Configuration updated: [white]{manager.get_env_file_path()}[/white]\n")


@cli.command()
def profiles():
    """
    List all available configuration profiles.
    """
    from rich.table import Table

    manager = ProfileManager()
    current_profile = manager.get_current_profile()

    console.print("\n[bold cyan]Available Profiles[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Profile", style="cyan", width=15)
    table.add_column("Description", style="white", width=50)
    table.add_column("Status", style="green", width=10)

    for prof, config in manager.list_profiles().items():
        status = "✓ Active" if prof == current_profile else ""
        table.add_row(prof.value, config.description, status)

    console.print(table)
    console.print()


@cli.command()
@click.argument('prompt', nargs=-1, required=True)
@click.option('--agent', type=click.Choice(['sophia', 'code', 'test', 'review', 'guardian']),
              help='Specific agent to use')
@click.option('--stream', is_flag=True, default=True, help='Stream responses (default: true)')
@click.option('--show-thoughts', is_flag=True, help='Show Tree of Thoughts visualization')
@click.option('--consciousness', is_flag=True, help='Show consciousness state')
def chat(prompt, agent, stream, show_thoughts, consciousness):
    """
    Chat with Max-Code AI assistant.

    Examples:
      max-code chat "How do I implement authentication?"
      max-code chat --agent sophia "Explain this codebase"
      max-code chat --consciousness "Design a REST API"
    """
    from core.chat_integration import ChatIntegration

    prompt_text = ' '.join(prompt)

    console.print(f"\n[bold cyan]Max-Code AI Assistant[/bold cyan]")
    if agent:
        console.print(f"Agent: [yellow]{agent.title()}[/yellow]")
    console.print()

    # User input
    console.print(f"[bold white]You:[/bold white] {prompt_text}\n")

    # Initialize chat integration
    try:
        integration = ChatIntegration()

        # Stream response with Rich
        console.print("[bold cyan]Max-Code:[/bold cyan] ", end="")
        for token in integration.chat(
            user_input=prompt_text,
            agent=agent,
            stream=stream,
            show_consciousness=consciousness
        ):
            console.print(token, end="")

        console.print("\n")  # Final newline

        # Close integration
        integration.close()

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--agent', type=click.Choice(['code', 'review']), default='code',
              help='Agent to use (default: code)')
def analyze(file_path, output, agent):
    """
    Analyze code file or directory.

    Examples:
      max-code analyze src/main.py
      max-code analyze --agent review src/
      max-code analyze --output report.md src/
    """
    console.print(f"\n[bold cyan]Code Analysis[/bold cyan]")
    console.print(f"Agent: [yellow]{agent.title()}[/yellow]")
    console.print(f"Target: [white]{file_path}[/white]\n")

    # Stub: Will integrate with MAXIMUS tomorrow
    console.print("[yellow]⚠ Analysis integration coming in FASE 6-8 (tomorrow)[/yellow]")
    console.print("[white]This will provide:[/white]")
    console.print("  • Code quality metrics")
    console.print("  • Security analysis")
    console.print("  • Best practices check")
    console.print("  • Refactoring suggestions")
    console.print()


@cli.command()
@click.argument('description', nargs=-1, required=True)
@click.option('--test-file', type=click.Path(), help='Generate test file')
@click.option('--framework', type=click.Choice(['pytest', 'unittest']), default='pytest',
              help='Testing framework (default: pytest)')
@click.option('--stream/--no-stream', default=True, help='Stream responses (default: true)')
def generate(description, test_file, framework, stream):
    """
    Generate code or tests from description.

    Examples:
      max-code generate "REST API endpoint for users"
      max-code generate --test-file tests/test_api.py "User authentication"
      max-code generate "Python function to check if number is prime"
    """
    from core.llm.unified_client import UnifiedLLMClient

    desc_text = ' '.join(description)

    console.print(f"\n[bold cyan]Code Generation[/bold cyan]")
    console.print(f"Description: [white]{desc_text}[/white]")
    if test_file:
        console.print(f"Test Framework: [yellow]{framework}[/yellow]")
    console.print()

    # Build prompt for code generation
    if test_file:
        prompt = f"""Generate {framework} tests for: {desc_text}

Requirements:
- Use {framework} framework
- Include comprehensive test cases
- Add docstrings
- Follow best practices"""
    else:
        prompt = f"""Generate production-ready code for: {desc_text}

Requirements:
- Clean, readable code
- Type hints
- Docstrings
- Error handling
- Best practices"""

    try:
        # Initialize LLM client with fallback
        client = UnifiedLLMClient()

        console.print("[bold cyan]Generated Code:[/bold cyan]\n")

        if stream:
            # Stream response
            for token in client.chat(message=prompt, stream=True):
                console.print(token, end="")
            console.print("\n")
        else:
            # Non-streaming
            response = client.chat(message=prompt, stream=False)
            console.print(response)
            console.print()

    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]⚠️  Claude API not available. Set ANTHROPIC_API_KEY in .env[/yellow]")
        console.print("[yellow]    Or set GEMINI_API_KEY for Gemini fallback[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
def health():
    """
    Check health of all services (Claude API + MAXIMUS backend).
    """
    from rich.table import Table
    from core import get_integration_manager

    settings = get_settings()

    console.print("\n[bold cyan]Service Health Check[/bold cyan]\n")

    # Get integration manager
    manager = get_integration_manager()
    summary = manager.get_service_summary()

    # Integration Mode
    mode_color = {
        "full": "green",
        "partial": "yellow",
        "standalone": "red"
    }.get(summary["mode"], "white")

    console.print(f"Integration Mode: [{mode_color}]{summary['mode'].upper()}[/{mode_color}]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Service", style="white", width=20)
    table.add_column("URL", style="cyan", width=40)
    table.add_column("Status", style="white", width=15)

    # Claude API
    api_status = "[green]✓ Ready[/green]" if settings.claude.api_key else "[red]✗ No API Key[/red]"
    table.add_row("Claude API", settings.claude.model, api_status)

    # MAXIMUS Services with real status
    services = [
        ("MAXIMUS Core", settings.maximus.core_url, summary["services"].get("maximus")),
        ("Penelope", settings.maximus.penelope_url, summary["services"].get("penelope")),
        ("Orchestrator", settings.maximus.orchestrator_url, summary["services"].get("orchestrator")),
        ("Oraculo", settings.maximus.oraculo_url, summary["services"].get("oraculo")),
        ("Atlas", settings.maximus.atlas_url, summary["services"].get("atlas")),
    ]

    for name, url, status in services:
        status_display = {
            "healthy": "[green]✓ Healthy[/green]",
            "degraded": "[yellow]⚠ Degraded[/yellow]",
            "unhealthy": "[red]✗ Unhealthy[/red]",
            "unknown": "[red]✗ Unknown[/red]"
        }.get(status, "[red]✗ Unknown[/red]")
        table.add_row(name, url, status_display)

    console.print(table)

    # Feature availability
    console.print("\n[bold cyan]Feature Availability:[/bold cyan]")
    features = summary["features"]
    for feature, available in features.items():
        icon = "✓" if available else "✗"
        color = "green" if available else "red"
        console.print(f"  [{color}]{icon}[/{color}] {feature.title()}")

    console.print()


@cli.command()
def agents():
    """
    Show available AI agents and their capabilities.
    """
    from rich.table import Table

    console.print("\n[bold cyan]Max-Code AI Agents[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Agent", style="yellow", width=12)
    table.add_column("Role", style="white", width=20)
    table.add_column("Capabilities", style="cyan", width=50)

    agents_data = [
        ("Sophia", "Architect", "System design, planning, architecture decisions"),
        ("Code", "Developer", "Code generation, refactoring, implementation"),
        ("Test", "QA Engineer", "Test generation, coverage analysis, debugging"),
        ("Review", "Code Reviewer", "Code quality, security, best practices"),
        ("Guardian", "Ethics Monitor", "Constitutional AI, ethical oversight"),
    ]

    for agent, role, capabilities in agents_data:
        table.add_row(agent, role, capabilities)

    console.print(table)
    console.print("\n[bold yellow]Features:[/bold yellow]")
    console.print("  • Multi-agent collaboration")
    console.print("  • Constitutional AI v3.0 governance")
    console.print("  • Tree of Thoughts reasoning")
    console.print("  • MAXIMUS consciousness integration")
    console.print()


def _bool_status(value: bool) -> str:
    """Convert boolean to status string."""
    return "[green]✓ Enabled[/green]" if value else "[red]✗ Disabled[/red]"


# Import and register health command (FASE 7)
try:
    from cli.health_command import health
    cli.add_command(health, name='health')
except ImportError as e:
    console.print(f"[yellow]Warning: Health command not available: {e}[/yellow]")

# Import and register predict command (FASE 9)
try:
    from cli.predict_command import predict
    cli.add_command(predict, name='predict')
except ImportError as e:
    console.print(f"[yellow]Warning: Predict command not available: {e}[/yellow]")

# Import and register learn command (FASE 9)
try:
    from cli.learn_command import learn
    cli.add_command(learn, name='learn')
except ImportError as e:
    console.print(f"[yellow]Warning: Learn command not available: {e}[/yellow]")

# Import and register sabbath command (FASE 9)
try:
    from cli.sabbath_command import sabbath
    cli.add_command(sabbath, name='sabbath')
except ImportError as e:
    console.print(f"[yellow]Warning: Sabbath command not available: {e}[/yellow]")

# Import and register task command (FASE 11 - Autonomous Agent)
try:
    from cli.task_command import task
    cli.add_command(task, name='task')
except ImportError as e:
    console.print(f"[yellow]Warning: Task command not available: {e}[/yellow]")

# Import and register streaming demo commands (Enhanced Thinking Display)
try:
    from cli.demo_streaming import demo_streaming, demo_streaming_all
    cli.add_command(demo_streaming, name='demo-streaming')
    cli.add_command(demo_streaming_all, name='demo-streaming-all')
except ImportError as e:
    console.print(f"[yellow]Warning: Streaming demo commands not available: {e}[/yellow]")

# Import and register P.P.B.P.R command (FASE 11 - Methodology Automation)
try:
    from cli.ppbpr_command import app as ppbpr_app
    # Convert Typer app to Click command
    import typer
    ppbpr_click = typer.main.get_command(ppbpr_app)
    cli.add_command(ppbpr_click, name='ppbpr')
except ImportError as e:
    console.print(f"[yellow]Warning: P.P.B.P.R command not available: {e}[/yellow]")

# Import and register B.P.R command (FASE 11 - B.P.R Variant)
try:
    from cli.bpr_command import app as bpr_app
    # Convert Typer app to Click command
    import typer
    bpr_click = typer.main.get_command(bpr_app)
    cli.add_command(bpr_click, name='bpr')
except ImportError as e:
    console.print(f"[yellow]Warning: B.P.R command not available: {e}[/yellow]")


@cli.command()
def repl():
    """
    Start interactive REPL shell.

    Features:
    - Natural language commands
    - EPL (Emoji Protocol Language) support
    - Command history (↑/↓)
    - Auto-completion (Tab)
    - Special commands (/help, /agents, /status, etc)
    - Command palette (Ctrl+P)
    - Agent shortcuts (/sophia, /code, /test, etc)
    - DREAM mode (Ctrl+D)

    Example:
      max-code repl
    """
    from cli.repl_enhanced import start_enhanced_repl
    start_enhanced_repl()


@cli.command()
def shell():
    """
    Start interactive REPL shell (alias for 'repl').

    Same as 'max-code repl' - launches Enhanced REPL with all features.
    """
    from cli.repl_enhanced import start_enhanced_repl
    start_enhanced_repl()


# Import and register Health Check command (FASE 7 - Health Monitoring)
try:
    from cli.commands.health import health as health_cmd
    cli.add_command(health_cmd, name='health')
except ImportError as e:
    console.print(f"[yellow]Warning: Health command not available: {e}[/yellow]")


if __name__ == '__main__':
    cli()
