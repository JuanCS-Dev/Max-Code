"""
Authenticated HTTP Client for Max-Code

Cliente HTTP que automaticamente:
1. Injeta Bearer token OAuth em todas as requisições
2. Detecta 401 e dispara token refresh automático
3. Retry automático após refresh
4. Fallback para API key se OAuth não disponível

USO LEGÍTIMO: Este cliente é para usar sua própria conta Claude Pro/Max x20
que você PAGA, sem consumir créditos de API.
"""

import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import AuthConfig
from .token_manager import get_token_manager
from .credentials import CredentialsManager


class AuthenticatedHTTPClient:
    """
    Cliente HTTP com autenticação OAuth automática

    Features:
    - Injeta Bearer token automaticamente
    - Auto-refresh em caso de 401
    - Retry logic
    - Fallback para API key
    - Thread-safe
    """

    def __init__(self, base_url: Optional[str] = None):
        """
        Inicializa cliente HTTP

        Args:
            base_url: URL base da API (default: Anthropic API)
        """
        self.base_url = base_url or AuthConfig.API_BASE_URL
        self.token_manager = get_token_manager()
        self.credentials_manager = CredentialsManager()

        # Session com retry logic
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        Cria session HTTP com retry logic

        Returns:
            requests.Session configurada
        """
        session = requests.Session()

        # Retry strategy
        retry_strategy = Retry(
            total=3,  # 3 tentativas
            backoff_factor=1,  # Exponential backoff: 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],  # Retry nestes status
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # User-Agent
        session.headers.update({
            'User-Agent': AuthConfig.USER_AGENT
        })

        return session

    def _get_auth_header(self) -> Optional[Dict[str, str]]:
        """
        Obtém header de autenticação

        Ordem de prioridade:
        1. OAuth token (do arquivo ~/.max-code/.credentials.json)
        2. Setup token (env var CLAUDE_CODE_OAUTH_TOKEN)
        3. API key (env var ANTHROPIC_API_KEY)

        Returns:
            Dict com Authorization header ou None
        """
        # 1. OAuth token (PRIORIDADE MÁXIMA)
        oauth_token = self.token_manager.get_valid_token()
        if oauth_token:
            return {'Authorization': f'Bearer {oauth_token}'}

        # 2. Setup token (env var)
        setup_token = AuthConfig.get_oauth_token_from_env()
        if setup_token:
            return {'Authorization': f'Bearer {setup_token}'}

        # 3. API key (FALLBACK)
        api_key = AuthConfig.get_api_key_from_env()
        if api_key:
            return {'x-api-key': api_key}

        return None

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Faz requisição HTTP com autenticação

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: Endpoint (ex: /v1/messages)
            **kwargs: Argumentos adicionais para requests

        Returns:
            requests.Response

        Raises:
            requests.HTTPError: Se autenticação falhar após retry
            ValueError: Se sem autenticação disponível
        """
        # Construir URL completa
        url = f"{self.base_url}{endpoint}"

        # Obter auth header
        auth_header = self._get_auth_header()
        if not auth_header:
            raise ValueError(
                "No authentication available. "
                "Please run 'max-code login' or set ANTHROPIC_API_KEY"
            )

        # Merge headers
        headers = kwargs.get('headers', {})
        headers.update(auth_header)
        kwargs['headers'] = headers

        # Primeira tentativa
        response = self.session.request(method, url, **kwargs)

        # Se 401, tentar refresh e retry uma vez
        if response.status_code == 401 and 'Bearer' in auth_header.get('Authorization', ''):
            # Token OAuth expirado - tentar refresh
            print("⚠️  Access token expired, refreshing...")

            refresh_success = self.token_manager.force_refresh()

            if refresh_success:
                # Retry com novo token
                auth_header = self._get_auth_header()
                if auth_header:
                    headers.update(auth_header)
                    kwargs['headers'] = headers

                    response = self.session.request(method, url, **kwargs)

        # Raise para status de erro (exceto se for esperado pelo caller)
        if not kwargs.get('allow_errors', False):
            response.raise_for_status()

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET request"""
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST request"""
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT request"""
        return self.request('PUT', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """PATCH request"""
        return self.request('PATCH', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        return self.request('DELETE', endpoint, **kwargs)

    def send_message(
        self,
        messages: list,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 8192,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Envia mensagem para Claude API

        IMPORTANTE: Usa OAuth token do seu plano Claude Max x20,
        NÃO consome créditos de API.

        Args:
            messages: Lista de mensagens no formato Claude
            model: Modelo a usar (default: Sonnet 4.5)
            max_tokens: Máximo de tokens na resposta
            **kwargs: Argumentos adicionais

        Returns:
            Resposta da API (JSON)
        """
        payload = {
            'model': model,
            'messages': messages,
            'max_tokens': max_tokens,
            **kwargs
        }

        response = self.post('/messages', json=payload)
        return response.json()


# ==================== SINGLETON INSTANCE ====================

_http_client_instance: Optional[AuthenticatedHTTPClient] = None


def get_http_client() -> AuthenticatedHTTPClient:
    """
    Obtém instância singleton do HTTP client

    Returns:
        AuthenticatedHTTPClient instance
    """
    global _http_client_instance

    if _http_client_instance is None:
        _http_client_instance = AuthenticatedHTTPClient()

    return _http_client_instance


def send_claude_message(
    messages: list,
    model: str = "claude-sonnet-4-5-20250929",
    **kwargs
) -> Dict[str, Any]:
    """
    Helper function para enviar mensagem ao Claude

    Usa OAuth token do seu plano Claude Max x20 (SEM consumir API credits)

    Args:
        messages: Lista de mensagens
        model: Modelo (default: Sonnet 4.5)
        **kwargs: Argumentos adicionais

    Returns:
        Resposta da API
    """
    client = get_http_client()
    return client.send_message(messages, model=model, **kwargs)


# ==================== EXEMPLO DE USO ====================

if __name__ == "__main__":
    """
    Exemplo de uso do HTTP client

    LEGÍTIMO: Este exemplo usa SEU plano Claude Max x20 que você paga,
    sem consumir créditos de API.
    """

    # Criar cliente
    client = get_http_client()

    # Exemplo de mensagem
    messages = [
        {
            "role": "user",
            "content": "Hello! Can you help me with Python code?"
        }
    ]

    try:
        # Enviar mensagem (usa OAuth token automaticamente)
        response = client.send_message(messages, model="claude-sonnet-4-5-20250929")

        print("Response:")
        print(response['content'][0]['text'])

    except ValueError as e:
        print(f"Authentication error: {e}")
        print("\nPlease run: max-code login")

    except Exception as e:
        print(f"Error: {e}")
