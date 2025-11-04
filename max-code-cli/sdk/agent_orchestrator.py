"""
Agent Orchestrator Implementation

Orquestra múltiplos agentes para resolver tarefas complexas.
"""

from typing import List, Dict
from .base_agent import BaseAgent, AgentTask, AgentResult
from .agent_pool import AgentPool


class AgentOrchestrator:
    """
    Agent Orchestrator

    Orquestra múltiplos agentes.

    EXEMPLO:
    ```
    Task: "Refatorar módulo auth.py"

    Orchestrator:
    1. Agent Plan → Gera plano de refactoring
    2. Agent Code → Executa refactoring
    3. Agent Test → Roda testes
    4. Agent Review → Code review
    ```
    """

    def __init__(self, agent_pool: AgentPool):
        self.agent_pool = agent_pool

    def orchestrate(
        self,
        task_description: str,
        agent_sequence: List[str]
    ) -> List[AgentResult]:
        """
        Orquestra múltiplos agentes em sequência

        Args:
            task_description: Descrição da tarefa
            agent_sequence: Lista de agent_ids em ordem

        Returns:
            Lista de AgentResult (um por agente)
        """
        print(f"🎭 Orchestrator: Starting task '{task_description[:50]}...'")
        print(f"   Agent sequence: {' → '.join(agent_sequence)}")

        results = []

        for agent_id in agent_sequence:
            # Criar task
            task = AgentTask(
                id=f"{agent_id}_task",
                description=task_description,
                parameters={},
            )

            # Executar
            result = self.agent_pool.execute_task(agent_id, task)
            results.append(result)

            # Se falhou, parar sequência
            if not result.success:
                print(f"   ❌ Sequence stopped: Agent '{agent_id}' failed")
                break

        print(f"   ✓ Orchestration complete ({len(results)}/{len(agent_sequence)} agents executed)")

        return results
