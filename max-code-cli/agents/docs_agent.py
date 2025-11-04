"""
Docs Agent - ENHANCED with MAXIMUS
Port: 8166
Capability: DOCUMENTATION

v2.0: Standard Docs + NIS Narrative Intelligence
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import NISClient


class DocsAgent(BaseAgent):
    """Documentation generation with narrative intelligence"""

    def __init__(self, agent_id: str = "docs_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Docs Agent (MAXIMUS-Enhanced)", port=8166)
        self.nis_client = NISClient() if enable_maximus else None

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.DOCUMENTATION]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        code_changes = task.parameters.get('changes', [])

        print(f"   📝 Phase 1: Generating standard docs...")
        standard_docs = f"# Documentation\n\nChanges: {len(code_changes)} files modified"

        narrative = None
        if self.nis_client:
            try:
                if await self.nis_client.health_check():
                    print(f"   📖 Phase 2: NIS narrative generation...")
                    from core.maximus_integration.nis_client import CodeChange, NarrativeStyle
                    narrative = await self.nis_client.generate_narrative(
                        changes=[CodeChange(**c) for c in code_changes] if code_changes else [],
                        style=NarrativeStyle.STORY,
                        context=task.parameters.get('context', {})
                    )
                    print(f"      └─ Generated: {narrative.title}")
                    standard_docs = f"{narrative.story}\n\n{standard_docs}"
            except:
                print(f"      ⚠️ NIS offline")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'docs': standard_docs, 'narrative': narrative},
            metrics={'mode': 'hybrid' if narrative else 'standalone'}
        )
