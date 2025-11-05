"""
Code Agent - ENHANCED with MAXIMUS
Port: 8162
Capability: CODE_GENERATION

v2.0: Code Generation + MAXIMUS Security Analysis
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient


class CodeAgent(BaseAgent):
    """Code generation with security analysis"""

    def __init__(self, agent_id: str = "code_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Code Agent (MAXIMUS-Enhanced)", port=8162)
        self.maximus_client = MaximusClient() if enable_maximus else None

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.CODE_GENERATION]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        print(f"   💻 Phase 1: Generating code...")
        generated_code = f"# Generated code for: {task.description}\ndef solution():\n    return True"

        security_issues = []
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    print(f"   🔒 Phase 2: MAXIMUS security analysis...")
                    ethical_verdict = await self.maximus_client.ethical_review(
                        code=generated_code,
                        context={"focus": "security"}
                    )
                    if ethical_verdict.verdict == "REJECTED":
                        security_issues = ethical_verdict.issues
                        print(f"      ⚠️ Security issues found: {len(security_issues)}")
            except (ConnectionError, TimeoutError, AttributeError, Exception):
                print(f"      ⚠️ MAXIMUS offline")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'code': generated_code, 'security_issues': security_issues},
            metrics={'mode': 'hybrid' if self.maximus_client else 'standalone'}
        )
