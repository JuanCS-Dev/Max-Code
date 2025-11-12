"""
Scientific Tests for EPL Learning Mode

Tests the 3-phase learning system that helps users learn EPL progressively.

Test Philosophy:
- Test REAL learning progression behavior
- Validate phase transitions and hint generation
- Test progress tracking and statistics
- Scientific rigor: reproducible, deterministic

Run:
    pytest tests/test_epl_learning_mode.py -v
"""

import pytest
import tempfile
import os
from datetime import datetime
from core.epl.learning_mode import (
    LearningMode,
    LearningPhase,
    UserProgress,
    LearningHint,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def learning_mode():
    """Create a learning mode instance without persistence"""
    return LearningMode()


@pytest.fixture
def learning_mode_with_storage():
    """Create a learning mode instance with temporary storage"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    # Write empty JSON to avoid load errors
    temp_file.write('{}')
    temp_file.close()

    learning = LearningMode(storage_path=temp_file.name)

    yield learning

    # Cleanup
    try:
        os.unlink(temp_file.name)
    except:
        pass


# ============================================================================
# TEST: UserProgress Structure
# ============================================================================

def test_user_progress_initialization():
    """Test UserProgress can be initialized"""
    progress = UserProgress()

    assert progress.total_interactions == 0
    assert progress.nl_to_epl_count == 0
    assert progress.epl_to_nl_count == 0
    assert progress.direct_epl_count == 0
    assert progress.phase == LearningPhase.OBSERVATION
    assert len(progress.patterns_learned) == 0


def test_user_progress_to_dict():
    """Test UserProgress serialization to dict"""
    progress = UserProgress()
    progress.total_interactions = 5
    progress.nl_to_epl_count = 3
    progress.direct_epl_count = 2

    progress_dict = progress.to_dict()

    assert progress_dict['total_interactions'] == 5
    assert progress_dict['nl_to_epl_count'] == 3
    assert progress_dict['direct_epl_count'] == 2
    assert progress_dict['phase'] == 'observation'


def test_user_progress_from_dict():
    """Test UserProgress deserialization from dict"""
    data = {
        'total_interactions': 10,
        'nl_to_epl_count': 6,
        'direct_epl_count': 4,
        'phase': 'hints',
    }

    progress = UserProgress.from_dict(data)

    assert progress.total_interactions == 10
    assert progress.nl_to_epl_count == 6
    assert progress.direct_epl_count == 4
    assert progress.phase == LearningPhase.HINTS


# ============================================================================
# TEST: LearningHint Structure
# ============================================================================

def test_learning_hint_structure():
    """Test LearningHint dataclass"""
    hint = LearningHint(
        phase=LearningPhase.OBSERVATION,
        message="💡 EPL: 🌳",
        epl_translation="🌳",
        confidence=0.95
    )

    assert hint.phase == LearningPhase.OBSERVATION
    assert hint.message == "💡 EPL: 🌳"
    assert hint.epl_translation == "🌳"
    assert hint.confidence == 0.95


# ============================================================================
# TEST: LearningMode Initialization
# ============================================================================

def test_learning_mode_initialization(learning_mode):
    """Test LearningMode can be initialized"""
    assert learning_mode is not None
    assert hasattr(learning_mode, 'progress')
    assert learning_mode.progress.phase == LearningPhase.OBSERVATION


def test_learning_mode_with_storage_path(learning_mode_with_storage):
    """Test LearningMode with storage path"""
    assert learning_mode_with_storage.storage_path is not None
    assert os.path.exists(learning_mode_with_storage.storage_path)


# ============================================================================
# TEST: Recording Interactions
# ============================================================================

def test_record_natural_language_interaction(learning_mode):
    """Test recording natural language interaction"""
    initial_count = learning_mode.progress.total_interactions

    learning_mode.record_interaction("natural_language")

    assert learning_mode.progress.total_interactions == initial_count + 1
    assert learning_mode.progress.nl_to_epl_count == 1
    assert learning_mode.progress.direct_epl_count == 0


def test_record_epl_interaction(learning_mode):
    """Test recording EPL interaction"""
    initial_count = learning_mode.progress.total_interactions

    learning_mode.record_interaction("epl")

    assert learning_mode.progress.total_interactions == initial_count + 1
    assert learning_mode.progress.direct_epl_count == 1
    assert learning_mode.progress.nl_to_epl_count == 0


def test_record_interaction_with_pattern(learning_mode):
    """Test recording interaction with pattern ID"""
    learning_mode.record_interaction("epl", pattern_id="pattern_123")

    assert "pattern_123" in learning_mode.progress.patterns_learned
    assert learning_mode.progress.patterns_learned["pattern_123"] == 1


def test_record_multiple_same_pattern(learning_mode):
    """Test recording multiple uses of same pattern"""
    learning_mode.record_interaction("epl", pattern_id="pattern_abc")
    learning_mode.record_interaction("epl", pattern_id="pattern_abc")
    learning_mode.record_interaction("epl", pattern_id="pattern_abc")

    assert learning_mode.progress.patterns_learned["pattern_abc"] == 3


# ============================================================================
# TEST: Phase Progression
# ============================================================================

def test_phase_1_observation_range(learning_mode):
    """Test Phase 1 (OBSERVATION) for interactions 0-10"""
    # Record 10 interactions
    for i in range(10):
        learning_mode.record_interaction("natural_language")

    # Should still be in OBSERVATION phase
    assert learning_mode.progress.phase == LearningPhase.OBSERVATION


def test_phase_2_hints_transition(learning_mode):
    """Test transition to Phase 2 (HINTS) at 11 interactions"""
    # Record 11 interactions
    for i in range(11):
        learning_mode.record_interaction("natural_language")

    # Should transition to HINTS phase
    assert learning_mode.progress.phase == LearningPhase.HINTS


def test_phase_2_hints_range(learning_mode):
    """Test Phase 2 (HINTS) for interactions 11-30"""
    # Record 30 interactions
    for i in range(30):
        learning_mode.record_interaction("natural_language")

    # Should still be in HINTS phase
    assert learning_mode.progress.phase == LearningPhase.HINTS


def test_phase_3_fluency_transition(learning_mode):
    """Test transition to Phase 3 (FLUENCY) at 31 interactions"""
    # Record 31 interactions
    for i in range(31):
        learning_mode.record_interaction("epl")

    # Should transition to FLUENCY phase
    assert learning_mode.progress.phase == LearningPhase.FLUENCY


# ============================================================================
# TEST: Hint Generation - Phase 1 (OBSERVATION)
# ============================================================================

def test_phase_1_hint_for_nl_input(learning_mode):
    """Test Phase 1 shows hint for natural language input"""
    # Start in Phase 1
    assert learning_mode.progress.phase == LearningPhase.OBSERVATION

    hint = learning_mode.get_hint(
        input_text="tree of thoughts",
        is_epl=False,
        epl_translation="🌳"
    )

    # Should show hint
    assert hint is not None
    assert isinstance(hint, LearningHint)
    assert hint.phase == LearningPhase.OBSERVATION
    assert "🌳" in hint.message


def test_phase_1_no_hint_for_epl_input(learning_mode):
    """Test Phase 1 doesn't show hint for EPL input"""
    hint = learning_mode.get_hint(
        input_text="🌳",
        is_epl=True,
        epl_translation=None
    )

    # Should not show hint (user already using EPL)
    assert hint is None


# ============================================================================
# TEST: Hint Generation - Phase 2 (HINTS)
# ============================================================================

def test_phase_2_hint_with_low_epl_proficiency(learning_mode):
    """Test Phase 2 shows stronger hints with low EPL proficiency"""
    # Advance to Phase 2 (11 interactions, mostly NL)
    for i in range(11):
        learning_mode.record_interaction("natural_language")

    assert learning_mode.progress.phase == LearningPhase.HINTS

    hint = learning_mode.get_hint(
        input_text="tree of thoughts",
        is_epl=False,
        epl_translation="🌳"
    )

    # Should show hint
    assert hint is not None
    assert hint.phase == LearningPhase.HINTS
    assert "Try using EPL" in hint.message or "🌳" in hint.message


def test_phase_2_hint_with_high_epl_proficiency(learning_mode):
    """Test Phase 2 shows softer hints with high EPL proficiency"""
    # Advance to Phase 2 with more EPL usage
    for i in range(11):
        if i < 5:
            learning_mode.record_interaction("natural_language")
        else:
            learning_mode.record_interaction("epl")

    assert learning_mode.progress.phase == LearningPhase.HINTS

    hint = learning_mode.get_hint(
        input_text="tree of thoughts",
        is_epl=False,
        epl_translation="🌳"
    )

    # Should still show hint but softer
    assert hint is not None
    assert hint.phase == LearningPhase.HINTS


# ============================================================================
# TEST: Hint Generation - Phase 3 (FLUENCY)
# ============================================================================

def test_phase_3_subtle_hint(learning_mode):
    """Test Phase 3 shows only subtle hints"""
    # Advance to Phase 3
    for i in range(31):
        learning_mode.record_interaction("epl")

    assert learning_mode.progress.phase == LearningPhase.FLUENCY

    hint = learning_mode.get_hint(
        input_text="tree of thoughts",
        is_epl=False,
        epl_translation="🌳"
    )

    # Should show subtle hint
    assert hint is not None
    assert hint.phase == LearningPhase.FLUENCY
    # Hint should be parenthetical or subtle
    assert "(" in hint.message or hint.confidence < 0.5


# ============================================================================
# TEST: Progress Summary
# ============================================================================

def test_get_progress_summary(learning_mode):
    """Test getting progress summary"""
    # Record some interactions
    learning_mode.record_interaction("natural_language")
    learning_mode.record_interaction("epl")
    learning_mode.record_interaction("epl")

    summary = learning_mode.get_progress_summary()

    assert 'phase' in summary
    assert 'total_interactions' in summary
    assert 'epl_proficiency' in summary
    assert 'patterns_learned' in summary

    assert summary['total_interactions'] == 3
    assert summary['phase'] == 'observation'


def test_progress_summary_epl_proficiency_calculation(learning_mode):
    """Test EPL proficiency calculation in progress summary"""
    # 2 NL, 8 EPL = 80% proficiency
    for i in range(2):
        learning_mode.record_interaction("natural_language")
    for i in range(8):
        learning_mode.record_interaction("epl")

    summary = learning_mode.get_progress_summary()

    # 8/10 = 80%
    assert "80%" in summary['epl_proficiency']


def test_progress_summary_includes_learning_time(learning_mode):
    """Test progress summary includes learning time"""
    learning_mode.record_interaction("epl")

    summary = learning_mode.get_progress_summary()

    assert 'time_learning' in summary
    assert summary['time_learning'] is not None


# ============================================================================
# TEST: Pattern Tracking
# ============================================================================

def test_track_most_used_patterns(learning_mode):
    """Test tracking most used patterns"""
    # Use different patterns
    learning_mode.record_interaction("epl", pattern_id="pattern_a")
    learning_mode.record_interaction("epl", pattern_id="pattern_a")
    learning_mode.record_interaction("epl", pattern_id="pattern_a")
    learning_mode.record_interaction("epl", pattern_id="pattern_b")
    learning_mode.record_interaction("epl", pattern_id="pattern_b")
    learning_mode.record_interaction("epl", pattern_id="pattern_c")

    summary = learning_mode.get_progress_summary()

    # Should have top patterns
    assert 'most_used_patterns' in summary
    top_patterns = summary['most_used_patterns']

    # pattern_a should be first (3 uses)
    assert len(top_patterns) >= 1
    assert top_patterns[0]['pattern_id'] == 'pattern_a'
    assert top_patterns[0]['uses'] == 3


# ============================================================================
# TEST: Persistence (Save/Load)
# ============================================================================

def test_save_progress_to_file(learning_mode_with_storage):
    """Test saving progress to file"""
    # Record some interactions
    learning_mode_with_storage.record_interaction("epl")
    learning_mode_with_storage.record_interaction("epl")

    # Progress should be saved
    assert os.path.exists(learning_mode_with_storage.storage_path)

    # File should contain data
    file_size = os.path.getsize(learning_mode_with_storage.storage_path)
    assert file_size > 0


def test_load_progress_from_file():
    """Test loading progress from file"""
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.write('{"total_interactions": 15, "phase": "hints"}')
    temp_file.close()

    try:
        # Load progress
        learning = LearningMode(storage_path=temp_file.name)

        # Should have loaded progress
        assert learning.progress.total_interactions == 15
        assert learning.progress.phase == LearningPhase.HINTS
    finally:
        os.unlink(temp_file.name)


def test_persistence_across_sessions():
    """Test progress persists across sessions"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.write('{}')  # Write empty JSON
    temp_file.close()

    try:
        # Session 1: record interactions
        learning1 = LearningMode(storage_path=temp_file.name)
        learning1.record_interaction("epl")
        learning1.record_interaction("epl")

        # Session 2: load and continue
        learning2 = LearningMode(storage_path=temp_file.name)

        # Should have loaded previous progress
        assert learning2.progress.total_interactions == 2
        assert learning2.progress.direct_epl_count == 2

    finally:
        try:
            os.unlink(temp_file.name)
        except:
            pass


# ============================================================================
# TEST: Edge Cases
# ============================================================================

def test_get_hint_without_epl_translation(learning_mode):
    """Test getting hint without EPL translation"""
    hint = learning_mode.get_hint(
        input_text="some text",
        is_epl=False,
        epl_translation=None
    )

    # Should not crash (might return None)
    assert hint is None or isinstance(hint, LearningHint)


def test_record_interaction_invalid_type(learning_mode):
    """Test recording interaction with invalid type"""
    # Should handle gracefully (or increment total only)
    initial = learning_mode.progress.total_interactions

    learning_mode.record_interaction("unknown_type")

    # Total should increment
    assert learning_mode.progress.total_interactions == initial + 1


def test_learning_mode_without_storage_doesnt_crash(learning_mode):
    """Test learning mode without storage doesn't crash"""
    # Should work fine without persistence
    learning_mode.record_interaction("epl")
    learning_mode.record_interaction("natural_language")

    assert learning_mode.progress.total_interactions == 2


# ============================================================================
# TEST: Realistic Learning Journey
# ============================================================================

def test_realistic_learning_journey(learning_mode):
    """Test realistic user learning journey through all phases"""
    # Phase 1: OBSERVATION (0-10) - User writes NL, sees EPL
    for i in range(10):
        learning_mode.record_interaction("natural_language")

    assert learning_mode.progress.phase == LearningPhase.OBSERVATION

    # Phase 2: HINTS (11-30) - User starts mixing NL and EPL
    for i in range(20):
        if i % 2 == 0:
            learning_mode.record_interaction("natural_language")
        else:
            learning_mode.record_interaction("epl")

    assert learning_mode.progress.phase == LearningPhase.HINTS

    # Phase 3: FLUENCY (31+) - User writes mostly EPL
    for i in range(20):
        if i % 5 == 0:
            learning_mode.record_interaction("natural_language")
        else:
            learning_mode.record_interaction("epl")

    assert learning_mode.progress.phase == LearningPhase.FLUENCY

    # Check final stats
    summary = learning_mode.get_progress_summary()
    assert summary['total_interactions'] == 50
    assert summary['phase'] == 'fluency'


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

1. UserProgress Structure (3 tests)
   - Initialization
   - to_dict serialization
   - from_dict deserialization

2. LearningHint Structure (1 test)
   - Hint dataclass

3. LearningMode Initialization (2 tests)
   - Basic initialization
   - With storage path

4. Recording Interactions (4 tests)
   - Natural language
   - EPL
   - With pattern
   - Multiple same pattern

5. Phase Progression (4 tests)
   - Phase 1 range
   - Phase 2 transition
   - Phase 2 range
   - Phase 3 transition

6. Phase 1 Hints (2 tests)
   - Hint for NL input
   - No hint for EPL input

7. Phase 2 Hints (2 tests)
   - Low proficiency hints
   - High proficiency hints

8. Phase 3 Hints (1 test)
   - Subtle hints

9. Progress Summary (3 tests)
   - Summary structure
   - Proficiency calculation
   - Learning time

10. Pattern Tracking (1 test)
    - Most used patterns

11. Persistence (3 tests)
    - Save to file
    - Load from file
    - Across sessions

12. Edge Cases (3 tests)
    - No EPL translation
    - Invalid type
    - Without storage

13. Realistic Journey (1 test)
    - Full learning progression

Total: 30 scientific tests for EPL Learning Mode
"""
