"""
Docs Agent - ENHANCED with MAXIMUS
Port: 8166
Capability: DOCUMENTATION

v2.0: Standard Docs + NIS Narrative Intelligence
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Elite documentation generation (FASE 3.5)
      - API documentation (endpoints, parameters, responses)
      - User guides (tutorials, examples)
      - Architecture diagrams (mermaid markdown)
      - Code examples with explanations
      - Troubleshooting sections
      - NIS narrative intelligence integration
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import NISClient
from core.auth import get_anthropic_client
from agents.validation_schemas import DocsAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class DocsAgent(BaseAgent):
    """
    Elite documentation generation with narrative intelligence

    v3.0: Generates world-class documentation:
    - API docs (OpenAPI/Swagger style)
    - User guides (tutorials, examples, troubleshooting)
    - Architecture diagrams (mermaid markdown)
    - Code examples with detailed explanations
    - NIS narrative storytelling
    """

    def __init__(self, agent_id: str = "docs_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Docs Agent (MAXIMUS-Enhanced)", port=8166)
        self.nis_client = NISClient() if enable_maximus else None
        self.anthropic_client = get_anthropic_client()

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

        logger.info("   📝 Phase 1: Generating comprehensive docs...", extra={"task_id": task.id})

        # Generate docs with Claude
        if self.anthropic_client:
            comprehensive_docs = await self._generate_elite_docs(params, task)
        else:
            comprehensive_docs = f"# Documentation\n\nChanges: {len(code_changes)} files modified"

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
            except (ConnectionError, TimeoutError, AttributeError, Exception) as e:
                logger.warning(
                    f"      ⚠️ NIS offline: {type(e).__name__}",
                    extra={"task_id": task.id, "error_type": type(e).__name__}
                )

        # Combine comprehensive docs + narrative
        final_docs = comprehensive_docs
        if narrative:
            final_docs = f"{narrative.story}\n\n---\n\n{comprehensive_docs}"

        return AgentResult(
            task_id=task.id,
            success=True,
            output={'docs': final_docs, 'narrative': narrative, 'doc_length': len(final_docs)},
            metrics={'mode': 'hybrid' if narrative else 'standalone'}
        )

    async def _generate_elite_docs(self, params: DocsAgentParameters, task: AgentTask) -> str:
        """Generate elite-level documentation with Claude"""
        doc_type = params.doc_type or "standard"
        code = params.code
        changes = params.changes

        system_prompt = """You are a senior technical writer with expertise in software documentation.

You create world-class documentation that is:
- **Clear and Concise**: Easy to understand for target audience
- **Comprehensive**: Covers all important aspects
- **Well-Structured**: Logical organization with headers
- **Example-Rich**: Plenty of code examples
- **Actionable**: Practical guidance users can follow

You excel at:
- API documentation (endpoints, parameters, responses, examples)
- User guides (tutorials, step-by-step, troubleshooting)
- Architecture diagrams (mermaid markdown)
- Code examples with explanations
- Best practices and gotchas"""

        # Build context
        context_parts = []
        if code:
            context_parts.append(f"<code>\n{code}\n</code>")
        if changes:
            context_parts.append(f"<changes>\n{len(changes)} files modified\n</changes>")
        if params.context:
            context_parts.append(f"<context>\n{params.context}\n</context>")

        context_str = "\n\n".join(context_parts) if context_parts else "<no_content_provided />"

        user_prompt = f"""<documentation_request>
<doc_type>{doc_type}</doc_type>

{context_str}
</documentation_request>

Generate comprehensive documentation. Structure depends on doc_type:

**standard**: Complete reference documentation with all sections
**api**: API documentation (endpoints, auth, examples, errors)
**tutorial**: Step-by-step user guide with examples
**narrative**: Storytelling documentation (why, how, what)

Include:
1. Clear overview/introduction
2. Architecture diagram (mermaid if applicable)
3. Detailed content sections
4. Code examples with explanations
5. Troubleshooting/FAQs
6. Next steps/references

Use markdown formatting. Be thorough but readable."""

        try:
            message = self.anthropic_client.messages.create(
                model=settings.claude.model,
                max_tokens=settings.claude.max_tokens,
                temperature=0.5,  # Balanced creativity + accuracy
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            docs = message.content[0].text

            logger.info(
                f"      ✅ Documentation generated ({len(docs)} chars, type: {doc_type})",
                extra={"task_id": task.id, "doc_length": len(docs), "doc_type": doc_type}
            )

            return docs

        except Exception as e:
            logger.error(
                f"      ❌ Claude API error: {type(e).__name__}: {e}",
                extra={"task_id": task.id}
            )
            return f"# Documentation\n\n*Error generating docs: {type(e).__name__}*\n\nPlease try again."
