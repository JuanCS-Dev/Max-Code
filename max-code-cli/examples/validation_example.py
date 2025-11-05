"""
Example: Pydantic Input Validation for Agents

Demonstrates validation schemas for all 9 agent types.
Shows successful validation and error handling.

Run: python examples/validation_example.py
"""

import sys
sys.path.insert(0, '.')

from agents.validation_schemas import validate_task_parameters
from pydantic import ValidationError


# =============================================================================
# EXAMPLE 1: Valid Parameters
# =============================================================================

def example_valid_parameters():
    print("=" * 70)
    print("EXAMPLE 1: Valid Parameters")
    print("=" * 70)

    # Code Agent - Valid
    try:
        params = validate_task_parameters('code', {
            'description': 'Write a function to calculate fibonacci numbers'
        })
        print(f"✅ Code Agent: {params.description[:50]}...")
    except ValidationError as e:
        print(f"❌ Code Agent failed: {e}")

    # Review Agent - Valid
    try:
        params = validate_task_parameters('review', {
            'code': 'def add(a, b): return a + b'
        })
        print(f"✅ Review Agent: code length {len(params.code)} chars")
    except ValidationError as e:
        print(f"❌ Review Agent failed: {e}")

    # Test Agent - Valid
    try:
        params = validate_task_parameters('test', {
            'function_code': 'def multiply(a, b): return a * b'
        })
        print(f"✅ Test Agent: function code provided")
    except ValidationError as e:
        print(f"❌ Test Agent failed: {e}")

    print()


# =============================================================================
# EXAMPLE 2: Invalid Parameters (Missing Required Fields)
# =============================================================================

def example_missing_required():
    print("=" * 70)
    print("EXAMPLE 2: Missing Required Fields")
    print("=" * 70)

    # Code Agent - Missing description
    try:
        params = validate_task_parameters('code', {})
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: Field required: 'description'")

    # Review Agent - Missing code
    try:
        params = validate_task_parameters('review', {})
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: Field required: 'code'")

    # Test Agent - Missing function_code
    try:
        params = validate_task_parameters('test', {})
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: Field required: 'function_code'")

    print()


# =============================================================================
# EXAMPLE 3: Invalid Data Types
# =============================================================================

def example_invalid_types():
    print("=" * 70)
    print("EXAMPLE 3: Invalid Data Types")
    print("=" * 70)

    # Code Agent - description too short
    try:
        params = validate_task_parameters('code', {
            'description': 'short'  # min_length=10
        })
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: String should have at least 10 characters")

    # Test Agent - invalid coverage_threshold
    try:
        params = validate_task_parameters('test', {
            'function_code': 'def test(): pass',
            'coverage_threshold': 1.5  # max 1.0
        })
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: Input should be less than or equal to 1")

    print()


# =============================================================================
# EXAMPLE 4: Pattern Validation
# =============================================================================

def example_pattern_validation():
    print("=" * 70)
    print("EXAMPLE 4: Pattern Validation")
    print("=" * 70)

    # Code Agent - invalid language
    try:
        params = validate_task_parameters('code', {
            'description': 'Write hello world',
            'language': 'cobol'  # Not in allowed pattern
        })
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: String should match pattern (python|javascript|...)")

    # Review Agent - valid review_type
    try:
        params = validate_task_parameters('review', {
            'code': 'def test(): pass',
            'review_type': 'security'  # Valid pattern
        })
        print(f"✅ Review Agent: review_type='{params.review_type}'")
    except ValidationError as e:
        print(f"❌ Should have passed: {e}")

    print()


# =============================================================================
# EXAMPLE 5: Complex Validation (Docs Agent with CodeChange)
# =============================================================================

def example_complex_validation():
    print("=" * 70)
    print("EXAMPLE 5: Complex Validation (Nested Models)")
    print("=" * 70)

    # Docs Agent - Valid with changes
    try:
        params = validate_task_parameters('docs', {
            'changes': [
                {
                    'file_path': 'src/main.py',
                    'change_type': 'modified',
                    'description': 'Added new feature',
                    'lines_changed': 42
                },
                {
                    'file_path': 'tests/test_main.py',
                    'change_type': 'added',
                    'description': 'Added tests for new feature',
                    'lines_changed': 15
                }
            ]
        })
        print(f"✅ Docs Agent: {len(params.changes)} changes validated")
        for change in params.changes:
            print(f"   - {change.file_path}: {change.change_type}")
    except ValidationError as e:
        print(f"❌ Failed: {e}")

    # Docs Agent - Invalid change_type
    try:
        params = validate_task_parameters('docs', {
            'changes': [
                {
                    'file_path': 'src/main.py',
                    'change_type': 'updated',  # Invalid (should be 'modified')
                    'description': 'Changed something'
                }
            ]
        })
        print(f"❌ Should have failed")
    except ValidationError as e:
        print(f"✅ Caught error: change_type must be (added|modified|deleted|renamed)")

    print()


# =============================================================================
# EXAMPLE 6: All Agent Types
# =============================================================================

def example_all_agents():
    print("=" * 70)
    print("EXAMPLE 6: All 9 Agent Types")
    print("=" * 70)

    agents = {
        'code': {'description': 'Generate factorial function'},
        'review': {'code': 'def factorial(n): return 1 if n == 0 else n * factorial(n-1)'},
        'test': {'function_code': 'def factorial(n): return 1 if n == 0 else n * factorial(n-1)'},
        'fix': {'code': 'def broken(): return x', 'error': 'NameError: x is not defined'},
        'docs': {'code': 'def factorial(n): return 1'},
        'architect': {'requirements': ['scalable', 'maintainable', 'fast']},
        'plan': {'goal': 'Implement new authentication system'},
        'explore': {'query': 'Find all database models'},
        'sleep': {'include_maximus': True, 'create_snapshot': True}
    }

    for agent_type, params in agents.items():
        try:
            validated = validate_task_parameters(agent_type, params)
            print(f"✅ {agent_type.upper()}: validated successfully")
        except ValidationError as e:
            print(f"❌ {agent_type.upper()}: {e}")

    print()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "PYDANTIC VALIDATION EXAMPLES" + " " * 25 + "║")
    print("║" + " " * 22 + "FASE 3.2 Complete" + " " * 29 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    example_valid_parameters()
    example_missing_required()
    example_invalid_types()
    example_pattern_validation()
    example_complex_validation()
    example_all_agents()

    print("=" * 70)
    print("✅ All validation examples completed!")
    print("=" * 70)
    print()

    print("📊 SUMMARY:")
    print("   - 9 agent types with Pydantic validation")
    print("   - Type safety enforced at runtime")
    print("   - Clear error messages for invalid inputs")
    print("   - Pattern matching for enum-like fields")
    print("   - Nested model validation (CodeChange)")
    print()

    print("Biblical Foundation:")
    print('"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)')
    print()


if __name__ == "__main__":
    main()
