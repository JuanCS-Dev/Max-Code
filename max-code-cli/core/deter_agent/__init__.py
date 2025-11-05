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

# Layer 2 - Deliberation
from .deliberation import (
    TreeOfThoughts,
    SelfConsistency,
    ChainOfThought,
    AdversarialCritic,
    Thought,
    ThoughtEvaluation,
)

# Layer 3 - State Management
from .state.memory_manager import MemoryManager, MemoryType, MemoryImportance
from .state.context_compression import ContextCompressor
from .state.progressive_disclosure import ProgressiveDisclosure
from .state.sub_agent_isolation import SubAgentIsolation

# Layer 4 - Execution
from .execution.tool_executor import ToolExecutor
from .execution.tdd_enforcer import TDDEnforcer
from .execution.self_correction import SelfCorrectionEngine
from .execution.git_native import GitNativeWorkflow
from .execution.bugbot import BugBot
from .execution.action_validator import ActionValidator

# Layer 5 - Incentive
from .incentive.reward_model import RewardModel
from .incentive.metrics_tracker import MetricsTracker
from .incentive.performance_monitor import PerformanceMonitor
from .incentive.feedback_loop import FeedbackLoop

__all__ = [
    # Deliberation (Layer 2)
    'TreeOfThoughts',
    'SelfConsistency',
    'ChainOfThought',
    'AdversarialCritic',
    'Thought',
    'ThoughtEvaluation',
    # State Management (Layer 3)
    'MemoryManager',
    'MemoryType',
    'MemoryImportance',
    'ContextCompressor',
    'ProgressiveDisclosure',
    'SubAgentIsolation',
    # Execution (Layer 4)
    'ToolExecutor',
    'TDDEnforcer',
    'SelfCorrectionEngine',
    'GitNativeWorkflow',
    'BugBot',
    'ActionValidator',
    # Incentive (Layer 5)
    'RewardModel',
    'MetricsTracker',
    'PerformanceMonitor',
    'FeedbackLoop',
]
