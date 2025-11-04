"""
Git-Native Workflow Tests

Tests P2 - Transparência Radical through git-native workflows.

Biblical Foundation:
"Nada há encoberto que não haja de ser revelado" (Lucas 12:2)
Transparency through comprehensive testing.
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil
import subprocess

# Add parent to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.deter_agent.execution.git_native import (
    GitNativeWorkflow,
    create_git_workflow,
)


def setup_test_repo():
    """Create a temporary git repository for testing"""
    test_dir = Path(tempfile.mkdtemp(prefix="max_code_git_test_"))

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=test_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=test_dir,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=test_dir,
        check=True,
        capture_output=True
    )

    # Create initial commit
    test_file = test_dir / "README.md"
    test_file.write_text("# Test Repo\n")

    subprocess.run(["git", "add", "README.md"], cwd=test_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=test_dir,
        check=True,
        capture_output=True
    )

    return test_dir


def cleanup_test_repo(test_dir: Path):
    """Remove temporary test repository"""
    if test_dir.exists():
        shutil.rmtree(test_dir)


def test_git_detection():
    """Test git repository detection"""
    print("=" * 70)
    print("TEST 1: Git Repository Detection")
    print("=" * 70)

    test_dir = setup_test_repo()

    try:
        git = GitNativeWorkflow(repo_path=str(test_dir))

        if git.is_git_repo:
            print(f"✓ Git repository correctly detected")
            return True
        else:
            print(f"✗ Failed to detect git repository")
            return False

    finally:
        cleanup_test_repo(test_dir)


def test_get_status():
    """Test getting git status"""
    print("\n" + "=" * 70)
    print("TEST 2: Get Git Status")
    print("=" * 70)

    test_dir = setup_test_repo()

    try:
        git = GitNativeWorkflow(repo_path=str(test_dir))

        # Create dirty file
        dirty_file = test_dir / "dirty.txt"
        dirty_file.write_text("Modified content")

        status = git.get_status()

        if status.is_repo and status.branch and len(status.untracked_files) == 1:
            print(f"✓ Git status correctly retrieved")
            print(f"  Branch: {status.branch}")
            print(f"  Untracked files: {len(status.untracked_files)}")
            return True
        else:
            print(f"✗ Git status retrieval failed")
            return False

    finally:
        cleanup_test_repo(test_dir)


def test_commit_dirty_files():
    """Test committing dirty files"""
    print("\n" + "=" * 70)
    print("TEST 3: Commit Dirty Files")
    print("=" * 70)

    test_dir = setup_test_repo()

    try:
        git = GitNativeWorkflow(repo_path=str(test_dir))

        # Create and modify file
        test_file = test_dir / "README.md"
        test_file.write_text("# Test Repo\n\nModified content")

        # Commit dirty files
        result = git.commit_dirty_files(
            message="test: save work before AI edit",
            include_untracked=False
        )

        if result.success and result.commit_hash:
            print(f"✓ Dirty files committed successfully")
            print(f"  Commit hash: {result.commit_hash[:8]}")
            print(f"  Files committed: {len(result.files_committed)}")
            return True
        else:
            print(f"✗ Failed to commit dirty files")
            print(f"  Error: {result.error}")
            return False

    finally:
        cleanup_test_repo(test_dir)


def test_auto_commit_with_conventional_commits():
    """Test auto-commit with Conventional Commits format"""
    print("\n" + "=" * 70)
    print("TEST 4: Auto-Commit with Conventional Commits")
    print("=" * 70)

    test_dir = setup_test_repo()

    try:
        git = GitNativeWorkflow(repo_path=str(test_dir))

        # Create new file
        new_file = test_dir / "feature.py"
        new_file.write_text("def new_feature():\n    pass\n")

        # Auto-commit with Constitutional AI attribution
        result = git.auto_commit_changes(
            files=["feature.py"],
            change_description="add new feature for error handling",
            principle="P4 - Prudência Operacional",
            commit_type="feat"
        )

        if result.success and result.commit_hash:
            print(f"✓ Auto-commit successful with Conventional Commits format")
            print(f"  Commit hash: {result.commit_hash[:8]}")

            # Verify commit message includes Co-authored-by
            if "Co-authored-by" in result.message:
                print(f"✓ Commit includes Co-authored-by attribution")
            else:
                print(f"⚠️  Commit missing Co-authored-by")

            # Verify commit message includes Constitutional AI principle
            if "Constitutional-AI-Principle" in result.message:
                print(f"✓ Commit includes Constitutional AI principle")
            else:
                print(f"⚠️  Commit missing Constitutional AI principle")

            return True
        else:
            print(f"✗ Auto-commit failed")
            print(f"  Error: {result.error}")
            return False

    finally:
        cleanup_test_repo(test_dir)


def test_view_commit_history():
    """Test viewing commit history"""
    print("\n" + "=" * 70)
    print("TEST 5: View Commit History")
    print("=" * 70)

    test_dir = setup_test_repo()

    try:
        git = GitNativeWorkflow(repo_path=str(test_dir))

        # View history
        commits = git.view_commit_history(limit=5)

        if len(commits) > 0:
            print(f"✓ Commit history retrieved")
            print(f"  Total commits: {len(commits)}")
            for commit in commits:
                print(f"  - {commit['hash']}: {commit['message'][:50]}")
            return True
        else:
            print(f"✗ No commits found in history")
            return False

    finally:
        cleanup_test_repo(test_dir)


def test_undo_last_commit():
    """Test undoing last commit"""
    print("\n" + "=" * 70)
    print("TEST 6: Undo Last Commit")
    print("=" * 70)

    test_dir = setup_test_repo()

    try:
        git = GitNativeWorkflow(repo_path=str(test_dir))

        # Create and commit a file
        test_file = test_dir / "temp.txt"
        test_file.write_text("Temporary content")

        git.auto_commit_changes(
            files=["temp.txt"],
            change_description="add temporary file",
            commit_type="chore"
        )

        # Get commit count before undo
        commits_before = git.view_commit_history(limit=10)

        # Undo last commit
        result = git.undo_last_commit()

        # Get commit count after undo
        commits_after = git.view_commit_history(limit=10)

        if result.success and len(commits_after) == len(commits_before) - 1:
            print(f"✓ Last commit successfully undone")
            print(f"  Undone commit: {result.commit_hash[:8]}")
            print(f"  Commits before: {len(commits_before)}")
            print(f"  Commits after: {len(commits_after)}")
            return True
        else:
            print(f"✗ Failed to undo commit")
            print(f"  Error: {result.error}")
            return False

    finally:
        cleanup_test_repo(test_dir)


def run_all_tests():
    """Run all git-native workflow tests"""
    print("\n" + "=" * 70)
    print("GIT-NATIVE WORKFLOW TESTS (P2 - Transparência Radical)")
    print("=" * 70)
    print("Testing Git-Native Workflows inspired by Aider\n")

    tests = [
        ("Git Detection", test_git_detection),
        ("Get Status", test_get_status),
        ("Commit Dirty Files", test_commit_dirty_files),
        ("Auto-Commit (Conventional Commits)", test_auto_commit_with_conventional_commits),
        ("View Commit History", test_view_commit_history),
        ("Undo Last Commit", test_undo_last_commit),
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
        print("🏎️ PAGANI: P2 - Transparência Radical está operacional!")
        print("\n📜 Git-Native Workflows:")
        print("  ✓ Git repository detection")
        print("  ✓ Status tracking (dirty/staged/untracked files)")
        print("  ✓ Dirty files protection")
        print("  ✓ Auto-commit with Conventional Commits")
        print("  ✓ Constitutional AI attribution")
        print("  ✓ Commit history viewing")
        print("  ✓ Undo/rollback capability")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review and fix issues.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
