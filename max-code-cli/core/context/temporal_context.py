"""
Temporal Context Collector - Pilar III (Session Memory)

Memória da Sessão Atual e Histórico Conversacional.

Biblical Foundation:
"Lembra-te dos dias da antiguidade, atenta para os anos de geração em geração"
(Deuteronômio 32:7) - Learn from history, remember patterns.

Architecture:
- Message buffer (recent history)
- Recursive summarization (old messages → summary)
- Task tracking (objective, attempts, progress)
- Frustration detection (user emotional state)
- Success patterns (what worked before)

Philosophy:
Without memory, every conversation is a fresh start.
With memory, we learn from mistakes and build continuity.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json

from .types import Message, MessageRole


@dataclass
class TaskState:
    """Current task tracking"""
    objective: str
    started_at: datetime
    attempt_count: int = 0
    sub_tasks: List[str] = field(default_factory=list)
    completed_sub_tasks: List[str] = field(default_factory=list)
    blocked_on: Optional[str] = None

    @property
    def progress(self) -> float:
        """Progress percentage (0.0 to 1.0)"""
        if not self.sub_tasks:
            return 0.0
        return len(self.completed_sub_tasks) / len(self.sub_tasks)

    @property
    def is_blocked(self) -> bool:
        return self.blocked_on is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'objective': self.objective,
            'started_at': self.started_at.isoformat(),
            'attempt_count': self.attempt_count,
            'sub_tasks': self.sub_tasks,
            'completed_sub_tasks': self.completed_sub_tasks,
            'blocked_on': self.blocked_on,
            'progress': self.progress,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskState':
        """Deserialize from dict"""
        data = data.copy()
        data['started_at'] = datetime.fromisoformat(data['started_at'])
        return cls(**data)


@dataclass
class SessionSummary:
    """Recursive summary of older messages"""
    summary_text: str
    covers_messages: int
    summarized_at: datetime
    oldest_message_time: datetime
    newest_message_time: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            'summary_text': self.summary_text,
            'covers_messages': self.covers_messages,
            'summarized_at': self.summarized_at.isoformat(),
            'oldest_message_time': self.oldest_message_time.isoformat(),
            'newest_message_time': self.newest_message_time.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionSummary':
        """Deserialize from dict"""
        data = data.copy()
        data['summarized_at'] = datetime.fromisoformat(data['summarized_at'])
        data['oldest_message_time'] = datetime.fromisoformat(data['oldest_message_time'])
        data['newest_message_time'] = datetime.fromisoformat(data['newest_message_time'])
        return cls(**data)


@dataclass
class TemporalState:
    """
    Complete temporal state

    Represents memory of the conversation session
    """
    # Active memory (recent messages)
    message_buffer: List[Message] = field(default_factory=list)

    # Compressed memory (old messages → summary)
    summaries: List[SessionSummary] = field(default_factory=list)

    # Task tracking
    current_task: Optional[TaskState] = None
    completed_tasks: List[TaskState] = field(default_factory=list)

    # User state detection
    user_frustrated: bool = False
    frustration_signals: List[str] = field(default_factory=list)

    # Success tracking
    last_success_timestamp: Optional[datetime] = None
    consecutive_failures: int = 0

    # Session metadata
    session_id: str = ""
    started_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            'message_buffer': [m.to_dict() for m in self.message_buffer],
            'summaries': [s.to_dict() for s in self.summaries],
            'current_task': self.current_task.to_dict() if self.current_task else None,
            'completed_tasks': [t.to_dict() for t in self.completed_tasks],
            'user_frustrated': self.user_frustrated,
            'frustration_signals': self.frustration_signals,
            'last_success_timestamp': self.last_success_timestamp.isoformat() if self.last_success_timestamp else None,
            'consecutive_failures': self.consecutive_failures,
            'session_id': self.session_id,
            'started_at': self.started_at.isoformat(),
        }


class TemporalContextCollector:
    """
    Pilar III: Temporal Context (Session Memory)

    Manages conversation history and task tracking across the session.

    Key Features:
    1. **Message Buffer**: Last N messages (active memory)
    2. **Recursive Summarization**: Old messages → compact summary
    3. **Task Tracking**: What are we trying to accomplish?
    4. **Frustration Detection**: Is user getting frustrated?
    5. **Pattern Learning**: What worked before?

    This solves the "Lost in the Middle" problem by:
    - Keeping recent context fresh (high attention)
    - Summarizing old context (preserves history without token bloat)
    - Detecting when user is stuck (adjust strategy)
    """

    def __init__(
        self,
        session_file: Optional[Path] = None,
        max_buffer_messages: int = 10,
        auto_summarize_threshold: int = 50,
    ):
        self.session_file = Path(session_file or Path.home() / ".max-code" / "session.json")
        self.session_file.parent.mkdir(parents=True, exist_ok=True)

        self.max_buffer_messages = max_buffer_messages
        self.auto_summarize_threshold = auto_summarize_threshold

        # Session state
        self.state = TemporalState()

        # Load existing session
        self._load_session()

    def add_message(self, role: MessageRole, content: str, metadata: Optional[Dict] = None):
        """
        Add message to buffer

        Auto-summarizes if buffer exceeds threshold
        """
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )

        self.state.message_buffer.append(message)

        # Auto-summarize if needed
        if len(self.state.message_buffer) > self.auto_summarize_threshold:
            self._auto_summarize()

        # Detect frustration
        if role == MessageRole.USER:
            self._detect_frustration(content)

        # Save session
        self._save_session()

    def get_context(self) -> TemporalState:
        """Get current temporal context"""
        return self.state

    def start_task(self, objective: str, sub_tasks: Optional[List[str]] = None):
        """Start tracking a new task"""
        if self.state.current_task:
            # Archive previous task
            self.state.completed_tasks.append(self.state.current_task)

        self.state.current_task = TaskState(
            objective=objective,
            started_at=datetime.now(),
            sub_tasks=sub_tasks or [],
        )

        self._save_session()

    def complete_sub_task(self, sub_task: str):
        """Mark sub-task as completed"""
        if not self.state.current_task:
            return

        if sub_task in self.state.current_task.sub_tasks:
            if sub_task not in self.state.current_task.completed_sub_tasks:
                self.state.current_task.completed_sub_tasks.append(sub_task)
                self._save_session()

    def complete_task(self, success: bool = True):
        """Complete current task"""
        if not self.state.current_task:
            return

        if success:
            self.state.last_success_timestamp = datetime.now()
            self.state.consecutive_failures = 0
        else:
            self.state.consecutive_failures += 1

        self.state.completed_tasks.append(self.state.current_task)
        self.state.current_task = None

        self._save_session()

    def increment_attempt(self):
        """Increment attempt counter for current task"""
        if self.state.current_task:
            self.state.current_task.attempt_count += 1
            self._save_session()

    def _auto_summarize(self):
        """
        Auto-summarize when buffer too large

        Strategy:
        1. Keep last N messages (active memory)
        2. Summarize older messages
        3. Append summary to summaries list
        """
        # Split buffer
        recent_messages = self.state.message_buffer[-self.max_buffer_messages:]
        old_messages = self.state.message_buffer[:-self.max_buffer_messages]

        if not old_messages:
            return

        # Generate summary (simple for now, can use LLM later)
        summary_text = self._simple_summarize(old_messages)

        # Create summary
        summary = SessionSummary(
            summary_text=summary_text,
            covers_messages=len(old_messages),
            summarized_at=datetime.now(),
            oldest_message_time=old_messages[0].timestamp,
            newest_message_time=old_messages[-1].timestamp,
        )

        # Update state
        self.state.summaries.append(summary)
        self.state.message_buffer = recent_messages

        self._save_session()

    def _simple_summarize(self, messages: List[Message]) -> str:
        """
        Simple summarization (bullet points)

        For production, use LLM-based summarization
        """
        # Count by role
        user_messages = [m for m in messages if m.role == MessageRole.USER]
        assistant_messages = [m for m in messages if m.role == MessageRole.ASSISTANT]

        # Extract key topics (simple keyword extraction)
        topics = set()
        for msg in messages:
            words = msg.content.lower().split()
            # Simple heuristic: extract capitalized words
            topics.update(w for w in words if len(w) > 5)

        topics_str = ', '.join(list(topics)[:10])

        summary = f"""Session summary ({len(messages)} messages):
- User inputs: {len(user_messages)}
- Assistant responses: {len(assistant_messages)}
- Key topics: {topics_str}
- Time range: {messages[0].timestamp.strftime('%H:%M')} - {messages[-1].timestamp.strftime('%H:%M')}
"""

        return summary

    def _detect_frustration(self, user_message: str):
        """
        Detect user frustration from message patterns

        Signals:
        - Negative keywords ("doesn't work", "error", "fail")
        - Repeated queries (same question multiple times)
        - Short angry messages ("wtf", "seriously?")
        - Excessive punctuation ("!!!", "???")
        """
        self.state.frustration_signals = []
        self.state.user_frustrated = False

        message_lower = user_message.lower()

        # Negative keywords
        negative_keywords = [
            "doesn't work", "not working", "error", "fail", "failed",
            "bug", "broken", "wrong", "incorrect", "problem", "issue",
            "wtf", "seriously", "again", "still"
        ]

        for keyword in negative_keywords:
            if keyword in message_lower:
                self.state.frustration_signals.append(f"negative_keyword: {keyword}")

        # Excessive punctuation
        if user_message.count('!') >= 2 or user_message.count('?') >= 3:
            self.state.frustration_signals.append("excessive_punctuation")

        # Short angry message
        if len(user_message) < 20 and any(kw in message_lower for kw in ['wtf', 'why', 'ugh']):
            self.state.frustration_signals.append("short_angry_message")

        # Repeated query detection (check last 5 messages)
        recent_user_msgs = [
            m.content.lower()
            for m in self.state.message_buffer[-5:]
            if m.role == MessageRole.USER
        ]

        if len(recent_user_msgs) >= 2:
            # Check similarity (simple: exact match)
            if recent_user_msgs.count(message_lower) > 1:
                self.state.frustration_signals.append("repeated_query")

        # Multiple failures
        if self.state.consecutive_failures >= 3:
            self.state.frustration_signals.append(f"consecutive_failures: {self.state.consecutive_failures}")

        # Set frustration flag
        if len(self.state.frustration_signals) >= 2:
            self.state.user_frustrated = True

    def _load_session(self):
        """Load session from disk"""
        if not self.session_file.exists():
            return

        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)

            # Reconstruct messages
            self.state.message_buffer = [
                Message(
                    role=MessageRole(m['role']),
                    content=m['content'],
                    timestamp=datetime.fromisoformat(m['timestamp']),
                    metadata=m.get('metadata', {})
                )
                for m in data.get('message_buffer', [])
            ]

            # Reconstruct summaries
            self.state.summaries = [
                SessionSummary.from_dict(s)
                for s in data.get('summaries', [])
            ]

            # Reconstruct task
            if data.get('current_task'):
                self.state.current_task = TaskState.from_dict(data['current_task'])

            # Load completed tasks
            self.state.completed_tasks = [
                TaskState.from_dict(t)
                for t in data.get('completed_tasks', [])
            ]

            # Load other fields
            self.state.user_frustrated = data.get('user_frustrated', False)
            self.state.frustration_signals = data.get('frustration_signals', [])
            self.state.consecutive_failures = data.get('consecutive_failures', 0)
            self.state.session_id = data.get('session_id', '')

            if data.get('last_success_timestamp'):
                self.state.last_success_timestamp = datetime.fromisoformat(data['last_success_timestamp'])

            if data.get('started_at'):
                self.state.started_at = datetime.fromisoformat(data['started_at'])

        except Exception as e:
            print(f"Error loading session: {e}")

    def _save_session(self):
        """Save session to disk"""
        try:
            data = self.state.to_dict()

            with open(self.session_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving session: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        total_messages = len(self.state.message_buffer) + sum(
            s.covers_messages for s in self.state.summaries
        )

        user_messages = sum(
            1 for m in self.state.message_buffer
            if m.role == MessageRole.USER
        )

        return {
            'total_messages': total_messages,
            'buffer_messages': len(self.state.message_buffer),
            'summaries': len(self.state.summaries),
            'user_messages': user_messages,
            'current_task': self.state.current_task.objective if self.state.current_task else None,
            'task_progress': self.state.current_task.progress if self.state.current_task else 0.0,
            'completed_tasks': len(self.state.completed_tasks),
            'user_frustrated': self.state.user_frustrated,
            'consecutive_failures': self.state.consecutive_failures,
            'session_duration_minutes': (datetime.now() - self.state.started_at).total_seconds() / 60,
        }


# Singleton instance
_collector: Optional[TemporalContextCollector] = None


def get_temporal_collector() -> TemporalContextCollector:
    """Get or create singleton temporal context collector"""
    global _collector
    if _collector is None:
        _collector = TemporalContextCollector()
    return _collector
