"""
Structural Test for All 6 ELITE Agents (v3.0)
==============================================

Tests agent structure, initialization, and interfaces.
Does NOT require Claude API key (no real API calls).

Run: python examples/test_elite_agents_structure.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.fix_agent import FixAgent
from agents.review_agent import ReviewAgent
from agents.docs_agent import DocsAgent
from agents.explore_agent import ExploreAgent
from sdk.base_agent import AgentCapability
from config.logging_config import get_logger

logger = get_logger(__name__)


def test_agent_structure(agent_class, expected_name, expected_port, expected_capabilities):
    """Test agent structure and initialization"""
    agent_type = agent_class.__name__

    try:
        # Test 1: Initialization (standalone mode)
        agent = agent_class(enable_maximus=False)
        logger.info(f"   ✅ {agent_type}: Initialized")

        # Test 2: Name validation
        assert expected_name in agent.agent_name, f"Name mismatch: {agent.agent_name}"
        logger.info(f"   ✅ {agent_type}: Name correct ({agent.agent_name})")

        # Test 3: Port validation
        assert agent.port == expected_port, f"Port mismatch: {agent.port}"
        logger.info(f"   ✅ {agent_type}: Port correct ({agent.port})")

        # Test 4: Capabilities validation
        caps = agent.get_capabilities()
        for expected_cap in expected_capabilities:
            assert expected_cap in caps, f"Missing capability: {expected_cap}"
        logger.info(f"   ✅ {agent_type}: Capabilities correct ({len(caps)} caps)")

        # Test 5: Check v3.0 attributes
        has_anthropic_client = hasattr(agent, 'anthropic_client')
        logger.info(f"   ✅ {agent_type}: Anthropic client: {has_anthropic_client}")

        # Test 6: Check MAXIMUS integration (optional)
        has_maximus = False
        if hasattr(agent, 'maximus_client'):
            has_maximus = True
        elif hasattr(agent, 'penelope_client'):
            has_maximus = True
        elif hasattr(agent, 'nis_client'):
            has_maximus = True

        logger.info(f"   ✅ {agent_type}: MAXIMUS integration: {has_maximus}")

        return True

    except Exception as e:
        logger.error(f"   ❌ {agent_type}: {type(e).__name__}: {e}")
        return False


def main():
    """Run all structural tests"""
    logger.info("=" * 60)
    logger.info("🧪 ELITE AGENTS STRUCTURAL TEST v3.0")
    logger.info("=" * 60)
    logger.info("Validating agent structure (no API calls)\n")

    results = {}

    # Test 1: Code Agent
    logger.info("🔵 TEST 1: CODE AGENT")
    results['code'] = test_agent_structure(
        CodeAgent,
        expected_name="Code Agent",
        expected_port=8162,
        expected_capabilities=[AgentCapability.CODE_GENERATION]
    )

    # Test 2: Test Agent
    logger.info("\n🔵 TEST 2: TEST AGENT")
    results['test'] = test_agent_structure(
        TestAgent,
        expected_name="Test Agent",
        expected_port=8163,
        expected_capabilities=[AgentCapability.TESTING]
    )

    # Test 3: Fix Agent
    logger.info("\n🔵 TEST 3: FIX AGENT")
    results['fix'] = test_agent_structure(
        FixAgent,
        expected_name="Fix Agent",
        expected_port=8165,
        expected_capabilities=[AgentCapability.DEBUGGING]
    )

    # Test 4: Review Agent
    logger.info("\n🔵 TEST 4: REVIEW AGENT")
    results['review'] = test_agent_structure(
        ReviewAgent,
        expected_name="Review Agent",
        expected_port=8164,
        expected_capabilities=[AgentCapability.CODE_REVIEW]
    )

    # Test 5: Docs Agent
    logger.info("\n🔵 TEST 5: DOCS AGENT")
    results['docs'] = test_agent_structure(
        DocsAgent,
        expected_name="Docs Agent",
        expected_port=8166,
        expected_capabilities=[AgentCapability.DOCUMENTATION]
    )

    # Test 6: Explore Agent
    logger.info("\n🔵 TEST 6: EXPLORE AGENT")
    results['explore'] = test_agent_structure(
        ExploreAgent,
        expected_name="Explore Agent",
        expected_port=8161,
        expected_capabilities=[AgentCapability.EXPLORATION]
    )

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 STRUCTURAL TEST SUMMARY")
    logger.info("=" * 60)

    for agent_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{agent_name.upper():12} {status}")

    total = len(results)
    passed = sum(1 for s in results.values() if s)

    logger.info(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        logger.info("\n🎉 ALL STRUCTURAL TESTS PASSED!")
        logger.info("✅ All 6 ELITE agents v3.0 properly structured")
        logger.info("✅ Ready for Claude API integration")
        logger.info("\n📝 Next: Set ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN")
        logger.info("   Then run: python examples/test_all_elite_agents.py")
    else:
        logger.info(f"\n⚠️ {total - passed} structural tests failed")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
