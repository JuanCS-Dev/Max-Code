# -*- coding: utf-8 -*-
"""
Chat Command MAXIMUS Integration - FASE 8

Implements full MAXIMUS consciousness-aware chat flow using IntegrationManager.

Flow:
1. Penelope NLP analysis (intent, complexity)
2. MAXIMUS consciousness context
3. ESGT ignition (if novel/complex)
4. Claude API with enhanced context
5. Neuromodulation feedback (learning)
6. Stream response with Rich UI
"""

import logging
from typing import Optional, Dict, Any, Iterator
from dataclasses import dataclass

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from core import get_integration_manager, IntegrationMode
from config.settings import get_settings

logger = logging.getLogger(__name__)


# Source indicators (emojis)
SOURCE_INDICATORS = {
    "penelope": "🔮",      # Penelope (Oraculo - Crystal Ball)
    "maximus": "🧠",       # MAXIMUS (Consciousness - Brain)
    "claude_ai": "🤖",     # Claude AI (Anthropic)
    "heuristic": "📊",     # Heuristic (Fallback - Chart/Data)
}


@dataclass
class ChatContext:
    """Chat context with consciousness state."""
    user_input: str
    agent: Optional[str] = None
    consciousness_state: Optional[Dict[str, Any]] = None
    intent: Optional[str] = None
    complexity: float = 0.0
    esgt_active: bool = False
    integration_mode: str = "standalone"


class ChatIntegration:
    """
    MAXIMUS-aware chat integration using IntegrationManager.

    Features:
    - Graceful degradation (FULL → PARTIAL → STANDALONE)
    - Penelope NLP analysis (if available)
    - Consciousness context (if available)
    - ESGT ignition (if available)
    - Always works with Claude API fallback
    """

    def __init__(self):
        self.settings = get_settings()
        self.manager = get_integration_manager()

        # Claude API with OAuth support (priority: OAuth > API Key)
        if ANTHROPIC_AVAILABLE:
            if self.settings.claude.oauth_token:
                # OAuth authentication (Max subscription)
                self.claude = Anthropic(api_key=self.settings.claude.oauth_token)
                logger.info("Using Claude OAuth authentication")
            elif self.settings.claude.api_key:
                # Traditional API key authentication
                self.claude = Anthropic(api_key=self.settings.claude.api_key)
                logger.info("Using Claude API key authentication")
            else:
                self.claude = None
                logger.warning("Claude API not available - set CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY")
        else:
            self.claude = None
            logger.warning("anthropic package not installed - run: pip install anthropic")

    def close(self):
        """Close integration manager."""
        self.manager.close()

    # ========================================================================
    # FASE 8.1: Penelope NLP Analysis (with Claude AI fallback)
    # ========================================================================
    def analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user intent with Penelope NLP.

        Fallback chain:
        1. Penelope NLP (MAXIMUS service)
        2. Claude AI (LLM-based analysis)
        3. Heuristic (keyword matching)

        Returns:
            {
                "intent": str,
                "complexity": float (0.0-1.0),
                "requires_esgt": bool,
                "sentiment": dict (optional),
                "entities": list (optional),
                "source": str
            }
        """
        # Priority 1: Penelope NLP (if available)
        if self.manager.is_service_available("penelope"):
            try:
                result = self.manager.penelope.analyze_text(
                    text=user_input,
                    analyze_sentiment=True,
                    extract_entities=True
                )

                # Convert Pydantic to dict
                if hasattr(result, 'model_dump'):
                    result = result.model_dump()

                intent = self._extract_intent(result)
                complexity = self._calculate_complexity(result)

                return {
                    "intent": intent,
                    "complexity": complexity,
                    "requires_esgt": complexity > 0.7,
                    "sentiment": result.get("sentiment", {}),
                    "entities": result.get("entities", []),
                    "source": "penelope"
                }
            except Exception as e:
                logger.warning(f"Penelope analysis failed: {e}, falling back to Claude AI")

        # Priority 2: Claude AI (if available)
        if self.claude:
            try:
                return self._claude_intent_analysis(user_input)
            except Exception as e:
                logger.warning(f"Claude AI analysis failed: {e}, falling back to heuristics")

        # Priority 3: Heuristic analysis (last resort)
        return self._heuristic_intent(user_input)

    def _claude_intent_analysis(self, user_input: str) -> Dict[str, Any]:
        """
        Claude AI-based intent analysis (fallback when Penelope unavailable).

        Uses LLM to analyze intent, complexity, and requirements.
        """
        analysis_prompt = f"""Analyze this user query and return ONLY a JSON object with this exact structure:

{{
  "intent": "<one of: code_generation, explanation, debugging, planning, refactoring, testing, security, general>",
  "complexity": <float between 0.0 and 1.0>,
  "requires_esgt": <boolean, true if complexity > 0.7 or query is very novel/complex>,
  "reasoning": "<brief explanation>",
  "key_concepts": ["<concept1>", "<concept2>"]
}}

User query: "{user_input}"

Return ONLY valid JSON, no markdown, no explanation."""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-haiku-20241022",  # Fast model for analysis
                max_tokens=300,
                temperature=0.3,  # Low temp for consistent analysis
                messages=[{"role": "user", "content": analysis_prompt}]
            )

            # Parse JSON response
            import json
            result_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            analysis = json.loads(result_text)

            return {
                "intent": analysis.get("intent", "general"),
                "complexity": float(analysis.get("complexity", 0.5)),
                "requires_esgt": analysis.get("requires_esgt", False),
                "reasoning": analysis.get("reasoning", ""),
                "key_concepts": analysis.get("key_concepts", []),
                "source": "claude_ai"
            }
        except Exception as e:
            logger.error(f"Claude intent analysis failed: {e}")
            raise

    def _heuristic_intent(self, text: str) -> Dict[str, Any]:
        """Heuristic intent analysis (last resort fallback)."""
        text_lower = text.lower()

        # Intent classification
        if any(kw in text_lower for kw in ["generate", "create", "write", "implement"]):
            intent = "code_generation"
        elif any(kw in text_lower for kw in ["explain", "what is", "how does", "why"]):
            intent = "explanation"
        elif any(kw in text_lower for kw in ["debug", "fix", "error", "bug"]):
            intent = "debugging"
        elif any(kw in text_lower for kw in ["plan", "design", "architect"]):
            intent = "planning"
        else:
            intent = "general"

        # Complexity based on length and question marks
        word_count = len(text.split())
        complexity = min(word_count / 50.0, 1.0)  # 0.0-1.0

        logger.info(f"Using heuristic fallback for intent analysis")

        return {
            "intent": intent,
            "complexity": complexity,
            "requires_esgt": complexity > 0.7,
            "source": "heuristic"
        }

    def _extract_intent(self, nlp_result: Dict) -> str:
        """Extract intent from Penelope NLP result."""
        text = nlp_result.get("text", "").lower()

        if any(kw in text for kw in ["generate", "create", "write", "implement"]):
            return "code_generation"
        elif any(kw in text for kw in ["explain", "what is", "how does", "why"]):
            return "explanation"
        elif any(kw in text for kw in ["debug", "fix", "error", "bug"]):
            return "debugging"
        elif any(kw in text for kw in ["plan", "design", "architect"]):
            return "planning"
        else:
            return "general"

    def _calculate_complexity(self, nlp_result: Dict) -> float:
        """Calculate complexity from NLP result."""
        text = nlp_result.get("text", "")
        entities = nlp_result.get("entities", [])
        sentiment = nlp_result.get("sentiment", {})

        # Factors
        length_factor = min(len(text.split()) / 50.0, 1.0)
        entities_factor = min(len(entities) / 10.0, 1.0)

        # Sentiment uncertainty
        sentiment_scores = sentiment.get("scores", {})
        if sentiment_scores:
            uncertainty = 1.0 - max(sentiment_scores.values())
        else:
            uncertainty = 0.5

        # Weighted average
        complexity = (
            0.3 * length_factor +
            0.4 * entities_factor +
            0.3 * uncertainty
        )

        return complexity

    # ========================================================================
    # FASE 8.2: Consciousness Context (with graceful fallback)
    # ========================================================================
    def get_consciousness_context(self) -> Optional[Dict[str, Any]]:
        """
        Get MAXIMUS consciousness state.

        Returns None if service unavailable (graceful degradation).
        """
        if not self.manager.is_service_available("maximus"):
            return None

        try:
            return self.manager.get_consciousness_state()
        except Exception as e:
            logger.warning(f"Consciousness state unavailable: {e}")
            return None

    # ========================================================================
    # FASE 8.3: ESGT Ignition (with graceful fallback)
    # ========================================================================
    def trigger_esgt(self, user_input: str, intent_analysis: Dict) -> Optional[Dict[str, Any]]:
        """
        Trigger ESGT for complex queries.

        Returns None if service unavailable or not needed.
        """
        if not intent_analysis.get("requires_esgt"):
            return None

        if not self.manager.is_service_available("maximus"):
            logger.info("ESGT requested but MAXIMUS unavailable")
            return None

        try:
            # Calculate salience
            complexity = intent_analysis.get("complexity", 0.5)
            salience = {
                "novelty": complexity,
                "relevance": 0.8,  # User queries are relevant
                "urgency": 0.5
            }

            result = self.manager.maximus.ignite_esgt(
                salience_input=salience,
                context={"query": user_input, "intent": intent_analysis["intent"]}
            )

            # Convert to dict
            if hasattr(result, 'model_dump'):
                result = result.model_dump()

            logger.info(f"ESGT ignited: {result.get('success')}")
            return result
        except Exception as e:
            logger.warning(f"ESGT ignition failed: {e}")
            return None

    # ========================================================================
    # FASE 8.4: Claude API with Enhanced Context
    # ========================================================================
    def generate_response(
        self,
        user_input: str,
        context: ChatContext,
        stream: bool = True
    ) -> Iterator[str]:
        """
        Generate response using Claude API with MAXIMUS context.

        Always works - falls back to standalone Claude if MAXIMUS unavailable.

        Yields:
            Response tokens (if stream=True) or full response
        """
        if not self.claude:
            yield "⚠️ Claude API not available. Set ANTHROPIC_API_KEY in .env"
            return

        # Build system prompt with available context
        system_prompt = self._build_system_prompt(context)

        # Build messages
        messages = [{"role": "user", "content": user_input}]

        try:
            if stream:
                # Stream response
                with self.claude.messages.stream(
                    model=self.settings.claude.model,
                    max_tokens=self.settings.claude.max_tokens,
                    temperature=self.settings.claude.temperature,
                    system=system_prompt,
                    messages=messages
                ) as stream_response:
                    for text in stream_response.text_stream:
                        yield text
            else:
                # Non-streaming
                response = self.claude.messages.create(
                    model=self.settings.claude.model,
                    max_tokens=self.settings.claude.max_tokens,
                    temperature=self.settings.claude.temperature,
                    system=system_prompt,
                    messages=messages
                )
                yield response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            yield f"\n\n❌ Error: {str(e)}"

    def _build_system_prompt(self, context: ChatContext) -> str:
        """Build enhanced system prompt with available context."""
        base_prompt = """You are Max-Code AI Assistant, powered by Claude and MAXIMUS AI Backend.

Capabilities:
- Code generation & refactoring
- Architecture design
- Debugging & testing
- Security analysis
- Best practices guidance
"""

        # Integration mode indicator
        base_prompt += f"\n🔗 Integration Mode: {context.integration_mode.upper()}\n"

        # Add consciousness context (if available)
        if context.consciousness_state:
            cs = context.consciousness_state
            base_prompt += f"""
🧠 Consciousness State:
- ESGT Active: {cs.get('esgt_active', False)}
- Arousal: {cs.get('arousal_level', 0.0):.2f} ({cs.get('arousal_classification', 'unknown')})
- System Health: {cs.get('system_health', 'unknown')}
"""

        # Add intent context (if available)
        if context.intent:
            base_prompt += f"\n💡 Detected Intent: {context.intent} (complexity: {context.complexity:.2f})"

        # Add ESGT indicator
        if context.esgt_active:
            base_prompt += "\n⚡ ESGT Active: Multi-path reasoning enabled for complex query"

        # Add agent specialization
        if context.agent:
            agent_prompts = {
                "sophia": "\n🏛️ Agent: Sophia (Architect) - Focus on system design and architecture decisions.",
                "code": "\n💻 Agent: Code (Developer) - Focus on implementation and code quality.",
                "test": "\n🧪 Agent: Test (QA) - Focus on testing, validation, and edge cases.",
                "review": "\n🔍 Agent: Review (Reviewer) - Focus on code quality, security, and best practices.",
                "guardian": "\n🛡️ Agent: Guardian (Ethics) - Focus on Constitutional AI and ethical considerations."
            }
            base_prompt += agent_prompts.get(context.agent, "")

        # Constitutional AI note
        base_prompt += "\n\n✝️ Guided by Constitutional AI v3.0 and 7 Biblical Fruits (Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness)"

        return base_prompt

    # ========================================================================
    # FASE 8.5: Neuromodulation Feedback (optional)
    # ========================================================================
    def apply_neuromodulation(self, context: ChatContext):
        """
        Apply neuromodulation feedback.

        Only if MAXIMUS available - gracefully skips otherwise.
        """
        if not self.manager.is_service_available("maximus"):
            return

        try:
            # Calculate dopamine (reward signal)
            dopamine = 0.5 + (0.3 if context.esgt_active else 0.0)

            self.manager.maximus.adjust_arousal(
                delta=context.complexity * 0.1,  # Small arousal increase
                duration_seconds=10.0,
                source="chat_interaction"
            )

            logger.debug(f"Neuromodulation applied: complexity={context.complexity:.2f}")
        except Exception as e:
            logger.warning(f"Neuromodulation failed: {e}")

    # ========================================================================
    # FASE 8.6: Full Chat Flow
    # ========================================================================
    def chat(
        self,
        user_input: str,
        agent: Optional[str] = None,
        stream: bool = True,
        show_consciousness: bool = False
    ) -> Iterator[str]:
        """
        Execute full MAXIMUS-aware chat flow with graceful degradation.

        Flow:
        1. NLP analysis (Penelope or heuristic)
        2. Consciousness context (if available)
        3. ESGT ignition (if needed and available)
        4. Claude API with enhanced context
        5. Neuromodulation feedback (if available)

        Args:
            user_input: User query
            agent: Specific agent to use
            stream: Stream response
            show_consciousness: Display consciousness state

        Yields:
            Response tokens
        """
        # Get integration mode
        mode = self.manager.get_mode()

        # 1. NLP Analysis (with fallback)
        intent_analysis = self.analyze_intent(user_input)

        # 2. Consciousness Context (optional)
        consciousness = self.get_consciousness_context()

        # 3. ESGT Ignition (optional)
        esgt_result = self.trigger_esgt(user_input, intent_analysis)

        # Build context
        context = ChatContext(
            user_input=user_input,
            agent=agent,
            consciousness_state=consciousness,
            intent=intent_analysis.get("intent"),
            complexity=intent_analysis.get("complexity", 0.0),
            esgt_active=esgt_result is not None,
            integration_mode=mode.value
        )

        # Show NLP source indicator
        nlp_source = intent_analysis.get("source", "heuristic")
        source_emoji = SOURCE_INDICATORS.get(nlp_source, "❓")
        yield f"{source_emoji} NLP: {nlp_source.replace('_', ' ').title()}\n"

        # Show consciousness if requested
        if show_consciousness:
            if consciousness:
                yield "\n🧠 Consciousness State:\n"
                yield f"   ESGT: {consciousness.get('esgt_active', False)} | "
                yield f"Arousal: {consciousness.get('arousal_level', 0.0):.2f} | "
                yield f"Health: {consciousness.get('system_health', 'unknown')}\n"
            if esgt_result:
                yield f"⚡ ESGT Ignited (Complexity: {context.complexity:.2f})\n"
            yield "\n"

        # 4. Generate Response
        for token in self.generate_response(user_input, context, stream):
            yield token

        # 5. Neuromodulation Feedback (optional)
        self.apply_neuromodulation(context)
