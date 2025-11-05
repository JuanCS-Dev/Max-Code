"""
OAuth Authentication System for Max-Code CLI

Supports both ANTHROPIC_API_KEY and CLAUDE_CODE_OAUTH_TOKEN authentication.

Biblical Foundation:
"Guarda-me como à menina do olho" (Salmos 17:8)
Protect authentication with utmost care.
"""

from .oauth_handler import (
    get_anthropic_client,
    setup_oauth_token,
    validate_credentials,
    CredentialType
)

__all__ = [
    'get_anthropic_client',
    'setup_oauth_token',
    'validate_credentials',
    'CredentialType',
]
