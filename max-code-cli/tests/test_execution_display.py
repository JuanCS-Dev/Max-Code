"""
Tests for Execution Display

Biblical Foundation:
"Tudo faço com boa ordem" (1 Coríntios 14:40)

Soli Deo Gloria
"""

import pytest
from io import StringIO
from rich.console import Console
from ui.execution_display import ExecutionDisplay, SimpleDisplay
from core.task_models import (
    Task,
    EnhancedExecutionPlan,
    TaskRequirement,
    TaskType
)


class TestExecutionDisplay:
    """Test ExecutionDisplay class"""
    
    def test_initialization(self):
        """Test display initialization"""
        plan = EnhancedExecutionPlan(
            goal="Test plan",
            tasks=[]
        )
        
        display = ExecutionDisplay(plan)
        
        assert display.plan == plan
        assert display.completed_count == 0
        assert display.failed_count == 0
        assert len(display.task_statuses) == 0
    
    def test_context_manager(self):
        """Test using display as context manager"""
        plan = EnhancedExecutionPlan(
            goal="Test plan",
            tasks=[]
        )
        
        # Should not raise exception
        with ExecutionDisplay(plan, console=Console(file=StringIO())) as display:
            assert display is not None
            assert display.live is not None
    
    def test_update_task_status_completed(self):
        """Test updating task to completed"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = ExecutionDisplay(plan, console=Console(file=StringIO()))
        
        # Update to completed
        display.update_task_status(task, "completed")
        
        assert display.task_statuses[task.id] == "completed"
        assert display.completed_count == 1
        assert display.failed_count == 0
    
    def test_update_task_status_failed(self):
        """Test updating task to failed"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = ExecutionDisplay(plan, console=Console(file=StringIO()))
        
        # Update to failed
        display.update_task_status(task, "failed")
        
        assert display.task_statuses[task.id] == "failed"
        assert display.completed_count == 0
        assert display.failed_count == 1
    
    def test_update_task_status_running(self):
        """Test updating task to running"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = ExecutionDisplay(plan, console=Console(file=StringIO()))
        
        # Update to running
        display.update_task_status(task, "running")
        
        assert display.task_statuses[task.id] == "running"
        assert display.completed_count == 0
        assert display.failed_count == 0
    
    def test_get_stats(self):
        """Test getting statistics"""
        task1 = Task(
            id="t1",
            description="Task 1",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        task2 = Task(
            id="t2",
            description="Task 2",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task1, task2]
        )
        
        display = ExecutionDisplay(plan, console=Console(file=StringIO()))
        
        # Mark one completed
        display.update_task_status(task1, "completed")
        
        stats = display.get_stats()
        
        assert stats["total_tasks"] == 2
        assert stats["completed"] == 1
        assert stats["failed"] == 0
        assert stats["remaining"] == 1
        assert stats["progress"] == 50.0
        assert "elapsed_seconds" in stats
    
    def test_render_tasks_table(self):
        """Test rendering tasks table"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = ExecutionDisplay(plan, console=Console(file=StringIO()))
        
        # Should not raise exception
        table = display._render_tasks_table()
        assert table is not None
    
    def test_render_summary(self):
        """Test rendering summary"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = ExecutionDisplay(plan, console=Console(file=StringIO()))
        
        # Should not raise exception
        panel = display._render_summary()
        assert panel is not None


class TestSimpleDisplay:
    """Test SimpleDisplay class"""
    
    def test_initialization(self):
        """Test simple display initialization"""
        plan = EnhancedExecutionPlan(
            goal="Test plan",
            tasks=[]
        )
        
        display = SimpleDisplay(plan)
        
        assert display.plan == plan
        assert display.completed_count == 0
        assert display.failed_count == 0
    
    def test_context_manager(self, capsys):
        """Test using simple display as context manager"""
        plan = EnhancedExecutionPlan(
            goal="Test plan",
            tasks=[]
        )
        
        with SimpleDisplay(plan) as display:
            assert display is not None
        
        # Check output
        captured = capsys.readouterr()
        assert "Starting: Test plan" in captured.out
        assert "Execution completed" in captured.out
    
    def test_update_task_status_completed(self, capsys):
        """Test updating task to completed"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = SimpleDisplay(plan)
        display.update_task_status(task, "completed")
        
        captured = capsys.readouterr()
        assert "COMPLETED" in captured.out
        assert "Test task" in captured.out
        assert display.completed_count == 1
    
    def test_update_task_status_failed(self, capsys):
        """Test updating task to failed"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = SimpleDisplay(plan)
        display.update_task_status(task, "failed")
        
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert display.failed_count == 1
    
    def test_update_task_status_running(self, capsys):
        """Test updating task to running"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task]
        )
        
        display = SimpleDisplay(plan)
        display.update_task_status(task, "running")
        
        captured = capsys.readouterr()
        assert "RUNNING" in captured.out
    
    def test_get_stats(self):
        """Test getting statistics"""
        task1 = Task(
            id="t1",
            description="Task 1",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        task2 = Task(
            id="t2",
            description="Task 2",
            type=TaskType.READ,
            requirements=TaskRequirement(agent_type="code", inputs={})
        )
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=[task1, task2]
        )
        
        display = SimpleDisplay(plan)
        
        # Mark one completed
        display.update_task_status(task1, "completed")
        
        stats = display.get_stats()
        
        assert stats["total_tasks"] == 2
        assert stats["completed"] == 1
        assert stats["failed"] == 0
        assert stats["remaining"] == 1
        assert stats["progress"] == 50.0


class TestIntegration:
    """Test integration scenarios"""
    
    def test_full_workflow_simple_display(self, capsys):
        """Test complete workflow with simple display"""
        # Create plan with multiple tasks
        tasks = [
            Task(
                id=f"t{i}",
                description=f"Task {i}",
                type=TaskType.READ,
                requirements=TaskRequirement(agent_type="code", inputs={})
            )
            for i in range(1, 4)
        ]
        
        plan = EnhancedExecutionPlan(
            goal="Complete workflow",
            tasks=tasks
        )
        
        with SimpleDisplay(plan) as display:
            # Simulate execution
            for task in tasks:
                display.update_task_status(task, "running")
                display.update_task_status(task, "completed")
        
        captured = capsys.readouterr()
        
        # Verify output
        assert "Starting: Complete workflow" in captured.out
        assert "Total tasks: 3" in captured.out
        assert "Execution completed" in captured.out
        assert "Completed: 3" in captured.out
    
    def test_with_failures(self, capsys):
        """Test workflow with failures"""
        tasks = [
            Task(
                id="t1",
                description="Task 1",
                type=TaskType.READ,
                requirements=TaskRequirement(agent_type="code", inputs={})
            ),
            Task(
                id="t2",
                description="Task 2",
                type=TaskType.READ,
                requirements=TaskRequirement(agent_type="code", inputs={})
            )
        ]
        
        plan = EnhancedExecutionPlan(
            goal="Test failures",
            tasks=tasks
        )
        
        with SimpleDisplay(plan) as display:
            display.update_task_status(tasks[0], "running")
            display.update_task_status(tasks[0], "completed")
            
            display.update_task_status(tasks[1], "running")
            display.update_task_status(tasks[1], "failed")
        
        captured = capsys.readouterr()
        
        assert "Completed: 1" in captured.out
        assert "Failed: 1" in captured.out
