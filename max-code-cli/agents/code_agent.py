from agents.utils import get_anthropic_client
"""
Code Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8162
Capability: CODE_GENERATION

v2.0: Code Generation + MAXIMUS Security Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Real Claude-powered code generation (FASE 3.5)
v3.1: DETER-AGENT Guardian integration (FASE 4.0)
      - Constitutional validation (P1-P6)
      - Deliberation quality check
      - Execution risk analysis
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Optional, AsyncIterator
import asyncio
from pydantic import ValidationError
from anthropic import Anthropic
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from core.deter_agent import Guardian, GuardianMode
from core.streaming import (
    ClaudeAgentIntegration,
    ThinkingPhase,
    EnhancedThinkingDisplay,
)
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

    def __init__(
        self,
        agent_id: str = "code_agent",
        enable_maximus: bool = True,
        enable_guardian: bool = True,
        guardian_mode: GuardianMode = GuardianMode.BALANCED
    ):
        super().__init__(agent_id=agent_id, agent_name="Code Agent (MAXIMUS + Guardian)", port=8162)
        self.maximus_client = MaximusClient() if enable_maximus else None

        # Initialize DETER-AGENT Guardian (controla comportamento Claude)
        self.guardian = Guardian(mode=guardian_mode) if enable_guardian else None
        if self.guardian:
            logger.info(
                f"   🛡️ Guardian initialized (mode: {guardian_mode.value})",
                extra={"guardian_mode": guardian_mode.value}
            )

        # Initialize Anthropic Claude client using centralized OAuth handler
        self.anthropic_client = get_anthropic_client()
        if self.anthropic_client:
            logger.info(
                f"   🧠 Claude API initialized (model: {settings.claude.model})",
                extra={"model": settings.claude.model}
            )
        
        # Initialize streaming integration
        self.streaming_integration = ClaudeAgentIntegration()

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

        # FASE 4.0: Guardian Pre-Check (antes de gerar código)
        if self.guardian:
            logger.info("   🛡️ Phase 0: Guardian pre-check...", extra={"task_id": task.id})

            action_context = {
                'action_type': 'code_generation',
                'description': task.description,
                'parameters': task.parameters,
                'language': params.language,
                'requirements': params.requirements,
            }

            guardian_decision = self.guardian.evaluate_action(action_context)

            if not guardian_decision.allowed:
                logger.error(
                    f"   ❌ Guardian BLOCKED action: {guardian_decision.reasoning}",
                    extra={"task_id": task.id, "reasoning": guardian_decision.reasoning}
                )
                return AgentResult(
                    task_id=task.id,
                    success=False,
                    output={
                        'error': 'Guardian blocked action',
                        'reasoning': guardian_decision.reasoning,
                        'constitutional_verdict': guardian_decision.constitutional_verdict,
                        'recommendations': guardian_decision.recommendations,
                    },
                    metrics={'guardian_blocked': True, 'mode': guardian_decision.mode.value}
                )

            logger.info(
                f"   ✅ Guardian approved: {guardian_decision.reasoning}",
                extra={"task_id": task.id}
            )

        logger.info("   💻 Phase 1: Generating code...", extra={"task_id": task.id})

        # Generate code using Claude API (if available) or fallback
        if self.anthropic_client:
            generated_code = await self._generate_with_claude(task, params)
        else:
            generated_code = self._generate_fallback(task, params)

        # FASE 4.0: Guardian Post-Check (depois de gerar código)
        if self.guardian:
            logger.info("   🛡️ Phase 1.5: Guardian post-check...", extra={"task_id": task.id})

            post_action_context = {
                'action_type': 'code_generation',
                'code': generated_code,
                'description': task.description,
                'parameters': task.parameters,
            }

            post_guardian_decision = self.guardian.evaluate_action(post_action_context)

            if not post_guardian_decision.allowed:
                logger.error(
                    f"   ❌ Guardian BLOCKED generated code: {post_guardian_decision.reasoning}",
                    extra={"task_id": task.id}
                )
                return AgentResult(
                    task_id=task.id,
                    success=False,
                    output={
                        'error': 'Guardian blocked generated code',
                        'reasoning': post_guardian_decision.reasoning,
                        'rejected_code': generated_code,
                        'execution_risks': post_guardian_decision.execution_risks,
                        'recommendations': post_guardian_decision.recommendations,
                    },
                    metrics={'guardian_post_blocked': True}
                )

            logger.info("   ✅ Guardian approved generated code", extra={"task_id": task.id})

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
Claude API unavailable - this is a functional template.
"""

def solution():
    """
    Implement: {task.description}
    
    This is a functional template. Replace with actual implementation.
    """
    # Step 1: Validate inputs
    # TODO: Add input validation
    
    # Step 2: Core logic
    # TODO: Implement main logic here
    result = None  # Replace with actual computation
    
    # Step 3: Return result
    return result

if __name__ == "__main__":
    output = solution()
    print(f"Result: {{output}}")
'''
        else:
            return f'''// {task.description}
// Generated by Max-Code (fallback mode)

function solution() {{
    // Step 1: Validate inputs
    // TODO: Add input validation
    
    // Step 2: Core logic
    // TODO: Implement main logic here
    const result = null; // Replace with actual computation
    
    // Step 3: Return result
    return result;
}}

// Main execution
const output = solution();
console.log("Result:", output);
'''
    
    async def execute_with_thinking(self, task: AgentTask) -> AgentResult:
        """
        Execute task with enhanced thinking display (streaming).
        
        This is the NEW execution method that shows real-time thinking process.
        Falls back to standard execute() if streaming unavailable.
        
        Args:
            task: Agent task to execute
        
        Returns:
            AgentResult with generated code
        """
        # Validate parameters
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
        
        # Guardian pre-check
        if self.guardian:
            logger.info("   🛡️ Guardian pre-check...", extra={"task_id": task.id})
            
            action_context = {
                'action_type': 'code_generation',
                'description': task.description,
                'parameters': task.parameters,
                'language': params.language,
                'requirements': params.requirements,
            }
            
            guardian_decision = self.guardian.evaluate_action(action_context)
            
            if not guardian_decision.allowed:
                logger.error(
                    f"   ❌ Guardian BLOCKED: {guardian_decision.reasoning}",
                    extra={"task_id": task.id}
                )
                return AgentResult(
                    task_id=task.id,
                    success=False,
                    output={
                        'error': 'Guardian blocked action',
                        'reasoning': guardian_decision.reasoning,
                        'recommendations': guardian_decision.recommendations,
                    },
                    metrics={'guardian_blocked': True}
                )
        
        # Build system prompt
        language = params.language or "python"
        context = params.context or ""
        requirements = params.requirements or []
        
        system_prompt = f"""You are an expert {language} developer with 15+ years of experience.

You write clean, maintainable, production-ready code following:
- SOLID principles
- Clear documentation
- Type hints/annotations
- Error handling
- Security best practices
- Performance optimization

You operate under VÉRTICE CONSTITUTION v3.0:
- P1: Complete code (no TODOs, placeholders)
- P2: Validate APIs (no hallucinations)
- P3: Critical thinking
- P4: Traceability
- P5: Systemic awareness
- P6: Token efficiency"""
        
        # Build prompt
        requirements_text = "\n".join([f"  - {r}" for r in requirements]) if requirements else ""
        context_text = f"\n\nContext:\n{context}" if context else ""
        
        prompt = f"""Generate {language} code for:
{task.description}
{context_text}

Requirements:
{requirements_text}

Provide production-ready, complete, functional code."""
        
        # Execute with streaming
        try:
            generated_code = await self.streaming_integration.execute_with_thinking(
                prompt=prompt,
                agent_name="code",
                system=system_prompt,
            )
            
            # Guardian post-check
            if self.guardian:
                logger.info("   🛡️ Guardian post-check...", extra={"task_id": task.id})
                
                post_context = {
                    'action_type': 'code_generation',
                    'code': generated_code,
                    'description': task.description,
                }
                
                post_decision = self.guardian.evaluate_action(post_context)
                
                if not post_decision.allowed:
                    logger.error(
                        f"   ❌ Guardian BLOCKED generated code: {post_decision.reasoning}",
                        extra={"task_id": task.id}
                    )
                    return AgentResult(
                        task_id=task.id,
                        success=False,
                        output={
                            'error': 'Guardian blocked generated code',
                            'reasoning': post_decision.reasoning,
                            'recommendations': post_decision.recommendations,
                        },
                        metrics={'guardian_post_blocked': True}
                    )
            
            # MAXIMUS security analysis (optional)
            security_issues = []
            if self.maximus_client:
                try:
                    if await self.maximus_client.health_check():
                        logger.info("   🔒 MAXIMUS security analysis...", extra={"task_id": task.id})
                        ethical_verdict = await self.maximus_client.ethical_review(
                            code=generated_code,
                            context={"focus": "security"}
                        )
                        if ethical_verdict.verdict == "REJECTED":
                            security_issues = ethical_verdict.issues
                            logger.warning(
                                f"      ⚠️ Security issues: {len(security_issues)}",
                                extra={"task_id": task.id}
                            )
                except Exception as e:
                    logger.warning(f"      ⚠️ MAXIMUS offline: {e}", extra={"task_id": task.id})
            
            return AgentResult(
                task_id=task.id,
                success=True,
                output={'code': generated_code, 'security_issues': security_issues},
                metrics={'mode': 'streaming', 'with_thinking': True}
            )
        
        except Exception as e:
            logger.error(
                f"   ❌ Streaming execution failed: {e}",
                extra={"task_id": task.id, "error": str(e)}
            )
            # Fallback to standard execution
            logger.info("   🔄 Falling back to standard execution...", extra={"task_id": task.id})
            return await self._execute_async(task)
    
    def execute_with_thinking_sync(self, task: AgentTask) -> AgentResult:
        """Sync wrapper for execute_with_thinking"""
        return asyncio.run(self.execute_with_thinking(task))
