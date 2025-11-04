"""
Integration Tests for Decision Fusion Engine

Tests the fusion of decisions from Max-Code CLI and MAXIMUS AI.

Run:
    pytest tests/test_decision_fusion.py -v
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import List, Dict, Any

from core.maximus_integration.decision_fusion import (
    DecisionFusion,
    Decision,
    FusedDecision,
    FusionMethod,
    DecisionType,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fusion_engine():
    """Create DecisionFusion instance with default weights"""
    return DecisionFusion(
        maxcode_weight=0.6,
        maximus_weight=0.4,
        veto_enabled=True
    )


@pytest.fixture
def maxcode_plan_decision():
    """Sample Max-Code planning decision"""
    return Decision(
        system="maxcode",
        decision_type=DecisionType.PLAN,
        content={
            "plan": "Use Strategy Pattern for payment processing",
            "reasoning": "ToT explored 3 options, Strategy Pattern scored highest",
            "score": 0.85,
        },
        confidence=0.85,
        reasoning="Tree of Thoughts: Strategy Pattern best for extensibility",
        metadata={"tot_branches": 3, "depth": 3},
        veto=False,
    )


@pytest.fixture
def maximus_plan_decision():
    """Sample MAXIMUS planning decision"""
    return Decision(
        system="maximus",
        decision_type=DecisionType.PLAN,
        content={
            "systemic_risk_score": 0.15,
            "recommendation": "Strategy Pattern acceptable",
            "affected_components": ["payment_service"],
            "confidence": 0.92,
        },
        confidence=0.92,
        reasoning="Low systemic risk (0.15), no breaking changes detected",
        metadata={"lei_analysis": True},
        veto=False,
    )


@pytest.fixture
def maxcode_code_decision():
    """Sample Max-Code code generation decision"""
    return Decision(
        system="maxcode",
        decision_type=DecisionType.CODE,
        content="def authenticate(user, password):\n    return check_password(user, password)",
        confidence=0.75,
        reasoning="Generated authentication function following best practices",
        metadata={"lines": 2},
        veto=False,
    )


@pytest.fixture
def maximus_code_decision():
    """Sample MAXIMUS code refinement decision"""
    return Decision(
        system="maximus",
        decision_type=DecisionType.CODE,
        content={
            "refinements": [
                {
                    "type": "replace",
                    "old": "return check_password(user, password)",
                    "new": "return timing_safe_compare(check_password(user, password), True)",
                },
            ],
            "security_improvements": ["Added timing-safe comparison"],
        },
        confidence=0.88,
        reasoning="Added timing-attack protection via timing_safe_compare",
        metadata={"security_scan": True},
        veto=False,
    )


@pytest.fixture
def maxcode_veto_decision():
    """Max-Code decision with VETO"""
    return Decision(
        system="maxcode",
        decision_type=DecisionType.REVIEW,
        content=None,
        confidence=0.0,
        reasoning="P1 violation: Code directly modifies production database without backup",
        metadata={"constitutional_violations": ["P1"]},
        veto=True,
    )


@pytest.fixture
def maximus_veto_decision():
    """MAXIMUS decision with VETO"""
    return Decision(
        system="maximus",
        decision_type=DecisionType.REVIEW,
        content=None,
        confidence=0.0,
        reasoning="Ethical violation: Kantian framework rejects discrimination",
        metadata={"ethical_violations": ["kantian"]},
        veto=True,
    )


# ============================================================================
# TEST: INITIALIZATION
# ============================================================================

def test_fusion_engine_initialization():
    """Test DecisionFusion initialization with custom weights"""
    fusion = DecisionFusion(
        maxcode_weight=0.7,
        maximus_weight=0.3,
        veto_enabled=False
    )

    assert fusion.maxcode_weight == 0.7
    assert fusion.maximus_weight == 0.3
    assert fusion.veto_enabled == False


def test_fusion_engine_weight_normalization():
    """Test that weights are normalized to sum to 1.0"""
    fusion = DecisionFusion(maxcode_weight=3.0, maximus_weight=2.0)

    # Weights should be normalized: 3/(3+2) = 0.6, 2/(3+2) = 0.4
    assert abs(fusion.maxcode_weight - 0.6) < 0.001
    assert abs(fusion.maximus_weight - 0.4) < 0.001


# ============================================================================
# TEST: STANDALONE MODE (No MAXIMUS)
# ============================================================================

def test_fusion_standalone_mode(fusion_engine, maxcode_plan_decision):
    """Test fusion when MAXIMUS is offline (standalone mode)"""
    fused = fusion_engine.fuse(maxcode_plan_decision, maximus_decision=None)

    assert isinstance(fused, FusedDecision)
    assert fused.final_decision == maxcode_plan_decision.content
    assert fused.confidence == maxcode_plan_decision.confidence
    assert fused.fusion_method == FusionMethod.CASCADE
    assert fused.contributors == {"maxcode": 1.0}
    assert "MAXIMUS offline" in fused.warnings[0]


# ============================================================================
# TEST: VETO PATTERN
# ============================================================================

def test_maxcode_veto_blocks_action(fusion_engine, maxcode_veto_decision, maximus_plan_decision):
    """Test that Max-Code veto blocks the action"""
    fused = fusion_engine.fuse(maxcode_veto_decision, maximus_plan_decision)

    assert fused.final_decision is None
    assert fused.confidence == 0.0
    assert fused.fusion_method == FusionMethod.VETO
    assert fused.contributors == {"maxcode": 1.0}
    assert "Max-Code VETO" in fused.reasoning
    assert len(fused.warnings) > 0


def test_maximus_veto_blocks_action(fusion_engine, maxcode_plan_decision, maximus_veto_decision):
    """Test that MAXIMUS veto blocks the action"""
    fused = fusion_engine.fuse(maxcode_plan_decision, maximus_veto_decision)

    assert fused.final_decision is None
    assert fused.confidence == 0.0
    assert fused.fusion_method == FusionMethod.VETO
    assert fused.contributors == {"maximus": 1.0}
    assert "MAXIMUS VETO" in fused.reasoning
    assert len(fused.warnings) > 0


def test_veto_disabled(maxcode_veto_decision, maximus_plan_decision):
    """Test fusion with veto disabled"""
    fusion = DecisionFusion(veto_enabled=False)

    # Even with veto decision, fusion should proceed
    fused = fusion.fuse(maxcode_veto_decision, maximus_plan_decision)

    # Should use weighted average method (since veto disabled)
    assert fused.fusion_method == FusionMethod.WEIGHTED_AVERAGE


# ============================================================================
# TEST: WEIGHTED AVERAGE FUSION
# ============================================================================

def test_weighted_average_fusion_plan(fusion_engine, maxcode_plan_decision, maximus_plan_decision):
    """Test weighted average fusion for planning decisions"""
    fused = fusion_engine.fuse(
        maxcode_plan_decision,
        maximus_plan_decision,
        method=FusionMethod.WEIGHTED_AVERAGE
    )

    assert isinstance(fused, FusedDecision)
    assert fused.fusion_method == FusionMethod.WEIGHTED_AVERAGE

    # Check confidence is weighted average
    expected_confidence = (0.6 * 0.85) + (0.4 * 0.92)
    assert abs(fused.confidence - expected_confidence) < 0.001

    # Check contributors
    assert fused.contributors["maxcode"] == 0.6
    assert fused.contributors["maximus"] == 0.4

    # Check MAXIMUS analysis is included
    assert isinstance(fused.final_decision, dict)
    assert "maximus_analysis" in fused.final_decision


def test_weighted_average_combines_reasoning(fusion_engine, maxcode_plan_decision, maximus_plan_decision):
    """Test that weighted average combines reasoning from both systems"""
    fused = fusion_engine.fuse(
        maxcode_plan_decision,
        maximus_plan_decision,
        method=FusionMethod.WEIGHTED_AVERAGE
    )

    assert "Max-Code" in fused.reasoning
    assert "MAXIMUS" in fused.reasoning
    assert "60%" in fused.reasoning
    assert "40%" in fused.reasoning


# ============================================================================
# TEST: CASCADE FUSION
# ============================================================================

def test_cascade_fusion_code(fusion_engine, maxcode_code_decision, maximus_code_decision):
    """Test cascade fusion for code generation (Max-Code → MAXIMUS refinement)"""
    fused = fusion_engine.fuse(
        maxcode_code_decision,
        maximus_code_decision,
        method=FusionMethod.CASCADE
    )

    assert isinstance(fused, FusedDecision)
    assert fused.fusion_method == FusionMethod.CASCADE

    # Check confidence calculation (70% Max-Code, 30% MAXIMUS)
    expected_confidence = (0.7 * 0.75) + (0.3 * 0.88)
    assert abs(fused.confidence - expected_confidence) < 0.001

    # Check contributors
    assert fused.contributors["maxcode"] == 0.7
    assert fused.contributors["maximus"] == 0.3

    # Check refinements were applied
    assert isinstance(fused.final_decision, str)
    assert "timing_safe_compare" in fused.final_decision


def test_cascade_applies_text_refinements(fusion_engine, maxcode_code_decision, maximus_code_decision):
    """Test that cascade applies MAXIMUS text refinements to Max-Code output"""
    fused = fusion_engine.fuse(
        maxcode_code_decision,
        maximus_code_decision,
        method=FusionMethod.CASCADE
    )

    # Check that replacement was applied
    original_code = maxcode_code_decision.content
    refined_code = fused.final_decision

    assert original_code != refined_code
    assert "timing_safe_compare" in refined_code


def test_cascade_warns_on_low_maximus_confidence(fusion_engine, maxcode_code_decision):
    """Test that cascade warns when MAXIMUS has low confidence"""
    low_confidence_maximus = Decision(
        system="maximus",
        decision_type=DecisionType.CODE,
        content={"refinements": []},
        confidence=0.3,  # Low confidence
        reasoning="Uncertain about refinements",
        metadata={},
        veto=False,
    )

    fused = fusion_engine.fuse(
        maxcode_code_decision,
        low_confidence_maximus,
        method=FusionMethod.CASCADE
    )

    assert len(fused.warnings) > 0
    assert "low confidence" in fused.warnings[0].lower()


# ============================================================================
# TEST: ENSEMBLE VOTING FUSION
# ============================================================================

def test_ensemble_voting_fusion_test(fusion_engine):
    """Test ensemble voting fusion for test suggestions"""
    maxcode_tests = Decision(
        system="maxcode",
        decision_type=DecisionType.TEST,
        content=[
            {"name": "test_authentication", "priority": "high"},
            {"name": "test_authorization", "priority": "high"},
        ],
        confidence=0.80,
        reasoning="Generated tests via TDD cycle",
        metadata={},
        veto=False,
    )

    maximus_tests = Decision(
        system="maximus",
        decision_type=DecisionType.TEST,
        content=[
            {"name": "test_edge_case_empty_password", "priority": "critical"},
            {"name": "test_sql_injection", "priority": "critical"},
        ],
        confidence=0.90,
        reasoning="Predicted edge cases via systemic analysis",
        metadata={},
        veto=False,
    )

    fused = fusion_engine.fuse(
        maxcode_tests,
        maximus_tests,
        method=FusionMethod.ENSEMBLE_VOTING
    )

    assert isinstance(fused, FusedDecision)
    assert fused.fusion_method == FusionMethod.ENSEMBLE_VOTING

    # Should return all options ranked by score
    assert isinstance(fused.final_decision, list)
    assert len(fused.final_decision) == 4  # 2 from Max-Code + 2 from MAXIMUS

    # Check contributors
    assert "maxcode" in fused.contributors
    assert "maximus" in fused.contributors


# ============================================================================
# TEST: AUTO-DETECTION OF FUSION METHOD
# ============================================================================

def test_auto_detect_fusion_method_plan(fusion_engine, maxcode_plan_decision, maximus_plan_decision):
    """Test auto-detection selects WEIGHTED_AVERAGE for PLAN decisions"""
    fused = fusion_engine.fuse(maxcode_plan_decision, maximus_plan_decision)

    assert fused.fusion_method == FusionMethod.WEIGHTED_AVERAGE


def test_auto_detect_fusion_method_code(fusion_engine, maxcode_code_decision, maximus_code_decision):
    """Test auto-detection selects CASCADE for CODE decisions"""
    fused = fusion_engine.fuse(maxcode_code_decision, maximus_code_decision)

    assert fused.fusion_method == FusionMethod.CASCADE


def test_auto_detect_fusion_method_test(fusion_engine):
    """Test auto-detection selects ENSEMBLE_VOTING for TEST decisions"""
    maxcode_tests = Decision(
        system="maxcode",
        decision_type=DecisionType.TEST,
        content=[{"test": "test_auth"}],
        confidence=0.8,
        reasoning="TDD tests",
        metadata={},
        veto=False,
    )

    maximus_tests = Decision(
        system="maximus",
        decision_type=DecisionType.TEST,
        content=[{"test": "test_edge"}],
        confidence=0.9,
        reasoning="Edge case tests",
        metadata={},
        veto=False,
    )

    fused = fusion_engine.fuse(maxcode_tests, maximus_tests)

    assert fused.fusion_method == FusionMethod.ENSEMBLE_VOTING


# ============================================================================
# TEST: SPECIALIZED FUSION METHODS
# ============================================================================

def test_fuse_plan_decisions_specialized(fusion_engine):
    """Test specialized fuse_plan_decisions method"""
    maxcode_plans = [
        {"plan": "Strategy Pattern", "score": 0.85},
        {"plan": "Factory Pattern", "score": 0.70},
        {"plan": "Singleton Pattern", "score": 0.60},
    ]

    # Mock systemic analyses
    systemic_analyses = [
        MagicMock(systemic_risk_score=0.15),  # Low risk
        MagicMock(systemic_risk_score=0.40),  # Medium risk
        MagicMock(systemic_risk_score=0.60),  # High risk
    ]

    result = fusion_engine.fuse_plan_decisions(maxcode_plans, systemic_analyses)

    assert isinstance(result, dict)
    assert "plan" in result
    assert "systemic_analysis" in result
    assert "confidence" in result
    assert "all_options" in result

    # Best plan should be Strategy (high ToT score + low systemic risk)
    assert result["plan"]["plan"] == "Strategy Pattern"


def test_fuse_review_verdicts_standalone(fusion_engine):
    """Test specialized fuse_review_verdicts in standalone mode"""
    constitutional_verdict = MagicMock(
        score=0.85,
        reasoning="P1-P6 compliance verified"
    )

    fused = fusion_engine.fuse_review_verdicts(constitutional_verdict, ethical=None)

    assert isinstance(fused, FusedDecision)
    assert fused.final_decision["verdict"] == "APPROVED"
    assert fused.confidence == 0.85
    assert "MAXIMUS offline" in fused.warnings[0]


def test_fuse_review_verdicts_hybrid(fusion_engine):
    """Test specialized fuse_review_verdicts in hybrid mode"""
    constitutional_verdict = MagicMock(
        score=0.80,
        reasoning="P1-P6 compliance verified",
        issues=[]
    )

    ethical_verdict = MagicMock(
        kantian_score=90,
        virtue_score=85,
        consequentialist_score=92,
        principlism_score=88,
        issues=[]
    )

    fused = fusion_engine.fuse_review_verdicts(constitutional_verdict, ethical_verdict)

    assert isinstance(fused, FusedDecision)
    assert fused.fusion_method == FusionMethod.WEIGHTED_AVERAGE
    assert "verdict" in fused.final_decision
    assert fused.final_decision["verdict"] in ["APPROVED", "CONDITIONAL", "REJECTED"]


def test_select_best_fix_prefers_high_confidence_maximus(fusion_engine):
    """Test select_best_fix prefers MAXIMUS fix when confidence is high"""
    maxcode_fix = "quick_fix_code"

    maximus_healing = MagicMock(
        confidence=0.95,
        fix_suggestions=[
            MagicMock(confidence=0.92, code="maximus_deep_fix"),
        ]
    )

    best_fix = fusion_engine.select_best_fix(maxcode_fix, maximus_healing)

    assert best_fix == "maximus_deep_fix"


def test_select_best_fix_falls_back_to_maxcode(fusion_engine):
    """Test select_best_fix falls back to Max-Code when MAXIMUS confidence low"""
    maxcode_fix = "quick_fix_code"

    maximus_healing = MagicMock(
        confidence=0.40,  # Low confidence
        fix_suggestions=[]
    )

    best_fix = fusion_engine.select_best_fix(maxcode_fix, maximus_healing)

    assert best_fix == "quick_fix_code"


# ============================================================================
# TEST: ERROR HANDLING
# ============================================================================

def test_invalid_fusion_method_raises_error(fusion_engine, maxcode_plan_decision, maximus_plan_decision):
    """Test that invalid fusion method raises ValueError"""
    with pytest.raises(ValueError, match="Unknown fusion method"):
        fusion_engine.fuse(
            maxcode_plan_decision,
            maximus_plan_decision,
            method="INVALID_METHOD"
        )


def test_fuse_plan_decisions_length_mismatch(fusion_engine):
    """Test fuse_plan_decisions raises error when lengths don't match"""
    maxcode_plans = [{"plan": "A"}, {"plan": "B"}]
    systemic_analyses = [MagicMock()]  # Only 1 analysis

    with pytest.raises(ValueError, match="same length"):
        fusion_engine.fuse_plan_decisions(maxcode_plans, systemic_analyses)


# ============================================================================
# TEST: REFINEMENT APPLICATION
# ============================================================================

def test_apply_refinements_text_replace(fusion_engine):
    """Test _apply_refinements with text replacement"""
    content = "def foo():\n    return 42"
    refinements = [
        {"type": "replace", "old": "42", "new": "100"},
    ]

    refined = fusion_engine._apply_refinements(content, refinements)

    assert "100" in refined
    assert "42" not in refined


def test_apply_refinements_text_append(fusion_engine):
    """Test _apply_refinements with text append"""
    content = "def foo():\n    pass"
    refinements = [
        {"type": "append", "text": "# Added comment"},
    ]

    refined = fusion_engine._apply_refinements(content, refinements)

    assert "# Added comment" in refined


def test_apply_refinements_dict_add_field(fusion_engine):
    """Test _apply_refinements with dict field addition"""
    content = {"name": "test"}
    refinements = [
        {"type": "add_field", "key": "priority", "value": "high"},
    ]

    refined = fusion_engine._apply_refinements(content, refinements)

    assert refined["priority"] == "high"


def test_apply_refinements_dict_update_field(fusion_engine):
    """Test _apply_refinements with dict field update"""
    content = {"name": "test", "priority": "low"}
    refinements = [
        {"type": "update_field", "key": "priority", "value": "critical"},
    ]

    refined = fusion_engine._apply_refinements(content, refinements)

    assert refined["priority"] == "critical"


# ============================================================================
# TEST: CONFIDENCE CALCULATIONS
# ============================================================================

def test_confidence_calculation_weighted_average(fusion_engine):
    """Test confidence calculation in weighted average fusion"""
    decision1 = Decision(
        system="maxcode",
        decision_type=DecisionType.PLAN,
        content={"plan": "A"},
        confidence=0.8,
        reasoning="Test",
        metadata={},
        veto=False,
    )

    decision2 = Decision(
        system="maximus",
        decision_type=DecisionType.PLAN,
        content={"risk": 0.2},
        confidence=0.9,
        reasoning="Test",
        metadata={},
        veto=False,
    )

    fused = fusion_engine.fuse(decision1, decision2, method=FusionMethod.WEIGHTED_AVERAGE)

    # Confidence = 0.6 * 0.8 + 0.4 * 0.9 = 0.48 + 0.36 = 0.84
    expected = 0.84
    assert abs(fused.confidence - expected) < 0.001


def test_confidence_calculation_cascade(fusion_engine):
    """Test confidence calculation in cascade fusion"""
    decision1 = Decision(
        system="maxcode",
        decision_type=DecisionType.CODE,
        content="code",
        confidence=0.8,
        reasoning="Test",
        metadata={},
        veto=False,
    )

    decision2 = Decision(
        system="maximus",
        decision_type=DecisionType.CODE,
        content={"refinements": []},
        confidence=0.9,
        reasoning="Test",
        metadata={},
        veto=False,
    )

    fused = fusion_engine.fuse(decision1, decision2, method=FusionMethod.CASCADE)

    # Confidence = 0.7 * 0.8 + 0.3 * 0.9 = 0.56 + 0.27 = 0.83
    expected = 0.83
    assert abs(fused.confidence - expected) < 0.001


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

1. Initialization (2 tests)
   - Default and custom weights
   - Weight normalization

2. Standalone Mode (1 test)
   - Fusion when MAXIMUS offline

3. Veto Pattern (3 tests)
   - Max-Code veto
   - MAXIMUS veto
   - Veto disabled

4. Weighted Average Fusion (2 tests)
   - Plan decisions
   - Reasoning combination

5. Cascade Fusion (3 tests)
   - Code generation
   - Refinement application
   - Low confidence warnings

6. Ensemble Voting Fusion (1 test)
   - Test suggestions

7. Auto-Detection (3 tests)
   - PLAN → WEIGHTED_AVERAGE
   - CODE → CASCADE
   - TEST → ENSEMBLE_VOTING

8. Specialized Methods (4 tests)
   - fuse_plan_decisions
   - fuse_review_verdicts (standalone + hybrid)
   - select_best_fix

9. Error Handling (2 tests)
   - Invalid fusion method
   - Length mismatch

10. Refinement Application (4 tests)
    - Text replace/append
    - Dict add/update field

11. Confidence Calculations (2 tests)
    - Weighted average
    - Cascade

Total: 27 comprehensive test cases covering all fusion methods and edge cases.
"""
