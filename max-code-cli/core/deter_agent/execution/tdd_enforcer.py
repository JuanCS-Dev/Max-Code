"""
TDD Enforcer Implementation

OBJETIVO: Forçar test-driven development (TESTS FIRST, CODE SECOND).

IDEIA CENTRAL:
- TDD = Write tests BEFORE writing code
- Previne lazy thinking ("vou escrever código e depois testar")
- Força pensar em interface/comportamento antes de implementar
- Melhora design (código testável = código bem desenhado)

MANDATO CONSTITUCIONAL (Artigo VIII, Seção 1):
"Para TODA modificação de código (≥10 linhas ou função nova), o agente deve:
1. Escrever testes PRIMEIRO
2. Ver testes falharem (RED)
3. Escrever código mínimo para passar (GREEN)
4. Refatorar (REFACTOR)

VIOLAÇÕES BLOQUEIAM MERGE."

BENEFÍCIOS:
- Força rigor (não lazy thinking)
- Melhora design (testable = good design)
- Aumenta coverage
- Previne regressions

"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from config.logging_config import get_logger

logger = get_logger(__name__)


class TestStatus(Enum):
    """Status do teste"""
    NOT_WRITTEN = "not_written"  # Teste ainda não escrito
    WRITTEN = "written"           # Teste escrito (mas não rodado)
    PASSING = "passing"           # Teste passando (GREEN)
    FAILING = "failing"           # Teste falhando (RED)
    SKIPPED = "skipped"           # Teste pulado


class TDDPhase(Enum):
    """Fase do ciclo TDD"""
    RED = "red"          # Testes falhando
    GREEN = "green"      # Testes passando
    REFACTOR = "refactor"  # Refatorando


class TDDViolation(Enum):
    """Tipo de violação TDD"""
    CODE_WITHOUT_TESTS = "code_without_tests"  # Código sem testes
    TESTS_NOT_RUN = "tests_not_run"            # Testes não rodados
    SKIPPED_RED_PHASE = "skipped_red_phase"    # Pulou fase RED
    INSUFFICIENT_COVERAGE = "insufficient_coverage"  # Coverage < 80%


@dataclass
class TestCase:
    """Um caso de teste"""
    id: str
    name: str
    file_path: str
    function_under_test: str  # Função que está testando
    status: TestStatus
    assertion_count: int = 0
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CodeChange:
    """Mudança de código"""
    id: str
    file_path: str
    function_name: Optional[str]
    lines_added: int
    lines_removed: int
    has_tests: bool = False
    test_cases: List[TestCase] = field(default_factory=list)
    coverage: Optional[float] = None  # 0.0-1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TDDCycle:
    """Um ciclo completo de TDD (RED → GREEN → REFACTOR)"""
    id: str
    code_change: CodeChange
    current_phase: TDDPhase
    red_phase_completed: bool = False
    green_phase_completed: bool = False
    refactor_phase_completed: bool = False
    violations: List[TDDViolation] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    def is_complete(self) -> bool:
        """Checa se ciclo está completo"""
        return (
            self.red_phase_completed and
            self.green_phase_completed and
            self.refactor_phase_completed
        )

    def has_violations(self) -> bool:
        """Checa se tem violações"""
        return len(self.violations) > 0


class TDDEnforcer:
    """
    TDD Enforcer Engine

    PROCESSO:
    1. DETECT CODE CHANGE: Detecta mudança de código
    2. CHECK TESTS: Verifica se tem testes
    3. RUN TESTS: Roda testes
    4. ENFORCE RED → GREEN → REFACTOR: Força ciclo TDD
    5. VALIDATE COVERAGE: Valida coverage ≥80%
    6. BLOCK IF VIOLATIONS: Bloqueia se houver violações

    BENEFÍCIOS:
    - Força rigor (TDD é obrigatório)
    - Melhora qualidade (tests first = better design)
    - Aumenta coverage
    - Previne lazy thinking

    "Provai os espíritos se são de Deus, porque já muitos falsos profetas se têm
     levantado no mundo." (1 João 4:1)
    """

    # Limites constitucionais
    MIN_COVERAGE = 0.80  # 80% minimum
    MIN_LINES_FOR_TDD = 10  # Se mudança ≥10 linhas, TDD obrigatório

    def __init__(self, strict_mode: bool = True):
        """
        Inicializa TDD Enforcer

        Args:
            strict_mode: Se True, qualquer violação = BLOCK
        """
        self.strict_mode = strict_mode

        # Active TDD cycles
        self.active_cycles: Dict[str, TDDCycle] = {}

        # Stats
        self.stats = {
            'total_code_changes': 0,
            'changes_with_tests': 0,
            'changes_without_tests': 0,
            'tdd_cycles_completed': 0,
            'tdd_violations': 0,
            'avg_coverage': [],
        }

    def start_tdd_cycle(self, code_change: CodeChange) -> TDDCycle:
        """
        Inicia ciclo TDD

        Args:
            code_change: Mudança de código

        Returns:
            TDDCycle iniciado
        """
        self.stats['total_code_changes'] += 1

        # Check se precisa de TDD
        needs_tdd = self._needs_tdd(code_change)

        if not needs_tdd:
            logger.info(f"📝 TDD Enforcer: Code change too small ({code_change.lines_added} lines), TDD not required")
            # Criar cycle mas marcar como complete
            cycle = TDDCycle(
                id=f"tdd_{self.stats['total_code_changes']}",
                code_change=code_change,
                current_phase=TDDPhase.GREEN,
                red_phase_completed=True,
                green_phase_completed=True,
                refactor_phase_completed=True,
            )
            return cycle

        logger.info(f"🔴 TDD Enforcer: Starting TDD cycle for {code_change.function_name or code_change.file_path}")
        logger.info(f"   Lines added: {code_change.lines_added}")
        cycle = TDDCycle(
            id=f"tdd_{self.stats['total_code_changes']}",
            code_change=code_change,
            current_phase=TDDPhase.RED,  # Sempre começa em RED
        )

        self.active_cycles[cycle.id] = cycle

        return cycle

    def _needs_tdd(self, code_change: CodeChange) -> bool:
        """
        Determina se mudança precisa de TDD

        Critérios:
        - Nova função: SIM
        - ≥10 linhas adicionadas: SIM
        - < 10 linhas: NÃO (trivial)
        """
        if code_change.function_name:
            # Nova função = precisa TDD
            return True

        if code_change.lines_added >= self.MIN_LINES_FOR_TDD:
            return True

        return False

    def enforce_red_phase(self, cycle: TDDCycle) -> bool:
        """
        Enforça fase RED (testes devem FALHAR)

        Returns:
            True se fase RED válida, False caso contrário
        """
        logger.info(f"   🔴 RED Phase: Checking tests...")
        # Check 1: Tem testes?
        if not cycle.code_change.has_tests or len(cycle.code_change.test_cases) == 0:
            cycle.violations.append(TDDViolation.CODE_WITHOUT_TESTS)
            self.stats['tdd_violations'] += 1
            logger.error(f"   ❌ VIOLATION: No tests written!")
            return False

        # Check 2: Testes foram rodados?
        tests_run = all(
            test.status != TestStatus.NOT_WRITTEN
            for test in cycle.code_change.test_cases
        )

        if not tests_run:
            cycle.violations.append(TDDViolation.TESTS_NOT_RUN)
            self.stats['tdd_violations'] += 1
            logger.error(f"   ❌ VIOLATION: Tests not run!")
            return False

        # Check 3: Testes devem estar FALHANDO (RED)
        all_passing = all(
            test.status == TestStatus.PASSING
            for test in cycle.code_change.test_cases
        )

        if all_passing:
            # Se todos testes já passam, pulou fase RED!
            cycle.violations.append(TDDViolation.SKIPPED_RED_PHASE)
            self.stats['tdd_violations'] += 1
            logger.warning(f"   ⚠️  WARNING: All tests passing (skipped RED phase?)")
            # Não bloquear por isso, mas registrar
            # return False

        # Mark RED phase complete
        cycle.red_phase_completed = True
        cycle.current_phase = TDDPhase.GREEN

        logger.info(f"   ✓ RED Phase complete")
        return True

    def enforce_green_phase(self, cycle: TDDCycle) -> bool:
        """
        Enforça fase GREEN (testes devem PASSAR)

        Returns:
            True se fase GREEN válida, False caso contrário
        """
        logger.info(f"   🟢 GREEN Phase: Checking tests...")
        # Check: Todos testes devem estar PASSANDO
        all_passing = all(
            test.status == TestStatus.PASSING
            for test in cycle.code_change.test_cases
        )

        if not all_passing:
            failing_tests = [
                test.name for test in cycle.code_change.test_cases
                if test.status == TestStatus.FAILING
            ]
            logger.error(f"   ❌ FAILURE: {len(failing_tests)} tests still failing: {failing_tests}")
            return False

        # Check: Coverage ≥80%?
        if cycle.code_change.coverage is not None:
            if cycle.code_change.coverage < self.MIN_COVERAGE:
                cycle.violations.append(TDDViolation.INSUFFICIENT_COVERAGE)
                self.stats['tdd_violations'] += 1
                logger.warning(f"   ⚠️  WARNING: Coverage ({cycle.code_change.coverage:.1%}) below minimum ({self.MIN_COVERAGE:.1%})")
                if self.strict_mode:
                    return False

            self.stats['avg_coverage'].append(cycle.code_change.coverage)

        # Mark GREEN phase complete
        cycle.green_phase_completed = True
        cycle.current_phase = TDDPhase.REFACTOR

        logger.info(f"   ✓ GREEN Phase complete")
        return True

    def enforce_refactor_phase(self, cycle: TDDCycle) -> bool:
        """
        Enforça fase REFACTOR (opcional, mas recomendado)

        Returns:
            True (sempre - refactor é opcional)
        """
        logger.info(f"   🔧 REFACTOR Phase: Optional cleanup...")
        # Refactor é opcional
        # Apenas marcar como complete
        cycle.refactor_phase_completed = True
        cycle.completed_at = datetime.utcnow()

        logger.info(f"   ✓ REFACTOR Phase complete")
        # Remove from active cycles
        if cycle.id in self.active_cycles:
            del self.active_cycles[cycle.id]

        self.stats['tdd_cycles_completed'] += 1

        if cycle.code_change.has_tests:
            self.stats['changes_with_tests'] += 1
        else:
            self.stats['changes_without_tests'] += 1

        return True

    def validate_cycle(self, cycle: TDDCycle) -> Dict[str, Any]:
        """
        Valida ciclo TDD completo

        Returns:
            {
                'valid': bool,
                'violations': List[TDDViolation],
                'can_merge': bool,
            }
        """
        violations = cycle.violations.copy()

        # Check se ciclo está completo
        if not cycle.is_complete():
            return {
                'valid': False,
                'violations': violations,
                'can_merge': False,
                'reason': 'TDD cycle not complete',
            }

        # Check se tem violações
        if cycle.has_violations():
            if self.strict_mode:
                return {
                    'valid': False,
                    'violations': violations,
                    'can_merge': False,
                    'reason': f'{len(violations)} TDD violations detected',
                }
            else:
                return {
                    'valid': True,  # Lenient mode
                    'violations': violations,
                    'can_merge': True,
                    'reason': f'Warnings: {len(violations)} TDD violations (lenient mode)',
                }

        return {
            'valid': True,
            'violations': violations,
            'can_merge': True,
            'reason': 'TDD cycle complete with no violations',
        }

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        avg_coverage = (
            sum(self.stats['avg_coverage']) / len(self.stats['avg_coverage'])
            if self.stats['avg_coverage'] else 0.0
        )

        return {
            **self.stats,
            'avg_coverage': round(avg_coverage, 3),
            'tdd_compliance_rate': (
                self.stats['changes_with_tests'] / self.stats['total_code_changes'] * 100
                if self.stats['total_code_changes'] > 0 else 0.0
            ),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        logger.info("  TDD ENFORCER - STATISTICS")
        print("="*60)
        logger.info(f"Total code changes:        {stats['total_code_changes']}")
        logger.info(f"Changes with tests:        {stats['changes_with_tests']} ({stats['tdd_compliance_rate']:.1f}%)")
        logger.info(f"Changes without tests:     {stats['changes_without_tests']}")
        logger.info(f"TDD cycles completed:      {stats['tdd_cycles_completed']}")
        logger.info(f"TDD violations:            {stats['tdd_violations']}")
        logger.info(f"Avg coverage:              {stats['avg_coverage']:.1%}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def create_code_change(
    file_path: str,
    function_name: Optional[str],
    lines_added: int,
    lines_removed: int = 0
) -> CodeChange:
    """
    Helper para criar CodeChange

    Args:
        file_path: Path do arquivo
        function_name: Nome da função (None se modificação geral)
        lines_added: Linhas adicionadas
        lines_removed: Linhas removidas

    Returns:
        CodeChange
    """
    return CodeChange(
        id=f"change_{datetime.utcnow().timestamp()}",
        file_path=file_path,
        function_name=function_name,
        lines_added=lines_added,
        lines_removed=lines_removed,
    )


def create_test_case(
    name: str,
    file_path: str,
    function_under_test: str,
    status: TestStatus = TestStatus.NOT_WRITTEN
) -> TestCase:
    """Helper para criar TestCase"""
    return TestCase(
        id=f"test_{datetime.utcnow().timestamp()}",
        name=name,
        file_path=file_path,
        function_under_test=function_under_test,
        status=status,
    )
