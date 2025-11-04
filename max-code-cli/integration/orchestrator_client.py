"""
MAXIMUS Orchestrator Service Client

Interfaces with Orchestrator for:
- Workflow coordination
- Multi-service orchestration
- Task routing
- State management
- MAPE-K loop coordination

PRODUCTION IMPLEMENTATION
"""

from typing import Dict, Any, Optional, List
from integration.base_client import BaseServiceClient, ServiceResponse


class OrchestratorClient(BaseServiceClient):
    """
    Client for MAXIMUS Orchestrator Service.

    Coordinates workflows across multiple MAXIMUS services,
    implementing the MAPE-K control loop.
    """

    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize Orchestrator client.

        Args:
            base_url: Orchestrator service URL
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        super().__init__(base_url, "Orchestrator", timeout, max_retries)

    # ========================================================================
    # WORKFLOW ORCHESTRATION
    # ========================================================================

    def create_workflow(self, workflow_def: Dict[str, Any]) -> ServiceResponse:
        """
        Create new workflow definition.

        Args:
            workflow_def: Workflow definition with steps and dependencies

        Returns:
            ServiceResponse with workflow ID
        """
        return self.post("/api/workflows", json=workflow_def)

    def execute_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> ServiceResponse:
        """
        Execute workflow with given inputs.

        Args:
            workflow_id: Workflow identifier
            inputs: Input parameters for workflow

        Returns:
            ServiceResponse with execution ID and initial status
        """
        return self.post(f"/api/workflows/{workflow_id}/execute", json=inputs)

    def get_workflow_status(self, execution_id: str) -> ServiceResponse:
        """
        Get workflow execution status.

        Args:
            execution_id: Execution identifier

        Returns:
            ServiceResponse with execution status and results
        """
        return self.get(f"/api/executions/{execution_id}")

    # ========================================================================
    # TASK ROUTING
    # ========================================================================

    def route_task(self, task: Dict[str, Any]) -> ServiceResponse:
        """
        Route task to appropriate service.

        Args:
            task: Task with 'type', 'payload', and routing hints

        Returns:
            ServiceResponse with routing decision
        """
        return self.post("/api/router/route", json=task)

    def get_service_capabilities(self) -> ServiceResponse:
        """
        Get capabilities of all registered services.

        Returns:
            ServiceResponse with service capabilities map
        """
        return self.get("/api/router/capabilities")

    # ========================================================================
    # MAPE-K CONTROL LOOP
    # ========================================================================

    def monitor_system(self) -> ServiceResponse:
        """
        Get system monitoring data (Monitor phase).

        Returns:
            ServiceResponse with system metrics
        """
        return self.get("/api/mape-k/monitor")

    def analyze_situation(self, metrics: Dict[str, Any]) -> ServiceResponse:
        """
        Analyze current situation (Analyze phase).

        Args:
            metrics: System metrics to analyze

        Returns:
            ServiceResponse with analysis results
        """
        return self.post("/api/mape-k/analyze", json=metrics)

    def plan_adaptation(self, analysis: Dict[str, Any]) -> ServiceResponse:
        """
        Plan system adaptation (Plan phase).

        Args:
            analysis: Analysis results

        Returns:
            ServiceResponse with adaptation plan
        """
        return self.post("/api/mape-k/plan", json=analysis)

    def execute_adaptation(self, plan: Dict[str, Any]) -> ServiceResponse:
        """
        Execute adaptation plan (Execute phase).

        Args:
            plan: Adaptation plan

        Returns:
            ServiceResponse with execution results
        """
        return self.post("/api/mape-k/execute", json=plan)

    def get_knowledge_base(self) -> ServiceResponse:
        """
        Get knowledge base (Knowledge component).

        Returns:
            ServiceResponse with knowledge base contents
        """
        return self.get("/api/mape-k/knowledge")

    # ========================================================================
    # STATE MANAGEMENT
    # ========================================================================

    def get_system_state(self) -> ServiceResponse:
        """
        Get current system state.

        Returns:
            ServiceResponse with complete system state
        """
        return self.get("/api/state")

    def update_system_state(self, state_updates: Dict[str, Any]) -> ServiceResponse:
        """
        Update system state.

        Args:
            state_updates: State changes to apply

        Returns:
            ServiceResponse with updated state
        """
        return self.put("/api/state", json=state_updates)

    # ========================================================================
    # SERVICE REGISTRY
    # ========================================================================

    def get_registered_services(self) -> ServiceResponse:
        """
        Get all registered services.

        Returns:
            ServiceResponse with service list
        """
        return self.get("/api/services")

    def get_service_info(self, service_name: str) -> ServiceResponse:
        """
        Get information about specific service.

        Args:
            service_name: Service name

        Returns:
            ServiceResponse with service details
        """
        return self.get(f"/api/services/{service_name}")

    # ========================================================================
    # METRICS & HEALTH
    # ========================================================================

    def get_orchestration_metrics(self) -> ServiceResponse:
        """
        Get orchestration metrics.

        Returns:
            ServiceResponse with metrics data
        """
        return self.get("/metrics")

    def get_health(self) -> ServiceResponse:
        """
        Get orchestrator health.

        Returns:
            ServiceResponse with health status
        """
        return self.get("/health")

    # ========================================================================
    # INTEGRATION HELPERS
    # ========================================================================

    def coordinate_multi_service_action(
        self,
        action_description: str,
        services_required: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> ServiceResponse:
        """
        Coordinate action across multiple services.

        Args:
            action_description: Description of action
            services_required: List of service names needed
            context: Optional context

        Returns:
            ServiceResponse with coordination plan
        """
        payload = {
            "action": action_description,
            "services": services_required,
            "context": context or {}
        }
        return self.post("/api/coordinate", json=payload)
