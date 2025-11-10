"""
Truth Engine - Objective Code Verification

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
Test everything. Hold onto what is good.

Architecture:
1. Requirement Parser: Extract requirements from prompt
2. Code Analyzer: Analyze actual implementation via AST
3. Test Runner: Execute tests and collect results
4. Truth Synthesizer: Combine evidence into verdict

Philosophy:
No LLM can fool tree-sitter AST parsing.
Either the function exists and has logic, or it doesn't.
"""

import re
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from .models import (
    RequirementSpec,
    ImplementationEvidence,
    ImplementationType,
    TestStatus,
    TruthMetrics,
    VerificationResult,
)

# Lazy imports
try:
    import tree_sitter_python as tspython
    from tree_sitter import Language, Parser
    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False


class RequirementParser:
    """
    Extract requirements from natural language prompt

    Uses heuristics + patterns to identify what was requested.

    Example:
        "Create calculator with add, subtract, multiply functions"
        → Requirements: add(), subtract(), multiply()
    """

    def extract_requirements(self, prompt: str) -> List[RequirementSpec]:
        """
        Extract requirements from prompt

        Strategies:
        1. Function names in backticks: `add()`, `subtract()`
        2. Verb patterns: "implement X", "create Y"
        3. List patterns: "functions: A, B, C"
        4. Numbered lists: "1. Do X\n2. Do Y"
        """
        requirements = []
        req_id = 0

        # Strategy 1: Backtick function names
        backtick_funcs = re.findall(r'`(\w+)\(\)`', prompt)
        for func_name in backtick_funcs:
            req_id += 1
            requirements.append(RequirementSpec(
                requirement_id=f"req_{req_id}",
                description=f"Implement function {func_name}()",
                function_name=func_name,
                priority=1
            ))

        # Strategy 2: Verb patterns
        verb_patterns = [
            r'implement (\w+)',
            r'create (\w+)',
            r'add (\w+)',
            r'build (\w+)',
        ]

        for pattern in verb_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            for match in matches:
                # Avoid duplicates
                if any(r.function_name == match for r in requirements):
                    continue

                req_id += 1
                requirements.append(RequirementSpec(
                    requirement_id=f"req_{req_id}",
                    description=f"Implement {match}",
                    function_name=match,
                    priority=2
                ))

        # Strategy 3: Numbered lists
        numbered_items = re.findall(r'^\d+\.\s+(.+)$', prompt, re.MULTILINE)
        for item in numbered_items:
            # Extract function name if present
            func_match = re.search(r'(\w+)\(', item)
            func_name = func_match.group(1) if func_match else None

            # Avoid duplicates
            if func_name and any(r.function_name == func_name for r in requirements):
                continue

            req_id += 1
            requirements.append(RequirementSpec(
                requirement_id=f"req_{req_id}",
                description=item.strip(),
                function_name=func_name,
                priority=1
            ))

        # Fallback: if no requirements found, treat whole prompt as one requirement
        if not requirements:
            requirements.append(RequirementSpec(
                requirement_id="req_1",
                description=prompt[:200],
                priority=1
            ))

        return requirements


class CodeAnalyzer:
    """
    Analyze code implementation using AST

    Classifies functions/classes as:
    - REAL: Has actual logic
    - MOCK: Just stub (pass, NotImplementedError, TODO)
    - MISSING: Doesn't exist
    """

    def __init__(self):
        self.parser = None
        if HAS_TREE_SITTER:
            PY_LANGUAGE = Language(tspython.language())
            self.parser = Parser(PY_LANGUAGE)

    def analyze_implementation(
        self,
        requirements: List[RequirementSpec],
        project_root: Path
    ) -> List[ImplementationEvidence]:
        """
        Analyze implementation for each requirement

        Returns evidence for each requirement
        """
        evidence_list = []

        for req in requirements:
            evidence = self._analyze_requirement(req, project_root)
            evidence_list.append(evidence)

        return evidence_list

    def _analyze_requirement(
        self,
        req: RequirementSpec,
        project_root: Path
    ) -> ImplementationEvidence:
        """Analyze single requirement"""

        # If requirement has file path, check that file
        if req.file_path:
            file_path = project_root / req.file_path
            if file_path.exists():
                return self._analyze_file(req, file_path)

        # Otherwise, search for function in all Python files
        if req.function_name:
            result = self._search_function(req.function_name, project_root)
            if result:
                return result

        # Not found
        return ImplementationEvidence(
            requirement=req,
            implementation_type=ImplementationType.MISSING,
            reason="Function not found in codebase"
        )

    def _analyze_file(
        self,
        req: RequirementSpec,
        file_path: Path
    ) -> ImplementationEvidence:
        """Analyze specific file"""

        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except Exception as e:
            return ImplementationEvidence(
                requirement=req,
                implementation_type=ImplementationType.MISSING,
                reason=f"Cannot read file: {e}"
            )

        # Parse with tree-sitter
        if self.parser and req.function_name:
            return self._parse_with_treesitter(req, file_path, code)
        else:
            return self._parse_simple(req, file_path, code)

    def _parse_with_treesitter(
        self,
        req: RequirementSpec,
        file_path: Path,
        code: str
    ) -> ImplementationEvidence:
        """Parse using tree-sitter"""

        tree = self.parser.parse(bytes(code, 'utf8'))
        root = tree.root_node

        # Find function
        for node in root.children:
            if node.type == 'function_definition':
                name_node = node.child_by_field_name('name')
                if not name_node:
                    continue

                func_name = code[name_node.start_byte:name_node.end_byte]

                if func_name == req.function_name:
                    # Found it! Check if mock or real
                    func_code = code[node.start_byte:node.end_byte]

                    impl_type, reason = self._classify_implementation(func_code)

                    return ImplementationEvidence(
                        requirement=req,
                        implementation_type=impl_type,
                        file_path=str(file_path),
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        code_snippet=func_code,
                        reason=reason
                    )

        # Not found in this file
        return ImplementationEvidence(
            requirement=req,
            implementation_type=ImplementationType.MISSING,
            reason=f"Function {req.function_name} not found in {file_path}"
        )

    def _parse_simple(
        self,
        req: RequirementSpec,
        file_path: Path,
        code: str
    ) -> ImplementationEvidence:
        """Simple regex-based parsing (fallback)"""

        if not req.function_name:
            return ImplementationEvidence(
                requirement=req,
                implementation_type=ImplementationType.MISSING,
                reason="No function name specified"
            )

        # Find function definition
        pattern = rf'def {re.escape(req.function_name)}\([^)]*\):'
        match = re.search(pattern, code)

        if not match:
            return ImplementationEvidence(
                requirement=req,
                implementation_type=ImplementationType.MISSING,
                reason=f"Function {req.function_name} not found"
            )

        # Extract function body (simple heuristic)
        start = match.start()
        # Find next 'def' or end of file
        next_def = re.search(r'\ndef ', code[match.end():])
        end = match.end() + next_def.start() if next_def else len(code)

        func_code = code[start:end]

        impl_type, reason = self._classify_implementation(func_code)

        return ImplementationEvidence(
            requirement=req,
            implementation_type=impl_type,
            file_path=str(file_path),
            code_snippet=func_code,
            reason=reason
        )

    def _classify_implementation(self, func_code: str) -> tuple[ImplementationType, str]:
        """
        Classify implementation as REAL, MOCK, or INCOMPLETE

        Heuristics for MOCK:
        - Only contains 'pass'
        - Only raises NotImplementedError
        - Has TODO/FIXME/MOCK comment
        - Just returns None without logic
        """
        # Normalize
        code_lower = func_code.lower()
        code_stripped = func_code.strip()

        # Check for mock indicators
        mock_indicators = [
            ('pass' in code_lower and code_lower.count('\n') <= 3, "Only contains 'pass'"),
            ('notimplementederror' in code_lower, "Raises NotImplementedError"),
            ('todo' in code_lower, "Contains TODO comment"),
            ('fixme' in code_lower, "Contains FIXME comment"),
            ('mock' in code_lower, "Contains MOCK comment"),
            ('stub' in code_lower, "Contains STUB comment"),
            ('placeholder' in code_lower, "Contains PLACEHOLDER comment"),
        ]

        for condition, reason in mock_indicators:
            if condition:
                return ImplementationType.MOCK, reason

        # Check for minimal implementation (likely incomplete)
        lines = [l.strip() for l in func_code.split('\n') if l.strip() and not l.strip().startswith('#')]

        # Remove def line
        if lines and lines[0].startswith('def '):
            lines = lines[1:]

        # If only 1-2 lines after def, likely incomplete
        if len(lines) <= 2:
            # Check if it's just 'return None' or 'return'
            if any('return none' in l.lower() or l == 'return' for l in lines):
                return ImplementationType.INCOMPLETE, "Only returns None without logic"

        # Has substantial logic
        if len(lines) >= 3:
            return ImplementationType.REAL, "Has implementation logic"

        return ImplementationType.INCOMPLETE, "Minimal implementation"

    def _search_function(
        self,
        func_name: str,
        project_root: Path
    ) -> Optional[ImplementationEvidence]:
        """Search for function across all Python files"""

        # Use grep for fast search
        try:
            result = subprocess.run(
                ['grep', '-r', '-n', f'def {func_name}(', str(project_root), '--include=*.py'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout:
                # Found! Parse first match
                first_line = result.stdout.split('\n')[0]
                file_path_str, line_num, _ = first_line.split(':', 2)

                file_path = Path(file_path_str)

                # Analyze this file
                req = RequirementSpec(
                    requirement_id="temp",
                    description=f"Function {func_name}",
                    function_name=func_name,
                    file_path=str(file_path)
                )

                return self._analyze_file(req, file_path)

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError):
            pass

        return None


class TestRunner:
    """
    Run tests and collect results

    Executes pytest with coverage and parses results
    """

    def run_tests(
        self,
        project_root: Path,
        test_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run pytest with coverage

        Returns:
            {
                'tests_total': int,
                'tests_passing': int,
                'tests_failing': int,
                'coverage': float,  # 0.0 to 1.0
                'duration_ms': float,
            }
        """
        start_time = time.time()

        # Build pytest command
        cmd = ['pytest', '--tb=short', '--quiet']

        if test_files:
            cmd.extend(test_files)

        # Add coverage
        cmd.extend(['--cov', '--cov-report=json'])

        try:
            result = subprocess.run(
                cmd,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            # Parse output
            stdout = result.stdout
            tests_passing = stdout.count(' passed')
            tests_failing = stdout.count(' failed')
            tests_total = tests_passing + tests_failing

            # Parse coverage
            coverage = 0.0
            coverage_file = project_root / 'coverage.json'
            if coverage_file.exists():
                try:
                    with open(coverage_file, 'r') as f:
                        coverage_data = json.load(f)
                    coverage = coverage_data.get('totals', {}).get('percent_covered', 0.0) / 100
                except Exception:
                    pass

            duration_ms = (time.time() - start_time) * 1000

            return {
                'tests_total': tests_total,
                'tests_passing': tests_passing,
                'tests_failing': tests_failing,
                'coverage': coverage,
                'duration_ms': duration_ms,
                'success': result.returncode == 0,
            }

        except subprocess.TimeoutExpired:
            return {
                'tests_total': 0,
                'tests_passing': 0,
                'tests_failing': 0,
                'coverage': 0.0,
                'duration_ms': 300000,
                'success': False,
                'error': 'Test execution timed out (5 minutes)'
            }


class TruthEngine:
    """
    Truth Engine - Complete Verification Pipeline

    Pipeline:
    1. Parse requirements from prompt
    2. Analyze code implementation
    3. Run tests
    4. Synthesize truth metrics

    Output: Objective VerificationResult
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = Path(project_root or Path.cwd())
        self.req_parser = RequirementParser()
        self.code_analyzer = CodeAnalyzer()
        self.test_runner = TestRunner()

    def verify(
        self,
        prompt: str,
        run_tests: bool = True
    ) -> VerificationResult:
        """
        Complete truth verification

        Args:
            prompt: Original prompt with requirements
            run_tests: Whether to execute tests

        Returns:
            VerificationResult with objective metrics
        """
        start_time = time.time()

        # 1. Extract requirements
        requirements = self.req_parser.extract_requirements(prompt)

        # 2. Analyze implementation
        evidence = self.code_analyzer.analyze_implementation(
            requirements,
            self.project_root
        )

        # 3. Run tests (if requested)
        test_results = {}
        if run_tests:
            test_results = self.test_runner.run_tests(self.project_root)

        # 4. Calculate metrics
        metrics = self._calculate_metrics(evidence, test_results)

        duration_ms = (time.time() - start_time) * 1000

        return VerificationResult(
            prompt=prompt,
            requirements=requirements,
            evidence=evidence,
            metrics=metrics,
            verification_duration_ms=duration_ms
        )

    def _calculate_metrics(
        self,
        evidence: List[ImplementationEvidence],
        test_results: Dict[str, Any]
    ) -> TruthMetrics:
        """Calculate truth metrics from evidence"""

        total_reqs = len(evidence)
        implemented = sum(1 for e in evidence if e.implementation_type == ImplementationType.REAL)
        mocked = sum(1 for e in evidence if e.implementation_type == ImplementationType.MOCK)
        missing = sum(1 for e in evidence if e.implementation_type == ImplementationType.MISSING)
        incomplete = sum(1 for e in evidence if e.implementation_type == ImplementationType.INCOMPLETE)

        return TruthMetrics(
            total_reqs=total_reqs,
            implemented=implemented,
            mocked=mocked,
            missing=missing,
            incomplete=incomplete,
            tests_total=test_results.get('tests_total', 0),
            tests_passing=test_results.get('tests_passing', 0),
            tests_failing=test_results.get('tests_failing', 0),
            coverage=test_results.get('coverage', 0.0),
        )
