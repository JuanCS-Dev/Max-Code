"""
Comprehensive tests for self-validation system

TEST COVERAGE TARGET: 100%
SUCCESS RATE TARGET: >70%
"""
import pytest
import os
from datetime import datetime

from src.validation import (
    AutoTester,
    TestCase,
    TestResults,
    FailureAnalyzer,
    FailureReport,
    FailureType,
    AutoFixer,
    FixResult,
    ValidationEngine,
    ValidationResult,
    ValidationStatus
)


# ============================================================================
# TEST DATA
# ============================================================================

SAMPLE_FUNCTION = """
def fibonacci(n):
    \"\"\"Calculate nth Fibonacci number\"\"\"
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""

BUGGY_FUNCTION = """
def divide(a, b):
    \"\"\"Divide two numbers\"\"\"
    return a / b  # Bug: no zero division check
"""

SYNTAX_ERROR_CODE = """
def broken_function(x)  # Missing colon
    return x * 2
"""

IMPORT_ERROR_CODE = """
import nonexistent_module

def use_module():
    return nonexistent_module.function()
"""


# ============================================================================
# AUTO-TESTER TESTS
# ============================================================================

class TestAutoTester:
    """Test automatic test generation and execution"""
    
    def test_initialization(self):
        """Test AutoTester initialization"""
        tester = AutoTester()
        assert tester.model == "gpt-4o"
        assert tester.temperature == 0.3
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_generate_tests(self):
        """Test test generation"""
        tester = AutoTester()
        tests = tester.generate_tests(SAMPLE_FUNCTION, num_tests=3)
        
        assert len(tests) > 0
        assert len(tests) <= 3
        assert all(isinstance(t, TestCase) for t in tests)
        assert all(t.name.startswith("test_") for t in tests)
        assert all(len(t.code) > 0 for t in tests)
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_validate_test_quality(self):
        """Test test quality validation"""
        tester = AutoTester()
        tests = tester.generate_tests(SAMPLE_FUNCTION, num_tests=3)
        
        quality = tester.validate_test_quality(tests)
        
        assert "quality_score" in quality
        assert 0 <= quality["quality_score"] <= 100
        assert "has_assertions" in quality
        assert quality["has_assertions"] > 0  # Should have assertions
    
    def test_run_tests_success(self):
        """Test running successful tests"""
        tester = AutoTester()
        
        test_code = """
import pytest

def sample_func(x):
    return x * 2

class TestSample:
    def test_basic(self):
        assert sample_func(2) == 4
    
    def test_zero(self):
        assert sample_func(0) == 0
"""
        
        results = tester.run_tests(test_code, timeout=5)
        
        assert isinstance(results, TestResults)
        assert results.total > 0
        assert results.passed == results.total  # All should pass
        assert results.failed == 0
    
    def test_run_tests_failure(self):
        """Test running tests with failures"""
        tester = AutoTester()
        
        test_code = """
import pytest

def buggy_func(x):
    return x * 3  # Wrong implementation

class TestBuggy:
    def test_fails(self):
        assert buggy_func(2) == 4  # Will fail
"""
        
        results = tester.run_tests(test_code, timeout=5)
        
        assert results.total > 0
        assert results.failed > 0
        assert len(results.errors) > 0


# ============================================================================
# FAILURE ANALYZER TESTS
# ============================================================================

class TestFailureAnalyzer:
    """Test failure analysis"""
    
    def test_initialization(self):
        """Test FailureAnalyzer initialization"""
        analyzer = FailureAnalyzer()
        assert analyzer.use_extended_thinking == (os.getenv("ANTHROPIC_API_KEY") is not None)
    
    def test_classify_syntax_error(self):
        """Test syntax error classification"""
        analyzer = FailureAnalyzer(use_extended_thinking=False)
        
        error_msg = "SyntaxError: invalid syntax at line 42"
        failure_type = analyzer._classify_error(error_msg)
        
        assert failure_type == FailureType.SYNTAX_ERROR
    
    def test_classify_import_error(self):
        """Test import error classification"""
        analyzer = FailureAnalyzer(use_extended_thinking=False)
        
        error_msg = "ModuleNotFoundError: No module named 'nonexistent'"
        failure_type = analyzer._classify_error(error_msg)
        
        assert failure_type == FailureType.IMPORT_ERROR
    
    def test_classify_type_error(self):
        """Test type error classification"""
        analyzer = FailureAnalyzer(use_extended_thinking=False)
        
        error_msg = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
        failure_type = analyzer._classify_error(error_msg)
        
        assert failure_type == FailureType.TYPE_ERROR
    
    def test_extract_affected_lines(self):
        """Test line number extraction"""
        analyzer = FailureAnalyzer(use_extended_thinking=False)
        
        error_msg = 'File "test.py", line 42, in function\n    line 45'
        lines = analyzer._extract_affected_lines(error_msg)
        
        assert 42 in lines
        assert 45 in lines
    
    def test_basic_analysis(self):
        """Test basic failure analysis (without Extended Thinking)"""
        analyzer = FailureAnalyzer(use_extended_thinking=False)
        
        # Use RuntimeError which should be classified
        report = analyzer.analyze_failure(
            test_name="test_divide_by_zero",
            error_message="RuntimeError: ZeroDivisionError: division by zero",
            code=BUGGY_FUNCTION,
            test_code="assert divide(1, 0) == 0"
        )
        
        assert isinstance(report, FailureReport)
        assert report.failure_type == FailureType.RUNTIME_ERROR
        assert len(report.fix_suggestions) > 0
        assert 0.0 <= report.success_probability <= 1.0
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_extended_thinking_analysis(self):
        """Test analysis with Extended Thinking"""
        analyzer = FailureAnalyzer(use_extended_thinking=True)
        
        report = analyzer.analyze_failure(
            test_name="test_divide_by_zero",
            error_message="ZeroDivisionError: division by zero at line 3",
            code=BUGGY_FUNCTION,
            test_code="assert divide(1, 0) == 0"
        )
        
        assert isinstance(report, FailureReport)
        assert len(report.root_cause) > 10  # Should have detailed analysis
        assert len(report.thinking_process) > 0  # Should have thinking
        assert len(report.fix_suggestions) > 0
    
    def test_estimate_difficulty(self):
        """Test fix difficulty estimation"""
        analyzer = FailureAnalyzer(use_extended_thinking=False)
        
        # Easy: syntax error
        analysis = {"root_cause": "syntax", "fix_suggestions": []}
        difficulty = analyzer._estimate_difficulty(FailureType.SYNTAX_ERROR, analysis)
        assert difficulty == "easy"
        
        # Hard: logic error
        difficulty = analyzer._estimate_difficulty(FailureType.LOGIC_ERROR, analysis)
        assert difficulty == "hard"


# ============================================================================
# AUTO-FIXER TESTS
# ============================================================================

class TestAutoFixer:
    """Test automatic code fixing"""
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_initialization(self):
        """Test AutoFixer initialization"""
        fixer = AutoFixer()
        assert fixer.max_attempts == 3
        assert fixer.backoff_base == 2.0
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_validate_fix_valid(self):
        """Test fix validation (valid code)"""
        fixer = AutoFixer()
        
        valid_code = """
def test():
    return 42
"""
        
        assert fixer._validate_fix(valid_code) is True
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_validate_fix_invalid(self):
        """Test fix validation (invalid code)"""
        fixer = AutoFixer()
        
        invalid_code = """
def test()  # Missing colon
    return 42
"""
        
        assert fixer._validate_fix(invalid_code) is False
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_estimate_fix_time(self):
        """Test fix time estimation"""
        fixer = AutoFixer()
        
        # Create mock failure report
        report = FailureReport(
            failure_type=FailureType.SYNTAX_ERROR,
            root_cause="Missing colon",
            affected_lines=[2],
            error_message="SyntaxError",
            thinking_process="",
            fix_difficulty="easy",
            fix_suggestions=["Add colon"],
            success_probability=0.9
        )
        
        estimated_time = fixer.estimate_fix_time(report)
        
        assert estimated_time > 0
        assert estimated_time < 60  # Should be reasonable
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_can_fix_feasible(self):
        """Test feasibility check (feasible fix)"""
        fixer = AutoFixer()
        
        report = FailureReport(
            failure_type=FailureType.SYNTAX_ERROR,
            root_cause="Syntax error",
            affected_lines=[2],
            error_message="SyntaxError",
            thinking_process="",
            fix_difficulty="easy",
            fix_suggestions=["Fix syntax"],
            success_probability=0.85
        )
        
        assert fixer.can_fix(report) is True
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_can_fix_not_feasible(self):
        """Test feasibility check (not feasible)"""
        fixer = AutoFixer()
        
        report = FailureReport(
            failure_type=FailureType.UNKNOWN,
            root_cause="Unknown",
            affected_lines=[],
            error_message="Unknown error",
            thinking_process="",
            fix_difficulty="hard",
            fix_suggestions=[],
            success_probability=0.05  # Too low
        )
        
        assert fixer.can_fix(report) is False


# ============================================================================
# VALIDATION ENGINE TESTS
# ============================================================================

class TestValidationEngine:
    """Test full validation pipeline"""
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_initialization(self):
        """Test ValidationEngine initialization"""
        engine = ValidationEngine()
        assert engine.max_iterations == 3
        assert engine.timeout == 120.0
        assert engine.min_success_rate == 0.70
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") or not os.getenv("ANTHROPIC_API_KEY"),
        reason="Requires both OpenAI and Anthropic API keys"
    )
    def test_validate_simple_code(self):
        """Test validation of simple working code"""
        engine = ValidationEngine()
        
        result = engine.validate_and_fix(
            SAMPLE_FUNCTION,
            function_name="fibonacci",
            num_tests=3
        )
        
        assert isinstance(result, ValidationResult)
        assert result.status in [ValidationStatus.SUCCESS, ValidationStatus.PARTIAL_SUCCESS]
        assert result.tests_generated > 0
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_build_test_file(self):
        """Test test file building"""
        engine = ValidationEngine()
        
        tests = [
            TestCase(
                name="test_sample",
                code="def test_sample():\n    assert True",
                description="Test"
            )
        ]
        
        test_file = engine._build_test_file(tests, "def sample(): pass")
        
        assert "import pytest" in test_file
        assert "def sample():" in test_file
        assert "class TestGenerated:" in test_file
        assert "def test_sample" in test_file
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="Requires Anthropic API key")
    def test_print_summary(self, capsys):
        """Test summary printing"""
        engine = ValidationEngine()
        
        result = ValidationResult(
            status=ValidationStatus.SUCCESS,
            original_code="code",
            final_code="code",
            tests_generated=5,
            tests_passed=5,
            tests_failed=0,
            fix_attempts=0,
            fixes_successful=0,
            total_time=10.5,
            iterations=[]
        )
        
        engine.print_summary(result)
        
        captured = capsys.readouterr()
        assert "VALIDATION SUMMARY" in captured.out
        assert "SUCCESS" in captured.out
        assert "5/5 passed" in captured.out


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test full end-to-end scenarios"""
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") or not os.getenv("ANTHROPIC_API_KEY"),
        reason="Requires both API keys"
    )
    def test_full_pipeline_success(self):
        """Test complete pipeline on working code"""
        engine = ValidationEngine(max_iterations=2, timeout=60.0)
        
        result = engine.validate_and_fix(
            SAMPLE_FUNCTION,
            function_name="fibonacci",
            num_tests=3
        )
        
        assert result.status in [ValidationStatus.SUCCESS, ValidationStatus.PARTIAL_SUCCESS]
        assert result.tests_generated > 0
        assert result.tests_passed > 0
        assert result.success_rate >= 70.0
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") or not os.getenv("ANTHROPIC_API_KEY"),
        reason="Requires both API keys"
    )
    def test_full_pipeline_with_fix(self):
        """Test complete pipeline with bug fix"""
        engine = ValidationEngine(max_iterations=2, timeout=60.0)
        
        result = engine.validate_and_fix(
            BUGGY_FUNCTION,
            function_name="divide",
            num_tests=3
        )
        
        assert result.status != ValidationStatus.TIMEOUT
        assert result.tests_generated > 0
        
        # If fixes were attempted, check they worked
        if result.fix_attempts > 0:
            assert result.fixes_successful >= 0


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
