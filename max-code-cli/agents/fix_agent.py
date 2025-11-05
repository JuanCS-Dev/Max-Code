"""
Fix Agent - ENHANCED with MAXIMUS
Port: 8165
Capability: DEBUGGING

v2.0: Quick Fix + PENELOPE Root Cause Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Real Claude-powered debugging (FASE 3.5)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import PENELOPEClient
from core.auth import get_anthropic_client
from agents.validation_schemas import FixAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class FixAgent(BaseAgent):
    """Bug fixing with root cause analysis"""

    def __init__(self, agent_id: str = "fix_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Fix Agent (MAXIMUS-Enhanced)", port=8165)
        self.penelope_client = PENELOPEClient() if enable_maximus else None
        self.anthropic_client = get_anthropic_client()

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.DEBUGGING]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        # Validate input parameters
        try:
            params = validate_task_parameters('fix', task.parameters or {})
            logger.info("   ✅ Parameters validated", extra={"task_id": task.id})
            broken_code = params.code
            error_trace = params.error
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

        logger.info("   🔧 Phase 1: Analyzing bug...", extra={"task_id": task.id})

        # Generate fix using Claude API
        if self.anthropic_client:
            fixed_code = await self._fix_with_claude(broken_code, error_trace, task)
        else:
            fixed_code = f"# Quick fix placeholder\n{broken_code}"

        healing = None
        if self.penelope_client:
            try:
                if await self.penelope_client.health_check():
                    logger.info("   🏥 Phase 2: PENELOPE root cause analysis...", extra={"task_id": task.id})
                    from core.maximus_integration.penelope_client import HealingContext
                    healing = await self.penelope_client.heal(
                        broken_code=broken_code,
                        error_trace=error_trace,
                        context=HealingContext()
                    )
                    logger.info(
                        f"      └─ Root cause: {healing.root_cause.primary_cause[:60]}...",
                        extra={"task_id": task.id, "root_cause": healing.root_cause.primary_cause}
                    )
                    if healing.fix_options:
                        best_fix = max(healing.fix_options, key=lambda f: f.confidence)
                        if best_fix.confidence > 0.8:  # High confidence PENELOPE fix
                            fixed_code = best_fix.code
                            logger.info(
                                f"         └─ Using PENELOPE fix (confidence: {best_fix.confidence:.2f})",
                                extra={"task_id": task.id, "confidence": best_fix.confidence}
                            )
            except (ConnectionError, TimeoutError, AttributeError, Exception) as e:
                logger.warning(
                    f"      ⚠️ PENELOPE offline: {type(e).__name__}",
                    extra={"task_id": task.id, "error_type": type(e).__name__}
                )

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'fixed_code': fixed_code, 'root_cause': healing.root_cause if healing else None},
            metrics={'mode': 'hybrid' if healing else 'standalone'}
        )

    async def _fix_with_claude(self, broken_code: str, error_trace: str, task: AgentTask) -> str:
        """Fix bug using Claude API with debugging expertise"""
        system_prompt = """You are an expert debugger and bug fixer with deep knowledge of Python, error analysis, and root cause identification.

You analyze bugs systematically:
- Read error traces carefully
- Identify root cause
- Propose minimal, surgical fix
- Explain reasoning
- Preserve original code structure"""

        user_prompt = f"""<bug_report>
<broken_code>
{broken_code}
</broken_code>

<error_trace>
{error_trace}
</error_trace>
</bug_report>

Analyze this bug and provide a fix. Follow these steps:

1. Identify the root cause of the error
2. Propose a minimal fix that addresses the root cause
3. Explain why this fix works
4. Preserve the original code structure as much as possible

Wrap the fixed code in <fixed_code> tags."""

        try:
            message = self.anthropic_client.messages.create(
                model=settings.claude.model,
                max_tokens=settings.claude.max_tokens,
                temperature=0.3,  # Lower temperature for precise fixes
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            response = message.content[0].text

            # Extract fixed code
            if "<fixed_code>" in response and "</fixed_code>" in response:
                start = response.index("<fixed_code>") + 12
                end = response.index("</fixed_code>")
                return response[start:end].strip()
            else:
                return response

        except Exception as e:
            logger.error(f"      ❌ Claude API error: {type(e).__name__}")
            return f"# Fix failed: {e}\n{broken_code}"
