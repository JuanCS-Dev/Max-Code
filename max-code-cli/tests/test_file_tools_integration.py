"""
File Tools Integration Test

Tests complete integration of file tools with ToolExecutor.

Biblical Foundation:
"Provai todas as coisas; retende o que é bom." (1 Tessalonicenses 5:21)
Test all things - validate completeness.
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.deter_agent.execution.tool_executor import (
    ToolExecutor,
    Tool,
    ToolType,
    ToolStatus,
)


def test_file_read():
    """Test FileReader integration"""
    print("=" * 70)
    print("TEST 1: FileReader Integration")
    print("=" * 70)

    executor = ToolExecutor()

    # Register file read tool
    tool = Tool(
        name="read_test",
        type=ToolType.FILE_READ,
        description="Read test file",
        parameters={'file_path': __file__, 'limit': 20}
    )
    executor.register_tool(tool)

    # Execute
    result = executor.execute("read_test")

    if result.status == ToolStatus.SUCCESS:
        print(f"✓ File read successful!")
        print(f"  Lines read: {len(result.output.split(chr(10)))}")
        print(f"  Execution time: {result.execution_time:.3f}s")
        print(f"\nFirst 10 lines of output:")
        for line in result.output.split('\n')[:10]:
            print(f"    {line}")
        return True
    else:
        print(f"✗ Failed: {result.error}")
        return False


def test_glob():
    """Test GlobTool integration"""
    print("\n" + "=" * 70)
    print("TEST 2: GlobTool Integration")
    print("=" * 70)

    executor = ToolExecutor()

    # Register glob tool
    tool = Tool(
        name="find_python_files",
        type=ToolType.GLOB,
        description="Find Python files in core/epl",
        parameters={'pattern': '**/*.py', 'path': 'core/epl/', 'max_results': 10}
    )
    executor.register_tool(tool)

    # Execute
    result = executor.execute("find_python_files")

    if result.status == ToolStatus.SUCCESS:
        print(f"✓ Glob successful!")
        print(f"  Execution time: {result.execution_time:.3f}s")
        print(f"\nOutput:\n{result.output}")
        return True
    else:
        print(f"✗ Failed: {result.error}")
        return False


def test_grep():
    """Test GrepTool integration"""
    print("\n" + "=" * 70)
    print("TEST 3: GrepTool Integration")
    print("=" * 70)

    executor = ToolExecutor()

    # Register grep tool
    tool = Tool(
        name="find_biblical_foundation",
        type=ToolType.GREP,
        description="Find Biblical Foundation comments",
        parameters={
            'pattern': 'Biblical Foundation',
            'path': 'core/epl/',
            'output_mode': 'files_with_matches'
        }
    )
    executor.register_tool(tool)

    # Execute
    result = executor.execute("find_biblical_foundation")

    if result.status == ToolStatus.SUCCESS:
        print(f"✓ Grep successful!")
        print(f"  Execution time: {result.execution_time:.3f}s")
        print(f"\nOutput:\n{result.output}")
        return True
    else:
        print(f"✗ Failed: {result.error}")
        return False


def test_file_write():
    """Test FileWriter integration"""
    print("\n" + "=" * 70)
    print("TEST 4: FileWriter Integration")
    print("=" * 70)

    executor = ToolExecutor()

    # Register file write tool
    test_file = "/tmp/max_code_test_integration.txt"
    content = """# Test File
This is a test file created by FileWriter integration test.

Biblical Foundation:
"Escreve a visão e torna-a bem legível" (Habacuque 2:2)
"""

    tool = Tool(
        name="write_test",
        type=ToolType.FILE_WRITE,
        description="Write test file",
        parameters={'file_path': test_file, 'content': content}
    )
    executor.register_tool(tool)

    # Execute
    result = executor.execute("write_test")

    if result.status == ToolStatus.SUCCESS:
        print(f"✓ File write successful!")
        print(f"  Execution time: {result.execution_time:.3f}s")
        print(f"  Output: {result.output}")

        # Verify file exists
        if Path(test_file).exists():
            print(f"  File created: {test_file}")

            # Cleanup
            Path(test_file).unlink()
            print(f"  Cleaned up test file")

        return True
    else:
        print(f"✗ Failed: {result.error}")
        return False


def test_file_edit():
    """Test FileEditor integration"""
    print("\n" + "=" * 70)
    print("TEST 5: FileEditor Integration")
    print("=" * 70)

    executor = ToolExecutor()

    # First, create a file to edit
    test_file = "/tmp/max_code_edit_integration.txt"
    original = """Line 1: Hello
Line 2: World
Line 3: Goodbye
"""

    write_tool = Tool(
        name="setup_edit_test",
        type=ToolType.FILE_WRITE,
        description="Setup file for edit test",
        parameters={'file_path': test_file, 'content': original}
    )
    executor.register_tool(write_tool)
    executor.execute("setup_edit_test")

    # Now edit it
    edit_tool = Tool(
        name="edit_test",
        type=ToolType.FILE_EDIT,
        description="Edit test file",
        parameters={
            'file_path': test_file,
            'old_string': 'World',
            'new_string': 'Universe'
        }
    )
    executor.register_tool(edit_tool)

    result = executor.execute("edit_test")

    if result.status == ToolStatus.SUCCESS:
        print(f"✓ File edit successful!")
        print(f"  Execution time: {result.execution_time:.3f}s")
        print(f"\nOutput:\n{result.output}")

        # Cleanup
        Path(test_file).unlink()
        # Remove backup
        import glob
        for backup in glob.glob(f"{test_file}.backup.*"):
            Path(backup).unlink()

        print(f"\n  Cleaned up test files")

        return True
    else:
        print(f"✗ Failed: {result.error}")
        return False


def test_all_tools_e2e():
    """End-to-end test using all tools"""
    print("\n" + "=" * 70)
    print("TEST 6: E2E - All Tools Together")
    print("=" * 70)

    executor = ToolExecutor()

    # Step 1: Find Python files in core/tools/
    print("\n1. Finding Python files in core/tools/...")
    glob_tool = Tool(
        name="find_tool_files",
        type=ToolType.GLOB,
        description="Find tool files",
        parameters={'pattern': '*.py', 'path': 'core/tools/'}
    )
    executor.register_tool(glob_tool)
    glob_result = executor.execute("find_tool_files")

    if glob_result.status != ToolStatus.SUCCESS:
        print(f"✗ Glob failed: {glob_result.error}")
        return False

    print(f"✓ Found files:\n{glob_result.output}")

    # Step 2: Search for specific pattern in those files
    print("\n2. Searching for 'Biblical Foundation'...")
    grep_tool = Tool(
        name="search_biblical",
        type=ToolType.GREP,
        description="Search for Biblical Foundation",
        parameters={
            'pattern': 'Biblical Foundation',
            'path': 'core/tools/',
            'output_mode': 'count'
        }
    )
    executor.register_tool(grep_tool)
    grep_result = executor.execute("search_biblical")

    if grep_result.status != ToolStatus.SUCCESS:
        print(f"✗ Grep failed: {grep_result.error}")
        return False

    print(f"✓ Search results:\n{grep_result.output}")

    # Step 3: Read one of the files
    print("\n3. Reading file_reader.py (first 30 lines)...")
    read_tool = Tool(
        name="read_file_reader",
        type=ToolType.FILE_READ,
        description="Read file_reader.py",
        parameters={'file_path': 'core/tools/file_reader.py', 'limit': 30}
    )
    executor.register_tool(read_tool)
    read_result = executor.execute("read_file_reader")

    if read_result.status != ToolStatus.SUCCESS:
        print(f"✗ Read failed: {read_result.error}")
        return False

    print(f"✓ Read successful! (showing first 10 lines)")
    for line in read_result.output.split('\n')[:10]:
        print(f"  {line}")

    # Print stats
    print("\n" + "=" * 70)
    print("E2E Test Statistics:")
    print("=" * 70)
    executor.print_stats()

    return True


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "=" * 70)
    print("FILE TOOLS INTEGRATION TESTS")
    print("=" * 70)
    print("Testing integration of 5 file tools with ToolExecutor\n")

    tests = [
        ("FileReader", test_file_read),
        ("GlobTool", test_glob),
        ("GrepTool", test_grep),
        ("FileWriter", test_file_write),
        ("FileEditor", test_file_edit),
        ("End-to-End", test_all_tools_e2e),
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
        print("\n🎉 ALL TESTS PASSED! File tools are fully integrated.")
        print("\n🏎️ Ferrari com rodas completas! Max-Code CLI está operacional!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review and fix issues.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
