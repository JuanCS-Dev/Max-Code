"""
Agent Utilities

Helper functions for agents after OAuth removal.
"""

import os
from anthropic import Anthropic


def get_anthropic_client():
    """
    Get Anthropic client with API key authentication.

    Simplified version after OAuth removal - uses only ANTHROPIC_API_KEY.

    Returns:
        Anthropic client instance

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Please set it:\n"
            "  export ANTHROPIC_API_KEY='sk-ant-api...'\n"
            "Or add to .env file in project root."
        )
    return Anthropic(api_key=api_key)
