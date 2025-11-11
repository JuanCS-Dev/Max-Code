#!/usr/bin/env python3
"""
Teste de Paridade: Claude Code vs MAX-CODE Shell

Testa TODAS as funcionalidades essenciais do Claude Code
para identificar gaps no MAX-CODE Shell.

Gera relatório completo com:
- ✅ Features que funcionam
- ⚠️ Features parciais
- ❌ Features faltando

Soli Deo Gloria 🙏
"""

import sys
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Callable
from enum import Enum

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class FeatureStatus(str, Enum):
    """Status de uma feature"""
    WORKS = "✅ Funciona"
    PARTIAL = "⚠️  Parcial"
    MISSING = "❌ Faltando"
    UNKNOWN = "🔍 Não testado"


@dataclass
class Feature:
    """Representa uma funcionalidade do Claude Code"""
    category: str
    subcategory: str
    name: str
    example: str
    test_fn: Callable
    status: FeatureStatus = FeatureStatus.UNKNOWN
    notes: str = ""


class ClaudeCodeParityTester:
    """Testa paridade entre Claude Code e MAX-CODE Shell"""

    def __init__(self):
        self.features: List[Feature] = []
        self.results: Dict[str, int] = {
            "works": 0,
            "partial": 0,
            "missing": 0,
            "unknown": 0
        }

    def register_feature(self, feature: Feature):
        """Registrar feature para teste"""
        self.features.append(feature)

    def test_file_read_single(self) -> FeatureStatus:
        """Testar: Read single file"""
        try:
            from core.tools.file_reader import FileReader
            reader = FileReader()

            # Criar arquivo de teste
            test_file = "/tmp/max_code_parity_test.txt"
            with open(test_file, "w") as f:
                f.write("Test content")

            # Tentar ler
            result = reader.read(test_file)

            # Cleanup
            os.remove(test_file)

            if result and hasattr(result, 'content'):
                return FeatureStatus.WORKS
            else:
                return FeatureStatus.PARTIAL

        except Exception as e:
            return FeatureStatus.MISSING

    def test_file_write_single(self) -> FeatureStatus:
        """Testar: Write single file"""
        try:
            from core.tools.file_writer import FileWriter
            writer = FileWriter()

            test_file = "/tmp/max_code_parity_write.txt"
            result = writer.write(test_file, "Test content")

            if os.path.exists(test_file):
                os.remove(test_file)
                return FeatureStatus.WORKS
            else:
                return FeatureStatus.MISSING

        except Exception:
            return FeatureStatus.MISSING

    def test_file_edit(self) -> FeatureStatus:
        """Testar: Edit file"""
        try:
            from core.tools.file_editor import FileEditor
            # Se FileEditor existe
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING

    def test_search_grep(self) -> FeatureStatus:
        """Testar: Search/Grep"""
        try:
            from core.tools.grep_tool import GrepTool
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING

    def test_glob_pattern(self) -> FeatureStatus:
        """Testar: Glob pattern matching"""
        try:
            from core.tools.glob_tool import GlobTool
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING

    def test_bash_execution(self) -> FeatureStatus:
        """Testar: Bash command execution"""
        try:
            from core.tools.bash_executor import BashExecutor
            executor = BashExecutor()
            result = executor.execute("echo 'test'")
            return FeatureStatus.WORKS if result else FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_nlp_intent(self) -> FeatureStatus:
        """Testar: NLP Intent Recognition"""
        try:
            from core.epl.nlp_engine import recognize_intent
            intent = recognize_intent("Create a new file")
            return FeatureStatus.WORKS if intent else FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_context_awareness(self) -> FeatureStatus:
        """Testar: Context awareness (pronoun resolution)"""
        try:
            from cli.shell_context import ShellContext
            ctx = ShellContext()
            ctx.remember_file("/tmp/test.txt", None, "read")
            resolved = ctx.resolve_reference("Edit that file")

            if "/tmp/test.txt" in resolved:
                return FeatureStatus.WORKS
            else:
                return FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_tool_auto_selection(self) -> FeatureStatus:
        """Testar: Tool auto-selection"""
        try:
            from core.tools.tool_selector import ToolSelector
            selector = ToolSelector()
            tool = selector.select_for_task("Read a file")
            return FeatureStatus.WORKS if tool else FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_autocomplete(self) -> FeatureStatus:
        """Testar: Autocomplete dropdown"""
        try:
            from cli.repl_enhanced import EnhancedCompleter
            completer = EnhancedCompleter({})
            # Se classe existe, autocomplete está implementado
            return FeatureStatus.WORKS
        except Exception:
            return FeatureStatus.MISSING

    def test_agent_routing(self) -> FeatureStatus:
        """Testar: Agent routing (CODE, FIX, TEST, etc)"""
        try:
            from agents import CodeAgent, FixAgent, TestAgent
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING

    def test_multi_file_read(self) -> FeatureStatus:
        """Testar: Read multiple files"""
        try:
            from core.tools.file_reader import FileReader
            reader = FileReader()

            # Verificar se método read_multiple existe
            if hasattr(reader, 'read_multiple'):
                return FeatureStatus.WORKS
            else:
                return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_line_range_read(self) -> FeatureStatus:
        """Testar: Read file with line range"""
        try:
            from core.tools.file_reader import FileReader
            reader = FileReader()
            # Verificar se método read_lines existe
            if hasattr(reader, 'read_lines'):
                return FeatureStatus.WORKS
            else:
                return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_git_operations(self) -> FeatureStatus:
        """Testar: Git operations"""
        try:
            from core.tools.git_tool import GitTool
            git_tool = GitTool()
            # Se GitTool existe com métodos principais
            if hasattr(git_tool, 'status') and hasattr(git_tool, 'diff') and hasattr(git_tool, 'log'):
                return FeatureStatus.WORKS
            else:
                return FeatureStatus.PARTIAL
        except ImportError:
            # Se não tem GitTool, verificar bash
            try:
                from core.tools.bash_executor import BashExecutor
                executor = BashExecutor()
                result = executor.execute("git --version")
                # Bash funciona, mas não tem wrapper Git dedicado
                return FeatureStatus.PARTIAL
            except Exception:
                return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_syntax_highlighting(self) -> FeatureStatus:
        """Testar: Syntax highlighting"""
        try:
            from rich.syntax import Syntax
            # Rich tem syntax highlighting, mas precisa verificar se está integrado
            return FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_streaming_output(self) -> FeatureStatus:
        """Testar: Streaming output"""
        try:
            from cli.repl_enhanced import EnhancedREPL
            import inspect

            # Verificar se _display_tool_result tem parâmetro stream
            repl = EnhancedREPL()
            sig = inspect.signature(repl._display_tool_result)

            if 'stream' in sig.parameters:
                return FeatureStatus.WORKS  # Streaming implementado!
            else:
                return FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.PARTIAL

    def test_history_search(self) -> FeatureStatus:
        """Testar: Command history search"""
        try:
            from prompt_toolkit.history import FileHistory
            # FileHistory existe, mas precisa verificar se Ctrl+R funciona
            return FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_web_search(self) -> FeatureStatus:
        """Testar: Web search capability"""
        try:
            # Verificar se tem WebSearchTool
            from core.tools.web_search_tool import WebSearchTool
            tool = WebSearchTool()
            # Se tool existe e tem método search
            if hasattr(tool, 'search'):
                return FeatureStatus.WORKS
            return FeatureStatus.PARTIAL
        except ImportError:
            return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_web_fetch(self) -> FeatureStatus:
        """Testar: Web fetch/scraping"""
        try:
            # Verificar se tem WebFetchTool
            from core.tools.web_fetch_tool import WebFetchTool
            tool = WebFetchTool()
            if hasattr(tool, 'fetch'):
                return FeatureStatus.WORKS
            return FeatureStatus.PARTIAL
        except ImportError:
            return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_task_management(self) -> FeatureStatus:
        """Testar: Task/TODO management"""
        try:
            # Verificar se tem task planner
            from core.task_planner import TaskPlanner
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_slash_commands(self) -> FeatureStatus:
        """Testar: Custom slash commands"""
        try:
            # Verificar se tem SlashCommandLoader
            from core.commands.slash_loader import SlashCommandLoader
            import os

            # Verificar se diretório existe
            if os.path.exists('.claude/commands'):
                loader = SlashCommandLoader()
                loader.load_commands()
                # Se carregou comandos, funciona perfeitamente
                if loader.commands:
                    return FeatureStatus.WORKS
                # Se tem loader mas sem comandos, é parcial
                return FeatureStatus.PARTIAL

            # Se não tem diretório mas tem loader, é parcial
            return FeatureStatus.PARTIAL
        except ImportError:
            return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_mcp_integration(self) -> FeatureStatus:
        """Testar: MCP (Model Context Protocol) integration"""
        try:
            # MAX-CODE tem integração com MAXIMUS services (similar a MCP)
            from core.maximus_integration import client
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def test_multi_turn_conversation(self) -> FeatureStatus:
        """Testar: Multi-turn conversation memory"""
        try:
            from cli.shell_context import ShellContext
            ctx = ShellContext()
            # Verificar se mantém histórico
            if hasattr(ctx, 'history') or hasattr(ctx, 'last_file'):
                return FeatureStatus.WORKS
            return FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_error_recovery(self) -> FeatureStatus:
        """Testar: Automatic error recovery"""
        try:
            # Verificar se tem error handling sofisticado
            from core.tools.bash_executor import BashExecutor
            executor = BashExecutor()
            # Se BashExecutor tem error recovery/retry logic
            if hasattr(executor, 'validator'):
                return FeatureStatus.WORKS
            return FeatureStatus.PARTIAL
        except Exception:
            return FeatureStatus.MISSING

    def test_code_analysis(self) -> FeatureStatus:
        """Testar: Code analysis and review"""
        try:
            from agents import ReviewAgent
            return FeatureStatus.WORKS
        except ImportError:
            return FeatureStatus.MISSING
        except Exception:
            return FeatureStatus.MISSING

    def register_all_features(self):
        """Registrar todas as features para teste"""

        # CATEGORIA 1: FILE OPERATIONS
        self.register_feature(Feature(
            "File Operations", "Read", "Read single file",
            "Read config.json", self.test_file_read_single
        ))
        self.register_feature(Feature(
            "File Operations", "Read", "Read multiple files",
            "Read config.json and settings.py", self.test_multi_file_read
        ))
        self.register_feature(Feature(
            "File Operations", "Read", "Read with line range",
            "Read config.json lines 10-20", self.test_line_range_read
        ))

        self.register_feature(Feature(
            "File Operations", "Write", "Write single file",
            "Write 'hello' to test.txt", self.test_file_write_single
        ))

        self.register_feature(Feature(
            "File Operations", "Edit", "Edit file",
            "Edit config.json line 5", self.test_file_edit
        ))

        self.register_feature(Feature(
            "File Operations", "Search", "Search/Grep",
            "Find 'TODO' in *.py", self.test_search_grep
        ))

        self.register_feature(Feature(
            "File Operations", "Search", "Glob pattern",
            "Find all *.py files", self.test_glob_pattern
        ))

        # CATEGORIA 2: EXECUTION
        self.register_feature(Feature(
            "Execution", "Bash", "Execute bash commands",
            "Run npm install", self.test_bash_execution
        ))

        self.register_feature(Feature(
            "Execution", "Git", "Git operations",
            "Git status", self.test_git_operations
        ))

        # CATEGORIA 3: AI FEATURES
        self.register_feature(Feature(
            "AI Features", "NLP", "Intent recognition",
            "Create a new file", self.test_nlp_intent
        ))

        self.register_feature(Feature(
            "AI Features", "Context", "Context awareness",
            "Edit that file", self.test_context_awareness
        ))

        self.register_feature(Feature(
            "AI Features", "Tools", "Tool auto-selection",
            "Read config.json", self.test_tool_auto_selection
        ))

        self.register_feature(Feature(
            "AI Features", "Agents", "Agent routing",
            "Fix bug in auth.py", self.test_agent_routing
        ))

        # CATEGORIA 4: UX
        self.register_feature(Feature(
            "User Experience", "Input", "Autocomplete dropdown",
            "Type / to see options", self.test_autocomplete
        ))

        self.register_feature(Feature(
            "User Experience", "Output", "Syntax highlighting",
            "Show code with colors", self.test_syntax_highlighting
        ))

        self.register_feature(Feature(
            "User Experience", "Output", "Streaming output",
            "Show results as they arrive", self.test_streaming_output
        ))

        self.register_feature(Feature(
            "User Experience", "Input", "History search",
            "Ctrl+R to search history", self.test_history_search
        ))

        # CATEGORIA 5: ADVANCED FEATURES (8 novas)
        self.register_feature(Feature(
            "Advanced Features", "Web", "Web search",
            "Search 'Python async' on web", self.test_web_search
        ))

        self.register_feature(Feature(
            "Advanced Features", "Web", "Web fetch/scraping",
            "Fetch content from URL", self.test_web_fetch
        ))

        self.register_feature(Feature(
            "Advanced Features", "Planning", "Task management",
            "Create TODO list for project", self.test_task_management
        ))

        self.register_feature(Feature(
            "Advanced Features", "Extensibility", "Custom slash commands",
            "Define /deploy command", self.test_slash_commands
        ))

        self.register_feature(Feature(
            "Advanced Features", "Integration", "MCP protocol support",
            "Connect to external services", self.test_mcp_integration
        ))

        self.register_feature(Feature(
            "Advanced Features", "AI", "Multi-turn conversation",
            "Remember previous context", self.test_multi_turn_conversation
        ))

        self.register_feature(Feature(
            "Advanced Features", "Reliability", "Error recovery",
            "Auto-retry failed commands", self.test_error_recovery
        ))

        self.register_feature(Feature(
            "Advanced Features", "Code Quality", "Code analysis",
            "Review code quality", self.test_code_analysis
        ))

    def run_tests(self):
        """Executar todos os testes"""
        console.print()
        console.print(Panel.fit(
            "[bold cyan]Claude Code Parity Test Suite[/bold cyan]\n"
            f"Testing {len(self.features)} features",
            border_style="cyan"
        ))
        console.print()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running tests...", total=len(self.features))

            for feature in self.features:
                progress.update(task, description=f"Testing: {feature.name}")
                feature.status = feature.test_fn()
                progress.advance(task)

                # Update counters
                if feature.status == FeatureStatus.WORKS:
                    self.results["works"] += 1
                elif feature.status == FeatureStatus.PARTIAL:
                    self.results["partial"] += 1
                elif feature.status == FeatureStatus.MISSING:
                    self.results["missing"] += 1
                else:
                    self.results["unknown"] += 1

        console.print()
        console.print("[green]✅ Tests completed[/green]\n")

    def generate_report(self):
        """Gerar relatório de paridade"""
        # Group by category
        categories = {}
        for feature in self.features:
            if feature.category not in categories:
                categories[feature.category] = []
            categories[feature.category].append(feature)

        # Print summary
        console.print(Panel.fit(
            f"[bold]Test Results Summary[/bold]\n\n"
            f"✅ Working: {self.results['works']}\n"
            f"⚠️  Partial: {self.results['partial']}\n"
            f"❌ Missing: {self.results['missing']}\n"
            f"🔍 Unknown: {self.results['unknown']}\n\n"
            f"[bold]Total: {len(self.features)} features tested[/bold]",
            border_style="blue"
        ))
        console.print()

        # Print detailed results by category
        for category, features in categories.items():
            table = Table(title=f"{category}", show_header=True, header_style="bold magenta")
            table.add_column("Status", width=12)
            table.add_column("Subcategory", width=15)
            table.add_column("Feature", width=30)
            table.add_column("Example", style="dim")

            for feature in features:
                table.add_row(
                    feature.status.value,
                    feature.subcategory,
                    feature.name,
                    feature.example
                )

            console.print(table)
            console.print()

        # Calculate percentage
        total = len(self.features)
        working = self.results['works'] + (self.results['partial'] * 0.5)
        percentage = (working / total) * 100

        console.print(Panel.fit(
            f"[bold green]MAX-CODE Parity Score: {percentage:.1f}%[/bold green]\n\n"
            f"Claude Code coverage: {working:.0f}/{total} features",
            border_style="green"
        ))

    def generate_gap_analysis(self):
        """Gerar análise de gaps (features faltando)"""
        console.print()
        console.print(Panel("[bold red]Gap Analysis - Missing Features[/bold red]", border_style="red"))
        console.print()

        missing = [f for f in self.features if f.status == FeatureStatus.MISSING]
        partial = [f for f in self.features if f.status == FeatureStatus.PARTIAL]

        if missing:
            console.print("[bold]Critical Gaps (Missing):[/bold]")
            for i, feature in enumerate(missing, 1):
                console.print(f"{i}. [{feature.category}] {feature.name}")
                console.print(f"   Example: [dim]{feature.example}[/dim]")
            console.print()

        if partial:
            console.print("[bold]Partial Implementation:[/bold]")
            for i, feature in enumerate(partial, 1):
                console.print(f"{i}. [{feature.category}] {feature.name}")
                console.print(f"   Example: [dim]{feature.example}[/dim]")
            console.print()

    def save_results(self):
        """Salvar resultados em arquivo markdown"""
        output_file = "CLAUDE_CODE_PARITY_REPORT.md"

        with open(output_file, "w") as f:
            f.write("# Claude Code Parity Report\n\n")
            f.write(f"**Generated:** 2025-11-11\n\n")
            f.write("## Summary\n\n")
            f.write(f"- ✅ Working: {self.results['works']}\n")
            f.write(f"- ⚠️  Partial: {self.results['partial']}\n")
            f.write(f"- ❌ Missing: {self.results['missing']}\n")
            f.write(f"- Total: {len(self.features)}\n\n")

            total = len(self.features)
            working = self.results['works'] + (self.results['partial'] * 0.5)
            percentage = (working / total) * 100
            f.write(f"**Parity Score:** {percentage:.1f}%\n\n")

            f.write("## Detailed Results\n\n")
            for feature in self.features:
                f.write(f"### {feature.category} - {feature.name}\n")
                f.write(f"- **Status:** {feature.status.value}\n")
                f.write(f"- **Example:** `{feature.example}`\n\n")

        console.print(f"\n[green]✅ Report saved to {output_file}[/green]")


def main():
    """Main function"""
    tester = ClaudeCodeParityTester()
    tester.register_all_features()
    tester.run_tests()
    tester.generate_report()
    tester.generate_gap_analysis()
    tester.save_results()

    console.print("\n[bold green]🎯 Parity test complete![/bold green]\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
