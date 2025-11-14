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

# Importar cliente LLM unificado com fallback Gemini
from core.llm.unified_client import UnifiedLLMClient

# Importar EPL NLP Engine para intent recognition
from core.epl.nlp_engine import recognize_intent, IntentType

# Importar Tool System para execução de ferramentas
from core.tools.tool_selector import ToolSelector

# Importar Context Manager para manter estado entre comandos
from cli.shell_context import ShellContext

# Importar Bash Executor para execução de comandos
from core.tools.bash_executor import BashExecutor

# Importar Git Wrapper para operações git
from core.tools.git_tool import GitTool

# Importar Web Search Tool
from core.tools.web_search_tool import WebSearchTool

# Importar Web Fetch Tool
from core.tools.web_fetch_tool import WebFetchTool

# Importar Slash Command Loader
from core.commands.slash_loader import SlashCommandLoader

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
    Completer com preview de comandos E ferramentas.
    Mostra descrição e exemplo de uso.

    Features:
    - /comandos (help, exit, clear, agents, config, etc)
    - /tools (read, write, edit, search, run, grep, glob)
    - Autocomplete inteligente com fuzzy matching
    """

    def __init__(self, commands: Dict[str, Dict], tool_selector=None):
        self.commands = commands
        self.tool_selector = tool_selector

        # Adicionar ferramentas principais ao autocomplete
        self.tools = {
            '/read': {
                'icon': '📖',
                'description': 'Read file contents - Example: /read config.json'
            },
            '/write': {
                'icon': '✍️',
                'description': 'Write content to file - Example: /write test.txt "content"'
            },
            '/edit': {
                'icon': '✏️',
                'description': 'Edit file with changes - Example: /edit config.json line 5 to "new value"'
            },
            '/search': {
                'icon': '🔍',
                'description': 'Search for pattern - Example: /search TODO in *.py'
            },
            '/grep': {
                'icon': '🔎',
                'description': 'Grep pattern in files - Example: /grep "import os" *.py'
            },
            '/run': {
                'icon': '⚡',
                'description': 'Execute bash command - Example: /run npm install'
            },
            '/bash': {
                'icon': '💻',
                'description': 'Run bash command - Example: /bash ls -la'
            },
            '/git': {
                'icon': '🌿',
                'description': 'Git operations - Example: /git status'
            },
            '/git-status': {
                'icon': '📍',
                'description': 'Show git status - Example: /git-status'
            },
            '/git-diff': {
                'icon': '🔀',
                'description': 'Show git diff - Example: /git-diff'
            },
            '/git-log': {
                'icon': '📜',
                'description': 'Show commit history - Example: /git-log'
            },
            '/git-branch': {
                'icon': '🌿',
                'description': 'List branches - Example: /git-branch'
            },
            '/search-web': {
                'icon': '🔍',
                'description': 'Search the web - Example: /search-web Python async'
            },
            '/web-search': {
                'icon': '🌐',
                'description': 'Search the web (alias) - Example: /web-search tutorials'
            },
            '/fetch': {
                'icon': '🌐',
                'description': 'Fetch URL content - Example: /fetch https://example.com'
            },
            '/web-fetch': {
                'icon': '📄',
                'description': 'Fetch URL (alias) - Example: /web-fetch https://docs.python.org'
            },
            # Development & Quality Tools (Phase 4)
            '/test': {
                'icon': '🧪',
                'description': 'Run tests with coverage - Example: /test --unit'
            },
            '/lint': {
                'icon': '🔍',
                'description': 'Run linters (flake8, black, isort) - Example: /lint --fix'
            },
            '/format': {
                'icon': '🎨',
                'description': 'Format code with black and isort - Example: /format'
            },
            '/typecheck': {
                'icon': '🔬',
                'description': 'Run mypy type checking - Example: /typecheck'
            },
            '/security': {
                'icon': '🔒',
                'description': 'Security scan (pip-audit, bandit) - Example: /security --full'
            },
            '/audit': {
                'icon': '📋',
                'description': 'Comprehensive audit script - Example: /audit'
            },
            '/coverage': {
                'icon': '📊',
                'description': 'Generate coverage reports - Example: /coverage'
            },
            '/ci': {
                'icon': '🚀',
                'description': 'Run CI checks locally - Example: /ci'
            },
            '/pre-push': {
                'icon': '✅',
                'description': 'Validate before pushing - Example: /pre-push'
            },
        }

    def get_completions(self, document, complete_event):
        """Gerar completions com metadata"""
        # 🔥 BORIS FIX: Use text_before_cursor and split to get current word
        text = document.text_before_cursor
        words = text.split()

        # Get the word being typed
        if not words:
            return

        word = words[-1]

        # Se não começar com /, não autocomplete
        if not word.startswith('/'):
            return

        # Completar comandos do shell
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

        # Completar ferramentas
        for tool_name, tool_meta in self.tools.items():
            if tool_name.startswith(word):
                display_meta = HTML(
                    f"<b>{tool_meta['icon']}</b> {tool_meta['description']}"
                )

                yield Completion(
                    tool_name,
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
        self.running = True

        # State
        self.current_agent: Optional[str] = None
        self.dream_mode: bool = False

        # Unified LLM client with Gemini fallback
        self.claude_client = UnifiedLLMClient()

        # Agent instances (lazy loading)
        self._agent_instances = {}

        # Shell Context para manter estado entre comandos
        self.context = ShellContext()

        # Tool Selector para auto-select tools (Read, Write, Edit, Bash, etc)
        self.tool_selector = ToolSelector()

        # Bash Executor para comandos shell diretos
        self.bash_executor = BashExecutor()

        # Git Tool para operações git
        self.git_tool = GitTool()

        # Web Search Tool
        self.web_search_tool = WebSearchTool(max_results=10)

        # Web Fetch Tool
        self.web_fetch_tool = WebFetchTool()

        # Slash Command Loader (custom commands from .claude/commands/*.md)
        self.slash_loader = SlashCommandLoader()
        self.slash_loader.load_commands()

        # Commands and session (need tool_selector to be initialized first)
        self.commands = self._load_commands()
        self.session = self._create_session()

        # Status bar for Constitutional AI monitoring
        from ui.status_bar import StatusBar
        self.status_bar = StatusBar(console=self.console)
        self.status_bar.update(
            git_branch=self._get_git_branch(),
            tokens_used=0
        )

    def _load_commands(self) -> Dict[str, Dict]:
        """
        Carregar TODOS comandos disponíveis.
        Inclui: agentes, especiais, SOFIA, DREAM, custom slash commands
        """
        commands = {
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

        # Add custom slash commands dynamically
        self._register_custom_commands(commands)

        return commands

    def _register_custom_commands(self, commands: Dict[str, Dict]):
        """
        Register custom slash commands from .claude/commands/*.md files.

        Boris: "Custom commands are user intentions crystallized.
        Load them, render them, execute them beautifully."
        """
        for cmd_name, slash_cmd in self.slash_loader.commands.items():
            # Create command key with / prefix
            cmd_key = f"/{cmd_name}"

            # Create handler that renders template and sends to Claude
            def make_handler(command):
                def handler(args_string: str):
                    # Parse arguments
                    args_list = args_string.split() if args_string else []

                    # Build args dict from command args definition
                    args_dict = {}
                    for i, arg_name in enumerate(command.args):
                        if i < len(args_list):
                            args_dict[arg_name] = args_list[i]
                        else:
                            args_dict[arg_name] = ""

                    # Render prompt with arguments
                    rendered_prompt = self.slash_loader.render_command(command.name, args_dict)

                    if not rendered_prompt:
                        console.print(f"[red]❌ Failed to render command: {command.name}[/red]")
                        return

                    # Display custom command execution
                    console.print(f"\n[dim]🎯 Executing custom command: /{command.name}[/dim]")

                    # Send to Claude for processing
                    self._process_natural(rendered_prompt)

                return handler

            # Register command
            commands[cmd_key] = {
                "icon": "⚡",  # Custom commands get lightning bolt icon
                "description": slash_cmd.description,
                "category": CommandCategory.AGENT,  # Treat as agent-like commands
                "handler": make_handler(slash_cmd)
            }

        # Log custom commands loaded
        if self.slash_loader.commands:
            console.print(f"[dim]✨ Loaded {len(self.slash_loader.commands)} custom command(s)[/dim]")

    def _create_session(self) -> PromptSession:
        """Criar prompt session com todas features"""
        history_file = Path.home() / '.max-code-history'

        return PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=EnhancedCompleter(self.commands, self.tool_selector),
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

        @bindings.add("c-s")
        def enter_sofia_plan(event):
            """SOFIA Plan Mode (Ctrl+S)"""
            event.app.exit()  # Exit prompt temporarily
            console.print("\n[bold cyan]🎯 SOFIA Plan Mode[/bold cyan]")
            console.print("[dim]Strategic planning with SOFIA wisdom...[/dim]\n")
            # Get plan input
            try:
                plan_input = input("What do you want to plan? › ").strip()
                if plan_input:
                    self._cmd_sofia_plan(plan_input)
            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Cancelled[/dim]\n")

        @bindings.add("c-q")
        def show_quick_help(event):
            """Quick Help (Ctrl+Q)"""
            # 🔥 BORIS FIX: Changed from Ctrl+H to Ctrl+Q
            # Reason: Backspace sends Ctrl+H in many terminals!
            from prompt_toolkit import print_formatted_text
            from prompt_toolkit.formatted_text import HTML

            print_formatted_text()
            print_formatted_text(HTML('<cyan><b>⚡ Quick Help - Keyboard Shortcuts</b></cyan>'))
            print_formatted_text()
            print_formatted_text(HTML('  <b>Ctrl+P</b>  Command Palette'))
            print_formatted_text(HTML('  <b>Ctrl+S</b>  SOFIA Plan Mode'))
            print_formatted_text(HTML('  <b>Ctrl+D</b>  Toggle DREAM Mode (critical analysis)'))
            print_formatted_text(HTML('  <b>Ctrl+A</b>  Agent Dashboard'))
            print_formatted_text(HTML('  <b>Ctrl+Q</b>  Quick Help (this help)'))
            print_formatted_text()
            print_formatted_text(HTML('  Type <b>/help</b> for full command list'))
            print_formatted_text()

        return bindings

    def _show_command_palette(self):
        """
        Show command list (simplified - no palette UI conflicts with event loop).

        🔥 BORIS FIX: Simplified to avoid asyncio conflicts
        Original CommandPalette has event loop issues when called from keybindings.
        """
        from rich.table import Table

        console.print("\n[bold cyan]📋 Available Commands[/bold cyan]\n")

        # Group commands by category
        by_category = {}
        for cmd_name, cmd_meta in self.commands.items():
            cat = cmd_meta['category'].value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((cmd_name, cmd_meta))

        # Display by category
        for category, cmds in sorted(by_category.items()):
            table = Table(title=f"{category.upper()}", show_header=False, border_style="dim")
            table.add_column("Command", style="cyan")
            table.add_column("Icon")
            table.add_column("Description", style="white")

            for cmd_name, cmd_meta in sorted(cmds):
                table.add_row(
                    cmd_name,
                    cmd_meta['icon'],
                    cmd_meta['description']
                )

            console.print(table)
            console.print()

        console.print("[dim]Type any command to use it, or /help for more info[/dim]\n")

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

            # Update status bar - agent thinking
            self.status_bar.update(
                active_agent=f"{agent_name.capitalize()}Agent",
                agent_status="thinking"
            )

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

            # Update status bar - agent active/completed
            self.status_bar.update(
                agent_status="idle"
            )

            # Display response with beautiful markdown rendering
            self._display_response(response)
            console.print()

        except Exception as e:
            # Reset status bar on error
            self.status_bar.update(
                active_agent=None,
                agent_status="idle"
            )
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

    def _get_git_branch(self) -> Optional[str]:
        """Get current git branch name."""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip() or None
        except Exception:
            pass
        return None

    def _get_prompt(self):
        """
        Generate beautiful prompt with MAXIMUS neon colors.

        🔥 BORIS FIX: Simplified to use basic ANSI colors (no hex)
        Fixes prompt_toolkit backspace bug and None returns.
        """
        from prompt_toolkit.formatted_text import FormattedText

        # Mode indicators
        prefix_parts = []
        if self.dream_mode:
            prefix_parts.append(('ansimagenta', '💭 '))
        if self.current_agent:
            prefix_parts.append(('ansiyellow', f'{self.current_agent} '))

        # Main prompt with ANSI colors (more stable than hex)
        # Green → Yellow gradient using ANSI
        prompt_parts = prefix_parts + [
            ('ansibrightgreen', 'm'),
            ('ansibrightgreen', 'a'),
            ('ansigreen', 'x'),
            ('ansiyellow', 'i'),
            ('ansiyellow', 'm'),
            ('ansibrightyellow', 'u'),
            ('ansiyellow', 's'),
            ('', ' '),
            ('ansicyan', '⚡'),
            ('', ' '),
            ('ansibrightgreen', '›'),
            ('', ' '),
        ]

        return FormattedText(prompt_parts)

    def _process_command(self, user_input: str):
        """Processar comando ou natural language"""
        # 🔥 PHASE 0.1 FIX: Recursion limit protection (Steve Jobs Suite 1.3)
        # Anthropic Pattern: Rule-based validation at entry point
        if not hasattr(self, '_recursion_depth'):
            self._recursion_depth = 0

        self._recursion_depth += 1

        # Max 50 recursive calls (prevents stack overflow)
        if self._recursion_depth > 50:
            console.print("\n[red]❌ Recursion limit reached (50 calls)[/red]")
            console.print("[yellow]⚠️  Possible infinite loop detected[/yellow]\n")
            self._recursion_depth = 0
            return

        try:
            user_input = user_input.strip()

            if not user_input:
                return

            # Comando especial
            if user_input.startswith('/'):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0]
                args = parts[1] if len(parts) > 1 else ""

                # ✨ BORIS FIX: `/` alone triggers Command Palette (like Claude Code)
                if cmd == '/' or cmd == '':
                    self._show_command_palette()
                    return

                # Verificar se é comando do shell (help, exit, etc)
                if cmd in self.commands:
                    # 🔥 BRUTAL FIX: Handle exceptions in command handlers
                    try:
                        handler = self.commands[cmd].get('handler')
                        if handler is None:
                            console.print(f"\n[red]❌ Command {cmd} has no handler[/red]\n")
                            return

                        handler(args)

                    except Exception as e:
                        console.print(f"\n[red]❌ Error executing {cmd}: {e}[/red]\n")
                        import traceback
                        if hasattr(self, 'debug') and self.debug:
                            console.print(f"[dim]{traceback.format_exc()}[/dim]")

                # Verificar se é comando de ferramenta (/read, /write, etc)
                elif cmd in ['/read', '/write', '/edit', '/search', '/grep', '/run', '/bash']:
                    # Remover o / e processar como natural language
                    tool_command = cmd[1:].capitalize() + ' ' + args
                    self._process_natural(tool_command)

                # Verificar se é comando de dev (Phase 4)
                elif cmd in ['/test', '/lint', '/format', '/typecheck', '/security', '/audit', '/coverage', '/ci', '/pre-push']:
                    self._handle_dev_command(cmd, args)

                else:
                    console.print(f"\n[red]❌ Unknown command: {cmd}[/red]")
                    console.print("[yellow]💡 Type /help or press Ctrl+P for commands[/yellow]")
                    console.print("[yellow]💡 Tools: /read, /write, /edit, /search, /grep, /run[/yellow]")
                    console.print("[yellow]💡 Dev: /test, /lint, /format, /typecheck, /security, /audit, /ci[/yellow]\n")

            # Natural language
            else:
                self._process_natural(user_input)

        finally:
            # 🔥 PHASE 0.1 FIX: Always decrement recursion counter
            self._recursion_depth -= 1

    def _process_natural(self, message: str):
        """
        Processar natural language com NLP Engine + Tool System.

        Flow:
        1. Resolve context references (that file, it, etc)
        2. NLP Intent Recognition (EPL)
        3. Router: Tool execution vs Agent vs Chat
        4. Update context
        """
        try:
            # STEP 0: Resolve context references
            original_message = message
            message = self.context.resolve_reference(message)
            if message != original_message:
                console.print(f"[dim]🔄 Resolved: {message}[/dim]")

            # STEP 1: Detect intent using EPL NLP Engine
            console.print("[dim]🧠 Analyzing intent...[/dim]")
            intent = recognize_intent(message)

            # STEP 2: Route based on message keywords (tool detection)
            message_lower = message.lower()

            # Detect tool commands by keywords
            tool_keywords = {
                'read': ['read', 'open', 'show', 'cat', 'display'],
                'write': ['write', 'create', 'save'],
                'edit': ['edit', 'change', 'modify', 'replace', 'update'],
                'search': ['find', 'search', 'grep', 'look for'],
                'run': ['run', 'execute', 'exec', 'bash'],
                'git': ['git status', 'git diff', 'git log', 'git branch', 'git commit', 'git push', 'git pull', 'git-'],
                'web-search': ['search-web', 'web-search', 'search web', 'google', 'duckduckgo'],
                'web-fetch': ['fetch', 'web-fetch', '/fetch', '/web-fetch', 'get url', 'download page']
            }

            detected_tool = None
            for tool, keywords in tool_keywords.items():
                if any(kw in message_lower for kw in keywords):
                    detected_tool = tool
                    break

            if detected_tool:
                # Direct tool execution (como Claude Code)
                self._execute_tool_command(message, detected_tool)

            elif intent.type in [IntentType.CODE, IntentType.FIX, IntentType.TEST,
                                IntentType.REVIEW, IntentType.DOCS, IntentType.PLAN]:
                # Route para agente especializado
                agent_map = {
                    IntentType.CODE: "code",
                    IntentType.FIX: "fix",
                    IntentType.TEST: "test",
                    IntentType.REVIEW: "review",
                    IntentType.DOCS: "docs",
                    IntentType.PLAN: "plan"
                }
                agent_name = agent_map.get(intent.type, "code")
                self._invoke_agent(agent_name, message)

            else:
                # Fallback: Chat mode com Claude
                self._chat_mode(message)

        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/red]\n")

    def _execute_tool_command(self, message: str, detected_tool: str):
        """Execute tool command using ToolSelector (auto-selects correct tool)"""
        try:
            # Special handling for bash commands (direct execution)
            if detected_tool == 'run':
                console.print("[dim]⚡ Executing bash command...[/dim]")

                # Extract command (remove "run" keyword)
                import re
                command = re.sub(r'^(run|execute|bash)\s+', '', message, flags=re.IGNORECASE)

                # Execute using BashExecutor
                result = self.bash_executor.execute(command)

                # Display result
                tool_result = {
                    "status": result.type,  # "success" or "error"
                    "tool": "bash",
                    "output": result.content[0].text if result.content else None,
                    "error": result.content[0].text if result.type == "error" else None
                }
                self._display_tool_result(tool_result)
                return

            # Special handling for git commands (Boris Technique)
            if detected_tool in ['git', 'git-status', 'git-diff', 'git-log', 'git-branch', 'git-commit', 'git-push', 'git-pull']:
                console.print("[dim]🌿 Executing git operation...[/dim]")

                import re

                # Parse git command
                # Examples:
                # "git status" -> status()
                # "git diff config.py" -> diff(file_path="config.py")
                # "git log --oneline" -> log(oneline=True)
                # "git commit -m 'message'" -> commit(message="message")

                # Extract git operation
                git_match = re.search(r'git[\s-]+(status|diff|log|branch|commit|push|pull)', message, re.IGNORECASE)

                if git_match:
                    operation = git_match.group(1).lower()

                    # Execute git operation
                    if operation == 'status':
                        verbose = '--verbose' in message.lower() or '-v' in message.lower()
                        result = self.git_tool.status(verbose=verbose)

                    elif operation == 'diff':
                        # Extract file path if specified
                        file_match = re.search(r'diff\s+([^\s]+)', message, re.IGNORECASE)
                        file_path = file_match.group(1) if file_match else None
                        staged = '--cached' in message.lower() or '--staged' in message.lower()
                        result = self.git_tool.diff(file_path=file_path, staged=staged)

                    elif operation == 'log':
                        oneline = '--oneline' in message.lower()
                        # Extract limit if specified (default 10)
                        limit_match = re.search(r'-n\s+(\d+)', message)
                        limit = int(limit_match.group(1)) if limit_match else 10
                        result = self.git_tool.log(limit=limit, oneline=oneline)

                    elif operation == 'branch':
                        list_all = '-a' in message.lower() or '--all' in message.lower()
                        result = self.git_tool.branch(list_all=list_all)

                    elif operation == 'commit':
                        # Extract commit message
                        msg_match = re.search(r'-m\s+["\']([^"\']+)["\']', message)
                        if msg_match:
                            commit_message = msg_match.group(1)
                            add_all = '-a' in message.lower() or '--all' in message.lower()
                            result = self.git_tool.commit(message=commit_message, add_all=add_all)
                        else:
                            result = ToolResult.error("❌ Commit message required. Use: git commit -m 'message'")

                    elif operation == 'push':
                        result = self.git_tool.push()

                    elif operation == 'pull':
                        result = self.git_tool.pull()

                    else:
                        result = ToolResult.error(f"❌ Git operation '{operation}' not supported yet")

                    # Display result
                    tool_result = {
                        "status": result.type,
                        "tool": f"git-{operation}",
                        "output": result.content[0].text if result.content else None,
                        "error": result.content[0].text if result.type == "error" else None
                    }
                    self._display_tool_result(tool_result)
                    return
                else:
                    # Fallback to bash executor for unknown git commands
                    result = self.bash_executor.execute(message)
                    tool_result = {
                        "status": result.type,
                        "tool": "git",
                        "output": result.content[0].text if result.content else None,
                        "error": result.content[0].text if result.type == "error" else None
                    }
                    self._display_tool_result(tool_result)
                    return

            # Special handling for web search (Boris Technique)
            if detected_tool == 'web-search':
                console.print("[dim]🔍 Searching the web...[/dim]")

                import re

                # Extract search query (remove trigger keywords)
                query = message
                for keyword in ['search-web', 'web-search', 'search web', 'google', 'duckduckgo', '/search-web', '/web-search']:
                    query = re.sub(r'\b' + re.escape(keyword) + r'\b', '', query, flags=re.IGNORECASE)
                query = query.strip()

                if not query:
                    result = ToolResult.error("❌ Please provide a search query\n\nExample: search-web Python async tutorial")
                else:
                    # Execute web search
                    result = self.web_search_tool.search(query)

                # Display result
                tool_result = {
                    "status": result.type,
                    "tool": "web-search",
                    "output": result.content[0].text if result.content else None,
                    "error": result.content[0].text if result.type == "error" else None
                }
                self._display_tool_result(tool_result)
                return

            # Special handling for web fetch (Boris Technique)
            if detected_tool == 'web-fetch':
                console.print("[dim]🌐 Fetching URL...[/dim]")

                import re

                # Extract URL (remove keywords)
                url = message
                for kw in ['fetch', 'web-fetch', '/fetch', '/web-fetch', 'get url', 'download page']:
                    url = re.sub(r'\b' + re.escape(kw) + r'\b', '', url, flags=re.IGNORECASE)
                url = url.strip()

                if not url or not url.startswith('http'):
                    result = ToolResult.error("❌ Please provide a valid URL\n\nExample: fetch https://example.com")
                else:
                    result = self.web_fetch_tool.fetch(url)

                tool_result = {
                    "status": result.type,
                    "tool": "web-fetch",
                    "output": result.content[0].text if result.content else None,
                    "error": result.content[0].text if result.type == "error" else None
                }
                self._display_tool_result(tool_result)
                return

            # Regular tool selection
            console.print("[dim]🔧 Selecting tool...[/dim]")

            # Usa ToolSelector.select_and_execute - ELE faz TUDO
            # (seleciona tool certa baseado na descrição e executa)
            result = self.tool_selector.select_and_execute(
                task_description=message,
                parameters={}  # ToolSelector extrai params do message
            )

            # Update context if file operation
            if "file" in message.lower() and result.status == "success":
                # Extract file path from message (simple regex)
                import re
                match = re.search(r'[\w/.]+\.\w+', message)
                if match:
                    file_path = match.group(0)
                    self.context.remember_file(file_path, None, detected_tool)

            # Display result
            tool_result = {
                "status": result.status,
                "tool": result.tool_name if hasattr(result, 'tool_name') else detected_tool,
                "output": str(result.content) if result.status == "success" else None,
                "error": result.error if result.status == "error" else None
            }
            self._display_tool_result(tool_result)

        except Exception as e:
            console.print(f"[red]❌ Tool execution failed: {e}[/red]\n")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")

    def _chat_mode(self, message: str):
        """
        Fallback: Chat direto com Claude API (Boris Streaming Technique).

        Philosophy:
        "Streaming creates the illusion of speed and keeps users engaged.
        The first word appearing in <200ms makes the system feel instant,
        even if the full response takes 10 seconds."
        """
        # Aplicar DREAM mode se ativo
        if self.dream_mode:
            system_prompt = "You are in DREAM mode - provide critical analysis, identify potential issues, and suggest improvements. Be constructively skeptical."
            message = f"[CRITICAL ANALYSIS] {message}"
        else:
            system_prompt = None

        # Beautiful streaming header (Boris style) with provider info
        active_provider = self.claude_client.get_active_provider()
        provider_emoji = "💭" if active_provider == "Claude" else "🔮"
        provider_label = "Claude Sonnet 4.5" if active_provider == "Claude" else "Gemini 2.5 Flash"

        console.print()
        console.print("[dim]" + "─" * 60 + "[/dim]")
        console.print(f"[bold cyan]{provider_emoji} {provider_label}[/bold cyan]")
        if active_provider == "Gemini":
            console.print("[yellow]⚡ Using Gemini fallback (Claude unavailable)[/yellow]")
        else:
            console.print("[dim]⚡ Streaming response...[/dim]")
        console.print()

        # Stream response with real-time display
        response_parts = []
        word_count = 0

        # 🔥 BORIS FIX: No try/except needed - UnifiedLLMClient handles fallback internally
        # Errors only surface if ALL providers fail (logged silently in unified_client)
        for chunk in self.claude_client.chat(message, stream=True, system=system_prompt):
            console.print(chunk, end="", style="white")
            response_parts.append(chunk)
            word_count += len(chunk.split())

            # Flush periodically for smooth streaming
            if word_count % 5 == 0:
                console.file.flush()

        # Footer
        console.print("\n")
        console.print("[dim]" + "─" * 60 + "[/dim]")
        console.print(f"[dim]✓ {word_count} words streamed[/dim]\n")

    def _display_tool_result(self, result, stream: bool = True):
        """
        Pretty print tool execution result with streaming (Boris Technique).

        Philosophy:
        "Output should appear instantly for small results, and stream
        gracefully for large results. The user should never wonder if
        the system is frozen."

        Args:
            result: Tool result dict
            stream: Enable streaming for large outputs (>500 chars)
        """
        import time
        from rich.syntax import Syntax

        output_text = result.get("output", "✅ Done")
        tool_name = result.get('tool', 'Tool')
        status = result.get("status")
        file_path = result.get("file_path", None)  # For syntax detection

        if status == "success":
            # Stream large outputs (Boris Technique: create sense of speed)
            if stream and output_text and len(output_text) > 500:
                # Show header immediately
                console.print()
                console.print(f"[bold green]✅ {tool_name}[/bold green]")
                console.print("[dim]" + "─" * 60 + "[/dim]")
                console.print()

                # Stream output word by word (feels fast but readable)
                words = output_text.split()
                for i, word in enumerate(words):
                    console.print(word, end=" ")

                    # Smart delay: faster for code, slower for prose
                    if word.endswith((':', ';', '{', '}', '(', ')')):
                        time.sleep(0.002)  # Very fast for code
                    elif word.endswith(('.', '!', '?')):
                        time.sleep(0.01)   # Slight pause at sentences
                    else:
                        time.sleep(0.005)  # Normal speed

                    # Flush every 10 words for smooth display
                    if i % 10 == 0:
                        console.file.flush()

                console.print()
                console.print()
                console.print("[dim]" + "─" * 60 + "[/dim]")
                console.print("[green]✓ Complete[/green]\n")
            else:
                # Show small outputs immediately with syntax highlighting if applicable
                display_content = self._apply_syntax_highlighting(
                    output_text,
                    file_path,
                    tool_name
                )

                console.print(Panel(
                    display_content,
                    title=f"✅ {tool_name}",
                    border_style="green"
                ))
        else:
            # Errors: always show immediately (no streaming)
            console.print(Panel(
                result.get("error", "Unknown error"),
                title=f"❌ {tool_name} Failed",
                border_style="red"
            ))
            console.print("[yellow]💡 Tip: Check command syntax or file permissions[/yellow]\n")

    def _apply_syntax_highlighting(self, content: str, file_path: Optional[str], tool_name: str):
        """
        Apply syntax highlighting to code output (Boris Technique).

        Philosophy:
        "Syntax highlighting isn't decoration - it's cognitive optimization.
        The right colors can reduce comprehension time by 40%."

        Args:
            content: Text content to display
            file_path: Optional file path for language detection
            tool_name: Tool name for context

        Returns:
            Rich Syntax object or plain string
        """
        from rich.syntax import Syntax
        from pathlib import Path

        # Only apply to file read operations or code-like content
        if tool_name not in ['read', 'FileReader', 'bash', 'file_reader']:
            return content

        # Detect language from file path
        language = "text"
        if file_path:
            ext = Path(file_path).suffix.lstrip('.')
            language_map = {
                'py': 'python',
                'js': 'javascript',
                'ts': 'typescript',
                'tsx': 'typescript',
                'jsx': 'javascript',
                'json': 'json',
                'yaml': 'yaml',
                'yml': 'yaml',
                'toml': 'toml',
                'md': 'markdown',
                'sh': 'bash',
                'bash': 'bash',
                'zsh': 'bash',
                'sql': 'sql',
                'html': 'html',
                'css': 'css',
                'rs': 'rust',
                'go': 'go',
                'java': 'java',
                'c': 'c',
                'cpp': 'cpp',
                'h': 'c',
                'hpp': 'cpp',
            }
            language = language_map.get(ext, "text")

        # Apply syntax highlighting if language detected
        if language != "text":
            try:
                return Syntax(
                    content,
                    language,
                    theme="monokai",
                    line_numbers=False,  # Already in output
                    word_wrap=True
                )
            except Exception:
                # Fallback to plain text if highlighting fails
                return content

        return content

    def _handle_dev_command(self, cmd: str, args: str):
        """
        Handle development commands (Phase 4).

        Commands: /test, /lint, /format, /typecheck, /security, /audit, /coverage, /ci, /pre-push
        """
        import subprocess

        console.print(f"\n[cyan]🚀 Running {cmd}...[/cyan]\n")

        # Map commands to subprocess calls
        cmd_map = {
            '/test': ['pytest', 'tests/', '--cov=sdk', '--cov=cli', '--cov=config', '--cov-report=term-missing'],
            '/lint': ['flake8', 'sdk/', 'cli/', 'config/', '--count', '--statistics'],
            '/format': ['black', 'sdk/', 'cli/', 'config/', 'tests/'],
            '/typecheck': ['mypy', 'sdk/', 'cli/', 'config/', '--config-file=mypy.ini'],
            '/security': ['pip-audit', '--desc'],
            '/audit': ['bash', 'audit-cli.sh'],
            '/coverage': ['pytest', 'tests/', '--cov=sdk', '--cov=cli', '--cov=config', '--cov-report=html', '--cov-report=xml'],
            '/ci': ['make', 'ci'],
            '/pre-push': ['make', 'pre-push'],
        }

        # Handle --fix flag for lint
        if cmd == '/lint' and '--fix' in args:
            console.print("[yellow]→[/yellow] Formatting with black...")
            subprocess.run(['black', 'sdk/', 'cli/', 'config/', 'tests/'])
            console.print("\n[yellow]→[/yellow] Sorting imports with isort...")
            subprocess.run(['isort', 'sdk/', 'cli/', 'config/', 'tests/'])
            console.print("\n[yellow]→[/yellow] Checking with flake8...")
            subprocess.run(cmd_map['/lint'])
            console.print("\n[green]✅ Code formatted and linted![/green]\n")
            return

        # Handle --full flag for security
        if cmd == '/security' and '--full' in args:
            console.print("[yellow]→[/yellow] Running pip-audit...")
            subprocess.run(['pip-audit', '--desc', '--fix-dry-run'])
            console.print("\n[yellow]→[/yellow] Running bandit...")
            subprocess.run(['bandit', '-r', 'sdk/', 'cli/', 'config/'])
            console.print("\n[green]✅ Security scan complete![/green]\n")
            return

        # Handle --unit flag for test
        if cmd == '/test' and '--unit' in args:
            console.print("[yellow]→[/yellow] Running unit tests...")
            subprocess.run(['pytest', 'tests/unit/', '-v'])
            console.print("\n[green]✅ Unit tests complete![/green]\n")
            return

        # Run default command
        if cmd in cmd_map:
            result = subprocess.run(cmd_map[cmd])

            if result.returncode == 0:
                console.print(f"\n[green]✅ {cmd} completed successfully![/green]\n")
            else:
                console.print(f"\n[red]❌ {cmd} failed![/red]\n")
        else:
            console.print(f"\n[red]❌ Unknown dev command: {cmd}[/red]\n")

    def run(self):
        """Run enhanced REPL with magnificent visuals"""
        # Welcome banner
        print_banner()

        console.print("[dim]✨ Shortcuts: Ctrl+P (palette) | Ctrl+S (SOFIA plan) | Ctrl+D (DREAM) | Ctrl+Q (help)[/dim]")
        console.print()

        # Display initial status bar
        console.print("[dim]Status:[/dim]")
        self.status_bar.render()
        console.print()

        # Main loop
        while self.running:
            try:
                user_input = self.session.prompt(
                    self._get_prompt()
                )

                # 🔥 BORIS FIX: Protect against None from prompt_toolkit
                if user_input is None:
                    continue

                user_input = user_input.strip()
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
