"""
Learning System Package

Learn from errors, extract patterns, recommend solutions.

RESEARCH-BASED IMPLEMENTATION:
- OpenAI embeddings: Semantic similarity
- Constitutional AI: Solution filtering
- TF-IDF + DBSCAN: Pattern extraction
- Success rate tracking: Learn from feedback

Components:
- ErrorDatabase: Store errors with embeddings
- PatternExtractor: ML-based pattern clustering
- SolutionRecommender: Rank and filter solutions
- LearningEngine: Orchestrator

Usage:
    from src.learning import LearningEngine
    
    engine = LearningEngine()
    error_id = engine.on_error("Task", "TypeError", "Error msg")
    solutions = engine.get_recommendations("TypeError", "Error msg")
"""
from .error_database import ErrorDatabase, StoredError
from .pattern_extractor import PatternExtractor, Pattern, extract_error_patterns
from .solution_recommender import SolutionRecommender, Solution
from .learning_engine import LearningEngine

__all__ = [
    "ErrorDatabase",
    "StoredError",
    "PatternExtractor",
    "Pattern",
    "extract_error_patterns",
    "SolutionRecommender",
    "Solution",
    "LearningEngine",
]
