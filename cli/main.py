#!/usr/bin/env python3
"""
Max-Code CLI - Main Entry Point

Constitutional Code Generation powered by DETER-AGENT framework.
Uses OAuth authentication with Claude.ai (your Claude Max x20 plan).
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from core.auth.config import AuthConfig
from core.auth.oauth import initiate_oauth_login
from core.auth.credentials import CredentialsManager, save_credentials
from core.auth.token_manager import get_token_manager
from core.auth.http_client import get_http_client

console = Console()


def print_banner():
    """Imprime banner do Max-Code"""
    banner = Text()
    banner.append("MAX-CODE CLI\n", style="bold cyan")
    banner.append("Constitutional Code Generation\n", style="white")
    banner.append("Powered by CONSTITUIÇÃO VÉRTICE v3.0", style="dim")

    console.print(Panel(banner, border_style="cyan"))


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="1.0.0-alpha")
def cli(ctx):
    """
    Max-Code CLI - Constitutional Code Generation

    Usa autenticação OAuth com Claude.ai (SEU plano Claude Max x20).
    NÃO consome créditos de API - usa sua assinatura paga.
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("\nUse --help to see available commands\n", style="dim")


@cli.command()
def login():
    """
    Authenticate with Claude.ai

    Opens browser for OAuth login using your Claude Pro/Max subscription.
    Tokens are stored securely in ~/.max-code/.credentials.json

    This allows you to use Max-Code with your PAID Claude Max x20 plan
    WITHOUT consuming API credits.
    """
    console.print("\n" + "="*70, style="cyan")
    console.print("  MAX-CODE AUTHENTICATION", style="bold cyan")
    console.print("="*70 + "\n", style="cyan")

    console.print("🔐 Initiating OAuth 2.0 + PKCE flow...\n")
    console.print("This will:", style="bold")
    console.print("  1. Open your browser for Claude.ai login")
    console.print("  2. Use your Claude Max x20 subscription (NO API credits consumed)")
    console.print("  3. Store tokens securely in ~/.max-code/.credentials.json")
    console.print("  4. Enable auto-refresh for uninterrupted usage\n")

    # Perguntar confirmação
    if not click.confirm("Continue with authentication?", default=True):
        console.print("❌ Authentication cancelled", style="yellow")
        return

    # Iniciar fluxo OAuth
    tokens = initiate_oauth_login()

    if not tokens:
        console.print("\n❌ Authentication failed", style="bold red")
        console.print("Please try again or check your network connection", style="dim")
        return

    # Salvar tokens
    success = save_credentials(
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token'],
        expires_in=tokens['expires_in']
    )

    if not success:
        console.print("\n❌ Failed to save credentials", style="bold red")
        return

    # Sucesso!
    console.print("\n" + "="*70, style="green")
    console.print("  ✅ AUTHENTICATION SUCCESSFUL!", style="bold green")
    console.print("="*70, style="green")

    console.print(f"\n✓ Tokens stored in: {AuthConfig.CREDENTIALS_FILE}", style="dim")
    console.print(f"✓ Access token valid for: ~{tokens.get('expires_in', 0) // 3600} hours")
    console.print("✓ Auto-refresh: ENABLED\n")

    console.print("You can now use Max-Code CLI with your Claude Max x20 subscription:", style="bold")
    console.print("  $ max-code ask \"Implement user authentication\"")
    console.print("  $ max-code fix \"Bug in login endpoint\"")
    console.print("  $ max-code commit\n")

    # Iniciar token manager
    token_manager = get_token_manager()
    console.print("✓ Token auto-refresh started (background thread)", style="dim green")


@cli.command()
def logout():
    """
    Remove stored authentication

    Deletes ~/.max-code/.credentials.json
    """
    manager = CredentialsManager()

    if not manager.exists():
        console.print("❌ No credentials found - already logged out", style="yellow")
        return

    if not click.confirm("Remove stored credentials?", default=True):
        console.print("❌ Logout cancelled", style="yellow")
        return

    success = manager.delete()

    if success:
        console.print("✅ Logged out successfully", style="green")
        console.print(f"   Deleted: {AuthConfig.CREDENTIALS_FILE}", style="dim")
    else:
        console.print("❌ Failed to delete credentials", style="red")


@cli.command()
def status():
    """
    Show authentication status

    Displays current authentication state, token validity, and expiration time.
    """
    manager = CredentialsManager()
    manager.print_status()


@cli.command()
@click.argument('prompt', required=True)
@click.option('--model', default='claude-sonnet-4-5-20250929', help='Claude model to use')
def ask(prompt: str, model: str):
    """
    Ask Claude a question (TESTING - uses OAuth token)

    This is a TEST command to verify OAuth authentication is working.
    Uses your Claude Max x20 subscription (NO API credits consumed).

    Example:
        max-code ask "What is the capital of France?"
    """
    console.print(f"\n🤔 Asking Claude (model: {model})...\n", style="cyan")

    try:
        # Obter client HTTP (usa OAuth automaticamente)
        client = get_http_client()

        # Preparar mensagem
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        # Enviar (usa OAuth token do seu plano Max x20)
        response = client.send_message(messages, model=model)

        # Extrair resposta
        answer = response['content'][0]['text']

        # Display
        console.print(Panel(
            answer,
            title="[bold cyan]Claude's Response[/bold cyan]",
            border_style="cyan"
        ))

        # Stats
        usage = response.get('usage', {})
        console.print(f"\n📊 Tokens used: {usage.get('input_tokens', 0)} input + {usage.get('output_tokens', 0)} output", style="dim")

    except ValueError as e:
        console.print(f"\n❌ Authentication error: {e}", style="bold red")
        console.print("\n💡 Please run: max-code login\n", style="yellow")

    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")


@cli.command()
def constitutional():
    """
    Show constitutional compliance metrics

    Displays CRS, LEI, FPC and constitutional compliance status.
    """
    console.print("\n" + "="*70, style="cyan")
    console.print("  CONSTITUTIONAL COMPLIANCE REPORT", style="bold cyan")
    console.print("  [DEMO - Full implementation coming soon]", style="dim")
    console.print("="*70 + "\n", style="cyan")

    console.print("MÉTRICAS DE DETERMINISMO", style="bold")
    console.print("├─ CRS (Context Retention Score):     [green]96.5% ✓[/green] (target: ≥95%)")
    console.print("├─ LEI (Lazy Execution Index):        [green]0.3   ✓[/green] (target: <1.0)")
    console.print("└─ FPC (First-Pass Correctness):      [green]83%   ✓[/green] (target: ≥80%)\n")

    console.print("CONFORMIDADE CONSTITUCIONAL", style="bold")
    console.print("├─ P1 (Completude Obrigatória):       [green]100% ✓[/green] (0 placeholders)")
    console.print("├─ P2 (Validação Preventiva):         [green]100% ✓[/green] (0 API hallucinations)")
    console.print("├─ P3 (Ceticismo Crítico):            [green]12 assumptions challenged ✓[/green]")
    console.print("├─ P4 (Rastreabilidade Total):        [green]100% ✓[/green] (all code traceable)")
    console.print("├─ P5 (Consciência Sistêmica):        [green]100% ✓[/green] (0 breaking changes)")
    console.print("└─ P6 (Eficiência de Token):          [green]97%  ✓[/green] (avg 1.2 iter/task)\n")

    console.print("STATUS: [bold green]✅ FULLY COMPLIANT[/bold green]")
    console.print("="*70 + "\n", style="cyan")


if __name__ == "__main__":
    cli()
