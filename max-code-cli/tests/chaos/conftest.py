"""
Conftest for Chaos Testing Suite - Fixtures with Failure Injection

Provides mocked agents/clients with chaos injection capabilities.
"""

import pytest
import time
from unittest.mock import Mock, MagicMock
from sdk.base_agent import AgentTask, AgentResult
from core.llm.unified_client import UnifiedLLMClient
from core.maximus_integration.client import MaximusClient
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


# ============================================================================
# CHAOS INJECTION FIXTURES
# ============================================================================

@pytest.fixture
def mock_agent_with_intermittent_failures():
    """Mock agent that fails intermittently"""
    mock_agent = Mock()
    call_count = {"count": 0}

    def execute_with_failures(task: AgentTask) -> AgentResult:
        call_count["count"] += 1
        # Fail every 3rd call
        if call_count["count"] % 3 == 0:
            raise Exception("Agent temporarily unavailable")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={"result": "Success"},
            metrics={"duration_ms": 50}
        )

    mock_agent.execute = execute_with_failures
    return mock_agent


@pytest.fixture
def mock_agent_with_latency():
    """Mock agent with injected latency"""
    mock_agent = Mock()

    def execute_with_latency(task: AgentTask, latency_ms=100) -> AgentResult:
        time.sleep(latency_ms / 1000)
        return AgentResult(
            task_id=task.id,
            success=True,
            output={"result": "Success"},
            metrics={"duration_ms": latency_ms}
        )

    mock_agent.execute = execute_with_latency
    return mock_agent


@pytest.fixture
def mock_maximus_with_failures():
    """Mock MAXIMUS client with service failures"""
    mock_client = MagicMock()  # Remove spec to allow health_check_all()

    # Mock health check to show failures
    mock_client.health_check_all.return_value = [
        {"service": "maximus-core", "status": "unhealthy", "latency_ms": None},
        {"service": "penelope", "status": "healthy", "latency_ms": 25},
        {"service": "maba", "status": "unhealthy", "latency_ms": None},
    ]

    # Mock analyze to fail
    mock_client.analyze_code.side_effect = Exception("Service unavailable: maximus-core")

    return mock_client


@pytest.fixture
def mock_maximus_all_down():
    """Mock MAXIMUS client with all services down"""
    mock_client = MagicMock()  # Remove spec to allow health_check_all()

    mock_client.health_check_all.return_value = [
        {"service": f"service_{i}", "status": "unhealthy", "latency_ms": None}
        for i in range(8)
    ]

    return mock_client


@pytest.fixture
def mock_maximus_with_recovery():
    """Mock MAXIMUS client that recovers after failures"""
    mock_client = MagicMock()  # Remove spec to allow health_check_all()
    check_count = {"count": 0}

    def health_with_recovery():
        check_count["count"] += 1
        # Fail first 2 checks, recover on 3rd
        if check_count["count"] <= 2:
            return [{"service": "maximus-core", "status": "unhealthy", "latency_ms": None}]
        return [{"service": "maximus-core", "status": "healthy", "latency_ms": 25}]

    mock_client.health_check_all.side_effect = health_with_recovery
    return mock_client
