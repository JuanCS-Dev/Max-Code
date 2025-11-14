"""End-to-end tests for complete workflows.

Day 4: Full stack testing of MABA functionality.

Tests real user workflows from API to database.

Author: Vértice Platform Team
License: Proprietary
"""
import pytest


@pytest.mark.e2e
@pytest.mark.slow
class TestCompleteWorkflows:
    """Test complete user workflows."""

    @pytest.mark.skip(reason="Requires full MABA service running")
    async def test_full_automation_workflow(self, authenticated_client):
        """Test complete browser automation workflow.
        
        Workflow:
        1. Create browser session
        2. Navigate to URL
        3. Click element
        4. Extract data
        5. Close session
        6. Verify learning occurred
        """
        # Step 1: Create session
        response = await authenticated_client.post(
            "/api/v1/sessions",
            json={"viewport_width": 1920, "viewport_height": 1080},
        )
        assert response.status_code == 200
        session_data = response.json()
        session_id = session_data["session_id"]

        # Step 2: Navigate
        response = await authenticated_client.post(
            f"/api/v1/navigate?session_id={session_id}",
            json={
                "url": "https://example.com",
                "wait_until": "networkidle",
            },
        )
        assert response.status_code == 200

        # Step 3: Click
        response = await authenticated_client.post(
            f"/api/v1/click?session_id={session_id}",
            json={"selector": "a"},
        )
        assert response.status_code == 200

        # Step 4: Extract
        response = await authenticated_client.post(
            f"/api/v1/extract?session_id={session_id}",
            json={"selectors": {"title": "h1"}},
        )
        assert response.status_code == 200

        # Step 5: Close session
        response = await authenticated_client.delete(
            f"/api/v1/sessions/{session_id}"
        )
        assert response.status_code == 200

        # Step 6: Verify learning
        response = await authenticated_client.post(
            "/api/v1/cognitive-map/query",
            json={
                "query_type": "recommend_selector",
                "parameters": {
                    "url": "https://example.com",
                    "action_type": "click",
                },
            },
        )
        assert response.status_code == 200
        query_result = response.json()
        assert query_result["found"] is True

    @pytest.mark.skip(reason="Requires full MABA service running")
    async def test_learning_across_sessions(self, authenticated_client):
        """Test that knowledge persists across multiple sessions."""
        url = "https://persistent-learning.com"
        selector = "button.learned"

        # Create 3 sessions and perform same action
        for i in range(3):
            # Create session
            response = await authenticated_client.post(
                "/api/v1/sessions",
                json={},
            )
            session_id = response.json()["session_id"]

            # Navigate
            await authenticated_client.post(
                f"/api/v1/navigate?session_id={session_id}",
                json={"url": url},
            )

            # Click
            await authenticated_client.post(
                f"/api/v1/click?session_id={session_id}",
                json={"selector": selector},
            )

            # Close
            await authenticated_client.delete(
                f"/api/v1/sessions/{session_id}"
            )

        # Check that knowledge accumulated
        response = await authenticated_client.post(
            "/api/v1/cognitive-map/query",
            json={
                "query_type": "recommend_selector",
                "parameters": {
                    "url": url,
                    "action_type": "click",
                },
            },
        )

        query_result = response.json()
        assert query_result["found"] is True
        recommendations = query_result["result"]["recommendations"]
        assert recommendations[0]["count"] == 3  # Learned 3 times
