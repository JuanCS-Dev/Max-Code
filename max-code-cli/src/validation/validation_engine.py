"""
Validation Engine: Orchestrate test → analyze → fix → retest loop

RESEARCH SYNTHESIS:
- Iterative validation loop
- Max 3 iterations with timeout
- Success rate tracking
- Comprehensive reporting

STRATEGY:
✅ Orchestrate full validation pipeline
✅ Generate tests → Run → Analyze failures → Fix → Retest
✅ Timeout: 2min per cycle
✅ Success target: >70% on common errors
"""
import logging
import time
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .auto_tester import AutoTester, TestCase, TestResults
from .failure_analyzer import FailureAnalyzer, FailureReport
from .auto_fixer import AutoFixer, FixResult

logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Status of validation"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ValidationResult:
    """Complete validation result"""
    status: ValidationStatus
    original_code: str
    final_code: Optional[str]
    tests_generated: int
    tests_passed: int
    tests_failed: int
    fix_attempts: int
    fixes_successful: int
    total_time: float
    iterations: List[Dict]  # History of each iteration
    
    @property
    def success_rate(self) -> float:
        """Calculate overall success rate"""
        if self.tests_generated == 0:
            return 0.0
        return (self.tests_passed / self.tests_generated) * 100
    
    @property
    def fix_success_rate(self) -> float:
        """Calculate fix success rate"""
        if self.fix_attempts == 0:
            return 0.0
        return (self.fixes_successful / self.fix_attempts) * 100


class ValidationEngine:
    """
    Orchestrate complete validation pipeline
    
    Pipeline:
    1. Generate tests (AutoTester)
    2. Run tests
    3. If failures:
       a. Analyze (FailureAnalyzer)
       b. Fix (AutoFixer)
       c. Retest
    4. Repeat until success or timeout
    
    Performance targets:
    - Timeout: 2min per validation cycle
    - Success rate: >70% on common errors
    - Max iterations: 3
    """
    
    def __init__(
        self,
        max_iterations: int = 3,
        timeout: float = 120.0,  # 2 minutes
        min_success_rate: float = 0.70  # 70%
    ):
        """
        Initialize validation engine
        
        Args:
            max_iterations: Max validation iterations
            timeout: Total timeout in seconds
            min_success_rate: Minimum acceptable success rate (0-1)
        """
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.min_success_rate = min_success_rate
        
        # Initialize components
        self.tester = AutoTester()
        self.analyzer = FailureAnalyzer()
        self.fixer = AutoFixer()
        
        logger.info(f"ValidationEngine initialized:")
        logger.info(f"  Max iterations: {max_iterations}")
        logger.info(f"  Timeout: {timeout}s")
        logger.info(f"  Min success rate: {min_success_rate:.0%}")
    
    def validate_and_fix(
        self,
        code: str,
        function_name: Optional[str] = None,
        num_tests: int = 5
    ) -> ValidationResult:
        """
        Complete validation and fix pipeline
        
        Args:
            code: Source code to validate
            function_name: Specific function to test (optional)
            num_tests: Number of tests to generate
            
        Returns:
            Validation result with all details
        """
        logger.info("="*80)
        logger.info("STARTING VALIDATION PIPELINE")
        logger.info("="*80)
        
        start_time = time.time()
        iterations = []
        current_code = code
        
        # Step 1: Generate tests
        logger.info("\n[STEP 1] Generating tests...")
        try:
            tests = self.tester.generate_tests(
                code,
                function_name=function_name,
                num_tests=num_tests
            )
            
            # Validate test quality
            quality = self.tester.validate_test_quality(tests)
            logger.info(f"  Test quality score: {quality['quality_score']:.1f}/100")
            
            if quality['quality_score'] < 50:
                logger.warning("  ⚠️  Test quality is low, results may be unreliable")
        
        except Exception as e:
            logger.error(f"  Test generation failed: {e}")
            
            return ValidationResult(
                status=ValidationStatus.FAILED,
                original_code=code,
                final_code=None,
                tests_generated=0,
                tests_passed=0,
                tests_failed=0,
                fix_attempts=0,
                fixes_successful=0,
                total_time=time.time() - start_time,
                iterations=[]
            )
        
        # Validation loop
        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"[ITERATION {iteration}/{self.max_iterations}]")
            logger.info(f"{'='*80}")
            
            iteration_start = time.time()
            
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > self.timeout:
                logger.error(f"  ⏱️  Timeout exceeded ({elapsed:.1f}s > {self.timeout}s)")
                
                return ValidationResult(
                    status=ValidationStatus.TIMEOUT,
                    original_code=code,
                    final_code=current_code,
                    tests_generated=len(tests),
                    tests_passed=0,
                    tests_failed=len(tests),
                    fix_attempts=iteration - 1,
                    fixes_successful=0,
                    total_time=elapsed,
                    iterations=iterations
                )
            
            # Step 2: Run tests
            logger.info("\n[STEP 2] Running tests...")
            
            # Combine tests into full test file
            test_code = self._build_test_file(tests, current_code)
            
            test_results = self.tester.run_tests(test_code)
            
            logger.info(f"  Results: {test_results.passed}/{test_results.total} passed ({test_results.success_rate:.1f}%)")
            
            # Check if we're done
            if test_results.failed == 0:
                logger.info("\n  ✅ All tests passed!")
                
                total_time = time.time() - start_time
                
                iterations.append({
                    "iteration": iteration,
                    "test_results": test_results,
                    "fix_applied": False,
                    "duration": time.time() - iteration_start
                })
                
                return ValidationResult(
                    status=ValidationStatus.SUCCESS,
                    original_code=code,
                    final_code=current_code,
                    tests_generated=len(tests),
                    tests_passed=test_results.passed,
                    tests_failed=0,
                    fix_attempts=iteration - 1,
                    fixes_successful=iteration - 1 if iteration > 1 else 0,
                    total_time=total_time,
                    iterations=iterations
                )
            
            # Check if success rate is acceptable
            if test_results.success_rate >= self.min_success_rate * 100:
                logger.info(f"\n  ✅ Success rate ({test_results.success_rate:.1f}%) meets threshold ({self.min_success_rate:.0%})")
                
                total_time = time.time() - start_time
                
                iterations.append({
                    "iteration": iteration,
                    "test_results": test_results,
                    "fix_applied": False,
                    "duration": time.time() - iteration_start
                })
                
                return ValidationResult(
                    status=ValidationStatus.PARTIAL_SUCCESS,
                    original_code=code,
                    final_code=current_code,
                    tests_generated=len(tests),
                    tests_passed=test_results.passed,
                    tests_failed=test_results.failed,
                    fix_attempts=iteration - 1,
                    fixes_successful=iteration - 1 if iteration > 1 else 0,
                    total_time=total_time,
                    iterations=iterations
                )
            
            # Step 3: Analyze failures
            logger.info("\n[STEP 3] Analyzing failures...")
            
            failure_reports = []
            for error in test_results.errors[:3]:  # Analyze top 3 failures
                try:
                    report = self.analyzer.analyze_failure(
                        test_name=error.get("test", "unknown"),
                        error_message=error.get("message", ""),
                        code=current_code,
                        test_code=test_code
                    )
                    failure_reports.append(report)
                    
                    logger.info(f"  Failure: {report.failure_type.value}")
                    logger.info(f"  Root cause: {report.root_cause[:100]}...")
                    logger.info(f"  Fix difficulty: {report.fix_difficulty}, Success prob: {report.success_probability:.0%}")
                
                except Exception as e:
                    logger.error(f"  Analysis failed: {e}")
            
            if not failure_reports:
                logger.error("  No failures could be analyzed")
                break
            
            # Step 4: Attempt fix (use first failure report)
            logger.info("\n[STEP 4] Attempting fix...")
            
            primary_failure = failure_reports[0]
            
            # Check if fix is feasible
            if not self.fixer.can_fix(primary_failure):
                logger.warning("  Fix not feasible, stopping validation")
                break
            
            try:
                fix_result = self.fixer.attempt_fix(current_code, primary_failure)
                
                if fix_result.success:
                    logger.info(f"  ✅ Fix successful after {len(fix_result.attempts)} attempts")
                    current_code = fix_result.final_code
                    
                    iterations.append({
                        "iteration": iteration,
                        "test_results": test_results,
                        "fix_applied": True,
                        "fix_result": fix_result,
                        "duration": time.time() - iteration_start
                    })
                else:
                    logger.error(f"  ❌ Fix failed after {len(fix_result.attempts)} attempts")
                    
                    iterations.append({
                        "iteration": iteration,
                        "test_results": test_results,
                        "fix_applied": False,
                        "fix_result": fix_result,
                        "duration": time.time() - iteration_start
                    })
                    break
            
            except Exception as e:
                logger.error(f"  Fix attempt failed: {e}")
                break
        
        # Final result (all iterations exhausted)
        total_time = time.time() - start_time
        
        logger.info("\n" + "="*80)
        logger.info("VALIDATION COMPLETE")
        logger.info("="*80)
        
        # Determine final status
        final_test_results = iterations[-1]["test_results"] if iterations else None
        
        if final_test_results and final_test_results.failed == 0:
            status = ValidationStatus.SUCCESS
        elif final_test_results and final_test_results.success_rate >= self.min_success_rate * 100:
            status = ValidationStatus.PARTIAL_SUCCESS
        else:
            status = ValidationStatus.FAILED
        
        return ValidationResult(
            status=status,
            original_code=code,
            final_code=current_code,
            tests_generated=len(tests),
            tests_passed=final_test_results.passed if final_test_results else 0,
            tests_failed=final_test_results.failed if final_test_results else len(tests),
            fix_attempts=sum(1 for it in iterations if it.get("fix_applied")),
            fixes_successful=sum(1 for it in iterations if it.get("fix_applied") and it.get("fix_result", {}).get("success")),
            total_time=total_time,
            iterations=iterations
        )
    
    def _build_test_file(self, tests: List[TestCase], code: str) -> str:
        """Build complete test file with imports and code"""
        test_file = "import pytest\n\n"
        
        # Add code under test (in a way tests can import it)
        test_file += "# Code under test\n"
        test_file += code + "\n\n"
        
        # Add tests
        test_file += "# Generated tests\n"
        test_file += "class TestGenerated:\n"
        test_file += '    """Auto-generated test suite"""\n\n'
        
        for test in tests:
            # Indent test method
            indented = "\n".join("    " + line for line in test.code.split("\n"))
            test_file += indented + "\n\n"
        
        return test_file
    
    def print_summary(self, result: ValidationResult):
        """Print validation summary"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Status: {result.status.value.upper()}")
        print(f"Tests: {result.tests_passed}/{result.tests_generated} passed ({result.success_rate:.1f}%)")
        print(f"Fixes: {result.fixes_successful}/{result.fix_attempts} successful ({result.fix_success_rate:.1f}%)")
        print(f"Time: {result.total_time:.1f}s")
        print(f"Iterations: {len(result.iterations)}")
        print("="*80)
    
    def __repr__(self) -> str:
        return f"ValidationEngine(max_iter={self.max_iterations}, timeout={self.timeout}s)"


# Convenience function
def validate_code(code: str, function_name: Optional[str] = None) -> ValidationResult:
    """Quick helper to validate code"""
    engine = ValidationEngine()
    return engine.validate_and_fix(code, function_name=function_name)
