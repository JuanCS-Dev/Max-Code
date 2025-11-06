"""
Tests for BaseHTTPClient - Circuit Breaker & Retry Logic

Production-ready testing for resilience patterns.
"""

import sys
import os

# Must add to path BEFORE any other imports
_test_dir = os.path.dirname(os.path.abspath(__file__))
_cli_root = os.path.dirname(os.path.dirname(_test_dir))
if _cli_root not in sys.path:
    sys.path.insert(0, _cli_root)

import pytest
import time
from unittest.mock import Mock, patch, MagicMock


class TestCircuitBreaker:
    """Test circuit breaker pattern."""

    def test_initial_state_closed(self):
        """Circuit breaker starts in CLOSED state."""
        pytest.importorskip("httpx")
        from integration.base_client import CircuitBreaker, CircuitState

        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED
        assert cb._failure_count == 0

    def test_circuit_opens_after_threshold(self):
        """Circuit opens after failure threshold."""
        pytest.importorskip("httpx")
        from integration.base_client import CircuitBreaker, CircuitState

        cb = CircuitBreaker(failure_threshold=2)

        def failing_func():
            raise Exception("Failure")

        # Reach threshold
        for _ in range(2):
            with pytest.raises(Exception):
                cb.call(failing_func)

        assert cb.state == CircuitState.OPEN

        # Next call should fail immediately
        with pytest.raises(Exception, match="Circuit breaker OPEN"):
            cb.call(failing_func)

    def test_circuit_half_open_after_timeout(self):
        """Circuit transitions to HALF_OPEN after recovery timeout."""
        pytest.importorskip("httpx")
        from integration.base_client import CircuitBreaker, CircuitState

        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.1)

        def failing_func():
            raise Exception("Failure")

        # Open circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)

        # Should be HALF_OPEN
        assert cb.state == CircuitState.HALF_OPEN

    def test_successful_call_resets_counter(self):
        """Successful call resets failure counter."""
        pytest.importorskip("httpx")
        from integration.base_client import CircuitBreaker, CircuitState

        cb = CircuitBreaker(failure_threshold=3)

        # Accumulate failures
        for _ in range(2):
            with pytest.raises(Exception):
                cb.call(lambda: (_ for _ in ()).throw(Exception("Fail")))

        assert cb._failure_count == 2

        # Successful call
        result = cb.call(lambda: "success")
        assert result == "success"
        assert cb._failure_count == 0
        assert cb.state == CircuitState.CLOSED


class TestBaseHTTPClient:
    """Test BaseHTTPClient functionality."""

    def test_client_initialization(self):
        """Client initializes with correct defaults."""
        pytest.importorskip("httpx")
        from integration.base_client import BaseHTTPClient, CircuitState

        client = BaseHTTPClient("http://localhost:8150")

        assert client.base_url == "http://localhost:8150"
        assert client.max_retries == 3
        assert client.circuit_breaker.state == CircuitState.CLOSED

        client.close()

    def test_base_url_strips_trailing_slash(self):
        """Base URL trailing slash is removed."""
        pytest.importorskip("httpx")
        from integration.base_client import BaseHTTPClient

        client = BaseHTTPClient("http://localhost:8150/")
        assert client.base_url == "http://localhost:8150"
        client.close()

    def test_context_manager(self):
        """Client works as context manager."""
        pytest.importorskip("httpx")
        from integration.base_client import BaseHTTPClient

        with BaseHTTPClient("http://localhost:8150") as client:
            assert client.base_url == "http://localhost:8150"
        # Client should be closed after exiting context

    @patch('integration.base_client.httpx.Client')
    def test_retry_on_failure(self, mock_httpx_client):
        """Requests retry on failure."""
        httpx = pytest.importorskip("httpx")
        from integration.base_client import BaseHTTPClient

        mock_client_instance = MagicMock()
        mock_httpx_client.return_value = mock_client_instance

        # First 2 attempts fail, 3rd succeeds
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}

        mock_client_instance.request.side_effect = [
            httpx.RequestError("Connection failed"),
            httpx.RequestError("Connection failed"),
            mock_response
        ]

        client = BaseHTTPClient("http://localhost:8150", max_retries=3)

        # Should succeed on 3rd attempt
        response = client.get("/test")
        assert response.status_code == 200

    @patch('integration.base_client.httpx.Client')
    def test_circuit_breaker_integration(self, mock_httpx_client):
        """Circuit breaker triggers on repeated failures."""
        httpx = pytest.importorskip("httpx")
        from integration.base_client import BaseHTTPClient, CircuitBreaker, CircuitState

        mock_client_instance = MagicMock()
        mock_httpx_client.return_value = mock_client_instance

        mock_client_instance.request.side_effect = httpx.RequestError("Connection failed")

        client = BaseHTTPClient("http://localhost:8150", max_retries=1)
        client.circuit_breaker = CircuitBreaker(failure_threshold=2)

        # First request fails
        with pytest.raises(httpx.RequestError):
            client.get("/test")

        # Second request fails and opens circuit
        with pytest.raises(httpx.RequestError):
            client.get("/test")

        assert client.circuit_breaker.state == CircuitState.OPEN

        # Third request fails immediately due to open circuit
        with pytest.raises(Exception, match="Circuit breaker OPEN"):
            client.get("/test")


class TestRetryBehavior:
    """Test retry behavior and timing."""

    @patch('integration.base_client.httpx.Client')
    @patch('time.sleep')
    def test_exponential_backoff(self, mock_sleep, mock_httpx_client):
        """Retry uses exponential backoff."""
        httpx = pytest.importorskip("httpx")
        from integration.base_client import BaseHTTPClient

        mock_client_instance = MagicMock()
        mock_httpx_client.return_value = mock_client_instance

        mock_client_instance.request.side_effect = httpx.RequestError("Fail")

        client = BaseHTTPClient("http://localhost:8150", max_retries=3)

        with pytest.raises(httpx.RequestError):
            client.get("/test")

        # Check exponential backoff: 1s, 2s
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1)  # 2^0
        mock_sleep.assert_any_call(2)  # 2^1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
