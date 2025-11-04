"""
Decision Fusion Engine

Merges decisions from Max-Code CLI (processing layer) and MAXIMUS AI (noble layer).

Fusion Strategies:
1. Veto Pattern: If any system vetoes, block action
2. Weighted Average: Combine scores with configurable weights
3. Ensemble Voting: Multiple samples vote on best option
4. Cascade: Max-Code generates, MAXIMUS refines

Biblical Foundation:
"Examinai tudo. Retende o bem."
(1 Tessalonicenses 5:21)
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import statistics


# ============================================================================
# ENUMS
# ============================================================================

class FusionMethod(str, Enum):
    """Decision fusion methods"""
    VETO = "veto"                    # Any veto blocks
    WEIGHTED_AVERAGE = "weighted"    # Weighted score combination
    ENSEMBLE_VOTING = "ensemble"     # Voting between options
    CASCADE = "cascade"              # Max-Code → MAXIMUS refinement


class DecisionType(str, Enum):
    """Types of decisions"""
    PLAN = "plan"
    CODE = "code"
    TEST = "test"
    REVIEW = "review"
    FIX = "fix"
    DOCS = "docs"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Decision:
    """Generic decision from an AI system"""
    system: str  # "maxcode" or "maximus"
    decision_type: DecisionType
    content: Any
    confidence: float  # 0.0 to 1.0
    reasoning: str
    metadata: Dict[str, Any]
    veto: bool = False  # True = system vetoes this decision


@dataclass
class FusedDecision:
    """Result of fusing Max-Code and MAXIMUS decisions"""
    final_decision: Any
    confidence: float
    fusion_method: FusionMethod
    contributors: Dict[str, float]  # {"maxcode": 0.6, "maximus": 0.4}
    reasoning: str
    warnings: List[str]


# ============================================================================
# DECISION FUSION ENGINE
# ============================================================================

class DecisionFusion:
    """
    Fuses decisions from Max-Code and MAXIMUS.

    The fusion engine intelligently combines decisions based on:
    - Decision type (plans, code, reviews, etc)
    - Confidence levels
    - Veto signals
    - Context

    Example:
        fusion = DecisionFusion()

        maxcode_decision = Decision(
            system="maxcode",
            decision_type=DecisionType.PLAN,
            content={"plan": "Use Strategy Pattern"},
            confidence=0.85,
            reasoning="ToT explored 3 options, Strategy best",
            metadata={}
        )

        maximus_decision = Decision(
            system="maximus",
            decision_type=DecisionType.PLAN,
            content={"systemic_risk": 0.2, "recommendation": "Strategy Pattern"},
            confidence=0.92,
            reasoning="Lowest systemic risk, no breaking changes",
            metadata={"affected_components": []}
        )

        fused = fusion.fuse(maxcode_decision, maximus_decision)
        print(f"Final: {fused.final_decision} (confidence: {fused.confidence})")
    """

    def __init__(
        self,
        maxcode_weight: float = 0.6,
        maximus_weight: float = 0.4,
        veto_enabled: bool = True,
    ):
        """
        Initialize Decision Fusion Engine.

        Args:
            maxcode_weight: Weight for Max-Code decisions (default: 0.6)
            maximus_weight: Weight for MAXIMUS decisions (default: 0.4)
            veto_enabled: Enable veto pattern (default: True)

        Note:
            Max-Code has higher weight (0.6) because it's the processing layer.
            MAXIMUS provides wisdom/guidance but Max-Code owns execution.
        """
        self.maxcode_weight = maxcode_weight
        self.maximus_weight = maximus_weight
        self.veto_enabled = veto_enabled

        # Normalize weights
        total_weight = maxcode_weight + maximus_weight
        self.maxcode_weight /= total_weight
        self.maximus_weight /= total_weight

    # ========================================================================
    # MAIN FUSION METHOD
    # ========================================================================

    def fuse(
        self,
        maxcode_decision: Decision,
        maximus_decision: Optional[Decision] = None,
        method: Optional[FusionMethod] = None,
    ) -> FusedDecision:
        """
        Fuse decisions from Max-Code and MAXIMUS.

        Args:
            maxcode_decision: Decision from Max-Code
            maximus_decision: Decision from MAXIMUS (optional)
            method: Fusion method (auto-detected if None)

        Returns:
            FusedDecision with final decision

        Example:
            # Standalone (no MAXIMUS)
            fused = fusion.fuse(maxcode_decision)

            # Hybrid (with MAXIMUS)
            fused = fusion.fuse(maxcode_decision, maximus_decision)
        """
        # If no MAXIMUS decision, return Max-Code standalone
        if maximus_decision is None:
            return FusedDecision(
                final_decision=maxcode_decision.content,
                confidence=maxcode_decision.confidence,
                fusion_method=FusionMethod.CASCADE,
                contributors={"maxcode": 1.0},
                reasoning=maxcode_decision.reasoning,
                warnings=["MAXIMUS offline - standalone mode"],
            )

        # Check for vetos
        if self.veto_enabled:
            if maxcode_decision.veto:
                return FusedDecision(
                    final_decision=None,
                    confidence=0.0,
                    fusion_method=FusionMethod.VETO,
                    contributors={"maxcode": 1.0},
                    reasoning=f"Max-Code VETO: {maxcode_decision.reasoning}",
                    warnings=["Action blocked by Max-Code veto"],
                )

            if maximus_decision.veto:
                return FusedDecision(
                    final_decision=None,
                    confidence=0.0,
                    fusion_method=FusionMethod.VETO,
                    contributors={"maximus": 1.0},
                    reasoning=f"MAXIMUS VETO: {maximus_decision.reasoning}",
                    warnings=["Action blocked by MAXIMUS veto"],
                )

        # Auto-detect fusion method if not specified
        if method is None:
            method = self._select_fusion_method(maxcode_decision, maximus_decision)

        # Apply fusion method
        if method == FusionMethod.WEIGHTED_AVERAGE:
            return self._fuse_weighted_average(maxcode_decision, maximus_decision)

        elif method == FusionMethod.ENSEMBLE_VOTING:
            return self._fuse_ensemble_voting(maxcode_decision, maximus_decision)

        elif method == FusionMethod.CASCADE:
            return self._fuse_cascade(maxcode_decision, maximus_decision)

        else:
            raise ValueError(f"Unknown fusion method: {method}")

    # ========================================================================
    # FUSION METHOD SELECTION
    # ========================================================================

    def _select_fusion_method(
        self,
        maxcode_decision: Decision,
        maximus_decision: Decision,
    ) -> FusionMethod:
        """
        Auto-select best fusion method based on decision type.

        Heuristics:
        - PLAN: Weighted average (combine systemic risk + ToT)
        - CODE: Cascade (Max-Code generates, MAXIMUS refines)
        - TEST: Ensemble (both suggest tests, vote on best)
        - REVIEW: Weighted average (combine constitutional + ethical)
        - FIX: Cascade (Max-Code fixes, MAXIMUS validates)
        - DOCS: Cascade (Max-Code generates, MAXIMUS enriches)
        """
        decision_type = maxcode_decision.decision_type

        if decision_type == DecisionType.PLAN:
            return FusionMethod.WEIGHTED_AVERAGE

        elif decision_type == DecisionType.CODE:
            return FusionMethod.CASCADE

        elif decision_type == DecisionType.TEST:
            return FusionMethod.ENSEMBLE_VOTING

        elif decision_type == DecisionType.REVIEW:
            return FusionMethod.WEIGHTED_AVERAGE

        elif decision_type in [DecisionType.FIX, DecisionType.DOCS]:
            return FusionMethod.CASCADE

        else:
            # Default: weighted average
            return FusionMethod.WEIGHTED_AVERAGE

    # ========================================================================
    # FUSION STRATEGIES
    # ========================================================================

    def _fuse_weighted_average(
        self,
        maxcode_decision: Decision,
        maximus_decision: Decision,
    ) -> FusedDecision:
        """
        Weighted average fusion.

        Combines scores/confidences using configured weights.
        Used for: PLAN, REVIEW
        """
        # Combine confidences
        combined_confidence = (
            self.maxcode_weight * maxcode_decision.confidence +
            self.maximus_weight * maximus_decision.confidence
        )

        # Merge content (prefer Max-Code content, enrich with MAXIMUS)
        final_decision = maxcode_decision.content.copy() if isinstance(maxcode_decision.content, dict) else maxcode_decision.content

        if isinstance(final_decision, dict):
            final_decision["maximus_analysis"] = maximus_decision.content

        # Combine reasoning
        combined_reasoning = (
            f"Max-Code ({self.maxcode_weight:.0%}): {maxcode_decision.reasoning}\n"
            f"MAXIMUS ({self.maximus_weight:.0%}): {maximus_decision.reasoning}"
        )

        return FusedDecision(
            final_decision=final_decision,
            confidence=combined_confidence,
            fusion_method=FusionMethod.WEIGHTED_AVERAGE,
            contributors={
                "maxcode": self.maxcode_weight,
                "maximus": self.maximus_weight,
            },
            reasoning=combined_reasoning,
            warnings=[],
        )

    def _fuse_ensemble_voting(
        self,
        maxcode_decision: Decision,
        maximus_decision: Decision,
    ) -> FusedDecision:
        """
        Ensemble voting fusion.

        Both systems provide multiple options, vote on best.
        Used for: TEST (multiple test suggestions)
        """
        # Extract options from both systems
        maxcode_options = maxcode_decision.content if isinstance(maxcode_decision.content, list) else [maxcode_decision.content]
        maximus_options = maximus_decision.content if isinstance(maximus_decision.content, list) else [maximus_decision.content]

        # Combine all options
        all_options = []

        # Max-Code options (weighted)
        for option in maxcode_options:
            all_options.append({
                "option": option,
                "score": maxcode_decision.confidence * self.maxcode_weight,
                "source": "maxcode",
            })

        # MAXIMUS options (weighted)
        for option in maximus_options:
            all_options.append({
                "option": option,
                "score": maximus_decision.confidence * self.maximus_weight,
                "source": "maximus",
            })

        # Sort by score
        all_options.sort(key=lambda x: x["score"], reverse=True)

        # Select top option
        best_option = all_options[0]

        # Calculate confidence (average of top 3)
        top_scores = [opt["score"] for opt in all_options[:3]]
        combined_confidence = statistics.mean(top_scores) if top_scores else 0.0

        # Count contributors
        maxcode_count = sum(1 for opt in all_options if opt["source"] == "maxcode")
        maximus_count = sum(1 for opt in all_options if opt["source"] == "maximus")
        total_count = maxcode_count + maximus_count

        return FusedDecision(
            final_decision=[opt["option"] for opt in all_options],  # Return all ranked
            confidence=combined_confidence,
            fusion_method=FusionMethod.ENSEMBLE_VOTING,
            contributors={
                "maxcode": maxcode_count / total_count if total_count > 0 else 0,
                "maximus": maximus_count / total_count if total_count > 0 else 0,
            },
            reasoning=f"Ensemble voting: {len(all_options)} options, best from {best_option['source']}",
            warnings=[],
        )

    def _fuse_cascade(
        self,
        maxcode_decision: Decision,
        maximus_decision: Decision,
    ) -> FusedDecision:
        """
        Cascade fusion.

        Max-Code generates, MAXIMUS refines/validates.
        Used for: CODE, FIX, DOCS
        """
        # Start with Max-Code output
        final_decision = maxcode_decision.content

        # Apply MAXIMUS refinements (if provided)
        refinements = []
        if isinstance(maximus_decision.content, dict):
            if "refinements" in maximus_decision.content:
                refinements = maximus_decision.content["refinements"]
                final_decision = self._apply_refinements(final_decision, refinements)

        # Calculate confidence (Max-Code primary, MAXIMUS validates)
        combined_confidence = (
            0.7 * maxcode_decision.confidence +  # 70% Max-Code
            0.3 * maximus_decision.confidence    # 30% MAXIMUS validation
        )

        warnings = []
        if maximus_decision.confidence < 0.5:
            warnings.append("MAXIMUS has low confidence in this decision")

        return FusedDecision(
            final_decision=final_decision,
            confidence=combined_confidence,
            fusion_method=FusionMethod.CASCADE,
            contributors={"maxcode": 0.7, "maximus": 0.3},
            reasoning=(
                f"Max-Code generated: {maxcode_decision.reasoning}\n"
                f"MAXIMUS refined: {maximus_decision.reasoning} "
                f"({len(refinements)} refinements applied)"
            ),
            warnings=warnings,
        )

    def _apply_refinements(
        self,
        content: Any,
        refinements: List[Dict[str, Any]],
    ) -> Any:
        """
        Apply MAXIMUS refinements to Max-Code content.

        Refinements can be:
        - Code changes (diffs)
        - Added sections (docs)
        - Improved naming
        - Security fixes
        """
        # If content is string (code/docs), apply text refinements
        if isinstance(content, str):
            refined = content
            for refinement in refinements:
                if refinement["type"] == "replace":
                    refined = refined.replace(refinement["old"], refinement["new"])
                elif refinement["type"] == "append":
                    refined += "\n" + refinement["text"]
            return refined

        # If content is dict, merge refinements
        elif isinstance(content, dict):
            refined = content.copy()
            for refinement in refinements:
                if refinement["type"] == "add_field":
                    refined[refinement["key"]] = refinement["value"]
                elif refinement["type"] == "update_field":
                    if refinement["key"] in refined:
                        refined[refinement["key"]] = refinement["value"]
            return refined

        # Otherwise, return as-is
        else:
            return content

    # ========================================================================
    # SPECIALIZED FUSION METHODS
    # ========================================================================

    def fuse_plan_decisions(
        self,
        maxcode_plans: List[Dict[str, Any]],
        systemic_analyses: List[Any],
    ) -> Dict[str, Any]:
        """
        Fuse planning decisions (Tree of Thoughts + Systemic Analysis).

        Args:
            maxcode_plans: Plans from Max-Code ToT
            systemic_analyses: Systemic analyses from MAXIMUS

        Returns:
            Best plan (lowest systemic risk + highest ToT score)
        """
        if len(maxcode_plans) != len(systemic_analyses):
            raise ValueError("Plans and analyses must have same length")

        # Score each plan
        scored_plans = []
        for plan, analysis in zip(maxcode_plans, systemic_analyses):
            # Combine ToT score + systemic risk (inverted)
            tot_score = plan.get("score", 0.5)
            systemic_risk = analysis.systemic_risk_score if hasattr(analysis, "systemic_risk_score") else 0.5

            combined_score = (
                self.maxcode_weight * tot_score +
                self.maximus_weight * (1.0 - systemic_risk)  # Lower risk = higher score
            )

            scored_plans.append({
                "plan": plan,
                "analysis": analysis,
                "combined_score": combined_score,
            })

        # Select best plan
        best = max(scored_plans, key=lambda x: x["combined_score"])

        return {
            "plan": best["plan"],
            "systemic_analysis": best["analysis"],
            "confidence": best["combined_score"],
            "all_options": scored_plans,
        }

    def fuse_review_verdicts(
        self,
        constitutional: Any,
        ethical: Optional[Any] = None,
    ) -> FusedDecision:
        """
        Fuse review verdicts (Constitutional + Ethical).

        Args:
            constitutional: Max-Code constitutional verdict (P1-P6)
            ethical: MAXIMUS ethical verdict (4 frameworks)

        Returns:
            FusedDecision with final verdict
        """
        # Extract scores
        constitutional_score = constitutional.score if hasattr(constitutional, "score") else 0.0

        if ethical is None:
            # Standalone mode
            return FusedDecision(
                final_decision={"verdict": "APPROVED" if constitutional_score >= 0.7 else "REJECTED"},
                confidence=constitutional_score,
                fusion_method=FusionMethod.CASCADE,
                contributors={"maxcode": 1.0},
                reasoning=constitutional.reasoning if hasattr(constitutional, "reasoning") else "",
                warnings=["MAXIMUS offline - only constitutional review"],
            )

        # Hybrid mode: combine scores
        ethical_score = (
            ethical.kantian_score +
            ethical.virtue_score +
            ethical.consequentialist_score +
            ethical.principlism_score
        ) / 400.0  # Normalize to 0-1

        combined_score = (
            self.maxcode_weight * constitutional_score +
            self.maximus_weight * ethical_score
        )

        # Determine verdict
        if combined_score >= 0.8:
            verdict = "APPROVED"
        elif combined_score >= 0.6:
            verdict = "CONDITIONAL"
        else:
            verdict = "REJECTED"

        return FusedDecision(
            final_decision={
                "verdict": verdict,
                "constitutional_score": constitutional_score,
                "ethical_score": ethical_score,
                "issues": getattr(constitutional, "issues", []) + getattr(ethical, "issues", []),
            },
            confidence=combined_score,
            fusion_method=FusionMethod.WEIGHTED_AVERAGE,
            contributors={"maxcode": self.maxcode_weight, "maximus": self.maximus_weight},
            reasoning=(
                f"Constitutional ({self.maxcode_weight:.0%}): {constitutional_score:.2f}\n"
                f"Ethical ({self.maximus_weight:.0%}): {ethical_score:.2f}"
            ),
            warnings=[],
        )

    def select_best_fix(
        self,
        maxcode_fix: str,
        maximus_healing: Any,
    ) -> str:
        """
        Select best fix (Max-Code quick fix vs MAXIMUS healing).

        Args:
            maxcode_fix: Quick fix from Max-Code
            maximus_healing: Healing suggestion from PENELOPE

        Returns:
            Best fix code
        """
        # If MAXIMUS has high confidence, prefer its fix
        if hasattr(maximus_healing, "confidence") and maximus_healing.confidence >= 0.8:
            if maximus_healing.fix_suggestions:
                best_maximus_fix = max(
                    maximus_healing.fix_suggestions,
                    key=lambda f: f.confidence
                )
                if best_maximus_fix.confidence > 0.7:
                    return best_maximus_fix.code

        # Otherwise, use Max-Code fix
        return maxcode_fix
