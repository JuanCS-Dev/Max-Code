"""
Comprehensive UI Testing Suite - Week 3 Day 5

Complete test coverage for all UI components:
- Banner system
- Formatter
- Progress indicators
- Agent display
- Menus
- Tree of Thoughts
- Streaming
- Error handling
"""

import sys
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')

import time
from datetime import datetime
from io import StringIO
from rich.console import Console

# Import all UI components
from ui.banner import MaxCodeBanner
from ui.banner_vcli_style import show_banner as show_vcli_banner
from ui.formatter import MaxCodeFormatter
from ui.progress import MaxCodeProgress
from ui.agents import AgentDisplay, Agent, AgentStatus, AgentEvent, AgentMessage
from ui.tree_of_thoughts import (
    ThoughtTree, ThoughtNode, BranchStatus,
    ReasoningSteps, ReasoningStep,
    ConstitutionalAnalysis, ConstitutionalScore
)
from ui.streaming import StreamingDisplay, LiveLogViewer, LogEntry, LogLevel
from ui.validation import *
from ui.exceptions import *


class UITestSuite:
    """Comprehensive UI test suite."""

    def __init__(self):
        self.console = Console(file=StringIO())
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []

    # ========================================================================
    # TEST HELPERS
    # ========================================================================

    def assert_true(self, condition: bool, message: str):
        """Assert condition is true."""
        if condition:
            self.tests_passed += 1
            self.test_results.append(('PASS', message))
            print(f"  ✓ {message}")
        else:
            self.tests_failed += 1
            self.test_results.append(('FAIL', message))
            print(f"  ✗ {message}")

    def assert_no_exception(self, func, *args, message: str = ""):
        """Assert function doesn't raise exception."""
        try:
            func(*args)
            self.tests_passed += 1
            self.test_results.append(('PASS', message or f"{func.__name__} succeeded"))
            print(f"  ✓ {message or f'{func.__name__} succeeded'}")
            return True
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append(('FAIL', f"{message or func.__name__}: {e}"))
            print(f"  ✗ {message or func.__name__}: {e}")
            return False

    def assert_raises(self, exception_type, func, *args, message: str = ""):
        """Assert function raises specific exception."""
        try:
            func(*args)
            self.tests_failed += 1
            self.test_results.append(('FAIL', f"{message}: Expected {exception_type.__name__} but no exception raised"))
            print(f"  ✗ {message}: Expected exception but none raised")
            return False
        except exception_type:
            self.tests_passed += 1
            self.test_results.append(('PASS', f"{message}: Correctly raised {exception_type.__name__}"))
            print(f"  ✓ {message}: Correctly raised {exception_type.__name__}")
            return True
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append(('FAIL', f"{message}: Expected {exception_type.__name__} but got {type(e).__name__}"))
            print(f"  ✗ {message}: Wrong exception type: {type(e).__name__}")
            return False

    # ========================================================================
    # BANNER TESTS
    # ========================================================================

    def test_banner(self):
        """Test banner system."""
        print("\n" + "=" * 80)
        print("TEST SUITE 1: BANNER SYSTEM")
        print("=" * 80)

        banner = MaxCodeBanner(console=self.console)

        # Test 1: Basic banner display
        self.assert_no_exception(
            banner.show,
            "3.0",
            message="Banner shows with version"
        )

        # Test 2: Banner with context
        self.assert_no_exception(
            lambda: banner.show("3.0", context={'model': 'Claude Sonnet 4.5'}),
            message="Banner shows with context"
        )

        # Test 3: Different styles
        for style in ['default', 'isometric', 'banner', 'bold']:
            self.assert_no_exception(
                lambda s=style: banner.show("3.0", style=s),
                message=f"Banner shows with style '{style}'"
            )

        # Test 4: vCLI-style banner
        original_console = Console
        self.assert_no_exception(
            lambda: show_vcli_banner("3.0", build_date="2025-11-04"),
            message="vCLI-style banner shows"
        )

    # ========================================================================
    # FORMATTER TESTS
    # ========================================================================

    def test_formatter(self):
        """Test formatter system."""
        print("\n" + "=" * 80)
        print("TEST SUITE 2: FORMATTER SYSTEM")
        print("=" * 80)

        fmt = MaxCodeFormatter(console=self.console)

        # Test 1: Success message
        self.assert_no_exception(
            fmt.print_success,
            "Test succeeded",
            message="Success message prints"
        )

        # Test 2: Error message
        self.assert_no_exception(
            lambda: fmt.print_error("Test error", "Detail"),
            message="Error message prints"
        )

        # Test 3: Warning message
        self.assert_no_exception(
            fmt.print_warning,
            "Test warning",
            message="Warning message prints"
        )

        # Test 4: Info message
        self.assert_no_exception(
            fmt.print_info,
            "Test info",
            message="Info message prints"
        )

        # Test 5: Debug message
        self.assert_no_exception(
            fmt.print_debug,
            "Test debug",
            message="Debug message prints"
        )

        # Test 6: Agent message
        self.assert_no_exception(
            lambda: fmt.print_agent_message("Sophia", "Analyzing", "Test"),
            message="Agent message prints"
        )

        # Test 7: Code highlighting
        self.assert_no_exception(
            lambda: fmt.print_code("print('Hello')", language="python"),
            message="Code highlighting works"
        )

        # Test 8: Table display
        data = [
            {'Name': 'Test1', 'Value': '123'},
            {'Name': 'Test2', 'Value': '456'},
        ]
        self.assert_no_exception(
            lambda: fmt.print_table(data, title="Test Table"),
            message="Table displays"
        )

        # Test 9: Constitutional status
        status = {'p1': True, 'p2': True, 'p3': False}
        self.assert_no_exception(
            lambda: fmt.print_constitutional_status(status),
            message="Constitutional status displays"
        )

    # ========================================================================
    # PROGRESS TESTS
    # ========================================================================

    def test_progress(self):
        """Test progress indicators."""
        print("\n" + "=" * 80)
        print("TEST SUITE 3: PROGRESS INDICATORS")
        print("=" * 80)

        progress = MaxCodeProgress(console=self.console)

        # Test 1: Spinner (short duration)
        def test_spinner():
            with progress.spinner("Testing..."):
                time.sleep(0.1)

        self.assert_no_exception(
            test_spinner,
            message="Spinner works"
        )

        # Test 2: Progress bar
        def test_bar():
            with progress.bar(total=10, description="Testing") as bar:
                for i in range(10):
                    bar.advance(1)

        self.assert_no_exception(
            test_bar,
            message="Progress bar works"
        )

        # Test 3: Multi-progress
        def test_multi():
            tasks = [
                {'name': 'Task1', 'total': 10, 'color': 'cyan'},
                {'name': 'Task2', 'total': 10, 'color': 'green'},
            ]
            with progress.multi_progress(tasks) as bars:
                for i in range(10):
                    bars['Task1'].advance(1)
                    bars['Task2'].advance(1)

        self.assert_no_exception(
            test_multi,
            message="Multi-progress works"
        )

    # ========================================================================
    # AGENT DISPLAY TESTS
    # ========================================================================

    def test_agent_display(self):
        """Test agent display system."""
        print("\n" + "=" * 80)
        print("TEST SUITE 4: AGENT DISPLAY")
        print("=" * 80)

        display = AgentDisplay(console=self.console)

        # Test 1: Dashboard with agents
        agents = [
            Agent("Sophia", "Architect", AgentStatus.ACTIVE, "Analyzing", 75.0),
            Agent("Code", "Developer", AgentStatus.ACTIVE, "Coding", 50.0),
            Agent("Test", "Validator", AgentStatus.IDLE, "Waiting", 0.0),
        ]
        self.assert_no_exception(
            lambda: display.show_dashboard(agents),
            message="Dashboard displays with agents"
        )

        # Test 2: Empty agents list
        self.assert_no_exception(
            lambda: display.show_dashboard([]),
            message="Dashboard handles empty list gracefully"
        )

        # Test 3: Agent with invalid progress (should clamp)
        bad_agent = Agent("Bad", "Test", AgentStatus.ACTIVE, "Test", 150.0)
        self.assert_no_exception(
            lambda: display.show_dashboard([bad_agent]),
            message="Dashboard handles invalid progress"
        )

        # Test 4: Agent with None task
        none_agent = Agent("None", "Test", AgentStatus.ACTIVE, None, 50.0)
        self.assert_no_exception(
            lambda: display.show_dashboard([none_agent]),
            message="Dashboard handles None task"
        )

        # Test 5: Timeline
        events = [
            AgentEvent(datetime.now(), "Sophia", "Started analysis"),
            AgentEvent(datetime.now(), "Code", "Coding", 5.2),
        ]
        self.assert_no_exception(
            lambda: display.show_timeline(events),
            message="Timeline displays"
        )

        # Test 6: Communication flow
        messages = [
            AgentMessage("Sophia", "Code", "request", "received", datetime.now()),
            AgentMessage("Code", "Test", "update", "sent", datetime.now()),
        ]
        self.assert_no_exception(
            lambda: display.show_communication(messages),
            message="Communication flow displays"
        )

        # Test 7: Workload
        self.assert_no_exception(
            lambda: display.show_workload(agents),
            message="Workload displays"
        )

    # ========================================================================
    # TREE OF THOUGHTS TESTS
    # ========================================================================

    def test_tree_of_thoughts(self):
        """Test Tree of Thoughts visualization."""
        print("\n" + "=" * 80)
        print("TEST SUITE 5: TREE OF THOUGHTS")
        print("=" * 80)

        tree = ThoughtTree(console=self.console)

        # Test 1: Basic tree
        root = ThoughtNode("root", "Root thought", 7.5, BranchStatus.ACTIVE)
        children = {
            "root": [
                ThoughtNode("child1", "Child 1", 8.0, BranchStatus.BEST, "root", 1),
                ThoughtNode("child2", "Child 2", 7.0, BranchStatus.ACTIVE, "root", 1),
            ]
        }
        self.assert_no_exception(
            lambda: tree.show_tree(root, children),
            message="Tree displays"
        )

        # Test 2: Reasoning steps
        reasoning = ReasoningSteps(console=self.console)
        steps = [
            ReasoningStep(1, "Think", "Reasoning", 8.0, "continue", "Good"),
            ReasoningStep(2, "Decide", "Decision", 9.0, "select", "Best"),
        ]
        self.assert_no_exception(
            lambda: reasoning.show_steps(steps),
            message="Reasoning steps display"
        )

        # Test 3: Constitutional analysis
        analysis = ConstitutionalAnalysis(console=self.console)
        scores = [
            ConstitutionalScore("P1", "Transcendence", 8.0, "Good", "violet"),
            ConstitutionalScore("P2", "Reasoning", 9.0, "Excellent", "blue"),
        ]
        self.assert_no_exception(
            lambda: analysis.show_analysis(scores),
            message="Constitutional analysis displays"
        )

        # Test 4: Radar chart
        self.assert_no_exception(
            lambda: analysis.show_radar_chart(scores),
            message="Radar chart displays"
        )

    # ========================================================================
    # STREAMING TESTS
    # ========================================================================

    def test_streaming(self):
        """Test streaming output."""
        print("\n" + "=" * 80)
        print("TEST SUITE 6: STREAMING OUTPUT")
        print("=" * 80)

        stream = StreamingDisplay(console=self.console)

        # Test 1: Text streaming
        def text_gen():
            for word in "Test streaming output".split():
                yield word + " "

        self.assert_no_exception(
            lambda: stream.stream_text(text_gen(), prefix="Output:"),
            message="Text streaming works"
        )

        # Test 2: Log viewer
        log_viewer = LiveLogViewer(console=self.console)

        def log_gen():
            yield LogEntry(datetime.now(), LogLevel.INFO, "Test log", "Test")
            yield LogEntry(datetime.now(), LogLevel.ERROR, "Test error", "Test")

        self.assert_no_exception(
            lambda: log_viewer.view_logs_table(log_gen(), max_rows=10),
            message="Log viewer works"
        )

    # ========================================================================
    # VALIDATION TESTS
    # ========================================================================

    def test_validation(self):
        """Test validation utilities."""
        print("\n" + "=" * 80)
        print("TEST SUITE 7: VALIDATION")
        print("=" * 80)

        # Test 1: validate_items - valid
        self.assert_no_exception(
            lambda: validate_items([1, 2, 3], min_items=1),
            message="validate_items accepts valid list"
        )

        # Test 2: validate_items - empty
        self.assert_raises(
            EmptyDataError,
            lambda: validate_items([], min_items=1),
            message="validate_items rejects empty list"
        )

        # Test 3: validate_score - valid
        self.assert_no_exception(
            lambda: validate_score(5.0, 0.0, 10.0),
            message="validate_score accepts valid score"
        )

        # Test 4: validate_score - invalid
        self.assert_raises(
            InvalidInputError,
            lambda: validate_score(15.0, 0.0, 10.0),
            message="validate_score rejects out of range"
        )

        # Test 5: validate_percentage - valid
        self.assert_no_exception(
            lambda: validate_percentage(50.0),
            message="validate_percentage accepts valid percentage"
        )

        # Test 6: validate_percentage - invalid
        self.assert_raises(
            InvalidInputError,
            lambda: validate_percentage(150.0),
            message="validate_percentage rejects >100"
        )

        # Test 7: validate_string - valid
        self.assert_no_exception(
            lambda: validate_string("test", min_length=1),
            message="validate_string accepts valid string"
        )

        # Test 8: validate_positive_int - valid
        self.assert_no_exception(
            lambda: validate_positive_int(5),
            message="validate_positive_int accepts positive"
        )

        # Test 9: validate_positive_int - invalid
        self.assert_raises(
            InvalidInputError,
            lambda: validate_positive_int(-5),
            message="validate_positive_int rejects negative"
        )

        # Test 10: validate_choice - valid
        self.assert_no_exception(
            lambda: validate_choice("a", ["a", "b", "c"]),
            message="validate_choice accepts valid choice"
        )

        # Test 11: validate_choice - invalid
        self.assert_raises(
            InvalidInputError,
            lambda: validate_choice("d", ["a", "b", "c"]),
            message="validate_choice rejects invalid choice"
        )

        # Test 12: validate_type - valid
        self.assert_no_exception(
            lambda: validate_type("test", str),
            message="validate_type accepts correct type"
        )

        # Test 13: validate_type - invalid
        self.assert_raises(
            InvalidInputError,
            lambda: validate_type(123, str),
            message="validate_type rejects wrong type"
        )

    # ========================================================================
    # EXCEPTION TESTS
    # ========================================================================

    def test_exceptions(self):
        """Test exception system."""
        print("\n" + "=" * 80)
        print("TEST SUITE 8: EXCEPTIONS")
        print("=" * 80)

        # Test 1: UIError with suggestion
        try:
            raise UIError("Test error", suggestion="Try this")
        except UIError as e:
            self.assert_true(
                e.message == "Test error" and e.suggestion == "Try this",
                "UIError stores message and suggestion"
            )

        # Test 2: InvalidInputError
        try:
            raise InvalidInputError("Invalid input")
        except InvalidInputError as e:
            self.assert_true(
                isinstance(e, UIError),
                "InvalidInputError is subclass of UIError"
            )

        # Test 3: EmptyDataError
        try:
            raise EmptyDataError("Empty data")
        except EmptyDataError as e:
            self.assert_true(
                isinstance(e, UIError),
                "EmptyDataError is subclass of UIError"
            )

    # ========================================================================
    # RUN ALL TESTS
    # ========================================================================

    def run_all(self):
        """Run all test suites."""
        print("\n" + "=" * 80)
        print("MAX-CODE CLI UI/UX - COMPREHENSIVE TEST SUITE")
        print("Week 3 Day 5 - Testing & Validation")
        print("=" * 80)

        start_time = time.time()

        # Run all test suites
        self.test_banner()
        self.test_formatter()
        self.test_progress()
        self.test_agent_display()
        self.test_tree_of_thoughts()
        self.test_streaming()
        self.test_validation()
        self.test_exceptions()

        elapsed = time.time() - start_time

        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")
        print(f"Total Tests: {self.tests_passed + self.tests_failed}")
        print(f"Success Rate: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%")
        print(f"Time Elapsed: {elapsed:.2f}s")
        print("=" * 80)

        if self.tests_failed == 0:
            print("\n✅ ALL TESTS PASSED! 🎯")
        else:
            print(f"\n⚠️  {self.tests_failed} TEST(S) FAILED")
            print("\nFailed tests:")
            for result_type, message in self.test_results:
                if result_type == 'FAIL':
                    print(f"  ✗ {message}")

        print()
        return self.tests_failed == 0


def main():
    """Run comprehensive UI test suite."""
    suite = UITestSuite()
    success = suite.run_all()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
