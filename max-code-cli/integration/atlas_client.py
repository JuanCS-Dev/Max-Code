"""
MAXIMUS Atlas Service Client

Interfaces with Atlas for:
- Context management
- Environment tracking
- Spatial reasoning
- Context switching

PRODUCTION IMPLEMENTATION
"""

from typing import Dict, Any, Optional, List
from integration.base_client import BaseServiceClient, ServiceResponse


class AtlasClient(BaseServiceClient):
    """
    Client for MAXIMUS Atlas Service.

    Provides context management and environmental awareness.
    """

    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize Atlas client.

        Args:
            base_url: Atlas service URL
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        super().__init__(base_url, "Atlas", timeout, max_retries)

    # ========================================================================
    # CONTEXT MANAGEMENT
    # ========================================================================

    def get_current_context(self) -> ServiceResponse:
        """
        Get current active context.

        Returns:
            ServiceResponse with context data
        """
        return self.get("/api/context/current")

    def create_context(self, context: Dict[str, Any]) -> ServiceResponse:
        """
        Create new context.

        Args:
            context: Context data with 'name', 'description', and 'metadata'

        Returns:
            ServiceResponse with context ID
        """
        return self.post("/api/context", json=context)

    def switch_context(self, context_id: str) -> ServiceResponse:
        """
        Switch to different context.

        Args:
            context_id: Context identifier

        Returns:
            ServiceResponse with new context state
        """
        return self.post(f"/api/context/{context_id}/activate")

    def update_context(self, context_id: str, updates: Dict[str, Any]) -> ServiceResponse:
        """
        Update context data.

        Args:
            context_id: Context identifier
            updates: Context updates

        Returns:
            ServiceResponse with updated context
        """
        return self.put(f"/api/context/{context_id}", json=updates)

    # ========================================================================
    # ENVIRONMENT TRACKING
    # ========================================================================

    def get_environment_state(self) -> ServiceResponse:
        """
        Get current environment state.

        Returns:
            ServiceResponse with environment metrics
        """
        return self.get("/api/environment/state")

    def track_event(self, event: Dict[str, Any]) -> ServiceResponse:
        """
        Track environmental event.

        Args:
            event: Event data with 'type', 'payload', and 'timestamp'

        Returns:
            ServiceResponse with tracking confirmation
        """
        return self.post("/api/environment/track", json=event)

    def get_event_history(self, limit: int = 10) -> ServiceResponse:
        """
        Get recent environmental events.

        Args:
            limit: Maximum number of events

        Returns:
            ServiceResponse with event history
        """
        return self.get(f"/api/environment/events?limit={limit}")

    # ========================================================================
    # SPATIAL REASONING
    # ========================================================================

    def get_spatial_map(self) -> ServiceResponse:
        """
        Get spatial relationship map.

        Returns:
            ServiceResponse with spatial topology
        """
        return self.get("/api/spatial/map")

    def compute_distance(self, entity_a: str, entity_b: str) -> ServiceResponse:
        """
        Compute distance between entities.

        Args:
            entity_a: First entity identifier
            entity_b: Second entity identifier

        Returns:
            ServiceResponse with distance metrics
        """
        payload = {
            "entity_a": entity_a,
            "entity_b": entity_b
        }
        return self.post("/api/spatial/distance", json=payload)

    # ========================================================================
    # METRICS & HEALTH
    # ========================================================================

    def get_context_metrics(self) -> ServiceResponse:
        """
        Get context management metrics.

        Returns:
            ServiceResponse with metrics data
        """
        return self.get("/metrics")

    def get_health(self) -> ServiceResponse:
        """
        Get Atlas health.

        Returns:
            ServiceResponse with health status
        """
        return self.get("/health")

    # ========================================================================
    # INTEGRATION HELPERS
    # ========================================================================

    def get_context_for_task(self, task_description: str) -> ServiceResponse:
        """
        Get or create appropriate context for task.

        Args:
            task_description: Description of task

        Returns:
            ServiceResponse with context recommendation
        """
        payload = {"task": task_description}
        return self.post("/api/context/recommend", json=payload)
