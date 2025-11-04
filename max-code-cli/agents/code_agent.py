"""
Code Agent - Port 8162
Capability: CODE_GENERATION
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class CodeAgent(BaseAgent):
    """Gera código"""

    def __init__(self, agent_id: str = "code_agent"):
        super().__init__(agent_id=agent_id, agent_name="Code Agent", port=8162)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.CODE_GENERATION]

    def execute(self, task: AgentTask) -> AgentResult:
        print(f"   💻 Generating code...")
        # Placeholder: em produção, gerar código real
        return AgentResult(task_id=task.id, success=True, output={'code': '# Generated code'})
