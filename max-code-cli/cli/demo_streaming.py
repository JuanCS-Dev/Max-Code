"""
Streaming Demo Command - Showcase Enhanced Thinking Display

Demonstrates world-class streaming with thinking process for all agents.

Usage:
    max-code demo-streaming [OPTIONS] PROMPT
    
Examples:
    max-code demo-streaming "Create a binary search function"
    max-code demo-streaming --agent test "Write tests for fibonacci"
    max-code demo-streaming --agent fix "Fix this bug: TypeError..."
    
Soli Deo Gloria
"""

import click
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from sdk.base_agent import AgentTask
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.fix_agent import FixAgent
from agents.docs_agent import DocsAgent
from agents.review_agent import ReviewAgent


console = Console()


@click.command(name="demo-streaming")
@click.argument("prompt")
@click.option(
    "--agent",
    type=click.Choice(["code", "test", "fix", "docs", "review"], case_sensitive=False),
    default="code",
    help="Agent to use for demo",
)
@click.option(
    "--language",
    default="python",
    help="Programming language (for code agent)",
)
@click.option(
    "--no-thinking",
    is_flag=True,
    help="Disable thinking display (standard execution)",
)
@click.option(
    "--guardian/--no-guardian",
    default=True,
    help="Enable/disable Guardian validation",
)
def demo_streaming(
    prompt: str,
    agent: str,
    language: str,
    no_thinking: bool,
    guardian: bool,
):
    """
    🎬 Demo Enhanced Streaming with Thinking Process
    
    Shows real-time thinking, tool usage, and output generation.
    """
    # Welcome banner
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[bold cyan]⚡ MAX-CODE STREAMING DEMO[/bold cyan]\n\n"
            f"[dim]Agent:[/dim] [bold]{agent.upper()}[/bold]\n"
            f"[dim]Thinking:[/dim] [bold]{'disabled' if no_thinking else 'enabled'}[/bold]\n"
            f"[dim]Guardian:[/dim] [bold]{'enabled' if guardian else 'disabled'}[/bold]"
        ),
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()
    
    # Create task
    task = AgentTask(
        id=f"demo-{agent}-001",
        description=prompt,
        agent_name=agent,
        parameters={
            'language': language,
        }
    )
    
    # Select agent
    agent_instance = _get_agent(agent, guardian)
    
    if not agent_instance:
        console.print("[red]❌ Agent not available[/red]")
        return
    
    # Execute
    try:
        if no_thinking:
            # Standard execution (no streaming)
            console.print("[yellow]Running without thinking display...[/yellow]\n")
            result = agent_instance.execute(task)
        else:
            # Enhanced execution with thinking
            console.print("[cyan]⚡ Starting enhanced execution with thinking display...[/cyan]\n")
            result = agent_instance.execute_with_thinking_sync(task)
        
        # Display result
        _display_result(result, agent)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


def _get_agent(agent_type: str, with_guardian: bool):
    """Get agent instance"""
    try:
        if agent_type == "code":
            return CodeAgent(enable_guardian=with_guardian)
        elif agent_type == "test":
            return TestAgent(enable_guardian=with_guardian)
        elif agent_type == "fix":
            return FixAgent(enable_guardian=with_guardian)
        elif agent_type == "docs":
            return DocsAgent(enable_guardian=with_guardian)
        elif agent_type == "review":
            return ReviewAgent(enable_guardian=with_guardian)
        return None
    except Exception as e:
        console.print(f"[red]Failed to initialize agent: {e}[/red]")
        return None


def _display_result(result, agent_type: str):
    """Display execution result"""
    console.print()
    console.print("─" * 80)
    
    if result.success:
        console.print("[bold green]✓ EXECUTION SUCCESSFUL[/bold green]\n")
        
        # Display output
        output = result.output
        
        if isinstance(output, dict):
            if 'code' in output:
                from rich.syntax import Syntax
                console.print(Panel(
                    Syntax(output['code'], "python", theme="monokai", line_numbers=True),
                    title="[bold green]Generated Code",
                    border_style="green",
                ))
            
            if 'security_issues' in output and output['security_issues']:
                console.print()
                console.print("[yellow]⚠️ Security Issues Found:[/yellow]")
                for issue in output['security_issues']:
                    console.print(f"  • {issue}")
            
            if 'tests' in output:
                console.print(Panel(
                    output['tests'],
                    title="[bold green]Generated Tests",
                    border_style="green",
                ))
        else:
            console.print(output)
        
        # Display metrics
        if result.metrics:
            console.print()
            console.print("[dim]Metrics:[/dim]")
            for key, value in result.metrics.items():
                console.print(f"  [dim]{key}:[/dim] {value}")
    
    else:
        console.print("[bold red]✗ EXECUTION FAILED[/bold red]\n")
        console.print(f"[red]Error:[/red] {result.output.get('error', 'Unknown error')}")
        
        if 'reasoning' in result.output:
            console.print(f"[dim]Reasoning:[/dim] {result.output['reasoning']}")
        
        if 'recommendations' in result.output:
            console.print()
            console.print("[yellow]Recommendations:[/yellow]")
            for rec in result.output['recommendations']:
                console.print(f"  • {rec}")
    
    console.print()
    console.print("─" * 80)


@click.command(name="demo-streaming-all")
@click.argument("prompt")
def demo_streaming_all(prompt: str):
    """
    🎬 Demo Streaming with ALL Agents
    
    Runs the same prompt through all agents with thinking display.
    """
    agents = ["code", "test", "docs", "review"]
    
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[bold cyan]⚡ MAX-CODE MULTI-AGENT STREAMING DEMO[/bold cyan]\n\n"
            f"[dim]Running:[/dim] [bold]{len(agents)} agents[/bold]\n"
            f"[dim]Prompt:[/dim] {prompt[:60]}..."
        ),
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()
    
    for agent_type in agents:
        console.print(f"\n{'='*80}")
        console.print(f"[bold cyan]AGENT: {agent_type.upper()}[/bold cyan]")
        console.print(f"{'='*80}\n")
        
        # Create task
        task = AgentTask(
            id=f"demo-{agent_type}-001",
            description=prompt,
            agent_name=agent_type,
        )
        
        # Get agent
        agent_instance = _get_agent(agent_type, guardian=True)
        
        if not agent_instance:
            console.print(f"[red]❌ {agent_type} agent not available[/red]")
            continue
        
        # Execute
        try:
            result = agent_instance.execute_with_thinking_sync(task)
            _display_result(result, agent_type)
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
        
        console.print()


# Export commands
__all__ = ["demo_streaming", "demo_streaming_all"]
