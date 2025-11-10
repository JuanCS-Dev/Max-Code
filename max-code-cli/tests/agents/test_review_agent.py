"""Tests for ReviewAgent"""
import pytest
from unittest.mock import AsyncMock, patch
from agents.review_agent import ReviewAgent


@pytest.fixture
def review_agent():
    with patch('agents.review_agent.ClaudeClient'):
        return ReviewAgent(api_key="test-key")


class TestReviewAgentInit:
    def test_initialization(self, review_agent):
        assert review_agent.client is not None


class TestCodeReview:
    @pytest.mark.asyncio
    async def test_review_code_basic(self, review_agent):
        review_agent.client.complete = AsyncMock(return_value={"review": "looks good"})
        result = await review_agent.review_code("def foo(): pass")
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_review_code_finds_issues(self, review_agent):
        review_agent.client.complete = AsyncMock(return_value={"issues": ["issue1"]})
        result = await review_agent.review_code("bad code")
        assert result is not None


class TestQualityChecks:
    @pytest.mark.asyncio
    async def test_check_quality_metrics(self, review_agent):
        result = await review_agent.check_quality_metrics("code")
        assert result is not None
