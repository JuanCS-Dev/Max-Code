"""
Self-Consistency Implementation

Baseado em "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
(Wang et al., Google, 2022)

OBJETIVO: Melhorar raciocínio através de múltiplas amostragens e votação.

IDEIA CENTRAL:
- Gerar múltiplas soluções (5-10) para o mesmo problema
- Usar temperature > 0 para diversidade
- Votar na solução mais consistente (maioria)

QUANDO USAR:
- Problemas com múltiplas soluções válidas
- Tarefas críticas (CRITICAL ou HIGH criticality)
- Quando precisamos de alta confiança

"Na multidão de conselheiros há segurança." (Provérbios 11:14)
"""

from typing import List, Dict, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from collections import Counter
from datetime import datetime
import hashlib
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class Solution:
    """Uma solução candidata"""
    id: str
    content: str  # Código, resposta, ou resultado
    reasoning: Optional[str] = None  # Chain of thought
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def hash(self) -> str:
        """Hash da solução (para votação)"""
        # Normalizar antes de hashear
        normalized = self.content.strip().lower()
        return hashlib.md5(normalized.encode(), usedforsecurity=False).hexdigest()


@dataclass
class ConsensusResult:
    """Resultado da votação/consensus"""
    winner: Solution
    vote_count: int
    total_votes: int
    confidence: float  # vote_count / total_votes
    all_solutions: List[Solution]
    vote_distribution: Dict[str, int]  # hash -> count
    is_unanimous: bool
    is_majority: bool  # > 50%

    def to_dict(self) -> Dict:
        return {
            'winner_content': self.winner.content[:200],
            'vote_count': self.vote_count,
            'total_votes': self.total_votes,
            'confidence': self.confidence,
            'is_unanimous': self.is_unanimous,
            'is_majority': self.is_majority,
            'vote_distribution': self.vote_distribution,
        }


class SelfConsistency:
    """
    Self-Consistency Engine

    PROCESSO:
    1. SAMPLE: Gera N soluções (5-10) com temperature > 0
    2. VOTE: Agrupa soluções similares e conta votos
    3. SELECT: Seleciona solução com mais votos

    BENEFÍCIOS:
    - Reduz erros de raciocínio (averaging over reasoning paths)
    - Aumenta confiança (consensus = mais confiável)
    - Detecta ambiguidades (múltiplas soluções viáveis = problema ambíguo)

    "Onde não há conselhos, caem os projetos,
     mas com os muitos conselheiros há bom êxito." (Provérbios 15:22)
    """

    DEFAULT_SAMPLES = 5
    MIN_SAMPLES = 3
    MAX_SAMPLES = 10

    def __init__(
        self,
        generator: Optional[Callable[[str, Dict], Solution]] = None,
        similarity_threshold: float = 0.9
    ):
        """
        Inicializa Self-Consistency Engine

        Args:
            generator: Função para gerar soluções (usa LLM)
            similarity_threshold: Threshold para considerar soluções "iguais"
        """
        self.generator = generator or self._default_generator
        self.similarity_threshold = similarity_threshold

        # Stats
        self.stats = {
            'total_problems': 0,
            'total_samples_generated': 0,
            'unanimous_consensus': 0,
            'majority_consensus': 0,
            'split_votes': 0,
            'avg_confidence': [],
        }

    def solve(
        self,
        problem: str,
        context: Optional[Dict] = None,
        num_samples: int = DEFAULT_SAMPLES,
        temperature: float = 0.7
    ) -> ConsensusResult:
        """
        Resolve problema usando Self-Consistency

        Args:
            problem: Problema a resolver
            context: Contexto adicional
            num_samples: Número de amostras (3-10)
            temperature: Temperature para diversidade (0.5-1.0)

        Returns:
            ConsensusResult com solução vencedora
        """
        self.stats['total_problems'] += 1

        # Validar num_samples
        if num_samples < self.MIN_SAMPLES:
            num_samples = self.MIN_SAMPLES
        elif num_samples > self.MAX_SAMPLES:
            num_samples = self.MAX_SAMPLES

        logger.info(f"🗳️  Self-Consistency: Generating {num_samples} independent solutions...")
        logger.info(f"   Problem: {problem[:80]}...")
        logger.info(f"   Temperature: {temperature}")
        # FASE 1: SAMPLE - gerar múltiplas soluções
        solutions = self._generate_samples(
            problem,
            context,
            num_samples,
            temperature
        )

        self.stats['total_samples_generated'] += len(solutions)

        logger.info(f"   ✓ Generated {len(solutions)} solutions")
        # FASE 2: VOTE - contar votos
        consensus = self._vote(solutions)

        # Update stats
        if consensus.is_unanimous:
            self.stats['unanimous_consensus'] += 1
        elif consensus.is_majority:
            self.stats['majority_consensus'] += 1
        else:
            self.stats['split_votes'] += 1

        self.stats['avg_confidence'].append(consensus.confidence)

        # Log resultado
        logger.info(f"\n   📊 Voting Results:")
        logger.info(f"   Winner: {consensus.vote_count}/{consensus.total_votes} votes")
        logger.info(f"   Confidence: {consensus.confidence:.1%}")
        logger.info(f"   Status: {'✓ UNANIMOUS' if consensus.is_unanimous else '✓ MAJORITY' if consensus.is_majority else '⚠ SPLIT'}")
        return consensus

    def _generate_samples(
        self,
        problem: str,
        context: Optional[Dict],
        num_samples: int,
        temperature: float
    ) -> List[Solution]:
        """
        Gera múltiplas soluções independentes

        Em produção, isso chama LLM com:
        - temperature > 0 (para diversidade)
        - múltiplas calls independentes
        - cada call é completamente independente (não vê outras soluções)
        """
        solutions = []

        for i in range(num_samples):
            solution = self.generator(
                problem,
                {
                    **(context or {}),
                    'sample_id': i + 1,
                    'temperature': temperature,
                }
            )
            solutions.append(solution)

        return solutions

    def _vote(self, solutions: List[Solution]) -> ConsensusResult:
        """
        Votação: encontra solução mais comum

        Agrupa soluções similares e conta votos.
        """
        # Agrupar por hash (soluções "idênticas")
        vote_counts: Dict[str, List[Solution]] = {}

        for solution in solutions:
            hash_key = solution.hash()

            if hash_key not in vote_counts:
                vote_counts[hash_key] = []

            vote_counts[hash_key].append(solution)

        # Encontrar vencedor (mais votos)
        winner_hash = max(vote_counts.keys(), key=lambda h: len(vote_counts[h]))
        winner_solutions = vote_counts[winner_hash]
        winner = winner_solutions[0]  # Pegar primeira (todas são similares)

        vote_count = len(winner_solutions)
        total_votes = len(solutions)

        # Calcular confidence
        confidence = vote_count / total_votes

        # Checks
        is_unanimous = (vote_count == total_votes)
        is_majority = (vote_count > total_votes / 2)

        # Vote distribution
        vote_distribution = {
            hash_key: len(sols)
            for hash_key, sols in vote_counts.items()
        }

        return ConsensusResult(
            winner=winner,
            vote_count=vote_count,
            total_votes=total_votes,
            confidence=confidence,
            all_solutions=solutions,
            vote_distribution=vote_distribution,
            is_unanimous=is_unanimous,
            is_majority=is_majority,
        )

    def _default_generator(
        self,
        problem: str,
        context: Dict
    ) -> Solution:
        """
        Generator padrão (placeholder - em produção usa LLM)

        Exemplo de prompt:
        ```
        Solve this problem:

        {problem}

        Think step-by-step and provide your reasoning.

        Final answer should be clear and unambiguous.
        ```

        Com temperature > 0 para diversidade.
        """
        # Placeholder: retornar solution mock
        import random

        # Simular diversidade de soluções
        sample_id = context.get('sample_id', 1)

        # 70% chance de mesma solução (simular consensus)
        # 30% chance de solução diferente
        if random.random() < 0.7:
            content = "Solution A: [Majority solution]"
        else:
            content = f"Solution B{sample_id}: [Alternative solution]"

        return Solution(
            id=f"solution_{sample_id}",
            content=content,
            reasoning="[Step-by-step reasoning from LLM]",
            confidence=random.uniform(0.7, 1.0),
        )

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        total = self.stats['total_problems']

        avg_confidence = (
            sum(self.stats['avg_confidence']) / len(self.stats['avg_confidence'])
            if self.stats['avg_confidence'] else 0.0
        )

        return {
            **self.stats,
            'unanimous_rate': (
                self.stats['unanimous_consensus'] / total * 100
                if total > 0 else 0.0
            ),
            'majority_rate': (
                self.stats['majority_consensus'] / total * 100
                if total > 0 else 0.0
            ),
            'split_rate': (
                self.stats['split_votes'] / total * 100
                if total > 0 else 0.0
            ),
            'avg_confidence': round(avg_confidence, 3),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        logger.info("  SELF-CONSISTENCY - STATISTICS")
        print("="*60)
        logger.info(f"Total problems solved:     {stats['total_problems']}")
        logger.info(f"Total samples generated:   {stats['total_samples_generated']}")
        logger.info(f"Unanimous consensus:       {stats['unanimous_consensus']} ({stats['unanimous_rate']:.1f}%)")
        logger.info(f"Majority consensus:        {stats['majority_consensus']} ({stats['majority_rate']:.1f}%)")
        logger.info(f"Split votes:               {stats['split_votes']} ({stats['split_rate']:.1f}%)")
        logger.info(f"Avg confidence:            {stats['avg_confidence']:.3f}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def self_consistency_solve(
    problem: str,
    context: Optional[Dict] = None,
    num_samples: int = 5,
    temperature: float = 0.7
) -> ConsensusResult:
    """
    Helper function para resolver com Self-Consistency

    Args:
        problem: Problema
        context: Contexto
        num_samples: Número de amostras (3-10)
        temperature: Temperature (0.5-1.0)

    Returns:
        ConsensusResult
    """
    sc = SelfConsistency()
    return sc.solve(problem, context, num_samples, temperature)
