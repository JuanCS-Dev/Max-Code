"""
Review Agent - ENHANCED with MAXIMUS
Port: 8164
Capability: CODE_REVIEW

v2.0: Constitutional (P1-P6) + MAXIMUS Ethical Review (4 frameworks)
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient, DecisionFusion, MaximusCache
from agents.validation_schemas import ReviewAgentParameters, validate_task_parameters
from config.logging_config import get_logger

logger = get_logger(__name__)


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
        # Validate input parameters
        try:
            params = validate_task_parameters('review', task.parameters or {})
            logger.info("   ✅ Parameters validated", extra={"task_id": task.id})
            code = params.code
        except ValidationError as e:
            logger.error(
                f"   ❌ Invalid parameters: {e}",
                extra={"task_id": task.id, "validation_errors": e.errors()}
            )
            return AgentResult(
                task_id=task.id,
                success=False,
                output={'error': 'Invalid parameters', 'details': e.errors()},
                metrics={'validation_failed': True}
            )

        logger.info("   🏛️ Phase 1: Constitutional review (P1-P6)...", extra={"task_id": task.id})
        constitutional_verdict = self.constitutional_engine.evaluate_all_principles({'code': code})

        ethical_verdict = None
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    logger.info("   ⚖️ Phase 2: MAXIMUS ethical review (4 frameworks)...", extra={"task_id": task.id})
                    ethical_verdict = await self.maximus_client.ethical_review(
                        code=code,
                        context=task.parameters.get('context', {})
                    )
                    logger.info(
                        f"      └─ Kantian: {ethical_verdict.kantian_score}/100, "
                        f"Virtue: {ethical_verdict.virtue_score}/100",
                        extra={
                            "task_id": task.id,
                            "kantian_score": ethical_verdict.kantian_score,
                            "virtue_score": ethical_verdict.virtue_score
                        }
                    )
            except (ConnectionError, TimeoutError, AttributeError, Exception) as e:
                logger.warning(
                    f"      ⚠️ MAXIMUS offline, using Constitutional only: {type(e).__name__}",
                    extra={"task_id": task.id, "error_type": type(e).__name__}
                )

        logger.info("   🔀 Phase 3: Fusion...", extra={"task_id": task.id})
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
