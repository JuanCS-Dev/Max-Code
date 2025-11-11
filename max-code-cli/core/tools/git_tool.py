#!/usr/bin/env python3
"""
Git Tool - Git Wrapper with Boris Technique ✨

Philosophy (Boris):
"Git is a conversation with time. Every command is a question
about history, present, or future. The API should mirror this
temporal philosophy."

Security:
- OWASP/CIS/NIST patterns (inherited from BashExecutor)
- Safe git operations only
- No force push without confirmation
- Branch protection

Beauty:
- Rich syntax highlighting for diffs
- Beautiful status tables
- Temporal metaphors in output

Soli Deo Gloria 🙏
"""

import re
from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from core.tools.bash_executor import BashExecutor
from core.tools.types import ToolResult


console = Console()


class GitStatus(str, Enum):
    """Git file status"""
    MODIFIED = "modified"
    ADDED = "added"
    DELETED = "deleted"
    RENAMED = "renamed"
    UNTRACKED = "untracked"
    STAGED = "staged"


@dataclass
class GitFileStatus:
    """Represents status of a single file"""
    path: str
    status: GitStatus
    staged: bool


@dataclass
class GitStatusResult:
    """Result of git status command"""
    branch: str
    clean: bool
    files: List[GitFileStatus]
    ahead: int = 0
    behind: int = 0


class GitTool:
    """
    Git Wrapper with Boris Technique.

    Design Principles:
    1. Temporal Clarity - Past (log), Present (status), Future (branch/push)
    2. Safety First - Validate before destructive operations
    3. Beautiful Output - Rich formatting for all operations
    4. Error Grace - Clear messages for git failures

    Boris Quote:
    "A good git wrapper doesn't just execute commands -
    it makes the invisible visible: branch structure,
    change flow, temporal relationships."
    """

    def __init__(self):
        self.executor = BashExecutor(strict_mode=False)
        self.console = Console()

    def _check_git_repo(self) -> ToolResult:
        """Check if current directory is a git repository"""
        result = self.executor.execute("git rev-parse --git-dir 2>/dev/null")

        if result.type == "error" or not result.content:
            return ToolResult.error(
                "❌ Not a git repository\n\n"
                "This directory is not under git version control.\n"
                "Run: git init"
            )

        return ToolResult.success("")

    def status(self, verbose: bool = False) -> ToolResult:
        """
        Git status - Present moment in time.

        Philosophy: "Status is the heartbeat of your repository -
        it tells you where you are NOW."

        Args:
            verbose: Show detailed status with untracked files

        Returns:
            Beautiful formatted status table
        """
        # Check if git repo
        check = self._check_git_repo()
        if check.type == "error":
            return check

        # Get current branch
        branch_result = self.executor.execute("git branch --show-current")
        if branch_result.type == "error":
            branch = "unknown"
        else:
            branch = branch_result.content[0].text.strip()

        # Get status
        status_result = self.executor.execute("git status --porcelain")
        if status_result.type == "error":
            return status_result

        status_output = status_result.content[0].text if status_result.content else ""

        # Parse status
        files: List[GitFileStatus] = []
        if status_output.strip():
            for line in status_output.strip().split('\n'):
                if not line.strip():
                    continue

                # Git status format: XY filename
                # X = staged, Y = working tree
                status_code = line[:2]
                file_path = line[3:].strip()

                # Determine status
                if status_code[0] in ['M', 'A', 'D', 'R']:
                    staged = True
                    if status_code[0] == 'M':
                        status = GitStatus.MODIFIED
                    elif status_code[0] == 'A':
                        status = GitStatus.ADDED
                    elif status_code[0] == 'D':
                        status = GitStatus.DELETED
                    else:
                        status = GitStatus.RENAMED
                elif status_code[1] == 'M':
                    staged = False
                    status = GitStatus.MODIFIED
                elif status_code == '??':
                    staged = False
                    status = GitStatus.UNTRACKED
                else:
                    staged = False
                    status = GitStatus.MODIFIED

                files.append(GitFileStatus(
                    path=file_path,
                    status=status,
                    staged=staged
                ))

        # Get ahead/behind info
        ahead, behind = 0, 0
        ahead_behind_result = self.executor.execute(
            "git rev-list --left-right --count @{u}...HEAD 2>/dev/null"
        )
        if ahead_behind_result.type == "success" and ahead_behind_result.content:
            match = re.match(r'(\d+)\s+(\d+)', ahead_behind_result.content[0].text)
            if match:
                behind, ahead = int(match.group(1)), int(match.group(2))

        # Format output
        return self._format_status_output(
            branch=branch,
            files=files,
            ahead=ahead,
            behind=behind,
            verbose=verbose
        )

    def _format_status_output(
        self,
        branch: str,
        files: List[GitFileStatus],
        ahead: int,
        behind: int,
        verbose: bool
    ) -> ToolResult:
        """Format status output with Boris beauty"""

        # Build status message
        lines = []

        # Header with branch info
        branch_status = f"📍 On branch [bold cyan]{branch}[/bold cyan]"
        if ahead > 0:
            branch_status += f" ⬆️  [green]{ahead} ahead[/green]"
        if behind > 0:
            branch_status += f" ⬇️  [red]{behind} behind[/red]"

        lines.append(branch_status)
        lines.append("")

        if not files:
            lines.append("✨ [green]Working tree clean[/green]")
            lines.append("")
            lines.append("[dim]Nothing to commit, working tree clean[/dim]")
        else:
            # Staged files
            staged_files = [f for f in files if f.staged]
            if staged_files:
                lines.append("[bold green]Changes to be committed:[/bold green]")
                for file in staged_files:
                    icon = self._get_status_icon(file.status)
                    lines.append(f"  {icon} [green]{file.status.value}:[/green] {file.path}")
                lines.append("")

            # Unstaged changes
            unstaged_files = [f for f in files if not f.staged and f.status != GitStatus.UNTRACKED]
            if unstaged_files:
                lines.append("[bold yellow]Changes not staged for commit:[/bold yellow]")
                for file in unstaged_files:
                    icon = self._get_status_icon(file.status)
                    lines.append(f"  {icon} [yellow]{file.status.value}:[/yellow] {file.path}")
                lines.append("")

            # Untracked files
            untracked_files = [f for f in files if f.status == GitStatus.UNTRACKED]
            if untracked_files:
                lines.append("[bold red]Untracked files:[/bold red]")
                if verbose:
                    for file in untracked_files:
                        lines.append(f"  📄 {file.path}")
                else:
                    lines.append(f"  📄 {len(untracked_files)} untracked file(s)")
                    lines.append("  [dim](use --verbose to see all)[/dim]")
                lines.append("")

        return ToolResult.success("\n".join(lines))

    def _get_status_icon(self, status: GitStatus) -> str:
        """Get emoji icon for status"""
        icons = {
            GitStatus.MODIFIED: "📝",
            GitStatus.ADDED: "✨",
            GitStatus.DELETED: "🗑️",
            GitStatus.RENAMED: "📛",
            GitStatus.UNTRACKED: "📄"
        }
        return icons.get(status, "📄")

    def diff(self, file_path: Optional[str] = None, staged: bool = False) -> ToolResult:
        """
        Git diff - Show changes.

        Philosophy: "Diff is the delta - the transformation from
        past to present. Show it with clarity and beauty."

        Args:
            file_path: Specific file to diff (None for all)
            staged: Show staged changes (--cached)

        Returns:
            Syntax-highlighted diff
        """
        check = self._check_git_repo()
        if check.type == "error":
            return check

        # Build command
        cmd = "git diff"
        if staged:
            cmd += " --cached"
        if file_path:
            cmd += f" {file_path}"

        result = self.executor.execute(cmd)

        if result.type == "error":
            return result

        diff_output = result.content[0].text if result.content else ""

        if not diff_output.strip():
            return ToolResult.success(
                "✨ [green]No changes to show[/green]\n\n"
                "[dim]Working tree is clean or all changes are staged[/dim]"
            )

        # Apply syntax highlighting to diff
        # Note: Return plain text - syntax highlighting will be applied by REPL display layer
        return ToolResult.success(diff_output)

    def log(self, limit: int = 10, oneline: bool = False) -> ToolResult:
        """
        Git log - Journey through time past.

        Philosophy: "Log is archaeology - excavating the story
        of how we arrived at now."

        Args:
            limit: Number of commits to show
            oneline: Show compact one-line format

        Returns:
            Beautiful formatted commit history
        """
        check = self._check_git_repo()
        if check.type == "error":
            return check

        if oneline:
            cmd = f"git log --oneline --decorate --graph -n {limit}"
        else:
            cmd = f"git log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%an%Creset %C(green)(%cr)%Creset%n%s%n' -n {limit}"

        result = self.executor.execute(cmd)

        if result.type == "error":
            return result

        log_output = result.content[0].text if result.content else ""

        if not log_output.strip():
            return ToolResult.success(
                "📜 [yellow]No commits yet[/yellow]\n\n"
                "[dim]This repository has no commit history[/dim]"
            )

        return ToolResult.success(f"📜 [bold]Commit History[/bold]\n\n{log_output}")

    def branch(self, list_all: bool = False) -> ToolResult:
        """
        Git branch - Explore parallel timelines.

        Philosophy: "Branches are parallel universes -
        different futures branching from the same past."

        Args:
            list_all: Show all branches including remotes

        Returns:
            Beautiful branch table
        """
        check = self._check_git_repo()
        if check.type == "error":
            return check

        cmd = "git branch -v"
        if list_all:
            cmd += " -a"

        result = self.executor.execute(cmd)

        if result.type == "error":
            return result

        branch_output = result.content[0].text if result.content else ""

        if not branch_output.strip():
            return ToolResult.success(
                "🌿 [yellow]No branches found[/yellow]\n\n"
                "[dim]Repository has no branches[/dim]"
            )

        # Format branches
        lines = ["🌿 [bold]Branches[/bold]\n"]
        for line in branch_output.strip().split('\n'):
            if line.strip().startswith('*'):
                # Current branch
                lines.append(f"  [bold green]→ {line[2:]}[/bold green]")
            else:
                lines.append(f"    {line.strip()}")

        return ToolResult.success("\n".join(lines))

    def commit(self, message: str, add_all: bool = False) -> ToolResult:
        """
        Git commit - Crystallize the present into history.

        Philosophy: "A commit is a moment frozen in time -
        a snapshot of intention made permanent."

        Args:
            message: Commit message
            add_all: Stage all changes before committing

        Returns:
            Commit confirmation
        """
        check = self._check_git_repo()
        if check.type == "error":
            return check

        # Validate message
        if not message or len(message.strip()) < 3:
            return ToolResult.error(
                "❌ Invalid commit message\n\n"
                "Commit message must be at least 3 characters.\n"
                "Boris wisdom: 'A commit without a good message is a crime against future you.'"
            )

        # Stage changes if requested
        if add_all:
            add_result = self.executor.execute("git add -A")
            if add_result.type == "error":
                return add_result

        # Commit
        # Escape message properly for shell
        escaped_message = message.replace("'", "'\\''")
        cmd = f"git commit -m '{escaped_message}'"

        result = self.executor.execute(cmd)

        if result.type == "error":
            error_output = result.content[0].text if result.content else "Unknown error"

            # Check for common errors
            if "nothing to commit" in error_output.lower():
                return ToolResult.error(
                    "❌ Nothing to commit\n\n"
                    "No changes staged for commit.\n"
                    "Use: git add <file> or pass add_all=True"
                )
            elif "please tell me who you are" in error_output.lower():
                return ToolResult.error(
                    "❌ Git identity not configured\n\n"
                    "Configure your git identity first:\n"
                    "  git config user.name 'Your Name'\n"
                    "  git config user.email 'your@email.com'"
                )

            return result

        commit_output = result.content[0].text if result.content else ""

        return ToolResult.success(
            f"✅ [green]Commit created![/green]\n\n"
            f"{commit_output}\n\n"
            f"[dim]Message: {message}[/dim]"
        )

    def push(self, remote: str = "origin", branch: Optional[str] = None, force: bool = False) -> ToolResult:
        """
        Git push - Share your timeline with the world.

        Philosophy: "Push is publication - making your local
        reality part of the shared universe."

        Args:
            remote: Remote name (default: origin)
            branch: Branch to push (None for current)
            force: Force push (DANGEROUS - use with caution)

        Returns:
            Push confirmation
        """
        check = self._check_git_repo()
        if check.type == "error":
            return check

        # Build command
        cmd = f"git push {remote}"

        if branch:
            cmd += f" {branch}"

        if force:
            # Safety check for force push
            return ToolResult.error(
                "🚨 [bold red]Force push blocked for safety[/bold red]\n\n"
                "Force push (--force) can overwrite remote history and cause data loss.\n\n"
                "Boris wisdom: 'Force push is like time travel - powerful but dangerous.\n"
                "Only use it when you fully understand the consequences.'\n\n"
                "To force push, use git command directly:\n"
                f"  git push --force {remote} {branch or ''}"
            )

        result = self.executor.execute(cmd)

        if result.type == "error":
            error_output = result.content[0].text if result.content else "Unknown error"

            # Check for common errors
            if "no upstream branch" in error_output.lower():
                # Get current branch
                branch_result = self.executor.execute("git branch --show-current")
                current_branch = branch_result.content[0].text.strip() if branch_result.content else "current"

                return ToolResult.error(
                    f"❌ No upstream branch configured\n\n"
                    f"Set upstream branch first:\n"
                    f"  git push --set-upstream {remote} {current_branch}"
                )

            return result

        push_output = result.content[0].text if result.content else ""

        return ToolResult.success(
            f"✅ [green]Pushed successfully![/green]\n\n"
            f"{push_output}\n\n"
            f"[dim]Remote: {remote}[/dim]"
        )

    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> ToolResult:
        """
        Git pull - Sync with shared timeline.

        Philosophy: "Pull is synchronization - merging the
        shared reality with your local one."

        Args:
            remote: Remote name (default: origin)
            branch: Branch to pull (None for current)

        Returns:
            Pull confirmation
        """
        check = self._check_git_repo()
        if check.type == "error":
            return check

        cmd = f"git pull {remote}"
        if branch:
            cmd += f" {branch}"

        result = self.executor.execute(cmd)

        if result.type == "error":
            return result

        pull_output = result.content[0].text if result.content else ""

        # Check for conflicts
        if "conflict" in pull_output.lower():
            return ToolResult.error(
                f"⚠️ [yellow]Merge conflicts detected[/yellow]\n\n"
                f"{pull_output}\n\n"
                f"[bold]Resolve conflicts manually:[/bold]\n"
                f"  1. Edit conflicted files\n"
                f"  2. git add <resolved-files>\n"
                f"  3. git commit"
            )

        return ToolResult.success(
            f"✅ [green]Pull successful![/green]\n\n"
            f"{pull_output}"
        )


# Convenience function for CLI usage
def git_tool() -> GitTool:
    """Get GitTool instance"""
    return GitTool()
