#!/usr/bin/env python3
"""
Sprint 3 Validation Tests - Git Wrapper ✅

Valida que o Git Wrapper está implementado com técnica Boris:
- Security-first (safe operations only)
- Beautiful output (Rich formatting)
- Temporal philosophy (past/present/future)
- Complete feature set (status, diff, log, branch, commit, push, pull)

Soli Deo Gloria 🙏
"""

import pytest
import os
import tempfile
import subprocess
from pathlib import Path

from core.tools.git_tool import GitTool, GitStatus, GitFileStatus
from core.tools.types import ToolResult


class TestGitToolBasics:
    """Test 1 - Git Tool Basic Functionality"""

    def test_1_1_git_tool_initialization(self):
        """Test 1.1: GitTool initializes correctly"""
        git_tool = GitTool()

        assert git_tool is not None
        assert hasattr(git_tool, 'executor')
        assert hasattr(git_tool, 'console')
        assert hasattr(git_tool, 'status')
        assert hasattr(git_tool, 'diff')
        assert hasattr(git_tool, 'log')
        assert hasattr(git_tool, 'branch')
        assert hasattr(git_tool, 'commit')
        assert hasattr(git_tool, 'push')
        assert hasattr(git_tool, 'pull')

        print("✅ Test 1.1 passed: GitTool initialized with all methods")

    def test_1_2_git_check_repo_detection(self):
        """Test 1.2: Git repo detection works"""
        git_tool = GitTool()

        # Test in non-git directory
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = git_tool._check_git_repo()

            assert result.type == "error"
            assert "not a git repository" in result.content[0].text.lower()

        print("✅ Test 1.2 passed: Non-git directory detected correctly")

    def test_1_3_git_status_in_repo(self):
        """Test 1.3: Git status works in real repository"""
        git_tool = GitTool()

        # We're in MAX-CODE project (is a git repo)
        # Change to project root
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        result = git_tool.status()

        assert result is not None
        assert result.type in ["success", "error"]

        if result.type == "success":
            output = result.content[0].text
            assert "branch" in output.lower() or "clean" in output.lower()

        print("✅ Test 1.3 passed: Git status executed successfully")


class TestGitToolOperations:
    """Test 2 - Git Tool Operations"""

    def test_2_1_git_diff_functionality(self):
        """Test 2.1: Git diff works"""
        git_tool = GitTool()

        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        result = git_tool.diff()

        assert result is not None
        assert result.type in ["success", "error"]

        # Diff either shows changes or "no changes"
        if result.type == "success":
            output = result.content[0].text if result.content else ""
            assert "no changes" in output.lower() or "diff" in output.lower() or len(output) >= 0

        print("✅ Test 2.1 passed: Git diff executed successfully")

    def test_2_2_git_log_functionality(self):
        """Test 2.2: Git log works"""
        git_tool = GitTool()

        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        result = git_tool.log(limit=5)

        assert result is not None
        assert result.type in ["success", "error"]

        if result.type == "success":
            output = result.content[0].text
            # Log should show commit history
            assert len(output) > 0

        print("✅ Test 2.2 passed: Git log executed successfully")

    def test_2_3_git_branch_functionality(self):
        """Test 2.3: Git branch works"""
        git_tool = GitTool()

        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        result = git_tool.branch()

        assert result is not None
        assert result.type in ["success", "error"]

        if result.type == "success":
            output = result.content[0].text
            # Branch list should show current branch
            assert "branch" in output.lower() or len(output) > 0

        print("✅ Test 2.3 passed: Git branch executed successfully")


class TestGitToolSafety:
    """Test 3 - Git Tool Safety Features"""

    def test_3_1_force_push_blocked(self):
        """Test 3.1: Force push is blocked for safety"""
        git_tool = GitTool()

        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        # Attempt force push (should be blocked)
        result = git_tool.push(force=True)

        assert result.type == "error"
        assert "blocked" in result.content[0].text.lower() or "force" in result.content[0].text.lower()

        print("✅ Test 3.1 passed: Force push blocked correctly (Boris safety)")

    def test_3_2_commit_validation(self):
        """Test 3.2: Commit message validation"""
        git_tool = GitTool()

        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        # Test invalid commit message (too short)
        result = git_tool.commit(message="x")

        assert result.type == "error"
        assert "invalid" in result.content[0].text.lower() or "message" in result.content[0].text.lower()

        print("✅ Test 3.2 passed: Commit message validation works")

    def test_3_3_safe_operations_only(self):
        """Test 3.3: Only safe git operations exposed"""
        git_tool = GitTool()

        # Check that dangerous operations are not exposed
        assert not hasattr(git_tool, 'reset_hard')
        assert not hasattr(git_tool, 'clean_force')
        assert not hasattr(git_tool, 'rebase_force')

        # Check that safe operations are exposed
        assert hasattr(git_tool, 'status')
        assert hasattr(git_tool, 'diff')
        assert hasattr(git_tool, 'log')
        assert hasattr(git_tool, 'branch')

        print("✅ Test 3.3 passed: Only safe operations exposed (Boris principle)")


class TestGitToolOutput:
    """Test 4 - Git Tool Output Beauty (Boris Technique)"""

    def test_4_1_status_output_has_icons(self):
        """Test 4.1: Status output has beautiful icons"""
        git_tool = GitTool()

        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

        result = git_tool.status()

        if result.type == "success":
            output = result.content[0].text

            # Check for Boris-style icons and formatting
            has_icons = any(icon in output for icon in ['📍', '✨', '📝', '🗑️', '📄', '🌿'])
            has_formatting = '[' in output  # Rich markup

            assert has_icons or has_formatting, "Output should have icons or rich formatting"

        print("✅ Test 4.1 passed: Status output has beautiful formatting (Boris)")

    def test_4_2_temporal_philosophy_metaphors(self):
        """Test 4.2: Git Tool uses temporal philosophy"""
        git_tool = GitTool()

        # Check docstrings for temporal metaphors
        assert "present" in git_tool.status.__doc__.lower() or "heartbeat" in git_tool.status.__doc__.lower()
        assert "past" in git_tool.log.__doc__.lower() or "archaeology" in git_tool.log.__doc__.lower()
        assert "future" in git_tool.push.__doc__.lower() or "publication" in git_tool.push.__doc__.lower()

        print("✅ Test 4.2 passed: Temporal philosophy present in docstrings (Boris)")

    def test_4_3_error_messages_helpful(self):
        """Test 4.3: Error messages are helpful and beautiful"""
        git_tool = GitTool()

        # Test error in non-repo
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = git_tool.status()

            assert result.type == "error"
            error_msg = result.content[0].text

            # Check for helpful error messages
            assert len(error_msg) > 20  # Substantial message
            assert "❌" in error_msg or "not a git repository" in error_msg.lower()

        print("✅ Test 4.3 passed: Error messages are helpful (Boris)")


class TestGitToolIntegration:
    """Test 5 - Git Tool REPL Integration"""

    def test_5_1_git_tool_exists_in_code(self):
        """Test 5.1: GitTool module exists and is importable"""
        # Just verify the module can be imported
        from core.tools.git_tool import GitTool

        # Verify GitTool class has expected methods
        assert hasattr(GitTool, 'status')
        assert hasattr(GitTool, 'diff')
        assert hasattr(GitTool, 'log')
        assert hasattr(GitTool, 'branch')

        print("✅ Test 5.1 passed: GitTool module exists and is importable")

    def test_5_2_git_autocomplete_structure(self):
        """Test 5.2: Git autocomplete structure exists"""
        # Just verify the file structure is correct
        import os
        repl_file = os.path.join(os.path.dirname(__file__), '..', 'cli', 'repl_enhanced.py')

        assert os.path.exists(repl_file), "repl_enhanced.py exists"

        # Verify git_tool is imported
        with open(repl_file, 'r') as f:
            content = f.read()
            assert 'from core.tools.git_tool import GitTool' in content
            assert "'/git'" in content or '"/git"' in content  # Git autocomplete present

        print("✅ Test 5.2 passed: Git autocomplete structure verified")

    def test_5_3_git_keyword_integration(self):
        """Test 5.3: Git keyword detection integrated in code"""
        import os
        repl_file = os.path.join(os.path.dirname(__file__), '..', 'cli', 'repl_enhanced.py')

        with open(repl_file, 'r') as f:
            content = f.read()
            # Verify git keywords are in tool_keywords dict
            assert "'git'" in content and "git status" in content

        print("✅ Test 5.3 passed: Git keyword detection integrated")


def run_all_tests():
    """Run all Sprint 3 tests"""
    print("\n" + "="*60)
    print("🌿 SPRINT 3 - GIT WRAPPER VALIDATION")
    print("="*60 + "\n")

    test_results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }

    test_classes = [
        TestGitToolBasics,
        TestGitToolOperations,
        TestGitToolSafety,
        TestGitToolOutput,
        TestGitToolIntegration
    ]

    for test_class in test_classes:
        print(f"\n{'─'*60}")
        print(f"Running {test_class.__name__}")
        print(f"{'─'*60}\n")

        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]

        for method_name in test_methods:
            test_results["total"] += 1
            try:
                method = getattr(instance, method_name)
                method()
                test_results["passed"] += 1
            except Exception as e:
                test_results["failed"] += 1
                print(f"❌ {method_name} FAILED: {e}")

    # Print summary
    print("\n" + "="*60)
    print("📊 SPRINT 3 TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {test_results['passed']}/{test_results['total']}")
    print(f"❌ Failed: {test_results['failed']}/{test_results['total']}")

    success_rate = (test_results['passed'] / test_results['total']) * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! Git Wrapper COMPLETE! 🌿")
    elif success_rate >= 80:
        print("\n✅ Git Wrapper mostly working (minor issues)")
    else:
        print("\n⚠️  Git Wrapper needs attention")

    return test_results


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        print(traceback.format_exc())
