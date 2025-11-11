---
name: refactor
description: Refactor code for better quality and maintainability
args: [target]
---

Refactor the {{ target }} following Constitutional AI principles and Boris Technique.

**Refactoring Goals:**

1. **Code Quality (Boris Technique):**
   - Security: Identify and fix vulnerabilities
   - Beauty: Improve code readability and style
   - Performance: Optimize for speed and efficiency

2. **Constitutional AI Principles:**
   - P1: Zero Trust - Validate all assumptions
   - P2: Completude - Ensure 100% functional implementation
   - P3: Visão Sistêmica - Consider system-wide impact
   - P6: Antifragilidade - Make code resilient to failures

3. **Refactoring Checklist:**
   - Extract duplicated code into functions
   - Improve naming (variables, functions, classes)
   - Add type hints for Python code
   - Add comprehensive docstrings
   - Simplify complex conditionals
   - Reduce function complexity (max 15 lines)
   - Add error handling where missing
   - Write/update tests for refactored code

4. **Testing:**
   - Run existing tests to ensure no regressions
   - Add new tests for edge cases
   - Verify code coverage remains high (>90%)

**Target:** {{ target }}
**Quality Standards:** Constitutional AI v3.0 + Boris Technique

Please refactor the code while maintaining 100% functionality and backward compatibility.

Soli Deo Gloria 🙏
