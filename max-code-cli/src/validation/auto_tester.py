"""
Auto-Tester: Generate and run tests dynamically

RESEARCH SYNTHESIS (2025-11-08):
- GPT-4: Fast test generation ($2.50/1M tokens)
- Claude: Deep test reasoning (when needed)
- pytest: Industry standard for Python testing

STRATEGY:
✅ Use GPT-4 for fast test generation (cheaper)
✅ Generate pytest-compatible tests
✅ Run tests in isolated subprocess
✅ Collect detailed failure information
"""
import logging
import subprocess
import tempfile
import ast
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """Single test case"""
    name: str
    code: str
    description: str


@dataclass
class TestResults:
    """Results from test execution"""
    total: int
    passed: int
    failed: int
    errors: List[Dict]
    duration: float
    output: str
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100


class AutoTester:
    """
    Automatic test generator and runner
    
    Features:
    - Generate pytest-compatible tests using GPT-4
    - Run tests in isolated environment
    - Collect detailed failure information
    - Support for unit, integration tests
    
    Performance targets:
    - Test generation: <5s
    - Test execution: <10s per test file
    """
    
    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.3  # Lower for deterministic tests
    ):
        """
        Initialize auto-tester
        
        Args:
            model: OpenAI model for test generation
            temperature: Generation temperature (lower = more deterministic)
        """
        self.model = model
        self.temperature = temperature
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Fallback to Anthropic if OpenAI not available
            api_key = os.getenv("ANTHROPIC_API_KEY")
            logger.warning("OPENAI_API_KEY not set, using Anthropic fallback")
        
        self.openai_client = OpenAI(api_key=api_key) if api_key else None
        
        logger.info(f"AutoTester initialized (model={model})")
    
    def generate_tests(
        self,
        code: str,
        function_name: Optional[str] = None,
        num_tests: int = 5
    ) -> List[TestCase]:
        """
        Generate test cases for code using GPT-4
        
        Strategy (from research):
        - Use GPT-4 for fast generation
        - Generate pytest-compatible tests
        - Cover edge cases, normal cases, error cases
        
        Args:
            code: Source code to test
            function_name: Specific function to test (optional)
            num_tests: Number of test cases to generate
            
        Returns:
            List of test cases
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        logger.info(f"Generating {num_tests} tests for code...")
        
        # Build prompt
        prompt = self._build_test_generation_prompt(code, function_name, num_tests)
        
        # Generate tests
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": "You are an expert at writing pytest tests. Generate comprehensive, pytest-compatible test cases."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            test_code = response.choices[0].message.content
            
            # Parse generated tests
            tests = self._parse_generated_tests(test_code)
            
            logger.info(f"✅ Generated {len(tests)} tests")
            return tests
        
        except Exception as e:
            logger.error(f"Test generation failed: {e}")
            raise
    
    def _build_test_generation_prompt(
        self,
        code: str,
        function_name: Optional[str],
        num_tests: int
    ) -> str:
        """Build prompt for test generation"""
        prompt = f"""Generate {num_tests} comprehensive pytest test cases for the following code.

CODE:
```python
{code}
```

Requirements:
1. Use pytest framework
2. Test edge cases, normal cases, and error cases
3. Use descriptive test names (test_<functionality>_<scenario>)
4. Include docstrings explaining what each test validates
5. Use appropriate assertions (assert, pytest.raises, etc)
6. Format: One test class with multiple test methods

"""
        
        if function_name:
            prompt += f"\nFocus specifically on testing the '{function_name}' function.\n"
        
        prompt += """
Output format:
```python
import pytest

class Test<FunctionName>:
    \"\"\"Test suite for <function>\"\"\"
    
    def test_case_1(self):
        \"\"\"Test description\"\"\"
        # Test code
        assert ...
    
    def test_case_2(self):
        \"\"\"Test description\"\"\"
        # Test code
        assert ...
```

Generate ONLY the test code, no explanations.
"""
        return prompt
    
    def _parse_generated_tests(self, test_code: str) -> List[TestCase]:
        """Parse generated test code into TestCase objects"""
        # Extract code from markdown if present
        if "```python" in test_code:
            test_code = test_code.split("```python")[1].split("```")[0].strip()
        elif "```" in test_code:
            test_code = test_code.split("```")[1].split("```")[0].strip()
        
        # Parse AST
        try:
            tree = ast.parse(test_code)
        except SyntaxError as e:
            logger.error(f"Generated test code has syntax error: {e}")
            raise
        
        # Extract test methods
        tests = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                        # Extract docstring
                        docstring = ast.get_docstring(item) or "No description"
                        
                        # Extract test method code
                        test_method_code = ast.unparse(item)
                        
                        tests.append(TestCase(
                            name=item.name,
                            code=test_method_code,
                            description=docstring
                        ))
        
        return tests
    
    def run_tests(
        self,
        test_code: str,
        timeout: int = 10
    ) -> TestResults:
        """
        Run pytest tests in isolated environment
        
        Args:
            test_code: Test code to execute
            timeout: Timeout in seconds
            
        Returns:
            Test results
        """
        logger.info("Running tests...")
        
        start_time = datetime.now()
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='_test.py',
            delete=False,
            dir='/tmp'
        ) as f:
            f.write(test_code)
            test_file = f.name
        
        try:
            # Run pytest
            result = subprocess.run(
                ['pytest', test_file, '-v', '--tb=short', '--no-header'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            # Parse results
            test_results = self._parse_pytest_output(
                result.stdout,
                result.stderr,
                result.returncode,
                duration
            )
            
            logger.info(f"✅ Tests completed: {test_results.passed}/{test_results.total} passed")
            
            return test_results
        
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Tests timed out after {timeout}s")
            
            return TestResults(
                total=0,
                passed=0,
                failed=0,
                errors=[{"type": "timeout", "message": f"Tests exceeded {timeout}s timeout"}],
                duration=duration,
                output="TIMEOUT"
            )
        
        finally:
            # Cleanup
            Path(test_file).unlink(missing_ok=True)
    
    def _parse_pytest_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        duration: float
    ) -> TestResults:
        """Parse pytest output into TestResults"""
        lines = stdout.split('\n')
        
        # Count results
        total = 0
        passed = 0
        failed = 0
        errors = []
        
        # Parse summary line (e.g., "3 passed, 2 failed in 0.5s")
        for line in lines:
            if " passed" in line or " failed" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed":
                        passed = int(parts[i-1])
                        total += passed
                    elif part == "failed":
                        failed = int(parts[i-1])
                        total += failed
        
        # Extract failure details
        current_test = None
        collecting_error = False
        error_lines = []
        
        for line in lines:
            if line.startswith("FAILED"):
                # New failure
                if current_test and error_lines:
                    errors.append({
                        "test": current_test,
                        "message": "\n".join(error_lines)
                    })
                current_test = line.split("::")[1].split(" ")[0] if "::" in line else "unknown"
                error_lines = []
                collecting_error = True
            elif collecting_error:
                if line.strip():
                    error_lines.append(line)
        
        # Add last error
        if current_test and error_lines:
            errors.append({
                "test": current_test,
                "message": "\n".join(error_lines)
            })
        
        # Add stderr if present
        if stderr:
            errors.append({
                "test": "stderr",
                "message": stderr
            })
        
        return TestResults(
            total=total,
            passed=passed,
            failed=failed,
            errors=errors,
            duration=duration,
            output=stdout
        )
    
    def validate_test_quality(self, tests: List[TestCase]) -> Dict[str, any]:
        """
        Validate quality of generated tests
        
        Checks:
        - Syntax validity
        - Proper assertions
        - Edge case coverage
        
        Returns:
            Quality metrics
        """
        metrics = {
            "total_tests": len(tests),
            "has_assertions": 0,
            "has_edge_cases": 0,
            "has_error_cases": 0,
            "avg_test_length": 0
        }
        
        total_length = 0
        
        for test in tests:
            # Check for assertions
            if "assert" in test.code:
                metrics["has_assertions"] += 1
            
            # Check for edge cases (heuristic)
            if any(keyword in test.name.lower() for keyword in ["edge", "boundary", "limit", "empty", "zero"]):
                metrics["has_edge_cases"] += 1
            
            # Check for error cases
            if "pytest.raises" in test.code or "exception" in test.description.lower():
                metrics["has_error_cases"] += 1
            
            total_length += len(test.code)
        
        if len(tests) > 0:
            metrics["avg_test_length"] = total_length // len(tests)
        
        # Quality score (0-100)
        score = 0
        if metrics["total_tests"] > 0:
            score += (metrics["has_assertions"] / metrics["total_tests"]) * 40  # 40% weight
            score += (metrics["has_edge_cases"] / max(metrics["total_tests"] * 0.3, 1)) * 30  # 30% weight
            score += (metrics["has_error_cases"] / max(metrics["total_tests"] * 0.2, 1)) * 30  # 30% weight
            score = min(score, 100)
        
        metrics["quality_score"] = score
        
        logger.info(f"Test quality score: {score:.1f}/100")
        
        return metrics
    
    def __repr__(self) -> str:
        return f"AutoTester(model={self.model})"


# Convenience function
def generate_and_run_tests(code: str, num_tests: int = 5) -> Tuple[List[TestCase], TestResults]:
    """Quick helper to generate and run tests"""
    tester = AutoTester()
    tests = tester.generate_tests(code, num_tests=num_tests)
    
    # Combine tests into full test file
    test_code = "import pytest\n\n"
    test_code += "\n\n".join(test.code for test in tests)
    
    results = tester.run_tests(test_code)
    
    return tests, results
