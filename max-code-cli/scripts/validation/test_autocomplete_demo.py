#!/usr/bin/env python3
"""
Demonstração do Autocomplete Dropdown no MAX-CODE Shell

Mostra as ferramentas disponíveis quando o usuário digita /

Soli Deo Gloria 🙏
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from cli.repl_enhanced import EnhancedCompleter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def demo_autocomplete():
    """Demonstrar o autocomplete"""

    console.print()
    console.print(Panel.fit(
        "[bold cyan]MAX-CODE Shell - Autocomplete Dropdown Demo[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    # Comandos do shell (exemplo)
    shell_commands = {
        '/help': {'icon': '❓', 'description': 'Show help message'},
        '/exit': {'icon': '👋', 'description': 'Exit shell'},
        '/clear': {'icon': '🧹', 'description': 'Clear screen'},
        '/agents': {'icon': '🤖', 'description': 'Show available agents'},
        '/config': {'icon': '⚙️', 'description': 'Show configuration'},
    }

    # Criar completer
    completer = EnhancedCompleter(shell_commands)

    # Simular documento com palavra digitada
    class FakeDocument:
        def __init__(self, text):
            self.text = text

        def get_word_before_cursor(self):
            return self.text

    # Test 1: Usuario digita "/"
    console.print("[bold]Test 1: User types '/'[/bold]\n")

    doc = FakeDocument('/')
    completions = list(completer.get_completions(doc, None))

    if completions:
        table = Table(title="Available Commands & Tools", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=15)
        table.add_column("Description", style="white")

        for completion in completions:
            # Extract text from HTML
            desc_html = str(completion.display_meta)
            # Simple HTML strip (for demo)
            desc = desc_html.replace('<b>', '').replace('</b>', '').replace('ansitext:', '')
            table.add_row(completion.text, desc)

        console.print(table)
        console.print()
        console.print(f"[green]✅ Found {len(completions)} completions[/green]\n")
    else:
        console.print("[red]❌ No completions found[/red]\n")

    # Test 2: Usuario digita "/r" (filtrando)
    console.print("[bold]Test 2: User types '/r' (filtering)[/bold]\n")

    doc = FakeDocument('/r')
    completions = list(completer.get_completions(doc, None))

    if completions:
        table = Table(title="Filtered Results", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=15)
        table.add_column("Description", style="white")

        for completion in completions:
            desc_html = str(completion.display_meta)
            desc = desc_html.replace('<b>', '').replace('</b>', '').replace('ansitext:', '')
            table.add_row(completion.text, desc)

        console.print(table)
        console.print()
        console.print(f"[green]✅ Found {len(completions)} matches[/green]\n")
    else:
        console.print("[yellow]⚠️  No matches for '/r'[/yellow]\n")

    # Test 3: Listar todas as ferramentas
    console.print("[bold]Test 3: All Available Tools[/bold]\n")

    tools_table = Table(title="Tool Commands", show_header=True, header_style="bold green")
    tools_table.add_column("Command", style="cyan", width=12)
    tools_table.add_column("Icon", justify="center", width=6)
    tools_table.add_column("Description", style="white")

    for tool_name, tool_meta in completer.tools.items():
        tools_table.add_row(
            tool_name,
            tool_meta['icon'],
            tool_meta['description']
        )

    console.print(tools_table)
    console.print()

    # Summary
    console.print(Panel.fit(
        f"[bold green]✅ Autocomplete Sistema Pronto![/bold green]\n\n"
        f"📊 Shell Commands: {len(shell_commands)}\n"
        f"🔧 Tool Commands: {len(completer.tools)}\n"
        f"🎯 Total Options: {len(shell_commands) + len(completer.tools)}\n\n"
        f"[cyan]Como usar:[/cyan]\n"
        f"1. Digite / no shell\n"
        f"2. Veja dropdown com comandos e ferramentas\n"
        f"3. Continue digitando para filtrar (/r, /re, /read)\n"
        f"4. Pressione TAB para autocompletar\n"
        f"5. Pressione ENTER para executar",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        demo_autocomplete()
        console.print("\n[bold green]🚀 Autocomplete dropdown implementado com sucesso![/bold green]")
        console.print("[dim]Agora quando você abrir o shell e digitar /, verá todas as opções[/dim]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
