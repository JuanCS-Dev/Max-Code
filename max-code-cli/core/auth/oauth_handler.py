"""
OAuth Authentication Handler

Handles both traditional API keys and OAuth tokens for Anthropic Claude.

Supports:
- ANTHROPIC_API_KEY (format: sk-ant-api...)
- CLAUDE_CODE_OAUTH_TOKEN (format: sk-ant-oat01-...)
- Claude Code credentials file (~/.claude/.credentials.json)

Biblical Foundation:
"Torre forte é o nome do Senhor" (Provérbios 18:10)
Secure authentication protects the system.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict
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


def load_claude_credentials() -> Optional[Dict]:
    """
    Load credentials from Claude Code credentials file.

    Reads from ~/.claude/.credentials.json (same as Claude Code).

    Returns:
        Dict with accessToken, refreshToken, expiresAt, or None if not found
    """
    credentials_file = Path.home() / ".claude" / ".credentials.json"

    if not credentials_file.exists():
        return None

    try:
        with open(credentials_file, 'r') as f:
            data = json.load(f)

        # Extract OAuth credentials
        oauth_data = data.get("claudeAiOauth", {})
        if not oauth_data:
            return None

        return {
            "accessToken": oauth_data.get("accessToken"),
            "refreshToken": oauth_data.get("refreshToken"),
            "expiresAt": oauth_data.get("expiresAt"),
            "scopes": oauth_data.get("scopes", []),
        }
    except Exception as e:
        logger.warning(f"Failed to load Claude credentials: {e}")
        return None


def get_anthropic_client(verify_health: bool = False) -> Optional[Anthropic]:
    """
    Get authenticated Anthropic client with optional health check.

    Tries authentication methods in order:
    1. Claude Code credentials file (~/.claude/.credentials.json)
    2. CLAUDE_CODE_OAUTH_TOKEN (OAuth token from environment)
    3. ANTHROPIC_API_KEY (Traditional API key)

    Args:
        verify_health: If True, verify client works with minimal API call

    Returns:
        Authenticated Anthropic client or None

    Example:
        >>> client = get_anthropic_client()
        >>> if client:
        ...     message = client.messages.create(...)
    """
    # Try Claude Code credentials file first (PRIORITY 1)
    claude_creds = load_claude_credentials()
    if claude_creds and claude_creds.get("accessToken"):
        access_token = claude_creds["accessToken"]
        try:
            client = Anthropic(api_key=access_token)

            # Optional health check
            if verify_health:
                if not _validate_token_health(access_token):
                    logger.warning("   ⚠️ Claude Code token failed health check")
                    # Continue to try other methods
                else:
                    logger.info(
                        "   🔑 Authenticated with Claude Code session (Pro Max) ✓",
                        extra={"auth_type": "claude_code", "health_check": "passed"}
                    )
                    return client
            else:
                logger.info(
                    "   🔑 Authenticated with Claude Code session (Pro Max)",
                    extra={"auth_type": "claude_code"}
                )
                return client
        except Exception as e:
            logger.warning(
                f"   ⚠️ Claude Code token invalid: {type(e).__name__}",
                extra={"error_type": type(e).__name__}
            )

    # Try OAuth token from environment (PRIORITY 2)
    oauth_token = os.getenv("CLAUDE_CODE_OAUTH_TOKEN")
    if oauth_token:
        cred_type = get_credential_type(oauth_token)
        if cred_type == CredentialType.OAUTH_TOKEN:
            try:
                client = Anthropic(api_key=oauth_token)

                # Optional health check
                if verify_health:
                    if not _validate_token_health(oauth_token):
                        logger.warning("   ⚠️ OAuth token failed health check")
                        # Continue to try API key
                    else:
                        logger.info(
                            "   🔑 Authenticated with OAuth token (Claude Max) ✓",
                            extra={"auth_type": "oauth", "health_check": "passed"}
                        )
                        return client
                else:
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

                # Optional health check
                if verify_health:
                    if not _validate_token_health(api_key):
                        logger.warning("   ⚠️ API key failed health check")
                        return None
                    logger.info(
                        "   🔑 Authenticated with API key ✓",
                        extra={"auth_type": "api_key", "health_check": "passed"}
                    )
                else:
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
    logger.info("      1. OAuth (Max): Run 'max-code auth login'")
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


def setup_oauth_token(auto_save: bool = True) -> bool:
    """
    Run 'claude setup-token' to generate OAuth token and auto-save to .env.

    This launches the Claude CLI OAuth flow:
    1. Opens browser for authentication
    2. Generates long-lived token
    3. Auto-saves to .env file (if auto_save=True)
    4. Validates token with health check

    Args:
        auto_save: If True, automatically save token to .env file

    Returns:
        True if successful, False otherwise

    Note:
        Requires 'claude' CLI to be installed.
        Install: npm install -g @anthropic-ai/claude-code

    Example:
        >>> if setup_oauth_token():
        ...     print("OAuth token saved and validated!")
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

        # Run claude setup-token (opens browser)
        result = subprocess.run(
            ["claude", "setup-token"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.error(f"   ❌ OAuth setup failed: {result.stderr}")
            return False

        # Extract token from output
        # Claude CLI outputs: "Your token: sk-ant-..."
        token = None
        for line in result.stdout.split('\n'):
            if 'token' in line.lower() and 'sk-ant-' in line:
                # Extract token (format: sk-ant-...)
                parts = line.split()
                for part in parts:
                    if part.startswith('sk-ant-'):
                        token = part.strip()
                        break

        if not token:
            logger.warning("   ⚠️  Could not extract token automatically")
            logger.info("   📋 Please copy the token manually and add to .env:")
            logger.info("      CLAUDE_CODE_OAUTH_TOKEN=<your-token>")
            return False

        logger.info("   ✅ OAuth token generated!")

        # Auto-save to .env
        if auto_save:
            if _save_token_to_env(token):
                logger.info("   💾 Token saved to .env file")

                # Health check
                if _validate_token_health(token):
                    logger.info("   ✅ Token validated with Claude API")
                    logger.info("   🎉 Setup complete! You're ready to use max-code.")
                    return True
                else:
                    logger.warning("   ⚠️  Token saved but health check failed")
                    logger.info("   💡 Token may need a few seconds to activate")
                    return True
            else:
                logger.warning("   ⚠️  Token generated but could not save to .env")
                logger.info("   📋 Please add manually:")
                logger.info(f"      CLAUDE_CODE_OAUTH_TOKEN={token}")
                return True
        else:
            logger.info("   📋 Token generated. Add to .env:")
            logger.info(f"      CLAUDE_CODE_OAUTH_TOKEN={token}")
            return True

    except FileNotFoundError:
        logger.error("   ❌ 'claude' CLI not installed")
        logger.info("   💡 Install: npm install -g @anthropic-ai/claude-code")
        return False
    except Exception as e:
        logger.error(f"   ❌ OAuth setup error: {type(e).__name__}: {e}")
        return False


def _save_token_to_env(token: str) -> bool:
    """
    Save OAuth token to .env file.

    Appends or updates CLAUDE_CODE_OAUTH_TOKEN in .env file.

    Args:
        token: OAuth token to save

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        from pathlib import Path

        # Find project root (where .env should be)
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir.parent.parent  # max-code-cli/
        env_file = project_root / ".env"

        # Read existing .env if it exists
        existing_lines = []
        token_exists = False

        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip().startswith('CLAUDE_CODE_OAUTH_TOKEN='):
                        # Update existing token
                        existing_lines.append(f'CLAUDE_CODE_OAUTH_TOKEN={token}\n')
                        token_exists = True
                    else:
                        existing_lines.append(line)

        # Append new token if not exists
        if not token_exists:
            existing_lines.append(f'\n# Claude OAuth Token (auto-generated)\nCLAUDE_CODE_OAUTH_TOKEN={token}\n')

        # Write back to .env
        with open(env_file, 'w') as f:
            f.writelines(existing_lines)

        # Reload environment variables
        os.environ['CLAUDE_CODE_OAUTH_TOKEN'] = token

        return True

    except Exception as e:
        logger.error(f"   ❌ Failed to save token: {e}")
        return False


def _validate_token_health(token: str) -> bool:
    """
    Validate OAuth token with Claude API health check.

    Makes a minimal API request to verify token works.

    Args:
        token: OAuth token to validate

    Returns:
        True if token is valid, False otherwise
    """
    try:
        from anthropic import Anthropic

        # Create client with token
        client = Anthropic(api_key=token)

        # Make minimal request (count tokens - cheapest operation)
        response = client.messages.count_tokens(
            model="claude-sonnet-4-5-20250929",
            messages=[{"role": "user", "content": "test"}]
        )

        # If we get here, token is valid
        return True

    except Exception as e:
        logger.debug(f"   Token health check failed: {e}")
        return False


def initiate_browser_oauth_flow() -> bool:
    """
    Iniciar OAuth flow via browser (como claude-code).

    Opens browser for user authentication, captures callback, and saves token.
    USES PARENT IMPLEMENTATION - No duplication.

    Returns:
        True se sucesso, False caso contrário

    Example:
        >>> if initiate_browser_oauth_flow():
        ...     print("Authentication successful!")
        ...     client = get_anthropic_client()
    """
    # Import from parent project (eliminates duplication)
    from core.auth.oauth import initiate_oauth_login
    from core.auth.config import AuthConfig

    # Call parent implementation
    tokens = initiate_oauth_login()

    if tokens:
        # Save tokens to credentials file
        AuthConfig.ensure_config_dir()
        credentials_file = AuthConfig.CREDENTIALS_FILE

        import time
        credentials = {
            "accessToken": tokens['access_token'],
            "refreshToken": tokens['refresh_token'],
            "expiresAt": int(time.time()) + tokens['expires_in'],
        }

        with open(credentials_file, 'w') as f:
            json.dump({"claudeAiOauth": credentials}, f, indent=2)

        # Set permissions (owner only)
        credentials_file.chmod(AuthConfig.CREDENTIALS_FILE_PERMISSIONS)

        logger.info("✅ OAuth flow completed successfully")
        logger.info(f"   Token saved to {credentials_file}")
        return True
    else:
        logger.error("❌ OAuth flow failed")
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
