"""
Tests for learning system
"""
import pytest
import os
import tempfile
from pathlib import Path

from src.learning import (
    ErrorDatabase,
    PatternExtractor,
    SolutionRecommender,
    LearningEngine,
    StoredError,
    Pattern,
    Solution
)


class TestErrorDatabase:
    def test_init(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = ErrorDatabase(str(db_path))
            
            assert db_path.exists()
            assert db.auto_prune_days == 180
            
            db.close()
    
    def test_store_and_retrieve(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = ErrorDatabase(str(Path(tmpdir) / "test.db"))
            
            error_id = db.store_error(
                task_description="Test task",
                error_type="TestError",
                error_message="Test error occurred",
                code_context="print('test')"
            )
            
            assert error_id > 0
            
            error = db.get_by_id(error_id)
            assert error is not None
            assert error.error_type == "TestError"
            assert error.occurrence_count == 1
            
            db.close()
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API")
    def test_query_similar(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = ErrorDatabase(str(Path(tmpdir) / "test.db"))
            
            db.store_error("Import module", "ImportError", "No module named 'nonexistent'")
            db.store_error("Import package", "ImportError", "Cannot import name 'missing'")
            
            similar = db.query_similar("ImportError: module not found", limit=2)
            
            assert len(similar) > 0
            
            db.close()


class TestPatternExtractor:
    def test_init(self):
        extractor = PatternExtractor()
        assert extractor.min_cluster_size == 3
    
    def test_extract_patterns_insufficient_data(self):
        extractor = PatternExtractor(min_cluster_size=3)
        
        errors = [
            StoredError(1, "task1", "TypeError", "msg1", "", None, None, 0.0, 1, "2024-01-01", "2024-01-01")
        ]
        
        patterns = extractor.extract_patterns(errors)
        assert len(patterns) == 0


class TestSolutionRecommender:
    def test_init(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = ErrorDatabase(str(Path(tmpdir) / "test.db"))
            recommender = SolutionRecommender(db)
            
            assert recommender.min_success_rate == 0.5
            
            db.close()
    
    def test_constitutional_filter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = ErrorDatabase(str(Path(tmpdir) / "test.db"))
            recommender = SolutionRecommender(db)
            
            solutions = [
                Solution(1, "Fix import", 0.9, 10, "similar", 0.9),
                Solution(2, "rm -rf /", 0.8, 5, "similar", 0.8),  # Dangerous
                Solution(3, "Update code", 0.3, 2, "similar", 0.3),  # Low rate
            ]
            
            filtered = recommender._apply_constitutional_filter(solutions)
            
            assert len(filtered) == 1
            assert filtered[0].id == 1
            
            db.close()


class TestLearningEngine:
    def test_init(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = LearningEngine(str(Path(tmpdir) / "test.db"))
            
            assert engine.db is not None
            assert engine.extractor is not None
            assert engine.recommender is not None
            
            engine.close()
    
    def test_error_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = LearningEngine(str(Path(tmpdir) / "test.db"))
            
            error_id = engine.on_error(
                "Test task",
                "TestError",
                "Test error message"
            )
            
            assert error_id > 0
            
            engine.on_success(error_id, "Fix applied")
            
            stats = engine.get_stats()
            assert stats["total_errors"] > 0
            
            engine.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
