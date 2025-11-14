"""Integration tests for learning flow.

Day 4: Test browser action → learning → recommendation flow.

Author: Vértice Platform Team
License: Proprietary
"""
import pytest

from cognitive_map.service import CognitiveMapService
from db.models import BrowserAction, BrowserSession, CognitiveMapPage


@pytest.mark.integration
@pytest.mark.database
class TestLearningIntegration:
    """Test complete learning flow."""

    async def test_action_to_learning_flow(self, db_session):
        """Test complete flow from action to learned knowledge."""
        # 1. Create browser session
        session = BrowserSession(status="active", browser_type="chromium")
        db_session.add(session)
        await db_session.flush()

        # 2. Perform browser action
        action = BrowserAction(
            session_id=session.id,
            action_type="click",
            url="https://example.com",
            selector="button.submit",
            success=True,
            duration_ms=200,
        )
        db_session.add(action)
        await db_session.commit()

        # 3. Learn from action
        cognitive_map = CognitiveMapService(db_session)
        await cognitive_map.learn_from_action(action)

        # 4. Verify knowledge was learned
        url_hash = CognitiveMapPage.hash_url("https://example.com")
        from sqlalchemy import select
        result = await db_session.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one()

        assert page.visited_count == 1
        assert page.importance_score > 0

        # 5. Get recommendations
        recommendations = await cognitive_map.recommend_selector(
            url="https://example.com", action_type="click"
        )

        assert len(recommendations) > 0
        assert recommendations[0]["selector"] == "button.submit"

    async def test_multiple_actions_improve_confidence(self, db_session):
        """Test that multiple successful actions improve recommendations."""
        session = BrowserSession(status="active")
        db_session.add(session)
        await db_session.flush()

        cognitive_map = CognitiveMapService(db_session)

        # Perform same action multiple times
        for i in range(5):
            action = BrowserAction(
                session_id=session.id,
                action_type="click",
                url="https://test.com",
                selector="button.reliable",
                success=True,
                duration_ms=150,
            )
            db_session.add(action)
            await db_session.flush()
            await cognitive_map.learn_from_action(action)

        await db_session.commit()

        # Get recommendation
        recommendations = await cognitive_map.recommend_selector(
            url="https://test.com", action_type="click"
        )

        assert len(recommendations) > 0
        assert recommendations[0]["count"] == 5  # All 5 successes recorded
