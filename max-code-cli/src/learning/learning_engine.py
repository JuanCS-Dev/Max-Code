"""
Learning Engine: Orchestrate error learning system
"""
import logging
from typing import List, Optional
from pathlib import Path

from .error_database import ErrorDatabase
from .pattern_extractor import PatternExtractor, Pattern
from .solution_recommender import SolutionRecommender, Solution

logger = logging.getLogger(__name__)


class LearningEngine:
    """
    Orchestrate learning from errors
    
    Features:
    - Store errors with context
    - Extract patterns periodically
    - Recommend solutions
    - Learn from feedback
    """
    
    def __init__(self, db_path: Optional[str] = None):
        self.db = ErrorDatabase(db_path or "data/errors.db")
        self.extractor = PatternExtractor()
        self.recommender = SolutionRecommender(self.db)
        
        logger.info("LearningEngine initialized")
    
    def on_error(
        self,
        task_description: str,
        error_type: str,
        error_message: str,
        code_context: str = ""
    ) -> int:
        """Record error occurrence"""
        error_id = self.db.store_error(
            task_description,
            error_type,
            error_message,
            code_context
        )
        
        logger.info(f"Recorded error {error_id}: {error_type}")
        return error_id
    
    def on_success(
        self,
        error_id: int,
        solution: str
    ):
        """Record successful solution"""
        self.db.update_success_rate(error_id, success=True)
        logger.info(f"Recorded success for error {error_id}")
    
    def get_recommendations(
        self,
        error_type: str,
        error_message: str,
        task_description: str = ""
    ) -> List[Solution]:
        """Get solution recommendations"""
        return self.recommender.recommend(
            error_type,
            error_message,
            task_description
        )
    
    def extract_patterns(self) -> List[Pattern]:
        """Extract patterns from all errors"""
        errors = self.db.get_all_errors(limit=100)
        return self.extractor.extract_patterns(errors)
    
    def get_stats(self):
        """Get learning statistics"""
        return self.db.get_stats()
    
    def close(self):
        self.db.close()
