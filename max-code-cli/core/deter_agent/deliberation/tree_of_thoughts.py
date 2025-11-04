"""
Tree of Thoughts (ToT) Implementation

Baseado em "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
(Yao et al., Princeton/Google, 2023)

OBJETIVO: Explorar múltiplos caminhos de solução antes de commitar,
movendo o agente de geração linear para busca deliberativa.

MANDATO CONSTITUCIONAL:
- Artigo VII, Seção 1: "O Executor Tático deve gerar 3-5 'pensamentos'
  (abordagens alternativas) para resolver o problema."

FILOSOFIA:
- NÃO gerar código linearmente
- EXPLORAR múltiplos caminhos
- AVALIAR alternativas
- SELECIONAR o caminho mais ROBUSTO (não o mais FÁCIL)

"Qual homem há entre vós que, querendo edificar uma torre,
 não se assenta primeiro a calcular os gastos...?" (Lucas 14:28)
"""

from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class EvaluationDimension(Enum):
    """Dimensões de avaliação de um pensamento"""
    CORRECTNESS = "correctness"           # Correção técnica
    ROBUSTNESS = "robustness"             # Robustez (edge cases)
    MAINTAINABILITY = "maintainability"   # Manutenibilidade
    PERFORMANCE = "performance"           # Performance
    SECURITY = "security"                 # Segurança
    SIMPLICITY = "simplicity"             # Simplicidade (Occam's Razor)
    TESTABILITY = "testability"           # Testabilidade


@dataclass
class ThoughtEvaluation:
    """Avaliação de um pensamento em múltiplas dimensões"""
    correctness: float  # 0.0-1.0
    robustness: float
    maintainability: float
    performance: float
    security: float
    simplicity: float
    testability: float

    # Score agregado (weighted average)
    overall_score: float = 0.0

    # Weights padrão (podem ser customizados)
    weights: Dict[str, float] = field(default_factory=lambda: {
        'correctness': 0.25,      # 25% - MAIS IMPORTANTE
        'robustness': 0.20,       # 20%
        'maintainability': 0.15,  # 15%
        'performance': 0.10,      # 10%
        'security': 0.15,         # 15%
        'simplicity': 0.05,       # 5%
        'testability': 0.10,      # 10%
    })

    def __post_init__(self):
        """Calcula overall score"""
        self.overall_score = (
            self.correctness * self.weights['correctness'] +
            self.robustness * self.weights['robustness'] +
            self.maintainability * self.weights['maintainability'] +
            self.performance * self.weights['performance'] +
            self.security * self.weights['security'] +
            self.simplicity * self.weights['simplicity'] +
            self.testability * self.weights['testability']
        )

    def to_dict(self) -> Dict[str, float]:
        """Serializa para dict"""
        return {
            'correctness': self.correctness,
            'robustness': self.robustness,
            'maintainability': self.maintainability,
            'performance': self.performance,
            'security': self.security,
            'simplicity': self.simplicity,
            'testability': self.testability,
            'overall_score': self.overall_score,
        }


@dataclass
class Thought:
    """
    Um 'pensamento' = uma abordagem alternativa para resolver o problema

    Cada pensamento representa uma estratégia distinta, não uma variação superficial.
    """
    id: str
    description: str                    # Descrição da abordagem
    approach: str                       # Detalhes técnicos da abordagem
    pros: List[str]                     # Vantagens
    cons: List[str]                     # Desvantagens
    assumptions: List[str]              # Premissas assumidas
    risks: List[str]                    # Riscos identificados
    complexity: str                     # LOW, MEDIUM, HIGH
    evaluation: Optional[ThoughtEvaluation] = None
    implementation_plan: Optional[List[str]] = None  # Steps de implementação
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        """String representation"""
        score = f"{self.evaluation.overall_score:.2f}" if self.evaluation else "N/A"
        return f"Thought({self.id}, score={score}, complexity={self.complexity})"

    def to_dict(self) -> Dict:
        """Serializa para dict"""
        return {
            'id': self.id,
            'description': self.description,
            'approach': self.approach,
            'pros': self.pros,
            'cons': self.cons,
            'assumptions': self.assumptions,
            'risks': self.risks,
            'complexity': self.complexity,
            'evaluation': self.evaluation.to_dict() if self.evaluation else None,
            'implementation_plan': self.implementation_plan,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
        }


class TreeOfThoughts:
    """
    Tree of Thoughts (ToT) Engine

    PROCESSO:
    1. GENERATE: Gera 3-5 pensamentos (abordagens alternativas)
    2. EVALUATE: Avalia cada pensamento em múltiplas dimensões
    3. SELECT: Seleciona o pensamento mais ROBUSTO (não o mais FÁCIL)
    4. EXPAND: (opcional) Expande o pensamento escolhido em sub-pensamentos

    MANDATO CONSTITUCIONAL (Artigo VII, Seção 1):
    - Mínimo 3 pensamentos
    - Máximo 5 pensamentos (para não desperdiçar tokens - P6)
    - Avaliação rigorosa em 7 dimensões

    "Os pensamentos do diligente tendem só à abundância,
     porém os de todo apressado, tão-somente à penúria." (Provérbios 21:5)
    """

    MIN_THOUGHTS = 3
    MAX_THOUGHTS = 5

    def __init__(
        self,
        generator: Optional[Callable[[str], List[Thought]]] = None,
        evaluator: Optional[Callable[[Thought], ThoughtEvaluation]] = None
    ):
        """
        Inicializa ToT Engine

        Args:
            generator: Função para gerar pensamentos (usa LLM)
            evaluator: Função para avaliar pensamentos (usa LLM ou heurística)
        """
        self.generator = generator or self._default_generator
        self.evaluator = evaluator or self._default_evaluator

        # Stats
        self.stats = {
            'total_problems': 0,
            'total_thoughts_generated': 0,
            'avg_thoughts_per_problem': 0.0,
            'best_scores': [],
        }

    def solve(
        self,
        problem: str,
        context: Optional[Dict] = None,
        num_thoughts: int = 3,
        return_all: bool = False
    ) -> Thought:
        """
        Resolve problema usando Tree of Thoughts

        Args:
            problem: Problema a resolver
            context: Contexto adicional
            num_thoughts: Número de pensamentos a gerar (3-5)
            return_all: Se True, retorna todos pensamentos (não só o melhor)

        Returns:
            Thought (ou List[Thought] se return_all=True)
        """
        self.stats['total_problems'] += 1

        # Validar num_thoughts
        if num_thoughts < self.MIN_THOUGHTS:
            num_thoughts = self.MIN_THOUGHTS
        elif num_thoughts > self.MAX_THOUGHTS:
            num_thoughts = self.MAX_THOUGHTS

        print(f"🌳 Tree of Thoughts: Generating {num_thoughts} alternative approaches...")
        print(f"   Problem: {problem[:80]}...")

        # FASE 1: GENERATE thoughts
        thoughts = self._generate_thoughts(problem, context, num_thoughts)
        self.stats['total_thoughts_generated'] += len(thoughts)

        print(f"   ✓ Generated {len(thoughts)} thoughts")

        # FASE 2: EVALUATE thoughts
        evaluated_thoughts = self._evaluate_thoughts(thoughts)

        print(f"   ✓ Evaluated all thoughts")

        # FASE 3: RANK thoughts
        ranked_thoughts = self._rank_thoughts(evaluated_thoughts)

        # Log top 3
        print(f"\n   📊 Top 3 Thoughts:")
        for i, thought in enumerate(ranked_thoughts[:3], 1):
            score = thought.evaluation.overall_score
            print(f"   {i}. {thought.description[:60]}... (score: {score:.2f})")

        # Update stats
        best_score = ranked_thoughts[0].evaluation.overall_score
        self.stats['best_scores'].append(best_score)
        self.stats['avg_thoughts_per_problem'] = (
            self.stats['total_thoughts_generated'] / self.stats['total_problems']
        )

        # FASE 4: SELECT best
        if return_all:
            return ranked_thoughts
        else:
            best_thought = ranked_thoughts[0]
            print(f"\n   🏆 Selected: {best_thought.description[:60]}...")
            return best_thought

    def _generate_thoughts(
        self,
        problem: str,
        context: Optional[Dict],
        num_thoughts: int
    ) -> List[Thought]:
        """
        Gera pensamentos alternativos

        Em produção, isso usaria LLM (Claude) com prompt engineering:
        - "Generate 3-5 DISTINCT approaches to solve this problem"
        - "Each approach should be fundamentally different, not just variations"
        """
        return self.generator(problem, context, num_thoughts)

    def _evaluate_thoughts(self, thoughts: List[Thought]) -> List[Thought]:
        """
        Avalia cada pensamento em múltiplas dimensões

        Em produção, isso usaria:
        - LLM para avaliar (Claude como judge)
        - Heurísticas (complexity analysis, security scanning)
        - Simulation (executar em digital twin)
        """
        evaluated = []
        for thought in thoughts:
            evaluation = self.evaluator(thought)
            thought.evaluation = evaluation
            evaluated.append(thought)

        return evaluated

    def _rank_thoughts(self, thoughts: List[Thought]) -> List[Thought]:
        """
        Rank thoughts por overall score (descendente)
        """
        return sorted(
            thoughts,
            key=lambda t: t.evaluation.overall_score,
            reverse=True
        )

    def _default_generator(
        self,
        problem: str,
        context: Optional[Dict],
        num_thoughts: int
    ) -> List[Thought]:
        """
        Generator padrão (placeholder - em produção usa LLM)

        Exemplo de prompt para LLM:
        ```
        You are a world-class software architect. Generate {num_thoughts} DISTINCT
        approaches to solve this problem:

        Problem: {problem}

        For each approach, provide:
        1. Description (1-2 sentences)
        2. Technical approach (2-3 sentences)
        3. Pros (2-3 points)
        4. Cons (2-3 points)
        5. Assumptions (1-2 points)
        6. Risks (1-2 points)
        7. Complexity (LOW/MEDIUM/HIGH)

        Make each approach FUNDAMENTALLY DIFFERENT, not just variations.
        ```
        """
        # Placeholder: retornar thoughts mock
        thoughts = []

        for i in range(num_thoughts):
            thought = Thought(
                id=f"thought_{i+1}",
                description=f"Approach {i+1}: [Would be generated by LLM]",
                approach="[Technical details from LLM]",
                pros=["Pro 1", "Pro 2"],
                cons=["Con 1", "Con 2"],
                assumptions=["Assumption 1"],
                risks=["Risk 1"],
                complexity=["LOW", "MEDIUM", "HIGH"][i % 3],
            )
            thoughts.append(thought)

        return thoughts

    def _default_evaluator(self, thought: Thought) -> ThoughtEvaluation:
        """
        Evaluator padrão (placeholder - em produção usa LLM + heurísticas)

        Exemplo de prompt para LLM:
        ```
        Evaluate this approach on a scale of 0.0 to 1.0:

        Approach: {thought.description}
        {thought.approach}

        Evaluate on these dimensions:
        1. Correctness: Is it technically correct?
        2. Robustness: Does it handle edge cases?
        3. Maintainability: Is it easy to maintain?
        4. Performance: Is it efficient?
        5. Security: Is it secure?
        6. Simplicity: Is it simple (Occam's Razor)?
        7. Testability: Is it testable?

        Return JSON:
        {
          "correctness": 0.9,
          "robustness": 0.8,
          ...
        }
        ```
        """
        # Placeholder: retornar evaluation mock
        # Em produção, isso seria chamada ao LLM
        import random
        return ThoughtEvaluation(
            correctness=random.uniform(0.7, 1.0),
            robustness=random.uniform(0.7, 1.0),
            maintainability=random.uniform(0.7, 1.0),
            performance=random.uniform(0.7, 1.0),
            security=random.uniform(0.7, 1.0),
            simplicity=random.uniform(0.7, 1.0),
            testability=random.uniform(0.7, 1.0),
        )

    def expand_thought(
        self,
        thought: Thought,
        depth: int = 1
    ) -> List[Thought]:
        """
        Expande um pensamento em sub-pensamentos (recursive ToT)

        Útil para problemas muito complexos onde precisamos explorar
        sub-problemas de forma hierárquica.

        Args:
            thought: Pensamento a expandir
            depth: Profundidade de expansão

        Returns:
            Lista de sub-pensamentos
        """
        if depth <= 0:
            return [thought]

        # Gerar sub-pensamentos para cada step do implementation plan
        sub_thoughts = []

        if thought.implementation_plan:
            for step in thought.implementation_plan[:3]:  # Limitar a 3 para não explodir
                # Gerar 2-3 sub-thoughts para este step
                step_thoughts = self._generate_thoughts(
                    problem=step,
                    context={'parent_thought': thought.id},
                    num_thoughts=2
                )
                sub_thoughts.extend(step_thoughts)

        return sub_thoughts

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        avg_score = (
            sum(self.stats['best_scores']) / len(self.stats['best_scores'])
            if self.stats['best_scores'] else 0.0
        )

        return {
            **self.stats,
            'avg_best_score': round(avg_score, 3),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("  TREE OF THOUGHTS - STATISTICS")
        print("="*60)
        print(f"Total problems solved:    {stats['total_problems']}")
        print(f"Total thoughts generated: {stats['total_thoughts_generated']}")
        print(f"Avg thoughts/problem:     {stats['avg_thoughts_per_problem']:.1f}")
        print(f"Avg best score:           {stats['avg_best_score']:.3f}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def tree_of_thoughts_solve(
    problem: str,
    context: Optional[Dict] = None,
    num_thoughts: int = 3
) -> Thought:
    """
    Helper function para resolver problema com ToT

    Args:
        problem: Problema
        context: Contexto
        num_thoughts: Número de pensamentos (3-5)

    Returns:
        Melhor Thought
    """
    tot = TreeOfThoughts()
    return tot.solve(problem, context, num_thoughts)
