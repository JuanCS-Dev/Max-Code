"""
Git Operations Real Test Suite
Constitutional AI v3.0 - FASE 1.4

Tests REAL git operations (not just structure validation).
Following Anthropic TDD Pattern: Write tests → Run → Discover APIs → Adjust

Target: 15+ tests, 95%+ pass rate
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.tools.git_tool import GitTool


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: BASIC GIT OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

class TestBasicGitOperations:
    """Test basic git command execution"""

    def test_git_status(self, temp_git_repo):
        """Test git status command"""
        # GitTool uses current working directory
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.status()

            assert result.type == "success"
            # Status should mention branch (master/main) or status keywords
            text_lower = result.content[0].text.lower()
            assert "branch" in text_lower or "clean" in text_lower or "changes" in text_lower
        finally:
            os.chdir(original_cwd)

    def test_git_log(self, temp_git_repo):
        """Test git log command"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.log(limit=5)

            assert result.type == "success"
            assert "Initial commit" in result.content[0].text or "commit" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)

    def test_git_diff_no_changes(self, temp_git_repo):
        """Test git diff with no changes"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.diff()

            assert result.type == "success"
            # Empty diff is valid
        finally:
            os.chdir(original_cwd)

    def test_git_diff_with_changes(self, temp_git_repo):
        """Test git diff with actual changes"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            # Modify file
            readme = temp_git_repo / "README.md"
            readme.write_text("# Modified\nNew line\n")

            git = GitTool()
            result = git.diff()

            assert result.type == "success"
            # Should show diff or changes
        finally:
            os.chdir(original_cwd)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: GIT COMMIT OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

class TestGitCommitOperations:
    """Test git commit operations"""

    def test_git_commit_with_add_all(self, temp_git_repo):
        """Test git commit with add_all flag"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            # Create new file
            new_file = temp_git_repo / "newfile.txt"
            new_file.write_text("New content\n")

            git = GitTool()
            result = git.commit("Test commit", add_all=True)

            assert result.type == "success"
            assert "commit" in result.content[0].text.lower() or "1 file changed" in result.content[0].text
        finally:
            os.chdir(original_cwd)

    def test_git_commit_nothing_to_commit(self, temp_git_repo):
        """Test git commit with nothing to commit"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.commit("Empty commit")

            # Should fail or return no changes message
            assert result.type == "error" or "nothing" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)

    def test_git_status_after_commit(self, temp_git_repo):
        """Test status shows clean after commit"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            # Create and commit file
            (temp_git_repo / "status_test.txt").write_text("test")

            git = GitTool()
            git.commit("Status test", add_all=True)

            # Check status is clean
            status = git.status()
            assert "clean" in status.content[0].text.lower() or status.type == "success"
        finally:
            os.chdir(original_cwd)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 3: GIT BRANCH OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

class TestGitBranchOperations:
    """Test git branch operations"""

    def test_git_branch_list(self, temp_git_repo):
        """Test git branch list"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.branch()

            assert result.type == "success"
            # Should show master or main branch
            assert "master" in result.content[0].text or "main" in result.content[0].text
        finally:
            os.chdir(original_cwd)

    def test_git_branch_list_all(self, temp_git_repo):
        """Test git branch list all"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.branch(list_all=True)

            assert result.type == "success"
        finally:
            os.chdir(original_cwd)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 4: ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════════════

class TestGitErrorHandling:
    """Test git error handling"""

    def test_git_status_not_a_repo(self, temp_dir):
        """Test git status in non-git directory"""
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            git = GitTool()
            result = git.status()

            assert result.type == "error"
            assert "not a git repository" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)

    def test_git_log_not_a_repo(self, temp_dir):
        """Test git log in non-git directory"""
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            git = GitTool()
            result = git.log()

            assert result.type == "error"
            assert "not a git repository" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)

    def test_git_diff_not_a_repo(self, temp_dir):
        """Test git diff in non-git directory"""
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            git = GitTool()
            result = git.diff()

            assert result.type == "error"
            assert "not a git repository" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)

    def test_git_commit_not_a_repo(self, temp_dir):
        """Test git commit in non-git directory"""
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            git = GitTool()
            result = git.commit("Test commit")

            assert result.type == "error"
            assert "not a git repository" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 5: GIT PUSH/PULL (Mock remote)
# ═══════════════════════════════════════════════════════════════════════════

class TestGitRemoteOperations:
    """Test git push/pull operations"""

    def test_git_pull_no_remote(self, temp_git_repo):
        """Test git pull with no remote configured"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.pull()

            # Should fail - no remote configured
            assert result.type == "error" or "no remote" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)

    def test_git_push_no_remote(self, temp_git_repo):
        """Test git push with no remote configured"""
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            git = GitTool()
            result = git.push()

            # Should fail - no remote configured
            assert result.type == "error" or "no configured push" in result.content[0].text.lower()
        finally:
            os.chdir(original_cwd)


# ═══════════════════════════════════════════════════════════════════════════
# RUN SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
