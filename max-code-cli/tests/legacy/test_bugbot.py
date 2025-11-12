"""
BugBot Tests - Proactive Error Detection

Tests P4 - Prudência Operacional through proactive error detection.

Biblical Foundation:
"Vigiai, estai firmes na fé" (1 Coríntios 16:13)
Vigilance through testing.
"""

import sys
import os
from pathlib import Path
import tempfile

# Add parent to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.deter_agent.execution.bugbot import (
    BugBot,
    ErrorSeverity,
    ErrorCategory,
    analyze_file,
)


def test_syntax_error_detection():
    """Test detection of syntax errors"""
    print("=" * 70)
    print("TEST 1: Syntax Error Detection")
    print("=" * 70)

    # Create file with syntax error
    test_file = Path(tempfile.mktemp(suffix=".py"))
    test_file.write_text("""
def broken_function(
    print("Missing closing parenthesis")
""")

    bugbot = BugBot()
    result = bugbot.analyze_file(str(test_file))

    test_file.unlink()

    if result.critical_issues > 0 and not result.is_safe_to_execute:
        print(f"✓ Syntax error detected")
        print(f"  Critical issues: {result.critical_issues}")
        print(f"  Safe to execute: {result.is_safe_to_execute}")
        return True
    else:
        print(f"✗ Failed to detect syntax error")
        return False


def test_security_risk_detection():
    """Test detection of security risks"""
    print("\n" + "=" * 70)
    print("TEST 2: Security Risk Detection")
    print("=" * 70)

    # Create file with eval() usage
    test_file = Path(tempfile.mktemp(suffix=".py"))
    test_file.write_text("""
def dangerous_function():
    user_input = input("Enter code: ")
    eval(user_input)  # Security risk!
""")

    bugbot = BugBot()
    result = bugbot.analyze_file(str(test_file))

    test_file.unlink()

    security_bugs = [bug for bug in result.bugs if bug.category == ErrorCategory.SECURITY_RISK]

    if len(security_bugs) > 0:
        print(f"✓ Security risk detected")
        print(f"  Security bugs found: {len(security_bugs)}")
        for bug in security_bugs:
            print(f"  - {bug.description}")
        return True
    else:
        print(f"✗ Failed to detect security risk")
        return False


def test_import_warning_detection():
    """Test detection of import warnings"""
    print("\n" + "=" * 70)
    print("TEST 3: Import Warning Detection")
    print("=" * 70)

    # Create file with wildcard import
    test_file = Path(tempfile.mktemp(suffix=".py"))
    test_file.write_text("""
from os import *

def some_function():
    pass
""")

    bugbot = BugBot()
    result = bugbot.analyze_file(str(test_file))

    test_file.unlink()

    style_warnings = [bug for bug in result.bugs if bug.category == ErrorCategory.STYLE_WARNING]

    if len(style_warnings) > 0:
        print(f"✓ Import warning detected")
        print(f"  Style warnings found: {len(style_warnings)}")
        return True
    else:
        print(f"✗ Failed to detect import warning")
        return False


def test_clean_file_analysis():
    """Test analysis of clean file (no issues)"""
    print("\n" + "=" * 70)
    print("TEST 4: Clean File Analysis")
    print("=" * 70)

    # Create clean file
    test_file = Path(tempfile.mktemp(suffix=".py"))
    test_file.write_text("""
def clean_function(x, y):
    \"\"\"A clean function with no issues\"\"\"
    result = x + y
    return result

if __name__ == "__main__":
    print(clean_function(1, 2))
""")

    bugbot = BugBot()
    result = bugbot.analyze_file(str(test_file))

    test_file.unlink()

    if len(result.bugs) == 0 and result.is_safe_to_execute:
        print(f"✓ Clean file correctly analyzed")
        print(f"  Bugs detected: {len(result.bugs)}")
        print(f"  Safe to execute: {result.is_safe_to_execute}")
        return True
    else:
        print(f"✗ Clean file incorrectly flagged")
        print(f"  Bugs detected: {len(result.bugs)}")
        return False


def test_directory_analysis():
    """Test analysis of entire directory"""
    print("\n" + "=" * 70)
    print("TEST 5: Directory Analysis")
    print("=" * 70)

    # Create temp directory with multiple files
    test_dir = Path(tempfile.mkdtemp(prefix="bugbot_test_"))

    # File 1: Clean
    (test_dir / "clean.py").write_text("def func(): pass")

    # File 2: With error
    (test_dir / "buggy.py").write_text("def broken(: pass")

    bugbot = BugBot()
    results = bugbot.analyze_directory(str(test_dir), recursive=False)

    # Cleanup
    for file in test_dir.glob("*.py"):
        file.unlink()
    test_dir.rmdir()

    if len(results) == 2:
        print(f"✓ Directory analysis successful")
        print(f"  Files analyzed: {len(results)}")
        safe_files = sum(1 for r in results if r.is_safe_to_execute)
        print(f"  Safe files: {safe_files}/{len(results)}")
        return True
    else:
        print(f"✗ Directory analysis failed")
        print(f"  Expected 2 files, got {len(results)}")
        return False


def test_statistics_tracking():
    """Test that statistics are properly tracked"""
    print("\n" + "=" * 70)
    print("TEST 6: Statistics Tracking")
    print("=" * 70)

    bugbot = BugBot()

    # Analyze a file with errors
    test_file = Path(tempfile.mktemp(suffix=".py"))
    test_file.write_text("def broken(: pass")

    bugbot.analyze_file(str(test_file))

    test_file.unlink()

    if (bugbot.stats['files_analyzed'] > 0 and
        bugbot.stats['bugs_detected'] > 0 and
        bugbot.stats['critical_issues_prevented'] > 0):
        print(f"✓ Statistics correctly tracked")
        print(f"  Files analyzed: {bugbot.stats['files_analyzed']}")
        print(f"  Bugs detected: {bugbot.stats['bugs_detected']}")
        print(f"  Critical issues prevented: {bugbot.stats['critical_issues_prevented']}")
        return True
    else:
        print(f"✗ Statistics tracking failed")
        return False


def test_convenience_function():
    """Test convenience function"""
    print("\n" + "=" * 70)
    print("TEST 7: Convenience Function")
    print("=" * 70)

    test_file = Path(tempfile.mktemp(suffix=".py"))
    test_file.write_text("def func(): pass")

    result = analyze_file(str(test_file))

    test_file.unlink()

    if result and result.is_safe_to_execute:
        print(f"✓ Convenience function works")
        return True
    else:
        print(f"✗ Convenience function failed")
        return False


def run_all_tests():
    """Run all BugBot tests"""
    print("\n" + "=" * 70)
    print("BUGBOT TESTS (P4 - Prudência Operacional)")
    print("=" * 70)
    print("Testing Proactive Error Detection\n")

    tests = [
        ("Syntax Error Detection", test_syntax_error_detection),
        ("Security Risk Detection", test_security_risk_detection),
        ("Import Warning Detection", test_import_warning_detection),
        ("Clean File Analysis", test_clean_file_analysis),
        ("Directory Analysis", test_directory_analysis),
        ("Statistics Tracking", test_statistics_tracking),
        ("Convenience Function", test_convenience_function),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
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
        print("\n🎉 ALL TESTS PASSED!")
        print("🏎️ PAGANI: P4 - Prudência Operacional está operacional!")
        print("\n🔍 BugBot - Proactive Error Detection:")
        print("  ✓ Syntax error detection")
        print("  ✓ Security risk detection")
        print("  ✓ Import warning detection")
        print("  ✓ Clean file analysis")
        print("  ✓ Directory-wide analysis")
        print("  ✓ Statistics tracking")
        print("  ✓ Easy-to-use API")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review and fix issues.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
