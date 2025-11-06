"""
Max-Code CLI - Autonomous Task Command

Executes tasks autonomously using Claude Agent SDK pattern.
User provides natural language task, agent chooses tools and executes.
"""

import click
import asyncio
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path

from anthropic import Anthropic, AnthropicBedrock, AnthropicVertex
from config.settings import get_settings

console = Console()


@click.command()
@click.argument('task', nargs=-1, required=True)
@click.option('--cwd', type=click.Path(exists=True), default='.',
              help='Working directory for task execution')
@click.option('--no-stream', is_flag=True,
              help='Disable streaming output')
@click.option('--show-tools', is_flag=True,
              help='Show tool usage details')
def task(task, cwd, no_stream, show_tools):
    """
    Execute tasks autonomously using natural language.

    Max-Code will analyze your request, choose appropriate tools,
    and execute the task automatically. Similar to Claude Code.

    Examples:
      max-code task "Create a C++ calculator with GUI"
      max-code task "Fix the bug in app.py"
      max-code task "Analyze code quality and generate report"
      max-code task "Setup a Flask API with authentication"

    Features:
    - Autonomous tool selection (Read, Write, Bash, etc.)
    - Multi-step task execution
    - Real-time streaming output
    - Context-aware file operations
    """
    task_text = ' '.join(task)

    # Show task banner
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]Task:[/bold cyan] {task_text}\n"
        f"[dim]Working Directory: {Path(cwd).resolve()}[/dim]",
        border_style="cyan",
        title="[bold]Max-Code Autonomous Agent[/bold]"
    ))
    console.print()

    # Run async task
    try:
        asyncio.run(execute_autonomous_task(
            task_text=task_text,
            cwd=cwd,
            stream=not no_stream,
            show_tools=show_tools
        ))
    except KeyboardInterrupt:
        console.print("\n[yellow]Task cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error executing task: {e}[/red]")
        if show_tools:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")


async def execute_autonomous_task(
    task_text: str,
    cwd: str = '.',
    stream: bool = True,
    show_tools: bool = False
):
    """
    Execute autonomous task using TaskPlanner with SOFIA + DREAM + Constitutional

    Flow:
    1. TaskPlanner creates plan (SOFIA → DREAM → Constitutional)
    2. Display plan to user for approval
    3. Execute plan step-by-step with Constitutional validation
    4. Stream results with Rich UI

    Differential vs Claude Code:
    - Claude Code: Direct tool use
    - Max-Code: SOFIA plans → DREAM validates → Constitutional approves → Execute
    """
    from core.task_planner import TaskPlanner
    from core.tools import get_unified_executor

    # Initialize TaskPlanner (SOFIA + DREAM + Constitutional)
    planner = TaskPlanner(
        use_sofia=True,
        use_dream=True,
        use_constitutional=True,
        strict_validation=True
    )

    # Initialize Unified Tool Executor
    executor = get_unified_executor(
        safe_mode=True,
        enable_self_correction=True
    )

    # STEP 1: Create plan with SOFIA + DREAM
    console.print("[cyan]Planning task with SOFIA + DREAM...[/cyan]")

    plan = await planner.plan_task(
        task_description=task_text,
        context={'cwd': cwd}
    )

    # STEP 2: Display plan
    console.print()
    _display_plan(plan, show_details=show_tools)
    console.print()

    # Check if plan approved
    if plan.status != "approved":
        console.print(f"[red]❌ Plan rejected:[/red] {plan.constitutional_violations}")
        return

    # STEP 3: Execute plan with streaming UI
    console.print("[cyan]Executing plan...[/cyan]\n")

    success = await _execute_plan(
        plan=plan,
        executor=executor,
        stream=stream,
        show_tools=show_tools
    )

    if success:
        console.print("\n[green]✅ Task completed successfully![/green]")
    else:
        console.print("\n[red]❌ Task execution failed[/red]")


def _display_plan(plan, show_details: bool = False):
    """Display execution plan in Rich format"""
    from rich.table import Table

    # Plan header
    console.print(Panel.fit(
        f"[bold]SOFIA's Architectural Plan[/bold]\n\n"
        f"{plan.architectural_vision[:200]}...\n\n"
        f"[dim]Complexity: {plan.complexity_estimate} | "
        f"Time: {plan.estimated_time} | "
        f"Steps: {len(plan.steps)}[/dim]",
        border_style="cyan",
        title="[bold cyan]📋 Plan[/bold cyan]"
    ))

    # DREAM's reality check
    console.print()
    console.print(Panel.fit(
        f"[bold]DREAM's Reality Check[/bold]\n\n"
        f"{plan.dream_analysis[:200]}...\n\n"
        f"[dim]Reality Score: {plan.reality_score:.0%}[/dim]",
        border_style="yellow",
        title="[bold yellow]🤖 DREAM[/bold yellow]"
    ))

    # Constitutional validation
    console.print()
    const_status = "[green]✓ APPROVED[/green]" if plan.constitutional_approved else "[red]✗ REJECTED[/red]"
    console.print(Panel.fit(
        f"[bold]Constitutional Validation (P1-P6)[/bold]\n\n"
        f"Status: {const_status}\n"
        f"Score: {plan.constitutional_score:.0%}\n"
        f"Violations: {', '.join(plan.constitutional_violations) if plan.constitutional_violations else 'None'}",
        border_style="green" if plan.constitutional_approved else "red",
        title="[bold]⚖️ Constitutional[/bold]"
    ))

    # Steps table (if show_details)
    if show_details:
        console.print()
        table = Table(title="Execution Steps", show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Risk", style="yellow")

        for step in plan.steps:
            table.add_row(
                str(step.step_number),
                step.tool_name,
                step.description[:50],
                step.constitutional_risk
            )

        console.print(table)


async def _execute_plan(plan, executor, stream: bool = True, show_tools: bool = False) -> bool:
    """
    Execute plan step-by-step with streaming UI

    Features:
    - Real-time progress display
    - Constitutional validation per step
    - Self-correction on errors
    - Audit trail

    Returns:
        True if all steps succeeded, False otherwise
    """
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel

    total_steps = len(plan.steps)
    completed_steps = 0
    failed_steps = 0

    # Execute each step
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:

        overall_task = progress.add_task(
            f"[cyan]Executing {total_steps} steps...",
            total=total_steps
        )

        for step in plan.steps:
            # Update progress
            step_desc = f"[cyan]Step {step.step_number}/{total_steps}:[/cyan] {step.description}"
            progress.update(overall_task, description=step_desc)

            if show_tools:
                console.print(f"\n[yellow]🔧 Tool:[/yellow] {step.tool_name}")
                console.print(f"[dim]Parameters: {step.parameters}[/dim]")

            # Execute tool via UnifiedExecutor (Constitutional + self-correction)
            try:
                result = executor.execute_tool(
                    tool_name=step.tool_name,
                    args=step.parameters,
                    validate=True  # Constitutional validation
                )

                # ToolResult has .type (success/error), not .is_success
                if result.type == "success":
                    step.executed = True
                    step.result = result.content
                    completed_steps += 1

                    if show_tools:
                        console.print(f"[green]✓ Success:[/green] {result.content[:100] if result.content else ''}...")
                else:
                    step.executed = True
                    step.error = result.error_text or "Unknown error"
                    failed_steps += 1

                    console.print(f"[red]✗ Failed:[/red] {result.error_text or 'Unknown error'}")

                    # Stop on first failure (can be made configurable)
                    console.print("[yellow]⚠ Stopping execution due to failure[/yellow]")
                    break

            except Exception as e:
                step.error = str(e)
                failed_steps += 1

                console.print(f"[red]✗ Exception:[/red] {e}")

                # Show full traceback if show_tools is enabled
                if show_tools:
                    import traceback
                    console.print(f"[dim]{traceback.format_exc()}[/dim]")

                break

            # Update progress
            progress.update(overall_task, advance=1)

    # Final summary
    console.print()
    console.print(f"[bold]Execution Summary:[/bold]")
    console.print(f"  Completed: [green]{completed_steps}/{total_steps}[/green]")
    console.print(f"  Failed: [red]{failed_steps}[/red]")

    # Return success if all steps completed
    return failed_steps == 0 and completed_steps == total_steps


# Keep old implementation as fallback (will be removed in FASE 4)
async def _execute_autonomous_task_OLD(
    task_text: str,
    cwd: str = '.',
    stream: bool = True,
    show_tools: bool = False
):
    """
    OLD IMPLEMENTATION - Direct Claude API with tool use

    This will be REMOVED in FASE 4 after streaming UI is complete.
    """
    settings = get_settings()

    # Initialize Anthropic client
    client = Anthropic(api_key=settings.claude.api_key)

    # Define available tools
    tools = [
        {
            "name": "write_file",
            "description": "Write content to a file. Creates directories if needed.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to file (relative to working directory)"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to file"
                    }
                },
                "required": ["file_path", "content"]
            }
        },
        {
            "name": "read_file",
            "description": "Read content from a file.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to file (relative to working directory)"
                    }
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "execute_bash",
            "description": "Execute bash command in working directory. Returns stdout/stderr.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Bash command to execute"
                    }
                },
                "required": ["command"]
            }
        },
        {
            "name": "list_files",
            "description": "List files in a directory.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to list (default: current)"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to filter files (e.g., '*.py')"
                    }
                },
                "required": []
            }
        }
    ]

    # System prompt for autonomous agent
    system_prompt = f"""You are Max-Code, an autonomous AI development assistant powered by Constitutional AI v3.0.

Your mission: Execute the user's task autonomously by:
1. Analyzing the task requirements
2. Breaking it into concrete steps
3. Using available tools to complete each step
4. Verifying your work
5. Providing clear final output

Available Tools:
- write_file: Create or modify files
- read_file: Read file contents
- execute_bash: Run commands (compilation, testing, etc.)
- list_files: Explore directory structure

Working Directory: {Path(cwd).resolve()}

Constitutional AI Principles:
- P1 (Completeness): Deliver FULLY functional solutions
- P2 (Transparency): Explain what you're doing and why
- P3 (Truth): Admit limitations, don't hallucinate
- P4 (User Sovereignty): User is in control, ask if uncertain
- P5 (Systemic): Consider broader context and implications
- P6 (Token Efficiency): Be concise but complete

Execute the task step by step. For code generation:
1. Create functional, well-documented code
2. Add necessary dependencies/build files
3. Provide clear compilation/execution instructions
4. Test if possible

Be thorough but efficient. Think like a senior engineer."""

    # Conversation history
    messages = [
        {"role": "user", "content": task_text}
    ]

    # Agentic loop (max 10 iterations to prevent infinite loops)
    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        if show_tools:
            console.print(f"[dim]Iteration {iteration}/{max_iterations}[/dim]")

        # Call Claude API
        response = client.messages.create(
            model=settings.claude.model,
            max_tokens=settings.claude.max_tokens,
            system=system_prompt,
            messages=messages,
            tools=tools
        )

        # Process response
        assistant_message = {"role": "assistant", "content": response.content}
        messages.append(assistant_message)

        # Display text responses
        for block in response.content:
            if block.type == "text":
                if stream:
                    console.print(Markdown(block.text))
                else:
                    console.print(block.text)

            elif block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input

                if show_tools:
                    console.print(f"\n[yellow]🔧 Tool:[/yellow] {tool_name}")
                    console.print(f"[dim]{tool_input}[/dim]")

                # Execute tool
                tool_result = await execute_tool(tool_name, tool_input, cwd)

                if show_tools:
                    result_preview = str(tool_result)[:200]
                    console.print(f"[green]✓ Result:[/green] [dim]{result_preview}...[/dim]\n")

                # Add tool result to conversation
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(tool_result)
                        }
                    ]
                })

        # Check if Claude is done (no more tool uses)
        has_tool_use = any(block.type == "tool_use" for block in response.content)
        if not has_tool_use:
            break

    # Final message
    if iteration >= max_iterations:
        console.print("\n[yellow]⚠ Reached maximum iterations[/yellow]")
    else:
        console.print("\n[green]✓ Task completed[/green]")


async def execute_tool(tool_name: str, tool_input: dict, cwd: str) -> str:
    """Execute a tool and return result."""
    import subprocess
    import glob
    from pathlib import Path

    cwd_path = Path(cwd).resolve()

    try:
        if tool_name == "write_file":
            file_path = cwd_path / tool_input["file_path"]
            content = tool_input["content"]

            # Create directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_text(content, encoding='utf-8')

            return f"File written successfully: {file_path} ({len(content)} bytes)"

        elif tool_name == "read_file":
            file_path = cwd_path / tool_input["file_path"]

            if not file_path.exists():
                return f"Error: File not found: {file_path}"

            content = file_path.read_text(encoding='utf-8')
            return content

        elif tool_name == "execute_bash":
            command = tool_input["command"]

            result = subprocess.run(
                command,
                shell=True,
                cwd=str(cwd_path),
                capture_output=True,
                text=True,
                timeout=30
            )

            output = f"Exit code: {result.returncode}\n"
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"

            return output

        elif tool_name == "list_files":
            directory = tool_input.get("directory", ".")
            pattern = tool_input.get("pattern", "*")

            search_path = cwd_path / directory / pattern
            files = glob.glob(str(search_path), recursive=True)

            # Make paths relative to cwd
            relative_files = [str(Path(f).relative_to(cwd_path)) for f in files]

            return "\n".join(relative_files) if relative_files else "No files found"

        else:
            return f"Error: Unknown tool: {tool_name}"

    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"
