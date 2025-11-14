"""
Agent Orchestrator Implementation

Orquestra múltiplos agentes para resolver tarefas complexas.

Boris Cherny Standard:
- Type hints completos
- Structured logging (no print)
- Comprehensive docstrings
"""

from typing import List, Dict, Optional
import logging
from .base_agent import BaseAgent, AgentTask, AgentResult
from .agent_pool import AgentPool

# Structured logging
logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Agent Orchestrator - Multi-agent task coordination.

    Orquestra múltiplos agentes para resolver tarefas complexas através
    de execução sequencial ou paralela.

    Attributes:
        agent_pool: Pool de agentes disponíveis

    Example:
        >>> from sdk.agent_pool import AgentPool
        >>> from sdk.agent_orchestrator import AgentOrchestrator
        >>>
        >>> pool = AgentPool()
        >>> pool.register_agent(plan_agent)
        >>> pool.register_agent(code_agent)
        >>>
        >>> orchestrator = AgentOrchestrator(pool)
        >>> results = orchestrator.orchestrate(
        ...     task_description="Refactor auth module",
        ...     agent_sequence=["plan-001", "code-001", "test-001"]
        ... )
        >>> for result in results:
        ...     print(f"Agent {result.task_id}: {result.success}")

    Typical Workflow:
        1. Plan Agent → Generates refactoring plan
        2. Code Agent → Executes refactoring
        3. Test Agent → Runs test suite
        4. Review Agent → Performs code review
    """

    def __init__(self, agent_pool: AgentPool) -> None:
        """
        Initialize Agent Orchestrator.

        Args:
            agent_pool: Pool of available agents to orchestrate

        Raises:
            ValueError: If agent_pool is None
        """
        if agent_pool is None:
            raise ValueError("agent_pool cannot be None")

        self.agent_pool = agent_pool
        logger.info("Agent orchestrator initialized", extra={"pool_size": len(agent_pool.agents)})

    def orchestrate(
        self,
        task_description: str,
        agent_sequence: List[str]
    ) -> List[AgentResult]:
        """
        Orchestrate multiple agents in sequence.

        Executes agents in the specified order, passing context between them.
        Each agent receives the task description and results from previous agents.

        Args:
            task_description: Description of the task to accomplish
            agent_sequence: List of agent IDs to execute in order

        Returns:
            List of AgentResult, one per agent in sequence

        Raises:
            ValueError: If agent_sequence is empty
            KeyError: If an agent ID is not found in the pool

        Example:
            >>> results = orchestrator.orchestrate(
            ...     task_description="Add authentication to API",
            ...     agent_sequence=["sophia-001", "code-001", "test-001"]
            ... )
            >>> assert all(r.success for r in results)
        """
        if not agent_sequence:
            raise ValueError("agent_sequence cannot be empty")

        logger.info(
            "Orchestration started",
            extra={
                "task": task_description[:80],
                "agent_count": len(agent_sequence),
                "sequence": " → ".join(agent_sequence)
            }
        )

        results: List[AgentResult] = []

        for idx, agent_id in enumerate(agent_sequence, 1):
            logger.debug(
                f"Executing agent {idx}/{len(agent_sequence)}",
                extra={"agent_id": agent_id}
            )

            agent = self.agent_pool.get_agent(agent_id)
            if agent is None:
                error_msg = f"Agent '{agent_id}' not found in pool"
                logger.error(error_msg, extra={"agent_id": agent_id})
                raise KeyError(error_msg)

            # Create task with context from previous results
            task = AgentTask(
                id=f"orchestrated-{idx}",
                description=task_description,
                parameters={
                    "previous_results": results,
                    "sequence_position": idx,
                    "total_agents": len(agent_sequence)
                }
            )

            # Execute agent
            result = agent.run(task)
            results.append(result)

            # Log result
            if result.success:
                logger.info(
                    "Agent completed successfully",
                    extra={"agent_id": agent_id, "task_id": task.id}
                )
            else:
                logger.warning(
                    "Agent completed with failure",
                    extra={"agent_id": agent_id, "error": result.error}
                )

                # Optionally stop on failure (configurable)
                # For now, continue execution

        success_count = sum(1 for r in results if r.success)
        logger.info(
            "Orchestration completed",
            extra={
                "total_agents": len(agent_sequence),
                "successful": success_count,
                "failed": len(agent_sequence) - success_count
            }
        )

        return results

    def orchestrate_parallel(
        self,
        task_description: str,
        agent_ids: List[str]
    ) -> List[AgentResult]:
        """
        Orchestrate multiple agents in parallel (future implementation).

        Args:
            task_description: Description of the task
            agent_ids: List of agent IDs to execute in parallel

        Returns:
            List of AgentResult from all agents

        Note:
            Currently executes sequentially. True parallelization requires
            async/await or threading, which will be implemented in Phase 4.
        """
        logger.warning(
            "Parallel orchestration not yet implemented - falling back to sequential",
            extra={"agent_count": len(agent_ids)}
        )
        return self.orchestrate(task_description, agent_ids)

    def get_stats(self) -> Dict[str, int]:
        """
        Get orchestrator statistics.

        Returns:
            Dictionary with agent pool statistics

        Example:
            >>> stats = orchestrator.get_stats()
            >>> print(f"Total agents: {stats['total_agents']}")
        """
        return {
            "total_agents": len(self.agent_pool.agents),
            "registered_capabilities": len(set(
                cap
                for agent in self.agent_pool.agents.values()
                for cap in agent.get_capabilities()
            ))
        }


# ============================================================
# BORIS CHERNY STANDARDS
# ============================================================

# ✅ Type hints: 100%
# ✅ Docstrings: Google style, comprehensive
# ✅ Logging: Structured (no print statements)
# ✅ Error handling: Specific exceptions with context
# ✅ Examples: Included in docstrings
#
# "Código limpo que parece poesia" - Boris Cherny
