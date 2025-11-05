"""
Code Agent - ENHANCED with MAXIMUS
Port: 8162
Capability: CODE_GENERATION

v2.0: Code Generation + MAXIMUS Security Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Real Claude-powered code generation (FASE 3.5)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Optional
import asyncio
from pydantic import ValidationError
from anthropic import Anthropic
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from core.auth import get_anthropic_client
from agents.validation_schemas import CodeAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class CodeAgent(BaseAgent):
    """
    Code generation with security analysis

    v3.0: Real Claude-powered code generation using:
    - Chain of thought reasoning
    - XML-structured requests
    - System prompts for role assignment
    - Progressive implementation steps
    - MAXIMUS security analysis integration
    """

    def __init__(self, agent_id: str = "code_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Code Agent (MAXIMUS-Enhanced)", port=8162)
        self.maximus_client = MaximusClient() if enable_maximus else None

        # Initialize Anthropic Claude client using centralized OAuth handler
        self.anthropic_client = get_anthropic_client()
        if self.anthropic_client:
            logger.info(
                f"   🧠 Claude API initialized (model: {settings.claude.model})",
                extra={"model": settings.claude.model}
            )

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

        # Generate code using Claude API (if available) or fallback
        if self.anthropic_client:
            generated_code = await self._generate_with_claude(task, params)
        else:
            generated_code = self._generate_fallback(task, params)

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

    async def _generate_with_claude(self, task: AgentTask, params: CodeAgentParameters) -> str:
        """
        Generate code using Claude API with best practices:
        - Chain of thought reasoning
        - XML-structured requests
        - System prompts for expert role
        - Progressive implementation
        """
        language = params.language or "python"
        context = params.context or ""
        requirements = params.requirements or []

        logger.info(
            f"      🧠 Calling Claude API (language: {language})...",
            extra={"task_id": task.id, "language": language}
        )

        # Build system prompt (role assignment)
        system_prompt = f"""You are an expert {language} developer with 15+ years of experience.

You write clean, maintainable, production-ready code following best practices:
- SOLID principles
- Clear documentation
- Type hints (Python) / types (TypeScript)
- Error handling
- Security best practices
- Performance optimization

You always explain your reasoning before generating code."""

        # Build user prompt with XML structure
        requirements_xml = ""
        if requirements:
            requirements_xml = "<requirements>\n" + "\n".join([f"  - {r}" for r in requirements]) + "\n</requirements>\n\n"

        context_xml = ""
        if context:
            context_xml = f"<context>\n{context}\n</context>\n\n"

        user_prompt = f"""<code_request>
<language>{language}</language>
<task>{task.description}</task>

{context_xml}{requirements_xml}</code_request>

Please generate production-ready code for this task. Follow these steps:

1. First, explain your reasoning and approach (chain of thought)
2. Then generate the code
3. Include docstrings/comments
4. Add error handling where appropriate
5. Use type hints/annotations

Wrap the final code in <code> tags."""

        try:
            # Call Claude API
            message = self.anthropic_client.messages.create(
                model=settings.claude.model,
                max_tokens=settings.claude.max_tokens,
                temperature=settings.claude.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract response
            response_text = message.content[0].text

            # Extract code from <code> tags if present
            if "<code>" in response_text and "</code>" in response_text:
                start = response_text.index("<code>") + 6
                end = response_text.index("</code>")
                generated_code = response_text[start:end].strip()
            else:
                # Fallback: use entire response
                generated_code = response_text

            logger.info(
                f"      ✅ Code generated ({len(generated_code)} chars)",
                extra={"task_id": task.id, "code_length": len(generated_code)}
            )

            return generated_code

        except Exception as e:
            logger.error(
                f"      ❌ Claude API error: {type(e).__name__}: {e}",
                extra={"task_id": task.id, "error_type": type(e).__name__}
            )
            # Fallback on API error
            return self._generate_fallback(task, params)

    def _generate_fallback(self, task: AgentTask, params: CodeAgentParameters) -> str:
        """Fallback code generation (when Claude API unavailable)"""
        language = params.language or "python"

        logger.warning(
            "      ⚠️ Using fallback code generation",
            extra={"task_id": task.id}
        )

        if language == "python":
            return f'''"""
{task.description}

Generated by Max-Code (fallback mode)
"""

def solution():
    """
    TODO: Implement {task.description}

    This is a placeholder generated because Claude API is unavailable.
    Please implement the actual logic.
    """
    raise NotImplementedError("TODO: Implement this function")

if __name__ == "__main__":
    solution()
'''
        else:
            return f"// {task.description}\n// TODO: Implement this in {language}"
