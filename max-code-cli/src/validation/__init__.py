"""
Self-Validation Package

Automatic test generation, failure analysis, and auto-fixing.

RESEARCH-BASED IMPLEMENTATION:
- Claude Extended Thinking: Deep failure analysis
- GPT-4: Fast test generation
- Iterative validate-fix loop
- Success rate target: >70%

Components:
- AutoTester: Generate and run pytest tests
- FailureAnalyzer: Analyze failures with Extended Thinking
- AutoFixer: Attempt automatic fixes (max 3 attempts)
- ValidationEngine: Orchestrate full pipeline

Usage:
    from src.validation import ValidationEngine
    
    engine = ValidationEngine()
    result = engine.validate_and_fix(code, function_name="my_func")
    
    if result.status == ValidationStatus.SUCCESS:
        print(f"All {result.tests_passed} tests passed!")
"""
from .auto_tester import (
    AutoTester,
    TestCase,
    TestResults,
    generate_and_run_tests
)
from .failure_analyzer import (
    FailureAnalyzer,
    FailureReport,
    FailureType,
    analyze_test_failure
)
from .auto_fixer import (
    AutoFixer,
    FixAttempt,
    FixResult,
    auto_fix_code
)
from .validation_engine import (
    ValidationEngine,
    ValidationResult,
    ValidationStatus,
    validate_code
)

__all__ = [
    # Auto-Tester
    "AutoTester",
    "TestCase",
    "TestResults",
    "generate_and_run_tests",
    
    # Failure Analyzer
    "FailureAnalyzer",
    "FailureReport",
    "FailureType",
    "analyze_test_failure",
    
    # Auto-Fixer
    "AutoFixer",
    "FixAttempt",
    "FixResult",
    "auto_fix_code",
    
    # Validation Engine
    "ValidationEngine",
    "ValidationResult",
    "ValidationStatus",
    "validate_code",
]
