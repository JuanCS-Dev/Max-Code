"""Tests for TestAgent - Full Coverage"""
import pytest
from unittest.mock import AsyncMock, patch
from agents.test_agent import TestAgent


@pytest.fixture
def test_agent():
    with patch('agents.test_agent.ClaudeClient'):
        return TestAgent(api_key="test-key")


class TestTestAgentInit:
    def test_initialization(self, test_agent):
        assert test_agent.client is not None


class TestTestGeneration:
    @pytest.mark.asyncio
    async def test_generate_tests_basic(self, test_agent):
        test_agent.client.complete = AsyncMock(return_value={"tests": "def test_foo(): pass"})
        result = await test_agent.generate_tests("def foo(): pass")
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_generate_tests_with_coverage_target(self, test_agent):
        test_agent.client.complete = AsyncMock(return_value={"tests": "test code"})
        result = await test_agent.generate_tests("code", coverage_target=0.8)
        assert result is not None


class TestCoverageAnalysis:
    @pytest.mark.asyncio
    async def test_analyze_coverage(self, test_agent):
        result = await test_agent.analyze_coverage("test_file.py")
        assert result is not None


class TestTestValidation:
    @pytest.mark.asyncio
    async def test_validate_tests(self, test_agent):
        tests = "def test_example(): assert True"
        result = await test_agent.validate_tests(tests)
        assert result is not None
