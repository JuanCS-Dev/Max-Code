"""
Explore Agent - Port 8161
Capability: EXPLORATION

v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from agents.validation_schemas import ExploreAgentParameters, validate_task_parameters
from config.logging_config import get_logger

logger = get_logger(__name__)


class ExploreAgent(BaseAgent):
    """Explora codebase"""

    def __init__(self, agent_id: str = "explore_agent"):
        super().__init__(agent_id=agent_id, agent_name="Explore Agent", port=8161)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.EXPLORATION]

    def execute(self, task: AgentTask) -> AgentResult:
        # Validate input parameters
        try:
            params = validate_task_parameters('explore', task.parameters or {})
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

        logger.info("   🔍 Exploring codebase...", extra={"task_id": task.id})
        # Placeholder: em produção, usar tools para explorar
        return AgentResult(task_id=task.id, success=True, output={'files': []})
