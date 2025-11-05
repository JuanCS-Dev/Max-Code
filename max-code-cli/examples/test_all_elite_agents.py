"""
Test Suite for All 6 ELITE Agents (v3.0)
=========================================

Tests all agents in standalone mode (no MAXIMUS required).
Validates real Claude API integration.

Run: python examples/test_all_elite_agents.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.fix_agent import FixAgent
from agents.review_agent import ReviewAgent
from agents.docs_agent import DocsAgent
from agents.explore_agent import ExploreAgent
from sdk.base_agent import AgentTask
from config.logging_config import get_logger

logger = get_logger(__name__)


async def test_code_agent():
    """Test 1: Code generation"""
    logger.info("=" * 60)
    logger.info("🧪 TEST 1: CODE AGENT (ELITE v3.0)")
    logger.info("=" * 60)

    agent = CodeAgent(agent_id="test_code", enable_maximus=False)

    task = AgentTask(
        id="test-code-1",
        description="Create a function that calculates fibonacci numbers",
        agent_id="test_code",
        parameters={
            "language": "python",
            "requirements": [
                "Use recursion with memoization",
                "Add type hints",
                "Include docstring"
            ]
        }
    )

    result = await agent._execute_async(task)

    logger.info(f"\n{'✅ SUCCESS' if result.success else '❌ FAILURE'}")
    logger.info(f"Code length: {len(result.output.get('code', ''))} chars")
    logger.info(f"Mode: {result.metrics.get('mode')}")

    if result.output.get('code'):
        logger.info("\nGenerated code preview:")
        logger.info(result.output['code'][:300] + "...")

    return result.success


async def test_test_agent():
    """Test 2: Test generation"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TEST 2: TEST AGENT (ELITE v3.0)")
    logger.info("=" * 60)

    agent = TestAgent(agent_id="test_test", enable_maximus=False)

    function_code = '''
def fibonacci(n: int) -> int:
    """Calculate nth fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
'''

    task = AgentTask(
        id="test-test-1",
        description="Generate tests for fibonacci function",
        agent_id="test_test",
        parameters={
            "function_code": function_code,
            "test_framework": "pytest",
            "coverage_threshold": 0.90
        }
    )

    result = await agent._execute_async(task)

    logger.info(f"\n{'✅ SUCCESS' if result.success else '❌ FAILURE'}")
    logger.info(f"Tests generated: {result.output.get('test_count', 0)}")
    logger.info(f"Mode: {result.metrics.get('mode')}")

    if result.output.get('test_code'):
        logger.info("\nTest code preview:")
        logger.info(result.output['test_code'][:300] + "...")

    return result.success


async def test_fix_agent():
    """Test 3: Bug fixing"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TEST 3: FIX AGENT (ELITE v3.0)")
    logger.info("=" * 60)

    agent = FixAgent(agent_id="test_fix", enable_maximus=False)

    broken_code = '''
def divide(a, b):
    return a / b
'''

    error_trace = '''
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    result = divide(10, 0)
  File "test.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
'''

    task = AgentTask(
        id="test-fix-1",
        description="Fix division by zero bug",
        agent_id="test_fix",
        parameters={
            "code": broken_code,
            "error": error_trace
        }
    )

    result = await agent._execute_async(task)

    logger.info(f"\n{'✅ SUCCESS' if result.success else '❌ FAILURE'}")
    logger.info(f"Fixed code length: {len(result.output.get('fixed_code', ''))} chars")
    logger.info(f"Mode: {result.metrics.get('mode')}")

    if result.output.get('fixed_code'):
        logger.info("\nFixed code preview:")
        logger.info(result.output['fixed_code'][:300] + "...")

    return result.success


async def test_review_agent():
    """Test 4: Code review"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TEST 4: REVIEW AGENT (ELITE v3.0)")
    logger.info("=" * 60)

    agent = ReviewAgent(agent_id="test_review", enable_maximus=False)

    code_to_review = '''
import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()
'''

    task = AgentTask(
        id="test-review-1",
        description="Review code for security and best practices",
        agent_id="test_review",
        parameters={
            "code": code_to_review,
            "review_type": "full",
            "context": "User authentication function"
        }
    )

    result = await agent._execute_async(task)

    logger.info(f"\n{'✅ SUCCESS' if result.success else '❌ FAILURE'}")
    logger.info(f"Overall score: {result.output.get('overall_score', 0):.2f}")
    logger.info(f"Mode: {result.metrics.get('mode')}")

    if result.output.get('claude_review'):
        review = result.output['claude_review']
        logger.info(f"\nMaintainability: {review.get('maintainability_score', 'N/A')}/10")
        logger.info(f"Critical issues: {review.get('critical_issues', 0)}")
        logger.info(f"High issues: {review.get('high_issues', 0)}")

    return result.success


async def test_docs_agent():
    """Test 5: Documentation generation"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TEST 5: DOCS AGENT (ELITE v3.0)")
    logger.info("=" * 60)

    agent = DocsAgent(agent_id="test_docs", enable_maximus=False)

    code = '''
class UserManager:
    """Manages user authentication and authorization."""

    def authenticate(self, username: str, password: str) -> bool:
        """Verify user credentials."""
        pass

    def authorize(self, user_id: int, resource: str) -> bool:
        """Check if user has access to resource."""
        pass
'''

    task = AgentTask(
        id="test-docs-1",
        description="Generate API documentation",
        agent_id="test_docs",
        parameters={
            "code": code,
            "doc_type": "api",
            "changes": []
        }
    )

    result = await agent._execute_async(task)

    logger.info(f"\n{'✅ SUCCESS' if result.success else '❌ FAILURE'}")
    logger.info(f"Doc length: {result.output.get('doc_length', 0)} chars")
    logger.info(f"Mode: {result.metrics.get('mode')}")

    if result.output.get('docs'):
        logger.info("\nDocumentation preview:")
        logger.info(result.output['docs'][:300] + "...")

    return result.success


async def test_explore_agent():
    """Test 6: Codebase exploration"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TEST 6: EXPLORE AGENT (ELITE v3.0)")
    logger.info("=" * 60)

    agent = ExploreAgent(agent_id="test_explore")

    task = AgentTask(
        id="test-explore-1",
        description="Analyze project structure",
        agent_id="test_explore",
        parameters={
            "query": "What is the architecture of this agent system?",
            "target": "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/agents",
            "scope": "full",
            "depth": 2
        }
    )

    result = await agent._execute_async(task)

    logger.info(f"\n{'✅ SUCCESS' if result.success else '❌ FAILURE'}")
    logger.info(f"Files found: {result.output.get('total_files', 0)}")
    logger.info(f"Scope: {result.metrics.get('scope')}")

    if result.output.get('structure'):
        structure = result.output['structure']
        logger.info(f"\nStructure:")
        logger.info(f"  Total LOC: {structure.get('total_loc', 0)}")
        logger.info(f"  Directories: {', '.join(structure.get('directories', []))}")
        logger.info(f"  Patterns: {', '.join(structure.get('patterns', []))}")

    if result.output.get('insights'):
        logger.info(f"\nInsights generated: ✅")

    return result.success


async def main():
    """Run all tests"""
    logger.info("🚀 ELITE AGENTS TEST SUITE v3.0")
    logger.info("Testing all 6 agents in standalone mode\n")

    # Check authentication
    from core.auth import get_anthropic_client
    client = get_anthropic_client()
    if not client:
        logger.error("❌ No authentication found!")
        logger.error("Set CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY")
        return

    logger.info("🔑 Authentication: ✅\n")

    # Run all tests
    results = {}

    try:
        results['code'] = await test_code_agent()
    except Exception as e:
        logger.error(f"❌ Code Agent failed: {e}")
        results['code'] = False

    try:
        results['test'] = await test_test_agent()
    except Exception as e:
        logger.error(f"❌ Test Agent failed: {e}")
        results['test'] = False

    try:
        results['fix'] = await test_fix_agent()
    except Exception as e:
        logger.error(f"❌ Fix Agent failed: {e}")
        results['fix'] = False

    try:
        results['review'] = await test_review_agent()
    except Exception as e:
        logger.error(f"❌ Review Agent failed: {e}")
        results['review'] = False

    try:
        results['docs'] = await test_docs_agent()
    except Exception as e:
        logger.error(f"❌ Docs Agent failed: {e}")
        results['docs'] = False

    try:
        results['explore'] = await test_explore_agent()
    except Exception as e:
        logger.error(f"❌ Explore Agent failed: {e}")
        results['explore'] = False

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)

    for agent_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{agent_name.upper():12} {status}")

    total = len(results)
    passed = sum(1 for s in results.values() if s)

    logger.info(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        logger.info("\n🎉 ALL TESTS PASSED! ELITE AGENTS v3.0 READY!")
    else:
        logger.info(f"\n⚠️ {total - passed} tests failed")


if __name__ == "__main__":
    asyncio.run(main())
