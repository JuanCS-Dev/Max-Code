"""
LLM Integration Layer

Handles communication with Claude using Pro Max subscription.
"""

from core.llm.claude_cli import (
    call_claude_cli,
    chat_with_claude,
    check_claude_cli_available,
    verify_claude_cli_setup,
)

__all__ = [
    'call_claude_cli',
    'chat_with_claude',
    'check_claude_cli_available',
    'verify_claude_cli_setup',
]
