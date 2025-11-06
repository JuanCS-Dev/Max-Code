"""
Base Agent Implementation

Classe base para todos os agentes especializados.

"A cada um é dada a manifestação do Espírito para o proveito comum"
(1 Coríntios 12:7)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import os
import sys

# Add parent directories to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.constitutional.engine import ConstitutionalEngine
from core.deter_agent.deliberation import TreeOfThoughts, ChainOfThought
from core.deter_agent.state import MemoryManager
from core.deter_agent.execution import ToolExecutor, TDDEnforcer
from core.deter_agent.incentive import MetricsTracker, RewardModel


class AgentCapability(Enum):
    """Capacidades que um agente pode ter"""
    PLANNING = "planning"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    DEBUGGING = "debugging"
    EXPLORATION = "exploration"


@dataclass
class AgentTask:
    """Uma tarefa para o agente"""
    id: str
    description: str
    parameters: Dict[str, Any]
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL


@dataclass
class AgentResult:
    """
    Resultado da execução do agente

    Automaticamente adiciona comentário de Dream (The Realist Contrarian)
    ao output para fornecer perspectiva alternativa e sugestões construtivas.
    """
    task_id: str
    success: bool
    output: Any
    error: Optional[str] = None
    metrics: Optional[Dict] = None
    dream_comment: Optional[str] = None  # Comentário realista construtivo do Dream

    def __post_init__(self):
        """Adiciona Dream comment automaticamente se não fornecido."""
        # Import here to avoid circular dependency
        from core.skeptic import add_skeptical_comment, SkepticalTone

        # Se dream_comment já foi fornecido, não sobrescrever
        if self.dream_comment is not None:
            return

        # Se output é string, adicionar Dream comment
        if isinstance(self.output, str) and len(self.output) > 100:
            # Build context from metrics
            context = self.metrics if self.metrics else {}

            # Add Dream comment (BALANCED tone by default)
            try:
                output_with_dream = add_skeptical_comment(
                    self.output,
                    context,
                    tone=SkepticalTone.BALANCED
                )
                # Store Dream comment separately (don't modify output)
                # Extract just the Dream part
                if "Dream (The" in output_with_dream:
                    dream_start = output_with_dream.find("="*70, len(self.output))
                    if dream_start > 0:
                        self.dream_comment = output_with_dream[dream_start:]
            except Exception:
                # If Dream fails, don't break AgentResult
                self.dream_comment = None

    def get_full_output(self) -> str:
        """
        Retorna output completo com Dream comment incluído.

        Use este método para obter output + análise realista do Dream.
        """
        if self.dream_comment:
            return str(self.output) + "\n" + self.dream_comment
        return str(self.output)

    def print_with_dream(self):
        """Imprime resultado com Dream comment."""
        print(self.get_full_output())


class BaseAgent(ABC):
    """
    Base Agent

    Classe abstrata base para todos os agentes especializados.

    TODOS os agentes herdam desta classe e implementam:
    - execute(): Lógica principal do agente
    - get_capabilities(): Quais capabilities o agente tem

    TODOS os agentes têm acesso a:
    - Constitutional Engine (P1-P6 validation)
    - DETER-AGENT layers (Deliberation, State, Execution, Incentive)
    - Memory Manager
    - Tool Executor
    - Metrics Tracker

    EXEMPLO:
    ```python
    class PlanAgent(BaseAgent):
        def get_capabilities(self) -> List[AgentCapability]:
            return [AgentCapability.PLANNING]

        def execute(self, task: AgentTask) -> AgentResult:
            # Usar ToT para gerar plano
            tot = self.tot
            thought = tot.solve(task.description)
            return AgentResult(
                task_id=task.id,
                success=True,
                output=thought,
            )
    ```
    """

    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        port: Optional[int] = None
    ):
        """
        Inicializa agente

        Args:
            agent_id: ID único do agente
            agent_name: Nome do agente
            port: Porta (para agentes que rodam como serviço)
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.port = port

        # Constitutional Core
        self.constitutional_engine = ConstitutionalEngine()

        # DETER-AGENT Layers
        self.tot = TreeOfThoughts()  # Layer 2: Deliberation
        self.cot = ChainOfThought()  # Layer 2: Deliberation
        self.memory = MemoryManager()  # Layer 3: State
        self.tools = ToolExecutor()  # Layer 4: Execution
        self.tdd = TDDEnforcer()  # Layer 4: Execution
        self.metrics = MetricsTracker()  # Layer 5: Incentive
        self.rewards = RewardModel()  # Layer 5: Incentive

        # Stats
        self.stats = {
            'total_tasks_executed': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
        }

        print(f"🤖 Agent '{self.agent_name}' initialized (ID: {self.agent_id})")

    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """
        Retorna capabilities do agente

        Deve ser implementado por subclasses.
        """
        pass

    @abstractmethod
    def execute(self, task: AgentTask) -> AgentResult:
        """
        Executa tarefa

        Deve ser implementado por subclasses.

        Args:
            task: Tarefa a executar

        Returns:
            AgentResult
        """
        pass

    def run(self, task: AgentTask) -> AgentResult:
        """
        Wrapper público para execute() que adiciona tracking e validação

        Este método NÃO deve ser sobrescrito.
        """
        self.stats['total_tasks_executed'] += 1

        print(f"\n▶️  Agent '{self.agent_name}': Starting task '{task.id}'")
        print(f"   Description: {task.description[:80]}...")

        try:
            # Execute task (implementado por subclass)
            result = self.execute(task)

            if result.success:
                self.stats['successful_tasks'] += 1
            else:
                self.stats['failed_tasks'] += 1

            print(f"   {'✓' if result.success else '❌'} Task completed (success: {result.success})")

            return result

        except Exception as e:
            self.stats['failed_tasks'] += 1
            print(f"   ❌ Task failed with exception: {e}")

            return AgentResult(
                task_id=task.id,
                success=False,
                output=None,
                error=str(e),
            )

    def get_stats(self) -> Dict:
        """Retorna estatísticas do agente"""
        total = self.stats['total_tasks_executed']
        return {
            **self.stats,
            'success_rate': (
                self.stats['successful_tasks'] / total * 100
                if total > 0 else 0.0
            ),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print(f"\n{'='*60}")
        print(f"  AGENT '{self.agent_name}' - STATISTICS")
        print(f"{'='*60}")
        print(f"Total tasks:               {stats['total_tasks_executed']}")
        print(f"Successful:                {stats['successful_tasks']} ({stats['success_rate']:.1f}%)")
        print(f"Failed:                    {stats['failed_tasks']}")
        print(f"{'='*60}\n")


# ==================== HELPER FUNCTIONS ====================

def create_agent_task(description: str, **parameters) -> AgentTask:
    """Helper para criar AgentTask"""
    import time
    return AgentTask(
        id=f"task_{int(time.time()*1000)}",
        description=description,
        parameters=parameters,
    )
