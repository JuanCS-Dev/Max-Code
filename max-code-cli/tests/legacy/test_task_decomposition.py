"""
Tests for Task Decomposition System

Comprehensive test suite for:
- Task models
- Task graph (DAG operations)
- Task decomposer
- Dependency resolver

Soli Deo Gloria
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

from core.task_models import (
    Task, TaskType, TaskStatus, TaskRequirement, TaskOutput,
    EnhancedExecutionPlan, toolstep_to_task
)
from core.task_graph import TaskGraph, TaskGraphBuilder
from core.dependency_resolver import DependencyResolver


class TestTaskModels:
    """Test task models and enums"""
    
    def test_task_creation(self):
        """Test creating a Task"""
        task = Task(
            id="task_1",
            description="Create main.py",
            type=TaskType.WRITE,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_writer"],
                inputs={"filepath": "main.py"},
                context_dependencies=[]
            ),
            depends_on=[],
            estimated_time=30
        )
        
        assert task.id == "task_1"
        assert task.description == "Create main.py"
        assert task.type == TaskType.WRITE
        assert task.status == TaskStatus.PENDING
        assert task.requirements.agent_type == "code"
        assert "file_writer" in task.requirements.tools
    
    def test_task_dependencies(self):
        """Test task dependency checking"""
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=["t1"])
        
        # task1 can execute (no dependencies)
        assert task1.can_execute(set())
        
        # task2 cannot execute without t1
        assert not task2.can_execute(set())
        
        # task2 can execute after t1 completes
        assert task2.can_execute({"t1"})
    
    def test_task_state_transitions(self):
        """Test task status transitions"""
        task = Task(id="t1", description="Test")
        
        # Initial state
        assert task.status == TaskStatus.PENDING
        
        # Mark ready
        task.mark_ready()
        assert task.status == TaskStatus.READY
        
        # Mark running
        task.mark_running()
        assert task.status == TaskStatus.RUNNING
        assert task.started_at is not None
        
        # Mark completed
        output = TaskOutput(success=True, data="result", context={})
        task.mark_completed(output)
        assert task.status == TaskStatus.COMPLETED
        assert task.output == output
        assert task.completed_at is not None
        assert task.get_execution_time() > 0
    
    def test_task_failure(self):
        """Test task failure handling"""
        task = Task(id="t1", description="Test")
        
        task.mark_failed("Error occurred")
        
        assert task.status == TaskStatus.FAILED
        assert task.output is not None
        assert task.output.success == False
        assert task.output.error == "Error occurred"
    
    def test_task_to_dict(self):
        """Test task serialization"""
        task = Task(
            id="t1",
            description="Test task",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="test",
                tools=["tool1"],
                inputs={"key": "value"}
            ),
            depends_on=["t0"],
            estimated_time=60
        )
        
        task_dict = task.to_dict()
        
        assert isinstance(task_dict, dict)
        assert task_dict['id'] == "t1"
        assert task_dict['description'] == "Test task"
        assert task_dict['type'] == "read"
        assert task_dict['agent'] == "test"
        assert task_dict['depends_on'] == ["t0"]
    
    def test_task_from_dict(self):
        """Test task deserialization"""
        data = {
            "id": "t1",
            "description": "Test",
            "type": "write",
            "agent": "code",
            "tools": ["file_writer"],
            "inputs": {"filepath": "test.py"},
            "depends_on": [],
            "estimated_time": 30,
            "risk_level": "low"
        }
        
        task = Task.from_dict(data)
        
        assert task.id == "t1"
        assert task.description == "Test"
        assert task.type == TaskType.WRITE
        assert task.requirements.agent_type == "code"


class TestTaskGraph:
    """Test task graph and DAG operations"""
    
    def test_simple_dag(self):
        """Test simple DAG creation"""
        task1 = Task(id="t1", description="T1", depends_on=[])
        task2 = Task(id="t2", description="T2", depends_on=["t1"])
        task3 = Task(id="t3", description="T3", depends_on=["t2"])
        
        graph = TaskGraph([task1, task2, task3])
        
        assert len(graph.tasks) == 3
        assert graph.graph.number_of_nodes() == 3
        assert graph.graph.number_of_edges() == 2
    
    def test_dag_validation_valid(self):
        """Test DAG validation with valid graph"""
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=["t1"])
        
        graph = TaskGraph([task1, task2])
        is_valid, errors = graph.is_valid_dag()
        
        assert is_valid
        assert len(errors) == 0
    
    def test_dag_validation_circular(self):
        """Test DAG validation with circular dependency"""
        task1 = Task(id="t1", depends_on=["t2"])
        task2 = Task(id="t2", depends_on=["t1"])
        
        graph = TaskGraph([task1, task2])
        is_valid, errors = graph.is_valid_dag()
        
        assert not is_valid
        assert len(errors) > 0
        assert any("circular" in err.lower() or "cycle" in err.lower() for err in errors)
    
    def test_topological_sort(self):
        """Test topological sorting"""
        # Create: t1 -> t2 -> t3
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=["t1"])
        task3 = Task(id="t3", depends_on=["t2"])
        
        # Add in wrong order
        graph = TaskGraph([task3, task1, task2])
        
        # Get correct order
        ordered = graph.get_execution_order()
        
        assert len(ordered) == 3
        assert ordered[0].id == "t1"
        assert ordered[1].id == "t2"
        assert ordered[2].id == "t3"
    
    def test_parallel_batches(self):
        """Test parallel batch identification"""
        # Create diamond:
        #      t1
        #     /  \
        #   t2    t3  (parallel)
        #     \  /
        #      t4
        
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=["t1"])
        task3 = Task(id="t3", depends_on=["t1"])
        task4 = Task(id="t4", depends_on=["t2", "t3"])
        
        graph = TaskGraph([task1, task2, task3, task4])
        batches = graph.get_parallel_batches()
        
        # Should have 3 batches
        assert len(batches) == 3
        
        # Batch 1: [t1]
        assert len(batches[0]) == 1
        assert batches[0][0].id == "t1"
        
        # Batch 2: [t2, t3] (parallel)
        assert len(batches[1]) == 2
        batch2_ids = {t.id for t in batches[1]}
        assert batch2_ids == {"t2", "t3"}
        
        # Batch 3: [t4]
        assert len(batches[2]) == 1
        assert batches[2][0].id == "t4"
    
    def test_root_and_leaf_tasks(self):
        """Test root and leaf task identification"""
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=[])
        task3 = Task(id="t3", depends_on=["t1", "t2"])
        
        graph = TaskGraph([task1, task2, task3])
        
        # Roots (no dependencies)
        roots = graph.get_root_tasks()
        assert len(roots) == 2
        root_ids = {t.id for t in roots}
        assert root_ids == {"t1", "t2"}
        
        # Leaves (no dependents)
        leaves = graph.get_leaf_tasks()
        assert len(leaves) == 1
        assert leaves[0].id == "t3"
    
    def test_critical_path(self):
        """Test critical path calculation"""
        # Create:
        #      t1(10s)
        #     /      \
        #  t2(5s)   t3(20s)  <- t3 is longer
        #     \      /
        #      t4(5s)
        
        task1 = Task(id="t1", estimated_time=10, depends_on=[])
        task2 = Task(id="t2", estimated_time=5, depends_on=["t1"])
        task3 = Task(id="t3", estimated_time=20, depends_on=["t1"])
        task4 = Task(id="t4", estimated_time=5, depends_on=["t2", "t3"])
        
        graph = TaskGraph([task1, task2, task3, task4])
        
        # Critical path: t1 -> t3 -> t4 = 10 + 20 + 5 = 35s
        critical_time = graph.calculate_critical_path_length()
        assert critical_time == 35
    
    def test_mermaid_export(self):
        """Test Mermaid diagram export"""
        task1 = Task(id="t1", description="Task 1", depends_on=[])
        task2 = Task(id="t2", description="Task 2", depends_on=["t1"])
        
        graph = TaskGraph([task1, task2])
        mermaid = graph.export_mermaid()
        
        assert "```mermaid" in mermaid
        assert "graph TD" in mermaid
        assert "t1" in mermaid
        assert "t2" in mermaid
        assert "-->" in mermaid


class TestTaskGraphBuilder:
    """Test TaskGraphBuilder"""
    
    def test_builder_basic(self):
        """Test basic builder usage"""
        builder = TaskGraphBuilder()
        
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=[])
        
        builder.add_task(task1).add_task(task2)
        
        graph = builder.build()
        
        assert len(graph.tasks) == 2
    
    def test_builder_add_dependency(self):
        """Test adding dependencies via builder"""
        builder = TaskGraphBuilder()
        
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=[])
        
        builder.add_tasks([task1, task2])
        builder.add_dependency("t2", "t1")  # t2 depends on t1
        
        graph = builder.build()
        
        task2 = graph.tasks["t2"]
        assert "t1" in task2.depends_on


class TestDependencyResolver:
    """Test dependency resolver"""
    
    def test_implicit_file_dependency(self):
        """Test detection of implicit file dependencies"""
        # t1 creates file.py
        task1 = Task(
            id="t1",
            description="Create file.py",
            type=TaskType.WRITE,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_writer"],
                inputs={"filepath": "file.py"}
            ),
            depends_on=[]
        )
        
        # t2 modifies file.py (but doesn't declare dependency)
        task2 = Task(
            id="t2",
            description="Modify file.py",
            type=TaskType.WRITE,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_editor"],
                inputs={"filepath": "file.py"}
            ),
            depends_on=[]  # Missing dependency!
        )
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task1, task2])
        resolver = DependencyResolver(plan)
        
        # Detect implicit
        implicit = resolver.detect_implicit_dependencies()
        
        assert len(implicit) > 0
        assert implicit[0][0] == "t1"  # creator
        assert implicit[0][1] == "t2"  # modifier
        assert "file.py" in implicit[0][2]  # reason
    
    def test_add_implicit_dependencies(self):
        """Test adding implicit dependencies"""
        task1 = Task(
            id="t1",
            description="Create file.py",
            requirements=TaskRequirement(
                agent_type="code",
                tools=[],
                inputs={"filepath": "file.py"}
            ),
            depends_on=[]
        )
        
        task2 = Task(
            id="t2",
            description="Modify file.py",
            type=TaskType.WRITE,
            requirements=TaskRequirement(
                agent_type="code",
                tools=[],
                inputs={"filepath": "file.py"}
            ),
            depends_on=[]
        )
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task1, task2])
        resolver = DependencyResolver(plan)
        
        # Add implicit deps
        updated = resolver.add_implicit_dependencies()
        
        # t2 should now depend on t1
        task2_updated = updated.get_task_by_id("t2")
        assert "t1" in task2_updated.depends_on
    
    def test_bottleneck_identification(self):
        """Test bottleneck identification"""
        # Create plan where t1 is a bottleneck
        task1 = Task(id="t1", estimated_time=120, depends_on=[])
        task2 = Task(id="t2", depends_on=["t1"])
        task3 = Task(id="t3", depends_on=["t1"])
        task4 = Task(id="t4", depends_on=["t1"])
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task1, task2, task3, task4])
        resolver = DependencyResolver(plan)
        
        bottlenecks = resolver.identify_bottlenecks()
        
        # t1 should be identified as bottleneck
        assert len(bottlenecks) > 0
        assert bottlenecks[0]['task'].id == "t1"
    
    def test_time_validation(self):
        """Test time estimate validation"""
        # Create task with unrealistic estimate
        task1 = Task(id="t1", estimated_time=2, depends_on=[])  # Too short
        task2 = Task(id="t2", estimated_time=700, depends_on=[])  # Too long
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task1, task2])
        resolver = DependencyResolver(plan)
        
        warnings = resolver.validate_time_estimates()
        
        assert len(warnings) > 0


class TestEnhancedExecutionPlan:
    """Test EnhancedExecutionPlan"""
    
    def test_plan_creation(self):
        """Test plan creation"""
        tasks = [
            Task(id="t1", description="Task 1", depends_on=[]),
            Task(id="t2", description="Task 2", depends_on=["t1"])
        ]
        
        plan = EnhancedExecutionPlan(
            goal="Test goal",
            tasks=tasks,
            estimated_total_time=60,
            complexity_score=30.0
        )
        
        assert plan.goal == "Test goal"
        assert len(plan.tasks) == 2
        assert plan.estimated_total_time == 60
        assert plan.complexity_score == 30.0
    
    def test_get_ready_tasks(self):
        """Test getting ready tasks"""
        task1 = Task(id="t1", depends_on=[])
        task2 = Task(id="t2", depends_on=["t1"])
        task3 = Task(id="t3", depends_on=["t2"])
        
        plan = EnhancedExecutionPlan(goal="Test", tasks=[task1, task2, task3])
        
        # Initially, only t1 is ready
        ready = plan.get_ready_tasks(set())
        assert len(ready) == 1
        assert ready[0].id == "t1"
        
        # After t1 completes, t2 is ready
        ready = plan.get_ready_tasks({"t1"})
        assert len(ready) == 1
        assert ready[0].id == "t2"
        
        # After t1 and t2, t3 is ready
        ready = plan.get_ready_tasks({"t1", "t2"})
        assert len(ready) == 1
        assert ready[0].id == "t3"
    
    def test_plan_statistics(self):
        """Test plan statistics"""
        tasks = [
            Task(id="t1", estimated_time=30, risk_level="low"),
            Task(id="t2", estimated_time=60, risk_level="medium"),
            Task(id="t3", estimated_time=45, risk_level="high")
        ]
        
        plan = EnhancedExecutionPlan(
            goal="Test",
            tasks=tasks,
            estimated_total_time=135
        )
        
        stats = plan.get_statistics()
        
        assert stats['total_tasks'] == 3
        assert stats['risk_counts']['low'] == 1
        assert stats['risk_counts']['medium'] == 1
        assert stats['risk_counts']['high'] == 1


# Integration tests (require actual components)
class TestIntegration:
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow from tasks to graph to analysis"""
        # Create tasks
        task1 = Task(id="t1", description="Install deps", estimated_time=20, depends_on=[])
        task2 = Task(id="t2", description="Create file", estimated_time=30, depends_on=["t1"])
        task3 = Task(id="t3", description="Write tests", estimated_time=60, depends_on=["t2"])
        
        # Create plan
        plan = EnhancedExecutionPlan(
            goal="Setup project",
            tasks=[task1, task2, task3],
            estimated_total_time=110,
            complexity_score=40.0
        )
        
        # Build graph
        graph = TaskGraph(plan.tasks)
        
        # Validate DAG
        is_valid, errors = graph.is_valid_dag()
        assert is_valid
        
        # Get execution order
        order = graph.get_execution_order()
        assert len(order) == 3
        assert order[0].id == "t1"
        
        # Analyze dependencies
        resolver = DependencyResolver(plan)
        suggestions = resolver.suggest_dependency_optimizations()
        
        # Should work without errors
        assert isinstance(suggestions, list)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
