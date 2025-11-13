"""
Plan Agent Implementation - ENHANCED with MAXIMUS

Agent especializado em planejamento com análise sistêmica profunda.

Port: 8160
Capability: PLANNING

v2.0 Features:
- Tree of Thoughts para gerar múltiplos planos (Max-Code)
- Systemic Impact Analysis para cada plano (MAXIMUS)
- Decision Fusion para selecionar melhor plano
- Fallback automático se MAXIMUS offline

v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)

Biblical Foundation:
"Os pensamentos do diligente tendem só à abundância"
(Provérbios 21:5)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List, Optional
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from config.logging_config import get_logger

logger = get_logger(__name__)

# MAXIMUS Integration (v2.0)
from core.maximus_integration import (
    MaximusClient,
    DecisionFusion,
    FallbackSystem,
    MaximusCache,
)
from agents.validation_schemas import PlanAgentParameters, validate_task_parameters
from core.maximus_integration.decision_fusion import Decision, DecisionType
from core.maximus_integration.fallback import FallbackStrategy


class PlanAgent(BaseAgent):
    """
    Plan Agent v2.0 (MAXIMUS-Enhanced)

    Hybrid Max-Code + MAXIMUS planning:
    - Max-Code: Tree of Thoughts exploration (3-5 plans)
    - MAXIMUS: Systemic impact analysis of each plan
    - Fusion: Select plan with lowest systemic risk + highest ToT score

    Fallback: If MAXIMUS offline, use standalone Max-Code ToT
    """

    def __init__(
        self,
        agent_id: str = "plan_agent",
        enable_maximus: bool = True,
        maximus_url: str = "http://localhost:8153",
    ):
        super().__init__(
            agent_id=agent_id,
            agent_name="Plan Agent (MAXIMUS-Enhanced)",
            port=8160,
        )

        # MAXIMUS Integration
        self.enable_maximus = enable_maximus
        self.maximus_client = MaximusClient(base_url=maximus_url) if enable_maximus else None
        self.decision_fusion = DecisionFusion(maxcode_weight=0.6, maximus_weight=0.4)
        self.fallback = FallbackSystem(default_strategy=FallbackStrategy.AUTO_FALLBACK)
        self.cache = MaximusCache()

        # Stats
        self.maximus_stats = {
            'hybrid_executions': 0,
            'standalone_executions': 0,
            'cache_hits': 0,
        }

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.PLANNING]

    def execute(self, task: AgentTask) -> AgentResult:
        """
        Executa planejamento híbrido (Max-Code + MAXIMUS)

        Args:
            task: Task com description do problema

        Returns:
            AgentResult com best plan selecionado
        """
        # Run async execution in sync context
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        """Async execution for MAXIMUS calls"""

        # Validate input parameters
        # ERGONOMICS FIX: If parameters are empty, use task.description as goal
        parameters = task.parameters or {}
        if not parameters.get('goal') and task.description:
            parameters = {'goal': task.description}
            logger.info("Using task description as goal", extra={"task_id": task.id})

        try:
            params = validate_task_parameters('plan', parameters)
            logger.info("Parameters validated", extra={"task_id": task.id})
        except ValidationError as e:
            logger.error(f"Invalid parameters: {e}", extra={"task_id": task.id, "error_details": e.errors()})
            return AgentResult(
                task_id=task.id,
                success=False,
                output={'error': 'Invalid parameters', 'details': e.errors()},
                metrics={'validation_failed': True}
            )

        logger.info("Starting Phase 1: Tree of Thoughts exploration", extra={"task_id": task.id})

        # PHASE 1: Max-Code Tree of Thoughts (gera múltiplos planos)
        thoughts = []
        for i in range(3):  # Gerar 3 alternativas
            thought = self.tot.solve(
                problem=task.description,
                num_thoughts=1,
            )
            thoughts.append(thought)
            logger.debug(
                f"Generated plan {i+1}: {thought.description[:60]}...",
                extra={"task_id": task.id, "plan_id": i+1, "complexity": thought.complexity}
            )

        # Convert thoughts to plans
        maxcode_plans = [
            {
                'id': i,
                'approach': thought.description,
                'steps': thought.implementation_plan or [],
                'pros': thought.pros,
                'cons': thought.cons,
                'complexity': thought.complexity,
                'tot_score': self._calculate_tot_score(thought),
            }
            for i, thought in enumerate(thoughts)
        ]

        # PHASE 2: MAXIMUS Systemic Analysis (optional)
        if self.enable_maximus and self.maximus_client:
            try:
                maximus_online = await self.maximus_client.health_check()

                if maximus_online:
                    logger.info("Starting Phase 2: MAXIMUS systemic analysis", extra={"task_id": task.id})

                    systemic_analyses = []
                    for plan in maxcode_plans:
                        # Check cache first
                        cached = self.cache.get_systemic_analysis(
                            action={"type": "plan", "plan": plan},
                            context={"task": task.description}
                        )

                        if cached:
                            systemic_analyses.append(cached)
                            self.maximus_stats['cache_hits'] += 1
                            logger.debug(
                                "MAXIMUS cache hit",
                                extra={"task_id": task.id, "plan_id": plan['id']+1}
                            )
                        else:
                            # Call MAXIMUS
                            analysis = await self.maximus_client.analyze_systemic_impact(
                                action={
                                    "type": "plan",
                                    "approach": plan['approach'],
                                    "steps": plan['steps'],
                                },
                                context={
                                    "task_description": task.description,
                                    "complexity": plan['complexity'],
                                }
                            )

                            systemic_analyses.append(analysis)

                            # Cache result
                            self.cache.set_systemic_analysis(
                                action={"type": "plan", "plan": plan},
                                context={"task": task.description},
                                result=analysis
                            )

                            logger.info(
                                f"MAXIMUS analysis completed for plan {plan['id']+1}",
                                extra={
                                    "task_id": task.id,
                                    "plan_id": plan['id']+1,
                                    "systemic_risk_score": analysis.systemic_risk_score,
                                    "confidence": analysis.confidence
                                }
                            )

                    # PHASE 3: Decision Fusion
                    logger.info("Starting Phase 3: Decision fusion", extra={"task_id": task.id})

                    best_plan = self.decision_fusion.fuse_plan_decisions(
                        maxcode_plans=maxcode_plans,
                        systemic_analyses=systemic_analyses
                    )

                    self.maximus_stats['hybrid_executions'] += 1

                    logger.info(
                        f"Plan selected via decision fusion: Plan {best_plan['plan']['id']+1}",
                        extra={
                            "task_id": task.id,
                            "selected_plan_id": best_plan['plan']['id']+1,
                            "combined_score": best_plan['confidence']
                        }
                    )

                    return AgentResult(
                        task_id=task.id,
                        success=True,
                        output={
                            'selected_plan': best_plan['plan'],
                            'plan': best_plan['plan'],  # Alias for test compatibility
                            'systemic_analysis': best_plan['systemic_analysis'],
                            'all_plans': best_plan['all_options'],
                            'mode': 'HYBRID',
                            'confidence': best_plan['confidence'],
                        },
                        metrics={
                            'mode': 'hybrid',
                            'plans_explored': len(maxcode_plans),
                            'maximus_online': True,
                        }
                    )

            except Exception as e:
                logger.warning(
                    f"MAXIMUS unavailable: {type(e).__name__}",
                    extra={"task_id": task.id, "error_type": type(e).__name__}
                )

        # FALLBACK: Standalone Max-Code (no MAXIMUS)
        logger.info("Fallback: Standalone mode (Max-Code only)", extra={"task_id": task.id})

        # Select best plan by ToT score only
        best_plan = max(maxcode_plans, key=lambda p: p['tot_score'])

        self.maximus_stats['standalone_executions'] += 1

        logger.info(
            f"Plan selected (standalone): Plan {best_plan['id']+1}",
            extra={
                "task_id": task.id,
                "selected_plan_id": best_plan['id']+1,
                "tot_score": best_plan['tot_score']
            }
        )

        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                'selected_plan': best_plan,
                'plan': best_plan,  # Alias for test compatibility
                'all_plans': maxcode_plans,
                'mode': 'STANDALONE',
                'confidence': best_plan['tot_score'],
            },
            metrics={
                'mode': 'standalone',
                'plans_explored': len(maxcode_plans),
                'maximus_online': False,
            }
        )

    def _calculate_tot_score(self, thought) -> float:
        """
        Calculate ToT score for a thought

        Score based on:
        - Number of pros vs cons
        - Complexity (lower is better)
        """
        pros_score = len(thought.pros) * 0.2
        cons_score = len(thought.cons) * -0.15

        # Complexity: LOW=1.0, MEDIUM=0.7, HIGH=0.4
        complexity_map = {'LOW': 1.0, 'MEDIUM': 0.7, 'HIGH': 0.4}
        complexity_score = complexity_map.get(thought.complexity, 0.5)

        total = max(0.0, min(1.0, 0.5 + pros_score + cons_score + complexity_score * 0.3))
        return total

    def get_maximus_stats(self) -> dict:
        """Get MAXIMUS integration statistics"""
        total = self.maximus_stats['hybrid_executions'] + self.maximus_stats['standalone_executions']
        return {
            **self.maximus_stats,
            'total_executions': total,
            'hybrid_rate': (
                self.maximus_stats['hybrid_executions'] / total * 100
                if total > 0 else 0.0
            ),
        }

    async def close(self):
        """Close MAXIMUS client"""
        if self.maximus_client:
            await self.maximus_client.close()
