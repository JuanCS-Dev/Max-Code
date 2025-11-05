"""
OAuth Authentication Handler

Handles both traditional API keys and OAuth tokens for Anthropic Claude.

Supports:
- ANTHROPIC_API_KEY (format: sk-ant-api...)
- CLAUDE_CODE_OAUTH_TOKEN (format: sk-ant-oat01-...)

Biblical Foundation:
"Torre forte é o nome do Senhor" (Provérbios 18:10)
Secure authentication protects the system.
"""

import os
import subprocess
from typing import Optional, Tuple
from enum import Enum
from anthropic import Anthropic
from config.logging_config import get_logger

logger = get_logger(__name__)


class CredentialType(Enum):
    """Types of credentials supported"""
    API_KEY = "api_key"           # ANTHROPIC_API_KEY (sk-ant-api...)
    OAUTH_TOKEN = "oauth_token"   # CLAUDE_CODE_OAUTH_TOKEN (sk-ant-oat01-...)
    NONE = "none"


def get_credential_type(credential: str) -> CredentialType:
    """
    Determine credential type from format.

    Args:
        credential: Credential string

    Returns:
        CredentialType enum

    Examples:
        >>> get_credential_type("sk-ant-api03-abc...")
        CredentialType.API_KEY
        >>> get_credential_type("sk-ant-oat01-xyz...")
        CredentialType.OAUTH_TOKEN
    """
    if not credential:
        return CredentialType.NONE

    if credential.startswith("sk-ant-oat01-"):
        return CredentialType.OAUTH_TOKEN
    elif credential.startswith("sk-ant-api"):
        return CredentialType.API_KEY
    elif credential.startswith("sk-ant-"):
        # Generic Anthropic key format
        return CredentialType.API_KEY
    else:
        return CredentialType.NONE


def get_anthropic_client() -> Optional[Anthropic]:
    """
    Get authenticated Anthropic client.

    Tries authentication methods in order:
    1. CLAUDE_CODE_OAUTH_TOKEN (OAuth token from claude setup-token)
    2. ANTHROPIC_API_KEY (Traditional API key)

    Returns:
        Authenticated Anthropic client or None

    Example:
        >>> client = get_anthropic_client()
        >>> if client:
        ...     message = client.messages.create(...)
    """
    # Try OAuth token first (preferred for Max subscribers)
    oauth_token = os.getenv("CLAUDE_CODE_OAUTH_TOKEN")
    if oauth_token:
        cred_type = get_credential_type(oauth_token)
        if cred_type == CredentialType.OAUTH_TOKEN:
            try:
                client = Anthropic(api_key=oauth_token)
                logger.info(
                    "   🔑 Authenticated with OAuth token (Claude Max)",
                    extra={"auth_type": "oauth"}
                )
                return client
            except Exception as e:
                logger.warning(
                    f"   ⚠️ OAuth token invalid: {type(e).__name__}",
                    extra={"error_type": type(e).__name__}
                )

    # Try traditional API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        cred_type = get_credential_type(api_key)
        if cred_type == CredentialType.API_KEY:
            try:
                client = Anthropic(api_key=api_key)
                logger.info(
                    "   🔑 Authenticated with API key",
                    extra={"auth_type": "api_key"}
                )
                return client
            except Exception as e:
                logger.warning(
                    f"   ⚠️ API key invalid: {type(e).__name__}",
                    extra={"error_type": type(e).__name__}
                )

    # No valid credentials
    logger.warning(
        "   ⚠️ No valid Anthropic credentials found",
        extra={"checked": ["CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY"]}
    )
    logger.info("   💡 To authenticate:")
    logger.info("      1. OAuth (Max): Run 'claude setup-token' and set CLAUDE_CODE_OAUTH_TOKEN")
    logger.info("      2. API Key: Set ANTHROPIC_API_KEY=sk-ant-api...")

    return None


def validate_credentials() -> Tuple[bool, CredentialType, str]:
    """
    Validate available credentials without creating client.

    Returns:
        Tuple of (is_valid, credential_type, message)

    Example:
        >>> valid, cred_type, msg = validate_credentials()
        >>> if valid:
        ...     print(f"Authenticated with {cred_type.value}")
    """
    # Check OAuth token
    oauth_token = os.getenv("CLAUDE_CODE_OAUTH_TOKEN")
    if oauth_token:
        cred_type = get_credential_type(oauth_token)
        if cred_type == CredentialType.OAUTH_TOKEN:
            return (True, CredentialType.OAUTH_TOKEN, "OAuth token found (Claude Max)")
        else:
            return (False, CredentialType.NONE, f"Invalid OAuth token format: {oauth_token[:20]}...")

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        cred_type = get_credential_type(api_key)
        if cred_type == CredentialType.API_KEY:
            return (True, CredentialType.API_KEY, "API key found")
        else:
            return (False, CredentialType.NONE, f"Invalid API key format: {api_key[:20]}...")

    return (False, CredentialType.NONE, "No credentials found")


def setup_oauth_token() -> bool:
    """
    Run 'claude setup-token' to generate OAuth token.

    This launches the Claude CLI OAuth flow:
    1. Opens browser for authentication
    2. Generates long-lived token
    3. Returns token to set as CLAUDE_CODE_OAUTH_TOKEN

    Returns:
        True if successful, False otherwise

    Note:
        Requires 'claude' CLI to be installed.
        Install: npm install -g @anthropic-ai/claude-code

    Example:
        >>> if setup_oauth_token():
        ...     print("OAuth token generated!")
    """
    try:
        logger.info("   🔐 Launching OAuth setup...")
        logger.info("      Running: claude setup-token")

        # Check if claude CLI exists
        result = subprocess.run(
            ["which", "claude"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.error("   ❌ 'claude' CLI not found")
            logger.info("   💡 Install: npm install -g @anthropic-ai/claude-code")
            return False

        # Run claude setup-token
        result = subprocess.run(
            ["claude", "setup-token"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logger.info("   ✅ OAuth token generated!")
            logger.info("   📋 Copy the token and run:")
            logger.info("      export CLAUDE_CODE_OAUTH_TOKEN=<token>")
            logger.info("")
            logger.info("   Or add to your .env file:")
            logger.info("      CLAUDE_CODE_OAUTH_TOKEN=<token>")
            return True
        else:
            logger.error(f"   ❌ OAuth setup failed: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("   ❌ 'claude' CLI not installed")
        logger.info("   💡 Install: npm install -g @anthropic-ai/claude-code")
        return False
    except Exception as e:
        logger.error(f"   ❌ OAuth setup error: {type(e).__name__}: {e}")
        return False


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("=== OAuth Authentication System Demo ===\n")

    # Test 1: Validate credentials
    logger.info("TEST 1: Validate credentials")
    valid, cred_type, message = validate_credentials()
    logger.info(f"  Valid: {valid}")
    logger.info(f"  Type: {cred_type.value}")
    logger.info(f"  Message: {message}")
    print()

    # Test 2: Get client
    logger.info("TEST 2: Get Anthropic client")
    client = get_anthropic_client()
    if client:
        logger.info("  ✅ Client authenticated successfully")
    else:
        logger.warning("  ⚠️ No authentication available")
    print()

    # Test 3: Token format detection
    logger.info("TEST 3: Token format detection")
    test_tokens = [
        ("sk-ant-oat01-abc123...", "OAuth token"),
        ("sk-ant-api03-xyz789...", "API key"),
        ("invalid-token", "Invalid"),
        ("", "Empty"),
    ]

    for token, expected in test_tokens:
        detected = get_credential_type(token)
        logger.info(f"  {token[:20]:<25} → {detected.value:<15} (expected: {expected})")
    print()

    logger.info("Biblical Foundation:")
    logger.info('"Torre forte é o nome do Senhor" (Provérbios 18:10)')
    logger.info("Secure authentication protects the entire system.")
