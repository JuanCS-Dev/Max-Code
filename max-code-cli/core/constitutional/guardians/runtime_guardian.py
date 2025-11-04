"""
Runtime Guardian

MISSÃO: Monitorar conformidade constitucional DURANTE execução.
AUTORIDADE: Pode INTERROMPER execução se violação detectada.

Este Guardian vigia ATIVAMENTE durante execução.
Se algo violar a constituição, ele PARA tudo.

"Vigiai e orai, para que não entreis em tentação; o espírito, na verdade, está pronto, mas a carne é fraca."
(Mateus 26:41)
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
import time

from ..validators.p6_token_efficiency import P6_Token_Efficiency_Monitor
from ..validators.p1_completeness import ViolationSeverity, Violation


class ExecutionPhase(Enum):
    """Fase de execução"""
    NOT_STARTED = "not_started"
    INITIALIZING = "initializing"
    PLANNING = "planning"
    GENERATING = "generating"
    VALIDATING = "validating"
    COMPLETING = "completing"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"
    FAILED = "failed"


class InterruptionReason(Enum):
    """Razão de interrupção"""
    MAX_ITERATIONS_EXCEEDED = "max_iterations_exceeded"
    CIRCULAR_ERROR = "circular_error"
    CRITICAL_VIOLATION = "critical_violation"
    TIMEOUT = "timeout"
    RESOURCE_LIMIT = "resource_limit"
    USER_REQUESTED = "user_requested"


@dataclass
class RuntimeSnapshot:
    """Snapshot do estado de runtime"""
    timestamp: datetime
    phase: ExecutionPhase
    iteration_num: int
    violations: List[Violation]
    metrics: Dict[str, Any]


@dataclass
class ExecutionSession:
    """Sessão de execução monitorada"""
    task_id: str
    started_at: datetime
    phase: ExecutionPhase = ExecutionPhase.NOT_STARTED
    current_iteration: int = 0
    snapshots: List[RuntimeSnapshot] = field(default_factory=list)
    violations_detected: List[Violation] = field(default_factory=list)
    was_interrupted: bool = False
    interruption_reason: Optional[InterruptionReason] = None
    completed_at: Optional[datetime] = None


class RuntimeGuardian:
    """
    Runtime Guardian

    RESPONSABILIDADES:
    - Monitorar execução em tempo real
    - Detectar violations durante execução
    - Interromper se necessário (P6 violations, erros circulares, etc)
    - Coletar snapshots de estado
    - Aplicar limites de recursos

    AUTORIDADE: Pode INTERROMPER execução

    "O Senhor guardará a tua entrada e a tua saída, desde agora e para sempre."
    (Salmos 121:8)
    """

    def __init__(
        self,
        token_monitor: P6_Token_Efficiency_Monitor,
        max_execution_time_seconds: int = 600  # 10 min default
    ):
        """
        Inicializa Guardian

        Args:
            token_monitor: Monitor P6 (token efficiency)
            max_execution_time_seconds: Timeout de execução
        """
        self.token_monitor = token_monitor
        self.max_execution_time = max_execution_time_seconds

        # Sessões ativas
        self._active_sessions: Dict[str, ExecutionSession] = {}

        # Thread de monitoramento
        self._monitoring_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()

        # Callbacks de interrupção
        self._interruption_callbacks: List[Callable[[str, InterruptionReason], None]] = []

        # Stats
        self.stats = {
            'sessions_monitored': 0,
            'sessions_completed': 0,
            'sessions_interrupted': 0,
            'violations_detected': 0,
        }

    def start_monitoring(self, task_id: str):
        """
        Inicia monitoramento de uma task

        Args:
            task_id: ID da task
        """
        self.stats['sessions_monitored'] += 1

        session = ExecutionSession(
            task_id=task_id,
            started_at=datetime.utcnow(),
            phase=ExecutionPhase.INITIALIZING
        )

        self._active_sessions[task_id] = session

        # Iniciar token monitoring (P6)
        self.token_monitor.start_task(task_id)

        # Capturar snapshot inicial
        self._take_snapshot(task_id)

    def update_phase(self, task_id: str, phase: ExecutionPhase):
        """
        Atualiza fase de execução

        Args:
            task_id: ID da task
            phase: Nova fase
        """
        if task_id not in self._active_sessions:
            return

        session = self._active_sessions[task_id]
        session.phase = phase

        self._take_snapshot(task_id)

    def record_iteration(
        self,
        task_id: str,
        had_diagnosis: bool,
        error_message: Optional[str] = None,
        fix_applied: Optional[str] = None,
        success: bool = False
    ) -> bool:
        """
        Registra iteração e VERIFICA se deve continuar

        Args:
            task_id: ID da task
            had_diagnosis: Se houve diagnóstico
            error_message: Mensagem de erro
            fix_applied: Fix aplicado
            success: Se teve sucesso

        Returns:
            True se pode continuar, False se deve INTERROMPER
        """
        if task_id not in self._active_sessions:
            return True

        session = self._active_sessions[task_id]
        session.current_iteration += 1

        # Registrar no P6 monitor
        result = self.token_monitor.record_iteration(
            task_id,
            had_diagnosis,
            error_message,
            fix_applied,
            success
        )

        # Verificar violations
        if result.violations:
            session.violations_detected.extend(result.violations)
            self.stats['violations_detected'] += len(result.violations)

            # Verificar se há CRITICAL violations
            critical = [v for v in result.violations if v.severity == ViolationSeverity.CRITICAL]

            if critical:
                # INTERROMPER!
                reason = self._determine_interruption_reason(critical)
                self._interrupt_session(task_id, reason)
                return False

        # Verificar timeout
        elapsed = (datetime.utcnow() - session.started_at).total_seconds()
        if elapsed > self.max_execution_time:
            self._interrupt_session(task_id, InterruptionReason.TIMEOUT)
            return False

        # Verificar se P6 permite continuar
        should_continue, reason = self.token_monitor.should_continue(task_id)
        if not should_continue:
            # Mapear reason para InterruptionReason
            if "circular" in reason.lower():
                interruption_reason = InterruptionReason.CIRCULAR_ERROR
            elif "max iterations" in reason.lower():
                interruption_reason = InterruptionReason.MAX_ITERATIONS_EXCEEDED
            else:
                interruption_reason = InterruptionReason.CRITICAL_VIOLATION

            self._interrupt_session(task_id, interruption_reason)
            return False

        # Snapshot
        self._take_snapshot(task_id)

        return True

    def complete_session(self, task_id: str):
        """
        Completa sessão com sucesso

        Args:
            task_id: ID da task
        """
        if task_id not in self._active_sessions:
            return

        session = self._active_sessions[task_id]
        session.phase = ExecutionPhase.COMPLETED
        session.completed_at = datetime.utcnow()

        self.stats['sessions_completed'] += 1

        # Snapshot final
        self._take_snapshot(task_id)

    def _interrupt_session(self, task_id: str, reason: InterruptionReason):
        """
        Interrompe sessão

        Args:
            task_id: ID da task
            reason: Razão da interrupção
        """
        if task_id not in self._active_sessions:
            return

        session = self._active_sessions[task_id]
        session.phase = ExecutionPhase.INTERRUPTED
        session.was_interrupted = True
        session.interruption_reason = reason
        session.completed_at = datetime.utcnow()

        self.stats['sessions_interrupted'] += 1

        # Invocar callbacks
        for callback in self._interruption_callbacks:
            try:
                callback(task_id, reason)
            except Exception as e:
                print(f"[RuntimeGuardian] Error in interruption callback: {e}")

        # Snapshot final
        self._take_snapshot(task_id)

    def _determine_interruption_reason(self, violations: List[Violation]) -> InterruptionReason:
        """Determina razão de interrupção com base em violations"""
        for v in violations:
            if "max iterations" in v.message.lower():
                return InterruptionReason.MAX_ITERATIONS_EXCEEDED
            elif "circular" in v.message.lower():
                return InterruptionReason.CIRCULAR_ERROR

        return InterruptionReason.CRITICAL_VIOLATION

    def _take_snapshot(self, task_id: str):
        """Captura snapshot do estado atual"""
        if task_id not in self._active_sessions:
            return

        session = self._active_sessions[task_id]

        snapshot = RuntimeSnapshot(
            timestamp=datetime.utcnow(),
            phase=session.phase,
            iteration_num=session.current_iteration,
            violations=session.violations_detected.copy(),
            metrics={
                'elapsed_seconds': (datetime.utcnow() - session.started_at).total_seconds(),
            }
        )

        session.snapshots.append(snapshot)

    def on_interruption(self, callback: Callable[[str, InterruptionReason], None]):
        """
        Registra callback para interrupções

        Args:
            callback: Função a chamar quando interromper
        """
        self._interruption_callbacks.append(callback)

    def get_session_report(self, task_id: str) -> Optional[Dict]:
        """
        Gera relatório da sessão

        Args:
            task_id: ID da task

        Returns:
            Dict com relatório ou None
        """
        if task_id not in self._active_sessions:
            return None

        session = self._active_sessions[task_id]

        elapsed = (
            (session.completed_at or datetime.utcnow()) - session.started_at
        ).total_seconds()

        return {
            'task_id': task_id,
            'phase': session.phase.value,
            'iterations': session.current_iteration,
            'elapsed_seconds': elapsed,
            'was_interrupted': session.was_interrupted,
            'interruption_reason': session.interruption_reason.value if session.interruption_reason else None,
            'violations_detected': len(session.violations_detected),
            'snapshots_captured': len(session.snapshots),
        }

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
            'active_sessions': len(self._active_sessions),
            'interruption_rate': (
                self.stats['sessions_interrupted'] / self.stats['sessions_monitored'] * 100
                if self.stats['sessions_monitored'] > 0 else 0.0
            ),
        }


# ==================== HELPER FUNCTIONS ====================

_runtime_guardian_instance: Optional[RuntimeGuardian] = None


def get_runtime_guardian() -> RuntimeGuardian:
    """Obtém instância singleton do runtime guardian"""
    global _runtime_guardian_instance

    if _runtime_guardian_instance is None:
        from ..validators.p6_token_efficiency import get_monitor
        monitor = get_monitor()
        _runtime_guardian_instance = RuntimeGuardian(monitor)

    return _runtime_guardian_instance
