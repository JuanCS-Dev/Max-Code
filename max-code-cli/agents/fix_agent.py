"""
Fix Agent - Port 8165
Capability: DEBUGGING
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class FixAgent(BaseAgent):
    """Bug fixing"""

    def __init__(self, agent_id: str = "fix_agent"):
        super().__init__(agent_id=agent_id, agent_name="Fix Agent", port=8165)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.DEBUGGING]

    def execute(self, task: AgentTask) -> AgentResult:
        print(f"   🔧 Fixing bug...")
        return AgentResult(task_id=task.id, success=True, output={'fixed': True})
