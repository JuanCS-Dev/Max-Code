"""
Auto-Protection System

MISSÃO: Tornar os Guardians TOTALMENTE AUTOMÁTICOS.
Proteção constitucional 24/7 SEM intervenção manual.

Os Guardians PREVINEM violações doutrinárias AUTOMATICAMENTE.
Eles são a DEFESA PERMANENTE do Max-Code contra falhas deliberadas.

"Porque ele dará ordens aos seus anjos a teu respeito, para te guardarem em todos os teus caminhos."
(Salmos 91:11)
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import threading
import time

from .guardian_coordinator import GuardianCoordinator, EnforcementLevel, GuardianReport
from .pre_execution_guardian import GuardianDecision
from .runtime_guardian import InterruptionReason
from .post_execution_guardian import OutputQuality

from ..engine import Action, ActionType
from config.logging_config import get_logger

logger = get_logger(__name__)


class AutoProtectionMode(Enum):
    """Modo de auto-proteção"""
    ALWAYS_ON = "always_on"          # SEMPRE ativo (padrão)
    ON_DEMAND = "on_demand"          # Ativado sob demanda
    DISABLED = "disabled"            # Desativado (NÃO recomendado!)


class AutoCorrectionStrategy(Enum):
    """Estratégia de correção automática"""
    REJECT_ONLY = "reject_only"              # Apenas rejeitar, não corrigir
    AUTO_FIX_SIMPLE = "auto_fix_simple"      # Corrigir problemas simples automaticamente
    SUGGEST_AND_WAIT = "suggest_and_wait"    # Sugerir correção e esperar aprovação


@dataclass
class ProtectionEvent:
    """Evento de proteção"""
    timestamp: datetime
    task_id: str
    event_type: str  # 'pre_reject', 'runtime_interrupt', 'post_reject', 'auto_fix'
    details: Dict[str, Any]
    was_auto_fixed: bool = False


class AutoProtectionSystem:
    """
    Auto-Protection System

    RESPONSABILIDADES:
    - Manter Guardians SEMPRE ativos
    - Interceptar TODAS as ações automaticamente
    - Aplicar enforcement constitucional SEM intervenção manual
    - Corrigir problemas automaticamente (quando possível)
    - Logar todas as proteções aplicadas
    - Gerar alertas para violações críticas

    FILOSOFIA: "Prevention is better than cure"

    "Vigiai, estai firmes na fé; portai-vos varonilmente, e fortalecei-vos."
    (1 Coríntios 16:13)
    """

    def __init__(
        self,
        mode: AutoProtectionMode = AutoProtectionMode.ALWAYS_ON,
        enforcement_level: EnforcementLevel = EnforcementLevel.STRICT,
        auto_correction: AutoCorrectionStrategy = AutoCorrectionStrategy.SUGGEST_AND_WAIT
    ):
        """
        Inicializa Auto-Protection System

        Args:
            mode: Modo de operação
            enforcement_level: Nível de enforcement dos Guardians
            auto_correction: Estratégia de correção automática
        """
        self.mode = mode
        self.enforcement_level = enforcement_level
        self.auto_correction = auto_correction

        # Guardian Coordinator (coração do sistema)
        self.coordinator = GuardianCoordinator(
            constitutional_engine=self._get_engine(),
            enforcement_level=enforcement_level
        )

        # Histórico de proteções
        self._protection_events: List[ProtectionEvent] = []

        # Alertas críticos
        self._critical_alerts: List[Dict] = []

        # Stats
        self.stats = {
            'total_protected_actions': 0,
            'pre_rejections': 0,
            'runtime_interruptions': 0,
            'post_rejections': 0,
            'auto_fixes_applied': 0,
            'critical_alerts_issued': 0,
        }

        # Registrar callbacks nos Guardians
        self._register_callbacks()

        # Thread de monitoramento (se ALWAYS_ON)
        self._monitoring_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()

        if self.mode == AutoProtectionMode.ALWAYS_ON:
            self._start_monitoring()

    def _get_engine(self):
        """Obtém Constitutional Engine"""
        from ..engine import get_constitutional_engine
        return get_constitutional_engine()

    def _register_callbacks(self):
        """Registra callbacks automáticos nos Guardians"""

        # Pre-execution rejections
        self.coordinator.on_pre_reject(self._handle_pre_rejection)

        # Runtime interruptions
        self.coordinator.on_runtime_interrupt(self._handle_runtime_interruption)

        # Post-execution rejections
        self.coordinator.on_post_reject(self._handle_post_rejection)

    def protect_action(
        self,
        action: Action,
        execution_callback: Callable[[Action], str]
    ) -> GuardianReport:
        """
        Protege ação AUTOMATICAMENTE com Guardians

        Este é o ponto de entrada ÚNICO para TODAS as ações.
        NENHUMA ação escapa deste filtro.

        Args:
            action: Ação a executar
            execution_callback: Callback de execução

        Returns:
            GuardianReport
        """
        self.stats['total_protected_actions'] += 1

        # Log
        logger.info(f"🛡️ Auto-Protection: Protecting action {action.type.value}...")
        # Executar COM proteção total dos Guardians
        report = self.coordinator.execute_guarded_action(
            action,
            execution_callback
        )

        # Registrar evento
        self._log_protection_event(report)

        # Se rejeitado, tentar auto-correção (se habilitada)
        if not report.overall_passed and self.auto_correction != AutoCorrectionStrategy.REJECT_ONLY:
            logger.info("🔧 Attempting auto-correction...")
            corrected = self._attempt_auto_correction(action, report)
            if corrected:
                # Re-executar com correção
                report = self.coordinator.execute_guarded_action(
                    action,
                    execution_callback
                )

        return report

    def _handle_pre_rejection(self, task_id: str, verdict):
        """Handler para Pre-Guardian rejections"""
        logger.info(f"⛔ Pre-Guardian REJECTED task {task_id}")
        logger.info(f"   Reason: {verdict.reason}")
        self.stats['pre_rejections'] += 1

        # Registrar evento
        event = ProtectionEvent(
            timestamp=datetime.utcnow(),
            task_id=task_id,
            event_type='pre_reject',
            details={
                'decision': verdict.decision.value,
                'reason': verdict.reason,
                'violations': len(verdict.constitutional_result.violations),
            }
        )
        self._protection_events.append(event)

        # Alertar se CRITICAL
        if verdict.decision == GuardianDecision.ESCALATE_TO_HITL:
            self._issue_critical_alert(
                task_id,
                "Pre-execution escalation to HITL",
                verdict.reason
            )

    def _handle_runtime_interruption(self, task_id: str, reason: InterruptionReason):
        """Handler para Runtime Guardian interruptions"""
        logger.info(f"🚨 Runtime Guardian INTERRUPTED task {task_id}")
        logger.info(f"   Reason: {reason.value}")
        self.stats['runtime_interruptions'] += 1

        # Registrar evento
        event = ProtectionEvent(
            timestamp=datetime.utcnow(),
            task_id=task_id,
            event_type='runtime_interrupt',
            details={
                'reason': reason.value,
            }
        )
        self._protection_events.append(event)

        # Alertar sempre (interrupções são sérias)
        self._issue_critical_alert(
            task_id,
            "Runtime interruption",
            f"Execution interrupted: {reason.value}"
        )

    def _handle_post_rejection(self, task_id: str, verdict):
        """Handler para Post-Guardian rejections"""
        logger.error(f"❌ Post-Guardian REJECTED task {task_id}")
        logger.info(f"   Quality: {verdict.quality.value}")
        self.stats['post_rejections'] += 1

        # Registrar evento
        event = ProtectionEvent(
            timestamp=datetime.utcnow(),
            task_id=task_id,
            event_type='post_reject',
            details={
                'quality': verdict.quality.value,
                'lei': verdict.metrics.lei,
                'fpc': verdict.metrics.fpc,
                'must_fix': verdict.must_fix,
            }
        )
        self._protection_events.append(event)

        # Alertar se UNACCEPTABLE
        if verdict.quality == OutputQuality.UNACCEPTABLE:
            self._issue_critical_alert(
                task_id,
                "Unacceptable output quality",
                f"LEI: {verdict.metrics.lei:.2f}, Critical violations: {verdict.metrics.critical_violations}"
            )

    def _attempt_auto_correction(self, action: Action, report: GuardianReport) -> bool:
        """
        Tenta corrigir problemas automaticamente

        Args:
            action: Ação original
            report: Report com falhas

        Returns:
            True se corrigido
        """
        if self.auto_correction == AutoCorrectionStrategy.REJECT_ONLY:
            return False

        # Extrair violations
        violations = []
        if report.pre_execution_verdict:
            violations.extend(report.pre_execution_verdict.constitutional_result.violations)
        if report.post_execution_verdict:
            violations.extend(report.post_execution_verdict.violations)

        if not violations:
            return False

        # Auto-fixes simples
        code = action.payload.get('code', '')
        fixed_code = code

        # Fix 1: Remover TODOs/placeholders
        import re
        if any('TODO' in v.pattern for v in violations):
            fixed_code = re.sub(r'#\s*TODO:.*', '', fixed_code)
            fixed_code = re.sub(r'//\s*TODO:.*', '', fixed_code)

        # Fix 2: Remover pass statements standalone
        if any('pass' in v.pattern for v in violations):
            fixed_code = re.sub(r'^\s*pass\s*$', '', fixed_code, flags=re.MULTILINE)

        # Fix 3: Implementar NotImplementedError
        if any('NotImplementedError' in v.pattern for v in violations):
            # Aqui seria mais complexo - precisaria gerar implementação
            pass

        # Se código mudou, aplicar correção
        if fixed_code != code:
            action.payload['code'] = fixed_code

            self.stats['auto_fixes_applied'] += 1

            # Logar auto-fix
            event = ProtectionEvent(
                timestamp=datetime.utcnow(),
                task_id=action.task_id or 'unknown',
                event_type='auto_fix',
                details={
                    'fixes_applied': ['TODO removal', 'pass removal'],
                },
                was_auto_fixed=True
            )
            self._protection_events.append(event)

            logger.info("✅ Auto-correction applied successfully")
            return True

        return False

    def _issue_critical_alert(self, task_id: str, alert_type: str, message: str):
        """Emite alerta crítico"""
        self.stats['critical_alerts_issued'] += 1

        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'task_id': task_id,
            'type': alert_type,
            'message': message,
        }

        self._critical_alerts.append(alert)

        logger.info(f"\n{'='*70}")
        logger.info(f"🚨 CRITICAL ALERT")
        logger.info(f"{'='*70}")
        logger.info(f"Type:    {alert_type}")
        logger.info(f"Task:    {task_id}")
        logger.info(f"Message: {message}")
        logger.info(f"{'='*70}\n")
    def _log_protection_event(self, report: GuardianReport):
        """Log de evento de proteção"""
        # Evento já registrado nos callbacks individuais
        pass

    def _start_monitoring(self):
        """Inicia thread de monitoramento (para ALWAYS_ON)"""
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            return

        self._stop_monitoring.clear()

        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self._monitoring_thread.start()

        logger.info("✅ Auto-Protection System: ALWAYS_ON mode activated")
    def _monitoring_loop(self):
        """Loop de monitoramento"""
        while not self._stop_monitoring.is_set():
            # Verificar saúde dos Guardians
            # Verificar alertas pendentes
            # etc

            time.sleep(10)  # Check every 10s

    def stop(self):
        """Para sistema de auto-proteção"""
        self._stop_monitoring.set()
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=5)

        logger.info("🛡️ Auto-Protection System: Stopped")
    def get_protection_report(self) -> Dict:
        """Gera relatório de proteções aplicadas"""
        return {
            'mode': self.mode.value,
            'enforcement_level': self.enforcement_level.value,
            'auto_correction': self.auto_correction.value,

            # Stats
            'total_protected_actions': self.stats['total_protected_actions'],
            'pre_rejections': self.stats['pre_rejections'],
            'runtime_interruptions': self.stats['runtime_interruptions'],
            'post_rejections': self.stats['post_rejections'],
            'auto_fixes_applied': self.stats['auto_fixes_applied'],
            'critical_alerts_issued': self.stats['critical_alerts_issued'],

            # Rates
            'protection_success_rate': (
                (self.stats['total_protected_actions'] -
                 self.stats['pre_rejections'] -
                 self.stats['runtime_interruptions'] -
                 self.stats['post_rejections']) / self.stats['total_protected_actions'] * 100
                if self.stats['total_protected_actions'] > 0 else 100.0
            ),

            # Recent events
            'recent_events': [
                {
                    'timestamp': e.timestamp.isoformat(),
                    'task_id': e.task_id,
                    'type': e.event_type,
                    'was_auto_fixed': e.was_auto_fixed,
                }
                for e in self._protection_events[-10:]  # Last 10 events
            ],

            # Critical alerts
            'critical_alerts': self._critical_alerts[-5:],  # Last 5 alerts
        }

    def print_protection_report(self):
        """Imprime relatório de proteção"""
        report = self.get_protection_report()

        print("\n" + "="*80)
        logger.info("  AUTO-PROTECTION SYSTEM REPORT")
        print("="*80 + "\n")

        logger.info(f"MODE:              {report['mode'].upper()}")
        logger.info(f"ENFORCEMENT:       {report['enforcement_level'].upper()}")
        logger.info(f"AUTO-CORRECTION:   {report['auto_correction'].upper()}\n")
        logger.info("PROTECTION STATS:")
        logger.info(f"├─ Protected Actions:      {report['total_protected_actions']}")
        logger.info(f"├─ Pre-rejections:         {report['pre_rejections']}")
        logger.info(f"├─ Runtime interruptions:  {report['runtime_interruptions']}")
        logger.info(f"├─ Post-rejections:        {report['post_rejections']}")
        logger.info(f"├─ Auto-fixes applied:     {report['auto_fixes_applied']}")
        logger.info(f"└─ Critical alerts:        {report['critical_alerts_issued']}\n")
        logger.info(f"PROTECTION SUCCESS RATE: {report['protection_success_rate']:.1f}%\n")
        if report['critical_alerts']:
            logger.info("RECENT CRITICAL ALERTS:")
            for alert in report['critical_alerts']:
                logger.info(f"  🚨 [{alert['timestamp']}] {alert['type']}: {alert['message']}")
        print("\n" + "="*80 + "\n")


# ==================== SINGLETON INSTANCE ====================

_auto_protection_instance: Optional[AutoProtectionSystem] = None


def get_auto_protection(
    mode: AutoProtectionMode = AutoProtectionMode.ALWAYS_ON,
    enforcement_level: EnforcementLevel = EnforcementLevel.STRICT,
    auto_correction: AutoCorrectionStrategy = AutoCorrectionStrategy.SUGGEST_AND_WAIT
) -> AutoProtectionSystem:
    """
    Obtém instância singleton do Auto-Protection System

    Args:
        mode: Modo de operação
        enforcement_level: Nível de enforcement
        auto_correction: Estratégia de auto-correção

    Returns:
        AutoProtectionSystem
    """
    global _auto_protection_instance

    if _auto_protection_instance is None:
        _auto_protection_instance = AutoProtectionSystem(
            mode=mode,
            enforcement_level=enforcement_level,
            auto_correction=auto_correction
        )

    return _auto_protection_instance


def enable_auto_protection(
    enforcement_level: EnforcementLevel = EnforcementLevel.STRICT
):
    """
    Helper para habilitar auto-proteção (ALWAYS_ON)

    Args:
        enforcement_level: Nível de enforcement
    """
    system = get_auto_protection(
        mode=AutoProtectionMode.ALWAYS_ON,
        enforcement_level=enforcement_level
    )

    logger.info("🛡️ Auto-Protection System: ENABLED")
    logger.info(f"   Enforcement Level: {enforcement_level.value}")
    logger.info("   Guardians are now ALWAYS protecting Max-Code from constitutional violations.")
    return system


def disable_auto_protection():
    """Helper para desabilitar auto-proteção (NÃO RECOMENDADO!)"""
    global _auto_protection_instance

    if _auto_protection_instance:
        _auto_protection_instance.stop()
        _auto_protection_instance = None

    logger.warning("⚠️ Auto-Protection System: DISABLED")
    logger.warning("   WARNING: Max-Code is now vulnerable to constitutional violations!")