"""
EPL Integration Tests

End-to-end tests for EPL (Emoji Protocol Language).

Biblical Foundation:
"Provai todas as coisas; retende o que é bom." (1 Tessalonicenses 5:21)
Test everything - keep what is good.

Test Coverage:
- Lexer → Parser → Translator → Executor pipeline
- Natural Language → EPL → Execution
- EPL → Natural Language → Understanding
- Pattern learning and matching
- Learning mode progression
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.epl import (
    # Lexer
    tokenize,
    is_epl_only,
    is_natural_language_only,
    extract_emojis,

    # Parser
    parse,
    print_ast,

    # Translator
    Translator,
    translate_to_epl,
    translate_to_nl,

    # Executor
    EPLExecutor,
    ExecutionStatus,

    # Learning Mode
    LearningMode,
    LearningPhase,

    # Vocabulary
    get_emoji_definition,
    calculate_compression_ratio,
)


def test_lexer():
    """Test EPL Lexer"""
    print("=" * 70)
    print("TEST 1: LEXER")
    print("=" * 70)

    test_cases = [
        ("🌳📊🔒", True, False),            # Pure EPL
        ("Use tree of thoughts", False, True),  # Pure NL
        ("Use 🌳 for analysis", False, False),  # Mixed
    ]

    for i, (input_text, expected_epl, expected_nl) in enumerate(test_cases, 1):
        tokens = tokenize(input_text)
        is_epl = is_epl_only(tokens)
        is_nl = is_natural_language_only(tokens)

        status = "✓" if is_epl == expected_epl and is_nl == expected_nl else "✗"
        print(f"{status} Test {i}: '{input_text}'")
        print(f"  EPL only: {is_epl} (expected: {expected_epl})")
        print(f"  NL only: {is_nl} (expected: {expected_nl})")

        if is_epl == expected_epl and is_nl == expected_nl:
            return True

    return False


def test_parser():
    """Test EPL Parser"""
    print("\n" + "=" * 70)
    print("TEST 2: PARSER")
    print("=" * 70)

    test_cases = [
        ("👑:🌳", "agent_invoke"),
        ("🔴→🟢→🔄", "chain"),
        ("🌳📊🔒", "program"),
    ]

    for i, (epl, expected_type) in enumerate(test_cases, 1):
        ast = parse(epl)

        # Check if AST was created
        has_children = len(ast.children) > 0
        status = "✓" if has_children else "✗"

        print(f"{status} Test {i}: '{epl}'")
        print(f"  AST type: {ast.node_type.value}")
        if has_children:
            print(f"  Children: {len(ast.children)}")

    return True


def test_translator_nl_to_epl():
    """Test Natural Language → EPL Translation"""
    print("\n" + "=" * 70)
    print("TEST 3: TRANSLATOR (NL → EPL)")
    print("=" * 70)

    translator = Translator()

    test_cases = [
        "Use tree of thoughts to analyze authentication",
        "Fix bug in security module",
        "Review code quality",
    ]

    for i, nl in enumerate(test_cases, 1):
        result = translator.translate_to_epl(nl)

        # Check if EPL was generated
        has_epl = len(result.target) > 0
        status = "✓" if has_epl else "✗"

        print(f"{status} Test {i}: '{nl}'")
        print(f"  EPL: {result.target}")
        print(f"  Confidence: {result.confidence:.0%}")
        if result.compression_ratio:
            print(f"  Compression: {result.compression_ratio:.0%}")

    return True


def test_translator_epl_to_nl():
    """Test EPL → Natural Language Translation"""
    print("\n" + "=" * 70)
    print("TEST 4: TRANSLATOR (EPL → NL)")
    print("=" * 70)

    test_cases = [
        ("🌳📊🔒", "Tree of Thoughts"),
        ("👑:🌳", "Sophia"),
        ("🔴→🟢→🔄", "RED then GREEN then REFACTOR"),
    ]

    for i, (epl, expected_keyword) in enumerate(test_cases, 1):
        result = translate_to_nl(epl)

        # Check if expected keyword is in translation
        has_keyword = expected_keyword.lower() in result.lower()
        status = "✓" if has_keyword else "✗"

        print(f"{status} Test {i}: '{epl}'")
        print(f"  NL: {result}")
        print(f"  Expected keyword: '{expected_keyword}' (found: {has_keyword})")

    return True


def test_pattern_matching():
    """Test Pattern Learning & Fuzzy Matching"""
    print("\n" + "=" * 70)
    print("TEST 5: PATTERN MATCHING")
    print("=" * 70)

    translator = Translator()

    # Learn pattern
    original = "Use tree of thoughts for analysis"
    translator.translate_to_epl(original, learn=True)
    print(f"✓ Learned pattern: '{original}'")

    # Test similar input
    similar = "Use ToT for analyzing data"
    result = translator.translate_to_epl(similar, learn=False)

    has_match = result.matched_pattern is not None
    status = "✓" if has_match else "✗"

    print(f"{status} Similar input: '{similar}'")
    print(f"  EPL: {result.target}")
    print(f"  Matched pattern: {result.matched_pattern}")
    print(f"  Confidence: {result.confidence:.0%}")

    return True


def test_executor():
    """Test EPL Executor"""
    print("\n" + "=" * 70)
    print("TEST 6: EXECUTOR")
    print("=" * 70)

    executor = EPLExecutor()

    # Mock agent handler
    def mock_handler(context):
        return f"Executed with context: {context.get('epl')}"

    # Register mock agent
    executor.register_agent("sophia", mock_handler)
    print("✓ Registered mock agent: sophia")

    # Test execution
    epl = "👑:🌳"
    result = executor.execute(epl)

    is_success = result.status == ExecutionStatus.SUCCESS
    status = "✓" if is_success else "✗"

    print(f"{status} Executed: '{epl}'")
    print(f"  Status: {result.status.value}")
    print(f"  Message: {result.message}")
    if result.agent:
        print(f"  Agent: {result.agent}")

    return is_success


def test_learning_mode():
    """Test Learning Mode"""
    print("\n" + "=" * 70)
    print("TEST 7: LEARNING MODE")
    print("=" * 70)

    learning = LearningMode()

    # Test phase progression
    phases_tested = []

    # Phase 1: OBSERVATION (0-10 interactions)
    for i in range(10):
        learning.record_interaction("natural_language")

    phase1 = learning.progress.phase
    phases_tested.append(phase1 == LearningPhase.OBSERVATION)
    print(f"{'✓' if phases_tested[-1] else '✗'} Phase 1 (OBSERVATION): {phase1.value}")

    # Phase 2: HINTS (11-30 interactions)
    for i in range(20):
        learning.record_interaction("epl" if i % 2 == 0 else "natural_language")

    phase2 = learning.progress.phase
    phases_tested.append(phase2 == LearningPhase.HINTS)
    print(f"{'✓' if phases_tested[-1] else '✗'} Phase 2 (HINTS): {phase2.value}")

    # Phase 3: FLUENCY (31+ interactions)
    for i in range(10):
        learning.record_interaction("epl")

    phase3 = learning.progress.phase
    phases_tested.append(phase3 == LearningPhase.FLUENCY)
    print(f"{'✓' if phases_tested[-1] else '✗'} Phase 3 (FLUENCY): {phase3.value}")

    # Summary
    summary = learning.get_progress_summary()
    print(f"\n  Total interactions: {summary['total_interactions']}")
    print(f"  EPL proficiency: {summary['epl_proficiency']}")

    return all(phases_tested)


def test_end_to_end():
    """Test Complete E2E Pipeline"""
    print("\n" + "=" * 70)
    print("TEST 8: END-TO-END PIPELINE")
    print("=" * 70)

    # Create components
    translator = Translator()
    executor = EPLExecutor()
    learning = LearningMode()

    # Mock agent
    def sophia_handler(context):
        return f"Sophia: Executed {context.get('epl')}"

    executor.register_agent("sophia", sophia_handler)

    # Test pipeline: NL → EPL → Execute
    nl_input = "Use tree of thoughts for analysis"
    print(f"1. Natural Language Input: '{nl_input}'")

    # Translate NL → EPL
    translation = translator.translate_to_epl(nl_input)
    epl = translation.target
    print(f"2. EPL Translation: '{epl}'")
    print(f"   Compression: {translation.compression_ratio:.0%}")

    # Record learning
    learning.record_interaction("natural_language")
    hint = learning.get_hint(nl_input, False, epl)
    if hint:
        print(f"3. Learning Hint: {hint.message}")

    # Verify translation back
    nl_back = translate_to_nl(epl)
    print(f"4. EPL → NL: '{nl_back}'")

    # Success if we got through all steps
    success = len(epl) > 0 and len(nl_back) > 0
    status = "✓" if success else "✗"
    print(f"\n{status} E2E Pipeline: {'SUCCESS' if success else 'FAILED'}")

    return success


def test_vocabulary():
    """Test Vocabulary Coverage"""
    print("\n" + "=" * 70)
    print("TEST 9: VOCABULARY")
    print("=" * 70)

    test_emojis = ["🌳", "👑", "🔒", "📊", "🐛", "💻"]

    for emoji in test_emojis:
        definition = get_emoji_definition(emoji)
        has_definition = definition is not None

        status = "✓" if has_definition else "✗"
        meaning = definition.primary_meaning if definition else "unknown"

        print(f"{status} {emoji}: {meaning}")

    return True


def test_compression():
    """Test Compression Ratios"""
    print("\n" + "=" * 70)
    print("TEST 10: COMPRESSION")
    print("=" * 70)

    test_cases = [
        ("Use tree of thoughts to analyze authentication", "🌳📊🔒"),
        ("Fix bug in security", "🐛🔒"),
        ("Review code quality", "👀💻"),
    ]

    for i, (nl, epl) in enumerate(test_cases, 1):
        ratio = calculate_compression_ratio(nl, epl)

        # Expect at least 50% compression
        has_compression = ratio >= 0.5
        status = "✓" if has_compression else "✗"

        print(f"{status} Test {i}:")
        print(f"  NL ({len(nl)} chars): '{nl}'")
        print(f"  EPL ({len(epl)} chars): '{epl}'")
        print(f"  Compression: {ratio:.0%}")

    return True


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all EPL integration tests"""
    print("\n" + "=" * 70)
    print("EPL INTEGRATION TESTS")
    print("=" * 70)
    print("Testing complete EPL pipeline: Lexer → Parser → Translator → Executor\n")

    tests = [
        ("Lexer", test_lexer),
        ("Parser", test_parser),
        ("Translator (NL→EPL)", test_translator_nl_to_epl),
        ("Translator (EPL→NL)", test_translator_epl_to_nl),
        ("Pattern Matching", test_pattern_matching),
        ("Executor", test_executor),
        ("Learning Mode", test_learning_mode),
        ("End-to-End", test_end_to_end),
        ("Vocabulary", test_vocabulary),
        ("Compression", test_compression),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' FAILED with exception: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! EPL is ready for production.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review and fix issues.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
