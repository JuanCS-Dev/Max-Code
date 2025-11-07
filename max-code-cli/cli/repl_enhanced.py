"""
Enhanced REPL para MAX-CODE CLI.

Features:
- Fuzzy command completion com preview
- Command palette (Ctrl+P) usando ui/command_palette.py EXISTENTE
- Atalhos de teclado para agentes
- Dashboard de agentes (Ctrl+A)
- Modo DREAM (Ctrl+D) - análise crítica
- Visual impressionante mas clean

Soli Deo Gloria 🙏
"""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from typing import Dict, Callable, Optional
import sys
from pathlib import Path

# Importar command palette EXISTENTE (não reimplementar!)
from ui.command_palette import CommandPalette, Command, CommandCategory
from ui.banner import print_banner
from ui.themes import ThemeManager
from ui.dashboard import Dashboard

# Importar cliente LLM criado no Sprint 1
from core.llm.client import ClaudeClient

# Importar agentes existentes
from agents import (
    ArchitectAgent,
    CodeAgent,
    TestAgent,
    ReviewAgent,
    FixAgent,
    DocsAgent,
    ExploreAgent,
    PlanAgent
)

console = Console()


class EnhancedCompleter(Completer):
    """
    Completer com preview de comandos.
    Mostra descrição e exemplo de uso.
    """

    def __init__(self, commands: Dict[str, Dict]):
        self.commands = commands

    def get_completions(self, document, complete_event):
        """Gerar completions com metadata"""
        word = document.get_word_before_cursor()

        # Se não começar com /, não autocomplete
        if not word.startswith('/'):
            return

        for cmd_name, cmd_meta in self.commands.items():
            if cmd_name.startswith(word):
                # Criar completion com preview
                display_meta = HTML(
                    f"<b>{cmd_meta['icon']}</b> {cmd_meta['description']}"
                )

                yield Completion(
                    cmd_name,
                    start_position=-len(word),
                    display_meta=display_meta
                )


class EnhancedREPL:
    """
    REPL Enhanced com command palette, atalhos de agentes, e visual impressionante.

    Integra com código EXISTENTE (não reimplementa):
    - ui/command_palette.py (completo, 436 linhas)
    - ui/banner.py (banner existente)
    - ui/themes.py (temas existentes)
    - ui/dashboard.py (dashboard existente)
    - agents/* (8 agentes implementados)
    """

    def __init__(self):
        self.console = Console()
        self.theme_manager = ThemeManager()
        self.dashboard = Dashboard()
        self.commands = self._load_commands()
        self.session = self._create_session()
        self.running = True

        # State
        self.current_agent: Optional[str] = None
        self.dream_mode: bool = False

        # Claude client
        self.claude_client = ClaudeClient()

        # Agent instances (lazy loading)
        self._agent_instances = {}

    def _load_commands(self) -> Dict[str, Dict]:
        """
        Carregar TODOS comandos disponíveis.
        Inclui: agentes, especiais, SOFIA, DREAM
        """
        return {
            # Comandos especiais
            "/help": {
                "icon": "❓",
                "description": "Show all available commands",
                "category": CommandCategory.HELP,
                "handler": self._cmd_help
            },
            "/exit": {
                "icon": "👋",
                "description": "Exit MAX-CODE shell",
                "category": CommandCategory.SYSTEM,
                "handler": self._cmd_exit
            },
            "/quit": {
                "icon": "👋",
                "description": "Exit MAX-CODE shell (alias)",
                "category": CommandCategory.SYSTEM,
                "handler": self._cmd_exit
            },
            "/clear": {
                "icon": "🧹",
                "description": "Clear screen",
                "category": CommandCategory.SYSTEM,
                "handler": self._cmd_clear
            },

            # Agentes (8 total)
            "/sophia": {
                "icon": "👑",
                "description": "Sophia - The Architect (system design)",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("architect", msg)
            },
            "/code": {
                "icon": "💻",
                "description": "Code generation agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("code", msg)
            },
            "/test": {
                "icon": "🧪",
                "description": "Test generation agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("test", msg)
            },
            "/review": {
                "icon": "🔍",
                "description": "Code review agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("review", msg)
            },
            "/fix": {
                "icon": "🔧",
                "description": "Bug fixing agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("fix", msg)
            },
            "/docs": {
                "icon": "📚",
                "description": "Documentation agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("docs", msg)
            },
            "/explore": {
                "icon": "🗺️",
                "description": "Codebase exploration agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("explore", msg)
            },
            "/plan": {
                "icon": "📋",
                "description": "Planning agent",
                "category": CommandCategory.AGENT,
                "handler": lambda msg: self._invoke_agent("plan", msg)
            },

            # Modos especiais (SOFIA e DREAM)
            "/sofia-plan": {
                "icon": "🎯",
                "description": "SOFIA Plan Mode - Strategic planning",
                "category": CommandCategory.AGENT,
                "handler": self._cmd_sofia_plan
            },
            "/dream": {
                "icon": "💭",
                "description": "DREAM Mode - Critical analysis and improvements",
                "category": CommandCategory.AGENT,
                "handler": self._cmd_dream
            },

            # Dashboard e UI
            "/dashboard": {
                "icon": "📊",
                "description": "Show agent dashboard",
                "category": CommandCategory.UI,
                "handler": self._cmd_dashboard
            },
            "/theme": {
                "icon": "🎨",
                "description": "Change theme (neon, fire, ocean, matrix, cyberpunk)",
                "category": CommandCategory.UI,
                "handler": self._cmd_theme
            },
        }

    def _create_session(self) -> PromptSession:
        """Criar prompt session com todas features"""
        history_file = Path.home() / '.max-code-history'

        return PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=EnhancedCompleter(self.commands),
            key_bindings=self._create_keybindings(),
            enable_history_search=True,
            vi_mode=False,
        )

    def _create_keybindings(self) -> KeyBindings:
        """Criar atalhos de teclado"""
        bindings = KeyBindings()

        @bindings.add("c-p")
        def show_palette(event):
            """Command Palette (Ctrl+P)"""
            event.app.exit()  # Exit prompt temporarily
            self._show_command_palette()

        @bindings.add("c-a")
        def show_agents(event):
            """Agent Dashboard (Ctrl+A)"""
            event.app.exit()  # Exit prompt temporarily
            self._cmd_dashboard("")

        @bindings.add("c-d")
        def toggle_dream(event):
            """Toggle DREAM mode (Ctrl+D)"""
            self.dream_mode = not self.dream_mode
            mode_status = "[green]enabled[/green]" if self.dream_mode else "[dim]disabled[/dim]"
            console.print(f"\n💭 DREAM mode {mode_status}\n")

        return bindings

    def _show_command_palette(self):
        """
        Mostrar command palette usando UI EXISTENTE.
        NÃO REIMPLEMENTAR - ui/command_palette.py JÁ ESTÁ COMPLETO!
        """
        palette = CommandPalette()

        # Registrar todos comandos
        for cmd_name, cmd_meta in self.commands.items():
            palette.register_command(Command(
                name=cmd_name.lstrip('/'),
                title=cmd_meta['description'],
                description=f"Category: {cmd_meta['category'].value}",
                category=cmd_meta['category'],
                icon=cmd_meta['icon'],
                handler=cmd_meta['handler']
            ))

        # Mostrar palette e executar comando selecionado
        try:
            selected_command = palette.show()
            if selected_command:
                # Executar handler do comando
                handler = self.commands.get(f"/{selected_command}", {}).get('handler')
                if handler:
                    # Pedir input adicional se necessário
                    additional_input = input(f"\n{selected_command} › ").strip()
                    handler(additional_input)
        except Exception as e:
            console.print(f"\n[red]Error in command palette: {e}[/red]\n")

    def _get_agent_instance(self, agent_name: str):
        """
        Get or create agent instance (lazy loading).

        Args:
            agent_name: Nome do agente (architect, code, test, etc.)

        Returns:
            Agent instance
        """
        if agent_name in self._agent_instances:
            return self._agent_instances[agent_name]

        # Map agent names to classes
        agent_map = {
            "architect": ArchitectAgent,
            "code": CodeAgent,
            "test": TestAgent,
            "review": ReviewAgent,
            "fix": FixAgent,
            "docs": DocsAgent,
            "explore": ExploreAgent,
            "plan": PlanAgent,
        }

        agent_class = agent_map.get(agent_name)
        if not agent_class:
            raise ValueError(f"Unknown agent: {agent_name}")

        # Instantiate agent
        agent = agent_class()
        self._agent_instances[agent_name] = agent
        return agent

    def _invoke_agent(self, agent_name: str, message: str):
        """
        Invocar agente especializado.

        Args:
            agent_name: Nome do agente (architect, code, test, etc.)
            message: Mensagem para o agente
        """
        if not message.strip():
            console.print(f"\n[yellow]Please provide a message for the {agent_name} agent[/yellow]\n")
            return

        try:
            # Get agent instance
            agent = self._get_agent_instance(agent_name)

            # Mostrar feedback
            icon_map = {
                "architect": "👑",
                "code": "💻",
                "test": "🧪",
                "review": "🔍",
                "fix": "🔧",
                "docs": "📚",
                "explore": "🗺️",
                "plan": "📋",
            }
            icon = icon_map.get(agent_name, "🤖")

            console.print(f"\n{icon} [cyan]Invoking {agent_name} agent...[/cyan]\n")

            # Process message through agent
            # Note: Agents may have different interfaces, adapt as needed
            if hasattr(agent, 'process'):
                response = agent.process(message)
            elif hasattr(agent, 'run'):
                response = agent.run(message)
            elif hasattr(agent, 'execute'):
                response = agent.execute(message)
            else:
                # Fallback: use Claude client directly with agent context
                system_prompt = f"You are the {agent_name} agent. Respond according to your specialization."
                response = self.claude_client.chat(message, system=system_prompt)

            # Display response with beautiful markdown rendering
            self._display_response(response)
            console.print()

        except Exception as e:
            console.print(f"\n[red]Error invoking agent: {e}[/red]\n")

    def _display_response(self, response: str):
        """
        Display agent response with beautiful markdown rendering.

        Args:
            response: Raw response text from agent
        """
        if not response:
            return

        # Check if response looks like markdown (has headers, lists, code blocks)
        has_markdown = any([
            '# ' in response or '## ' in response or '### ' in response,  # Headers
            '```' in response,  # Code blocks
            '- ' in response or '* ' in response or '1. ' in response,    # Lists
            '**' in response or '__' in response,                         # Bold
            '`' in response,                                               # Inline code
        ])

        if has_markdown:
            # Render as markdown for beautiful formatting
            try:
                md = Markdown(response)
                console.print(md)
            except Exception:
                # Fallback to plain text if markdown parsing fails
                console.print(response)
        else:
            # Plain text response - just print directly
            console.print(response)

    def _cmd_help(self, _):
        """Mostrar help de comandos"""
        table = Table(title="MAX-CODE Commands", show_header=True, border_style="cyan")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Icon", justify="center")
        table.add_column("Description", style="dim")

        # Group by category
        categories = {}
        for cmd, meta in self.commands.items():
            cat = meta['category'].value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((cmd, meta))

        # Display by category
        for category, cmds in sorted(categories.items()):
            table.add_row(f"\n[bold]{category.upper()}[/bold]", "", "", style="bold")
            for cmd, meta in sorted(cmds):
                table.add_row(cmd, meta['icon'], meta['description'])

        console.print("\n")
        console.print(table)
        console.print("\n[dim]💡 Press Ctrl+P for command palette | Ctrl+A for agent dashboard[/dim]\n")

    def _cmd_exit(self, _):
        """Sair do shell"""
        self.running = False
        console.print("\n[cyan]👋 Goodbye! Soli Deo Gloria 🙏[/cyan]\n")

    def _cmd_clear(self, _):
        """Limpar tela"""
        console.clear()

    def _cmd_sofia_plan(self, message: str):
        """
        SOFIA Plan Mode - Planejamento estratégico.
        Usa o agent architect em modo de planejamento.
        """
        console.print("\n[cyan bold]🎯 SOFIA Plan Mode[/cyan bold]")
        console.print("[dim]Strategic planning and architecture design[/dim]\n")

        if not message.strip():
            console.print("[yellow]Please provide a planning task[/yellow]\n")
            return

        # Invocar architect agent com contexto de planejamento
        plan_message = f"[PLAN MODE - STRATEGIC] {message}"
        self._invoke_agent("architect", plan_message)

    def _cmd_dream(self, message: str):
        """
        DREAM Mode - Análise crítica e propostas de melhoria.
        Agente cético que questiona e propõe melhorias.
        """
        console.print("\n[cyan bold]💭 DREAM Mode - Critical Analysis[/cyan bold]")
        console.print("[dim]Skeptical review and improvement proposals[/dim]\n")

        if not message.strip():
            # Se não há mensagem, apenas toggle o modo
            self.dream_mode = not self.dream_mode
            mode_status = "[green]enabled[/green]" if self.dream_mode else "[dim]disabled[/dim]"
            console.print(f"💭 DREAM mode {mode_status}\n")
            return

        # Usar review agent em modo crítico
        critical_message = f"[DREAM MODE - CRITICAL ANALYSIS] {message}"
        self._invoke_agent("review", critical_message)

    def _cmd_dashboard(self, _):
        """Mostrar dashboard de agentes"""
        try:
            # Usar dashboard existente
            self.dashboard.show()
        except Exception as e:
            # Fallback simples se dashboard não funcionar
            console.print("\n[cyan bold]📊 Agent Dashboard[/cyan bold]\n")

            table = Table(show_header=True, border_style="dim")
            table.add_column("Agent", style="cyan")
            table.add_column("Icon")
            table.add_column("Status")

            agents = [
                ("Sophia (Architect)", "👑", "Ready"),
                ("Code Generator", "💻", "Ready"),
                ("Test Generator", "🧪", "Ready"),
                ("Code Reviewer", "🔍", "Ready"),
                ("Bug Fixer", "🔧", "Ready"),
                ("Documentor", "📚", "Ready"),
                ("Explorer", "🗺️", "Ready"),
                ("Planner", "📋", "Ready"),
            ]

            for name, icon, status in agents:
                table.add_row(name, icon, f"[green]{status}[/green]")

            console.print(table)
            console.print("\n[dim]Press any key to continue...[/dim]\n")

    def _cmd_theme(self, theme_name: str):
        """Trocar tema"""
        if not theme_name.strip():
            console.print("\n[yellow]Available themes: neon, fire, ocean, matrix, cyberpunk[/yellow]\n")
            return

        try:
            self.theme_manager.set_theme(theme_name.strip())
            console.print(f"\n[green]✨ Theme changed to {theme_name}[/green]\n")
        except Exception as e:
            console.print(f"\n[red]Error changing theme: {e}[/red]\n")
            console.print("[yellow]Available themes: neon, fire, ocean, matrix, cyberpunk[/yellow]\n")

    def _get_prompt(self) -> HTML:
        """
        Gerar prompt formatado.
        Visual clean mas com personalidade.
        """
        # Indicadores de modo
        mode_indicator = ""
        if self.dream_mode:
            mode_indicator = "<cyan>💭</cyan> "
        if self.current_agent:
            mode_indicator += f"<yellow>{self.current_agent}</yellow> "

        # Prompt base
        return HTML(
            f"{mode_indicator}"
            "<b><ansicyan>max-code</ansicyan></b> "
            "<ansigreen>❯</ansigreen> "
        )

    def _process_command(self, user_input: str):
        """Processar comando ou natural language"""
        user_input = user_input.strip()

        if not user_input:
            return

        # Comando especial
        if user_input.startswith('/'):
            parts = user_input.split(maxsplit=1)
            cmd = parts[0]
            args = parts[1] if len(parts) > 1 else ""

            if cmd in self.commands:
                self.commands[cmd]['handler'](args)
            else:
                console.print(f"\n[red]❌ Unknown command: {cmd}[/red]")
                console.print("[yellow]💡 Type /help or press Ctrl+P[/yellow]\n")

        # Natural language
        else:
            self._process_natural(user_input)

    def _process_natural(self, message: str):
        """Processar natural language via Claude API"""
        try:
            # Aplicar DREAM mode se ativo
            if self.dream_mode:
                system_prompt = "You are in DREAM mode - provide critical analysis, identify potential issues, and suggest improvements. Be constructively skeptical."
                message = f"[CRITICAL ANALYSIS] {message}"
            else:
                system_prompt = None

            # Display streaming
            console.print()
            console.print("[dim]⚡ Thinking...[/dim]")

            # Stream response
            response_parts = []
            for chunk in self.claude_client.chat(message, stream=True, system=system_prompt):
                console.print(chunk, end="")
                response_parts.append(chunk)

            console.print("\n")

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")
            console.print("[yellow]💡 Check your authentication: max-code auth login[/yellow]\n")

    def run(self):
        """Rodar enhanced REPL"""
        # Welcome banner
        print_banner()

        console.print("[dim]Type /help for commands or Ctrl+P for command palette[/dim]")
        console.print()

        # Main loop
        while self.running:
            try:
                user_input = self.session.prompt(
                    self._get_prompt()
                ).strip()

                self._process_command(user_input)

            except KeyboardInterrupt:
                console.print()
                continue

            except EOFError:
                self._cmd_exit("")
                break

            except Exception as e:
                console.print(f"\n[red]❌ Error: {e}[/red]\n")
                continue


def start_enhanced_repl():
    """Entry point para enhanced REPL"""
    try:
        repl = EnhancedREPL()
        repl.run()
    except KeyboardInterrupt:
        console.print("\n[cyan]👋 Goodbye![/cyan]\n")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]\n")
        sys.exit(1)
