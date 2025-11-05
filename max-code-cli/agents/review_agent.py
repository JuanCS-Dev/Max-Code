"""
Review Agent - ENHANCED with MAXIMUS
Port: 8164
Capability: CODE_REVIEW

v2.0: Constitutional (P1-P6) + MAXIMUS Ethical Review (4 frameworks)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient, DecisionFusion, MaximusCache


class ReviewAgent(BaseAgent):
    """Code review with Constitutional + Ethical analysis"""

    def __init__(self, agent_id: str = "review_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Review Agent (MAXIMUS-Enhanced)", port=8164)
        self.maximus_client = MaximusClient() if enable_maximus else None
        self.decision_fusion = DecisionFusion()
        self.cache = MaximusCache()

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.CODE_REVIEW]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        code = task.parameters.get('code', '')

        print(f"   🏛️ Phase 1: Constitutional review (P1-P6)...")
        constitutional_verdict = self.constitutional_engine.evaluate_all_principles({'code': code})

        ethical_verdict = None
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    print(f"   ⚖️ Phase 2: MAXIMUS ethical review (4 frameworks)...")
                    ethical_verdict = await self.maximus_client.ethical_review(
                        code=code,
                        context=task.parameters.get('context', {})
                    )
                    print(f"      └─ Kantian: {ethical_verdict.kantian_score}/100, "
                          f"Virtue: {ethical_verdict.virtue_score}/100")
            except (ConnectionError, TimeoutError, AttributeError, Exception):
                print(f"      ⚠️ MAXIMUS offline, using Constitutional only")

        print(f"   🔀 Phase 3: Fusion...")
        final_verdict = self.decision_fusion.fuse_review_verdicts(
            constitutional=constitutional_verdict,
            ethical=ethical_verdict
        )

        return AgentResult(
            task_id=task.id,
            success=final_verdict.final_decision.get('verdict') != 'REJECTED',
            output=final_verdict.final_decision,
            metrics={'mode': 'hybrid' if ethical_verdict else 'standalone'}
        )
