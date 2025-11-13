from agents.utils import get_anthropic_client
"""
Review Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8164
Capability: CODE_REVIEW

v2.0: Constitutional (P1-P6) + MAXIMUS Ethical Review (4 frameworks)
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Deep Claude-powered code review (FASE 3.5)
      - Security analysis (OWASP Top 10)
      - Performance optimization suggestions
      - Best practices validation
      - Architecture review
      - Maintainability score
v3.1: DETER-AGENT Guardian - OBRIGA Claude a obedecer Constitution
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient, DecisionFusion, MaximusCache
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import ReviewAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class ReviewAgent(BaseAgent):
    """
    Code review with Constitutional + Ethical + Technical analysis

    v3.0: Elite-level code review covering:
    - Security (OWASP Top 10, injection, XSS, auth)
    - Performance (algorithms, complexity, bottlenecks)
    - Best practices (SOLID, DRY, naming, documentation)
    - Architecture (coupling, cohesion, modularity)
    - Maintainability (complexity, readability, testability)
    - Constitutional AI (P1-P6 principles)
    - Ethical review (4 frameworks via MAXIMUS)
    """

    def __init__(
        self,
        agent_id: str = "review_agent",
        enable_maximus: bool = True,
        enable_guardian: bool = True,
        guardian_mode: GuardianMode = GuardianMode.BALANCED
    ):
        super().__init__(agent_id=agent_id, agent_name="Review Agent (Guardian + MAXIMUS)", port=8164)
        self.maximus_client = MaximusClient() if enable_maximus else None

        # Initialize DETER-AGENT Guardian (OBRIGA Claude a obedecer Constitution)
        self.guardian = Guardian(mode=guardian_mode) if enable_guardian else None
        if self.guardian:
            logger.info(
                f"   🛡️ Guardian initialized (mode: {guardian_mode.value})",
                extra={"guardian_mode": guardian_mode.value}
            )

        self.anthropic_client = get_anthropic_client()
        self.decision_fusion = DecisionFusion()
        self.cache = MaximusCache()

        # Constitutional Engine with REAL validators
        from core.constitutional.engine import ConstitutionalEngine
        self.constitutional_engine = ConstitutionalEngine()

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
                output={
                    'error': 'Invalid parameters',
                    'verdict': 'ERROR',
                    'details': e.errors()
                },
                metrics={'validation_failed': True}
            )

        # Guardian Pre-Check (OBRIGA Claude a obedecer Constitution)
        # ERGONOMICS FIX: Skip Guardian for vague/exploratory requests
        vague_keywords = ['make it better', 'improve', 'help', 'review this', 'check']
        is_vague_request = any(keyword in task.description.lower() for keyword in vague_keywords)
        code_is_simple_stub = code.strip().count('\n') < 3 and 'pass' in code

        if self.guardian and not (is_vague_request and code_is_simple_stub):
            logger.info("   🛡️ Phase 0: Guardian constitutional check...", extra={"task_id": task.id})

            action_context = {
                'action_type': 'code_review',
                'description': task.description,
                'code': code,
                'parameters': task.parameters,
            }

            guardian_decision = self.guardian.evaluate_action(action_context)

            if not guardian_decision.allowed:
                logger.error(f"   ❌ Guardian BLOCKED: {guardian_decision.reasoning}", extra={"task_id": task.id})
                return AgentResult(
                    task_id=task.id,
                    success=False,
                    output={
                        'error': 'Constitutional violation - Guardian blocked action',
                        'verdict': 'REJECTED',
                        'reasoning': guardian_decision.reasoning,
                        'recommendations': guardian_decision.recommendations,
                    },
                    metrics={'guardian_blocked': True}
                )

            logger.info(f"   ✅ Guardian approved", extra={"task_id": task.id})
        elif is_vague_request and code_is_simple_stub:
            logger.info("   🔍 Skipping Guardian for exploratory/vague request", extra={"task_id": task.id})

        # Phase 0.5: Syntax validation (fast pre-check)
        logger.info("   🔍 Phase 0.5: Syntax validation...", extra={"task_id": task.id})
        syntax_issues = []
        try:
            import ast
            ast.parse(code)
            logger.info("   ✅ Syntax valid", extra={"task_id": task.id})
        except SyntaxError as e:
            syntax_issues.append({
                'severity': 'high',
                'type': 'syntax_error',
                'message': f"Syntax error: {str(e)}",
                'line': e.lineno,
                'offset': e.offset,
                'text': e.text
            })
            logger.warning(f"   ⚠️ Syntax error detected: {e}", extra={"task_id": task.id})

        # Phase 1: Deep technical review with Claude
        claude_review = None
        if self.anthropic_client:
            logger.info("   🔍 Phase 1: Deep technical review...", extra={"task_id": task.id})
            claude_review = await self._deep_review_with_claude(code, params, task)

        # Phase 2: Constitutional review (P1-P6)
        logger.info("   🏛️ Phase 2: Constitutional review (P1-P6)...", extra={"task_id": task.id})
        constitutional_verdict = self.constitutional_engine.evaluate_all_principles({'code': code})

        ethical_verdict = None
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    logger.info("   ⚖️ Phase 3: MAXIMUS ethical review (4 frameworks)...", extra={"task_id": task.id})
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

        logger.info("   🔀 Phase 4: Fusion...", extra={"task_id": task.id})
        final_verdict = self.decision_fusion.fuse_review_verdicts(
            constitutional=constitutional_verdict,
            ethical=ethical_verdict
        )

        # Combine all reviews
        output = {
            'claude_review': claude_review,
            'constitutional': constitutional_verdict,
            'ethical': ethical_verdict,
            'syntax_issues': syntax_issues,  # Add syntax validation results
            'issues': syntax_issues,  # Alias for test compatibility
            'final_verdict': final_verdict.final_decision,
            'verdict': final_verdict.final_decision.get('verdict'),  # Shortcut for tests
            'reasoning': final_verdict.final_decision.get('reasoning'),
            'overall_score': self._calculate_overall_score(claude_review, constitutional_verdict, ethical_verdict),
            'ethical_score': self._calculate_ethical_score(ethical_verdict) if ethical_verdict else None
        }

        return AgentResult(
            task_id=task.id,
            success=final_verdict.final_decision.get('verdict') != 'REJECTED',
            output=output,
            metrics={'mode': 'hybrid' if ethical_verdict else 'standalone'}
        )

    async def _deep_review_with_claude(self, code: str, params: ReviewAgentParameters, task: AgentTask) -> Dict[str, Any]:
        """
        Perform elite-level code review with Claude.

        Reviews:
        - Security (OWASP Top 10)
        - Performance (complexity, algorithms)
        - Best practices (SOLID, DRY, documentation)
        - Architecture (coupling, modularity)
        - Maintainability (readability, testability)
        """
        review_type = params.review_type or "full"

        system_prompt = """You are a senior software architect and security expert with 20+ years of experience.

You conduct elite-level code reviews covering:

**Security** (OWASP Top 10):
- Injection (SQL, XSS, command injection)
- Authentication & authorization flaws
- Sensitive data exposure
- Security misconfiguration
- Cryptographic failures

**Performance**:
- Algorithm complexity (O(n) analysis)
- Database queries (N+1, missing indexes)
- Memory leaks
- Caching opportunities
- Bottlenecks

**Best Practices**:
- SOLID principles
- DRY (Don't Repeat Yourself)
- Clear naming conventions
- Comprehensive documentation
- Error handling
- Type safety

**Architecture**:
- Coupling and cohesion
- Modularity and reusability
- Design patterns
- Separation of concerns
- Scalability

**Maintainability**:
- Code complexity (cyclomatic)
- Readability
- Test coverage needs
- Technical debt

You provide actionable, specific recommendations with code examples."""

        user_prompt = f"""<code_review_request>
<code>
{code}
</code>

<review_type>{review_type}</review_type>
<context>{params.context or 'No additional context'}</context>
</code_review_request>

Perform a comprehensive code review. Structure your analysis as:

1. **Security Issues** (severity: critical/high/medium/low)
2. **Performance Concerns**
3. **Best Practice Violations**
4. **Architecture Recommendations**
5. **Maintainability Score** (0-10 with explanation)
6. **Summary** (top 3 priorities)

For each issue:
- Describe the problem
- Explain the impact
- Provide specific fix with code example
- Assign severity/priority

Be thorough but constructive."""

        try:
            message = self.anthropic_client.messages.create(
                model=settings.claude.model,
                max_tokens=settings.claude.max_tokens,
                temperature=0.4,  # Balanced for thorough analysis
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            response_text = message.content[0].text

            # Parse review into structured format
            review = {
                'raw_analysis': response_text,
                'review_type': review_type,
                'code_length': len(code),
                'timestamp': task.id
            }

            # Extract maintainability score if present
            import re
            score_match = re.search(r'Maintainability Score.*?(\d+)/10', response_text, re.IGNORECASE)
            if score_match:
                review['maintainability_score'] = int(score_match.group(1))

            # Count issues by severity
            review['critical_issues'] = len(re.findall(r'severity.*?critical', response_text, re.IGNORECASE))
            review['high_issues'] = len(re.findall(r'severity.*?high', response_text, re.IGNORECASE))
            review['medium_issues'] = len(re.findall(r'severity.*?medium', response_text, re.IGNORECASE))

            logger.info(
                f"      ✅ Review complete (maintainability: {review.get('maintainability_score', 'N/A')}/10)",
                extra={"task_id": task.id, "issues": review['critical_issues'] + review['high_issues']}
            )

            return review

        except Exception as e:
            logger.error(
                f"      ❌ Claude API error: {type(e).__name__}: {e}",
                extra={"task_id": task.id}
            )
            return {
                'error': f"{type(e).__name__}: {e}",
                'fallback': True
            }

    def _calculate_overall_score(self, claude_review: Dict, constitutional: Any, ethical: Any) -> float:
        """Calculate overall review score (0-1)"""
        scores = []

        # Claude maintainability (0-10 → 0-1)
        if claude_review and 'maintainability_score' in claude_review:
            scores.append(claude_review['maintainability_score'] / 10.0)

        # Constitutional average (already 0-1)
        if constitutional:
            # ConstitutionalResult has principle_scores dict (P1-P6)
            const_scores = list(constitutional.principle_scores.values())
            if const_scores:
                scores.append(sum(const_scores) / len(const_scores))

        # Ethical average (0-100 → 0-1)
        if ethical:
            eth_scores = [
                ethical.kantian_score / 100.0,
                ethical.virtue_score / 100.0,
                ethical.consequentialist_score / 100.0,
                ethical.principlism_score / 100.0
            ]
            scores.append(sum(eth_scores) / len(eth_scores))

        return sum(scores) / len(scores) if scores else 0.0

    def _calculate_ethical_score(self, ethical: Any) -> float:
        """Calculate ethical score (0-1) from EthicalVerdict"""
        if not ethical:
            return None
        
        # Average of all ethical framework scores (0-100 → 0-1)
        eth_scores = [
            ethical.kantian_score / 100.0,
            ethical.virtue_score / 100.0,
            ethical.consequentialist_score / 100.0,
            ethical.principlism_score / 100.0
        ]
        return sum(eth_scores) / len(eth_scores)
