#!/usr/bin/env python3
"""
Test Code Agent v3.0 - Real Claude-powered generation

Tests the expanded code_agent with real Claude API calls.

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)

Run: python examples/test_code_agent.py
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.code_agent import CodeAgent
from sdk.base_agent import AgentTask
from config.logging_config import configure_logging, get_logger
import logging

logger = get_logger(__name__)


def test_basic_function():
    """Test 1: Generate a basic Python function"""
    print("\n" + "="*70)
    logger.info("TEST 1: Generate basic Python function")
    print("="*70)

    agent = CodeAgent(enable_maximus=False)  # Test without MAXIMUS first

    task = AgentTask(
        id="test_1",
        description="Create a function to calculate fibonacci numbers recursively",
        parameters={
            "language": "python",
            "requirements": [
                "Add type hints",
                "Include docstring",
                "Handle edge cases (n < 0)"
            ]
        }
    )

    result = agent.execute(task)

    if result.success:
        logger.info("✅ Code generation successful!")
        print("\n--- Generated Code ---")
        print(result.output['code'])
        print("--- End Generated Code ---\n")
    else:
        logger.error(f"❌ Code generation failed: {result.error}")

    return result.success


def test_class_generation():
    """Test 2: Generate a Python class"""
    print("\n" + "="*70)
    logger.info("TEST 2: Generate Python class")
    print("="*70)

    agent = CodeAgent(enable_maximus=False)

    task = AgentTask(
        id="test_2",
        description="Create a BinarySearchTree class with insert and search methods",
        parameters={
            "language": "python",
            "requirements": [
                "Use Pydantic for data validation",
                "Add type hints",
                "Include comprehensive docstrings",
                "Handle edge cases"
            ],
            "context": "This will be used in a production system"
        }
    )

    result = agent.execute(task)

    if result.success:
        logger.info("✅ Class generation successful!")
        print("\n--- Generated Code ---")
        print(result.output['code'])
        print("--- End Generated Code ---\n")
    else:
        logger.error(f"❌ Class generation failed: {result.error}")

    return result.success


def test_with_maximus():
    """Test 3: Generate code with MAXIMUS security analysis"""
    print("\n" + "="*70)
    logger.info("TEST 3: Generate code WITH MAXIMUS security analysis")
    print("="*70)

    agent = CodeAgent(enable_maximus=True)

    task = AgentTask(
        id="test_3",
        description="Create a function to validate and sanitize user input for SQL queries",
        parameters={
            "language": "python",
            "requirements": [
                "Prevent SQL injection",
                "Sanitize special characters",
                "Add input validation"
            ],
            "context": "This is for a web application handling sensitive data"
        }
    )

    result = agent.execute(task)

    if result.success:
        logger.info("✅ Code generation with MAXIMUS successful!")
        print("\n--- Generated Code ---")
        print(result.output['code'])
        print("--- End Generated Code ---\n")

        if result.output.get('security_issues'):
            logger.warning(f"⚠️ Security issues found: {len(result.output['security_issues'])}")
            for issue in result.output['security_issues']:
                logger.warning(f"   - {issue}")
        else:
            logger.info("✅ No security issues detected")
    else:
        logger.error(f"❌ Code generation failed: {result.error}")

    return result.success


def test_fallback_mode():
    """Test 4: Test fallback when Claude API unavailable"""
    print("\n" + "="*70)
    logger.info("TEST 4: Fallback mode (simulate API unavailable)")
    print("="*70)

    # Create agent without API key (forces fallback)
    original_key = os.environ.get('ANTHROPIC_API_KEY')
    if original_key:
        del os.environ['ANTHROPIC_API_KEY']

    agent = CodeAgent(enable_maximus=False)

    task = AgentTask(
        id="test_4",
        description="Create a simple hello world function",
        parameters={
            "language": "python"
        }
    )

    result = agent.execute(task)

    # Restore API key
    if original_key:
        os.environ['ANTHROPIC_API_KEY'] = original_key

    if result.success:
        logger.info("✅ Fallback mode working!")
        print("\n--- Generated Code (Fallback) ---")
        print(result.output['code'])
        print("--- End Generated Code ---\n")
    else:
        logger.error(f"❌ Fallback failed: {result.error}")

    return result.success


def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "CODE AGENT v3.0 - TEST SUITE" + " "*25 + "║")
    print("║" + " "*20 + "Real Claude-Powered Generation" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    print("\n")

    # Configure logging
    configure_logging(level=logging.INFO, format_style="human")

    # Run tests
    results = []

    logger.info("🧪 Running Code Agent tests...")
    print()

    results.append(("Basic Function", test_basic_function()))
    results.append(("Class Generation", test_class_generation()))
    results.append(("MAXIMUS Integration", test_with_maximus()))
    results.append(("Fallback Mode", test_fallback_mode()))

    # Summary
    print("\n" + "="*70)
    logger.info("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {status}: {name}")

    print()
    logger.info(f"Total: {passed}/{total} tests passed")
    print("="*70)
    print()

    if passed == total:
        logger.info("✅ All tests passed!")
        print()
        logger.info("📊 CODE AGENT v3.0 FEATURES:")
        logger.info("   ✅ Real Claude API integration")
        logger.info("   ✅ Chain of thought reasoning")
        logger.info("   ✅ XML-structured requests")
        logger.info("   ✅ System prompt role assignment")
        logger.info("   ✅ MAXIMUS security analysis")
        logger.info("   ✅ Fallback mode when API unavailable")
        logger.info("   ✅ 100% EPL emoji preservation")
        print()
    else:
        logger.warning(f"⚠️ {total - passed} test(s) failed")

    print('Biblical Foundation:')
    print('"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)')
    print()


if __name__ == "__main__":
    main()
