"""
Max-Code Authentication Module

Implementa autenticação OAuth 2.0 + PKCE para usar Claude Pro/Max sem API keys.
Baseado na investigação completa do Claude Code authentication system.

Modules:
- config: Configurações e constantes OAuth
- oauth: Fluxo OAuth 2.0 + PKCE
- credentials: Armazenamento seguro de tokens
- token_manager: Auto-refresh de tokens
- http_client: Cliente HTTP com Bearer token
"""

from .config import AuthConfig
from .oauth import OAuthFlow
from .credentials import CredentialsManager
from .token_manager import TokenManager
from .http_client import AuthenticatedHTTPClient

__all__ = [
    'AuthConfig',
    'OAuthFlow',
    'CredentialsManager',
    'TokenManager',
    'AuthenticatedHTTPClient',
]
