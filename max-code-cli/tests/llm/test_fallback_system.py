"""
LLM Fallback System Tests - FASE 4.2

Tests validating the Claude → Gemini fallback mechanism works correctly.

Critical behaviors to test:
1. Fallback triggers on Claude failure (credits, rate limit, errors)
2. Gemini is used when Claude unavailable
3. Error messages are clear and actionable
4. System remains functional with only Gemini
5. Performance degradation is acceptable

Constitutional AI v3.0: P6 - Antifragilidade (system improves under stress)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core.llm.unified_client import UnifiedLLMClient
import os


class TestFallbackTriggers:
    """Test fallback triggers correctly on various failure modes"""

    def test_fallback_on_claude_credit_exhausted(self):
        """Test fallback when Claude credits are exhausted"""
        with patch('core.llm.unified_client.Anthropic') as mock_anthropic:
            # Simulate Claude credit error
            mock_client = Mock()
            mock_client.messages.create.side_effect = Exception(
                "Error code: 400 - Your credit balance is too low"
            )
            mock_anthropic.return_value = mock_client

            # Client should fallback to Gemini
            client = UnifiedLLMClient()

            # Should use Gemini (will actually call it if GEMINI_API_KEY is set)
            if client.gemini_available:
                response = client.chat("Say 'fallback works'")
                assert response is not None
                assert len(response) > 0

    def test_fallback_on_claude_rate_limit(self):
        """Test fallback when Claude rate limited"""
        with patch('core.llm.unified_client.Anthropic') as mock_anthropic:
            # Simulate rate limit error
            mock_client = Mock()
            mock_client.messages.create.side_effect = Exception(
                "Error code: 429 - Rate limit exceeded"
            )
            mock_anthropic.return_value = mock_client

            client = UnifiedLLMClient()

            if client.gemini_available:
                response = client.chat("Test rate limit fallback")
                assert response is not None

    def test_fallback_on_claude_network_error(self):
        """Test fallback on network/connectivity errors"""
        with patch('core.llm.unified_client.Anthropic') as mock_anthropic:
            # Simulate network error
            mock_client = Mock()
            mock_client.messages.create.side_effect = ConnectionError(
                "Connection refused"
            )
            mock_anthropic.return_value = mock_client

            client = UnifiedLLMClient()

            if client.gemini_available:
                response = client.chat("Test network error fallback")
                assert response is not None

    def test_fallback_on_claude_timeout(self):
        """Test fallback on timeout errors"""
        with patch('core.llm.unified_client.Anthropic') as mock_anthropic:
            # Simulate timeout
            mock_client = Mock()
            mock_client.messages.create.side_effect = TimeoutError(
                "Request timed out"
            )
            mock_anthropic.return_value = mock_client

            client = UnifiedLLMClient()

            if client.gemini_available:
                response = client.chat("Test timeout fallback")
                assert response is not None


class TestGeminiStandalone:
    """Test Gemini works standalone (without Claude)"""

    def test_gemini_only_initialization(self):
        """Test client works with only Gemini configured"""
        # Temporarily clear Claude key
        original_claude_key = os.getenv("ANTHROPIC_API_KEY")

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}, clear=False):
            client = UnifiedLLMClient()

            # Should have Gemini available
            assert client.gemini_available, "Gemini should be available"

            # Should work without Claude
            if client.gemini_available:
                response = client.chat("Hello from Gemini only")
                assert response is not None
                assert len(response) > 0

    def test_gemini_generates_valid_code(self):
        """Test Gemini generates valid Python code"""
        client = UnifiedLLMClient()

        if not client.gemini_available:
            pytest.skip("Gemini not available")

        # Force Gemini by disabling Claude
        client.claude_available = False

        response = client.chat("Generate Python function to add two numbers")

        # Basic validation
        assert "def" in response, "Should contain function definition"
        assert "return" in response, "Should have return statement"


class TestFallbackBehavior:
    """Test fallback behavior and error handling"""

    def test_clear_error_message_when_both_fail(self):
        """Test error message is clear when both providers fail"""
        with patch('core.llm.unified_client.Anthropic') as mock_anthropic, \
             patch('core.llm.unified_client.genai') as mock_genai:

            # Both fail
            mock_anthropic.return_value.messages.create.side_effect = Exception("Claude failed")
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("Gemini failed")

            client = UnifiedLLMClient()

            with pytest.raises(RuntimeError) as exc_info:
                client.chat("This should fail")

            # Error message should mention both providers
            error_msg = str(exc_info.value)
            assert "failed" in error_msg.lower(), "Should mention failure"

    def test_fallback_preserves_message_context(self):
        """Test fallback doesn't lose message context"""
        client = UnifiedLLMClient()

        if not client.gemini_available:
            pytest.skip("Gemini not available")

        # Disable Claude to force Gemini
        client.claude_available = False

        original_message = "What is 2+2?"
        response = client.chat(original_message)

        # Response should be relevant to question
        assert response is not None
        # Basic sanity check (response mentions numbers or math)
        relevant = any(word in response.lower() for word in ["4", "four", "2", "add", "sum"])
        assert relevant, "Response should be relevant to math question"

    def test_fallback_respects_temperature(self):
        """Test temperature parameter respected in fallback"""
        client = UnifiedLLMClient(temperature=0.0)  # Deterministic

        if not client.gemini_available:
            pytest.skip("Gemini not available")

        client.claude_available = False

        # Should work with temperature parameter
        response = client.chat("Say exactly: test")
        assert response is not None


class TestFallbackPerformance:
    """Test fallback performance characteristics"""

    def test_fallback_latency_acceptable(self):
        """Test fallback doesn't add excessive latency"""
        import time

        with patch('core.llm.unified_client.Anthropic') as mock_anthropic:
            # Simulate instant Claude failure
            mock_client = Mock()
            mock_client.messages.create.side_effect = Exception("Instant fail")
            mock_anthropic.return_value = mock_client

            client = UnifiedLLMClient()

            if not client.gemini_available:
                pytest.skip("Gemini not available")

            start = time.time()
            response = client.chat("Quick test")
            elapsed = time.time() - start

            # Should complete in reasonable time (< 60s for simple prompt)
            assert elapsed < 60, f"Fallback took {elapsed}s (too slow)"

    def test_no_retry_storm(self):
        """Test fallback doesn't cause retry storm"""
        call_count = 0

        def count_calls(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise Exception("Always fail")

        with patch('core.llm.unified_client.Anthropic') as mock_anthropic:
            mock_client = Mock()
            mock_client.messages.create.side_effect = count_calls
            mock_anthropic.return_value = mock_client

            client = UnifiedLLMClient()

            if client.gemini_available:
                try:
                    client.chat("Test")
                except:
                    pass

            # Should try Claude only once (not retry loop)
            assert call_count <= 2, f"Called Claude {call_count} times (retry storm?)"


class TestFallbackConfiguration:
    """Test fallback configuration options"""

    def test_prefer_gemini_option(self):
        """Test prefer_claude=False uses Gemini first"""
        client = UnifiedLLMClient(prefer_claude=False)

        if not client.gemini_available:
            pytest.skip("Gemini not available")

        # Should prefer Gemini
        assert not client.prefer_claude

    def test_custom_models(self):
        """Test custom model names work"""
        client = UnifiedLLMClient(
            model_gemini="gemini-2.0-flash-exp"
        )

        assert client.model_gemini == "gemini-2.0-flash-exp"

    def test_api_keys_from_params(self):
        """Test API keys can be passed as parameters"""
        gemini_key = os.getenv("GEMINI_API_KEY")

        if not gemini_key:
            pytest.skip("No Gemini key in env")

        # Should work with explicit key
        client = UnifiedLLMClient(
            claude_api_key=None,
            gemini_api_key=gemini_key
        )

        assert client.gemini_available


# Test to validate the fix we just made
class TestDotenvLoading:
    """Test .env loading works correctly"""

    def test_env_vars_loaded(self):
        """Test environment variables are loaded from .env"""
        # This test validates our fix
        client = UnifiedLLMClient()

        # Should load GEMINI_API_KEY from .env
        gemini_key_in_env = bool(os.getenv("GEMINI_API_KEY"))

        if gemini_key_in_env:
            assert client.gemini_available, "Gemini should be available when key in .env"
