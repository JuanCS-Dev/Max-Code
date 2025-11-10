"""
Tests for Tool Integration

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)

Soli Deo Gloria
"""

import pytest
from core.tool_integration import ToolIntegration, get_tool_integration
from core.task_models import Task, TaskType, TaskRequirement
from core.tools.types import ToolResult


class TestToolIntegration:
    """Test ToolIntegration class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        integration = ToolIntegration()
        
        assert integration.enhanced_registry is not None
        assert integration.registry is not None
        assert integration.selector is not None
        assert integration.auto_select is True
    
    def test_select_tool_explicit(self):
        """Test explicit tool selection"""
        integration = ToolIntegration()
        
        task = Task(
            id="task_1",
            description="Read a file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "test.txt"}
            )
        )
        
        # Select explicit tool
        tool = integration.select_tool_for_task(task, explicit_tool_name="file_reader")
        
        assert tool is not None
        assert tool.name == "file_reader"
    
    def test_select_tool_from_requirements(self):
        """Test tool selection from task requirements"""
        integration = ToolIntegration()
        
        task = Task(
            id="task_1",
            description="Read a file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_reader"],
                inputs={"file_path": "test.txt"}
            )
        )
        
        # Should use tool from requirements
        tool = integration.select_tool_for_task(task)
        
        assert tool is not None
        assert tool.name == "file_reader"
    
    def test_select_tool_auto(self):
        """Test automatic tool selection"""
        integration = ToolIntegration(auto_select_tools=True)
        
        task = Task(
            id="task_1",
            description="Read the config.json file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "config.json"}
            )
        )
        
        # Should auto-select appropriate tool
        tool = integration.select_tool_for_task(task)
        
        assert tool is not None
        assert tool.capabilities.can_read is True
    
    def test_select_tool_no_auto(self):
        """Test no selection when auto-select disabled"""
        integration = ToolIntegration(auto_select_tools=False)
        
        task = Task(
            id="task_1",
            description="Read a file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={}
            )
        )
        
        # Should return None (no auto-select, no explicit tool)
        tool = integration.select_tool_for_task(task)
        
        assert tool is None
    
    def test_validate_tool_success(self):
        """Test successful tool validation"""
        integration = ToolIntegration()
        
        task = Task(
            id="task_1",
            description="Read file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_reader"],
                inputs={"file_path": "test.txt"}
            )
        )
        
        tool = integration.select_tool_for_task(task)
        valid, issues = integration.validate_tool(tool, task)
        
        # Should be valid (has required params, correct capability)
        assert valid is True or len(issues) == 0
    
    def test_validate_tool_capability_mismatch(self):
        """Test validation fails with capability mismatch"""
        integration = ToolIntegration()
        
        # Task requires write, but file_reader can only read
        task = Task(
            id="task_1",
            description="Write file",
            type=TaskType.WRITE,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_reader"],  # Wrong tool for write
                inputs={"file_path": "test.txt", "content": "test"}
            )
        )
        
        tool = integration.enhanced_registry.get_tool("file_reader")
        valid, issues = integration.validate_tool(tool, task)
        
        # Should fail (tool can't write)
        assert valid is False
        assert any("write" in issue.lower() for issue in issues)
    
    def test_execute_tool_mock(self):
        """Test tool execution (basic check)"""
        integration = ToolIntegration()
        
        # Create simple task
        task = Task(
            id="task_1",
            description="Read README",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_reader"],
                inputs={"file_path": "README.md"}
            )
        )
        
        tool = integration.select_tool_for_task(task)
        result = integration.execute_tool(tool, task, validate_first=False)
        
        # Should return ToolResult
        assert isinstance(result, ToolResult)
    
    def test_execute_task_all_in_one(self):
        """Test execute_task convenience method"""
        integration = ToolIntegration()
        
        task = Task(
            id="task_1",
            description="Read README.md file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "README.md"}
            )
        )
        
        # All-in-one: select + validate + execute
        result = integration.execute_task(task)
        
        assert isinstance(result, ToolResult)
    
    @pytest.mark.asyncio
    async def test_execute_tasks_batch(self):
        """Test batch task execution"""
        integration = ToolIntegration()
        
        tasks = [
            Task(
                id="task_1",
                description="Read README.md",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"file_path": "README.md"}
                )
            ),
            Task(
                id="task_2",
                description="Read setup.py",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"file_path": "setup.py"}
                )
            ),
        ]
        
        results = await integration.execute_tasks_batch(tasks, validate=False)
        
        assert isinstance(results, dict)
        assert len(results) == 2
        assert "task_1" in results
        assert "task_2" in results
    
    def test_get_tools_summary(self):
        """Test getting tools summary"""
        integration = ToolIntegration()
        
        summary = integration.get_tools_summary()
        
        assert "total_tools" in summary
        assert "by_category" in summary
        assert "capabilities_count" in summary
        assert "tool_names" in summary
        assert summary["total_tools"] > 0
    
    def test_get_tool_info(self):
        """Test getting tool info"""
        integration = ToolIntegration()
        
        info = integration.get_tool_info("file_reader")
        
        assert info is not None
        assert info["name"] == "file_reader"
        assert "description" in info
        assert "capabilities" in info
        assert "requirements" in info
        assert "performance" in info
    
    def test_get_tool_info_nonexistent(self):
        """Test getting info for nonexistent tool"""
        integration = ToolIntegration()
        
        info = integration.get_tool_info("nonexistent_tool")
        
        assert info is None
    
    def test_suggest_tools(self):
        """Test tool suggestions"""
        integration = ToolIntegration()
        
        suggestions = integration.suggest_tools_for_description(
            "Read the config file",
            count=3
        )
        
        assert isinstance(suggestions, list)
        assert len(suggestions) <= 3
        
        # Should suggest tools that can read
        if suggestions:
            assert suggestions[0].capabilities.can_read is True


class TestGlobalInstance:
    """Test global instance management"""
    
    def test_singleton(self):
        """Test get_tool_integration returns singleton"""
        integration1 = get_tool_integration()
        integration2 = get_tool_integration()
        
        assert integration1 is integration2
    
    def test_global_usage(self):
        """Test using global instance"""
        integration = get_tool_integration()
        
        summary = integration.get_tools_summary()
        
        assert summary["total_tools"] > 0
