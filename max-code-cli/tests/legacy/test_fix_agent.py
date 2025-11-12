"""
Comprehensive Scientific Test Suite for FixAgent

This test suite validates the FixAgent's bug detection, root cause analysis,
fix suggestion generation, and fix validation capabilities.

Test Coverage:
- Agent initialization and configuration
- Quick fix mode (standalone)
- PENELOPE integration mode (hybrid)
- Root cause analysis
- Bug detection across different bug types
- Fix suggestion generation and validation
- Error handling and resilience
- Different bug categories (syntax, logic, security, performance)
- Edge cases and boundary conditions
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from agents.fix_agent import FixAgent
from sdk.base_agent import AgentTask, AgentResult, AgentCapability
from core.maximus_integration.penelope_client import (
    HealingContext,
    HealingSuggestion,
    RootCause,
    FixOption
)


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def fix_agent_standalone():
    """FixAgent in standalone mode (no MAXIMUS)"""
    return FixAgent(agent_id="fix-test", enable_maximus=False)


@pytest.fixture
def fix_agent_with_maximus():
    """FixAgent with MAXIMUS integration enabled"""
    return FixAgent(agent_id="fix-test", enable_maximus=True)


@pytest.fixture
def sample_syntax_bug():
    """Sample syntax error code"""
    return {
        "code": """
def authenticate(user, password):
    if user.password = password:  # BUG: assignment instead of comparison
        return True
    return False
""",
        "error": "SyntaxError: invalid syntax (line 2)"
    }


@pytest.fixture
def sample_logic_bug():
    """Sample logic error code"""
    return {
        "code": """
def calculate_discount(price, discount_percent):
    discount = price * discount_percent  # BUG: should divide by 100
    return price - discount
""",
        "error": "ValueError: discount exceeds price"
    }


@pytest.fixture
def sample_security_bug():
    """Sample security vulnerability"""
    return {
        "code": """
def execute_query(user_input):
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # BUG: SQL injection
    return db.execute(query)
""",
        "error": "Security: SQL injection vulnerability detected"
    }


@pytest.fixture
def sample_null_pointer_bug():
    """Sample null pointer bug"""
    return {
        "code": """
def get_user_email(user_id):
    user = db.get_user(user_id)
    return user.email  # BUG: user might be None
""",
        "error": "AttributeError: 'NoneType' object has no attribute 'email'"
    }


@pytest.fixture
def sample_healing_suggestion():
    """Mock healing suggestion from PENELOPE"""
    return HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Assignment operator (=) used instead of comparison operator (==)",
            contributing_factors=["Common typo", "Missing linter checks"],
            confidence=0.95,
            evidence=["Line 2: 'if user.password = password'", "SyntaxError on assignment in condition"]
        ),
        fix_options=[
            FixOption(
                description="Replace assignment with equality comparison",
                code="    if user.password == password:",
                confidence=0.98,
                side_effects=[],
                explanation="Change = to == for comparison"
            ),
            FixOption(
                description="Use identity check",
                code="    if user.password is password:",
                confidence=0.45,
                side_effects=["May not work for string comparison"],
                explanation="Use 'is' operator for identity check"
            )
        ],
        prevention_strategies=["Enable pylint/flake8", "Use strict mode"],
        confidence=0.95,
        analysis="Syntax error caused by assignment in boolean context"
    )


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_fix_agent_initialization_standalone():
    """Test FixAgent initialization in standalone mode"""
    agent = FixAgent(agent_id="fix-1", enable_maximus=False)

    assert agent.agent_id == "fix-1"
    assert agent.agent_name == "Fix Agent (MAXIMUS-Enhanced)"
    assert agent.port == 8165
    assert agent.penelope_client is None

    print("Test passed: FixAgent initialized correctly in standalone mode")


@pytest.mark.asyncio
async def test_fix_agent_initialization_with_maximus():
    """Test FixAgent initialization with MAXIMUS enabled"""
    agent = FixAgent(agent_id="fix-2", enable_maximus=True)

    assert agent.agent_id == "fix-2"
    assert agent.penelope_client is not None
    assert hasattr(agent.penelope_client, 'heal')
    assert hasattr(agent.penelope_client, 'health_check')

    print("Test passed: FixAgent initialized correctly with MAXIMUS")


def test_fix_agent_capabilities():
    """Test FixAgent declares correct capabilities"""
    agent = FixAgent(agent_id="fix-3", enable_maximus=False)
    capabilities = agent.get_capabilities()

    assert AgentCapability.DEBUGGING in capabilities
    assert len(capabilities) >= 1

    print("Test passed: FixAgent has correct capabilities")


# ============================================================================
# STANDALONE MODE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_standalone_quick_fix_syntax_error(fix_agent_standalone, sample_syntax_bug):
    """Test standalone mode quick fix for syntax error"""
    task = AgentTask(
        id="fix-syntax-001",
        description="Fix syntax error in authentication function",
        parameters=sample_syntax_bug
    )

    result = await fix_agent_standalone._execute_async(task)

    assert result.success
    assert result.task_id == "fix-syntax-001"
    assert "fixed_code" in result.output
    assert result.metrics["mode"] == "standalone"
    assert result.output["root_cause"] is None  # No PENELOPE in standalone

    print("Test passed: Standalone quick fix for syntax error")


@pytest.mark.asyncio
async def test_standalone_quick_fix_logic_error(fix_agent_standalone, sample_logic_bug):
    """Test standalone mode quick fix for logic error"""
    task = AgentTask(
        id="fix-logic-001",
        description="Fix logic error in discount calculation",
        parameters=sample_logic_bug
    )

    result = await fix_agent_standalone._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output
    assert sample_logic_bug["code"] in result.output["fixed_code"]
    assert result.metrics["mode"] == "standalone"

    print("Test passed: Standalone quick fix for logic error")


@pytest.mark.asyncio
async def test_standalone_empty_code():
    """Test standalone mode with empty code"""
    agent = FixAgent(agent_id="fix-empty", enable_maximus=False)

    task = AgentTask(
        id="fix-empty-001",
        description="Fix empty code",
        parameters={"code": "", "error": "No code provided"}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Standalone handles empty code gracefully")


@pytest.mark.asyncio
async def test_standalone_no_error_trace():
    """Test standalone mode without error trace"""
    agent = FixAgent(agent_id="fix-no-error", enable_maximus=False)

    task = AgentTask(
        id="fix-no-error-001",
        description="Fix code without error trace",
        parameters={
            "code": "def buggy_function(): pass",
            "error": ""
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Standalone handles missing error trace")


# ============================================================================
# HYBRID MODE TESTS (WITH PENELOPE)
# ============================================================================

@pytest.mark.asyncio
async def test_hybrid_mode_penelope_online(fix_agent_with_maximus, sample_syntax_bug, sample_healing_suggestion):
    """Test hybrid mode when PENELOPE is online and provides fix"""
    task = AgentTask(
        id="fix-hybrid-001",
        description="Fix syntax error with PENELOPE",
        parameters=sample_syntax_bug
    )

    # Mock PENELOPE client
    with patch.object(fix_agent_with_maximus.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(fix_agent_with_maximus.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = sample_healing_suggestion

            result = await fix_agent_with_maximus._execute_async(task)

            assert result.success
            assert "fixed_code" in result.output
            assert "root_cause" in result.output
            assert result.output["root_cause"] is not None
            assert result.metrics["mode"] == "hybrid"

            # Verify PENELOPE was called
            mock_health.assert_called_once()
            mock_heal.assert_called_once()

            # Verify best fix was selected
            assert result.output["fixed_code"] == sample_healing_suggestion.fix_options[0].code

    print("Test passed: Hybrid mode with PENELOPE online")


@pytest.mark.asyncio
async def test_hybrid_mode_penelope_offline(fix_agent_with_maximus, sample_syntax_bug):
    """Test hybrid mode fallback when PENELOPE is offline"""
    task = AgentTask(
        id="fix-hybrid-002",
        description="Fix syntax error when PENELOPE offline",
        parameters=sample_syntax_bug
    )

    # Mock PENELOPE offline
    with patch.object(fix_agent_with_maximus.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = False

        result = await fix_agent_with_maximus._execute_async(task)

        assert result.success
        assert "fixed_code" in result.output
        assert result.output["root_cause"] is None
        assert result.metrics["mode"] == "standalone"  # Falls back

        mock_health.assert_called_once()

    print("Test passed: Hybrid mode fallback when PENELOPE offline")


@pytest.mark.asyncio
async def test_hybrid_mode_penelope_error(fix_agent_with_maximus, sample_syntax_bug):
    """Test hybrid mode when PENELOPE throws error"""
    task = AgentTask(
        id="fix-hybrid-003",
        description="Fix with PENELOPE error handling",
        parameters=sample_syntax_bug
    )

    # Mock PENELOPE error
    with patch.object(fix_agent_with_maximus.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(fix_agent_with_maximus.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.side_effect = Exception("PENELOPE connection error")

            result = await fix_agent_with_maximus._execute_async(task)

            # Should still succeed with fallback
            assert result.success
            assert "fixed_code" in result.output
            assert result.metrics["mode"] == "standalone"

    print("Test passed: Hybrid mode handles PENELOPE errors gracefully")


@pytest.mark.asyncio
async def test_hybrid_mode_low_confidence_fix():
    """Test hybrid mode when PENELOPE fix has low confidence"""
    agent = FixAgent(agent_id="fix-low-conf", enable_maximus=True)

    task = AgentTask(
        id="fix-low-conf-001",
        description="Fix with low confidence suggestion",
        parameters={
            "code": "def buggy(): pass",
            "error": "Some error"
        }
    )

    # Mock low confidence fix
    low_confidence_healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Unknown issue",
            contributing_factors=[],
            confidence=0.3,
            evidence=[]
        ),
        fix_options=[
            FixOption(
                description="Uncertain fix",
                code="# Uncertain fix",
                confidence=0.5,  # Below 0.7 threshold
                side_effects=["May not work"],
                explanation="Not sure"
            )
        ],
        prevention_strategies=[],
        confidence=0.3,
        analysis="Low confidence analysis"
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = low_confidence_healing

            result = await agent._execute_async(task)

            assert result.success
            # Should use quick fix because confidence < 0.7
            assert "Quick fix applied" in result.output["fixed_code"]

    print("Test passed: Hybrid mode rejects low confidence fixes")


# ============================================================================
# ROOT CAUSE ANALYSIS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_root_cause_syntax_error(fix_agent_with_maximus, sample_syntax_bug):
    """Test root cause analysis for syntax error"""
    task = AgentTask(
        id="fix-rca-001",
        description="Analyze root cause of syntax error",
        parameters=sample_syntax_bug
    )

    root_cause = RootCause(
        primary_cause="Assignment operator (=) instead of comparison (==)",
        contributing_factors=["Typo", "No linter"],
        confidence=0.95,
        evidence=["Line 2 syntax error"]
    )

    healing = HealingSuggestion(
        root_cause=root_cause,
        fix_options=[],
        prevention_strategies=[],
        confidence=0.95,
        analysis="Syntax error"
    )

    with patch.object(fix_agent_with_maximus.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(fix_agent_with_maximus.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await fix_agent_with_maximus._execute_async(task)

            assert result.success
            assert result.output["root_cause"] == root_cause
            assert root_cause.primary_cause == "Assignment operator (=) instead of comparison (==)"
            assert root_cause.confidence == 0.95

    print("Test passed: Root cause analysis for syntax error")


@pytest.mark.asyncio
async def test_root_cause_null_pointer(fix_agent_with_maximus, sample_null_pointer_bug):
    """Test root cause analysis for null pointer error"""
    task = AgentTask(
        id="fix-rca-002",
        description="Analyze null pointer error",
        parameters=sample_null_pointer_bug
    )

    root_cause = RootCause(
        primary_cause="Accessing attribute on potentially None object",
        contributing_factors=["No null check", "Database query may return None"],
        confidence=0.92,
        evidence=["AttributeError on line 3", "user.email access without validation"]
    )

    healing = HealingSuggestion(
        root_cause=root_cause,
        fix_options=[
            FixOption(
                description="Add null check",
                code="    if user is None:\n        return None\n    return user.email",
                confidence=0.95,
                side_effects=[],
                explanation="Check if user exists before accessing email"
            )
        ],
        prevention_strategies=["Use Optional typing", "Add defensive checks"],
        confidence=0.92,
        analysis="Null pointer dereference"
    )

    with patch.object(fix_agent_with_maximus.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(fix_agent_with_maximus.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await fix_agent_with_maximus._execute_async(task)

            assert result.success
            assert result.output["root_cause"].primary_cause == "Accessing attribute on potentially None object"
            assert len(result.output["root_cause"].contributing_factors) == 2

    print("Test passed: Root cause analysis for null pointer error")


# ============================================================================
# BUG TYPE SPECIFIC TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_fix_security_vulnerability(fix_agent_with_maximus, sample_security_bug):
    """Test fixing security vulnerability (SQL injection)"""
    task = AgentTask(
        id="fix-security-001",
        description="Fix SQL injection vulnerability",
        parameters=sample_security_bug
    )

    healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="SQL injection vulnerability - unsanitized user input",
            contributing_factors=["Direct string interpolation", "No parameterized queries"],
            confidence=0.99,
            evidence=["f-string with user_input in SQL query"]
        ),
        fix_options=[
            FixOption(
                description="Use parameterized query",
                code='    query = "SELECT * FROM users WHERE name = ?"\n    return db.execute(query, (user_input,))',
                confidence=0.98,
                side_effects=[],
                explanation="Use parameterized queries to prevent SQL injection"
            )
        ],
        prevention_strategies=["Always use parameterized queries", "Input validation", "ORM usage"],
        confidence=0.99,
        analysis="Critical security vulnerability"
    )

    with patch.object(fix_agent_with_maximus.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(fix_agent_with_maximus.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await fix_agent_with_maximus._execute_async(task)

            assert result.success
            assert "SQL injection" in result.output["root_cause"].primary_cause
            assert result.output["root_cause"].confidence >= 0.95

    print("Test passed: Security vulnerability detection and fixing")


@pytest.mark.asyncio
async def test_fix_off_by_one_error():
    """Test fixing off-by-one error (logic bug)"""
    agent = FixAgent(agent_id="fix-off-by-one", enable_maximus=True)

    task = AgentTask(
        id="fix-logic-002",
        description="Fix off-by-one error in array access",
        parameters={
            "code": """
def get_last_element(arr):
    return arr[len(arr)]  # BUG: should be len(arr)-1
""",
            "error": "IndexError: list index out of range"
        }
    )

    healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Off-by-one error - index equals length instead of length-1",
            contributing_factors=["Array indexing starts at 0", "No bounds check"],
            confidence=0.96,
            evidence=["IndexError", "arr[len(arr)] access"]
        ),
        fix_options=[
            FixOption(
                description="Fix array index",
                code="    return arr[len(arr) - 1]",
                confidence=0.97,
                side_effects=[],
                explanation="Use len(arr)-1 for last element"
            ),
            FixOption(
                description="Use negative indexing",
                code="    return arr[-1]",
                confidence=0.98,
                side_effects=[],
                explanation="Python supports negative indexing"
            )
        ],
        prevention_strategies=["Use negative indexing", "Add bounds checking"],
        confidence=0.96,
        analysis="Classic off-by-one error"
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await agent._execute_async(task)

            assert result.success
            assert "off-by-one" in result.output["root_cause"].primary_cause.lower()

    print("Test passed: Off-by-one error detection and fixing")


@pytest.mark.asyncio
async def test_fix_race_condition():
    """Test detecting race condition bug"""
    agent = FixAgent(agent_id="fix-race", enable_maximus=True)

    task = AgentTask(
        id="fix-concurrency-001",
        description="Fix race condition in counter",
        parameters={
            "code": """
counter = 0

def increment():
    global counter
    temp = counter
    counter = temp + 1  # BUG: race condition
""",
            "error": "Race condition: inconsistent counter value in multi-threaded environment"
        }
    )

    healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Race condition - non-atomic read-modify-write operation",
            contributing_factors=["Shared mutable state", "No synchronization"],
            confidence=0.88,
            evidence=["Global counter", "Multi-step update", "Multi-threaded context"]
        ),
        fix_options=[
            FixOption(
                description="Use threading lock",
                code="import threading\nlock = threading.Lock()\n\ndef increment():\n    with lock:\n        global counter\n        counter += 1",
                confidence=0.92,
                side_effects=["Performance overhead from locking"],
                explanation="Synchronize access with lock"
            )
        ],
        prevention_strategies=["Use atomic operations", "Thread-safe data structures"],
        confidence=0.88,
        analysis="Concurrency bug"
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await agent._execute_async(task)

            assert result.success
            assert "race condition" in result.output["root_cause"].primary_cause.lower()

    print("Test passed: Race condition detection")


@pytest.mark.asyncio
async def test_fix_memory_leak():
    """Test detecting memory leak"""
    agent = FixAgent(agent_id="fix-memory", enable_maximus=True)

    task = AgentTask(
        id="fix-memory-001",
        description="Fix memory leak in event handlers",
        parameters={
            "code": """
class EventEmitter:
    def __init__(self):
        self.handlers = []

    def subscribe(self, handler):
        self.handlers.append(handler)  # BUG: never removed
""",
            "error": "MemoryError: handlers list grows indefinitely"
        }
    )

    healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Memory leak - event handlers never unsubscribed",
            contributing_factors=["No cleanup mechanism", "Growing list"],
            confidence=0.91,
            evidence=["handlers.append() without removal", "Memory growth pattern"]
        ),
        fix_options=[
            FixOption(
                description="Add unsubscribe method",
                code="def unsubscribe(self, handler):\n    if handler in self.handlers:\n        self.handlers.remove(handler)",
                confidence=0.93,
                side_effects=[],
                explanation="Provide way to remove handlers"
            )
        ],
        prevention_strategies=["Weak references", "Context managers for cleanup"],
        confidence=0.91,
        analysis="Resource leak"
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await agent._execute_async(task)

            assert result.success
            assert "memory leak" in result.output["root_cause"].primary_cause.lower()

    print("Test passed: Memory leak detection")


# ============================================================================
# FIX VALIDATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_fix_confidence_scoring():
    """Test that fix options are scored by confidence"""
    agent = FixAgent(agent_id="fix-confidence", enable_maximus=True)

    task = AgentTask(
        id="fix-conf-001",
        description="Test confidence scoring",
        parameters={"code": "buggy", "error": "error"}
    )

    # Multiple fix options with different confidences
    healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Test issue",
            contributing_factors=[],
            confidence=0.8,
            evidence=[]
        ),
        fix_options=[
            FixOption(description="Fix 1", code="fix1", confidence=0.60, side_effects=[], explanation="Low"),
            FixOption(description="Fix 2", code="fix2", confidence=0.95, side_effects=[], explanation="High"),
            FixOption(description="Fix 3", code="fix3", confidence=0.75, side_effects=[], explanation="Medium"),
        ],
        prevention_strategies=[],
        confidence=0.8,
        analysis="Test"
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await agent._execute_async(task)

            assert result.success
            # Should select highest confidence fix (0.95)
            assert result.output["fixed_code"] == "fix2"

    print("Test passed: Fix confidence scoring works correctly")


@pytest.mark.asyncio
async def test_multiple_fix_options_selection():
    """Test selection of best fix from multiple options"""
    agent = FixAgent(agent_id="fix-multi", enable_maximus=True)

    task = AgentTask(
        id="fix-multi-001",
        description="Select best fix from multiple options",
        parameters={
            "code": "def buggy(): x = y",
            "error": "NameError: name 'y' is not defined"
        }
    )

    healing = HealingSuggestion(
        root_cause=RootCause(
            primary_cause="Undefined variable",
            contributing_factors=[],
            confidence=0.9,
            evidence=[]
        ),
        fix_options=[
            FixOption(
                description="Initialize y",
                code="def buggy():\n    y = 0\n    x = y",
                confidence=0.85,
                side_effects=[],
                explanation="Add initialization"
            ),
            FixOption(
                description="Remove assignment",
                code="def buggy():\n    pass",
                confidence=0.40,
                side_effects=["Removes functionality"],
                explanation="Remove problematic line"
            ),
            FixOption(
                description="Add parameter",
                code="def buggy(y):\n    x = y",
                confidence=0.90,
                side_effects=["Changes function signature"],
                explanation="Make y a parameter"
            ),
        ],
        prevention_strategies=[],
        confidence=0.9,
        analysis="Variable scope issue"
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = healing

            result = await agent._execute_async(task)

            assert result.success
            # Should pick highest confidence (0.90)
            assert "def buggy(y):" in result.output["fixed_code"]

    print("Test passed: Multiple fix options selection")


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_malformed_task():
    """Test handling of malformed task"""
    agent = FixAgent(agent_id="fix-malformed", enable_maximus=False)

    task = AgentTask(
        id="fix-malformed-001",
        description="Malformed task",
        parameters={}  # Missing 'code' and 'error'
    )

    result = await agent._execute_async(task)

    # Should handle gracefully
    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Malformed task handled gracefully")


@pytest.mark.asyncio
async def test_very_large_code_input():
    """Test handling of very large code input"""
    agent = FixAgent(agent_id="fix-large", enable_maximus=False)

    # Generate large code
    large_code = "\n".join([f"def function_{i}(): pass" for i in range(1000)])

    task = AgentTask(
        id="fix-large-001",
        description="Fix large code file",
        parameters={
            "code": large_code,
            "error": "Some error in large file"
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Large code input handled")


@pytest.mark.asyncio
async def test_special_characters_in_code():
    """Test handling of special characters in code"""
    agent = FixAgent(agent_id="fix-special", enable_maximus=False)

    task = AgentTask(
        id="fix-special-001",
        description="Fix code with special characters",
        parameters={
            "code": """
def process(text):
    # Unicode: \u0394 \u03A3
    return text.replace('\n', '\\n').encode('utf-8')
""",
            "error": "UnicodeDecodeError"
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Special characters handled correctly")


@pytest.mark.asyncio
async def test_concurrent_fix_requests():
    """Test handling multiple concurrent fix requests"""
    agent = FixAgent(agent_id="fix-concurrent", enable_maximus=False)

    tasks = [
        AgentTask(
            id=f"fix-concurrent-{i}",
            description=f"Fix bug {i}",
            parameters={"code": f"def bug_{i}(): pass", "error": f"Error {i}"}
        )
        for i in range(5)
    ]

    # Execute concurrently
    results = await asyncio.gather(*[agent._execute_async(task) for task in tasks])

    assert len(results) == 5
    assert all(r.success for r in results)
    assert all("fixed_code" in r.output for r in results)

    print("Test passed: Concurrent fix requests handled")


# ============================================================================
# EDGE CASES TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_already_fixed_code():
    """Test when code is already correct"""
    agent = FixAgent(agent_id="fix-already", enable_maximus=False)

    task = AgentTask(
        id="fix-already-001",
        description="Fix already correct code",
        parameters={
            "code": """
def calculate_sum(a, b):
    return a + b
""",
            "error": ""
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Already correct code handled")


@pytest.mark.asyncio
async def test_unfixable_code():
    """Test completely broken/unfixable code"""
    agent = FixAgent(agent_id="fix-unfixable", enable_maximus=True)

    task = AgentTask(
        id="fix-unfixable-001",
        description="Fix unfixable code",
        parameters={
            "code": "@@#$%^&*()",
            "error": "SyntaxError: invalid syntax"
        }
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = False

        result = await agent._execute_async(task)

        # Should still succeed (with quick fix fallback)
        assert result.success
        assert "fixed_code" in result.output

    print("Test passed: Unfixable code handled with fallback")


@pytest.mark.asyncio
async def test_multiline_error_trace():
    """Test handling of multiline error traces"""
    agent = FixAgent(agent_id="fix-multiline", enable_maximus=False)

    error_trace = """
Traceback (most recent call last):
  File "test.py", line 10, in <module>
    result = divide(10, 0)
  File "test.py", line 5, in divide
    return a / b
ZeroDivisionError: division by zero
"""

    task = AgentTask(
        id="fix-multiline-001",
        description="Fix division by zero",
        parameters={
            "code": "def divide(a, b):\n    return a / b",
            "error": error_trace
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "fixed_code" in result.output

    print("Test passed: Multiline error trace handled")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_end_to_end_fix_workflow(sample_syntax_bug, sample_healing_suggestion):
    """Test complete end-to-end fix workflow"""
    agent = FixAgent(agent_id="fix-e2e", enable_maximus=True)

    task = AgentTask(
        id="fix-e2e-001",
        description="Complete fix workflow",
        parameters=sample_syntax_bug
    )

    with patch.object(agent.penelope_client, 'health_check', new_callable=AsyncMock) as mock_health:
        with patch.object(agent.penelope_client, 'heal', new_callable=AsyncMock) as mock_heal:
            mock_health.return_value = True
            mock_heal.return_value = sample_healing_suggestion

            # Execute fix
            result = await agent._execute_async(task)

            # Validate complete workflow
            assert result.success
            assert result.task_id == "fix-e2e-001"
            assert "fixed_code" in result.output
            assert "root_cause" in result.output
            assert result.output["root_cause"] is not None
            assert result.metrics["mode"] == "hybrid"

            # Validate root cause analysis
            root_cause = result.output["root_cause"]
            assert root_cause.confidence > 0.7
            assert len(root_cause.evidence) > 0

            # Validate fix was applied
            fixed_code = result.output["fixed_code"]
            assert fixed_code == sample_healing_suggestion.fix_options[0].code

    print("Test passed: End-to-end fix workflow")


def test_execute_method_wrapper():
    """Test the synchronous execute method wrapper"""
    agent = FixAgent(agent_id="fix-sync", enable_maximus=False)

    task = AgentTask(
        id="fix-sync-001",
        description="Test sync wrapper",
        parameters={"code": "def test(): pass", "error": ""}
    )

    # Call synchronous execute (which wraps async)
    result = agent.execute(task)

    assert result.success
    assert isinstance(result, AgentResult)
    assert "fixed_code" in result.output

    print("Test passed: Synchronous execute wrapper works")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    import sys
    import os

    # Add parent directory to path for imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    print("=" * 80)
    print("FIXAGENT COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()
    print("NOTE: This is a basic standalone runner.")
    print("For full test execution with mocking and coverage, use:")
    print("  pytest tests/test_fix_agent.py -v --cov=agents.fix_agent")
    print("=" * 80)
    print()

    # Run basic tests without mocking
    try:
        print("Running basic initialization tests...")
        asyncio.run(test_fix_agent_initialization_standalone())
        asyncio.run(test_fix_agent_initialization_with_maximus())
        test_fix_agent_capabilities()

        print("\n--- Standalone Mode Tests ---")
        agent = FixAgent(enable_maximus=False)
        asyncio.run(test_standalone_empty_code())
        asyncio.run(test_standalone_no_error_trace())

        print("\n--- Error Handling Tests ---")
        asyncio.run(test_malformed_task())
        asyncio.run(test_very_large_code_input())
        asyncio.run(test_special_characters_in_code())
        asyncio.run(test_concurrent_fix_requests())

        print("\n--- Edge Cases Tests ---")
        asyncio.run(test_already_fixed_code())
        asyncio.run(test_multiline_error_trace())

        print("\n--- Integration Tests ---")
        test_execute_method_wrapper()

        print("\n" + "=" * 80)
        print("BASIC TESTS COMPLETE")
        print("For full test suite with mocking, run: pytest tests/test_fix_agent.py -v")
        print("=" * 80)
    except Exception as e:
        print(f"\nError running tests: {e}")
        print("\nPlease run with pytest for full test coverage:")
        print("  cd '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli'")
        print("  pytest tests/test_fix_agent.py -v --cov=agents.fix_agent")
