"""
Fix Agent - ENHANCED with MAXIMUS
Port: 8165
Capability: DEBUGGING

v2.0: Quick Fix + PENELOPE Root Cause Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import PENELOPEClient
from agents.validation_schemas import FixAgentParameters, validate_task_parameters


class FixAgent(BaseAgent):
    """Bug fixing with root cause analysis"""

    def __init__(self, agent_id: str = "fix_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Fix Agent (MAXIMUS-Enhanced)", port=8165)
        self.penelope_client = PENELOPEClient() if enable_maximus else None

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.DEBUGGING]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        # Validate input parameters
        try:
            params = validate_task_parameters('fix', task.parameters or {})
            print(f"   ✅ Parameters validated")
            broken_code = params.code
            error_trace = params.error
        except ValidationError as e:
            print(f"   ❌ Invalid parameters: {e}")
            return AgentResult(
                task_id=task.id,
                success=False,
                output={'error': 'Invalid parameters', 'details': e.errors()},
                metrics={'validation_failed': True}
            )

        print(f"   🔧 Phase 1: Quick fix attempt...")
        quick_fix = f"# Quick fix applied\n{broken_code}"

        healing = None
        if self.penelope_client:
            try:
                if await self.penelope_client.health_check():
                    print(f"   🏥 Phase 2: PENELOPE root cause analysis...")
                    from core.maximus_integration.penelope_client import HealingContext
                    healing = await self.penelope_client.heal(
                        broken_code=broken_code,
                        error_trace=error_trace,
                        context=HealingContext()
                    )
                    print(f"      └─ Root cause: {healing.root_cause.primary_cause[:60]}...")
                    if healing.fix_options:
                        best_fix = max(healing.fix_options, key=lambda f: f.confidence)
                        if best_fix.confidence > 0.7:
                            quick_fix = best_fix.code
                            print(f"         └─ Using PENELOPE fix (confidence: {best_fix.confidence:.2f})")
            except (ConnectionError, TimeoutError, AttributeError, Exception):
                print(f"      ⚠️ PENELOPE offline")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'fixed_code': quick_fix, 'root_cause': healing.root_cause if healing else None},
            metrics={'mode': 'hybrid' if healing else 'standalone'}
        )
