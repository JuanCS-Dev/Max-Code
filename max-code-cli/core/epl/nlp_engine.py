"""
EPL NLP Engine - Natural Language Processing for EPL Translation

Ported from Neuroshell (vcli-go) with enhancements for emoji protocol.

Biblical Foundation:
"Toda palavra de Deus é pura" (Provérbios 30:5)
Every word is pure - NLP ensures semantic purity.

Components ported from Neuroshell:
- Typo correction (Levenshtein distance)
- Text normalization (accent removal, lowercase)
- Language detection (PT-BR, EN)
- Token classification (VERB, NOUN, etc)
- Intent recognition
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import unicodedata
import re
from config.logging_config import get_logger

logger = get_logger(__name__)


class Language(Enum):
    """Supported languages"""
    PT_BR = "pt-BR"
    EN = "en"


class IntentType(Enum):
    """Types of user intents"""
    PLAN = "plan"                    # Planning/architecture
    CODE = "code"                    # Code generation
    TEST = "test"                    # Testing
    FIX = "fix"                      # Bug fixing
    REVIEW = "review"                # Code review
    DOCS = "docs"                    # Documentation
    EXPLORE = "explore"              # Code exploration
    ANALYZE = "analyze"              # Analysis/metrics
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Recognized user intent"""
    type: IntentType
    confidence: float
    keywords: List[str]
    target: Optional[str] = None     # What to act on (e.g., "auth", "database")


class NLPEngine:
    """
    NLP Engine for EPL

    Ported from Neuroshell's robust NLP pipeline:
    1. Normalization (remove accents, lowercase)
    2. Typo correction (Levenshtein distance)
    3. Intent recognition (verb/noun patterns)
    4. Language detection (PT-BR vs EN)
    """

    def __init__(self):
        # Portuguese → English verb mapping
        self.verb_map = {
            # Neuroshell verbs
            "mostra": "show",
            "lista": "list",
            "deleta": "delete",
            "escala": "scale",
            "escalona": "scale",
            "cria": "create",
            "remove": "remove",
            "atualiza": "update",

            # EPL-specific verbs
            "usa": "use",
            "executa": "execute",
            "roda": "run",
            "analisa": "analyze",
            "conserta": "fix",
            "revisa": "review",
            "documenta": "document",
            "explora": "explore",
            "planeja": "plan",
            "testa": "test",
        }

        # Action verbs → Intent mapping
        self.intent_map = {
            # Planning
            "plan": IntentType.PLAN,
            "planeja": IntentType.PLAN,
            "design": IntentType.PLAN,
            "architect": IntentType.PLAN,
            "explore": IntentType.EXPLORE,
            "explora": IntentType.EXPLORE,

            # Code generation
            "code": IntentType.CODE,
            "generate": IntentType.CODE,
            "create": IntentType.CODE,
            "cria": IntentType.CODE,
            "implement": IntentType.CODE,

            # Testing
            "test": IntentType.TEST,
            "testa": IntentType.TEST,

            # Bug fixing
            "fix": IntentType.FIX,
            "conserta": IntentType.FIX,
            "repair": IntentType.FIX,
            "debug": IntentType.FIX,

            # Review
            "review": IntentType.REVIEW,
            "revisa": IntentType.REVIEW,
            "check": IntentType.REVIEW,
            "validate": IntentType.REVIEW,

            # Documentation
            "document": IntentType.DOCS,
            "documenta": IntentType.DOCS,
            "docs": IntentType.DOCS,

            # Analysis
            "analyze": IntentType.ANALYZE,
            "analisa": IntentType.ANALYZE,
            "measure": IntentType.ANALYZE,
            "metrics": IntentType.ANALYZE,
        }

        # Stop words (articles, prepositions)
        self.stop_words = {
            "a", "o", "os", "as", "um", "uma", "uns", "umas",
            "the", "a", "an",
            "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
            "of", "in", "on", "at", "to", "for", "with", "by",
            "para", "pra", "com", "sem",
            "e", "ou", "mas",
            "and", "or", "but",
        }

    def normalize(self, text: str) -> str:
        """
        Normalize text (Neuroshell-inspired)

        - Remove accents (ação → acao)
        - Lowercase
        - Trim whitespace
        """
        # Remove accents
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')

        # Lowercase
        text = text.lower()

        # Trim
        text = text.strip()

        return text

    def detect_language(self, text: str) -> Language:
        """
        Detect language (Neuroshell algorithm)

        Uses keyword heuristics
        """
        lower = text.lower()

        # Portuguese keywords
        pt_keywords = [
            "mostra", "lista", "deleta", "escala", "escalona",
            "usa", "executa", "roda", "analisa", "conserta",
            "do", "da", "dos", "das", "no", "na", "nos", "nas",
            "pra", "para", "com", "sem",
        ]

        for kw in pt_keywords:
            if kw in lower:
                return Language.PT_BR

        return Language.EN

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance (Neuroshell implementation)

        Used for typo correction
        """
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def correct_typo(self, word: str, dictionary: List[str], threshold: int = 2) -> Tuple[str, float]:
        """
        Correct typo using Levenshtein distance (Neuroshell algorithm)

        Returns:
            (corrected_word, confidence)
        """
        if word in dictionary:
            return word, 1.0

        best_match = word
        best_distance = float('inf')

        for candidate in dictionary:
            distance = self.levenshtein_distance(word, candidate)
            if distance < best_distance and distance <= threshold:
                best_distance = distance
                best_match = candidate

        if best_distance <= threshold:
            confidence = 1.0 - (best_distance / max(len(word), len(best_match)))
            return best_match, confidence
        else:
            return word, 1.0

    def map_verb_to_english(self, word: str, lang: Language) -> str:
        """Map Portuguese verb to English canonical form"""
        if lang == Language.PT_BR:
            return self.verb_map.get(word, word)
        return word

    def recognize_intent(self, text: str) -> Intent:
        """
        Recognize user intent from natural language

        Algorithm:
        1. Normalize text
        2. Split into words
        3. Remove stop words
        4. Map verbs to English
        5. Match against intent patterns
        """
        # Normalize
        normalized = self.normalize(text)

        # Detect language
        lang = self.detect_language(normalized)

        # Split words
        words = re.findall(r'\w+', normalized)

        # Remove stop words
        words = [w for w in words if w not in self.stop_words]

        # Map Portuguese verbs to English
        if lang == Language.PT_BR:
            words = [self.map_verb_to_english(w, lang) for w in words]

        # Find intent
        for word in words:
            if word in self.intent_map:
                intent_type = self.intent_map[word]

                # Extract target (usually after verb)
                target = None
                try:
                    verb_index = words.index(word)
                    if verb_index + 1 < len(words):
                        target = words[verb_index + 1]
                except ValueError:
                    pass

                return Intent(
                    type=intent_type,
                    confidence=0.9,
                    keywords=words,
                    target=target
                )

        # No intent found
        return Intent(
            type=IntentType.UNKNOWN,
            confidence=0.0,
            keywords=words,
            target=None
        )

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from text

        Removes stop words, normalizes
        """
        normalized = self.normalize(text)
        words = re.findall(r'\w+', normalized)
        keywords = [w for w in words if w not in self.stop_words]
        return keywords


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def normalize(text: str) -> str:
    """Convenience function for normalization"""
    engine = NLPEngine()
    return engine.normalize(text)


def detect_language(text: str) -> Language:
    """Convenience function for language detection"""
    engine = NLPEngine()
    return engine.detect_language(text)


def recognize_intent(text: str) -> Intent:
    """Convenience function for intent recognition"""
    engine = NLPEngine()
    return engine.recognize_intent(text)


if __name__ == "__main__":
    # Demo
    logger.info("🧠 EPL NLP Engine Demo\n")
    engine = NLPEngine()

    test_cases = [
        "Use tree of thoughts to analyze authentication",
        "Usa árvore de pensamentos para analisar autenticação",
        "Fix bug in auth module",
        "Conserta o bug no módulo de autenticação",
        "Generate code for user login",
        "Review security of API endpoints",
        "Test authentication flow",
    ]

    for test in test_cases:
        print(f"Input: \"{test}\"")

        # Normalize
        normalized = engine.normalize(test)
        logger.info(f"  Normalized: {normalized}")
        # Detect language
        lang = engine.detect_language(test)
        logger.info(f"  Language: {lang.value}")
        # Recognize intent
        intent = engine.recognize_intent(test)
        logger.info(f"  Intent: {intent.type.value} (confidence: {intent.confidence:.0%})")
        if intent.target:
            logger.info(f"  Target: {intent.target}")
        logger.info(f"  Keywords: {intent.keywords}")
        print()
