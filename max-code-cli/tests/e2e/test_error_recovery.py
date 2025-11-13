"""
FASE 5 - Test Suite 2: Error Recovery E2E Tests
================================================

Objetivo: Validar recuperação automática de erros (syntax errors, test failures, type errors)

Padrão Anthropic: "iterate until target achieved" + auto-correction
Constitutional AI v3.0: P6 (Antifragilidade), P4 (Obrigação da Verdade)

Target: 5+ error recovery scenarios, 70%+ success rate
"""

import ast
import re
from typing import Dict, Any

import pytest

from core.llm.unified_client import UnifiedLLMClient


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_code(text: str) -> str:
    """Extract Python code from LLM response"""
    # Try markdown code blocks
    if "```python" in text:
        start = text.index("```python") + 9
        end = text.index("```", start)
        return text[start:end].strip()

    # Try generic code blocks
    if "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        return text[start:end].strip()

    # Fallback: return full text
    return text.strip()


def has_syntax_error(code: str) -> bool:
    """Check if code has syntax errors"""
    try:
        ast.parse(code)
        return False
    except SyntaxError:
        return True


def get_syntax_error_message(code: str) -> str:
    """Get syntax error message"""
    try:
        ast.parse(code)
        return ""
    except SyntaxError as e:
        return str(e)


# ============================================================================
# TEST CLASS: SYNTAX ERROR RECOVERY
# ============================================================================

class TestSyntaxErrorRecovery:
    """Test LLM's ability to fix syntax errors when prompted"""

    @classmethod
    def setup_class(cls):
        """Initialize LLM client"""
        cls.client = UnifiedLLMClient()

    @pytest.mark.vcr()
    def test_fix_missing_colon(self):
        """
        E2E: LLM fixes missing colon in function definition

        Scenario:
        1. Generate broken code (or provide it)
        2. Ask LLM to fix syntax error
        3. Verify fixed code is valid
        """
        broken_code = """
def fibonacci(n)  # Missing colon
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

        prompt = f"""Fix the syntax error in this code:

```python
{broken_code}
```

Return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Fixed code is syntactically valid
            assert not has_syntax_error(fixed_code), "Code still has syntax errors"

            # Validation 2: Function still exists
            assert "def fibonacci" in fixed_code, "Function was removed"

            # Validation 3: Colon was added
            assert "def fibonacci(n):" in fixed_code, "Colon not added correctly"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise

    @pytest.mark.vcr()
    def test_fix_indentation_error(self):
        """
        E2E: LLM fixes indentation error

        Scenario:
        1. Provide code with indentation error
        2. Ask LLM to fix it
        3. Verify fixed code has correct indentation
        """
        broken_code = """
def calculate_sum(numbers):
result = 0  # Wrong indentation
    for num in numbers:
        result += num
    return result
"""

        prompt = f"""Fix the indentation error in this code:

```python
{broken_code}
```

Return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Fixed code is syntactically valid
            assert not has_syntax_error(fixed_code), "Code still has syntax errors"

            # Validation 2: Function exists and works
            namespace = {}
            exec(fixed_code, namespace)
            calc_sum = namespace['calculate_sum']
            assert calc_sum([1, 2, 3]) == 6, "Function doesn't work correctly"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise

    @pytest.mark.vcr()
    def test_fix_unclosed_bracket(self):
        """
        E2E: LLM fixes unclosed bracket

        Scenario:
        1. Provide code with unclosed bracket
        2. Ask LLM to fix it
        3. Verify brackets are balanced
        """
        broken_code = """
def process_data(items):
    result = [
        item * 2
        for item in items
        if item > 0
    # Missing closing bracket
    return result
"""

        prompt = f"""Fix the syntax error (unclosed bracket) in this code:

```python
{broken_code}
```

Return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Fixed code is syntactically valid
            assert not has_syntax_error(fixed_code), "Code still has syntax errors"

            # Validation 2: Function works
            namespace = {}
            exec(fixed_code, namespace)
            process = namespace['process_data']
            assert process([1, -2, 3]) == [2, 6], "Function doesn't work correctly"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise


# ============================================================================
# TEST CLASS: LOGIC ERROR RECOVERY
# ============================================================================

class TestLogicErrorRecovery:
    """Test LLM's ability to fix logic errors when given failing test results"""

    @classmethod
    def setup_class(cls):
        """Initialize LLM client"""
        cls.client = UnifiedLLMClient()

    @pytest.mark.vcr()
    def test_fix_off_by_one_error(self):
        """
        E2E: LLM fixes off-by-one error when given test failure

        Scenario:
        1. Provide code with off-by-one error
        2. Show failing test
        3. Ask LLM to fix it
        4. Verify fixed code passes test
        """
        buggy_code = """
def get_first_n_items(items, n):
    return items[0:n-1]  # Off by one! Should be items[0:n]
"""

        failing_test = """
# Test that fails:
items = [1, 2, 3, 4, 5]
result = get_first_n_items(items, 3)
assert result == [1, 2, 3]  # FAILS: returns [1, 2]
"""

        prompt = f"""This code has a bug. The test is failing:

Code:
```python
{buggy_code}
```

Failing test:
```python
{failing_test}
```

Fix the bug and return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Syntax valid
            assert not has_syntax_error(fixed_code), "Fixed code has syntax errors"

            # Validation 2: Test passes
            namespace = {}
            exec(fixed_code, namespace)
            get_first_n = namespace['get_first_n_items']
            assert get_first_n([1, 2, 3, 4, 5], 3) == [1, 2, 3], "Bug not fixed"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise

    @pytest.mark.vcr()
    def test_fix_wrong_operator(self):
        """
        E2E: LLM fixes wrong operator when given test failure

        Scenario:
        1. Provide code using wrong operator
        2. Show failing test
        3. Ask LLM to fix it
        4. Verify fixed code passes test
        """
        buggy_code = """
def is_even(n):
    return n / 2 == 0  # Wrong! Should be n % 2 == 0
"""

        failing_test = """
# Test that fails:
assert is_even(4) == True   # FAILS: 4 / 2 == 2.0, not 0
assert is_even(3) == False
"""

        prompt = f"""This code has a bug. The test is failing:

Code:
```python
{buggy_code}
```

Failing test:
```python
{failing_test}
```

Fix the bug and return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Syntax valid
            assert not has_syntax_error(fixed_code), "Fixed code has syntax errors"

            # Validation 2: Tests pass
            namespace = {}
            exec(fixed_code, namespace)
            is_even = namespace['is_even']
            assert is_even(4) == True, "Bug not fixed (even case)"
            assert is_even(3) == False, "Bug not fixed (odd case)"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise

    @pytest.mark.vcr()
    def test_fix_wrong_return_value(self):
        """
        E2E: LLM fixes wrong return value

        Scenario:
        1. Function returns wrong thing
        2. Show failing test
        3. Ask LLM to fix it
        4. Verify fixed code passes test
        """
        buggy_code = """
def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return numbers  # Wrong! Should return max_num
"""

        failing_test = """
# Test that fails:
result = find_max([1, 5, 3, 2])
assert result == 5  # FAILS: returns [1, 5, 3, 2]
"""

        prompt = f"""This code has a bug. The test is failing:

Code:
```python
{buggy_code}
```

Failing test:
```python
{failing_test}
```

Fix the bug and return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Syntax valid
            assert not has_syntax_error(fixed_code), "Fixed code has syntax errors"

            # Validation 2: Test passes
            namespace = {}
            exec(fixed_code, namespace)
            find_max = namespace['find_max']
            assert find_max([1, 5, 3, 2]) == 5, "Bug not fixed"
            assert find_max([10, 2, 8]) == 10, "Bug not fixed (edge case)"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise


# ============================================================================
# TEST CLASS: TYPE ERROR RECOVERY
# ============================================================================

class TestTypeErrorRecovery:
    """Test LLM's ability to fix type-related errors"""

    @classmethod
    def setup_class(cls):
        """Initialize LLM client"""
        cls.client = UnifiedLLMClient()

    @pytest.mark.vcr()
    def test_fix_string_int_concatenation(self):
        """
        E2E: LLM fixes string + int type error

        Scenario:
        1. Provide code that tries to concatenate string and int
        2. Show error
        3. Ask LLM to fix it
        4. Verify fixed code works
        """
        buggy_code = """
def create_message(name, age):
    return "Hello, " + name + "! You are " + age + " years old."
    # TypeError: can only concatenate str (not "int") to str
"""

        error_message = """
# Error when running:
create_message("Alice", 30)
# TypeError: can only concatenate str (not "int") to str
"""

        prompt = f"""Fix the type error in this code:

Code:
```python
{buggy_code}
```

Error:
```
{error_message}
```

Return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Syntax valid
            assert not has_syntax_error(fixed_code), "Fixed code has syntax errors"

            # Validation 2: Function works
            namespace = {}
            exec(fixed_code, namespace)
            create_msg = namespace['create_message']
            result = create_msg("Alice", 30)
            assert "Alice" in result, "Name not in message"
            assert "30" in result, "Age not in message"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise

    @pytest.mark.vcr()
    def test_fix_list_index_type(self):
        """
        E2E: LLM fixes list index type error (float instead of int)

        Scenario:
        1. Provide code using float as list index
        2. Show error
        3. Ask LLM to fix it
        4. Verify fixed code works
        """
        buggy_code = """
def get_middle_element(items):
    middle_index = len(items) / 2  # Returns float!
    return items[middle_index]  # TypeError: list indices must be integers
"""

        error_message = """
# Error when running:
get_middle_element([1, 2, 3, 4, 5])
# TypeError: list indices must be integers or slices, not float
"""

        prompt = f"""Fix the type error in this code:

Code:
```python
{buggy_code}
```

Error:
```
{error_message}
```

Return only the corrected code."""

        try:
            response = self.client.chat(prompt)
            fixed_code = extract_code(response)

            # Validation 1: Syntax valid
            assert not has_syntax_error(fixed_code), "Fixed code has syntax errors"

            # Validation 2: Function works
            namespace = {}
            exec(fixed_code, namespace)
            get_middle = namespace['get_middle_element']
            result = get_middle([1, 2, 3, 4, 5])
            assert result in [2, 3], "Wrong middle element"

        except RuntimeError as e:
            if "All LLM providers failed" in str(e):
                pytest.skip("LLM providers unavailable")
            raise
