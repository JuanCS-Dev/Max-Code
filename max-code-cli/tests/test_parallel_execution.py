#!/usr/bin/env python3
"""
Testes para Parallel & Sequential Execution

Testing:
- ParallelExecutor (async execution, semaphore, timeout)
- SequentialPipeline (ordered execution, fail-fast)
- ToolChain (data flow, composition)
- CommandParser (natural language parsing)
"""

import pytest
import asyncio
import time
from unittest.mock import Mock

from core.execution import (
    ParallelExecutor,
    SequentialPipeline,
    ToolChain,
    Task,
    ExecutionResult,
    ExecutionStatus,
    CommandParser,
    ParsedCommand,
    ExecutionMode
)


class TestParallelExecutor:
    """Test ParallelExecutor"""

    def test_parallel_executor_initialization(self):
        """Test executor initializes correctly"""
        executor = ParallelExecutor(max_parallel=3, default_timeout=30)

        assert executor.max_parallel == 3
        assert executor.default_timeout == 30

    def test_parallel_execution_success(self):
        """Test successful parallel execution"""
        def task_func(value):
            time.sleep(0.1)
            return value * 2

        tasks = [
            Task(id="task1", name="Task 1", func=task_func, args=(5,)),
            Task(id="task2", name="Task 2", func=task_func, args=(10,)),
            Task(id="task3", name="Task 3", func=task_func, args=(15,)),
        ]

        executor = ParallelExecutor(max_parallel=3)
        results = executor.run_parallel(tasks)

        assert len(results) == 3
        assert results["task1"].status == ExecutionStatus.SUCCESS
        assert results["task1"].output == 10
        assert results["task2"].output == 20
        assert results["task3"].output == 30

    def test_parallel_execution_with_timeout(self):
        """Test task timeout enforcement"""
        def slow_task():
            time.sleep(5)
            return "done"

        tasks = [
            Task(id="slow", name="Slow Task", func=slow_task, timeout_seconds=0.5)
        ]

        executor = ParallelExecutor()
        results = executor.run_parallel(tasks)

        assert results["slow"].status == ExecutionStatus.TIMEOUT

    def test_parallel_execution_with_error(self):
        """Test error handling in parallel execution"""
        def failing_task():
            raise ValueError("Task failed!")

        tasks = [
            Task(id="fail", name="Failing Task", func=failing_task)
        ]

        executor = ParallelExecutor()
        results = executor.run_parallel(tasks)

        assert results["fail"].status == ExecutionStatus.FAILED
        assert "Task failed!" in results["fail"].error

    def test_parallel_execution_concurrency_limit(self):
        """Test concurrency limit is respected"""
        execution_times = []

        def track_execution():
            execution_times.append(time.time())
            time.sleep(0.2)
            return "done"

        # Create 5 tasks with max_parallel=2
        tasks = [
            Task(id=f"task{i}", name=f"Task {i}", func=track_execution)
            for i in range(5)
        ]

        executor = ParallelExecutor(max_parallel=2)
        start_time = time.time()
        results = executor.run_parallel(tasks)
        total_time = time.time() - start_time

        # With max_parallel=2, 5 tasks should take ~3 batches
        # Each batch ~0.2s = ~0.6s total (plus overhead)
        assert total_time >= 0.6
        assert total_time < 1.0  # Shouldn't take 5*0.2=1.0s (sequential)

    def test_async_function_execution(self):
        """Test execution of async functions"""
        async def async_task(value):
            await asyncio.sleep(0.1)
            return value * 2

        tasks = [
            Task(id="async1", name="Async Task", func=async_task, args=(5,))
        ]

        executor = ParallelExecutor()
        results = executor.run_parallel(tasks)

        assert results["async1"].status == ExecutionStatus.SUCCESS
        assert results["async1"].output == 10


class TestSequentialPipeline:
    """Test SequentialPipeline"""

    def test_sequential_pipeline_success(self):
        """Test successful sequential execution"""
        def step1():
            return 10

        def step2():
            return 20

        def step3():
            return 30

        tasks = [
            Task(id="step1", name="Step 1", func=step1),
            Task(id="step2", name="Step 2", func=step2),
            Task(id="step3", name="Step 3", func=step3),
        ]

        pipeline = SequentialPipeline()
        results = pipeline.run_pipeline(tasks)

        assert len(results) == 3
        assert all(r.status == ExecutionStatus.SUCCESS for r in results.values())

    def test_sequential_pipeline_fail_fast(self):
        """Test fail-fast mode stops on first error"""
        def step1():
            return "success"

        def step2():
            raise ValueError("Step 2 failed!")

        def step3():
            return "should not execute"

        tasks = [
            Task(id="step1", name="Step 1", func=step1),
            Task(id="step2", name="Step 2", func=step2),
            Task(id="step3", name="Step 3", func=step3),
        ]

        pipeline = SequentialPipeline()
        results = pipeline.run_pipeline(tasks, fail_fast=True)

        # Only first 2 tasks should execute
        assert len(results) == 2
        assert results["step1"].status == ExecutionStatus.SUCCESS
        assert results["step2"].status == ExecutionStatus.FAILED
        assert "step3" not in results

    def test_sequential_pipeline_continue_on_error(self):
        """Test continue-on-error mode"""
        def step1():
            return "success"

        def step2():
            raise ValueError("Step 2 failed!")

        def step3():
            return "still executes"

        tasks = [
            Task(id="step1", name="Step 1", func=step1),
            Task(id="step2", name="Step 2", func=step2),
            Task(id="step3", name="Step 3", func=step3),
        ]

        pipeline = SequentialPipeline()
        results = pipeline.run_pipeline(tasks, fail_fast=False)

        # All tasks should execute
        assert len(results) == 3
        assert results["step3"].status == ExecutionStatus.SUCCESS

    def test_sequential_execution_order(self):
        """Test tasks execute in order"""
        execution_order = []

        def step1():
            execution_order.append(1)
            return 1

        def step2():
            execution_order.append(2)
            return 2

        def step3():
            execution_order.append(3)
            return 3

        tasks = [
            Task(id="step1", name="Step 1", func=step1),
            Task(id="step2", name="Step 2", func=step2),
            Task(id="step3", name="Step 3", func=step3),
        ]

        pipeline = SequentialPipeline()
        pipeline.run_pipeline(tasks)

        assert execution_order == [1, 2, 3]


class TestToolChain:
    """Test ToolChain"""

    def test_tool_chain_basic(self):
        """Test basic tool chaining"""
        def double(x):
            return x * 2

        def add_ten(x):
            return x + 10

        def square(x):
            return x ** 2

        chain = ToolChain()
        result = chain.chain([double, add_ten, square], initial_input=5)

        # (5 * 2) + 10 = 20, 20^2 = 400
        assert result == 400

    def test_tool_chain_with_transform(self):
        """Test tool chain with transformation"""
        def get_length(s):
            return len(s)

        def double(n):
            return n * 2

        def transform(x):
            return x + 1

        chain = ToolChain()
        result = chain.chain(
            [get_length, double],
            initial_input="hello",
            transform=transform
        )

        # len("hello") = 5, transform(5) = 6, 6*2 = 12, transform(12) = 13
        # Transform applies after each tool
        assert result == 13

    def test_tool_chain_error_propagation(self):
        """Test that errors propagate through chain"""
        def working_tool(x):
            return x * 2

        def failing_tool(x):
            raise ValueError("Tool failed!")

        chain = ToolChain()

        with pytest.raises(ValueError, match="Tool failed!"):
            chain.chain([working_tool, failing_tool], initial_input=5)


class TestCommandParser:
    """Test CommandParser"""

    def test_parse_parallel_command_english(self):
        """Test parsing parallel command in English"""
        parsed = CommandParser.parse("run agents code test review in parallel")

        assert parsed.mode == ExecutionMode.PARALLEL
        assert "code" in parsed.commands
        assert "test" in parsed.commands
        assert "review" in parsed.commands

    def test_parse_parallel_command_portuguese(self):
        """Test parsing parallel command in Portuguese"""
        parsed = CommandParser.parse("lança code test em paralelo")

        assert parsed.mode == ExecutionMode.PARALLEL

    def test_parse_sequential_command(self):
        """Test parsing sequential command"""
        parsed = CommandParser.parse("execute step1 then step2 then step3 sequentially")

        assert parsed.mode == ExecutionMode.SEQUENTIAL
        assert len(parsed.commands) == 3

    def test_parse_chain_command(self):
        """Test parsing tool chain command"""
        parsed = CommandParser.parse("chain grep 'TODO' | filter .py | count")

        assert parsed.mode == ExecutionMode.CHAIN
        assert len(parsed.commands) == 3

    def test_parse_single_command(self):
        """Test parsing single command"""
        parsed = CommandParser.parse("just a regular command")

        assert parsed.mode == ExecutionMode.SINGLE
        assert len(parsed.commands) == 1

    def test_is_complex_command(self):
        """Test complex command detection"""
        assert CommandParser.is_complex_command("run in parallel") is True
        assert CommandParser.is_complex_command("execute then after") is True
        assert CommandParser.is_complex_command("chain | pipe") is True
        assert CommandParser.is_complex_command("regular command") is False


class TestTask:
    """Test Task dataclass"""

    def test_task_creation(self):
        """Test task can be created"""
        def my_func():
            return "result"

        task = Task(
            id="test",
            name="Test Task",
            func=my_func,
            timeout_seconds=30.0
        )

        assert task.id == "test"
        assert task.name == "Test Task"
        assert task.func == my_func
        assert task.timeout_seconds == 30.0


class TestExecutionResult:
    """Test ExecutionResult dataclass"""

    def test_execution_result_creation(self):
        """Test result can be created"""
        result = ExecutionResult(
            task_id="test",
            status=ExecutionStatus.SUCCESS,
            output="result data",
            duration_ms=150.5
        )

        assert result.task_id == "test"
        assert result.status == ExecutionStatus.SUCCESS
        assert result.output == "result data"
        assert result.duration_ms == 150.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
