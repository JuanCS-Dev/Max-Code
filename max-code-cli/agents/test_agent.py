"""
Test Agent - Port 8163
Capability: TESTING
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class TestAgent(BaseAgent):
    """Gera e roda testes"""

    def __init__(self, agent_id: str = "test_agent"):
        super().__init__(agent_id=agent_id, agent_name="Test Agent", port=8163)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.TESTING]

    def execute(self, task: AgentTask) -> AgentResult:
        print(f"   🧪 Testing...")
        return AgentResult(task_id=task.id, success=True, output={'tests_passed': True})
