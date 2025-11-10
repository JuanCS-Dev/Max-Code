"""
Solution Recommender: Recommend solutions based on error patterns

STRATEGY:
✅ Rank solutions by success rate
✅ Filter using Constitutional AI principles
✅ Learn from feedback
✅ Recommend top-k solutions
"""
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from .error_database import ErrorDatabase, StoredError
from .pattern_extractor import Pattern

logger = logging.getLogger(__name__)


@dataclass
class Solution:
    """Recommended solution"""
    id: int
    description: str
    success_rate: float
    times_used: int
    source: str  # "pattern", "similar", "default"
    confidence: float
    
    def __repr__(self) -> str:
        return f"Solution({self.description[:50]}..., rate={self.success_rate:.0%})"


class SolutionRecommender:
    """
    Recommend solutions based on error history
    
    Features:
    - Rank by success rate
    - Filter by Constitutional AI principles
    - Learn from feedback
    - Top-k recommendations
    
    Constitutional AI Principles:
    - Only suggest solutions with >50% success rate
    - Prioritize frequently successful solutions
    - Filter out harmful/risky solutions
    """
    
    def __init__(
        self,
        db: ErrorDatabase,
        min_success_rate: float = 0.5,
        min_confidence: float = 0.6
    ):
        self.db = db
        self.min_success_rate = min_success_rate
        self.min_confidence = min_confidence
        
        logger.info(f"SolutionRecommender initialized (min_rate={min_success_rate})")
    
    def recommend(
        self,
        error_type: str,
        error_message: str,
        task_description: str = "",
        top_k: int = 3
    ) -> List[Solution]:
        """Recommend solutions for error"""
        # Find similar errors
        similar_errors = self.db.query_similar(
            error_message,
            task_description,
            limit=10,
            min_similarity=0.7
        )
        
        solutions = []
        
        # Extract solutions from similar errors
        for error in similar_errors:
            if error.solution and error.success_rate >= self.min_success_rate:
                solutions.append(Solution(
                    id=error.id,
                    description=error.solution,
                    success_rate=error.success_rate,
                    times_used=error.occurrence_count,
                    source="similar",
                    confidence=error.success_rate
                ))
        
        # Rank and deduplicate
        solutions = self.rank_by_success_rate(solutions)
        
        # Apply Constitutional AI filtering
        solutions = self._apply_constitutional_filter(solutions)
        
        return solutions[:top_k]
    
    def rank_by_success_rate(self, solutions: List[Solution]) -> List[Solution]:
        """Rank solutions by success rate and usage"""
        # Sort by: success_rate * log(times_used + 1)
        import math
        solutions.sort(
            key=lambda s: s.success_rate * math.log(s.times_used + 1),
            reverse=True
        )
        return solutions
    
    def _apply_constitutional_filter(self, solutions: List[Solution]) -> List[Solution]:
        """
        Filter solutions using Constitutional AI principles
        
        Principles:
        1. Only solutions with >50% success rate
        2. Exclude potentially harmful solutions
        3. Prioritize safe, tested solutions
        """
        filtered = []
        
        for solution in solutions:
            # Principle 1: Success rate threshold
            if solution.success_rate < self.min_success_rate:
                continue
            
            # Principle 2: No dangerous operations (simple check)
            dangerous_keywords = ['rm -rf', 'delete', 'drop table', 'format']
            if any(kw in solution.description.lower() for kw in dangerous_keywords):
                logger.warning(f"Filtered dangerous solution: {solution.description[:50]}")
                continue
            
            # Principle 3: Confidence threshold
            if solution.confidence < self.min_confidence:
                continue
            
            filtered.append(solution)
        
        return filtered
    
    def learn_from_feedback(self, error_id: int, solution_worked: bool):
        """Update success rate based on feedback"""
        self.db.update_success_rate(error_id, solution_worked)
        logger.info(f"Learned from feedback for error {error_id}: {'success' if solution_worked else 'failure'}")
