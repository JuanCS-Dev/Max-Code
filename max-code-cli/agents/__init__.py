"""
Specialized Agents

Agentes especializados do Max-Code CLI.

AGENTS:
- PlanAgent: Planejamento (Port 8160)
- ExploreAgent: Exploração de codebase (Port 8161)
- CodeAgent: Geração de código (Port 8162)
- TestAgent: Geração de testes (Port 8163)
- ReviewAgent: Code review (Port 8164)
- FixAgent: Bug fixing (Port 8165)
- DocsAgent: Documentação (Port 8166)
- ArchitectAgent: Sophia - A Arquiteta, Co-Architect (Port 8167)
"""

from .plan_agent import PlanAgent
from .explore_agent import ExploreAgent
from .code_agent import CodeAgent
from .test_agent import TestAgent
from .review_agent import ReviewAgent
from .fix_agent import FixAgent
from .docs_agent import DocsAgent
from .architect_agent import ArchitectAgent

__all__ = [
    'PlanAgent',
    'ExploreAgent',
    'CodeAgent',
    'TestAgent',
    'ReviewAgent',
    'FixAgent',
    'DocsAgent',
    'ArchitectAgent',
]
