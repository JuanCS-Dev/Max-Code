"""
Unified LLM Client with Gemini Fallback

Tries Claude first, falls back to Gemini if Claude fails (credits, rate limits, etc)

Constitutional AI v3.0 Compliant
"""

from typing import Optional, Iterator, Dict, Any
from anthropic import Anthropic
import google.generativeai as genai
import os
from dotenv import load_dotenv
from config.logging_config import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


class UnifiedLLMClient:
    """
    LLM Client with automatic fallback: Claude → Gemini

    Provides transparent fallback when Claude API fails:
    - Credit balance too low
    - Rate limits exceeded
    - Network errors
    - Any other API errors

    Falls back to Gemini 2.5 Flash automatically.
    """

    def __init__(
        self,
        claude_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        prefer_claude: bool = True,
        model_claude: str = "claude-sonnet-4-20250514",
        model_gemini: str = "gemini-2.5-flash",
        max_tokens: int = 4096,
        temperature: float = 1.0
    ):
        """
        Initialize unified LLM client

        Args:
            claude_api_key: Anthropic API key (or from ANTHROPIC_API_KEY env)
            gemini_api_key: Google Gemini API key (or from GEMINI_API_KEY env)
            prefer_claude: Try Claude first if True (default)
            model_claude: Claude model to use
            model_gemini: Gemini model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        """
        self.prefer_claude = prefer_claude
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Initialize Claude
        self.claude_api_key = claude_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model_claude = model_claude
        self.claude_client = None
        self.claude_available = False

        if self.claude_api_key:
            try:
                self.claude_client = Anthropic(api_key=self.claude_api_key)
                self.claude_available = True
                logger.info("✅ Claude client initialized")
            except Exception as e:
                logger.warning(f"⚠️  Claude initialization failed: {e}")

        # Initialize Gemini
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.model_gemini = model_gemini
        self.gemini_client = None
        self.gemini_available = False

        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_client = genai.GenerativeModel(model_name=self.model_gemini)
                self.gemini_available = True
                logger.info("✅ Gemini client initialized")
            except Exception as e:
                logger.warning(f"⚠️  Gemini initialization failed: {e}")

        if not self.claude_available and not self.gemini_available:
            logger.error("❌ No LLM provider available! Configure ANTHROPIC_API_KEY or GEMINI_API_KEY")

    def chat(
        self,
        message: str,
        stream: bool = False,
        system: Optional[str] = None,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Send message to LLM with automatic fallback

        Tries providers in order (Claude first by default), falls back on error.

        Args:
            message: User message
            stream: Whether to stream response
            system: Optional system prompt
            **kwargs: Additional parameters

        Returns:
            Response string (or iterator if streaming)
        """
        # 🔥 BORIS FIX: Streaming requires resilient generator wrapper
        if stream:
            return self._resilient_stream(message, system=system, **kwargs)

        # Non-streaming: original logic (works fine)
        providers = self._get_provider_order()

        for provider_name, provider_func in providers:
            try:
                logger.info(f"🔄 Trying {provider_name}...")
                result = provider_func(message, stream=False, system=system, **kwargs)
                logger.info(f"✅ {provider_name} succeeded")
                return result
            except Exception as e:
                logger.warning(f"⚠️  {provider_name} failed: {e}")

                # Check if it's a credit/billing error
                error_str = str(e).lower()
                if "credit" in error_str or "balance" in error_str or "billing" in error_str:
                    logger.warning(f"💳 {provider_name} has billing issues, trying fallback...")

                # Try next provider
                continue

        # All providers failed
        raise RuntimeError(
            "❌ All LLM providers failed! "
            f"Claude available: {self.claude_available}, "
            f"Gemini available: {self.gemini_available}"
        )

    def _get_provider_order(self) -> list[tuple[str, callable]]:
        """Get ordered list of providers to try"""
        providers = []

        if self.prefer_claude:
            if self.claude_available:
                providers.append(("Claude", self._chat_claude))
            if self.gemini_available:
                providers.append(("Gemini", self._chat_gemini))
        else:
            if self.gemini_available:
                providers.append(("Gemini", self._chat_gemini))
            if self.claude_available:
                providers.append(("Claude", self._chat_claude))

        return providers

    def _resilient_stream(
        self,
        message: str,
        system: Optional[str] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        🔥 BORIS FIX: Resilient streaming with mid-stream fallback

        The problem: Generators fail DURING iteration, not at creation.
        The solution: Wrap iteration, catch errors, seamlessly switch providers.

        Philosophy: "Users should never see provider failures. That's our job."
        """
        providers = self._get_provider_order()

        for provider_name, provider_func in providers:
            try:
                logger.debug(f"🔄 Streaming from {provider_name}...")

                # Get the generator
                stream_gen = provider_func(message, stream=True, system=system, **kwargs)

                # Iterate and yield - this is where Claude may fail
                for chunk in stream_gen:
                    yield chunk

                # Success! No need to try other providers
                logger.debug(f"✅ {provider_name} streaming completed")
                return

            except Exception as e:
                # Log silently (as Boris intended - no user-facing errors!)
                error_str = str(e).lower()

                if "credit" in error_str or "balance" in error_str:
                    logger.info(f"💳 {provider_name} credits exhausted, trying fallback...")
                else:
                    logger.debug(f"⚠️  {provider_name} stream failed: {e}")

                # Try next provider
                continue

        # All providers failed - now we must tell the user
        logger.error("❌ All streaming providers failed")
        yield "\n\n[System: All LLM providers are currently unavailable. Please try again later.]"

    def _chat_claude(
        self,
        message: str,
        stream: bool = False,
        system: Optional[str] = None,
        **kwargs
    ) -> str | Iterator[str]:
        """Chat using Claude"""
        messages = [{"role": "user", "content": message}]

        params = {
            "model": kwargs.get("model", self.model_claude),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": messages,
        }

        if system:
            params["system"] = system

        if stream:
            return self._stream_claude(params)
        else:
            response = self.claude_client.messages.create(**params)
            if response.content and len(response.content) > 0:
                return response.content[0].text
            return ""

    def _stream_claude(self, params: dict) -> Iterator[str]:
        """Stream response from Claude"""
        with self.claude_client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                yield text

    def _chat_gemini(
        self,
        message: str,
        stream: bool = False,
        system: Optional[str] = None,
        **kwargs
    ) -> str | Iterator[str]:
        """Chat using Gemini"""
        # Combine system + user message for Gemini
        full_message = message
        if system:
            full_message = f"{system}\n\n{message}"

        generation_config = genai.GenerationConfig(
            max_output_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature)
        )

        # Permissive safety settings for research
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]

        if stream:
            return self._stream_gemini(full_message, generation_config, safety_settings)
        else:
            response = self.gemini_client.generate_content(
                full_message,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            try:
                return response.text
            except ValueError as e:
                raise RuntimeError(f"Gemini content blocked or empty: {e}")

    def _stream_gemini(
        self,
        message: str,
        generation_config,
        safety_settings
    ) -> Iterator[str]:
        """Stream response from Gemini"""
        response = self.gemini_client.generate_content(
            message,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True
        )

        for chunk in response:
            try:
                yield chunk.text
            except ValueError:
                # Skip blocked chunks
                continue

    def chat_with_history(
        self,
        messages: list[Dict[str, str]],
        stream: bool = False,
        system: Optional[str] = None,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Chat with conversation history

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream response
            system: Optional system prompt
            **kwargs: Additional parameters

        Returns:
            Response (complete or streaming)
        """
        providers = self._get_provider_order()

        for provider_name, _ in providers:
            try:
                if provider_name == "Claude":
                    return self._chat_history_claude(messages, stream, system, **kwargs)
                elif provider_name == "Gemini":
                    return self._chat_history_gemini(messages, stream, system, **kwargs)
            except Exception as e:
                logger.warning(f"⚠️  {provider_name} history chat failed: {e}")
                continue

        raise RuntimeError("❌ All providers failed for history chat")

    def _chat_history_claude(
        self,
        messages: list[Dict[str, str]],
        stream: bool,
        system: Optional[str],
        **kwargs
    ) -> str | Iterator[str]:
        """Chat with history using Claude"""
        params = {
            "model": kwargs.get("model", self.model_claude),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": messages,
        }

        if system:
            params["system"] = system

        if stream:
            with self.claude_client.messages.stream(**params) as stream:
                for text in stream.text_stream:
                    yield text
        else:
            response = self.claude_client.messages.create(**params)
            if response.content and len(response.content) > 0:
                return response.content[0].text
            return ""

    def _chat_history_gemini(
        self,
        messages: list[Dict[str, str]],
        stream: bool,
        system: Optional[str],
        **kwargs
    ) -> str | Iterator[str]:
        """Chat with history using Gemini"""
        # Convert messages to Gemini format
        # Gemini doesn't have native message history, so concatenate
        conversation = []
        if system:
            conversation.append(system)

        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            conversation.append(f"{role.upper()}: {content}")

        full_message = "\n\n".join(conversation)

        return self._chat_gemini(full_message, stream=stream, **kwargs)

    def get_active_provider(self) -> str:
        """Get name of active provider"""
        if self.prefer_claude and self.claude_available:
            return "Claude"
        elif self.gemini_available:
            return "Gemini"
        elif self.claude_available:
            return "Claude"
        return "None"

    def health_check(self) -> Dict[str, bool]:
        """
        Check health of all providers

        Returns:
            Dict with provider availability
        """
        status = {
            "claude": False,
            "gemini": False
        }

        # Test Claude
        if self.claude_available:
            try:
                response = self.claude_client.messages.create(
                    model=self.model_claude,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "test"}]
                )
                status["claude"] = response is not None
            except Exception as e:
                logger.debug(f"Claude health check failed: {e}")

        # Test Gemini
        if self.gemini_available:
            try:
                response = self.gemini_client.generate_content("test")
                status["gemini"] = response is not None
            except Exception as e:
                logger.debug(f"Gemini health check failed: {e}")

        return status


def create_unified_client(**kwargs) -> UnifiedLLMClient:
    """
    Factory function to create UnifiedLLMClient

    Args:
        **kwargs: Arguments passed to UnifiedLLMClient constructor

    Returns:
        Configured UnifiedLLMClient instance
    """
    return UnifiedLLMClient(**kwargs)


# Example usage
if __name__ == "__main__":
    # Test unified client with fallback
    client = UnifiedLLMClient()

    print(f"Active provider: {client.get_active_provider()}")

    # Test chat
    try:
        response = client.chat("Hello! What's 2+2?")
        print(f"\nResponse: {response}")
    except Exception as e:
        print(f"Error: {e}")

    # Health check
    health = client.health_check()
    print(f"\nHealth: {health}")
