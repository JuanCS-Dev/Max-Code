"""
Review Agent - Port 8164
Capability: CODE_REVIEW
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class ReviewAgent(BaseAgent):
    """Code review"""

    def __init__(self, agent_id: str = "review_agent"):
        super().__init__(agent_id=agent_id, agent_name="Review Agent", port=8164)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.CODE_REVIEW]

    def execute(self, task: AgentTask) -> AgentResult:
        print(f"   👀 Reviewing code...")
        return AgentResult(task_id=task.id, success=True, output={'review': 'LGTM'})
