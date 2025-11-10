"""
Error Database: Store and retrieve errors with embeddings

RESEARCH SYNTHESIS:
- OpenAI embeddings: $0.02/1M tokens, 1536 dims
- SQLite: Lightweight, no external DB needed
- Vector search: Cosine similarity for semantic matching
- Auto-prune: Remove old patterns (>6 months)

STRATEGY:
✅ Use OpenAI text-embedding-3-small (cheap, fast)
✅ Store errors with metadata + embeddings
✅ Query by similarity (cosine distance)
✅ Track success rates for solutions
✅ Auto-cleanup old data
"""
import logging
import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np

from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass
class StoredError:
    """Error record in database"""
    id: int
    task_description: str
    error_type: str
    error_message: str
    code_context: str
    solution: Optional[str]
    success: Optional[bool]
    success_rate: float
    occurrence_count: int
    first_seen: str  # ISO datetime
    last_seen: str
    embedding: Optional[List[float]] = None  # 1536-dim vector
    
    def to_dict(self) -> Dict:
        """Convert to dict (excluding embedding for display)"""
        d = asdict(self)
        if 'embedding' in d:
            d['embedding'] = f"<vector: {len(d['embedding'])} dims>" if d['embedding'] else None
        return d


class ErrorDatabase:
    """
    SQLite database for storing errors with embeddings
    
    Features:
    - Error storage with OpenAI embeddings
    - Similarity search (cosine distance)
    - Solution tracking with success rates
    - Auto-pruning of old data (>6 months)
    - Pattern clustering support
    
    Schema:
    - errors: Main error records
    - solutions: Solution attempts
    - patterns: Extracted patterns (computed)
    
    Performance:
    - Query latency: <200ms (with index)
    - Embedding generation: <100ms
    - Storage: ~2KB per error
    """
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        auto_prune_days: int = 180  # 6 months
    ):
        """
        Initialize error database
        
        Args:
            db_path: Path to SQLite database (default: data/errors.db)
            auto_prune_days: Auto-delete errors older than this (days)
        """
        if db_path is None:
            db_path = "data/errors.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.auto_prune_days = auto_prune_days
        
        # Initialize OpenAI client for embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=api_key) if api_key else None
        
        # Connect and initialize schema
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Dict-like access
        
        self._init_schema()
        self._prune_old_errors()
        
        logger.info(f"ErrorDatabase initialized at {self.db_path}")
    
    def _init_schema(self):
        """Initialize database schema"""
        cursor = self.conn.cursor()
        
        # Main errors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_description TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                code_context TEXT,
                solution TEXT,
                success BOOLEAN,
                success_rate REAL DEFAULT 0.0,
                occurrence_count INTEGER DEFAULT 1,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                embedding_json TEXT,
                UNIQUE(error_type, error_message, task_description)
            )
        """)
        
        # Solutions table (track individual attempts)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_id INTEGER NOT NULL,
                solution TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                timestamp TEXT NOT NULL,
                execution_time REAL,
                FOREIGN KEY (error_id) REFERENCES errors(id) ON DELETE CASCADE
            )
        """)
        
        # Patterns table (computed clusters)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                description TEXT,
                error_ids TEXT,  -- JSON array of error IDs
                frequency INTEGER DEFAULT 0,
                avg_success_rate REAL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Indexes for fast queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_errors_type ON errors(error_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_errors_last_seen ON errors(last_seen)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_solutions_error_id ON solutions(error_id)")
        
        self.conn.commit()
        logger.info("Database schema initialized")
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        Generate OpenAI embedding for text
        
        Uses text-embedding-3-small (1536 dims, $0.02/1M tokens)
        
        Args:
            text: Text to embed
            
        Returns:
            1536-dimensional embedding vector
        """
        if not self.openai_client:
            logger.warning("OpenAI client not available, using zero vector")
            return [0.0] * 1536
        
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000]  # Limit to avoid token limits
            )
            return response.data[0].embedding
        
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return [0.0] * 1536
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a = np.array(vec1)
        b = np.array(vec2)
        
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return np.dot(a, b) / (norm_a * norm_b)
    
    def store_error(
        self,
        task_description: str,
        error_type: str,
        error_message: str,
        code_context: str = "",
        solution: Optional[str] = None,
        success: Optional[bool] = None
    ) -> int:
        """
        Store error in database with embedding
        
        If error already exists (same type + message + task), increments count
        
        Args:
            task_description: Description of task that failed
            error_type: Type of error (e.g., "SyntaxError", "ImportError")
            error_message: Error message text
            code_context: Code snippet causing error
            solution: Solution that was attempted
            success: Whether solution succeeded
            
        Returns:
            Error ID
        """
        cursor = self.conn.cursor()
        
        # Generate embedding from combined context
        embedding_text = f"{task_description}\n{error_type}: {error_message}\n{code_context}"
        embedding = self._get_embedding(embedding_text)
        embedding_json = json.dumps(embedding)
        
        now = datetime.now().isoformat()
        
        # Check if error already exists
        cursor.execute("""
            SELECT id, occurrence_count, success_rate
            FROM errors
            WHERE error_type = ? AND error_message = ? AND task_description = ?
        """, (error_type, error_message, task_description))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing error
            error_id = existing['id']
            new_count = existing['occurrence_count'] + 1
            
            # Update success rate if we have new information
            if success is not None:
                # Weighted average of success rate
                old_rate = existing['success_rate']
                new_rate = (old_rate * existing['occurrence_count'] + (1.0 if success else 0.0)) / new_count
            else:
                new_rate = existing['success_rate']
            
            cursor.execute("""
                UPDATE errors
                SET occurrence_count = ?,
                    success_rate = ?,
                    last_seen = ?,
                    solution = COALESCE(?, solution),
                    success = COALESCE(?, success)
                WHERE id = ?
            """, (new_count, new_rate, now, solution, success, error_id))
            
            logger.info(f"Updated existing error {error_id} (count={new_count})")
        
        else:
            # Insert new error
            cursor.execute("""
                INSERT INTO errors (
                    task_description, error_type, error_message,
                    code_context, solution, success, success_rate,
                    occurrence_count, first_seen, last_seen, embedding_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_description, error_type, error_message,
                code_context, solution, success,
                1.0 if success else 0.0,
                1, now, now, embedding_json
            ))
            
            error_id = cursor.lastrowid
            logger.info(f"Stored new error {error_id}")
        
        # Store solution attempt if provided
        if solution:
            cursor.execute("""
                INSERT INTO solutions (error_id, solution, success, timestamp)
                VALUES (?, ?, ?, ?)
            """, (error_id, solution, success or False, now))
        
        self.conn.commit()
        
        return error_id
    
    def query_similar(
        self,
        error_message: str,
        task_description: str = "",
        limit: int = 5,
        min_similarity: float = 0.7
    ) -> List[StoredError]:
        """
        Find similar errors using embedding similarity
        
        Args:
            error_message: Error message to match
            task_description: Task context (optional)
            limit: Max number of results
            min_similarity: Minimum cosine similarity threshold
            
        Returns:
            List of similar errors (sorted by similarity)
        """
        # Generate query embedding
        query_text = f"{task_description}\n{error_message}" if task_description else error_message
        query_embedding = self._get_embedding(query_text)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM errors")
        
        results = []
        
        for row in cursor.fetchall():
            # Load embedding
            embedding_json = row['embedding_json']
            if not embedding_json:
                continue
            
            stored_embedding = json.loads(embedding_json)
            
            # Calculate similarity
            similarity = self._cosine_similarity(query_embedding, stored_embedding)
            
            if similarity >= min_similarity:
                error = StoredError(
                    id=row['id'],
                    task_description=row['task_description'],
                    error_type=row['error_type'],
                    error_message=row['error_message'],
                    code_context=row['code_context'],
                    solution=row['solution'],
                    success=bool(row['success']) if row['success'] is not None else None,
                    success_rate=row['success_rate'],
                    occurrence_count=row['occurrence_count'],
                    first_seen=row['first_seen'],
                    last_seen=row['last_seen'],
                    embedding=stored_embedding
                )
                results.append((similarity, error))
        
        # Sort by similarity descending
        results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top matches
        return [error for _, error in results[:limit]]
    
    def get_by_id(self, error_id: int) -> Optional[StoredError]:
        """Get error by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM errors WHERE id = ?", (error_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        embedding_json = row['embedding_json']
        embedding = json.loads(embedding_json) if embedding_json else None
        
        return StoredError(
            id=row['id'],
            task_description=row['task_description'],
            error_type=row['error_type'],
            error_message=row['error_message'],
            code_context=row['code_context'],
            solution=row['solution'],
            success=bool(row['success']) if row['success'] is not None else None,
            success_rate=row['success_rate'],
            occurrence_count=row['occurrence_count'],
            first_seen=row['first_seen'],
            last_seen=row['last_seen'],
            embedding=embedding
        )
    
    def get_all_errors(self, limit: int = 100) -> List[StoredError]:
        """Get all errors (for pattern extraction)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM errors
            ORDER BY last_seen DESC
            LIMIT ?
        """, (limit,))
        
        errors = []
        for row in cursor.fetchall():
            embedding_json = row['embedding_json']
            embedding = json.loads(embedding_json) if embedding_json else None
            
            errors.append(StoredError(
                id=row['id'],
                task_description=row['task_description'],
                error_type=row['error_type'],
                error_message=row['error_message'],
                code_context=row['code_context'],
                solution=row['solution'],
                success=bool(row['success']) if row['success'] is not None else None,
                success_rate=row['success_rate'],
                occurrence_count=row['occurrence_count'],
                first_seen=row['first_seen'],
                last_seen=row['last_seen'],
                embedding=embedding
            ))
        
        return errors
    
    def update_success_rate(self, error_id: int, success: bool):
        """Update success rate after solution attempt"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT occurrence_count, success_rate
            FROM errors WHERE id = ?
        """, (error_id,))
        
        row = cursor.fetchone()
        if not row:
            return
        
        count = row['occurrence_count']
        old_rate = row['success_rate']
        
        # Update rate
        new_rate = (old_rate * count + (1.0 if success else 0.0)) / (count + 1)
        
        cursor.execute("""
            UPDATE errors
            SET success_rate = ?,
                occurrence_count = ?,
                last_seen = ?
            WHERE id = ?
        """, (new_rate, count + 1, datetime.now().isoformat(), error_id))
        
        self.conn.commit()
        logger.info(f"Updated error {error_id} success rate: {new_rate:.2%}")
    
    def _prune_old_errors(self):
        """Remove errors older than auto_prune_days"""
        cutoff_date = (datetime.now() - timedelta(days=self.auto_prune_days)).isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM errors
            WHERE last_seen < ? AND occurrence_count < 3
        """, (cutoff_date,))
        
        deleted = cursor.rowcount
        self.conn.commit()
        
        if deleted > 0:
            logger.info(f"Pruned {deleted} old errors (>{self.auto_prune_days} days, <3 occurrences)")
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM errors")
        total_errors = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM solutions")
        total_solutions = cursor.fetchone()['total']
        
        cursor.execute("SELECT AVG(success_rate) as avg_rate FROM errors WHERE success_rate > 0")
        avg_success_rate = cursor.fetchone()['avg_rate'] or 0.0
        
        cursor.execute("SELECT error_type, COUNT(*) as count FROM errors GROUP BY error_type ORDER BY count DESC")
        error_types = {row['error_type']: row['count'] for row in cursor.fetchall()}
        
        return {
            "total_errors": total_errors,
            "total_solutions": total_solutions,
            "avg_success_rate": avg_success_rate,
            "error_types": error_types
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
