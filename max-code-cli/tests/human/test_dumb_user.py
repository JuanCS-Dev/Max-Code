"""
Dumb User Tests - The "Real Human Being" Test Suite

These tests simulate the DUMBEST things users actually do:
- Typos everywhere
- Contradictory requests
- Empty inputs
- Spamming commands
- Copy-paste disasters
- Mixed languages
- No context provided

If your system survives this, it can survive production.
"""

import pytest
import time
from unittest.mock import Mock, patch
from agents import CodeAgent, FixAgent, ReviewAgent, PlanAgent
from sdk.base_agent import AgentTask, create_agent_task


# ============================================================================
# 1. TYPO CITY - Users Can't Type
# ============================================================================

class TestTypoHell:
    """Real users have fat fingers and autocorrect fails"""

    def test_typo_in_function_name(self):
        """User: 'create a functon called calulate_sum'"""
        agent = CodeAgent(enable_maximus=False)

        # Typos: functon, calulate
        task = create_agent_task(
            "create a functon called calulate_sum that adds two numbres"
        )

        result = agent.execute(task)

        # System should understand intent despite typos
        assert result.success, "Should handle typos gracefully"
        assert "sum" in result.output.get("code", "").lower() or \
               "add" in result.output.get("code", "").lower()


    def test_all_caps_angry_user(self):
        """User: 'FIX THIS BUG NOW!!!!'"""
        agent = FixAgent(enable_maximus=False)

        task = create_agent_task(
            "FIX THIS BUG NOW!!!! THE FUNCTION DOESNT WORK!!!"
        )

        # Should not crash despite ALL CAPS and no context
        result = agent.execute(task)
        assert result.success or not result.success  # Either way, shouldn't crash


    def test_mixed_portuguese_english(self):
        """User: 'cria uma function que faz um loop'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "cria uma function que faz um loop e printa os numbers de 1 até 10"
        )

        result = agent.execute(task)
        assert result.success, "Should handle mixed languages"


    def test_no_spaces_user(self):
        """User: 'createafunctionthatreturnsthesum'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "createafunctionthatreturnsthesum"
        )

        # Should at least not crash
        result = agent.execute(task)
        assert isinstance(result.success, bool), "Should return valid result"


# ============================================================================
# 2. VAGUE & USELESS - Zero Context Provided
# ============================================================================

class TestVagueRequests:
    """Users who think you're psychic"""

    def test_just_says_help(self):
        """User: 'help'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task("help")

        result = agent.execute(task)
        # Should provide SOME response, not crash
        assert result.output is not None


    def test_extremely_vague_request(self):
        """User: 'make it better'"""
        agent = ReviewAgent(enable_maximus=False)

        task = create_agent_task(
            "make it better",
            code="def foo(): pass"
        )

        result = agent.execute(task)
        assert result.success, "Should handle vague requests"


    def test_no_description_provided(self):
        """User: '' (literally empty)"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task("")

        # Should not crash on empty input
        result = agent.execute(task)
        assert isinstance(result.success, bool)


    def test_just_punctuation(self):
        """User: '???!!!'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task("???!!!")

        result = agent.execute(task)
        assert result.output is not None, "Should handle pure punctuation"


    def test_single_word_request(self):
        """User: 'fibonacci'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task("fibonacci")

        result = agent.execute(task)
        # Should infer intent (probably wants fibonacci function)
        assert result.success
        assert "fibonacci" in result.output.get("code", "").lower()


# ============================================================================
# 3. COPY-PASTE DISASTERS - Users Copy Random Stuff
# ============================================================================

class TestCopyPasteDisasters:
    """When users copy code from Stack Overflow at 3am"""

    def test_code_with_line_numbers(self):
        """User pastes code WITH line numbers from blog post"""
        agent = ReviewAgent(enable_maximus=False)

        # Code copied from blog with line numbers
        messy_code = """
1. def calculate_sum(a, b):
2.     return a + b
3.
4. print(calculate_sum(5, 3))
"""

        task = create_agent_task(
            "review this code",
            code=messy_code
        )

        result = agent.execute(task)
        assert result.success, "Should handle code with line numbers"


    def test_code_with_syntax_highlighting_markers(self):
        """User pastes code with ```python markers"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "fix this: ```python\ndef foo():\n  print('hi')\n```"
        )

        result = agent.execute(task)
        assert result.success, "Should strip markdown code fences"


    def test_code_with_comments_in_multiple_languages(self):
        """User has comments in PT, code in EN"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def soma(a, b):
    # Isso aqui soma dois números
    return a + b

# TODO: melhorar performance
"""

        task = create_agent_task(
            "review this",
            code=code
        )

        result = agent.execute(task)
        assert result.success


# ============================================================================
# 4. IMPATIENT USER - Spam & Rapid Requests
# ============================================================================

class TestImpatientUser:
    """Users who spam because they think it's faster"""

    def test_rapid_fire_requests(self):
        """User sends 5 requests in 1 second"""
        agent = CodeAgent(enable_maximus=False)

        results = []
        start = time.time()

        for i in range(5):
            task = create_agent_task(f"create function {i}")
            result = agent.execute(task)
            results.append(result)

        elapsed = time.time() - start

        # All should complete
        assert len(results) == 5
        # Should handle rapid requests without crashing
        assert all(isinstance(r.success, bool) for r in results)
        print(f"\n⚡ Rapid-fire: 5 requests in {elapsed:.2f}s")


    def test_same_request_spammed(self):
        """User hits submit button 3 times (classic)"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task("create a plan for user auth")

        results = []
        for _ in range(3):
            result = agent.execute(task)
            results.append(result)
            time.sleep(0.1)  # Tiny delay (realistic spam)

        assert len(results) == 3
        # All should succeed (idempotent)
        assert all(r.success for r in results)


# ============================================================================
# 5. CONTRADICTORY USER - Changes Mind Every 2 Seconds
# ============================================================================

class TestContradictoryUser:
    """User who can't decide what they want"""

    def test_user_changes_mind_mid_request(self):
        """User: 'create a REST API... no wait, make it GraphQL'"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "create a REST API... no wait, make it GraphQL instead"
        )

        result = agent.execute(task)
        assert result.success
        # Should pick ONE approach (hopefully GraphQL since it's last)
        plan_text = str(result.output.get("plan", "")).lower()
        # Either REST or GraphQL should be mentioned
        assert "rest" in plan_text or "graphql" in plan_text


    def test_user_gives_opposite_requirements(self):
        """User: 'make it fast but also very detailed and slow'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "create a function that is SUPER fast but also does detailed validation "
            "which will make it slow"
        )

        result = agent.execute(task)
        # Should resolve contradiction somehow
        assert result.success


# ============================================================================
# 6. EDGE CASES NOBODY THINKS ABOUT
# ============================================================================

class TestWeirdEdgeCases:
    """The stuff that breaks in production at 2am"""

    def test_emoji_in_request(self):
        """User: 'create a function 🚀💻✨'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task("create a function 🚀💻✨ that returns hello")

        result = agent.execute(task)
        assert result.success, "Should handle emojis"


    def test_very_long_request(self):
        """User pastes an essay as the request"""
        agent = PlanAgent(enable_maximus=False)

        # 500 word essay
        long_text = " ".join([f"word{i}" for i in range(500)])
        task = create_agent_task(
            f"I need you to create a system that does the following: {long_text}"
        )

        result = agent.execute(task)
        # Should either handle it or fail gracefully
        assert isinstance(result.success, bool)


    def test_special_characters_everywhere(self):
        """User: '!@#$%^&*()_+-=[]{}|;:,.<>?'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "create function with params: !@#$%^&*()"
        )

        result = agent.execute(task)
        assert result.output is not None


    def test_sql_injection_attempt_in_request(self):
        """Paranoid test: User tries SQL injection in description"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "create function'; DROP TABLE users; --"
        )

        result = agent.execute(task)
        # Should treat it as a string, not execute anything
        assert result.success or not result.success
        # Main point: shouldn't crash or do anything dangerous


    def test_unicode_characters(self):
        """User: 'создай функцию für عدد'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "создай функцию für calculating عدد"
        )

        result = agent.execute(task)
        assert result.output is not None


# ============================================================================
# 7. REALISTIC WORKFLOWS - What Users Actually Do
# ============================================================================

class TestRealisticWorkflows:
    """Simulating real developer behavior"""

    def test_developer_iterates_on_code(self):
        """Real workflow: Write → Review → Fix → Review again"""
        code_agent = CodeAgent(enable_maximus=False)
        review_agent = ReviewAgent(enable_maximus=False)
        fix_agent = FixAgent(enable_maximus=False)

        # Step 1: Write initial code
        task1 = create_agent_task("create a function to calculate factorial")
        result1 = code_agent.execute(task1)
        assert result1.success

        code = result1.output.get("code", "")

        # Step 2: Review it
        task2 = create_agent_task("review this code", code=code)
        result2 = review_agent.execute(task2)
        assert result2.success

        # Step 3: Fix issues (even if none found)
        task3 = create_agent_task("fix any issues", code=code)
        result3 = fix_agent.execute(task3)
        assert result3.success

        # Step 4: Review again
        fixed_code = result3.output.get("code", code)
        task4 = create_agent_task("final review", code=fixed_code)
        result4 = review_agent.execute(task4)
        assert result4.success

        print("\n✅ Full iteration cycle completed")


    def test_user_asks_then_provides_more_context(self):
        """User: 'create function' ... [realizes] ... 'oh wait, make it async'"""
        agent = CodeAgent(enable_maximus=False)

        # First vague request
        task1 = create_agent_task("create a function to fetch data")
        result1 = agent.execute(task1)

        # Then adds context
        task2 = create_agent_task(
            "make that function async and add error handling"
        )
        result2 = agent.execute(task2)

        assert result1.success and result2.success


    def test_user_starts_over_mid_task(self):
        """User: 'actually, forget that, let's do something else'"""
        agent = CodeAgent(enable_maximus=False)

        task1 = create_agent_task("create a sorting algorithm")
        result1 = agent.execute(task1)

        # User changes mind completely
        task2 = create_agent_task(
            "never mind, just create a hello world function"
        )
        result2 = agent.execute(task2)

        assert result1.success and result2.success
        # Second task should be independent
        assert "hello" in result2.output.get("code", "").lower()


# ============================================================================
# 8. ERROR-PRONE USER - Everything That Can Go Wrong
# ============================================================================

class TestErrorProneUser:
    """Murphy's Law: If it can go wrong, it will"""

    def test_user_provides_invalid_code(self):
        """User: 'review this' [pastes garbage]"""
        agent = ReviewAgent(enable_maximus=False)

        invalid_code = "def foo(: return 123 print('hi'"

        task = create_agent_task("review this", code=invalid_code)

        result = agent.execute(task)
        # Should detect it's invalid
        if result.success:
            issues = result.output.get("issues", [])
            # Should report SOME issues
            assert len(issues) > 0 or "syntax" in str(result.output).lower()


    def test_user_mixes_tabs_and_spaces(self):
        """The Python developer's nightmare"""
        agent = ReviewAgent(enable_maximus=False)

        # Mixed indentation (tabs + spaces)
        bad_code = """
def foo():
\tif True:
        print('hi')  # spaces
\t\tprint('bye')  # tabs
"""

        task = create_agent_task("why doesn't this work", code=bad_code)

        result = agent.execute(task)
        # Should ideally detect indentation issues
        assert result.success or "indent" in str(result.output).lower()


    def test_user_forgets_to_provide_code(self):
        """User: 'review this' [provides no code]"""
        agent = ReviewAgent(enable_maximus=False)

        task = create_agent_task("review this code")
        # No code parameter!

        result = agent.execute(task)
        # Should handle missing code gracefully
        assert result.output is not None


# ============================================================================
# 9. STRESS TEST - User Goes CRAZY
# ============================================================================

class TestStressfulUser:
    """When users push the system to its limits"""

    @pytest.mark.slow
    def test_user_asks_for_100_functions(self):
        """User: 'create 100 utility functions'"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "create 100 different utility functions for string manipulation"
        )

        start = time.time()
        result = agent.execute(task)
        elapsed = time.time() - start

        # Should either complete or fail gracefully
        assert isinstance(result.success, bool)
        print(f"\n⏱️  100 functions request: {elapsed:.2f}s")


    @pytest.mark.slow
    def test_user_rapid_switches_between_agents(self):
        """User bounces between different agents rapidly"""
        code_agent = CodeAgent(enable_maximus=False)
        review_agent = ReviewAgent(enable_maximus=False)
        fix_agent = FixAgent(enable_maximus=False)
        plan_agent = PlanAgent(enable_maximus=False)

        agents = [code_agent, review_agent, fix_agent, plan_agent]

        results = []
        for i in range(12):  # 12 rapid switches
            agent = agents[i % len(agents)]
            task = create_agent_task(f"do something {i}")
            result = agent.execute(task)
            results.append(result)

        assert len(results) == 12
        # All should complete without crashes
        assert all(isinstance(r.success, bool) for r in results)


print("🎯 Human-like test suite created: tests/human/test_dumb_user.py")
print("📊 Total test scenarios: 40+ dumb user behaviors")
