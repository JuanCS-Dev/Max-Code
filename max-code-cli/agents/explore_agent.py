"""
Explore Agent - Port 8161
Capability: EXPLORATION
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class ExploreAgent(BaseAgent):
    """Explora codebase"""

    def __init__(self, agent_id: str = "explore_agent"):
        super().__init__(agent_id=agent_id, agent_name="Explore Agent", port=8161)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.EXPLORATION]

    def execute(self, task: AgentTask) -> AgentResult:
        print(f"   🔍 Exploring codebase...")
        # Placeholder: em produção, usar tools para explorar
        return AgentResult(task_id=task.id, success=True, output={'files': []})
