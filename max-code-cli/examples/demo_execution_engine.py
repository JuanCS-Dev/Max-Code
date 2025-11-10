"""
Demo: Execution Engine with Display

Shows complete execution workflow with:
- Plan creation
- Display integration
- Retry logic
- Progress tracking

Soli Deo Gloria
"""

import asyncio
from core.execution_engine import ExecutionEngine, RetryStrategy
from core.task_models import (
    Task,
    EnhancedExecutionPlan,
    TaskRequirement,
    TaskType
)
from ui.execution_display import SimpleDisplay


async def demo_simple_execution():
    """Demo 1: Simple sequential execution"""
    print("\n" + "="*60)
    print("DEMO 1: Simple Sequential Execution")
    print("="*60)
    
    # Create simple plan
    tasks = [
        Task(
            id="t1",
            description="Analyze project structure",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="explore",
                inputs={"path": "."}
            )
        ),
        Task(
            id="t2",
            description="Read main configuration",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "setup.py"}
            ),
            depends_on=["t1"]
        ),
        Task(
            id="t3",
            description="Analyze dependencies",
            type=TaskType.THINK,
            requirements=TaskRequirement(
                agent_type="explore",
                inputs={}
            ),
            depends_on=["t2"]
        )
    ]
    
    plan = EnhancedExecutionPlan(
        goal="Analyze project structure and dependencies",
        tasks=tasks
    )
    
    # Create engine with simple display
    engine = ExecutionEngine(
        max_retries=2,
        retry_strategy=RetryStrategy.EXPONENTIAL,
        enable_parallel=False
    )
    
    # Execute with display
    with SimpleDisplay(plan) as display:
        result = await engine.execute_plan(plan, display=display)
    
    # Show results
    print(f"\n✅ Execution completed!")
    print(f"   Total tasks: {result['total_tasks']}")
    print(f"   Completed: {result['completed_tasks']}")
    print(f"   Failed: {result['failed_tasks']}")
    print(f"   Time: {result['execution_time']:.2f}s")


async def demo_parallel_execution():
    """Demo 2: Parallel execution"""
    print("\n" + "="*60)
    print("DEMO 2: Parallel Execution")
    print("="*60)
    
    # Create plan with independent tasks
    tasks = [
        Task(
            id="t1",
            description="Read README.md",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "README.md"}
            )
        ),
        Task(
            id="t2",
            description="Read setup.py",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "setup.py"}
            )
        ),
        Task(
            id="t3",
            description="Read requirements.txt",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "requirements.txt"}
            )
        )
    ]
    
    plan = EnhancedExecutionPlan(
        goal="Read all configuration files",
        tasks=tasks
    )
    
    # Create engine with parallel execution
    engine = ExecutionEngine(
        max_retries=2,
        enable_parallel=True  # Enable parallel
    )
    
    # Execute
    with SimpleDisplay(plan) as display:
        result = await engine.execute_plan(plan, display=display)
    
    print(f"\n✅ Parallel execution completed in {result['execution_time']:.2f}s")
    print(f"   Completed: {result['completed_tasks']}/{result['total_tasks']}")


async def demo_with_retry():
    """Demo 3: Execution with retry logic"""
    print("\n" + "="*60)
    print("DEMO 3: Execution with Retry")
    print("="*60)
    
    # Create plan with task that might fail
    tasks = [
        Task(
            id="t1",
            description="Read non-existent file (will retry)",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "nonexistent.txt"}
            )
        ),
        Task(
            id="t2",
            description="Read existing file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "README.md"}
            )
        )
    ]
    
    plan = EnhancedExecutionPlan(
        goal="Test retry logic",
        tasks=tasks
    )
    
    # Create engine with aggressive retry
    engine = ExecutionEngine(
        max_retries=3,
        retry_strategy=RetryStrategy.EXPONENTIAL,
        base_delay=0.5
    )
    
    # Setup callbacks to show retry
    def on_fail(task, error):
        print(f"\n❌ Task {task.id} failed: {error}")
    
    engine.on_task_fail = on_fail
    
    # Execute
    with SimpleDisplay(plan) as display:
        result = await engine.execute_plan(plan, display=display)
    
    print(f"\n📊 Result:")
    print(f"   Completed: {result['completed_tasks']}")
    print(f"   Failed: {result['failed_tasks']}")
    print(f"   (Task t1 was retried 3 times before failing)")


async def demo_with_checkpointing():
    """Demo 4: Checkpointing and recovery"""
    print("\n" + "="*60)
    print("DEMO 4: Checkpointing")
    print("="*60)
    
    # Create plan
    tasks = [
        Task(
            id=f"t{i}",
            description=f"Process item {i}",
            type=TaskType.THINK,
            requirements=TaskRequirement(
                agent_type="explore",
                inputs={"item": i}
            )
        )
        for i in range(1, 6)
    ]
    
    plan = EnhancedExecutionPlan(
        goal="Process multiple items",
        tasks=tasks
    )
    
    # Create engine
    engine = ExecutionEngine()
    
    # Setup callback to save checkpoint
    def on_complete(task, result):
        print(f"✓ Completed {task.id}, saving checkpoint...")
        engine.save_checkpoint("checkpoint.json")
    
    engine.on_task_complete = on_complete
    
    # Execute
    with SimpleDisplay(plan) as display:
        result = await engine.execute_plan(plan, display=display)
    
    print(f"\n💾 Checkpoint saved after each task")
    print(f"   Final state: {result['completed_tasks']}/{result['total_tasks']} completed")


async def demo_progress_tracking():
    """Demo 5: Real-time progress tracking"""
    print("\n" + "="*60)
    print("DEMO 5: Progress Tracking")
    print("="*60)
    
    # Create plan
    tasks = [
        Task(
            id=f"t{i}",
            description=f"Step {i}",
            type=TaskType.THINK,
            requirements=TaskRequirement(
                agent_type="explore",
                inputs={}
            )
        )
        for i in range(1, 11)
    ]
    
    plan = EnhancedExecutionPlan(
        goal="Multi-step process",
        tasks=tasks
    )
    
    # Create engine
    engine = ExecutionEngine(enable_parallel=False)
    
    # Track progress
    print("\nProgress tracking:")
    
    def on_complete(task, result):
        stats = engine.get_execution_stats()
        print(f"  Progress: {stats['progress']:.1f}% ({stats['completed']}/{stats['total_tasks']})")
    
    engine.on_task_complete = on_complete
    
    # Execute
    with SimpleDisplay(plan) as display:
        result = await engine.execute_plan(plan, display=display)
    
    print(f"\n✅ All tasks completed!")


async def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("🚀 EXECUTION ENGINE DEMO")
    print("="*60)
    
    # Run demos
    await demo_simple_execution()
    
    await demo_parallel_execution()
    
    await demo_with_retry()
    
    await demo_with_checkpointing()
    
    await demo_progress_tracking()
    
    print("\n" + "="*60)
    print("✅ ALL DEMOS COMPLETED")
    print("="*60)
    print("\n🙏 Soli Deo Gloria!\n")


if __name__ == "__main__":
    asyncio.run(main())
