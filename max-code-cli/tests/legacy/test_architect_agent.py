"""
Test Suite for Sophia - A Arquiteta (ArchitectAgent)

Testes funcionais para o agente co-arquiteto.
"""

import pytest
import asyncio
from agents.architect_agent import ArchitectAgent, ArchitecturalConcern
from sdk.base_agent import AgentTask


@pytest.mark.asyncio
async def test_architect_agent_initialization():
    """Test Sophia initialization"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    assert sophia.agent_id == "sophia"
    assert sophia.agent_name == "Sophia - A Arquiteta (Co-Architect)"
    assert sophia.port == 8167
    assert sophia.decision_fusion.maxcode_weight == 0.5
    assert sophia.decision_fusion.maximus_weight == 0.5
    print("✅ Sophia initialized correctly")


@pytest.mark.asyncio
async def test_architect_agent_standalone_mode():
    """Test Sophia in standalone mode (no MAXIMUS)"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    task = AgentTask(
        id="arch-001",
        description="Design a scalable microservices architecture for e-commerce",
        parameters={
            "requirements": [
                "Handle 10k requests/sec",
                "99.9% availability",
                "Easy to maintain"
            ]
        }
    )

    result = await sophia._execute_async(task)

    assert result.success
    assert "architectural_decision" in result.output
    assert result.metrics["mode"] == "standalone"

    decision = result.output["architectural_decision"]
    assert hasattr(decision, "decision")
    assert hasattr(decision, "rationale")
    assert hasattr(decision, "alternatives_considered")
    assert len(decision.alternatives_considered) >= 2

    print(f"✅ Sophia standalone mode works")
    print(f"   Decision: {decision.decision[:100]}...")
    print(f"   Alternatives considered: {len(decision.alternatives_considered)}")


@pytest.mark.asyncio
async def test_architect_agent_problem_analysis():
    """Test Sophia's problem analysis capability"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    task = AgentTask(
        id="arch-002",
        description="We have a monolith with 500k LOC. Performance is degrading. What should we do?",
        parameters={
            "requirements": ["scalability", "performance"],
            "constraints": ["legacy code"]
        }
    )

    # Test internal method
    problem_analysis = sophia._analyze_problem(task)

    assert "complexity" in problem_analysis
    assert "concerns" in problem_analysis
    assert problem_analysis["complexity"] in ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]

    # Should identify scalability and performance concerns
    concerns = problem_analysis["concerns"]
    assert any(c in [ArchitecturalConcern.SCALABILITY, ArchitecturalConcern.PERFORMANCE]
               for c in concerns)

    print(f"✅ Problem analysis works")
    print(f"   Complexity: {problem_analysis['complexity']}")
    print(f"   Concerns: {[c.value for c in concerns]}")


@pytest.mark.asyncio
async def test_architect_agent_red_team():
    """Test Sophia's adversarial criticism (Red Team)"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    option = {
        "id": "opt-1",
        "approach": "Migrate to microservices",
        "description": "Break monolith into 20 microservices",
        "pros": ["Better scalability", "Independent deployment"],
        "cons": ["Increased complexity", "Distributed transactions"],
        "complexity": "HIGH",
        "patterns": ["microservices", "event-driven"],
    }

    criticisms = sophia._red_team_criticism(option)

    assert len(criticisms) > 0
    for criticism in criticisms:
        assert "concern" in criticism
        assert "question" in criticism
        assert "risk_level" in criticism

    print(f"✅ Red Team criticism works")
    print(f"   Generated {len(criticisms)} critical questions")
    for i, crit in enumerate(criticisms[:3], 1):
        print(f"   {i}. [{crit['risk_level']}] {crit['question'][:80]}...")


@pytest.mark.asyncio
async def test_architect_agent_decision_history():
    """Test Sophia's decision history tracking"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    initial_count = len(sophia.decision_history)

    task = AgentTask(
        id="arch-003",
        description="Choose between REST and GraphQL for API",
        parameters={
            "requirements": ["API design"],
            "constraints": []
        }
    )

    result = await sophia._execute_async(task)

    assert len(sophia.decision_history) == initial_count + 1
    assert result.success

    latest_decision = sophia.decision_history[-1]
    assert hasattr(latest_decision, "id")
    assert hasattr(latest_decision, "decision")
    assert hasattr(latest_decision, "timestamp")

    print(f"✅ Decision history tracking works")
    print(f"   Total decisions: {len(sophia.decision_history)}")


def test_design_pattern_knowledge():
    """Test Sophia's design pattern knowledge base"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    # Should have knowledge of common patterns
    common_patterns = ["microservices", "event-driven", "layered", "cqrs"]

    for pattern in common_patterns:
        pattern_info = sophia._get_design_pattern_info(pattern)
        assert pattern_info is not None
        assert hasattr(pattern_info, "name")
        assert hasattr(pattern_info, "use_case")
        assert hasattr(pattern_info, "pros")
        assert hasattr(pattern_info, "cons")

    print(f"✅ Design pattern knowledge base works")
    print(f"   Tested {len(common_patterns)} common patterns")


@pytest.mark.asyncio
async def test_architect_agent_architectural_options():
    """Test Sophia's architectural options exploration (Tree of Thoughts)"""
    sophia = ArchitectAgent(agent_id="sophia", enable_maximus=False)

    task = AgentTask(
        id="arch-004",
        description="Design authentication system for multi-tenant SaaS",
        parameters={}
    )

    problem_analysis = sophia._analyze_problem(task)
    options = sophia._explore_architectural_options(task, problem_analysis)

    # Should generate 3 options
    assert len(options) == 3

    for option in options:
        assert "id" in option
        assert "approach" in option
        assert "pros" in option
        assert "cons" in option
        assert "complexity" in option

    print(f"✅ Architectural options exploration works")
    print(f"   Generated {len(options)} architectural options")
    for i, opt in enumerate(options, 1):
        print(f"   {i}. {opt['approach']} (Complexity: {opt['complexity']})")


if __name__ == "__main__":
    print("=" * 60)
    print("SOPHIA - A ARQUITETA - Test Suite")
    print("=" * 60)

    # Run tests
    asyncio.run(test_architect_agent_initialization())
    asyncio.run(test_architect_agent_standalone_mode())
    asyncio.run(test_architect_agent_problem_analysis())
    asyncio.run(test_architect_agent_red_team())
    asyncio.run(test_architect_agent_decision_history())
    test_design_pattern_knowledge()
    asyncio.run(test_architect_agent_architectural_options())

    print("\n" + "=" * 60)
    print("✅ All Sophia tests passed!")
    print("=" * 60)
