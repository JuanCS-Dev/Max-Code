"""
Deliberation Layer - DETER-AGENT Layer 2

OBJETIVO: Forçar raciocínio explícito, estruturado e exploratório.

Move o agente de um gerador de resposta reativo para um solucionador
de problemas deliberado.

Baseado em:
- "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
  (Yao et al., Princeton/Google)
- "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
  (Wang et al., Google)

"Os pensamentos do diligente tendem só à abundância..." (Provérbios 21:5)
"""

from .tree_of_thoughts import (
    TreeOfThoughts,
    Thought,
    ThoughtEvaluation,
    EvaluationDimension,
)
from .self_consistency import SelfConsistency, ConsensusResult
from .chain_of_thought import ChainOfThought, ReasoningStep
from .adversarial_critic import AdversarialCritic, Critique

__all__ = [
    # Tree of Thoughts
    'TreeOfThoughts',
    'Thought',
    'ThoughtEvaluation',
    'EvaluationDimension',

    # Self-Consistency
    'SelfConsistency',
    'ConsensusResult',

    # Chain of Thought
    'ChainOfThought',
    'ReasoningStep',

    # Adversarial Critic
    'AdversarialCritic',
    'Critique',
]
