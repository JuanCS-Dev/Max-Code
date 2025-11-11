"""
Auto-Fixer: Attempt automatic code fixes

RESEARCH SYNTHESIS:
- Claude: Best for generating fixes (reasoning)
- Max 3 attempts with exponential backoff
- Validate fixes before applying
- Track fix history to avoid loops

STRATEGY:
✅ Use Claude for fix generation
✅ Apply fixes incrementally
✅ Validate each fix before accepting
✅ Exponential backoff between attempts
"""
import logging
import time
import os
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime

import anthropic

from .failure_analyzer import FailureReport, FailureType

logger = logging.getLogger(__name__)


@dataclass
class FixAttempt:
    """Single fix attempt record"""
    attempt_number: int
    fixed_code: str
    changes_made: str
    timestamp: datetime
    success: bool


@dataclass
class FixResult:
    """Result of fix attempts"""
    success: bool
    final_code: Optional[str]
    attempts: List[FixAttempt]
    total_time: float


class AutoFixer:
    """
    Automatic code fixer
    
    Features:
    - Generate fixes using Claude
    - Max 3 attempts with backoff
    - Validate fixes before applying
    - Track fix history
    
    Performance targets:
    - Fix generation: <5s per attempt
    - Total time: <30s (3 attempts max)
    - Success rate: >70% on common errors
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        backoff_base: float = 2.0,
        model: str = "claude-3-5-haiku-20241022"
    ):
        """
        Initialize auto-fixer
        
        Args:
            max_attempts: Maximum fix attempts (default: 3)
            backoff_base: Exponential backoff base (default: 2.0)
            model: Claude model for fix generation
        """
        self.max_attempts = max_attempts
        self.backoff_base = backoff_base
        self.model = model
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY required for AutoFixer")
        
        self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        
        logger.info(f"AutoFixer initialized (max_attempts={max_attempts})")
    
    def attempt_fix(
        self,
        code: str,
        failure_report: FailureReport,
        previous_attempts: Optional[List[FixAttempt]] = None
    ) -> FixResult:
        """
        Attempt to fix code based on failure report
        
        Strategy:
        1. Generate fix using Claude
        2. Validate fix (syntax check)
        3. If valid, accept and test
        4. If fails, retry with backoff (max 3 attempts)
        
        Args:
            code: Original code with error
            failure_report: Analysis of the failure
            previous_attempts: Previous fix attempts (for context)
            
        Returns:
            Fix result with success status and final code
        """
        logger.info(f"Attempting auto-fix (max {self.max_attempts} attempts)...")
        
        start_time = time.time()
        attempts = previous_attempts or []
        
        for attempt_num in range(1, self.max_attempts + 1):
            logger.info(f"  Attempt {attempt_num}/{self.max_attempts}...")
            
            # Generate fix
            try:
                fixed_code, changes = self._generate_fix(
                    code,
                    failure_report,
                    attempts
                )
            except Exception as e:
                logger.error(f"  Fix generation failed: {e}")
                
                # Record failed attempt
                attempts.append(FixAttempt(
                    attempt_number=attempt_num,
                    fixed_code=code,
                    changes_made=f"Generation failed: {str(e)}",
                    timestamp=datetime.now(),
                    success=False
                ))
                
                # Backoff before retry
                if attempt_num < self.max_attempts:
                    backoff_time = self.backoff_base ** attempt_num
                    logger.info(f"  Backing off for {backoff_time:.1f}s...")
                    time.sleep(backoff_time)
                
                continue
            
            # Validate fix (basic syntax check)
            if self._validate_fix(fixed_code):
                logger.info(f"  ✅ Fix validated successfully")
                
                attempts.append(FixAttempt(
                    attempt_number=attempt_num,
                    fixed_code=fixed_code,
                    changes_made=changes,
                    timestamp=datetime.now(),
                    success=True
                ))
                
                total_time = time.time() - start_time
                
                return FixResult(
                    success=True,
                    final_code=fixed_code,
                    attempts=attempts,
                    total_time=total_time
                )
            else:
                logger.warning(f"  ❌ Fix validation failed")
                
                attempts.append(FixAttempt(
                    attempt_number=attempt_num,
                    fixed_code=fixed_code,
                    changes_made=changes,
                    timestamp=datetime.now(),
                    success=False
                ))
                
                # Backoff before retry
                if attempt_num < self.max_attempts:
                    backoff_time = self.backoff_base ** attempt_num
                    logger.info(f"  Backing off for {backoff_time:.1f}s...")
                    time.sleep(backoff_time)
        
        # All attempts failed
        total_time = time.time() - start_time
        logger.error(f"  All {self.max_attempts} fix attempts failed")
        
        return FixResult(
            success=False,
            final_code=None,
            attempts=attempts,
            total_time=total_time
        )
    
    def _generate_fix(
        self,
        code: str,
        failure_report: FailureReport,
        previous_attempts: List[FixAttempt]
    ) -> tuple[str, str]:
        """
        Generate fix using Claude
        
        Returns:
            (fixed_code, changes_description)
        """
        # Build context from previous attempts
        attempts_context = ""
        if previous_attempts:
            attempts_context = "\n\nPREVIOUS FIX ATTEMPTS (failed):\n"
            for attempt in previous_attempts:
                attempts_context += f"\nAttempt {attempt.attempt_number}:\n"
                attempts_context += f"Changes: {attempt.changes_made}\n"
                attempts_context += "This approach did not work.\n"
        
        prompt = f"""Fix the following code based on the failure analysis.

FAILURE ANALYSIS:
- Type: {failure_report.failure_type.value}
- Root Cause: {failure_report.root_cause}
- Error: {failure_report.error_message}
- Affected Lines: {failure_report.affected_lines}
- Fix Difficulty: {failure_report.fix_difficulty}

FIX SUGGESTIONS:
{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(failure_report.fix_suggestions))}

ORIGINAL CODE:
```python
{code}
```
{attempts_context}

INSTRUCTIONS:
1. Fix the code based on the root cause and suggestions
2. Make minimal changes (only what's necessary)
3. Preserve existing functionality
4. Ensure the fix addresses the root cause
5. Add comments explaining critical changes

Provide:
1. The complete fixed code (in ```python code block)
2. A brief description of changes made

Format:
CHANGES:
<description of what was changed and why>

FIXED CODE:
```python
<complete fixed code>
```
"""
        
        response = self.anthropic_client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        # Extract changes description
        changes = "No description provided"
        if "CHANGES:" in response_text:
            changes_part = response_text.split("CHANGES:")[1].split("FIXED CODE:")[0].strip()
            changes = changes_part
        
        # Extract fixed code
        if "```python" in response_text:
            fixed_code = response_text.split("```python")[1].split("```")[0].strip()
        elif "```" in response_text:
            fixed_code = response_text.split("```")[1].split("```")[0].strip()
        else:
            # No code block, try to extract code
            fixed_code = response_text
        
        return fixed_code, changes
    
    def _validate_fix(self, code: str) -> bool:
        """
        Validate fixed code
        
        Basic validation:
        - Syntax check (can parse as Python)
        - No obvious issues
        
        Returns:
            True if valid, False otherwise
        """
        import ast
        
        try:
            # Try to parse as Python
            ast.parse(code)
            return True
        except SyntaxError as e:
            logger.warning(f"  Syntax validation failed: {e}")
            return False
        except Exception as e:
            logger.warning(f"  Validation failed: {e}")
            return False
    
    def estimate_fix_time(self, failure_report: FailureReport) -> float:
        """
        Estimate time required for fix
        
        Based on difficulty and success probability
        
        Returns:
            Estimated time in seconds
        """
        base_times = {
            "easy": 5.0,
            "medium": 10.0,
            "hard": 20.0
        }
        
        base_time = base_times.get(failure_report.fix_difficulty, 10.0)
        
        # Adjust for expected attempts
        # If success prob is low, expect more attempts
        expected_attempts = 1 / max(failure_report.success_probability, 0.1)
        expected_attempts = min(expected_attempts, self.max_attempts)
        
        # Add backoff time
        total_backoff = sum(self.backoff_base ** i for i in range(1, int(expected_attempts)))
        
        return base_time * expected_attempts + total_backoff
    
    def can_fix(self, failure_report: FailureReport, max_time: float = 60.0) -> bool:
        """
        Check if fix is feasible
        
        Based on:
        - Success probability
        - Estimated time
        - Failure type
        
        Args:
            failure_report: Failure analysis
            max_time: Maximum time budget in seconds
            
        Returns:
            True if fix is feasible
        """
        # Check success probability
        if failure_report.success_probability < 0.10:
            logger.info("Fix not feasible: success probability too low")
            return False
        
        # Check estimated time
        estimated_time = self.estimate_fix_time(failure_report)
        if estimated_time > max_time:
            logger.info(f"Fix not feasible: estimated time ({estimated_time:.1f}s) exceeds budget ({max_time:.1f}s)")
            return False
        
        # Check failure type (some types are too hard)
        if failure_report.failure_type in [FailureType.UNKNOWN, FailureType.TIMEOUT]:
            logger.info("Fix not feasible: failure type too complex")
            return False
        
        return True
    
    def __repr__(self) -> str:
        return f"AutoFixer(max_attempts={self.max_attempts})"


# Convenience function
def auto_fix_code(code: str, failure_report: FailureReport) -> FixResult:
    """Quick helper to attempt auto-fix"""
    fixer = AutoFixer()
    return fixer.attempt_fix(code, failure_report)
