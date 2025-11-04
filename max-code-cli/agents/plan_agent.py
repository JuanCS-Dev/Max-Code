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

Biblical Foundation:
"Os pensamentos do diligente tendem só à abundância"
(Provérbios 21:5)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List, Optional
import asyncio
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult

# MAXIMUS Integration (v2.0)
from core.maximus_integration import (
    MaximusClient,
    DecisionFusion,
    FallbackSystem,
    MaximusCache,
)
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

        print(f"   🌳 Phase 1: Tree of Thoughts exploration...")

        # PHASE 1: Max-Code Tree of Thoughts (gera múltiplos planos)
        thoughts = []
        for i in range(3):  # Gerar 3 alternativas
            thought = self.tot.solve(
                problem=task.description,
                num_thoughts=1,
            )
            thoughts.append(thought)
            print(f"      ├─ Plan {i+1}: {thought.description[:60]}...")

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
                    print(f"   🧠 Phase 2: MAXIMUS systemic analysis...")

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
                            print(f"      ├─ Plan {plan['id']+1}: CACHE HIT")
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

                            print(f"      ├─ Plan {plan['id']+1}: Risk={analysis.systemic_risk_score:.2f} "
                                  f"(Confidence={analysis.confidence:.2f})")

                    # PHASE 3: Decision Fusion
                    print(f"   ⚖️  Phase 3: Decision fusion...")

                    best_plan = self.decision_fusion.fuse_plan_decisions(
                        maxcode_plans=maxcode_plans,
                        systemic_analyses=systemic_analyses
                    )

                    self.maximus_stats['hybrid_executions'] += 1

                    print(f"      └─ Selected: Plan {best_plan['plan']['id']+1} "
                          f"(Combined Score: {best_plan['confidence']:.2f})")

                    return AgentResult(
                        task_id=task.id,
                        success=True,
                        output={
                            'selected_plan': best_plan['plan'],
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
                print(f"      ⚠️  MAXIMUS unavailable: {e}")

        # FALLBACK: Standalone Max-Code (no MAXIMUS)
        print(f"   📊 Fallback: Standalone mode (Max-Code only)...")

        # Select best plan by ToT score only
        best_plan = max(maxcode_plans, key=lambda p: p['tot_score'])

        self.maximus_stats['standalone_executions'] += 1

        print(f"      └─ Selected: Plan {best_plan['id']+1} "
              f"(ToT Score: {best_plan['tot_score']:.2f})")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                'selected_plan': best_plan,
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
