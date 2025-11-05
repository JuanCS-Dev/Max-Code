"""
Self-Correction Loops - P5: Autocorreção Humilde

Biblical Foundation:
"O caminho do insensato é reto aos seus próprios olhos,
 mas o que dá ouvidos ao conselho é sábio." (Provérbios 12:15)

Self-correction through wisdom - humility in action.

CONCEITO:
Após execução de uma ferramenta, detecta erros automaticamente e tenta autocorrigir
antes de escalar para o usuário. Implementa P5 - Autocorreção Humilde.

PROCESSO:
1. DETECT: Detecta erros na execução
2. ANALYZE: Analisa causa raiz do erro
3. PLAN: Planeja correção
4. RETRY: Executa correção automaticamente
5. ESCALATE: Se falhar após N tentativas, escala para usuário

BENEFÍCIOS:
- Reduz iterações manuais
- Aprende com erros
- Alinha com P5 - Autocorreção Humilde
- Integra com Guardian Runtime

Inspired by GitHub Copilot's Agent Mode self-correction,
but with Constitutional AI governance.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import re
from config.logging_config import get_logger

logger = get_logger(__name__)


class ErrorCategory(Enum):
    """Categorias de erro para autocorreção"""
    FILE_NOT_FOUND = "file_not_found"
    PERMISSION_DENIED = "permission_denied"
    SYNTAX_ERROR = "syntax_error"
    TYPE_ERROR = "type_error"
    RUNTIME_ERROR = "runtime_error"
    TIMEOUT = "timeout"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN = "unknown"


class CorrectionStrategy(Enum):
    """Estratégias de correção"""
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    ADJUST_PARAMETERS = "adjust_parameters"
    ALTERNATIVE_APPROACH = "alternative_approach"
    ESCALATE_TO_USER = "escalate_to_user"


@dataclass
class ErrorAnalysis:
    """Análise de erro"""
    category: ErrorCategory
    original_error: str
    root_cause: str
    suggested_fix: str
    confidence: float  # 0.0 a 1.0
    strategy: CorrectionStrategy
    parameters_to_adjust: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CorrectionAttempt:
    """Tentativa de correção"""
    attempt_number: int
    strategy: CorrectionStrategy
    analysis: ErrorAnalysis
    success: bool
    output: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SelfCorrectionResult:
    """Resultado do self-correction loop"""
    original_tool_name: str
    original_error: str
    corrected: bool
    attempts: List[CorrectionAttempt]
    final_output: Optional[Any] = None
    final_error: Optional[str] = None
    total_attempts: int = 0
    learning: Optional[str] = None  # O que aprendemos com este erro


class SelfCorrectionEngine:
    """
    Self-Correction Loop Engine

    Implementa P5 - Autocorreção Humilde através de loops de autocorreção.

    Features:
    - Detecção automática de erros
    - Análise de causa raiz
    - Múltiplas estratégias de correção
    - Learning from failures
    - Constitutional AI governance

    Example:
        >>> engine = SelfCorrectionEngine(max_attempts=3)
        >>> result = engine.correct_execution(
        ...     tool_executor=executor,
        ...     tool_name="read_file",
        ...     parameters={"file_path": "/wrong/path.txt"},
        ...     original_error="File not found: /wrong/path.txt"
        ... )
    """

    def __init__(self, max_attempts: int = 3, learning_enabled: bool = True):
        """
        Inicializa Self-Correction Engine

        Args:
            max_attempts: Número máximo de tentativas de correção
            learning_enabled: Se True, aprende com erros anteriores
        """
        self.max_attempts = max_attempts
        self.learning_enabled = learning_enabled

        # Learning database (erros já vistos e suas correções)
        self.error_patterns: Dict[str, ErrorAnalysis] = {}

        # Statistics
        self.stats = {
            'total_corrections': 0,
            'successful_corrections': 0,
            'failed_corrections': 0,
            'escalated_to_user': 0,
            'patterns_learned': 0,
        }

    def correct_execution(
        self,
        tool_executor,  # ToolExecutor instance
        tool_name: str,
        parameters: Dict[str, Any],
        original_error: str
    ) -> SelfCorrectionResult:
        """
        Tenta autocorrigir uma execução que falhou

        Args:
            tool_executor: Instância do ToolExecutor
            tool_name: Nome da ferramenta que falhou
            parameters: Parâmetros originais
            original_error: Erro original

        Returns:
            SelfCorrectionResult com resultado da correção

        Process:
            1. Analisa erro
            2. Tenta corrigir até max_attempts
            3. Se bem-sucedido, retorna resultado corrigido
            4. Se falhar, escala para usuário
        """
        self.stats['total_corrections'] += 1

        logger.error(f"\n🔄 Self-Correction: Analyzing error in '{tool_name}'...")
        attempts: List[CorrectionAttempt] = []

        # Análise inicial do erro
        analysis = self._analyze_error(original_error, tool_name, parameters)

        # PROTEÇÃO: Se o erro não é corrigível automaticamente, escala imediatamente
        if analysis.strategy == CorrectionStrategy.ESCALATE_TO_USER:
            logger.error(f"   ⚠️  Error requires manual intervention, escalating to user...")
            self.stats['escalated_to_user'] += 1
            return SelfCorrectionResult(
                original_tool_name=tool_name,
                original_error=original_error,
                corrected=False,
                attempts=[],
                final_error=original_error,
                total_attempts=0,
                learning=self._generate_learning(analysis, False)
            )

        logger.error(f"   ├─ Error category: {analysis.category.value}")
        logger.info(f"   ├─ Root cause: {analysis.root_cause}")
        logger.info(f"   ├─ Strategy: {analysis.strategy.value}")
        logger.info(f"   └─ Confidence: {analysis.confidence:.0%}")
        # Loop de correção
        for attempt_num in range(1, self.max_attempts + 1):
            logger.info(f"\n   🔧 Attempt {attempt_num}/{self.max_attempts}: {analysis.strategy.value}")
            # Aplica estratégia de correção
            corrected_params = self._apply_correction_strategy(
                parameters,
                analysis
            )

            # Tenta executar novamente
            try:
                # Usa o tool_executor para tentar novamente
                tool = tool_executor.registered_tools.get(tool_name)
                if not tool:
                    # Erro fatal: ferramenta não existe
                    attempt = CorrectionAttempt(
                        attempt_number=attempt_num,
                        strategy=analysis.strategy,
                        analysis=analysis,
                        success=False,
                        error=f"Tool '{tool_name}' not found in executor"
                    )
                    attempts.append(attempt)
                    break

                # CRITICAL: Desabilita self-correction temporariamente para evitar recursão infinita
                original_self_correction_state = tool_executor.enable_self_correction
                tool_executor.enable_self_correction = False

                # Atualiza parâmetros e tenta executar
                tool.parameters = corrected_params
                result = tool_executor.execute(tool_name, corrected_params)

                # Restaura estado original
                tool_executor.enable_self_correction = original_self_correction_state

                if result.status.value == "SUCCESS":
                    # Sucesso! Autocorreção funcionou
                    attempt = CorrectionAttempt(
                        attempt_number=attempt_num,
                        strategy=analysis.strategy,
                        analysis=analysis,
                        success=True,
                        output=result.output
                    )
                    attempts.append(attempt)

                    logger.info(f"   ✓ Self-correction successful!")
                    # Aprende com este sucesso
                    if self.learning_enabled:
                        self._learn_from_correction(analysis, corrected_params)

                    self.stats['successful_corrections'] += 1

                    return SelfCorrectionResult(
                        original_tool_name=tool_name,
                        original_error=original_error,
                        corrected=True,
                        attempts=attempts,
                        final_output=result.output,
                        total_attempts=attempt_num,
                        learning=self._generate_learning(analysis, True)
                    )
                else:
                    # Ainda falhou, tenta próxima estratégia
                    attempt = CorrectionAttempt(
                        attempt_number=attempt_num,
                        strategy=analysis.strategy,
                        analysis=analysis,
                        success=False,
                        error=result.error
                    )
                    attempts.append(attempt)

                    logger.error(f"   ✗ Attempt failed: {result.error}")
                    # Re-analisa com novo erro
                    analysis = self._analyze_error(result.error, tool_name, corrected_params)

            except Exception as e:
                # Erro durante tentativa de correção
                # Restaura self-correction em caso de exceção
                if 'original_self_correction_state' in locals():
                    tool_executor.enable_self_correction = original_self_correction_state

                attempt = CorrectionAttempt(
                    attempt_number=attempt_num,
                    strategy=analysis.strategy,
                    analysis=analysis,
                    success=False,
                    error=str(e)
                )
                attempts.append(attempt)

                logger.info(f"   ✗ Exception during correction: {e}")
        # Todas as tentativas falharam - escala para usuário
        logger.error(f"\n   ⚠️  Self-correction failed after {self.max_attempts} attempts")
        logger.info(f"   📤 Escalating to user...")
        self.stats['failed_corrections'] += 1
        self.stats['escalated_to_user'] += 1

        return SelfCorrectionResult(
            original_tool_name=tool_name,
            original_error=original_error,
            corrected=False,
            attempts=attempts,
            final_error=attempts[-1].error if attempts else original_error,
            total_attempts=len(attempts),
            learning=self._generate_learning(analysis, False)
        )

    def _analyze_error(
        self,
        error: str,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> ErrorAnalysis:
        """
        Analisa erro para determinar categoria e estratégia de correção

        Args:
            error: Mensagem de erro
            tool_name: Nome da ferramenta
            parameters: Parâmetros usados

        Returns:
            ErrorAnalysis com diagnóstico
        """
        error_lower = error.lower()

        # Pattern matching para categorização de erro

        # File not found
        if any(pattern in error_lower for pattern in ['file not found', 'no such file', 'does not exist']):
            # Tenta inferir caminho correto
            suggested_fix = "Try checking if file path is absolute, or search for similar files"

            return ErrorAnalysis(
                category=ErrorCategory.FILE_NOT_FOUND,
                original_error=error,
                root_cause="File path does not exist or is incorrect",
                suggested_fix=suggested_fix,
                confidence=0.9,
                strategy=CorrectionStrategy.ALTERNATIVE_APPROACH,
                parameters_to_adjust={'file_path': 'search_for_similar'}
            )

        # Permission denied
        if any(pattern in error_lower for pattern in ['permission denied', 'access denied', 'forbidden']):
            return ErrorAnalysis(
                category=ErrorCategory.PERMISSION_DENIED,
                original_error=error,
                root_cause="Insufficient permissions to access resource",
                suggested_fix="Check file permissions or try alternative location",
                confidence=0.95,
                strategy=CorrectionStrategy.ESCALATE_TO_USER,  # Não podemos corrigir permissões
            )

        # Syntax errors
        if any(pattern in error_lower for pattern in ['syntax error', 'invalid syntax', 'unexpected token']):
            return ErrorAnalysis(
                category=ErrorCategory.SYNTAX_ERROR,
                original_error=error,
                root_cause="Syntax error in code or parameters",
                suggested_fix="Fix syntax by adjusting parameters",
                confidence=0.8,
                strategy=CorrectionStrategy.ADJUST_PARAMETERS,
            )

        # Type errors
        if any(pattern in error_lower for pattern in ['type error', 'expected', 'got']):
            return ErrorAnalysis(
                category=ErrorCategory.TYPE_ERROR,
                original_error=error,
                root_cause="Type mismatch in parameters",
                suggested_fix="Convert parameter to correct type",
                confidence=0.85,
                strategy=CorrectionStrategy.ADJUST_PARAMETERS,
            )

        # Timeout
        if any(pattern in error_lower for pattern in ['timeout', 'timed out', 'time limit']):
            return ErrorAnalysis(
                category=ErrorCategory.TIMEOUT,
                original_error=error,
                root_cause="Operation exceeded time limit",
                suggested_fix="Retry with increased timeout or simpler query",
                confidence=0.9,
                strategy=CorrectionStrategy.RETRY_WITH_BACKOFF,
                parameters_to_adjust={'timeout': 'increase'}
            )

        # Network errors
        if any(pattern in error_lower for pattern in ['connection', 'network', 'unreachable', 'refused']):
            return ErrorAnalysis(
                category=ErrorCategory.NETWORK_ERROR,
                original_error=error,
                root_cause="Network connectivity issue",
                suggested_fix="Retry with exponential backoff",
                confidence=0.85,
                strategy=CorrectionStrategy.RETRY_WITH_BACKOFF,
            )

        # Validation errors
        if any(pattern in error_lower for pattern in ['validation', 'invalid', 'must be']):
            return ErrorAnalysis(
                category=ErrorCategory.VALIDATION_ERROR,
                original_error=error,
                root_cause="Parameter validation failed",
                suggested_fix="Adjust parameters to meet validation requirements",
                confidence=0.8,
                strategy=CorrectionStrategy.ADJUST_PARAMETERS,
            )

        # Unknown error - escala para usuário
        return ErrorAnalysis(
            category=ErrorCategory.UNKNOWN,
            original_error=error,
            root_cause="Unable to determine root cause automatically",
            suggested_fix="Manual intervention required",
            confidence=0.3,
            strategy=CorrectionStrategy.ESCALATE_TO_USER,
        )

    def _apply_correction_strategy(
        self,
        parameters: Dict[str, Any],
        analysis: ErrorAnalysis
    ) -> Dict[str, Any]:
        """
        Aplica estratégia de correção aos parâmetros

        Args:
            parameters: Parâmetros originais
            analysis: Análise do erro

        Returns:
            Parâmetros corrigidos
        """
        corrected = parameters.copy()

        if analysis.strategy == CorrectionStrategy.ADJUST_PARAMETERS:
            # Ajusta parâmetros baseado na análise
            for key, adjustment in analysis.parameters_to_adjust.items():
                if adjustment == 'increase' and key in corrected:
                    # Aumenta valor numérico (ex: timeout)
                    if isinstance(corrected[key], (int, float)):
                        corrected[key] = corrected[key] * 2

                elif adjustment == 'search_for_similar':
                    # File not found - poderia tentar buscar arquivo similar
                    # Por enquanto, mantém original (será implementado depois)
                    pass

        elif analysis.strategy == CorrectionStrategy.RETRY_WITH_BACKOFF:
            # Adiciona retry com backoff
            if 'timeout' in corrected:
                corrected['timeout'] = corrected.get('timeout', 30) * 1.5

        return corrected

    def _learn_from_correction(
        self,
        analysis: ErrorAnalysis,
        successful_params: Dict[str, Any]
    ):
        """
        Aprende com correção bem-sucedida

        Args:
            analysis: Análise do erro que foi corrigido
            successful_params: Parâmetros que funcionaram
        """
        # Cria padrão de erro para reutilizar no futuro
        error_signature = self._create_error_signature(analysis.original_error)

        if error_signature not in self.error_patterns:
            self.error_patterns[error_signature] = analysis
            self.stats['patterns_learned'] += 1

            logger.error(f"   📚 Learned new error pattern: {error_signature[:50]}...")
    def _create_error_signature(self, error: str) -> str:
        """Cria assinatura única para erro (para pattern matching futuro)"""
        # Remove detalhes específicos (paths, números) para generalizar
        signature = re.sub(r'/[^\s]+', '<PATH>', error)
        signature = re.sub(r'\d+', '<NUM>', signature)
        return signature

    def _generate_learning(self, analysis: ErrorAnalysis, success: bool) -> str:
        """
        Gera learning string explicando o que foi aprendido

        Args:
            analysis: Análise do erro
            success: Se correção foi bem-sucedida

        Returns:
            Learning string para auditoria
        """
        if success:
            return (
                f"✓ Learned: {analysis.category.value} errors can be fixed by "
                f"{analysis.strategy.value}. Root cause: {analysis.root_cause}"
            )
        else:
            return (
                f"✗ Failed to correct {analysis.category.value} error automatically. "
                f"Root cause: {analysis.root_cause}. Suggestion: {analysis.suggested_fix}"
            )

    def print_stats(self):
        """Imprime estatísticas de self-correction"""
        print("\n" + "=" * 70)
        logger.info("   SELF-CORRECTION ENGINE STATISTICS")
        print("=" * 70)

        total = self.stats['total_corrections']
        success = self.stats['successful_corrections']
        success_rate = (success / total * 100) if total > 0 else 0

        logger.info(f"  Total corrections attempted: {total}")
        logger.info(f"  Successful corrections: {success} ({success_rate:.1f}%)")
        logger.error(f"  Failed corrections: {self.stats['failed_corrections']}")
        logger.info(f"  Escalated to user: {self.stats['escalated_to_user']}")
        logger.info(f"  Patterns learned: {self.stats['patterns_learned']}")
        print("=" * 70)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_self_correction_engine(max_attempts: int = 3) -> SelfCorrectionEngine:
    """
    Cria instância de Self-Correction Engine

    Args:
        max_attempts: Número máximo de tentativas

    Returns:
        SelfCorrectionEngine configurado

    Example:
        >>> engine = create_self_correction_engine(max_attempts=3)
    """
    return SelfCorrectionEngine(max_attempts=max_attempts, learning_enabled=True)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("🔄 Self-Correction Loop Demo\n")
    print("=" * 70)
    logger.info("P5 - Autocorreção Humilde in action!")
    print("=" * 70)

    # Mock ToolExecutor for demo
    class MockToolExecutor:
        def __init__(self):
            self.registered_tools = {
                'read_file': type('Tool', (), {'parameters': {}})()
            }
            self.execution_count = 0

        def execute(self, tool_name, parameters):
            self.execution_count += 1

            # Simula: primeira tentativa falha, segunda sucede
            if self.execution_count == 1:
                return type('Result', (), {
                    'status': type('Status', (), {'value': 'FAILURE'})(),
                    'output': None,
                    'error': 'File not found: /wrong/path.txt'
                })()
            else:
                return type('Result', (), {
                    'status': type('Status', (), {'value': 'SUCCESS'})(),
                    'output': 'File contents here...',
                    'error': None
                })()

    # Create engine
    engine = SelfCorrectionEngine(max_attempts=3)
    executor = MockToolExecutor()

    # Test correction
    logger.error("\nTEST: File not found error correction\n")
    result = engine.correct_execution(
        tool_executor=executor,
        tool_name='read_file',
        parameters={'file_path': '/wrong/path.txt'},
        original_error='File not found: /wrong/path.txt'
    )

    print("\n" + "=" * 70)
    logger.info("RESULT:")
    print("=" * 70)
    logger.info(f"  Corrected: {result.corrected}")
    logger.info(f"  Total attempts: {result.total_attempts}")
    logger.info(f"  Learning: {result.learning}")
    if result.corrected:
        logger.info(f"\n  ✓ Final output: {str(result.final_output)[:100]}...")
    else:
        logger.error(f"\n  ✗ Final error: {result.final_error}")
    # Print stats
    engine.print_stats()

    logger.info("\n✅ Self-Correction Loop Demo Complete!")
    logger.info("🏎️ PAGANI: P5 - Autocorreção Humilde implementado!")