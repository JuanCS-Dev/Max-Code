"""
Dynamic Context Collector - Pilar II (Runtime)

Percepção em Tempo Real do Ambiente de Desenvolvimento.

Biblical Foundation:
"Vigiai e orai, para que não entreis em tentação" (Mateus 26:41)
Stay alert to the current state - situational awareness is survival.

Architecture:
- Git state (status, diff, branch)
- Shell feedback (last command, stdout/stderr)
- Running processes (dev servers, tests)
- Environment variables
- Unsaved buffers (editor integration)

Philosophy:
Static context is what the code IS.
Dynamic context is what the code is DOING right now.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import subprocess
import os
import psutil
from datetime import datetime


@dataclass
class GitStatus:
    """
    Structured git status

    Parsed from `git status --porcelain`
    """
    staged: List[str] = field(default_factory=list)
    unstaged: List[str] = field(default_factory=list)
    untracked: List[str] = field(default_factory=list)
    conflicted: List[str] = field(default_factory=list)

    current_branch: Optional[str] = None
    tracking_branch: Optional[str] = None
    ahead: int = 0  # Commits ahead of remote
    behind: int = 0  # Commits behind remote

    is_clean: bool = False
    is_detached: bool = False

    @classmethod
    def parse(cls, status_output: str, branch_output: str = "") -> 'GitStatus':
        """
        Parse git status --porcelain output

        Format:
        XY PATH
        X = staged status, Y = unstaged status
        """
        status = cls()

        for line in status_output.strip().split('\n'):
            if not line:
                continue

            code = line[:2]
            path = line[3:].strip()

            # Staged changes
            if code[0] != ' ' and code[0] != '?':
                status.staged.append(path)

            # Unstaged changes
            if code[1] != ' ' and code[1] != '?':
                status.unstaged.append(path)

            # Untracked
            if code == '??':
                status.untracked.append(path)

            # Conflicted
            if code in ['DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU']:
                status.conflicted.append(path)

        # Parse branch info
        if branch_output:
            status._parse_branch(branch_output)

        status.is_clean = not any([
            status.staged,
            status.unstaged,
            status.untracked,
            status.conflicted
        ])

        return status

    def _parse_branch(self, branch_output: str):
        """Parse git branch -vv output"""
        # Example: "* main 1234567 [origin/main: ahead 2, behind 1] Commit message"
        for line in branch_output.split('\n'):
            if line.startswith('*'):
                parts = line.split()
                if len(parts) >= 2:
                    self.current_branch = parts[1]

                # Check for tracking info
                if '[' in line and ']' in line:
                    tracking_part = line[line.index('[') + 1:line.index(']')]
                    if ':' in tracking_part:
                        self.tracking_branch = tracking_part.split(':')[0].strip()

                        # Parse ahead/behind
                        if 'ahead' in tracking_part:
                            try:
                                self.ahead = int(tracking_part.split('ahead')[1].split(',')[0].strip())
                            except (ValueError, IndexError):
                                pass

                        if 'behind' in tracking_part:
                            try:
                                self.behind = int(tracking_part.split('behind')[1].split(']')[0].strip())
                            except (ValueError, IndexError):
                                pass

                # Check for detached HEAD
                if '(HEAD detached' in line:
                    self.is_detached = True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            'staged': self.staged,
            'unstaged': self.unstaged,
            'untracked': self.untracked,
            'conflicted': self.conflicted,
            'current_branch': self.current_branch,
            'tracking_branch': self.tracking_branch,
            'ahead': self.ahead,
            'behind': self.behind,
            'is_clean': self.is_clean,
            'is_detached': self.is_detached,
        }


@dataclass
class ProcessInfo:
    """Running process information"""
    pid: int
    name: str
    cmdline: str
    cwd: str
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    status: str = "running"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'pid': self.pid,
            'name': self.name,
            'cmdline': self.cmdline,
            'cwd': self.cwd,
            'cpu_percent': self.cpu_percent,
            'memory_mb': self.memory_mb,
            'status': self.status,
        }


@dataclass
class ShellFeedback:
    """Last shell command feedback"""
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    timestamp: datetime

    @property
    def success(self) -> bool:
        return self.exit_code == 0

    @property
    def has_errors(self) -> bool:
        return bool(self.stderr) or self.exit_code != 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'command': self.command,
            'stdout': self.stdout[:1000],  # Truncate
            'stderr': self.stderr[:1000],
            'exit_code': self.exit_code,
            'duration_ms': self.duration_ms,
            'timestamp': self.timestamp.isoformat(),
            'success': self.success,
            'has_errors': self.has_errors,
        }


@dataclass
class DynamicState:
    """
    Complete dynamic state snapshot

    Represents the CURRENT state of the development environment
    """
    # Working directory
    cwd: str

    # Git state
    git_status: Optional[GitStatus] = None
    git_diff_staged: str = ""
    git_diff_unstaged: str = ""
    git_recent_commits: List[Dict[str, str]] = field(default_factory=list)

    # Shell feedback
    last_command: Optional[ShellFeedback] = None

    # Running processes (dev servers, tests, etc.)
    dev_processes: List[ProcessInfo] = field(default_factory=list)

    # Environment
    env_vars: Dict[str, str] = field(default_factory=dict)
    python_version: str = ""
    venv_active: bool = False
    venv_path: Optional[str] = None

    # Timestamp
    collected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            'cwd': self.cwd,
            'git_status': self.git_status.to_dict() if self.git_status else None,
            'git_diff_staged': self.git_diff_staged[:500],  # Truncate
            'git_diff_unstaged': self.git_diff_unstaged[:500],
            'git_recent_commits': self.git_recent_commits[:5],
            'last_command': self.last_command.to_dict() if self.last_command else None,
            'dev_processes': [p.to_dict() for p in self.dev_processes],
            'env_vars': self.env_vars,
            'python_version': self.python_version,
            'venv_active': self.venv_active,
            'venv_path': self.venv_path,
            'collected_at': self.collected_at.isoformat(),
        }


class DynamicContextCollector:
    """
    Pilar II: Dynamic Context (Runtime State)

    Captures ephemeral state that changes during development:
    - What files are modified (git status)
    - What the last command output was (stderr)
    - What processes are running (dev servers)
    - What's the environment (venv, Python version)

    This is CRITICAL for understanding context that static analysis misses.

    Example:
        collector = DynamicContextCollector()
        state = collector.collect()

        if state.last_command and state.last_command.has_errors:
            print(f"Last command failed: {state.last_command.stderr}")
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = Path(project_root or Path.cwd())

    def collect(self) -> DynamicState:
        """
        Collect complete dynamic state

        Fast operation (<100ms typically)
        """
        state = DynamicState(cwd=str(self.project_root))

        # Git state
        state.git_status = self._get_git_status()
        state.git_diff_staged = self._get_git_diff(staged=True)
        state.git_diff_unstaged = self._get_git_diff(staged=False)
        state.git_recent_commits = self._get_recent_commits(n=5)

        # Environment
        state.env_vars = self._get_relevant_env_vars()
        state.python_version = self._get_python_version()
        state.venv_active = self._is_venv_active()
        state.venv_path = os.environ.get('VIRTUAL_ENV')

        # Running processes
        state.dev_processes = self._get_dev_processes()

        return state

    def _get_git_status(self) -> Optional[GitStatus]:
        """Get structured git status"""
        try:
            # Get status
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            # Get branch info
            branch_result = subprocess.run(
                ['git', 'branch', '-vv'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            return GitStatus.parse(
                status_result.stdout,
                branch_result.stdout
            )

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _get_git_diff(self, staged: bool = False) -> str:
        """Get git diff"""
        try:
            cmd = ['git', 'diff']
            if staged:
                cmd.append('--staged')

            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            return result.stdout

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return ""

    def _get_recent_commits(self, n: int = 5) -> List[Dict[str, str]]:
        """Get recent commit history"""
        try:
            result = subprocess.run(
                ['git', 'log', f'-{n}', '--pretty=format:%H|%an|%ae|%s|%ar'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                parts = line.split('|')
                if len(parts) >= 5:
                    commits.append({
                        'hash': parts[0],
                        'author_name': parts[1],
                        'author_email': parts[2],
                        'message': parts[3],
                        'relative_time': parts[4],
                    })

            return commits

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return []

    def _get_relevant_env_vars(self) -> Dict[str, str]:
        """Get relevant environment variables"""
        relevant_vars = [
            'PATH',
            'PYTHONPATH',
            'VIRTUAL_ENV',
            'CONDA_DEFAULT_ENV',
            'SHELL',
            'TERM',
            'EDITOR',
            'HOME',
            'USER',
        ]

        return {
            var: os.environ.get(var, '')
            for var in relevant_vars
            if os.environ.get(var)
        }

    def _get_python_version(self) -> str:
        """Get Python version"""
        try:
            result = subprocess.run(
                ['python3', '--version'],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return "unknown"

    def _is_venv_active(self) -> bool:
        """Check if virtual environment is active"""
        return 'VIRTUAL_ENV' in os.environ or 'CONDA_DEFAULT_ENV' in os.environ

    def _get_dev_processes(self) -> List[ProcessInfo]:
        """
        Get development-related processes

        Looks for:
        - Python processes (pytest, uvicorn, gunicorn)
        - Node processes (npm, yarn, webpack)
        - Docker containers
        - Database servers
        """
        processes = []

        # Keywords indicating dev processes
        dev_keywords = [
            'pytest', 'python', 'uvicorn', 'gunicorn', 'flask', 'django',
            'npm', 'node', 'yarn', 'webpack', 'vite',
            'docker', 'docker-compose',
            'postgres', 'mysql', 'redis', 'mongodb',
            'jupyter', 'notebook',
        ]

        try:
            current_user = psutil.Process().username()

            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd', 'username']):
                try:
                    info = proc.info

                    # Only current user's processes
                    if info.get('username') != current_user:
                        continue

                    # Check if dev-related
                    name = info.get('name', '').lower()
                    cmdline = ' '.join(info.get('cmdline', [])).lower()

                    if any(kw in name or kw in cmdline for kw in dev_keywords):
                        # Get additional info
                        cpu = proc.cpu_percent(interval=0.1)
                        memory = proc.memory_info().rss / 1024 / 1024  # MB

                        processes.append(ProcessInfo(
                            pid=info['pid'],
                            name=info['name'],
                            cmdline=cmdline[:200],  # Truncate
                            cwd=info.get('cwd', ''),
                            cpu_percent=cpu,
                            memory_mb=memory,
                            status=proc.status(),
                        ))

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

        except Exception as e:
            print(f"Error collecting processes: {e}")

        return processes


# Singleton instance
_collector: Optional[DynamicContextCollector] = None


def get_dynamic_collector() -> DynamicContextCollector:
    """Get or create singleton dynamic context collector"""
    global _collector
    if _collector is None:
        _collector = DynamicContextCollector()
    return _collector
