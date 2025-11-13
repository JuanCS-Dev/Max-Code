"""
Conftest for Load Testing Suite - Fixtures and Mocking

Provides mocked agents for fast, isolated load testing.
"""

import pytest
from unittest.mock import Mock, MagicMock
from sdk.base_agent import AgentTask, AgentResult
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# ============================================================================
# MOCKED AGENT FIXTURES
# ============================================================================

@pytest.fixture
def mock_code_agent():
    """Mock CodeAgent that returns instantly"""
    mock_agent = Mock()

    def mock_execute(task: AgentTask) -> AgentResult:
        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                "code": """
def fibonacci(n):
    if n <= 1:
        return n
    cache = {0: 0, 1: 1}
    for i in range(2, n + 1):
        cache[i] = cache[i-1] + cache[i-2]
    return cache[n]
""",
                "language": "python",
                "explanation": "Fibonacci with memoization"
            },
            metrics={"duration_ms": 50}
        )

    mock_agent.execute = mock_execute
    mock_agent.agent_id = "code_agent"
    mock_agent.agent_name = "Code Agent (Mocked)"

    return mock_agent


@pytest.fixture
def mock_plan_agent():
    """Mock PlanAgent that returns instantly"""
    mock_agent = Mock()

    def mock_execute(task: AgentTask) -> AgentResult:
        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                "plan": [
                    {"step": 1, "action": "Analyze requirements"},
                    {"step": 2, "action": "Design architecture"},
                    {"step": 3, "action": "Implement core logic"},
                    {"step": 4, "action": "Write tests"},
                    {"step": 5, "action": "Deploy"}
                ],
                "estimated_hours": 8
            },
            metrics={"duration_ms": 30}
        )

    mock_agent.execute = mock_execute
    mock_agent.agent_id = "plan_agent"
    mock_agent.agent_name = "Plan Agent (Mocked)"

    return mock_agent


@pytest.fixture
def mock_review_agent():
    """Mock ReviewAgent that returns instantly"""
    mock_agent = Mock()

    def mock_execute(task: AgentTask) -> AgentResult:
        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                "issues": [
                    {"severity": "low", "message": "Consider adding type hints"},
                    {"severity": "medium", "message": "Missing docstring"}
                ],
                "score": 85,
                "recommendation": "APPROVE_WITH_SUGGESTIONS"
            },
            metrics={"duration_ms": 40}
        )

    mock_agent.execute = mock_execute
    mock_agent.agent_id = "review_agent"
    mock_agent.agent_name = "Review Agent (Mocked)"

    return mock_agent


@pytest.fixture
def mock_test_agent():
    """Mock TestAgent that returns instantly"""
    mock_agent = Mock()

    def mock_execute(task: AgentTask) -> AgentResult:
        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                "tests": """
def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(6) == 8
    assert fibonacci(10) == 55
""",
                "coverage": 95,
                "test_count": 4
            },
            metrics={"duration_ms": 45}
        )

    mock_agent.execute = mock_execute
    mock_agent.agent_id = "test_agent"
    mock_agent.agent_name = "Test Agent (Mocked)"

    return mock_agent
