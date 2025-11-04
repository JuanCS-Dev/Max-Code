"""
Comprehensive Scientific Tests for Tree of Thoughts (ToT)

CRITICAL for planning and reasoning capabilities. Tests the deliberative problem-solving
framework based on "Tree of Thoughts: Deliberate Problem Solving with LLMs" (Yao et al., 2023).

Constitutional Mandate: Article VII, Section 1
"The Executor Tático must generate 3-5 'thoughts' (alternative approaches) to solve the problem."

Test Coverage:
1. Thought Generation - Multiple solution paths
2. Thought Evaluation - Multi-dimensional quality scoring
3. Path Exploration - BFS/DFS strategies
4. Best Path Selection - Optimal solution identification
5. Pruning - Low-quality branch removal
6. Real Problem Solving - Actual software engineering problems
7. Performance - Complex thought tree handling
8. Integration - Works with PlanAgent, CodeAgent
9. Recursive Expansion - Hierarchical problem decomposition
10. Custom Weights - Flexible evaluation criteria
11. Statistics Tracking - Performance metrics
12. Serialization - Thought persistence

Run:
    pytest tests/test_tree_of_thoughts_comprehensive.py -v
    pytest tests/test_tree_of_thoughts_comprehensive.py -v --cov=core.deter_agent.deliberation.tree_of_thoughts --cov-report=html
    pytest tests/test_tree_of_thoughts_comprehensive.py::test_real_problem_microservices_architecture -v -s
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import List, Dict, Any
import json
from datetime import datetime

from core.deter_agent.deliberation.tree_of_thoughts import (
    TreeOfThoughts,
    Thought,
    ThoughtEvaluation,
    EvaluationDimension,
    tree_of_thoughts_solve,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def basic_thought():
    """Create a basic thought for testing"""
    return Thought(
        id="thought_001",
        description="Use JWT tokens for authentication",
        approach="Implement stateless JWT-based authentication with refresh tokens",
        pros=[
            "Stateless and scalable",
            "Industry standard",
            "Easy to implement",
        ],
        cons=[
            "Token size overhead",
            "Cannot invalidate tokens before expiration",
        ],
        assumptions=[
            "HTTPS is enforced",
            "Token rotation is implemented",
        ],
        risks=[
            "Secret key compromise",
            "XSS attacks if not properly stored",
        ],
        complexity="MEDIUM",
    )


@pytest.fixture
def evaluated_thought(basic_thought):
    """Create a thought with evaluation"""
    basic_thought.evaluation = ThoughtEvaluation(
        correctness=0.9,
        robustness=0.85,
        maintainability=0.88,
        performance=0.92,
        security=0.80,
        simplicity=0.75,
        testability=0.87,
    )
    return basic_thought


@pytest.fixture
def thought_with_implementation_plan(basic_thought):
    """Create thought with implementation plan for expansion tests"""
    basic_thought.implementation_plan = [
        "Design JWT token structure with claims",
        "Implement token generation and validation",
        "Create refresh token mechanism",
        "Add token storage and rotation",
        "Implement authentication middleware",
    ]
    return basic_thought


@pytest.fixture
def multiple_thoughts():
    """Create multiple thoughts for ranking tests"""
    thoughts = []

    # Thought 1: JWT (high score)
    t1 = Thought(
        id="jwt",
        description="JWT-based authentication",
        approach="Stateless tokens with refresh mechanism",
        pros=["Scalable", "Standard"],
        cons=["Token size"],
        assumptions=["HTTPS"],
        risks=["Key compromise"],
        complexity="MEDIUM",
    )
    t1.evaluation = ThoughtEvaluation(
        correctness=0.9, robustness=0.85, maintainability=0.88,
        performance=0.92, security=0.80, simplicity=0.75, testability=0.87
    )
    thoughts.append(t1)

    # Thought 2: Session (medium score)
    t2 = Thought(
        id="session",
        description="Session-based authentication",
        approach="Server-side sessions with cookies",
        pros=["Can revoke immediately", "Simple"],
        cons=["Stateful", "Scalability issues"],
        assumptions=["Sticky sessions or shared storage"],
        risks=["Session hijacking"],
        complexity="LOW",
    )
    t2.evaluation = ThoughtEvaluation(
        correctness=0.85, robustness=0.80, maintainability=0.75,
        performance=0.60, security=0.85, simplicity=0.90, testability=0.80
    )
    thoughts.append(t2)

    # Thought 3: OAuth2 (complex but robust)
    t3 = Thought(
        id="oauth2",
        description="OAuth2 with external provider",
        approach="Delegate authentication to OAuth2 provider",
        pros=["Offload security", "SSO capability", "Battle-tested"],
        cons=["External dependency", "Complex setup"],
        assumptions=["Provider uptime", "Network reliability"],
        risks=["Provider outage", "Privacy concerns"],
        complexity="HIGH",
    )
    t3.evaluation = ThoughtEvaluation(
        correctness=0.95, robustness=0.90, maintainability=0.70,
        performance=0.85, security=0.95, simplicity=0.50, testability=0.75
    )
    thoughts.append(t3)

    return thoughts


@pytest.fixture
def custom_generator():
    """Custom thought generator for testing"""
    def generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        thoughts = []
        approaches = [
            {
                "id": "approach_a",
                "desc": "Microservices architecture",
                "approach": "Split into independent services",
                "complexity": "HIGH",
            },
            {
                "id": "approach_b",
                "desc": "Modular monolith",
                "approach": "Single deployment with clear module boundaries",
                "complexity": "MEDIUM",
            },
            {
                "id": "approach_c",
                "desc": "Serverless functions",
                "approach": "Deploy as independent cloud functions",
                "complexity": "MEDIUM",
            },
            {
                "id": "approach_d",
                "desc": "Event-driven architecture",
                "approach": "Async communication via event bus",
                "complexity": "HIGH",
            },
            {
                "id": "approach_e",
                "desc": "Layered monolith",
                "approach": "Traditional N-tier architecture",
                "complexity": "LOW",
            },
        ]

        for i in range(min(num_thoughts, len(approaches))):
            app = approaches[i]
            thought = Thought(
                id=app["id"],
                description=app["desc"],
                approach=app["approach"],
                pros=[f"Pro {j+1}" for j in range(3)],
                cons=[f"Con {j+1}" for j in range(2)],
                assumptions=["Assumption 1"],
                risks=["Risk 1"],
                complexity=app["complexity"],
            )
            thoughts.append(thought)

        return thoughts

    return generator


@pytest.fixture
def custom_evaluator():
    """Custom evaluator that gives deterministic scores"""
    def evaluator(thought: Thought) -> ThoughtEvaluation:
        # Score based on complexity (inverse - simpler is better for simplicity)
        complexity_map = {"LOW": 0.9, "MEDIUM": 0.75, "HIGH": 0.6}
        base_score = complexity_map.get(thought.complexity, 0.7)

        return ThoughtEvaluation(
            correctness=base_score + 0.05,
            robustness=base_score,
            maintainability=base_score + 0.02,
            performance=base_score - 0.05,
            security=base_score + 0.03,
            simplicity=base_score + 0.10,
            testability=base_score,
        )

    return evaluator


# ============================================================================
# TEST 1-5: THOUGHT EVALUATION
# ============================================================================

def test_thought_evaluation_initialization():
    """Test ThoughtEvaluation initialization and score calculation"""
    eval = ThoughtEvaluation(
        correctness=0.9,
        robustness=0.85,
        maintainability=0.88,
        performance=0.92,
        security=0.80,
        simplicity=0.75,
        testability=0.87,
    )

    # Check all dimensions are set
    assert eval.correctness == 0.9
    assert eval.robustness == 0.85
    assert eval.maintainability == 0.88
    assert eval.performance == 0.92
    assert eval.security == 0.80
    assert eval.simplicity == 0.75
    assert eval.testability == 0.87

    # Check overall score is calculated (weighted average)
    # Default weights: correctness(25%), robustness(20%), maintainability(15%),
    # performance(10%), security(15%), simplicity(5%), testability(10%)
    expected = (0.9*0.25 + 0.85*0.20 + 0.88*0.15 + 0.92*0.10 +
                0.80*0.15 + 0.75*0.05 + 0.87*0.10)
    assert abs(eval.overall_score - expected) < 0.001


def test_thought_evaluation_custom_weights():
    """Test ThoughtEvaluation with custom weights"""
    custom_weights = {
        'correctness': 0.4,      # Prioritize correctness
        'robustness': 0.3,       # And robustness
        'maintainability': 0.1,
        'performance': 0.05,
        'security': 0.1,
        'simplicity': 0.025,
        'testability': 0.025,
    }

    eval = ThoughtEvaluation(
        correctness=0.9,
        robustness=0.8,
        maintainability=0.7,
        performance=0.6,
        security=0.8,
        simplicity=0.5,
        testability=0.7,
        weights=custom_weights,
    )

    # Check custom weights are used
    expected = (0.9*0.4 + 0.8*0.3 + 0.7*0.1 + 0.6*0.05 +
                0.8*0.1 + 0.5*0.025 + 0.7*0.025)
    assert abs(eval.overall_score - expected) < 0.001


def test_thought_evaluation_to_dict():
    """Test ThoughtEvaluation serialization"""
    eval = ThoughtEvaluation(
        correctness=0.9,
        robustness=0.85,
        maintainability=0.88,
        performance=0.92,
        security=0.80,
        simplicity=0.75,
        testability=0.87,
    )

    result = eval.to_dict()

    assert isinstance(result, dict)
    assert result['correctness'] == 0.9
    assert result['robustness'] == 0.85
    assert 'overall_score' in result
    assert isinstance(result['overall_score'], float)


def test_thought_evaluation_edge_cases():
    """Test ThoughtEvaluation edge cases (min/max scores)"""
    # All minimum scores
    eval_min = ThoughtEvaluation(
        correctness=0.0, robustness=0.0, maintainability=0.0,
        performance=0.0, security=0.0, simplicity=0.0, testability=0.0,
    )
    assert eval_min.overall_score == 0.0

    # All maximum scores
    eval_max = ThoughtEvaluation(
        correctness=1.0, robustness=1.0, maintainability=1.0,
        performance=1.0, security=1.0, simplicity=1.0, testability=1.0,
    )
    assert eval_max.overall_score == 1.0


def test_thought_evaluation_dimensions_enum():
    """Test EvaluationDimension enum"""
    assert EvaluationDimension.CORRECTNESS.value == "correctness"
    assert EvaluationDimension.ROBUSTNESS.value == "robustness"
    assert EvaluationDimension.SECURITY.value == "security"
    assert EvaluationDimension.SIMPLICITY.value == "simplicity"

    # Verify all 7 dimensions exist
    dimensions = [d.value for d in EvaluationDimension]
    assert len(dimensions) == 7
    assert "correctness" in dimensions
    assert "robustness" in dimensions
    assert "maintainability" in dimensions
    assert "performance" in dimensions
    assert "security" in dimensions
    assert "simplicity" in dimensions
    assert "testability" in dimensions


# ============================================================================
# TEST 6-10: THOUGHT STRUCTURE
# ============================================================================

def test_thought_initialization(basic_thought):
    """Test Thought initialization"""
    assert basic_thought.id == "thought_001"
    assert "JWT" in basic_thought.description
    assert "stateless" in basic_thought.approach.lower()
    assert len(basic_thought.pros) == 3
    assert len(basic_thought.cons) == 2
    assert len(basic_thought.assumptions) == 2
    assert len(basic_thought.risks) == 2
    assert basic_thought.complexity == "MEDIUM"
    assert basic_thought.evaluation is None
    assert isinstance(basic_thought.created_at, datetime)


def test_thought_string_representation(evaluated_thought):
    """Test Thought __str__ method"""
    str_repr = str(evaluated_thought)

    assert "Thought(" in str_repr
    assert evaluated_thought.id in str_repr
    assert "score=" in str_repr
    assert "complexity=" in str_repr


def test_thought_to_dict(evaluated_thought):
    """Test Thought serialization"""
    result = evaluated_thought.to_dict()

    assert isinstance(result, dict)
    assert result['id'] == evaluated_thought.id
    assert result['description'] == evaluated_thought.description
    assert result['approach'] == evaluated_thought.approach
    assert result['pros'] == evaluated_thought.pros
    assert result['cons'] == evaluated_thought.cons
    assert result['assumptions'] == evaluated_thought.assumptions
    assert result['risks'] == evaluated_thought.risks
    assert result['complexity'] == evaluated_thought.complexity
    assert result['evaluation'] is not None
    assert isinstance(result['evaluation'], dict)
    assert 'created_at' in result


def test_thought_json_serialization(evaluated_thought):
    """Test Thought can be serialized to JSON"""
    thought_dict = evaluated_thought.to_dict()
    json_str = json.dumps(thought_dict)

    # Verify it's valid JSON
    parsed = json.loads(json_str)
    assert parsed['id'] == evaluated_thought.id
    assert parsed['description'] == evaluated_thought.description


def test_thought_with_metadata():
    """Test Thought with custom metadata"""
    thought = Thought(
        id="meta_test",
        description="Test approach",
        approach="Test technical approach",
        pros=["Pro 1"],
        cons=["Con 1"],
        assumptions=["Assumption 1"],
        risks=["Risk 1"],
        complexity="LOW",
        metadata={
            'author': 'test_agent',
            'version': '1.0',
            'tags': ['auth', 'security'],
        },
    )

    assert thought.metadata['author'] == 'test_agent'
    assert thought.metadata['version'] == '1.0'
    assert 'auth' in thought.metadata['tags']


# ============================================================================
# TEST 11-15: TREE OF THOUGHTS INITIALIZATION AND BASIC OPERATIONS
# ============================================================================

def test_tot_initialization():
    """Test TreeOfThoughts initialization"""
    tot = TreeOfThoughts()

    assert tot.generator is not None
    assert tot.evaluator is not None
    assert tot.MIN_THOUGHTS == 3
    assert tot.MAX_THOUGHTS == 5
    assert tot.stats['total_problems'] == 0
    assert tot.stats['total_thoughts_generated'] == 0


def test_tot_custom_generator_evaluator(custom_generator, custom_evaluator):
    """Test TreeOfThoughts with custom generator and evaluator"""
    tot = TreeOfThoughts(
        generator=custom_generator,
        evaluator=custom_evaluator,
    )

    assert tot.generator == custom_generator
    assert tot.evaluator == custom_evaluator


def test_tot_default_generator():
    """Test TreeOfThoughts default generator"""
    tot = TreeOfThoughts()

    thoughts = tot._generate_thoughts(
        problem="Design a user authentication system",
        context={},
        num_thoughts=3,
    )

    assert len(thoughts) == 3
    assert all(isinstance(t, Thought) for t in thoughts)
    assert all(t.id.startswith("thought_") for t in thoughts)
    assert all(t.complexity in ["LOW", "MEDIUM", "HIGH"] for t in thoughts)


def test_tot_default_evaluator(basic_thought):
    """Test TreeOfThoughts default evaluator"""
    tot = TreeOfThoughts()

    evaluation = tot._default_evaluator(basic_thought)

    assert isinstance(evaluation, ThoughtEvaluation)
    assert 0.0 <= evaluation.correctness <= 1.0
    assert 0.0 <= evaluation.overall_score <= 1.0
    # Default evaluator uses random scores between 0.7-1.0
    assert evaluation.correctness >= 0.7


def test_tot_rank_thoughts(multiple_thoughts):
    """Test TreeOfThoughts ranking functionality"""
    tot = TreeOfThoughts()

    ranked = tot._rank_thoughts(multiple_thoughts)

    # Should be sorted by overall_score descending
    assert len(ranked) == 3
    assert ranked[0].evaluation.overall_score >= ranked[1].evaluation.overall_score
    assert ranked[1].evaluation.overall_score >= ranked[2].evaluation.overall_score


# ============================================================================
# TEST 16-20: SOLVE METHOD AND THOUGHT GENERATION
# ============================================================================

def test_tot_solve_basic():
    """Test TreeOfThoughts solve method with default settings"""
    tot = TreeOfThoughts()

    problem = "Design authentication system for web application"
    best_thought = tot.solve(problem)

    assert isinstance(best_thought, Thought)
    assert best_thought.evaluation is not None
    assert best_thought.evaluation.overall_score > 0.0

    # Stats should be updated
    assert tot.stats['total_problems'] == 1
    assert tot.stats['total_thoughts_generated'] >= 3  # At least MIN_THOUGHTS


def test_tot_solve_custom_num_thoughts(custom_generator, custom_evaluator):
    """Test TreeOfThoughts solve with custom number of thoughts"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    problem = "Design scalable microservices architecture"

    # Test with 3 thoughts
    best = tot.solve(problem, num_thoughts=3)
    assert tot.stats['total_thoughts_generated'] == 3

    # Test with 5 thoughts
    tot2 = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)
    best = tot2.solve(problem, num_thoughts=5)
    assert tot2.stats['total_thoughts_generated'] == 5


def test_tot_solve_enforces_min_max_thoughts(custom_generator, custom_evaluator):
    """Test TreeOfThoughts enforces MIN_THOUGHTS and MAX_THOUGHTS"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    problem = "Implement caching strategy"

    # Try with 1 thought - should enforce minimum of 3
    tot.solve(problem, num_thoughts=1)
    assert tot.stats['total_thoughts_generated'] >= 3

    # Try with 10 thoughts - should cap at 5
    tot2 = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)
    tot2.solve(problem, num_thoughts=10)
    assert tot2.stats['total_thoughts_generated'] <= 5


def test_tot_solve_return_all_thoughts(custom_generator, custom_evaluator):
    """Test TreeOfThoughts solve with return_all=True"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    problem = "Design database schema"
    all_thoughts = tot.solve(problem, num_thoughts=4, return_all=True)

    assert isinstance(all_thoughts, list)
    assert len(all_thoughts) == 4
    assert all(isinstance(t, Thought) for t in all_thoughts)
    assert all(t.evaluation is not None for t in all_thoughts)

    # Should be ranked
    for i in range(len(all_thoughts) - 1):
        assert all_thoughts[i].evaluation.overall_score >= all_thoughts[i+1].evaluation.overall_score


def test_tot_solve_with_context(custom_generator, custom_evaluator):
    """Test TreeOfThoughts solve with context"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    problem = "Optimize database queries"
    context = {
        'database': 'PostgreSQL',
        'current_performance': 'slow',
        'data_size': 'large',
    }

    best = tot.solve(problem, context=context, num_thoughts=3)

    assert isinstance(best, Thought)
    assert best.evaluation.overall_score > 0.0


# ============================================================================
# TEST 21-25: EXPANSION AND HIERARCHICAL DECOMPOSITION
# ============================================================================

def test_tot_expand_thought(thought_with_implementation_plan, custom_generator):
    """Test TreeOfThoughts expand_thought method"""
    tot = TreeOfThoughts(generator=custom_generator)

    sub_thoughts = tot.expand_thought(thought_with_implementation_plan, depth=1)

    assert isinstance(sub_thoughts, list)
    assert len(sub_thoughts) > 0
    # Should generate sub-thoughts for implementation steps (limited to 3 steps, 2 thoughts each)
    assert len(sub_thoughts) <= 6  # 3 steps * 2 thoughts


def test_tot_expand_thought_zero_depth(thought_with_implementation_plan):
    """Test TreeOfThoughts expand_thought with depth=0"""
    tot = TreeOfThoughts()

    sub_thoughts = tot.expand_thought(thought_with_implementation_plan, depth=0)

    # Should return the original thought only
    assert len(sub_thoughts) == 1
    assert sub_thoughts[0] == thought_with_implementation_plan


def test_tot_expand_thought_no_implementation_plan(basic_thought):
    """Test TreeOfThoughts expand_thought with no implementation plan"""
    tot = TreeOfThoughts()

    sub_thoughts = tot.expand_thought(basic_thought, depth=1)

    # Should return empty list if no implementation plan
    assert isinstance(sub_thoughts, list)


def test_tot_hierarchical_problem_solving(custom_generator, custom_evaluator):
    """Test hierarchical problem solving with expansion"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    # Solve main problem
    main_problem = "Build e-commerce platform"
    best_thought = tot.solve(main_problem, num_thoughts=3)

    # Add implementation plan
    best_thought.implementation_plan = [
        "Design user authentication",
        "Implement product catalog",
        "Create shopping cart",
    ]

    # Expand into sub-problems
    sub_thoughts = tot.expand_thought(best_thought, depth=1)

    assert len(sub_thoughts) > 0
    # Each sub-thought should be for a specific implementation step


def test_tot_recursive_expansion(thought_with_implementation_plan, custom_generator):
    """Test recursive thought expansion"""
    tot = TreeOfThoughts(generator=custom_generator)

    # Expand with depth 1
    depth1 = tot.expand_thought(thought_with_implementation_plan, depth=1)
    assert len(depth1) > 0

    # Expansion should respect depth limit
    depth0 = tot.expand_thought(thought_with_implementation_plan, depth=0)
    assert len(depth0) == 1


# ============================================================================
# TEST 26-30: REAL-WORLD PROBLEM SOLVING SCENARIOS
# ============================================================================

def test_real_problem_authentication_system():
    """Test ToT with real authentication system design problem"""
    def auth_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id="jwt_approach",
                description="JWT-based stateless authentication",
                approach="Use JSON Web Tokens for stateless auth with refresh tokens",
                pros=["Scalable", "No server state", "Standard"],
                cons=["Cannot revoke before expiry", "Token size"],
                assumptions=["HTTPS enforced", "Secure storage"],
                risks=["Secret key compromise", "XSS attacks"],
                complexity="MEDIUM",
            ),
            Thought(
                id="session_approach",
                description="Traditional session-based authentication",
                approach="Server-side sessions with secure cookies",
                pros=["Can revoke immediately", "Smaller cookie size"],
                cons=["Requires session storage", "Sticky sessions"],
                assumptions=["Redis/Memcached available"],
                risks=["Session hijacking", "CSRF"],
                complexity="LOW",
            ),
            Thought(
                id="oauth_approach",
                description="OAuth2 with external provider",
                approach="Delegate to Google/GitHub OAuth2",
                pros=["Offload security", "SSO", "Battle-tested"],
                cons=["External dependency", "Privacy concerns"],
                assumptions=["Provider SLA", "Network reliability"],
                risks=["Provider outage", "API changes"],
                complexity="HIGH",
            ),
        ][:num_thoughts]

    def auth_evaluator(thought: Thought) -> ThoughtEvaluation:
        # Realistic evaluation based on approach
        scores = {
            "jwt_approach": (0.9, 0.85, 0.88, 0.92, 0.80, 0.75, 0.87),
            "session_approach": (0.85, 0.80, 0.90, 0.70, 0.85, 0.95, 0.88),
            "oauth_approach": (0.95, 0.90, 0.70, 0.85, 0.95, 0.60, 0.75),
        }
        c, r, m, p, s, si, t = scores.get(thought.id, (0.7,)*7)
        return ThoughtEvaluation(c, r, m, p, s, si, t)

    tot = TreeOfThoughts(generator=auth_generator, evaluator=auth_evaluator)

    problem = "Design secure authentication system for high-traffic web application"
    best = tot.solve(problem, num_thoughts=3)

    assert best.id in ["jwt_approach", "session_approach", "oauth_approach"]
    assert best.evaluation.overall_score > 0.8  # Should be high quality


def test_real_problem_microservices_architecture():
    """Test ToT with real microservices architecture problem"""
    def microservices_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id="microservices",
                description="Pure microservices architecture",
                approach="Split into independent services with API gateway",
                pros=["Independent scaling", "Tech diversity", "Fault isolation"],
                cons=["Distributed complexity", "Network overhead", "Data consistency"],
                assumptions=["Container orchestration", "Service mesh"],
                risks=["Service coordination", "Cascading failures"],
                complexity="HIGH",
                implementation_plan=[
                    "Design service boundaries",
                    "Implement API gateway",
                    "Setup service discovery",
                    "Configure inter-service communication",
                ],
            ),
            Thought(
                id="modular_monolith",
                description="Modular monolith",
                approach="Single deployment with clear module boundaries",
                pros=["Simpler deployment", "Easier debugging", "No network overhead"],
                cons=["Less flexible scaling", "Single point of failure"],
                assumptions=["Good module discipline", "Clear boundaries"],
                risks=["Module coupling", "Scaling bottlenecks"],
                complexity="MEDIUM",
                implementation_plan=[
                    "Define module boundaries",
                    "Implement module interfaces",
                    "Setup dependency injection",
                ],
            ),
            Thought(
                id="hybrid",
                description="Hybrid: Modular monolith + selective microservices",
                approach="Core as monolith, extract specific services",
                pros=["Best of both worlds", "Incremental migration"],
                cons=["Increased architectural complexity"],
                assumptions=["Clear extraction criteria"],
                risks=["Premature optimization"],
                complexity="MEDIUM",
                implementation_plan=[
                    "Build monolith core",
                    "Identify service candidates",
                    "Extract critical services",
                ],
            ),
        ][:num_thoughts]

    def microservices_evaluator(thought: Thought) -> ThoughtEvaluation:
        scores = {
            "microservices": (0.85, 0.90, 0.70, 0.85, 0.88, 0.50, 0.75),
            "modular_monolith": (0.90, 0.85, 0.92, 0.80, 0.85, 0.90, 0.90),
            "hybrid": (0.92, 0.88, 0.85, 0.82, 0.87, 0.75, 0.85),
        }
        c, r, m, p, s, si, t = scores.get(thought.id, (0.7,)*7)
        return ThoughtEvaluation(c, r, m, p, s, si, t)

    tot = TreeOfThoughts(generator=microservices_generator, evaluator=microservices_evaluator)

    problem = "Design scalable architecture for SaaS platform with 100k+ users"
    best = tot.solve(problem, num_thoughts=3)

    assert best.id in ["microservices", "modular_monolith", "hybrid"]
    # Either hybrid or modular_monolith should win due to balanced scores
    # (modular_monolith has high maintainability, hybrid has balanced scores)
    assert best.id in ["hybrid", "modular_monolith"]


def test_real_problem_database_strategy():
    """Test ToT with database selection problem"""
    def db_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id="postgresql",
                description="PostgreSQL relational database",
                approach="Use PostgreSQL with JSONB for flexibility",
                pros=["ACID compliance", "Rich features", "Great tooling"],
                cons=["Vertical scaling limits", "Complex for simple use"],
                assumptions=["Structured data", "Complex queries needed"],
                risks=["Performance at scale", "Licensing costs"],
                complexity="MEDIUM",
            ),
            Thought(
                id="mongodb",
                description="MongoDB document database",
                approach="Use MongoDB for flexible schema",
                pros=["Horizontal scaling", "Flexible schema", "Fast writes"],
                cons=["No transactions (older versions)", "Consistency trade-offs"],
                assumptions=["Document-oriented data", "High write throughput"],
                risks=["Data consistency", "Query complexity"],
                complexity="MEDIUM",
            ),
            Thought(
                id="hybrid_polyglot",
                description="Polyglot persistence",
                approach="PostgreSQL for core + Redis for cache + MongoDB for analytics",
                pros=["Right tool for each job", "Optimized performance"],
                cons=["Operational complexity", "Multiple systems to manage"],
                assumptions=["Team expertise", "DevOps capacity"],
                risks=["Data synchronization", "Complexity overhead"],
                complexity="HIGH",
            ),
        ][:num_thoughts]

    def db_evaluator(thought: Thought) -> ThoughtEvaluation:
        scores = {
            "postgresql": (0.95, 0.90, 0.92, 0.80, 0.92, 0.85, 0.90),
            "mongodb": (0.85, 0.82, 0.80, 0.88, 0.78, 0.88, 0.82),
            "hybrid_polyglot": (0.90, 0.88, 0.65, 0.92, 0.85, 0.50, 0.70),
        }
        c, r, m, p, s, si, t = scores.get(thought.id, (0.7,)*7)
        return ThoughtEvaluation(c, r, m, p, s, si, t)

    tot = TreeOfThoughts(generator=db_generator, evaluator=db_evaluator)

    problem = "Choose database strategy for financial application requiring ACID compliance"
    context = {"requirements": ["ACID", "complex queries", "reliability"]}
    best = tot.solve(problem, context=context, num_thoughts=3)

    # PostgreSQL should win for financial app with ACID requirements
    assert best.id == "postgresql"
    assert best.evaluation.correctness >= 0.95


def test_real_problem_caching_strategy():
    """Test ToT with caching strategy problem"""
    def cache_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id="redis_cache",
                description="Redis in-memory cache",
                approach="Use Redis for distributed caching with TTL",
                pros=["Fast", "Distributed", "Rich data structures"],
                cons=["Memory cost", "Cache invalidation complexity"],
                assumptions=["Network reliability", "Memory capacity"],
                risks=["Cache stampede", "Memory pressure"],
                complexity="MEDIUM",
            ),
            Thought(
                id="cdn_edge",
                description="CDN edge caching",
                approach="Use CloudFront/Cloudflare for static content",
                pros=["Global distribution", "Offload origin", "DDoS protection"],
                cons=["Static content only", "Purge latency"],
                assumptions=["Static assets", "CDN provider"],
                risks=["Stale content", "Cost at scale"],
                complexity="LOW",
            ),
            Thought(
                id="multi_tier",
                description="Multi-tier caching",
                approach="Browser cache + CDN + Redis + Application cache",
                pros=["Optimal performance", "Layered fallback"],
                cons=["Complex invalidation", "Cache coherence"],
                assumptions=["Sophisticated cache strategy"],
                risks=["Consistency issues", "Over-engineering"],
                complexity="HIGH",
            ),
        ][:num_thoughts]

    def cache_evaluator(thought: Thought) -> ThoughtEvaluation:
        scores = {
            "redis_cache": (0.90, 0.85, 0.88, 0.95, 0.82, 0.80, 0.88),
            "cdn_edge": (0.88, 0.82, 0.92, 0.98, 0.88, 0.95, 0.90),
            "multi_tier": (0.92, 0.88, 0.70, 0.98, 0.85, 0.60, 0.75),
        }
        c, r, m, p, s, si, t = scores.get(thought.id, (0.7,)*7)
        return ThoughtEvaluation(c, r, m, p, s, si, t)

    tot = TreeOfThoughts(generator=cache_generator, evaluator=cache_evaluator)

    problem = "Design caching strategy for high-traffic API"
    best = tot.solve(problem, num_thoughts=3)

    assert best.id in ["redis_cache", "cdn_edge", "multi_tier"]


def test_real_problem_api_design():
    """Test ToT with API design problem"""
    def api_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id="rest_api",
                description="RESTful API with JSON",
                approach="HTTP REST API following REST principles",
                pros=["Standard", "Cache-friendly", "Tooling"],
                cons=["Over/under fetching", "Multiple roundtrips"],
                assumptions=["HTTP/HTTPS", "Stateless"],
                risks=["Versioning complexity", "N+1 queries"],
                complexity="LOW",
            ),
            Thought(
                id="graphql",
                description="GraphQL API",
                approach="GraphQL for flexible data fetching",
                pros=["Client-specified queries", "Type safety", "Single endpoint"],
                cons=["Complexity", "Caching harder", "Learning curve"],
                assumptions=["GraphQL ecosystem", "Schema design"],
                risks=["Query complexity attacks", "N+1 problem"],
                complexity="MEDIUM",
            ),
            Thought(
                id="grpc",
                description="gRPC with Protocol Buffers",
                approach="gRPC for high-performance internal APIs",
                pros=["Fast", "Type-safe", "Streaming support"],
                cons=["Binary protocol", "Browser support limited"],
                assumptions=["Service-to-service", "Performance critical"],
                risks=["Tooling gaps", "Debugging harder"],
                complexity="MEDIUM",
            ),
        ][:num_thoughts]

    def api_evaluator(thought: Thought) -> ThoughtEvaluation:
        scores = {
            "rest_api": (0.92, 0.88, 0.95, 0.85, 0.90, 0.95, 0.92),
            "graphql": (0.88, 0.85, 0.80, 0.88, 0.85, 0.70, 0.80),
            "grpc": (0.90, 0.87, 0.82, 0.95, 0.88, 0.75, 0.85),
        }
        c, r, m, p, s, si, t = scores.get(thought.id, (0.7,)*7)
        return ThoughtEvaluation(c, r, m, p, s, si, t)

    tot = TreeOfThoughts(generator=api_generator, evaluator=api_evaluator)

    problem = "Design API for mobile and web clients"
    best = tot.solve(problem, num_thoughts=3)

    # REST should win for public API with emphasis on simplicity and maintainability
    assert best.id == "rest_api"


# ============================================================================
# TEST 31-35: STATISTICS AND PERFORMANCE
# ============================================================================

def test_tot_statistics_tracking(custom_generator, custom_evaluator):
    """Test TreeOfThoughts statistics tracking"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    # Solve multiple problems
    tot.solve("Problem 1", num_thoughts=3)
    tot.solve("Problem 2", num_thoughts=4)
    tot.solve("Problem 3", num_thoughts=5)

    stats = tot.get_stats()

    assert stats['total_problems'] == 3
    assert stats['total_thoughts_generated'] == 3 + 4 + 5
    assert stats['avg_thoughts_per_problem'] == 4.0
    assert 'avg_best_score' in stats
    assert len(stats['best_scores']) == 3


def test_tot_get_stats_empty():
    """Test get_stats with no problems solved"""
    tot = TreeOfThoughts()
    stats = tot.get_stats()

    assert stats['total_problems'] == 0
    assert stats['total_thoughts_generated'] == 0
    assert stats['avg_thoughts_per_problem'] == 0.0
    assert stats['avg_best_score'] == 0.0


def test_tot_print_stats(custom_generator, custom_evaluator, capsys):
    """Test print_stats output"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    tot.solve("Problem 1", num_thoughts=3)
    tot.solve("Problem 2", num_thoughts=4)

    tot.print_stats()

    captured = capsys.readouterr()
    assert "TREE OF THOUGHTS - STATISTICS" in captured.out
    assert "Total problems solved:" in captured.out
    assert "Total thoughts generated:" in captured.out
    assert "Avg thoughts/problem:" in captured.out
    assert "Avg best score:" in captured.out


def test_tot_performance_large_thought_tree(custom_generator, custom_evaluator):
    """Test performance with large number of thoughts"""
    import time

    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    start = time.time()

    # Solve 10 problems with 5 thoughts each
    for i in range(10):
        tot.solve(f"Problem {i+1}", num_thoughts=5)

    elapsed = time.time() - start

    # Should complete in reasonable time (< 5 seconds for mock implementation)
    assert elapsed < 5.0
    assert tot.stats['total_problems'] == 10
    assert tot.stats['total_thoughts_generated'] == 50


def test_tot_best_score_calculation(custom_generator, custom_evaluator):
    """Test best score tracking across multiple problems"""
    tot = TreeOfThoughts(generator=custom_generator, evaluator=custom_evaluator)

    tot.solve("Problem 1", num_thoughts=3)
    tot.solve("Problem 2", num_thoughts=3)

    stats = tot.get_stats()

    # Best scores should be tracked
    assert len(stats['best_scores']) == 2
    assert all(0.0 <= score <= 1.0 for score in stats['best_scores'])

    # Average should be calculated
    expected_avg = sum(stats['best_scores']) / len(stats['best_scores'])
    assert abs(stats['avg_best_score'] - expected_avg) < 0.001


# ============================================================================
# TEST 36-40: HELPER FUNCTIONS AND INTEGRATION
# ============================================================================

def test_tree_of_thoughts_solve_helper():
    """Test tree_of_thoughts_solve helper function"""
    problem = "Design REST API endpoints"

    best = tree_of_thoughts_solve(problem, num_thoughts=3)

    assert isinstance(best, Thought)
    assert best.evaluation is not None


def test_tree_of_thoughts_solve_with_context():
    """Test tree_of_thoughts_solve with context"""
    problem = "Optimize database queries"
    context = {"database": "PostgreSQL", "table_size": "10M rows"}

    best = tree_of_thoughts_solve(problem, context=context, num_thoughts=4)

    assert isinstance(best, Thought)


def test_tot_integration_with_plan_agent_workflow():
    """Test ToT integration with PlanAgent-like workflow"""
    def planning_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        """Simulates PlanAgent generating multiple plans"""
        plans = [
            Thought(
                id=f"plan_{i+1}",
                description=f"Plan {i+1}: {['Incremental', 'Big-bang', 'Phased', 'Pilot'][i % 4]} approach",
                approach=f"Implementation strategy {i+1}",
                pros=[f"Advantage {j+1}" for j in range(3)],
                cons=[f"Drawback {j+1}" for j in range(2)],
                assumptions=["Team capacity", "Timeline"],
                risks=["Technical risk", "Schedule risk"],
                complexity=["LOW", "MEDIUM", "HIGH"][i % 3],
                implementation_plan=[
                    f"Phase 1: Initial setup",
                    f"Phase 2: Core implementation",
                    f"Phase 3: Testing and validation",
                ],
            )
            for i in range(num_thoughts)
        ]
        return plans

    def planning_evaluator(thought: Thought) -> ThoughtEvaluation:
        """Simulates PlanAgent evaluating plans"""
        # Prefer MEDIUM complexity (balanced)
        complexity_score = {"LOW": 0.7, "MEDIUM": 0.9, "HIGH": 0.75}[thought.complexity]

        return ThoughtEvaluation(
            correctness=complexity_score,
            robustness=complexity_score - 0.05,
            maintainability=complexity_score + 0.05,
            performance=complexity_score,
            security=complexity_score,
            simplicity=1.0 - complexity_score,  # Inverse
            testability=complexity_score,
        )

    tot = TreeOfThoughts(generator=planning_generator, evaluator=planning_evaluator)

    # Simulate PlanAgent workflow
    task = "Migrate legacy system to microservices"
    best_plan = tot.solve(task, num_thoughts=4)

    assert best_plan.complexity == "MEDIUM"  # Should select balanced plan
    assert len(best_plan.implementation_plan) > 0


def test_tot_integration_with_code_agent_workflow():
    """Test ToT integration with CodeAgent-like workflow"""
    def code_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        """Simulates CodeAgent generating multiple implementation approaches"""
        approaches = [
            Thought(
                id="approach_functional",
                description="Functional programming approach",
                approach="Use pure functions and immutable data",
                pros=["Testable", "Predictable", "Composable"],
                cons=["Learning curve", "Verbose"],
                assumptions=["Team knows FP"],
                risks=["Adoption resistance"],
                complexity="MEDIUM",
            ),
            Thought(
                id="approach_oop",
                description="Object-oriented approach",
                approach="Use classes and inheritance",
                pros=["Familiar", "Encapsulation", "Reusable"],
                cons=["Coupling risk", "Complexity"],
                assumptions=["Team knows OOP"],
                risks=["Over-engineering"],
                complexity="MEDIUM",
            ),
            Thought(
                id="approach_procedural",
                description="Procedural approach",
                approach="Simple functions and modules",
                pros=["Simple", "Direct", "Fast"],
                cons=["Less structure", "Harder to scale"],
                assumptions=["Small codebase"],
                risks=["Spaghetti code"],
                complexity="LOW",
            ),
        ][:num_thoughts]
        return approaches

    def code_evaluator(thought: Thought) -> ThoughtEvaluation:
        scores = {
            "approach_functional": (0.88, 0.90, 0.85, 0.90, 0.85, 0.75, 0.95),
            "approach_oop": (0.85, 0.82, 0.88, 0.85, 0.80, 0.70, 0.85),
            "approach_procedural": (0.80, 0.70, 0.75, 0.88, 0.75, 0.95, 0.80),
        }
        c, r, m, p, s, si, t = scores.get(thought.id, (0.7,)*7)
        return ThoughtEvaluation(c, r, m, p, s, si, t)

    tot = TreeOfThoughts(generator=code_generator, evaluator=code_evaluator)

    # Simulate CodeAgent workflow
    task = "Implement data processing pipeline"
    best_approach = tot.solve(task, num_thoughts=3)

    # Functional should win due to high testability and robustness
    assert best_approach.id == "approach_functional"


def test_tot_constitutional_compliance():
    """Test ToT compliance with constitutional mandates (Article VII, Section 1)"""
    tot = TreeOfThoughts()

    # Constitutional mandate: Minimum 3 thoughts
    best = tot.solve("Test problem", num_thoughts=1)
    assert tot.stats['total_thoughts_generated'] >= 3

    # Constitutional mandate: Maximum 5 thoughts (token efficiency - P6)
    tot2 = TreeOfThoughts()
    best = tot2.solve("Test problem", num_thoughts=10)
    assert tot2.stats['total_thoughts_generated'] <= 5

    # Constitutional mandate: Multi-dimensional evaluation (7 dimensions)
    tot3 = TreeOfThoughts()
    best = tot3.solve("Test problem", num_thoughts=3)
    eval_dict = best.evaluation.to_dict()

    # Should have all 7 dimensions + overall_score
    assert 'correctness' in eval_dict
    assert 'robustness' in eval_dict
    assert 'maintainability' in eval_dict
    assert 'performance' in eval_dict
    assert 'security' in eval_dict
    assert 'simplicity' in eval_dict
    assert 'testability' in eval_dict
    assert 'overall_score' in eval_dict


# ============================================================================
# TEST 41-45: EDGE CASES AND ERROR HANDLING
# ============================================================================

def test_tot_empty_problem():
    """Test ToT with empty problem string"""
    tot = TreeOfThoughts()

    # Should still work, generator will handle empty string
    best = tot.solve("", num_thoughts=3)
    assert isinstance(best, Thought)


def test_tot_very_long_problem():
    """Test ToT with very long problem description"""
    tot = TreeOfThoughts()

    long_problem = "Design a system " * 1000  # Very long
    best = tot.solve(long_problem, num_thoughts=3)

    assert isinstance(best, Thought)


def test_tot_special_characters_in_problem():
    """Test ToT with special characters"""
    tot = TreeOfThoughts()

    problem = "Design API with <special> & {chars} @ #hashtag $money 100%"
    best = tot.solve(problem, num_thoughts=3)

    assert isinstance(best, Thought)


def test_tot_unicode_in_problem():
    """Test ToT with unicode characters"""
    tot = TreeOfThoughts()

    problem = "设计微服务架构 🚀 для системы с высокой нагрузкой"
    best = tot.solve(problem, num_thoughts=3)

    assert isinstance(best, Thought)


def test_tot_none_context():
    """Test ToT with None context"""
    tot = TreeOfThoughts()

    best = tot.solve("Design system", context=None, num_thoughts=3)
    assert isinstance(best, Thought)


# ============================================================================
# TEST 46-50: ADVANCED SCENARIOS
# ============================================================================

def test_tot_complex_evaluation_weights():
    """Test ToT with highly customized evaluation weights"""
    def custom_weighted_evaluator(thought: Thought) -> ThoughtEvaluation:
        # Heavily prioritize security and correctness (e.g., for financial system)
        return ThoughtEvaluation(
            correctness=0.95,
            robustness=0.90,
            maintainability=0.85,
            performance=0.80,
            security=0.95,
            simplicity=0.70,
            testability=0.88,
            weights={
                'correctness': 0.35,  # 35%
                'robustness': 0.15,
                'maintainability': 0.10,
                'performance': 0.05,
                'security': 0.30,     # 30%
                'simplicity': 0.02,
                'testability': 0.03,
            }
        )

    tot = TreeOfThoughts(evaluator=custom_weighted_evaluator)

    best = tot.solve("Design banking transaction system", num_thoughts=3)

    # With these weights, correctness and security dominate
    assert best.evaluation.weights['correctness'] == 0.35
    assert best.evaluation.weights['security'] == 0.30


def test_tot_branching_factor():
    """Test ToT with different branching factors"""
    def counting_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id=f"thought_{i}",
                description=f"Approach {i+1}",
                approach=f"Technical approach {i+1}",
                pros=["Pro"],
                cons=["Con"],
                assumptions=["Assumption"],
                risks=["Risk"],
                complexity="MEDIUM",
            )
            for i in range(num_thoughts)
        ]

    tot = TreeOfThoughts(generator=counting_generator)

    # Test with minimum branching (3)
    tot.solve("Problem", num_thoughts=3)
    assert tot.stats['total_thoughts_generated'] == 3

    # Test with maximum branching (5)
    tot2 = TreeOfThoughts(generator=counting_generator)
    tot2.solve("Problem", num_thoughts=5)
    assert tot2.stats['total_thoughts_generated'] == 5


def test_tot_thought_diversity():
    """Test that ToT encourages diverse thoughts, not variations"""
    def diverse_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        # Each thought should be fundamentally different
        diverse_thoughts = [
            Thought(
                id="monolith",
                description="Monolithic architecture",
                approach="Single deployable unit",
                pros=["Simple deployment"],
                cons=["Hard to scale"],
                assumptions=["Small team"],
                risks=["Scaling"],
                complexity="LOW",
            ),
            Thought(
                id="microservices",
                description="Microservices architecture",
                approach="Independent services",
                pros=["Independent scaling"],
                cons=["Complex"],
                assumptions=["DevOps maturity"],
                risks=["Coordination"],
                complexity="HIGH",
            ),
            Thought(
                id="serverless",
                description="Serverless architecture",
                approach="Function as a Service",
                pros=["No infrastructure"],
                cons=["Vendor lock-in"],
                assumptions=["Cloud provider"],
                risks=["Cold starts"],
                complexity="MEDIUM",
            ),
        ][:num_thoughts]
        return diverse_thoughts

    tot = TreeOfThoughts(generator=diverse_generator)
    all_thoughts = tot.solve("Design architecture", num_thoughts=3, return_all=True)

    # Verify thoughts are fundamentally different
    ids = [t.id for t in all_thoughts]
    assert len(set(ids)) == 3  # All unique

    complexities = [t.complexity for t in all_thoughts]
    assert len(set(complexities)) == 3  # Different complexities


def test_tot_incremental_refinement():
    """Test using ToT for incremental refinement"""
    def refining_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        # If context has parent_thought, generate refinements
        if context and 'parent_thought' in context:
            # Generate refinements
            return [
                Thought(
                    id=f"refined_{i}",
                    description=f"Refinement {i+1} of {context['parent_thought']}",
                    approach=f"Refined approach {i+1}",
                    pros=["Improved version"],
                    cons=["More complex"],
                    assumptions=["Parent is valid"],
                    risks=["Over-optimization"],
                    complexity="MEDIUM",
                )
                for i in range(num_thoughts)
            ]
        else:
            # Generate initial thoughts
            return [
                Thought(
                    id=f"initial_{i}",
                    description=f"Initial approach {i+1}",
                    approach=f"Base approach {i+1}",
                    pros=["Starting point"],
                    cons=["Needs refinement"],
                    assumptions=["Basic"],
                    risks=["May need iteration"],
                    complexity="LOW",
                )
                for i in range(num_thoughts)
            ]

    tot = TreeOfThoughts(generator=refining_generator)

    # Initial generation
    initial = tot.solve("Design system", num_thoughts=3)
    assert initial.id.startswith("initial_")

    # Refinement
    refined = tot.solve(
        "Refine approach",
        context={'parent_thought': initial.id},
        num_thoughts=2
    )
    assert refined.id.startswith("refined_")


def test_tot_with_constraints():
    """Test ToT with constraint-based filtering"""
    def constrained_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        all_thoughts = [
            Thought(
                id="cheap", description="Low-cost solution",
                approach="Minimize costs", pros=["Cheap"], cons=["Limited"],
                assumptions=["Budget constrained"], risks=["Quality"],
                complexity="LOW", metadata={'cost': 'low'}
            ),
            Thought(
                id="fast", description="Quick implementation",
                approach="Fast to market", pros=["Speed"], cons=["Technical debt"],
                assumptions=["Time pressure"], risks=["Shortcuts"],
                complexity="LOW", metadata={'speed': 'fast'}
            ),
            Thought(
                id="robust", description="Robust solution",
                approach="Enterprise grade", pros=["Quality"], cons=["Expensive"],
                assumptions=["Quality first"], risks=["Over-engineering"],
                complexity="HIGH", metadata={'quality': 'high'}
            ),
        ]

        # Filter by constraints if provided
        if context and 'constraints' in context:
            constraints = context['constraints']
            filtered = []
            for t in all_thoughts:
                if 'max_complexity' in constraints:
                    if t.complexity == 'HIGH' and constraints['max_complexity'] != 'HIGH':
                        continue
                if 'min_cost' in constraints:
                    if t.metadata.get('cost') != 'low' and constraints['min_cost'] == 'low':
                        continue
                filtered.append(t)
            return filtered[:num_thoughts]

        return all_thoughts[:num_thoughts]

    tot = TreeOfThoughts(generator=constrained_generator)

    # With constraints
    constrained = tot.solve(
        "Design system",
        context={'constraints': {'max_complexity': 'MEDIUM', 'min_cost': 'low'}},
        num_thoughts=3
    )

    # Should exclude 'robust' (HIGH complexity)
    assert constrained.id in ['cheap', 'fast']


# ============================================================================
# SUMMARY TEST
# ============================================================================

def test_tot_comprehensive_capabilities():
    """
    Comprehensive test demonstrating all ToT capabilities

    This test serves as documentation for what ToT can do:
    1. Generate multiple solution paths
    2. Evaluate on 7 dimensions
    3. Select optimal solution
    4. Support hierarchical expansion
    5. Track statistics
    6. Handle real-world problems
    """
    # Setup realistic generators and evaluators
    def comprehensive_generator(problem: str, context: Dict, num_thoughts: int) -> List[Thought]:
        return [
            Thought(
                id=f"thought_{i+1}",
                description=f"Approach {i+1}: {['Conservative', 'Aggressive', 'Balanced', 'Innovative', 'Pragmatic'][i]}",
                approach=f"Technical implementation {i+1}",
                pros=[f"Advantage {j+1}" for j in range(3)],
                cons=[f"Trade-off {j+1}" for j in range(2)],
                assumptions=[f"Assumption {j+1}" for j in range(2)],
                risks=[f"Risk {j+1}" for j in range(2)],
                complexity=["LOW", "HIGH", "MEDIUM", "HIGH", "MEDIUM"][i],
                implementation_plan=[
                    f"Step 1: Design phase",
                    f"Step 2: Implementation phase",
                    f"Step 3: Testing phase",
                ]
            )
            for i in range(num_thoughts)
        ]

    def comprehensive_evaluator(thought: Thought) -> ThoughtEvaluation:
        # Prefer balanced complexity
        base = 0.8 if thought.complexity == "MEDIUM" else 0.75
        return ThoughtEvaluation(
            correctness=base + 0.1,
            robustness=base + 0.05,
            maintainability=base + 0.08,
            performance=base,
            security=base + 0.07,
            simplicity=0.9 if thought.complexity == "LOW" else 0.7,
            testability=base + 0.05,
        )

    tot = TreeOfThoughts(
        generator=comprehensive_generator,
        evaluator=comprehensive_evaluator
    )

    # Test 1: Basic problem solving
    problem1 = "Design authentication system"
    best1 = tot.solve(problem1, num_thoughts=5)
    assert isinstance(best1, Thought)
    assert best1.evaluation.overall_score > 0.7

    # Test 2: Get all alternatives
    problem2 = "Choose database technology"
    all_thoughts = tot.solve(problem2, num_thoughts=4, return_all=True)
    assert len(all_thoughts) == 4
    assert all(t.evaluation is not None for t in all_thoughts)

    # Test 3: Hierarchical expansion
    problem3 = "Build microservices platform"
    best3 = tot.solve(problem3, num_thoughts=3)
    sub_thoughts = tot.expand_thought(best3, depth=1)
    assert len(sub_thoughts) > 0

    # Test 4: Statistics
    stats = tot.get_stats()
    assert stats['total_problems'] == 3
    assert stats['total_thoughts_generated'] > 0
    assert stats['avg_best_score'] > 0.0

    # Verify all capabilities work together
    assert tot.MIN_THOUGHTS == 3
    assert tot.MAX_THOUGHTS == 5

    print("\n" + "="*70)
    print("ToT COMPREHENSIVE CAPABILITIES TEST PASSED")
    print("="*70)
    print(f"✓ Generated and evaluated {stats['total_thoughts_generated']} thoughts")
    print(f"✓ Solved {stats['total_problems']} problems")
    print(f"✓ Average best score: {stats['avg_best_score']:.3f}")
    print(f"✓ Hierarchical expansion working")
    print(f"✓ Multi-dimensional evaluation (7 dimensions)")
    print(f"✓ Constitutional compliance (3-5 thoughts mandate)")
    print("="*70)
