#!/usr/bin/env python3
"""
Demo: Natural Language Parallel Agent Execution
Como Claude Code - Você fala, ele executa!

Exemplos de comandos que funcionam:
- "lança 5 agentes em paralelo pra andar mais rápido"
- "run agents code test review in parallel"
- "execute code and test agents concurrently"

Soli Deo Gloria 🙏
"""

from core.execution import ParallelExecutor, Task, CommandParser, ExecutionMode
from rich.console import Console
from rich.panel import Panel
import time

console = Console()


# Simulação de agentes
def code_agent(task_desc: str) -> str:
    """Simula Code Agent trabalhando"""
    time.sleep(1.5)
    return f"✅ Code Agent: {task_desc} implementado"


def test_agent(task_desc: str) -> str:
    """Simula Test Agent trabalhando"""
    time.sleep(1.2)
    return f"✅ Test Agent: Testes para {task_desc} criados"


def review_agent(task_desc: str) -> str:
    """Simula Review Agent trabalhando"""
    time.sleep(0.8)
    return f"✅ Review Agent: {task_desc} revisado"


def docs_agent(task_desc: str) -> str:
    """Simula Docs Agent trabalhando"""
    time.sleep(1.0)
    return f"✅ Docs Agent: Documentação para {task_desc} atualizada"


def fix_agent(task_desc: str) -> str:
    """Simula Fix Agent trabalhando"""
    time.sleep(1.3)
    return f"✅ Fix Agent: Bugs em {task_desc} corrigidos"


# Mapeamento de agentes
AGENTS = {
    'code': code_agent,
    'test': test_agent,
    'review': review_agent,
    'docs': docs_agent,
    'fix': fix_agent,
}


def process_natural_language_command(user_input: str, task_description: str = "feature X"):
    """
    Processa comando em linguagem natural e executa agentes.

    Isso é o que vai no REPL!
    """
    console.print(f"\n[bold cyan]🎤 Você disse:[/bold cyan] '{user_input}'")

    # Parse comando
    parsed = CommandParser.parse(user_input)

    if parsed.mode == ExecutionMode.PARALLEL:
        console.print(f"[green]✓[/green] Detectei execução paralela de {len(parsed.commands)} agentes!")

        # Criar tasks
        tasks = []
        for agent_name in parsed.commands:
            if agent_name in AGENTS:
                task = Task(
                    id=agent_name,
                    name=f"{agent_name.capitalize()} Agent",
                    func=AGENTS[agent_name],
                    args=(task_description,),
                    timeout_seconds=5.0
                )
                tasks.append(task)
            else:
                console.print(f"[yellow]⚠️  Agente '{agent_name}' não existe[/yellow]")

        if tasks:
            # Executar em paralelo!
            console.print(f"\n[bold yellow]🚀 Lançando {len(tasks)} agentes em paralelo...[/bold yellow]")

            executor = ParallelExecutor(max_parallel=len(tasks))
            results = executor.run_parallel(tasks)

            # Mostrar resultados
            console.print(f"\n[bold green]✅ Todos os agentes finalizaram![/bold green]")

            for task_id, result in results.items():
                if result.output:
                    console.print(f"  {result.output}")

            # Calcular speedup
            total_duration = sum(r.duration_ms for r in results.values())
            max_duration = max(r.duration_ms for r in results.values())
            speedup = total_duration / max_duration if max_duration > 0 else 1

            console.print(
                f"\n[bold cyan]⚡ Speedup:[/bold cyan] {speedup:.1f}x mais rápido "
                f"({max_duration:.0f}ms vs {total_duration:.0f}ms sequencial)"
            )

    elif parsed.mode == ExecutionMode.SEQUENTIAL:
        console.print(f"[blue]ℹ️[/blue] Detectei execução sequencial")
        # Implementar sequential...

    elif parsed.mode == ExecutionMode.CHAIN:
        console.print(f"[magenta]🔗[/magenta] Detectei tool chain")
        # Implementar chain...

    else:
        console.print(f"[dim]Comando simples - processando normalmente...[/dim]")


# Demo
if __name__ == "__main__":
    console.print(Panel(
        "[bold cyan]MAX-CODE - Natural Language Parallel Execution Demo[/bold cyan]\n\n"
        "Fale naturalmente e os agentes entendem!\n\n"
        "Como Claude Code: 'lança 5 agentes em paralelo pra andar mais rápido'",
        border_style="cyan"
    ))

    # Teste 1: Português natural
    console.print("\n[bold]═══ TESTE 1: Português Natural ═══[/bold]")
    process_natural_language_command(
        "lança code test review em paralelo pra andar mais rápido",
        "auth module"
    )

    # Teste 2: Inglês
    console.print("\n\n[bold]═══ TESTE 2: Inglês ═══[/bold]")
    process_natural_language_command(
        "run agents code test docs review fix in parallel",
        "payment API"
    )

    # Teste 3: Simples
    console.print("\n\n[bold]═══ TESTE 3: Simples ═══[/bold]")
    process_natural_language_command(
        "code and test together",
        "login feature"
    )

    console.print("\n\n[bold green]✅ Demo completo![/bold green]")
    console.print("[dim]No REPL real, isso funciona EXATAMENTE assim![/dim]")
