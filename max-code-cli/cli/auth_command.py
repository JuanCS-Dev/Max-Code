"""
Max-Code CLI - Authentication Command

Handles OAuth authentication with Claude API.

Biblical Foundation:
"Guarda-me como à menina do olho" (Salmos 17:8)
"""

import click
import os
from rich.console import Console
from rich.panel import Panel

from core.auth.oauth_handler import setup_oauth_token, get_anthropic_client
from core.auth import validate_credentials, CredentialType

console = Console()


@click.group()
def auth():
    """
    Manage Claude API authentication.

    Use OAuth tokens or API keys to authenticate with Claude.
    """
    pass


@auth.command()
@click.option('--no-save', is_flag=True, help='Do not auto-save token to .env')
def login(no_save):
    """
    Authenticate with Claude via OAuth.

    This will:
    1. Open your browser for authentication
    2. Extract the OAuth token
    3. Auto-save to .env file (unless --no-save)
    4. Validate with Claude API

    Example:
      max-code auth login
      max-code auth login --no-save
    """
    console.print("\n[bold cyan]Max-Code - Claude Authentication[/bold cyan]\n")

    console.print("[yellow]Opening browser for authentication...[/yellow]")
    console.print("[dim]Please complete the OAuth flow in your browser.[/dim]\n")

    # Run OAuth setup with auto-save
    auto_save = not no_save
    success = setup_oauth_token(auto_save=auto_save)

    if success:
        console.print()
        console.print(Panel(
            "[bold green]✓ Authentication Successful![/bold green]\n\n"
            "Your Claude API token has been configured and validated.\n"
            f"{'Token saved to .env file.' if auto_save else 'Token not saved (--no-save flag).'}\n\n"
            "[cyan]Next Steps:[/cyan]\n"
            "  • Run: [white]max-code task \"your task here\"[/white]\n"
            "  • Or: [white]max-code chat \"your question\"[/white]",
            title="🎉 Ready to Go!",
            border_style="green"
        ))
        console.print()
    else:
        console.print()
        console.print(Panel(
            "[bold red]✗ Authentication Failed[/bold red]\n\n"
            "Could not complete OAuth authentication.\n\n"
            "[yellow]Troubleshooting:[/yellow]\n"
            "  1. Make sure Claude CLI is installed: [white]pip install claude-cli[/white]\n"
            "  2. Check your internet connection\n"
            "  3. Try manual setup: Set [white]ANTHROPIC_API_KEY[/white] in .env\n\n"
            "[cyan]Get API Key:[/cyan]\n"
            "  https://console.anthropic.com/settings/keys",
            title="⚠️  Authentication Error",
            border_style="red"
        ))
        console.print()


@auth.command()
def status():
    """
    Check authentication status.

    Shows current Claude API configuration and validates token.

    Example:
      max-code auth status
    """
    from config.settings import get_settings

    console.print("\n[bold cyan]Authentication Status[/bold cyan]\n")

    settings = get_settings()

    # Check environment variables
    console.print("[bold yellow]Environment Variables:[/bold yellow]")
    oauth_set = "CLAUDE_CODE_OAUTH_TOKEN" in os.environ
    api_set = "ANTHROPIC_API_KEY" in os.environ

    if oauth_set:
        token = os.environ["CLAUDE_CODE_OAUTH_TOKEN"]
        console.print(f"  [green]✓[/green] CLAUDE_CODE_OAUTH_TOKEN: {token[:20]}... (OAuth)")
    else:
        console.print("  [dim]⚠️  CLAUDE_CODE_OAUTH_TOKEN: Not set[/dim]")

    if api_set:
        key = os.environ["ANTHROPIC_API_KEY"]
        console.print(f"  [green]✓[/green] ANTHROPIC_API_KEY: {key[:20]}... (API Key)")
    else:
        console.print("  [dim]⚠️  ANTHROPIC_API_KEY: Not set[/dim]")

    console.print()

    # Validate credentials
    valid, cred_type, message = validate_credentials()

    console.print("[bold yellow]Validation:[/bold yellow]")
    if valid:
        console.print(f"  [green]✓[/green] Status: Valid")
        console.print(f"  [cyan]Type:[/cyan] {cred_type.value}")
        console.print(f"  [dim]{message}[/dim]")
    else:
        console.print(f"  [red]✗[/red] Status: Invalid")
        console.print(f"  [dim]{message}[/dim]")

    console.print()

    # Test client creation
    if valid:
        console.print("[yellow]Testing Claude API connection...[/yellow]")
        client = get_anthropic_client(verify_health=True)

        if client:
            console.print("[green]✓[/green] API connection successful\n")

            # Show configuration
            console.print("[bold yellow]Configuration:[/bold yellow]")
            console.print(f"  Model: [white]{settings.claude.model}[/white]")
            console.print(f"  Max Tokens: [white]{settings.claude.max_tokens}[/white]")
            console.print(f"  Temperature: [white]{settings.claude.temperature}[/white]")
            console.print()
        else:
            console.print("[red]✗[/red] API connection failed")
            console.print("[yellow]Token may be expired or invalid.[/yellow]")
            console.print("[dim]Run: [white]max-code auth login[/white] to re-authenticate[/dim]\n")
    else:
        console.print("[yellow]⚠️  No valid credentials configured[/yellow]")
        console.print("[dim]Run: [white]max-code auth login[/white] to authenticate[/dim]\n")


@auth.command()
def convert():
    """
    Convert OAuth token to API key.

    Converts OAuth token (sk-ant-oat01-...) from credentials file
    to permanent API key (sk-ant-api03-...) using Claude Code endpoint.

    This is done automatically when using the client, but can be
    triggered manually for troubleshooting.

    Example:
      max-code auth convert
    """
    from core.auth.oauth_handler import load_claude_credentials, _save_api_key_to_credentials
    from core.auth.token_converter import TokenConverter

    console.print("\n[bold cyan]OAuth → API Key Conversion[/bold cyan]\n")

    # Load credentials
    console.print("[yellow]Loading OAuth credentials...[/yellow]")
    creds = load_claude_credentials()

    if not creds:
        console.print("[red]✗[/red] No credentials found in ~/.claude/.credentials.json")
        console.print("[dim]Run: [white]max-code auth login[/white] first[/dim]\n")
        return

    # Check if already has API key
    if creds.get("apiKey"):
        console.print("[green]✓[/green] API key already exists in credentials")
        api_key = creds["apiKey"]
        console.print(f"   API Key: {api_key[:20]}...\n")

        # Ask if user wants to regenerate
        if not click.confirm("Regenerate API key?", default=False):
            console.print("[dim]Keeping existing API key[/dim]\n")
            return

    # Get OAuth token
    access_token = creds.get("accessToken")
    if not access_token:
        console.print("[red]✗[/red] No OAuth token found in credentials\n")
        return

    if not TokenConverter.is_oauth_token(access_token):
        console.print(f"[red]✗[/red] Invalid OAuth token format: {access_token[:20]}...")
        console.print("[dim]Expected: sk-ant-oat01-...[/dim]\n")
        return

    console.print(f"[green]✓[/green] OAuth token found: {access_token[:20]}...\n")

    # Convert
    console.print("[yellow]Converting OAuth token to API key...[/yellow]")
    console.print("[dim]Endpoint: POST /api/oauth/claude_cli/create_api_key[/dim]\n")

    api_key = TokenConverter.convert_oauth_to_api_key(access_token)

    if api_key:
        console.print()
        console.print("[green]✓[/green] Conversion successful!")
        console.print(f"   API Key: {api_key[:20]}...\n")

        # Save to credentials
        console.print("[yellow]Saving API key to credentials...[/yellow]")
        if _save_api_key_to_credentials(api_key):
            console.print("[green]✓[/green] API key saved to ~/.claude/.credentials.json\n")

            console.print(Panel(
                "[bold green]✓ Conversion Complete![/bold green]\n\n"
                "Your OAuth token has been converted to a permanent API key.\n"
                "The API key is now saved and will be used automatically.\n\n"
                "[cyan]Next Steps:[/cyan]\n"
                "  • Run: [white]max-code shell[/white]\n"
                "  • Or: [white]max-code chat \"your question\"[/white]",
                title="🎉 Ready to Use!",
                border_style="green"
            ))
        else:
            console.print("[red]✗[/red] Failed to save API key\n")
    else:
        console.print()
        console.print(Panel(
            "[bold red]✗ Conversion Failed[/bold red]\n\n"
            "Could not convert OAuth token to API key.\n\n"
            "[yellow]Possible causes:[/yellow]\n"
            "  1. OAuth token expired\n"
            "  2. Insufficient permissions (missing 'org:create_api_key' scope)\n"
            "  3. Network error\n\n"
            "[cyan]Solution:[/cyan]\n"
            "  Run: [white]max-code auth login[/white] to get a fresh token",
            title="⚠️  Conversion Error",
            border_style="red"
        ))

    console.print()


@auth.command()
def logout():
    """
    Remove authentication token.

    This will remove the Claude API token from your .env file.

    Example:
      max-code auth logout
    """
    from pathlib import Path

    console.print("\n[bold cyan]Logout[/bold cyan]\n")

    # Find .env file
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    if not env_file.exists():
        console.print("[yellow]No .env file found. Already logged out.[/yellow]\n")
        return

    # Read and remove token lines
    with open(env_file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    removed = False
    for line in lines:
        if line.strip().startswith('ANTHROPIC_API_KEY=') or \
           line.strip().startswith('CLAUDE_CODE_OAUTH_TOKEN='):
            removed = True
            continue
        new_lines.append(line)

    if removed:
        # Write back
        with open(env_file, 'w') as f:
            f.writelines(new_lines)

        console.print("[green]✓[/green] Authentication token removed")
        console.print("[dim]Run [white]max-code auth login[/white] to authenticate again[/dim]\n")
    else:
        console.print("[yellow]No authentication token found in .env file.[/yellow]\n")


if __name__ == '__main__':
    auth()
