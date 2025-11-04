"""
Agent Registry Implementation

Registry de agentes disponíveis (catálogo).
"""

from typing import Dict, List, Type
from .base_agent import BaseAgent, AgentCapability


class AgentRegistry:
    """
    Agent Registry

    Catálogo de tipos de agentes disponíveis.
    """

    def __init__(self):
        self.agent_classes: Dict[str, Type[BaseAgent]] = {}

    def register_agent_class(self, agent_type: str, agent_class: Type[BaseAgent]):
        """Registra classe de agente"""
        self.agent_classes[agent_type] = agent_class
        print(f"📚 Agent Registry: Registered agent type '{agent_type}'")

    def get_agent_class(self, agent_type: str) -> Type[BaseAgent]:
        """Retorna classe de agente"""
        if agent_type not in self.agent_classes:
            raise ValueError(f"Agent type '{agent_type}' not registered")

        return self.agent_classes[agent_type]

    def instantiate_agent(self, agent_type: str, agent_id: str, **kwargs) -> BaseAgent:
        """Instancia agente"""
        agent_class = self.get_agent_class(agent_type)
        return agent_class(agent_id=agent_id, **kwargs)

    def list_agent_types(self) -> List[str]:
        """Lista tipos de agentes disponíveis"""
        return list(self.agent_classes.keys())
