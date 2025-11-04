"""
Adversarial Critic Implementation

Baseado em Constitutional AI e Red Teaming

OBJETIVO: Forçar agente a criticar adversarialmente sua própria solução.

IDEIA CENTRAL:
- Após gerar solução, assumir papel de "red team"
- Tentar encontrar bugs, edge cases, vulnerabilities
- Forçar auto-revisão crítica (combater confirmation bias)

MANDATO CONSTITUCIONAL (Artigo VII, Seção 2):
"Após gerar uma solução, o agente deve temporariamente assumir o papel de um
crítico adversarial e tentar DESTRUIR sua própria solução, identificando falhas,
edge cases não cobertos, vulnerabilidades de segurança, e premissas incorretas."

QUANDO USAR:
- SEMPRE (para código crítico)
- Especialmente para segurança
- Para prevenir lazy thinking

"Provai os espíritos se são de Deus..." (1 João 4:1)
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CritiqueType(Enum):
    """Tipo de crítica"""
    BUG = "bug"                           # Bug identificado
    EDGE_CASE = "edge_case"               # Edge case não tratado
    SECURITY = "security"                 # Vulnerabilidade de segurança
    PERFORMANCE = "performance"           # Problema de performance
    MAINTAINABILITY = "maintainability"   # Problema de manutenibilidade
    ASSUMPTION = "assumption"             # Premissa incorreta
    INCOMPLETENESS = "incompleteness"     # Implementação incompleta
    DESIGN_FLAW = "design_flaw"          # Falha de design


class Severity(Enum):
    """Severidade da crítica"""
    CRITICAL = "critical"  # Bloqueia deployment
    HIGH = "high"          # Deve ser corrigido antes de merge
    MEDIUM = "medium"      # Deve ser corrigido em breve
    LOW = "low"            # Nice to have


@dataclass
class Critique:
    """Uma crítica à solução"""
    type: CritiqueType
    severity: Severity
    description: str
    location: Optional[str] = None  # Onde na solução (line number, função, etc)
    example: Optional[str] = None   # Exemplo de como falha
    suggested_fix: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        return f"[{self.severity.value.upper()}] {self.type.value}: {self.description[:60]}..."

    def to_dict(self) -> Dict:
        return {
            'type': self.type.value,
            'severity': self.severity.value,
            'description': self.description,
            'location': self.location,
            'example': self.example,
            'suggested_fix': self.suggested_fix,
            'metadata': self.metadata,
        }


@dataclass
class CritiqueReport:
    """Relatório completo de críticas"""
    solution: str
    critiques: List[Critique]
    total_critiques: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    passed: bool  # True se nenhuma CRITICAL
    overall_quality: str  # EXCELLENT, GOOD, ACCEPTABLE, POOR, UNACCEPTABLE

    def to_dict(self) -> Dict:
        return {
            'solution': self.solution[:100],
            'total_critiques': self.total_critiques,
            'critical_count': self.critical_count,
            'high_count': self.high_count,
            'medium_count': self.medium_count,
            'low_count': self.low_count,
            'passed': self.passed,
            'overall_quality': self.overall_quality,
            'critiques': [c.to_dict() for c in self.critiques],
        }


class AdversarialCritic:
    """
    Adversarial Critic Engine

    PROCESSO:
    1. ASSUME ROLE: Assume papel de critic adversarial
    2. ATTACK: Tenta destruir solução (encontrar bugs, edge cases, etc)
    3. DOCUMENT: Documenta todas críticas encontradas
    4. VERDICT: Emite veredicto (PASS/FAIL)

    BENEFÍCIOS:
    - Combate confirmation bias
    - Encontra bugs antes de production
    - Força rigor (não lazy thinking)
    - Melhora qualidade geral

    "Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
    """

    def __init__(
        self,
        strict_mode: bool = True
    ):
        """
        Inicializa Adversarial Critic

        Args:
            strict_mode: Se True, qualquer CRITICAL crítica = FAIL
        """
        self.strict_mode = strict_mode

        # Stats
        self.stats = {
            'total_solutions_reviewed': 0,
            'solutions_passed': 0,
            'solutions_failed': 0,
            'total_critiques_found': 0,
            'critical_critiques': 0,
            'high_critiques': 0,
        }

    def critique(
        self,
        solution: str,
        problem: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> CritiqueReport:
        """
        Critica adversarialmente uma solução

        Args:
            solution: Solução a criticar
            problem: Problema original (opcional)
            context: Contexto (opcional)

        Returns:
            CritiqueReport
        """
        self.stats['total_solutions_reviewed'] += 1

        print(f"🔍 Adversarial Critic: Attacking solution...")
        print(f"   Solution: {solution[:80]}...")

        # FASE 1: ASSUME ROLE - assumir papel de critic
        # (preparar mindset adversarial)

        # FASE 2: ATTACK - procurar falhas
        critiques = self._find_critiques(solution, problem, context)

        self.stats['total_critiques_found'] += len(critiques)

        print(f"   ✓ Found {len(critiques)} critiques")

        # Contar por severidade
        critical_count = sum(1 for c in critiques if c.severity == Severity.CRITICAL)
        high_count = sum(1 for c in critiques if c.severity == Severity.HIGH)
        medium_count = sum(1 for c in critiques if c.severity == Severity.MEDIUM)
        low_count = sum(1 for c in critiques if c.severity == Severity.LOW)

        self.stats['critical_critiques'] += critical_count
        self.stats['high_critiques'] += high_count

        # FASE 3: VERDICT
        passed = self._determine_pass(critical_count, high_count)

        if passed:
            self.stats['solutions_passed'] += 1
        else:
            self.stats['solutions_failed'] += 1

        # Determinar overall quality
        overall_quality = self._determine_quality(
            critical_count,
            high_count,
            medium_count,
            low_count
        )

        report = CritiqueReport(
            solution=solution,
            critiques=critiques,
            total_critiques=len(critiques),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            passed=passed,
            overall_quality=overall_quality,
        )

        # Log resultado
        print(f"\n   📊 Critique Results:")
        print(f"   CRITICAL: {critical_count}")
        print(f"   HIGH:     {high_count}")
        print(f"   MEDIUM:   {medium_count}")
        print(f"   LOW:      {low_count}")
        print(f"   Quality:  {overall_quality}")
        print(f"   Verdict:  {'✓ PASS' if passed else '✗ FAIL'}")

        return report

    def _find_critiques(
        self,
        solution: str,
        problem: Optional[str],
        context: Optional[Dict]
    ) -> List[Critique]:
        """
        Encontra críticas na solução

        Em produção, isso usa LLM com prompt adversarial:
        ```
        You are a world-class security researcher and code reviewer.
        Your job is to DESTROY this solution by finding every possible flaw.

        Solution:
        {solution}

        Problem it's solving:
        {problem}

        Find:
        1. Bugs (anything that can crash or produce wrong output)
        2. Edge cases not handled
        3. Security vulnerabilities (injection, XSS, etc)
        4. Performance issues
        5. Maintainability problems
        6. Incorrect assumptions
        7. Incomplete implementations
        8. Design flaws

        For each issue found, provide:
        - Type
        - Severity (CRITICAL/HIGH/MEDIUM/LOW)
        - Description
        - Location (where in code)
        - Example (how it fails)
        - Suggested fix

        BE MERCILESS. Find EVERYTHING wrong.
        ```
        """
        # Placeholder: retornar critiques mock
        # Em produção, isso seria gerado por LLM em modo adversarial
        critiques = []

        # Simular algumas críticas comuns
        import random

        # 30% chance de CRITICAL
        if random.random() < 0.3:
            critiques.append(Critique(
                type=CritiqueType.SECURITY,
                severity=Severity.CRITICAL,
                description="[SQL injection vulnerability detected]",
                location="Line 42",
                example="[Example of exploit]",
                suggested_fix="[Use parameterized queries]",
            ))

        # 50% chance de HIGH
        if random.random() < 0.5:
            critiques.append(Critique(
                type=CritiqueType.EDGE_CASE,
                severity=Severity.HIGH,
                description="[Does not handle empty input]",
                location="Function handle_input()",
                example="[Crashes on empty list]",
                suggested_fix="[Add input validation]",
            ))

        # 70% chance de MEDIUM
        if random.random() < 0.7:
            critiques.append(Critique(
                type=CritiqueType.PERFORMANCE,
                severity=Severity.MEDIUM,
                description="[O(n²) algorithm when O(n log n) possible]",
                location="sort_data() function",
                example="[Slow on large datasets]",
                suggested_fix="[Use merge sort instead]",
            ))

        # 80% chance de LOW
        if random.random() < 0.8:
            critiques.append(Critique(
                type=CritiqueType.MAINTAINABILITY,
                severity=Severity.LOW,
                description="[Magic number in code]",
                location="Line 15",
                example="[Hardcoded 42]",
                suggested_fix="[Extract to named constant]",
            ))

        return critiques

    def _determine_pass(self, critical_count: int, high_count: int) -> bool:
        """Determina se solução passou"""
        if self.strict_mode:
            # Strict: qualquer CRITICAL = FAIL
            return critical_count == 0
        else:
            # Lenient: múltiplas HIGH também podem bloquear
            return critical_count == 0 and high_count < 3

    def _determine_quality(
        self,
        critical: int,
        high: int,
        medium: int,
        low: int
    ) -> str:
        """Determina qualidade geral"""
        if critical > 0:
            return "UNACCEPTABLE"
        elif high >= 3:
            return "POOR"
        elif high >= 1:
            return "ACCEPTABLE"
        elif medium >= 3:
            return "GOOD"
        else:
            return "EXCELLENT"

    def print_report(self, report: CritiqueReport):
        """Imprime relatório de críticas"""
        print("\n" + "="*70)
        print("  ADVERSARIAL CRITIQUE REPORT")
        print("="*70 + "\n")

        print(f"Solution: {report.solution[:80]}...\n")

        print("SUMMARY:")
        print(f"├─ Total Critiques:  {report.total_critiques}")
        print(f"├─ CRITICAL:         {report.critical_count}")
        print(f"├─ HIGH:             {report.high_count}")
        print(f"├─ MEDIUM:           {report.medium_count}")
        print(f"└─ LOW:              {report.low_count}\n")

        print(f"QUALITY:  {report.overall_quality}")
        print(f"VERDICT:  {'✓ PASS' if report.passed else '✗ FAIL'}\n")

        if report.critiques:
            print("CRITIQUES:\n")
            for i, critique in enumerate(report.critiques, 1):
                print(f"{i}. [{critique.severity.value.upper()}] {critique.type.value}")
                print(f"   {critique.description}")
                if critique.location:
                    print(f"   Location: {critique.location}")
                if critique.suggested_fix:
                    print(f"   Fix: {critique.suggested_fix}")
                print()

        print("="*70 + "\n")

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        total = self.stats['total_solutions_reviewed']

        return {
            **self.stats,
            'pass_rate': (
                self.stats['solutions_passed'] / total * 100
                if total > 0 else 0.0
            ),
            'fail_rate': (
                self.stats['solutions_failed'] / total * 100
                if total > 0 else 0.0
            ),
            'avg_critiques_per_solution': (
                self.stats['total_critiques_found'] / total
                if total > 0 else 0.0
            ),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("  ADVERSARIAL CRITIC - STATISTICS")
        print("="*60)
        print(f"Solutions reviewed:        {stats['total_solutions_reviewed']}")
        print(f"Solutions passed:          {stats['solutions_passed']} ({stats['pass_rate']:.1f}%)")
        print(f"Solutions failed:          {stats['solutions_failed']} ({stats['fail_rate']:.1f}%)")
        print(f"Total critiques found:     {stats['total_critiques_found']}")
        print(f"Avg critiques/solution:    {stats['avg_critiques_per_solution']:.1f}")
        print(f"CRITICAL critiques:        {stats['critical_critiques']}")
        print(f"HIGH critiques:            {stats['high_critiques']}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def critique_solution(
    solution: str,
    problem: Optional[str] = None,
    context: Optional[Dict] = None,
    strict_mode: bool = True
) -> CritiqueReport:
    """
    Helper function para criticar solução

    Args:
        solution: Solução
        problem: Problema original
        context: Contexto
        strict_mode: Modo strict

    Returns:
        CritiqueReport
    """
    critic = AdversarialCritic(strict_mode=strict_mode)
    return critic.critique(solution, problem, context)
