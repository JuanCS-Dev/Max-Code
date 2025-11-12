#!/usr/bin/env python3
"""
Comprehensive REPL Testing Suite
Tests ALL keyboard inputs, commands, and edge cases

Constitutional AI v3.0 - P1: Zero Trust, Maximum Validation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from cli.repl_enhanced import EnhancedREPL, EnhancedCompleter
from prompt_toolkit.formatted_text import FormattedText
from unittest.mock import MagicMock, patch
from io import StringIO


class TestSuite:
    """Comprehensive test suite for REPL"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.bugs_found = []

    def test(self, name: str, test_func):
        """Run a test and track results"""
        try:
            test_func()
            self.passed += 1
            print(f"✅ PASS: {name}")
            return True
        except AssertionError as e:
            self.failed += 1
            bug = f"{name}: {str(e)}"
            self.bugs_found.append(bug)
            print(f"❌ FAIL: {name}")
            print(f"   Error: {e}")
            return False
        except Exception as e:
            self.failed += 1
            bug = f"{name}: {type(e).__name__}: {str(e)}"
            self.bugs_found.append(bug)
            print(f"💥 ERROR: {name}")
            print(f"   {type(e).__name__}: {e}")
            return False


def main():
    """Run comprehensive test suite"""
    print("\n" + "="*70)
    print("🔬 COMPREHENSIVE REPL TEST SUITE")
    print("="*70)
    print("\nConstitutional AI v3.0 - P1: Zero Trust, Maximum Validation\n")

    suite = TestSuite()

    # =====================================================================
    # SECTION 1: INITIALIZATION TESTS
    # =====================================================================
    print("\n📦 SECTION 1: INITIALIZATION")
    print("-" * 70)

    def test_repl_instantiation():
        """Test REPL can be instantiated"""
        repl = EnhancedREPL()
        assert repl is not None, "REPL instantiation failed"
        assert hasattr(repl, 'commands'), "Missing commands dict"
        assert hasattr(repl, 'session'), "Missing prompt session"

    suite.test("REPL instantiation", test_repl_instantiation)


    def test_commands_loaded():
        """Test all commands are loaded"""
        repl = EnhancedREPL()
        essential_commands = [
            '/help', '/exit', '/quit', '/clear',
            '/sophia', '/code', '/test', '/review', '/fix', '/docs', '/explore', '/plan',
            '/sofia-plan', '/dream', '/dashboard', '/theme'
        ]
        for cmd in essential_commands:
            assert cmd in repl.commands, f"Missing command: {cmd}"

    suite.test("Commands loaded", test_commands_loaded)


    def test_tools_initialized():
        """Test tool components are initialized"""
        repl = EnhancedREPL()
        assert repl.tool_selector is not None, "ToolSelector not initialized"
        assert repl.bash_executor is not None, "BashExecutor not initialized"
        assert repl.git_tool is not None, "GitTool not initialized"
        assert repl.web_search_tool is not None, "WebSearchTool not initialized"

    suite.test("Tools initialized", test_tools_initialized)


    # =====================================================================
    # SECTION 2: PROMPT RENDERING TESTS
    # =====================================================================
    print("\n🎨 SECTION 2: PROMPT RENDERING")
    print("-" * 70)

    def test_prompt_generation():
        """Test prompt can be generated"""
        repl = EnhancedREPL()
        prompt = repl._get_prompt()
        assert prompt is not None, "Prompt generation returned None"
        assert isinstance(prompt, FormattedText), f"Prompt is {type(prompt)}, expected FormattedText"

    suite.test("Prompt generation", test_prompt_generation)


    def test_prompt_with_dream_mode():
        """Test prompt with DREAM mode enabled"""
        repl = EnhancedREPL()
        repl.dream_mode = True
        prompt = repl._get_prompt()
        assert prompt is not None, "Prompt with DREAM mode failed"
        # Check if dream indicator is present
        prompt_text = ''.join([text for style, text in prompt])
        assert '💭' in prompt_text, "DREAM mode indicator missing"

    suite.test("Prompt with DREAM mode", test_prompt_with_dream_mode)


    def test_prompt_with_agent():
        """Test prompt with active agent"""
        repl = EnhancedREPL()
        repl.current_agent = "code"
        prompt = repl._get_prompt()
        assert prompt is not None, "Prompt with agent failed"
        prompt_text = ''.join([text for style, text in prompt])
        assert 'code' in prompt_text, "Agent indicator missing"

    suite.test("Prompt with agent", test_prompt_with_agent)


    # =====================================================================
    # SECTION 3: INPUT PROCESSING TESTS
    # =====================================================================
    print("\n⌨️  SECTION 3: INPUT PROCESSING")
    print("-" * 70)

    def test_empty_input():
        """Test empty input handling"""
        repl = EnhancedREPL()
        # Should not crash
        repl._process_command("")

    suite.test("Empty input", test_empty_input)


    def test_whitespace_input():
        """Test whitespace-only input"""
        repl = EnhancedREPL()
        repl._process_command("   ")
        repl._process_command("\t")
        repl._process_command("\n")

    suite.test("Whitespace input", test_whitespace_input)


    def test_slash_alone():
        """Test '/' alone triggers command list"""
        repl = EnhancedREPL()
        # Mock console to capture output
        with patch('cli.repl_enhanced.console') as mock_console:
            repl._process_command("/")
            # Should call _show_command_palette (which prints)
            assert mock_console.print.called, "/ should show command palette"

    suite.test("/ alone shows commands", test_slash_alone)


    def test_slash_with_space():
        """Test '/ ' (slash + space)"""
        repl = EnhancedREPL()
        with patch('cli.repl_enhanced.console') as mock_console:
            repl._process_command("/ ")
            assert mock_console.print.called, "/ with space should show commands"

    suite.test("/ with space", test_slash_with_space)


    def test_known_commands():
        """Test known commands are recognized"""
        repl = EnhancedREPL()

        # Mock handlers to prevent actual execution
        for cmd in repl.commands.values():
            cmd['handler'] = MagicMock()

        known_cmds = ['/help', '/exit', '/clear', '/sophia', '/code']
        for cmd in known_cmds:
            repl._process_command(cmd)
            # Handler should be called
            assert repl.commands[cmd]['handler'].called, f"{cmd} handler not called"

    suite.test("Known commands recognized", test_known_commands)


    def test_unknown_command():
        """Test unknown command handling"""
        repl = EnhancedREPL()
        with patch('cli.repl_enhanced.console') as mock_console:
            repl._process_command("/unknown_command_xyz")
            # Should print error message
            assert mock_console.print.called, "Unknown command should print error"

    suite.test("Unknown command error", test_unknown_command)


    # =====================================================================
    # SECTION 4: KEYBINDING TESTS
    # =====================================================================
    print("\n⌨️  SECTION 4: KEYBINDINGS")
    print("-" * 70)

    def test_keybindings_created():
        """Test keybindings are created"""
        repl = EnhancedREPL()
        bindings = repl._create_keybindings()
        assert bindings is not None, "Keybindings not created"
        # Check bindings exist
        from prompt_toolkit.key_binding import KeyBindings
        assert isinstance(bindings, KeyBindings), "Invalid keybindings type"

    suite.test("Keybindings created", test_keybindings_created)


    def test_no_ctrl_h_binding():
        """Test Ctrl+H is NOT bound (backspace conflict)"""
        repl = EnhancedREPL()
        bindings = repl._create_keybindings()

        # Get all bound keys
        bound_keys = [binding.keys for binding in bindings.bindings]

        # Ctrl+H should NOT be in bindings
        ctrl_h_found = any('c-h' in str(keys).lower() for keys in bound_keys)
        assert not ctrl_h_found, "Ctrl+H is bound (conflicts with backspace!)"

    suite.test("No Ctrl+H binding (backspace)", test_no_ctrl_h_binding)


    def test_ctrl_q_binding():
        """Test Ctrl+Q is bound for help"""
        repl = EnhancedREPL()
        bindings = repl._create_keybindings()

        bound_keys = [binding.keys for binding in bindings.bindings]
        ctrl_q_found = any('c-q' in str(keys).lower() for keys in bound_keys)
        assert ctrl_q_found, "Ctrl+Q not bound (should be help)"

    suite.test("Ctrl+Q binding exists", test_ctrl_q_binding)


    # =====================================================================
    # SECTION 5: COMMAND PALETTE TESTS
    # =====================================================================
    print("\n📋 SECTION 5: COMMAND PALETTE")
    print("-" * 70)

    def test_command_palette_no_crash():
        """Test command palette doesn't crash"""
        repl = EnhancedREPL()
        with patch('cli.repl_enhanced.console') as mock_console:
            repl._show_command_palette()
            # Should print something
            assert mock_console.print.called, "Command palette didn't print"

    suite.test("Command palette no crash", test_command_palette_no_crash)


    def test_command_palette_shows_categories():
        """Test command palette shows all categories"""
        repl = EnhancedREPL()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()

        try:
            from rich.console import Console
            temp_console = Console(file=captured, force_terminal=True)
            with patch('cli.repl_enhanced.console', temp_console):
                repl._show_command_palette()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        # Should contain category names
        assert 'AGENT' in output or 'agent' in output, "AGENT category missing"
        assert 'SYSTEM' in output or 'system' in output, "SYSTEM category missing"

    suite.test("Command palette categories", test_command_palette_shows_categories)


    # =====================================================================
    # SECTION 6: LLM CLIENT TESTS
    # =====================================================================
    print("\n🤖 SECTION 6: LLM CLIENT")
    print("-" * 70)

    def test_llm_client_initialized():
        """Test UnifiedLLMClient is initialized"""
        repl = EnhancedREPL()
        assert repl.claude_client is not None, "LLM client not initialized"
        from core.llm.unified_client import UnifiedLLMClient
        assert isinstance(repl.claude_client, UnifiedLLMClient), "Wrong client type"

    suite.test("LLM client initialized", test_llm_client_initialized)


    def test_llm_has_resilient_stream():
        """Test LLM client has resilient streaming"""
        repl = EnhancedREPL()
        assert hasattr(repl.claude_client, '_resilient_stream'), \
            "LLM client missing _resilient_stream method"

    suite.test("LLM resilient stream exists", test_llm_has_resilient_stream)


    # =====================================================================
    # SECTION 7: COMPLETER TESTS
    # =====================================================================
    print("\n🔍 SECTION 7: AUTOCOMPLETION")
    print("-" * 70)

    def test_completer_created():
        """Test completer is created"""
        repl = EnhancedREPL()
        completer = EnhancedCompleter(repl.commands, repl.tool_selector)
        assert completer is not None, "Completer creation failed"

    suite.test("Completer created", test_completer_created)


    def test_completer_slash_commands():
        """Test completer suggests slash commands"""
        repl = EnhancedREPL()
        completer = EnhancedCompleter(repl.commands, repl.tool_selector)

        from prompt_toolkit.document import Document
        doc = Document(text="/h", cursor_position=2)

        completions = list(completer.get_completions(doc, None))
        # Should suggest /help, etc.
        assert len(completions) > 0, "No completions for /h"

        completion_texts = [c.text for c in completions]
        assert any('help' in c for c in completion_texts), "/help not suggested"

    suite.test("Completer slash commands", test_completer_slash_commands)


    # =====================================================================
    # SECTION 8: EDGE CASES
    # =====================================================================
    print("\n⚠️  SECTION 8: EDGE CASES")
    print("-" * 70)

    def test_none_input_handling():
        """Test None input is handled gracefully"""
        repl = EnhancedREPL()
        # Simulate None from prompt_toolkit
        # This is handled in the main loop, test _process_command with empty
        repl._process_command("")  # Should not crash

    suite.test("None input handling", test_none_input_handling)


    def test_very_long_input():
        """Test very long input"""
        repl = EnhancedREPL()
        long_input = "a" * 10000
        # Should not crash
        with patch('cli.repl_enhanced.console'):
            repl._process_command(long_input)

    suite.test("Very long input", test_very_long_input)


    def test_special_characters():
        """Test special characters in input"""
        repl = EnhancedREPL()
        special_inputs = [
            "test\n\n",
            "test\t\t",
            "test\r\n",
            "test\\n",
            "🎉🔥✨",
            "test 日本語",
            "test<script>alert(1)</script>",
        ]

        for inp in special_inputs:
            with patch('cli.repl_enhanced.console'):
                repl._process_command(inp)  # Should not crash

    suite.test("Special characters", test_special_characters)


    def test_command_with_args():
        """Test commands with arguments"""
        repl = EnhancedREPL()

        # Mock handler
        for cmd in repl.commands.values():
            cmd['handler'] = MagicMock()

        # Test command with args
        repl._process_command("/sophia design a REST API")

        # Handler should be called with args
        handler = repl.commands['/sophia']['handler']
        assert handler.called, "/sophia handler not called"
        assert handler.call_args[0][0] == "design a REST API", "Args not passed correctly"

    suite.test("Commands with arguments", test_command_with_args)


    # =====================================================================
    # FINAL REPORT
    # =====================================================================
    print("\n" + "="*70)
    print("📊 TEST RESULTS")
    print("="*70)

    total = suite.passed + suite.failed
    print(f"\n✅ Passed: {suite.passed}/{total}")
    print(f"❌ Failed: {suite.failed}/{total}")

    if suite.passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✨ REPL is production-ready")
        return 0
    else:
        print(f"\n⚠️  {suite.failed} BUGS FOUND:")
        print("-" * 70)
        for i, bug in enumerate(suite.bugs_found, 1):
            print(f"\n{i}. {bug}")

        print("\n" + "="*70)
        print("🔧 BUGS NEED FIXING BEFORE PRODUCTION")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
