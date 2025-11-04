"""
Plan Agent Implementation

Agent especializado em planejamento.

Port: 8160
Capability: PLANNING

Usa Tree of Thoughts para gerar múltiplos planos e selecionar o melhor.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult


class PlanAgent(BaseAgent):
    """
    Plan Agent

    Gera planos de ação usando Tree of Thoughts.
    """

    def __init__(self, agent_id: str = "plan_agent"):
        super().__init__(
            agent_id=agent_id,
            agent_name="Plan Agent",
            port=8160,
        )

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.PLANNING]

    def execute(self, task: AgentTask) -> AgentResult:
        """
        Executa planejamento usando ToT

        Args:
            task: Task com description do problema

        Returns:
            AgentResult com plano
        """
        print(f"   🧠 Planning: Using Tree of Thoughts...")

        # Usar ToT para gerar plano
        thought = self.tot.solve(
            problem=task.description,
            num_thoughts=3,  # Gerar 3 alternativas
        )

        # Extrair plano
        plan = {
            'approach': thought.description,
            'steps': thought.implementation_plan or [],
            'pros': thought.pros,
            'cons': thought.cons,
            'complexity': thought.complexity,
        }

        return AgentResult(
            task_id=task.id,
            success=True,
            output=plan,
        )
