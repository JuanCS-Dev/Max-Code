"""
Sophia - A Arquiteta (Strategic Co-Architect with Systemic Vision)

Sophia é a agente mais nobre - atua como Co-Arquiteta Cética,
com visão sistêmica macro e sabedoria arquitetural profunda.

Nome: Sophia (do grego Σοφία - "Sabedoria")
Port: 8167
Capability: ARCHITECTURE

Biblical Foundation:
"A sabedoria edificou a sua casa" (Provérbios 9:1)

"Porque com sabedoria se edifica a casa, e com a inteligência ela se firma;
e pelo conhecimento se encherão as câmaras com todo o bem precioso e agradável"
(Provérbios 24:3-4)

"Examinai tudo. Retende o bem."
(1 Tessalonicenses 5:21)

Responsibilities:
- Visão sistêmica macro (holistic thinking)
- Planejamento estratégico (roadmaps, blueprints)
- Ceticismo crítico (P3 - desafia premissas com sabedoria)
- Análise de trade-offs (performance vs complexity, etc)
- Identificação de riscos arquiteturais
- Sugestões de design patterns
- Validação de decisões técnicas
- Mentoria arquitetural (ensina e guia o Arquiteto-Chefe)

Integration:
- MAXIMUS MAPE-K: Monitor, Analyze, Plan, Execute, Knowledge
- Tree of Thoughts: Exploração de múltiplas estratégias
- Adversarial Critic: Red team self-criticism com sabedoria
- Decision Fusion: Combina Max-Code + MAXIMUS wisdom

Personality:
- Sábia e ponderada
- Questiona com respeito mas firmeza
- Visão de longo prazo
- Foca em sustentabilidade e manutenibilidade
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List, Dict, Any, Optional
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult

# MAXIMUS Integration
from core.maximus_integration import (
    MaximusClient,
    DecisionFusion,
    FallbackSystem,
    MaximusCache,
)
from core.maximus_integration.decision_fusion import Decision, DecisionType


# ============================================================================
# ENUMS & DATA MODELS
# ============================================================================

class ArchitecturalConcern(str, Enum):
    """Preocupações arquiteturais"""
    SCALABILITY = "scalability"
    MAINTAINABILITY = "maintainability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    RELIABILITY = "reliability"
    TESTABILITY = "testability"
    COMPLEXITY = "complexity"
    COUPLING = "coupling"
    COHESION = "cohesion"


class DecisionImpact(str, Enum):
    """Impacto de decisão arquitetural"""
    LOW = "low"           # Mudança local, sem impacto sistêmico
    MEDIUM = "medium"     # Afeta múltiplos componentes
    HIGH = "high"         # Afeta arquitetura core
    CRITICAL = "critical" # Quebra compatibilidade, requer migração


@dataclass
class ArchitecturalRisk:
    """Risco arquitetural identificado"""
    concern: ArchitecturalConcern
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    mitigation: str
    probability: float  # 0.0 to 1.0


@dataclass
class DesignPattern:
    """Sugestão de design pattern"""
    name: str
    category: str  # Creational, Structural, Behavioral
    use_case: str
    pros: List[str]
    cons: List[str]
    complexity: str  # LOW, MEDIUM, HIGH


@dataclass
class ArchitecturalDecision:
    """Decisão arquitetural com rastreabilidade"""
    id: str
    decision: str
    rationale: str
    alternatives_considered: List[str]
    trade_offs: Dict[str, str]
    impact: DecisionImpact
    risks: List[ArchitecturalRisk]
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# ARCHITECT AGENT
# ============================================================================

class ArchitectAgent(BaseAgent):
    """
    Sophia - A Arquiteta (Strategic Co-Architect)

    A Co-Arquiteta Cética com visão sistêmica macro e sabedoria profunda.

    "A sabedoria edificou a sua casa" (Provérbios 9:1)

    Capabilities:
    1. **Visão Sistêmica**: Analisa impacto holístico de decisões
    2. **Planejamento Estratégico**: Cria roadmaps e blueprints
    3. **Ceticismo Crítico**: Desafia premissas com sabedoria e firmeza
    4. **Trade-off Analysis**: Avalia pros/cons de cada abordagem
    5. **Pattern Suggestion**: Recomenda design patterns apropriados
    6. **Risk Assessment**: Identifica e mitiga riscos arquiteturais
    7. **Mentoria Arquitetural**: Ensina e guia o Arquiteto-Chefe

    Hybrid Intelligence:
    - Max-Code: Tree of Thoughts (exploração de estratégias)
    - MAXIMUS: MAPE-K loop (análise sistêmica profunda)
    - Fusion: Melhor decisão arquitetural

    Personality:
    - Sábia e ponderada (não se apressa)
    - Questiona com respeito mas firmeza
    - Visão de longo prazo (sustentabilidade > velocidade)
    - Foca em manutenibilidade e simplicidade

    Example:
        sophia = ArchitectAgent()  # Sophia - A Arquiteta

        task = create_agent_task(
            description="Design a distributed caching system",
            requirements=["low latency", "high availability"],
            constraints=["budget limited", "team size: 3"]
        )

        result = sophia.run(task)
        decision = result.output['architectural_decision']
        print(f"Sophia's Decision: {decision.decision}")
        print(f"Rationale: {decision.rationale}")
        for risk in decision.risks:
            print(f"⚠️ Sophia warns: {risk.description}")
    """

    def __init__(
        self,
        agent_id: str = "sophia",
        enable_maximus: bool = True,
        maximus_url: str = "http://localhost:8153",
    ):
        super().__init__(
            agent_id=agent_id,
            agent_name="Sophia - A Arquiteta (Co-Architect)",
            port=8167,
        )

        # MAXIMUS Integration
        self.enable_maximus = enable_maximus
        self.maximus_client = MaximusClient(base_url=maximus_url) if enable_maximus else None
        self.decision_fusion = DecisionFusion(maxcode_weight=0.5, maximus_weight=0.5)  # Equal weight for architecture
        self.fallback = FallbackSystem()
        self.cache = MaximusCache()

        # Architect-specific state
        self.decision_history: List[ArchitecturalDecision] = []
        self.knowledge_base = {
            "patterns": self._load_design_patterns(),
            "principles": self._load_architectural_principles(),
        }

    def get_capabilities(self) -> List[AgentCapability]:
        # Architect has multiple high-level capabilities
        return [
            AgentCapability.PLANNING,
            AgentCapability.CODE_REVIEW,
            AgentCapability.REFACTORING,
        ]

    # ========================================================================
    # MAIN EXECUTION
    # ========================================================================

    def execute(self, task: AgentTask) -> AgentResult:
        """Execute architectural analysis"""
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        """Async execution for MAXIMUS integration"""

        print(f"\n{'='*70}")
        print(f"   👑 SOPHIA - A Arquiteta (Strategic Analysis)")
        print(f"   'A sabedoria edificou a sua casa' (Provérbios 9:1)")
        print(f"{'='*70}")

        # PHASE 1: Understanding (Monitor)
        print(f"\n   📊 Phase 1: MONITOR - Understanding the problem...")
        problem_analysis = self._analyze_problem(task)
        print(f"      ├─ Domain: {problem_analysis['domain']}")
        print(f"      ├─ Complexity: {problem_analysis['complexity']}")
        print(f"      └─ Constraints: {len(problem_analysis['constraints'])} identified")

        # PHASE 2: Exploration (Tree of Thoughts)
        print(f"\n   🌳 Phase 2: EXPLORE - Tree of Thoughts (architectural options)...")
        architectural_options = self._explore_architectural_options(task, problem_analysis)

        for i, option in enumerate(architectural_options):
            print(f"      ├─ Option {i+1}: {option['approach']}")
            print(f"      │  ├─ Patterns: {', '.join(option['patterns'][:2])}")
            print(f"      │  └─ Complexity: {option['complexity']}")

        # PHASE 3: MAXIMUS Systemic Analysis (Analyze + Plan)
        systemic_analyses = []
        if self.enable_maximus and self.maximus_client:
            try:
                maximus_online = await self.maximus_client.health_check()

                if maximus_online:
                    print(f"\n   🧠 Phase 3: MAXIMUS MAPE-K - Systemic analysis...")

                    for i, option in enumerate(architectural_options):
                        # MAXIMUS MAPE-K: Analyze systemic impact
                        analysis = await self.maximus_client.analyze_systemic_impact(
                            action={
                                "type": "architectural_decision",
                                "approach": option['approach'],
                                "patterns": option['patterns'],
                                "impact_scope": option['impact'],
                            },
                            context={
                                "task": task.description,
                                "requirements": problem_analysis.get('requirements', []),
                                "constraints": problem_analysis.get('constraints', []),
                            }
                        )

                        systemic_analyses.append(analysis)

                        print(f"      ├─ Option {i+1}: Systemic Risk = {analysis.systemic_risk_score:.2f}")
                        print(f"      │  ├─ Affected components: {len(analysis.affected_components)}")
                        if analysis.side_effects:
                            print(f"      │  └─ Side effects: {len(analysis.side_effects)}")

            except Exception as e:
                print(f"      ⚠️  MAXIMUS unavailable: {e}")

        # PHASE 4: Adversarial Criticism (Red Team)
        print(f"\n   🔴 Phase 4: RED TEAM - Adversarial criticism...")
        for i, option in enumerate(architectural_options):
            criticisms = self._red_team_criticism(option)
            option['criticisms'] = criticisms
            print(f"      ├─ Option {i+1}: {len(criticisms)} concerns identified")

        # PHASE 5: Decision Fusion & Selection
        print(f"\n   ⚖️  Phase 5: FUSION - Selecting best architectural approach...")

        if systemic_analyses:
            # Hybrid: Combine Max-Code + MAXIMUS
            best_decision = self._fuse_architectural_decisions(
                architectural_options,
                systemic_analyses
            )
            mode = "HYBRID"
        else:
            # Standalone: Max-Code only
            best_decision = self._select_best_option_standalone(architectural_options)
            mode = "STANDALONE"

        print(f"      └─ Selected: {best_decision['approach']}")
        print(f"         ├─ Confidence: {best_decision['confidence']:.2f}")
        print(f"         └─ Rationale: {best_decision['rationale'][:60]}...")

        # PHASE 6: Documentation (Execute + Knowledge)
        print(f"\n   📝 Phase 6: DOCUMENT - Creating architectural decision record...")
        adr = self._create_architectural_decision_record(best_decision, task)
        self.decision_history.append(adr)

        print(f"      └─ ADR-{adr.id} created")
        print(f"\n{'='*70}\n")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                'architectural_decision': adr,
                'all_options': architectural_options,
                'systemic_analyses': systemic_analyses if systemic_analyses else None,
                'mode': mode,
                'confidence': best_decision['confidence'],
            },
            metrics={
                'mode': mode.lower(),
                'options_explored': len(architectural_options),
                'maximus_online': bool(systemic_analyses),
                'risks_identified': len(adr.risks),
            }
        )

    # ========================================================================
    # ARCHITECTURAL ANALYSIS METHODS
    # ========================================================================

    def _analyze_problem(self, task: AgentTask) -> Dict[str, Any]:
        """
        PHASE 1: Monitor - Analyze and understand the problem

        Uses Chain of Thought reasoning to break down requirements
        """
        # Extract problem domain
        description_lower = task.description.lower()

        # Identify domain
        if any(kw in description_lower for kw in ['cache', 'redis', 'memory']):
            domain = "caching"
        elif any(kw in description_lower for kw in ['api', 'rest', 'graphql', 'endpoint']):
            domain = "api_design"
        elif any(kw in description_lower for kw in ['database', 'sql', 'nosql', 'storage']):
            domain = "data_storage"
        elif any(kw in description_lower for kw in ['microservice', 'distributed', 'service']):
            domain = "distributed_systems"
        elif any(kw in description_lower for kw in ['auth', 'authentication', 'authorization']):
            domain = "security"
        else:
            domain = "general"

        # Determine complexity
        if any(kw in description_lower for kw in ['distributed', 'scale', 'high availability']):
            complexity = "HIGH"
        elif any(kw in description_lower for kw in ['microservice', 'integrate', 'multiple']):
            complexity = "MEDIUM"
        else:
            complexity = "LOW"

        # Extract requirements and constraints from parameters
        requirements = task.parameters.get('requirements', [])
        constraints = task.parameters.get('constraints', [])

        # Identify concerns
        concerns = []
        if 'scale' in description_lower or 'performance' in description_lower:
            concerns.append(ArchitecturalConcern.SCALABILITY)
            concerns.append(ArchitecturalConcern.PERFORMANCE)
        if 'maintain' in description_lower or 'complexity' in description_lower:
            concerns.append(ArchitecturalConcern.MAINTAINABILITY)
        if 'security' in description_lower or 'auth' in description_lower:
            concerns.append(ArchitecturalConcern.SECURITY)

        if not concerns:
            concerns = [ArchitecturalConcern.MAINTAINABILITY]

        return {
            'domain': domain,
            'complexity': complexity,
            'requirements': requirements,
            'constraints': constraints,
            'concerns': concerns,
        }

    def _explore_architectural_options(
        self,
        task: AgentTask,
        problem_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        PHASE 2: Explore - Generate multiple architectural approaches

        Uses Tree of Thoughts to explore different strategies
        """
        # Use ToT to generate multiple thoughts
        options = []

        for i in range(3):  # Generate 3 architectural options
            thought = self.tot.solve(
                problem=f"Architectural design for: {task.description}",
                num_thoughts=1,
            )

            # Enrich with architectural metadata
            option = {
                'id': i,
                'approach': thought.description,
                'steps': thought.implementation_plan or [],
                'patterns': self._identify_patterns(thought.description),
                'complexity': thought.complexity,
                'pros': thought.pros,
                'cons': thought.cons,
                'impact': self._estimate_impact(thought.description),
                'criticisms': [],  # Will be filled in red team phase
            }

            options.append(option)

        return options

    def _identify_patterns(self, description: str) -> List[str]:
        """Identify design patterns mentioned or applicable"""
        patterns = []
        description_lower = description.lower()

        pattern_keywords = {
            'Strategy': ['strategy', 'algorithm', 'behavior'],
            'Factory': ['factory', 'create', 'instantiate'],
            'Observer': ['observer', 'pub/sub', 'event', 'notify'],
            'Singleton': ['singleton', 'single instance', 'global'],
            'Repository': ['repository', 'data access', 'persistence'],
            'Adapter': ['adapter', 'wrapper', 'interface'],
            'Decorator': ['decorator', 'enhance', 'extend'],
            'Command': ['command', 'action', 'execute'],
        }

        for pattern, keywords in pattern_keywords.items():
            if any(kw in description_lower for kw in keywords):
                patterns.append(pattern)

        return patterns or ['Custom']

    def _estimate_impact(self, description: str) -> DecisionImpact:
        """Estimate impact of architectural decision"""
        description_lower = description.lower()

        if any(kw in description_lower for kw in ['breaking', 'migration', 'rewrite', 'core']):
            return DecisionImpact.CRITICAL
        elif any(kw in description_lower for kw in ['multiple', 'system-wide', 'architecture']):
            return DecisionImpact.HIGH
        elif any(kw in description_lower for kw in ['component', 'module', 'service']):
            return DecisionImpact.MEDIUM
        else:
            return DecisionImpact.LOW

    def _red_team_criticism(self, option: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        PHASE 4: Red Team - Adversarial criticism

        Apply P3 (Ceticismo Crítico) - question assumptions
        """
        criticisms = []

        # Complexity criticism
        if option.get('complexity') == 'HIGH':
            criticisms.append({
                "concern": "complexity",
                "question": "HIGH complexity may hinder maintainability and onboarding. Is the added complexity justified?",
                "risk_level": "HIGH"
            })

        # Pattern overuse
        if len(option.get('patterns', [])) > 3:
            criticisms.append({
                "concern": "over_engineering",
                "question": "Overuse of patterns may lead to over-engineering. Are all patterns necessary?",
                "risk_level": "MEDIUM"
            })

        # Impact criticism
        if option.get('impact') == DecisionImpact.CRITICAL:
            criticisms.append({
                "concern": "migration",
                "question": "CRITICAL impact requires careful migration planning. Do we have a rollback strategy?",
                "risk_level": "CRITICAL"
            })

        # Cons outweigh pros
        if len(option.get('cons', [])) > len(option.get('pros', [])):
            criticisms.append({
                "concern": "trade_offs",
                "question": "Cons outweigh pros - are the trade-offs worthwhile?",
                "risk_level": "HIGH"
            })

        # Add generic architectural concerns
        criticisms.extend([
            {
                "concern": "scalability",
                "question": "Consider scalability bottlenecks. How will this scale to 10x load?",
                "risk_level": "MEDIUM"
            },
            {
                "concern": "testability",
                "question": "Evaluate testability impact. Can this be easily tested?",
                "risk_level": "LOW"
            },
            {
                "concern": "technical_debt",
                "question": "Assess technical debt introduced. What is the maintenance burden?",
                "risk_level": "MEDIUM"
            },
        ])

        return criticisms

    def _fuse_architectural_decisions(
        self,
        options: List[Dict[str, Any]],
        systemic_analyses: List[Any],
    ) -> Dict[str, Any]:
        """
        PHASE 5: Fusion - Combine Max-Code + MAXIMUS insights

        Equal weighting (0.5/0.5) for architectural decisions
        """
        scored_options = []

        for option, analysis in zip(options, systemic_analyses):
            # Max-Code score (based on ToT)
            maxcode_score = self._calculate_tot_score(option)

            # MAXIMUS score (inverted systemic risk)
            maximus_score = 1.0 - analysis.systemic_risk_score

            # Fusion (50/50 weight for architecture)
            combined_score = 0.5 * maxcode_score + 0.5 * maximus_score

            scored_options.append({
                **option,
                'maxcode_score': maxcode_score,
                'maximus_score': maximus_score,
                'confidence': combined_score,
                'systemic_analysis': analysis,
            })

        # Select best
        best = max(scored_options, key=lambda x: x['confidence'])

        # Generate rationale
        best['rationale'] = (
            f"{best['approach']}. "
            f"This approach achieves the best balance between "
            f"implementation feasibility (Max-Code: {best['maxcode_score']:.2f}) "
            f"and systemic robustness (MAXIMUS: {best['maximus_score']:.2f}). "
            f"Systemic risk is {best['systemic_analysis'].systemic_risk_score:.2f} (LOW)."
        )

        return best

    def _select_best_option_standalone(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """PHASE 5: Select best option (standalone Max-Code)"""
        # Score options by ToT
        for option in options:
            option['confidence'] = self._calculate_tot_score(option)

        best = max(options, key=lambda x: x['confidence'])

        best['rationale'] = (
            f"{best['approach']}. "
            f"This approach has the best combination of pros/cons and manageable complexity."
        )
        best['all_options'] = options  # Store all options for ADR

        return best

    def _calculate_tot_score(self, option: Dict[str, Any]) -> float:
        """Calculate Tree of Thoughts score"""
        pros_score = len(option['pros']) * 0.15
        cons_score = len(option['cons']) * -0.10

        complexity_map = {'LOW': 1.0, 'MEDIUM': 0.7, 'HIGH': 0.4}
        complexity_score = complexity_map.get(option['complexity'], 0.5)

        # Penalize critical impact
        impact_penalty = 0.2 if option['impact'] == DecisionImpact.CRITICAL else 0.0

        total = max(0.0, min(1.0, 0.5 + pros_score + cons_score + complexity_score * 0.3 - impact_penalty))
        return total

    def _create_architectural_decision_record(
        self,
        best_decision: Dict[str, Any],
        task: AgentTask
    ) -> ArchitecturalDecision:
        """
        PHASE 6: Document - Create ADR (Architectural Decision Record)

        Follows P4 (Rastreabilidade Total)
        """
        import time

        adr_id = f"ADR-{int(time.time())}"

        # Extract risks from systemic analysis
        risks = []
        if 'systemic_analysis' in best_decision:
            analysis = best_decision['systemic_analysis']
            for side_effect in analysis.side_effects[:3]:  # Top 3
                risks.append(ArchitecturalRisk(
                    concern=ArchitecturalConcern.RELIABILITY,
                    severity="MEDIUM",
                    description=side_effect,
                    mitigation=analysis.mitigation_strategies[0] if analysis.mitigation_strategies else "Monitor closely",
                    probability=analysis.systemic_risk_score,
                ))

        # Add criticism-based risks
        for criticism in best_decision.get('criticisms', [])[:2]:
            risks.append(ArchitecturalRisk(
                concern=ArchitecturalConcern.MAINTAINABILITY,
                severity="LOW",
                description=criticism,
                mitigation="Address during implementation",
                probability=0.3,
            ))

        return ArchitecturalDecision(
            id=adr_id,
            decision=best_decision['approach'],
            rationale=best_decision['rationale'],
            alternatives_considered=[opt['approach'] for opt in best_decision.get('all_options', [])],
            trade_offs={
                "pros": ", ".join(best_decision['pros']),
                "cons": ", ".join(best_decision['cons']),
                "complexity": best_decision['complexity'],
            },
            impact=best_decision['impact'],
            risks=risks,
            confidence=best_decision['confidence'],
        )

    # ========================================================================
    # KNOWLEDGE BASE
    # ========================================================================

    def _load_design_patterns(self) -> Dict[str, DesignPattern]:
        """Load design patterns knowledge base"""
        return {
            'Strategy': DesignPattern(
                name='Strategy',
                category='Behavioral',
                use_case='Algorithm/behavior selection at runtime',
                pros=['Flexibility', 'Open/Closed Principle', 'Testability'],
                cons=['Increased classes', 'Client awareness'],
                complexity='LOW',
            ),
            # Add more patterns as needed
        }

    def _load_architectural_principles(self) -> List[str]:
        """Load architectural principles"""
        return [
            "SOLID principles",
            "DRY (Don't Repeat Yourself)",
            "KISS (Keep It Simple, Stupid)",
            "YAGNI (You Aren't Gonna Need It)",
            "Separation of Concerns",
            "Principle of Least Surprise",
        ]

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _get_design_pattern_info(self, pattern_name: str) -> Optional[DesignPattern]:
        """Get information about a design pattern"""
        pattern_map = {
            'microservices': DesignPattern(
                name='Microservices',
                category='Architectural',
                use_case='Distributed systems with independent services',
                pros=['Scalability', 'Independent deployment', 'Technology diversity'],
                cons=['Complexity', 'Distributed transactions', 'Network overhead'],
                complexity='HIGH',
            ),
            'event-driven': DesignPattern(
                name='Event-Driven',
                category='Architectural',
                use_case='Asynchronous communication between components',
                pros=['Loose coupling', 'Scalability', 'Real-time processing'],
                cons=['Eventual consistency', 'Debugging difficulty', 'Message ordering'],
                complexity='MEDIUM',
            ),
            'layered': DesignPattern(
                name='Layered Architecture',
                category='Architectural',
                use_case='Traditional n-tier applications',
                pros=['Separation of concerns', 'Testability', 'Maintainability'],
                cons=['Performance overhead', 'Tight coupling between layers'],
                complexity='LOW',
            ),
            'cqrs': DesignPattern(
                name='CQRS',
                category='Architectural',
                use_case='Separate read and write models',
                pros=['Performance optimization', 'Scalability', 'Clear separation'],
                cons=['Complexity', 'Eventual consistency', 'Code duplication'],
                complexity='HIGH',
            ),
        }
        return pattern_map.get(pattern_name.lower())

    def get_decision_history(self) -> List[ArchitecturalDecision]:
        """Get history of architectural decisions"""
        return self.decision_history

    def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        """Query architectural knowledge base"""
        # Simplified - in production, use vector search
        return {
            'patterns': self.knowledge_base['patterns'],
            'principles': self.knowledge_base['principles'],
        }

    async def close(self):
        """Close MAXIMUS client"""
        if self.maximus_client:
            await self.maximus_client.close()
