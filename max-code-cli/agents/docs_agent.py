"""
Docs Agent - Port 8166
Capability: DOCUMENTATION
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class DocsAgent(BaseAgent):
    """Geração de documentação"""

    def __init__(self, agent_id: str = "docs_agent"):
        super().__init__(agent_id=agent_id, agent_name="Docs Agent", port=8166)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.DOCUMENTATION]

    def execute(self, task: AgentTask) -> AgentResult:
        print(f"   📝 Generating documentation...")
        return AgentResult(task_id=task.id, success=True, output={'docs': '# Documentation'})
