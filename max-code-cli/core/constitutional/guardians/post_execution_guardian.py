"""
Post-Execution Guardian

MISSÃO: Validar resultado DEPOIS de execução completa.
AUTORIDADE: Pode REJEITAR output final não-constitucional.

Este Guardian é a ÚLTIMA linha de defesa.
O output FINAL deve ser impecável.

"Examinai tudo. Retende o bem."
(1 Tessalonicenses 5:21)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ..engine import ConstitutionalEngine, Action, ActionType
from ..validators.p1_completeness import ViolationSeverity, P1_Completeness_Validator
from ..models import Violation
from ..validators.p2_api_validator import P2_API_Validator
from ..validators.p5_systemic import P5_Systemic_Analyzer
from config.logging_config import get_logger

logger = get_logger(__name__)


class OutputQuality(Enum):
    """Qualidade do output"""
    EXCELLENT = "excellent"      # LEI < 0.5, FPC ≥ 90%, zero violations
    GOOD = "good"                # LEI < 1.0, FPC ≥ 80%, minor violations
    ACCEPTABLE = "acceptable"    # LEI < 2.0, FPC ≥ 70%, no critical violations
    POOR = "poor"                # LEI ≥ 2.0 ou FPC < 70%
    UNACCEPTABLE = "unacceptable"  # Critical violations presentes


@dataclass
class OutputMetrics:
    """Métricas do output final"""
    lei: float  # Lazy Execution Index
    fpc: float  # First-Pass Correctness
    total_violations: int
    critical_violations: int
    high_violations: int
    lines_of_code: int
    cyclomatic_complexity: Optional[float] = None
    test_coverage: Optional[float] = None


@dataclass
class FinalVerdict:
    """Veredicto final do Guardian"""
    quality: OutputQuality
    metrics: OutputMetrics
    violations: List[Violation]
    passed: bool
    reason: str
    suggestions: List[str]
    must_fix: List[str]  # Fixes obrigatórios se rejeitar


class PostExecutionGuardian:
    """
    Post-Execution Guardian

    RESPONSABILIDADES:
    - Validar código gerado final
    - Calcular métricas de qualidade (LEI, FPC, etc)
    - Detectar problemas que passaram despercebidos
    - Emitir veredicto final: ACCEPT ou REJECT
    - Sugerir melhorias

    AUTORIDADE: Pode REJEITAR output final

    "Pelos seus frutos os conhecereis."
    (Mateus 7:20)
    """

    def __init__(
        self,
        constitutional_engine: ConstitutionalEngine,
        p1_validator: Optional[P1_Completeness_Validator] = None,
        p2_validator: Optional[P2_API_Validator] = None,
        p5_analyzer: Optional[P5_Systemic_Analyzer] = None
    ):
        """
        Inicializa Guardian

        Args:
            constitutional_engine: Engine constitucional
            p1_validator: Validator P1 (opcional)
            p2_validator: Validator P2 (opcional)
            p5_analyzer: Analyzer P5 (opcional)
        """
        self.engine = constitutional_engine
        self.p1_validator = p1_validator or P1_Completeness_Validator()
        self.p2_validator = p2_validator or P2_API_Validator()
        self.p5_analyzer = p5_analyzer or P5_Systemic_Analyzer()

        # Stats
        self.stats = {
            'total_validations': 0,
            'accepted': 0,
            'rejected': 0,
            'excellent_outputs': 0,
            'good_outputs': 0,
            'acceptable_outputs': 0,
            'poor_outputs': 0,
        }

    def validate_output(
        self,
        code: str,
        language: str = 'python',
        context: Optional[Dict] = None,
        task_id: Optional[str] = None
    ) -> FinalVerdict:
        """
        Valida output final

        Args:
            code: Código gerado
            language: Linguagem
            context: Contexto (metadata, etc)
            task_id: ID da task (para P6 metrics)

        Returns:
            FinalVerdict
        """
        self.stats['total_validations'] += 1

        # 1. Validar com Constitutional Engine
        action = Action(
            task_id=task_id or 'post-validation',
            action_type=ActionType.CODE_GENERATION,
            intent=f'Validate generated {language} code',
            context={'code': code, 'language': language},
            constitutional_context=context or {}
        )

        constitutional_result = self.engine.execute_action(action)

        # 2. Verificações adicionais de segurança PRIMEIRO
        security_violations = self._security_audit(code)

        # 3. Calcular métricas específicas (incluindo security violations)
        metrics = self._calculate_metrics(code, language, task_id, security_violations)

        # 4. Análise de qualidade
        all_violations = constitutional_result.violations + security_violations
        quality = self._determine_quality(metrics, all_violations)

        # 5. Emitir veredicto
        verdict = self._emit_verdict(quality, metrics, all_violations)

        # 6. Atualizar stats
        self._update_stats(quality, verdict.passed)

        return verdict

    def _calculate_metrics(
        self,
        code: str,
        language: str,
        task_id: Optional[str],
        security_violations: List[Violation] = None
    ) -> OutputMetrics:
        """Calcula métricas do output"""

        # LEI (Lazy Execution Index)
        try:
            lei = self.p1_validator.calculate_lei(code)
        except (AttributeError, Exception):
            # Fallback if calculate_lei not available
            lei = 0.5

        # FPC (First-Pass Correctness)
        try:
            from ..validators.p6_token_efficiency import get_monitor
            monitor = get_monitor()
            fpc = monitor.calculate_fpc() if task_id else 100.0
        except (ImportError, AttributeError, Exception):
            # Fallback if P6 monitor not available
            fpc = 100.0

        # Violations
        p1_result = self.p1_validator.validate(code, language)
        p2_result = self.p2_validator.validate(code, language)

        all_violations = p1_result.violations + p2_result.violations

        # Include security violations in metrics
        if security_violations:
            all_violations.extend(security_violations)

        critical_count = sum(1 for v in all_violations if v.severity == ViolationSeverity.CRITICAL)
        high_count = sum(1 for v in all_violations if v.severity == ViolationSeverity.HIGH)

        # LOC
        lines = [line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        loc = len(lines)

        return OutputMetrics(
            lei=lei,
            fpc=fpc,
            total_violations=len(all_violations),
            critical_violations=critical_count,
            high_violations=high_count,
            lines_of_code=loc
        )

    def _determine_quality(
        self,
        metrics: OutputMetrics,
        violations: List[Violation]
    ) -> OutputQuality:
        """Determina qualidade do output"""

        # UNACCEPTABLE: critical violations
        if metrics.critical_violations > 0:
            return OutputQuality.UNACCEPTABLE

        # POOR: LEI alto ou FPC baixo
        if metrics.lei >= 2.0 or metrics.fpc < 70.0:
            return OutputQuality.POOR

        # EXCELLENT: LEI < 0.5, FPC ≥ 90%, zero violations
        if metrics.lei < 0.5 and metrics.fpc >= 90.0 and metrics.total_violations == 0:
            return OutputQuality.EXCELLENT

        # GOOD: LEI < 1.0, FPC ≥ 80%, minor violations
        if metrics.lei < 1.0 and metrics.fpc >= 80.0 and metrics.high_violations == 0:
            return OutputQuality.GOOD

        # ACCEPTABLE: caso contrário
        return OutputQuality.ACCEPTABLE

    def _security_audit(self, code: str) -> List[Violation]:
        """Auditoria de segurança adicional"""
        violations = []

        # Padrões de ALTA severidade
        security_patterns = [
            (r'os\.system\s*\(', 'os.system() usage (command injection risk)'),
            (r'subprocess\.\w+\s*\([^)]*shell\s*=\s*True', 'subprocess with shell=True (command injection)'),
            (r'eval\s*\(', 'eval() usage (code injection)'),
            (r'exec\s*\(', 'exec() usage (code injection)'),
            (r'__import__\s*\(', 'Dynamic import (__import__)'),
            (r'pickle\.loads?\s*\(', 'pickle usage (arbitrary code execution)'),
        ]

        import re
        for pattern, description in security_patterns:
            matches = re.findall(pattern, code)
            if matches:
                violations.append(Violation(
                    principle="P2",
                    severity=ViolationSeverity.CRITICAL,
                    message=f"Security vulnerability detected: {description}",
                    suggestion="Use safer alternatives or sanitize input",
                    context={"pattern": pattern, "description": description}
                ))

        return violations

    def _emit_verdict(
        self,
        quality: OutputQuality,
        metrics: OutputMetrics,
        violations: List[Violation]
    ) -> FinalVerdict:
        """Emite veredicto final"""

        # Determinar se passou
        passed = quality in [OutputQuality.EXCELLENT, OutputQuality.GOOD, OutputQuality.ACCEPTABLE]

        # Razão
        reason = self._generate_reason(quality, metrics)

        # Suggestions
        suggestions = self._generate_suggestions(quality, metrics, violations)

        # Must-fix (se rejeitado)
        must_fix = []
        if not passed:
            must_fix = [v.message for v in violations if v.severity == ViolationSeverity.CRITICAL]

        return FinalVerdict(
            quality=quality,
            metrics=metrics,
            violations=violations,
            passed=passed,
            reason=reason,
            suggestions=suggestions,
            must_fix=must_fix
        )

    def _generate_reason(self, quality: OutputQuality, metrics: OutputMetrics) -> str:
        """Gera razão do veredicto"""
        reasons = {
            OutputQuality.EXCELLENT: f"Output is EXCELLENT: LEI={metrics.lei:.2f}, FPC={metrics.fpc:.1f}%, zero violations",
            OutputQuality.GOOD: f"Output is GOOD: LEI={metrics.lei:.2f}, FPC={metrics.fpc:.1f}%, minor violations only",
            OutputQuality.ACCEPTABLE: f"Output is ACCEPTABLE: LEI={metrics.lei:.2f}, FPC={metrics.fpc:.1f}%",
            OutputQuality.POOR: f"Output is POOR: LEI={metrics.lei:.2f} (target: <1.0), FPC={metrics.fpc:.1f}% (target: ≥80%)",
            OutputQuality.UNACCEPTABLE: f"Output is UNACCEPTABLE: {metrics.critical_violations} CRITICAL violations detected",
        }
        return reasons.get(quality, "Quality undetermined")

    def _generate_suggestions(
        self,
        quality: OutputQuality,
        metrics: OutputMetrics,
        violations: List[Violation]
    ) -> List[str]:
        """Gera suggestions para melhorar output"""
        suggestions = []

        # LEI alto
        if metrics.lei >= 1.0:
            suggestions.append(f"Reduce LEI from {metrics.lei:.2f} to <1.0 by removing placeholders/TODOs")

        # FPC baixo
        if metrics.fpc < 80.0:
            suggestions.append(f"Improve FPC from {metrics.fpc:.1f}% to ≥80% by reducing iterations")

        # Violations
        for v in violations:
            if v.suggestion:
                suggestions.append(f"[{v.principle}] {v.suggestion}")

        return suggestions

    def _update_stats(self, quality: OutputQuality, passed: bool):
        """Atualiza estatísticas"""
        if passed:
            self.stats['accepted'] += 1
        else:
            self.stats['rejected'] += 1

        quality_map = {
            OutputQuality.EXCELLENT: 'excellent_outputs',
            OutputQuality.GOOD: 'good_outputs',
            OutputQuality.ACCEPTABLE: 'acceptable_outputs',
            OutputQuality.POOR: 'poor_outputs',
        }

        if quality in quality_map:
            self.stats[quality_map[quality]] += 1

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
            'acceptance_rate': (
                self.stats['accepted'] / self.stats['total_validations'] * 100
                if self.stats['total_validations'] > 0 else 100.0
            ),
            'excellence_rate': (
                self.stats['excellent_outputs'] / self.stats['total_validations'] * 100
                if self.stats['total_validations'] > 0 else 0.0
            ),
        }

    def print_verdict(self, verdict: FinalVerdict):
        """Imprime veredicto (formato bonito)"""
        print("\n" + "="*70)
        logger.info("  POST-EXECUTION GUARDIAN VERDICT")
        print("="*70 + "\n")

        # Quality
        quality_symbols = {
            OutputQuality.EXCELLENT: "★★★★★",
            OutputQuality.GOOD: "★★★★☆",
            OutputQuality.ACCEPTABLE: "★★★☆☆",
            OutputQuality.POOR: "★★☆☆☆",
            OutputQuality.UNACCEPTABLE: "★☆☆☆☆",
        }

        symbol = quality_symbols.get(verdict.quality, "?")
        status = "✓ ACCEPTED" if verdict.passed else "✗ REJECTED"

        logger.info(f"QUALITY: {symbol} {verdict.quality.value.upper()}")
        logger.info(f"STATUS:  {status}")
        logger.info(f"REASON:  {verdict.reason}\n")
        # Métricas
        m = verdict.metrics
        logger.info("METRICS:")
        logger.info(f"├─ LEI (Lazy Execution Index):     {m.lei:.2f}   {'✓' if m.lei < 1.0 else '✗'} (target: <1.0)")
        logger.info(f"├─ FPC (First-Pass Correctness):   {m.fpc:.1f}%  {'✓' if m.fpc >= 80.0 else '✗'} (target: ≥80%)")
        logger.info(f"├─ Lines of Code:                  {m.lines_of_code}")
        logger.info(f"└─ Violations:                     {m.total_violations} (Critical: {m.critical_violations}, High: {m.high_violations})\n")
        # Must-fix (se rejeitado)
        if verdict.must_fix:
            logger.info("MUST FIX (before re-submission):")
            for fix in verdict.must_fix:
                logger.info(f"  ✗ {fix}")
            print()

        # Suggestions
        if verdict.suggestions:
            logger.info("SUGGESTIONS:")
            for suggestion in verdict.suggestions:
                logger.info(f"  → {suggestion}")
            print()

        print("="*70 + "\n")


# ==================== HELPER FUNCTIONS ====================

def validate_final_output(
    code: str,
    language: str = 'python',
    context: Optional[Dict] = None,
    task_id: Optional[str] = None
) -> FinalVerdict:
    """
    Helper function para validar output final

    Args:
        code: Código gerado
        language: Linguagem
        context: Contexto
        task_id: ID da task

    Returns:
        FinalVerdict
    """
    from ..engine import get_constitutional_engine

    engine = get_constitutional_engine()
    guardian = PostExecutionGuardian(engine)

    return guardian.validate_output(code, language, context, task_id)
