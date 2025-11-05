#!/usr/bin/env python3
"""
Max-Code CLI - OAuth Authentication Command

Handles OAuth token setup and validation.

Usage:
    python cli/auth_command.py setup     # Setup OAuth token
    python cli/auth_command.py validate  # Validate credentials
    python cli/auth_command.py status    # Show auth status

Biblical Foundation:
"Guarda-me como à menina do olho" (Salmos 17:8)
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.auth import (
    setup_oauth_token,
    validate_credentials,
    get_anthropic_client,
    CredentialType
)
from config.logging_config import configure_logging, get_logger
import logging

logger = get_logger(__name__)


def cmd_setup():
    """Setup OAuth token via 'claude setup-token'"""
    print("\n" + "="*70)
    logger.info("🔐 Max-Code OAuth Setup")
    print("="*70)
    print()

    logger.info("This will launch the Claude CLI OAuth flow:")
    logger.info("  1. Opens browser for authentication")
    logger.info("  2. Generates long-lived token (sk-ant-oat01-...)")
    logger.info("  3. Returns token to set as CLAUDE_CODE_OAUTH_TOKEN")
    print()

    input("Press ENTER to continue or Ctrl+C to cancel...")
    print()

    success = setup_oauth_token()

    print()
    if success:
        logger.info("✅ OAuth setup complete!")
        print()
        logger.info("Next steps:")
        logger.info("  1. Copy the token from above")
        logger.info("  2. Add to your environment:")
        logger.info("     export CLAUDE_CODE_OAUTH_TOKEN=<token>")
        logger.info("")
        logger.info("  Or add to .env file:")
        logger.info("     CLAUDE_CODE_OAUTH_TOKEN=<token>")
    else:
        logger.error("❌ OAuth setup failed")
        logger.info("")
        logger.info("Alternative: Use API key instead")
        logger.info("  1. Get key from: https://console.anthropic.com")
        logger.info("  2. Set: export ANTHROPIC_API_KEY=sk-ant-api...")

    print("="*70)
    print()


def cmd_validate():
    """Validate current credentials"""
    print("\n" + "="*70)
    logger.info("🔍 Max-Code Credential Validation")
    print("="*70)
    print()

    valid, cred_type, message = validate_credentials()

    logger.info(f"Status: {'✅ Valid' if valid else '❌ Invalid'}")
    logger.info(f"Type:   {cred_type.value}")
    logger.info(f"Info:   {message}")
    print()

    if valid:
        logger.info("✅ Authentication configured correctly")

        # Test actual client creation
        client = get_anthropic_client()
        if client:
            logger.info("✅ Client created successfully")
        else:
            logger.warning("⚠️ Client creation failed despite valid credentials")
    else:
        logger.warning("⚠️ No valid credentials found")
        print()
        logger.info("To authenticate:")
        logger.info("  Option 1 (OAuth - Max subscription):")
        logger.info("    max-code auth setup")
        logger.info("")
        logger.info("  Option 2 (API Key):")
        logger.info("    export ANTHROPIC_API_KEY=sk-ant-api...")

    print("="*70)
    print()


def cmd_status():
    """Show authentication status and environment info"""
    print("\n" + "="*70)
    logger.info("📊 Max-Code Authentication Status")
    print("="*70)
    print()

    # Check environment variables
    logger.info("Environment Variables:")
    oauth_set = "CLAUDE_CODE_OAUTH_TOKEN" in os.environ
    api_set = "ANTHROPIC_API_KEY" in os.environ

    if oauth_set:
        token = os.environ["CLAUDE_CODE_OAUTH_TOKEN"]
        logger.info(f"  ✅ CLAUDE_CODE_OAUTH_TOKEN: {token[:20]}... (OAuth)")
    else:
        logger.info("  ⚠️  CLAUDE_CODE_OAUTH_TOKEN: Not set")

    if api_set:
        key = os.environ["ANTHROPIC_API_KEY"]
        logger.info(f"  ✅ ANTHROPIC_API_KEY: {key[:20]}... (API Key)")
    else:
        logger.info("  ⚠️  ANTHROPIC_API_KEY: Not set")

    print()

    # Validate credentials
    valid, cred_type, message = validate_credentials()
    logger.info(f"Validation: {'✅ Valid' if valid else '❌ Invalid'}")
    logger.info(f"Type:       {cred_type.value}")
    logger.info(f"Message:    {message}")

    print()

    # Authentication priority
    logger.info("Authentication Priority:")
    logger.info("  1. CLAUDE_CODE_OAUTH_TOKEN (OAuth - preferred for Max)")
    logger.info("  2. ANTHROPIC_API_KEY (API Key - traditional)")

    print()

    # Recommendations
    if not valid:
        logger.warning("⚠️  No valid credentials configured")
        print()
        logger.info("Recommended: Run 'max-code auth setup' to configure OAuth")
    elif cred_type == CredentialType.OAUTH_TOKEN:
        logger.info("✅ Using OAuth (Claude Max subscription)")
    elif cred_type == CredentialType.API_KEY:
        logger.info("✅ Using API Key (traditional authentication)")

    print("="*70)
    print()


def main():
    """Main CLI entry point"""
    configure_logging(level=logging.INFO, format_style="human")

    if len(sys.argv) < 2:
        print("\nUsage: max-code auth <command>")
        print("\nCommands:")
        print("  setup     Setup OAuth token via 'claude setup-token'")
        print("  validate  Validate current credentials")
        print("  status    Show authentication status")
        print()
        print('Biblical Foundation:')
        print('"Guarda-me como à menina do olho" (Salmos 17:8)')
        print()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "setup":
        cmd_setup()
    elif command == "validate":
        cmd_validate()
    elif command == "status":
        cmd_status()
    else:
        logger.error(f"Unknown command: {command}")
        logger.info("Valid commands: setup, validate, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
