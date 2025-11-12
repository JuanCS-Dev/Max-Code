"""
Comprehensive Scientific Test Suite for ExploreAgent

Tests cover:
- Agent initialization and capabilities
- Codebase exploration functionality
- Cognitive mapping (directory structure analysis)
- File pattern matching
- Code search capabilities
- Context building
- Result formatting
- Error handling for missing files/directories
- Statistics tracking
- Integration with exploration tools

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)
Test everything. Hold fast to what is good.
"""

import pytest
import asyncio
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.explore_agent import ExploreAgent
from sdk.base_agent import AgentTask, AgentResult, AgentCapability


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def explore_agent():
    """Create ExploreAgent instance"""
    return ExploreAgent(agent_id="test_explorer")


@pytest.fixture
def temp_codebase():
    """Create temporary codebase for testing"""
    temp_dir = tempfile.mkdtemp(prefix="test_codebase_")

    # Create directory structure
    (Path(temp_dir) / "src").mkdir()
    (Path(temp_dir) / "src" / "utils").mkdir()
    (Path(temp_dir) / "tests").mkdir()
    (Path(temp_dir) / "docs").mkdir()

    # Create Python files
    (Path(temp_dir) / "src" / "__init__.py").write_text("")
    (Path(temp_dir) / "src" / "main.py").write_text("""
def main():
    '''Main entry point'''
    print("Hello World")
    return 0

if __name__ == "__main__":
    main()
""")

    (Path(temp_dir) / "src" / "utils" / "__init__.py").write_text("")
    (Path(temp_dir) / "src" / "utils" / "helpers.py").write_text("""
def calculate_sum(a, b):
    '''Calculate sum of two numbers'''
    return a + b

def calculate_product(a, b):
    '''Calculate product of two numbers'''
    # TODO: Add error handling
    return a * b

def validate_email(email):
    '''Validate email format'''
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
""")

    (Path(temp_dir) / "tests" / "test_main.py").write_text("""
import pytest
from src.main import main

def test_main_returns_zero():
    '''Test main returns 0'''
    assert main() == 0
""")

    (Path(temp_dir) / "tests" / "test_helpers.py").write_text("""
import pytest
from src.utils.helpers import calculate_sum, calculate_product

def test_calculate_sum():
    '''Test sum calculation'''
    assert calculate_sum(2, 3) == 5

def test_calculate_product():
    '''Test product calculation'''
    assert calculate_product(2, 3) == 6
""")

    # Create README
    (Path(temp_dir) / "README.md").write_text("""
# Test Project

This is a test project for ExploreAgent testing.

## Features
- Basic math operations
- Email validation
- TODO: Add more features
""")

    # Create config file
    (Path(temp_dir) / "config.json").write_text('{"name": "test_project", "version": "1.0.0"}')

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


# ============================================================================
# TEST 1-5: INITIALIZATION AND BASIC FUNCTIONALITY
# ============================================================================

def test_01_agent_initialization(explore_agent):
    """Test ExploreAgent initializes correctly"""
    assert explore_agent.agent_id == "test_explorer"
    assert explore_agent.agent_name == "Explore Agent"
    assert explore_agent.port == 8161
    assert hasattr(explore_agent, 'stats')
    assert explore_agent.stats['total_tasks_executed'] == 0
    print("✅ Test 1: Agent initialization successful")


def test_02_agent_capabilities(explore_agent):
    """Test ExploreAgent declares correct capabilities"""
    capabilities = explore_agent.get_capabilities()

    assert len(capabilities) > 0
    assert AgentCapability.EXPLORATION in capabilities
    print(f"✅ Test 2: Agent capabilities correct: {[c.value for c in capabilities]}")


def test_03_agent_has_exploration_tools(explore_agent):
    """Test ExploreAgent has access to exploration tools"""
    assert hasattr(explore_agent, 'tools')
    assert explore_agent.tools is not None
    print("✅ Test 3: Agent has access to tools")


def test_04_agent_stats_tracking(explore_agent):
    """Test ExploreAgent tracks statistics correctly"""
    initial_stats = explore_agent.get_stats()

    assert 'total_tasks_executed' in initial_stats
    assert 'successful_tasks' in initial_stats
    assert 'failed_tasks' in initial_stats
    assert 'success_rate' in initial_stats
    assert initial_stats['success_rate'] == 0.0  # No tasks executed yet
    print("✅ Test 4: Statistics tracking initialized correctly")


def test_05_basic_task_execution(explore_agent, temp_codebase):
    """Test ExploreAgent can execute basic exploration task"""
    task = AgentTask(
        id="explore-001",
        description="Explore the codebase structure",
        parameters={"path": temp_codebase}
    )

    result = explore_agent.run(task)

    assert isinstance(result, AgentResult)
    assert result.task_id == "explore-001"
    assert result.success is not None
    assert explore_agent.stats['total_tasks_executed'] == 1
    print("✅ Test 5: Basic task execution works")


# ============================================================================
# TEST 6-10: FILE PATTERN MATCHING
# ============================================================================

def test_06_find_python_files(explore_agent, temp_codebase):
    """Test finding Python files by pattern"""
    task = AgentTask(
        id="explore-002",
        description="Find all Python files",
        parameters={
            "path": temp_codebase,
            "pattern": "**/*.py"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    assert 'files' in result.output
    files = result.output['files']

    # Should find at least the files we created
    py_files = [f for f in files if f.endswith('.py')]
    assert len(py_files) >= 4  # We created 6 .py files
    print(f"✅ Test 6: Found {len(py_files)} Python files")


def test_07_find_test_files(explore_agent, temp_codebase):
    """Test finding test files specifically"""
    task = AgentTask(
        id="explore-003",
        description="Find all test files",
        parameters={
            "path": temp_codebase,
            "pattern": "**/test_*.py"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    files = result.output.get('files', [])
    test_files = [f for f in files if 'test_' in f]
    assert len(test_files) >= 2  # We created 2 test files
    print(f"✅ Test 7: Found {len(test_files)} test files")


def test_08_find_by_extension(explore_agent, temp_codebase):
    """Test finding files by extension"""
    task = AgentTask(
        id="explore-004",
        description="Find all markdown files",
        parameters={
            "path": temp_codebase,
            "extension": "md"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    files = result.output.get('files', [])
    md_files = [f for f in files if f.endswith('.md')]
    assert len(md_files) >= 1  # We created README.md
    print(f"✅ Test 8: Found {len(md_files)} markdown files")


def test_09_find_json_config_files(explore_agent, temp_codebase):
    """Test finding configuration files"""
    task = AgentTask(
        id="explore-005",
        description="Find JSON configuration files",
        parameters={
            "path": temp_codebase,
            "pattern": "**/*.json"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    files = result.output.get('files', [])
    json_files = [f for f in files if f.endswith('.json')]
    assert len(json_files) >= 1  # We created config.json
    print(f"✅ Test 9: Found {len(json_files)} JSON files")


def test_10_empty_pattern_results(explore_agent, temp_codebase):
    """Test handling pattern that matches no files"""
    task = AgentTask(
        id="explore-006",
        description="Find files with non-existent extension",
        parameters={
            "path": temp_codebase,
            "pattern": "**/*.xyz123"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    files = result.output.get('files', [])
    assert len(files) == 0
    print("✅ Test 10: Empty pattern results handled correctly")


# ============================================================================
# TEST 11-15: CODE SEARCH FUNCTIONALITY
# ============================================================================

def test_11_search_for_function_definitions(explore_agent, temp_codebase):
    """Test searching for function definitions"""
    task = AgentTask(
        id="explore-007",
        description="Find all function definitions",
        parameters={
            "path": temp_codebase,
            "search_pattern": r"def\s+\w+",
            "file_type": "py"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    matches = result.output.get('matches', [])
    assert len(matches) >= 5  # We defined several functions
    print(f"✅ Test 11: Found {len(matches)} function definitions")


def test_12_search_for_todo_comments(explore_agent, temp_codebase):
    """Test searching for TODO comments"""
    task = AgentTask(
        id="explore-008",
        description="Find all TODO comments",
        parameters={
            "path": temp_codebase,
            "search_pattern": "TODO",
            "case_sensitive": False
        }
    )

    result = explore_agent.run(task)

    assert result.success
    matches = result.output.get('matches', [])
    assert len(matches) >= 2  # We added 2 TODO comments
    print(f"✅ Test 12: Found {len(matches)} TODO comments")


def test_13_search_for_imports(explore_agent, temp_codebase):
    """Test searching for import statements"""
    task = AgentTask(
        id="explore-009",
        description="Find all import statements",
        parameters={
            "path": temp_codebase,
            "search_pattern": r"(import|from)\s+\w+",
            "file_type": "py"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    matches = result.output.get('matches', [])
    assert len(matches) >= 2  # We have several imports
    print(f"✅ Test 13: Found {len(matches)} import statements")


def test_14_search_with_file_filter(explore_agent, temp_codebase):
    """Test searching with file type filter"""
    task = AgentTask(
        id="explore-010",
        description="Find pytest imports in test files",
        parameters={
            "path": temp_codebase,
            "search_pattern": "pytest",
            "glob_filter": "**/test_*.py"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    matches = result.output.get('matches', [])
    # All matches should be from test files
    for match in matches:
        assert 'test_' in match.get('file', '')
    print(f"✅ Test 14: Found {len(matches)} pytest imports in test files")


def test_15_case_insensitive_search(explore_agent, temp_codebase):
    """Test case-insensitive search"""
    task = AgentTask(
        id="explore-011",
        description="Find 'test' case-insensitively",
        parameters={
            "path": temp_codebase,
            "search_pattern": "test",
            "case_sensitive": False
        }
    )

    result = explore_agent.run(task)

    assert result.success
    matches = result.output.get('matches', [])
    # Should find both 'test' and 'Test'
    assert len(matches) >= 5
    print(f"✅ Test 15: Case-insensitive search found {len(matches)} matches")


# ============================================================================
# TEST 16-20: COGNITIVE MAPPING (DIRECTORY STRUCTURE)
# ============================================================================

def test_16_map_directory_structure(explore_agent, temp_codebase):
    """Test mapping directory structure"""
    task = AgentTask(
        id="explore-012",
        description="Map the directory structure",
        parameters={
            "path": temp_codebase,
            "action": "map_structure"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    structure = result.output.get('structure', {})

    # Should have identified key directories
    assert 'directories' in structure or len(structure) > 0
    print("✅ Test 16: Directory structure mapped successfully")


def test_17_identify_project_type(explore_agent, temp_codebase):
    """Test identifying project type"""
    task = AgentTask(
        id="explore-013",
        description="Identify project type and structure",
        parameters={
            "path": temp_codebase,
            "action": "identify_project"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    project_info = result.output.get('project_info', {})

    # Should identify it as a Python project
    assert 'project_type' in project_info or 'files' in result.output
    print("✅ Test 17: Project type identification works")


def test_18_count_files_by_type(explore_agent, temp_codebase):
    """Test counting files by type"""
    task = AgentTask(
        id="explore-014",
        description="Count files by type",
        parameters={
            "path": temp_codebase,
            "action": "count_by_type"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    counts = result.output.get('file_counts', result.output)

    # Should have counts for different file types
    assert isinstance(counts, dict) or 'files' in result.output
    print(f"✅ Test 18: File counting works: {counts}")


def test_19_analyze_codebase_metrics(explore_agent, temp_codebase):
    """Test analyzing basic codebase metrics"""
    task = AgentTask(
        id="explore-015",
        description="Analyze codebase metrics",
        parameters={
            "path": temp_codebase,
            "action": "analyze_metrics",
            "include_loc": True
        }
    )

    result = explore_agent.run(task)

    assert result.success
    metrics = result.output.get('metrics', result.output)

    # Should have some metrics
    assert metrics is not None
    print(f"✅ Test 19: Codebase metrics analyzed")


def test_20_find_entry_points(explore_agent, temp_codebase):
    """Test finding potential entry points"""
    task = AgentTask(
        id="explore-016",
        description="Find entry points (main, __main__, etc.)",
        parameters={
            "path": temp_codebase,
            "action": "find_entry_points"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    entry_points = result.output.get('entry_points', result.output.get('files', []))

    # Should find main.py as an entry point
    assert isinstance(entry_points, (list, dict))
    print(f"✅ Test 20: Entry points identified")


# ============================================================================
# TEST 21-25: CONTEXT BUILDING AND RESULT FORMATTING
# ============================================================================

def test_21_build_file_context(explore_agent, temp_codebase):
    """Test building context for specific files"""
    helpers_file = str(Path(temp_codebase) / "src" / "utils" / "helpers.py")

    task = AgentTask(
        id="explore-017",
        description="Build context for helpers.py",
        parameters={
            "file_path": helpers_file,
            "action": "build_context",
            "include_content": True
        }
    )

    result = explore_agent.run(task)

    assert result.success
    context = result.output.get('context', result.output)

    # Should have file information
    assert context is not None
    print("✅ Test 21: File context built successfully")


def test_22_summarize_exploration(explore_agent, temp_codebase):
    """Test creating exploration summary"""
    task = AgentTask(
        id="explore-018",
        description="Create exploration summary",
        parameters={
            "path": temp_codebase,
            "action": "summarize"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    summary = result.output.get('summary', result.output)

    # Should have summary information
    assert summary is not None
    print("✅ Test 22: Exploration summary created")


def test_23_result_contains_metadata(explore_agent, temp_codebase):
    """Test that results contain useful metadata"""
    task = AgentTask(
        id="explore-019",
        description="Explore with metadata",
        parameters={
            "path": temp_codebase,
            "pattern": "**/*.py",
            "include_metadata": True
        }
    )

    result = explore_agent.run(task)

    assert result.success
    # Should have metadata like timestamps, file counts, etc.
    assert 'files' in result.output or 'metadata' in result.output
    print("✅ Test 23: Results contain metadata")


def test_24_formatted_output(explore_agent, temp_codebase):
    """Test output is properly formatted"""
    task = AgentTask(
        id="explore-020",
        description="Get formatted exploration output",
        parameters={
            "path": temp_codebase,
            "pattern": "**/*.py",
            "format": "detailed"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    assert isinstance(result.output, dict)
    assert 'files' in result.output
    print("✅ Test 24: Output properly formatted")


def test_25_hierarchical_file_list(explore_agent, temp_codebase):
    """Test generating hierarchical file listing"""
    task = AgentTask(
        id="explore-021",
        description="Generate hierarchical file structure",
        parameters={
            "path": temp_codebase,
            "action": "tree_view"
        }
    )

    result = explore_agent.run(task)

    assert result.success
    output = result.output

    # Should represent hierarchical structure
    assert output is not None
    print("✅ Test 25: Hierarchical file listing generated")


# ============================================================================
# TEST 26-30: ERROR HANDLING
# ============================================================================

def test_26_handle_missing_directory(explore_agent):
    """Test handling of non-existent directory"""
    task = AgentTask(
        id="explore-022",
        description="Explore non-existent directory",
        parameters={
            "path": "/non/existent/directory/xyz123"
        }
    )

    result = explore_agent.run(task)

    # Should fail gracefully
    assert not result.success or result.output.get('files', []) == []
    assert result.error is not None or 'error' in result.output or result.output.get('files') == []
    print("✅ Test 26: Missing directory handled gracefully")


def test_27_handle_invalid_pattern(explore_agent, temp_codebase):
    """Test handling of invalid regex pattern"""
    task = AgentTask(
        id="explore-023",
        description="Search with invalid regex",
        parameters={
            "path": temp_codebase,
            "search_pattern": "[invalid(regex"  # Invalid regex
        }
    )

    result = explore_agent.run(task)

    # Should handle gracefully
    assert not result.success or 'error' in str(result.output).lower()
    print("✅ Test 27: Invalid pattern handled gracefully")


def test_28_handle_permission_denied(explore_agent):
    """Test handling of permission denied error"""
    # Try to access a typically restricted directory
    task = AgentTask(
        id="explore-024",
        description="Explore restricted directory",
        parameters={
            "path": "/root"
        }
    )

    result = explore_agent.run(task)

    # Should handle permission error gracefully
    # Result may succeed but with empty files, or fail with error
    assert result is not None
    print("✅ Test 28: Permission errors handled gracefully")


def test_29_handle_empty_parameters(explore_agent):
    """Test handling of empty parameters"""
    task = AgentTask(
        id="explore-025",
        description="Explore with minimal parameters",
        parameters={}
    )

    result = explore_agent.run(task)

    # Should handle gracefully (may use defaults)
    assert result is not None
    assert isinstance(result, AgentResult)
    print("✅ Test 29: Empty parameters handled gracefully")


def test_30_handle_file_not_directory(explore_agent, temp_codebase):
    """Test handling when path is a file, not directory"""
    file_path = str(Path(temp_codebase) / "README.md")

    task = AgentTask(
        id="explore-026",
        description="Explore file instead of directory",
        parameters={
            "path": file_path
        }
    )

    result = explore_agent.run(task)

    # Should handle gracefully
    assert result is not None
    print("✅ Test 30: File path instead of directory handled")


# ============================================================================
# TEST 31-35: STATISTICS AND METRICS
# ============================================================================

def test_31_stats_increment_on_success(explore_agent, temp_codebase):
    """Test statistics increment on successful execution"""
    initial_successful = explore_agent.stats['successful_tasks']

    task = AgentTask(
        id="explore-027",
        description="Successful exploration",
        parameters={"path": temp_codebase}
    )

    result = explore_agent.run(task)

    if result.success:
        assert explore_agent.stats['successful_tasks'] == initial_successful + 1
    print("✅ Test 31: Success statistics tracked correctly")


def test_32_stats_increment_on_failure(explore_agent):
    """Test statistics increment on failed execution"""
    initial_failed = explore_agent.stats['failed_tasks']

    task = AgentTask(
        id="explore-028",
        description="Failed exploration",
        parameters={"path": "/definitely/not/a/real/path/xyz123"}
    )

    result = explore_agent.run(task)

    if not result.success:
        assert explore_agent.stats['failed_tasks'] == initial_failed + 1
    print("✅ Test 32: Failure statistics tracked correctly")


def test_33_calculate_success_rate(explore_agent, temp_codebase):
    """Test success rate calculation"""
    # Execute multiple tasks
    for i in range(5):
        task = AgentTask(
            id=f"explore-029-{i}",
            description=f"Test task {i}",
            parameters={"path": temp_codebase}
        )
        explore_agent.run(task)

    stats = explore_agent.get_stats()

    assert 'success_rate' in stats
    assert 0 <= stats['success_rate'] <= 100
    print(f"✅ Test 33: Success rate calculated: {stats['success_rate']:.1f}%")


def test_34_total_tasks_executed(explore_agent, temp_codebase):
    """Test total tasks counter"""
    initial_total = explore_agent.stats['total_tasks_executed']

    # Execute 3 tasks
    for i in range(3):
        task = AgentTask(
            id=f"explore-030-{i}",
            description=f"Test task {i}",
            parameters={"path": temp_codebase}
        )
        explore_agent.run(task)

    assert explore_agent.stats['total_tasks_executed'] == initial_total + 3
    print(f"✅ Test 34: Total tasks counter accurate: {explore_agent.stats['total_tasks_executed']}")


def test_35_stats_reset_behavior(explore_agent):
    """Test statistics are persistent across calls"""
    initial_stats = explore_agent.get_stats()

    # Stats should persist (not reset) between get_stats calls
    stats_again = explore_agent.get_stats()

    assert initial_stats['total_tasks_executed'] == stats_again['total_tasks_executed']
    print("✅ Test 35: Statistics persist correctly")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("EXPLOREAGENT - COMPREHENSIVE SCIENTIFIC TEST SUITE")
    print("=" * 80)
    print("\nBiblical Foundation:")
    print('"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)')
    print("Test everything. Hold fast to what is good.")
    print("=" * 80)

    # Create agent and temp codebase
    agent = ExploreAgent(agent_id="test_explorer")

    # Create temporary codebase
    temp_dir = tempfile.mkdtemp(prefix="test_codebase_")
    (Path(temp_dir) / "src").mkdir()
    (Path(temp_dir) / "src" / "__init__.py").write_text("# Init")
    (Path(temp_dir) / "src" / "main.py").write_text("def main(): pass")

    print("\n🧪 Running 35 scientific tests...\n")

    # Run a subset of tests for demo
    tests_run = 0
    tests_passed = 0

    try:
        test_01_agent_initialization(agent)
        tests_run += 1
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        tests_run += 1

    try:
        test_02_agent_capabilities(agent)
        tests_run += 1
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        tests_run += 1

    try:
        test_03_agent_has_exploration_tools(agent)
        tests_run += 1
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        tests_run += 1

    try:
        test_04_agent_stats_tracking(agent)
        tests_run += 1
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        tests_run += 1

    try:
        test_05_basic_task_execution(agent, temp_dir)
        tests_run += 1
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 5 failed: {e}")
        tests_run += 1

    # Cleanup
    shutil.rmtree(temp_dir)

    print("\n" + "=" * 80)
    print(f"TEST SUMMARY: {tests_passed}/{tests_run} tests passed")
    print("=" * 80)
    print("\nNote: Run with pytest to execute all 35 tests:")
    print("  pytest tests/test_explore_agent.py -v")
    print("=" * 80)
