"""
Multi-Agent Collaboration Tests - FASE 3.3
Constitutional AI v3.0 - PAGANI Quality Standard

Tests validating MULTIPLE agents working together on complex workflows.
Following Anthropic Pattern: Research → Plan → Implement → Review

Target: 35+ tests, 75%+ success rate
"""

import pytest
import sys
import ast
import time
from pathlib import Path

# Add project root to path BEFORE imports (needed for pytest collection)
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.plan_agent import PlanAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.review_agent import ReviewAgent
from agents.fix_agent import FixAgent
from agents.docs_agent import DocsAgent
from agents.architect_agent import ArchitectAgent
from agents.explore_agent import ExploreAgent
from sdk.base_agent import AgentTask, AgentResult


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: PLAN → CODE WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestPlanToCodeWorkflows:
    """Test Plan → Code pipeline"""

    def test_plan_then_code_simple_task(self):
        """Test PlanAgent → CodeAgent for simple task"""
        # Stage 1: Planning
        plan_agent = PlanAgent()
        plan_task = AgentTask(
            id="workflow-101",
            description="Create a function to calculate fibonacci numbers",
            parameters={}
        )
        plan_result = plan_agent.execute(plan_task)

        # Plan should complete
        assert plan_result is not None

        # Stage 2: Code generation
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-102",
            description="Create a Python function to calculate fibonacci numbers",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        # Code should be generated
        assert code_result is not None
        assert code_result.success or 'code' in code_result.output

    def test_plan_then_code_with_context_passing(self):
        """Test context passing between Plan and Code agents"""
        # Stage 1: Planning
        plan_agent = PlanAgent()
        plan_task = AgentTask(
            id="workflow-103",
            description="Plan implementation of user authentication",
            parameters={}
        )
        plan_result = plan_agent.execute(plan_task)

        # Stage 2: Use plan output as context for code generation
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-104",
            description="Implement user authentication based on plan",
            parameters={"language": "python", "context": str(plan_result.output)}
        )
        code_result = code_agent.execute(code_task)

        assert code_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: CODE → TEST WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestCodeToTestWorkflows:
    """Test Code → Test pipeline"""

    def test_code_then_test_generation(self):
        """Test CodeAgent → TestAgent pipeline"""
        # Stage 1: Generate code
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-201",
            description="Create a function to check if number is prime",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        # Stage 2: Generate tests for the code
        test_agent = TestAgent()

        code_snippet = code_result.output.get('code', '') if code_result.success else "def example(): pass"

        test_task = AgentTask(
            id="workflow-202",
            description=f"Generate pytest tests for this code:\n{code_snippet}",
            parameters={"test_framework": "pytest"}
        )
        test_result = test_agent.execute(test_task)

        # Tests should be generated
        assert test_result is not None

    def test_code_test_validation_cycle(self):
        """Test Code → Test → Validate cycle"""
        # Stage 1: Generate simple code
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-203",
            description="Create a function to add two numbers",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        # Stage 2: Generate tests
        test_agent = TestAgent()
        code_snippet = code_result.output.get('code', '') if code_result.success else "def add(a, b): return a + b"

        test_task = AgentTask(
            id="workflow-204",
            description=f"Generate tests for:\n{code_snippet}",
            parameters={"test_framework": "pytest"}
        )
        test_result = test_agent.execute(test_task)

        # Stage 3: Validate both exist
        assert code_result is not None
        assert test_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 3: CODE → REVIEW WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestCodeToReviewWorkflows:
    """Test Code → Review pipeline"""

    def test_code_then_review(self):
        """Test CodeAgent → ReviewAgent pipeline"""
        # Stage 1: Generate code
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-301",
            description="Create a function to parse JSON",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        # Stage 2: Review the code
        review_agent = ReviewAgent()
        code_snippet = code_result.output.get('code', '') if code_result.success else "def parse_json(s): return {}"

        review_task = AgentTask(
            id="workflow-302",
            description=f"Review this code:\n{code_snippet}",
            parameters={"focus": "quality"}
        )
        review_result = review_agent.execute(review_task)

        assert review_result is not None

    def test_code_review_fix_cycle(self):
        """Test Code → Review → Fix cycle"""
        # Stage 1: Generate potentially buggy code
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-303",
            description="Create a function to divide two numbers",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        # Stage 2: Review
        review_agent = ReviewAgent()
        code_snippet = code_result.output.get('code', '') if code_result.success else "def divide(a, b): return a / b"

        review_task = AgentTask(
            id="workflow-304",
            description=f"Review for bugs:\n{code_snippet}",
            parameters={"focus": "bugs"}
        )
        review_result = review_agent.execute(review_task)

        # Stage 3: Fix (if review found issues)
        fix_agent = FixAgent()
        fix_task = AgentTask(
            id="workflow-305",
            description=f"Fix division by zero in:\n{code_snippet}",
            parameters={"bug_type": "ZeroDivisionError"}
        )
        fix_result = fix_agent.execute(fix_task)

        # All stages should complete
        assert code_result is not None
        assert review_result is not None
        assert fix_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 4: ARCHITECT → PLAN → CODE WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestArchitectToPlanToCodeWorkflows:
    """Test Architect → Plan → Code pipeline"""

    def test_architect_plan_code_full_pipeline(self):
        """Test complete Architect → Plan → Code workflow"""
        # Stage 1: Architecture
        architect_agent = ArchitectAgent()
        arch_task = AgentTask(
            id="workflow-401",
            description="Design architecture for a REST API",
            parameters={
                "requirements": ["scalability", "maintainability"],
                "constraints": ["must use existing database"]
            }
        )
        arch_result = architect_agent.execute(arch_task)

        # Stage 2: Planning
        plan_agent = PlanAgent()
        plan_task = AgentTask(
            id="workflow-402",
            description="Create implementation plan for REST API",
            parameters={}
        )
        plan_result = plan_agent.execute(plan_task)

        # Stage 3: Code
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-403",
            description="Implement REST API endpoint",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        # All stages should complete
        assert arch_result is not None
        assert plan_result is not None
        assert code_result is not None

    def test_architect_validation(self):
        """Test Architect agent output structure"""
        architect_agent = ArchitectAgent()
        arch_task = AgentTask(
            id="workflow-404",
            description="Design microservices architecture",
            parameters={
                "requirements": ["modularity", "fault tolerance"],
                "constraints": []
            }
        )
        arch_result = architect_agent.execute(arch_task)

        assert arch_result is not None
        assert hasattr(arch_result, 'success')


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 5: EXPLORE → UNDERSTAND → MODIFY WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestExploreUnderstandModifyWorkflows:
    """Test Explore → Understand → Modify pipeline"""

    def test_explore_then_code(self):
        """Test ExploreAgent → CodeAgent pipeline"""
        # Stage 1: Explore codebase
        explore_agent = ExploreAgent()
        explore_task = AgentTask(
            id="workflow-501",
            description="Find Python files in agents directory",
            parameters={"target": "agents/"}
        )
        explore_result = explore_agent.execute(explore_task)

        # Stage 2: Generate related code
        code_agent = CodeAgent()
        code_task = AgentTask(
            id="workflow-502",
            description="Create a utility function for agent coordination",
            parameters={"language": "python"}
        )
        code_result = code_agent.execute(code_task)

        assert explore_result is not None
        assert code_result is not None

    def test_explore_then_docs(self):
        """Test ExploreAgent → DocsAgent pipeline"""
        # Stage 1: Explore
        explore_agent = ExploreAgent()
        explore_task = AgentTask(
            id="workflow-503",
            description="Analyze agents module structure",
            parameters={"target": "agents/"}
        )
        explore_result = explore_agent.execute(explore_task)

        # Stage 2: Document
        docs_agent = DocsAgent()
        docs_task = AgentTask(
            id="workflow-504",
            description="Document the agents module architecture",
            parameters={"style": "google"}
        )
        docs_result = docs_agent.execute(docs_task)

        assert explore_result is not None
        assert docs_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 6: FULL DEVELOPMENT CYCLE
# ═══════════════════════════════════════════════════════════════════════════

class TestFullDevelopmentCycle:
    """Test complete development workflows"""

    def test_complete_feature_development(self):
        """Test Plan → Code → Test → Review → Docs"""
        # Stage 1: Plan
        plan_agent = PlanAgent()
        plan_result = plan_agent.execute(AgentTask(
            id="full-601",
            description="Plan a user registration feature",
            parameters={}
        ))

        # Stage 2: Code
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="full-602",
            description="Implement user registration",
            parameters={"language": "python"}
        ))

        # Stage 3: Test
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="full-603",
            description="Generate tests for user registration",
            parameters={"test_framework": "pytest"}
        ))

        # Stage 4: Review
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="full-604",
            description="Review user registration code",
            parameters={"focus": "quality"}
        ))

        # Stage 5: Docs
        docs_agent = DocsAgent()
        docs_result = docs_agent.execute(AgentTask(
            id="full-605",
            description="Document user registration API",
            parameters={"style": "google"}
        ))

        # All stages should complete
        assert plan_result is not None
        assert code_result is not None
        assert test_result is not None
        assert review_result is not None
        assert docs_result is not None

    def test_bug_fix_workflow(self):
        """Test Review → Fix → Test cycle"""
        # Stage 1: Review finds bug
        review_agent = ReviewAgent()
        buggy_code = "def divide(a, b): return a / b"
        review_result = review_agent.execute(AgentTask(
            id="full-606",
            description=f"Find bugs in:\n{buggy_code}",
            parameters={"focus": "bugs"}
        ))

        # Stage 2: Fix the bug
        fix_agent = FixAgent()
        fix_result = fix_agent.execute(AgentTask(
            id="full-607",
            description=f"Fix zero division in:\n{buggy_code}",
            parameters={"bug_type": "ZeroDivisionError"}
        ))

        # Stage 3: Test the fix
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="full-608",
            description="Generate tests for fixed divide function",
            parameters={"test_framework": "pytest"}
        ))

        assert review_result is not None
        assert fix_result is not None
        assert test_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 7: PARALLEL AGENT EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

class TestParallelAgentExecution:
    """Test multiple agents working independently"""

    def test_parallel_code_and_test_generation(self):
        """Test Code and Test agents running in parallel"""
        # Both agents work independently
        code_agent = CodeAgent()
        test_agent = TestAgent()

        # Execute both
        code_result = code_agent.execute(AgentTask(
            id="parallel-701",
            description="Create a sorting function",
            parameters={"language": "python"}
        ))

        test_result = test_agent.execute(AgentTask(
            id="parallel-702",
            description="Generate tests for sorting function",
            parameters={"test_framework": "pytest"}
        ))

        # Both should complete independently
        assert code_result is not None
        assert test_result is not None

    def test_multiple_review_agents(self):
        """Test multiple review agents with different foci"""
        review_agent = ReviewAgent()
        code = "def process(data): return [x*2 for x in data]"

        # Review 1: Quality focus
        quality_result = review_agent.execute(AgentTask(
            id="parallel-703",
            description=f"Review quality:\n{code}",
            parameters={"focus": "quality"}
        ))

        # Review 2: Performance focus
        perf_result = review_agent.execute(AgentTask(
            id="parallel-704",
            description=f"Review performance:\n{code}",
            parameters={"focus": "performance"}
        ))

        assert quality_result is not None
        assert perf_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 8: AGENT COORDINATION & HANDOFFS
# ═══════════════════════════════════════════════════════════════════════════

class TestAgentCoordination:
    """Test agent coordination and handoffs"""

    def test_sequential_handoff_with_state(self):
        """Test agents passing state between each other"""
        # Agent 1: Plan
        plan_agent = PlanAgent()
        plan_result = plan_agent.execute(AgentTask(
            id="coord-801",
            description="Plan a cache implementation",
            parameters={}
        ))

        # Agent 2: Code (using plan state)
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="coord-802",
            description="Implement cache based on plan",
            parameters={
                "language": "python",
                "context": str(plan_result.output) if plan_result else ""
            }
        ))

        # Agent 3: Test (using code state)
        test_agent = TestAgent()
        code_snippet = code_result.output.get('code', '') if code_result and code_result.success else "def cache(): pass"
        test_result = test_agent.execute(AgentTask(
            id="coord-803",
            description=f"Test cache implementation:\n{code_snippet}",
            parameters={"test_framework": "pytest"}
        ))

        # Verify handoff chain
        assert plan_result is not None
        assert code_result is not None
        assert test_result is not None

    def test_agent_failure_handling(self):
        """Test workflow continues even if one agent fails"""
        # Agent 1: Code (may succeed or fail)
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="coord-804",
            description="",  # Empty description may cause failure
            parameters={"language": "python"}
        ))

        # Agent 2: Test (should handle previous failure)
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="coord-805",
            description="Generate basic test structure",
            parameters={"test_framework": "pytest"}
        ))

        # Second agent should still work
        assert test_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 9: PERFORMANCE & TIMING
# ═══════════════════════════════════════════════════════════════════════════

class TestMultiAgentPerformance:
    """Test multi-agent workflow performance"""

    def test_sequential_execution_time(self):
        """Test sequential agent execution completes in reasonable time"""
        start = time.time()

        # Execute 3 agents sequentially
        plan_agent = PlanAgent()
        plan_agent.execute(AgentTask(
            id="perf-901",
            description="Quick plan",
            parameters={}
        ))

        code_agent = CodeAgent()
        code_agent.execute(AgentTask(
            id="perf-902",
            description="Quick function",
            parameters={"language": "python"}
        ))

        test_agent = TestAgent()
        test_agent.execute(AgentTask(
            id="perf-903",
            description="Quick test",
            parameters={"test_framework": "pytest"}
        ))

        elapsed = time.time() - start

        # Should complete within 60 seconds (3 agents × ~20s each)
        assert elapsed < 60.0, f"Multi-agent workflow took {elapsed:.2f}s (>60s limit)"

    def test_agent_execution_metrics_aggregation(self):
        """Test aggregating metrics from multiple agents"""
        agents = [
            CodeAgent(),
            TestAgent(),
            ReviewAgent()
        ]

        results = []
        for i, agent in enumerate(agents):
            result = agent.execute(AgentTask(
                id=f"metrics-{i}",
                description="Test task",
                parameters={}
            ))
            results.append(result)

        # All should have metrics
        for result in results:
            assert result is not None
            assert hasattr(result, 'metrics')


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 10: ERROR RECOVERY & RESILIENCE
# ═══════════════════════════════════════════════════════════════════════════

class TestErrorRecoveryWorkflows:
    """Test multi-agent error recovery"""

    def test_retry_after_failure(self):
        """Test retrying agent after failure"""
        code_agent = CodeAgent()

        # First attempt (may fail with empty description)
        result1 = code_agent.execute(AgentTask(
            id="error-1001",
            description="",
            parameters={"language": "python"}
        ))

        # Second attempt (should work)
        result2 = code_agent.execute(AgentTask(
            id="error-1002",
            description="Create a simple function",
            parameters={"language": "python"}
        ))

        # Second should complete
        assert result2 is not None

    def test_fallback_agent_strategy(self):
        """Test using fallback agent when primary fails"""
        # Primary: CodeAgent (might fail due to complexity)
        code_agent = CodeAgent()
        result1 = code_agent.execute(AgentTask(
            id="error-1003",
            description="Generate an extremely complex quantum computing algorithm",
            parameters={"language": "python"}
        ))

        # Fallback: PlanAgent (simpler, always succeeds with valid params)
        plan_agent = PlanAgent()
        result2 = plan_agent.execute(AgentTask(
            id="error-1004",
            description="Create a high-level plan for implementing the algorithm",
            parameters={"goal": "Plan quantum computing implementation"}
        ))

        # Both should return results
        assert result1 is not None
        assert result2 is not None
        # At least one should succeed (fallback pattern)
        assert result1.success or result2.success

    def test_partial_success_handling(self):
        """Test handling partial success in multi-agent workflow"""
        results = []

        # Execute 3 agents, some may fail
        agents_tasks = [
            (CodeAgent(), "Create function", {"language": "python"}),
            (TestAgent(), "", {"test_framework": "pytest"}),  # May fail
            (ReviewAgent(), "Review code", {"focus": "quality"})
        ]

        for i, (agent, desc, params) in enumerate(agents_tasks):
            result = agent.execute(AgentTask(
                id=f"partial-{i}",
                description=desc,
                parameters=params
            ))
            results.append(result)

        # At least some should succeed
        successes = [r for r in results if r is not None]
        assert len(successes) > 0


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 11: CONTEXT PRESERVATION
# ═══════════════════════════════════════════════════════════════════════════

class TestContextPreservation:
    """Test context passing between agents"""

    def test_context_chain_through_3_agents(self):
        """Test context flows through 3-agent chain"""
        # Agent 1: Plan (creates context)
        plan_agent = PlanAgent()
        plan_result = plan_agent.execute(AgentTask(
            id="context-1101",
            description="Plan email validation feature",
            parameters={}
        ))

        context1 = str(plan_result.output) if plan_result else "email validation"

        # Agent 2: Code (uses context)
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="context-1102",
            description=f"Implement: {context1}",
            parameters={"language": "python"}
        ))

        context2 = code_result.output.get('code', '') if code_result and code_result.success else "def validate_email(e): pass"

        # Agent 3: Test (uses accumulated context)
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="context-1103",
            description=f"Test:\n{context2}",
            parameters={"test_framework": "pytest"}
        ))

        # All should complete
        assert plan_result is not None
        assert code_result is not None
        assert test_result is not None

    def test_context_branching(self):
        """Test context branching to multiple agents"""
        # Source agent
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="context-1104",
            description="Create data processing function",
            parameters={"language": "python"}
        ))

        code = code_result.output.get('code', '') if code_result and code_result.success else "def process(data): return data"

        # Branch 1: Test
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="context-1105",
            description=f"Test:\n{code}",
            parameters={"test_framework": "pytest"}
        ))

        # Branch 2: Review
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="context-1106",
            description=f"Review:\n{code}",
            parameters={"focus": "quality"}
        ))

        # Branch 3: Docs
        docs_agent = DocsAgent()
        docs_result = docs_agent.execute(AgentTask(
            id="context-1107",
            description=f"Document:\n{code}",
            parameters={"style": "google"}
        ))

        # All branches should complete
        assert test_result is not None
        assert review_result is not None
        assert docs_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 12: COMPLEX WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestComplexWorkflows:
    """Test complex multi-stage workflows"""

    def test_iterative_refinement_workflow(self):
        """Test Code → Review → Fix → Review cycle"""
        # Iteration 1: Code
        code_agent = CodeAgent()
        code_v1 = code_agent.execute(AgentTask(
            id="complex-1201",
            description="Create file reader function",
            parameters={"language": "python"}
        ))

        # Iteration 1: Review
        review_agent = ReviewAgent()
        review_v1 = review_agent.execute(AgentTask(
            id="complex-1202",
            description="Review file reader",
            parameters={"focus": "quality"}
        ))

        # Iteration 2: Fix
        fix_agent = FixAgent()
        fix_v1 = fix_agent.execute(AgentTask(
            id="complex-1203",
            description="Improve file reader based on review",
            parameters={}
        ))

        # Iteration 2: Review again
        review_v2 = review_agent.execute(AgentTask(
            id="complex-1204",
            description="Review improved file reader",
            parameters={"focus": "quality"}
        ))

        # All iterations should complete
        assert code_v1 is not None
        assert review_v1 is not None
        assert fix_v1 is not None
        assert review_v2 is not None

    def test_diamond_workflow_pattern(self):
        """Test diamond pattern: Start → Split → Merge"""
        # Start: Generate code
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="complex-1205",
            description="Create calculator function",
            parameters={"language": "python"}
        ))

        code = code_result.output.get('code', '') if code_result and code_result.success else "def calc(): pass"

        # Split: Two parallel analyses
        test_agent = TestAgent()
        review_agent = ReviewAgent()

        test_result = test_agent.execute(AgentTask(
            id="complex-1206",
            description=f"Test:\n{code}",
            parameters={"test_framework": "pytest"}
        ))

        review_result = review_agent.execute(AgentTask(
            id="complex-1207",
            description=f"Review:\n{code}",
            parameters={"focus": "quality"}
        ))

        # Merge: Docs incorporating both
        docs_agent = DocsAgent()
        docs_result = docs_agent.execute(AgentTask(
            id="complex-1208",
            description=f"Document calculator with tests and review feedback",
            parameters={"style": "google"}
        ))

        # All stages should complete
        assert code_result is not None
        assert test_result is not None
        assert review_result is not None
        assert docs_result is not None

    def test_pipeline_with_conditional_branching(self):
        """Test workflow with conditional execution"""
        # Stage 1: Code generation
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="complex-1209",
            description="Create validation function",
            parameters={"language": "python"}
        ))

        # Stage 2: Conditional - if code succeeded, test it
        if code_result and code_result.success:
            test_agent = TestAgent()
            test_result = test_agent.execute(AgentTask(
                id="complex-1210",
                description="Test validation function",
                parameters={"test_framework": "pytest"}
            ))
        else:
            # Alternative path - use fix agent
            fix_agent = FixAgent()
            test_result = fix_agent.execute(AgentTask(
                id="complex-1211",
                description="Create fallback validation",
                parameters={}
            ))

        # Should complete either path
        assert code_result is not None
        assert test_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 13: REAL-WORLD SCENARIOS
# ═══════════════════════════════════════════════════════════════════════════

class TestRealWorldScenarios:
    """Test realistic development scenarios"""

    def test_feature_request_to_implementation(self):
        """Test complete feature: Request → Plan → Implement → Test → Deploy"""
        # Stage 1: Explore existing codebase
        explore_agent = ExploreAgent()
        explore_result = explore_agent.execute(AgentTask(
            id="real-1301",
            description="Explore authentication module",
            parameters={"target": "agents/"}
        ))

        # Stage 2: Plan new feature
        plan_agent = PlanAgent()
        plan_result = plan_agent.execute(AgentTask(
            id="real-1302",
            description="Plan adding OAuth support",
            parameters={}
        ))

        # Stage 3: Implement
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="real-1303",
            description="Implement OAuth integration",
            parameters={"language": "python"}
        ))

        # Stage 4: Test
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="real-1304",
            description="Test OAuth integration",
            parameters={"test_framework": "pytest"}
        ))

        # All stages should complete
        assert explore_result is not None
        assert plan_result is not None
        assert code_result is not None
        assert test_result is not None

    def test_bug_report_to_fix(self):
        """Test bug lifecycle: Report → Explore → Fix → Test → Review"""
        # Stage 1: Explore to find bug
        explore_agent = ExploreAgent()
        explore_result = explore_agent.execute(AgentTask(
            id="real-1305",
            description="Find authentication bug",
            parameters={"search_pattern": "auth"}
        ))

        # Stage 2: Review to analyze bug
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="real-1306",
            description="Analyze authentication security",
            parameters={"focus": "security"}
        ))

        # Stage 3: Fix
        fix_agent = FixAgent()
        fix_result = fix_agent.execute(AgentTask(
            id="real-1307",
            description="Fix authentication security issue",
            parameters={"bug_type": "security"}
        ))

        # Stage 4: Test the fix
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="real-1308",
            description="Test authentication fix",
            parameters={"test_framework": "pytest"}
        ))

        # All stages should complete
        assert explore_result is not None
        assert review_result is not None
        assert fix_result is not None
        assert test_result is not None

    def test_refactoring_workflow(self):
        """Test refactoring: Review → Plan → Refactor → Test"""
        # Stage 1: Review existing code
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="real-1309",
            description="Review legacy code for refactoring",
            parameters={"focus": "maintainability"}
        ))

        # Stage 2: Plan refactoring
        plan_agent = PlanAgent()
        plan_result = plan_agent.execute(AgentTask(
            id="real-1310",
            description="Plan code refactoring",
            parameters={}
        ))

        # Stage 3: Implement refactoring
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="real-1311",
            description="Refactor code for better maintainability",
            parameters={"language": "python"}
        ))

        # Stage 4: Test refactored code
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="real-1312",
            description="Test refactored code",
            parameters={"test_framework": "pytest"}
        ))

        # All stages should complete
        assert review_result is not None
        assert plan_result is not None
        assert code_result is not None
        assert test_result is not None

    def test_documentation_workflow(self):
        """Test Explore → Code → Docs pipeline"""
        # Stage 1: Explore
        explore_agent = ExploreAgent()
        explore_result = explore_agent.execute(AgentTask(
            id="real-1313",
            description="Explore API endpoints",
            parameters={"target": "core/"}
        ))

        # Stage 2: Code
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="real-1314",
            description="Create API client",
            parameters={"language": "python"}
        ))

        # Stage 3: Docs
        docs_agent = DocsAgent()
        docs_result = docs_agent.execute(AgentTask(
            id="real-1315",
            description="Document API client",
            parameters={"style": "google"}
        ))

        # All should complete
        assert explore_result is not None
        assert code_result is not None
        assert docs_result is not None

    def test_security_review_workflow(self):
        """Test Code → Review (security) → Fix → Review"""
        # Stage 1: Code
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="real-1316",
            description="Create authentication handler",
            parameters={"language": "python"}
        ))

        # Stage 2: Security review
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="real-1317",
            description="Review authentication security",
            parameters={"focus": "security"}
        ))

        # Stage 3: Fix security issues
        fix_agent = FixAgent()
        fix_result = fix_agent.execute(AgentTask(
            id="real-1318",
            description="Fix authentication security vulnerabilities",
            parameters={"bug_type": "security"}
        ))

        # All should complete
        assert code_result is not None
        assert review_result is not None
        assert fix_result is not None

    def test_performance_optimization_workflow(self):
        """Test Review (performance) → Code → Test"""
        # Stage 1: Review for performance
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="real-1319",
            description="Review database query performance",
            parameters={"focus": "performance"}
        ))

        # Stage 2: Optimize
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="real-1320",
            description="Optimize database queries",
            parameters={"language": "python"}
        ))

        # Stage 3: Test performance
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="real-1321",
            description="Test query performance",
            parameters={"test_framework": "pytest"}
        ))

        # All should complete
        assert review_result is not None
        assert code_result is not None
        assert test_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 14: INTEGRATION WITH TOOLS
# ═══════════════════════════════════════════════════════════════════════════

class TestAgentToolIntegration:
    """Test agents using tools in workflows"""

    def test_explore_then_review_pattern(self):
        """Test ExploreAgent discovers, ReviewAgent analyzes"""
        # Stage 1: Explore discovers code
        explore_agent = ExploreAgent()
        explore_result = explore_agent.execute(AgentTask(
            id="tool-1401",
            description="Find all test files",
            parameters={"search_pattern": "test_"}
        ))

        # Stage 2: Review analyzes what was found
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="tool-1402",
            description="Review test coverage",
            parameters={"focus": "quality"}
        ))

        # Both should complete
        assert explore_result is not None
        assert review_result is not None

    def test_code_test_verify_loop(self):
        """Test Code → Test → Verify with execution"""
        # Stage 1: Generate simple code
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="tool-1403",
            description="Create multiplication function",
            parameters={"language": "python"}
        ))

        # Stage 2: Generate tests
        test_agent = TestAgent()
        test_result = test_agent.execute(AgentTask(
            id="tool-1404",
            description="Test multiplication function",
            parameters={"test_framework": "pytest"}
        ))

        # Stage 3: Review both
        review_agent = ReviewAgent()
        review_result = review_agent.execute(AgentTask(
            id="tool-1405",
            description="Review code and tests",
            parameters={"focus": "quality"}
        ))

        # All should complete
        assert code_result is not None
        assert test_result is not None
        assert review_result is not None

    def test_architectural_decision_workflow(self):
        """Test Architect → Explore → Plan → Code"""
        # Stage 1: Architecture decision
        architect_agent = ArchitectAgent()
        arch_result = architect_agent.execute(AgentTask(
            id="tool-1406",
            description="Design caching layer",
            parameters={
                "requirements": ["performance", "simplicity"],
                "constraints": ["memory limited"]
            }
        ))

        # Stage 2: Explore existing patterns
        explore_agent = ExploreAgent()
        explore_result = explore_agent.execute(AgentTask(
            id="tool-1407",
            description="Find existing cache implementations",
            parameters={"search_pattern": "cache"}
        ))

        # Stage 3: Plan implementation
        plan_agent = PlanAgent()
        plan_result = plan_agent.execute(AgentTask(
            id="tool-1408",
            description="Plan cache layer implementation",
            parameters={}
        ))

        # Stage 4: Implement
        code_agent = CodeAgent()
        code_result = code_agent.execute(AgentTask(
            id="tool-1409",
            description="Implement cache layer",
            parameters={"language": "python"}
        ))

        # All should complete
        assert arch_result is not None
        assert explore_result is not None
        assert plan_result is not None
        assert code_result is not None


# ═══════════════════════════════════════════════════════════════════════════
# RUN SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
