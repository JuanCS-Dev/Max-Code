"""
OAuth Token to API Key Converter

Converte OAuth tokens do Claude Pro Max (sk-ant-oat01-...) em API keys permanentes
(sk-ant-api03-...) usando o endpoint oficial do Claude Code.

DESCOBERTA CRÍTICA (Engenharia Reversa Claude Code):
- OAuth tokens NÃO funcionam diretamente com api.anthropic.com/v1/messages
- Claude Code converte OAuth → API Key via endpoint específico
- Endpoint: POST /api/oauth/claude_cli/create_api_key
- Header: Authorization: Bearer {oauth_token}

Fluxo:
1. User faz OAuth login → recebe sk-ant-oat01-...
2. Converter chama endpoint → recebe sk-ant-api03-...
3. API key é permanente e funciona com API Claude

Biblical Foundation:
"Convertei-vos e vivei" (Ezequiel 18:32)
Transformação gera vida funcional.
"""

import requests
from typing import Optional, Dict
from pathlib import Path
from config.logging_config import get_logger

logger = get_logger(__name__)


class TokenConverter:
    """
    Conversor de OAuth tokens para API keys

    Baseado em engenharia reversa do Claude Code oficial.
    """

    # Endpoint descoberto via reverse engineering
    CREATE_API_KEY_ENDPOINT = "https://api.anthropic.com/api/oauth/claude_cli/create_api_key"
    ROLES_ENDPOINT = "https://api.anthropic.com/api/oauth/claude_cli/roles"

    # Timeout para requests
    REQUEST_TIMEOUT = 30

    @staticmethod
    def convert_oauth_to_api_key(
        oauth_token: str,
        name: Optional[str] = "max-code-cli"
    ) -> Optional[str]:
        """
        Converte OAuth token (sk-ant-oat01-...) em API key (sk-ant-api03-...)

        Args:
            oauth_token: OAuth access token do Claude Pro Max
            name: Nome para identificar a API key (opcional)

        Returns:
            API key permanente (sk-ant-api03-...) ou None se falhar

        Example:
            >>> oauth_token = "sk-ant-oat01-..."
            >>> api_key = TokenConverter.convert_oauth_to_api_key(oauth_token)
            >>> print(api_key)
            sk-ant-api03-...

        Raises:
            requests.RequestException: Se request falhar
        """
        logger.info("🔄 Converting OAuth token to API key...")

        # Validar formato do token
        if not oauth_token.startswith("sk-ant-oat01-"):
            logger.error(f"❌ Invalid OAuth token format: {oauth_token[:20]}...")
            logger.info("   Expected: sk-ant-oat01-...")
            return None

        try:
            # Headers conforme Claude Code oficial
            headers = {
                "Authorization": f"Bearer {oauth_token}",
                "Content-Type": "application/json",
                "User-Agent": "max-code-cli/1.0.0"
            }

            # Body (pode ser vazio ou conter metadata)
            body = {}
            if name:
                body["name"] = name

            # POST request para criar API key
            logger.debug(f"POST {TokenConverter.CREATE_API_KEY_ENDPOINT}")
            response = requests.post(
                TokenConverter.CREATE_API_KEY_ENDPOINT,
                headers=headers,
                json=body,
                timeout=TokenConverter.REQUEST_TIMEOUT
            )

            # Verificar response
            if response.status_code == 200:
                data = response.json()
                api_key = data.get("api_key")

                if api_key:
                    logger.info("✅ OAuth token converted successfully!")
                    logger.info(f"   API Key: {api_key[:20]}...")
                    return api_key
                else:
                    logger.error("❌ API key not found in response")
                    logger.debug(f"Response: {data}")
                    return None

            elif response.status_code == 401:
                logger.error("❌ OAuth token invalid or expired")
                logger.info("   Run: max-code auth login")
                return None

            elif response.status_code == 403:
                logger.error("❌ Insufficient permissions")
                logger.info("   OAuth token lacks 'org:create_api_key' scope")
                return None

            else:
                logger.error(f"❌ Conversion failed: HTTP {response.status_code}")
                logger.debug(f"Response: {response.text}")
                return None

        except requests.RequestException as e:
            logger.error(f"❌ Network error during conversion: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error during conversion: {e}")
            return None

    @staticmethod
    def verify_oauth_roles(oauth_token: str) -> Optional[Dict]:
        """
        Verifica roles/permissões do OAuth token

        Útil para debugging e validação de scopes.

        Args:
            oauth_token: OAuth access token

        Returns:
            Dict com roles ou None se falhar

        Example:
            >>> roles = TokenConverter.verify_oauth_roles(oauth_token)
            >>> print(roles)
            {'roles': ['user:inference', 'org:create_api_key']}
        """
        logger.info("🔍 Verifying OAuth roles...")

        try:
            headers = {
                "Authorization": f"Bearer {oauth_token}",
                "User-Agent": "max-code-cli/1.0.0"
            }

            response = requests.get(
                TokenConverter.ROLES_ENDPOINT,
                headers=headers,
                timeout=TokenConverter.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                roles = response.json()
                logger.info(f"✅ Roles: {roles}")
                return roles
            else:
                logger.warning(f"⚠️ Failed to get roles: HTTP {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"❌ Error verifying roles: {e}")
            return None

    @staticmethod
    def is_oauth_token(token: str) -> bool:
        """
        Verifica se string é um OAuth token válido

        Args:
            token: String para verificar

        Returns:
            True se é OAuth token (sk-ant-oat01-...)
        """
        return token.startswith("sk-ant-oat01-") if token else False

    @staticmethod
    def is_api_key(key: str) -> bool:
        """
        Verifica se string é uma API key válida

        Args:
            key: String para verificar

        Returns:
            True se é API key (sk-ant-api03-...)
        """
        return key.startswith("sk-ant-api") if key else False


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def convert_oauth_to_api_key(oauth_token: str) -> Optional[str]:
    """
    Wrapper function para conversão OAuth → API Key

    Args:
        oauth_token: OAuth token do Claude Pro Max

    Returns:
        API key ou None
    """
    return TokenConverter.convert_oauth_to_api_key(oauth_token)


def verify_oauth_roles(oauth_token: str) -> Optional[Dict]:
    """
    Wrapper function para verificação de roles

    Args:
        oauth_token: OAuth token

    Returns:
        Dict com roles ou None
    """
    return TokenConverter.verify_oauth_roles(oauth_token)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    import sys

    logger.info("=== Token Converter Demo ===\n")

    # Test token format detection
    logger.info("TEST 1: Token format detection")
    test_tokens = [
        ("sk-ant-oat01-abc123...", "OAuth token"),
        ("sk-ant-api03-xyz789...", "API key"),
        ("invalid-token", "Invalid"),
    ]

    for token, expected in test_tokens:
        is_oauth = TokenConverter.is_oauth_token(token)
        is_api = TokenConverter.is_api_key(token)
        logger.info(f"  {token[:20]:<25} → OAuth: {is_oauth}, API: {is_api}")

    print()

    # Test conversion (requires real OAuth token)
    if len(sys.argv) > 1:
        oauth_token = sys.argv[1]
        logger.info("TEST 2: OAuth → API Key conversion")
        logger.info(f"  OAuth Token: {oauth_token[:20]}...")

        # Verify roles first
        roles = verify_oauth_roles(oauth_token)
        if roles:
            logger.info(f"  Roles: {roles}")

        # Convert
        api_key = convert_oauth_to_api_key(oauth_token)
        if api_key:
            logger.info(f"  ✅ API Key: {api_key[:20]}...")
        else:
            logger.error("  ❌ Conversion failed")
    else:
        logger.info("TEST 2: Skipped (no OAuth token provided)")
        logger.info("  Usage: python token_converter.py <oauth-token>")

    print()
    logger.info("Biblical Foundation:")
    logger.info('"Convertei-vos e vivei" (Ezequiel 18:32)')
    logger.info("Transformação OAuth → API Key gera funcionalidade.")
