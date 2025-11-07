"""
Claude CLI Wrapper - Pro Max Subscription Integration

Uses 'claude -p' subprocess to leverage Claude Pro Max x20 subscription
without requiring paid API access.

Biblical Foundation:
"A palavra de Deus é viva e eficaz" (Hebreus 4:12)
True communication flows through authentic channels.
"""

import subprocess
import shlex
from typing import Optional, Dict, Any
from pathlib import Path
from config.logging_config import get_logger

logger = get_logger(__name__)


def check_claude_cli_available() -> bool:
    """
    Check if 'claude' CLI is installed and available.

    Returns:
        True if claude CLI is found, False otherwise
    """
    try:
        result = subprocess.run(
            ["which", "claude"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        logger.debug(f"Failed to check claude CLI: {e}")
        return False


def call_claude_cli(
    prompt: str,
    timeout: int = 120,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> Optional[str]:
    """
    Call Claude CLI with -p flag for programmatic use.

    Uses Pro Max x20 subscription - NO API BILLING.

    Args:
        prompt: User prompt to send to Claude
        timeout: Timeout in seconds (default: 120)
        max_tokens: Maximum tokens to generate (optional)
        temperature: Temperature 0-1 (optional)

    Returns:
        Claude's response text, or None if failed

    Example:
        >>> response = call_claude_cli("Say hello in 5 words")
        >>> print(response)
        "Hello! How can I help!"

    Note:
        Requires 'claude' CLI installed: npm install -g @anthropic-ai/claude-code
        Uses OAuth credentials from ~/.claude/.credentials.json
    """
    # Check CLI availability
    if not check_claude_cli_available():
        logger.error("   ❌ 'claude' CLI not found")
        logger.info("   💡 Install: npm install -g @anthropic-ai/claude-code")
        logger.info("   💡 Login: claude login")
        return None

    # Build command
    cmd = ["claude", "-p", prompt]

    # Add optional parameters
    if max_tokens:
        cmd.extend(["--max-tokens", str(max_tokens)])
    if temperature is not None:
        cmd.extend(["--temperature", str(temperature)])

    try:
        logger.debug(f"   🔄 Calling Claude CLI (Pro Max subscription)...")
        logger.debug(f"   📝 Prompt: {prompt[:100]}...")

        # Run claude command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode != 0:
            logger.error(f"   ❌ Claude CLI failed: {result.stderr}")

            # Check if authentication issue
            if "authentication" in result.stderr.lower() or "login" in result.stderr.lower():
                logger.error("   🔐 Authentication error")
                logger.info("   💡 Run: claude login")

            return None

        # Extract response
        response = result.stdout.strip()

        logger.debug(f"   ✅ Response received ({len(response)} chars)")
        logger.info(
            "   🎉 Claude Pro Max responded",
            extra={"response_length": len(response), "auth_type": "pro_max"}
        )

        return response

    except subprocess.TimeoutExpired:
        logger.error(f"   ⏰ Claude CLI timeout after {timeout}s")
        return None
    except Exception as e:
        logger.error(f"   ❌ Claude CLI error: {type(e).__name__}: {e}")
        return None


def chat_with_claude(
    prompt: str,
    show_thinking: bool = False,
    timeout: int = 120,
) -> Optional[Dict[str, Any]]:
    """
    Chat with Claude using Pro Max subscription (wrapper with metadata).

    Args:
        prompt: User prompt
        show_thinking: If True, return thinking process (future enhancement)
        timeout: Timeout in seconds

    Returns:
        Dict with response, metadata, or None if failed
        {
            "response": str,
            "auth_type": "pro_max",
            "billing": "subscription",
            "model": "claude-sonnet-4-5",
        }

    Example:
        >>> result = chat_with_claude("Explain recursion in 2 sentences")
        >>> print(result["response"])
    """
    response = call_claude_cli(prompt, timeout=timeout)

    if response is None:
        return None

    return {
        "response": response,
        "auth_type": "pro_max",
        "billing": "subscription",
        "model": "claude-sonnet-4-5",
        "success": True,
    }


def verify_claude_cli_setup() -> Dict[str, Any]:
    """
    Verify Claude CLI is properly configured.

    Returns:
        Dict with status information:
        {
            "installed": bool,
            "authenticated": bool,
            "credentials_file_exists": bool,
            "test_response": Optional[str],
        }

    Example:
        >>> status = verify_claude_cli_setup()
        >>> if status["authenticated"]:
        ...     print("✅ Ready to use!")
    """
    status = {
        "installed": False,
        "authenticated": False,
        "credentials_file_exists": False,
        "test_response": None,
    }

    # Check if CLI installed
    status["installed"] = check_claude_cli_available()
    if not status["installed"]:
        return status

    # Check credentials file
    credentials_file = Path.home() / ".claude" / ".credentials.json"
    status["credentials_file_exists"] = credentials_file.exists()

    # Test with minimal prompt
    test_response = call_claude_cli("test", timeout=10)
    status["test_response"] = test_response
    status["authenticated"] = test_response is not None

    return status


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("=== Claude CLI Wrapper Demo ===\n")

    # Test 1: Check CLI availability
    logger.info("TEST 1: Check CLI availability")
    available = check_claude_cli_available()
    logger.info(f"  Claude CLI available: {available}")
    print()

    if not available:
        logger.error("  ❌ Install: npm install -g @anthropic-ai/claude-code")
        logger.error("  ❌ Login: claude login")
        exit(1)

    # Test 2: Verify setup
    logger.info("TEST 2: Verify setup")
    status = verify_claude_cli_setup()
    logger.info(f"  Installed: {status['installed']}")
    logger.info(f"  Credentials file exists: {status['credentials_file_exists']}")
    logger.info(f"  Authenticated: {status['authenticated']}")
    logger.info(f"  Test response: {status['test_response']}")
    print()

    # Test 3: Simple chat
    logger.info("TEST 3: Simple chat")
    response = call_claude_cli("Say hello in 5 words")
    if response:
        logger.info(f"  ✅ Response: {response}")
    else:
        logger.error("  ❌ No response")
    print()

    # Test 4: Chat with metadata
    logger.info("TEST 4: Chat with metadata")
    result = chat_with_claude("Explain recursion in 2 sentences")
    if result:
        logger.info(f"  ✅ Success: {result['success']}")
        logger.info(f"  📝 Response: {result['response'][:100]}...")
        logger.info(f"  🔐 Auth type: {result['auth_type']}")
        logger.info(f"  💰 Billing: {result['billing']}")
    else:
        logger.error("  ❌ Failed")
    print()

    logger.info("Biblical Foundation:")
    logger.info('"A palavra de Deus é viva e eficaz" (Hebreus 4:12)')
    logger.info("True communication flows through authentic channels.")
