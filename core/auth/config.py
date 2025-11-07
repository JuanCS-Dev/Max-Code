"""
OAuth Configuration for Max-Code

Constantes e configurações para autenticação OAuth 2.0 + PKCE com Claude.ai
"""

import os
from pathlib import Path
from typing import Optional


class AuthConfig:
    """Configuração de autenticação OAuth para Max-Code"""

    # ==================== ENDPOINTS ====================

    # Authorization endpoint (onde user faz login)
    # NOTA: Usar console.anthropic.com ao invés de claude.ai para compatibilidade com token exchange
    AUTHORIZATION_URL = "https://console.anthropic.com/oauth/authorize"

    # Token exchange endpoint
    TOKEN_URL = "https://api.anthropic.com/v1/oauth/token"

    # API endpoint
    API_BASE_URL = "https://api.anthropic.com/v1"

    # Redirect URI (servidor local para callback)
    REDIRECT_URI = "http://localhost:5678/callback"

    # ==================== CLIENT ID ====================

    # Client ID público do Claude Code (pode exigir registro próprio)
    # TODO: Registrar client_id próprio com Anthropic (support@anthropic.com)
    CLIENT_ID = "9d1c250a-e61b-44d9-88ed-5944d1962f5e"

    # ==================== SCOPES ====================

    # Scopes OAuth solicitados (Anthropic proprietário)
    # NOTA: Anthropic NÃO aceita scopes OpenID padrão (openid, profile, email)
    # Usa scopes proprietários específicos - baseado em Claude Code oficial
    SCOPES = [
        "user:inference",   # API inference (Claude Pro Max)
        "user:profile",     # Perfil do usuário (Anthropic proprietário)
    ]

    # ==================== TOKEN LIFETIMES ====================

    # Access token válido por ~8-12 horas
    ACCESS_TOKEN_LIFETIME_HOURS = 12

    # Refresh token válido por ~1 ano
    REFRESH_TOKEN_LIFETIME_DAYS = 365

    # Setup token (CI/CD) válido por ~1 ano
    SETUP_TOKEN_LIFETIME_DAYS = 365

    # Margem de segurança para refresh (renovar 5 min antes de expirar)
    REFRESH_MARGIN_SECONDS = 300

    # ==================== STORAGE ====================

    # Diretório de configuração
    CONFIG_DIR = Path.home() / ".max-code"

    # Arquivo de credenciais
    CREDENTIALS_FILE = CONFIG_DIR / ".credentials.json"

    # Permissões do arquivo (apenas owner pode ler/escrever)
    CREDENTIALS_FILE_PERMISSIONS = 0o600

    # ==================== PKCE ====================

    # Tamanho do code_verifier (43-128 caracteres)
    PKCE_VERIFIER_LENGTH = 64

    # Método de challenge (SHA256)
    PKCE_CHALLENGE_METHOD = "S256"

    # ==================== HTTP ====================

    # Porta do servidor local para callback
    CALLBACK_SERVER_PORT = 5678

    # Timeout para aguardar callback (segundos)
    CALLBACK_TIMEOUT = 300  # 5 minutos

    # Timeout para requisições HTTP (segundos)
    HTTP_REQUEST_TIMEOUT = 30

    # User-Agent
    USER_AGENT = "Max-Code-CLI/1.0.0"

    # ==================== VARIÁVEIS DE AMBIENTE ====================

    @staticmethod
    def get_oauth_token_from_env() -> Optional[str]:
        """
        Obtém token OAuth de variável de ambiente (fallback)

        Ordem de prioridade:
        1. CLAUDE_CODE_OAUTH_TOKEN (setup token de longa duração)
        2. MAX_CODE_OAUTH_TOKEN (token específico Max-Code)

        Returns:
            Token OAuth ou None se não encontrado
        """
        return (
            os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") or
            os.environ.get("MAX_CODE_OAUTH_TOKEN")
        )

    @staticmethod
    def get_api_key_from_env() -> Optional[str]:
        """
        Obtém API key de variável de ambiente (fallback de último recurso)

        Returns:
            API key ou None se não encontrado
        """
        return os.environ.get("ANTHROPIC_API_KEY")

    @staticmethod
    def ensure_config_dir():
        """Garante que diretório de configuração existe"""
        AuthConfig.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        # Definir permissões: apenas owner pode acessar
        AuthConfig.CONFIG_DIR.chmod(0o700)

    # ==================== TOKEN PATTERNS ====================

    # Padrões de tokens para validação
    TOKEN_PATTERNS = {
        'access_token': r'^sk-ant-oat01-[A-Za-z0-9_-]{90,}$',
        'refresh_token': r'^sk-ant-ort01-[A-Za-z0-9_-]{90,}$',
        'setup_token': r'^sk-ant-oat01-[A-Za-z0-9_-]{90,}$',
    }

    # ==================== PRIORIDADE DE AUTENTICAÇÃO ====================

    @staticmethod
    def get_auth_priority_description() -> str:
        """
        Retorna descrição da ordem de prioridade de autenticação

        Ordem (conforme Claude Code):
        1. OAuth token (arquivo ~/.max-code/.credentials.json)
        2. Setup token (variável CLAUDE_CODE_OAUTH_TOKEN)
        3. API key (variável ANTHROPIC_API_KEY)
        4. Prompt para login OAuth
        """
        return """
Max-Code Authentication Priority:

1. OAuth Token (HIGHEST PRIORITY)
   - File: ~/.max-code/.credentials.json
   - Auto-refresh: Yes
   - Lifetime: ~12 hours (access) / ~1 year (refresh)

2. Setup Token (MEDIUM PRIORITY)
   - Environment: CLAUDE_CODE_OAUTH_TOKEN
   - Use case: CI/CD, automation
   - Lifetime: ~1 year

3. API Key (LOW PRIORITY - FALLBACK)
   - Environment: ANTHROPIC_API_KEY
   - Use case: When OAuth not available
   - Note: Consumes API credits

4. Interactive Login (LAST RESORT)
   - Command: max-code login
   - Opens browser for OAuth flow
   - Stores tokens in ~/.max-code/.credentials.json
"""

    # ==================== MESSAGES ====================

    LOGIN_PROMPT_MESSAGE = """
╔═══════════════════════════════════════════════════════════════╗
║              MAX-CODE AUTHENTICATION REQUIRED                  ║
╚═══════════════════════════════════════════════════════════════╝

No valid authentication found.

Please choose one of the following options:

1. Login with Claude.ai account (RECOMMENDED):
   $ max-code login

   This will:
   - Open browser for Claude.ai login
   - Use your Claude Pro/Max subscription
   - Store tokens securely in ~/.max-code/.credentials.json
   - Auto-refresh tokens automatically

2. Use setup token (for CI/CD):
   $ claude setup-token
   $ export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."

3. Use API key (consumes credits):
   $ export ANTHROPIC_API_KEY="sk-ant-api..."

After authentication, run your command again.
"""

    LOGIN_SUCCESS_MESSAGE = """
╔═══════════════════════════════════════════════════════════════╗
║              AUTHENTICATION SUCCESSFUL!                        ║
╚═══════════════════════════════════════════════════════════════╝

✅ Tokens stored in: {credentials_file}
✅ Access token valid for: ~{access_hours} hours
✅ Refresh token valid for: ~{refresh_days} days
✅ Auto-refresh: ENABLED

You can now use Max-Code CLI with your Claude Pro/Max subscription.

Example commands:
  $ max-code ask "Implement user authentication"
  $ max-code fix "Bug in login endpoint"
  $ max-code commit

To check authentication status:
  $ max-code auth status
"""

    TOKEN_REFRESH_MESSAGE = """
🔄 Refreshing access token...
   (Your session will continue uninterrupted)
"""

    TOKEN_EXPIRED_MESSAGE = """
⚠️  Your refresh token has expired (~1 year lifetime).
    Please login again:

    $ max-code login
"""


# ==================== HELPER FUNCTIONS ====================

def get_credentials_file_path() -> Path:
    """Retorna caminho do arquivo de credenciais"""
    return AuthConfig.CREDENTIALS_FILE


def get_config_dir() -> Path:
    """Retorna diretório de configuração"""
    return AuthConfig.CONFIG_DIR


def is_oauth_token(token: str) -> bool:
    """Verifica se string é um token OAuth válido"""
    import re
    patterns = AuthConfig.TOKEN_PATTERNS.values()
    return any(re.match(pattern, token) for pattern in patterns)


def is_api_key(key: str) -> bool:
    """Verifica se string é uma API key válida"""
    import re
    pattern = r'^sk-ant-api\d{2}-[A-Za-z0-9_-]{95}$'
    return bool(re.match(pattern, key))
