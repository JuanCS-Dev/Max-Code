"""
Tests for Enhanced Decorators (v2.0)

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)

Soli Deo Gloria
"""

import pytest
import asyncio
from core.tools.decorator import (
    enhanced_tool,
    quick_tool,
    search_tool,
    write_tool,
    execute_tool,
)
from core.tools.tool_metadata import ToolCategory
from core.tools.types import ToolResult
from core.tools.enhanced_registry import get_enhanced_registry


class TestEnhancedTool:
    """Test @enhanced_tool decorator"""
    
    def test_basic_sync_function(self):
        """Test basic synchronous function decoration"""
        @enhanced_tool(
            name="test_tool",
            description="Test tool",
            can_read=True,
            auto_register=False
        )
        def my_tool(arg1: str) -> ToolResult:
            return ToolResult.success(f"Result: {arg1}")
        
        # Check metadata attached
        assert hasattr(my_tool, '_tool_name')
        assert my_tool._tool_name == "test_tool"
        assert hasattr(my_tool, '_tool_enhanced_metadata')
        
        # Check enhanced metadata
        metadata = my_tool._tool_enhanced_metadata
        assert metadata.name == "test_tool"
        assert metadata.capabilities.can_read is True
        assert metadata.capabilities.can_write is False
    
    def test_basic_async_function(self):
        """Test basic asynchronous function decoration"""
        @enhanced_tool(
            name="async_test",
            description="Async test",
            can_execute=True,
            auto_register=False
        )
        async def my_async_tool(arg1: str) -> ToolResult:
            await asyncio.sleep(0.01)
            return ToolResult.success(f"Async result: {arg1}")
        
        assert my_async_tool._tool_is_async is True
        assert my_async_tool._tool_name == "async_test"
    
    def test_parameter_extraction(self):
        """Test automatic parameter extraction from function signature"""
        @enhanced_tool(
            name="multi_param",
            description="Multiple parameters",
            auto_register=False
        )
        def multi_param(
            name: str,
            age: int,
            active: bool,
            tags: list
        ) -> ToolResult:
            return ToolResult.success("ok")
        
        metadata = multi_param._tool_enhanced_metadata
        params = metadata.parameters
        
        assert len(params) == 4
        
        # Check name parameter
        name_param = next(p for p in params if p['name'] == 'name')
        assert name_param['type'] == 'string'
        assert name_param['required'] is True
        
        # Check age parameter
        age_param = next(p for p in params if p['name'] == 'age')
        assert age_param['type'] == 'number'
        
        # Check active parameter
        active_param = next(p for p in params if p['name'] == 'active')
        assert active_param['type'] == 'boolean'
        
        # Check tags parameter
        tags_param = next(p for p in params if p['name'] == 'tags')
        assert tags_param['type'] == 'array'
    
    def test_optional_parameters(self):
        """Test optional vs required parameter detection"""
        @enhanced_tool(
            name="optional_test",
            description="Optional params",
            auto_register=False
        )
        def optional_test(
            required: str,
            optional: str = "default"
        ) -> ToolResult:
            return ToolResult.success("ok")
        
        metadata = optional_test._tool_enhanced_metadata
        params = metadata.parameters
        
        required_param = next(p for p in params if p['name'] == 'required')
        assert required_param['required'] is True
        
        optional_param = next(p for p in params if p['name'] == 'optional')
        assert optional_param['required'] is False
    
    def test_capabilities_flags(self):
        """Test capability flags"""
        @enhanced_tool(
            name="capable_tool",
            description="Tool with capabilities",
            can_read=True,
            can_write=True,
            can_search=True,
            can_execute=False,
            auto_register=False
        )
        def capable_tool(arg: str) -> ToolResult:
            return ToolResult.success("ok")
        
        caps = capable_tool._tool_enhanced_metadata.capabilities
        assert caps.can_read is True
        assert caps.can_write is True
        assert caps.can_search is True
        assert caps.can_execute is False
    
    def test_requirements_flags(self):
        """Test requirement flags"""
        @enhanced_tool(
            name="req_tool",
            description="Tool with requirements",
            requires_filepath=True,
            requires_pattern=True,
            requires_content=False,
            auto_register=False
        )
        def req_tool(arg: str) -> ToolResult:
            return ToolResult.success("ok")
        
        reqs = req_tool._tool_enhanced_metadata.requirements
        assert reqs.requires_filepath is True
        assert reqs.requires_pattern is True
        assert reqs.requires_content is False
    
    def test_performance_flags(self):
        """Test performance characteristics"""
        @enhanced_tool(
            name="perf_tool",
            description="Tool with performance flags",
            safe=False,
            destructive=True,
            expensive=True,
            estimated_time=30,
            auto_register=False
        )
        def perf_tool(arg: str) -> ToolResult:
            return ToolResult.success("ok")
        
        perf = perf_tool._tool_enhanced_metadata.performance
        assert perf.safe is False
        assert perf.destructive is True
        assert perf.expensive is True
        assert perf.estimated_time == 30
    
    def test_category_assignment(self):
        """Test tool category assignment"""
        @enhanced_tool(
            name="search_tool",
            description="Search tool",
            category=ToolCategory.SEARCH,
            auto_register=False
        )
        def search_tool(pattern: str) -> ToolResult:
            return ToolResult.success("ok")
        
        assert search_tool._tool_enhanced_metadata.category == ToolCategory.SEARCH
    
    def test_tags_and_examples(self):
        """Test tags and examples"""
        examples = [
            {"input": {"arg": "test"}, "output": "Result: test"}
        ]
        
        @enhanced_tool(
            name="tagged_tool",
            description="Tool with tags",
            tags=["tag1", "tag2", "custom"],
            examples=examples,
            auto_register=False
        )
        def tagged_tool(arg: str) -> ToolResult:
            return ToolResult.success(f"Result: {arg}")
        
        metadata = tagged_tool._tool_enhanced_metadata
        assert "tag1" in metadata.tags
        assert "tag2" in metadata.tags
        assert len(metadata.examples) == 1
    
    def test_execution_sync(self):
        """Test actual execution of sync tool"""
        @enhanced_tool(
            name="exec_test",
            description="Execution test",
            auto_register=False
        )
        def exec_test(message: str) -> ToolResult:
            return ToolResult.success(f"Echo: {message}")
        
        result = exec_test({"message": "hello"})
        
        assert isinstance(result, ToolResult)
        assert result.type == "success"
        assert "Echo: hello" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_execution_async(self):
        """Test actual execution of async tool"""
        @enhanced_tool(
            name="async_exec",
            description="Async execution test",
            auto_register=False
        )
        async def async_exec(message: str) -> ToolResult:
            await asyncio.sleep(0.01)
            return ToolResult.success(f"Async echo: {message}")
        
        result = await async_exec({"message": "hello async"})
        
        assert isinstance(result, ToolResult)
        assert result.type == "success"
        assert "Async echo: hello async" in result.content[0].text
    
    def test_error_handling(self):
        """Test error handling in decorated function"""
        @enhanced_tool(
            name="error_test",
            description="Error handling test",
            auto_register=False
        )
        def error_test(arg: str) -> ToolResult:
            raise ValueError("Intentional error")
        
        result = error_test({"arg": "test"})
        
        assert isinstance(result, ToolResult)
        assert result.type == "error"
        assert "Intentional error" in result.content[0].text
    
    def test_auto_register(self):
        """Test automatic registration with enhanced registry"""
        @enhanced_tool(
            name="auto_reg_test",
            description="Auto registration test",
            can_read=True,
            auto_register=True  # Should auto-register
        )
        def auto_reg_test(arg: str) -> ToolResult:
            return ToolResult.success("ok")
        
        # Check if registered
        registry = get_enhanced_registry()
        tool = registry.get_tool("auto_reg_test")
        
        assert tool is not None
        assert tool.name == "auto_reg_test"
        assert tool.capabilities.can_read is True


class TestQuickTool:
    """Test @quick_tool decorator"""
    
    def test_quick_tool_defaults(self):
        """Test quick_tool sets appropriate defaults"""
        @quick_tool("quick_test", "Quick test tool")
        def quick_test(filepath: str) -> ToolResult:
            return ToolResult.success(f"Read: {filepath}")
        
        metadata = quick_test._tool_enhanced_metadata
        
        # Check defaults
        assert metadata.capabilities.can_read is True
        assert metadata.performance.safe is True
        assert metadata.category == ToolCategory.FILE_OPS
    
    def test_quick_tool_without_name(self):
        """Test quick_tool using function name"""
        @quick_tool()
        def my_quick_tool(arg: str) -> ToolResult:
            '''Quick tool with docstring'''
            return ToolResult.success("ok")
        
        assert my_quick_tool._tool_name == "my_quick_tool"
        assert "docstring" in my_quick_tool._tool_description.lower()


class TestSearchTool:
    """Test @search_tool decorator"""
    
    def test_search_tool_defaults(self):
        """Test search_tool sets search-specific defaults"""
        @search_tool("grep_test", "Grep test tool")
        def grep_test(pattern: str, path: str = ".") -> ToolResult:
            return ToolResult.success("found")
        
        metadata = grep_test._tool_enhanced_metadata
        
        assert metadata.category == ToolCategory.SEARCH
        assert metadata.capabilities.can_read is True
        assert metadata.capabilities.can_search is True
        assert metadata.requirements.requires_pattern is True


class TestWriteTool:
    """Test @write_tool decorator"""
    
    def test_write_tool_defaults(self):
        """Test write_tool sets write-specific defaults"""
        @write_tool("writer_test", "Writer test tool")
        def writer_test(filepath: str, content: str) -> ToolResult:
            return ToolResult.success("written")
        
        metadata = writer_test._tool_enhanced_metadata
        
        assert metadata.capabilities.can_write is True
        assert metadata.requirements.requires_filepath is True
        assert metadata.requirements.requires_content is True
        assert metadata.performance.destructive is True
        assert metadata.performance.safe is False


class TestExecuteTool:
    """Test @execute_tool decorator"""
    
    def test_execute_tool_defaults(self):
        """Test execute_tool sets execution-specific defaults"""
        @execute_tool("exec_test", "Execute test tool")
        async def exec_test(command: str) -> ToolResult:
            return ToolResult.success("executed")
        
        metadata = exec_test._tool_enhanced_metadata
        
        assert metadata.category == ToolCategory.EXECUTION
        assert metadata.capabilities.can_execute is True
        assert metadata.performance.destructive is True
        assert metadata.performance.safe is False
        assert metadata.performance.expensive is True


class TestIntegration:
    """Integration tests"""
    
    def test_multiple_decorators_coexist(self):
        """Test multiple decorated tools can coexist"""
        @quick_tool("tool1", "Tool 1")
        def tool1(arg: str) -> ToolResult:
            return ToolResult.success("1")
        
        @search_tool("tool2", "Tool 2")
        def tool2(pattern: str) -> ToolResult:
            return ToolResult.success("2")
        
        @write_tool("tool3", "Tool 3")
        def tool3(filepath: str, content: str) -> ToolResult:
            return ToolResult.success("3")
        
        assert tool1._tool_name == "tool1"
        assert tool2._tool_name == "tool2"
        assert tool3._tool_name == "tool3"
        
        # Each has different capabilities
        assert tool1._tool_enhanced_metadata.capabilities.can_read is True
        assert tool2._tool_enhanced_metadata.capabilities.can_search is True
        assert tool3._tool_enhanced_metadata.capabilities.can_write is True
    
    def test_registry_integration(self):
        """Test integration with EnhancedToolRegistry"""
        @enhanced_tool(
            name="reg_int_test",
            description="Registry integration test",
            can_read=True,
            can_search=True,
            tags=["test", "integration"],
            auto_register=True
        )
        def reg_int_test(pattern: str) -> ToolResult:
            return ToolResult.success("ok")
        
        # Get from registry
        registry = get_enhanced_registry()
        tool = registry.get_tool("reg_int_test")
        
        assert tool is not None
        assert tool.name == "reg_int_test"
        assert tool.capabilities.can_read is True
        assert tool.capabilities.can_search is True
        assert "test" in tool.tags
        assert "integration" in tool.tags
