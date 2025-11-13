"""
Conversation Flow Tests - Multi-Turn Interactions

Real users don't send one perfect request. They have back-and-forth conversations,
change their mind, provide incomplete info, and gradually converge on a solution.

Categories:
1. Incremental Refinement (user adds details over multiple turns)
2. Scope Creep (requirements grow during conversation)
3. Context Switching (jumping between different topics)
4. Debugging Sessions (iterative problem-solving)
5. Learning Conversations (user asking questions while building)
"""

import pytest
from sdk.base_agent import create_agent_task
from agents.plan_agent import PlanAgent
from agents.review_agent import ReviewAgent
from agents.fix_agent import FixAgent
from agents.code_agent import CodeAgent


# ============================================================================
# 1. INCREMENTAL REFINEMENT
# ============================================================================

class TestIncrementalRefinement:
    """User starts vague, gradually adds constraints"""

    def test_progressive_detail_addition(self):
        """User adds more details each turn"""
        agent = PlanAgent(enable_maximus=False)

        # Turn 1: Super vague
        task1 = create_agent_task("need an API")
        result1 = agent.execute(task1)
        assert result1.success

        # Turn 2: Add more context
        task2 = create_agent_task(
            "need an API... for users... to upload files"
        )
        result2 = agent.execute(task2)
        assert result2.success

        # Turn 3: Add constraints
        task3 = create_agent_task(
            "need an API for users to upload files... "
            "max 10MB... only images... with virus scanning"
        )
        result3 = agent.execute(task3)
        assert result3.success
        # Each iteration should build on previous

    def test_clarification_cycle(self):
        """User responds to clarifying questions"""
        agent = CodeAgent(enable_maximus=False)

        # Turn 1: Ambiguous
        task1 = create_agent_task("create a cache")
        result1 = agent.execute(task1)
        assert result1.success

        # Turn 2: Clarify (as if agent asked about TTL)
        task2 = create_agent_task(
            "create a cache... ttl should be 1 hour"
        )
        result2 = agent.execute(task2)
        assert result2.success

        # Turn 3: More clarification (as if asked about storage)
        task3 = create_agent_task(
            "create a cache with 1 hour ttl... use Redis"
        )
        result3 = agent.execute(task3)
        assert result3.success


# ============================================================================
# 2. SCOPE CREEP
# ============================================================================

class TestScopeCreep:
    """Requirements grow during conversation"""

    def test_feature_creep_explosion(self):
        """Classic scope creep"""
        agent = PlanAgent(enable_maximus=False)

        # Start simple
        task1 = create_agent_task("create login function")
        result1 = agent.execute(task1)
        assert result1.success

        # Add OAuth
        task2 = create_agent_task(
            "create login function... "
            "oh and support Google OAuth too"
        )
        result2 = agent.execute(task2)
        assert result2.success

        # Add MFA
        task3 = create_agent_task(
            "create login function with Google OAuth... "
            "and 2FA... and biometric... and magic links... "
            "and remember me... and session management"
        )
        result3 = agent.execute(task3)
        assert result3.success
        # Should handle exploding scope

    def test_performance_requirements_added_later(self):
        """User adds performance constraints after initial design"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "create user search... "
            "oh wait it needs to search 10 million users... "
            "in under 100ms... "
            "with fuzzy matching... "
            "and autocomplete"
        )

        result = agent.execute(task)
        assert result.success
        # Should recognize need for indexing/caching


# ============================================================================
# 3. CONTEXT SWITCHING
# ============================================================================

class TestContextSwitching:
    """User jumps between different problems"""

    def test_mid_conversation_topic_change(self):
        """User completely changes topic mid-flow"""
        plan_agent = PlanAgent(enable_maximus=False)
        review_agent = ReviewAgent(enable_maximus=False)

        # Working on API
        task1 = create_agent_task("plan REST API for blog")
        result1 = plan_agent.execute(task1)
        assert result1.success

        # Suddenly: database question
        task2 = create_agent_task(
            "wait, should I use postgres or mongo for this"
        )
        result2 = plan_agent.execute(task2)
        assert result2.success

        # Back to API, but different endpoint
        task3 = create_agent_task(
            "ok back to the API... review this auth code",
            code="def login(): pass"
        )
        result3 = review_agent.execute(task3)
        assert result3.success

    def test_interrupt_with_urgent_bug(self):
        """User interrupts planning with urgent bug"""
        plan_agent = PlanAgent(enable_maximus=False)
        fix_agent = FixAgent(enable_maximus=False)

        # Planning new feature
        task1 = create_agent_task("plan email notification system")
        result1 = plan_agent.execute(task1)
        assert result1.success

        # INTERRUPT: Production bug!
        task2 = create_agent_task(
            "WAIT stop everything, production is down, fix this NOW",
            error="Database connection refused"
        )
        result2 = fix_agent.execute(task2)
        assert result2.success

        # Might come back to planning later
        # (or might not - that's life)


# ============================================================================
# 4. DEBUGGING SESSIONS
# ============================================================================

class TestDebuggingSession:
    """Iterative debugging like real developers"""

    def test_progressive_bug_isolation(self):
        """User narrows down bug over multiple attempts"""
        agent = FixAgent(enable_maximus=False)

        # Attempt 1: Vague error
        task1 = create_agent_task(
            "something's wrong with my code",
            error="TypeError"
        )
        result1 = agent.execute(task1)
        assert result1.success

        # Attempt 2: More context
        task2 = create_agent_task(
            "TypeError when processing user data... "
            "specifically when user.age is None",
            error="TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'"
        )
        result2 = agent.execute(task2)
        assert result2.success

        # Attempt 3: Provides code
        task3 = create_agent_task(
            "TypeError with None age values",
            code="total = sum([user.age for user in users])",
            error="TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'"
        )
        result3 = agent.execute(task3)
        assert result3.success

    def test_tried_fixes_didnt_work(self):
        """User reports what they already tried"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
def process():
    # Tried: wrapping in try/except - didn't help
    # Tried: adding sleep(1) - didn't help
    # Tried: restarting server - didn't help
    # Tried: clearing cache - didn't help
    data = fetch_data()
    return data.value  # Still crashes here
"""

        task = create_agent_task(
            "none of my fixes worked, what am i missing",
            code=broken_code,
            error="AttributeError: 'NoneType' object has no attribute 'value'"
        )

        result = agent.execute(task)
        assert result.success
        # Should recognize: fetch_data() returning None


# ============================================================================
# 5. LEARNING CONVERSATIONS
# ============================================================================

class TestLearningConversations:
    """User learns while building"""

    def test_why_questions_during_implementation(self):
        """User asks 'why' after each step"""
        agent = CodeAgent(enable_maximus=False)

        # Implement something
        task1 = create_agent_task("create async function to fetch data")
        result1 = agent.execute(task1)
        assert result1.success

        # Ask why
        task2 = create_agent_task(
            "why did you use async instead of regular function"
        )
        result2 = agent.execute(task2)
        assert result2.success

        # Ask about specific keyword
        task3 = create_agent_task(
            "what does 'await' actually do"
        )
        result3 = agent.execute(task3)
        assert result3.success

    def test_comparison_questions(self):
        """User wants to understand trade-offs"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "should i use REST or GraphQL... "
            "what's the difference... "
            "which is easier for beginners... "
            "which is better for mobile apps"
        )

        result = agent.execute(task)
        assert result.success
        # Should provide educational comparison


# ============================================================================
# 6. EMOTIONAL STATE CHANGES
# ============================================================================

class TestEmotionalStates:
    """User's emotional state affects communication"""

    def test_frustration_progression(self):
        """User gets increasingly frustrated"""
        agent = FixAgent(enable_maximus=False)

        # Attempt 1: Calm
        task1 = create_agent_task(
            "this doesn't work",
            error="AttributeError"
        )
        result1 = agent.execute(task1)
        assert result1.success

        # Attempt 2: Frustrated
        task2 = create_agent_task(
            "still doesn't work!!!",
            error="AttributeError"
        )
        result2 = agent.execute(task2)
        assert result2.success

        # Attempt 3: Rage
        task3 = create_agent_task(
            "WHY DOESN'T THIS WORK I'VE BEEN AT THIS FOR 4 HOURS",
            error="AttributeError"
        )
        result3 = agent.execute(task3)
        assert result3.success
        # Should remain calm and helpful

    def test_excitement_to_reality_check(self):
        """User excited about idea, then realizes complexity"""
        agent = PlanAgent(enable_maximus=False)

        # Excited
        task1 = create_agent_task(
            "I HAVE THE BEST IDEA! AI-powered real-time collaborative "
            "video editing with blockchain and AR!!!"
        )
        result1 = agent.execute(task1)
        assert result1.success

        # Reality check
        task2 = create_agent_task(
            "ok maybe that's too complex... "
            "let's just start with basic video upload"
        )
        result2 = agent.execute(task2)
        assert result2.success


# ============================================================================
# 7. PARTIAL INFORMATION FLOW
# ============================================================================

class TestPartialInformation:
    """User provides info in pieces"""

    def test_code_provided_in_chunks(self):
        """User sends code across multiple messages"""
        agent = ReviewAgent(enable_maximus=False)

        # Chunk 1
        task1 = create_agent_task(
            "review this",
            code="def process(data):"
        )
        result1 = agent.execute(task1)
        assert result1.success

        # Chunk 2: More complete
        task2 = create_agent_task(
            "review this",
            code="""
def process(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""
        )
        result2 = agent.execute(task2)
        assert result2.success

    def test_error_message_comes_later(self):
        """User provides code first, error message later"""
        agent = FixAgent(enable_maximus=False)

        # First: just code
        task1 = create_agent_task(
            "this code has a bug",
            code="def calc(x): return x / 0"
        )
        result1 = agent.execute(task1)
        assert result1.success

        # Then: error message
        task2 = create_agent_task(
            "oh and the error is: ZeroDivisionError: division by zero",
            code="def calc(x): return x / 0",
            error="ZeroDivisionError: division by zero"
        )
        result2 = agent.execute(task2)
        assert result2.success


# ============================================================================
# 8. FOLLOW-UP QUESTIONS
# ============================================================================

class TestFollowUpQuestions:
    """User asks follow-ups about previous responses"""

    def test_what_about_edge_cases(self):
        """User asks about edge cases after implementation"""
        code_agent = CodeAgent(enable_maximus=False)
        review_agent = ReviewAgent(enable_maximus=False)

        # Get implementation
        task1 = create_agent_task("create function to parse user input")
        result1 = code_agent.execute(task1)
        assert result1.success

        # Ask about edge cases
        task2 = create_agent_task(
            "what if input is None",
            code=str(result1.output)  # Reference previous output
        )
        result2 = review_agent.execute(task2)
        assert result2.success

        # More edge cases
        task3 = create_agent_task(
            "what if input is empty string",
            code=str(result1.output)
        )
        result3 = review_agent.execute(task3)
        assert result3.success

    def test_can_you_explain_this_part(self):
        """User asks about specific part of code"""
        agent = CodeAgent(enable_maximus=False)

        code = """
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
"""

        task = create_agent_task(
            "can you explain what 'a, b = b, a + b' does",
            code=code
        )

        result = agent.execute(task)
        assert result.success


# ============================================================================
# 9. MISUNDERSTANDINGS AND CORRECTIONS
# ============================================================================

class TestMisunderstandingsAndCorrections:
    """User corrects agent's misunderstanding"""

    def test_no_not_that_i_meant_this(self):
        """User clarifies what they actually meant"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "create a tree... "
            "no not a data structure tree... "
            "i mean a decision tree... "
            "no wait not for ML... "
            "i mean like a flow chart... "
            "actually just call it a workflow diagram"
        )

        result = agent.execute(task)
        assert result.success
        # Should focus on final clarification: workflow diagram

    def test_wrong_terminology_correction(self):
        """User uses wrong term, then corrects"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "create a function... "
            "wait no sorry i meant a class... "
            "actually just a simple function is fine"
        )

        result = agent.execute(task)
        # Should create function (latest instruction)
        assert result.success


# ============================================================================
# 10. MULTI-FILE CONTEXT
# ============================================================================

class TestMultiFileContext:
    """User references multiple files in conversation"""

    def test_this_file_affects_that_file(self):
        """User explains relationship between files"""
        agent = ReviewAgent(enable_maximus=False)

        task = create_agent_task(
            "review this auth.py file... "
            "note: it imports from database.py which I showed you earlier... "
            "and it's called by api.py",
            code="""
from database import User

def authenticate(username, password):
    user = User.find(username)
    return user.check_password(password)
"""
        )

        result = agent.execute(task)
        assert result.success


print("✅ Conversation Flow test suite created!")
print("Categories: 10")
print("Focus: Multi-turn realistic interactions")
