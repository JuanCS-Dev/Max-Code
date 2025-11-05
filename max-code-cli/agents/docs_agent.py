"""
Docs Agent - ENHANCED with MAXIMUS
Port: 8166
Capability: DOCUMENTATION

v2.0: Standard Docs + NIS Narrative Intelligence
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import NISClient
from agents.validation_schemas import DocsAgentParameters, validate_task_parameters
from config.logging_config import get_logger

logger = get_logger(__name__)


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
        # Validate input parameters
        try:
            params = validate_task_parameters('docs', task.parameters or {})
            logger.info("   ✅ Parameters validated", extra={"task_id": task.id})
            code_changes = params.changes
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

        logger.info("   📝 Phase 1: Generating standard docs...", extra={"task_id": task.id})
        standard_docs = f"# Documentation\n\nChanges: {len(code_changes)} files modified"

        narrative = None
        if self.nis_client:
            try:
                if await self.nis_client.health_check():
                    logger.info("   📖 Phase 2: NIS narrative generation...", extra={"task_id": task.id})
                    from core.maximus_integration.nis_client import CodeChange, NarrativeStyle
                    narrative = await self.nis_client.generate_narrative(
                        changes=[CodeChange(**c) for c in code_changes] if code_changes else [],
                        style=NarrativeStyle.STORY,
                        context=task.parameters.get('context', {})
                    )
                    logger.info(
                        f"      └─ Generated: {narrative.title}",
                        extra={"task_id": task.id, "narrative_title": narrative.title}
                    )
                    standard_docs = f"{narrative.story}\n\n{standard_docs}"
            except (ConnectionError, TimeoutError, AttributeError, Exception) as e:
                logger.warning(
                    f"      ⚠️ NIS offline: {type(e).__name__}",
                    extra={"task_id": task.id, "error_type": type(e).__name__}
                )

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'docs': standard_docs, 'narrative': narrative},
            metrics={'mode': 'hybrid' if narrative else 'standalone'}
        )
