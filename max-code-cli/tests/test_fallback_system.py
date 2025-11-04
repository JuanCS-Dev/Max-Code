"""
Integration Tests for Fallback System

Tests graceful degradation when MAXIMUS AI is offline.

Run:
    pytest tests/test_fallback_system.py -v
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any

from core.maximus_integration.fallback import (
    FallbackSystem,
    FallbackResult,
    FallbackMode,
    FallbackStrategy,
    FallbackMetrics,
    FallbackContext,
    with_fallback,
    check_maximus_or_warn,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fallback_system():
    """Create FallbackSystem instance with default settings"""
    return FallbackSystem(
        default_strategy=FallbackStrategy.AUTO_FALLBACK,
        timeout_threshold=2.0,
        max_retries=1
    )


@pytest.fixture
def ask_user_fallback():
    """Create FallbackSystem with ASK_USER strategy"""
    return FallbackSystem(
        default_strategy=FallbackStrategy.ASK_USER,
        timeout_threshold=2.0,
        max_retries=1
    )


@pytest.fixture
def fail_fast_fallback():
    """Create FallbackSystem with FAIL_FAST strategy"""
    return FallbackSystem(
        default_strategy=FallbackStrategy.FAIL_FAST,
        timeout_threshold=2.0,
        max_retries=1
    )


@pytest.fixture
def primary_success():
    """Mock primary function that succeeds"""
    async def fn():
        await asyncio.sleep(0.01)  # Simulate network call
        return {"status": "success", "data": "from MAXIMUS"}
    return fn


@pytest.fixture
def primary_timeout():
    """Mock primary function that times out"""
    async def fn():
        await asyncio.sleep(5.0)  # Simulate timeout (> 2s threshold)
        return {"status": "timeout"}
    return fn


@pytest.fixture
def primary_error():
    """Mock primary function that raises error"""
    async def fn():
        raise ConnectionError("MAXIMUS unreachable")
    return fn


@pytest.fixture
def fallback_fn():
    """Mock fallback function"""
    async def fn():
        await asyncio.sleep(0.01)
        return {"status": "fallback", "data": "from Max-Code standalone"}
    return fn


# ============================================================================
# TEST: INITIALIZATION
# ============================================================================

def test_fallback_system_initialization():
    """Test FallbackSystem initialization with custom parameters"""
    fallback = FallbackSystem(
        default_strategy=FallbackStrategy.FAIL_FAST,
        timeout_threshold=5.0,
        max_retries=3
    )

    assert fallback.default_strategy == FallbackStrategy.FAIL_FAST
    assert fallback.timeout_threshold == 5.0
    assert fallback.max_retries == 3
    assert isinstance(fallback.metrics, FallbackMetrics)


def test_fallback_metrics_initialization():
    """Test FallbackMetrics starts with zero values"""
    metrics = FallbackMetrics()

    assert metrics.total_executions == 0
    assert metrics.hybrid_executions == 0
    assert metrics.standalone_executions == 0
    assert metrics.failed_executions == 0
    assert metrics.user_approvals == 0
    assert metrics.user_rejections == 0
    assert metrics.avg_maximus_latency_ms == 0.0
    assert metrics.avg_fallback_latency_ms == 0.0


# ============================================================================
# TEST: HYBRID MODE (MAXIMUS Online)
# ============================================================================

@pytest.mark.asyncio
async def test_execute_with_fallback_hybrid_mode(fallback_system, primary_success, fallback_fn):
    """Test execution in hybrid mode when MAXIMUS is online"""
    result = await fallback_system.execute_with_fallback(
        primary_fn=primary_success,
        fallback_fn=fallback_fn,
        task_critical=False
    )

    assert isinstance(result, FallbackResult)
    assert result.mode == FallbackMode.HYBRID
    assert result.maximus_available == True
    assert result.result["status"] == "success"
    assert result.result["data"] == "from MAXIMUS"
    assert result.latency_ms > 0
    assert len(result.warnings) == 0


@pytest.mark.asyncio
async def test_hybrid_mode_updates_metrics(fallback_system, primary_success, fallback_fn):
    """Test that hybrid mode execution updates metrics correctly"""
    await fallback_system.execute_with_fallback(
        primary_fn=primary_success,
        fallback_fn=fallback_fn,
    )

    metrics = fallback_system.get_metrics()

    assert metrics.total_executions == 1
    assert metrics.hybrid_executions == 1
    assert metrics.standalone_executions == 0
    assert metrics.failed_executions == 0
    assert metrics.avg_maximus_latency_ms > 0


# ============================================================================
# TEST: STANDALONE MODE (MAXIMUS Offline)
# ============================================================================

@pytest.mark.asyncio
async def test_execute_with_fallback_standalone_mode_auto(fallback_system, primary_error, fallback_fn):
    """Test auto fallback to standalone mode when MAXIMUS fails"""
    result = await fallback_system.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
        task_critical=False
    )

    assert isinstance(result, FallbackResult)
    assert result.mode == FallbackMode.STANDALONE
    assert result.maximus_available == False
    assert result.result["status"] == "fallback"
    assert result.result["data"] == "from Max-Code standalone"
    assert len(result.warnings) > 0
    assert "MAXIMUS offline" in result.warnings[0]


@pytest.mark.asyncio
async def test_standalone_mode_updates_metrics(fallback_system, primary_error, fallback_fn):
    """Test that standalone mode execution updates metrics correctly"""
    await fallback_system.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
    )

    metrics = fallback_system.get_metrics()

    assert metrics.total_executions == 1
    assert metrics.hybrid_executions == 0
    assert metrics.standalone_executions == 1
    assert metrics.failed_executions == 0
    assert metrics.avg_fallback_latency_ms > 0


@pytest.mark.asyncio
async def test_fallback_on_timeout(fallback_system, primary_timeout, fallback_fn):
    """Test fallback triggers on timeout"""
    # Lower timeout threshold for faster test
    fallback_system.timeout_threshold = 0.1

    result = await fallback_system.execute_with_fallback(
        primary_fn=primary_timeout,
        fallback_fn=fallback_fn,
    )

    assert result.mode == FallbackMode.STANDALONE
    assert result.maximus_available == False


# ============================================================================
# TEST: FAIL_FAST STRATEGY
# ============================================================================

@pytest.mark.asyncio
async def test_fail_fast_critical_task(fail_fast_fallback, primary_error, fallback_fn):
    """Test FAIL_FAST strategy blocks critical tasks when MAXIMUS offline"""
    result = await fail_fast_fallback.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
        task_critical=True  # Critical task
    )

    assert isinstance(result, FallbackResult)
    assert result.mode == FallbackMode.FAILED
    assert result.maximus_available == False
    assert result.result is None
    assert "Critical task blocked" in result.warnings[0]


@pytest.mark.asyncio
async def test_fail_fast_non_critical_task(fail_fast_fallback, primary_error, fallback_fn):
    """Test FAIL_FAST strategy allows non-critical tasks in fallback mode"""
    result = await fail_fast_fallback.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
        task_critical=False  # Non-critical task
    )

    # Should fallback since task is not critical
    assert result.mode == FallbackMode.STANDALONE
    assert result.result is not None


@pytest.mark.asyncio
async def test_fail_fast_updates_metrics(fail_fast_fallback, primary_error, fallback_fn):
    """Test FAIL_FAST strategy updates metrics correctly"""
    await fail_fast_fallback.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
        task_critical=True
    )

    metrics = fail_fast_fallback.get_metrics()

    assert metrics.total_executions == 1
    assert metrics.failed_executions == 1


# ============================================================================
# TEST: ASK_USER STRATEGY
# ============================================================================

@pytest.mark.asyncio
async def test_ask_user_approved(ask_user_fallback, primary_error, fallback_fn):
    """Test ASK_USER strategy when user approves fallback"""
    # Mock user input to approve
    with patch.object(ask_user_fallback, '_ask_user_continue', return_value=True):
        result = await ask_user_fallback.execute_with_fallback(
            primary_fn=primary_error,
            fallback_fn=fallback_fn,
            context={"task_description": "Test task"}
        )

    assert result.mode == FallbackMode.STANDALONE
    assert result.user_approved_fallback == True
    assert result.result is not None


@pytest.mark.asyncio
async def test_ask_user_rejected(ask_user_fallback, primary_error, fallback_fn):
    """Test ASK_USER strategy when user rejects fallback"""
    # Mock user input to reject
    with patch.object(ask_user_fallback, '_ask_user_continue', return_value=False):
        result = await ask_user_fallback.execute_with_fallback(
            primary_fn=primary_error,
            fallback_fn=fallback_fn,
            context={"task_description": "Test task"}
        )

    assert result.mode == FallbackMode.FAILED
    assert result.user_approved_fallback == False
    assert result.result is None
    assert "User rejected" in result.warnings[0]


@pytest.mark.asyncio
async def test_ask_user_updates_metrics_approval(ask_user_fallback, primary_error, fallback_fn):
    """Test ASK_USER strategy updates metrics on approval"""
    with patch.object(ask_user_fallback, '_ask_user_continue', return_value=True):
        await ask_user_fallback.execute_with_fallback(
            primary_fn=primary_error,
            fallback_fn=fallback_fn,
        )

    metrics = ask_user_fallback.get_metrics()

    assert metrics.user_approvals == 1
    assert metrics.user_rejections == 0
    assert metrics.standalone_executions == 1


@pytest.mark.asyncio
async def test_ask_user_updates_metrics_rejection(ask_user_fallback, primary_error, fallback_fn):
    """Test ASK_USER strategy updates metrics on rejection"""
    with patch.object(ask_user_fallback, '_ask_user_continue', return_value=False):
        await ask_user_fallback.execute_with_fallback(
            primary_fn=primary_error,
            fallback_fn=fallback_fn,
        )

    metrics = ask_user_fallback.get_metrics()

    assert metrics.user_approvals == 0
    assert metrics.user_rejections == 1
    assert metrics.failed_executions == 1


# gordurinha

def test_ask_user_continue_input_yes(ask_user_fallback):
    """Test _ask_user_continue with 'yes' input"""
    with patch('builtins.input', return_value='y'):
        result = ask_user_fallback._ask_user_continue({"task_description": "Test"})

    assert result == True


def test_ask_user_continue_input_no(ask_user_fallback):
    """Test _ask_user_continue with 'no' input"""
    with patch('builtins.input', return_value='n'):
        result = ask_user_fallback._ask_user_continue({"task_description": "Test"})

    assert result == False


def test_ask_user_continue_input_default(ask_user_fallback):
    """Test _ask_user_continue with empty input (default = no)"""
    with patch('builtins.input', return_value=''):
        result = ask_user_fallback._ask_user_continue({"task_description": "Test"})

    assert result == False


# ============================================================================
# TEST: STRATEGY OVERRIDE
# ============================================================================

@pytest.mark.asyncio
async def test_strategy_override(fallback_system, primary_error, fallback_fn):
    """Test that strategy parameter overrides default strategy"""
    # Default is AUTO_FALLBACK, but override with FAIL_FAST
    result = await fallback_system.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
        task_critical=True,
        strategy=FallbackStrategy.FAIL_FAST  # Override
    )

    # Should fail (FAIL_FAST) despite default being AUTO_FALLBACK
    assert result.mode == FallbackMode.FAILED


# ============================================================================
# TEST: CONTEXT MANAGER
# ============================================================================

@pytest.mark.asyncio
async def test_fallback_context_maximus_online():
    """Test FallbackContext when MAXIMUS is online"""
    mock_client = MagicMock()
    mock_client.health_check = AsyncMock(return_value=True)

    async with FallbackContext(mock_client, timeout=2.0) as fb:
        assert fb.maximus_available == True


@pytest.mark.asyncio
async def test_fallback_context_maximus_offline():
    """Test FallbackContext when MAXIMUS is offline"""
    mock_client = MagicMock()
    mock_client.health_check = AsyncMock(side_effect=ConnectionError("Offline"))

    async with FallbackContext(mock_client, timeout=2.0) as fb:
        assert fb.maximus_available == False


@pytest.mark.asyncio
async def test_fallback_context_timeout():
    """Test FallbackContext times out properly"""
    mock_client = MagicMock()

    async def slow_health_check():
        await asyncio.sleep(5.0)
        return True

    mock_client.health_check = slow_health_check

    async with FallbackContext(mock_client, timeout=0.1) as fb:
        assert fb.maximus_available == False


# ============================================================================
# TEST: CONVENIENCE FUNCTIONS
# ============================================================================

@pytest.mark.asyncio
async def test_with_fallback_convenience_function(primary_success, fallback_fn):
    """Test with_fallback convenience function"""
    result = await with_fallback(
        primary_fn=primary_success,
        fallback_fn=fallback_fn,
        ask_user=False
    )

    assert isinstance(result, FallbackResult)
    assert result.mode == FallbackMode.HYBRID


@pytest.mark.asyncio
async def test_check_maximus_or_warn_online():
    """Test check_maximus_or_warn when MAXIMUS is online"""
    mock_client = MagicMock()
    mock_client.health_check = AsyncMock(return_value=True)

    result = await check_maximus_or_warn(mock_client)

    assert result == True


@pytest.mark.asyncio
async def test_check_maximus_or_warn_offline():
    """Test check_maximus_or_warn when MAXIMUS is offline"""
    mock_client = MagicMock()
    mock_client.health_check = AsyncMock(return_value=False)

    result = await check_maximus_or_warn(mock_client)

    assert result == False


@pytest.mark.asyncio
async def test_check_maximus_or_warn_error():
    """Test check_maximus_or_warn when health check raises error"""
    mock_client = MagicMock()
    mock_client.health_check = AsyncMock(side_effect=ConnectionError("Network error"))

    result = await check_maximus_or_warn(mock_client)

    assert result == False


# ============================================================================
# TEST: METRICS
# ============================================================================

def test_get_metrics(fallback_system):
    """Test get_metrics returns FallbackMetrics"""
    metrics = fallback_system.get_metrics()

    assert isinstance(metrics, FallbackMetrics)


def test_reset_metrics(fallback_system):
    """Test reset_metrics clears all metrics"""
    # Manually set some metrics
    fallback_system.metrics.total_executions = 10
    fallback_system.metrics.hybrid_executions = 5

    # Reset
    fallback_system.reset_metrics()

    # Verify reset
    metrics = fallback_system.get_metrics()
    assert metrics.total_executions == 0
    assert metrics.hybrid_executions == 0


def test_print_metrics(fallback_system, capsys):
    """Test print_metrics outputs to console"""
    fallback_system.metrics.total_executions = 10
    fallback_system.metrics.hybrid_executions = 6
    fallback_system.metrics.standalone_executions = 3
    fallback_system.metrics.failed_executions = 1

    fallback_system.print_metrics()

    captured = capsys.readouterr()
    output = captured.out

    assert "Fallback System Metrics" in output
    assert "Total Executions:" in output
    assert "10" in output


def test_update_avg():
    """Test _update_avg calculates running average correctly"""
    fallback = FallbackSystem()

    # First value
    avg1 = fallback._update_avg(0.0, 100.0, 1)
    assert avg1 == 100.0

    # Second value
    avg2 = fallback._update_avg(avg1, 200.0, 2)
    assert avg2 == 150.0  # (100 + 200) / 2

    # Third value
    avg3 = fallback._update_avg(avg2, 300.0, 3)
    assert avg3 == 200.0  # (100 + 200 + 300) / 3


def test_pct_calculation(fallback_system):
    """Test _pct calculates percentage correctly"""
    assert fallback_system._pct(5, 10) == "50.0%"
    assert fallback_system._pct(1, 3) == "33.3%"
    assert fallback_system._pct(0, 10) == "0.0%"
    assert fallback_system._pct(0, 0) == "0%"  # Edge case


# ============================================================================
# TEST: LATENCY TRACKING
# ============================================================================

@pytest.mark.asyncio
async def test_latency_tracking_hybrid(fallback_system, primary_success, fallback_fn):
    """Test latency tracking for hybrid mode"""
    result = await fallback_system.execute_with_fallback(
        primary_fn=primary_success,
        fallback_fn=fallback_fn,
    )

    assert result.latency_ms > 0
    assert fallback_system.metrics.avg_maximus_latency_ms > 0


@pytest.mark.asyncio
async def test_latency_tracking_standalone(fallback_system, primary_error, fallback_fn):
    """Test latency tracking for standalone mode"""
    result = await fallback_system.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
    )

    assert result.latency_ms > 0
    assert fallback_system.metrics.avg_fallback_latency_ms > 0
    assert "Fallback latency:" in result.warnings[1]


# ============================================================================
# TEST: MULTIPLE EXECUTIONS
# ============================================================================

@pytest.mark.asyncio
async def test_multiple_executions_mixed(fallback_system, primary_success, primary_error, fallback_fn):
    """Test multiple executions with mixed results"""
    # First execution: hybrid (success)
    result1 = await fallback_system.execute_with_fallback(
        primary_fn=primary_success,
        fallback_fn=fallback_fn,
    )

    # Second execution: standalone (error)
    result2 = await fallback_system.execute_with_fallback(
        primary_fn=primary_error,
        fallback_fn=fallback_fn,
    )

    # Third execution: hybrid (success)
    result3 = await fallback_system.execute_with_fallback(
        primary_fn=primary_success,
        fallback_fn=fallback_fn,
    )

    # Verify results
    assert result1.mode == FallbackMode.HYBRID
    assert result2.mode == FallbackMode.STANDALONE
    assert result3.mode == FallbackMode.HYBRID

    # Verify metrics
    metrics = fallback_system.get_metrics()
    assert metrics.total_executions == 3
    assert metrics.hybrid_executions == 2
    assert metrics.standalone_executions == 1
    assert metrics.failed_executions == 0


# ============================================================================
# TEST: ERROR HANDLING
# ============================================================================

@pytest.mark.asyncio
async def test_fallback_result_warnings_initialization():
    """Test FallbackResult warnings list is initialized"""
    result = FallbackResult(
        result="test",
        mode=FallbackMode.HYBRID,
        latency_ms=100.0,
        maximus_available=True
    )

    assert result.warnings == []


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

1. Initialization (2 tests)
   - FallbackSystem initialization
   - FallbackMetrics initialization

2. Hybrid Mode (2 tests)
   - Successful execution when MAXIMUS online
   - Metrics updates

3. Standalone Mode (3 tests)
   - Auto fallback on error
   - Metrics updates
   - Timeout handling

4. FAIL_FAST Strategy (3 tests)
   - Blocks critical tasks
   - Allows non-critical tasks
   - Metrics updates

5. ASK_USER Strategy (6 tests)
   - User approval flow
   - User rejection flow
   - Metrics updates (approval/rejection)
   - Input handling (yes/no/default)

6. Strategy Override (1 test)
   - Parameter overrides default

7. Context Manager (3 tests)
   - MAXIMUS online/offline
   - Timeout handling

8. Convenience Functions (4 tests)
   - with_fallback()
   - check_maximus_or_warn() (online/offline/error)

9. Metrics (5 tests)
   - get_metrics()
   - reset_metrics()
   - print_metrics()
   - _update_avg()
   - _pct()

10. Latency Tracking (2 tests)
    - Hybrid mode latency
    - Standalone mode latency

11. Multiple Executions (1 test)
    - Mixed hybrid/standalone executions

12. Error Handling (1 test)
    - FallbackResult initialization

Total: 33 comprehensive test cases covering all fallback strategies and edge cases.
"""
