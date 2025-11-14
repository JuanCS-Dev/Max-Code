"""Performance benchmarks for MABA.

Day 4: Performance testing of critical paths.

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
import time
from datetime import datetime


@pytest.mark.performance
@pytest.mark.database
class TestDatabasePerformance:
    """Test database operation performance."""

    async def test_cognitive_map_learning_performance(
        self, db_session, benchmark_config, performance_thresholds
    ):
        """Benchmark learning from browser actions."""
        from cognitive_map.service import CognitiveMapService
        from db.models import BrowserAction, BrowserSession

        # Setup
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        cognitive_map = CognitiveMapService(db_session)

        # Benchmark
        action = BrowserAction(
            session_id=session.id,
            action_type="click",
            url="https://benchmark.com",
            selector="button.test",
            success=True,
        )
        db_session.add(action)
        await db_session.flush()

        start = time.time()
        await cognitive_map.learn_from_action(action)
        duration = time.time() - start

        # Assert performance
        threshold = performance_thresholds["cognitive_map_learn"]
        assert duration < threshold, f"Learning took {duration}s, threshold is {threshold}s"

    async def test_recommendation_query_performance(
        self, db_with_sample_data, performance_thresholds
    ):
        """Benchmark selector recommendation queries."""
        from cognitive_map.service import CognitiveMapService

        cognitive_map = CognitiveMapService(db_with_sample_data)

        start = time.time()
        recommendations = await cognitive_map.recommend_selector(
            url="https://example.com",
            action_type="click",
            limit=10,
        )
        duration = time.time() - start

        # Should be fast query
        assert duration < performance_thresholds["db_query"]

    async def test_statistics_query_performance(
        self, db_with_sample_data, performance_thresholds
    ):
        """Benchmark statistics aggregation."""
        from cognitive_map.service import CognitiveMapService

        cognitive_map = CognitiveMapService(db_with_sample_data)

        start = time.time()
        stats = await cognitive_map.get_statistics()
        duration = time.time() - start

        # Statistics should be reasonably fast
        assert duration < performance_thresholds["db_query"]


@pytest.mark.performance
class TestScalability:
    """Test scalability with large datasets."""

    @pytest.mark.slow
    async def test_many_pages_performance(self, db_session):
        """Test performance with many learned pages."""
        from db.models import CognitiveMapPage

        # Create 1000 pages
        pages = []
        for i in range(1000):
            page = CognitiveMapPage(
                url=f"https://test{i}.com",
                url_hash=CognitiveMapPage.hash_url(f"https://test{i}.com"),
                domain=f"test{i}.com",
                visited_count=i % 10,
                importance_score=float(i % 100),
            )
            pages.append(page)

        db_session.add_all(pages)
        await db_session.commit()

        # Test query performance
        from cognitive_map.service import CognitiveMapService
        cognitive_map = CognitiveMapService(db_session)

        start = time.time()
        important = await cognitive_map.get_important_pages(min_score=50, limit=10)
        duration = time.time() - start

        # Should still be fast with 1000 pages
        assert duration < 1.0  # 1 second
        assert len(important) <= 10
