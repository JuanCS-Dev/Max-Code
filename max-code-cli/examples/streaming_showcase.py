#!/usr/bin/env python3
"""
Streaming Showcase - Live Examples of Enhanced Thinking Display

Run this script to see world-class streaming in action.

Usage:
    python examples/streaming_showcase.py

Soli Deo Gloria
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from core.streaming import (
    EnhancedThinkingDisplay,
    ThinkingPhase,
    ThinkingDisplayConfig,
)
from agents.code_agent import CodeAgent
from sdk.agent_task import AgentTask


console = Console()


async def demo_basic_thinking():
    """Demo 1: Basic thinking display"""
    console.print()
    console.print(Panel(
        "[bold cyan]Demo 1: Basic Thinking Display[/bold cyan]\n"
        "[dim]Shows thinking steps without actual agent execution[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    async with EnhancedThinkingDisplay(agent_name="demo") as display:
        # Initialize
        display.add_thinking_step(
            ThinkingPhase.INITIALIZING,
            "Starting demonstration..."
        )
        await display.update()
        await asyncio.sleep(1)
        display.complete_thinking_step()
        
        # Analyze
        display.add_thinking_step(
            ThinkingPhase.ANALYZING,
            "Analyzing requirements and context..."
        )
        await display.update()
        await asyncio.sleep(1.5)
        display.complete_thinking_step("Requirements understood")
        
        # Plan
        display.add_thinking_step(
            ThinkingPhase.PLANNING,
            "Planning implementation strategy..."
        )
        await display.update()
        await asyncio.sleep(1.2)
        display.complete_thinking_step("Plan created")
        
        # Execute
        display.add_thinking_step(
            ThinkingPhase.EXECUTING,
            "Generating output..."
        )
        await display.update()
        await asyncio.sleep(1)
        
        # Add output
        display.add_output("Hello from Enhanced Thinking Display!")
        display.add_output("This is a demonstration of world-class streaming.")
        await display.update()
        await asyncio.sleep(0.5)
        
        # Complete
        display.complete_thinking_step("Output generated")
        display.add_thinking_step(
            ThinkingPhase.COMPLETING,
            "Demonstration complete"
        )
        await display.update()
        await asyncio.sleep(1)
    
    console.print("[green]✓ Demo 1 complete[/green]\n")


async def demo_tool_tracking():
    """Demo 2: Tool use tracking"""
    console.print()
    console.print(Panel(
        "[bold cyan]Demo 2: Tool Use Tracking[/bold cyan]\n"
        "[dim]Shows how tool invocations are tracked and displayed[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    config = ThinkingDisplayConfig(
        show_thinking=True,
        show_tools=True,
        show_metrics=True,
    )
    
    async with EnhancedThinkingDisplay(agent_name="tools", config=config) as display:
        # Start
        display.add_thinking_step(
            ThinkingPhase.ANALYZING,
            "Preparing to use tools..."
        )
        await display.update()
        await asyncio.sleep(0.8)
        
        # Tool 1: Read file
        display.add_tool_use("read_file", {"path": "main.py"})
        await display.update()
        await asyncio.sleep(1)
        display.complete_tool_use("read_file", "File content loaded (250 lines)")
        await display.update()
        await asyncio.sleep(0.5)
        
        # Tool 2: Analyze code
        display.add_tool_use("analyze_complexity", {"file": "main.py"})
        await display.update()
        await asyncio.sleep(1.2)
        display.complete_tool_use("analyze_complexity", {"score": 8, "quality": "good"})
        await display.update()
        await asyncio.sleep(0.5)
        
        # Tool 3: Write file
        display.add_tool_use("write_file", {"path": "output.txt", "content": "..."})
        await display.update()
        await asyncio.sleep(0.8)
        display.complete_tool_use("write_file", "File written successfully")
        await display.update()
        
        # Complete
        display.add_thinking_step(
            ThinkingPhase.COMPLETING,
            "All tools executed successfully"
        )
        await display.update()
        await asyncio.sleep(1)
    
    console.print("[green]✓ Demo 2 complete[/green]\n")


async def demo_code_preview():
    """Demo 3: Code preview"""
    console.print()
    console.print(Panel(
        "[bold cyan]Demo 3: Code Preview[/bold cyan]\n"
        "[dim]Shows live code generation with syntax highlighting[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    config = ThinkingDisplayConfig(
        show_thinking=True,
        show_code_preview=True,
    )
    
    async with EnhancedThinkingDisplay(agent_name="code", config=config) as display:
        # Planning
        display.add_thinking_step(
            ThinkingPhase.PLANNING,
            "Designing function structure..."
        )
        await display.update()
        await asyncio.sleep(1)
        display.complete_thinking_step()
        
        # Generating
        display.add_thinking_step(
            ThinkingPhase.EXECUTING,
            "Generating code..."
        )
        await display.update()
        
        # Add code incrementally
        code_lines = [
            "def fibonacci(n: int) -> int:",
            "    \"\"\"Calculate fibonacci number.\"\"\"",
            "    if n <= 1:",
            "        return n",
            "    return fibonacci(n-1) + fibonacci(n-2)",
        ]
        
        code = ""
        for line in code_lines:
            code += line + "\n"
            display.add_code(code, language="python")
            await display.update()
            await asyncio.sleep(0.5)
        
        # Complete
        display.complete_thinking_step("Code generated")
        display.add_thinking_step(
            ThinkingPhase.VALIDATING,
            "Validating code quality..."
        )
        await display.update()
        await asyncio.sleep(1)
        display.complete_thinking_step("Code validated ✓")
        await display.update()
        await asyncio.sleep(0.5)
    
    console.print("[green]✓ Demo 3 complete[/green]\n")


async def demo_error_handling():
    """Demo 4: Error handling"""
    console.print()
    console.print(Panel(
        "[bold cyan]Demo 4: Error Handling[/bold cyan]\n"
        "[dim]Shows how errors are displayed gracefully[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    async with EnhancedThinkingDisplay(agent_name="error") as display:
        # Start normally
        display.add_thinking_step(
            ThinkingPhase.ANALYZING,
            "Processing request..."
        )
        await display.update()
        await asyncio.sleep(1)
        display.complete_thinking_step()
        
        # Execute with error
        display.add_thinking_step(
            ThinkingPhase.EXECUTING,
            "Executing operation..."
        )
        await display.update()
        await asyncio.sleep(1)
        
        # Tool fails
        display.add_tool_use("risky_operation", {"data": "test"})
        await display.update()
        await asyncio.sleep(0.8)
        display.fail_tool_use("risky_operation", "Connection timeout after 5s")
        await display.update()
        
        # Error phase
        display.add_thinking_step(
            ThinkingPhase.ERROR,
            "Operation failed: Connection timeout"
        )
        await display.update()
        await asyncio.sleep(2)
    
    console.print("[yellow]✓ Demo 4 complete (error handled gracefully)[/yellow]\n")


async def demo_real_agent():
    """Demo 5: Real agent execution (requires API key)"""
    console.print()
    console.print(Panel(
        "[bold cyan]Demo 5: Real Agent Execution[/bold cyan]\n"
        "[dim]Executes actual CodeAgent with streaming[/dim]\n"
        "[yellow]⚠️  Requires ANTHROPIC_API_KEY in environment[/yellow]",
        border_style="cyan"
    ))
    console.print()
    
    # Check if API key exists
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[yellow]⚠️  ANTHROPIC_API_KEY not found, skipping real agent demo[/yellow]")
        console.print("[dim]Set ANTHROPIC_API_KEY to run this demo[/dim]\n")
        return
    
    try:
        # Create agent and task
        agent = CodeAgent()
        task = AgentTask(
            id="demo-real-001",
            description="Create a simple hello world function in Python",
            parameters={'language': 'python'}
        )
        
        # Execute with thinking
        console.print("[cyan]Executing real agent...[/cyan]\n")
        result = await agent.execute_with_thinking(task)
        
        # Display result
        if result.success:
            console.print()
            console.print("[bold green]✓ Agent execution successful![/bold green]\n")
            
            from rich.syntax import Syntax
            console.print(Panel(
                Syntax(
                    result.output['code'],
                    "python",
                    theme="monokai",
                    line_numbers=True
                ),
                title="[bold green]Generated Code",
                border_style="green"
            ))
        else:
            console.print(f"[red]✗ Agent execution failed: {result.output.get('error')}[/red]")
    
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        console.print("[dim]Note: This demo requires Claude API access[/dim]")
    
    console.print()


async def main():
    """Run all demos"""
    console.print()
    console.print(Panel(
        Text.from_markup(
            "[bold cyan]⚡ ENHANCED STREAMING SHOWCASE[/bold cyan]\n\n"
            "[dim]World-class streaming with thinking display[/dim]\n"
            "[dim]Demonstrating all features[/dim]"
        ),
        border_style="cyan",
        padding=(1, 2),
    ))
    
    demos = [
        ("Basic Thinking Display", demo_basic_thinking),
        ("Tool Use Tracking", demo_tool_tracking),
        ("Code Preview", demo_code_preview),
        ("Error Handling", demo_error_handling),
        ("Real Agent Execution", demo_real_agent),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        console.print(f"\n[bold]Running Demo {i}/{len(demos)}: {name}[/bold]")
        console.input("[dim]Press Enter to continue...[/dim]")
        
        try:
            await demo_func()
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  Interrupted by user[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]✗ Demo failed: {e}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
    
    console.print()
    console.print(Panel(
        "[bold green]✓ ALL DEMOS COMPLETE[/bold green]\n"
        "[dim]Enhanced streaming showcase finished[/dim]",
        border_style="green"
    ))
    console.print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Showcase interrupted[/yellow]")
