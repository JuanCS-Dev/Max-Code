"""
Execution Module - Parallel & Sequential Execution Engine

Provides:
- ParallelExecutor: Run multiple agents concurrently
- SequentialPipeline: Execute actions in order
- ToolChain: Chain tools with data flow
- CommandParser: Parse complex execution commands

Example usage:
```python
from core.execution import ParallelExecutor, Task

# Run agents in parallel
executor = ParallelExecutor(max_parallel=3)
tasks = [
    Task(id="code", name="Code Agent", func=code_agent.run),
    Task(id="test", name="Test Agent", func=test_agent.run),
]
results = executor.run_parallel(tasks)
```

Soli Deo Gloria 🙏
"""

from .parallel_executor import (
    ParallelExecutor,
    SequentialPipeline,
    ToolChain,
    Task,
    ExecutionResult,
    ExecutionStatus
)

from .command_parser import (
    CommandParser,
    ParsedCommand,
    ExecutionMode
)

__all__ = [
    'ParallelExecutor',
    'SequentialPipeline',
    'ToolChain',
    'Task',
    'ExecutionResult',
    'ExecutionStatus',
    'CommandParser',
    'ParsedCommand',
    'ExecutionMode',
]
