"""
Git-Native Workflows - P2: Transparência Radical

Biblical Foundation:
"Nada há encoberto que não haja de ser revelado;
 nem oculto que não haja de ser conhecido." (Lucas 12:2)

Transparency through git - every change is tracked.

CONCEITO:
Inspired by Aider's git-native workflow, but enhanced with Constitutional AI principles.
Every code change lands as a git commit with descriptive messages, enabling:
- Complete auditability (P2 - Transparência Radical)
- Easy rollback (P5 - Autocorreção Humilde)
- Clear attribution (P4 - Rastreabilidade)
- Atomic history for code review

PROCESSO:
1. PROTECT: Commit dirty files before editing (protect user work)
2. EDIT: Make AI-assisted changes
3. COMMIT: Auto-commit with AI-generated message
4. ATTRIBUTE: Mark as AI-assisted with Constitutional AI principles

BENEFÍCIOS:
- Every change is a git operation
- Descriptive commit messages (Conventional Commits)
- Easy undo (git revert)
- Clear attribution (Co-authored-by)
- Aligns with P2 - Transparência Radical

Inspired by Aider (https://aider.chat/docs/git.html)
Enhanced with Constitutional AI governance.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import subprocess
import os
from datetime import datetime


@dataclass
class GitStatus:
    """Status do repositório git"""
    is_repo: bool
    branch: str
    dirty_files: List[str]
    staged_files: List[str]
    untracked_files: List[str]
    has_changes: bool


@dataclass
class CommitResult:
    """Resultado de um commit"""
    success: bool
    commit_hash: Optional[str] = None
    message: Optional[str] = None
    files_committed: List[str] = None
    error: Optional[str] = None


class GitNativeWorkflow:
    """
    Git-Native Workflow Engine

    Implementa P2 - Transparência Radical através de git-native workflows.
    Inspirado no Aider, mas com Constitutional AI governance.

    Features:
    - Auto-commit após cada edição
    - AI-generated commit messages (Conventional Commits)
    - Dirty files protection
    - Constitutional AI attribution
    - Co-authored-by metadata

    Example:
        >>> git = GitNativeWorkflow(repo_path="/path/to/repo")
        >>> status = git.get_status()
        >>> if status.dirty_files:
        ...     git.commit_dirty_files("Protecting user work before AI edit")
        >>> # Make AI edit...
        >>> git.auto_commit_changes(
        ...     files=["src/main.py"],
        ...     change_description="Added error handling",
        ...     principle="P4 - Prudência Operacional"
        ... )
    """

    def __init__(self, repo_path: Optional[str] = None):
        """
        Inicializa Git-Native Workflow

        Args:
            repo_path: Caminho do repositório (None = current dir)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.author_name = "Max-Code CLI"
        self.author_email = "max-code@constitutional-ai.dev"

        # Verifica se é um repositório git
        self.is_git_repo = self._check_git_repo()

    def _check_git_repo(self) -> bool:
        """Verifica se o diretório é um repositório git"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_status(self) -> GitStatus:
        """
        Obtém status do repositório git

        Returns:
            GitStatus com informações do repositório
        """
        if not self.is_git_repo:
            return GitStatus(
                is_repo=False,
                branch="",
                dirty_files=[],
                staged_files=[],
                untracked_files=[],
                has_changes=False
            )

        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            branch = branch_result.stdout.strip()

            # Get status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )

            dirty_files = []
            staged_files = []
            untracked_files = []

            for line in status_result.stdout.splitlines():
                if len(line) < 4:
                    continue

                status_code = line[:2]
                filepath = line[3:]

                if status_code == "??":
                    untracked_files.append(filepath)
                elif status_code[0] != " ":
                    staged_files.append(filepath)
                else:
                    dirty_files.append(filepath)

            has_changes = bool(dirty_files or staged_files or untracked_files)

            return GitStatus(
                is_repo=True,
                branch=branch,
                dirty_files=dirty_files,
                staged_files=staged_files,
                untracked_files=untracked_files,
                has_changes=has_changes
            )

        except Exception as e:
            print(f"⚠️  Error getting git status: {e}")
            return GitStatus(
                is_repo=True,
                branch="unknown",
                dirty_files=[],
                staged_files=[],
                untracked_files=[],
                has_changes=False
            )

    def commit_dirty_files(
        self,
        message: Optional[str] = None,
        include_untracked: bool = False
    ) -> CommitResult:
        """
        Commit dirty files (proteção antes de AI edit)

        Args:
            message: Commit message (None = auto-generate)
            include_untracked: Se True, inclui arquivos untracked

        Returns:
            CommitResult com resultado do commit
        """
        if not self.is_git_repo:
            return CommitResult(
                success=False,
                error="Not a git repository"
            )

        status = self.get_status()

        if not status.has_changes:
            return CommitResult(
                success=True,
                message="No changes to commit",
                files_committed=[]
            )

        try:
            # Add dirty files
            files_to_add = status.dirty_files + (status.untracked_files if include_untracked else [])

            if not files_to_add:
                return CommitResult(
                    success=True,
                    message="No files to commit",
                    files_committed=[]
                )

            for filepath in files_to_add:
                subprocess.run(
                    ["git", "add", filepath],
                    cwd=self.repo_path,
                    check=True,
                    timeout=10
                )

            # Generate commit message if not provided
            if not message:
                message = "chore: save work before AI-assisted edit\n\nProtecting user changes before Max-Code CLI edit."

            # Create commit
            commit_message = f"{message}\n\nCo-authored-by: Max-Code CLI <max-code@constitutional-ai.dev>"

            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_path,
                check=True,
                timeout=10
            )

            # Get commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            commit_hash = hash_result.stdout.strip()

            print(f"✓ Committed {len(files_to_add)} file(s) to protect user work")
            print(f"  Commit: {commit_hash[:8]}")

            return CommitResult(
                success=True,
                commit_hash=commit_hash,
                message=message,
                files_committed=files_to_add
            )

        except subprocess.CalledProcessError as e:
            return CommitResult(
                success=False,
                error=f"Git commit failed: {e}"
            )

    def auto_commit_changes(
        self,
        files: List[str],
        change_description: str,
        principle: Optional[str] = None,
        commit_type: str = "feat"
    ) -> CommitResult:
        """
        Auto-commit AI-assisted changes com Conventional Commits

        Args:
            files: Lista de arquivos modificados
            change_description: Descrição da mudança
            principle: Princípio Constitutional AI aplicado (ex: "P5 - Autocorreção Humilde")
            commit_type: Tipo do commit (feat, fix, refactor, etc)

        Returns:
            CommitResult com resultado do commit

        Commit Message Format (Conventional Commits):
            <type>: <description>

            <body>

            Co-authored-by: Max-Code CLI <max-code@constitutional-ai.dev>
            Constitutional-AI-Principle: <principle>
        """
        if not self.is_git_repo:
            return CommitResult(
                success=False,
                error="Not a git repository"
            )

        try:
            # Add files
            for filepath in files:
                subprocess.run(
                    ["git", "add", filepath],
                    cwd=self.repo_path,
                    check=True,
                    timeout=10
                )

            # Generate commit message (Conventional Commits format)
            commit_title = f"{commit_type}: {change_description}"

            body_lines = [
                "",
                f"AI-assisted change by Max-Code CLI.",
            ]

            if principle:
                body_lines.append(f"Guided by {principle}.")

            body_lines.extend([
                "",
                "🤖 Generated with Max-Code CLI (Constitutional AI)",
                "",
                "Co-authored-by: Max-Code CLI <max-code@constitutional-ai.dev>"
            ])

            if principle:
                body_lines.append(f"Constitutional-AI-Principle: {principle}")

            commit_message = commit_title + "\n" + "\n".join(body_lines)

            # Create commit
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_path,
                check=True,
                timeout=10
            )

            # Get commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            commit_hash = hash_result.stdout.strip()

            print(f"\n✓ Auto-committed AI-assisted changes (P2 - Transparência Radical)")
            print(f"  Commit: {commit_hash[:8]}")
            print(f"  Type: {commit_type}")
            print(f"  Files: {', '.join(files)}")
            if principle:
                print(f"  Principle: {principle}")

            return CommitResult(
                success=True,
                commit_hash=commit_hash,
                message=commit_message,
                files_committed=files
            )

        except subprocess.CalledProcessError as e:
            return CommitResult(
                success=False,
                error=f"Git commit failed: {e}"
            )

    def generate_commit_message_from_diff(
        self,
        files: List[str]
    ) -> str:
        """
        Gera commit message analisando diff

        Args:
            files: Arquivos modificados

        Returns:
            Commit message sugerido

        Note:
            Por enquanto usa heurística simples.
            Futuramente, pode usar LLM para analisar diff.
        """
        if not files:
            return "chore: update files"

        # Heurística simples baseada em arquivos
        if any("test" in f.lower() for f in files):
            return "test: update tests"
        elif any(".md" in f.lower() for f in files):
            return "docs: update documentation"
        elif any("fix" in f.lower() or "bug" in f.lower() for f in files):
            return "fix: resolve issues"
        elif any("refactor" in f.lower() for f in files):
            return "refactor: improve code structure"
        else:
            return "feat: add new functionality"

    def undo_last_commit(self) -> CommitResult:
        """
        Desfaz último commit (mantém mudanças em working directory)

        Returns:
            CommitResult indicando sucesso

        Note:
            Usa git reset --soft HEAD~1 para preservar mudanças
        """
        if not self.is_git_repo:
            return CommitResult(
                success=False,
                error="Not a git repository"
            )

        try:
            # Get commit hash before undoing
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            commit_hash = hash_result.stdout.strip()

            # Undo commit (soft reset - keeps changes)
            subprocess.run(
                ["git", "reset", "--soft", "HEAD~1"],
                cwd=self.repo_path,
                check=True,
                timeout=10
            )

            print(f"✓ Undid last commit: {commit_hash[:8]}")
            print(f"  Changes preserved in working directory")

            return CommitResult(
                success=True,
                commit_hash=commit_hash,
                message="Commit undone"
            )

        except subprocess.CalledProcessError as e:
            return CommitResult(
                success=False,
                error=f"Git reset failed: {e}"
            )

    def view_commit_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Visualiza histórico de commits

        Args:
            limit: Número de commits para mostrar

        Returns:
            Lista de dicts com informações dos commits
        """
        if not self.is_git_repo:
            return []

        try:
            result = subprocess.run(
                ["git", "log", f"-{limit}", "--pretty=format:%H|%s|%an|%ar"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )

            commits = []
            for line in result.stdout.splitlines():
                parts = line.split("|", 3)
                if len(parts) == 4:
                    commits.append({
                        "hash": parts[0][:8],
                        "message": parts[1],
                        "author": parts[2],
                        "time": parts[3]
                    })

            return commits

        except subprocess.CalledProcessError:
            return []


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_git_workflow(repo_path: Optional[str] = None) -> GitNativeWorkflow:
    """
    Cria instância de Git-Native Workflow

    Args:
        repo_path: Caminho do repositório (None = current dir)

    Returns:
        GitNativeWorkflow configurado

    Example:
        >>> git = create_git_workflow()
        >>> status = git.get_status()
    """
    return GitNativeWorkflow(repo_path=repo_path)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("📜 Git-Native Workflow Demo\n")
    print("=" * 70)
    print("P2 - Transparência Radical in action!")
    print("=" * 70)

    git = GitNativeWorkflow()

    # Test 1: Check git status
    print("\nTEST 1: Get Git Status")
    print("-" * 70)

    status = git.get_status()

    if status.is_repo:
        print(f"✓ Git repository detected")
        print(f"  Branch: {status.branch}")
        print(f"  Dirty files: {len(status.dirty_files)}")
        print(f"  Staged files: {len(status.staged_files)}")
        print(f"  Untracked files: {len(status.untracked_files)}")
        print(f"  Has changes: {status.has_changes}")
    else:
        print(f"⚠️  Not a git repository")

    # Test 2: View commit history
    print("\nTEST 2: View Commit History")
    print("-" * 70)

    commits = git.view_commit_history(limit=5)

    if commits:
        print(f"✓ Found {len(commits)} recent commits:")
        for commit in commits:
            print(f"  {commit['hash']}: {commit['message']}")
            print(f"    by {commit['author']}, {commit['time']}")
    else:
        print(f"⚠️  No commits found")

    print("\n" + "=" * 70)
    print("✅ Git-Native Workflow Demo Complete!")
    print("🏎️ PAGANI: P2 - Transparência Radical implementado!")
