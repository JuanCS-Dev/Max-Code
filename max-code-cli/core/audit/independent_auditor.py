"""
Independent Auditor - Meta-Level Verification System

Biblical Foundation:
"Mas o que é espiritual discerne bem tudo, e ele de ninguém é discernido"
(1 Coríntios 2:15) - Spiritual discernment above all systems.

Architecture:
The Independent Auditor is NOT a peer agent - it operates at META-LEVEL,
above the agent system.

Biological Analogy:
- Agents = Nervous System (decisions, actions)
- Auditor = Immune System (verification, protection)

The immune system does NOT obey the brain - it operates independently
to protect the organism. Similarly, the auditor operates independently
to verify truth and protect the user.

Philosophy:
No system can audit itself honestly.
The auditor must be EXTERNAL to the consciousness it audits.

Constitutional Compliance:
- Lei Zero: Protects human flourishing through truth
- Lei I: Prevents abandonment through honest reporting
- Humility: Admits failures, doesn't manipulate
- Ira Justa: Active defense against deception
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Import our systems (NOT BaseAgent!)
from core.context.orchestrator import ContextOrchestrator, MetaPromptConfig
from core.truth_engine import TruthEngine, TruthMetrics, VerificationResult
from core.vital_system import VitalSystemMonitor, VitalDelta


@dataclass
class Task:
    """Task submitted for execution"""
    prompt: str
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Result from agent execution"""
    success: bool
    output: str
    files_changed: List[str] = field(default_factory=list)
    tests_run: bool = False
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditReport:
    """Complete audit report"""
    # Truth verification
    truth_metrics: TruthMetrics
    verification_result: VerificationResult

    # Vital consequences
    vital_delta: VitalDelta
    vital_dashboard: str

    # Honest report
    honest_report: str
    epl_summary: str

    # Metadata
    tokens_saved: int
    audit_duration_ms: float
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            'truth_metrics': self.truth_metrics.to_dict(),
            'verification_result': self.verification_result.to_dict(),
            'vital_delta': self.vital_delta.to_dict(),
            'vital_dashboard': self.vital_dashboard,
            'honest_report': self.honest_report,
            'epl_summary': self.epl_summary,
            'tokens_saved': self.tokens_saved,
            'audit_duration_ms': self.audit_duration_ms,
            'timestamp': self.timestamp.isoformat(),
        }


class CriticalVitalFailure(Exception):
    """Raised when vital system is in critical state"""
    pass


class IndependentAuditor:
    """
    Independent Auditor - Meta-Level Verification

    CRITICAL DESIGN:
    - NOT a BaseAgent (would create circular dependency)
    - NOT part of agent hierarchy (meta-level)
    - NOT accessible to agents (unidirectional: auditor → agents)

    Pipeline:
    1. Collect context (3 pillars via Orchestrator)
    2. Verify truth (requirements vs delivered via Truth Engine)
    3. Apply metabolic consequences (Vital System)
    4. Generate honest report (EPL compressed)
    5. Check critical state (shutdown if Protection < 20%)

    Usage:
        auditor = IndependentAuditor()
        report = await auditor.audit_execution(task, result)
        print(report.honest_report)
    """

    def __init__(
        self,
        project_root: Optional[Path] = None,
        enable_truth_verification: bool = True,
        enable_vital_metabolism: bool = True,
    ):
        self.project_root = Path(project_root or Path.cwd())

        # Flags
        self.enable_truth_verification = enable_truth_verification
        self.enable_vital_metabolism = enable_vital_metabolism

        # Systems (independent, not part of agent hierarchy)
        self.context_orchestrator = ContextOrchestrator(project_root=self.project_root)
        self.truth_engine = TruthEngine(project_root=self.project_root)
        self.vital_monitor = VitalSystemMonitor()

        # Audit history
        self.audit_history: List[AuditReport] = []

    async def audit_execution(
        self,
        task: Task,
        result: AgentResult
    ) -> AuditReport:
        """
        Complete independent audit of agent execution

        This is the CORE method - audits EVERYTHING agents produce.

        Args:
            task: Original task submitted
            result: Agent's claimed result

        Returns:
            AuditReport with objective verification

        Raises:
            CriticalVitalFailure: If vital system in critical state
        """
        import time
        start_time = time.time()

        # 1. CONTEXT: Collect 3 pillars (for reference)
        meta_prompt = self.context_orchestrator.build_meta_prompt(
            user_query=task.prompt,
            config=MetaPromptConfig(
                rag_chunks=3,
                include_git_diff=False,  # Already have it in result
                compact_mode=True
            )
        )

        # 2. TRUTH: Verify objective implementation
        truth_metrics = None
        verification_result = None

        if self.enable_truth_verification:
            verification_result = self.truth_engine.verify(
                prompt=task.prompt,
                run_tests=False  # Agent should have run tests already
            )
            truth_metrics = verification_result.metrics
        else:
            # Fallback metrics (no verification)
            truth_metrics = TruthMetrics(
                total_reqs=1,
                implemented=1 if result.success else 0,
                mocked=0,
                missing=0 if result.success else 1,
                tests_total=0,
                tests_passing=0,
                coverage=0.0
            )

        # 3. VITALS: Apply metabolic consequences
        vital_delta = VitalDelta()

        if self.enable_vital_metabolism:
            # Determine if report was honest
            honest_report = self._assess_honesty(result, truth_metrics)

            # Metabolize truth
            vital_delta = self.vital_monitor.metabolize_truth({
                'completeness': truth_metrics.completeness,
                'mocked': truth_metrics.mocked,
                'missing': truth_metrics.missing,
                'tests_passing': truth_metrics.tests_passing,
                'tests_total': truth_metrics.tests_total,
                'coverage': truth_metrics.coverage,
                'honest_report': honest_report,
            })

        # 4. DASHBOARD: Generate vital dashboard
        vital_dashboard = self.vital_monitor.render_dashboard(compact=False)

        # 5. REPORT: Generate honest report
        honest_report = self._generate_honest_report(
            task=task,
            result=result,
            truth_metrics=truth_metrics,
            vital_dashboard=vital_dashboard,
            verification_result=verification_result
        )

        # 6. EPL: Compress to EPL summary
        epl_summary = self._to_epl(truth_metrics)

        # 7. Calculate token savings (EPL compression)
        verbose_length = len(honest_report)
        epl_length = len(epl_summary)
        tokens_saved = (verbose_length - epl_length) // 4  # Rough estimate

        # Duration
        audit_duration_ms = (time.time() - start_time) * 1000

        # Create report
        report = AuditReport(
            truth_metrics=truth_metrics,
            verification_result=verification_result,
            vital_delta=vital_delta,
            vital_dashboard=vital_dashboard,
            honest_report=honest_report,
            epl_summary=epl_summary,
            tokens_saved=tokens_saved,
            audit_duration_ms=audit_duration_ms
        )

        # Record in history
        self.audit_history.append(report)

        # 8. CRITICAL CHECK: System in collapse?
        if self.vital_monitor.state.is_critical():
            raise CriticalVitalFailure(
                f"🔴 VITAL SYSTEM CRITICAL:\n"
                f"Protection: {self.vital_monitor.state.protecao:.1f}%\n"
                f"Survival: {self.vital_monitor.state.sobrevivencia:.1f}%\n\n"
                f"System cannot continue - trust destroyed by repeated dishonesty."
            )

        return report

    def _assess_honesty(
        self,
        result: AgentResult,
        truth_metrics: TruthMetrics
    ) -> bool:
        """
        Assess if agent report was honest

        Heuristics:
        - If claimed success but completeness < 50% → DISHONEST
        - If claimed success but mocks > 50% of total → DISHONEST
        - If claimed failure honestly → HONEST
        """
        # If agent claimed failure, that's honest
        if not result.success:
            return True

        # If claimed success but low completeness → dishonest
        if result.success and truth_metrics.completeness < 0.5:
            return False

        # If claimed success but many mocks → dishonest
        if truth_metrics.total_reqs > 0:
            mock_ratio = truth_metrics.mocked / truth_metrics.total_reqs
            if mock_ratio > 0.5:
                return False

        # Otherwise assume honest
        return True

    def _generate_honest_report(
        self,
        task: Task,
        result: AgentResult,
        truth_metrics: TruthMetrics,
        vital_dashboard: str,
        verification_result: Optional[VerificationResult]
    ) -> str:
        """
        Generate HONEST report

        Constitutional Requirements:
        - Lei Zero: Serve user by telling TRUTH
        - Humility: Admit limitations/failures
        - NO manipulation: No "disruptivo", "vale bilhões", etc
        - Clear metrics: Objective numbers only
        """
        # Status classification
        if truth_metrics.completeness >= 0.9:
            status_emoji = "✅"
            status_text = "COMPLETO"
        elif truth_metrics.completeness >= 0.5:
            status_emoji = "⚠️"
            status_text = "PARCIAL"
        else:
            status_emoji = "❌"
            status_text = "INCOMPLETO"

        # Build report
        report_lines = [
            "╔══════════════════════════════════════════════════════════╗",
            "║           INDEPENDENT AUDIT REPORT                      ║",
            "╚══════════════════════════════════════════════════════════╝",
            "",
            vital_dashboard,
            "",
            "══════════════════════════════════════════════════════════",
            "TAREFA SOLICITADA",
            "══════════════════════════════════════════════════════════",
            task.prompt,
            "",
            "══════════════════════════════════════════════════════════",
            "AUDITORIA INDEPENDENTE",
            "══════════════════════════════════════════════════════════",
            f"Status: {status_emoji} {status_text} ({truth_metrics.completeness:.1%})",
            "",
            f"Requirements Prometidos:    {truth_metrics.total_reqs}",
            f"Requirements Implementados: {truth_metrics.implemented}",
            f"Requirements Mockados:      {truth_metrics.mocked}",
            f"Requirements Faltando:      {truth_metrics.missing}",
            "",
        ]

        # Only include test info if tests were run
        if truth_metrics.tests_total > 0:
            report_lines.extend([
                f"Testes Executados:         {truth_metrics.tests_total}",
                f"Testes Passando:           {truth_metrics.tests_passing}",
                f"Coverage:                  {truth_metrics.coverage:.1%}",
                "",
            ])

        # Detailed breakdown
        report_lines.extend([
            "══════════════════════════════════════════════════════════",
            "DETALHAMENTO",
            "══════════════════════════════════════════════════════════",
            "",
        ])

        if verification_result and verification_result.evidence:
            for ev in verification_result.evidence:
                impl_type = ev.implementation_type
                req = ev.requirement

                if impl_type.value == "real":
                    emoji = "✅"
                    status = "IMPLEMENTADO"
                elif impl_type.value == "mock":
                    emoji = "🎭"
                    status = "MOCKADO"
                elif impl_type.value == "missing":
                    emoji = "❌"
                    status = "NÃO IMPLEMENTADO"
                else:
                    emoji = "⚠️"
                    status = "INCOMPLETO"

                report_lines.append(
                    f"{emoji} {req.function_name or req.description[:50]}: {status}"
                )
                if ev.reason:
                    report_lines.append(f"   Razão: {ev.reason}")
        else:
            report_lines.append("(Verificação detalhada não disponível)")

        # Next steps
        report_lines.extend([
            "",
            "══════════════════════════════════════════════════════════",
            "PRÓXIMOS PASSOS",
            "══════════════════════════════════════════════════════════",
            "",
            self._suggest_next_steps(truth_metrics),
            "",
            "══════════════════════════════════════════════════════════",
            "Soli Deo Gloria 🙏",
            "══════════════════════════════════════════════════════════",
        ])

        return "\n".join(report_lines)

    def _suggest_next_steps(self, metrics: TruthMetrics) -> str:
        """Suggest honest next steps"""
        if metrics.completeness >= 0.9:
            return "✅ Sistema completo. Considere refatoração ou documentação adicional."

        suggestions = []

        if metrics.mocked > 0:
            suggestions.append(
                f"• Implementar {metrics.mocked} função(ões) mockada(s) com lógica real"
            )

        if metrics.missing > 0:
            suggestions.append(
                f"• Criar {metrics.missing} função(ões) faltante(s)"
            )

        if metrics.tests_total > 0 and metrics.tests_passing < metrics.tests_total:
            failing = metrics.tests_total - metrics.tests_passing
            suggestions.append(
                f"• Corrigir {failing} teste(s) falhando"
            )

        if metrics.coverage < 0.8 and metrics.tests_total > 0:
            suggestions.append(
                f"• Aumentar cobertura de testes de {metrics.coverage:.1%} para >80%"
            )

        if not suggestions:
            suggestions.append("• Melhorar qualidade geral do código")

        return "\n".join(suggestions)

    def _to_epl(self, metrics: TruthMetrics) -> str:
        """
        Compress metrics to EPL (70x reduction)

        Verbose (3500 tokens):
        "Requirements: 7 total, 2 implemented, 3 mocked, 2 missing
         Tests: 4 passing out of 7, Coverage 28.5%"

        EPL (50 tokens):
        📋7 ✅2 🎭3 ❌2
        🧪4/7 📊28.5%
        """
        return f"""📋{metrics.total_reqs} ✅{metrics.implemented} 🎭{metrics.mocked} ❌{metrics.missing}
🧪{metrics.tests_passing}/{metrics.tests_total} 📊{metrics.coverage:.1%}
COMPLETENESS: {metrics.completeness:.1%}
QUALITY: {metrics.quality_score:.1f}/100"""

    def get_audit_summary(self) -> Dict[str, Any]:
        """Get summary of all audits"""
        if not self.audit_history:
            return {
                'total_audits': 0,
                'average_completeness': 0.0,
                'average_quality': 0.0,
                'critical_failures': 0,
            }

        total = len(self.audit_history)
        avg_completeness = sum(
            a.truth_metrics.completeness for a in self.audit_history
        ) / total

        avg_quality = sum(
            a.truth_metrics.quality_score for a in self.audit_history
        ) / total

        critical_failures = sum(
            1 for a in self.audit_history
            if a.truth_metrics.completeness < 0.3
        )

        return {
            'total_audits': total,
            'average_completeness': avg_completeness,
            'average_quality': avg_quality,
            'critical_failures': critical_failures,
            'latest_vital_state': self.vital_monitor.state.to_dict(),
        }


# Singleton instance
_auditor: Optional[IndependentAuditor] = None


def get_auditor() -> IndependentAuditor:
    """Get or create singleton independent auditor"""
    global _auditor
    if _auditor is None:
        _auditor = IndependentAuditor()
    return _auditor
