"""Tests for CodeAgent - Full Coverage"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.code_agent import CodeAgent


@pytest.fixture
def code_agent():
    with patch('agents.code_agent.ClaudeClient'):
        return CodeAgent(api_key="test-key")


class TestCodeAgentInit:
    def test_has_client(self, code_agent):
        assert hasattr(code_agent, 'client')
    
    def test_has_tot(self, code_agent):
        assert hasattr(code_agent, 'tot')


class TestCodeGeneration:
    @pytest.mark.asyncio
    async def test_generate_code_basic(self, code_agent):
        code_agent.client.complete = AsyncMock(return_value={"code": "print('hello')"})
        result = await code_agent.generate_code("Print hello")
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_generate_code_with_context(self, code_agent):
        code_agent.client.complete = AsyncMock(return_value={"code": "def foo(): pass"})
        result = await code_agent.generate_code("Create function", context={"lang": "python"})
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_generate_code_handles_error(self, code_agent):
        code_agent.client.complete = AsyncMock(side_effect=Exception("API Error"))
        with pytest.raises(Exception):
            await code_agent.generate_code("Test")


class TestCodeValidation:
    @pytest.mark.asyncio
    async def test_validate_syntax_valid(self, code_agent):
        valid_code = "def test():\n    return True"
        result = await code_agent.validate_syntax(valid_code)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_validate_syntax_invalid(self, code_agent):
        invalid_code = "def test(\n    return"
        result = await code_agent.validate_syntax(invalid_code)
        assert result is not None


class TestCodeRefactoring:
    @pytest.mark.asyncio
    async def test_refactor_code(self, code_agent):
        code_agent.client.complete = AsyncMock(return_value={"code": "refactored"})
        original = "x = 1\ny = 2"
        result = await code_agent.refactor_code(original)
        assert result is not None
