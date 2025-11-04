"""
Pre-Execution Guardian

MISSÃO: Validar TODAS as ações ANTES de execução.
AUTORIDADE: Pode BLOQUEAR qualquer ação não-constitucional.

Este Guardian é a PRIMEIRA linha de defesa constitucional.
NADA passa sem aprovação.

"O Senhor é a minha luz e a minha salvação; de quem terei temor?"
(Salmos 27:1)
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..engine import ConstitutionalEngine, Action, ActionType, ConstitutionalResult
from ..validators.p1_completeness import ViolationSeverity


class GuardianDecision(Enum):
    """Decisão do Guardian"""
    APPROVE = "approve"           # Aprovado - pode prosseguir
    REJECT = "reject"             # Rejeitado - bloquear
    APPROVE_WITH_WARNING = "approve_with_warning"  # Aprovado mas com avisos
    ESCALATE_TO_HITL = "escalate_to_hitl"  # Escalar para Human-in-the-Loop


@dataclass
class GuardianVerdict:
    """Veredicto do Guardian"""
    decision: GuardianDecision
    constitutional_result: ConstitutionalResult
    reason: str
    suggestions: List[str]
    should_proceed: bool
    warnings: List[str]


class PreExecutionGuardian:
    """
    Pre-Execution Guardian

    RESPONSABILIDADES:
    - Validar action contra Constitutional Engine
    - Verificar se action respeita P1-P6
    - Bloquear actions não-constitucionais
    - Sugerir correções
    - Escalar para HITL quando necessário

    AUTORIDADE: TOTAL - pode bloquear QUALQUER ação

    "Porque o Senhor conhece o caminho dos justos, mas o caminho dos ímpios perecerá."
    (Salmos 1:6)
    """

    def __init__(self, constitutional_engine: ConstitutionalEngine):
        """
        Inicializa Guardian

        Args:
            constitutional_engine: Engine constitucional
        """
        self.engine = constitutional_engine

        # Stats
        self.stats = {
            'total_validations': 0,
            'approved': 0,
            'rejected': 0,
            'approved_with_warning': 0,
            'escalated_to_hitl': 0,
        }

    def validate_action(self, action: Action) -> GuardianVerdict:
        """
        Valida ação ANTES de execução

        Args:
            action: Ação a validar

        Returns:
            GuardianVerdict com decisão
        """
        self.stats['total_validations'] += 1

        # Executar validação constitucional
        result = self.engine.execute_action(action)

        # Analisar resultado e emitir veredicto
        verdict = self._analyze_and_decide(action, result)

        # Atualizar stats
        self._update_stats(verdict.decision)

        return verdict

    def _analyze_and_decide(
        self,
        action: Action,
        result: ConstitutionalResult
    ) -> GuardianVerdict:
        """
        Analisa resultado constitucional e emite veredicto

        Args:
            action: Ação
            result: Resultado da validação constitucional

        Returns:
            GuardianVerdict
        """
        # Separar violations por severity
        critical_violations = [
            v for v in result.violations
            if v.severity == ViolationSeverity.CRITICAL
        ]
        high_violations = [
            v for v in result.violations
            if v.severity == ViolationSeverity.HIGH
        ]
        medium_violations = [
            v for v in result.violations
            if v.severity == ViolationSeverity.MEDIUM
        ]
        low_violations = [
            v for v in result.violations
            if v.severity == ViolationSeverity.LOW
        ]

        # REGRA 1: CRITICAL violations → REJECT (sem exceções)
        if critical_violations:
            return GuardianVerdict(
                decision=GuardianDecision.REJECT,
                constitutional_result=result,
                reason=f"Action contains {len(critical_violations)} CRITICAL constitutional violations",
                suggestions=self._extract_suggestions(critical_violations),
                should_proceed=False,
                warnings=[]
            )

        # REGRA 2: Multiple HIGH violations → ESCALATE to HITL
        if len(high_violations) >= 3:
            return GuardianVerdict(
                decision=GuardianDecision.ESCALATE_TO_HITL,
                constitutional_result=result,
                reason=f"Action contains {len(high_violations)} HIGH violations (threshold: 3)",
                suggestions=self._extract_suggestions(high_violations),
                should_proceed=False,
                warnings=[]
            )

        # REGRA 3: Some HIGH violations → APPROVE WITH WARNING
        if high_violations:
            return GuardianVerdict(
                decision=GuardianDecision.APPROVE_WITH_WARNING,
                constitutional_result=result,
                reason=f"Action has {len(high_violations)} HIGH violations but can proceed with warnings",
                suggestions=self._extract_suggestions(high_violations),
                should_proceed=True,
                warnings=[v.message for v in high_violations]
            )

        # REGRA 4: Only MEDIUM/LOW violations → APPROVE WITH WARNING
        if medium_violations or low_violations:
            all_minor = medium_violations + low_violations
            return GuardianVerdict(
                decision=GuardianDecision.APPROVE_WITH_WARNING,
                constitutional_result=result,
                reason=f"Action has {len(all_minor)} minor violations",
                suggestions=self._extract_suggestions(all_minor),
                should_proceed=True,
                warnings=[v.message for v in all_minor]
            )

        # REGRA 5: No violations → APPROVE
        return GuardianVerdict(
            decision=GuardianDecision.APPROVE,
            constitutional_result=result,
            reason="Action is fully constitutional",
            suggestions=[],
            should_proceed=True,
            warnings=[]
        )

    def _extract_suggestions(self, violations: List) -> List[str]:
        """Extrai suggestions das violations"""
        suggestions = []
        for v in violations:
            if v.suggestion:
                suggestions.append(f"[{v.principle}] {v.suggestion}")
        return suggestions

    def _update_stats(self, decision: GuardianDecision):
        """Atualiza estatísticas"""
        if decision == GuardianDecision.APPROVE:
            self.stats['approved'] += 1
        elif decision == GuardianDecision.REJECT:
            self.stats['rejected'] += 1
        elif decision == GuardianDecision.APPROVE_WITH_WARNING:
            self.stats['approved_with_warning'] += 1
        elif decision == GuardianDecision.ESCALATE_TO_HITL:
            self.stats['escalated_to_hitl'] += 1

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
            'approval_rate': (
                (self.stats['approved'] + self.stats['approved_with_warning'])
                / self.stats['total_validations'] * 100
                if self.stats['total_validations'] > 0 else 100.0
            ),
            'rejection_rate': (
                self.stats['rejected'] / self.stats['total_validations'] * 100
                if self.stats['total_validations'] > 0 else 0.0
            ),
        }

    def print_verdict(self, verdict: GuardianVerdict):
        """
        Imprime veredicto (formato bonito)

        Args:
            verdict: Veredicto
        """
        print("\n" + "="*70)
        print("  PRE-EXECUTION GUARDIAN VERDICT")
        print("="*70 + "\n")

        # Decisão
        decision_symbol = {
            GuardianDecision.APPROVE: "✓",
            GuardianDecision.REJECT: "✗",
            GuardianDecision.APPROVE_WITH_WARNING: "⚠",
            GuardianDecision.ESCALATE_TO_HITL: "↑",
        }

        symbol = decision_symbol.get(verdict.decision, "?")
        print(f"DECISION: {symbol} {verdict.decision.value.upper()}")
        print(f"REASON:   {verdict.reason}")
        print(f"PROCEED:  {'YES' if verdict.should_proceed else 'NO'}\n")

        # Warnings
        if verdict.warnings:
            print("WARNINGS:")
            for warning in verdict.warnings:
                print(f"  ⚠ {warning}")
            print()

        # Suggestions
        if verdict.suggestions:
            print("SUGGESTIONS:")
            for suggestion in verdict.suggestions:
                print(f"  → {suggestion}")
            print()

        # Constitutional Score
        score = verdict.constitutional_result.constitutional_score
        score_bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        print(f"CONSTITUTIONAL SCORE: {score:.2f} [{score_bar}]")

        print("="*70 + "\n")


# ==================== HELPER FUNCTIONS ====================

def validate_before_execution(action: Action) -> GuardianVerdict:
    """
    Helper function para validar ação antes de execução

    Args:
        action: Ação

    Returns:
        GuardianVerdict
    """
    from ..engine import get_constitutional_engine

    engine = get_constitutional_engine()
    guardian = PreExecutionGuardian(engine)

    return guardian.validate_action(action)
