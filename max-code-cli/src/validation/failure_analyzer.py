"""
Failure Analyzer: Deep analysis of test failures using Claude Extended Thinking

RESEARCH SYNTHESIS:
- Claude Extended Thinking: Best for complex analysis
- Pattern matching: Common error types
- Root cause analysis: Multi-step reasoning

STRATEGY:
✅ Use Claude Extended Thinking for deep failure analysis
✅ Pattern match common error types first (fast)
✅ Generate actionable fix suggestions
✅ Estimate fix difficulty and success probability
"""
import logging
import os
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

import anthropic

logger = logging.getLogger(__name__)


class FailureType(Enum):
    """Types of test failures"""
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    RUNTIME_ERROR = "runtime_error"
    ASSERTION_ERROR = "assertion_error"
    TYPE_ERROR = "type_error"
    ATTRIBUTE_ERROR = "attribute_error"
    LOGIC_ERROR = "logic_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass
class FailureReport:
    """Detailed failure analysis report"""
    failure_type: FailureType
    root_cause: str
    affected_lines: List[int]
    error_message: str
    thinking_process: str  # From Claude Extended Thinking
    fix_difficulty: str  # "easy", "medium", "hard"
    fix_suggestions: List[str]
    success_probability: float  # 0.0-1.0


class FailureAnalyzer:
    """
    Analyze test failures with deep reasoning
    
    Features:
    - Pattern matching for common errors
    - Claude Extended Thinking for complex analysis
    - Root cause identification
    - Fix suggestion generation
    
    Performance:
    - Simple errors: <1s (pattern matching)
    - Complex errors: <10s (Extended Thinking)
    """
    
    # Common error patterns
    ERROR_PATTERNS = {
        FailureType.SYNTAX_ERROR: [
            r"SyntaxError",
            r"invalid syntax",
            r"unexpected EOF",
            r"IndentationError"
        ],
        FailureType.IMPORT_ERROR: [
            r"ImportError",
            r"ModuleNotFoundError",
            r"cannot import name",
            r"No module named"
        ],
        FailureType.TYPE_ERROR: [
            r"TypeError",
            r"unsupported operand type",
            r"takes \d+ positional",
            r"missing \d+ required"
        ],
        FailureType.ATTRIBUTE_ERROR: [
            r"AttributeError",
            r"has no attribute",
            r"'NoneType' object"
        ],
        FailureType.ASSERTION_ERROR: [
            r"AssertionError",
            r"assert .* failed"
        ],
        FailureType.RUNTIME_ERROR: [
            r"RuntimeError",
            r"ZeroDivisionError",
            r"ValueError",
            r"KeyError",
            r"IndexError"
        ],
    }
    
    def __init__(
        self,
        use_extended_thinking: bool = True,
        thinking_budget: int = 2048
    ):
        """
        Initialize failure analyzer
        
        Args:
            use_extended_thinking: Enable Claude Extended Thinking
            thinking_budget: Token budget for reasoning (min 1024)
        """
        self.use_extended_thinking = use_extended_thinking
        self.thinking_budget = thinking_budget
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not set, extended thinking disabled")
            self.use_extended_thinking = False
        
        self.anthropic_client = anthropic.Anthropic(api_key=api_key) if api_key else None
        
        logger.info(f"FailureAnalyzer initialized (extended_thinking={use_extended_thinking})")
    
    def analyze_failure(
        self,
        test_name: str,
        error_message: str,
        code: str,
        test_code: str
    ) -> FailureReport:
        """
        Analyze test failure with deep reasoning
        
        Strategy:
        1. Pattern match for quick classification
        2. Use Claude Extended Thinking for root cause
        3. Generate actionable fix suggestions
        
        Args:
            test_name: Name of failed test
            error_message: Error message from test
            code: Source code being tested
            test_code: Test code that failed
            
        Returns:
            Detailed failure report
        """
        logger.info(f"Analyzing failure: {test_name}")
        
        # Step 1: Quick classification via pattern matching
        failure_type = self._classify_error(error_message)
        logger.info(f"  Classified as: {failure_type.value}")
        
        # Step 2: Extract error details
        affected_lines = self._extract_affected_lines(error_message)
        
        # Step 3: Deep analysis
        if self.use_extended_thinking and self.anthropic_client:
            # Use Claude Extended Thinking for complex analysis
            analysis = self._analyze_with_extended_thinking(
                test_name,
                error_message,
                code,
                test_code,
                failure_type
            )
        else:
            # Fallback: Basic analysis
            analysis = self._basic_analysis(
                error_message,
                failure_type
            )
        
        # Step 4: Estimate fix difficulty
        fix_difficulty = self._estimate_difficulty(failure_type, analysis)
        
        # Step 5: Calculate success probability
        success_prob = self._estimate_success_probability(failure_type, fix_difficulty)
        
        report = FailureReport(
            failure_type=failure_type,
            root_cause=analysis["root_cause"],
            affected_lines=affected_lines,
            error_message=error_message,
            thinking_process=analysis.get("thinking", ""),
            fix_difficulty=fix_difficulty,
            fix_suggestions=analysis["fix_suggestions"],
            success_probability=success_prob
        )
        
        logger.info(f"  Root cause: {report.root_cause[:100]}...")
        logger.info(f"  Difficulty: {fix_difficulty}, Success prob: {success_prob:.0%}")
        
        return report
    
    def _classify_error(self, error_message: str) -> FailureType:
        """Classify error type via pattern matching"""
        for failure_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    return failure_type
        
        return FailureType.UNKNOWN
    
    def _extract_affected_lines(self, error_message: str) -> List[int]:
        """Extract line numbers from error message"""
        lines = []
        
        # Pattern: "line 42" or "File \"...\", line 42"
        matches = re.findall(r'line (\d+)', error_message)
        lines.extend(int(m) for m in matches)
        
        return sorted(set(lines))
    
    def _analyze_with_extended_thinking(
        self,
        test_name: str,
        error_message: str,
        code: str,
        test_code: str,
        failure_type: FailureType
    ) -> Dict:
        """
        Analyze failure using Claude Extended Thinking
        
        From research:
        - Enable thinking with budget_tokens parameter
        - Thinking block comes first in response
        - Transparent multi-step reasoning
        """
        logger.info("  Using Claude Extended Thinking for deep analysis...")
        
        prompt = f"""Analyze this test failure and provide a detailed root cause analysis and fix suggestions.

TEST NAME: {test_name}
FAILURE TYPE: {failure_type.value}

ERROR MESSAGE:
{error_message}

SOURCE CODE:
```python
{code}
```

TEST CODE:
```python
{test_code}
```

Provide:
1. Root cause of the failure (be specific)
2. Why the error occurred (explain the logic)
3. 3-5 concrete fix suggestions (ranked by likelihood of success)

Think step-by-step about the problem before suggesting fixes.
"""
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=4096,
                thinking={
                    "type": "enabled",
                    "budget_tokens": self.thinking_budget
                },
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract thinking and text blocks
            thinking = ""
            analysis_text = ""
            
            for block in response.content:
                if block.type == "thinking":
                    thinking = block.thinking
                elif block.type == "text":
                    analysis_text = block.text
            
            # Parse analysis
            return self._parse_analysis_response(analysis_text, thinking)
        
        except Exception as e:
            logger.error(f"Extended thinking analysis failed: {e}")
            # Fallback to basic
            return self._basic_analysis(error_message, failure_type)
    
    def _parse_analysis_response(self, analysis_text: str, thinking: str) -> Dict:
        """Parse Claude's analysis response"""
        # Extract root cause (look for "Root cause:" or similar)
        root_cause = "Unknown"
        if "root cause" in analysis_text.lower():
            lines = analysis_text.split("\n")
            for i, line in enumerate(lines):
                if "root cause" in line.lower():
                    # Get next non-empty line
                    for j in range(i+1, len(lines)):
                        if lines[j].strip():
                            root_cause = lines[j].strip()
                            break
                    break
        
        # Extract fix suggestions (numbered list or bullet points)
        fix_suggestions = []
        lines = analysis_text.split("\n")
        for line in lines:
            # Match patterns like "1. ", "- ", "* "
            if re.match(r'^\s*[\d\-\*\+]\s+', line):
                suggestion = re.sub(r'^\s*[\d\-\*\+]\s+', '', line).strip()
                if suggestion and len(suggestion) > 10:  # Filter noise
                    fix_suggestions.append(suggestion)
        
        # Limit to top 5
        fix_suggestions = fix_suggestions[:5]
        
        return {
            "root_cause": root_cause,
            "thinking": thinking,
            "fix_suggestions": fix_suggestions if fix_suggestions else ["Review the error message and code carefully"]
        }
    
    def _basic_analysis(self, error_message: str, failure_type: FailureType) -> Dict:
        """Basic analysis without Extended Thinking"""
        # Generate basic root cause based on error type
        root_causes = {
            FailureType.SYNTAX_ERROR: "Code has syntax errors that prevent execution",
            FailureType.IMPORT_ERROR: "Missing or incorrectly named import",
            FailureType.TYPE_ERROR: "Type mismatch in operation or function call",
            FailureType.ATTRIBUTE_ERROR: "Accessing non-existent attribute or method",
            FailureType.ASSERTION_ERROR: "Test assertion failed - expected vs actual mismatch",
            FailureType.RUNTIME_ERROR: "Runtime error during execution",
            FailureType.UNKNOWN: "Unexpected error occurred"
        }
        
        root_cause = root_causes.get(failure_type, "Unknown error")
        
        # Basic fix suggestions
        fix_suggestions = {
            FailureType.SYNTAX_ERROR: [
                "Check for missing colons, parentheses, or brackets",
                "Verify indentation is consistent",
                "Look for typos in keywords"
            ],
            FailureType.IMPORT_ERROR: [
                "Verify module is installed (pip install)",
                "Check import statement syntax",
                "Ensure module name is correct"
            ],
            FailureType.TYPE_ERROR: [
                "Check function argument types",
                "Add type conversion if needed",
                "Verify operation is valid for given types"
            ],
            FailureType.ATTRIBUTE_ERROR: [
                "Check if object is None before accessing",
                "Verify attribute name is correct",
                "Ensure object has been properly initialized"
            ],
            FailureType.ASSERTION_ERROR: [
                "Review expected vs actual values",
                "Check test logic and assumptions",
                "Verify function behavior matches expectations"
            ],
        }
        
        suggestions = fix_suggestions.get(failure_type, ["Review error and code carefully"])
        
        return {
            "root_cause": root_cause,
            "thinking": "",
            "fix_suggestions": suggestions
        }
    
    def _estimate_difficulty(self, failure_type: FailureType, analysis: Dict) -> str:
        """
        Estimate fix difficulty
        
        Returns: "easy", "medium", or "hard"
        """
        # Easy fixes
        if failure_type in [FailureType.SYNTAX_ERROR, FailureType.IMPORT_ERROR]:
            return "easy"
        
        # Medium fixes
        if failure_type in [FailureType.TYPE_ERROR, FailureType.ATTRIBUTE_ERROR]:
            return "medium"
        
        # Hard fixes
        if failure_type in [FailureType.LOGIC_ERROR, FailureType.UNKNOWN]:
            return "hard"
        
        # Default
        return "medium"
    
    def _estimate_success_probability(self, failure_type: FailureType, difficulty: str) -> float:
        """
        Estimate probability of successful auto-fix
        
        Based on difficulty and error type
        """
        base_probs = {
            "easy": 0.85,
            "medium": 0.60,
            "hard": 0.30
        }
        
        base = base_probs.get(difficulty, 0.50)
        
        # Adjust based on failure type
        if failure_type == FailureType.SYNTAX_ERROR:
            return min(base + 0.10, 0.95)  # Syntax easier
        elif failure_type == FailureType.LOGIC_ERROR:
            return max(base - 0.20, 0.10)  # Logic harder
        
        return base
    
    def suggest_fixes(self, report: FailureReport) -> List[str]:
        """
        Get ranked fix suggestions from failure report
        
        Returns:
            List of fix suggestions (ranked by priority)
        """
        return report.fix_suggestions
    
    def __repr__(self) -> str:
        return f"FailureAnalyzer(extended_thinking={self.use_extended_thinking})"


# Convenience function
def analyze_test_failure(test_name: str, error_message: str, code: str, test_code: str) -> FailureReport:
    """Quick helper to analyze a failure"""
    analyzer = FailureAnalyzer()
    return analyzer.analyze_failure(test_name, error_message, code, test_code)
