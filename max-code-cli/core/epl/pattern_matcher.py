"""
EPL Pattern Matcher - Fuzzy phrase matching and learning

Ported from Neuroshell learning engine with adaptations for EPL.

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
Test everything, keep what works - pattern matching learns from usage.

Features:
- Fuzzy phrase matching (similar inputs → same EPL)
- Pattern learning (frequency, success rate)
- Context-aware matching
- Confidence scoring
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class Pattern:
    """
    Learned pattern (Neuroshell-inspired)

    A pattern represents a learned mapping:
    Natural Language → EPL → Agent Action
    """
    id: str
    input: str                    # Natural language input
    epl: str                      # EPL translation
    intent_type: str              # Intent (plan, code, fix, etc)
    frequency: int = 1            # Times used
    success_rate: float = 1.0     # Success rate (0-1)
    last_used: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence: float = 1.0       # Pattern confidence

    def to_dict(self) -> Dict:
        """Serialize to dict"""
        return {
            'id': self.id,
            'input': self.input,
            'epl': self.epl,
            'intent_type': self.intent_type,
            'frequency': self.frequency,
            'success_rate': self.success_rate,
            'last_used': self.last_used,
            'created_at': self.created_at,
            'confidence': self.confidence,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Pattern':
        """Deserialize from dict"""
        return Pattern(
            id=data['id'],
            input=data['input'],
            epl=data['epl'],
            intent_type=data['intent_type'],
            frequency=data.get('frequency', 1),
            success_rate=data.get('success_rate', 1.0),
            last_used=data.get('last_used', datetime.utcnow().isoformat()),
            created_at=data.get('created_at', datetime.utcnow().isoformat()),
            confidence=data.get('confidence', 1.0),
        )


@dataclass
class MatchResult:
    """Result of pattern matching"""
    pattern: Optional[Pattern]
    similarity: float             # 0-1, how similar is input to pattern
    confidence: float             # 0-1, how confident are we
    matched: bool


class PatternMatcher:
    """
    Pattern Matcher for EPL

    Learns from usage and provides fuzzy matching.
    Inspired by Neuroshell's learning engine.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.patterns: Dict[str, Pattern] = {}
        self.storage_path = storage_path

        # Load patterns from disk if available
        if storage_path:
            self._load_patterns()

    def generate_pattern_id(self, input: str) -> str:
        """Generate unique pattern ID from input"""
        # Normalize and hash
        normalized = input.lower().strip()
        return hashlib.md5(normalized.encode(), usedforsecurity=False).hexdigest()[:16]

    def learn_pattern(
        self,
        input: str,
        epl: str,
        intent_type: str,
        success: bool = True
    ):
        """
        Learn a new pattern or update existing

        Args:
            input: Natural language input
            epl: EPL translation
            intent_type: Type of intent (plan, code, fix, etc)
            success: Whether this execution was successful
        """
        pattern_id = self.generate_pattern_id(input)

        if pattern_id in self.patterns:
            # Update existing pattern
            pattern = self.patterns[pattern_id]
            pattern.frequency += 1
            pattern.last_used = datetime.utcnow().isoformat()

            # Update success rate (exponential moving average)
            alpha = 0.3  # Weight for new observation
            if success:
                pattern.success_rate = alpha * 1.0 + (1 - alpha) * pattern.success_rate
            else:
                pattern.success_rate = alpha * 0.0 + (1 - alpha) * pattern.success_rate

            # Update confidence based on frequency and success rate
            # More frequent + higher success = higher confidence
            freq_score = min(pattern.frequency / 10.0, 1.0)  # Cap at 10 uses
            pattern.confidence = 0.5 * freq_score + 0.5 * pattern.success_rate

        else:
            # Create new pattern
            pattern = Pattern(
                id=pattern_id,
                input=input,
                epl=epl,
                intent_type=intent_type,
                frequency=1,
                success_rate=1.0 if success else 0.0,
                confidence=0.5,  # Start with medium confidence
            )
            self.patterns[pattern_id] = pattern

        # Persist to disk
        if self.storage_path:
            self._save_patterns()

    def find_similar_pattern(
        self,
        input: str,
        threshold: float = 0.7
    ) -> MatchResult:
        """
        Find most similar pattern to input

        Uses fuzzy matching (word overlap, Jaccard similarity)

        Args:
            input: Natural language input
            threshold: Minimum similarity threshold (0-1)

        Returns:
            MatchResult with best matching pattern
        """
        if not self.patterns:
            return MatchResult(
                pattern=None,
                similarity=0.0,
                confidence=0.0,
                matched=False
            )

        best_pattern = None
        best_similarity = 0.0

        # Normalize input
        input_words = set(input.lower().split())

        for pattern in self.patterns.values():
            # Calculate word overlap (Jaccard similarity)
            pattern_words = set(pattern.input.lower().split())

            intersection = input_words & pattern_words
            union = input_words | pattern_words

            if len(union) == 0:
                similarity = 0.0
            else:
                similarity = len(intersection) / len(union)

            # Boost similarity for high-confidence patterns
            boosted_similarity = similarity * (0.7 + 0.3 * pattern.confidence)

            if boosted_similarity > best_similarity:
                best_similarity = boosted_similarity
                best_pattern = pattern

        # Check threshold
        if best_similarity >= threshold and best_pattern:
            return MatchResult(
                pattern=best_pattern,
                similarity=best_similarity,
                confidence=best_pattern.confidence,
                matched=True
            )
        else:
            return MatchResult(
                pattern=None,
                similarity=best_similarity,
                confidence=0.0,
                matched=False
            )

    def get_top_patterns(self, n: int = 10) -> List[Pattern]:
        """Get top N most used patterns"""
        sorted_patterns = sorted(
            self.patterns.values(),
            key=lambda p: (p.frequency, p.confidence),
            reverse=True
        )
        return sorted_patterns[:n]

    def get_recent_patterns(self, n: int = 10) -> List[Pattern]:
        """Get N most recently used patterns"""
        sorted_patterns = sorted(
            self.patterns.values(),
            key=lambda p: p.last_used,
            reverse=True
        )
        return sorted_patterns[:n]

    def get_stats(self) -> Dict:
        """Get matcher statistics"""
        if not self.patterns:
            return {
                'total_patterns': 0,
                'avg_frequency': 0.0,
                'avg_success_rate': 0.0,
                'avg_confidence': 0.0,
            }

        total = len(self.patterns)
        avg_freq = sum(p.frequency for p in self.patterns.values()) / total
        avg_success = sum(p.success_rate for p in self.patterns.values()) / total
        avg_conf = sum(p.confidence for p in self.patterns.values()) / total

        return {
            'total_patterns': total,
            'avg_frequency': avg_freq,
            'avg_success_rate': avg_success,
            'avg_confidence': avg_conf,
        }

    # ========================================================================
    # PERSISTENCE
    # ========================================================================

    def _save_patterns(self):
        """Save patterns to disk (JSON)"""
        if not self.storage_path:
            return

        data = {
            'patterns': [p.to_dict() for p in self.patterns.values()]
        }

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_patterns(self):
        """Load patterns from disk"""
        if not self.storage_path:
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for pattern_data in data.get('patterns', []):
                    pattern = Pattern.from_dict(pattern_data)
                    self.patterns[pattern.id] = pattern
        except FileNotFoundError:
            # No patterns file yet
            pass


if __name__ == "__main__":
    # Demo
    logger.info("🎯 EPL Pattern Matcher Demo\n")
    matcher = PatternMatcher()

    # Learn some patterns
    patterns_to_learn = [
        ("Use tree of thoughts to analyze auth", "🌳📊🔒", "analyze"),
        ("Analyze authentication security", "📊🔒", "analyze"),
        ("Fix bug in auth module", "🐛→🔧 auth", "fix"),
        ("Fix authentication bug", "🐛🔒→🔧", "fix"),
        ("Generate code for login", "💻 login", "code"),
    ]

    logger.info("Learning patterns...")
    for input_text, epl, intent in patterns_to_learn:
        matcher.learn_pattern(input_text, epl, intent, success=True)
        logger.info(f"  ✓ Learned: '{input_text}' → {epl}")
    logger.info(f"\nTotal patterns learned: {len(matcher.patterns)}")
    # Test fuzzy matching
    print("\n" + "="*60)
    logger.info("Testing fuzzy matching:\n")
    test_inputs = [
        "Use ToT to analyze authentication",  # Similar to pattern 1
        "Analyze auth security",               # Similar to pattern 2
        "Fix the auth bug",                    # Similar to pattern 3
        "Create code for user login",          # Similar to pattern 5
        "Deploy to production",                # No similar pattern
    ]

    for test_input in test_inputs:
        logger.info(f"Input: '{test_input}'")
        result = matcher.find_similar_pattern(test_input, threshold=0.5)

        if result.matched:
            logger.info(f"  ✓ Match found!")
            logger.info(f"    Similar to: '{result.pattern.input}'")
            logger.info(f"    EPL: {result.pattern.epl}")
            logger.info(f"    Similarity: {result.similarity:.2%}")
            logger.info(f"    Confidence: {result.confidence:.2%}")
        else:
            logger.info(f"  ✗ No similar pattern found")
            logger.info(f"    Best similarity: {result.similarity:.2%}")
        print()

    # Stats
    print("="*60)
    logger.info("Pattern Statistics:\n")
    stats = matcher.get_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            logger.info(f"  {key}: {value:.2f}")
        else:
            logger.info(f"  {key}: {value}")
    print("\n" + "="*60)
    logger.info("Top Patterns:\n")
    for i, pattern in enumerate(matcher.get_top_patterns(3), 1):
        logger.info(f"  {i}. '{pattern.input}' → {pattern.epl}")
        logger.info(f"     Used {pattern.frequency}x, Success: {pattern.success_rate:.0%}")