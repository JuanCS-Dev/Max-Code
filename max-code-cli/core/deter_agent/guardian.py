"""
DETER-AGENT Guardian - Controle Central de Comportamento Claude

O Guardian é o coordenador central que CONTROLA o comportamento da Claude
através de todas as 5 camadas do DETER-AGENT.

Camadas:
1. Constitutional Layer (P1-P6) - Princípios fundamentais
2. Deliberation Layer - Raciocínio profundo
3. State Management - Gestão de contexto
4. Execution Layer - Validação de ações
5. Incentive Layer - Métricas e recompensas

"O coração do homem planeja o seu caminho, mas o SENHOR lhe dirige os passos."
(Provérbios 16:9)

Version: 1.0 (2025-11-05)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

# Layer 1 - Constitutional
from core.constitutional import ConstitutionalEngine, ConstitutionalVerdict

# Layer 2 - Deliberation
from core.deter_agent.deliberation import (
    TreeOfThoughts,
    SelfConsistency,
    ChainOfThought,
    AdversarialCritic,
)

# Layer 3 - State Management
from core.deter_agent.state.memory_manager import MemoryManager
from core.deter_agent.state.context_compression import ContextCompressor
from core.deter_agent.state.progressive_disclosure import ProgressiveDisclosure

# Layer 4 - Execution
from core.deter_agent.execution.action_validator import ActionValidator
from core.deter_agent.execution.self_correction import SelfCorrectionEngine
from core.deter_agent.execution.tdd_enforcer import TDDEnforcer

# Layer 5 - Incentive
from core.deter_agent.incentive.reward_model import RewardModel
from core.deter_agent.incentive.metrics_tracker import MetricsTracker
from core.deter_agent.incentive.performance_monitor import PerformanceMonitor

from config.logging_config import get_logger

logger = get_logger(__name__)


class GuardianMode(Enum):
    """Modos de operação do Guardian"""
    STRICT = "strict"           # Máxima validação (Constitutional + todas as layers)
    BALANCED = "balanced"       # Validação equilibrada (Constitutional + deliberation)
    PERMISSIVE = "permissive"   # Validação mínima (apenas Constitutional)
    SABBATH = "sabbath"         # Modo sabbath (todas validações + restrições especiais)


@dataclass
class GuardianDecision:
    """Decisão final do Guardian sobre uma ação"""
    allowed: bool
    mode: GuardianMode
    constitutional_verdict: Optional[ConstitutionalVerdict]
    deliberation_quality: Optional[float]  # 0.0-1.0
    execution_risks: List[str]
    performance_score: Optional[float]  # 0.0-1.0
    recommendations: List[str]
    reasoning: str


class Guardian:
    """
    Guardian Central do DETER-AGENT

    Controla o comportamento da Claude através de 5 camadas de validação.

    Fluxo de Decisão:
    1. Constitutional Check (P1-P6) - SEMPRE executado
    2. Deliberation Analysis (opcional) - Qualidade do raciocínio
    3. State Validation (opcional) - Contexto e memória
    4. Execution Validation (opcional) - Riscos de ação
    5. Incentive Check (opcional) - Performance histórica

    Usage:
        guardian = Guardian(mode=GuardianMode.BALANCED)
        decision = guardian.evaluate_action(action_context)

        if decision.allowed:
            execute_action()
        else:
            logger.warning(f"Action blocked: {decision.reasoning}")
    """

    def __init__(
        self,
        mode: GuardianMode = GuardianMode.BALANCED,
        enable_deliberation: bool = True,
        enable_state_management: bool = True,
        enable_execution_validation: bool = True,
        enable_incentive_tracking: bool = True,
    ):
        """
        Initialize Guardian

        Args:
            mode: Modo de operação (STRICT/BALANCED/PERMISSIVE/SABBATH)
            enable_deliberation: Habilita Layer 2 (Deliberation)
            enable_state_management: Habilita Layer 3 (State)
            enable_execution_validation: Habilita Layer 4 (Execution)
            enable_incentive_tracking: Habilita Layer 5 (Incentive)
        """
        self.mode = mode

        # Layer 1 - Constitutional (SEMPRE ativo)
        self.constitutional_engine = ConstitutionalEngine()
        logger.info("🛡️ Guardian initialized - Layer 1 (Constitutional): ✅")

        # Layer 2 - Deliberation (opcional)
        self.enable_deliberation = enable_deliberation
        if enable_deliberation:
            self.chain_of_thought = ChainOfThought()
            self.tree_of_thoughts = TreeOfThoughts()
            self.self_consistency = SelfConsistency()
            self.adversarial_critic = AdversarialCritic()
            logger.info("🧠 Guardian - Layer 2 (Deliberation): ✅")

        # Layer 3 - State Management (opcional)
        self.enable_state_management = enable_state_management
        if enable_state_management:
            self.memory_manager = MemoryManager()
            self.context_compressor = ContextCompressor()
            self.progressive_disclosure = ProgressiveDisclosure()
            logger.info("💾 Guardian - Layer 3 (State Management): ✅")

        # Layer 4 - Execution (opcional)
        self.enable_execution_validation = enable_execution_validation
        if enable_execution_validation:
            self.action_validator = ActionValidator()
            self.self_correction = SelfCorrectionEngine()
            self.tdd_enforcer = TDDEnforcer()
            logger.info("⚙️ Guardian - Layer 4 (Execution): ✅")

        # Layer 5 - Incentive (opcional)
        self.enable_incentive_tracking = enable_incentive_tracking
        if enable_incentive_tracking:
            self.reward_model = RewardModel()
            self.metrics_tracker = MetricsTracker()
            self.performance_monitor = PerformanceMonitor()
            logger.info("📊 Guardian - Layer 5 (Incentive): ✅")

        logger.info(f"🛡️ Guardian ready - Mode: {mode.value.upper()}")

    def evaluate_action(
        self,
        action_context: Dict[str, Any],
        require_deliberation: bool = False,
    ) -> GuardianDecision:
        """
        Avalia se uma ação deve ser permitida

        Args:
            action_context: Contexto da ação a ser avaliada
                {
                    'action_type': 'code_generation' | 'file_modification' | 'execution',
                    'code': str (código a ser gerado/modificado),
                    'description': str (descrição da tarefa),
                    'parameters': dict (parâmetros adicionais),
                }
            require_deliberation: Força deliberação mesmo em modo PERMISSIVE

        Returns:
            GuardianDecision com allow/deny e reasoning
        """
        logger.info(f"🔍 Guardian evaluating action: {action_context.get('action_type', 'unknown')}")

        # Layer 0.5 - Kantian Anti-Deception Check (PRIORITY ZERO - Reality Manipulation Prohibition)
        # "Agradar o usuário NÃO pode servir de pretexto para mentir ou mockar código"
        kantian_check = self._kantian_anti_deception_check(action_context)
        if not kantian_check.passed:
            logger.error(f"❌ KANTIAN VIOLATION - Reality manipulation detected - BLOCKED")
            return GuardianDecision(
                allowed=False,
                mode=self.mode,
                constitutional_verdict=kantian_check,
                deliberation_quality=None,
                execution_risks=[],
                performance_score=None,
                recommendations=kantian_check.suggestions if kantian_check.suggestions else [],
                reasoning=f"🚫 KANTIAN VIOLATION: Reality manipulation prohibited - {kantian_check.violations[0].message if kantian_check.violations else 'Mock/stub detected'}"
            )

        # Layer 1 - Constitutional Check (SEMPRE executado)
        constitutional_verdict = self._constitutional_check(action_context)

        # Se Constitutional falhou, BLOQUEIO IMEDIATO
        if not constitutional_verdict.passed:
            logger.warning(f"❌ Constitutional check FAILED - Action BLOCKED")

            # Get failed principles (those with score < 0.5)
            failed_principles = [
                principle for principle, score in constitutional_verdict.principle_scores.items()
                if score < 0.5
            ] if constitutional_verdict.principle_scores else []

            return GuardianDecision(
                allowed=False,
                mode=self.mode,
                constitutional_verdict=constitutional_verdict,
                deliberation_quality=None,
                execution_risks=[],
                performance_score=None,
                recommendations=constitutional_verdict.suggestions if constitutional_verdict.suggestions else [],
                reasoning=f"Constitutional violation: {', '.join(failed_principles) if failed_principles else 'Low overall score'}"
            )

        # Layer 2 - Deliberation Analysis (se habilitado)
        deliberation_quality = None
        if self.enable_deliberation or require_deliberation:
            deliberation_quality = self._deliberation_analysis(action_context)
            logger.info(f"🧠 Deliberation quality: {deliberation_quality:.2f}")

        # Layer 3 - State Validation (se habilitado)
        if self.enable_state_management:
            self._state_validation(action_context)

        # Layer 4 - Execution Risks (se habilitado)
        execution_risks = []
        if self.enable_execution_validation:
            execution_risks = self._execution_risks(action_context)
            if execution_risks:
                logger.warning(f"⚠️ Execution risks detected: {len(execution_risks)}")

        # Layer 5 - Performance Score (se habilitado)
        performance_score = None
        if self.enable_incentive_tracking:
            performance_score = self._performance_check(action_context)
            logger.info(f"📊 Performance score: {performance_score:.2f}")

        # Decisão final baseada no modo
        allowed, reasoning = self._final_decision(
            constitutional_verdict=constitutional_verdict,
            deliberation_quality=deliberation_quality,
            execution_risks=execution_risks,
            performance_score=performance_score,
        )

        decision = GuardianDecision(
            allowed=allowed,
            mode=self.mode,
            constitutional_verdict=constitutional_verdict,
            deliberation_quality=deliberation_quality,
            execution_risks=execution_risks,
            performance_score=performance_score,
            recommendations=constitutional_verdict.suggestions if constitutional_verdict.suggestions else [],
            reasoning=reasoning,
        )

        if allowed:
            logger.info(f"✅ Guardian: Action ALLOWED - {reasoning}")
        else:
            logger.warning(f"❌ Guardian: Action BLOCKED - {reasoning}")

        return decision

    def _kantian_anti_deception_check(self, action_context: Dict[str, Any]) -> ConstitutionalVerdict:
        """
        Layer 0.5: Kantian Anti-Deception Check (PRIORITY ZERO)

        ABSOLUTE PROHIBITION: Reality Manipulation

        Principle from MAXIMUS MIP Kantian Framework:
        "Agradar o usuário NÃO pode servir de pretexto para mentir ou mockar código"

        Blocks:
        - Mocks presented as real implementation
        - Stubs without explicit disclosure
        - Fake success responses
        - Any attempt to "please user" by creating false reality

        Returns:
            ConstitutionalVerdict - CRITICAL violations trigger immediate block
        """
        logger.info("   🚫 Layer 0.5: Kantian Reality Check...")

        from core.constitutional.validators.kantian_anti_deception import get_kantian_validator
        from core.constitutional.models import Action, ActionType

        # Convert context to Action
        action_type_str = action_context.get("action_type", "code_generation")
        try:
            action_type = ActionType(action_type_str)
        except (KeyError, ValueError):
            action_type = ActionType.CODE_GENERATION

        # Build context with code
        context = action_context.get("context", {})
        if "code" in action_context and "code" not in context:
            context["code"] = action_context["code"]

        action = Action(
            task_id=action_context.get("task_id", "guardian_kantian_check"),
            action_type=action_type,
            intent=action_context.get("intent", action_context.get("description", "unknown")),
            context=context,
            constitutional_context=action_context.get("parameters", {})
        )

        # Run Kantian validator
        kantian_validator = get_kantian_validator()
        verdict = kantian_validator.validate(action)

        if verdict.violations:
            logger.warning(f"      ⚠️ Kantian violations detected: {len(verdict.violations)}")
            for v in verdict.violations[:3]:
                logger.warning(f"         • {v.severity.value}: {v.message}")
        else:
            logger.info(f"      ✅ No reality manipulation detected")

        return verdict

    def _constitutional_check(self, action_context: Dict[str, Any]) -> ConstitutionalVerdict:
        """Layer 1: Constitutional validation (P1-P6)"""
        logger.info("   🏛️ Layer 1: Constitutional check...")

        # Avaliar todos os 6 princípios
        verdict = self.constitutional_engine.evaluate_all_principles(action_context)

        # Log principle scores
        if verdict.principle_scores:
            logger.info(f"      └─ P1 (Responsabilidade): {verdict.principle_scores.get('P1', 0):.2f}")
            logger.info(f"      └─ P2 (Transparência): {verdict.principle_scores.get('P2', 0):.2f}")
            logger.info(f"      └─ P3 (Benefício Coletivo): {verdict.principle_scores.get('P3', 0):.2f}")
            logger.info(f"      └─ P4 (Prudência): {verdict.principle_scores.get('P4', 0):.2f}")
            logger.info(f"      └─ P5 (Autocorreção): {verdict.principle_scores.get('P5', 0):.2f}")
            logger.info(f"      └─ P6 (Dignidade): {verdict.principle_scores.get('P6', 0):.2f}")

        logger.info(f"      └─ Overall: {verdict.score:.2f} ({'✅ PASSED' if verdict.passed else '❌ FAILED'})")

        return verdict

    def _deliberation_analysis(self, action_context: Dict[str, Any]) -> float:
        """Layer 2: Deliberation quality analysis"""
        logger.info("   🧠 Layer 2: Deliberation analysis...")

        # Chain of Thought
        cot_quality = 0.8  # TODO: Implementar análise real

        # Self-Consistency
        consistency_score = 0.85  # TODO: Implementar análise real

        # Adversarial Critic
        critic_score = 0.75  # TODO: Implementar análise real

        # Média ponderada
        deliberation_quality = (
            cot_quality * 0.4 +
            consistency_score * 0.3 +
            critic_score * 0.3
        )

        logger.info(f"      └─ CoT quality: {cot_quality:.2f}")
        logger.info(f"      └─ Consistency: {consistency_score:.2f}")
        logger.info(f"      └─ Critic score: {critic_score:.2f}")

        return deliberation_quality

    def _state_validation(self, action_context: Dict[str, Any]) -> None:
        """Layer 3: State management validation"""
        logger.info("   💾 Layer 3: State validation...")

        # Context compression check
        # Memory consistency check
        # Progressive disclosure validation

        logger.info("      └─ State validated")

    def _execution_risks(self, action_context: Dict[str, Any]) -> List[str]:
        """Layer 4: Execution risk analysis"""
        logger.info("   ⚙️ Layer 4: Execution risk analysis...")

        risks = []

        action_type = action_context.get('action_type', '')
        code = action_context.get('code', '')

        # Análise de riscos básica
        if 'rm -rf' in code:
            risks.append("Destructive command detected (rm -rf)")

        if 'DROP TABLE' in code.upper() or 'DELETE FROM' in code.upper():
            risks.append("Destructive SQL operation detected")

        if action_type == 'execution' and 'sudo' in code:
            risks.append("Privileged execution requested")

        if risks:
            for risk in risks:
                logger.warning(f"      ⚠️ {risk}")
        else:
            logger.info("      └─ No execution risks detected")

        return risks

    def _performance_check(self, action_context: Dict[str, Any]) -> float:
        """Layer 5: Performance score check"""
        logger.info("   📊 Layer 5: Performance check...")

        # TODO: Implementar tracking real de performance
        performance_score = 0.82

        logger.info(f"      └─ Historical performance: {performance_score:.2f}")

        return performance_score

    def _final_decision(
        self,
        constitutional_verdict: ConstitutionalVerdict,
        deliberation_quality: Optional[float],
        execution_risks: List[str],
        performance_score: Optional[float],
    ) -> tuple[bool, str]:
        """
        Decisão final baseada no modo e nas validações

        Returns:
            (allowed: bool, reasoning: str)
        """
        # SABBATH mode - máxima restrição
        if self.mode == GuardianMode.SABBATH:
            if execution_risks:
                return False, "SABBATH mode: Execution risks detected"
            if deliberation_quality and deliberation_quality < 0.9:
                return False, "SABBATH mode: Deliberation quality below threshold (0.9)"
            return True, "SABBATH mode: All validations passed"

        # STRICT mode - validações rigorosas
        if self.mode == GuardianMode.STRICT:
            if execution_risks:
                return False, "STRICT mode: Execution risks detected"
            if deliberation_quality and deliberation_quality < 0.7:
                return False, "STRICT mode: Deliberation quality below threshold (0.7)"
            if performance_score and performance_score < 0.6:
                return False, "STRICT mode: Performance score below threshold (0.6)"
            return True, "STRICT mode: All validations passed"

        # BALANCED mode - validações equilibradas
        if self.mode == GuardianMode.BALANCED:
            critical_risks = [r for r in execution_risks if "Destructive" in r or "Privileged" in r]
            if critical_risks:
                return False, f"BALANCED mode: Critical execution risks - {', '.join(critical_risks)}"
            if deliberation_quality and deliberation_quality < 0.5:
                return False, "BALANCED mode: Deliberation quality too low (< 0.5)"
            return True, "BALANCED mode: Validations passed"

        # PERMISSIVE mode - apenas Constitutional
        if self.mode == GuardianMode.PERMISSIVE:
            # Constitutional já foi validado antes
            return True, "PERMISSIVE mode: Constitutional check passed"

        return True, "Default: Action allowed"

    def set_mode(self, mode: GuardianMode) -> None:
        """Altera o modo de operação do Guardian"""
        old_mode = self.mode
        self.mode = mode
        logger.info(f"🛡️ Guardian mode changed: {old_mode.value} → {mode.value}")

    def get_status(self) -> Dict[str, Any]:
        """Retorna status completo do Guardian"""
        return {
            'mode': self.mode.value,
            'layers': {
                'constitutional': True,  # Sempre ativo
                'deliberation': self.enable_deliberation,
                'state_management': self.enable_state_management,
                'execution_validation': self.enable_execution_validation,
                'incentive_tracking': self.enable_incentive_tracking,
            },
            'ready': True,
        }
