"""
Test Suite for Enhanced Streaming + Thinking Display

Tests:
- Thinking display rendering
- Claude streaming adapter
- Agent integration
- Tool use tracking
- Performance metrics

Soli Deo Gloria
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

from core.streaming.thinking_display import (
    ThinkingPhase,
    ThinkingStep,
    ToolUse,
    EnhancedThinkingDisplay,
    ThinkingDisplayConfig,
)
from core.streaming.claude_adapter import ClaudeStreamAdapter, ClaudeAgentIntegration
from core.streaming.types import StreamChunk, StreamEventType


class TestThinkingStep:
    """Test ThinkingStep dataclass"""
    
    def test_create_step(self):
        """Test creating thinking step"""
        step = ThinkingStep(
            phase=ThinkingPhase.ANALYZING,
            description="Analyzing code structure"
        )
        
        assert step.phase == ThinkingPhase.ANALYZING
        assert step.description == "Analyzing code structure"
        assert not step.completed
        assert step.error is None
    
    def test_complete_step(self):
        """Test completing thinking step"""
        step = ThinkingStep(
            phase=ThinkingPhase.PLANNING,
            description="Planning implementation"
        )
        
        step.complete(result="Plan created")
        
        assert step.completed
        assert step.result == "Plan created"
        assert step.duration >= 0
    
    def test_fail_step(self):
        """Test failing thinking step"""
        step = ThinkingStep(
            phase=ThinkingPhase.EXECUTING,
            description="Executing action"
        )
        
        step.fail(error="Action failed")
        
        assert step.completed
        assert step.error == "Action failed"
        assert step.phase == ThinkingPhase.ERROR


class TestToolUse:
    """Test ToolUse tracking"""
    
    def test_create_tool_use(self):
        """Test creating tool use"""
        tool = ToolUse(
            tool_name="read_file",
            input_params={"path": "main.py"}
        )
        
        assert tool.tool_name == "read_file"
        assert tool.input_params["path"] == "main.py"
        assert not tool.completed
    
    def test_complete_tool_use(self):
        """Test completing tool use"""
        tool = ToolUse(
            tool_name="write_file",
            input_params={"path": "test.py", "content": "# Test"}
        )
        
        tool.complete(output="File written")
        
        assert tool.completed
        assert tool.output == "File written"
        assert tool.duration >= 0
    
    def test_fail_tool_use(self):
        """Test failing tool use"""
        tool = ToolUse(
            tool_name="execute_command",
            input_params={"cmd": "test"}
        )
        
        tool.fail(error="Command not found")
        
        assert tool.completed
        assert tool.error == "Command not found"


class TestEnhancedThinkingDisplay:
    """Test EnhancedThinkingDisplay"""
    
    def test_initialization(self):
        """Test display initialization"""
        display = EnhancedThinkingDisplay(agent_name="code")
        
        assert display.agent_name == "code"
        assert display.current_phase == ThinkingPhase.INITIALIZING
        assert len(display.thinking_steps) == 0
        assert len(display.tool_uses) == 0
    
    def test_add_thinking_step(self):
        """Test adding thinking step"""
        display = EnhancedThinkingDisplay(agent_name="test")
        
        display.add_thinking_step(
            ThinkingPhase.ANALYZING,
            "Analyzing test coverage"
        )
        
        assert len(display.thinking_steps) == 1
        assert display.current_phase == ThinkingPhase.ANALYZING
        assert display.thinking_steps[0].description == "Analyzing test coverage"
    
    def test_add_tool_use(self):
        """Test adding tool use"""
        display = EnhancedThinkingDisplay(agent_name="fix")
        
        display.add_tool_use("lint_code", {"file": "app.py"})
        
        assert len(display.tool_uses) == 1
        assert display.tool_uses[0].tool_name == "lint_code"
    
    def test_complete_tool_use(self):
        """Test completing tool use"""
        display = EnhancedThinkingDisplay(agent_name="review")
        
        display.add_tool_use("analyze_complexity", {"file": "main.py"})
        display.complete_tool_use("analyze_complexity", {"score": 8})
        
        assert display.tool_uses[0].completed
        assert display.tool_uses[0].output == {"score": 8}
    
    def test_add_output(self):
        """Test adding output"""
        display = EnhancedThinkingDisplay(agent_name="docs")
        
        display.add_output("Generated documentation")
        
        assert len(display.output_lines) == 1
        assert display.output_lines[0] == "Generated documentation"
    
    def test_add_code(self):
        """Test adding code block"""
        display = EnhancedThinkingDisplay(agent_name="code")
        
        code = "def hello():\n    print('Hello')"
        display.add_code(code, language="python")
        
        assert len(display.code_blocks) == 1
        assert display.code_blocks[0][0] == "python"
        assert display.code_blocks[0][1] == code
    
    def test_context_manager_sync(self):
        """Test sync context manager"""
        with EnhancedThinkingDisplay(
            agent_name="test",
            config=ThinkingDisplayConfig(show_thinking=False)
        ) as display:
            display.add_thinking_step(
                ThinkingPhase.INITIALIZING,
                "Starting test"
            )
            assert len(display.thinking_steps) == 1
    
    @pytest.mark.asyncio
    async def test_context_manager_async(self):
        """Test async context manager"""
        async with EnhancedThinkingDisplay(
            agent_name="code",
            config=ThinkingDisplayConfig(show_thinking=False)
        ) as display:
            display.add_thinking_step(
                ThinkingPhase.ANALYZING,
                "Analyzing code"
            )
            await display.update()
            assert len(display.thinking_steps) == 1


class TestClaudeStreamAdapter:
    """Test ClaudeStreamAdapter"""
    
    def test_initialization(self):
        """Test adapter initialization"""
        adapter = ClaudeStreamAdapter(api_key="test-key")
        
        assert adapter.model == "claude-sonnet-4-20250514"
        assert adapter.max_tokens == 4096
    
    def test_is_thinking_content(self):
        """Test thinking content detection"""
        adapter = ClaudeStreamAdapter()
        
        # Thinking content
        assert adapter._is_thinking_content("I need to analyze this code")
        assert adapter._is_thinking_content("First, I'll check the structure")
        assert adapter._is_thinking_content("Let me think about this approach")
        assert adapter._is_thinking_content("I'm analyzing and considering the best solution")
        
        # Non-thinking content
        assert not adapter._is_thinking_content("def hello():")
        assert not adapter._is_thinking_content("Here is the code:")
        assert not adapter._is_thinking_content("The result is 42")
    
    def test_enhance_system_prompt(self):
        """Test system prompt enhancement"""
        adapter = ClaudeStreamAdapter()
        
        original = "You are a helpful assistant."
        enhanced = adapter._enhance_system_prompt(original)
        
        assert "thinking process" in enhanced.lower()
        assert original in enhanced
    
    def test_get_default_system_prompt(self):
        """Test default system prompt generation"""
        adapter = ClaudeStreamAdapter()
        
        prompt = adapter._get_default_system_prompt("code")
        
        assert "CODE" in prompt.upper()
        assert "VÉRTICE CONSTITUTION" in prompt
        assert "thinking process" in prompt.lower()


class TestClaudeAgentIntegration:
    """Test ClaudeAgentIntegration"""
    
    def test_initialization(self):
        """Test integration initialization"""
        integration = ClaudeAgentIntegration(api_key="test-key")
        
        assert integration.adapter is not None
        assert integration.adapter.api_key == "test-key"


class TestStreamingPerformance:
    """Test streaming performance"""
    
    @pytest.mark.asyncio
    async def test_display_update_performance(self):
        """Test display update speed"""
        display = EnhancedThinkingDisplay(
            agent_name="code",
            config=ThinkingDisplayConfig(show_thinking=False)
        )
        
        start = datetime.now()
        
        # Add multiple steps
        for i in range(100):
            display.add_thinking_step(
                ThinkingPhase.EXECUTING,
                f"Step {i}"
            )
            await display.update()
        
        duration = (datetime.now() - start).total_seconds()
        
        # Should complete in < 1 second
        assert duration < 1.0
    
    def test_tool_use_tracking_performance(self):
        """Test tool use tracking performance"""
        display = EnhancedThinkingDisplay(
            agent_name="test",
            config=ThinkingDisplayConfig(show_thinking=False)
        )
        
        start = datetime.now()
        
        # Track multiple tools
        for i in range(100):
            display.add_tool_use(f"tool_{i}", {"param": i})
            display.complete_tool_use(f"tool_{i}", f"result_{i}")
        
        duration = (datetime.now() - start).total_seconds()
        
        # Should complete in < 0.1 second
        assert duration < 0.1
        assert len(display.tool_uses) == 100


class TestStreamingIntegration:
    """Integration tests for complete streaming flow"""
    
    @pytest.mark.asyncio
    async def test_full_streaming_flow(self):
        """Test complete streaming flow with thinking"""
        # This would require mocking Claude API
        # Placeholder for integration test
        pass
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in streaming"""
        display = EnhancedThinkingDisplay(
            agent_name="code",
            config=ThinkingDisplayConfig(show_thinking=False)
        )
        
        # Simulate error
        display.add_thinking_step(
            ThinkingPhase.ERROR,
            "Error occurred"
        )
        
        assert display.current_phase == ThinkingPhase.ERROR


# Test configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
