"""
Tests for Plan Preview System

Tests:
- Plan visualization
- ExecutionPlan integration
- Confirmation UI
- Risk display

Soli Deo Gloria
"""

import pytest
from io import StringIO
from rich.console import Console

from core.plan_visualizer import PlanVisualizer, preview_and_confirm
from core.task_planner import ExecutionPlan, ToolStep, PlanStatus
from datetime import datetime


class TestPlanVisualizer:
    """Test plan visualization"""
    
    def test_initialization(self):
        """Test visualizer initialization"""
        visualizer = PlanVisualizer()
        
        assert visualizer.console is not None
        assert isinstance(visualizer.console, Console)
    
    def test_show_plan_basic(self):
        """Test showing basic plan"""
        # Create simple plan
        steps = [
            ToolStep(
                step_number=1,
                tool_name="file_writer",
                description="Create main.py",
                parameters={"path": "main.py"},
                expected_output="File created",
                constitutional_risk="LOW"
            ),
            ToolStep(
                step_number=2,
                tool_name="code_agent",
                description="Generate function",
                parameters={"prompt": "Hello world"},
                expected_output="Function generated",
                constitutional_risk="MEDIUM"
            )
        ]
        
        plan = ExecutionPlan(
            task_id="test-001",
            task_description="Create hello world",
            architectural_vision="Simple Python script",
            complexity_estimate="LOW",
            estimated_time="5 seconds",
            dependencies=[],
            dream_analysis="Realistic plan",
            reality_score=0.9,
            alternative_suggestions=[],
            risks_identified=[],
            steps=steps,
            constitutional_approved=True,
            constitutional_score=0.95
        )
        
        # Capture output
        console = Console(file=StringIO())
        visualizer = PlanVisualizer(console)
        
        # Should not raise
        visualizer.show_plan(plan)
        
        # Check output was generated
        output = console.file.getvalue()
        assert len(output) > 0
        assert "test-001" in output or "hello world" in output.lower()
    
    def test_show_plan_with_risks(self):
        """Test plan with various risk levels"""
        steps = [
            ToolStep(
                step_number=1,
                tool_name="file_reader",
                description="Read config",
                parameters={},
                expected_output="Config data",
                constitutional_risk="LOW"
            ),
            ToolStep(
                step_number=2,
                tool_name="file_editor",
                description="Modify critical file",
                parameters={},
                expected_output="File modified",
                constitutional_risk="HIGH"
            ),
            ToolStep(
                step_number=3,
                tool_name="bash_tool",
                description="Run system command",
                parameters={},
                expected_output="Command output",
                constitutional_risk="CRITICAL"
            )
        ]
        
        plan = ExecutionPlan(
            task_id="test-002",
            task_description="Complex task",
            architectural_vision="Multi-step process",
            complexity_estimate="HIGH",
            estimated_time="2 minutes",
            dependencies=["bash", "python"],
            dream_analysis="Some risks present",
            reality_score=0.6,
            alternative_suggestions=["Use safer approach"],
            risks_identified=["System command execution"],
            steps=steps,
            constitutional_approved=False,
            constitutional_score=0.4,
            constitutional_violations=["P3: High risk operation without safeguards"]
        )
        
        console = Console(file=StringIO())
        visualizer = PlanVisualizer(console)
        
        visualizer.show_plan(plan)
        
        output = console.file.getvalue()
        assert "CRITICAL" in output or "🚨" in output
        assert "HIGH" in output or "🔴" in output
    
    def test_risk_level_colors(self):
        """Test risk level color mapping"""
        visualizer = PlanVisualizer()
        
        assert visualizer.RISK_COLORS["LOW"] == "green"
        assert visualizer.RISK_COLORS["MEDIUM"] == "yellow"
        assert visualizer.RISK_COLORS["HIGH"] == "red"
        assert visualizer.RISK_COLORS["CRITICAL"] == "bold red"
    
    def test_risk_level_icons(self):
        """Test risk level icon mapping"""
        visualizer = PlanVisualizer()
        
        assert visualizer.RISK_ICONS["LOW"] == "🟢"
        assert visualizer.RISK_ICONS["MEDIUM"] == "🟡"
        assert visualizer.RISK_ICONS["HIGH"] == "🔴"
        assert visualizer.RISK_ICONS["CRITICAL"] == "🚨"
    
    def test_show_plan_without_sofia(self):
        """Test plan without SOFIA analysis"""
        steps = [
            ToolStep(
                step_number=1,
                tool_name="test_tool",
                description="Test step",
                parameters={},
                expected_output="Output",
                constitutional_risk="LOW"
            )
        ]
        
        plan = ExecutionPlan(
            task_id="test-003",
            task_description="Minimal plan",
            architectural_vision="",  # Empty
            complexity_estimate="LOW",
            estimated_time="1 second",
            dependencies=[],
            dream_analysis="",  # Empty
            reality_score=1.0,
            alternative_suggestions=[],
            risks_identified=[],
            steps=steps
        )
        
        console = Console(file=StringIO())
        visualizer = PlanVisualizer(console)
        
        # Should not raise even with empty fields
        visualizer.show_plan(plan)
        
        output = console.file.getvalue()
        assert len(output) > 0
    
    def test_show_plan_empty_steps(self):
        """Test plan with no steps"""
        plan = ExecutionPlan(
            task_id="test-004",
            task_description="Empty plan",
            architectural_vision="No steps",
            complexity_estimate="LOW",
            estimated_time="0 seconds",
            dependencies=[],
            dream_analysis="Invalid plan",
            reality_score=0.0,
            alternative_suggestions=["Add steps"],
            risks_identified=["No execution steps"],
            steps=[]  # Empty
        )
        
        console = Console(file=StringIO())
        visualizer = PlanVisualizer(console)
        
        visualizer.show_plan(plan)
        
        output = console.file.getvalue()
        assert "No execution steps" in output or "0" in output


class TestExecutionPlanIntegration:
    """Test integration with ExecutionPlan model"""
    
    def test_execution_plan_to_dict(self):
        """Test ExecutionPlan.to_dict() method"""
        steps = [
            ToolStep(
                step_number=1,
                tool_name="test_tool",
                description="Test",
                parameters={},
                expected_output="Output",
                constitutional_risk="LOW"
            )
        ]
        
        plan = ExecutionPlan(
            task_id="test-005",
            task_description="Test plan",
            architectural_vision="Vision",
            complexity_estimate="LOW",
            estimated_time="1s",
            dependencies=[],
            dream_analysis="Analysis",
            reality_score=1.0,
            alternative_suggestions=[],
            risks_identified=[],
            steps=steps
        )
        
        plan_dict = plan.to_dict()
        
        assert isinstance(plan_dict, dict)
        assert plan_dict['task_id'] == "test-005"
        assert plan_dict['task_description'] == "Test plan"
        assert len(plan_dict['steps']) == 1
    
    def test_plan_status_enum(self):
        """Test PlanStatus enum values"""
        assert PlanStatus.PENDING.value == "pending"
        assert PlanStatus.PLANNING.value == "planning"
        assert PlanStatus.APPROVED.value == "approved"
        assert PlanStatus.EXECUTING.value == "executing"
        assert PlanStatus.COMPLETED.value == "completed"
        assert PlanStatus.FAILED.value == "failed"


class TestConvenienceFunction:
    """Test convenience functions"""
    
    def test_preview_and_confirm(self):
        """Test preview_and_confirm function"""
        steps = [
            ToolStep(
                step_number=1,
                tool_name="test_tool",
                description="Test",
                parameters={},
                expected_output="Output",
                constitutional_risk="LOW"
            )
        ]
        
        plan = ExecutionPlan(
            task_id="test-006",
            task_description="Test",
            architectural_vision="Vision",
            complexity_estimate="LOW",
            estimated_time="1s",
            dependencies=[],
            dream_analysis="Analysis",
            reality_score=1.0,
            alternative_suggestions=[],
            risks_identified=[],
            steps=steps
        )
        
        # Function should exist and be callable
        assert callable(preview_and_confirm)
        
        # Note: Can't easily test interactive confirmation
        # without mocking user input


class TestToolStep:
    """Test ToolStep model"""
    
    def test_tool_step_creation(self):
        """Test creating ToolStep"""
        step = ToolStep(
            step_number=1,
            tool_name="file_writer",
            description="Write file",
            parameters={"path": "test.py"},
            expected_output="File written",
            constitutional_risk="LOW"
        )
        
        assert step.step_number == 1
        assert step.tool_name == "file_writer"
        assert step.description == "Write file"
        assert step.constitutional_risk == "LOW"
        assert step.executed == False
        assert step.result is None
        assert step.error is None
    
    def test_tool_step_execution_state(self):
        """Test ToolStep execution state"""
        step = ToolStep(
            step_number=1,
            tool_name="test_tool",
            description="Test",
            parameters={},
            expected_output="Output",
            constitutional_risk="LOW"
        )
        
        # Initially not executed
        assert step.executed == False
        
        # Mark as executed with result
        step.executed = True
        step.result = {"success": True}
        
        assert step.executed == True
        assert step.result is not None
        assert step.error is None
        
        # Mark as failed
        step.error = "Test error"
        
        assert step.error == "Test error"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
