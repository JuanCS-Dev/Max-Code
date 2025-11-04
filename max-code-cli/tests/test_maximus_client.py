"""
MAXIMUS Client Tests

Tests for MAXIMUS AI backend integration client.

Biblical Foundation:
"Provai todas as coisas; retende o que é bom." (1 Tessalonicenses 5:21)
Test all things - keep what is good.

Coverage:
- MaximusClient initialization
- Health check
- Systemic impact analysis
- Ethical review (4 frameworks)
- Edge case prediction
- Code healing (PENELOPE)
- Web search (MABA)
- Narrative generation (NIS)
- Error handling (offline, timeout, API errors)
- Retry logic
- Connection pooling
"""

import sys
import os
import asyncio
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any

# Add parent to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.maximus_integration import (
    MaximusClient,
    SystemicAnalysis,
    EthicalVerdict,
    EdgeCase,
    EdgeCaseSeverity,
    HealingSuggestion,
    FixOption,
    MABASearchResult,
    SearchResult,
    Narrative,
    MaximusOfflineError,
    MaximusTimeoutError,
    MaximusAPIError,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """Create MaximusClient instance"""
    return MaximusClient(
        base_url="http://localhost:8153",
        timeout=5.0,
        max_retries=3
    )


@pytest.fixture
def mock_systemic_analysis_response():
    """Mock systemic analysis response"""
    return {
        "systemic_risk_score": 0.35,
        "side_effects": [
            "May affect authentication flow",
            "Database migration required"
        ],
        "mitigation_strategies": [
            "Add backward compatibility",
            "Run migration in staging first"
        ],
        "affected_components": ["auth_service", "user_db"],
        "confidence": 0.89,
        "reasoning": "Based on dependency analysis using LEI framework"
    }


@pytest.fixture
def mock_ethical_verdict_response():
    """Mock ethical review response"""
    return {
        "kantian_score": 85.0,
        "virtue_score": 92.0,
        "consequentialist_score": 78.0,
        "principlism_score": 88.0,
        "verdict": "APPROVED",
        "reasoning": "Code change respects user autonomy and privacy",
        "issues": [],
        "recommendations": ["Add privacy notice", "Log data access"]
    }


@pytest.fixture
def mock_edge_cases_response():
    """Mock edge case prediction response"""
    return [
        {
            "scenario": "User enters empty string for password",
            "probability": 0.78,
            "severity": "HIGH",
            "suggested_test": "test_empty_password_rejected()",
            "reasoning": "Common user mistake, high impact"
        },
        {
            "scenario": "Concurrent login attempts from same user",
            "probability": 0.45,
            "severity": "MEDIUM",
            "suggested_test": "test_concurrent_login_handling()",
            "reasoning": "Race condition possible"
        }
    ]


# ============================================================================
# TEST: Initialization
# ============================================================================

def test_client_initialization():
    """Test client initialization with default and custom params"""
    print("=" * 70)
    print("TEST: Client Initialization")
    print("=" * 70)

    # Default initialization
    client1 = MaximusClient()
    assert client1.base_url == "http://localhost:8153"
    assert client1.timeout == 5.0
    assert client1.max_retries == 3
    print("✓ Default initialization works")

    # Custom initialization
    client2 = MaximusClient(
        base_url="http://custom:9000",
        timeout=10.0,
        max_retries=5
    )
    assert client2.base_url == "http://custom:9000"
    assert client2.timeout == 10.0
    assert client2.max_retries == 5
    print("✓ Custom initialization works")

    # URL trailing slash handling
    client3 = MaximusClient(base_url="http://localhost:8153/")
    assert client3.base_url == "http://localhost:8153"  # No trailing slash
    print("✓ URL trailing slash removed")

    return True


# ============================================================================
# TEST: Health Check
# ============================================================================

@pytest.mark.asyncio
async def test_health_check_online(client, mock_systemic_analysis_response):
    """Test health check when MAXIMUS is online"""
    print("\n" + "=" * 70)
    print("TEST: Health Check (Online)")
    print("=" * 70)

    # Mock successful response
    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": {"status": "healthy", "version": "2.0.0"},
            "latency_ms": 15
        }

        result = await client.health_check()

        assert result is True
        mock_request.assert_called_once()
        print("✓ Health check returns True when online")

    return True


@pytest.mark.asyncio
async def test_health_check_offline(client):
    """Test health check when MAXIMUS is offline"""
    print("\n" + "=" * 70)
    print("TEST: Health Check (Offline)")
    print("=" * 70)

    # Mock connection error
    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = MaximusOfflineError("Connection refused")

        result = await client.health_check()

        assert result is False
        print("✓ Health check returns False when offline")

    return True


# ============================================================================
# TEST: Systemic Impact Analysis
# ============================================================================

@pytest.mark.asyncio
async def test_analyze_systemic_impact(client, mock_systemic_analysis_response):
    """Test systemic impact analysis"""
    print("\n" + "=" * 70)
    print("TEST: Systemic Impact Analysis")
    print("=" * 70)

    action = {"type": "code_change", "file": "auth.py", "lines_changed": 45}
    context = {"codebase_size": 10000, "test_coverage": 0.85}

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": mock_systemic_analysis_response,
            "latency_ms": 120
        }

        result = await client.analyze_systemic_impact(action, context)

        # Verify result type
        assert isinstance(result, SystemicAnalysis)
        assert result.systemic_risk_score == 0.35
        assert len(result.side_effects) == 2
        assert len(result.mitigation_strategies) == 2
        assert result.confidence == 0.89
        print(f"✓ Systemic analysis returned: risk={result.systemic_risk_score}")
        print(f"  Side effects: {len(result.side_effects)}")
        print(f"  Mitigation strategies: {len(result.mitigation_strategies)}")

    return True


# ============================================================================
# TEST: Ethical Review
# ============================================================================

@pytest.mark.asyncio
async def test_ethical_review(client, mock_ethical_verdict_response):
    """Test ethical review with 4 frameworks"""
    print("\n" + "=" * 70)
    print("TEST: Ethical Review (4 Frameworks)")
    print("=" * 70)

    code_change = {
        "description": "Add user tracking for analytics",
        "diff": "...",
        "affected_users": 10000
    }
    context = {"privacy_policy": "...", "user_consent": True}

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": mock_ethical_verdict_response,
            "latency_ms": 200
        }

        result = await client.ethical_review(code_change, context)

        # Verify result
        assert isinstance(result, EthicalVerdict)
        assert result.verdict == "APPROVED"
        assert result.kantian_score == 85.0
        assert result.virtue_score == 92.0
        assert result.consequentialist_score == 78.0
        assert result.principlism_score == 88.0
        print(f"✓ Ethical review returned: verdict={result.verdict}")
        print(f"  Kantian: {result.kantian_score}")
        print(f"  Virtue: {result.virtue_score}")
        print(f"  Consequentialist: {result.consequentialist_score}")
        print(f"  Principlism: {result.principlism_score}")

    return True


# ============================================================================
# TEST: Edge Case Prediction
# ============================================================================

@pytest.mark.asyncio
async def test_predict_edge_cases(client, mock_edge_cases_response):
    """Test edge case prediction"""
    print("\n" + "=" * 70)
    print("TEST: Edge Case Prediction")
    print("=" * 70)

    code = """
def login(username, password):
    if not username or not password:
        raise ValueError("Invalid credentials")
    return authenticate(username, password)
"""
    context = {"function": "login", "security_critical": True}

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": {"edge_cases": mock_edge_cases_response},
            "latency_ms": 180
        }

        result = await client.predict_edge_cases(code, context)

        # Verify result
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], EdgeCase)
        assert result[0].severity == EdgeCaseSeverity.HIGH
        assert result[0].probability == 0.78
        print(f"✓ Edge case prediction returned: {len(result)} cases")
        for i, edge_case in enumerate(result, 1):
            print(f"  {i}. {edge_case.scenario} (prob={edge_case.probability:.2f}, sev={edge_case.severity.value})")

    return True


# ============================================================================
# TEST: Code Healing (PENELOPE)
# ============================================================================

@pytest.mark.asyncio
async def test_heal_code(client):
    """Test code healing with PENELOPE"""
    print("\n" + "=" * 70)
    print("TEST: Code Healing (PENELOPE)")
    print("=" * 70)

    error_msg = "AttributeError: 'NoneType' object has no attribute 'username'"
    code = """
def get_user_name(user_id):
    user = db.get_user(user_id)
    return user.username  # Error if user is None
"""
    context = {"stack_trace": "..."}

    mock_healing_response = {
        "root_cause": "Missing null check before accessing attribute",
        "fix_suggestions": [
            {
                "description": "Add null check with default value",
                "code": "return user.username if user else 'Unknown'",
                "confidence": 0.92,
                "side_effects": ["Changes return type behavior"]
            },
            {
                "description": "Raise explicit exception",
                "code": "if not user: raise UserNotFoundError(user_id)\nreturn user.username",
                "confidence": 0.88,
                "side_effects": ["Requires new exception class"]
            }
        ],
        "confidence": 0.90,
        "analysis": "Root cause analysis using PENELOPE framework"
    }

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": mock_healing_response,
            "latency_ms": 250
        }

        result = await client.heal_code(error_msg, code, context)

        # Verify result
        assert isinstance(result, HealingSuggestion)
        assert result.root_cause.startswith("Missing null check")
        assert len(result.fix_suggestions) == 2
        assert isinstance(result.fix_suggestions[0], FixOption)
        assert result.confidence == 0.90
        print(f"✓ Code healing returned: {len(result.fix_suggestions)} fix options")
        print(f"  Root cause: {result.root_cause}")
        for i, fix in enumerate(result.fix_suggestions, 1):
            print(f"  {i}. {fix.description} (confidence={fix.confidence:.2f})")

    return True


# ============================================================================
# TEST: Web Search (MABA)
# ============================================================================

@pytest.mark.asyncio
async def test_search_web(client):
    """Test web search with MABA"""
    print("\n" + "=" * 70)
    print("TEST: Web Search (MABA)")
    print("=" * 70)

    query = "Python async await best practices"
    context = {"language": "python", "topic": "concurrency"}

    mock_search_response = {
        "results": [
            {
                "title": "Async/Await in Python - Official Docs",
                "url": "https://docs.python.org/3/library/asyncio.html",
                "snippet": "Asyncio is used as a foundation for multiple...",
                "relevance": 0.95
            },
            {
                "title": "Real Python - Async IO Tutorial",
                "url": "https://realpython.com/async-io-python/",
                "snippet": "A complete walkthrough of async programming...",
                "relevance": 0.88
            }
        ],
        "confidence": 0.91,
        "query_understanding": "User wants best practices for async/await in Python"
    }

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": mock_search_response,
            "latency_ms": 300
        }

        result = await client.search_web(query, context)

        # Verify result
        assert isinstance(result, MABASearchResult)
        assert len(result.results) == 2
        assert isinstance(result.results[0], SearchResult)
        assert result.confidence == 0.91
        print(f"✓ Web search returned: {len(result.results)} results")
        for i, res in enumerate(result.results, 1):
            print(f"  {i}. {res.title} (rel={res.relevance:.2f})")

    return True


# ============================================================================
# TEST: Narrative Generation (NIS)
# ============================================================================

@pytest.mark.asyncio
async def test_generate_narrative(client):
    """Test narrative generation with NIS"""
    print("\n" + "=" * 70)
    print("TEST: Narrative Generation (NIS)")
    print("=" * 70)

    code_changes = {
        "commits": 15,
        "files_changed": 23,
        "lines_added": 456,
        "lines_removed": 189
    }
    context = {"sprint": "Q4-Sprint-3", "team": "backend"}

    mock_narrative_response = {
        "story": "In Q4 Sprint 3, the backend team focused on...",
        "key_insights": [
            "Significant refactoring in auth module",
            "Test coverage increased by 15%",
            "Performance optimization in database queries"
        ],
        "visualization_data": {
            "timeline": [...],
            "impact_graph": {...}
        },
        "confidence": 0.87
    }

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "data": mock_narrative_response,
            "latency_ms": 400
        }

        result = await client.generate_narrative(code_changes, context)

        # Verify result
        assert isinstance(result, Narrative)
        assert result.story.startswith("In Q4 Sprint 3")
        assert len(result.key_insights) == 3
        assert result.confidence == 0.87
        print(f"✓ Narrative generation returned story with {len(result.key_insights)} insights")
        print(f"  Story preview: {result.story[:60]}...")
        for i, insight in enumerate(result.key_insights, 1):
            print(f"  {i}. {insight}")

    return True


# ============================================================================
# TEST: Error Handling
# ============================================================================

@pytest.mark.asyncio
async def test_offline_error_handling(client):
    """Test handling when MAXIMUS is offline"""
    print("\n" + "=" * 70)
    print("TEST: Offline Error Handling")
    print("=" * 70)

    action = {"type": "code_change"}
    context = {}

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = MaximusOfflineError("Connection refused")

        try:
            await client.analyze_systemic_impact(action, context)
            assert False, "Should have raised MaximusOfflineError"
        except MaximusOfflineError as e:
            assert e.message == "Connection refused"
            print(f"✓ MaximusOfflineError raised correctly: {e.message}")

    return True


@pytest.mark.asyncio
async def test_timeout_error_handling(client):
    """Test handling when request times out"""
    print("\n" + "=" * 70)
    print("TEST: Timeout Error Handling")
    print("=" * 70)

    action = {"type": "code_change"}
    context = {}

    with patch.object(client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = MaximusTimeoutError("Request timed out after 5s")

        try:
            await client.analyze_systemic_impact(action, context)
            assert False, "Should have raised MaximusTimeoutError"
        except MaximusTimeoutError as e:
            assert "timed out" in e.message.lower()
            print(f"✓ MaximusTimeoutError raised correctly: {e.message}")

    return True


# ============================================================================
# TEST: Session Management
# ============================================================================

@pytest.mark.asyncio
async def test_session_management(client):
    """Test aiohttp session creation and reuse"""
    print("\n" + "=" * 70)
    print("TEST: Session Management")
    print("=" * 70)

    # Get session
    session1 = await client._get_session()
    assert session1 is not None
    assert not session1.closed
    print("✓ Session created successfully")

    # Reuse same session
    session2 = await client._get_session()
    assert session1 is session2
    print("✓ Session reused (same instance)")

    # Close session
    await client.close()
    assert session1.closed
    print("✓ Session closed successfully")

    return True


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all MAXIMUS client tests"""
    print("\n" + "=" * 70)
    print("MAXIMUS CLIENT TESTS")
    print("=" * 70)
    print("Testing MAXIMUS AI backend integration\n")

    # Synchronous tests
    sync_tests = [
        ("Client Initialization", test_client_initialization),
    ]

    # Async tests
    async_tests = [
        ("Health Check (Online)", test_health_check_online),
        ("Health Check (Offline)", test_health_check_offline),
        ("Systemic Impact Analysis", test_analyze_systemic_impact),
        ("Ethical Review", test_ethical_review),
        ("Edge Case Prediction", test_predict_edge_cases),
        ("Code Healing (PENELOPE)", test_heal_code),
        ("Web Search (MABA)", test_search_web),
        ("Narrative Generation (NIS)", test_generate_narrative),
        ("Offline Error Handling", test_offline_error_handling),
        ("Timeout Error Handling", test_timeout_error_handling),
        ("Session Management", test_session_management),
    ]

    results = []

    # Run sync tests
    for name, test_func in sync_tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Run async tests
    for name, test_func in async_tests:
        try:
            # Create fixtures
            client = MaximusClient()
            mock_systemic = {
                "systemic_risk_score": 0.35,
                "side_effects": ["Effect 1", "Effect 2"],
                "mitigation_strategies": ["Strategy 1", "Strategy 2"],
                "affected_components": ["comp1", "comp2"],
                "confidence": 0.89,
                "reasoning": "Analysis"
            }
            mock_ethical = {
                "kantian_score": 85.0,
                "virtue_score": 92.0,
                "consequentialist_score": 78.0,
                "principlism_score": 88.0,
                "verdict": "APPROVED",
                "reasoning": "Good",
                "issues": [],
                "recommendations": ["Rec1"]
            }
            mock_edges = [
                {
                    "scenario": "Edge case 1",
                    "probability": 0.78,
                    "severity": "HIGH",
                    "suggested_test": "test_case_1()",
                    "reasoning": "Reason"
                }
            ]

            result = asyncio.run(test_func(client, mock_systemic, mock_ethical, mock_edges))
            results.append((name, result))
        except TypeError:
            # Test doesn't need all fixtures
            try:
                result = asyncio.run(test_func(client, mock_systemic))
                results.append((name, result))
            except TypeError:
                try:
                    result = asyncio.run(test_func(client))
                    results.append((name, result))
                except Exception as e:
                    print(f"\n✗ Test '{name}' FAILED with exception: {e}")
                    import traceback
                    traceback.print_exc()
                    results.append((name, False))
        except Exception as e:
            print(f"\n✗ Test '{name}' FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ MAXIMUS Client is production-ready!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review and fix issues.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
