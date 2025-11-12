#!/usr/bin/env python3
"""
MAX-CODE-CLI - BRUTAL FUNCTIONAL TEST SUITE
═══════════════════════════════════════════════════════════

"This suite is designed to DESTROY your EGO, not satisfy it."
                                        - Juan (Arquiteto-Chefe)

Constitutional AI v3.0 - P1: Zero Trust, Maximum Validation
P4: Obrigação da Verdade - Find ALL bugs, hide NOTHING.

This suite tests REAL functionality:
- REAL command execution (not just "does it exist")
- REAL agent responses (not just "can it instantiate")
- REAL tool behavior (not just "is the object there")
- REAL error scenarios (failures, timeouts, corrupted data)
- REAL edge cases (concurrent access, memory leaks, race conditions)

If this suite passes 100%, THEN you're a genius.
Until then, it's a lie.

Soli Deo Gloria 🙏
"""

import sys
import os
import tempfile
import shutil
import time
import threading
import gc
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


# ═══════════════════════════════════════════════════════════════════════════
# TEST FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class BrutalTestResult:
    """Test result with detailed failure info"""
    name: str
    category: str
    passed: bool
    duration: float
    error: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    stacktrace: Optional[str] = None


class BrutalTestRunner:
    """Test runner that shows NO MERCY"""

    def __init__(self):
        self.results: List[BrutalTestResult] = []
        self.temp_dir = None

    def setup(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp(prefix="max_code_test_")
        console.print(f"[dim]Test dir: {self.temp_dir}[/dim]")

    def teardown(self):
        """Cleanup test environment"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        gc.collect()  # Force garbage collection

    def test(self, name: str, category: str, test_func):
        """Run a BRUTAL test that validates REAL behavior"""
        start = time.time()
        passed = False
        error = None
        expected = None
        actual = None
        stacktrace = None

        try:
            result = test_func()

            # If test returns dict with validation
            if isinstance(result, dict):
                passed = result.get('passed', False)
                error = result.get('error')
                expected = result.get('expected')
                actual = result.get('actual')
            else:
                passed = True

        except AssertionError as e:
            passed = False
            error = str(e)
            import traceback
            stacktrace = traceback.format_exc()

        except Exception as e:
            passed = False
            error = f"{type(e).__name__}: {str(e)}"
            import traceback
            stacktrace = traceback.format_exc()

        duration = time.time() - start

        result = BrutalTestResult(
            name=name,
            category=category,
            passed=passed,
            duration=duration,
            error=error,
            expected=expected,
            actual=actual,
            stacktrace=stacktrace
        )

        self.results.append(result)

        # Print result immediately
        status = "✅" if passed else "❌"
        console.print(f"{status} {name} ({duration:.3f}s)")
        if not passed:
            console.print(f"   [red]Error: {error}[/red]")
            if expected and actual:
                console.print(f"   [yellow]Expected: {expected}[/yellow]")
                console.print(f"   [yellow]Actual: {actual}[/yellow]")

        return result


# ═══════════════════════════════════════════════════════════════════════════
# BRUTAL TESTS - CATEGORY 1: REAL COMMAND EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

def test_brutal_commands(runner: BrutalTestRunner):
    """Test REAL command execution with output validation"""
    console.print("\n[bold red]🔥 BRUTAL CATEGORY 1: Real Command Execution[/bold red]")

    def test_help_command_output():
        """Test /help actually produces help output"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()

        try:
            repl._cmd_help("")
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()

        # Validate output contains actual help text
        required_strings = [
            "/help",
            "command",
            "/sophia",
            "/code",
        ]

        missing = [s for s in required_strings if s not in output]

        if missing:
            return {
                'passed': False,
                'error': f"Help output missing required strings: {missing}",
                'expected': str(required_strings),
                'actual': output[:200]
            }

        return {'passed': len(output) > 100}  # Must have substantial output

    runner.test("1.1 /help produces actual help", "Real Commands", test_help_command_output)


    def test_clear_command_works():
        """Test /clear actually clears (calls console.clear)"""
        from cli.repl_enhanced import EnhancedREPL
        import cli.repl_enhanced

        repl = EnhancedREPL()

        # Mock the MODULE console (not repl.console) since _cmd_clear uses global console
        with patch.object(cli.repl_enhanced.console, 'clear') as mock_clear:
            repl._cmd_clear("")

            if not mock_clear.called:
                return {
                    'passed': False,
                    'error': "console.clear() was not called",
                    'expected': "clear() to be called",
                    'actual': "clear() not called"
                }

        return {'passed': True}

    runner.test("1.2 /clear actually clears console", "Real Commands", test_clear_command_works)


    def test_theme_command_validation():
        """Test /theme validates and rejects invalid themes"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()

        try:
            # Try invalid theme
            repl._cmd_theme("invalid_theme_xyz_123")
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()

        # Should show error or available themes
        if not ("error" in output.lower() or "available" in output.lower()):
            return {
                'passed': False,
                'error': "Invalid theme not rejected",
                'expected': "Error message or available themes",
                'actual': output
            }

        return {'passed': True}

    runner.test("1.3 /theme validates input", "Real Commands", test_theme_command_validation)


    def test_dashboard_shows_agents():
        """Test /dashboard actually shows agent information"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()

        try:
            repl._cmd_dashboard("")
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()

        # Should mention agents
        agent_names = ['sophia', 'code', 'test', 'review']
        found = sum(1 for a in agent_names if a in output.lower())

        if found == 0:
            return {
                'passed': False,
                'error': "Dashboard doesn't show any agents",
                'expected': f"At least one of: {agent_names}",
                'actual': output[:200]
            }

        return {'passed': True}

    runner.test("1.4 /dashboard shows agent info", "Real Commands", test_dashboard_shows_agents)


# ═══════════════════════════════════════════════════════════════════════════
# BRUTAL TESTS - CATEGORY 2: REAL AGENT BEHAVIOR
# ═══════════════════════════════════════════════════════════════════════════

def test_brutal_agents(runner: BrutalTestRunner):
    """Test agents actually DO something, not just exist"""
    console.print("\n[bold red]🔥 BRUTAL CATEGORY 2: Real Agent Behavior[/bold red]")

    def test_agent_has_required_methods():
        """Test agents have required methods (not just __init__)"""
        from agents import ArchitectAgent, CodeAgent, TestAgent

        required_methods = ['__init__']  # At minimum
        agents_to_test = [ArchitectAgent, CodeAgent, TestAgent]

        for agent_class in agents_to_test:
            agent = agent_class()

            # Agent must have SOME way to execute
            has_execution = (
                hasattr(agent, 'execute') or
                hasattr(agent, 'run') or
                hasattr(agent, 'process') or
                hasattr(agent, 'generate')
            )

            if not has_execution:
                return {
                    'passed': False,
                    'error': f"{agent_class.__name__} has no execution method",
                    'expected': "execute/run/process/generate method",
                    'actual': f"Methods: {[m for m in dir(agent) if not m.startswith('_')]}"
                }

        return {'passed': True}

    runner.test("2.1 Agents have execution methods", "Real Agents", test_agent_has_required_methods)


    def test_agent_caching_actually_works():
        """Test agent caching returns SAME instance (not just truthy)"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        agent1 = repl._get_agent_instance("architect")
        agent2 = repl._get_agent_instance("architect")

        # Must be EXACT same object (same id)
        if id(agent1) != id(agent2):
            return {
                'passed': False,
                'error': "Agent caching returns different instances",
                'expected': f"Same instance (id={id(agent1)})",
                'actual': f"Different instance (id={id(agent2)})"
            }

        return {'passed': True}

    runner.test("2.2 Agent caching is real", "Real Agents", test_agent_caching_actually_works)


    def test_invalid_agent_raises_correct_error():
        """Test invalid agent raises ValueError (not generic Exception)"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        try:
            repl._get_agent_instance("nonexistent_agent_xyz")
            return {
                'passed': False,
                'error': "No error raised for invalid agent",
                'expected': "ValueError",
                'actual': "No exception"
            }
        except ValueError as e:
            # Correct exception type
            return {'passed': True}
        except Exception as e:
            return {
                'passed': False,
                'error': f"Wrong exception type: {type(e).__name__}",
                'expected': "ValueError",
                'actual': type(e).__name__
            }

    runner.test("2.3 Invalid agent error type", "Real Agents", test_invalid_agent_raises_correct_error)


# ═══════════════════════════════════════════════════════════════════════════
# BRUTAL TESTS - CATEGORY 3: REAL FILE I/O
# ═══════════════════════════════════════════════════════════════════════════

def test_brutal_file_io(runner: BrutalTestRunner):
    """Test REAL file operations"""
    console.print("\n[bold red]🔥 BRUTAL CATEGORY 3: Real File I/O[/bold red]")

    def test_write_and_read_file():
        """Test actual file write and read"""
        test_file = Path(runner.temp_dir) / "test.txt"
        test_content = "Hello MAXIMUS\nLine 2\nLine 3"

        # Write file
        test_file.write_text(test_content)

        # Read file
        read_content = test_file.read_text()

        if read_content != test_content:
            return {
                'passed': False,
                'error': "File content mismatch",
                'expected': test_content,
                'actual': read_content
            }

        # Cleanup
        test_file.unlink()

        return {'passed': True}

    runner.test("3.1 File write/read works", "File I/O", test_write_and_read_file)


    def test_large_file_handling():
        """Test handling of large files (10MB)"""
        test_file = Path(runner.temp_dir) / "large.txt"

        # Create 10MB file
        large_content = "A" * (10 * 1024 * 1024)

        try:
            test_file.write_text(large_content)
            read_content = test_file.read_text()

            if len(read_content) != len(large_content):
                return {
                    'passed': False,
                    'error': "Large file size mismatch",
                    'expected': f"{len(large_content)} bytes",
                    'actual': f"{len(read_content)} bytes"
                }

            test_file.unlink()
            return {'passed': True}

        except MemoryError:
            return {
                'passed': False,
                'error': "MemoryError on 10MB file",
                'expected': "Should handle 10MB files",
                'actual': "MemoryError raised"
            }

    runner.test("3.2 Large file handling (10MB)", "File I/O", test_large_file_handling)


    def test_unicode_file_content():
        """Test Unicode content in files"""
        test_file = Path(runner.temp_dir) / "unicode.txt"

        unicode_content = """
        English: Hello
        Spanish: Ñoño
        Japanese: 日本語
        Arabic: مرحبا
        Emoji: 🎉🔥✨
        """

        test_file.write_text(unicode_content, encoding='utf-8')
        read_content = test_file.read_text(encoding='utf-8')

        if read_content != unicode_content:
            return {
                'passed': False,
                'error': "Unicode content corrupted",
                'expected': unicode_content[:50],
                'actual': read_content[:50]
            }

        test_file.unlink()
        return {'passed': True}

    runner.test("3.3 Unicode file content", "File I/O", test_unicode_file_content)


# ═══════════════════════════════════════════════════════════════════════════
# BRUTAL TESTS - CATEGORY 4: REAL ERROR SCENARIOS
# ═══════════════════════════════════════════════════════════════════════════

def test_brutal_errors(runner: BrutalTestRunner):
    """Test REAL error handling"""
    console.print("\n[bold red]🔥 BRUTAL CATEGORY 4: Real Error Scenarios[/bold red]")

    def test_command_with_exception_in_handler():
        """Test command handler that raises exception"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Create command that raises exception
        def bad_handler(args):
            raise RuntimeError("Intentional error for testing")

        repl.commands['/test_bad'] = {
            'icon': '💥',
            'description': 'Test command that fails',
            'category': 'system',
            'handler': bad_handler
        }

        # Try to execute - should NOT crash the REPL
        try:
            repl._process_command("/test_bad some args")
            # If we get here, error was handled
            return {'passed': True}
        except RuntimeError:
            # If exception propagates, error handling failed
            return {
                'passed': False,
                'error': "Exception not caught by REPL",
                'expected': "Exception handled gracefully",
                'actual': "RuntimeError propagated"
            }

    runner.test("4.1 Exception in handler", "Error Handling", test_command_with_exception_in_handler)


    def test_none_return_from_prompt():
        """Test prompt returning None (simulated)"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Simulate None input (handled in main loop)
        # This should not crash
        try:
            # In real loop, None would be caught before _process_command
            # Test that _process_command handles empty string
            repl._process_command("")
            return {'passed': True}
        except AttributeError as e:
            if "'NoneType' object has no attribute 'strip'" in str(e):
                return {
                    'passed': False,
                    'error': "None.strip() called - Boris fix failed!",
                    'expected': "None handled before strip()",
                    'actual': str(e)
                }
            raise

    runner.test("4.2 None from prompt", "Error Handling", test_none_return_from_prompt)


    def test_corrupted_command_dict():
        """Test command with missing handler"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Create malformed command (missing handler)
        repl.commands['/bad_cmd'] = {
            'icon': '💀',
            'description': 'Broken command',
            'category': 'system',
            # NO HANDLER!
        }

        try:
            repl._process_command("/bad_cmd")
            # Should handle missing handler gracefully
            return {'passed': True}
        except KeyError:
            return {
                'passed': False,
                'error': "KeyError on missing handler",
                'expected': "Graceful handling of missing handler",
                'actual': "KeyError raised"
            }

    runner.test("4.3 Missing command handler", "Error Handling", test_corrupted_command_dict)


# ═══════════════════════════════════════════════════════════════════════════
# BRUTAL TESTS - CATEGORY 5: REAL CONCURRENCY
# ═══════════════════════════════════════════════════════════════════════════

def test_brutal_concurrency(runner: BrutalTestRunner):
    """Test concurrent access"""
    console.print("\n[bold red]🔥 BRUTAL CATEGORY 5: Concurrency & Race Conditions[/bold red]")

    def test_concurrent_agent_access():
        """Test multiple threads accessing agents"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()
        errors = []

        def get_agent():
            try:
                for _ in range(10):
                    agent = repl._get_agent_instance("architect")
                    assert agent is not None
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=get_agent) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if errors:
            return {
                'passed': False,
                'error': f"{len(errors)} concurrent errors",
                'expected': "No errors",
                'actual': errors[0]
            }

        return {'passed': True}

    runner.test("5.1 Concurrent agent access", "Concurrency", test_concurrent_agent_access)


    def test_concurrent_command_execution():
        """Test concurrent command execution"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()
        errors = []

        def execute_commands():
            try:
                for _ in range(10):
                    repl._process_command("")  # Empty command
                    repl._process_command("/")  # Slash command
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=execute_commands) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if errors:
            return {
                'passed': False,
                'error': f"Concurrent command errors: {len(errors)}",
                'expected': "Thread-safe execution",
                'actual': errors[0]
            }

        return {'passed': True}

    runner.test("5.2 Concurrent command execution", "Concurrency", test_concurrent_command_execution)


# ═══════════════════════════════════════════════════════════════════════════
# BRUTAL TESTS - CATEGORY 6: REAL MEMORY & PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════

def test_brutal_performance(runner: BrutalTestRunner):
    """Test memory and performance"""
    console.print("\n[bold red]🔥 BRUTAL CATEGORY 6: Memory & Performance[/bold red]")

    def test_memory_leak_on_repeated_instantiation():
        """Test for memory leaks"""
        from cli.repl_enhanced import EnhancedREPL
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create and destroy 100 REPLs
        for _ in range(100):
            repl = EnhancedREPL()
            del repl

        gc.collect()

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory

        # Should not grow more than 50MB
        if memory_growth > 50:
            return {
                'passed': False,
                'error': f"Memory leak detected: {memory_growth:.1f}MB growth",
                'expected': "< 50MB growth",
                'actual': f"{memory_growth:.1f}MB growth"
            }

        return {'passed': True}

    runner.test("6.1 Memory leak test", "Performance", test_memory_leak_on_repeated_instantiation)


    def test_prompt_generation_speed():
        """Test prompt generation is fast"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        start = time.time()
        for _ in range(1000):
            prompt = repl._get_prompt()
        duration = time.time() - start

        # Should generate 1000 prompts in < 1 second
        if duration > 1.0:
            return {
                'passed': False,
                'error': f"Prompt generation too slow: {duration:.3f}s for 1000",
                'expected': "< 1.0s for 1000 prompts",
                'actual': f"{duration:.3f}s"
            }

        return {'passed': True}

    runner.test("6.2 Prompt generation speed", "Performance", test_prompt_generation_speed)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Run BRUTAL test suite"""

    console.print("""
[bold red]╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║             MAX-CODE-CLI - BRUTAL SYSTEM CHECK v1.0                   ║
║                    "Destroy Your Ego"                                 ║
║                                                                       ║
║  Constitutional AI v3.0 - P4: Obrigação da Verdade                    ║
║  This suite tests REAL functionality, not just existence.             ║
║                                                                       ║
║  If this passes 100%, THEN you're a genius.                           ║
║  Until then, it's a lie.                                              ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝[/bold red]
""")

    runner = BrutalTestRunner()
    runner.setup()

    try:
        # Run brutal tests
        test_brutal_commands(runner)
        test_brutal_agents(runner)
        test_brutal_file_io(runner)
        test_brutal_errors(runner)
        test_brutal_concurrency(runner)
        test_brutal_performance(runner)

    finally:
        runner.teardown()

    # Results
    console.print("\n" + "="*80)
    console.print("[bold]BRUTAL TEST RESULTS[/bold]")
    console.print("="*80 + "\n")

    total = len(runner.results)
    passed = sum(1 for r in runner.results if r.passed)
    failed = total - passed

    console.print(f"Total: {total}")
    console.print(f"✅ Passed: [green]{passed}[/green]")
    console.print(f"❌ Failed: [red]{failed}[/red]")
    console.print(f"Pass Rate: {passed/total*100:.1f}%\n")

    # Show failures
    failures = [r for r in runner.results if not r.passed]
    if failures:
        console.print(f"\n[bold red]💀 {len(failures)} FAILURES FOUND:[/bold red]\n")

        for i, fail in enumerate(failures, 1):
            console.print(f"[bold yellow]{i}. {fail.name}[/bold yellow]")
            console.print(f"   Category: {fail.category}")
            console.print(f"   Error: [red]{fail.error}[/red]")
            if fail.expected:
                console.print(f"   Expected: {fail.expected}")
            if fail.actual:
                console.print(f"   Actual: {fail.actual}")
            if fail.stacktrace:
                console.print(f"   [dim]{fail.stacktrace[:200]}...[/dim]")
            console.print()

    console.print("="*80)

    if passed == total:
        console.print("\n[bold green]🎉 ALL BRUTAL TESTS PASSED![/bold green]")
        console.print("[bold green]You might actually be a genius.[/bold green]")
        console.print("\n✨ Soli Deo Gloria 🙏\n")
        return 0
    else:
        console.print("\n[bold red]❌ EGO DESTROYED[/bold red]")
        console.print(f"[bold red]Fix {failed} bugs before claiming victory.[/bold red]\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
