"""
Unified Claude API client for MAX-CODE CLI.

Provides high-level interface for Claude interactions with streaming support.
"""

from typing import Optional, Iterator, Dict, Any
from anthropic import Anthropic
from core.auth.oauth_handler import get_anthropic_client, CredentialType, validate_credentials


class ClaudeClient:
    """
    Unified client for Claude API interactions.

    Handles authentication, streaming, and response formatting automatically.
    """

    DEFAULT_MODEL = "claude-sonnet-4"
    DEFAULT_MAX_TOKENS = 4096

    def __init__(
        self,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 1.0
    ):
        """
        Initialize Claude client.

        Args:
            model: Claude model to use (default: claude-sonnet-4)
            max_tokens: Maximum tokens in response (default: 4096)
            temperature: Sampling temperature (default: 1.0)
        """
        self.client = get_anthropic_client()
        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS
        self.temperature = temperature

        # Verificar tipo de credencial usando validate_credentials()
        _, cred_type, _ = validate_credentials()
        self.credential_type = cred_type

    def chat(
        self,
        message: str,
        stream: bool = False,
        system: Optional[str] = None,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Send message to Claude and get response.

        Args:
            message: User message to send
            stream: Whether to stream response (default: False)
            system: Optional system prompt
            **kwargs: Additional parameters for Claude API

        Returns:
            Complete response string if stream=False, iterator if stream=True
        """
        if stream:
            return self._stream_response(message, system=system, **kwargs)
        return self._get_response(message, system=system, **kwargs)

    def _stream_response(
        self,
        message: str,
        system: Optional[str] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream response from Claude.

        Yields:
            Text chunks as they arrive
        """
        messages = [{"role": "user", "content": message}]

        # Construir parâmetros
        params = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": messages,
        }

        # Adicionar system prompt se fornecido
        if system:
            params["system"] = system

        # Stream response
        with self.client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                yield text

    def _get_response(
        self,
        message: str,
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Get complete response from Claude.

        Returns:
            Complete response text
        """
        messages = [{"role": "user", "content": message}]

        # Construir parâmetros
        params = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": messages,
        }

        # Adicionar system prompt se fornecido
        if system:
            params["system"] = system

        # Get response
        response = self.client.messages.create(**params)

        # Extrair texto da resposta
        if response.content and len(response.content) > 0:
            return response.content[0].text
        return ""

    def chat_with_history(
        self,
        messages: list[Dict[str, str]],
        stream: bool = False,
        system: Optional[str] = None,
        **kwargs
    ) -> str | Iterator[str]:
        """
        Chat with conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream response
            system: Optional system prompt
            **kwargs: Additional parameters

        Returns:
            Response (complete or streaming)
        """
        # Construir parâmetros
        params = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": messages,
        }

        # Adicionar system prompt se fornecido
        if system:
            params["system"] = system

        if stream:
            with self.client.messages.stream(**params) as stream:
                for text in stream.text_stream:
                    yield text
        else:
            response = self.client.messages.create(**params)
            if response.content and len(response.content) > 0:
                return response.content[0].text
            return ""

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Aproximação: ~4 caracteres por token
        return len(text) // 4

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about current model configuration.

        Returns:
            Dict with model, max_tokens, temperature, credential_type
        """
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "credential_type": self.credential_type.value if self.credential_type else "none",
        }

    def health_check(self) -> bool:
        """
        Check if Claude API is accessible.

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Tentar uma requisição simples
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return response is not None
        except Exception as e:
            print(f"Health check failed: {e}")
            return False


def create_client(**kwargs) -> ClaudeClient:
    """
    Factory function to create ClaudeClient instance.

    Args:
        **kwargs: Arguments passed to ClaudeClient constructor

    Returns:
        Configured ClaudeClient instance
    """
    return ClaudeClient(**kwargs)
