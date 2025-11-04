"""
Guardian Coordinator

MISSÃO: Coordenar os 3 Guardians (Pre, Runtime, Post) em orquestração perfeita.
AUTORIDADE: SUPREMA - controla TODO o ciclo de enforcement constitucional.

Este é o MAESTRO que rege a sinfonia constitucional.
Ele garante que NADA escapa da vigilância dos Guardians.

"E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos pensamentos em Cristo Jesus."
(Filipenses 4:7)
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .pre_execution_guardian import PreExecutionGuardian, GuardianVerdict, GuardianDecision
from .runtime_guardian import RuntimeGuardian, ExecutionPhase, InterruptionReason
from .post_execution_guardian import PostExecutionGuardian, FinalVerdict, OutputQuality

from ..engine import ConstitutionalEngine, Action, ActionType


class EnforcementLevel(Enum):
    """Nível de enforcement"""
    STRICT = "strict"      # Zero tolerância - qualquer CRITICAL bloqueia
    BALANCED = "balanced"  # Tolerância mínima - múltiplos HIGH bloqueiam
    LENIENT = "lenient"    # Mais permissivo - apenas CRITICAL múltiplos bloqueiam


@dataclass
class GuardianReport:
    """Relatório completo dos Guardians"""
    task_id: str
    started_at: datetime
    completed_at: Optional[datetime]

    # Pre-execution
    pre_execution_verdict: GuardianVerdict

    # Runtime
    runtime_report: Optional[Dict]
    was_interrupted: bool
    interruption_reason: Optional[InterruptionReason]

    # Post-execution
    post_execution_verdict: Optional[FinalVerdict]

    # Overall
    overall_passed: bool
    enforcement_level: EnforcementLevel

    # Metrics
    total_iterations: int
    total_violations: int
    constitutional_score: float


class GuardianCoordinator:
    """
    Guardian Coordinator

    RESPONSABILIDADES:
    - Coordenar Pre, Runtime, Post Guardians
    - Orquestrar enforcement constitucional end-to-end
    - Decidir se action pode prosseguir em cada fase
    - Coletar métricas agregadas
    - Gerar relatório completo

    AUTORIDADE: SUPREMA - pode bloquear em QUALQUER fase

    "O Senhor é o meu pastor, nada me faltará."
    (Salmos 23:1)
    """

    def __init__(
        self,
        constitutional_engine: ConstitutionalEngine,
        enforcement_level: EnforcementLevel = EnforcementLevel.STRICT
    ):
        """
        Inicializa Coordinator

        Args:
            constitutional_engine: Engine constitucional
            enforcement_level: Nível de enforcement
        """
        self.engine = constitutional_engine
        self.enforcement_level = enforcement_level

        # Criar Guardians
        self.pre_guardian = PreExecutionGuardian(constitutional_engine)
        self.runtime_guardian = RuntimeGuardian(
            constitutional_engine.validators['P6']
        )
        self.post_guardian = PostExecutionGuardian(constitutional_engine)

        # Reports ativos
        self._active_reports: Dict[str, GuardianReport] = {}

        # Callbacks
        self._on_pre_reject_callbacks: List[Callable[[str, GuardianVerdict], None]] = []
        self._on_runtime_interrupt_callbacks: List[Callable[[str, InterruptionReason], None]] = []
        self._on_post_reject_callbacks: List[Callable[[str, FinalVerdict], None]] = []

        # Stats agregadas
        self.stats = {
            'total_actions': 0,
            'pre_rejected': 0,
            'runtime_interrupted': 0,
            'post_rejected': 0,
            'fully_approved': 0,
        }

        # Registrar callback de interrupção no runtime guardian
        self.runtime_guardian.on_interruption(self._handle_runtime_interruption)

    def execute_guarded_action(
        self,
        action: Action,
        execution_callback: Callable[[Action], str]
    ) -> GuardianReport:
        """
        Executa ação SOB PROTEÇÃO CONSTITUCIONAL COMPLETA

        Este método:
        1. PRE-VALIDATION (Pre-Guardian)
        2. RUNTIME MONITORING (Runtime Guardian)
        3. EXECUTION (via callback)
        4. POST-VALIDATION (Post-Guardian)

        Args:
            action: Ação a executar
            execution_callback: Função que executa a ação e retorna código gerado

        Returns:
            GuardianReport com resultado completo
        """
        self.stats['total_actions'] += 1

        task_id = action.task_id or f"task_{datetime.utcnow().timestamp()}"
        action.task_id = task_id

        started_at = datetime.utcnow()

        # ============================================================
        # FASE 1: PRE-EXECUTION VALIDATION
        # ============================================================
        print("\n⏳ E o Verbo se fez carne... (João 1:14) - Validating action...")

        pre_verdict = self.pre_guardian.validate_action(action)

        # Criar report
        report = GuardianReport(
            task_id=task_id,
            started_at=started_at,
            completed_at=None,
            pre_execution_verdict=pre_verdict,
            runtime_report=None,
            was_interrupted=False,
            interruption_reason=None,
            post_execution_verdict=None,
            overall_passed=False,
            enforcement_level=self.enforcement_level,
            total_iterations=0,
            total_violations=len(pre_verdict.constitutional_result.violations),
            constitutional_score=pre_verdict.constitutional_result.constitutional_score
        )

        self._active_reports[task_id] = report

        # Verificar se pode prosseguir
        if not pre_verdict.should_proceed:
            print("✗ Pre-execution Guardian REJECTED action")
            self.stats['pre_rejected'] += 1

            # Invocar callbacks
            for callback in self._on_pre_reject_callbacks:
                callback(task_id, pre_verdict)

            report.completed_at = datetime.utcnow()
            return report

        print("✓ Pre-execution Guardian APPROVED")

        # ============================================================
        # FASE 2: RUNTIME MONITORING + EXECUTION
        # ============================================================
        print("⏳ Vigiai e orai... (Mateus 26:41) - Monitoring execution...")

        self.runtime_guardian.start_monitoring(task_id)
        self.runtime_guardian.update_phase(task_id, ExecutionPhase.GENERATING)

        # Executar via callback
        try:
            generated_code = execution_callback(action)
        except Exception as e:
            print(f"✗ Execution failed: {e}")
            self.runtime_guardian.update_phase(task_id, ExecutionPhase.FAILED)
            report.completed_at = datetime.utcnow()
            return report

        # Completar monitoring
        self.runtime_guardian.complete_session(task_id)
        runtime_report = self.runtime_guardian.get_session_report(task_id)

        report.runtime_report = runtime_report
        report.was_interrupted = runtime_report.get('was_interrupted', False)
        report.interruption_reason = (
            InterruptionReason(runtime_report['interruption_reason'])
            if runtime_report.get('interruption_reason') else None
        )
        report.total_iterations = runtime_report.get('iterations', 0)

        # Se foi interrompido, parar aqui
        if report.was_interrupted:
            print(f"✗ Runtime Guardian INTERRUPTED: {report.interruption_reason.value}")
            self.stats['runtime_interrupted'] += 1
            report.completed_at = datetime.utcnow()
            return report

        print("✓ Runtime Guardian: Execution completed")

        # ============================================================
        # FASE 3: POST-EXECUTION VALIDATION
        # ============================================================
        print("⏳ Examinai tudo... (1 Tessalonicenses 5:21) - Validating output...")

        language = action.payload.get('language', 'python')
        context = action.metadata

        post_verdict = self.post_guardian.validate_output(
            generated_code,
            language,
            context,
            task_id
        )

        report.post_execution_verdict = post_verdict
        report.total_violations += len(post_verdict.violations)

        # Verificar se passou
        if not post_verdict.passed:
            print(f"✗ Post-execution Guardian REJECTED: {post_verdict.quality.value}")
            self.stats['post_rejected'] += 1

            # Invocar callbacks
            for callback in self._on_post_reject_callbacks:
                callback(task_id, post_verdict)

            report.completed_at = datetime.utcnow()
            return report

        print(f"✓ Post-execution Guardian APPROVED: {post_verdict.quality.value}")

        # ============================================================
        # APROVAÇÃO COMPLETA!
        # ============================================================
        report.overall_passed = True
        report.completed_at = datetime.utcnow()
        self.stats['fully_approved'] += 1

        print("✓ GUARDIAN COORDINATION: FULLY APPROVED")

        return report

    def _handle_runtime_interruption(self, task_id: str, reason: InterruptionReason):
        """Handler para interrupções do runtime guardian"""
        for callback in self._on_runtime_interrupt_callbacks:
            try:
                callback(task_id, reason)
            except Exception as e:
                print(f"[GuardianCoordinator] Error in runtime interrupt callback: {e}")

    def on_pre_reject(self, callback: Callable[[str, GuardianVerdict], None]):
        """Registra callback para rejeições pre-execution"""
        self._on_pre_reject_callbacks.append(callback)

    def on_runtime_interrupt(self, callback: Callable[[str, InterruptionReason], None]):
        """Registra callback para interrupções runtime"""
        self._on_runtime_interrupt_callbacks.append(callback)

    def on_post_reject(self, callback: Callable[[str, FinalVerdict], None]):
        """Registra callback para rejeições post-execution"""
        self._on_post_reject_callbacks.append(callback)

    def get_report(self, task_id: str) -> Optional[GuardianReport]:
        """Obtém report de uma task"""
        return self._active_reports.get(task_id)

    def get_stats(self) -> Dict:
        """Retorna estatísticas agregadas"""
        return {
            **self.stats,
            'approval_rate': (
                self.stats['fully_approved'] / self.stats['total_actions'] * 100
                if self.stats['total_actions'] > 0 else 100.0
            ),
            'pre_rejection_rate': (
                self.stats['pre_rejected'] / self.stats['total_actions'] * 100
                if self.stats['total_actions'] > 0 else 0.0
            ),
            'runtime_interruption_rate': (
                self.stats['runtime_interrupted'] / self.stats['total_actions'] * 100
                if self.stats['total_actions'] > 0 else 0.0
            ),
            'post_rejection_rate': (
                self.stats['post_rejected'] / self.stats['total_actions'] * 100
                if self.stats['total_actions'] > 0 else 0.0
            ),
        }

    def print_full_report(self, report: GuardianReport):
        """Imprime relatório completo (formato bonito)"""
        print("\n" + "="*80)
        print("  GUARDIAN COORDINATION REPORT")
        print("="*80 + "\n")

        # Task info
        print(f"TASK ID:          {report.task_id}")
        print(f"STARTED:          {report.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if report.completed_at:
            elapsed = (report.completed_at - report.started_at).total_seconds()
            print(f"COMPLETED:        {report.completed_at.strftime('%Y-%m-%d %H:%M:%S')} ({elapsed:.1f}s)")
        print(f"ENFORCEMENT:      {report.enforcement_level.value.upper()}\n")

        # Overall status
        status = "✓ APPROVED" if report.overall_passed else "✗ REJECTED"
        print(f"OVERALL STATUS:   {status}")
        print(f"ITERATIONS:       {report.total_iterations}")
        print(f"TOTAL VIOLATIONS: {report.total_violations}")
        print(f"CONST. SCORE:     {report.constitutional_score:.2f}\n")

        # Phase breakdown
        print("PHASE BREAKDOWN:")
        print("├─ PRE-EXECUTION:  ", end="")
        if report.pre_execution_verdict.should_proceed:
            print("✓ Approved")
        else:
            print(f"✗ Rejected ({report.pre_execution_verdict.decision.value})")

        print("├─ RUNTIME:        ", end="")
        if report.was_interrupted:
            print(f"✗ Interrupted ({report.interruption_reason.value})")
        else:
            print("✓ Completed")

        print("└─ POST-EXECUTION: ", end="")
        if report.post_execution_verdict:
            if report.post_execution_verdict.passed:
                print(f"✓ Approved ({report.post_execution_verdict.quality.value})")
            else:
                print(f"✗ Rejected ({report.post_execution_verdict.quality.value})")
        else:
            print("(not reached)")

        print("\n" + "="*80 + "\n")


# ==================== SINGLETON INSTANCE ====================

_coordinator_instance: Optional[GuardianCoordinator] = None


def get_guardian_coordinator(
    enforcement_level: EnforcementLevel = EnforcementLevel.STRICT
) -> GuardianCoordinator:
    """Obtém instância singleton do coordinator"""
    global _coordinator_instance

    if _coordinator_instance is None:
        from ..engine import get_constitutional_engine
        engine = get_constitutional_engine()
        _coordinator_instance = GuardianCoordinator(engine, enforcement_level)

    return _coordinator_instance


def execute_with_guardians(
    action: Action,
    execution_callback: Callable[[Action], str],
    enforcement_level: EnforcementLevel = EnforcementLevel.STRICT
) -> GuardianReport:
    """
    Helper function para executar ação com proteção completa dos Guardians

    Args:
        action: Ação
        execution_callback: Função de execução
        enforcement_level: Nível de enforcement

    Returns:
        GuardianReport
    """
    coordinator = get_guardian_coordinator(enforcement_level)
    return coordinator.execute_guarded_action(action, execution_callback)
