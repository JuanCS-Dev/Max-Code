"""
Max-Code Agent SDK

SDK para criar agentes especializados no Max-Code CLI.

COMPONENTES:
1. BaseAgent: Classe base para todos os agentes
2. AgentPool: Pool de agentes (gerenciamento)
3. AgentRegistry: Registry de agentes disponíveis
4. AgentOrchestrator: Orquestração de múltiplos agentes

"Porque, assim como o corpo é um e tem muitos membros, e todos os membros,
 sendo muitos, são um só corpo, assim é Cristo também." (1 Coríntios 12:12)
"""

from .base_agent import BaseAgent, AgentCapability
from .agent_pool import AgentPool
from .agent_registry import AgentRegistry
from .agent_orchestrator import AgentOrchestrator

__all__ = [
    'BaseAgent',
    'AgentCapability',
    'AgentPool',
    'AgentRegistry',
    'AgentOrchestrator',
]
