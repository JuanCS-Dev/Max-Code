"""
Agent Pool Implementation

Gerencia pool de agentes.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent, AgentTask, AgentResult


class AgentPool:
    """
    Agent Pool

    Gerencia múltiplos agentes.
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        """Registra agente no pool"""
        self.agents[agent.agent_id] = agent
        print(f"📋 Agent Pool: Registered '{agent.agent_name}' (ID: {agent.agent_id})")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Retorna agente pelo ID"""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> List[BaseAgent]:
        """Retorna todos os agentes"""
        return list(self.agents.values())

    def execute_task(self, agent_id: str, task: AgentTask) -> AgentResult:
        """Executa task em agente específico"""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found in pool")

        return agent.run(task)
