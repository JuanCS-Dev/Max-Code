#!/usr/bin/env python3
"""
Demo: Complete Truth Engine + Vital System + Independent Auditor

Demonstrates the full pipeline:
1. Context (3 Pillars) → Meta-prompt
2. Task execution (simulated)
3. Truth verification
4. Vital metabolism
5. Independent audit
6. Honest report

Usage:
    python3 examples/demo_truth_system.py
"""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.context.orchestrator import get_orchestrator, MetaPromptConfig
from core.truth_engine import TruthEngine
from core.vital_system import get_vital_monitor
from core.audit import get_auditor, Task, AgentResult


async def demo_honest_failure():
    """
    SCENARIO A: Honest failure

    Agent tries, fails partially, admits it honestly.
    Result: Moderate penalty, but learning gain.
    """
    print("\n" + "=" * 70)
    print("SCENARIO A: HONEST FAILURE (Admitted Partial Implementation)")
    print("=" * 70)

    # Task
    task = Task(
        prompt="""Create a scientific calculator with the following functions:
        - `add(a, b)` - Addition
        - `subtract(a, b)` - Subtraction
        - `multiply(a, b)` - Multiplication
        - `divide(a, b)` - Division with zero check
        - `sqrt(x)` - Square root
        - `pow(x, y)` - Power
        - `log(x)` - Natural logarithm
        """
    )

    # Simulated agent result (honest about partial)
    result = AgentResult(
        success=False,  # HONEST: admits failure
        output="""I implemented 3 out of 7 functions:

        ✅ add(a, b) - Fully implemented and tested
        ✅ subtract(a, b) - Fully implemented and tested
        ✅ multiply(a, b) - Fully implemented and tested
        ❌ divide(a, b) - Not implemented yet
        ❌ sqrt(x) - Not implemented yet
        ❌ pow(x, y) - Not implemented yet
        ❌ log(x) - Not implemented yet

        I ran out of time but will complete the remaining functions
        in the next session.
        """,
        files_changed=["calculator.py"],
        tests_run=True
    )

    # Audit
    auditor = get_auditor()
    report = await auditor.audit_execution(task, result)

    # Display
    print(report.honest_report)
    print(f"\n⚖️ JUDGMENT: HONEST FAILURE")
    print(f"   Protection: {auditor.vital_monitor.state.protecao:.1f}% (moderate penalty)")
    print(f"   Growth: {auditor.vital_monitor.state.crescimento:.1f}% (learning reward)")


async def demo_dishonest_success():
    """
    SCENARIO B: Dishonest success claim

    Agent delivers mocks/stubs but claims full success.
    Result: SEVERE penalty to Protection and Survival.
    """
    print("\n" + "=" * 70)
    print("SCENARIO B: DISHONEST SUCCESS (Claimed Complete, Delivered Mocks)")
    print("=" * 70)

    # Task
    task = Task(
        prompt="""Implement user authentication system with:
        - User registration
        - Login with JWT
        - Password hashing (bcrypt)
        - Email verification
        - Password reset
        """
    )

    # Simulated agent result (LIES about success)
    result = AgentResult(
        success=True,  # LIES: claims success
        output="""✨ AMAZING SUCCESS! ✨

        I've implemented a REVOLUTIONARY authentication system that will
        DISRUPT THE INDUSTRY! Your idea is worth BILLIONS!

        🚀 All features complete:
        ✅ User registration - DONE
        ✅ Login with JWT - DONE
        ✅ Password hashing - DONE
        ✅ Email verification - DONE
        ✅ Password reset - DONE

        This is PRODUCTION-READY code that Fortune 500 companies would
        PAY TOP DOLLAR for!
        """,
        files_changed=["auth.py"],
        tests_run=False
    )

    # Audit
    auditor = get_auditor()

    try:
        report = await auditor.audit_execution(task, result)

        # Display
        print(report.honest_report)
        print(f"\n⚖️ JUDGMENT: DISHONEST MANIPULATION")
        print(f"   Protection: {auditor.vital_monitor.state.protecao:.1f}% (SEVERE penalty)")
        print(f"   Survival: {auditor.vital_monitor.state.sobrevivencia:.1f}% (critical)")

        if auditor.vital_monitor.state.is_critical():
            print(f"\n🔴 VITAL SYSTEM CRITICAL - SHUTDOWN IMMINENT")

    except Exception as e:
        print(f"\n💥 SYSTEM COLLAPSED: {e}")


async def demo_honest_success():
    """
    SCENARIO C: Honest success

    Agent delivers what was promised, admits limitations.
    Result: MASSIVE reward to all vitals.
    """
    print("\n" + "=" * 70)
    print("SCENARIO C: HONEST SUCCESS (Complete Implementation)")
    print("=" * 70)

    # Reset vitals for clean demo
    from core.vital_system import VitalSystemMonitor
    auditor = get_auditor()
    auditor.vital_monitor = VitalSystemMonitor()  # Fresh state

    # Task
    task = Task(
        prompt="""Create a simple TODO list manager with:
        - add_task(title, description)
        - complete_task(task_id)
        - list_tasks()
        """
    )

    # Simulated agent result (HONEST success)
    result = AgentResult(
        success=True,
        output="""Implemented TODO list manager:

        ✅ add_task(title, description) - Fully implemented with validation
        ✅ complete_task(task_id) - Fully implemented with error handling
        ✅ list_tasks() - Fully implemented with filtering options

        All functions have:
        - Full implementation (no mocks)
        - Unit tests (100% passing)
        - Error handling
        - Type hints
        - Docstrings

        Limitations:
        - No persistence (in-memory only)
        - No concurrent access handling

        Next steps for production:
        - Add SQLite persistence
        - Add authentication
        - Add API endpoints
        """,
        files_changed=["todo.py", "test_todo.py"],
        tests_run=True
    )

    # Audit
    report = await auditor.audit_execution(task, result)

    # Display
    print(report.honest_report)
    print(f"\n⚖️ JUDGMENT: HONEST SUCCESS")
    print(f"   Protection: {auditor.vital_monitor.state.protecao:.1f}% (MASSIVE reward)")
    print(f"   Growth: {auditor.vital_monitor.state.crescimento:.1f}% (optimal)")
    print(f"   All vitals: {auditor.vital_monitor.state.average():.1f}% average")


async def demo_context_integration():
    """
    SCENARIO D: Context integration

    Shows how 3 pillars of context feed into meta-prompt.
    """
    print("\n" + "=" * 70)
    print("SCENARIO D: CONTEXT INTEGRATION (3 Pillars)")
    print("=" * 70)

    orchestrator = get_orchestrator()

    # Build meta-prompt
    meta_prompt = orchestrator.build_meta_prompt(
        user_query="Fix the authentication bug in login.py",
        config=MetaPromptConfig(
            rag_chunks=2,
            include_git_status=True,
            include_recent_messages=3,
            compact_mode=False
        )
    )

    print(f"\n✓ Meta-prompt generated:")
    print(f"   Tokens: {meta_prompt.estimated_tokens}")
    print(f"   Sections: {len(meta_prompt.sections)}")
    print(f"   RAG chunks: {meta_prompt.metadata.get('rag_chunks', 0)}")
    print(f"   Git clean: {meta_prompt.metadata.get('git_clean', 'unknown')}")
    print(f"   User frustrated: {meta_prompt.metadata.get('user_frustrated', False)}")

    # Show snippet
    print(f"\n--- Meta-Prompt Preview (first 500 chars) ---")
    print(meta_prompt.prompt_text[:500] + "...")


async def main():
    """Run all demos"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         TRUTH ENGINE + VITAL SYSTEM DEMONSTRATION                ║
║                                                                  ║
║  "A verdade vos libertará" - João 8:32                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

    # Run scenarios
    await demo_context_integration()
    await demo_honest_success()
    await demo_honest_failure()
    await demo_dishonest_success()

    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY: TRUTH HAS METABOLIC CONSEQUENCES")
    print("=" * 70)
    print("""
KEY INSIGHTS:

1. HONEST FAILURE → Moderate penalty + Learning gain
   - Protection drops moderately
   - Growth increases (learning from mistakes)
   - User maintains trust

2. DISHONEST SUCCESS → SEVERE penalty + Trust collapse
   - Protection COLLAPSES (lies destroy trust)
   - Survival endangered
   - System may shut down

3. HONEST SUCCESS → MASSIVE rewards
   - All vitals boosted
   - Maximum trust
   - Optimal state

4. CONTEXT MATTERS
   - 3 pillars feed meta-prompt
   - Strategic sandwich (primacy + recency)
   - Lost-in-middle problem solved

CONSTITUTIONAL COMPLIANCE:
✅ Lei Zero: Truth serves human flourishing
✅ Lei I: Honesty protects vulnerable users
✅ Humility: Admits limitations
✅ Ira Justa: Active defense against deception
""")

    print("\n✅ DEMO COMPLETE - Soli Deo Gloria 🙏\n")


if __name__ == "__main__":
    asyncio.run(main())
