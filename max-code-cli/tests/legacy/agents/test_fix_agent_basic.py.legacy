"""Tests for FixAgent"""
import pytest
from unittest.mock import AsyncMock, patch
from agents.fix_agent import FixAgent


@pytest.fixture
def fix_agent():
    with patch('agents.fix_agent.ClaudeClient'):
        return FixAgent(api_key="test-key")


class TestFixAgentInit:
    def test_has_client(self, fix_agent):
        assert fix_agent.client is not None


class TestBugFixing:
    @pytest.mark.asyncio
    async def test_fix_bug_basic(self, fix_agent):
        fix_agent.client.complete = AsyncMock(return_value={"fixed_code": "corrected"})
        result = await fix_agent.fix_bug("buggy code", "error message")
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_fix_bug_with_context(self, fix_agent):
        fix_agent.client.complete = AsyncMock(return_value={"fix": "done"})
        result = await fix_agent.fix_bug("code", "error", context={"file": "test.py"})
        assert result is not None


class TestErrorAnalysis:
    @pytest.mark.asyncio
    async def test_analyze_error(self, fix_agent):
        result = await fix_agent.analyze_error("NameError: name 'x' is not defined")
        assert result is not None
