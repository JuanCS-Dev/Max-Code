#!/usr/bin/env python3
"""
Parallel & Sequential Executor - Advanced Execution Engine com Boris Technique ✨

Philosophy (Boris):
"Parallelism is efficiency. Sequencing is correctness.
Know when to race, know when to wait."

Features:
- Parallel agent execution (asyncio-based)
- Sequential action pipelines
- Tool chaining with dependency resolution
- Timeout enforcement
- Error recovery
- Beautiful progress tracking

Architecture:
┌─────────────────────────────────────────┐
│         Execution Coordinator           │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐            │
│  │ Agent 1  │  │ Agent 2  │ Parallel   │
│  └──────────┘  └──────────┘            │
│       │              │                  │
│       ▼              ▼                  │
│  ┌────────────────────────┐            │
│  │  Sequential Pipeline   │            │
│  │  Tool1 → Tool2 → Tool3 │            │
│  └────────────────────────┘            │
└─────────────────────────────────────────┘

Security:
- Timeout enforcement (no infinite loops)
- Resource limits (max parallel tasks)
- Error isolation (one failure ≠ total failure)

Beauty:
- Real-time progress display
- Colored output per agent
- Clear error messages
- Performance metrics

Soli Deo Gloria 🙏
"""

import asyncio
from typing import List, Dict, Any, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import time

from rich.console import Console
from rich.progress import Progress, TaskID, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich.live import Live


console = Console()


class ExecutionStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class ExecutionResult:
    """Result of a task execution"""
    task_id: str
    status: ExecutionStatus
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Task:
    """Executable task"""
    id: str
    name: str
    func: Callable
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    timeout_seconds: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)


class ParallelExecutor:
    """
    Execute multiple agents in parallel.

    Boris: "Multiple minds think faster than one.
    Let agents work together, not wait in line."
    """

    def __init__(
        self,
        max_parallel: int = 5,
        default_timeout: float = 30.0
    ):
        """
        Initialize parallel executor.

        Args:
            max_parallel: Max tasks to run concurrently
            default_timeout: Default task timeout in seconds
        """
        self.max_parallel = max_parallel
        self.default_timeout = default_timeout
        self.console = Console()

    async def execute_parallel(
        self,
        tasks: List[Task],
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, ExecutionResult]:
        """
        Execute tasks in parallel with concurrency limit.

        Args:
            tasks: List of tasks to execute
            progress_callback: Optional callback for progress updates

        Returns:
            Dict of task_id -> ExecutionResult
        """
        results: Dict[str, ExecutionResult] = {}
        semaphore = asyncio.Semaphore(self.max_parallel)

        async def execute_task(task: Task) -> ExecutionResult:
            """Execute single task with semaphore"""
            async with semaphore:
                start_time = time.time()
                task_timeout = task.timeout_seconds or self.default_timeout

                try:
                    # Run task with timeout
                    if asyncio.iscoroutinefunction(task.func):
                        output = await asyncio.wait_for(
                            task.func(*task.args, **task.kwargs),
                            timeout=task_timeout
                        )
                    else:
                        # Run sync function in executor
                        loop = asyncio.get_event_loop()
                        output = await asyncio.wait_for(
                            loop.run_in_executor(None, task.func, *task.args),
                            timeout=task_timeout
                        )

                    duration_ms = (time.time() - start_time) * 1000

                    return ExecutionResult(
                        task_id=task.id,
                        status=ExecutionStatus.SUCCESS,
                        output=output,
                        duration_ms=duration_ms
                    )

                except asyncio.TimeoutError:
                    duration_ms = (time.time() - start_time) * 1000
                    return ExecutionResult(
                        task_id=task.id,
                        status=ExecutionStatus.TIMEOUT,
                        error=f"Task timed out after {task_timeout}s",
                        duration_ms=duration_ms
                    )

                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000
                    return ExecutionResult(
                        task_id=task.id,
                        status=ExecutionStatus.FAILED,
                        error=str(e),
                        duration_ms=duration_ms
                    )

        # Execute all tasks concurrently
        task_futures = [execute_task(task) for task in tasks]
        task_results = await asyncio.gather(*task_futures)

        # Build results dict
        for result in task_results:
            results[result.task_id] = result

            # Progress callback
            if progress_callback:
                progress_callback(result)

        return results

    def run_parallel(self, tasks: List[Task]) -> Dict[str, ExecutionResult]:
        """
        Synchronous wrapper for parallel execution.

        Args:
            tasks: Tasks to execute

        Returns:
            Dict of results
        """
        # Display progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeRemainingColumn(),
            console=self.console
        ) as progress:
            progress_task = progress.add_task(
                "[cyan]Executing agents in parallel...",
                total=len(tasks)
            )

            completed_count = 0

            def on_progress(result: ExecutionResult):
                nonlocal completed_count
                completed_count += 1
                progress.update(progress_task, completed=completed_count)

                # Show result
                status_icon = "✓" if result.status == ExecutionStatus.SUCCESS else "✗"
                status_color = "green" if result.status == ExecutionStatus.SUCCESS else "red"
                self.console.print(
                    f"[{status_color}]{status_icon}[/{status_color}] "
                    f"{result.task_id}: {result.status.value} "
                    f"({result.duration_ms:.0f}ms)"
                )

            # Run async execution
            results = asyncio.run(
                self.execute_parallel(tasks, on_progress)
            )

        return results


class SequentialPipeline:
    """
    Execute actions sequentially with dependency resolution.

    Boris: "Pipelines flow like rivers - step by step,
    each building on the last."
    """

    def __init__(self):
        """Initialize sequential pipeline"""
        self.console = Console()

    async def execute_pipeline(
        self,
        tasks: List[Task],
        fail_fast: bool = True
    ) -> Dict[str, ExecutionResult]:
        """
        Execute tasks sequentially in order.

        Args:
            tasks: Ordered list of tasks
            fail_fast: Stop on first failure

        Returns:
            Dict of task_id -> ExecutionResult
        """
        results: Dict[str, ExecutionResult] = {}

        for i, task in enumerate(tasks):
            self.console.print(
                f"[cyan]Step {i+1}/{len(tasks)}:[/cyan] {task.name}"
            )

            start_time = time.time()
            timeout = task.timeout_seconds or 30.0

            try:
                # Execute task
                if asyncio.iscoroutinefunction(task.func):
                    output = await asyncio.wait_for(
                        task.func(*task.args, **task.kwargs),
                        timeout=timeout
                    )
                else:
                    loop = asyncio.get_event_loop()
                    output = await asyncio.wait_for(
                        loop.run_in_executor(None, task.func, *task.args),
                        timeout=timeout
                    )

                duration_ms = (time.time() - start_time) * 1000

                result = ExecutionResult(
                    task_id=task.id,
                    status=ExecutionStatus.SUCCESS,
                    output=output,
                    duration_ms=duration_ms
                )

                results[task.id] = result

                self.console.print(
                    f"[green]✓[/green] {task.name} completed ({duration_ms:.0f}ms)"
                )

            except asyncio.TimeoutError:
                duration_ms = (time.time() - start_time) * 1000
                result = ExecutionResult(
                    task_id=task.id,
                    status=ExecutionStatus.TIMEOUT,
                    error=f"Timeout after {timeout}s",
                    duration_ms=duration_ms
                )
                results[task.id] = result

                self.console.print(
                    f"[red]✗[/red] {task.name} timed out"
                )

                if fail_fast:
                    break

            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                result = ExecutionResult(
                    task_id=task.id,
                    status=ExecutionStatus.FAILED,
                    error=str(e),
                    duration_ms=duration_ms
                )
                results[task.id] = result

                self.console.print(
                    f"[red]✗[/red] {task.name} failed: {e}"
                )

                if fail_fast:
                    break

        return results

    def run_pipeline(
        self,
        tasks: List[Task],
        fail_fast: bool = True
    ) -> Dict[str, ExecutionResult]:
        """
        Synchronous wrapper for pipeline execution.

        Args:
            tasks: Sequential tasks
            fail_fast: Stop on first error

        Returns:
            Execution results
        """
        self.console.print(
            Panel(
                f"[bold cyan]Sequential Pipeline[/bold cyan]\n"
                f"Tasks: {len(tasks)} | Fail-fast: {fail_fast}",
                border_style="cyan"
            )
        )

        results = asyncio.run(self.execute_pipeline(tasks, fail_fast))

        # Summary
        success_count = sum(1 for r in results.values() if r.status == ExecutionStatus.SUCCESS)
        total_duration = sum(r.duration_ms for r in results.values())

        self.console.print(
            f"\n[bold]Pipeline Complete:[/bold] "
            f"{success_count}/{len(tasks)} succeeded "
            f"({total_duration:.0f}ms total)"
        )

        return results


class ToolChain:
    """
    Chain tools with data flow.

    Boris: "Tools compose like functions.
    Output of one is input of next."
    """

    def __init__(self):
        """Initialize tool chain"""
        self.console = Console()

    def chain(
        self,
        tools: List[Callable],
        initial_input: Any,
        transform: Optional[Callable] = None
    ) -> Any:
        """
        Chain tools together, passing output to next input.

        Args:
            tools: List of tools (functions)
            initial_input: Input to first tool
            transform: Optional transform function between tools

        Returns:
            Final output
        """
        current_input = initial_input

        for i, tool in enumerate(tools):
            self.console.print(
                f"[dim]→ Tool {i+1}/{len(tools)}: {tool.__name__}[/dim]"
            )

            try:
                # Execute tool
                output = tool(current_input)

                # Transform if needed
                if transform:
                    output = transform(output)

                # Use as next input
                current_input = output

            except Exception as e:
                self.console.print(
                    f"[red]✗ Tool {tool.__name__} failed: {e}[/red]"
                )
                raise

        self.console.print("[green]✓ Tool chain complete[/green]")
        return current_input


# Demo
if __name__ == "__main__":
    import random

    console.print("[bold cyan]PARALLEL & SEQUENTIAL EXECUTOR DEMO[/bold cyan]\n")

    # Demo 1: Parallel agents
    console.print("[bold]1. PARALLEL AGENTS:[/bold]")

    def agent_task(agent_name: str, duration: float) -> str:
        """Simulate agent work"""
        time.sleep(duration)
        return f"{agent_name} completed"

    parallel_tasks = [
        Task(id="code", name="Code Agent", func=agent_task, args=("Code", 1.0)),
        Task(id="test", name="Test Agent", func=agent_task, args=("Test", 1.5)),
        Task(id="review", name="Review Agent", func=agent_task, args=("Review", 0.8)),
    ]

    executor = ParallelExecutor(max_parallel=3)
    results = executor.run_parallel(parallel_tasks)

    console.print()

    # Demo 2: Sequential pipeline
    console.print("[bold]2. SEQUENTIAL PIPELINE:[/bold]")

    def step1() -> str:
        time.sleep(0.5)
        return "Step 1 data"

    def step2() -> str:
        time.sleep(0.5)
        return "Step 2 data"

    def step3() -> str:
        time.sleep(0.5)
        return "Step 3 data"

    pipeline_tasks = [
        Task(id="step1", name="Read config", func=step1),
        Task(id="step2", name="Process data", func=step2),
        Task(id="step3", name="Write output", func=step3),
    ]

    pipeline = SequentialPipeline()
    results = pipeline.run_pipeline(pipeline_tasks)

    console.print()

    # Demo 3: Tool chain
    console.print("[bold]3. TOOL CHAIN:[/bold]")

    def tool1(x):
        return x * 2

    def tool2(x):
        return x + 10

    def tool3(x):
        return x ** 2

    chain = ToolChain()
    result = chain.chain([tool1, tool2, tool3], initial_input=5)
    console.print(f"[green]Final result: {result}[/green]")

    console.print("\n[bold green]✓ Demo complete![/bold green]")
