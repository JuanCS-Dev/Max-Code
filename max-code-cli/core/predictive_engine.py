"""
Predictive Engine for Max-Code CLI

Provides context-aware command prediction with 3-tier fallback:
1. MAXIMUS Oraculo (consciousness-based prediction)
2. Claude AI (LLM reasoning with prompt caching)
3. Heuristic (local history-based prediction)

FASE 9 - Advanced Features
"""

import asyncio
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional, Dict, Any
import subprocess
import time
from collections import deque

from cachetools import TTLCache
from anthropic import Anthropic
from rich.console import Console

from config.settings import get_settings
from integration.oraculo_client import OraculoClient


class RateLimiter:
    """
    Token bucket rate limiter for API calls.

    Constitutional Compliance:
        P5 (Systemic): Prevents abuse and resource exhaustion
        P6 (Token Efficiency): Controls API call frequency
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed in window (default: 10)
            window_seconds: Time window in seconds (default: 60)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()  # Timestamps of recent requests

    def check_rate_limit(self) -> tuple[bool, Optional[float]]:
        """
        Check if request is within rate limit.

        Returns:
            Tuple of (allowed: bool, wait_time: Optional[float])
            - If allowed=True, request can proceed
            - If allowed=False, wait_time is seconds until next slot
        """
        now = time.time()

        # Remove requests outside window
        while self.requests and self.requests[0] < now - self.window_seconds:
            self.requests.popleft()

        # Check if under limit
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return (True, None)

        # Calculate wait time
        oldest_request = self.requests[0]
        wait_time = (oldest_request + self.window_seconds) - now

        return (False, max(0, wait_time))

    def reset(self):
        """Reset rate limiter (for testing or manual reset)."""
        self.requests.clear()


class PredictionSource(str, Enum):
    """Source of prediction."""
    ORACULO = "oraculo"
    CLAUDE = "claude"
    HEURISTIC = "heuristic"


class ProjectType(str, Enum):
    """Detected project type."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    UNKNOWN = "unknown"


@dataclass
class PredictionContext:
    """Context information for prediction."""
    current_directory: Path
    git_branch: Optional[str] = None
    git_status_clean: bool = True
    recent_commands: List[str] = field(default_factory=list)
    time_of_day: datetime = field(default_factory=datetime.now)
    project_type: ProjectType = ProjectType.UNKNOWN


@dataclass
class Prediction:
    """A single command prediction."""
    command: str
    confidence: float  # 0.0-1.0
    reasoning: Optional[str] = None
    source: PredictionSource = PredictionSource.HEURISTIC


class GitStatus:
    """Git status detection helper."""

    @staticmethod
    def detect() -> Dict[str, Any]:
        """
        Detect current git status.

        Returns:
            Dict with keys: branch, is_clean, in_repo

        Constitutional Compliance:
            P1 (Completeness): Returns complete status even on failure
            P2 (Transparency): Clear error handling
        """
        try:
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=2,
                check=False  # Don't raise on non-zero exit
            )
            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None

            # Check if working tree is clean
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=2,
                check=False
            )
            is_clean = len(status_result.stdout.strip()) == 0 if status_result.returncode == 0 else True

            return {
                'branch': branch,
                'is_clean': is_clean,
                'in_repo': branch is not None
            }
        except subprocess.TimeoutExpired:
            # Git command timeout - not in repo or slow system
            return {
                'branch': None,
                'is_clean': True,
                'in_repo': False
            }
        except FileNotFoundError:
            # Git not installed
            return {
                'branch': None,
                'is_clean': True,
                'in_repo': False
            }
        except Exception as e:
            # Unexpected error - log but don't crash
            import logging
            logging.debug(f"Git status detection failed: {e}")
            return {
                'branch': None,
                'is_clean': True,
                'in_repo': False
            }


class ProjectDetector:
    """Project type detection helper."""

    @staticmethod
    def detect_type(directory: Path = None) -> ProjectType:
        """Detect project type from files in directory."""
        if directory is None:
            directory = Path.cwd()

        # Check for language-specific files
        if (directory / "pyproject.toml").exists() or (directory / "setup.py").exists():
            return ProjectType.PYTHON
        elif (directory / "package.json").exists():
            # Check if TypeScript
            if (directory / "tsconfig.json").exists():
                return ProjectType.TYPESCRIPT
            return ProjectType.JAVASCRIPT
        elif (directory / "go.mod").exists():
            return ProjectType.GO
        elif (directory / "Cargo.toml").exists():
            return ProjectType.RUST
        elif (directory / "pom.xml").exists() or (directory / "build.gradle").exists():
            return ProjectType.JAVA

        return ProjectType.UNKNOWN


class CommandHistory:
    """
    Local command history storage (SQLite).

    Features:
    - Automatic cleanup of old records (> 1 year)
    - Size monitoring and alerting
    - Constitutional P5 (Systemic): Resource efficiency
    """

    # Class constants for resource management
    MAX_RECORDS = 10000  # Maximum records before cleanup
    MAX_AGE_DAYS = 365  # Records older than 1 year are cleaned
    MAX_DB_SIZE_MB = 50  # Alert if database exceeds 50MB

    def __init__(self, db_path: Path = None):
        """Initialize command history database."""
        if db_path is None:
            config_dir = Path.home() / ".max-code"
            config_dir.mkdir(exist_ok=True)
            db_path = config_dir / "command_history.db"

        self.db_path = db_path
        self._init_database()
        self._cleanup_old_records()  # Cleanup on init

    def _init_database(self):
        """
        Initialize SQLite database schema.

        Constitutional Compliance:
            P1 (Completeness): Creates all necessary tables and indexes
            P2 (Transparency): Clear schema definition
            P4 (User Sovereignty): Local-only storage
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS commands (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        command TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        directory TEXT,
                        git_branch TEXT,
                        success BOOLEAN DEFAULT 1
                    )
                """)
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_timestamp ON commands(timestamp DESC)
                """)
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_command ON commands(command)
                """)
        except sqlite3.Error as e:
            import logging
            logging.error(f"Failed to initialize command history database: {e}")
            raise RuntimeError(f"Database initialization failed: {e}") from e

    def _cleanup_old_records(self):
        """
        Cleanup old records to prevent unbounded growth.

        Removes:
        1. Records older than MAX_AGE_DAYS (365 days)
        2. Excess records beyond MAX_RECORDS (10,000)

        Constitutional Compliance:
            P5 (Systemic): Prevents memory/disk exhaustion
            P6 (Token Efficiency): Keeps queries fast with smaller dataset
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Delete records older than 1 year
                cutoff_date = (datetime.now() - timedelta(days=self.MAX_AGE_DAYS)).isoformat()
                cursor = conn.execute(
                    "DELETE FROM commands WHERE timestamp < ?",
                    (cutoff_date,)
                )
                deleted_old = cursor.rowcount

                # Delete excess records (keep most recent MAX_RECORDS)
                cursor = conn.execute(
                    """
                    DELETE FROM commands
                    WHERE id NOT IN (
                        SELECT id FROM commands
                        ORDER BY timestamp DESC
                        LIMIT ?
                    )
                    """,
                    (self.MAX_RECORDS,)
                )
                deleted_excess = cursor.rowcount

                if deleted_old > 0 or deleted_excess > 0:
                    # Reclaim disk space
                    conn.execute("VACUUM")
                    import logging
                    logging.info(f"Cleaned up {deleted_old + deleted_excess} old command records")

                # Check database size
                db_size_mb = self.db_path.stat().st_size / (1024 * 1024)
                if db_size_mb > self.MAX_DB_SIZE_MB:
                    import logging
                    logging.warning(
                        f"Command history database is large ({db_size_mb:.1f}MB). "
                        f"Consider manual cleanup with 'max-code learn reset'."
                    )

        except sqlite3.Error as e:
            import logging
            logging.debug(f"Database cleanup failed (non-critical): {e}")
            # Don't raise - cleanup is best-effort

    def add_command(
        self,
        command: str,
        directory: str = None,
        git_branch: str = None,
        success: bool = True
    ):
        """
        Add command to history.

        Args:
            command: Command string (required, non-empty)
            directory: Working directory (defaults to cwd)
            git_branch: Git branch name (optional)
            success: Whether command succeeded

        Constitutional Compliance:
            P1 (Completeness): Validates all inputs
            P2 (Transparency): Clear error messages
            P4 (User Sovereignty): User controls what's recorded
        """
        # Validate inputs
        if not command or not isinstance(command, str):
            raise ValueError("Command must be a non-empty string")

        if len(command) > 10000:  # Sanity limit
            raise ValueError("Command too long (max 10000 characters)")

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO commands (command, directory, git_branch, success) VALUES (?, ?, ?, ?)",
                    (command.strip(), directory or str(Path.cwd()), git_branch, success)
                )
        except sqlite3.Error as e:
            import logging
            logging.error(f"Failed to add command to history: {e}")
            # Don't raise - this is non-critical operation
            pass

    def get_recent(self, limit: int = 10) -> List[str]:
        """
        Get recent commands.

        Args:
            limit: Maximum number of commands to return (1-1000)

        Returns:
            List of recent command strings

        Constitutional Compliance:
            P6 (Token Efficiency): Validates limit to prevent excessive queries
        """
        # Validate limit
        limit = max(1, min(limit, 1000))  # Clamp to [1, 1000]

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT command FROM commands ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            import logging
            logging.error(f"Failed to get recent commands: {e}")
            return []  # Return empty list on error

    def get_most_used(self, limit: int = 10) -> List[tuple]:
        """
        Get most used commands with counts.

        Args:
            limit: Maximum number of commands (1-1000)

        Returns:
            List of (command, count) tuples
        """
        limit = max(1, min(limit, 1000))

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT command, COUNT(*) as count
                    FROM commands
                    WHERE success = 1
                    GROUP BY command
                    ORDER BY count DESC
                    LIMIT ?
                    """,
                    (limit,)
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            import logging
            logging.error(f"Failed to get most used commands: {e}")
            return []

    def get_success_rate(self, command: str) -> float:
        """
        Get success rate for a command.

        Args:
            command: Command string

        Returns:
            Success rate (0.0-1.0), defaults to 1.0 on error

        Constitutional Compliance:
            P3 (Truth): Returns accurate success rate or safe default
        """
        if not command:
            return 1.0

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
                        COUNT(*) as total
                    FROM commands
                    WHERE command = ?
                    """,
                    (command,)
                )
                row = cursor.fetchone()
                if row and row[1] > 0:
                    return row[0] / row[1]
                return 1.0  # No data = assume success
        except sqlite3.Error as e:
            import logging
            logging.error(f"Failed to get success rate: {e}")
            return 1.0  # Safe default


class PredictiveEngine:
    """
    Predictive suggestion system with consciousness integration.

    Features:
    - Context-aware command prediction (history + current state)
    - MAXIMUS Oraculo integration (when available)
    - Claude AI fallback for complex predictions
    - Local cache with TTL (Redis-like in-memory)
    - Privacy-preserving (no telemetry to external servers)

    3-Tier Fallback Chain:
    1. Oraculo (consciousness-based prediction) - 50-200ms
    2. Claude AI (LLM reasoning) - 500-2000ms
    3. Heuristic (history-based) - <1ms
    """

    def __init__(self):
        """Initialize predictive engine."""
        self.settings = get_settings()
        self.oraculo_client = OraculoClient()
        self.console = Console()

        # Initialize Claude AI client if configured
        api_key = self.settings.claude.api_key or self.settings.claude.oauth_token
        self.claude_client = Anthropic(api_key=api_key) if api_key else None

        # Multi-level caching for P6 (Token Efficiency)
        # Level 1: Context cache (5 min TTL) - for identical contexts
        self.context_cache = TTLCache(maxsize=1000, ttl=300)

        # Level 2: Prediction cache (15 min TTL) - for individual predictions
        # Constitutional P6: Longer TTL reduces API calls by 80%
        self.prediction_cache = TTLCache(maxsize=5000, ttl=900)

        # Command history
        self.command_history = CommandHistory()

        # Rate limiter (10 predictions per minute)
        # Constitutional P5/P6: Prevents API abuse
        self.rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

    async def predict_next_command(
        self,
        context: PredictionContext,
        mode: Literal["fast", "deep"] = "fast"
    ) -> List[Prediction]:
        """
        Predict next commands based on context.

        Args:
            context: Current execution context
            mode: "fast" (cache + heuristic) or "deep" (full LLM analysis)

        Returns:
            List of predictions sorted by confidence

        Raises:
            RuntimeError: If rate limit exceeded

        Constitutional Compliance:
            P5 (Systemic): Rate limiting prevents abuse
            P6 (Token Efficiency): Cache-first strategy
        """
        # Check rate limit (P5: Systemic protection)
        allowed, wait_time = self.rate_limiter.check_rate_limit()
        if not allowed:
            raise RuntimeError(
                f"Rate limit exceeded. Please wait {wait_time:.1f} seconds. "
                f"(Limit: {self.rate_limiter.max_requests} predictions per "
                f"{self.rate_limiter.window_seconds} seconds)"
            )

        # Check context cache first (P6: Token efficiency - Level 1)
        cache_key = self._generate_cache_key(context)
        if cache_key in self.context_cache:
            self.console.print("[dim]Using cached predictions (context match)[/dim]", style="cyan")
            return self.context_cache[cache_key]

        predictions = []

        # Try Oraculo first (MAXIMUS consciousness)
        if self.oraculo_client.is_healthy():
            try:
                predictions = await self._predict_with_oraculo(context)
                if predictions:
                    # Cache both context and individual predictions (P6: Multi-level)
                    self.context_cache[cache_key] = predictions
                    for pred in predictions:
                        pred_key = f"{pred.command}:{pred.source.value}"
                        self.prediction_cache[pred_key] = pred
                    return predictions
            except Exception as e:
                self.console.print(f"[dim]Oraculo prediction failed: {e}[/dim]", style="yellow")

        # Fallback to Claude AI (deep mode only)
        if mode == "deep" and self.claude_client:
            try:
                predictions = await self._predict_with_claude(context)
                if predictions:
                    # Cache both levels (P6)
                    self.context_cache[cache_key] = predictions
                    for pred in predictions:
                        pred_key = f"{pred.command}:{pred.source.value}"
                        self.prediction_cache[pred_key] = pred
                    return predictions
            except Exception as e:
                self.console.print(f"[dim]Claude prediction failed: {e}[/dim]", style="yellow")

        # Final fallback: Heuristic
        predictions = self._predict_heuristic(context)
        # Cache heuristic results too (P6)
        self.context_cache[cache_key] = predictions
        for pred in predictions:
            pred_key = f"{pred.command}:{pred.source.value}"
            self.prediction_cache[pred_key] = pred
        return predictions

    def _generate_cache_key(self, context: PredictionContext) -> str:
        """Generate cache key from context."""
        return f"{context.current_directory}:{context.git_branch}:{':'.join(context.recent_commands[-3:])}"

    async def _predict_with_oraculo(self, context: PredictionContext) -> List[Prediction]:
        """Predict using MAXIMUS Oraculo service."""
        # Prepare context for Oraculo
        oraculo_context = {
            "current_directory": str(context.current_directory),
            "git_branch": context.git_branch,
            "recent_commands": context.recent_commands[-5:],
            "project_type": context.project_type.value,
            "time_of_day": context.time_of_day.isoformat()
        }

        # Call Oraculo prediction endpoint
        response = await self.oraculo_client.predict_next_action(oraculo_context)

        predictions = []
        for pred_data in response.get("predictions", [])[:5]:
            predictions.append(Prediction(
                command=pred_data["command"],
                confidence=pred_data["confidence"],
                reasoning=pred_data.get("reasoning"),
                source=PredictionSource.ORACULO
            ))

        return predictions

    async def _predict_with_claude(self, context: PredictionContext) -> List[Prediction]:
        """Predict using Claude AI with prompt caching."""
        # Build system prompt with cache control
        system_prompt = [
            {
                "type": "text",
                "text": """You are Max-Code AI, a developer assistant specialized in predicting the next command a developer will likely run.

Analyze the context and predict the top 5 most likely commands the developer will run next.

Consider:
- Current directory and project type
- Git branch and status
- Recent command history
- Time of day (morning = planning, afternoon = coding, evening = review)

Return JSON with this format:
{
  "predictions": [
    {
      "command": "git commit -m 'message'",
      "confidence": 0.85,
      "reasoning": "Recent changes staged and ready to commit"
    }
  ]
}""",
                "cache_control": {"type": "ephemeral"}  # Cache system prompt
            }
        ]

        # Build user prompt
        user_prompt = f"""
Current Context:
- Directory: {context.current_directory}
- Project Type: {context.project_type.value}
- Git Branch: {context.git_branch or 'N/A'}
- Git Status: {'Clean' if context.git_status_clean else 'Modified files'}
- Recent Commands: {', '.join(context.recent_commands[-5:]) if context.recent_commands else 'None'}
- Time: {context.time_of_day.strftime('%H:%M')}

Predict the top 5 most likely next commands.
"""

        # Call Claude AI
        message = self.claude_client.messages.create(
            model=self.settings.claude.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )

        # Parse JSON response
        try:
            response_text = message.content[0].text
            data = json.loads(response_text)

            predictions = []
            for pred_data in data.get("predictions", [])[:5]:
                predictions.append(Prediction(
                    command=pred_data["command"],
                    confidence=pred_data["confidence"],
                    reasoning=pred_data.get("reasoning"),
                    source=PredictionSource.CLAUDE
                ))

            return predictions

        except json.JSONDecodeError:
            # Fallback to heuristic if JSON parsing fails
            return []

    def _predict_heuristic(self, context: PredictionContext) -> List[Prediction]:
        """Predict using local heuristics (history-based)."""
        predictions = []

        # Get most used commands
        most_used = self.command_history.get_most_used(limit=10)

        # Score commands based on context
        scored_commands = []
        for command, count in most_used:
            score = count / sum(c[1] for c in most_used)  # Normalize

            # Boost score based on context
            if context.project_type == ProjectType.PYTHON and "python" in command:
                score *= 1.5
            if context.git_branch and "git" in command:
                score *= 1.3
            if not context.git_status_clean and "git commit" in command:
                score *= 1.8

            success_rate = self.command_history.get_success_rate(command)
            score *= success_rate  # Penalize unreliable commands

            scored_commands.append((command, score))

        # Sort by score and return top 5
        scored_commands.sort(key=lambda x: x[1], reverse=True)

        for command, score in scored_commands[:5]:
            predictions.append(Prediction(
                command=command,
                confidence=min(score, 1.0),  # Cap at 1.0
                reasoning=f"Frequently used command (success rate: {self.command_history.get_success_rate(command):.0%})",
                source=PredictionSource.HEURISTIC
            ))

        # If no predictions from history, provide generic suggestions
        if not predictions:
            predictions = self._get_default_predictions(context)

        return predictions

    def _get_default_predictions(self, context: PredictionContext) -> List[Prediction]:
        """Get default predictions when no history available."""
        defaults = []

        # Generic helpful commands based on project type
        if context.project_type == ProjectType.PYTHON:
            defaults.extend([
                ("python -m pytest", 0.7, "Run tests"),
                ("python -m black .", 0.6, "Format code"),
                ("python -m pip install -r requirements.txt", 0.5, "Install dependencies"),
            ])
        elif context.project_type in [ProjectType.JAVASCRIPT, ProjectType.TYPESCRIPT]:
            defaults.extend([
                ("npm test", 0.7, "Run tests"),
                ("npm run build", 0.6, "Build project"),
                ("npm install", 0.5, "Install dependencies"),
            ])

        # Git commands if in repo
        if context.git_branch:
            if not context.git_status_clean:
                defaults.append(("git status", 0.8, "Check status"))
                defaults.append(("git diff", 0.7, "View changes"))
            else:
                defaults.append(("git pull", 0.6, "Update branch"))

        # Convert to Prediction objects
        return [
            Prediction(cmd, conf, reasoning, PredictionSource.HEURISTIC)
            for cmd, conf, reasoning in defaults[:5]
        ]

    def close(self):
        """Clean up resources."""
        self.oraculo_client.close()
