"""
EPL Translator - Bidirectional Natural Language ↔ Emoji Translation

The heart of EPL: translates between natural language and emoji protocol.

Biblical Foundation:
"E o SENHOR desceu para ver a cidade e a torre que os filhos dos homens edificavam.
E disse: Eis que o povo é um, e todos têm uma mesma língua" (Gênesis 11:5-6)

EPL is our unified language - compression without loss of meaning.

Translation Pipeline:
    Natural Language → EPL:
    1. NLP normalization & intent recognition
    2. Pattern matching (fuzzy)
    3. Keyword → Emoji mapping
    4. Construct EPL expression

    EPL → Natural Language:
    1. Parse EPL (AST)
    2. Emoji → Concept mapping
    3. Construct readable sentence
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re

from .lexer import tokenize, is_epl_only, extract_emojis, extract_words, Token, TokenType
from .parser import parse, ASTNode, ASTNodeType
from .nlp_engine import NLPEngine, Intent, IntentType
from .pattern_matcher import PatternMatcher, MatchResult
from .vocabulary import (
    EMOJI_VOCABULARY,
    get_emoji_definition,
    get_emoji_by_alias,
    EmojiCategory,
    calculate_compression_ratio,
)


@dataclass
class TranslationResult:
    """Result of translation"""
    source: str                      # Original input
    target: str                      # Translated output
    confidence: float                # 0-1, confidence in translation
    compression_ratio: Optional[float] = None  # For NL→EPL
    source_type: str = "unknown"     # "natural_language" or "epl"
    target_type: str = "unknown"     # "natural_language" or "epl"
    intent: Optional[Intent] = None  # Recognized intent (for NL input)
    matched_pattern: Optional[str] = None  # If pattern was matched


class Translator:
    """
    EPL Translator

    Bidirectional translation between natural language and EPL.

    Features:
    - NL → EPL: Intent recognition + keyword mapping
    - EPL → NL: AST traversal + concept expansion
    - Pattern learning from usage
    - Fuzzy matching for similar inputs
    """

    def __init__(self, pattern_storage_path: Optional[str] = None):
        self.nlp = NLPEngine()
        self.pattern_matcher = PatternMatcher(storage_path=pattern_storage_path)

        # Build reverse mapping: concept → emoji
        self.concept_to_emoji: Dict[str, str] = {}
        for emoji, definition in EMOJI_VOCABULARY.items():
            # Primary meaning
            primary = definition.primary_meaning.lower()
            if primary not in self.concept_to_emoji:
                self.concept_to_emoji[primary] = emoji

            # Aliases
            for alias in definition.aliases:
                alias_lower = alias.lower()
                if alias_lower not in self.concept_to_emoji:
                    self.concept_to_emoji[alias_lower] = emoji

        # Special keywords for operators
        self.operator_keywords = {
            "then": "→",
            "followed by": "→",
            "leads to": "→",
            "and": "+",
            "with": "+",
            "or": "|",
            "alternative": "|",
        }

    # ========================================================================
    # TRANSLATION: Natural Language → EPL
    # ========================================================================

    def translate_to_epl(
        self,
        text: str,
        learn: bool = True
    ) -> TranslationResult:
        """
        Translate natural language to EPL

        Args:
            text: Natural language input
            learn: Whether to learn this pattern (default: True)

        Returns:
            TranslationResult with EPL translation

        Example:
            >>> translator = Translator()
            >>> result = translator.translate_to_epl("Use tree of thoughts to analyze auth")
            >>> print(result.target)
            "🌳📊🔒"
            >>> print(result.compression_ratio)
            0.75  # 75% compression
        """
        # Check if already EPL
        tokens = tokenize(text)
        if is_epl_only(tokens):
            return TranslationResult(
                source=text,
                target=text,
                confidence=1.0,
                source_type="epl",
                target_type="epl",
            )

        # Try pattern matching first (fuzzy)
        pattern_result = self.pattern_matcher.find_similar_pattern(text, threshold=0.7)
        if pattern_result.matched:
            # Found similar pattern, use its EPL
            epl = pattern_result.pattern.epl

            # Learn this usage
            if learn:
                self.pattern_matcher.learn_pattern(
                    text,
                    epl,
                    pattern_result.pattern.intent_type,
                    success=True
                )

            compression_ratio = calculate_compression_ratio(text, epl)

            return TranslationResult(
                source=text,
                target=epl,
                confidence=pattern_result.confidence,
                compression_ratio=compression_ratio,
                source_type="natural_language",
                target_type="epl",
                matched_pattern=pattern_result.pattern.input,
            )

        # No pattern match, translate from scratch
        intent = self.nlp.recognize_intent(text)
        keywords = self.nlp.extract_keywords(text)

        # Map keywords to emojis
        emojis: List[str] = []
        seen_emojis: set = set()
        for keyword in keywords:
            emoji = self._keyword_to_emoji(keyword, intent)
            if emoji and emoji not in seen_emojis:
                emojis.append(emoji)
                seen_emojis.add(emoji)

        # Construct EPL (deduplicated)
        epl = "".join(emojis)

        # Calculate confidence (based on keyword match rate)
        confidence = len(emojis) / max(len(keywords), 1)

        # Learn this pattern
        if learn and epl:
            self.pattern_matcher.learn_pattern(
                text,
                epl,
                intent.type.value,
                success=confidence > 0.5
            )

        compression_ratio = calculate_compression_ratio(text, epl) if epl else 0.0

        return TranslationResult(
            source=text,
            target=epl,
            confidence=confidence,
            compression_ratio=compression_ratio,
            source_type="natural_language",
            target_type="epl",
            intent=intent,
        )

    def _keyword_to_emoji(self, keyword: str, intent: Intent) -> Optional[str]:
        """
        Map keyword to emoji

        Uses:
        1. Direct concept mapping
        2. Intent-based mapping
        3. Alias matching
        """
        keyword_lower = keyword.lower()

        # Direct mapping
        if keyword_lower in self.concept_to_emoji:
            return self.concept_to_emoji[keyword_lower]

        # Intent-based mapping
        intent_emoji = self._intent_to_emoji(intent.type)
        if intent_emoji:
            return intent_emoji

        # Fuzzy alias matching (partial match)
        for concept, emoji in self.concept_to_emoji.items():
            if keyword_lower in concept or concept in keyword_lower:
                return emoji

        return None

    def _intent_to_emoji(self, intent_type: IntentType) -> Optional[str]:
        """Map intent type to emoji"""
        intent_map = {
            IntentType.PLAN: "🗺️",
            IntentType.CODE: "💻",
            IntentType.TEST: "🧪",
            IntentType.FIX: "🐛",
            IntentType.REVIEW: "👀",
            IntentType.DOCS: "📚",
            IntentType.EXPLORE: "🔍",
            IntentType.ANALYZE: "📊",
        }
        return intent_map.get(intent_type)

    # ========================================================================
    # TRANSLATION: EPL → Natural Language
    # ========================================================================

    def translate_to_natural_language(
        self,
        epl: str,
        verbose: bool = False
    ) -> TranslationResult:
        """
        Translate EPL to natural language

        Args:
            epl: EPL input (emojis)
            verbose: Whether to generate verbose explanation (default: False)

        Returns:
            TranslationResult with natural language translation

        Example:
            >>> translator = Translator()
            >>> result = translator.translate_to_natural_language("🌳📊🔒")
            >>> print(result.target)
            "Use Tree of Thoughts to analyze security"
        """
        # Check if already natural language
        tokens = tokenize(epl)
        if not is_epl_only(tokens):
            return TranslationResult(
                source=epl,
                target=epl,
                confidence=1.0,
                source_type="natural_language",
                target_type="natural_language",
            )

        # Parse EPL into AST
        ast = parse(epl)

        # Traverse AST and generate natural language
        nl = self._ast_to_natural_language(ast, verbose=verbose)

        return TranslationResult(
            source=epl,
            target=nl,
            confidence=1.0,  # EPL parsing is deterministic
            source_type="epl",
            target_type="natural_language",
        )

    def _ast_to_natural_language(
        self,
        node: ASTNode,
        verbose: bool = False
    ) -> str:
        """
        Convert AST to natural language

        Recursive traversal of AST
        """
        if node.node_type == ASTNodeType.PROGRAM:
            # Join all statements
            parts = []
            for child in node.children:
                nl = self._ast_to_natural_language(child, verbose)
                if nl:
                    parts.append(nl)
            return ". ".join(parts) if parts else ""

        elif node.node_type == ASTNodeType.AGENT_INVOKE:
            # Agent invocation: "Sophia: <action>"
            agent_meaning = node.meaning or node.value
            action = ""
            if node.children:
                action = self._ast_to_natural_language(node.children[0], verbose)

            if verbose:
                return f"{agent_meaning} performs: {action}"
            else:
                return f"{agent_meaning}: {action}"

        elif node.node_type == ASTNodeType.CHAIN:
            # Chain: "A then B then C"
            parts = []
            for child in node.children:
                if child.node_type == ASTNodeType.OPERATOR and child.value == "→":
                    parts.append("then")
                else:
                    nl = self._ast_to_natural_language(child, verbose)
                    parts.append(nl)
            return " ".join(parts)

        elif node.node_type == ASTNodeType.BINARY_OP:
            # Binary operator: "A and B" or "A or B"
            left = self._ast_to_natural_language(node.children[0], verbose) if len(node.children) > 0 else ""
            right = self._ast_to_natural_language(node.children[1], verbose) if len(node.children) > 1 else ""

            if node.value == "+":
                return f"{left} and {right}"
            elif node.value == "|":
                return f"{left} or {right}"
            else:
                return f"{left} {node.value} {right}"

        elif node.node_type == ASTNodeType.EMOJI:
            # Emoji terminal
            definition = get_emoji_definition(node.value)
            if definition:
                if verbose:
                    return f"{definition.primary_meaning} ({node.value})"
                else:
                    return definition.primary_meaning
            else:
                return node.value

        elif node.node_type == ASTNodeType.OPERATOR:
            # Operator terminal (shouldn't appear alone)
            return node.meaning or node.value

        else:
            # Default: join children
            parts = []
            for child in node.children:
                nl = self._ast_to_natural_language(child, verbose)
                if nl:
                    parts.append(nl)
            return " ".join(parts)

    # ========================================================================
    # UTILITY
    # ========================================================================

    def get_stats(self) -> Dict:
        """Get translator statistics"""
        return {
            "pattern_matcher": self.pattern_matcher.get_stats(),
            "vocabulary_size": len(EMOJI_VOCABULARY),
            "concept_mappings": len(self.concept_to_emoji),
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def translate_to_epl(text: str) -> str:
    """Convenience function: Natural language → EPL"""
    translator = Translator()
    result = translator.translate_to_epl(text)
    return result.target


def translate_to_nl(epl: str) -> str:
    """Convenience function: EPL → Natural language"""
    translator = Translator()
    result = translator.translate_to_natural_language(epl)
    return result.target


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("🔄 EPL Translator Demo\n")

    translator = Translator()

    # ========================================================================
    # TEST 1: Natural Language → EPL
    # ========================================================================
    print("="*70)
    print("TEST 1: Natural Language → EPL")
    print("="*70)

    nl_test_cases = [
        "Use tree of thoughts to analyze authentication",
        "Fix bug in security module",
        "Review code quality",
        "Generate tests for API",
        "Plan architecture for microservices",
    ]

    for i, test in enumerate(nl_test_cases, 1):
        print(f"\n{i}. Input: \"{test}\"")
        result = translator.translate_to_epl(test, learn=True)
        print(f"   EPL: {result.target}")
        print(f"   Confidence: {result.confidence:.0%}")
        if result.compression_ratio:
            print(f"   Compression: {result.compression_ratio:.0%}")
        if result.intent:
            print(f"   Intent: {result.intent.type.value}")

    # ========================================================================
    # TEST 2: EPL → Natural Language
    # ========================================================================
    print("\n" + "="*70)
    print("TEST 2: EPL → Natural Language")
    print("="*70)

    epl_test_cases = [
        "🌳📊🔒",
        "👑:🌳",
        "🔴→🟢→🔄",
        "👑:🌳→💡→🏆",
        "🐛→🔧",
    ]

    for i, test in enumerate(epl_test_cases, 1):
        print(f"\n{i}. Input: \"{test}\"")
        result = translator.translate_to_natural_language(test, verbose=False)
        print(f"   Natural Language: {result.target}")

        # Also show verbose
        result_verbose = translator.translate_to_natural_language(test, verbose=True)
        print(f"   Verbose: {result_verbose.target}")

    # ========================================================================
    # TEST 3: Fuzzy Pattern Matching
    # ========================================================================
    print("\n" + "="*70)
    print("TEST 3: Fuzzy Pattern Matching")
    print("="*70)

    # First, learn some patterns
    print("\nLearning patterns...")
    patterns = [
        ("Use tree of thoughts for analysis", "🌳📊"),
        ("Analyze using tree of thoughts", "🌳📊"),
        ("Fix authentication bug", "🐛🔒"),
    ]

    for nl, epl in patterns:
        translator.pattern_matcher.learn_pattern(nl, epl, "analyze", success=True)
        print(f"  ✓ Learned: '{nl}' → {epl}")

    # Now test similar inputs
    print("\nTesting similar inputs...")
    similar_inputs = [
        "Use ToT for analyzing data",           # Similar to pattern 1
        "Analyze with tree of thoughts",        # Similar to pattern 2
        "Fix the auth bug",                     # Similar to pattern 3
    ]

    for test in similar_inputs:
        print(f"\n  Input: \"{test}\"")
        result = translator.translate_to_epl(test, learn=False)
        print(f"    EPL: {result.target}")
        print(f"    Confidence: {result.confidence:.0%}")
        if result.matched_pattern:
            print(f"    Matched: '{result.matched_pattern}'")

    # ========================================================================
    # STATISTICS
    # ========================================================================
    print("\n" + "="*70)
    print("STATISTICS")
    print("="*70)
    stats = translator.get_stats()
    print(f"\nVocabulary size: {stats['vocabulary_size']} emojis")
    print(f"Concept mappings: {stats['concept_mappings']}")
    print(f"\nPattern Matcher:")
    for key, value in stats['pattern_matcher'].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
