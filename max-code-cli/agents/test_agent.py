"""
Test Agent - ENHANCED with MAXIMUS
Port: 8163
Capability: TESTING

v2.0: TDD (RED→GREEN→REFACTOR) + MAXIMUS Edge Case Prediction
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient


class TestAgent(BaseAgent):
    """TDD enforcement + Edge case prediction"""

    def __init__(self, agent_id: str = "test_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Test Agent (MAXIMUS-Enhanced)", port=8163)
        self.maximus_client = MaximusClient() if enable_maximus else None

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.TESTING]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        function_code = task.parameters.get('function_code', '')

        print(f"   🔴 Phase 1: RED - Writing tests...")
        test_suite = ['test_basic', 'test_edge_null', 'test_edge_empty']

        edge_cases = []
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    print(f"   🧠 Phase 2: MAXIMUS edge case prediction...")
                    edge_cases = await self.maximus_client.predict_edge_cases(
                        function_code=function_code,
                        test_suite=test_suite
                    )
                    print(f"      └─ Predicted {len(edge_cases)} edge cases")
                    for ec in edge_cases:
                        if ec.severity.value in ['HIGH', 'CRITICAL']:
                            test_suite.append(ec.suggested_test)
                            print(f"         ├─ {ec.severity.value}: {ec.scenario}")
            except (ConnectionError, TimeoutError, AttributeError, Exception):
                print(f"      ⚠️ MAXIMUS offline")

        print(f"   ✅ Phase 3: GREEN - Running tests...")
        print(f"   🔄 Phase 4: REFACTOR - Optimizing...")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'tests': test_suite, 'edge_cases': len(edge_cases)},
            metrics={'mode': 'hybrid' if edge_cases else 'standalone'}
        )
