"""
EPL Learning Mode - 3-Phase User Learning System

Helps users gradually learn EPL through progressive exposure.

Biblical Foundation:
"Porque a visão ainda está para o tempo determinado, mas ao fim falará" (Habacuque 2:3)
Learning takes time - patience brings fluency.

Learning Phases:
    Phase 1 - OBSERVATION (0-10 uses):
        User writes natural language
        System shows EPL translation
        Passive learning through observation

    Phase 2 - HINTS (11-30 uses):
        User can write either NL or EPL
        System provides hints when NL is used
        Active learning through suggestion

    Phase 3 - FLUENCY (31+ uses):
        User primarily writes EPL
        System only translates when needed
        Natural fluency achieved
"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class LearningPhase(Enum):
    """Phases of EPL learning"""
    OBSERVATION = "observation"     # 0-10 uses
    HINTS = "hints"                  # 11-30 uses
    FLUENCY = "fluency"              # 31+ uses


@dataclass
class UserProgress:
    """Track user's learning progress"""
    total_interactions: int = 0           # Total EPL interactions
    nl_to_epl_count: int = 0              # Times used NL → EPL
    epl_to_nl_count: int = 0              # Times used EPL → NL
    direct_epl_count: int = 0             # Times wrote EPL directly

    # Pattern usage
    patterns_learned: Dict[str, int] = field(default_factory=dict)  # pattern_id → usage count

    # Phase thresholds
    phase: LearningPhase = LearningPhase.OBSERVATION

    # Timestamps
    first_use: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_use: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        """Serialize to dict"""
        return {
            'total_interactions': self.total_interactions,
            'nl_to_epl_count': self.nl_to_epl_count,
            'epl_to_nl_count': self.epl_to_nl_count,
            'direct_epl_count': self.direct_epl_count,
            'patterns_learned': self.patterns_learned,
            'phase': self.phase.value,
            'first_use': self.first_use,
            'last_use': self.last_use,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'UserProgress':
        """Deserialize from dict"""
        return UserProgress(
            total_interactions=data.get('total_interactions', 0),
            nl_to_epl_count=data.get('nl_to_epl_count', 0),
            epl_to_nl_count=data.get('epl_to_nl_count', 0),
            direct_epl_count=data.get('direct_epl_count', 0),
            patterns_learned=data.get('patterns_learned', {}),
            phase=LearningPhase(data.get('phase', 'observation')),
            first_use=data.get('first_use', datetime.utcnow().isoformat()),
            last_use=data.get('last_use', datetime.utcnow().isoformat()),
        )


@dataclass
class LearningHint:
    """Hint provided to user during learning"""
    phase: LearningPhase
    message: str
    epl_translation: Optional[str] = None
    confidence: float = 1.0


class LearningMode:
    """
    EPL Learning Mode Manager

    Manages user progression through 3 phases:
    1. Observation (passive)
    2. Hints (active)
    3. Fluency (natural)

    Tracks usage patterns and provides appropriate hints.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path
        self.progress = UserProgress()

        # Load existing progress
        if storage_path:
            self._load_progress()

    def record_interaction(
        self,
        input_type: str,  # "natural_language" or "epl"
        pattern_id: Optional[str] = None
    ):
        """
        Record user interaction

        Args:
            input_type: Type of input ("natural_language" or "epl")
            pattern_id: Optional pattern ID if pattern was used
        """
        self.progress.total_interactions += 1
        self.progress.last_use = datetime.utcnow().isoformat()

        if input_type == "natural_language":
            self.progress.nl_to_epl_count += 1
        elif input_type == "epl":
            self.progress.direct_epl_count += 1

        # Track pattern usage
        if pattern_id:
            if pattern_id not in self.progress.patterns_learned:
                self.progress.patterns_learned[pattern_id] = 0
            self.progress.patterns_learned[pattern_id] += 1

        # Update phase
        self._update_phase()

        # Persist
        if self.storage_path:
            self._save_progress()

    def _update_phase(self):
        """Update learning phase based on usage"""
        total = self.progress.total_interactions

        if total <= 10:
            self.progress.phase = LearningPhase.OBSERVATION
        elif total <= 30:
            self.progress.phase = LearningPhase.HINTS
        else:
            self.progress.phase = LearningPhase.FLUENCY

    def get_hint(
        self,
        input_text: str,
        is_epl: bool,
        epl_translation: Optional[str] = None
    ) -> Optional[LearningHint]:
        """
        Get learning hint based on current phase

        Args:
            input_text: User input
            is_epl: Whether input is already EPL
            epl_translation: EPL translation (if input was NL)

        Returns:
            LearningHint if hint should be shown, None otherwise
        """
        phase = self.progress.phase

        if phase == LearningPhase.OBSERVATION:
            # Phase 1: Always show EPL translation when user writes NL
            if not is_epl and epl_translation:
                return LearningHint(
                    phase=phase,
                    message=f"💡 EPL: {epl_translation}",
                    epl_translation=epl_translation,
                    confidence=1.0,
                )

        elif phase == LearningPhase.HINTS:
            # Phase 2: Provide hints, encourage EPL usage
            if not is_epl and epl_translation:
                # Calculate EPL proficiency
                epl_ratio = self.progress.direct_epl_count / max(self.progress.total_interactions, 1)

                if epl_ratio < 0.3:
                    # Still using mostly NL, provide strong hint
                    return LearningHint(
                        phase=phase,
                        message=f"💡 Try using EPL: {epl_translation}",
                        epl_translation=epl_translation,
                        confidence=0.8,
                    )
                else:
                    # Getting better, just show translation
                    return LearningHint(
                        phase=phase,
                        message=f"✨ EPL: {epl_translation}",
                        epl_translation=epl_translation,
                        confidence=0.6,
                    )

        elif phase == LearningPhase.FLUENCY:
            # Phase 3: User is fluent, only hint if they ask
            if not is_epl and epl_translation:
                # Only show subtle hint
                return LearningHint(
                    phase=phase,
                    message=f"({epl_translation})",
                    epl_translation=epl_translation,
                    confidence=0.3,
                )

        return None

    def get_progress_summary(self) -> Dict:
        """Get user progress summary"""
        total = self.progress.total_interactions
        epl_ratio = self.progress.direct_epl_count / max(total, 1)

        return {
            'phase': self.progress.phase.value,
            'total_interactions': total,
            'epl_proficiency': f"{epl_ratio:.0%}",
            'patterns_learned': len(self.progress.patterns_learned),
            'most_used_patterns': self._get_top_patterns(5),
            'time_learning': self._calculate_learning_time(),
        }

    def _get_top_patterns(self, n: int = 5) -> list:
        """Get top N most used patterns"""
        sorted_patterns = sorted(
            self.progress.patterns_learned.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [
            {'pattern_id': pid, 'uses': count}
            for pid, count in sorted_patterns[:n]
        ]

    def _calculate_learning_time(self) -> str:
        """Calculate time spent learning"""
        try:
            first = datetime.fromisoformat(self.progress.first_use)
            last = datetime.fromisoformat(self.progress.last_use)
            delta = last - first

            if delta.days > 0:
                return f"{delta.days} days"
            elif delta.seconds > 3600:
                hours = delta.seconds // 3600
                return f"{hours} hours"
            elif delta.seconds > 60:
                minutes = delta.seconds // 60
                return f"{minutes} minutes"
            else:
                return f"{delta.seconds} seconds"
        except (ValueError, AttributeError, TypeError):
            return "unknown"

    # ========================================================================
    # PERSISTENCE
    # ========================================================================

    def _save_progress(self):
        """Save progress to disk"""
        if not self.storage_path:
            return

        with open(self.storage_path, 'w') as f:
            json.dump(self.progress.to_dict(), f, indent=2)

    def _load_progress(self):
        """Load progress from disk"""
        if not self.storage_path:
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.progress = UserProgress.from_dict(data)
        except FileNotFoundError:
            # No progress file yet
            pass


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("🎓 EPL Learning Mode Demo\n")

    learning = LearningMode()

    # Simulate user learning journey
    interactions = [
        # Phase 1: OBSERVATION (0-10)
        ("Use tree of thoughts", False, "🌳"),
        ("Fix bug in auth", False, "🐛🔒"),
        ("Review code", False, "👀💻"),
        ("Analyze security", False, "📊🔒"),
        ("Plan architecture", False, "🗺️"),
        ("Use ToT for analysis", False, "🌳📊"),
        ("Fix auth bug", False, "🐛🔒"),
        ("Review security", False, "👀🔒"),
        ("Analyze metrics", False, "📊"),
        ("Plan refactor", False, "🗺️🔄"),
        ("Generate tests", False, "🧪"),

        # Phase 2: HINTS (11-30) - user starts using EPL
        ("🌳📊", True, None),
        ("Analyze with ToT", False, "🌳📊"),
        ("🐛🔒", True, None),
        ("Fix the bug", False, "🐛🔧"),
        ("👀💻", True, None),
        ("Review code quality", False, "👀💻"),
        ("🌳", True, None),
        ("📊🔒", True, None),
        ("Analyze auth", False, "📊🔒"),
        ("🗺️", True, None),
        ("🧪", True, None),
        ("Test the API", False, "🧪"),
        ("🌳📊🔒", True, None),
        ("👑:🌳", True, None),
        ("Use Sophia with ToT", False, "👑:🌳"),
        ("🔴→🟢", True, None),
        ("Red to green", False, "🔴→🟢"),
        ("🌳→💡", True, None),
        ("ToT to ideas", False, "🌳→💡"),
        ("👑:🌳→💡→🏆", True, None),

        # Phase 3: FLUENCY (31+) - mostly EPL
        ("🌳📊", True, None),
        ("🐛→🔧", True, None),
        ("👑:🌳", True, None),
        ("🔴→🟢→🔄", True, None),
        ("👀💻", True, None),
        ("Occasionally natural language", False, "📊"),
        ("🌳→💡→🏆", True, None),
        ("🧪", True, None),
        ("🗺️🔄", True, None),
        ("📊🔒", True, None),
    ]

    print("Simulating user learning journey...\n")
    print("=" * 70)

    for i, (input_text, is_epl, epl_translation) in enumerate(interactions, 1):
        # Record interaction
        input_type = "epl" if is_epl else "natural_language"
        learning.record_interaction(input_type)

        # Get hint
        hint = learning.get_hint(input_text, is_epl, epl_translation)

        # Print progress at phase transitions
        if i in [1, 11, 31]:
            print(f"\n--- Interaction {i}: {learning.progress.phase.value.upper()} PHASE ---")

        # Show some examples
        if i in [1, 2, 3, 11, 12, 15, 31, 32, 36]:
            print(f"\nInteraction {i}:")
            print(f"  Input: {input_text}")
            print(f"  Type: {'EPL' if is_epl else 'Natural Language'}")
            if hint:
                print(f"  Hint: {hint.message}")

    # Final summary
    print("\n" + "=" * 70)
    print("LEARNING SUMMARY")
    print("=" * 70)

    summary = learning.get_progress_summary()
    print(f"\nPhase: {summary['phase'].upper()}")
    print(f"Total interactions: {summary['total_interactions']}")
    print(f"EPL proficiency: {summary['epl_proficiency']}")
    print(f"Time learning: {summary['time_learning']}")

    print("\n✨ Congratulations! You've achieved EPL fluency!")
