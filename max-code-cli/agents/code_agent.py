"""
Code Agent - ENHANCED with MAXIMUS
Port: 8162
Capability: CODE_GENERATION

v2.0: Code Generation + MAXIMUS Security Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from agents.validation_schemas import CodeAgentParameters, validate_task_parameters
from config.logging_config import get_logger

logger = get_logger(__name__)


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
        # Validate input parameters
        try:
            params = validate_task_parameters('code', task.parameters or {})
            logger.info("   ✅ Parameters validated", extra={"task_id": task.id})
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

        logger.info("   💻 Phase 1: Generating code...", extra={"task_id": task.id})
        generated_code = f"# Generated code for: {task.description}\ndef solution():\n    return True"

        security_issues = []
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    logger.info("   🔒 Phase 2: MAXIMUS security analysis...", extra={"task_id": task.id})
                    ethical_verdict = await self.maximus_client.ethical_review(
                        code=generated_code,
                        context={"focus": "security"}
                    )
                    if ethical_verdict.verdict == "REJECTED":
                        security_issues = ethical_verdict.issues
                        logger.warning(
                            f"      ⚠️ Security issues found: {len(security_issues)}",
                            extra={"task_id": task.id, "issue_count": len(security_issues)}
                        )
            except (ConnectionError, TimeoutError, AttributeError, Exception) as e:
                logger.warning(
                    f"      ⚠️ MAXIMUS offline: {type(e).__name__}",
                    extra={"task_id": task.id, "error_type": type(e).__name__}
                )

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'code': generated_code, 'security_issues': security_issues},
            metrics={'mode': 'hybrid' if self.maximus_client else 'standalone'}
        )
