"""
DETER-AGENT Framework

Execução Determinística através de Aplicação e Raciocínio em Camadas

5 Layers:
1. Constitutional Layer ✅ (já implementado em core/constitutional)
2. Deliberation Layer (Tree of Thoughts, Self-Consistency)
3. State Management Layer (Context Compression, Memory)
4. Execution Layer (Tool Use, TDD Enforcement)
5. Incentive Layer (Metrics, Reward Shaping)

"Tudo tem o seu tempo determinado..." (Eclesiastes 3:1)
"""

from .deliberation import (
    TreeOfThoughts,
    SelfConsistency,
    ChainOfThought,
    AdversarialCritic,
    Thought,
    ThoughtEvaluation,
)

__all__ = [
    # Deliberation
    'TreeOfThoughts',
    'SelfConsistency',
    'ChainOfThought',
    'AdversarialCritic',
    'Thought',
    'ThoughtEvaluation',
]
