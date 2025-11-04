"""
Chain of Thought (CoT) Implementation

Baseado em "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
(Wei et al., Google, 2022)

OBJETIVO: Forçar raciocínio explícito passo-a-passo.

IDEIA CENTRAL:
- Antes de gerar solução final, gerar reasoning steps
- Cada step é explícito e verificável
- Raciocínio estruturado previne lazy thinking

QUANDO USAR:
- Problemas complexos que requerem raciocínio multi-step
- Debugging (para entender por que modelo decidiu algo)
- Traceability (P4 - rastrear raciocínio)

"Vinde, pois, e arrazoemos, diz o Senhor..." (Isaías 1:18)
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ReasoningType(Enum):
    """Tipo de raciocínio"""
    ANALYSIS = "analysis"           # Análise do problema
    ASSUMPTION = "assumption"       # Premissa assumida
    INFERENCE = "inference"         # Inferência lógica
    CALCULATION = "calculation"     # Cálculo
    CONCLUSION = "conclusion"       # Conclusão
    QUESTION = "question"           # Pergunta/dúvida
    DECISION = "decision"           # Decisão tomada


@dataclass
class ReasoningStep:
    """Um passo de raciocínio"""
    step_number: int
    type: ReasoningType
    content: str
    justification: Optional[str] = None
    alternatives_considered: List[str] = field(default_factory=list)
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        return f"Step {self.step_number} ({self.type.value}): {self.content[:60]}..."

    def to_dict(self) -> Dict:
        return {
            'step_number': self.step_number,
            'type': self.type.value,
            'content': self.content,
            'justification': self.justification,
            'alternatives_considered': self.alternatives_considered,
            'confidence': self.confidence,
            'metadata': self.metadata,
        }


@dataclass
class ChainOfThoughtResult:
    """Resultado do raciocínio Chain of Thought"""
    problem: str
    reasoning_steps: List[ReasoningStep]
    final_answer: str
    total_steps: int
    avg_confidence: float
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'problem': self.problem[:100],
            'total_steps': self.total_steps,
            'avg_confidence': self.avg_confidence,
            'reasoning_steps': [step.to_dict() for step in self.reasoning_steps],
            'final_answer': self.final_answer[:200],
            'warnings': self.warnings,
        }


class ChainOfThought:
    """
    Chain of Thought (CoT) Engine

    PROCESSO:
    1. DECOMPOSE: Quebra problema em sub-problemas
    2. REASON: Para cada sub-problema, gera reasoning step
    3. CHAIN: Encadeia steps em sequência lógica
    4. SYNTHESIZE: Sintetiza resposta final

    BENEFÍCIOS:
    - Raciocínio explícito (não "black box")
    - Verificável (cada step pode ser validado)
    - Traceable (P4 compliance)
    - Debugging facilitado

    "Vinde, pois, e arrazoemos, diz o Senhor; ainda que os vossos pecados
     sejam como a escarlata, eles se tornarão brancos como a neve." (Isaías 1:18)
    """

    def __init__(
        self,
        max_steps: int = 10,
        min_confidence: float = 0.6
    ):
        """
        Inicializa CoT Engine

        Args:
            max_steps: Máximo de steps (para prevenir loops infinitos)
            min_confidence: Confidence mínima para aceitar step
        """
        self.max_steps = max_steps
        self.min_confidence = min_confidence

        # Stats
        self.stats = {
            'total_problems': 0,
            'total_steps_generated': 0,
            'avg_steps_per_problem': 0.0,
            'low_confidence_steps': 0,
        }

    def reason(
        self,
        problem: str,
        context: Optional[Dict] = None,
        include_alternatives: bool = True
    ) -> ChainOfThoughtResult:
        """
        Gera raciocínio Chain of Thought para problema

        Args:
            problem: Problema a resolver
            context: Contexto adicional
            include_alternatives: Se True, inclui alternativas consideradas

        Returns:
            ChainOfThoughtResult
        """
        self.stats['total_problems'] += 1

        print(f"🧠 Chain of Thought: Reasoning step-by-step...")
        print(f"   Problem: {problem[:80]}...")

        # FASE 1: DECOMPOSE - quebrar problema
        sub_problems = self._decompose_problem(problem, context)

        print(f"   ✓ Decomposed into {len(sub_problems)} sub-problems")

        # FASE 2: REASON - gerar steps para cada sub-problema
        reasoning_steps = []

        for i, sub_problem in enumerate(sub_problems, 1):
            step = self._generate_reasoning_step(
                step_number=i,
                sub_problem=sub_problem,
                context=context,
                include_alternatives=include_alternatives
            )

            reasoning_steps.append(step)

            # Check confidence
            if step.confidence < self.min_confidence:
                self.stats['low_confidence_steps'] += 1
                print(f"   ⚠ Step {i} has low confidence ({step.confidence:.2f})")

            # Check max steps
            if i >= self.max_steps:
                print(f"   ⚠ Reached max steps ({self.max_steps}), stopping")
                break

        self.stats['total_steps_generated'] += len(reasoning_steps)

        print(f"   ✓ Generated {len(reasoning_steps)} reasoning steps")

        # FASE 3: SYNTHESIZE - sintetizar resposta final
        final_answer = self._synthesize_answer(reasoning_steps)

        # Calcular métricas
        avg_confidence = (
            sum(s.confidence for s in reasoning_steps) / len(reasoning_steps)
            if reasoning_steps else 0.0
        )

        # Warnings
        warnings = []
        if avg_confidence < 0.7:
            warnings.append(f"Low average confidence ({avg_confidence:.2f})")

        if len(reasoning_steps) >= self.max_steps:
            warnings.append(f"Reached maximum steps ({self.max_steps})")

        # Update stats
        self.stats['avg_steps_per_problem'] = (
            self.stats['total_steps_generated'] / self.stats['total_problems']
        )

        result = ChainOfThoughtResult(
            problem=problem,
            reasoning_steps=reasoning_steps,
            final_answer=final_answer,
            total_steps=len(reasoning_steps),
            avg_confidence=avg_confidence,
            warnings=warnings,
        )

        print(f"\n   📊 Reasoning Complete:")
        print(f"   Steps: {result.total_steps}")
        print(f"   Avg Confidence: {result.avg_confidence:.2f}")

        return result

    def _decompose_problem(
        self,
        problem: str,
        context: Optional[Dict]
    ) -> List[str]:
        """
        Decompõe problema em sub-problemas

        Em produção, isso usa LLM:
        ```
        Break down this problem into logical sub-problems:

        Problem: {problem}

        List 3-7 sub-problems that need to be solved.
        ```
        """
        # Placeholder: retornar sub-problems mock
        # Em produção, isso seria gerado por LLM
        return [
            "Understand the requirements",
            "Identify constraints and edge cases",
            "Choose appropriate approach",
            "Plan implementation steps",
            "Identify potential risks",
        ]

    def _generate_reasoning_step(
        self,
        step_number: int,
        sub_problem: str,
        context: Optional[Dict],
        include_alternatives: bool
    ) -> ReasoningStep:
        """
        Gera reasoning step para sub-problema

        Em produção, isso usa LLM:
        ```
        Reason through this sub-problem:

        {sub_problem}

        Provide:
        1. Your analysis
        2. Any assumptions you're making
        3. Your reasoning
        4. Alternatives you considered (if any)
        5. Your confidence (0-1)
        ```
        """
        # Placeholder: retornar step mock
        # Em produção, isso seria gerado por LLM
        import random

        step_types = list(ReasoningType)
        step_type = random.choice(step_types)

        alternatives = []
        if include_alternatives:
            alternatives = ["Alternative 1", "Alternative 2"]

        return ReasoningStep(
            step_number=step_number,
            type=step_type,
            content=f"[Reasoning for: {sub_problem}]",
            justification="[Justification from LLM]",
            alternatives_considered=alternatives,
            confidence=random.uniform(0.7, 1.0),
        )

    def _synthesize_answer(
        self,
        reasoning_steps: List[ReasoningStep]
    ) -> str:
        """
        Sintetiza resposta final a partir dos steps

        Em produção, isso usa LLM:
        ```
        Based on this reasoning chain:

        {reasoning_steps}

        Provide the final answer/solution.
        ```
        """
        # Placeholder: retornar answer mock
        # Em produção, isso seria sintetizado por LLM
        return "[Final answer synthesized from reasoning chain]"

    def explain_reasoning(self, result: ChainOfThoughtResult) -> str:
        """
        Gera explicação legível do raciocínio

        Útil para debugging e transparency (P4)
        """
        lines = []
        lines.append(f"Problem: {result.problem}\n")
        lines.append("Reasoning Steps:\n")

        for step in result.reasoning_steps:
            lines.append(f"{step.step_number}. [{step.type.value.upper()}] {step.content}")

            if step.justification:
                lines.append(f"   Why: {step.justification}")

            if step.alternatives_considered:
                lines.append(f"   Alternatives: {', '.join(step.alternatives_considered)}")

            lines.append(f"   Confidence: {step.confidence:.2f}\n")

        lines.append(f"\nFinal Answer: {result.final_answer}")

        if result.warnings:
            lines.append(f"\nWarnings:")
            for warning in result.warnings:
                lines.append(f"  ⚠ {warning}")

        return "\n".join(lines)

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
            'low_confidence_rate': (
                self.stats['low_confidence_steps'] / self.stats['total_steps_generated'] * 100
                if self.stats['total_steps_generated'] > 0 else 0.0
            ),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("  CHAIN OF THOUGHT - STATISTICS")
        print("="*60)
        print(f"Total problems solved:     {stats['total_problems']}")
        print(f"Total steps generated:     {stats['total_steps_generated']}")
        print(f"Avg steps/problem:         {stats['avg_steps_per_problem']:.1f}")
        print(f"Low confidence steps:      {stats['low_confidence_steps']} ({stats['low_confidence_rate']:.1f}%)")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def chain_of_thought_reason(
    problem: str,
    context: Optional[Dict] = None,
    include_alternatives: bool = True
) -> ChainOfThoughtResult:
    """
    Helper function para raciocínio CoT

    Args:
        problem: Problema
        context: Contexto
        include_alternatives: Incluir alternativas

    Returns:
        ChainOfThoughtResult
    """
    cot = ChainOfThought()
    return cot.reason(problem, context, include_alternatives)
