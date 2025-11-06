"""
Orchestrator Service Client - Workflow Coordination

Production HTTP client for MAXIMUS Orchestrator Service.
Based on real API endpoints from services/orchestrator/main.py

Endpoints:
- GET  /health
- POST /orchestrate
- GET  /workflow/{id}/status

Port: 8154 (Docker) | localhost:8154 (dev)
"""

import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logging.warning("httpx not installed. Install: pip install httpx")

from integration.base_client import BaseHTTPClient

logger = logging.getLogger(__name__)


# Request/Response Models
class OrchestrationRequest(BaseModel):
    """POST /orchestrate request."""
    workflow_name: str = Field(..., description="Workflow to execute")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Workflow parameters")
    priority: int = Field(5, ge=1, le=10, description="Priority 1-10")


class WorkflowStatus(BaseModel):
    """Workflow status response."""
    workflow_id: str
    status: str
    current_step: Optional[str] = None
    progress: float = 0.0
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


if HTTPX_AVAILABLE:
    class OrchestratorClient(BaseHTTPClient):
        """
        Orchestrator Service Client - Workflow Coordination.

        Example:
            client = OrchestratorClient()
            status = client.orchestrate("threat_hunting", {"target": "192.168.1.1"})
            print(f"Workflow: {status.workflow_id}, Status: {status.status}")
        """

        def __init__(self, base_url: str = "http://localhost:8154", **kwargs):
            super().__init__(base_url=base_url, **kwargs)

        def health(self) -> Dict[str, Any]:
            """Get health status."""
            response = self.get("/health")
            return response.json()

        def orchestrate(
            self,
            workflow_name: str,
            parameters: Optional[Dict[str, Any]] = None,
            priority: int = 5
        ) -> WorkflowStatus:
            """
            Start an orchestration workflow.

            Args:
                workflow_name: Name of workflow to execute
                parameters: Workflow parameters
                priority: Priority 1-10 (10 highest)

            Returns:
                WorkflowStatus with workflow_id and initial status
            """
            request = OrchestrationRequest(
                workflow_name=workflow_name,
                parameters=parameters,
                priority=priority
            )
            response = self.post("/orchestrate", json=request.model_dump())
            return WorkflowStatus(**response.json())

        def get_workflow_status(self, workflow_id: str) -> WorkflowStatus:
            """
            Get workflow status.

            Args:
                workflow_id: Workflow identifier

            Returns:
                WorkflowStatus with current state and progress
            """
            response = self.get(f"/workflow/{workflow_id}/status")
            return WorkflowStatus(**response.json())

else:
    class OrchestratorClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required: pip install httpx")
