"""
Tests for Execution Engine

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)

Soli Deo Gloria
"""

import pytest
import asyncio
from core.execution_engine import (
    ExecutionEngine,
    ExecutionState,
    RetryStrategy,
    ExecutionPolicy,
    get_execution_engine
)
from core.task_models import (
    Task,
    EnhancedExecutionPlan,
    TaskRequirement,
    TaskType,
    TaskStatus
)


class TestExecutionEngine:
    """Test ExecutionEngine class"""
    
    def test_initialization(self):
        """Test engine initialization"""
        engine = ExecutionEngine()
        
        assert engine.state == ExecutionState.IDLE
        assert engine.max_retries == 3
        assert engine.retry_strategy == RetryStrategy.EXPONENTIAL
        assert engine.enable_parallel is True
    
    def test_custom_configuration(self):
        """Test engine with custom configuration"""
        engine = ExecutionEngine(
            max_retries=5,
            retry_strategy=RetryStrategy.LINEAR,
            base_delay=2.0,
            max_delay=120.0,
            enable_parallel=False
        )
        
        assert engine.max_retries == 5
        assert engine.retry_strategy == RetryStrategy.LINEAR
        assert engine.base_delay == 2.0
        assert engine.max_delay == 120.0
        assert engine.enable_parallel is False
    
    def test_calculate_retry_delay_exponential(self):
        """Test exponential backoff calculation"""
        engine = ExecutionEngine(
            retry_strategy=RetryStrategy.EXPONENTIAL,
            base_delay=1.0
        )
        
        # Attempt 0: base_delay * 2^0 = 1.0
        delay0 = engine._calculate_retry_delay(0)
        assert 1.0 <= delay0 <= 1.2  # With jitter
        
        # Attempt 1: base_delay * 2^1 = 2.0
        delay1 = engine._calculate_retry_delay(1)
        assert 2.0 <= delay1 <= 2.3
        
        # Attempt 2: base_delay * 2^2 = 4.0
        delay2 = engine._calculate_retry_delay(2)
        assert 4.0 <= delay2 <= 4.5
    
    def test_calculate_retry_delay_linear(self):
        """Test linear backoff calculation"""
        engine = ExecutionEngine(
            retry_strategy=RetryStrategy.LINEAR,
            base_delay=1.0
        )
        
        # Attempt 0: base_delay * 1 = 1.0
        delay0 = engine._calculate_retry_delay(0)
        assert 1.0 <= delay0 <= 1.2
        
        # Attempt 1: base_delay * 2 = 2.0
        delay1 = engine._calculate_retry_delay(1)
        assert 2.0 <= delay1 <= 2.3
        
        # Attempt 2: base_delay * 3 = 3.0
        delay2 = engine._calculate_retry_delay(2)
        assert 3.0 <= delay2 <= 3.4
    
    def test_calculate_retry_delay_immediate(self):
        """Test immediate retry (no delay)"""
        engine = ExecutionEngine(retry_strategy=RetryStrategy.IMMEDIATE)
        
        delay = engine._calculate_retry_delay(0)
        assert delay == 0.0
    
    def test_calculate_retry_delay_max_cap(self):
        """Test delay is capped at max_delay"""
        engine = ExecutionEngine(
            retry_strategy=RetryStrategy.EXPONENTIAL,
            base_delay=10.0,
            max_delay=20.0
        )
        
        # Attempt 10 would be huge without cap
        delay = engine._calculate_retry_delay(10)
        assert delay <= 20.0
    
    def test_pause_resume(self):
        """Test pause and resume"""
        engine = ExecutionEngine()
        
        engine.pause()
        assert engine.state == ExecutionState.PAUSED
        
        engine.resume()
        assert engine.state == ExecutionState.EXECUTING
    
    def test_cancel(self):
        """Test cancellation"""
        engine = ExecutionEngine()
        
        engine.cancel()
        assert engine.state == ExecutionState.CANCELLED
    
    def test_get_execution_stats_empty(self):
        """Test stats with no plan"""
        engine = ExecutionEngine()
        
        stats = engine.get_execution_stats()
        
        assert stats["state"] == "idle"
        assert stats["total_tasks"] == 0
        assert stats["completed"] == 0
        assert stats["failed"] == 0
        assert stats["progress"] == 0
    
    @pytest.mark.asyncio
    async def test_execute_plan_invalid(self):
        """Test execution with invalid plan (circular dependency)"""
        engine = ExecutionEngine()
        
        # Create circular dependency: t1 -> t2 -> t1
        task1 = Task(
            id="t1",
            description="Task 1",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={}),
            depends_on=["t2"]
        )
        
        task2 = Task(
            id="t2",
            description="Task 2",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={}),
            depends_on=["t1"]
        )
        
        plan = EnhancedExecutionPlan(
            goal="Invalid plan",
            tasks=[task1, task2]
        )
        
        result = await engine.execute_plan(plan)
        
        assert result["success"] is False
        assert "Invalid plan" in result["error"]
    
    @pytest.mark.asyncio
    async def test_execute_simple_plan(self):
        """Test execution of simple plan"""
        engine = ExecutionEngine(max_retries=1)
        
        # Create simple plan with 2 tasks
        task1 = Task(
            id="t1",
            description="Read README.md",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "README.md"}
            )
        )
        
        task2 = Task(
            id="t2",
            description="Think about the code",
            type=TaskType.THINK,
            requirements=TaskRequirement(agent_type="explore", inputs={}),
            depends_on=["t1"]
        )
        
        plan = EnhancedExecutionPlan(
            goal="Read and think",
            tasks=[task1, task2]
        )
        
        result = await engine.execute_plan(plan)
        
        assert isinstance(result, dict)
        assert "success" in result
        assert "completed_tasks" in result
        assert "total_tasks" in result
        assert result["total_tasks"] == 2
    
    @pytest.mark.asyncio
    async def test_gather_dependency_context(self):
        """Test context gathering from dependencies"""
        from core.task_models import TaskOutput
        
        engine = ExecutionEngine()
        
        # Setup plan with dependencies
        task1 = Task(
            id="t1",
            description="Task 1",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        # Mark completed with TaskOutput
        task_output = TaskOutput(
            success=True,
            data="output from t1",
            context={"key1": "value1"}
        )
        task1.mark_completed(task_output)
        
        task2 = Task(
            id="t2",
            description="Task 2",
            type=TaskType.WRITE,
            requirements=TaskRequirement(agent_type="code", inputs={}),
            depends_on=["t1"]
        )
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task1, task2])
        engine.current_plan = plan
        
        # Gather context for task2
        context = engine._gather_dependency_context(task2)
        
        assert "key1" in context
        assert "t1_output" in context
        assert context["key1"] == "value1"


class TestExecutionPolicy:
    """Test ExecutionPolicy class"""
    
    def test_policy_defaults(self):
        """Test policy default values"""
        policy = ExecutionPolicy()
        
        assert policy.stop_on_first_failure is False
        assert policy.skip_failed_dependencies is False
        assert policy.allow_partial_success is True
        assert policy.timeout_per_task is None
        assert policy.timeout_total is None
    
    def test_policy_custom(self):
        """Test policy with custom values"""
        policy = ExecutionPolicy(
            stop_on_first_failure=True,
            skip_failed_dependencies=True,
            allow_partial_success=False,
            timeout_per_task=60,
            timeout_total=300
        )
        
        assert policy.stop_on_first_failure is True
        assert policy.skip_failed_dependencies is True
        assert policy.allow_partial_success is False
        assert policy.timeout_per_task == 60
        assert policy.timeout_total == 300


class TestCheckpointing:
    """Test checkpoint/recovery functionality"""
    
    def test_save_checkpoint(self, tmp_path):
        """Test saving checkpoint"""
        import json
        
        engine = ExecutionEngine()
        engine.completed_tasks = {"t1", "t2"}
        engine.failed_tasks = {"t3"}
        
        checkpoint_file = tmp_path / "checkpoint.json"
        engine.save_checkpoint(str(checkpoint_file))
        
        assert checkpoint_file.exists()
        
        # Verify content
        with open(checkpoint_file) as f:
            data = json.load(f)
        
        assert data["state"] == "idle"
        assert set(data["completed_tasks"]) == {"t1", "t2"}
        assert set(data["failed_tasks"]) == {"t3"}
    
    def test_load_checkpoint(self, tmp_path):
        """Test loading checkpoint"""
        import json
        
        # Create checkpoint file
        checkpoint_file = tmp_path / "checkpoint.json"
        checkpoint_data = {
            "state": "executing",
            "completed_tasks": ["t1", "t2"],
            "failed_tasks": ["t3"],
            "timestamp": "2025-01-01T00:00:00"
        }
        
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f)
        
        # Load into engine
        engine = ExecutionEngine()
        success = engine.load_checkpoint(str(checkpoint_file))
        
        assert success is True
        assert engine.state == ExecutionState.EXECUTING
        assert engine.completed_tasks == {"t1", "t2"}
        assert engine.failed_tasks == {"t3"}
    
    def test_load_checkpoint_invalid(self, tmp_path):
        """Test loading invalid checkpoint"""
        checkpoint_file = tmp_path / "invalid.json"
        checkpoint_file.write_text("invalid json")
        
        engine = ExecutionEngine()
        success = engine.load_checkpoint(str(checkpoint_file))
        
        assert success is False


class TestCallbacks:
    """Test callback functionality"""
    
    @pytest.mark.asyncio
    async def test_on_task_start_callback(self):
        """Test on_task_start callback"""
        engine = ExecutionEngine(max_retries=1)
        
        callback_called = []
        
        def on_start(task):
            callback_called.append(task.id)
        
        engine.on_task_start = on_start
        
        # Simple task
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "README.md"}
            )
        )
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task])
        
        await engine.execute_plan(plan)
        
        assert "t1" in callback_called


class TestGlobalInstance:
    """Test global instance management"""
    
    def test_singleton(self):
        """Test get_execution_engine returns singleton"""
        engine1 = get_execution_engine()
        engine2 = get_execution_engine()
        
        assert engine1 is engine2
    
    def test_global_usage(self):
        """Test using global instance"""
        engine = get_execution_engine()
        
        stats = engine.get_execution_stats()
        
        assert "state" in stats
        assert "total_tasks" in stats
