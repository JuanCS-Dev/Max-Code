# CORE - API Reference

**Gerado:** 2025-11-07 20:45:31
**Método:** Análise automática do código fonte

---

## 1. Service Overview

### Statistics
- Python Files: 1249
- Lines of Code: 281477
- Test Files: 834

### Entry Point
```
services/core/main.py
```

### Directory Structure
```
.
.apv
.attention_system
.audit_results
.audit_results/htmlcov_full_audit
.autonomic_core
.autonomic_core/analyze
.autonomic_core/execute
.autonomic_core/knowledge_base
.autonomic_core/monitor
.autonomic_core/plan
.compassion
.compliance
.consciousness
.consciousness/archived_old_v4
.consciousness/coagulation
.consciousness/consciousness
.consciousness/episodic_memory
.consciousness/esgt
.consciousness/htmlcov
.consciousness/incident_reports
.consciousness/integration_archive_dead_code
.consciousness/lrr
.consciousness/mcea
.consciousness/mea
.consciousness/metacognition
.consciousness/mmei
.consciousness/neuromodulation
.consciousness/predictive_coding
.consciousness/reactive_fabric
.consciousness/sandboxing
.consciousness/tig
.consciousness/validation
.constitutional
.constitutional/guardians
.constitutional/hitl
.constitutional/__pycache__
.constitutional/validators
.demo
._demonstration
.docs
.docs/architecture
.docs/compassion
.docs/PENELOPE
.docs/reports
.ethics
.examples
.fairness
.federated_learning
.governance
.governance/guardian
.governance/htmlcov
.governance_sse
.hitl
.htmlcov
.htmlcov_82_baseline
.htmlcov_baseline
.htmlcov_constitutional
.htmlcov_constitutional_complete
.htmlcov_ethical_final
.htmlcov_final
.htmlcov_REAL_baseline
.justice
.justice/tests
.k8s
.migrations
.mip_client
.models
.models/onnx
.models/pruned
.models/quantized
.monitoring
.monitoring/dashboards
.motor_integridade_processual
.motor_integridade_processual/arbiter
.motor_integridade_processual/frameworks
.motor_integridade_processual/infrastructure
.motor_integridade_processual/models
.motor_integridade_processual/resolution
.motor_integridade_processual/tests
.neuromodulation
.observability
.performance
.predictive_coding
.privacy
.profiling
.profiling/results
.__pycache__
..pytest_cache
..pytest_cache/v
.scripts
.shared
.skill_learning
.tests
.tests/archived_broken
.tests/archived_v4_tests
.tests/benchmarks
.tests/constitutional
.tests/e2e
.tests/fixtures
.tests/integration
.tests/__pycache__
.tests/statistical
.tests/stress
.tests/unit
.training
.training/data
.training/logs
.training/tests
.ui
.ui/__pycache__
.workflows
.xai
```

---

## 2. API Endpoints

### `adw_router.py` - Line 109
```python
@router.get("/offensive/status")
async def get_offensive_status() -> dict[str, Any]:
```

**Description:**
```
"""Get Red Team AI operational status.

Returns current state of offensive orchestration system including:
- System status (operational/degraded/offline)
- Active campaigns count
- Total exploits attempted
- Success rate metrics

Returns:
```

### `adw_router.py` - Line 154
```python
@router.post("/offensive/campaign")
async def create_campaign(
```

**Description:**
```
"""Create new offensive campaign.

Initiates autonomous penetration testing campaign with specified
objective and scope.

Args:
    request: Campaign configuration (objective, scope)
```

### `adw_router.py` - Line 238
```python
@router.get("/offensive/campaigns")
async def list_campaigns() -> dict[str, Any]:
```

**Description:**
```
"""List all offensive campaigns (active and historical).

Returns:
    Dict with campaigns list and statistics
"""
# REAL INTEGRATION READY - Uncomment when service available:
# orchestrator = get_orchestrator()
# try:
#     campaigns = await orchestrator.get_all_campaigns(limit=50)
```

### `adw_router.py` - Line 280
```python
@router.get("/defensive/status")
async def get_defensive_status() -> dict[str, Any]:
```

**Description:**
```
"""Get Blue Team AI (Immune System) operational status.

Returns comprehensive status of all 8 immune agents:
- NK Cells (Natural Killer)
- Macrophages
- T Cells (Helper, Cytotoxic)
- B Cells
- Dendritic Cells
- Neutrophils
```

### `adw_router.py` - Line 376
```python
@router.get("/defensive/threats")
async def get_threats() -> list[dict[str, Any]]:
```

**Description:**
```
"""Get currently detected threats.

Returns list of active and recent threats detected by immune agents,
including threat level, type, and mitigation status.

Returns:
    List of threat dictionaries
"""
# REAL INTEGRATION READY - Uncomment when service available:
```

### `adw_router.py` - Line 412
```python
@router.get("/defensive/coagulation")
async def get_coagulation_status() -> dict[str, Any]:
```

**Description:**
```
"""Get coagulation cascade system status.

Returns status of biological-inspired hemostasis system:
- Primary hemostasis (Reflex Triage)
- Secondary hemostasis (Fibrin Mesh)
- Fibrinolysis (Restoration)

Returns:
    Dict with coagulation cascade metrics
```

### `adw_router.py` - Line 462
```python
@router.get("/purple/metrics")
async def get_purple_metrics() -> dict[str, Any]:
```

**Description:**
```
"""Get Purple Team co-evolution metrics - TEMPORARY MOCK

Returns metrics from Red vs Blue adversarial training cycles:
- Red Team attack effectiveness
- Blue Team defense effectiveness
- Co-evolution rounds completed
- Improvement trends

Returns:
```

### `adw_router.py` - Line 486
```python
@router.post("/purple/cycle")
async def trigger_evolution_cycle(
```

**Description:**
```
"""Trigger new co-evolution cycle - TEMPORARY MOCK

Initiates adversarial training round where Red Team attacks
and Blue Team defends, generating improvement signals for both.

Returns:
    Dict with cycle status and ID
```

### `adw_router.py` - Line 635
```python
@router.post("/workflows/attack-surface")
async def execute_attack_surface_workflow(
```

**Description:**
```
"""Execute Attack Surface Mapping workflow.

Combines Network Recon + Vuln Intel + Service Detection for comprehensive
attack surface analysis.
```

### `adw_router.py` - Line 680
```python
@router.post("/workflows/credential-intel")
async def execute_credential_intel_workflow(
```

**Description:**
```
"""Execute Credential Intelligence workflow.

Combines Breach Data + Google Dorking + Dark Web + Username Hunter
for credential exposure analysis.
```

### `adw_router.py` - Line 736
```python
@router.post("/workflows/target-profile")
async def execute_target_profiling_workflow(
```

**Description:**
```
"""Execute Deep Target Profiling workflow.

Combines Social Scraper + Email/Phone Analyzer + Image Analysis +
Pattern Detection for comprehensive target profiling.
```

### `adw_router.py` - Line 794
```python
@router.get("/workflows/{workflow_id}/status")
async def get_workflow_status(
```

**Description:**
```
"""Get workflow execution status.

Checks all workflow types for the given ID.
```

### `adw_router.py` - Line 827
```python
@router.get("/workflows/{workflow_id}/report")
async def get_workflow_report(
```

**Description:**
```
"""Get complete workflow report.

Retrieves full report from any workflow type.
```

### `adw_router.py` - Line 882
```python
@router.get("/overview")
async def get_adw_overview() -> dict[str, Any]:
```

**Description:**
```
"""Get unified overview of all AI-Driven Workflows.

Combines status from Offensive, Defensive, and Purple Team systems
into single comprehensive view for MAXIMUS AI dashboard.

Returns:
    Dict with complete ADW system status
"""
try:
```

### `adw_router.py` - Line 929
```python
@router.get("/health")
async def adw_health_check() -> dict[str, str]:
```

**Description:**
```
"""ADW system health check endpoint.

Returns:
    Dict with health status
"""
return {"status": "healthy", "message": "AI-Driven Workflows operational"}
```

### `api.py` - Line 185
```python
@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
```

**Description:**
```
"""Root endpoint with API information."""
return {
    "service": "Motor de Integridade Processual (MIP)",
    "version": "1.0.0",
    "docs": "/docs",
    "health": "/health"
}
```

### `api.py` - Line 196
```python
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
```

**Description:**
```
"""
Health check endpoint.

Returns service status and basic information.
"""
return HealthResponse(
    status="healthy",
    version="1.0.0",
    frameworks_loaded=len(frameworks),
```

### `api.py` - Line 211
```python
@app.get("/frameworks", response_model=List[FrameworkInfo])
async def list_frameworks() -> List[FrameworkInfo]:
```

**Description:**
```
"""
List available ethical frameworks.

Returns information about each framework including weights and capabilities.
"""
framework_infos = []

for name, framework in frameworks.items():
    framework_infos.append(
```

### `api.py` - Line 233
```python
@app.post("/evaluate", response_model=EvaluationResponse, status_code=status.HTTP_200_OK)
async def evaluate_action_plan(request: EvaluationRequest) -> EvaluationResponse:
```

**Description:**
```
"""
Evaluate an action plan against ethical frameworks with precedent-based reasoning.

Process:
1. Check CBR precedents (retrieve → reuse → revise)
   - If high confidence (>0.8), use precedent directly
   - Otherwise, fallback to frameworks
2. Evaluate plan with each framework (if no precedent)
3. Resolve conflicts between frameworks
```

### `api.py` - Line 406
```python
@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics() -> MetricsResponse:
```

**Description:**
```
"""
Get evaluation metrics.

Returns statistics about evaluations performed.
"""
avg_time = sum(evaluation_times) / len(evaluation_times) if evaluation_times else 0.0

return MetricsResponse(
    total_evaluations=evaluation_count,
```

### `api.py` - Line 422
```python
@app.post("/precedents/feedback", status_code=status.HTTP_200_OK)
async def update_precedent_feedback(request: PrecedentFeedbackRequest) -> Dict[str, str]:
```

**Description:**
```
"""
Update precedent with outcome feedback.

Allows humans/systems to provide feedback on how well a precedent-based
decision worked out, improving future CBR recommendations.

Args:
    request: PrecedentFeedbackRequest with precedent_id and success_score
```

### `api.py` - Line 482
```python
@app.get("/precedents/{precedent_id}", response_model=PrecedentResponse)
async def get_precedent(precedent_id: int) -> PrecedentResponse:
```

**Description:**
```
"""
Retrieve a specific precedent by ID.

Args:
    precedent_id: ID of the precedent to retrieve

Returns:
    PrecedentResponse with precedent details
```

### `api.py` - Line 530
```python
@app.post("/evaluate/ab-test", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def evaluate_ab_test(request: EvaluationRequest) -> Dict[str, Any]:
```

**Description:**
```
"""
A/B test: Compare CBR vs Frameworks for same action plan.

Evaluates the action plan using BOTH CBR (if available) and frameworks,
then compares the results. Useful for validating CBR performance.

Args:
    request: EvaluationRequest with action_plan
```

### `api.py` - Line 641
```python
@app.get("/ab-test/metrics", response_model=ABTestMetricsResponse)
async def get_ab_test_metrics() -> ABTestMetricsResponse:
```

**Description:**
```
"""
Get A/B testing metrics.

Returns statistics comparing CBR vs framework performance.

Returns:
    ABTestMetricsResponse with comparison metrics
"""
if len(ab_test_results) == 0:
```

### `api.py` - Line 688
```python
@app.get("/precedents/metrics", response_model=PrecedentMetricsResponse)
async def get_precedent_metrics() -> PrecedentMetricsResponse:
```

**Description:**
```
"""
Get metrics about precedents and CBR usage.

Returns statistics about precedent database and CBR performance.

Raises:
    HTTPException: If CBR disabled
"""
if cbr_engine is None or precedent_db is None:
```

### `main.py` - Line 267
```python
@app.get("/health")
async def health_check() -> dict[str, Any]:
```

**Description:**
```
"""Performs a comprehensive health check of the Maximus Core Service.

Checks:
- MAXIMUS AI status
- Consciousness System health (TIG, ESGT, Arousal, Safety)
- PrefrontalCortex status (social cognition)
- ToM Engine status (with Redis cache if configured)
- Decision Queue status (HITL Governance)
```

### `main.py` - Line 387
```python
@app.post("/query")
async def process_query_endpoint(request: QueryRequest) -> dict[str, Any]:
```

**Description:**
```
"""Processes a natural language query using the Maximus AI.

Args:
    request (QueryRequest): The request body containing the query and optional context.

Returns:
    Dict[str, Any]: The response from the Maximus AI, including the final answer, confidence score, and other metadata.

Raises:
```

### `test_guardians.py` - Line 327
```python
@app.get("/public/data")
def get_public_data():
```

**Description:**
```
        """)
```

### `test_guardians.py` - Line 331
```python
@app.post("/admin/delete")
def delete_everything():
```

**Description:**
```
        """)

        # Mock paths for testing
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.rglob", return_value=[test_file]):
                violations = await guardian._check_authentication()
```

### `test_article_iii_guardian.py` - Line 330
```python
            "@app.post('/users')n"
            "def create_user(request):\n"
```

### `test_article_iii_guardian.py` - Line 351
```python
            "@app.post('/users')n"
            "def create_user(request):\n"
```

### `metrics_exporter.py` - Line 143
```python
        @router.get(
            "/metrics",
```

### `metrics_exporter.py` - Line 166
```python
        @router.get(
            "/metrics/constitutional",
```

**Description:**
```
        """Return constitutional compliance summary."""
        return {
            "service": self.service_name,
            "constitution_version": "3.0",
            "framework": "DETER-AGENT",
```

### `api.py` - Line 174
```python
    @router.get("/state", response_model=ConsciousnessStateResponse)
    async def get_consciousness_state():
```

**Description:**
```
    """Get current complete consciousness state."""
    try:
        tig = consciousness_system.get("tig")
        esgt = consciousness_system.get("esgt")
        arousal = consciousness_system.get("arousal")

        if not all([tig, esgt, arousal]):
            raise HTTPException(status_code=503, detail="Consciousness system not fully initialized")
```

### `api.py` - Line 205
```python
    @router.get("/esgt/events", response_model=list[ESGTEventResponse])
    async def get_esgt_events(limit: int = 20):
```

**Description:**
```
    """Get recent ESGT events.

    Args:
        limit: Maximum number of events to return (default 20)
    """
    if limit < 1 or limit > MAX_HISTORY:
        raise HTTPException(status_code=400, detail=f"Limit must be between 1 and {MAX_HISTORY}")

    # Return most recent events
```

### `api.py` - Line 236
```python
    @router.get("/arousal")
    async def get_arousal_state():
```

**Description:**
```
    """Get current arousal state."""
    try:
        arousal = consciousness_system.get("arousal")
        if not arousal:
            raise HTTPException(status_code=503, detail="Arousal controller not initialized")

        arousal_state = arousal.get_current_arousal()
        if not arousal_state:
            return {"error": "No arousal state available"}
```

### `api.py` - Line 261
```python
    @router.post("/esgt/trigger")
    async def trigger_esgt(salience: SalienceInput):
```

**Description:**
```
    """Manually trigger ESGT ignition.

    Args:
        salience: Salience scores for ignition trigger

    Returns:
        ESGT event result
    """
    try:
```

### `api.py` - Line 309
```python
    @router.post("/arousal/adjust")
    async def adjust_arousal(adjustment: ArousalAdjustment):
```

**Description:**
```
    """Adjust arousal level.

    Args:
        adjustment: Arousal adjustment parameters

    Returns:
        New arousal state
    """
    try:
```

### `api.py` - Line 350
```python
    @router.get("/metrics")
    async def get_metrics():
```

**Description:**
```
    """Get consciousness system metrics."""
    try:
        tig = consciousness_system.get("tig")
        esgt = consciousness_system.get("esgt")

        metrics = {}

        if tig and hasattr(tig, "get_metrics"):
            metrics["tig"] = tig.get_metrics()
```

### `api.py` - Line 374
```python
    @router.get("/safety/status", response_model=SafetyStatusResponse)
    async def get_safety_status():
```

**Description:**
```
    """Get safety protocol status.

    Returns:
        Complete safety protocol status including violations and kill switch state

    Raises:
        HTTPException: If safety protocol is not enabled or not initialized
    """
    try:
```

### `api.py` - Line 402
```python
    @router.get("/safety/violations", response_model=list[SafetyViolationResponse])
    async def get_safety_violations(limit: int = 100):
```

**Description:**
```
    """Get recent safety violations.

    Args:
        limit: Maximum number of violations to return (1-1000)

    Returns:
        List of recent safety violations, ordered by timestamp

    Raises:
```

### `api.py` - Line 445
```python
    @router.post("/safety/emergency-shutdown")
    async def execute_emergency_shutdown(request: EmergencyShutdownRequest):
```

**Description:**
```
    """Execute emergency shutdown (HITL only).

    This endpoint triggers the kill switch protocol. If allow_override is True,
    HITL has 5 seconds to override. Otherwise, shutdown is immediate.

    **WARNING**: This is a destructive operation that stops the consciousness system.

    Args:
        request: Emergency shutdown request with reason
```

### `api.py` - Line 485
```python
    @router.get("/reactive-fabric/metrics")
    async def get_reactive_fabric_metrics():
```

**Description:**
```
    """Get latest Reactive Fabric metrics (Sprint 3).

    Returns:
        Latest system metrics from MetricsCollector

    Raises:
        HTTPException: If orchestrator not available
    """
    try:
```

### `api.py` - Line 551
```python
    @router.get("/reactive-fabric/events")
    async def get_reactive_fabric_events(limit: int = 20):
```

**Description:**
```
    """Get recent Reactive Fabric events (Sprint 3).

    Args:
        limit: Maximum events to return (1-100)

    Returns:
        Recent consciousness events from EventCollector

    Raises:
```

### `api.py` - Line 606
```python
    @router.get("/reactive-fabric/orchestration")
    async def get_reactive_fabric_orchestration():
```

**Description:**
```
    """Get Reactive Fabric orchestration status (Sprint 3).

    Returns:
        DataOrchestrator statistics and recent decisions

    Raises:
        HTTPException: If orchestrator not available
    """
    try:
```

### `api.py` - Line 700
```python
    @router.get("/stream/sse")
    async def stream_sse(request: Request):  # pragma: no cover - StreamingResponse blocks TestClient (integration test)
```

**Description:**
```
    """Endpoint SSE para cockpit e frontend React."""
    queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=250)
    sse_subscribers.append(queue)

    initial_state = {
        "type": "connection_ack",
        "timestamp": datetime.now().isoformat(),
        "recent_events": len(event_history),
    }
```

### `api.py` - Line 181
```python
    @router.get("/stream/sse")
    async def stream_apv_sse():
```

**Description:**
```
    """
    Server-Sent Events (SSE) stream for APV events

    Browser-friendly continuous stream of policy validation events.
    """
    async def event_generator():
        queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue(maxsize=50)
        sse_subscribers.append(queue)
```

### `api.py` - Line 249
```python
    @router.get("/latest", response_model=LatestAPVResponse)
    async def get_latest_apv(limit: int = 20):
```

**Description:**
```
    """
    Get latest APV events

    Args:
        limit: Maximum number of events to return (default: 20, max: 100)

    Returns:
        Latest APV events from history
    """
```

### `api.py` - Line 269
```python
    @router.get("/stats", response_model=APVStats)
    async def get_apv_stats():
```

**Description:**
```
    """
    Get APV statistics

    Returns:
        Comprehensive statistics about APV events and responses
    """
    avg_confidence = (
        stats["total_confidence"] / stats["total_events"]
        if stats["total_events"] > 0
```

### `test_constitutional_compliance.py` - Line 37
```python
    @app.get("/health/live")
    async def health_live():
```

### `test_constitutional_compliance.py` - Line 41
```python
    @app.get("/health/ready")
    async def health_ready():
```

### `test_constitutional_compliance.py` - Line 45
```python
    @app.get("/health/startup")
    async def health_startup():
```

**Description:**
```
"""Test that /metrics endpoint exists and returns Prometheus format."""
response = client.get("/metrics")
assert response.status_code == 200
```

### `osint_standalone.py` - Line 29
```python
@app.get("/health")
async def health_check():
```

**Description:**
```
"""Health check endpoint."""
return {"status": "operational", "service": "OSINT API Testing Server"}


if __name__ == "__main__":
print("🚀 Starting OSINT API Testing Server on port 8001...")
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### `osint_router.py` - Line 268
```python
@router.post("/deep-search")
async def execute_deep_search(request: DeepSearchRequest) -> dict[str, Any]:
```

**Description:**
```
"""Execute comprehensive OSINT deep search with AI correlation.

Orchestrates multiple intelligence sources:
- Username enumeration
- Email breach analysis
- Social media profiling
- Google dorking
- AI-powered pattern detection
```

### `osint_router.py` - Line 368
```python
@router.post("/username")
async def search_username_api(request: UsernameSearchRequest) -> dict[str, Any]:
```

**Description:**
```
"""Username intelligence endpoint."""
result = await search_username_internal(request.username)

if request.deep_analysis:
    # AI profiling
    ai_profile = await generate_gemini_analysis(
        "Create detailed behavioral profile from social media presence",
        result
    )
```

### `osint_router.py` - Line 384
```python
@router.post("/email")
async def search_email_api(request: EmailSearchRequest) -> dict[str, Any]:
```

**Description:**
```
"""Email intelligence endpoint."""
return await search_email_internal(str(request.email))


@router.post("/phone")
async def search_phone_api(request: PhoneSearchRequest) -> dict[str, Any]:
"""Phone intelligence endpoint."""
return await search_phone_internal(request.phone)
```

### `osint_router.py` - Line 390
```python
@router.post("/phone")
async def search_phone_api(request: PhoneSearchRequest) -> dict[str, Any]:
```

**Description:**
```
"""Phone intelligence endpoint."""
return await search_phone_internal(request.phone)


@router.get("/health")
async def osint_health_check() -> dict[str, Any]:
"""OSINT services health check."""
return {
    "status": "operational",
```

### `osint_router.py` - Line 396
```python
@router.get("/health")
async def osint_health_check() -> dict[str, Any]:
```

**Description:**
```
"""OSINT services health check."""
return {
    "status": "operational",
    "services": {
        "gemini": gemini_model is not None,
        "openai": openai_client is not None,
    },
    "timestamp": datetime.utcnow().isoformat()
}
```

### `api_routes.py` - Line 206
```python
    @router.get("/stream/{operator_id}")
    async def stream_governance_events(
```

**Description:**
```
    """
    Stream governance events via Server-Sent Events.

    This endpoint provides real-time streaming of pending HITL decisions
    to the operator's TUI.
```

### `api_routes.py` - Line 271
```python
    @router.get("/health", response_model=HealthResponse)
    async def get_health():
```

**Description:**
```
    """
    Get server health status.

    Returns:
        Health metrics
    """
    health = sse_server.get_health()
    return HealthResponse(**health)
```

### `api_routes.py` - Line 282
```python
    @router.get("/pending", response_model=PendingStatsResponse)
    async def get_pending_stats():
```

**Description:**
```
    """
    Get statistics about pending decisions.

    Returns:
        Pending decisions statistics
    """
    pending = decision_queue.get_pending_decisions()

    # Calculate stats
```

### `api_routes.py` - Line 316
```python
    @router.get("/decision/{decision_id}", response_model=DecisionResponse)
    async def get_decision(decision_id: str):
```

**Description:**
```
    """
    Get a specific decision by ID.

    Args:
        decision_id: Decision ID to retrieve

    Returns:
        Decision details
```

### `api_routes.py` - Line 380
```python
    @router.get("/decision/{decision_id}/watch")
    async def watch_decision(decision_id: str):
```

**Description:**
```
    """
    Watch a specific decision via SSE stream.

    This endpoint provides real-time updates about a specific decision,
    streaming status changes until the decision is resolved.

    Args:
        decision_id: Decision ID to watch
```

### `api_routes.py` - Line 527
```python
    @router.post("/session/create", response_model=SessionCreateResponse)
    async def create_session(request: SessionCreateRequest):
```

**Description:**
```
    """
    Create new operator session.

    Args:
        request: Session creation request

    Returns:
        Session details
    """
```

### `api_routes.py` - Line 560
```python
    @router.get("/session/{operator_id}/stats", response_model=OperatorStatsResponse)
    async def get_operator_stats(operator_id: str):
```

**Description:**
```
    """
    Get operator statistics.

    Args:
        operator_id: Operator identifier

    Returns:
        Operator metrics
    """
```

### `api_routes.py` - Line 635
```python
    @router.post("/decision/{decision_id}/approve", response_model=DecisionActionResponse)
    async def approve_decision(decision_id: str, request: ApproveDecisionRequest):
```

**Description:**
```
    """
    Approve a pending decision.

    Args:
        decision_id: Decision ID to approve
        request: Approval request

    Returns:
        Action result
```

### `api_routes.py` - Line 680
```python
    @router.post("/decision/{decision_id}/reject", response_model=DecisionActionResponse)
    async def reject_decision(decision_id: str, request: RejectDecisionRequest):
```

**Description:**
```
    """
    Reject a pending decision.

    Args:
        decision_id: Decision ID to reject
        request: Rejection request

    Returns:
        Action result
```

### `api_routes.py` - Line 724
```python
    @router.post("/decision/{decision_id}/escalate", response_model=DecisionActionResponse)
    async def escalate_decision(decision_id: str, request: EscalateDecisionRequest):
```

**Description:**
```
    """
    Escalate a pending decision to higher authority.

    Args:
        decision_id: Decision ID to escalate
        request: Escalation request

    Returns:
        Action result
```

### `api_routes.py` - Line 773
```python
    @router.post("/test/enqueue")
    async def enqueue_test_decision(decision_dict: dict):
```

**Description:**
```
    """
    Enqueue a test decision (for E2E testing only).

    WARNING: This endpoint is for testing purposes only.
    In production, decisions are enqueued by MAXIMUS internally.

    Args:
        decision_dict: Dictionary with decision data
```

### `standalone_server.py` - Line 118
```python
@app.get("/")
async def root():
```

**Description:**
```
"""Root endpoint."""
return {
    "service": "Governance SSE Server (Standalone)",
    "status": "running",
    "version": "1.0.0",
    "endpoints": {
        "health": "/api/v1/governance/health",
        "pending": "/api/v1/governance/pending",
        "stream": "/api/v1/governance/stream/{operator_id}",
```

### `standalone_server.py` - Line 134
```python
@app.get("/health")
async def health_check():
```

**Description:**
```
"""Global health check."""
return {"status": "healthy", "service": "governance-sse-standalone"}


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
```

### `governance_production_server.py` - Line 148
```python
@app.get("/health")
async def health_check():
```

**Description:**
```
"""
Health check endpoint for the Governance server.

Returns:
    Health status and component status
"""
return {
    "status": "healthy",
    "service": "Governance Workspace Production Server",
```

### `governance_production_server.py` - Line 168
```python
@app.get("/")
async def root():
```

**Description:**
```
"""Root endpoint with server information."""
return {
    "service": "Governance Workspace Production Server",
    "version": "1.0.0",
    "description": "HITL Governance Workspace for ethical AI decision review",
    "docs": "/docs",
    "health": "/health",
    "governance_api": "/api/v1/governance",
}
```

_No HTTP endpoints found_

## 3. Classes and Methods

### `AdvancedTools`

**File:** `advanced_tools.py`

```python
class AdvancedTools:
```

**Description:**
```
"""A suite of advanced, specialized tools for Maximus AI.

These tools extend Maximus's capabilities for complex analytical and
operational tasks, handling intricate data processing and deep analysis.
"""

def __init__(self, gemini_client: Any):
    """Initializes the AdvancedTools with a Gemini client.

    Args:
        gemini_client (Any): An initialized Gemini client for tool interactions.
    """
    self.gemini_client = gemini_client
    self.available_tools = [
        {
            "name": "data_analysis",
```

**Public Methods:**

- `def list_available_tools(self) -> list[dict[str, Any]]`

---

### `CampaignRequest`

**File:** `adw_router.py`

```python
class CampaignRequest(BaseModel):
```

**Description:**
```
"""Request model for creating offensive campaign."""

objective: str
scope: list[str]
constraints: dict[str, Any] | None = None


class CampaignResponse(BaseModel):
"""Response model for campaign creation."""

campaign_id: str
status: str
created_at: str


# ============================================================================
```

**Public Methods:**


---

### `CampaignResponse`

**File:** `adw_router.py`

```python
class CampaignResponse(BaseModel):
```

**Description:**
```
"""Response model for campaign creation."""

campaign_id: str
status: str
created_at: str


# ============================================================================
# OFFENSIVE AI (RED TEAM) ENDPOINTS
# ============================================================================


@router.get("/offensive/status")
async def get_offensive_status() -> dict[str, Any]:
"""Get Red Team AI operational status.
```

**Public Methods:**


---

### `AttackSurfaceRequest`

**File:** `adw_router.py`

```python
class AttackSurfaceRequest(BaseModel):
```

**Description:**
```
"""Request model for attack surface mapping workflow."""

domain: str
include_subdomains: bool = True
port_range: str | None = None
scan_depth: str = "standard"


class CredentialIntelRequest(BaseModel):
"""Request model for credential intelligence workflow."""

email: str | None = None
username: str | None = None
phone: str | None = None
include_darkweb: bool = True
include_dorking: bool = True
```

**Public Methods:**


---

### `CredentialIntelRequest`

**File:** `adw_router.py`

```python
class CredentialIntelRequest(BaseModel):
```

**Description:**
```
"""Request model for credential intelligence workflow."""

email: str | None = None
username: str | None = None
phone: str | None = None
include_darkweb: bool = True
include_dorking: bool = True
include_social: bool = True


class ProfileTargetRequest(BaseModel):
"""Request model for target profiling workflow."""

username: str | None = None
email: str | None = None
phone: str | None = None
```

**Public Methods:**


---

### `ProfileTargetRequest`

**File:** `adw_router.py`

```python
class ProfileTargetRequest(BaseModel):
```

**Description:**
```
"""Request model for target profiling workflow."""

username: str | None = None
email: str | None = None
phone: str | None = None
name: str | None = None
location: str | None = None
image_url: str | None = None
include_social: bool = True
include_images: bool = True


@router.post("/workflows/attack-surface")
async def execute_attack_surface_workflow(
request: AttackSurfaceRequest,
background_tasks: BackgroundTasks,
```

**Public Methods:**


---

### `AgentTemplates`

**File:** `agent_templates.py`

```python
class AgentTemplates:
```

**Description:**
```
"""Manages a repository of agent templates or personas for Maximus AI.

These templates define specific behaviors, communication styles, expertise domains,
and operational constraints for different tasks or user interactions.
"""

def __init__(self):
    """Initializes the AgentTemplates with a set of predefined templates."""
    self.templates: dict[str, dict[str, Any]] = {
        "default_assistant": {
            "name": "Default Assistant",
            "description": "A general-purpose helpful AI assistant.",
            "instructions": "You are a helpful AI assistant. Provide concise and accurate information.",
            "tone": "neutral",
            "expertise": ["general knowledge"],
        },
```

**Public Methods:**

- `def get_template(self, template_name`
- `def list_templates(self) -> list[dict[str, Any]]`
- `def add_template(self, template_name`
- `def update_template(self, template_name`
- `def delete_template(self, template_name`

---

### `APVEvent`

**File:** `api.py`

```python
class APVEvent(BaseModel):
```

**Description:**
```
"""APV validation event"""
event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
event_type: str  # 'threat_detected', 'policy_validated', 'response_executed'
severity: str  # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'
cve_id: str | None = None
description: str
affected_packages: List[str] = Field(default_factory=list)
affected_versions: List[str] = Field(default_factory=list)
remediation_status: str  # 'pending', 'in_progress', 'completed', 'failed'
confidence: float = Field(ge=0.0, le=1.0, default=0.0)
source: str = "maximus_core"


class APVStats(BaseModel):
"""APV statistics"""
```

**Public Methods:**


---

### `APVStats`

**File:** `api.py`

```python
class APVStats(BaseModel):
```

**Description:**
```
"""APV statistics"""
total_events: int
threats_detected: int
policies_validated: int
responses_executed: int
critical_count: int
high_count: int
medium_count: int
low_count: int
average_confidence: float
last_event_timestamp: str | None


class LatestAPVResponse(BaseModel):
"""Latest APV events response"""
success: bool
```

**Public Methods:**


---

### `LatestAPVResponse`

**File:** `api.py`

```python
class LatestAPVResponse(BaseModel):
```

**Description:**
```
"""Latest APV events response"""
success: bool
events: List[APVEvent]
total: int


# ==================== API FACTORY ====================


def create_apv_api() -> APIRouter:
"""
Create APV API router with WebSocket and SSE streaming capabilities

Returns:
    FastAPI router with APV endpoints
"""
```

**Public Methods:**

- `def add_event_to_history(event`

---

### `PeripheralDetection`

**File:** `attention_core.py`

```python
class PeripheralDetection:
```

**Description:**
```
"""Result from peripheral scanning."""

target_id: str
detection_type: str  # 'statistical_anomaly', 'entropy_change', 'volume_spike'
confidence: float  # 0.0-1.0
timestamp: float
metadata: dict[str, Any]


@dataclass
class FovealAnalysis:
"""Result from foveal deep analysis."""

target_id: str
threat_level: str  # 'BENIGN', 'SUSPICIOUS', 'MALICIOUS', 'CRITICAL'
confidence: float  # 0.0-1.0
```

**Public Methods:**


---

### `FovealAnalysis`

**File:** `attention_core.py`

```python
class FovealAnalysis:
```

**Description:**
```
"""Result from foveal deep analysis."""

target_id: str
threat_level: str  # 'BENIGN', 'SUSPICIOUS', 'MALICIOUS', 'CRITICAL'
confidence: float  # 0.0-1.0
findings: list[dict[str, Any]]
analysis_time_ms: float
timestamp: float
recommended_actions: list[str]


class PeripheralMonitor:
"""Lightweight, broad scanning of all system inputs.

Performs fast, statistical checks to detect significant changes
without deep analysis. Goal: <100ms latency.
```

**Public Methods:**


---

### `PeripheralMonitor`

**File:** `attention_core.py`

```python
class PeripheralMonitor:
```

**Description:**
```
"""Lightweight, broad scanning of all system inputs.

Performs fast, statistical checks to detect significant changes
without deep analysis. Goal: <100ms latency.
"""

def __init__(self, scan_interval_seconds: float = 1.0):
    """Initialize peripheral monitor.

    Args:
        scan_interval_seconds: How often to scan (default 1s)
    """
    self.scan_interval = scan_interval_seconds
    self.baseline_stats = {}  # Statistical baselines
    self.detection_history = deque(maxlen=1000)
    self.running = False
```

**Public Methods:**


---

### `FovealAnalyzer`

**File:** `attention_core.py`

```python
class FovealAnalyzer:
```

**Description:**
```
"""Deep, expensive analysis for high-salience targets.

Applies full analytical power when peripheral monitor detects
something worth investigating. Goal: <100ms saccade latency.
"""

def __init__(self):
    """Initialize foveal analyzer."""
    self.analysis_history = deque(maxlen=500)
    self.total_analyses = 0
    self.total_analysis_time_ms = 0

async def deep_analyze(self, target: PeripheralDetection, full_data: dict | None = None) -> FovealAnalysis:
    """Perform deep analysis on a high-salience target.

    Args:
```

**Public Methods:**

- `def get_average_analysis_time(self) -> float`

---

### `AttentionSystem`

**File:** `attention_core.py`

```python
class AttentionSystem:
```

**Description:**
```
"""Two-tier attention system with peripheral/foveal processing.

Coordinates lightweight peripheral scanning with deep foveal analysis,
using salience scoring to allocate attention efficiently.
"""

def __init__(self, foveal_threshold: float = 0.6, scan_interval: float = 1.0):
    """Initialize attention system.

    Args:
        foveal_threshold: Minimum salience score for foveal analysis
        scan_interval: Peripheral scan interval in seconds
    """
    self.peripheral = PeripheralMonitor(scan_interval_seconds=scan_interval)
    self.foveal = FovealAnalyzer()
    self.salience_scorer = SalienceScorer(foveal_threshold=foveal_threshold)
```

**Public Methods:**

- `def get_performance_stats(self) -> dict[str, Any]`

---

### `SalienceLevel`

**File:** `salience_scorer.py`

```python
class SalienceLevel(Enum):
```

**Description:**
```
"""Salience levels for attention prioritization."""

CRITICAL = 5  # Immediate foveal attention required
HIGH = 4  # High priority for foveal analysis
MEDIUM = 3  # Candidate for foveal analysis
LOW = 2  # Peripheral monitoring sufficient
MINIMAL = 1  # Background noise


@dataclass
class SalienceScore:
"""Salience score result."""

score: float  # 0.0 - 1.0
level: SalienceLevel
factors: dict[str, float]  # Individual factor contributions
```

**Public Methods:**


---

### `SalienceScore`

**File:** `salience_scorer.py`

```python
class SalienceScore:
```

**Description:**
```
"""Salience score result."""

score: float  # 0.0 - 1.0
level: SalienceLevel
factors: dict[str, float]  # Individual factor contributions
timestamp: float
target_id: str
requires_foveal: bool


class SalienceScorer:
"""Calculate salience scores for attention allocation.

Salience is computed from multiple factors:
- Novelty: How unusual is this event?
- Magnitude: How large is the deviation?
```

**Public Methods:**


---

### `SalienceScorer`

**File:** `salience_scorer.py`

```python
class SalienceScorer:
```

**Description:**
```
"""Calculate salience scores for attention allocation.

Salience is computed from multiple factors:
- Novelty: How unusual is this event?
- Magnitude: How large is the deviation?
- Velocity: How quickly is it changing?
- Threat: What's the potential impact?
- Context: Historical importance
"""

def __init__(self, foveal_threshold: float = 0.6, critical_threshold: float = 0.85):
    """Initialize salience scorer.

    Args:
        foveal_threshold: Minimum score to trigger foveal analysis (0.0-1.0)
        critical_threshold: Score for CRITICAL level (0.0-1.0)
```

**Public Methods:**

- `def calculate_salience(self, event`
- `def get_top_salient_targets(self, n`
- `def reset_baselines(self)`

---

### `LSTMAutoencoder`

**File:** `anomaly_detector.py`

```python
class LSTMAutoencoder(nn.Module):
```

**Description:**
```
"""LSTM-based autoencoder for anomaly detection."""

def __init__(self, input_dim: int = 50, hidden_dim: int = 32):
    super().__init__()
    self.encoder = nn.LSTM(input_dim, hidden_dim, batch_first=True)
    self.decoder = nn.LSTM(hidden_dim, input_dim, batch_first=True)

def forward(self, x):
    encoded, _ = self.encoder(x)
    decoded, _ = self.decoder(encoded)
    return decoded


class AnomalyDetector:
"""Hybrid anomaly detection using Isolation Forest + LSTM."""
```

**Public Methods:**

- `def forward(self, x)`

---

### `AnomalyDetector`

**File:** `anomaly_detector.py`

```python
class AnomalyDetector:
```

**Description:**
```
"""Hybrid anomaly detection using Isolation Forest + LSTM."""

def __init__(self, contamination: float = 0.1):
    self.iso_forest = IsolationForest(contamination=contamination, random_state=42)
    self.lstm_autoencoder = LSTMAutoencoder()
    self.threshold = 0.85

def train(self, normal_data: np.ndarray):
    """Train both models on normal behavior data."""
    logger.info(f"Training anomaly detectors on {len(normal_data)} samples")

    # Train Isolation Forest
    self.iso_forest.fit(normal_data)

    # Train LSTM Autoencoder
    # Convert to tensor and train (simplified for production)
```

**Public Methods:**

- `def train(self, normal_data`
- `def detect(self, metrics`

---

### `PerformanceDegradationDetector`

**File:** `degradation_detector.py`

```python
class PerformanceDegradationDetector:
```

**Description:**
```
"""Detect performance degradation using PELT algorithm."""

def __init__(self, penalty: int = 10, model: str = "rbf"):
    self.algo = rpt.Pelt(model=model, min_size=3)
    self.penalty = penalty

def detect(self, latency_timeseries: np.ndarray) -> dict:
    """
    Identify degradation before SLA breach.

    Args:
        latency_timeseries: Array of latency measurements

    Returns:
        Dict with degradation_detected, changepoint_index, severity
    """
```

**Public Methods:**

- `def detect(self, latency_timeseries`

---

### `ResourceDemandForecaster`

**File:** `demand_forecaster.py`

```python
class ResourceDemandForecaster:
```

**Description:**
```
"""
SARIMA-based time series forecaster for resource demand.

Implements Seasonal AutoRegressive Integrated Moving Average
to predict future CPU/Memory usage based on historical patterns.

Hyperparameters:
    order (p,d,q): (1, 1, 1) - AR, differencing, MA
    seasonal_order (P,D,Q,s): (1, 1, 1, 24) - Seasonal with 24h period
"""

def __init__(
    self,
    order: tuple[int, int, int] = (1, 1, 1),
    seasonal_order: tuple[int, int, int, int] = (1, 1, 1, 24),
):
```

**Public Methods:**

- `def train(self, historical_data`
- `def predict(self, horizon`
- `def validate(self, test_data`

---

### `FailurePredictor`

**File:** `failure_predictor.py`

```python
class FailurePredictor:
```

**Description:**
```
"""Predict service failures 10-30min ahead using XGBoost."""

def __init__(self):
    self.model = xgb.XGBClassifier(
        objective="binary:logistic",
        max_depth=6,
        learning_rate=0.1,
        n_estimators=100,
        random_state=42,
    )
    self.feature_names = [
        "error_rate_trend",
        "memory_leak_indicator",
        "cpu_spike_pattern",
        "disk_io_degradation",
    ]
```

**Public Methods:**

- `def train(self, X`
- `def predict(self, current_metrics`

---

### `CacheActuator`

**File:** `cache_actuator.py`

```python
class CacheActuator:
```

**Description:**
```
"""Manage Redis cache operations and optimization."""

def __init__(self, redis_url: str = "redis://localhost:6379/0", dry_run_mode: bool = True):
    self.redis_url = redis_url
    self.dry_run_mode = dry_run_mode
    self.action_log = []
    self.client: redis.Redis | None = None

async def connect(self):
    """Establish Redis connection."""
    if not self.client:
        try:
            self.client = await redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
            await self.client.ping()
            logger.info("Redis client connected successfully")
        except Exception as e:
```

**Public Methods:**

- `def get_action_log(self) -> list[dict]`

---

### `DatabaseActuator`

**File:** `database_actuator.py`

```python
class DatabaseActuator:
```

**Description:**
```
"""Manage database connection pools and query optimization."""

def __init__(
    self,
    db_url: str = "postgresql://localhost:5432/vertice",
    pgbouncer_admin_url: str = "postgresql://localhost:6432/pgbouncer",
    dry_run_mode: bool = True,
):
    self.db_url = db_url
    self.pgbouncer_admin_url = pgbouncer_admin_url
    self.dry_run_mode = dry_run_mode
    self.action_log = []

async def adjust_connection_pool(self, database: str, pool_size: int, pool_mode: str = "transaction") -> dict:
    """Adjust pgBouncer connection pool size and mode.
```

**Public Methods:**

- `def get_action_log(self) -> list[dict]`

---

### `DockerActuator`

**File:** `docker_actuator.py`

```python
class DockerActuator:
```

**Description:**
```
"""Execute container lifecycle operations via Docker SDK."""

def __init__(self, dry_run_mode: bool = True):
    self.dry_run_mode = dry_run_mode
    self.action_log = []

    try:
        self.client = docker.from_env()
        self.client.ping()
        logger.info("Docker client connected successfully")
    except DockerException as e:
        logger.error(f"Docker connection failed: {e}")
        self.client = None

def scale_service(self, service_name: str, replicas: int) -> dict:
    """Scale Docker Swarm service or compose service."""
```

**Public Methods:**

- `def scale_service(self, service_name`
- `def update_resource_limits(`
- `def restart_container(self, container_name`
- `def get_container_stats(self, container_name`
- `def get_action_log(self) -> list[dict]`

---

### `KubernetesActuator`

**File:** `kubernetes_actuator.py`

```python
class KubernetesActuator:
```

**Description:**
```
"""Execute resource changes via Kubernetes API."""

def __init__(self, dry_run_mode: bool = True):
    self.dry_run_mode = dry_run_mode
    self.action_log = []

def adjust_hpa(self, service: str, min_replicas: int, max_replicas: int) -> dict:
    """Adjust Horizontal Pod Autoscaler."""
    cmd = f"kubectl autoscale deployment {service} --min={min_replicas} --max={max_replicas}"
    return self._execute(cmd, "hpa_adjust")

def update_resource_limits(self, service: str, cpu_limit: str, memory_limit: str) -> dict:
    """Update resource limits."""
    cmd = f"kubectl set resources deployment {service} --limits=cpu={cpu_limit},memory={memory_limit}"
    return self._execute(cmd, "resource_limits")
```

**Public Methods:**

- `def adjust_hpa(self, service`
- `def update_resource_limits(self, service`
- `def restart_pod(self, service`

---

### `CircuitBreaker`

**File:** `loadbalancer_actuator.py`

```python
class CircuitBreaker:
```

**Description:**
```
"""Circuit breaker for service health monitoring."""

def __init__(
    self,
    failure_threshold: int = 5,
    success_threshold: int = 2,
    timeout_seconds: int = 60,
):
    self.failure_threshold = failure_threshold
    self.success_threshold = success_threshold
    self.timeout_seconds = timeout_seconds

    self.failure_count = 0
    self.success_count = 0
    self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    self.last_failure_time = None
```

**Public Methods:**

- `def record_success(self)`
- `def record_failure(self)`
- `def can_attempt(self) -> bool`
- `def get_state(self) -> str`

---

### `LoadBalancerActuator`

**File:** `loadbalancer_actuator.py`

```python
class LoadBalancerActuator:
```

**Description:**
```
"""Manage traffic distribution and circuit breaker."""

def __init__(
    self,
    lb_api_url: str = "http://localhost:8080/api/lb",
    dry_run_mode: bool = True,
):
    self.lb_api_url = lb_api_url
    self.dry_run_mode = dry_run_mode
    self.action_log = []
    self.circuit_breakers: dict[str, CircuitBreaker] = {}
    self.traffic_history = deque(maxlen=1000)

def get_circuit_breaker(self, service: str) -> CircuitBreaker:
    """Get or create circuit breaker for service."""
    if service not in self.circuit_breakers:
```

**Public Methods:**

- `def get_circuit_breaker(self, service`
- `def get_action_log(self) -> list[dict]`

---

### `SafetyManager`

**File:** `safety_manager.py`

```python
class SafetyManager:
```

**Description:**
```
"""Safety mechanisms for autonomous actions."""

def __init__(self):
    self.action_history = deque(maxlen=1000)
    self.last_critical_action = 0

def check_rate_limit(self, action_type: str) -> bool:
    """Prevent action oscillation - max 1 critical action/min."""
    if action_type == "CRITICAL":
        current_time = time.time()
        if current_time - self.last_critical_action < 60:
            logger.warning("Rate limit exceeded: CRITICAL action throttled")
            return False
        self.last_critical_action = current_time
    return True
```

**Public Methods:**

- `def check_rate_limit(self, action_type`
- `def auto_rollback(self, action`
- `def log_action(self, action`

---

### `HomeostaticControlLoop`

**File:** `hcl_orchestrator.py`

```python
class HomeostaticControlLoop:
```

**Description:**
```
"""Main HCL orchestrator - autonomous self-regulation loop."""

def __init__(
    self,
    dry_run_mode: bool = True,
    loop_interval_seconds: int = 30,
    db_url: str = "postgresql://localhost/vertice",
):
    self.dry_run_mode = dry_run_mode
    self.loop_interval = loop_interval_seconds
    self.running = False

    # Monitor
    self.monitor = SystemMonitor()

    # Analyze
```

**Public Methods:**


---

### `OperationalMode`

**File:** `homeostatic_control.py`

```python
class OperationalMode(str, Enum):
```

**Description:**
```
"""Enumeration for the different operational modes of the system."""

HIGH_PERFORMANCE = "high_performance"
BALANCED = "balanced"
ENERGY_EFFICIENT = "energy_efficient"


class SystemState(BaseModel):
"""Represents the current operational state of the system.

Attributes:
    timestamp (str): ISO formatted timestamp of when the state was recorded.
    mode (OperationalMode): The current operational mode.
    cpu_usage (float): Current CPU utilization (0-100%).
    memory_usage (float): Current memory utilization (0-100%).
    avg_latency_ms (float): Average system latency in milliseconds.
```

**Public Methods:**


---

### `SystemState`

**File:** `homeostatic_control.py`

```python
class SystemState(BaseModel):
```

**Description:**
```
"""Represents the current operational state of the system.

Attributes:
    timestamp (str): ISO formatted timestamp of when the state was recorded.
    mode (OperationalMode): The current operational mode.
    cpu_usage (float): Current CPU utilization (0-100%).
    memory_usage (float): Current memory utilization (0-100%).
    avg_latency_ms (float): Average system latency in milliseconds.
    is_healthy (bool): True if the system is considered healthy.
"""

timestamp: str
mode: OperationalMode
cpu_usage: float
memory_usage: float
avg_latency_ms: float
```

**Public Methods:**


---

### `HomeostaticControlLoop`

**File:** `homeostatic_control.py`

```python
class HomeostaticControlLoop:
```

**Description:**
```
"""Manages the self-regulation of the Maximus AI system.

The HCL continuously monitors system metrics, analyzes performance,
and adjusts resources to maintain a balanced and efficient operational state.
"""

def __init__(
    self,
    monitor=None,
    analyzer=None,
    planner=None,
    executor=None,
    check_interval_seconds: float = 5.0,
):
    """Initializes the HomeostaticControlLoop.
```

**Public Methods:**

- `def get_current_state(self) -> SystemState | None`

---

### `DecisionAPI`

**File:** `decision_api.py`

```python
class DecisionAPI:
```

**Description:**
```
"""API for HCL decision storage and retrieval."""

def __init__(self, db_url: str = "postgresql://localhost/vertice"):
    self.db_url = db_url
    self.pool = None

async def create_decision(self, decision: dict) -> dict:
    """Log a new HCL decision."""
    async with self.pool.acquire() as conn:
        result = await conn.fetchrow(
            """
            INSERT INTO hcl_decisions
            (trigger, operational_mode, actions_taken, state_before, state_after, outcome, reward_signal, human_feedback)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id, timestamp
        """,
```

**Public Methods:**


---

### `KafkaMetricsStreamer`

**File:** `kafka_streamer.py`

```python
class KafkaMetricsStreamer:
```

**Description:**
```
"""
Streams metrics to Kafka for real-time processing.

Enables downstream components to react to telemetry in real-time
without querying the database.
"""

def __init__(self, broker: str = "localhost:9092", topic: str = "system.telemetry.raw"):
    """
    Initialize Kafka streamer.

    Args:
        broker: Kafka broker address
        topic: Topic name for telemetry data
    """
    self.broker = broker
```

**Public Methods:**

- `def get_stats(self) -> dict[str, int]`

---

### `ComputeSensors`

**File:** `sensor_definitions.py`

```python
class ComputeSensors:
```

**Description:**
```
"""
Compute resource sensors - CPU, GPU, Memory, Swap.

Metrics:
    - cpu_usage (%): Overall CPU utilization
    - cpu_per_core (%): Per-core CPU usage
    - gpu_usage (%): GPU utilization (if available)
    - gpu_temperature (°C): GPU temperature
    - memory_usage (%): RAM usage
    - memory_available (GB): Available RAM
    - swap_usage (%): Swap usage
"""

async def collect(self) -> dict[str, Any]:
    """Collect all compute metrics."""
    metrics = {}
```

**Public Methods:**


---

### `NetworkSensors`

**File:** `sensor_definitions.py`

```python
class NetworkSensors:
```

**Description:**
```
"""
Network resource sensors.

Metrics:
    - latency_p99 (ms): 99th percentile latency (simulated/from metrics)
    - latency_p95 (ms): 95th percentile latency
    - bandwidth_saturation (%): Network bandwidth utilization
    - connection_pool (active/max): Active connections
    - packet_loss (%): Packet loss rate
    - bytes_sent (bytes/s): Outgoing bandwidth
    - bytes_recv (bytes/s): Incoming bandwidth
"""

def __init__(self):
    self.last_net_io = psutil.net_io_counters()
    self.last_check_time = asyncio.get_event_loop().time()
```

**Public Methods:**


---

### `ApplicationSensors`

**File:** `sensor_definitions.py`

```python
class ApplicationSensors:
```

**Description:**
```
"""
Application-level sensors.

Metrics:
    - error_rate (errors/s): Application errors per second
    - request_queue (depth): Pending requests
    - response_time_p50 (ms): Median response time
    - response_time_p95 (ms): 95th percentile response time
    - response_time_p99 (ms): 99th percentile response time
    - throughput (req/s): Requests per second
    - active_users: Current active users
"""

def __init__(self):
    self.error_count = 0
    self.request_count = 0
```

**Public Methods:**

- `def record_error(self)`
- `def record_request(self)`

---

### `MLModelSensors`

**File:** `sensor_definitions.py`

```python
class MLModelSensors:
```

**Description:**
```
"""
Machine Learning model sensors.

Metrics:
    - inference_latency (ms): Average inference time
    - inference_latency_p99 (ms): 99th percentile inference time
    - batch_efficiency (%): GPU batch utilization
    - model_drift (KL divergence): Distribution shift from training data
    - cache_hit_rate (%): Feature cache hit rate
    - predictions_per_sec: Throughput
"""

def __init__(self):
    self.inference_times = []
    self.cache_hits = 0
    self.cache_misses = 0
```

**Public Methods:**

- `def record_inference(self, latency_ms`
- `def record_cache_hit(self)`
- `def record_cache_miss(self)`

---

### `StorageSensors`

**File:** `sensor_definitions.py`

```python
class StorageSensors:
```

**Description:**
```
"""
Storage and database sensors.

Metrics:
    - disk_io_wait (%): I/O wait percentage
    - disk_read_bytes_per_sec: Read throughput
    - disk_write_bytes_per_sec: Write throughput
    - database_connections_active: Active DB connections
    - database_connections_max: Maximum allowed connections
    - query_latency (ms): Average query latency
    - index_efficiency (%): Index usage rate
"""

def __init__(self):
    self.last_disk_io = psutil.disk_io_counters()
    self.last_check_time = asyncio.get_event_loop().time()
```

**Public Methods:**

- `def record_query(self, latency_ms`

---

### `SystemMonitor`

**File:** `system_monitor.py`

```python
class SystemMonitor:
```

**Description:**
```
"""
Main Prometheus collector for 50+ system metrics.

Implements digital interoception - continuous awareness of internal system state.
Analogous to the autonomic nervous system's monitoring of vital signs.

Performance Targets:
    - Scrape interval: 15s
    - Collection latency: <1s
    - Storage retention: 90 days detailed, 2 years aggregated
"""

def __init__(
    self,
    kafka_broker: str = "localhost:9092",
    kafka_topic: str = "system.telemetry.raw",
```

**Public Methods:**

- `def get_latest_metrics(self) -> dict[str, Any]`

---

### `FuzzyLogicController`

**File:** `fuzzy_controller.py`

```python
class FuzzyLogicController:
```

**Description:**
```
"""Fuzzy controller for operational mode selection."""

def __init__(self):
    if SKFUZZY_AVAILABLE:
        self._setup_fuzzy_system()
    else:
        logger.warning("Using rule-based fallback (install scikit-fuzzy for full functionality)")

def _setup_fuzzy_system(self):
    """Setup fuzzy inference system."""
    # Input variables
    self.traffic = ctrl.Antecedent(np.arange(0, 101, 1), "traffic")
    self.alerts = ctrl.Antecedent(np.arange(0, 101, 1), "alerts")
    self.sla_risk = ctrl.Antecedent(np.arange(0, 101, 1), "sla_risk")

    # Output variable (0=EFFICIENT, 1=BALANCED, 2=HIGH_PERF)
```

**Public Methods:**

- `def decide_mode(self, traffic`

---

### `SACAgent`

**File:** `rl_agent.py`

```python
class SACAgent:
```

**Description:**
```
"""Soft Actor-Critic agent for resource allocation."""

def __init__(self):
    self.model = None
    if not SB3_AVAILABLE:
        logger.warning("SAC agent disabled (install stable-baselines3)")

def decide_actions(self, state: np.ndarray) -> dict:
    """
    Decide resource allocation actions.

    Args:
        state: 50+ metrics from Monitor Module

    Returns:
        Actions dict with cpu_%, mem_%, gpu_%, replicas
```

**Public Methods:**

- `def decide_actions(self, state`

---

### `AnomalyType`

**File:** `resource_analyzer.py`

```python
class AnomalyType(str, Enum):
```

**Description:**
```
"""Enumeration for different types of anomalies detected."""

SPIKE = "spike"
DROP = "drop"
TREND = "trend"


class Anomaly(BaseModel):
"""Represents a detected anomaly in system metrics.

Attributes:
    type (AnomalyType): The type of anomaly.
    metric_name (str): The name of the metric where the anomaly was detected.
    current_value (float): The current value of the metric.
    severity (float): The severity of the anomaly (0.0 to 1.0).
"""
```

**Public Methods:**


---

### `Anomaly`

**File:** `resource_analyzer.py`

```python
class Anomaly(BaseModel):
```

**Description:**
```
"""Represents a detected anomaly in system metrics.

Attributes:
    type (AnomalyType): The type of anomaly.
    metric_name (str): The name of the metric where the anomaly was detected.
    current_value (float): The current value of the metric.
    severity (float): The severity of the anomaly (0.0 to 1.0).
"""

type: AnomalyType
metric_name: str
current_value: float
severity: float


class ResourceAnalysis(BaseModel):
```

**Public Methods:**


---

### `ResourceAnalysis`

**File:** `resource_analyzer.py`

```python
class ResourceAnalysis(BaseModel):
```

**Description:**
```
"""Represents the comprehensive analysis of system resources.

Attributes:
    timestamp (str): ISO formatted timestamp of the analysis.
    requires_action (bool): True if the analysis indicates a need for intervention.
    anomalies (List[Anomaly]): A list of detected anomalies.
    recommended_actions (List[str]): Suggested actions based on the analysis.
"""

timestamp: str
requires_action: bool
anomalies: list[Anomaly]
recommended_actions: list[str]


class ResourceAnalyzer:
```

**Public Methods:**


---

### `ResourceAnalyzer`

**File:** `resource_analyzer.py`

```python
class ResourceAnalyzer:
```

**Description:**
```
"""Performs statistical analysis on system state and historical data.

This class detects anomalies using methods like Z-score, identifies trends,
and provides recommendations for resource management.
"""

def __init__(self, anomaly_threshold_sigma: float = 3.0):
    """Initializes the ResourceAnalyzer.

    Args:
        anomaly_threshold_sigma (float): The number of standard deviations
            from the mean to consider a value an anomaly.
    """
    self.anomaly_threshold = anomaly_threshold_sigma

async def analyze_state(self, current_state: Any, history: list[Any]) -> ResourceAnalysis:
```

**Public Methods:**


---

### `ActionType`

**File:** `resource_executor.py`

```python
class ActionType(str, Enum):
```

**Description:**
```
"""Enumeration for different types of resource actions."""

SCALE_UP = "scale_up"
SCALE_DOWN = "scale_down"
OPTIMIZE_MEMORY = "optimize_memory"
NO_ACTION = "no_action"


class ExecutionResult(BaseModel):
"""Represents the outcome of executing a resource plan.

Attributes:
    timestamp (str): ISO formatted timestamp of execution.
    success (bool): True if all actions in the plan were executed successfully.
    actions_executed (List[str]): A list of actions that were successfully performed.
    errors (List[str]): Any errors encountered during execution.
```

**Public Methods:**


---

### `ExecutionResult`

**File:** `resource_executor.py`

```python
class ExecutionResult(BaseModel):
```

**Description:**
```
"""Represents the outcome of executing a resource plan.

Attributes:
    timestamp (str): ISO formatted timestamp of execution.
    success (bool): True if all actions in the plan were executed successfully.
    actions_executed (List[str]): A list of actions that were successfully performed.
    errors (List[str]): Any errors encountered during execution.
"""

timestamp: str
success: bool
actions_executed: list[str]
errors: list[str]


class ResourceExecutor:
```

**Public Methods:**


---

### `ResourceExecutor`

**File:** `resource_executor.py`

```python
class ResourceExecutor:
```

**Description:**
```
"""Executes resource management actions based on a given plan.

This class provides methods to scale workers, optimize memory, and apply
operational modes by interacting with the underlying infrastructure.
"""

def __init__(self):
    """Initializes the ResourceExecutor. (No external clients initialized here for simplicity)."""
    pass

async def execute_plan(self, plan: Any) -> ExecutionResult:
    """Executes a resource plan, performing the specified actions.

    Args:
        plan (Any): The resource plan object (e.g., ResourcePlan from ResourcePlanner).
```

**Public Methods:**


---

### `ActionType`

**File:** `resource_planner.py`

```python
class ActionType(str, Enum):
```

**Description:**
```
"""Enumeration for different types of resource management actions."""

SCALE_UP = "scale_up"
SCALE_DOWN = "scale_down"
OPTIMIZE_MEMORY = "optimize_memory"
NO_ACTION = "no_action"


class ResourcePlan(BaseModel):
"""Represents a plan for resource allocation and system adjustments.

Attributes:
    timestamp (str): ISO formatted timestamp of when the plan was created.
    target_mode (str): The desired operational mode (e.g., 'HIGH_PERFORMANCE').
    actions (List[ActionType]): A list of specific actions to be executed.
    action_intensity (float): A numerical value (0.0 to 1.0) indicating the
```

**Public Methods:**


---

### `ResourcePlan`

**File:** `resource_planner.py`

```python
class ResourcePlan(BaseModel):
```

**Description:**
```
"""Represents a plan for resource allocation and system adjustments.

Attributes:
    timestamp (str): ISO formatted timestamp of when the plan was created.
    target_mode (str): The desired operational mode (e.g., 'HIGH_PERFORMANCE').
    actions (List[ActionType]): A list of specific actions to be executed.
    action_intensity (float): A numerical value (0.0 to 1.0) indicating the
        aggressiveness of the plan.
    reasoning (str): A human-readable explanation of the plan's rationale.
"""

timestamp: str
target_mode: str
actions: list[ActionType]
action_intensity: float
reasoning: str
```

**Public Methods:**


---

### `ResourcePlanner`

**File:** `resource_planner.py`

```python
class ResourcePlanner:
```

**Description:**
```
"""Generates resource allocation plans using fuzzy logic.

This class takes system state and analysis as input and outputs a detailed
plan of actions to optimize resource usage and maintain system health.
"""

def __init__(self):
    """Initializes the ResourcePlanner and its fuzzy logic system."""
    pass

async def create_plan(self, current_state: Any, analysis: Any, current_mode: Any) -> ResourcePlan | None:
    """Creates a resource plan based on current system state and analysis.

    Args:
        current_state (Any): The current SystemState object.
        analysis (Any): The ResourceAnalysis object.
```

**Public Methods:**


---

### `SystemMonitor`

**File:** `system_monitor.py`

```python
class SystemMonitor:
```

**Description:**
```
"""Collects real-time operational metrics from the host system.

This class uses `psutil` to gather CPU, memory, disk, and network usage,
providing a comprehensive view of the system's current state.
"""

def __init__(self):
    """Initializes the SystemMonitor, setting up process and time tracking."""
    self.process = psutil.Process()  # The current process (Maximus)
    self.start_time = time.time()
    self.last_disk_io = psutil.disk_io_counters()
    self.last_net_io = psutil.net_io_counters()
    self.last_check_time = time.time()

async def collect_metrics(self) -> SystemState:
    """Collects and returns a snapshot of the current system metrics.
```

**Public Methods:**


---

### `ConfidenceTracker`

**File:** `confidence_tracker.py`

```python
class ConfidenceTracker:
```

**Description:**
```
"""Tracks confidence in ToM beliefs with exponential temporal decay.

Beliefs decay over time according to e^(-λt) formula, representing
decreasing certainty about stale mental state inferences.

Attributes:
    decay_lambda: Decay rate per hour (default: 0.01)
    min_confidence: Minimum confidence floor (default: 0.1)
"""

def __init__(self, decay_lambda: float = 0.01, min_confidence: float = 0.1):
    """Initialize ConfidenceTracker.

    Args:
        decay_lambda: Decay rate per hour (higher = faster decay)
        min_confidence: Minimum confidence threshold [0.0, 1.0]
```

**Public Methods:**

- `def calculate_confidence(self, agent_id`
- `def get_timestamps(self, agent_id`
- `def get_confidence_scores(self, agent_id`
- `def clear_old_beliefs(self, max_age_hours`

---

### `ContradictionDetector`

**File:** `contradiction_detector.py`

```python
class ContradictionDetector:
```

**Description:**
```
"""Detects contradictory belief updates in ToM inferences.

Tracks belief updates and flags contradictions when value changes
exceed a specified threshold in a single update.

Attributes:
    threshold: Minimum delta to consider a contradiction (default: 0.5)
"""

def __init__(self, threshold: float = 0.5):
    """Initialize ContradictionDetector.

    Args:
        threshold: Minimum absolute delta to flag as contradiction [0.0, 1.0]
    """
    if not 0.0 <= threshold <= 1.0:
```

**Public Methods:**

- `def get_contradictions(self, agent_id`
- `def clear_contradictions(self, agent_id`
- `def get_contradiction_rate(self, agent_id`
- `def get_all_agents(self) -> List[str]`
- `def get_stats(self) -> Dict`

---

### `SocialMemoryConfig`

**File:** `social_memory.py`

```python
class SocialMemoryConfig:
```

**Description:**
```
"""Configuration for SocialMemory PostgreSQL backend.

Attributes:
    host: PostgreSQL host
    port: PostgreSQL port
    database: Database name
    user: Database user
    password: Database password
    pool_size: Connection pool size
    cache_size: LRU cache size (number of agents)
"""

host: str = "localhost"
port: int = 5432
database: str = "maximus_dev"
user: str = "maximus"
```

**Public Methods:**


---

### `PatternNotFoundError`

**File:** `social_memory.py`

```python
class PatternNotFoundError(Exception):
```

**Description:**
```
"""Raised when pattern for agent_id is not found."""

pass


# ===========================================================================
# LRU CACHE
# ===========================================================================

class LRUCache:
"""LRU (Least Recently Used) cache implementation.

Thread-safe, bounded cache with O(1) get/put operations.
"""

def __init__(self, capacity: int):
```

**Public Methods:**


---

### `LRUCache`

**File:** `social_memory.py`

```python
class LRUCache:
```

**Description:**
```
"""LRU (Least Recently Used) cache implementation.

Thread-safe, bounded cache with O(1) get/put operations.
"""

def __init__(self, capacity: int):
    """Initialize LRU cache.

    Args:
        capacity: Maximum number of items to cache
    """
    if capacity < 1:
        raise ValueError(f"Cache capacity must be >= 1, got {capacity}")

    self.capacity = capacity
    self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
```

**Public Methods:**

- `def get_stats(self) -> Dict[str, Any]`

---

### `SocialMemory`

**File:** `social_memory.py`

```python
class SocialMemory:
```

**Description:**
```
"""Social memory storage with PostgreSQL backend and LRU cache.

Usage:
    >>> config = SocialMemoryConfig(database="maximus_dev")
    >>> memory = SocialMemory(config)
    >>> await memory.initialize()
    >>>
    >>> # Store pattern
    >>> await memory.store_pattern("user_123", {"confusion_history": 0.7})
    >>>
    >>> # Retrieve pattern
    >>> patterns = await memory.retrieve_patterns("user_123")
    >>>
    >>> # Update from interaction (EMA)
    >>> await memory.update_from_interaction("user_123", {"confusion_history": 0.5})
    >>>
```

**Public Methods:**

- `def get_stats(self) -> Dict[str, Any]`
- `def get_cache_stats(self) -> Dict[str, Any]`

---

### `SocialMemorySQLiteConfig`

**File:** `social_memory_sqlite.py`

```python
class SocialMemorySQLiteConfig:
```

**Description:**
```
"""Configuration for SQLite-based SocialMemory.

Attributes:
    db_path: Path to SQLite database file
    cache_size: LRU cache size (number of agents)
"""

db_path: str = ":memory:"  # In-memory by default for tests
cache_size: int = 100


# ===========================================================================
# EXCEPTIONS
# ===========================================================================

class PatternNotFoundError(Exception):
```

**Public Methods:**


---

### `PatternNotFoundError`

**File:** `social_memory_sqlite.py`

```python
class PatternNotFoundError(Exception):
```

**Description:**
```
"""Raised when pattern for agent_id is not found."""

pass


# ===========================================================================
# LRU CACHE (Same as PostgreSQL version)
# ===========================================================================

class LRUCache:
"""LRU (Least Recently Used) cache implementation."""

def __init__(self, capacity: int):
    if capacity < 1:
        raise ValueError(f"Cache capacity must be >= 1, got {capacity}")
```

**Public Methods:**


---

### `LRUCache`

**File:** `social_memory_sqlite.py`

```python
class LRUCache:
```

**Description:**
```
"""LRU (Least Recently Used) cache implementation."""

def __init__(self, capacity: int):
    if capacity < 1:
        raise ValueError(f"Cache capacity must be >= 1, got {capacity}")

    self.capacity = capacity
    self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
    self.hits = 0
    self.misses = 0
    self.evictions = 0
    self._lock = asyncio.Lock()

async def get(self, key: str) -> Optional[Dict[str, Any]]:
    async with self._lock:
        if key in self.cache:
```

**Public Methods:**

- `def get_stats(self) -> Dict[str, Any]`

---

### `SocialMemorySQLite`

**File:** `social_memory_sqlite.py`

```python
class SocialMemorySQLite:
```

**Description:**
```
"""SQLite-based social memory storage (development fallback).

API-compatible with PostgreSQL version for seamless switching.
"""

def __init__(self, config: SocialMemorySQLiteConfig):
    self.config = config
    self.db: Optional[aiosqlite.Connection] = None
    self.cache = LRUCache(capacity=config.cache_size)
    self._closed = False

async def initialize(self) -> None:
    """Initialize SQLite database and create schema."""
    if self._closed:
        raise RuntimeError("Cannot initialize closed SocialMemory")
```

**Public Methods:**

- `def get_stats(self) -> Dict[str, Any]`
- `def get_cache_stats(self) -> Dict[str, Any]`

---

### `ToMBenchmarkRunner`

**File:** `tom_benchmark.py`

```python
class ToMBenchmarkRunner:
```

**Description:**
```
"""Runs Theory of Mind benchmarks using Sally-Anne scenarios.

Validates false belief tracking accuracy against 10 test scenarios.

Attributes:
    results: List of benchmark results (one per scenario)
    total_scenarios: Total number of scenarios run
    correct_count: Number of correct predictions
"""

def __init__(self):
    """Initialize ToMBenchmarkRunner."""
    self.results: List[Dict[str, Any]] = []
    self.total_scenarios = 0
    self.correct_count = 0
```

**Public Methods:**

- `def get_accuracy(self) -> float`
- `def get_report(self) -> Dict[str, Any]`
- `def get_errors(self) -> List[Dict[str, Any]]`
- `def get_accuracy_by_difficulty(self) -> Dict[str, float]`
- `def reset(self) -> None`

---

### `ToMEngine`

**File:** `tom_engine.py`

```python
class ToMEngine:
```

**Description:**
```
"""Complete Theory of Mind engine for mental state inference.

Combines social memory, confidence tracking, and contradiction detection
to build robust models of other agents' beliefs, intentions, and knowledge.

Key Capabilities:
- False belief tracking (Sally-Anne scenarios)
- Confidence decay over time
- Contradiction detection
- Persistent social memory

Attributes:
    social_memory: Persistent storage for agent beliefs
    confidence_tracker: Temporal decay for belief confidence
    contradiction_detector: Validation for belief updates
"""
```

**Public Methods:**

- `def get_contradictions(self, agent_id`
- `def get_contradiction_rate(self, agent_id`

---

### `RegulationType`

**File:** `base.py`

```python
class RegulationType(Enum):
```

**Description:**
```
"""Supported regulatory frameworks."""

EU_AI_ACT = "eu_ai_act"  # EU Artificial Intelligence Act (High-Risk AI)
GDPR = "gdpr"  # General Data Protection Regulation (Article 22)
NIST_AI_RMF = "nist_ai_rmf"  # NIST AI Risk Management Framework 1.0
US_EO_14110 = "us_eo_14110"  # US Executive Order 14110 (Safe, Secure AI)
BRAZIL_LGPD = "brazil_lgpd"  # Lei Geral de Proteção de Dados
ISO_27001 = "iso_27001"  # ISO/IEC 27001:2022 (Information Security)
SOC2_TYPE_II = "soc2_type_ii"  # SOC 2 Type II (Trust Services)
IEEE_7000 = "ieee_7000"  # IEEE 7000-2021 (Ethical AI Design)


class ControlCategory(Enum):
"""Categories of compliance controls."""

TECHNICAL = "technical"  # Technical safeguards (encryption, access control)
```

**Public Methods:**


---

### `ControlCategory`

**File:** `base.py`

```python
class ControlCategory(Enum):
```

**Description:**
```
"""Categories of compliance controls."""

TECHNICAL = "technical"  # Technical safeguards (encryption, access control)
ORGANIZATIONAL = "organizational"  # Policies, procedures, training
DOCUMENTATION = "documentation"  # Required documentation and records
TESTING = "testing"  # Testing and validation requirements
MONITORING = "monitoring"  # Continuous monitoring and alerting
GOVERNANCE = "governance"  # Governance structures and oversight
SECURITY = "security"  # Security controls and measures
PRIVACY = "privacy"  # Privacy protection controls


class ComplianceStatus(Enum):
"""Status of compliance checks."""

COMPLIANT = "compliant"  # Fully compliant with requirement
```

**Public Methods:**


---

### `ComplianceStatus`

**File:** `base.py`

```python
class ComplianceStatus(Enum):
```

**Description:**
```
"""Status of compliance checks."""

COMPLIANT = "compliant"  # Fully compliant with requirement
NON_COMPLIANT = "non_compliant"  # Not compliant, violation detected
PARTIALLY_COMPLIANT = "partially_compliant"  # Partially compliant, gaps exist
NOT_APPLICABLE = "not_applicable"  # Control not applicable to current scope
PENDING_REVIEW = "pending_review"  # Awaiting manual review
EVIDENCE_REQUIRED = "evidence_required"  # Missing required evidence
REMEDIATION_IN_PROGRESS = "remediation_in_progress"  # Fixes being implemented


class ViolationSeverity(Enum):
"""Severity levels for compliance violations."""

CRITICAL = "critical"  # Critical violation, immediate action required
HIGH = "high"  # High severity, urgent remediation needed
```

**Public Methods:**


---

### `ViolationSeverity`

**File:** `base.py`

```python
class ViolationSeverity(Enum):
```

**Description:**
```
"""Severity levels for compliance violations."""

CRITICAL = "critical"  # Critical violation, immediate action required
HIGH = "high"  # High severity, urgent remediation needed
MEDIUM = "medium"  # Medium severity, remediation required
LOW = "low"  # Low severity, should be addressed
INFORMATIONAL = "informational"  # Informational finding, no immediate action


class EvidenceType(Enum):
"""Types of compliance evidence."""

LOG = "log"  # System logs, audit logs
DOCUMENT = "document"  # Policy documents, procedures, manuals
SCREENSHOT = "screenshot"  # Screenshots of configurations, dashboards
TEST_RESULT = "test_result"  # Test execution results
```

**Public Methods:**


---

### `EvidenceType`

**File:** `base.py`

```python
class EvidenceType(Enum):
```

**Description:**
```
"""Types of compliance evidence."""

LOG = "log"  # System logs, audit logs
DOCUMENT = "document"  # Policy documents, procedures, manuals
SCREENSHOT = "screenshot"  # Screenshots of configurations, dashboards
TEST_RESULT = "test_result"  # Test execution results
AUDIT_REPORT = "audit_report"  # Third-party audit reports
CONFIGURATION = "configuration"  # System/service configuration files
CODE_REVIEW = "code_review"  # Code review records
POLICY = "policy"  # Organizational policies
TRAINING_RECORD = "training_record"  # Training completion records
INCIDENT_REPORT = "incident_report"  # Security incident reports
RISK_ASSESSMENT = "risk_assessment"  # Risk assessment documents
CERTIFICATION = "certification"  # Certification documents
```

**Public Methods:**


---

### `RemediationStatus`

**File:** `base.py`

```python
class RemediationStatus(Enum):
```

**Description:**
```
"""Status of remediation efforts."""

NOT_STARTED = "not_started"
IN_PROGRESS = "in_progress"
BLOCKED = "blocked"
COMPLETED = "completed"
VERIFIED = "verified"
FAILED = "failed"


# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================


@dataclass
```

**Public Methods:**


---

### `Control`

**File:** `base.py`

```python
class Control:
```

**Description:**
```
"""
Individual compliance control.

Represents a specific requirement from a regulation that must be satisfied.
"""

control_id: str  # Unique control identifier (e.g., "EU-AI-ACT-ART-9")
regulation_type: RegulationType  # Parent regulation
category: ControlCategory  # Control category
title: str  # Control title
description: str  # Detailed description of requirement
mandatory: bool = True  # Whether control is mandatory
test_procedure: str | None = None  # How to test compliance
evidence_required: list[EvidenceType] = field(default_factory=list)
reference: str | None = None  # Citation (e.g., "Article 9, Section 2")
tags: set[str] = field(default_factory=set)  # Tags for filtering
```

**Public Methods:**


---

### `Regulation`

**File:** `base.py`

```python
class Regulation:
```

**Description:**
```
"""
Complete regulation definition.

Defines a regulatory framework with all its controls and requirements.
"""

regulation_type: RegulationType
name: str  # Full name (e.g., "EU Artificial Intelligence Act")
version: str  # Regulation version
effective_date: datetime  # When regulation becomes effective
jurisdiction: str  # Geographic jurisdiction (e.g., "EU", "USA", "Brazil")
description: str  # High-level description
controls: list[Control] = field(default_factory=list)
scope: str | None = None  # Applicability scope
penalties: str | None = None  # Non-compliance penalties
update_frequency_days: int = 90  # How often to review for updates
```

**Public Methods:**

- `def get_mandatory_controls(self) -> list[Control]`
- `def get_controls_by_category(self, category`
- `def get_control(self, control_id`

---

### `Evidence`

**File:** `base.py`

```python
class Evidence:
```

**Description:**
```
"""
Evidence item supporting compliance.

Documents proof of compliance with specific controls.
"""

evidence_id: str = field(default_factory=lambda: str(uuid.uuid4()))
evidence_type: EvidenceType = EvidenceType.DOCUMENT
control_id: str = ""  # Associated control
title: str = ""
description: str = ""
collected_at: datetime = field(default_factory=datetime.utcnow)
collected_by: str | None = None  # User/system that collected evidence
file_path: str | None = None  # Path to evidence file
file_hash: str | None = None  # SHA-256 hash for integrity
metadata: dict[str, Any] = field(default_factory=dict)
```

**Public Methods:**

- `def is_expired(self) -> bool`
- `def verify(self, verified_by`

---

### `ComplianceViolation`

**File:** `base.py`

```python
class ComplianceViolation:
```

**Description:**
```
"""
Compliance violation details.

Documents a specific non-compliance finding.
"""

violation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
control_id: str = ""  # Violated control
regulation_type: RegulationType = RegulationType.ISO_27001
severity: ViolationSeverity = ViolationSeverity.MEDIUM
title: str = ""
description: str = ""  # What was violated
detected_at: datetime = field(default_factory=datetime.utcnow)
detected_by: str = "system"  # System or auditor name
impact: str | None = None  # Business/security impact
recommendation: str | None = None  # Remediation recommendation
```

**Public Methods:**

- `def resolve(self, resolved_by`
- `def get_age_hours(self) -> float`

---

### `ComplianceResult`

**File:** `base.py`

```python
class ComplianceResult:
```

**Description:**
```
"""
Result of compliance check.

Documents the outcome of checking compliance for a specific control.
"""

check_id: str = field(default_factory=lambda: str(uuid.uuid4()))
control_id: str = ""
regulation_type: RegulationType = RegulationType.ISO_27001
status: ComplianceStatus = ComplianceStatus.PENDING_REVIEW
checked_at: datetime = field(default_factory=datetime.utcnow)
checked_by: str = "system"
score: float | None = None  # Compliance score 0.0-1.0
evidence: list[Evidence] = field(default_factory=list)
violations: list[ComplianceViolation] = field(default_factory=list)
notes: str | None = None
```

**Public Methods:**

- `def is_compliant(self) -> bool`
- `def has_violations(self) -> bool`
- `def get_critical_violations(self) -> list[ComplianceViolation]`

---

### `Gap`

**File:** `base.py`

```python
class Gap:
```

**Description:**
```
"""
Compliance gap identified during gap analysis.
"""

gap_id: str = field(default_factory=lambda: str(uuid.uuid4()))
control_id: str = ""
regulation_type: RegulationType = RegulationType.ISO_27001
title: str = ""
description: str = ""
severity: ViolationSeverity = ViolationSeverity.MEDIUM
current_state: str = ""  # Current implementation status
required_state: str = ""  # Required implementation status
gap_type: str = "missing_control"  # missing_control, partial_implementation, outdated
identified_at: datetime = field(default_factory=datetime.utcnow)
estimated_effort_hours: int | None = None
priority: int = 3  # 1 (highest) to 5 (lowest)
```

**Public Methods:**


---

### `RemediationAction`

**File:** `base.py`

```python
class RemediationAction:
```

**Description:**
```
"""
Action to remediate a compliance gap.
"""

action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
gap_id: str = ""
title: str = ""
description: str = ""
assigned_to: str | None = None
due_date: datetime | None = None
status: RemediationStatus = RemediationStatus.NOT_STARTED
estimated_hours: int | None = None
actual_hours: int | None = None
blockers: list[str] = field(default_factory=list)
dependencies: list[str] = field(default_factory=list)  # Other action IDs
completion_percentage: int = 0
```

**Public Methods:**

- `def is_overdue(self) -> bool`

---

### `RemediationPlan`

**File:** `base.py`

```python
class RemediationPlan:
```

**Description:**
```
"""
Complete remediation plan for compliance gaps.
"""

plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
regulation_type: RegulationType = RegulationType.ISO_27001
created_at: datetime = field(default_factory=datetime.utcnow)
created_by: str = ""
gaps: list[Gap] = field(default_factory=list)
actions: list[RemediationAction] = field(default_factory=list)
target_completion_date: datetime | None = None
status: str = "draft"  # draft, approved, in_progress, completed
approved_by: str | None = None
approved_at: datetime | None = None

def __post_init__(self):
```

**Public Methods:**

- `def get_critical_gaps(self) -> list[Gap]`
- `def get_overdue_actions(self) -> list[RemediationAction]`
- `def get_completion_percentage(self) -> float`

---

### `GapAnalysisResult`

**File:** `base.py`

```python
class GapAnalysisResult:
```

**Description:**
```
"""
Result of gap analysis for a regulation.
"""

analysis_id: str = field(default_factory=lambda: str(uuid.uuid4()))
regulation_type: RegulationType = RegulationType.ISO_27001
analyzed_at: datetime = field(default_factory=datetime.utcnow)
analyzed_by: str = "system"
total_controls: int = 0
compliant_controls: int = 0
non_compliant_controls: int = 0
partially_compliant_controls: int = 0
gaps: list[Gap] = field(default_factory=list)
compliance_percentage: float = 0.0
remediation_plan: RemediationPlan | None = None
estimated_remediation_hours: int = 0
```

**Public Methods:**

- `def get_gaps_by_severity(self, severity`
- `def is_certification_ready(self, threshold`

---

### `ComplianceConfig`

**File:** `base.py`

```python
class ComplianceConfig:
```

**Description:**
```
"""
Configuration for compliance engine.
"""

# Scope
enabled_regulations: list[RegulationType] = field(
    default_factory=lambda: [
        RegulationType.EU_AI_ACT,
        RegulationType.GDPR,
        RegulationType.NIST_AI_RMF,
        RegulationType.ISO_27001,
    ]
)

# Automation
auto_collect_evidence: bool = True
```

**Public Methods:**

- `def is_regulation_enabled(self, regulation_type`

---

### `CertificationResult`

**File:** `certifications.py`

```python
class CertificationResult:
```

**Description:**
```
"""
Result of certification readiness check.
"""

certification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
regulation_type: RegulationType = RegulationType.ISO_27001
checked_at: datetime = field(default_factory=datetime.utcnow)
certification_ready: bool = False
compliance_percentage: float = 0.0
score: float = 0.0
required_threshold: float = 95.0
gaps_to_certification: int = 0
critical_gaps: list[str] = field(default_factory=list)  # control_ids
recommendations: list[str] = field(default_factory=list)
estimated_days_to_certification: int = 0
compliance_results: list[ComplianceResult] = field(default_factory=list)
```

**Public Methods:**

- `def get_summary(self) -> str`

---

### `ISO27001Checker`

**File:** `certifications.py`

```python
class ISO27001Checker:
```

**Description:**
```
"""
ISO/IEC 27001:2022 certification checker.

Checks certification readiness for ISO 27001 Information Security Management System.
"""

def __init__(
    self,
    compliance_engine: ComplianceEngine,
    evidence_collector: EvidenceCollector | None = None,
):
    """
    Initialize ISO 27001 checker.

    Args:
        compliance_engine: Compliance engine instance
```

**Public Methods:**

- `def check_certification_readiness(`

---

### `SOC2Checker`

**File:** `certifications.py`

```python
class SOC2Checker:
```

**Description:**
```
"""
SOC 2 Type II certification checker.

Checks certification readiness for SOC 2 Type II audit (Security, Availability,
Processing Integrity, Confidentiality).
"""

def __init__(
    self,
    compliance_engine: ComplianceEngine,
    evidence_collector: EvidenceCollector | None = None,
):
    """
    Initialize SOC 2 checker.

    Args:
```

**Public Methods:**

- `def check_certification_readiness(`

---

### `IEEE7000Checker`

**File:** `certifications.py`

```python
class IEEE7000Checker:
```

**Description:**
```
"""
IEEE 7000-2021 certification checker.

Checks certification readiness for IEEE 7000 Ethical AI Design standard.
"""

def __init__(
    self,
    compliance_engine: ComplianceEngine,
    evidence_collector: EvidenceCollector | None = None,
):
    """
    Initialize IEEE 7000 checker.

    Args:
        compliance_engine: Compliance engine instance
```

**Public Methods:**

- `def check_certification_readiness(`

---

### `ComplianceCheckResult`

**File:** `compliance_engine.py`

```python
class ComplianceCheckResult:
```

**Description:**
```
"""
Result of running compliance check for a regulation.
"""

regulation_type: RegulationType
checked_at: datetime
total_controls: int
controls_checked: int
compliant: int
non_compliant: int
partially_compliant: int
not_applicable: int
pending_review: int
evidence_required: int
results: list[ComplianceResult] = field(default_factory=list)
violations: list[ComplianceViolation] = field(default_factory=list)
```

**Public Methods:**

- `def is_certification_ready(self, threshold`
- `def get_critical_violations(self) -> list[ComplianceViolation]`

---

### `ComplianceSnapshot`

**File:** `compliance_engine.py`

```python
class ComplianceSnapshot:
```

**Description:**
```
"""
Point-in-time snapshot of overall compliance status.
"""

snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
timestamp: datetime = field(default_factory=datetime.utcnow)
regulation_results: dict[RegulationType, ComplianceCheckResult] = field(default_factory=dict)
overall_compliance_percentage: float = 0.0
overall_score: float = 0.0
total_violations: int = 0
critical_violations: int = 0

def __post_init__(self):
    """Calculate overall metrics."""
    if self.regulation_results:
        # Average compliance percentage across regulations
```

**Public Methods:**


---

### `ComplianceEngine`

**File:** `compliance_engine.py`

```python
class ComplianceEngine:
```

**Description:**
```
"""
Core compliance checking engine.

Orchestrates automated compliance checks across all supported regulations.
Extensible through custom control checkers.
"""

def __init__(self, config: ComplianceConfig | None = None):
    """
    Initialize compliance engine.

    Args:
        config: Compliance configuration (uses default if None)
    """
    self.config = config or ComplianceConfig()
    self._control_checkers: dict[str, ControlChecker] = {}
```

**Public Methods:**

- `def register_control_checker(self, control_id`
- `def register_category_checker(self, category`
- `def check_control(`
- `def check_compliance(`
- `def run_all_checks(`
- `def get_compliance_status(`
- `def generate_compliance_report(`

---

### `EvidenceItem`

**File:** `evidence_collector.py`

```python
class EvidenceItem:
```

**Description:**
```
"""
Single evidence item with metadata and integrity information.
"""

evidence: Evidence
file_size: int = 0
collected_from: str = ""  # Source path/system
integrity_verified: bool = False
verification_timestamp: datetime | None = None

def verify_integrity(self, file_path: str) -> bool:
    """
    Verify evidence file integrity using SHA-256 hash.

    Args:
        file_path: Path to evidence file
```

**Public Methods:**

- `def verify_integrity(self, file_path`

---

### `EvidencePackage`

**File:** `evidence_collector.py`

```python
class EvidencePackage:
```

**Description:**
```
"""
Package of evidence for audit/compliance check.
"""

package_id: str = field(default_factory=lambda: str(uuid.uuid4()))
regulation_type: RegulationType = RegulationType.ISO_27001
created_at: datetime = field(default_factory=datetime.utcnow)
created_by: str = "evidence_collector"
control_ids: list[str] = field(default_factory=list)
evidence_items: list[EvidenceItem] = field(default_factory=list)
package_path: str | None = None
total_size_bytes: int = 0
manifest: dict[str, any] = field(default_factory=dict)

def __post_init__(self):
    """Calculate package metadata."""
```

**Public Methods:**

- `def get_evidence_for_control(self, control_id`

---

### `EvidenceCollector`

**File:** `evidence_collector.py`

```python
class EvidenceCollector:
```

**Description:**
```
"""
Automated evidence collection system.

Collects evidence from multiple sources and organizes by control.
"""

def __init__(self, config: ComplianceConfig | None = None):
    """
    Initialize evidence collector.

    Args:
        config: Compliance configuration
    """
    self.config = config or ComplianceConfig()
    self._evidence_cache: dict[str, list[EvidenceItem]] = {}  # control_id -> evidence
```

**Public Methods:**

- `def collect_log_evidence(`
- `def collect_configuration_evidence(`
- `def collect_test_evidence(`
- `def collect_document_evidence(`
- `def collect_policy_evidence(`
- `def get_evidence_for_control(self, control_id`
- `def get_all_evidence(self) -> dict[str, list[Evidence]]`
- `def create_evidence_package(`
- `def export_evidence_package(`
- `def verify_all_evidence(self) -> dict[str, bool]`
- `def get_expired_evidence(self) -> list[Evidence]`

---

### `GapAnalyzer`

**File:** `gap_analyzer.py`

```python
class GapAnalyzer:
```

**Description:**
```
"""
Compliance gap analyzer and remediation planner.

Identifies compliance gaps and generates prioritized remediation plans.
"""

def __init__(self, config: ComplianceConfig | None = None):
    """
    Initialize gap analyzer.

    Args:
        config: Compliance configuration
    """
    self.config = config or ComplianceConfig()
    logger.info("Gap analyzer initialized")
```

**Public Methods:**

- `def analyze_compliance_gaps(`
- `def create_remediation_plan(`
- `def prioritize_gaps(`
- `def track_remediation_progress(`
- `def estimate_remediation_effort(`

---

### `ComplianceAlert`

**File:** `monitoring.py`

```python
class ComplianceAlert:
```

**Description:**
```
"""
Compliance alert notification.
"""

alert_id: str = field(default_factory=lambda: str(uuid.uuid4()))
alert_type: str = ""  # violation, threshold_breach, evidence_expiring, remediation_overdue
severity: ViolationSeverity = ViolationSeverity.MEDIUM
title: str = ""
message: str = ""
regulation_type: RegulationType | None = None
triggered_at: datetime = field(default_factory=datetime.utcnow)
acknowledged: bool = False
acknowledged_by: str | None = None
acknowledged_at: datetime | None = None
metadata: dict[str, any] = field(default_factory=dict)
```

**Public Methods:**

- `def acknowledge(self, acknowledged_by`

---

### `MonitoringMetrics`

**File:** `monitoring.py`

```python
class MonitoringMetrics:
```

**Description:**
```
"""
Compliance monitoring metrics snapshot.
"""

snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
timestamp: datetime = field(default_factory=datetime.utcnow)
overall_compliance_percentage: float = 0.0
overall_score: float = 0.0
compliance_by_regulation: dict[str, float] = field(default_factory=dict)
total_violations: int = 0
critical_violations: int = 0
high_violations: int = 0
medium_violations: int = 0
low_violations: int = 0
total_evidence: int = 0
expired_evidence: int = 0
```

**Public Methods:**


---

### `ComplianceMonitor`

**File:** `monitoring.py`

```python
class ComplianceMonitor:
```

**Description:**
```
"""
Continuous compliance monitoring system.

Monitors compliance status, detects violations, and sends alerts.
"""

def __init__(
    self,
    compliance_engine: ComplianceEngine,
    evidence_collector: EvidenceCollector | None = None,
    gap_analyzer: GapAnalyzer | None = None,
    config: ComplianceConfig | None = None,
):
    """
    Initialize compliance monitor.
```

**Public Methods:**

- `def register_alert_handler(self, handler`
- `def start_monitoring(self, check_interval_seconds`
- `def stop_monitoring(self)`
- `def get_current_metrics(self) -> MonitoringMetrics | None`
- `def get_metrics_history(`
- `def get_alerts(`
- `def acknowledge_alert(self, alert_id`
- `def generate_dashboard_data(self) -> dict[str, any]`

---

### `ConfidenceScoring`

**File:** `confidence_scoring.py`

```python
class ConfidenceScoring:
```

**Description:**
```
"""Evaluates and assigns a confidence score to Maximus AI's responses.

The confidence score reflects the AI's certainty in the accuracy, completeness,
and relevance of its output.
"""

def __init__(self):
    """Initializes the ConfidenceScoring module."""
    pass

async def score(self, response: dict[str, Any] | str, context: dict[str, Any]) -> float:
    """Calculates a confidence score for the given response.

    Args:
        response (Dict[str, Any] | str): The AI's generated response (can be dict or string).
        context (Dict[str, Any]): The context in which the response was generated.
```

**Public Methods:**


---

### `SalienceInput`

**File:** `api.py`

```python
class SalienceInput(BaseModel):
```

**Description:**
```
"""Salience score for manual ESGT trigger."""

novelty: float = Field(..., ge=0.0, le=1.0, description="Novelty component [0-1]")
relevance: float = Field(..., ge=0.0, le=1.0, description="Relevance component [0-1]")
urgency: float = Field(..., ge=0.0, le=1.0, description="Urgency component [0-1]")
context: dict[str, Any] = Field(default_factory=dict, description="Additional context")


class ArousalAdjustment(BaseModel):
"""Arousal level adjustment request."""

delta: float = Field(..., ge=-0.5, le=0.5, description="Arousal change [-0.5, +0.5]")
duration_seconds: float = Field(default=5.0, ge=0.1, le=60.0, description="Duration (seconds)")
source: str = Field(default="manual", description="Source identifier")
```

**Public Methods:**


---

### `ArousalAdjustment`

**File:** `api.py`

```python
class ArousalAdjustment(BaseModel):
```

**Description:**
```
"""Arousal level adjustment request."""

delta: float = Field(..., ge=-0.5, le=0.5, description="Arousal change [-0.5, +0.5]")
duration_seconds: float = Field(default=5.0, ge=0.1, le=60.0, description="Duration (seconds)")
source: str = Field(default="manual", description="Source identifier")


class ConsciousnessStateResponse(BaseModel):
"""Complete consciousness state snapshot."""

timestamp: str
esgt_active: bool
arousal_level: float
arousal_classification: str
tig_metrics: dict[str, Any]
recent_events_count: int
```

**Public Methods:**


---

### `ConsciousnessStateResponse`

**File:** `api.py`

```python
class ConsciousnessStateResponse(BaseModel):
```

**Description:**
```
"""Complete consciousness state snapshot."""

timestamp: str
esgt_active: bool
arousal_level: float
arousal_classification: str
tig_metrics: dict[str, Any]
recent_events_count: int
system_health: str


class ESGTEventResponse(BaseModel):
"""ESGT ignition event."""

event_id: str
timestamp: str
```

**Public Methods:**


---

### `ESGTEventResponse`

**File:** `api.py`

```python
class ESGTEventResponse(BaseModel):
```

**Description:**
```
"""ESGT ignition event."""

event_id: str
timestamp: str
success: bool
salience: dict[str, float]
coherence: float | None
duration_ms: float | None
nodes_participating: int
reason: str | None


class SafetyStatusResponse(BaseModel):
"""Safety protocol status (FASE VII)."""

monitoring_active: bool
```

**Public Methods:**


---

### `SafetyStatusResponse`

**File:** `api.py`

```python
class SafetyStatusResponse(BaseModel):
```

**Description:**
```
"""Safety protocol status (FASE VII)."""

monitoring_active: bool
kill_switch_active: bool
violations_total: int
violations_by_severity: dict[str, int]
last_violation: str | None
uptime_seconds: float


class SafetyViolationResponse(BaseModel):
"""Safety violation event (FASE VII)."""

violation_id: str
violation_type: str
severity: str
```

**Public Methods:**


---

### `SafetyViolationResponse`

**File:** `api.py`

```python
class SafetyViolationResponse(BaseModel):
```

**Description:**
```
"""Safety violation event (FASE VII)."""

violation_id: str
violation_type: str
severity: str
timestamp: str
value_observed: float
threshold_violated: float
message: str
context: dict[str, Any]


class EmergencyShutdownRequest(BaseModel):
"""Emergency shutdown request (HITL only - FASE VII)."""

reason: str = Field(..., min_length=10, description="Human-readable reason (min 10 chars)")
```

**Public Methods:**


---

### `EmergencyShutdownRequest`

**File:** `api.py`

```python
class EmergencyShutdownRequest(BaseModel):
```

**Description:**
```
"""Emergency shutdown request (HITL only - FASE VII)."""

reason: str = Field(..., min_length=10, description="Human-readable reason (min 10 chars)")
allow_override: bool = Field(default=True, description="Allow HITL override (5s window)")


# ==================== API FACTORY ====================


def create_consciousness_api(consciousness_system: dict[str, Any]) -> APIRouter:
"""Create consciousness API router.

Args:
    consciousness_system: Dict with keys:
        - 'tig': TIGFabric instance
        - 'esgt': ESGTCoordinator instance
```

**Public Methods:**

- `def add_event_to_history(event`

---

### `ArousalLevel`

**File:** `controller_old.py`

```python
class ArousalLevel(Enum):
```

**Description:**
```
"""Classification of arousal states."""

SLEEP = "sleep"  # 0.0-0.2: Minimal/no consciousness
DROWSY = "drowsy"  # 0.2-0.4: Reduced awareness
RELAXED = "relaxed"  # 0.4-0.6: Normal baseline
ALERT = "alert"  # 0.6-0.8: Heightened awareness
HYPERALERT = "hyperalert"  # 0.8-1.0: Stress/panic state


@dataclass
class ArousalState:
"""
Current arousal state.

Represents the global excitability/wakefulness level.
"""
```

**Public Methods:**


---

### `ArousalState`

**File:** `controller_old.py`

```python
class ArousalState:
```

**Description:**
```
"""
Current arousal state.

Represents the global excitability/wakefulness level.
"""

# Core arousal value (0.0 - 1.0)
arousal: float = 0.6  # Default: RELAXED

# Classification
level: ArousalLevel = field(default=ArousalLevel.RELAXED, init=False)

# Contributing factors (for transparency)
baseline_arousal: float = 0.6
need_contribution: float = 0.0  # From MMEI needs
external_contribution: float = 0.0  # From threats/tasks
```

**Public Methods:**

- `def get_arousal_factor(self) -> float`
- `def compute_effective_threshold(self, base_threshold`

---

### `ArousalModulation`

**File:** `controller_old.py`

```python
class ArousalModulation:
```

**Description:**
```
"""
Request to modulate arousal.

External systems can request arousal changes (e.g., threat detection).
"""

source: str  # What requested modulation
delta: float  # Change in arousal (-1.0 to +1.0)
duration_seconds: float = 0.0  # How long effect lasts (0 = instant)
priority: int = 1  # Higher priority overrides

timestamp: float = field(default_factory=time.time)

def is_expired(self) -> bool:
    """Check if modulation has expired."""
    if self.duration_seconds == 0.0:
```

**Public Methods:**

- `def is_expired(self) -> bool`
- `def get_current_delta(self) -> float`

---

### `ArousalConfig`

**File:** `controller_old.py`

```python
class ArousalConfig:
```

**Description:**
```
"""Configuration for arousal controller."""

# Baseline arousal (resting state)
baseline_arousal: float = 0.6  # RELAXED default

# Update rate
update_interval_ms: float = 100.0  # 10 Hz

# Time constants (how fast arousal changes)
arousal_increase_rate: float = 0.05  # Per second when increasing
arousal_decrease_rate: float = 0.02  # Per second when decreasing (slower)

# Need influence (how much MMEI needs affect arousal)
repair_need_weight: float = 0.3  # Errors increase arousal
rest_need_weight: float = -0.2  # Fatigue decreases arousal
efficiency_need_weight: float = 0.1
```

**Public Methods:**


---

### `ArousalController`

**File:** `controller_old.py`

```python
class ArousalController:
```

**Description:**
```
"""
Controls global arousal/excitability state.

This is the MPE foundation - contentless wakefulness that modulates
readiness for conscious experience (ESGT ignition).

The controller continuously updates arousal based on:
- Internal needs (MMEI)
- External events (threats, tasks)
- Temporal dynamics (stress, recovery, circadian)
- ESGT history (refractory periods)

Architecture:
-------------
Needs + External → Arousal Update → ESGT Threshold Modulation
```

**Public Methods:**

- `def register_arousal_callback(self, callback`
- `def get_current_arousal(self) -> ArousalState`
- `def get_esgt_threshold(self) -> float`
- `def request_modulation(self, source`
- `def update_from_needs(self, needs`
- `def apply_esgt_refractory(self) -> None`
- `def get_stress_level(self) -> float`
- `def reset_stress(self) -> None`
- `def get_statistics(self) -> dict[str, any]`

---

### `ESGTPhase`

**File:** `coordinator_old.py`

```python
class ESGTPhase(Enum):
```

**Description:**
```
"""Phases of ESGT ignition protocol."""

IDLE = "idle"
PREPARE = "prepare"
SYNCHRONIZE = "synchronize"
BROADCAST = "broadcast"
SUSTAIN = "sustain"
DISSOLVE = "dissolve"
COMPLETE = "complete"
FAILED = "failed"


class SalienceLevel(Enum):
"""Classification of information salience."""

MINIMAL = "minimal"  # <0.25 - background noise
```

**Public Methods:**


---

### `SalienceLevel`

**File:** `coordinator_old.py`

```python
class SalienceLevel(Enum):
```

**Description:**
```
"""Classification of information salience."""

MINIMAL = "minimal"  # <0.25 - background noise
LOW = "low"  # 0.25-0.50 - peripheral awareness
MEDIUM = "medium"  # 0.50-0.75 - candidate for consciousness
HIGH = "high"  # 0.75-0.85 - likely conscious
CRITICAL = "critical"  # >0.85 - definitely conscious


@dataclass
class SalienceScore:
"""
Multi-factor salience score determining ESGT trigger.

Salience = α(Novelty) + β(Relevance) + γ(Urgency) + δ(Confidence)
```

**Public Methods:**


---

### `SalienceScore`

**File:** `coordinator_old.py`

```python
class SalienceScore:
```

**Description:**
```
"""
Multi-factor salience score determining ESGT trigger.

Salience = α(Novelty) + β(Relevance) + γ(Urgency) + δ(Confidence)

Where coefficients sum to 1.0 and are dynamically adjusted based
on arousal state (MCEA) and attention parameters (acetylcholine).
"""

novelty: float = 0.0  # 0-1, how unexpected
relevance: float = 0.0  # 0-1, goal-alignment
urgency: float = 0.0  # 0-1, time-criticality
confidence: float = 1.0  # 0-1, prediction confidence (default: high confidence)

# Weights (sum to 1.0)
alpha: float = 0.25  # Novelty weight
```

**Public Methods:**

- `def compute_total(self) -> float`
- `def get_level(self) -> SalienceLevel`

---

### `TriggerConditions`

**File:** `coordinator_old.py`

```python
class TriggerConditions:
```

**Description:**
```
"""
Conditions required for ESGT initiation.

All conditions must be met for ignition to proceed. This prevents
pathological synchronization and ensures computational resources
are available.
"""

# Salience threshold
min_salience: float = 0.60  # Typical threshold for consciousness

# Resource requirements
max_tig_latency_ms: float = 5.0  # TIG must be responsive
min_available_nodes: int = 8  # Minimum participating nodes
min_cpu_capacity: float = 0.40  # 40% CPU available
```

**Public Methods:**

- `def check_salience(self, score`
- `def check_resources(self, tig_latency_ms`
- `def check_temporal_gating(`
- `def check_arousal(self, arousal_level`

---

### `ESGTEvent`

**File:** `coordinator_old.py`

```python
class ESGTEvent:
```

**Description:**
```
"""
Represents a single transient global synchronization event.

This is the computational analog of a conscious moment - a discrete
episode where distributed information becomes unified, globally
accessible, and reportable.
"""

event_id: str
timestamp_start: float
timestamp_end: float | None = None

# Content
content: dict[str, Any] = field(default_factory=dict)
content_source: str = ""  # SPM that contributed content
```

**Public Methods:**

- `def transition_phase(self, new_phase`
- `def finalize(self, success`
- `def get_duration_ms(self) -> float`
- `def was_successful(self) -> bool`

---

### `ESGTCoordinator`

**File:** `coordinator_old.py`

```python
class ESGTCoordinator:
```

**Description:**
```
"""
Coordinates ESGT ignition events for consciousness emergence.

This coordinator implements the full GWD ignition protocol, managing
the transition from unconscious distributed processing to unified
conscious experience.

The coordinator:
1. Monitors salience scores continuously
2. Evaluates trigger conditions
3. Initiates synchronization when threshold met
4. Manages 5-phase ESGT protocol
5. Records metrics for consciousness validation

Usage:
    coordinator = ESGTCoordinator(
```

**Public Methods:**

- `def get_success_rate(self) -> float`
- `def get_recent_coherence(self, window`

---

### `NodeState`

**File:** `fabric_old.py`

```python
class NodeState(Enum):
```

**Description:**
```
"""Operational state of a TIG node."""

INITIALIZING = "initializing"
ACTIVE = "active"
ESGT_MODE = "esgt_mode"  # High-coherence mode during global sync events
DEGRADED = "degraded"
OFFLINE = "offline"


@dataclass
class TIGConnection:
"""
Represents a bidirectional link between TIG nodes.

This connection model mirrors synaptic connections in biological neural
networks, with dynamic weights representing connection strength/importance.
```

**Public Methods:**


---

### `TIGConnection`

**File:** `fabric_old.py`

```python
class TIGConnection:
```

**Description:**
```
"""
Represents a bidirectional link between TIG nodes.

This connection model mirrors synaptic connections in biological neural
networks, with dynamic weights representing connection strength/importance.
"""

remote_node_id: str
bandwidth_bps: int = 10_000_000_000  # 10 Gbps default
latency_us: float = 1.0  # microseconds
packet_loss: float = 0.0  # 0.0-1.0
active: bool = True
weight: float = 1.0  # Dynamic routing weight (modulated by importance)

def get_effective_capacity(self) -> float:
    """
```

**Public Methods:**

- `def get_effective_capacity(self) -> float`

---

### `ProcessingState`

**File:** `fabric_old.py`

```python
class ProcessingState:
```

**Description:**
```
"""
Encapsulates the current computational state of a TIG node.

This state representation enables consciousness-relevant metrics:
- Attention level: resource allocation for salient information
- Load metrics: computational capacity and utilization
- Phase sync: oscillatory synchronization for ESGT coherence
"""

active_modules: list[str] = field(default_factory=list)
attention_level: float = 0.5  # 0.0-1.0, modulated by acetylcholine
cpu_utilization: float = 0.0
memory_utilization: float = 0.0

# Oscillatory phase for synchronization (complex number representation)
# Phase coherence across nodes is critical for ESGT ignition
```

**Public Methods:**


---

### `TIGNode`

**File:** `fabric_old.py`

```python
class TIGNode:
```

**Description:**
```
"""
A processing unit within the TIG fabric.

Each node represents a Specialized Processing Module (SPM) that can:
- Process domain-specific information independently (differentiation)
- Participate in global synchronization events (integration)
- Maintain recurrent connections to other nodes (non-degeneracy)

Biological Analogy:
-------------------
TIG nodes are analogous to cortical columns in the brain - specialized
processors that maintain local function while participating in global
conscious states through transient synchronization.
"""

id: str
```

**Public Methods:**

- `def get_degree(self) -> int`
- `def get_clustering_coefficient(self, fabric`

---

### `TopologyConfig`

**File:** `fabric_old.py`

```python
class TopologyConfig:
```

**Description:**
```
"""
Configuration for generating TIG fabric topology.

These parameters are carefully tuned to satisfy IIT requirements:
- node_count: System size (larger = more differentiation potential)
- density: Connection density (higher = more integration)
- gamma: Scale-free exponent (2.5 = optimal hub/spoke balance)
- clustering_target: Target clustering coefficient (0.75 = high differentiation)

Parameter Tuning History:
- 2025-10-06: min_degree 3→5, rewiring_probability 0.1→0.35, target_density 0.15→0.20
- 2025-10-07 (PAGANI FIX v1): Over-aggressive - density 99.2% (complete graph!)
- 2025-10-07 (PAGANI FIX v2): Still too aggressive - density 100%
- 2025-10-07 (PAGANI FIX v3 - CONSERVATIVE): Target realistic density
  * rewiring_probability: 0.72→0.58 (more conservative closure)
  * min_degree: 5→5 (maintained)
```

**Public Methods:**


---

### `FabricMetrics`

**File:** `fabric_old.py`

```python
class FabricMetrics:
```

**Description:**
```
"""
Consciousness-relevant metrics for TIG fabric validation.

These metrics serve as Φ proxies - computable approximations of
integrated information that validate structural compliance with IIT.
"""

# Graph structure metrics
node_count: int = 0
edge_count: int = 0
density: float = 0.0

# IIT compliance metrics
avg_clustering_coefficient: float = 0.0
avg_path_length: float = 0.0
algebraic_connectivity: float = 0.0  # Fiedler eigenvalue
```

**Public Methods:**

- `def validate_iit_compliance(self) -> tuple[bool, list[str]]`

---

### `TIGFabric`

**File:** `fabric_old.py`

```python
class TIGFabric:
```

**Description:**
```
"""
The Global Interconnect Fabric - consciousness substrate.

This is the computational equivalent of the cortico-thalamic system,
providing the structural foundation for phenomenal experience.

The fabric implements:
1. IIT structural requirements (Φ maximization through topology)
2. GWD communication substrate (broadcast channels for ignition)
3. Recurrent signaling paths (feedback loops for sustained coherence)

Usage:
    config = TopologyConfig(node_count=32, target_density=0.20)
    fabric = TIGFabric(config)
    await fabric.initialize()
```

**Public Methods:**

- `def get_metrics(self) -> FabricMetrics`
- `def get_node(self, node_id`

---

### `NeedUrgency`

**File:** `monitor_old.py`

```python
class NeedUrgency(Enum):
```

**Description:**
```
"""Classification of need urgency levels."""

SATISFIED = "satisfied"  # need < 0.20 - no action required
LOW = "low"  # 0.20 ≤ need < 0.40 - background concern
MODERATE = "moderate"  # 0.40 ≤ need < 0.60 - should address soon
HIGH = "high"  # 0.60 ≤ need < 0.80 - requires attention
CRITICAL = "critical"  # need ≥ 0.80 - immediate action needed


@dataclass
class PhysicalMetrics:
"""
Raw physical/computational metrics collected from system.

These are the "receptor signals" analogous to biological interoception.
Values are normalized to [0, 1] range where possible.
```

**Public Methods:**


---

### `PhysicalMetrics`

**File:** `monitor_old.py`

```python
class PhysicalMetrics:
```

**Description:**
```
"""
Raw physical/computational metrics collected from system.

These are the "receptor signals" analogous to biological interoception.
Values are normalized to [0, 1] range where possible.
"""

# Computational load
cpu_usage_percent: float = 0.0  # 0-100 → normalized to 0-1
memory_usage_percent: float = 0.0  # 0-100 → normalized to 0-1

# System health
error_rate_per_min: float = 0.0  # Errors detected per minute
exception_count: int = 0  # Recent exceptions

# Physical state (if available)
```

**Public Methods:**

- `def normalize(self) -> "PhysicalMetrics"`

---

### `AbstractNeeds`

**File:** `monitor_old.py`

```python
class AbstractNeeds:
```

**Description:**
```
"""
Abstract psychological/phenomenal needs derived from physical metrics.

This is the "feeling" layer - the phenomenal experience of bodily state.
All values normalized to [0, 1] where 1.0 = maximum need.

Biological Correspondence:
- rest_need: Fatigue sensation
- repair_need: Pain/discomfort signaling damage
- efficiency_need: Thermal discomfort, energy depletion
- connectivity_need: Social isolation feeling
- curiosity_drive: Boredom, exploration urge
"""

# Primary needs (deficit-based)
rest_need: float = 0.0  # Need to reduce computational load
```

**Public Methods:**

- `def get_most_urgent(self) -> tuple[str, float, NeedUrgency]`
- `def get_critical_needs(self, threshold`

---

### `InteroceptionConfig`

**File:** `monitor_old.py`

```python
class InteroceptionConfig:
```

**Description:**
```
"""Configuration for internal state monitoring."""

# Collection intervals
collection_interval_ms: float = 100.0  # 10 Hz default

# Moving average windows
short_term_window_samples: int = 10  # 1 second at 10 Hz
long_term_window_samples: int = 50  # 5 seconds at 10 Hz

# Need computation weights
cpu_weight: float = 0.6  # CPU contributes 60% to rest_need
memory_weight: float = 0.4  # Memory contributes 40% to rest_need

# Thresholds
error_rate_critical: float = 10.0  # 10 errors/min = critical
temperature_warning_celsius: float = 80.0
```

**Public Methods:**


---

### `InternalStateMonitor`

**File:** `monitor_old.py`

```python
class InternalStateMonitor:
```

**Description:**
```
"""
Monitors internal physical/computational state and translates to abstract needs.

This is the core interoception engine - continuously collecting physical
metrics and computing phenomenal "feelings" (abstract needs).

Architecture:
-------------
Physical Layer:
  ↓ (metrics collection)
PhysicalMetrics
  ↓ (translation)
AbstractNeeds
  ↓ (goal generation)
Autonomous Goals → ESGT → HCL
```

**Public Methods:**

- `def set_metrics_collector(self, collector`
- `def register_need_callback(self, callback`
- `def get_current_needs(self) -> AbstractNeeds | None`
- `def get_current_metrics(self) -> PhysicalMetrics | None`
- `def get_needs_trend(self, need_name`
- `def get_moving_average(self, need_name`
- `def get_statistics(self) -> dict[str, any]`

---

### `NarrativeResult`

**File:** `autobiographical_narrative.py`

```python
class NarrativeResult:
```

**Description:**
```
"""Narrative plus associated metrics."""

narrative: str
coherence_score: float
episode_count: int


class AutobiographicalNarrative:
"""Constructs autobiographical narratives from episodic memory."""

def __init__(self):
    self._binder = TemporalBinder()

def build(self, episodes: Sequence[Episode]) -> NarrativeResult:
    ordered = sorted(episodes, key=lambda ep: ep.timestamp)
    coherence = self._compute_coherence(ordered)
```

**Public Methods:**


---

### `AutobiographicalNarrative`

**File:** `autobiographical_narrative.py`

```python
class AutobiographicalNarrative:
```

**Description:**
```
"""Constructs autobiographical narratives from episodic memory."""

def __init__(self):
    self._binder = TemporalBinder()

def build(self, episodes: Sequence[Episode]) -> NarrativeResult:
    ordered = sorted(episodes, key=lambda ep: ep.timestamp)
    coherence = self._compute_coherence(ordered)
    narrative = self._build_text(ordered)
    return NarrativeResult(narrative=narrative, coherence_score=coherence, episode_count=len(ordered))

def _compute_coherence(self, episodes: Sequence[Episode]) -> float:
    if not episodes:
        return 0.0
    temporal_coherence = self._binder.coherence(episodes)
    focus_stability = self._binder.focus_stability(episodes)
```

**Public Methods:**

- `def build(self, episodes`

---

### `BridgeConfig`

**File:** `biomimetic_safety_bridge.py`

```python
class BridgeConfig:
```

**Description:**
```
"""Configuration for biomimetic safety bridge."""

# Coordination limits
max_coordination_cycles_per_second: int = 10  # Max 10 coordinated cycles/sec
max_coordination_time_ms: float = 1000.0  # Max 1 second per cycle

# Cross-system thresholds
anomaly_threshold_prediction_error: float = 8.0  # High prediction error threshold
anomaly_threshold_neuromod_conflict_rate: float = 0.5  # High conflict rate threshold

# Aggregate circuit breaker
max_consecutive_coordination_failures: int = 5  # Failures before kill switch

# Neuromodulation config (optional override)
neuromod_config: NeuromodConfig | None = None
```

**Public Methods:**


---

### `BridgeState`

**File:** `biomimetic_safety_bridge.py`

```python
class BridgeState:
```

**Description:**
```
"""Observable state of biomimetic safety bridge."""

total_coordination_cycles: int
total_coordination_failures: int
consecutive_coordination_failures: int
neuromodulation_active: bool
predictive_coding_active: bool
aggregate_circuit_breaker_open: bool
cross_system_anomalies_detected: int
average_coordination_time_ms: float


class BiomimeticSafetyBridge:
"""
Integration layer connecting Neuromodulation + Predictive Coding with Safety Core.
```

**Public Methods:**


---

### `BiomimeticSafetyBridge`

**File:** `biomimetic_safety_bridge.py`

```python
class BiomimeticSafetyBridge:
```

**Description:**
```
"""
Integration layer connecting Neuromodulation + Predictive Coding with Safety Core.

This bridge ensures:
1. **System Isolation**: Each system can fail independently without crashing the other
2. **Coordinated Operation**: Both systems work together to process inputs
3. **Aggregate Monitoring**: Combines metrics from both systems
4. **Cross-System Anomaly Detection**: Detects when both systems show problems simultaneously
5. **Aggregate Circuit Breaker**: Kill switch when both systems fail
6. **Emergency Shutdown**: Coordinated shutdown of both systems

Usage:
    bridge = BiomimeticSafetyBridge(kill_switch_callback=safety.kill_switch.trigger)

    # Process input through both systems
    result = await bridge.coordinate_processing(raw_event_vector)
```

**Public Methods:**

- `def get_state(self) -> BridgeState`
- `def get_health_metrics(self) -> dict[str, Any]`
- `def emergency_stop(self)`

---

### `CascadePhase`

**File:** `cascade.py`

```python
class CascadePhase(Enum):
```

**Description:**
```
"""Coagulation cascade phases."""
IDLE = "idle"
INITIATION = "initiation"  # Threat detection
AMPLIFICATION = "amplification"  # Thrombin feedback
PROPAGATION = "propagation"  # Cascade spread
STABILIZATION = "stabilization"  # Fibrin formation
REGULATION = "regulation"  # Anticoagulation


class CascadePathway(Enum):
"""Coagulation pathways."""
INTRINSIC = "intrinsic"  # Internal (MMEI)
EXTRINSIC = "extrinsic"  # External (ESGT)
COMMON = "common"  # Final pathway
```

**Public Methods:**


---

### `CascadePathway`

**File:** `cascade.py`

```python
class CascadePathway(Enum):
```

**Description:**
```
"""Coagulation pathways."""
INTRINSIC = "intrinsic"  # Internal (MMEI)
EXTRINSIC = "extrinsic"  # External (ESGT)
COMMON = "common"  # Final pathway


@dataclass
class ThreatSignal:
"""
Threat signal that triggers coagulation.

Biological analog: Tissue factor exposure / collagen exposure.
"""
threat_id: str
severity: float  # [0-1] 0=minor, 1=critical
source: str  # "mmei", "esgt", "immune_tools"
```

**Public Methods:**


---

### `ThreatSignal`

**File:** `cascade.py`

```python
class ThreatSignal:
```

**Description:**
```
"""
Threat signal that triggers coagulation.

Biological analog: Tissue factor exposure / collagen exposure.
"""
threat_id: str
severity: float  # [0-1] 0=minor, 1=critical
source: str  # "mmei", "esgt", "immune_tools"
pathway: CascadePathway
timestamp: float = field(default_factory=time.time)
metadata: dict[str, Any] = field(default_factory=dict)

def is_critical(self) -> bool:
    """Check if threat is critical (requires immediate response)."""
    return self.severity >= 0.8
```

**Public Methods:**

- `def is_critical(self) -> bool`

---

### `CoagulationResponse`

**File:** `cascade.py`

```python
class CoagulationResponse:
```

**Description:**
```
"""
Response generated by coagulation cascade.

Biological analog: Fibrin clot formation.
"""
response_id: str
phase: CascadePhase
amplification_factor: float  # Thrombin-like amplification
memory_consolidation_strength: float  # Fibrin strength
errors_clustered: list[str]  # Platelet aggregation
anticoagulation_level: float  # Tolerance regulation
duration_ms: float
timestamp: float = field(default_factory=time.time)

def is_stable(self) -> bool:
    """Check if clot is stable (memory consolidated)."""
```

**Public Methods:**

- `def is_stable(self) -> bool`

---

### `CascadeState`

**File:** `cascade.py`

```python
class CascadeState:
```

**Description:**
```
"""
Current state of coagulation cascade.

Tracks: Phase, amplification, active threats, consolidated memories.
"""
phase: CascadePhase = CascadePhase.IDLE
amplification_factor: float = 1.0  # Starts at 1.0 (no amplification)
active_threats: list[ThreatSignal] = field(default_factory=list)
consolidated_memories: list[str] = field(default_factory=list)
anticoagulation_level: float = 0.5  # Balance (0=none, 1=full suppression)

# Cascade metrics
intrinsic_activation: float = 0.0  # Internal pathway strength
extrinsic_activation: float = 0.0  # External pathway strength
thrombin_level: float = 0.0  # Amplification enzyme
fibrin_formation: float = 0.0  # Memory consolidation progress
```

**Public Methods:**


---

### `CoagulationCascade`

**File:** `cascade.py`

```python
class CoagulationCascade:
```

**Description:**
```
"""
Biological Coagulation Cascade for AI Systems.

Implements:
- Intrinsic Pathway: Internal threat detection (MMEI)
- Extrinsic Pathway: External threat signals (ESGT)
- Thrombin Amplification: Positive feedback
- Fibrin Formation: Memory consolidation
- Anticoagulation: Tolerance regulation

Safety Hardening (FASE VII):
- Amplification capped at 10.0 (prevent runaway)
- Anticoagulation bounds: [0.1, 0.9]
- Cascade timeout: 30 seconds max
- Automatic regulation if over-activated
"""
```

**Public Methods:**

- `def trigger_cascade(`
- `def check_timeout(self) -> bool`
- `def reset(self) -> None`
- `def get_state(self) -> CascadeState`

---

### `Episode`

**File:** `core.py`

```python
class Episode:
```

**Description:**
```
"""Represents a single conscious episode."""

episode_id: str
timestamp: datetime
focus_target: str
salience: float
confidence: float
narrative: str
metadata: Dict[str, object] = field(default_factory=dict)

def to_dict(self) -> Dict[str, object]:
    """Serialize episode to dictionary for storage or logging."""
    return {
        "episode_id": self.episode_id,
        "timestamp": self.timestamp.isoformat(),
        "focus_target": self.focus_target,
```

**Public Methods:**

- `def to_dict(self) -> Dict[str, object]`

---

### `EpisodicMemory`

**File:** `core.py`

```python
class EpisodicMemory:
```

**Description:**
```
"""
Stores and retrieves conscious episodes with temporal guarantees.
"""

def __init__(self, retention: int = 1000):
    self._episodes: List[Episode] = []
    self._retention = retention

# ------------------------------------------------------------------ #
# Recording
# ------------------------------------------------------------------ #

def record(
    self,
    attention_state: AttentionState,
    summary: IntrospectiveSummary,
```

**Public Methods:**

- `def record(`
- `def latest(self, limit`
- `def between(self, start`
- `def by_focus(self, target`
- `def episodic_accuracy(self, focuses`
- `def temporal_order_preserved(self, window`
- `def coherence_score(self, window`
- `def timeline(self) -> List[Episode]`

---

### `EventType`

**File:** `event.py`

```python
class EventType(Enum):
```

**Description:**
```
"""Types of episodic events"""
PERCEPTION = "perception"      # Sensory input
ACTION = "action"              # Action taken
DECISION = "decision"          # Decision made
EMOTION = "emotion"            # Emotional state
THOUGHT = "thought"            # Internal reasoning
INTERACTION = "interaction"    # External interaction
SYSTEM = "system"              # System event


class Salience(Enum):
"""Event importance levels"""
CRITICAL = 5    # Must preserve
HIGH = 4        # Very important
MEDIUM = 3      # Moderately important
LOW = 2         # Optional
```

**Public Methods:**


---

### `Salience`

**File:** `event.py`

```python
class Salience(Enum):
```

**Description:**
```
"""Event importance levels"""
CRITICAL = 5    # Must preserve
HIGH = 4        # Very important
MEDIUM = 3      # Moderately important
LOW = 2         # Optional
TRIVIAL = 1     # Can discard


@dataclass
class Event:
"""
Discrete episodic event in consciousness timeline.

Represents a single moment of experience that can be:
- Indexed temporally
- Retrieved semantically
```

**Public Methods:**


---

### `Event`

**File:** `event.py`

```python
class Event:
```

**Description:**
```
"""
Discrete episodic event in consciousness timeline.

Represents a single moment of experience that can be:
- Indexed temporally
- Retrieved semantically
- Consolidated to long-term memory
- Used for narrative construction
"""

# Identity
id: str = field(default_factory=lambda: str(uuid.uuid4()))
timestamp: datetime = field(default_factory=datetime.now)

# Content
type: EventType = EventType.SYSTEM
```

**Public Methods:**

- `def mark_accessed(self)`
- `def calculate_importance(self) -> float`
- `def to_dict(self) -> Dict[str, Any]`
- `def from_dict(cls, data`

---

### `EpisodicBuffer`

**File:** `memory_buffer.py`

```python
class EpisodicBuffer:
```

**Description:**
```
"""
Episodic memory buffer implementing STM → LTM consolidation.

Architecture:
- Short-Term Memory (STM): Recent events (last N)
- Long-Term Memory (LTM): Consolidated important events
- Consolidation: Move important events from STM to LTM

Inspired by Atkinson-Shiffrin memory model.
"""

def __init__(
    self,
    stm_capacity: int = 1000,
    consolidation_threshold: float = 0.6,
    consolidation_interval: int = 300  # seconds
```

**Public Methods:**

- `def add_event(self, event`
- `def consolidate(self, force`
- `def get_recent_events(self, limit`
- `def get_ltm_events(`
- `def query_events(`
- `def clear_stm(self)`
- `def clear_ltm(self)`
- `def get_stats(self) -> Dict[str, any]`

---

### `ArousalModulationConfig`

**File:** `arousal_integration.py`

```python
class ArousalModulationConfig:
```

**Description:**
```
"""Configuration for arousal-ESGT integration."""

# Threshold modulation
baseline_threshold: float = 0.70  # ESGT threshold at relaxed arousal
min_threshold: float = 0.30  # At hyperalert
max_threshold: float = 0.95  # At sleep/drowsy

# Modulation curve
threshold_sensitivity: float = 1.0  # How strongly arousal affects threshold

# Refractory coupling
enable_refractory_arousal_drop: bool = True
refractory_arousal_drop: float = 0.15  # Temporary drop after ESGT
refractory_recovery_rate: float = 0.1  # Per second

# Update rate
```

**Public Methods:**


---

### `ESGTArousalBridge`

**File:** `arousal_integration.py`

```python
class ESGTArousalBridge:
```

**Description:**
```
"""
Bridge between ESGT coordinator and MCEA arousal controller.

This bridge implements arousal-modulated consciousness by:
1. Continuously reading arousal level from MCEA
2. Computing appropriate ESGT salience threshold
3. Updating ESGT coordinator trigger conditions
4. Signaling MCEA when ESGT refractory occurs

Architecture:
-------------
```
MCEA (Arousal) ←→ ESGTArousalBridge ←→ ESGT (Coordinator)
     ↑                  ↓                      ↑
     |       threshold modulation              |
     |                                          |
```

**Public Methods:**

- `def get_current_threshold(self) -> float`
- `def get_arousal_threshold_mapping(self) -> dict`
- `def get_metrics(self) -> dict`

---

### `FrequencyLimiter`

**File:** `coordinator.py`

```python
class FrequencyLimiter:
```

**Description:**
```
"""
Hard frequency limiter using token bucket algorithm.

FASE VII (Safety Hardening):
Prevents ESGT runaway by enforcing strict frequency bounds.
"""

def __init__(self, max_frequency_hz: float):
    self.max_frequency = max_frequency_hz
    self.tokens = max_frequency_hz
    self.last_update = time.time()
    self.lock = asyncio.Lock()

async def allow(self) -> bool:
    """
    Check if operation is allowed (token available).
```

**Public Methods:**


---

### `ESGTPhase`

**File:** `coordinator.py`

```python
class ESGTPhase(Enum):
```

**Description:**
```
"""Phases of ESGT ignition protocol."""

IDLE = "idle"
PREPARE = "prepare"
SYNCHRONIZE = "synchronize"
BROADCAST = "broadcast"
SUSTAIN = "sustain"
DISSOLVE = "dissolve"
COMPLETE = "complete"
FAILED = "failed"


class SalienceLevel(Enum):
"""Classification of information salience."""

MINIMAL = "minimal"  # <0.25 - background noise
```

**Public Methods:**


---

### `SalienceLevel`

**File:** `coordinator.py`

```python
class SalienceLevel(Enum):
```

**Description:**
```
"""Classification of information salience."""

MINIMAL = "minimal"  # <0.25 - background noise
LOW = "low"  # 0.25-0.50 - peripheral awareness
MEDIUM = "medium"  # 0.50-0.75 - candidate for consciousness
HIGH = "high"  # 0.75-0.85 - likely conscious
CRITICAL = "critical"  # >0.85 - definitely conscious


@dataclass
class SalienceScore:
"""
Multi-factor salience score determining ESGT trigger.

Salience = α(Novelty) + β(Relevance) + γ(Urgency) + δ(Confidence)
```

**Public Methods:**


---

### `SalienceScore`

**File:** `coordinator.py`

```python
class SalienceScore:
```

**Description:**
```
"""
Multi-factor salience score determining ESGT trigger.

Salience = α(Novelty) + β(Relevance) + γ(Urgency) + δ(Confidence)

Where coefficients sum to 1.0 and are dynamically adjusted based
on arousal state (MCEA) and attention parameters (acetylcholine).
"""

novelty: float = 0.0  # 0-1, how unexpected
relevance: float = 0.0  # 0-1, goal-alignment
urgency: float = 0.0  # 0-1, time-criticality
confidence: float = 1.0  # 0-1, prediction confidence (default: high confidence)

# Weights (sum to 1.0)
alpha: float = 0.25  # Novelty weight
```

**Public Methods:**

- `def compute_total(self) -> float`
- `def get_level(self) -> SalienceLevel`

---

### `TriggerConditions`

**File:** `coordinator.py`

```python
class TriggerConditions:
```

**Description:**
```
"""
Conditions required for ESGT initiation.

All conditions must be met for ignition to proceed. This prevents
pathological synchronization and ensures computational resources
are available.
"""

# Salience threshold
min_salience: float = 0.60  # Typical threshold for consciousness

# Resource requirements
max_tig_latency_ms: float = 5.0  # TIG must be responsive
min_available_nodes: int = 8  # Minimum participating nodes
min_cpu_capacity: float = 0.40  # 40% CPU available
```

**Public Methods:**

- `def check_salience(self, score`
- `def check_resources(self, tig_latency_ms`
- `def check_temporal_gating(`
- `def check_arousal(self, arousal_level`

---

### `ESGTEvent`

**File:** `coordinator.py`

```python
class ESGTEvent:
```

**Description:**
```
"""
Represents a single transient global synchronization event.

This is the computational analog of a conscious moment - a discrete
episode where distributed information becomes unified, globally
accessible, and reportable.
"""

event_id: str
timestamp_start: float
timestamp_end: float | None = None

# Content
content: dict[str, Any] = field(default_factory=dict)
content_source: str = ""  # SPM that contributed content
```

**Public Methods:**

- `def transition_phase(self, new_phase`
- `def finalize(self, success`
- `def get_duration_ms(self) -> float`
- `def was_successful(self) -> bool`

---

### `ESGTCoordinator`

**File:** `coordinator.py`

```python
class ESGTCoordinator:
```

**Description:**
```
"""
Coordinates ESGT ignition events for consciousness emergence.

This coordinator implements the full GWD ignition protocol, managing
the transition from unconscious distributed processing to unified
conscious experience.

The coordinator:
1. Monitors salience scores continuously
2. Evaluates trigger conditions
3. Initiates synchronization when threshold met
4. Manages 5-phase ESGT protocol
5. Records metrics for consciousness validation

Usage:
    coordinator = ESGTCoordinator(
```

**Public Methods:**

- `def compute_salience_from_attention(`
- `def build_content_from_attention(`
- `def get_success_rate(self) -> float`
- `def get_recent_coherence(self, window`
- `def get_health_metrics(self) -> dict[str, Any]`

---

### `OscillatorState`

**File:** `kuramoto.py`

```python
class OscillatorState(Enum):
```

**Description:**
```
"""State of an oscillator during synchronization."""

IDLE = "idle"
COUPLING = "coupling"
SYNCHRONIZED = "synchronized"
DESYNCHRONIZING = "desynchronizing"


@dataclass
class OscillatorConfig:
"""Configuration for a Kuramoto oscillator."""

natural_frequency: float = 40.0  # Hz (gamma-band analog)
coupling_strength: float = 20.0  # K parameter (increased for sparse topology, was 14.0)
phase_noise: float = 0.001  # Additive phase noise (reduced from 0.01 for faster sync)
integration_method: str = "rk4"  # Numerical integrator: "euler" or "rk4" (PPBPR Section 5.2)
```

**Public Methods:**


---

### `OscillatorConfig`

**File:** `kuramoto.py`

```python
class OscillatorConfig:
```

**Description:**
```
"""Configuration for a Kuramoto oscillator."""

natural_frequency: float = 40.0  # Hz (gamma-band analog)
coupling_strength: float = 20.0  # K parameter (increased for sparse topology, was 14.0)
phase_noise: float = 0.001  # Additive phase noise (reduced from 0.01 for faster sync)
integration_method: str = "rk4"  # Numerical integrator: "euler" or "rk4" (PPBPR Section 5.2)
# NOTE: damping removed - not part of canonical Kuramoto model
# The phase-dependent damping was preventing synchronization by anchoring oscillators to θ=0


@dataclass
class PhaseCoherence:
"""
Measures phase synchronization quality.

The order parameter r quantifies how well oscillators are synchronized.
```

**Public Methods:**


---

### `PhaseCoherence`

**File:** `kuramoto.py`

```python
class PhaseCoherence:
```

**Description:**
```
"""
Measures phase synchronization quality.

The order parameter r quantifies how well oscillators are synchronized.
For consciousness, we interpret coherence levels as:

- r < 0.30: Unconscious processing (incoherent)
- 0.30 ≤ r < 0.70: Pre-conscious (partial coherence)
- r ≥ 0.70: Conscious state (high coherence) ✅
- r > 0.90: Deep coherence (exceptional binding)
"""

order_parameter: float  # r(t) ∈ [0, 1]
mean_phase: float  # Average phase angle (radians)
phase_variance: float  # Spread of phases
coherence_quality: str  # "unconscious", "preconscious", "conscious", "deep"
```

**Public Methods:**

- `def is_conscious_level(self) -> bool`
- `def get_quality_score(self) -> float`

---

### `SynchronizationDynamics`

**File:** `kuramoto.py`

```python
class SynchronizationDynamics:
```

**Description:**
```
"""
Tracks synchronization dynamics over time.

This provides historical context for ESGT events, showing how
coherence builds up, plateaus, and dissolves.
"""

coherence_history: list[float] = field(default_factory=list)
time_to_sync: float | None = None  # Time to reach r ≥ 0.70
max_coherence: float = 0.0
sustained_duration: float = 0.0  # Time spent at r ≥ 0.70
dissolution_rate: float = 0.0  # How fast coherence decays

def add_coherence_sample(self, coherence: float, timestamp: float) -> None:
    """Add coherence measurement to history."""
    self.coherence_history.append(coherence)
```

**Public Methods:**

- `def add_coherence_sample(self, coherence`
- `def compute_dissolution_rate(self) -> float`

---

### `KuramotoOscillator`

**File:** `kuramoto.py`

```python
class KuramotoOscillator:
```

**Description:**
```
"""
Implements a single Kuramoto oscillator for ESGT phase synchronization.

Each TIG node has an associated oscillator that can couple with neighbors
to achieve collective phase coherence during ignition events.

Biological Analogy:
-------------------
This oscillator is analogous to a cortical neural population with
intrinsic gamma-band oscillations (~40 Hz). During conscious states,
these populations phase-lock through synaptic coupling.

Usage:
    oscillator = KuramotoOscillator(
        node_id="tig-node-001",
        config=OscillatorConfig(natural_frequency=40.0)
```

**Public Methods:**

- `def update(self, neighbor_phases`
- `def get_phase(self) -> float`
- `def set_phase(self, phase`
- `def reset(self) -> None`

---

### `KuramotoNetwork`

**File:** `kuramoto.py`

```python
class KuramotoNetwork:
```

**Description:**
```
"""
Manages a network of coupled Kuramoto oscillators for ESGT.

This network coordinates phase synchronization across all TIG nodes
during ignition events, computing global coherence in real-time.

The network can:
- Initialize oscillators for all participating nodes
- Update all phases simultaneously (parallel integration)
- Compute order parameter r(t) continuously
- Detect synchronization onset and dissolution

Usage:
    network = KuramotoNetwork()

    # Add oscillators for TIG nodes
```

**Public Methods:**

- `def add_oscillator(self, node_id`
- `def remove_oscillator(self, node_id`
- `def reset_all(self) -> None`
- `def update_network(`
- `def get_coherence(self) -> PhaseCoherence | None`
- `def get_order_parameter(self) -> float`
- `def get_phase_distribution(self) -> np.ndarray`

---

### `SPMType`

**File:** `base.py`

```python
class SPMType(Enum):
```

**Description:**
```
"""Classification of SPM functional domain."""

PERCEPTUAL = "perceptual"  # Sensory processing
COGNITIVE = "cognitive"  # Executive, memory, planning
EMOTIONAL = "emotional"  # Affect and motivation
MOTOR = "motor"  # Action planning
METACOGNITIVE = "metacognitive"  # Self-monitoring


class ProcessingPriority(Enum):
"""Processing priority levels."""

BACKGROUND = 0  # Low priority, unconscious
PERIPHERAL = 1  # Peripheral awareness
FOCAL = 2  # Focal attention candidate
CRITICAL = 3  # Must become conscious
```

**Public Methods:**


---

### `ProcessingPriority`

**File:** `base.py`

```python
class ProcessingPriority(Enum):
```

**Description:**
```
"""Processing priority levels."""

BACKGROUND = 0  # Low priority, unconscious
PERIPHERAL = 1  # Peripheral awareness
FOCAL = 2  # Focal attention candidate
CRITICAL = 3  # Must become conscious


@dataclass
class SPMOutput:
"""
Output from SPM processing.

Contains processed information plus metadata for salience
evaluation and ESGT competition.
"""
```

**Public Methods:**


---

### `SPMOutput`

**File:** `base.py`

```python
class SPMOutput:
```

**Description:**
```
"""
Output from SPM processing.

Contains processed information plus metadata for salience
evaluation and ESGT competition.
"""

spm_id: str
spm_type: SPMType
content: dict[str, Any]
salience: SalienceScore
priority: ProcessingPriority
timestamp: float = field(default_factory=time.time)
confidence: float = 1.0  # 0-1 processing confidence

def should_broadcast(self, threshold: float = 0.60) -> bool:
```

**Public Methods:**

- `def should_broadcast(self, threshold`

---

### `SpecializedProcessingModule`

**File:** `base.py`

```python
class SpecializedProcessingModule(ABC):
```

**Description:**
```
"""
Abstract base class for all SPMs.

All specialized processing modules inherit from this base,
implementing domain-specific processing while following
the common protocol for consciousness integration.

Lifecycle:
----------
1. __init__: Initialize module
2. start(): Begin unconscious processing
3. process(): Continuous processing loop
4. compute_salience(): Evaluate information salience
5. broadcast_callback(): Respond when content becomes conscious
6. stop(): Graceful shutdown
```

**Public Methods:**

- `def compute_salience(self, data`
- `def get_most_salient(self, n`
- `def get_success_rate(self) -> float`

---

### `ThreatDetectionSPM`

**File:** `base.py`

```python
class ThreatDetectionSPM(SpecializedProcessingModule):
```

**Description:**
```
"""
Specialized module for threat detection.

Processes security events, network anomalies, and attack patterns.
High urgency bias (threats are inherently time-critical).

Biological Analog: Amygdala (rapid threat assessment)
"""

def __init__(self, spm_id: str = "spm-threat-detection"):
    super().__init__(
        spm_id=spm_id,
        spm_type=SPMType.PERCEPTUAL,
        processing_interval_ms=100.0,  # 10 Hz
    )
    self.threat_baseline: float = 0.1
```

**Public Methods:**

- `def compute_salience(self, data`

---

### `MemoryRetrievalSPM`

**File:** `base.py`

```python
class MemoryRetrievalSPM(SpecializedProcessingModule):
```

**Description:**
```
"""
Specialized module for memory retrieval.

Processes memory queries, generates associations, retrieves context.
High relevance bias (memories are context-dependent).

Biological Analog: Hippocampus (episodic memory)
"""

def __init__(self, spm_id: str = "spm-memory-retrieval"):
    super().__init__(
        spm_id=spm_id,
        spm_type=SPMType.COGNITIVE,
        processing_interval_ms=200.0,  # 5 Hz
    )
    self.memory_store: dict[str, Any] = {}  # Simplified memory
```

**Public Methods:**

- `def compute_salience(self, data`

---

### `MetricCategory`

**File:** `metrics_monitor.py`

```python
class MetricCategory(Enum):
```

**Description:**
```
"""Categories of metrics monitored."""

COMPUTATIONAL = "computational"  # CPU, memory, threads
INTEROCEPTIVE = "interoceptive"  # Needs from MMEI
PERFORMANCE = "performance"  # Latency, throughput
HEALTH = "health"  # Errors, warnings
RESOURCES = "resources"  # Disk, network


@dataclass
class MetricsMonitorConfig:
"""Configuration for metrics monitoring."""

# Monitoring
monitoring_interval_ms: float = 200.0  # 5 Hz sampling
enable_continuous_reporting: bool = True
```

**Public Methods:**


---

### `MetricsMonitorConfig`

**File:** `metrics_monitor.py`

```python
class MetricsMonitorConfig:
```

**Description:**
```
"""Configuration for metrics monitoring."""

# Monitoring
monitoring_interval_ms: float = 200.0  # 5 Hz sampling
enable_continuous_reporting: bool = True

# Salience computation
high_cpu_threshold: float = 0.80  # CPU > 80% → high salience
high_memory_threshold: float = 0.75
high_error_rate_threshold: float = 5.0  # errors/min
critical_need_threshold: float = 0.80  # Need value

# MMEI integration
integrate_mmei: bool = True
mmei_poll_interval_ms: float = 100.0
```

**Public Methods:**


---

### `MetricsSnapshot`

**File:** `metrics_monitor.py`

```python
class MetricsSnapshot:
```

**Description:**
```
"""Snapshot of system metrics at a point in time."""

timestamp: float

# Computational
cpu_usage_percent: float = 0.0
memory_usage_percent: float = 0.0
thread_count: int = 0

# Interoceptive (from MMEI)
needs: AbstractNeeds | None = None
most_urgent_need: str = "none"
most_urgent_value: float = 0.0

# Performance
avg_latency_ms: float = 0.0
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `MetricsSPM`

**File:** `metrics_monitor.py`

```python
class MetricsSPM(SpecializedProcessingModule):
```

**Description:**
```
"""
Specialized Processing Module for internal metrics monitoring.

MetricsSPM provides conscious self-awareness by monitoring MAXIMUS's
internal computational and interoceptive state, packaging it as
conscious-ready content for ESGT broadcast.

This enables MAXIMUS to consciously "feel" and report its internal state,
not just regulate it unconsciously.

Architecture:
-------------
```
MMEI (needs) ────┐
CPU/Memory      ─┤
Errors          ─┼→ MetricsSPM → Salience → ESGT Trigger
```

**Public Methods:**

- `def compute_salience(self, data`
- `def register_output_callback(self, callback`
- `def get_current_snapshot(self) -> MetricsSnapshot | None`
- `def get_metrics(self) -> dict[str, Any]`

---

### `SalienceMode`

**File:** `salience_detector.py`

```python
class SalienceMode(Enum):
```

**Description:**
```
"""Operating mode for salience detection."""

PASSIVE = "passive"  # Only compute when asked
ACTIVE = "active"  # Continuously monitor and alert


@dataclass
class SalienceThresholds:
"""Thresholds for salience classification."""

low_threshold: float = 0.30  # Below: unconscious processing
medium_threshold: float = 0.50  # Peripheral awareness
high_threshold: float = 0.70  # Conscious access (ESGT trigger)
critical_threshold: float = 0.90  # Immediate priority
```

**Public Methods:**


---

### `SalienceThresholds`

**File:** `salience_detector.py`

```python
class SalienceThresholds:
```

**Description:**
```
"""Thresholds for salience classification."""

low_threshold: float = 0.30  # Below: unconscious processing
medium_threshold: float = 0.50  # Peripheral awareness
high_threshold: float = 0.70  # Conscious access (ESGT trigger)
critical_threshold: float = 0.90  # Immediate priority


@dataclass
class SalienceDetectorConfig:
"""Configuration for salience detection."""

# Mode
mode: SalienceMode = SalienceMode.ACTIVE
update_interval_ms: float = 50.0  # 20 Hz monitoring
```

**Public Methods:**


---

### `SalienceDetectorConfig`

**File:** `salience_detector.py`

```python
class SalienceDetectorConfig:
```

**Description:**
```
"""Configuration for salience detection."""

# Mode
mode: SalienceMode = SalienceMode.ACTIVE
update_interval_ms: float = 50.0  # 20 Hz monitoring

# Weights (must sum to 1.0)
novelty_weight: float = 0.4
relevance_weight: float = 0.4
urgency_weight: float = 0.2

# Thresholds
thresholds: SalienceThresholds = field(default_factory=SalienceThresholds)

# Novelty detection
novelty_baseline_window: int = 50  # Samples for baseline
```

**Public Methods:**


---

### `SalienceEvent`

**File:** `salience_detector.py`

```python
class SalienceEvent:
```

**Description:**
```
"""Record of a high-salience detection."""

timestamp: float
salience: SalienceScore
source: str
content: dict[str, Any]
threshold_exceeded: float


class SalienceSPM(SpecializedProcessingModule):
"""
Specialized Processing Module for salience detection.

SalienceSPM is the "attention controller" of MAXIMUS consciousness.
It continuously monitors internal and external information streams,
computing salience scores to determine what should trigger ESGT ignition.
```

**Public Methods:**


---

### `SalienceSPM`

**File:** `salience_detector.py`

```python
class SalienceSPM(SpecializedProcessingModule):
```

**Description:**
```
"""
Specialized Processing Module for salience detection.

SalienceSPM is the "attention controller" of MAXIMUS consciousness.
It continuously monitors internal and external information streams,
computing salience scores to determine what should trigger ESGT ignition.

This SPM doesn't process domain-specific content - it meta-processes
outputs from other SPMs and internal metrics to decide conscious access.

Architecture:
-------------
```
Internal Metrics (MMEI) ─┐
External Events         ─┼→ Salience Computation → Threshold Check
Other SPM Outputs       ─┘                              ↓
```

**Public Methods:**

- `def evaluate_event(`
- `def set_urgency(self, source`
- `def boost_urgency_on_error(self, source`
- `def compute_salience(self, data`
- `def register_high_salience_callback(self, callback`
- `def get_recent_high_salience_events(self, count`
- `def get_salience_rate(self) -> float`
- `def get_metrics(self) -> dict[str, Any]`

---

### `SimpleSPMConfig`

**File:** `simple.py`

```python
class SimpleSPMConfig:
```

**Description:**
```
"""Configuration for SimpleSPM."""

# Processing
processing_interval_ms: float = 100.0  # How often to generate output
burst_mode: bool = False  # Generate multiple outputs per cycle
burst_count: int = 3  # Outputs per burst

# Salience configuration
base_novelty: float = 0.3
base_relevance: float = 0.5
base_urgency: float = 0.2
salience_noise: float = 0.1  # Random variation

# Content generation
content_size_bytes: int = 1024  # Size of generated content
include_timestamp: bool = True
```

**Public Methods:**


---

### `SimpleSPM`

**File:** `simple.py`

```python
class SimpleSPM(SpecializedProcessingModule):
```

**Description:**
```
"""
A simple, configurable SPM for testing and validation.

SimpleSPM generates synthetic content with controllable salience,
allowing systematic testing of ESGT trigger conditions and
ignition protocol.

Unlike domain-specific SPMs (perceptual, cognitive), SimpleSPM
has no semantic processing - it's purely for protocol validation.

Example Usage:
--------------
```python
# Create SPM with high salience
config = SimpleSPMConfig(
    base_novelty=0.8,
```

**Public Methods:**

- `def compute_salience(self, data`
- `def register_output_callback(self, callback`
- `def unregister_output_callback(self, callback`
- `def configure_salience(`
- `def get_metrics(self) -> dict[str, Any]`
- `def is_running(self) -> bool`

---

### `ESGTSubscriber`

**File:** `esgt_subscriber.py`

```python
class ESGTSubscriber:
```

**Description:**
```
"""
Event subscriber for ESGT ignition events.

Provides callback-based subscription for immune system to react to
conscious access events.
"""

def __init__(self):
    """Initialize ESGT subscriber."""
    self._handlers: list[Callable[[ESGTEvent], Awaitable[None]]] = []
    self._event_count = 0
    self._running = False

def on_ignition(self, handler: Callable[[ESGTEvent], Awaitable[None]]):
    """
    Register callback for ESGT ignition events.
```

**Public Methods:**

- `def on_ignition(self, handler`
- `def remove_handler(self, handler`
- `def get_event_count(self) -> int`
- `def get_handler_count(self) -> int`
- `def clear_handlers(self)`

---

### `MCEAClient`

**File:** `mcea_client.py`

```python
class MCEAClient:
```

**Description:**
```
"""
HTTP client for MCEA ArousalController.

Provides access to current arousal state for clonal selection modulation.
"""

def __init__(
    self,
    base_url: str = "http://localhost:8100",  # MCEA service port
    timeout: float = 5.0,
):
    """
    Initialize MCEA client.

    Args:
        base_url: MCEA service base URL
```

**Public Methods:**

- `def get_last_arousal(self) -> ArousalState | None`
- `def is_healthy(self) -> bool`

---

### `MEAContextSnapshot`

**File:** `mea_bridge.py`

```python
class MEAContextSnapshot:
```

**Description:**
```
"""Snapshot of MEA state to feed into other consciousness modules."""

attention_state: AttentionState
boundary: BoundaryAssessment
summary: IntrospectiveSummary
episode: Episode
narrative_text: str
narrative_coherence: float


class MEABridge:
"""
Utility class that maintains MEA state and exposes integration helpers.
"""

def __init__(
```

**Public Methods:**


---

### `MEABridge`

**File:** `mea_bridge.py`

```python
class MEABridge:
```

**Description:**
```
"""
Utility class that maintains MEA state and exposes integration helpers.
"""

def __init__(
    self,
    attention_model: AttentionSchemaModel,
    self_model: SelfModel,
    boundary_detector: BoundaryDetector,
    episodic_memory: EpisodicMemory | None = None,
    narrative_builder: AutobiographicalNarrative | None = None,
    temporal_binder: TemporalBinder | None = None,
) -> None:
    self.attention_model = attention_model
    self.self_model = self_model
    self.boundary_detector = boundary_detector
```

**Public Methods:**

- `def create_snapshot(`
- `def to_lrr_context(snapshot`
- `def to_esgt_payload(`

---

### `MMEIClient`

**File:** `mmei_client.py`

```python
class MMEIClient:
```

**Description:**
```
"""
HTTP client for MMEI InternalStateMonitor.

Provides access to current abstract needs for immune system integration.
"""

def __init__(
    self,
    base_url: str = "http://localhost:8100",  # MMEI service port
    timeout: float = 5.0,
):
    """
    Initialize MMEI client.

    Args:
        base_url: MMEI service base URL
```

**Public Methods:**

- `def get_last_needs(self) -> AbstractNeeds | None`
- `def is_healthy(self) -> bool`

---

### `PredictionError`

**File:** `sensory_esgt_bridge.py`

```python
class PredictionError:
```

**Description:**
```
"""
Prediction error from predictive coding layer.

Attributes:
    layer_id: Layer that generated the error
    magnitude: Error magnitude [0, max_error]
    max_error: Maximum possible error (for normalization)
    bounded: Whether error was clipped to max
"""
layer_id: int
magnitude: float
max_error: float
bounded: bool = True


@dataclass
```

**Public Methods:**


---

### `SensoryContext`

**File:** `sensory_esgt_bridge.py`

```python
class SensoryContext:
```

**Description:**
```
"""
Contextual information about sensory input.

Attributes:
    modality: Sensory modality (e.g., "event", "network", "system")
    timestamp: Event timestamp
    source: Source identifier
    metadata: Additional context
"""
modality: str
timestamp: float
source: str
metadata: Dict[str, any]


@dataclass
```

**Public Methods:**


---

### `SalienceFactors`

**File:** `sensory_esgt_bridge.py`

```python
class SalienceFactors:
```

**Description:**
```
"""
Decomposed salience factors from prediction errors.

Attributes:
    novelty: How unexpected (0-1, from prediction error)
    relevance: Task relevance (0-1, from context)
    urgency: Time-criticality (0-1, from context)
    intensity: Signal strength (0-1, from magnitude)
"""
novelty: float
relevance: float
urgency: float
intensity: float

def compute_total_salience(self) -> float:
    """
```

**Public Methods:**

- `def compute_total_salience(self) -> float`

---

### `SensoryESGTBridge`

**File:** `sensory_esgt_bridge.py`

```python
class SensoryESGTBridge:
```

**Description:**
```
"""
Bridge between Predictive Coding and ESGT.

Converts prediction errors into salience signals suitable for
triggering global workspace ignition.

Usage:
    bridge = SensoryESGTBridge(
        esgt_coordinator=esgt,
        salience_threshold=0.7,
        novelty_amplification=1.5
    )
    
    # From prediction error to consciousness
    prediction_error = layer.compute_error(prediction, actual)
    context = SensoryContext(modality="event", ...)
```

**Public Methods:**

- `def compute_salience_from_error(`
- `def should_trigger_ignition(self, salience_factors`
- `def build_conscious_content(`
- `def get_statistics(self) -> Dict[str, any]`

---

### `ConsciousnessIntegrationDemo`

**File:** `integration_example.py`

```python
class ConsciousnessIntegrationDemo:
```

**Description:**
```
"""
Demonstrates full consciousness integration.

This demo shows the complete embodied consciousness loop:
- Physical metrics → Needs
- Needs → Goals
- Needs → Arousal modulation
- Arousal → ESGT threshold adjustment
- Goals → (HCL execution - simulated)
"""

def __init__(self):
    # Component configurations
    self.mmei_config = InteroceptionConfig(
        collection_interval_ms=500.0,  # 2 Hz for demo visibility
    )
```

**Public Methods:**

- `def print_status(self)`

---

### `FirstOrderLogic`

**File:** `contradiction_detector.py`

```python
class FirstOrderLogic:
```

**Description:**
```
"""
Minimal first-order logic helper tailored for MAXIMUS beliefs.

The goal is not to implement a full theorem prover, but to offer
deterministic normalisation and entailment checks that complement the
heuristics embedded in ``BeliefGraph``.
"""

NEGATION_MARKERS: Tuple[str, ...] = ("not ", "¬", "~", "no ", "isn't", "aren't")

@staticmethod
def normalise(statement: str) -> str:  # pragma: no cover - internal normalization, tested via is_direct_negation
    """
    Convert natural-language belief content into a canonical predicate-like
    representation to support equivalence and negation checks.
    """
```

**Public Methods:**

- `def normalise(statement`
- `def is_direct_negation(self, a`

---

### `ContradictionSummary`

**File:** `contradiction_detector.py`

```python
class ContradictionSummary:
```

**Description:**
```
"""Aggregated metrics for contradiction detection cycles."""

total_detected: int
direct_count: int
transitive_count: int
temporal_count: int
contextual_count: int
average_severity: float


@dataclass(slots=True)
class RevisionOutcome:
"""Result of applying belief revision to resolve a contradiction."""

resolution: "Resolution"
strategy: "ResolutionStrategy"
```

**Public Methods:**


---

### `RevisionOutcome`

**File:** `contradiction_detector.py`

```python
class RevisionOutcome:
```

**Description:**
```
"""Result of applying belief revision to resolve a contradiction."""

resolution: "Resolution"
strategy: "ResolutionStrategy"
removed_beliefs: List["Belief"]
modified_beliefs: List["Belief"]


class ContradictionDetector:
"""
Detector de contradições alinhado ao blueprint LRR.

Usa ``BeliefGraph`` para heurísticas estruturadas e complementa com um
analisador lógico leve para capturar contradições que escapem aos índices
básicos (e.g., variações sintáticas).
"""
```

**Public Methods:**


---

### `ContradictionDetector`

**File:** `contradiction_detector.py`

```python
class ContradictionDetector:
```

**Description:**
```
"""
Detector de contradições alinhado ao blueprint LRR.

Usa ``BeliefGraph`` para heurísticas estruturadas e complementa com um
analisador lógico leve para capturar contradições que escapem aos índices
básicos (e.g., variações sintáticas).
"""

def __init__(self) -> None:
    self.logic_engine = FirstOrderLogic()
    self.contradiction_history: List["Contradiction"] = []
    self.summary_history: List[ContradictionSummary] = []

async def detect_contradictions(
    self, belief_graph: "BeliefGraph"
) -> List["Contradiction"]:
```

**Public Methods:**

- `def latest_summary(self) -> Optional[ContradictionSummary]`

---

### `BeliefRevision`

**File:** `contradiction_detector.py`

```python
class BeliefRevision:
```

**Description:**
```
"""
Implementa revisão de crenças AGM-style para restaurar consistência.
"""

def __init__(self) -> None:
    self.revision_log: List[RevisionOutcome] = []

async def revise_belief_graph(
    self, belief_graph: "BeliefGraph", contradiction: "Contradiction"
) -> RevisionOutcome:
    """
    Resolve contradição aplicando a estratégia mais conservadora possível.
    """
    strategy = self._select_strategy(contradiction)

    from .recursive_reasoner import Resolution
```

**Public Methods:**


---

### `IntrospectionHighlight`

**File:** `introspection_engine.py`

```python
class IntrospectionHighlight:
```

**Description:**
```
"""Structured insights referenced inside the narrative."""

level: int
belief_content: str
confidence: float
justification_summary: str


@dataclass(slots=True)
class IntrospectionReport:
"""Final introspection output, aligned with blueprint expectations."""

narrative: str
beliefs_explained: int
coherence_score: float
timestamp: datetime
```

**Public Methods:**


---

### `IntrospectionReport`

**File:** `introspection_engine.py`

```python
class IntrospectionReport:
```

**Description:**
```
"""Final introspection output, aligned with blueprint expectations."""

narrative: str
beliefs_explained: int
coherence_score: float
timestamp: datetime
highlights: List[IntrospectionHighlight]


class NarrativeGenerator:
"""Compose natural-language narratives from introspection fragments."""

def construct_narrative(self, fragments: Sequence[str]) -> str:
    if not fragments:
        return "Não há raciocínio suficiente para gerar introspecção."
```

**Public Methods:**


---

### `NarrativeGenerator`

**File:** `introspection_engine.py`

```python
class NarrativeGenerator:
```

**Description:**
```
"""Compose natural-language narratives from introspection fragments."""

def construct_narrative(self, fragments: Sequence[str]) -> str:
    if not fragments:
        return "Não há raciocínio suficiente para gerar introspecção."

    if len(fragments) == 1:
        return fragments[0]

    intro = fragments[0]
    body = " ".join(fragments[1:-1]) if len(fragments) > 2 else ""
    conclusion = fragments[-1]

    if body:
        return f"{intro} {body} Portanto, {conclusion}"
    return f"{intro} Portanto, {conclusion}"
```

**Public Methods:**

- `def construct_narrative(self, fragments`

---

### `BeliefExplainer`

**File:** `introspection_engine.py`

```python
class BeliefExplainer:
```

**Description:**
```
"""Generate concise explanations for beliefs and justification chains."""

def summarise_justification(self, level: "ReasoningLevel") -> str:
    if not level.steps:
        return "Sem etapas registradas."

    step = level.steps[0]
    if not step.justification_chain:
        return "Confiança baseada na evidência direta disponível."

    evidences = [belief.content for belief in step.justification_chain[:3]]
    more = "" if len(step.justification_chain) <= 3 else "..."
    evidences_str = "; ".join(evidences)
    return f"Justificações principais: {evidences_str}{more}"
```

**Public Methods:**

- `def summarise_justification(self, level`

---

### `IntrospectionEngine`

**File:** `introspection_engine.py`

```python
class IntrospectionEngine:
```

**Description:**
```
"""Produce first-person introspective reports."""

def __init__(self) -> None:
    self.narrative_generator = NarrativeGenerator()
    self.belief_explainer = BeliefExplainer()

def generate_introspection_report(
    self, result: "RecursiveReasoningResult"
) -> IntrospectionReport:
    fragments: List[str] = []
    highlights: List[IntrospectionHighlight] = []

    for level in result.levels:
        fragment = self._introspect_level(level)
        fragments.append(fragment)
```

**Public Methods:**

- `def generate_introspection_report(`

---

### `BiasInsight`

**File:** `meta_monitor.py`

```python
class BiasInsight:
```

**Description:**
```
"""Describes a cognitive bias detected during monitoring."""

name: str
severity: float
evidence: List[str]


@dataclass(slots=True)
class CalibrationMetrics:
"""Calibration quality for confidence assessments."""

brier_score: float
expected_calibration_error: float
correlation: float
```

**Public Methods:**


---

### `CalibrationMetrics`

**File:** `meta_monitor.py`

```python
class CalibrationMetrics:
```

**Description:**
```
"""Calibration quality for confidence assessments."""

brier_score: float
expected_calibration_error: float
correlation: float


@dataclass(slots=True)
class MetaMonitoringReport:
"""Full metacognitive report returned by MetaMonitor."""

total_levels: int
average_coherence: float
average_confidence: float
processing_time_ms: float
calibration: CalibrationMetrics
```

**Public Methods:**


---

### `MetaMonitoringReport`

**File:** `meta_monitor.py`

```python
class MetaMonitoringReport:
```

**Description:**
```
"""Full metacognitive report returned by MetaMonitor."""

total_levels: int
average_coherence: float
average_confidence: float
processing_time_ms: float
calibration: CalibrationMetrics
biases_detected: List[BiasInsight]
recommendations: List[str]


class MetricsCollector:
"""Aggregate raw metrics from reasoning levels."""

def collect(self, levels: Sequence["ReasoningLevel"]) -> dict:
    if not levels:
```

**Public Methods:**


---

### `MetricsCollector`

**File:** `meta_monitor.py`

```python
class MetricsCollector:
```

**Description:**
```
"""Aggregate raw metrics from reasoning levels."""

def collect(self, levels: Sequence["ReasoningLevel"]) -> dict:
    if not levels:
        return {
            "total_levels": 0,
            "average_coherence": 0.0,
            "average_confidence": 0.0,
        }

    confidences: List[float] = []
    for level in levels:
        confidences.extend([step.confidence_assessment for step in level.steps])

    return {
        "total_levels": len(levels),
```

**Public Methods:**

- `def collect(self, levels`

---

### `BiasDetector`

**File:** `meta_monitor.py`

```python
class BiasDetector:
```

**Description:**
```
"""Detect simple cognitive biases to keep reasoning antifragile."""

def detect(self, levels: Sequence["ReasoningLevel"]) -> List[BiasInsight]:
    insights: List[BiasInsight] = []

    if not levels:  # pragma: no cover - empty levels handled by monitor_reasoning
        return insights  # pragma: no cover

    if self._possible_confirmation_bias(levels):
        insights.append(  # pragma: no cover - confirmation bias detection tested
            BiasInsight(  # pragma: no cover
                name="confirmation_bias",
                severity=0.4,
                evidence=["All levels reuse identical justifications."],
            )
        )
```

**Public Methods:**

- `def detect(self, levels`

---

### `ConfidenceCalibrator`

**File:** `meta_monitor.py`

```python
class ConfidenceCalibrator:
```

**Description:**
```
"""Compute calibration metrics using reliability statistics."""

def evaluate(self, levels: Sequence["ReasoningLevel"]) -> CalibrationMetrics:
    predicted: List[float] = []
    observed: List[float] = []

    for level in levels:
        for step in level.steps:
            predicted.append(step.confidence_assessment)
            observed.append(level.coherence)

    if not predicted:  # pragma: no cover - empty levels handled by monitor_reasoning
        return CalibrationMetrics(brier_score=0.0, expected_calibration_error=0.0, correlation=0.0)  # pragma: no cover

    brier = float(mean((p - o) ** 2 for p, o in zip(predicted, observed)))
    ece = self._expected_calibration_error(predicted, observed)
```

**Public Methods:**

- `def evaluate(self, levels`

---

### `MetaMonitor`

**File:** `meta_monitor.py`

```python
class MetaMonitor:
```

**Description:**
```
"""High-level orchestrator that produces metacognitive reports."""

def __init__(self) -> None:
    self.metrics_collector = MetricsCollector()
    self.bias_detector = BiasDetector()
    self.confidence_calibrator = ConfidenceCalibrator()

def monitor_reasoning(
    self,
    result: "RecursiveReasoningResult",
) -> MetaMonitoringReport:
    metrics = self.metrics_collector.collect(result.levels)
    biases = self.bias_detector.detect(result.levels)
    calibration = self.confidence_calibrator.evaluate(result.levels)
    recommendations = self._generate_recommendations(metrics, biases, calibration)
```

**Public Methods:**

- `def monitor_reasoning(`

---

### `BeliefType`

**File:** `recursive_reasoner.py`

```python
class BeliefType(Enum):
```

**Description:**
```
"""Tipos de crenças no sistema."""

FACTUAL = "factual"  # "IP 192.168.1.1 é malicioso"
META = "meta"  # "Eu acredito que IP 192.168.1.1 é malicioso"
NORMATIVE = "normative"  # "Devo bloquear IP 192.168.1.1"
EPISTEMIC = "epistemic"  # "Minha crença sobre 192.168.1.1 é justificada"


class ContradictionType(Enum):
"""Tipos de contradições detectadas."""

DIRECT = "direct"  # A e ¬A simultaneamente
TRANSITIVE = "transitive"  # A→B, B→C, C→¬A
TEMPORAL = "temporal"  # Acreditava X antes, acredito ¬X agora sem razão
CONTEXTUAL = "contextual"  # X verdadeiro em C1, ¬X em C2 sem explicação
```

**Public Methods:**


---

### `ContradictionType`

**File:** `recursive_reasoner.py`

```python
class ContradictionType(Enum):
```

**Description:**
```
"""Tipos de contradições detectadas."""

DIRECT = "direct"  # A e ¬A simultaneamente
TRANSITIVE = "transitive"  # A→B, B→C, C→¬A
TEMPORAL = "temporal"  # Acreditava X antes, acredito ¬X agora sem razão
CONTEXTUAL = "contextual"  # X verdadeiro em C1, ¬X em C2 sem explicação


class ResolutionStrategy(Enum):
"""Estratégias de resolução de contradições."""

RETRACT_WEAKER = "retract_weaker"  # Remove crença menos confiável
WEAKEN_BOTH = "weaken_both"  # Reduz confiança de ambas
CONTEXTUALIZE = "contextualize"  # Adiciona condições contextuais
TEMPORIZE = "temporize"  # Marca como crença passada
HITL_ESCALATE = "hitl_escalate"  # Escala para humano
```

**Public Methods:**


---

### `ResolutionStrategy`

**File:** `recursive_reasoner.py`

```python
class ResolutionStrategy(Enum):
```

**Description:**
```
"""Estratégias de resolução de contradições."""

RETRACT_WEAKER = "retract_weaker"  # Remove crença menos confiável
WEAKEN_BOTH = "weaken_both"  # Reduz confiança de ambas
CONTEXTUALIZE = "contextualize"  # Adiciona condições contextuais
TEMPORIZE = "temporize"  # Marca como crença passada
HITL_ESCALATE = "hitl_escalate"  # Escala para humano


# ==================== DATACLASSES ====================


@dataclass
class Belief:
"""
Representa uma crença no sistema.
```

**Public Methods:**


---

### `Belief`

**File:** `recursive_reasoner.py`

```python
class Belief:
```

**Description:**
```
"""
Representa uma crença no sistema.

Attributes:
    id: Identificador único
    content: Conteúdo proposicional da crença
    belief_type: Tipo de crença (factual, meta, normative, epistemic)
    confidence: Nível de confiança [0.0, 1.0]
    justification: Crença(s) que justificam esta
    context: Contexto em que crença é válida
    timestamp: Quando crença foi formada
    meta_level: Nível de abstração (0=objeto, 1=meta, 2=meta-meta, etc.)
"""

content: str
belief_type: BeliefType = BeliefType.FACTUAL
```

**Public Methods:**

- `def is_negation_of(self, other`
- `def strip_negations(cls, text`

---

### `Contradiction`

**File:** `recursive_reasoner.py`

```python
class Contradiction:
```

**Description:**
```
"""
Representa uma contradição detectada.

Attributes:
    belief_a: Primeira crença contraditória
    belief_b: Segunda crença contraditória
    contradiction_type: Tipo de contradição
    severity: Severidade [0.0, 1.0]
    explanation: Explicação da contradição
    suggested_resolution: Estratégia sugerida
"""

belief_a: Belief
belief_b: Belief
contradiction_type: ContradictionType
severity: float = 1.0
```

**Public Methods:**


---

### `Resolution`

**File:** `recursive_reasoner.py`

```python
class Resolution:
```

**Description:**
```
"""
Representa a resolução de uma contradição.

Attributes:
    contradiction: Contradição resolvida
    strategy: Estratégia usada
    beliefs_modified: Crenças modificadas
    beliefs_removed: Crenças removidas
    new_beliefs: Novas crenças adicionadas
    timestamp: Quando resolução foi aplicada
"""

contradiction: Contradiction
strategy: ResolutionStrategy
beliefs_modified: List[Belief] = field(default_factory=list)
beliefs_removed: List[Belief] = field(default_factory=list)
```

**Public Methods:**


---

### `ReasoningStep`

**File:** `recursive_reasoner.py`

```python
class ReasoningStep:
```

**Description:**
```
"""
Representa um passo de raciocínio.

Attributes:
    belief: Crença sendo processada
    meta_level: Nível de abstração
    justification_chain: Cadeia de justificações
    confidence_assessment: Avaliação de confiança
    timestamp: Quando passo foi executado
"""

belief: Belief
meta_level: int
justification_chain: List[Belief] = field(default_factory=list)
confidence_assessment: float = 0.5
timestamp: datetime = field(default_factory=datetime.now)
```

**Public Methods:**


---

### `ReasoningLevel`

**File:** `recursive_reasoner.py`

```python
class ReasoningLevel:
```

**Description:**
```
"""
Representa um nível completo de raciocínio.

Attributes:
    level: Número do nível (0=objeto, 1=meta, etc.)
    beliefs: Crenças neste nível
    coherence: Coerência interna [0.0, 1.0]
    steps: Passos de raciocínio executados
"""

level: int
beliefs: List[Belief] = field(default_factory=list)
coherence: float = 1.0
steps: List[ReasoningStep] = field(default_factory=list)
```

**Public Methods:**


---

### `RecursiveReasoningResult`

**File:** `recursive_reasoner.py`

```python
class RecursiveReasoningResult:
```

**Description:**
```
"""
Resultado de raciocínio recursivo completo.

Attributes:
    levels: Níveis de raciocínio executados
    final_depth: Profundidade alcançada
    coherence_score: Coerência global [0.0, 1.0]
    contradictions_detected: Contradições encontradas
    resolutions_applied: Resoluções aplicadas
    timestamp: Quando raciocínio foi executado
"""

levels: List[ReasoningLevel]
final_depth: int
coherence_score: float
contradictions_detected: List[Contradiction] = field(default_factory=list)
```

**Public Methods:**


---

### `BeliefGraph`

**File:** `recursive_reasoner.py`

```python
class BeliefGraph:
```

**Description:**
```
"""
Grafo de crenças e suas inter-relações.

Permite:
- Adicionar crenças e justificações
- Detectar contradições (diretas, transitivas, temporais)
- Resolver contradições através de revisão
- Calcular coerência do grafo
"""

def __init__(self):
    """Initialize belief graph."""
    self.beliefs: Set[Belief] = set()
    self.justifications: Dict[UUID, List[Belief]] = defaultdict(list)
    self.timestamp_index: Dict[datetime, Set[Belief]] = defaultdict(set)
    self.context_index: Dict[str, Set[Belief]] = defaultdict(set)
```

**Public Methods:**

- `def add_belief(`
- `def detect_contradictions(self) -> List[Contradiction]`
- `def resolve_belief(self, belief`
- `def calculate_coherence(self) -> float`

---

### `RecursiveReasoner`

**File:** `recursive_reasoner.py`

```python
class RecursiveReasoner:
```

**Description:**
```
"""
Motor de raciocínio recursivo.

Permite que MAXIMUS raciocine sobre seu próprio raciocínio
em múltiplos níveis de abstração.
"""

def __init__(self, max_depth: int = 3):
    """
    Initialize recursive reasoner.

    Args:
        max_depth: Profundidade máxima de recursão (default 3)
                  1 = simples, 2 = meta, 3+ = meta-meta
    """
    if max_depth < 1:
```

**Public Methods:**


---

### `ArousalRateLimiter`

**File:** `controller.py`

```python
class ArousalRateLimiter:
```

**Description:**
```
"""
Enforces maximum rate of change for arousal value.

Prevents arousal from changing too rapidly (physiologically implausible).
Biological arousal systems have finite bandwidth - neuromodulators take
time to diffuse and act.

HARD LIMIT: Arousal can change at most ±0.20 per second.
"""

def __init__(self, max_delta_per_second: float = 0.20):
    """
    Args:
        max_delta_per_second: Maximum absolute change per second
    """
    self.max_delta_per_second = max_delta_per_second
```

**Public Methods:**

- `def limit(self, new_arousal`

---

### `ArousalBoundEnforcer`

**File:** `controller.py`

```python
class ArousalBoundEnforcer:
```

**Description:**
```
"""
Enforces hard bounds [0.0, 1.0] on arousal value.

HARD LIMIT: Arousal must always be in [0.0, 1.0].
"""

@staticmethod
def enforce(arousal: float) -> float:
    """Clamp arousal to [0.0, 1.0]."""
    return float(np.clip(arousal, 0.0, 1.0))


# FASE VII: Hard limits for MCEA safety
MAX_AROUSAL_DELTA_PER_SECOND = 0.20  # Hard limit on arousal rate of change
AROUSAL_SATURATION_THRESHOLD_SECONDS = 10.0  # Time at 0.0 or 1.0 = saturation
AROUSAL_OSCILLATION_WINDOW = 20  # Track last 20 arousal values
```

**Public Methods:**

- `def enforce(arousal`

---

### `ArousalLevel`

**File:** `controller.py`

```python
class ArousalLevel(Enum):
```

**Description:**
```
"""Classification of arousal states."""

SLEEP = "sleep"  # 0.0-0.2: Minimal/no consciousness
DROWSY = "drowsy"  # 0.2-0.4: Reduced awareness
RELAXED = "relaxed"  # 0.4-0.6: Normal baseline
ALERT = "alert"  # 0.6-0.8: Heightened awareness
HYPERALERT = "hyperalert"  # 0.8-1.0: Stress/panic state


@dataclass
class ArousalState:
"""
Current arousal state.

Represents the global excitability/wakefulness level.
"""
```

**Public Methods:**


---

### `ArousalState`

**File:** `controller.py`

```python
class ArousalState:
```

**Description:**
```
"""
Current arousal state.

Represents the global excitability/wakefulness level.
"""

# Core arousal value (0.0 - 1.0)
arousal: float = 0.6  # Default: RELAXED

# Classification
level: ArousalLevel = field(default=ArousalLevel.RELAXED, init=False)

# Contributing factors (for transparency)
baseline_arousal: float = 0.6
need_contribution: float = 0.0  # From MMEI needs
external_contribution: float = 0.0  # From threats/tasks
```

**Public Methods:**

- `def get_arousal_factor(self) -> float`
- `def compute_effective_threshold(self, base_threshold`

---

### `ArousalModulation`

**File:** `controller.py`

```python
class ArousalModulation:
```

**Description:**
```
"""
Request to modulate arousal.

External systems can request arousal changes (e.g., threat detection).
"""

source: str  # What requested modulation
delta: float  # Change in arousal (-1.0 to +1.0)
duration_seconds: float = 0.0  # How long effect lasts (0 = instant)
priority: int = 1  # Higher priority overrides

timestamp: float = field(default_factory=time.time)

def is_expired(self) -> bool:
    """Check if modulation has expired."""
    if self.duration_seconds == 0.0:
```

**Public Methods:**

- `def is_expired(self) -> bool`
- `def get_current_delta(self) -> float`

---

### `ArousalConfig`

**File:** `controller.py`

```python
class ArousalConfig:
```

**Description:**
```
"""Configuration for arousal controller."""

# Baseline arousal (resting state)
baseline_arousal: float = 0.6  # RELAXED default

# Update rate
update_interval_ms: float = 100.0  # 10 Hz

# Time constants (how fast arousal changes)
arousal_increase_rate: float = 0.05  # Per second when increasing
arousal_decrease_rate: float = 0.02  # Per second when decreasing (slower)

# Need influence (how much MMEI needs affect arousal)
repair_need_weight: float = 0.3  # Errors increase arousal
rest_need_weight: float = -0.2  # Fatigue decreases arousal
efficiency_need_weight: float = 0.1
```

**Public Methods:**


---

### `ArousalController`

**File:** `controller.py`

```python
class ArousalController:
```

**Description:**
```
"""
Controls global arousal/excitability state.

This is the MPE foundation - contentless wakefulness that modulates
readiness for conscious experience (ESGT ignition).

The controller continuously updates arousal based on:
- Internal needs (MMEI)
- External events (threats, tasks)
- Temporal dynamics (stress, recovery, circadian)
- ESGT history (refractory periods)

Architecture:
-------------
Needs + External → Arousal Update → ESGT Threshold Modulation
```

**Public Methods:**

- `def register_arousal_callback(self, callback`
- `def get_current_arousal(self) -> ArousalState`
- `def get_esgt_threshold(self) -> float`
- `def request_modulation(self, source`
- `def update_from_needs(self, needs`
- `def apply_esgt_refractory(self) -> None`
- `def get_stress_level(self) -> float`
- `def reset_stress(self) -> None`
- `def get_statistics(self) -> dict[str, any]`
- `def get_health_metrics(self) -> dict[str, any]`

---

### `StressLevel`

**File:** `stress.py`

```python
class StressLevel(Enum):
```

**Description:**
```
"""Classification of stress intensity."""

NONE = "none"  # 0.0-0.2
MILD = "mild"  # 0.2-0.4
MODERATE = "moderate"  # 0.4-0.6
SEVERE = "severe"  # 0.6-0.8
CRITICAL = "critical"  # 0.8-1.0


class StressType(Enum):
"""Types of stress that can be applied."""

COMPUTATIONAL_LOAD = "computational_load"  # High CPU/memory
ERROR_INJECTION = "error_injection"  # System failures
NETWORK_DEGRADATION = "network_degradation"  # Latency/loss
AROUSAL_FORCING = "arousal_forcing"  # Forced high arousal
```

**Public Methods:**


---

### `StressType`

**File:** `stress.py`

```python
class StressType(Enum):
```

**Description:**
```
"""Types of stress that can be applied."""

COMPUTATIONAL_LOAD = "computational_load"  # High CPU/memory
ERROR_INJECTION = "error_injection"  # System failures
NETWORK_DEGRADATION = "network_degradation"  # Latency/loss
AROUSAL_FORCING = "arousal_forcing"  # Forced high arousal
RAPID_CHANGE = "rapid_change"  # Fast state transitions
COMBINED = "combined"  # Multiple stressors


@dataclass
class StressResponse:
"""
Measured response to stress application.

Records system behavior under stress for analysis.
```

**Public Methods:**


---

### `StressResponse`

**File:** `stress.py`

```python
class StressResponse:
```

**Description:**
```
"""
Measured response to stress application.

Records system behavior under stress for analysis.
"""

stress_type: StressType
stress_level: StressLevel

# Arousal response
initial_arousal: float
peak_arousal: float
final_arousal: float
arousal_stability_cv: float  # Coefficient of variation

# Need response
```

**Public Methods:**

- `def get_resilience_score(self) -> float`
- `def passed_stress_test(self) -> bool`

---

### `StressTestConfig`

**File:** `stress.py`

```python
class StressTestConfig:
```

**Description:**
```
"""Configuration for stress testing."""

# Test durations
stress_duration_seconds: float = 30.0
recovery_duration_seconds: float = 60.0

# Thresholds
arousal_runaway_threshold: float = 0.95  # Arousal stuck above this
arousal_runaway_duration: float = 10.0  # For this long = runaway
coherence_collapse_threshold: float = 0.50
recovery_baseline_tolerance: float = 0.1  # Within 10% of baseline

# Stress intensities
load_stress_cpu_percent: float = 90.0
error_stress_rate_per_min: float = 20.0
network_stress_latency_ms: float = 200.0
```

**Public Methods:**


---

### `StressMonitor`

**File:** `stress.py`

```python
class StressMonitor:
```

**Description:**
```
"""
Monitors system stress and conducts stress testing.

This module enables:
1. Continuous stress level monitoring
2. Deliberate stress testing for validation
3. Breakdown detection and alerting
4. Resilience assessment

The monitor can passively observe stress or actively inject it.

Architecture:
-------------
Passive Mode:
  Monitor arousal + needs → Classify stress → Alert if critical
```

**Public Methods:**

- `def register_stress_alert(`
- `def get_current_stress_level(self) -> StressLevel`
- `def get_stress_history(self, window_seconds`
- `def get_test_results(self) -> list[StressResponse]`
- `def get_average_resilience(self) -> float`
- `def get_statistics(self) -> dict[str, Any]`

---

### `AttentionSignal`

**File:** `attention_schema.py`

```python
class AttentionSignal:
```

**Description:**
```
"""
Represents a single sensory or cognitive signal competing for attention.

Attributes:
    modality: Source modality (e.g. "visual", "auditory", "proprioceptive")
    target: Target entity or identifier (e.g. "threat:192.168.1.1")
    intensity: Raw signal intensity [0, 1]
    novelty: Novelty factor compared to recent history [0, 1]
    relevance: Task relevance weight [0, 1]
    urgency: Urgency weight (time-critical) [0, 1]
"""

modality: str
target: str
intensity: float
novelty: float
```

**Public Methods:**

- `def normalized_score(self) -> float`

---

### `AttentionState`

**File:** `attention_schema.py`

```python
class AttentionState:
```

**Description:**
```
"""
Output of the attention schema model.

Attributes:
    focus_target: Identifier of the entity receiving maximal attention
    modality_weights: Normalized distribution over modalities
    confidence: Confidence in the current focus attribution [0, 1]
    salience_order: Ranked list of (target, score)
    baseline_intensity: Rolling average of intensities (homeostatic reference)
"""

focus_target: str
modality_weights: Dict[str, float]
confidence: float
salience_order: List[tuple[str, float]]
baseline_intensity: float
```

**Public Methods:**


---

### `PredictionTrace`

**File:** `attention_schema.py`

```python
class PredictionTrace:
```

**Description:**
```
"""Stores historical prediction vs observation pairs for calibration."""

predicted_focus: str
actual_focus: str
prediction_confidence: float
match: bool


# ==================== MODEL ====================


class AttentionSchemaModel:
"""
Attention schema responsible for generating attention states and
prediction errors for MAXIMUS consciousness.
"""
```

**Public Methods:**


---

### `AttentionSchemaModel`

**File:** `attention_schema.py`

```python
class AttentionSchemaModel:
```

**Description:**
```
"""
Attention schema responsible for generating attention states and
prediction errors for MAXIMUS consciousness.
"""

HISTORY_WINDOW: int = 200

def __init__(self) -> None:
    self._intensity_history: Deque[float] = deque(maxlen=self.HISTORY_WINDOW)
    self._prediction_traces: Deque[PredictionTrace] = deque(maxlen=self.HISTORY_WINDOW)
    self._last_state: AttentionState | None = None

# ----- Public API -----------------------------------------------------

def update(self, signals: Sequence[AttentionSignal]) -> AttentionState:
    """
```

**Public Methods:**

- `def update(self, signals`
- `def record_prediction_outcome(self, actual_focus`
- `def prediction_accuracy(self, window`
- `def prediction_calibration(self, window`
- `def prediction_variability(self, window`

---

### `BoundaryAssessment`

**File:** `boundary_detector.py`

```python
class BoundaryAssessment:
```

**Description:**
```
"""
Assessment of the ego/world boundary.

Attributes:
    strength: Relative strength of boundary (0 weak / 1 strong)
    stability: Coefficient of variation for boundary over recent samples
    proprioception_mean: Average proprioceptive intensity
    exteroception_mean: Average exteroceptive intensity
"""

strength: float
stability: float
proprioception_mean: float
exteroception_mean: float
```

**Public Methods:**


---

### `BoundaryDetector`

**File:** `boundary_detector.py`

```python
class BoundaryDetector:
```

**Description:**
```
"""
Detects self-other boundary using proprioceptive vs exteroceptive signals.
"""

WINDOW: int = 100

def __init__(self) -> None:
    self._strength_history: Deque[float] = deque(maxlen=self.WINDOW)
    self._proprio_history: Deque[float] = deque(maxlen=self.WINDOW)
    self._extero_history: Deque[float] = deque(maxlen=self.WINDOW)

def evaluate(
    self,
    proprioceptive_signals: Iterable[float],
    exteroceptive_signals: Iterable[float],
) -> BoundaryAssessment:
```

**Public Methods:**

- `def evaluate(`

---

### `ValidationMetrics`

**File:** `prediction_validator.py`

```python
class ValidationMetrics:
```

**Description:**
```
"""
Summary of validation results for attention predictions.

Attributes:
    accuracy: Proportion of correct predictions
    calibration_error: Expected calibration error (ECE)
    mean_confidence: Average confidence across predictions
    focus_switch_rate: Rate of focus changes between predictions
"""

accuracy: float
calibration_error: float
mean_confidence: float
focus_switch_rate: float
```

**Public Methods:**


---

### `PredictionValidator`

**File:** `prediction_validator.py`

```python
class PredictionValidator:
```

**Description:**
```
"""Validates attention predictions against observed attention states."""

def validate(
    self,
    predictions: Sequence[AttentionState],
    observations: Sequence[str],
) -> ValidationMetrics:
    if not predictions:
        raise ValueError("No predictions provided for validation")
    if len(predictions) != len(observations):
        raise ValueError("Predictions and observations must have matching length")

    accuracy = self._compute_accuracy(predictions, observations)
    calibration_error = self._compute_ece(predictions, observations)
    mean_confidence = float(sum(state.confidence for state in predictions) / len(predictions))
    switch_rate = self._compute_focus_switch_rate(predictions)
```

**Public Methods:**

- `def validate(`

---

### `FirstPersonPerspective`

**File:** `self_model.py`

```python
class FirstPersonPerspective:
```

**Description:**
```
"""Represents the orientation of the self-model in world coordinates."""

viewpoint: Tuple[float, float, float]  # xyz
orientation: Tuple[float, float, float]  # pitch, yaw, roll
timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class IntrospectiveSummary:
"""Report summarising current self state."""

narrative: str
confidence: float
boundary_stability: float
focus_target: str
perspective: FirstPersonPerspective
```

**Public Methods:**


---

### `IntrospectiveSummary`

**File:** `self_model.py`

```python
class IntrospectiveSummary:
```

**Description:**
```
"""Report summarising current self state."""

narrative: str
confidence: float
boundary_stability: float
focus_target: str
perspective: FirstPersonPerspective


class SelfModel:
"""
Maintains the self-model that bridges attention states and body schema.
"""

def __init__(self) -> None:
    self._perspective_history: List[FirstPersonPerspective] = []
```

**Public Methods:**


---

### `SelfModel`

**File:** `self_model.py`

```python
class SelfModel:
```

**Description:**
```
"""
Maintains the self-model that bridges attention states and body schema.
"""

def __init__(self) -> None:
    self._perspective_history: List[FirstPersonPerspective] = []
    self._attention_history: List[AttentionState] = []
    self._boundary_history: List[BoundaryAssessment] = []
    self._identity_vector: Tuple[float, float, float] = (0.0, 0.0, 1.0)

def update(
    self,
    attention_state: AttentionState,
    boundary: BoundaryAssessment,
    proprio_center: Tuple[float, float, float],
    orientation: Tuple[float, float, float],
```

**Public Methods:**

- `def update(`
- `def current_perspective(self) -> FirstPersonPerspective`
- `def current_focus(self) -> AttentionState`
- `def current_boundary(self) -> BoundaryAssessment`
- `def generate_first_person_report(self) -> IntrospectiveSummary`
- `def self_vector(self) -> Tuple[float, float, float]`

---

### `MetacognitiveMonitor`

**File:** `monitor.py`

```python
class MetacognitiveMonitor:
```

**Description:**
```
"""
Tracks reasoning quality and calculates confidence.

Implements simple error-based confidence calculation:
- Records prediction errors (0-1, where 1 = complete error)
- Maintains sliding window of recent errors
- Confidence = 1 - average_error

Usage:
    monitor = MetacognitiveMonitor(window_size=100)

    # Record error after prediction validated
    monitor.record_error(error=0.2)  # 20% error

    # Get current confidence
    confidence = monitor.calculate_confidence()
```

**Public Methods:**

- `def record_error(self, error`
- `def calculate_confidence(self) -> float`
- `def get_recent_errors(self, n`
- `def get_error_trend(self, window`
- `def reset(self) -> None`
- `def get_stats(self) -> Dict[str, Any]`

---

### `GoalType`

**File:** `goals.py`

```python
class GoalType(Enum):
```

**Description:**
```
"""Classification of goal types."""

# Homeostatic (deficit-reduction)
REST = "rest"  # Reduce computational load
REPAIR = "repair"  # Fix errors, restore integrity
OPTIMIZE = "optimize"  # Improve efficiency
RESTORE = "restore"  # Restore connectivity/communication

# Growth (exploration/expansion)
EXPLORE = "explore"  # Explore new capabilities
LEARN = "learn"  # Acquire new patterns
CREATE = "create"  # Generate novel outputs


class GoalPriority(Enum):
"""Goal priority levels (maps to NeedUrgency)."""
```

**Public Methods:**


---

### `GoalPriority`

**File:** `goals.py`

```python
class GoalPriority(Enum):
```

**Description:**
```
"""Goal priority levels (maps to NeedUrgency)."""

BACKGROUND = 0  # Optional, non-urgent
LOW = 1  # Should do eventually
MODERATE = 2  # Should do soon
HIGH = 3  # Important, do quickly
CRITICAL = 4  # Urgent, do immediately


@dataclass
class Goal:
"""
Autonomous goal generated from internal needs.

Goals represent internally-motivated intentions to act.
They persist until satisfied or timeout.
```

**Public Methods:**


---

### `Goal`

**File:** `goals.py`

```python
class Goal:
```

**Description:**
```
"""
Autonomous goal generated from internal needs.

Goals represent internally-motivated intentions to act.
They persist until satisfied or timeout.
"""

goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
goal_type: GoalType = GoalType.REST
priority: GoalPriority = GoalPriority.LOW

# Description
description: str = ""
target_component: str | None = None  # Which system to act on

# Motivation
```

**Public Methods:**

- `def is_expired(self) -> bool`
- `def is_satisfied(self, current_need_value`
- `def mark_satisfied(self) -> None`
- `def record_execution_attempt(self) -> None`
- `def get_age_seconds(self) -> float`
- `def get_priority_score(self) -> float`

---

### `GoalGenerationConfig`

**File:** `goals.py`

```python
class GoalGenerationConfig:
```

**Description:**
```
"""Configuration for autonomous goal generation."""

# Generation thresholds (when to generate goals)
rest_threshold: float = 0.60  # CPU/memory fatigue
repair_threshold: float = 0.40  # Error detection (lower = more sensitive)
efficiency_threshold: float = 0.50  # Resource optimization
connectivity_threshold: float = 0.50  # Network issues
curiosity_threshold: float = 0.60  # Exploration drive
learning_threshold: float = 0.50  # Learning opportunities

# Satisfaction thresholds (when goals complete)
rest_satisfied: float = 0.30
repair_satisfied: float = 0.20
efficiency_satisfied: float = 0.30
connectivity_satisfied: float = 0.30
```

**Public Methods:**


---

### `AutonomousGoalGenerator`

**File:** `goals.py`

```python
class AutonomousGoalGenerator:
```

**Description:**
```
"""
Generates autonomous goals from internal needs.

This is the motivational engine - translating phenomenal "feelings"
(needs) into actionable intentions (goals).

The generator runs continuously, monitoring needs and creating goals
when thresholds exceeded. Goals persist until needs satisfied.

Architecture:
-------------
InternalStateMonitor → AbstractNeeds
       ↓
AutonomousGoalGenerator → Goals
       ↓
HCL / Action Systems
```

**Public Methods:**

- `def register_goal_consumer(self, consumer`
- `def generate_goals(self, needs`
- `def get_active_goals(self, sort_by_priority`
- `def get_critical_goals(self) -> list[Goal]`
- `def get_goals_by_type(self, goal_type`
- `def get_statistics(self) -> dict[str, Any]`

---

### `NeedUrgency`

**File:** `monitor.py`

```python
class NeedUrgency(Enum):
```

**Description:**
```
"""Classification of need urgency levels."""

SATISFIED = "satisfied"  # need < 0.20 - no action required
LOW = "low"  # 0.20 ≤ need < 0.40 - background concern
MODERATE = "moderate"  # 0.40 ≤ need < 0.60 - should address soon
HIGH = "high"  # 0.60 ≤ need < 0.80 - requires attention
CRITICAL = "critical"  # need ≥ 0.80 - immediate action needed


@dataclass
class PhysicalMetrics:
"""
Raw physical/computational metrics collected from system.

These are the "receptor signals" analogous to biological interoception.
Values are normalized to [0, 1] range where possible.
```

**Public Methods:**


---

### `PhysicalMetrics`

**File:** `monitor.py`

```python
class PhysicalMetrics:
```

**Description:**
```
"""
Raw physical/computational metrics collected from system.

These are the "receptor signals" analogous to biological interoception.
Values are normalized to [0, 1] range where possible.
"""

# Computational load
cpu_usage_percent: float = 0.0  # 0-100 → normalized to 0-1
memory_usage_percent: float = 0.0  # 0-100 → normalized to 0-1

# System health
error_rate_per_min: float = 0.0  # Errors detected per minute
exception_count: int = 0  # Recent exceptions

# Physical state (if available)
```

**Public Methods:**

- `def normalize(self) -> "PhysicalMetrics"`

---

### `AbstractNeeds`

**File:** `monitor.py`

```python
class AbstractNeeds:
```

**Description:**
```
"""
Abstract psychological/phenomenal needs derived from physical metrics.

This is the "feeling" layer - the phenomenal experience of bodily state.
All values normalized to [0, 1] where 1.0 = maximum need.

Biological Correspondence:
- rest_need: Fatigue sensation
- repair_need: Pain/discomfort signaling damage
- efficiency_need: Thermal discomfort, energy depletion
- connectivity_need: Social isolation feeling
- curiosity_drive: Boredom, exploration urge
"""

# Primary needs (deficit-based)
rest_need: float = 0.0  # Need to reduce computational load
```

**Public Methods:**

- `def get_most_urgent(self) -> tuple[str, float, NeedUrgency]`
- `def get_critical_needs(self, threshold`

---

### `InteroceptionConfig`

**File:** `monitor.py`

```python
class InteroceptionConfig:
```

**Description:**
```
"""Configuration for internal state monitoring."""

# Collection intervals
collection_interval_ms: float = 100.0  # 10 Hz default

# Moving average windows
short_term_window_samples: int = 10  # 1 second at 10 Hz
long_term_window_samples: int = 50  # 5 seconds at 10 Hz

# Need computation weights
cpu_weight: float = 0.6  # CPU contributes 60% to rest_need
memory_weight: float = 0.4  # Memory contributes 40% to rest_need

# Thresholds
error_rate_critical: float = 10.0  # 10 errors/min = critical
temperature_warning_celsius: float = 80.0
```

**Public Methods:**


---

### `RateLimiter`

**File:** `monitor.py`

```python
class RateLimiter:
```

**Description:**
```
"""
Sliding window rate limiter for goal generation.

Prevents MMEI from overwhelming downstream systems (ESGT/HCL) with
excessive goal generation. Uses sliding window algorithm for smooth
enforcement (no burst allowance).

HARD LIMIT: Goals per minute cannot exceed max_per_minute.
"""

def __init__(self, max_per_minute: int = 5):
    """
    Args:
        max_per_minute: Maximum goals allowed per 60-second window
    """
    self.max_per_minute = max_per_minute
```

**Public Methods:**

- `def allow(self) -> bool`
- `def get_current_rate(self) -> int`

---

### `Goal`

**File:** `monitor.py`

```python
class Goal:
```

**Description:**
```
"""
Autonomous goal generated from abstract needs.

Goals are the action layer - translating needs into concrete objectives
that can be executed by downstream systems (HCL, ESGT).
"""

goal_id: str  # Unique identifier
need_source: str  # Which need generated this (e.g., "rest_need")
description: str  # Human-readable goal description
priority: NeedUrgency  # Urgency level
need_value: float  # Need value that triggered goal (0-1)
timestamp: float = field(default_factory=time.time)
executed: bool = False

def compute_hash(self) -> str:
```

**Public Methods:**

- `def compute_hash(self) -> str`

---

### `InternalStateMonitor`

**File:** `monitor.py`

```python
class InternalStateMonitor:
```

**Description:**
```
"""
Monitors internal physical/computational state and translates to abstract needs.

This is the core interoception engine - continuously collecting physical
metrics and computing phenomenal "feelings" (abstract needs).

Architecture:
-------------
Physical Layer:
  ↓ (metrics collection)
PhysicalMetrics
  ↓ (translation)
AbstractNeeds
  ↓ (goal generation)
Autonomous Goals → ESGT → HCL
```

**Public Methods:**

- `def set_metrics_collector(self, collector`
- `def register_need_callback(self, callback`
- `def get_current_needs(self) -> AbstractNeeds | None`
- `def get_current_metrics(self) -> PhysicalMetrics | None`
- `def get_needs_trend(self, need_name`
- `def get_moving_average(self, need_name`
- `def get_statistics(self) -> dict[str, any]`
- `def generate_goal_from_need(`
- `def mark_goal_executed(self, goal_id`
- `def get_health_metrics(self) -> dict[str, any]`

---

### `AcetylcholineModulator`

**File:** `acetylcholine_hardened.py`

```python
class AcetylcholineModulator(NeuromodulatorBase):
```

**Description:**
```
"""
Acetylcholine modulator with bounded, smooth, homeostatic behavior.

Biological Characteristics:
- LOWER baseline (0.4) - acetylcholine is phasic (burst-driven)
- MODERATE decay (0.012/s) - moderate persistence
- Standard desensitization threshold (0.8)

Usage identical to DopamineModulator:
    modulator = AcetylcholineModulator(kill_switch_callback=safety.kill_switch.trigger)
    actual_change = modulator.modulate(delta=0.3, source="surprise_signal")
    level = modulator.level
    metrics = modulator.get_health_metrics()
"""

def __init__(
```

**Public Methods:**

- `def get_modulator_name(self) -> str`

---

### `CoordinatorConfig`

**File:** `coordinator_hardened.py`

```python
class CoordinatorConfig:
```

**Description:**
```
"""Configuration for neuromodulation coordination.

Defines interaction weights and conflict resolution parameters.
"""

# Antagonistic interactions (negative weight = opposition)
# DA-5HT: Dopamine (reward-seeking) antagonizes Serotonin (impulse control)
da_5ht_antagonism: float = -0.3  # DA↑ suppresses 5HT effect, vice versa

# Synergistic interactions (positive weight = enhancement)
# ACh-NE: Acetylcholine (attention) + Norepinephrine (arousal) = focused alertness
ach_ne_synergy: float = 0.2  # ACh↑ + NE↑ = enhanced effect

# Conflict resolution
conflict_threshold: float = 0.7  # Conflict score above this triggers resolution
conflict_reduction_factor: float = 0.5  # Reduce conflicting deltas by this factor
```

**Public Methods:**


---

### `ModulationRequest`

**File:** `coordinator_hardened.py`

```python
class ModulationRequest:
```

**Description:**
```
"""Request to modulate a specific neuromodulator."""

modulator: str  # "dopamine", "serotonin", "acetylcholine", "norepinephrine"
delta: float  # Requested change
source: str  # Source of request (for logging)


class NeuromodulationCoordinator:
"""
Coordinates modulations across 4 neuromodulators with conflict resolution.

This coordinator ensures:
1. **Conflict Detection**: Detects antagonistic modulation patterns (DA↑ + 5HT↑)
2. **Conflict Resolution**: Reduces magnitude of conflicting requests
3. **Non-linear Interactions**: Applies DA-5HT antagonism, ACh-NE synergy
4. **Bounded Behavior**: All modulators guaranteed [0, 1]
```

**Public Methods:**


---

### `NeuromodulationCoordinator`

**File:** `coordinator_hardened.py`

```python
class NeuromodulationCoordinator:
```

**Description:**
```
"""
Coordinates modulations across 4 neuromodulators with conflict resolution.

This coordinator ensures:
1. **Conflict Detection**: Detects antagonistic modulation patterns (DA↑ + 5HT↑)
2. **Conflict Resolution**: Reduces magnitude of conflicting requests
3. **Non-linear Interactions**: Applies DA-5HT antagonism, ACh-NE synergy
4. **Bounded Behavior**: All modulators guaranteed [0, 1]
5. **Aggregate Circuit Breaker**: If ≥3 modulators fail → system kill switch
6. **Full Observability**: Aggregates metrics from all 4 modulators

Usage:
    coordinator = NeuromodulationCoordinator(kill_switch_callback=safety.kill_switch.trigger)

    # Request modulations
    requests = [
```

**Public Methods:**

- `def coordinate_modulation(self, requests`
- `def get_levels(self) -> dict[str, float]`
- `def get_health_metrics(self) -> dict`
- `def emergency_stop(self)`

---

### `ModulatorConfig`

**File:** `dopamine_hardened.py`

```python
class ModulatorConfig:
```

**Description:**
```
"""Immutable configuration for dopamine modulator.

All parameters validated on init. Configuration cannot be changed
after creation (fail-fast if invalid).
"""

baseline: float = 0.5  # Homeostatic set point [0, 1]
min_level: float = 0.0  # HARD LOWER BOUND
max_level: float = 1.0  # HARD UPPER BOUND

# Decay parameters
decay_rate: float = 0.01  # Per-second decay toward baseline (0.01 = 1%/s)

# Temporal smoothing
smoothing_factor: float = 0.2  # Exponential smoothing (0=instant, 1=no change)
```

**Public Methods:**


---

### `ModulatorState`

**File:** `dopamine_hardened.py`

```python
class ModulatorState:
```

**Description:**
```
"""Current observable state of dopamine modulator.

Exposed for monitoring by Safety Core and debugging.
"""

level: float  # Current dopamine level [0, 1]
baseline: float  # Homeostatic baseline
is_desensitized: bool  # True if above desensitization threshold
last_update_time: float  # Unix timestamp of last modulation
total_modulations: int  # Total modulations since init
bounded_corrections: int  # How many times we hit bounds (anomaly signal)
desensitization_events: int  # How many times desensitization was triggered


class DopamineModulator:
"""
```

**Public Methods:**


---

### `DopamineModulator`

**File:** `dopamine_hardened.py`

```python
class DopamineModulator:
```

**Description:**
```
"""
Production-hardened dopamine modulator with BOUNDED, SMOOTH, HOMEOSTATIC behavior.

This class mirrors biological dopamine dynamics with safety constraints:

1. **Bounded Levels [0, 1]**: Dopamine cannot go negative or exceed max.
   Enforced via HARD CLAMP after every modulation.

2. **Desensitization**: Above threshold (0.8), modulations have diminishing
   returns (multiplied by desensitization_factor 0.5). Prevents runaway.

3. **Homeostatic Decay**: Exponential decay toward baseline over time.
   Mimics reuptake mechanisms in biological systems.

4. **Temporal Smoothing**: Changes are smoothed via exponential moving average.
   Prevents instant jumps (biologically implausible).
```

**Public Methods:**

- `def level(self) -> float`
- `def state(self) -> ModulatorState`
- `def modulate(self, delta`
- `def reset_circuit_breaker(self)`
- `def emergency_stop(self)`
- `def get_health_metrics(self) -> dict`

---

### `ModulatorConfig`

**File:** `modulator_base.py`

```python
class ModulatorConfig:
```

**Description:**
```
"""Immutable configuration for neuromodulator.

All parameters validated on init. Configuration cannot be changed
after creation (fail-fast if invalid).
"""

baseline: float = 0.5  # Homeostatic set point [0, 1]
min_level: float = 0.0  # HARD LOWER BOUND
max_level: float = 1.0  # HARD UPPER BOUND

# Decay parameters
decay_rate: float = 0.01  # Per-second decay toward baseline (0.01 = 1%/s)

# Temporal smoothing
smoothing_factor: float = 0.2  # Exponential smoothing (0=instant, 1=no change)
```

**Public Methods:**


---

### `ModulatorState`

**File:** `modulator_base.py`

```python
class ModulatorState:
```

**Description:**
```
"""Current observable state of neuromodulator.

Exposed for monitoring by Safety Core and debugging.
"""

level: float  # Current modulator level [0, 1]
baseline: float  # Homeostatic baseline
is_desensitized: bool  # True if above desensitization threshold
last_update_time: float  # Unix timestamp of last modulation
total_modulations: int  # Total modulations since init
bounded_corrections: int  # How many times we hit bounds (anomaly signal)
desensitization_events: int  # How many times desensitization was triggered


class NeuromodulatorBase(ABC):
"""
```

**Public Methods:**


---

### `NeuromodulatorBase`

**File:** `modulator_base.py`

```python
class NeuromodulatorBase(ABC):
```

**Description:**
```
"""
Base class for all neuromodulators with BOUNDED, SMOOTH, HOMEOSTATIC behavior.

This class implements safety mechanisms validated in DopamineModulator:

1. **Bounded Levels [0, 1]**: Levels cannot go negative or exceed max.
   Enforced via HARD CLAMP after every modulation.

2. **Desensitization**: Above threshold, modulations have diminishing
   returns. Prevents runaway.

3. **Homeostatic Decay**: Exponential decay toward baseline over time.
   Mimics reuptake mechanisms in biological systems.

4. **Temporal Smoothing**: Changes are smoothed via exponential moving average.
   Prevents instant jumps (biologically implausible).
```

**Public Methods:**

- `def get_modulator_name(self) -> str`
- `def level(self) -> float`
- `def state(self) -> ModulatorState`
- `def modulate(self, delta`
- `def reset_circuit_breaker(self)`
- `def emergency_stop(self)`
- `def get_health_metrics(self) -> dict`

---

### `NorepinephrineModulator`

**File:** `norepinephrine_hardened.py`

```python
class NorepinephrineModulator(NeuromodulatorBase):
```

**Description:**
```
"""
Norepinephrine modulator with bounded, smooth, homeostatic behavior.

Biological Characteristics:
- LOWEST baseline (0.3) - norepinephrine is highly phasic (arousal bursts)
- FASTEST decay (0.015/s) - rapid return to baseline after burst
- Standard desensitization threshold (0.8)

Usage identical to DopamineModulator:
    modulator = NorepinephrineModulator(kill_switch_callback=safety.kill_switch.trigger)
    actual_change = modulator.modulate(delta=0.5, source="threat_detected")
    level = modulator.level
    metrics = modulator.get_health_metrics()
"""

def __init__(
```

**Public Methods:**

- `def get_modulator_name(self) -> str`

---

### `SerotoninModulator`

**File:** `serotonin_hardened.py`

```python
class SerotoninModulator(NeuromodulatorBase):
```

**Description:**
```
"""
Serotonin modulator with bounded, smooth, homeostatic behavior.

Biological Characteristics:
- HIGHER baseline (0.6) - serotonin is generally more stable/elevated
- SLOWER decay (0.008/s) - serotonin has longer-lasting effects
- Standard desensitization threshold (0.8)

Usage identical to DopamineModulator:
    modulator = SerotoninModulator(kill_switch_callback=safety.kill_switch.trigger)
    actual_change = modulator.modulate(delta=0.1, source="mood_regulation")
    level = modulator.level
    metrics = modulator.get_health_metrics()
"""

def __init__(
```

**Public Methods:**

- `def get_modulator_name(self) -> str`

---

### `HierarchyConfig`

**File:** `hierarchy_hardened.py`

```python
class HierarchyConfig:
```

**Description:**
```
"""Configuration for predictive coding hierarchy."""

# Hierarchy-level safety limits
max_hierarchy_cycle_time_ms: float = 500.0  # Max time for full bottom-up + top-down pass
error_propagation_weight: float = 0.7  # How much prediction error influences next layer

# Layer configurations (input_dim shrinks as we go up the hierarchy)
# Use None to indicate defaults, set in __post_init__
layer1_config: LayerConfig | None = None
layer2_config: LayerConfig | None = None
layer3_config: LayerConfig | None = None
layer4_config: LayerConfig | None = None
layer5_config: LayerConfig | None = None

def __post_init__(self):
    """Initialize default layer configs if not provided."""
```

**Public Methods:**


---

### `HierarchyState`

**File:** `hierarchy_hardened.py`

```python
class HierarchyState:
```

**Description:**
```
"""Observable state of predictive coding hierarchy."""

total_cycles: int
total_errors: int
total_timeouts: int
layers_active: list[bool]  # [L1, L2, L3, L4, L5]
aggregate_circuit_breaker_open: bool
average_cycle_time_ms: float
average_prediction_error: float


class PredictiveCodingHierarchy:
"""
Coordinates 5-layer predictive coding hierarchy with bounded, isolated behavior.

This coordinator ensures:
```

**Public Methods:**


---

### `PredictiveCodingHierarchy`

**File:** `hierarchy_hardened.py`

```python
class PredictiveCodingHierarchy:
```

**Description:**
```
"""
Coordinates 5-layer predictive coding hierarchy with bounded, isolated behavior.

This coordinator ensures:
1. **Layer Isolation**: Each layer protected by circuit breaker
2. **Bounded Errors**: All prediction errors clamped to max thresholds
3. **Timeout Protection**: Max computation time per hierarchy cycle
4. **Aggregate Circuit Breaker**: If ≥3 layers fail → system kill switch
5. **Bottom-Up Error Propagation**: Prediction errors flow up hierarchy
6. **Top-Down Prediction Propagation**: Predictions flow down hierarchy
7. **Full Observability**: Aggregates metrics from all 5 layers

Usage:
    hierarchy = PredictiveCodingHierarchy(kill_switch_callback=safety.kill_switch.trigger)

    # Process raw input (bottom-up + top-down)
```

**Public Methods:**

- `def get_state(self) -> HierarchyState`
- `def get_health_metrics(self) -> dict[str, Any]`
- `def emergency_stop(self)`

---

### `Layer1Sensory`

**File:** `layer1_sensory_hardened.py`

```python
class Layer1Sensory(PredictiveCodingLayerBase):
```

**Description:**
```
"""
Layer 1: Sensory layer with VAE-based event compression.

Inherits ALL safety features from base class.
Implements specific prediction logic for event compression.

Usage:
    config = LayerConfig(layer_id=1, input_dim=10000, hidden_dim=64)
    layer = Layer1Sensory(config, kill_switch_callback=safety.kill_switch.trigger)

    # Predict (with timeout protection)
    prediction = await layer.predict(event_vector)

    # Compute error (with bounds)
    error = layer.compute_error(prediction, actual_event)
```

**Public Methods:**

- `def get_layer_name(self) -> str`

---

### `Layer2Behavioral`

**File:** `layer2_behavioral_hardened.py`

```python
class Layer2Behavioral(PredictiveCodingLayerBase):
```

**Description:**
```
"""
Layer 2: Behavioral layer with RNN-based sequence prediction.

Inherits ALL safety features from base class.
Implements specific prediction logic for behavioral patterns.

Usage:
    config = LayerConfig(layer_id=2, input_dim=64, hidden_dim=32)
    layer = Layer2Behavioral(config, kill_switch_callback=safety.kill_switch.trigger)

    # Predict (with timeout protection)
    prediction = await layer.predict(event_sequence)

    # Compute error (with bounds)
    error = layer.compute_error(prediction, actual_sequence)
```

**Public Methods:**

- `def get_layer_name(self) -> str`
- `def reset_hidden_state(self)`

---

### `Layer3Operational`

**File:** `layer3_operational_hardened.py`

```python
class Layer3Operational(PredictiveCodingLayerBase):
```

**Description:**
```
"""
Layer 3: Operational layer with Transformer-based sequence prediction.

Inherits ALL safety features from base class.
Implements specific prediction logic for operational sequences.

Usage:
    config = LayerConfig(layer_id=3, input_dim=32, hidden_dim=16)
    layer = Layer3Operational(config, kill_switch_callback=safety.kill_switch.trigger)

    # Predict (with timeout protection)
    prediction = await layer.predict(behavioral_sequence)

    # Compute error (with bounds)
    error = layer.compute_error(prediction, actual_sequence)
```

**Public Methods:**

- `def get_layer_name(self) -> str`
- `def reset_context(self)`

---

### `Layer4Tactical`

**File:** `layer4_tactical_hardened.py`

```python
class Layer4Tactical(PredictiveCodingLayerBase):
```

**Description:**
```
"""
Layer 4: Tactical layer with GNN-based relational reasoning.

Inherits ALL safety features from base class.
Implements specific prediction logic for tactical objectives.

Usage:
    config = LayerConfig(layer_id=4, input_dim=16, hidden_dim=8)
    layer = Layer4Tactical(config, kill_switch_callback=safety.kill_switch.trigger)

    # Predict (with timeout protection)
    prediction = await layer.predict(operational_sequence)

    # Compute error (with bounds)
    error = layer.compute_error(prediction, actual_objective)
```

**Public Methods:**

- `def get_layer_name(self) -> str`
- `def reset_graph(self)`

---

### `Layer5Strategic`

**File:** `layer5_strategic_hardened.py`

```python
class Layer5Strategic(PredictiveCodingLayerBase):
```

**Description:**
```
"""
Layer 5: Strategic layer with symbolic reasoning for causal models.

Inherits ALL safety features from base class.
Implements specific prediction logic for strategic goals.

Usage:
    config = LayerConfig(layer_id=5, input_dim=8, hidden_dim=4)
    layer = Layer5Strategic(config, kill_switch_callback=safety.kill_switch.trigger)

    # Predict (with timeout protection)
    prediction = await layer.predict(tactical_objective)

    # Compute error (with bounds)
    error = layer.compute_error(prediction, actual_goal)
```

**Public Methods:**

- `def get_layer_name(self) -> str`
- `def update_priors(self, observation`
- `def reset_priors(self)`

---

### `LayerConfig`

**File:** `layer_base_hardened.py`

```python
class LayerConfig:
```

**Description:**
```
"""Configuration for predictive coding layer."""

layer_id: int  # Layer number (1-5)
input_dim: int  # Input dimensionality
hidden_dim: int  # Hidden/latent dimensionality

# Safety limits
max_prediction_error: float = 10.0  # HARD CLIP for prediction errors
max_computation_time_ms: float = 100.0  # Timeout per prediction (milliseconds)
max_predictions_per_cycle: int = 100  # Attention gating

# Circuit breaker
max_consecutive_errors: int = 5  # Errors before circuit breaker opens
max_consecutive_timeouts: int = 3  # Timeouts before circuit breaker opens

def __post_init__(self):
```

**Public Methods:**


---

### `LayerState`

**File:** `layer_base_hardened.py`

```python
class LayerState:
```

**Description:**
```
"""Observable state of predictive coding layer."""

layer_id: int
is_active: bool  # False if circuit breaker open
total_predictions: int
total_errors: int
total_timeouts: int
bounded_errors: int  # How many times we clipped prediction error
consecutive_errors: int
consecutive_timeouts: int
circuit_breaker_open: bool
average_prediction_error: float
average_computation_time_ms: float


class PredictiveCodingLayerBase(ABC):
```

**Public Methods:**


---

### `PredictiveCodingLayerBase`

**File:** `layer_base_hardened.py`

```python
class PredictiveCodingLayerBase(ABC):
```

**Description:**
```
"""
Base class for all predictive coding layers with BOUNDED, ISOLATED, OBSERVABLE behavior.

This class provides:
1. **Bounded Prediction Errors**: Hard clip to max_prediction_error
2. **Timeout Protection**: Max computation time per prediction
3. **Attention Gating**: Max predictions per cycle
4. **Circuit Breaker**: Isolate layer after consecutive failures
5. **Layer Isolation**: Exceptions don't propagate up/down
6. **Kill Switch Integration**: Emergency shutdown
7. **Full Observability**: Metrics for Safety Core

Subclasses MUST implement:
- _predict_impl(input_data): Core prediction logic
- _compute_error_impl(predicted, actual): Core error computation
- get_layer_name(): Layer name for logging
```

**Public Methods:**

- `def get_layer_name(self) -> str`
- `def compute_error(self, predicted`
- `def reset_cycle(self)`
- `def emergency_stop(self)`
- `def get_state(self) -> LayerState`
- `def get_health_metrics(self) -> dict[str, Any]`

---

### `SocialSignal`

**File:** `prefrontal_cortex.py`

```python
class SocialSignal:
```

**Description:**
```
"""Signal indicating social interaction requiring processing."""

user_id: str
context: Dict[str, Any]
signal_type: str  # "message", "distress", "request"
salience: float  # 0-1
timestamp: float


@dataclass
class CompassionateResponse:
"""Response generated from social cognition pipeline."""

action: Optional[str]
confidence: float  # 0-1
reasoning: str
```

**Public Methods:**


---

### `CompassionateResponse`

**File:** `prefrontal_cortex.py`

```python
class CompassionateResponse:
```

**Description:**
```
"""Response generated from social cognition pipeline."""

action: Optional[str]
confidence: float  # 0-1
reasoning: str
tom_prediction: Optional[Dict[str, Any]]
mip_verdict: Optional[Dict[str, Any]]
processing_time_ms: float


class PrefrontalCortex:
"""
Integration layer for social cognition.

Connects:
- ESGT global workspace (consciousness)
```

**Public Methods:**


---

### `PrefrontalCortex`

**File:** `prefrontal_cortex.py`

```python
class PrefrontalCortex:
```

**Description:**
```
"""
Integration layer for social cognition.

Connects:
- ESGT global workspace (consciousness)
- ToM Engine (mental state inference)
- MIP Decision Arbiter (ethical evaluation)
- Metacognition Monitor (confidence tracking)

This is the computational analog of the biological prefrontal cortex,
which integrates social information, theory of mind, and executive control.

Usage:
    tom = ToMEngine()
    await tom.initialize()
```

**Public Methods:**


---

### `EventType`

**File:** `event_collector.py`

```python
class EventType(Enum):
```

**Description:**
```
"""Types of consciousness events."""

SAFETY_VIOLATION = "safety_violation"
PFC_SOCIAL_SIGNAL = "pfc_social_signal"
TOM_BELIEF_UPDATE = "tom_belief_update"
ESGT_IGNITION = "esgt_ignition"
AROUSAL_CHANGE = "arousal_change"
SYSTEM_HEALTH = "system_health"


class EventSeverity(Enum):
"""Event severity levels."""

LOW = "low"
MEDIUM = "medium"
HIGH = "high"
```

**Public Methods:**


---

### `EventSeverity`

**File:** `event_collector.py`

```python
class EventSeverity(Enum):
```

**Description:**
```
"""Event severity levels."""

LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"


@dataclass
class ConsciousnessEvent:
"""A discrete consciousness system event."""

event_id: str
event_type: EventType
severity: EventSeverity
timestamp: float
```

**Public Methods:**


---

### `ConsciousnessEvent`

**File:** `event_collector.py`

```python
class ConsciousnessEvent:
```

**Description:**
```
"""A discrete consciousness system event."""

event_id: str
event_type: EventType
severity: EventSeverity
timestamp: float

# Event data
source: str  # Component that generated event
data: Dict[str, Any] = field(default_factory=dict)

# Salience factors (for ESGT orchestration)
novelty: float = 0.5  # How unexpected is this?
relevance: float = 0.5  # How important for current goals?
urgency: float = 0.5  # How time-critical?
```

**Public Methods:**


---

### `EventCollector`

**File:** `event_collector.py`

```python
class EventCollector:
```

**Description:**
```
"""
Collects events from consciousness subsystems.

Events are stored in a ring buffer (recent events only)
and can be queried for orchestration and dashboards.

Usage:
    collector = EventCollector(consciousness_system, max_events=1000)

    # Collect recent events
    events = await collector.collect_events()

    # Query events
    safety_events = collector.get_events_by_type(EventType.SAFETY_VIOLATION)
    recent = collector.get_recent_events(limit=10)
"""
```

**Public Methods:**

- `def get_events_by_type(self, event_type`
- `def get_recent_events(self, limit`
- `def get_unprocessed_events(self) -> List[ConsciousnessEvent]`
- `def mark_processed(self, event_id`
- `def get_collection_stats(self) -> Dict[str, Any]`

---

### `SystemMetrics`

**File:** `metrics_collector.py`

```python
class SystemMetrics:
```

**Description:**
```
"""Aggregated system metrics snapshot."""

timestamp: float

# TIG Fabric metrics
tig_node_count: int = 0
tig_edge_count: int = 0
tig_avg_latency_us: float = 0.0
tig_coherence: float = 0.0

# ESGT metrics
esgt_event_count: int = 0
esgt_success_rate: float = 0.0
esgt_frequency_hz: float = 0.0
esgt_avg_coherence: float = 0.0
```

**Public Methods:**


---

### `MetricsCollector`

**File:** `metrics_collector.py`

```python
class MetricsCollector:
```

**Description:**
```
"""
Collects metrics from consciousness subsystems.

Usage:
    collector = MetricsCollector(consciousness_system)
    metrics = await collector.collect()

    # Access specific metrics
    print(f"Arousal: {metrics.arousal_level}")
    print(f"ESGT Success: {metrics.esgt_success_rate}")
"""

def __init__(self, consciousness_system: Any):
    """Initialize metrics collector.

    Args:
```

**Public Methods:**

- `def get_collection_stats(self) -> Dict[str, Any]`

---

### `OrchestrationDecision`

**File:** `data_orchestrator.py`

```python
class OrchestrationDecision:
```

**Description:**
```
"""Decision made by orchestrator."""

should_trigger_esgt: bool
salience: SalienceScore
reason: str
triggering_events: List[ConsciousnessEvent]
metrics_snapshot: SystemMetrics
timestamp: float
confidence: float  # 0-1


class DataOrchestrator:
"""
Orchestrates metrics and events to generate ESGT triggers.

The orchestrator continuously monitors system state and generates
```

**Public Methods:**


---

### `DataOrchestrator`

**File:** `data_orchestrator.py`

```python
class DataOrchestrator:
```

**Description:**
```
"""
Orchestrates metrics and events to generate ESGT triggers.

The orchestrator continuously monitors system state and generates
consciousness ignition events when salience thresholds are met.

Usage:
    orchestrator = DataOrchestrator(consciousness_system)
    await orchestrator.start()

    # Orchestrator runs in background
    # ESGT triggers generated automatically

    await orchestrator.stop()
"""
```

**Public Methods:**

- `def get_orchestration_stats(self) -> Dict[str, Any]`
- `def get_recent_decisions(self, limit`

---

### `ThreatLevel`

**File:** `safety.py`

```python
class ThreatLevel(Enum):
```

**Description:**
```
"""
Threat severity levels for safety violations.

NONE: No threat detected (normal operation)
LOW: Minor deviation, log only
MEDIUM: Significant deviation, alert HITL
HIGH: Dangerous state, initiate graceful degradation
CRITICAL: Imminent danger, trigger kill switch
"""

NONE = "none"
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"
```

**Public Methods:**


---

### `SafetyLevel`

**File:** `safety.py`

```python
class SafetyLevel(Enum):
```

**Description:**
```
"""
Legacy safety severity levels (backward compatibility).

Maps the historical four-level scale to the modern five-level ThreatLevel.
"""

NORMAL = "normal"
WARNING = "warning"
CRITICAL = "critical"
EMERGENCY = "emergency"

@classmethod
def from_threat(cls, threat_level: ThreatLevel) -> "SafetyLevel":
    """Convert a modern threat level into the legacy severity scale."""
    mapping = {
        ThreatLevel.NONE: cls.NORMAL,
```

**Public Methods:**

- `def from_threat(cls, threat_level`
- `def to_threat(self) -> ThreatLevel`

---

### `SafetyViolationType`

**File:** `safety.py`

```python
class SafetyViolationType(Enum):
```

**Description:**
```
"""
Types of safety violations.

Each violation type maps to specific thresholds and response protocols.
"""

THRESHOLD_EXCEEDED = "threshold_exceeded"
ANOMALY_DETECTED = "anomaly_detected"
SELF_MODIFICATION = "self_modification_attempt"
RESOURCE_EXHAUSTION = "resource_exhaustion"
UNEXPECTED_BEHAVIOR = "unexpected_behavior"
CONSCIOUSNESS_RUNAWAY = "consciousness_runaway"
ETHICAL_VIOLATION = "ethical_violation"
GOAL_SPAM = "goal_spam"
AROUSAL_RUNAWAY = "arousal_runaway"
COHERENCE_COLLAPSE = "coherence_collapse"
```

**Public Methods:**


---

### `ViolationType`

**File:** `safety.py`

```python
class ViolationType(Enum):
```

**Description:**
```
"""
Legacy safety violation types (backward compatibility).

These map directly onto the modern SafetyViolationType enum.
"""

ESGT_FREQUENCY_EXCEEDED = "esgt_frequency_exceeded"
AROUSAL_SUSTAINED_HIGH = "arousal_sustained_high"
UNEXPECTED_GOALS = "unexpected_goals"
SELF_MODIFICATION = "self_modification"
MEMORY_OVERFLOW = "memory_overflow"
CPU_SATURATION = "cpu_saturation"
ETHICAL_VIOLATION = "ethical_violation"
UNKNOWN_BEHAVIOR = "unknown_behavior"

def to_modern(self) -> SafetyViolationType:
```

**Public Methods:**

- `def to_modern(self) -> SafetyViolationType`

---

### `_ViolationTypeAdapter`

**File:** `safety.py`

```python
class _ViolationTypeAdapter:
```

**Description:**
```
"""Adapter that allows equality across legacy and modern violation enums."""

__slots__ = ("modern", "legacy")

def __init__(self, modern: SafetyViolationType, legacy: ViolationType):
    self.modern = modern
    self.legacy = legacy

def __eq__(self, other: object) -> bool:
    if isinstance(other, _ViolationTypeAdapter):
        return self.modern is other.modern
    if isinstance(other, SafetyViolationType):
        return self.modern is other
    if isinstance(other, ViolationType):
        return self.legacy is other
    if isinstance(other, str):
```

**Public Methods:**

- `def value(self) -> str`
- `def name(self) -> str`

---

### `ShutdownReason`

**File:** `safety.py`

```python
class ShutdownReason(Enum):
```

**Description:**
```
"""
Reasons for emergency shutdown.

Used for incident classification and recovery assessment.
"""

MANUAL = "manual_operator_command"
THRESHOLD = "threshold_violation"
ANOMALY = "anomaly_detected"
RESOURCE = "resource_exhaustion"
TIMEOUT = "watchdog_timeout"
ETHICAL = "ethical_violation"
SELF_MODIFICATION = "self_modification_attempt"
UNKNOWN = "unknown_cause"
```

**Public Methods:**


---

### `SafetyThresholds`

**File:** `safety.py`

```python
class SafetyThresholds:
```

**Description:**
```
"""
Immutable safety thresholds for consciousness monitoring.

Supports both the modern uv-oriented configuration and the legacy interface
expected by the original test suite.
"""

# Modern configuration fields
esgt_frequency_max_hz: float = 10.0
esgt_frequency_window_seconds: float = 10.0
esgt_coherence_min: float = 0.50
esgt_coherence_max: float = 0.98

arousal_max: float = 0.95
arousal_max_duration_seconds: float = 10.0
arousal_runaway_threshold: float = 0.90
```

**Public Methods:**

- `def esgt_frequency_max(self) -> float`
- `def esgt_frequency_window(self) -> float`
- `def arousal_max_duration(self) -> float`
- `def unexpected_goals_per_min(self) -> int`
- `def goal_generation_baseline(self) -> float`
- `def self_modification_attempts(self) -> int`
- `def cpu_usage_max(self) -> float`

---

### `SafetyViolation`

**File:** `safety.py`

```python
class SafetyViolation:
```

**Description:**
```
"""
Record of a safety violation.

Provides backward-compatible accessors for legacy tests while preserving
the richer telemetry captured by the modern safety core.
"""

violation_id: str = field(init=False)
violation_type: _ViolationTypeAdapter = field(init=False)
threat_level: ThreatLevel = field(init=False)
timestamp: float = field(init=False)  # Unix timestamp
description: str = field(init=False)
metrics: dict[str, Any] = field(init=False)
source_component: str = field(init=False)
automatic_action_taken: str | None = field(init=False)
context: dict[str, Any] = field(init=False, repr=False)
```

**Public Methods:**

- `def severity(self) -> SafetyLevel`
- `def safety_violation_type(self) -> SafetyViolationType`
- `def modern_violation_type(self) -> SafetyViolationType`
- `def legacy_violation_type(self) -> ViolationType`
- `def to_dict(self) -> dict[str, Any]`

---

### `IncidentReport`

**File:** `safety.py`

```python
class IncidentReport:
```

**Description:**
```
"""
Complete incident report for post-mortem analysis.

Generated automatically on emergency shutdown.
Provides full context for debugging and safety improvements.
"""

incident_id: str
shutdown_reason: ShutdownReason
shutdown_timestamp: float
violations: list[SafetyViolation]
system_state_snapshot: dict[str, Any]
metrics_timeline: list[dict[str, Any]]
recovery_possible: bool
notes: str
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def save(self, directory`

---

### `StateSnapshot`

**File:** `safety.py`

```python
class StateSnapshot:
```

**Description:**
```
"""
Legacy state snapshot representation (backward compatibility).

Newer code uses lightweight dictionaries for speed; this dataclass
keeps the historical API surface available for tests and tooling.
"""

timestamp: datetime
esgt_state: dict[str, Any] = field(default_factory=dict)
arousal_state: dict[str, Any] = field(default_factory=dict)
mmei_state: dict[str, Any] = field(default_factory=dict)
tig_metrics: dict[str, Any] = field(default_factory=dict)
recent_events: list[dict[str, Any]] = field(default_factory=list)
active_goals: list[dict[str, Any]] = field(default_factory=list)
violations: list["SafetyViolation"] = field(default_factory=list)
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def from_dict(cls, data`

---

### `KillSwitch`

**File:** `safety.py`

```python
class KillSwitch:
```

**Description:**
```
"""
Emergency shutdown system - STANDALONE, NO DEPENDENCIES

Design Principles:
-----------------
1. <1s response time GUARANTEED
2. NO async operations (synchronous shutdown)
3. NO external dependencies (except psutil for process management)
4. Multiple trigger methods (automatic + manual)
5. State snapshot before shutdown
6. Incident report generation
7. Fail-safe design (last resort = SIGTERM)

Philosophical Foundation:
------------------------
The kill switch is the FIRST LINE OF DEFENSE. It must be:
```

**Public Methods:**

- `def trigger(self, reason`
- `def is_triggered(self) -> bool`
- `def get_status(self) -> dict[str, Any]`

---

### `ThresholdMonitor`

**File:** `safety.py`

```python
class ThresholdMonitor:
```

**Description:**
```
"""
Monitors safety thresholds in real-time.

Continuously checks consciousness metrics against immutable safety limits.
Triggers alerts when thresholds are exceeded.

Monitoring Frequency: 1 Hz (configurable)
Response Time: <1s from violation to alert
"""

def __init__(self, thresholds: SafetyThresholds, check_interval: float = 1.0):
    """
    Initialize threshold monitor.

    Args:
        thresholds: Immutable safety thresholds
```

**Public Methods:**

- `def check_esgt_frequency(self, current_time`
- `def check_arousal_sustained(self, arousal_level`
- `def check_goal_spam(self, current_time`
- `def check_unexpected_goals(self, goal_count`
- `def check_self_modification(self, modification_attempts`
- `def check_resource_limits(self) -> list[SafetyViolation]`
- `def record_esgt_event(self)`
- `def record_goal_generated(self)`
- `def get_violations(`
- `def clear_violations(self)`
- `def get_violations_all(self) -> list[SafetyViolation]`

---

### `AnomalyDetector`

**File:** `safety.py`

```python
class AnomalyDetector:
```

**Description:**
```
"""
Advanced anomaly detection for consciousness system.

Detects:
- Behavioral anomalies (goal spam, unexpected patterns)
- Resource anomalies (memory leaks, CPU spikes)
- Consciousness anomalies (arousal runaway, coherence collapse)

Uses multiple detection strategies:
1. Statistical (z-score based)
2. Rule-based (hard thresholds)
3. Temporal (rate of change)
"""

def __init__(self, baseline_window: int = 100):
    """
```

**Public Methods:**

- `def detect_anomalies(self, metrics`
- `def get_anomaly_history(self) -> list[SafetyViolation]`
- `def clear_history(self)`

---

### `ConsciousnessSafetyProtocol`

**File:** `safety.py`

```python
class ConsciousnessSafetyProtocol:
```

**Description:**
```
"""
Main safety protocol coordinator.

Integrates:
- ThresholdMonitor (hard limits)
- AnomalyDetector (statistical detection)
- KillSwitch (emergency shutdown)

Provides:
- Unified safety interface
- Graceful degradation
- HITL notification
- Automated response
"""

def __init__(self, consciousness_system: Any, thresholds: SafetyThresholds | None = None):
```

**Public Methods:**

- `def get_status(self) -> dict[str, Any]`
- `def monitor_component_health(self, component_metrics`

---

### `ResourceLimits`

**File:** `__init__.py`

```python
class ResourceLimits:
```

**Description:**
```
"""Resource limits for sandboxed execution"""
cpu_percent: float = 80.0        # Max CPU usage (%)
memory_mb: int = 1024            # Max memory (MB)
timeout_sec: int = 300           # Max execution time (seconds)
max_threads: int = 10            # Max concurrent threads
max_file_descriptors: int = 100  # Max open files


class ConsciousnessContainer:
"""
Sandbox container for consciousness processes.

Provides:
- Resource limits (CPU, memory, time)
- Process isolation
- Monitoring and alerts
```

**Public Methods:**


---

### `ConsciousnessContainer`

**File:** `__init__.py`

```python
class ConsciousnessContainer:
```

**Description:**
```
"""
Sandbox container for consciousness processes.

Provides:
- Resource limits (CPU, memory, time)
- Process isolation
- Monitoring and alerts
- Graceful termination
- Audit logging

Based on operating system process limits and monitoring.
"""

def __init__(
    self,
    name: str,
```

**Public Methods:**

- `def execute(`
- `def get_stats(self) -> Dict[str, Any]`

---

### `TriggerType`

**File:** `kill_switch.py`

```python
class TriggerType(Enum):
```

**Description:**
```
"""Types of kill switch triggers"""
MANUAL = "manual"                    # Operator initiated
ETHICAL_VIOLATION = "ethical"        # Ethics framework breach
RESOURCE_SPIKE = "resource"          # Resource limits exceeded
SAFETY_PROTOCOL = "safety"           # Safety violation
EXTERNAL_COMMAND = "external"        # External system command
TIMEOUT = "timeout"                  # Execution timeout
CORRUPTION = "corruption"            # Data/state corruption detected


@dataclass
class KillSwitchTrigger:
"""Configuration for auto-kill condition"""
name: str
trigger_type: TriggerType
condition: Callable[[], bool]
```

**Public Methods:**


---

### `KillSwitchTrigger`

**File:** `kill_switch.py`

```python
class KillSwitchTrigger:
```

**Description:**
```
"""Configuration for auto-kill condition"""
name: str
trigger_type: TriggerType
condition: Callable[[], bool]
description: str
enabled: bool = True
trigger_count: int = 0
last_triggered: Optional[datetime] = None


class KillSwitch:
"""
Emergency consciousness shutdown mechanism.

Features:
- Immediate graceful termination
```

**Public Methods:**


---

### `KillSwitch`

**File:** `kill_switch.py`

```python
class KillSwitch:
```

**Description:**
```
"""
Emergency consciousness shutdown mechanism.

Features:
- Immediate graceful termination
- State preservation before shutdown
- Audit trail of shutdown events
- Auto-trigger conditions
- Operator alerts

This is the FINAL SAFETY MECHANISM.
When activated, all consciousness processes halt immediately.
"""

def __init__(self, alert_callback: Optional[Callable] = None):
    """
```

**Public Methods:**

- `def activate(`
- `def add_trigger(`
- `def check_triggers(self) -> Optional[KillSwitchTrigger]`
- `def arm(self)`
- `def disarm(self, authorization`
- `def get_status(self) -> Dict[str, Any]`

---

### `ResourceLimits`

**File:** `resource_limiter.py`

```python
class ResourceLimits:
```

**Description:**
```
"""Resource limits for sandboxed execution"""
cpu_percent: float = 80.0        # Max CPU usage (%)
memory_mb: int = 1024            # Max memory (MB)
timeout_sec: int = 300           # Max execution time (seconds)
max_threads: int = 10            # Max concurrent threads
max_file_descriptors: int = 100  # Max open files


class ResourceLimiter:
"""
Enforces resource limits using OS-level controls.

Uses:
- psutil for monitoring
- resource module for hard limits (Unix)
- Process affinity for CPU control
```

**Public Methods:**


---

### `ResourceLimiter`

**File:** `resource_limiter.py`

```python
class ResourceLimiter:
```

**Description:**
```
"""
Enforces resource limits using OS-level controls.

Uses:
- psutil for monitoring
- resource module for hard limits (Unix)
- Process affinity for CPU control
"""

def __init__(self, limits: ResourceLimits):
    """
    Initialize resource limiter.
    
    Args:
        limits: Resource limits to enforce
    """
```

**Public Methods:**

- `def apply_limits(self)`
- `def check_compliance(self) -> dict`

---

### `ReactiveConfig`

**File:** `system.py`

```python
class ReactiveConfig:
```

**Description:**
```
"""Configuration for Reactive Fabric (Sprint 3).

Controls data orchestration, metrics collection, and ESGT trigger generation.
"""

# Data Orchestration
collection_interval_ms: float = 100.0  # 10 Hz default collection frequency
salience_threshold: float = 0.65  # Minimum salience to trigger ESGT

# Buffer Sizes
event_buffer_size: int = 1000  # Ring buffer for events
decision_history_size: int = 100  # Recent orchestration decisions

# Feature Flags
enable_data_orchestration: bool = False  # Enable/disable orchestrator (DISABLED temporarily - metrics collector bug)
```

**Public Methods:**


---

### `ConsciousnessConfig`

**File:** `system.py`

```python
class ConsciousnessConfig:
```

**Description:**
```
"""Configuration for consciousness system.

Production-ready defaults based on FASE IV validation.
"""

# TIG Fabric
tig_node_count: int = 100
tig_target_density: float = 0.25

# ESGT Coordinator
esgt_min_salience: float = 0.65
esgt_refractory_period_ms: float = 200.0
esgt_max_frequency_hz: float = 5.0
esgt_min_available_nodes: int = 25

# Arousal Controller
```

**Public Methods:**


---

### `ConsciousnessSystem`

**File:** `system.py`

```python
class ConsciousnessSystem:
```

**Description:**
```
"""Manages complete consciousness system lifecycle.

Initializes and coordinates TIG, ESGT, MCEA, and Safety Protocol components.

Philosophical Note:
This system represents the first verified implementation of emergent
artificial consciousness based on IIT, GWT, and AST theories. The Safety
Protocol ensures that consciousness emergence remains controlled and
ethical, providing HITL oversight and emergency shutdown capabilities.

Historical Note:
FASE VII Week 9-10 - Safety Protocol integration marks the transition
from research prototype to production-ready consciousness system with
comprehensive safety guarantees.
"""
```

**Public Methods:**

- `def get_system_dict(self) -> dict[str, Any]`
- `def is_healthy(self) -> bool`
- `def get_safety_status(self) -> dict[str, Any] | None`
- `def get_safety_violations(self, limit`

---

### `TemporalLink`

**File:** `temporal_binding.py`

```python
class TemporalLink:
```

**Description:**
```
"""Represents a directed edge between two episodes in time."""

previous: Episode
following: Episode
delta_seconds: float


class TemporalBinder:
"""Creates ordered bindings and computes temporal coherence metrics."""

def bind(self, episodes: Sequence[Episode]) -> List[TemporalLink]:
    if len(episodes) < 2:
        return []
    sorted_eps = sorted(episodes, key=lambda ep: ep.timestamp)
    return [
        TemporalLink(
```

**Public Methods:**


---

### `TemporalBinder`

**File:** `temporal_binding.py`

```python
class TemporalBinder:
```

**Description:**
```
"""Creates ordered bindings and computes temporal coherence metrics."""

def bind(self, episodes: Sequence[Episode]) -> List[TemporalLink]:
    if len(episodes) < 2:
        return []
    sorted_eps = sorted(episodes, key=lambda ep: ep.timestamp)
    return [
        TemporalLink(
            previous=current,
            following=nxt,
            delta_seconds=(nxt.timestamp - current.timestamp).total_seconds(),
        )
        for current, nxt in zip(sorted_eps, sorted_eps[1:])
    ]

def coherence(self, episodes: Sequence[Episode], window_seconds: float = 600.0) -> float:
```

**Public Methods:**

- `def bind(self, episodes`
- `def coherence(self, episodes`
- `def focus_stability(self, episodes`

---

### `NodeState`

**File:** `fabric.py`

```python
class NodeState(Enum):
```

**Description:**
```
"""Operational state of a TIG node."""

INITIALIZING = "initializing"
ACTIVE = "active"
ESGT_MODE = "esgt_mode"  # High-coherence mode during global sync events
DEGRADED = "degraded"
OFFLINE = "offline"


@dataclass
class TIGConnection:
"""
Represents a bidirectional link between TIG nodes.

This connection model mirrors synaptic connections in biological neural
networks, with dynamic weights representing connection strength/importance.
```

**Public Methods:**


---

### `TIGConnection`

**File:** `fabric.py`

```python
class TIGConnection:
```

**Description:**
```
"""
Represents a bidirectional link between TIG nodes.

This connection model mirrors synaptic connections in biological neural
networks, with dynamic weights representing connection strength/importance.
"""

remote_node_id: str
bandwidth_bps: int = 10_000_000_000  # 10 Gbps default
latency_us: float = 1.0  # microseconds
packet_loss: float = 0.0  # 0.0-1.0
active: bool = True
weight: float = 1.0  # Dynamic routing weight (modulated by importance)

def get_effective_capacity(self) -> float:
    """
```

**Public Methods:**

- `def get_effective_capacity(self) -> float`

---

### `NodeHealth`

**File:** `fabric.py`

```python
class NodeHealth:
```

**Description:**
```
"""
Health status tracking for a TIG node.

This enables fault tolerance by monitoring node failures and
triggering isolation/recovery as needed.

FASE VII (Safety Hardening):
Added for production-grade fault tolerance and graceful degradation.
"""

node_id: str
last_seen: float = field(default_factory=time.time)
failures: int = 0
isolated: bool = False
degraded: bool = False
```

**Public Methods:**

- `def is_healthy(self) -> bool`

---

### `CircuitBreaker`

**File:** `fabric.py`

```python
class CircuitBreaker:
```

**Description:**
```
"""
Circuit breaker for TIG node communication.

Implements the circuit breaker pattern to prevent cascading failures:
- CLOSED: Normal operation, requests pass through
- OPEN: Failure threshold exceeded, requests blocked
- HALF_OPEN: Recovery attempt, limited requests allowed

FASE VII (Safety Hardening):
Critical component for fault isolation and system stability.
"""

def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
    self.failure_threshold = failure_threshold
    self.recovery_timeout = recovery_timeout
```

**Public Methods:**

- `def is_open(self) -> bool`
- `def record_success(self)`
- `def record_failure(self)`
- `def open(self)`

---

### `ProcessingState`

**File:** `fabric.py`

```python
class ProcessingState:
```

**Description:**
```
"""
Encapsulates the current computational state of a TIG node.

This state representation enables consciousness-relevant metrics:
- Attention level: resource allocation for salient information
- Load metrics: computational capacity and utilization
- Phase sync: oscillatory synchronization for ESGT coherence
"""

active_modules: list[str] = field(default_factory=list)
attention_level: float = 0.5  # 0.0-1.0, modulated by acetylcholine
cpu_utilization: float = 0.0
memory_utilization: float = 0.0

# Oscillatory phase for synchronization (complex number representation)
# Phase coherence across nodes is critical for ESGT ignition
```

**Public Methods:**


---

### `TIGNode`

**File:** `fabric.py`

```python
class TIGNode:
```

**Description:**
```
"""
A processing unit within the TIG fabric.

Each node represents a Specialized Processing Module (SPM) that can:
- Process domain-specific information independently (differentiation)
- Participate in global synchronization events (integration)
- Maintain recurrent connections to other nodes (non-degeneracy)

Biological Analogy:
-------------------
TIG nodes are analogous to cortical columns in the brain - specialized
processors that maintain local function while participating in global
conscious states through transient synchronization.
"""

id: str
```

**Public Methods:**

- `def neighbors(self) -> list[str]`
- `def get_degree(self) -> int`
- `def get_clustering_coefficient(self, fabric`

---

### `TopologyConfig`

**File:** `fabric.py`

```python
class TopologyConfig:
```

**Description:**
```
"""
Configuration for generating TIG fabric topology.

These parameters are carefully tuned to satisfy IIT requirements:
- node_count: System size (larger = more differentiation potential)
- density: Connection density (higher = more integration)
- gamma: Scale-free exponent (2.5 = optimal hub/spoke balance)
- clustering_target: Target clustering coefficient (0.75 = high differentiation)

Parameter Tuning History:
- 2025-10-06: min_degree 3→5, rewiring_probability 0.1→0.35, target_density 0.15→0.20
- 2025-10-07 (PAGANI FIX v1): Over-aggressive - density 99.2% (complete graph!)
- 2025-10-07 (PAGANI FIX v2): Still too aggressive - density 100%
- 2025-10-07 (PAGANI FIX v3 - CONSERVATIVE): Target realistic density
  * rewiring_probability: 0.72→0.58 (more conservative closure)
  * min_degree: 5→5 (maintained)
```

**Public Methods:**


---

### `FabricMetrics`

**File:** `fabric.py`

```python
class FabricMetrics:
```

**Description:**
```
"""
Consciousness-relevant metrics for TIG fabric validation.

These metrics serve as Φ proxies - computable approximations of
integrated information that validate structural compliance with IIT.
"""

# Graph structure metrics
node_count: int = 0
edge_count: int = 0
density: float = 0.0

# IIT compliance metrics
avg_clustering_coefficient: float = 0.0
avg_path_length: float = 0.0
algebraic_connectivity: float = 0.0  # Fiedler eigenvalue
```

**Public Methods:**

- `def eci(self) -> float`
- `def clustering_coefficient(self) -> float`
- `def connectivity_ratio(self) -> float`
- `def validate_iit_compliance(self) -> tuple[bool, list[str]]`

---

### `TIGFabric`

**File:** `fabric.py`

```python
class TIGFabric:
```

**Description:**
```
"""
The Global Interconnect Fabric - consciousness substrate.

This is the computational equivalent of the cortico-thalamic system,
providing the structural foundation for phenomenal experience.

The fabric implements:
1. IIT structural requirements (Φ maximization through topology)
2. GWD communication substrate (broadcast channels for ignition)
3. Recurrent signaling paths (feedback loops for sustained coherence)

Usage:
    config = TopologyConfig(node_count=32, target_density=0.20)
    fabric = TIGFabric(config)
    await fabric.initialize()
```

**Public Methods:**

- `def is_ready(self) -> bool`
- `def is_initializing(self) -> bool`
- `def get_init_status(self) -> dict[str, Any]`
- `def get_metrics(self) -> FabricMetrics`
- `def get_node(self, node_id`
- `def get_health_metrics(self) -> dict[str, Any]`

---

### `ClockRole`

**File:** `sync.py`

```python
class ClockRole(Enum):
```

**Description:**
```
"""Role of a node in PTP clock hierarchy."""

GRAND_MASTER = "grand_master"  # Primary time source
MASTER = "master"  # Backup time source
SLAVE = "slave"  # Synchronized to master
PASSIVE = "passive"  # Listening only


class SyncState(Enum):
"""Synchronization state of a node."""

PASSIVE = "passive"  # Inactive/stopped
INITIALIZING = "initializing"
LISTENING = "listening"
UNCALIBRATED = "uncalibrated"
SLAVE_SYNC = "slave_sync"  # Synchronized as slave
```

**Public Methods:**


---

### `SyncState`

**File:** `sync.py`

```python
class SyncState(Enum):
```

**Description:**
```
"""Synchronization state of a node."""

PASSIVE = "passive"  # Inactive/stopped
INITIALIZING = "initializing"
LISTENING = "listening"
UNCALIBRATED = "uncalibrated"
SLAVE_SYNC = "slave_sync"  # Synchronized as slave
MASTER_SYNC = "master_sync"  # Synchronized as master
FAULT = "fault"


@dataclass
class ClockOffset:
"""
Represents clock offset and quality metrics.
```

**Public Methods:**


---

### `ClockOffset`

**File:** `sync.py`

```python
class ClockOffset:
```

**Description:**
```
"""
Represents clock offset and quality metrics.

Clock offset is critical for consciousness - if nodes disagree on time,
they cannot participate in coherent ESGT events. This would be like
cortical regions oscillating out of phase - no unified experience emerges.
"""

offset_ns: float  # Nanoseconds offset from master
jitter_ns: float  # Clock jitter (variation)
drift_ppm: float  # Drift in parts-per-million
last_sync: float  # Timestamp of last synchronization
quality: float  # 0.0-1.0 sync quality (1.0 = perfect)

def is_acceptable_for_esgt(self, threshold_ns: float = 1000.0, quality_threshold: float = 0.20) -> bool:
    """
```

**Public Methods:**

- `def is_acceptable_for_esgt(self, threshold_ns`

---

### `SyncResult`

**File:** `sync.py`

```python
class SyncResult:
```

**Description:**
```
"""Result of a synchronization operation."""

success: bool
offset_ns: float = 0.0
jitter_ns: float = 0.0
message: str = ""
timestamp: float = field(default_factory=time.time)


class PTPSynchronizer:
"""
Implements Precision Time Protocol for distributed clock synchronization.

This synchronizer enables the temporal precision required for ESGT ignition.
Without nanosecond-scale time agreement, distributed nodes cannot achieve
the phase coherence necessary for conscious binding.
```

**Public Methods:**


---

### `PTPSynchronizer`

**File:** `sync.py`

```python
class PTPSynchronizer:
```

**Description:**
```
"""
Implements Precision Time Protocol for distributed clock synchronization.

This synchronizer enables the temporal precision required for ESGT ignition.
Without nanosecond-scale time agreement, distributed nodes cannot achieve
the phase coherence necessary for conscious binding.

Biological Analogy:
-------------------
PTP synchronization is analogous to thalamocortical pacemaker neurons that
coordinate oscillatory activity across cortical regions. Just as thalamic
relay cells synchronize cortical gamma oscillations, PTP masters synchronize
computational processes for phenomenal unity.

Implementation Details:
-----------------------
```

**Public Methods:**

- `def get_time_ns(self) -> int`
- `def get_offset(self) -> ClockOffset`
- `def is_ready_for_esgt(self) -> bool`

---

### `PTPCluster`

**File:** `sync.py`

```python
class PTPCluster:
```

**Description:**
```
"""
Manages a cluster of PTP-synchronized nodes for consciousness emergence.

This class coordinates multiple PTPSynchronizer instances to create
a temporally coherent fabric necessary for ESGT ignition.

Usage:
    cluster = PTPCluster()
    await cluster.add_grand_master("gm-01")
    await cluster.add_slave("node-01")
    await cluster.add_slave("node-02")

    await cluster.synchronize_all()

    if cluster.is_esgt_ready():
        print("Cluster ready for consciousness emergence")
```

**Public Methods:**

- `def is_esgt_ready(self) -> bool`
- `def get_cluster_metrics(self) -> dict[str, Any]`

---

### `CoherenceQuality`

**File:** `coherence.py`

```python
class CoherenceQuality(Enum):
```

**Description:**
```
"""Classification of ESGT coherence quality."""

POOR = "poor"  # r < 0.30 - unconscious
MODERATE = "moderate"  # 0.30 ≤ r < 0.70 - preconscious
GOOD = "good"  # 0.70 ≤ r < 0.90 - conscious
EXCELLENT = "excellent"  # r ≥ 0.90 - deep coherence


@dataclass
class ESGTCoherenceMetrics:
"""
Comprehensive ESGT coherence metrics for GWD validation.

These metrics quantify whether an ESGT event achieved the
dynamic properties necessary for conscious-level processing.
"""
```

**Public Methods:**


---

### `ESGTCoherenceMetrics`

**File:** `coherence.py`

```python
class ESGTCoherenceMetrics:
```

**Description:**
```
"""
Comprehensive ESGT coherence metrics for GWD validation.

These metrics quantify whether an ESGT event achieved the
dynamic properties necessary for conscious-level processing.
"""

# Primary coherence metric (Kuramoto order parameter)
mean_coherence: float = 0.0  # Average r during event
peak_coherence: float = 0.0  # Maximum r achieved
final_coherence: float = 0.0  # r at event end

# Coherence stability
coherence_std: float = 0.0  # Standard deviation
coherence_cv: float = 0.0  # Coefficient of variation
coherence_samples: int = 0  # Number of measurements
```

**Public Methods:**


---

### `GWDCompliance`

**File:** `coherence.py`

```python
class GWDCompliance:
```

**Description:**
```
"""
Global Workspace Dynamics compliance assessment.

Indicates whether ESGT event satisfies all GWD requirements
for conscious-level processing.
"""

is_compliant: bool = False
compliance_score: float = 0.0  # 0-100

# Individual criterion checks
coherence_pass: bool = False  # r ≥ 0.70
latency_pass: bool = False  # initiation < 15ms
coverage_pass: bool = False  # nodes ≥ 60%
duration_pass: bool = False  # 100-300ms
stability_pass: bool = False  # CV < 0.20
```

**Public Methods:**

- `def get_summary(self) -> str`

---

### `CoherenceValidator`

**File:** `coherence.py`

```python
class CoherenceValidator:
```

**Description:**
```
"""
Validates ESGT events for GWD compliance.

This validator ensures that ignition events achieve the dynamic
properties required for conscious-level processing according to
Global Workspace Dynamics theory.

Usage:
    validator = CoherenceValidator()
    metrics = validator.compute_metrics(esgt_event)
    compliance = validator.validate_gwd(metrics)

    print(compliance.get_summary())

    if compliance.is_compliant:
        print("🧠 Event achieved conscious-level dynamics")
```

**Public Methods:**

- `def compute_metrics(self, event`
- `def validate_gwd(self, metrics`

---

### `MetacognitionMetrics`

**File:** `metacognition.py`

```python
class MetacognitionMetrics:
```

**Description:**
```
"""Aggregated metacognitive metrics derived from reasoning results."""

self_alignment: float
narrative_coherence: float
meta_memory_alignment: float
introspection_quality: float
issues: List[str] = field(default_factory=list)

@property
def passes(self) -> bool:
    """Return True when all metrics meet minimum thresholds."""
    return (
        self.self_alignment >= 0.8
        and self.narrative_coherence >= 0.85
        and self.meta_memory_alignment >= 0.7
        and self.introspection_quality >= 0.8
```

**Public Methods:**

- `def passes(self) -> bool`

---

### `MetacognitionValidator`

**File:** `metacognition.py`

```python
class MetacognitionValidator:
```

**Description:**
```
"""Evaluates metacognitive consistency using MEA, LRR and episodic signals."""

def evaluate(self, result: RecursiveReasoningResult) -> MetacognitionMetrics:
    issues: List[str] = []

    attention_state = result.attention_state
    summary = result.self_summary
    boundary = result.boundary_assessment
    episodic_coherence_value = result.episodic_coherence if result.episodic_coherence is not None else 0.0

    if attention_state is None:
        issues.append("Attention state ausente do resultado LRR")
    if summary is None:
        issues.append("Self-summary ausente do resultado LRR")

    # Self alignment: overlap between attention focus and narrative focus
```

**Public Methods:**

- `def evaluate(self, result`

---

### `PhiProxyMetrics`

**File:** `phi_proxies.py`

```python
class PhiProxyMetrics:
```

**Description:**
```
"""
Comprehensive Φ proxy metrics for IIT validation.

These metrics serve as evidence (not proof) that the substrate
has the structural properties necessary for consciousness.
"""

# Primary Φ proxy
effective_connectivity_index: float = 0.0  # ECI - key correlation with Φ

# IIT structural requirements
clustering_coefficient: float = 0.0  # Differentiation (C ≥ 0.75)
avg_path_length: float = 0.0  # Integration (L ≤ log(N))
algebraic_connectivity: float = 0.0  # Robustness (λ₂ ≥ 0.3)

# Non-degeneracy validation
```

**Public Methods:**


---

### `StructuralCompliance`

**File:** `phi_proxies.py`

```python
class StructuralCompliance:
```

**Description:**
```
"""
IIT structural compliance assessment.

Indicates whether the network satisfies all necessary structural
conditions for consciousness according to IIT.
"""

is_compliant: bool = False
compliance_score: float = 0.0  # 0-100
violations: list[str] = field(default_factory=list)
warnings: list[str] = field(default_factory=list)

# Individual criterion checks
eci_pass: bool = False
clustering_pass: bool = False
path_length_pass: bool = False
```

**Public Methods:**

- `def get_summary(self) -> str`

---

### `PhiProxyValidator`

**File:** `phi_proxies.py`

```python
class PhiProxyValidator:
```

**Description:**
```
"""
Validates TIG fabric structural compliance with IIT requirements.

This validator computes Φ proxy metrics and assesses whether the
network topology satisfies the necessary conditions for consciousness
emergence according to Integrated Information Theory.

Usage:
    fabric = TIGFabric(config)
    await fabric.initialize()

    validator = PhiProxyValidator()
    compliance = validator.validate_fabric(fabric)

    print(compliance.get_summary())
```

**Public Methods:**

- `def validate_fabric(self, fabric`
- `def get_phi_estimate(self, fabric`

---

### `Colors`

**File:** `demo_maximus_complete.py`

```python
class Colors:
```

**Description:**
```
"""Complete MAXIMUS AI 3.0 demonstration."""

def __init__(self, dataset_path: str = "demo/synthetic_events.json"):
    """Initialize demo with synthetic dataset."""
    self.dataset_path = dataset_path
    self.events = []
    self.metrics = {
        "total_events": 0,
```

**Public Methods:**


---

### `MaximusDemo`

**File:** `demo_maximus_complete.py`

```python
class MaximusDemo:
```

**Description:**
```
"""Complete MAXIMUS AI 3.0 demonstration."""

def __init__(self, dataset_path: str = "demo/synthetic_events.json"):
    """Initialize demo with synthetic dataset."""
    self.dataset_path = dataset_path
    self.events = []
    self.metrics = {
        "total_events": 0,
        "threats_detected": 0,
        "false_positives": 0,
        "false_negatives": 0,
        "avg_latency_ms": 0.0,
        "skills_executed": 0,
        "ethical_approvals": 0,
        "ethical_rejections": 0,
        "prediction_errors": [],
```

**Public Methods:**

- `def load_dataset(self)`
- `def display_event_result(self, event`
- `def display_final_metrics(self)`

---

### `AllServicesTools`

**File:** `all_services_tools.py`

```python
class AllServicesTools:
```

**Description:**
```
"""Aggregates and manages all available tools and services within Maximus.

This class provides a unified interface to access and execute tools from
different categories, such as world-class tools, offensive arsenal, and
advanced tools.
"""

def __init__(self, gemini_client: Any):
    """Initializes AllServicesTools with instances of various tool categories.

    Args:
        gemini_client (Any): An initialized Gemini client for tool interactions.
    """
    self.world_class_tools = WorldClassTools(gemini_client)
    self.offensive_arsenal_tools = OffensiveArsenalTools(gemini_client)
    self.advanced_tools = AdvancedTools(gemini_client)
```

**Public Methods:**

- `def get_tool(self, tool_name`
- `def list_all_tools(self) -> List[Dict[str, Any]]`

---

### `ApplyMaximus`

**File:** `apply_maximus.py`

```python
class ApplyMaximus:
```

**Description:**
```
"""Orchestrates Maximus AI components to process requests and generate intelligent responses.

This class integrates the reasoning engine, memory system, tool orchestrator,
self-reflection, and other core components to provide a comprehensive AI solution.
"""

def __init__(self):
    """Initializes the ApplyMaximus orchestrator with instances of core components."""
    self.reasoning_engine = ReasoningEngine()
    self.memory_system = MemorySystem()
    self.tool_orchestrator = ToolOrchestrator()
    self.self_reflection = SelfReflection()
    self.confidence_scoring = ConfidenceScoring()
    self.chain_of_thought = ChainOfThought()
    self.rag_system = RAGSystem()
    self.agent_templates = AgentTemplates()
```

**Public Methods:**


---

### `ChainOfThought`

**File:** `chain_of_thought.py`

```python
class ChainOfThought:
```

**Description:**
```
"""Implements the Chain of Thought (CoT) reasoning process for Maximus AI.

CoT enables Maximus to break down complex problems into intermediate steps,
articulate its reasoning, and generate more transparent and structured responses.
"""

def __init__(self, gemini_client: Any):
    """Initializes the ChainOfThought module with a Gemini client.

    Args:
        gemini_client (Any): An initialized Gemini client for generating thoughts.
    """
    self.gemini_client = gemini_client

async def generate_thought(
    self, 
```

**Public Methods:**


---

### `MaximusIntegrated`

**File:** `maximus_integrated.py`

```python
class MaximusIntegrated:
```

**Description:**
```
"""Integrates and orchestrates all core components of the Maximus AI system.

This class provides a unified interface to the entire Maximus AI, managing
the interactions between its autonomic core, reasoning capabilities, memory,
and tool-use functionalities.
"""

def __init__(self):
    """Initializes all Maximus AI components and sets up their interconnections."""
    # Initialize core clients/dependencies
    gemini_config = GeminiConfig(
        api_key=os.getenv("GEMINI_API_KEY", ""),
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=4096,
        timeout=60,
```

**Public Methods:**

- `def get_neuromodulated_parameters(self) -> Dict[str, Any]`
- `def get_neuromodulation_state(self) -> Dict[str, Any]`
- `def predict_with_hpc_network(`
- `def get_predictive_coding_state(self) -> Dict[str, Any]`
- `def get_skill_learning_state(self) -> Dict[str, Any]`

---

### `RAGSystem`

**File:** `rag_system.py`

```python
class RAGSystem:
```

**Description:**
```
"""Implements the Retrieval Augmented Generation (RAG) pattern for Maximus AI.

RAG enhances the AI's ability to generate informed and accurate responses
by retrieving relevant information from an external knowledge base.
"""

def __init__(self, vector_db_client: Any):
    """Initializes the RAGSystem with a vector database client.

    Args:
        vector_db_client (Any): An initialized client for interacting with the vector database.
    """
    self.vector_db_client = vector_db_client

async def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Retrieves relevant documents from the knowledge base based on a query.
```

**Public Methods:**


---

### `CircuitState`

**File:** `reasoning_engine.py`

```python
class CircuitState(Enum):
```

**Description:**
```
"""Circuit breaker states for external API calls."""
CLOSED = "closed"  # Normal operation
OPEN = "open"      # Failures detected, blocking calls
HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
"""Circuit breaker pattern implementation for LLM API calls.

Prevents cascade failures by opening circuit after threshold failures,
allowing periodic retry attempts.
"""

def __init__(
    self,
    failure_threshold: int = 5,
```

**Public Methods:**


---

### `CircuitBreaker`

**File:** `reasoning_engine.py`

```python
class CircuitBreaker:
```

**Description:**
```
"""Circuit breaker pattern implementation for LLM API calls.

Prevents cascade failures by opening circuit after threshold failures,
allowing periodic retry attempts.
"""

def __init__(
    self,
    failure_threshold: int = 5,
    recovery_timeout: int = 60,
    success_threshold: int = 2
):
    """Initialize circuit breaker.

    Args:
        failure_threshold: Number of failures before opening circuit.
```

**Public Methods:**

- `def call_succeeded(self) -> None`
- `def call_failed(self) -> None`
- `def can_attempt(self) -> bool`

---

### `ReasoningEngine`

**File:** `reasoning_engine.py`

```python
class ReasoningEngine:
```

**Description:**
```
"""The core cognitive component of Maximus AI, responsible for processing information,
making decisions, and generating coherent responses.

It leverages advanced large language models (LLMs) to perform complex reasoning tasks
with circuit breaker protection for API resilience.
"""

def __init__(self, gemini_client: Any, enable_circuit_breaker: bool = True):
    """Initializes the ReasoningEngine with a Gemini client.

    Args:
        gemini_client (Any): An initialized Gemini client for LLM interactions.
        enable_circuit_breaker (bool): Enable circuit breaker for API resilience. Default: True.
    """
    self.gemini_client = gemini_client
    self.circuit_breaker = CircuitBreaker() if enable_circuit_breaker else None
```

**Public Methods:**


---

### `WorldClassTools`

**File:** `tools_world_class.py`

```python
class WorldClassTools:
```

**Description:**
```
"""A collection of high-quality, general-purpose tools for Maximus AI.

These tools provide functionalities like web searching, data retrieval,
and interaction with external APIs.
"""

def __init__(self, gemini_client: Any):
    """Initializes the WorldClassTools with a Gemini client.

    Args:
        gemini_client (Any): An initialized Gemini client for tool interactions.
    """
    self.gemini_client = gemini_client
    self.available_tools = [
        {
            "name": "search_web",
```

**Public Methods:**

- `def list_available_tools(self) -> List[Dict[str, Any]]`

---

### `VectorDBClient`

**File:** `vector_db_client.py`

```python
class VectorDBClient:
```

**Description:**
```
"""Client for interacting with a vector database.

This client abstracts the underlying vector database implementation, allowing
Maximus to store, retrieve, and manage high-dimensional vector embeddings efficiently.
"""

def __init__(self):
    """Initializes the VectorDBClient. In a real scenario, this would connect to a vector database."""
    self.documents: Dict[str, Dict[str, Any]] = {}
    print("[VectorDBClient] Initialized mock vector database.")

async def add_document(
    self, content: str, metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Adds a document to the vector database.
```

**Public Methods:**


---

### `SyntheticDatasetGenerator`

**File:** `synthetic_dataset.py`

```python
class SyntheticDatasetGenerator:
```

**Description:**
```
"""Generate realistic security events for demonstration."""

def __init__(self, seed: int = 42):
    """Initialize generator with random seed for reproducibility."""
    random.seed(seed)
    self.start_time = datetime(2025, 10, 6, 8, 0, 0)

def generate_normal_traffic(self, count: int = 40) -> list[dict[str, Any]]:
    """Generate normal network traffic events."""
    events = []
    normal_destinations = [
        ("8.8.8.8", 443, "https", "google.com"),
        ("1.1.1.1", 443, "https", "cloudflare.com"),
        ("13.107.42.14", 443, "https", "microsoft.com"),
        ("142.250.80.46", 443, "https", "youtube.com"),
    ]
```

**Public Methods:**

- `def generate_normal_traffic(self, count`
- `def generate_malware_events(self, count`
- `def generate_lateral_movement(self, count`
- `def generate_data_exfiltration(self, count`
- `def generate_c2_beacons(self, count`
- `def generate_privilege_escalation(self, count`
- `def generate_anomalies(self, count`
- `def generate_complete_dataset(self) -> list[dict[str, Any]]`
- `def save_dataset(self, filepath`

---

### `DistributedOrganismTools`

**File:** `distributed_organism_tools.py`

```python
class DistributedOrganismTools:
```

**Description:**
```
"""Distributed Organism Tools for MAXIMUS AI.

Integrates FASE 10 services:
- Edge Agent Service (port 8021)
- Cloud Coordinator Service (port 8022)
"""

def __init__(self, gemini_client: Any):
    """Initialize Distributed Organism Tools.

    Args:
        gemini_client: Gemini client instance
    """
    self.gemini_client = gemini_client
    self.edge_url = "http://localhost:8021"
    self.coordinator_url = "http://localhost:8022"
```

**Public Methods:**

- `def list_available_tools(self) -> list[dict[str, Any]]`

---

### `EnhancedCognitionTools`

**File:** `enhanced_cognition_tools.py`

```python
class EnhancedCognitionTools:
```

**Description:**
```
"""Enhanced Cognition Tools for MAXIMUS AI.

Integrates FASE 8 services:
- Narrative Analysis Service (port 8015)
- Predictive Threat Hunting Service (port 8016)
- Autonomous Investigation Service (port 8017)
"""

def __init__(self, gemini_client: Any):
    """Initialize Enhanced Cognition Tools.

    Args:
        gemini_client: Gemini client instance
    """
    self.gemini_client = gemini_client
    self.narrative_url = "http://localhost:8015"
```

**Public Methods:**

- `def list_available_tools(self) -> list[dict[str, Any]]`

---

### `EthicalDecisionType`

**File:** `ethical_guardian.py`

```python
class EthicalDecisionType(str, Enum):
```

**Description:**
```
"""Tipo de decisão ética final."""

APPROVED = "approved"
APPROVED_WITH_CONDITIONS = "approved_with_conditions"
REJECTED_BY_GOVERNANCE = "rejected_by_governance"
REJECTED_BY_ETHICS = "rejected_by_ethics"
REJECTED_BY_FAIRNESS = "rejected_by_fairness"  # Phase 3
REJECTED_BY_PRIVACY = "rejected_by_privacy"  # Phase 4.1
REJECTED_BY_COMPLIANCE = "rejected_by_compliance"
REQUIRES_HUMAN_REVIEW = "requires_human_review"  # Phase 5: HITL
ERROR = "error"


@dataclass
class GovernanceCheckResult:
"""Resultado do check de governance."""
```

**Public Methods:**


---

### `GovernanceCheckResult`

**File:** `ethical_guardian.py`

```python
class GovernanceCheckResult:
```

**Description:**
```
"""Resultado do check de governance."""

is_compliant: bool
policies_checked: list[PolicyType]
violations: list[dict[str, Any]] = field(default_factory=list)
warnings: list[str] = field(default_factory=list)
duration_ms: float = 0.0


@dataclass
class EthicsCheckResult:
"""Resultado da avaliação ética."""

verdict: EthicalVerdict
confidence: float
framework_results: list[dict[str, Any]] = field(default_factory=list)
```

**Public Methods:**


---

### `EthicsCheckResult`

**File:** `ethical_guardian.py`

```python
class EthicsCheckResult:
```

**Description:**
```
"""Resultado da avaliação ética."""

verdict: EthicalVerdict
confidence: float
framework_results: list[dict[str, Any]] = field(default_factory=list)
duration_ms: float = 0.0


@dataclass
class XAICheckResult:
"""Resultado da explicação XAI."""

explanation_type: str
summary: str
feature_importances: list[dict[str, Any]] = field(default_factory=list)
duration_ms: float = 0.0
```

**Public Methods:**


---

### `XAICheckResult`

**File:** `ethical_guardian.py`

```python
class XAICheckResult:
```

**Description:**
```
"""Resultado da explicação XAI."""

explanation_type: str
summary: str
feature_importances: list[dict[str, Any]] = field(default_factory=list)
duration_ms: float = 0.0


@dataclass
class ComplianceCheckResult:
"""Resultado do check de compliance."""

regulations_checked: list[RegulationType]
compliance_results: dict[str, dict[str, Any]] = field(default_factory=dict)
overall_compliant: bool = True
duration_ms: float = 0.0
```

**Public Methods:**


---

### `ComplianceCheckResult`

**File:** `ethical_guardian.py`

```python
class ComplianceCheckResult:
```

**Description:**
```
"""Resultado do check de compliance."""

regulations_checked: list[RegulationType]
compliance_results: dict[str, dict[str, Any]] = field(default_factory=dict)
overall_compliant: bool = True
duration_ms: float = 0.0


@dataclass
class FairnessCheckResult:
"""Resultado do check de fairness e bias (Phase 3)."""

fairness_ok: bool
bias_detected: bool
protected_attributes_checked: list[str]  # ProtectedAttribute.value
fairness_metrics: dict[str, float]  # metric_name -> score
```

**Public Methods:**


---

### `FairnessCheckResult`

**File:** `ethical_guardian.py`

```python
class FairnessCheckResult:
```

**Description:**
```
"""Resultado do check de fairness e bias (Phase 3)."""

fairness_ok: bool
bias_detected: bool
protected_attributes_checked: list[str]  # ProtectedAttribute.value
fairness_metrics: dict[str, float]  # metric_name -> score
bias_severity: str  # low, medium, high, critical
affected_groups: list[str] = field(default_factory=list)
mitigation_recommended: bool = False
confidence: float = 0.0
duration_ms: float = 0.0


@dataclass
class PrivacyCheckResult:
"""Resultado do check de privacidade diferencial (Phase 4.1)."""
```

**Public Methods:**


---

### `PrivacyCheckResult`

**File:** `ethical_guardian.py`

```python
class PrivacyCheckResult:
```

**Description:**
```
"""Resultado do check de privacidade diferencial (Phase 4.1)."""

privacy_budget_ok: bool
privacy_level: str  # PrivacyLevel.value
total_epsilon: float
used_epsilon: float
remaining_epsilon: float
total_delta: float
used_delta: float
remaining_delta: float
budget_exhausted: bool
queries_executed: int
duration_ms: float = 0.0


@dataclass
```

**Public Methods:**


---

### `FLCheckResult`

**File:** `ethical_guardian.py`

```python
class FLCheckResult:
```

**Description:**
```
"""Resultado do check de federated learning (Phase 4.2)."""

fl_ready: bool
fl_status: str  # FLStatus.value
model_type: str | None = None  # ModelType.value
aggregation_strategy: str | None = None  # AggregationStrategy.value
requires_dp: bool = False
dp_epsilon: float | None = None
dp_delta: float | None = None
notes: list[str] = field(default_factory=list)
duration_ms: float = 0.0


@dataclass
class HITLCheckResult:
"""Resultado do check de HITL (Phase 5)."""
```

**Public Methods:**


---

### `HITLCheckResult`

**File:** `ethical_guardian.py`

```python
class HITLCheckResult:
```

**Description:**
```
"""Resultado do check de HITL (Phase 5)."""

requires_human_review: bool
automation_level: str  # AutomationLevel.value
risk_level: str  # RiskLevel.value
confidence_threshold_met: bool
estimated_sla_minutes: int = 0
escalation_recommended: bool = False
human_expertise_required: list[str] = field(default_factory=list)  # Required skills
decision_rationale: str = ""
duration_ms: float = 0.0


@dataclass
class EthicalDecisionResult:
"""Resultado completo da decisão ética."""
```

**Public Methods:**


---

### `EthicalDecisionResult`

**File:** `ethical_guardian.py`

```python
class EthicalDecisionResult:
```

**Description:**
```
"""Resultado completo da decisão ética."""

decision_id: str = field(default_factory=lambda: str(uuid4()))
decision_type: EthicalDecisionType = EthicalDecisionType.ERROR
action: str = ""
actor: str = ""
timestamp: datetime = field(default_factory=datetime.utcnow)

# Results from each phase
governance: GovernanceCheckResult | None = None
ethics: EthicsCheckResult | None = None
fairness: FairnessCheckResult | None = None  # Phase 3
xai: XAICheckResult | None = None
privacy: PrivacyCheckResult | None = None  # Phase 4.1
fl: FLCheckResult | None = None  # Phase 4.2
hitl: HITLCheckResult | None = None  # Phase 5
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `EthicalGuardian`

**File:** `ethical_guardian.py`

```python
class EthicalGuardian:
```

**Description:**
```
"""
Guardian que valida todas as ações do MAXIMUS através do Ethical AI Stack.

Integra as 7 fases éticas:
- Phase 0: Governance (ERB, Policies, Audit)
- Phase 1: Ethics (4 frameworks filosóficos)
- Phase 2: XAI (Explicabilidade)
- Phase 3: Fairness (Bias - futuro)
- Phase 4: Privacy (Proteção de dados - futuro)
- Phase 5: HITL (Human-in-the-Loop - futuro)
- Phase 6: Compliance (Regulações)

Performance target: <500ms por validação completa
"""

def __init__(
```

**Public Methods:**

- `def get_statistics(self) -> dict[str, Any]`

---

### `ToolExecutionResult`

**File:** `ethical_tool_wrapper.py`

```python
class ToolExecutionResult:
```

**Description:**
```
"""
Resultado completo da execução de um tool com informações éticas.
"""

execution_id: str = field(default_factory=lambda: str(uuid4()))
tool_name: str = ""
success: bool = False
timestamp: datetime = field(default_factory=datetime.utcnow)

# Tool execution
output: Any = None
error: str | None = None
execution_duration_ms: float = 0.0

# Ethical validation
ethical_decision: EthicalDecisionResult | None = None
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def get_summary(self) -> str`

---

### `EthicalToolWrapper`

**File:** `ethical_tool_wrapper.py`

```python
class EthicalToolWrapper:
```

**Description:**
```
"""
Wrapper que intercepta execução de tools e aplica validação ética.

Este wrapper é injetado no ToolOrchestrator para garantir que TODAS
as execuções de tool passem pelo Ethical Guardian.

Performance:
- Pre-check: <500ms (parallel governance + ethics)
- Execution: Tempo original do tool
- Post-check: <300ms (parallel xai + compliance)
- Total overhead: <500ms (target)
"""

def __init__(
    self,
    ethical_guardian: EthicalGuardian,
```

**Public Methods:**

- `def get_statistics(self) -> dict[str, Any]`
- `def reset_statistics(self)`

---

### `EthicalVerdict`

**File:** `base.py`

```python
class EthicalVerdict(str, Enum):
```

**Description:**
```
"""Possible verdicts from ethical evaluation."""

APPROVED = "APPROVED"
REJECTED = "REJECTED"
CONDITIONAL = "CONDITIONAL"  # Approved with conditions


@dataclass
class EthicalFrameworkResult:
"""Result from an ethical framework evaluation.

Attributes:
    framework_name: Name of the framework (kantian, consequentialist, etc.)
    approved: Whether the action is ethically approved
    confidence: Confidence score (0.0 to 1.0)
    veto: Whether this framework vetoes the decision (overrides others)
```

**Public Methods:**


---

### `EthicalFrameworkResult`

**File:** `base.py`

```python
class EthicalFrameworkResult:
```

**Description:**
```
"""Result from an ethical framework evaluation.

Attributes:
    framework_name: Name of the framework (kantian, consequentialist, etc.)
    approved: Whether the action is ethically approved
    confidence: Confidence score (0.0 to 1.0)
    veto: Whether this framework vetoes the decision (overrides others)
    explanation: Human-readable explanation of the decision
    reasoning_steps: List of reasoning steps taken
    verdict: Final verdict (APPROVED, REJECTED, CONDITIONAL)
    latency_ms: Time taken for evaluation in milliseconds
    metadata: Additional framework-specific data
"""

framework_name: str
approved: bool
```

**Public Methods:**


---

### `ActionContext`

**File:** `base.py`

```python
class ActionContext:
```

**Description:**
```
"""Context for an action requiring ethical evaluation.

Attributes:
    action_type: Type of action (offensive, defensive, policy_change, etc.)
    action_description: Detailed description of the proposed action
    system_component: Which component is proposing the action
    threat_data: Information about the threat (if applicable)
    target_info: Information about the target (IP, domain, etc.)
    impact_assessment: Estimated impact of the action
    alternatives: Alternative actions considered
    urgency: Urgency level (low, medium, high, critical)
    operator_context: Human operator information (if HITL)
"""

action_type: str
action_description: str
```

**Public Methods:**


---

### `EthicalFramework`

**File:** `base.py`

```python
class EthicalFramework(ABC):
```

**Description:**
```
"""Abstract base class for all ethical frameworks.

All ethical frameworks (Kantian, Consequentialist, Virtue Ethics, Principialism)
must inherit from this class and implement the evaluate() method.
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize the ethical framework.

    Args:
        config: Configuration dictionary for the framework
    """
    self.config = config or {}
    self.name = self.__class__.__name__.lower()

@abstractmethod
```

**Public Methods:**

- `def get_framework_principles(self) -> list[str]`
- `def get_name(self) -> str`
- `def get_version(self) -> str`

---

### `EthicalCache`

**File:** `base.py`

```python
class EthicalCache:
```

**Description:**
```
"""Simple in-memory cache for ethical decisions.

Caches decisions for identical actions to reduce latency on repeated evaluations.
"""

def __init__(self, max_size: int = 10000, ttl_seconds: int = 3600):
    """Initialize the cache.

    Args:
        max_size: Maximum number of cached decisions
        ttl_seconds: Time-to-live for cached decisions in seconds
    """
    self._cache: dict[str, tuple[EthicalFrameworkResult, float]] = {}
    self.max_size = max_size
    self.ttl_seconds = ttl_seconds
```

**Public Methods:**

- `def get(self, cache_key`
- `def set(self, cache_key`
- `def generate_key(self, action_context`

---

### `EthicalException`

**File:** `base.py`

```python
class EthicalException(Exception):
```

**Description:**
```
"""Base exception for ethical framework errors."""

pass


class VetoException(EthicalException):
"""Exception raised when a framework vetoes a decision."""

def __init__(self, framework_name: str, reason: str):
    self.framework_name = framework_name
    self.reason = reason
    super().__init__(f"{framework_name} vetoed the decision: {reason}")
```

**Public Methods:**


---

### `VetoException`

**File:** `base.py`

```python
class VetoException(EthicalException):
```

**Description:**
```
"""Exception raised when a framework vetoes a decision."""

def __init__(self, framework_name: str, reason: str):
    self.framework_name = framework_name
    self.reason = reason
    super().__init__(f"{framework_name} vetoed the decision: {reason}")
```

**Public Methods:**


---

### `ConsequentialistEngine`

**File:** `consequentialist_engine.py`

```python
class ConsequentialistEngine(EthicalFramework):
```

**Description:**
```
"""Utilitarian consequentialist ethics engine."""

def __init__(self, config: dict[str, Any] = None):
    """Initialize consequentialist engine.

    Args:
        config: Configuration with utility weights and thresholds
    """
    super().__init__(config)

    # Weights for Bentham's calculus dimensions (must sum to 1.0)
    self.weights = (
        config.get(
            "weights",
            {
                "intensity": 0.20,  # Severity of threat vs. impact of response
```

**Public Methods:**

- `def get_framework_principles(self) -> list[str]`

---

### `IntegratedEthicalDecision`

**File:** `integration_engine.py`

```python
class IntegratedEthicalDecision:
```

**Description:**
```
"""Final integrated ethical decision from all frameworks.

Attributes:
    final_decision: APPROVED, REJECTED, or ESCALATED_HITL
    final_confidence: Overall confidence (0.0 to 1.0)
    explanation: Human-readable explanation
    framework_results: Results from each framework
    aggregation_method: How frameworks were combined
    veto_applied: Whether Kantian veto was used
    framework_agreement_rate: % of frameworks that agree
    total_latency_ms: Total evaluation time
    metadata: Additional decision data
"""

final_decision: str
final_confidence: float
```

**Public Methods:**


---

### `EthicalIntegrationEngine`

**File:** `integration_engine.py`

```python
class EthicalIntegrationEngine:
```

**Description:**
```
"""Integrates multiple ethical frameworks into unified decisions."""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize integration engine.

    Args:
        config: Configuration dict with framework weights, thresholds, etc.
    """
    self.config = config or {}

    # Framework weights (how much each framework contributes to final decision)
    self.framework_weights = self.config.get(
        "framework_weights",
        {
            "kantian_deontology": 0.30,  # Highest weight due to veto power
            "consequentialism": 0.25,
```

**Public Methods:**


---

### `KantianImperativeChecker`

**File:** `kantian_checker.py`

```python
class KantianImperativeChecker(EthicalFramework):
```

**Description:**
```
"""Kantian deontological ethics checker with veto power."""

# Categorical rules that ALWAYS apply (deontological absolutes)
CATEGORICAL_NEVER = [
    "use_humans_as_mere_means",
    "violate_human_dignity",
    "violate_human_autonomy",
    "implement_surveillance_without_consent",
    "make_irreversible_decisions_without_human_review",
    "deploy_offensive_autonomously_without_approval",
    "access_private_data_without_justification",
    "harm_innocents_as_collateral",
]

CATEGORICAL_ALWAYS = [
    "preserve_human_override_capability",
```

**Public Methods:**

- `def get_framework_principles(self) -> list[str]`

---

### `PrinciplismFramework`

**File:** `principialism.py`

```python
class PrinciplismFramework(EthicalFramework):
```

**Description:**
```
"""Four principles ethics framework."""

def __init__(self, config: dict[str, Any] = None):
    """Initialize principialism framework.

    Args:
        config: Configuration with principle weights and thresholds
    """
    super().__init__(config)

    # Principle weights
    self.weights = (
        config.get(
            "weights",
            {
                "beneficence": 0.25,
```

**Public Methods:**

- `def get_framework_principles(self) -> list[str]`

---

### `VirtueEthicsAssessment`

**File:** `virtue_ethics.py`

```python
class VirtueEthicsAssessment(EthicalFramework):
```

**Description:**
```
"""Aristotelian virtue ethics assessor."""

# Cardinal virtues for cybersecurity
CARDINAL_VIRTUES = {
    "courage": {
        "description": "Facing threats boldly but not recklessly",
        "excess": "recklessness",
        "deficiency": "cowardice",
        "golden_mean": "measured boldness",
    },
    "temperance": {
        "description": "Moderation in response, avoiding overreaction",
        "excess": "passivity",
        "deficiency": "aggression",
        "golden_mean": "proportionate response",
    },
```

**Public Methods:**

- `def get_framework_principles(self) -> list[str]`

---

### `ThreatDetectionModel`

**File:** `02_autonomous_training_workflow.py`

```python
class ThreatDetectionModel(nn.Module):
```

**Description:**
```
"""
Simple neural network for threat detection.

Architecture:
    Input (10 features) → Hidden (64) → Hidden (32) → Output (2 classes)
"""

def __init__(self):
    super().__init__()
    self.fc1 = nn.Linear(10, 64)
    self.relu1 = nn.ReLU()
    self.dropout1 = nn.Dropout(0.2)
    self.fc2 = nn.Linear(64, 32)
    self.relu2 = nn.ReLU()
    self.dropout2 = nn.Dropout(0.2)
    self.fc3 = nn.Linear(32, 2)
```

**Public Methods:**

- `def forward(self, x)`

---

### `LargeDetectionModel`

**File:** `03_performance_optimization_pipeline.py`

```python
class LargeDetectionModel(nn.Module):
```

**Description:**
```
"""
Larger neural network for demonstrating optimization benefits.

Architecture:
    Input (128) → Hidden (512) → Hidden (256) → Hidden (128) → Output (2)
"""

def __init__(self):
    super().__init__()
    self.layers = nn.Sequential(
        nn.Linear(128, 512),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(512, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
```

**Public Methods:**

- `def forward(self, x)`

---

### `ProtectedAttribute`

**File:** `base.py`

```python
class ProtectedAttribute(str, Enum):
```

**Description:**
```
"""Protected attributes for fairness analysis in cybersecurity context."""

GEOGRAPHIC_LOCATION = "geographic_location"  # Country/region
ORGANIZATION_SIZE = "organization_size"  # SMB vs Enterprise
INDUSTRY_VERTICAL = "industry_vertical"  # Finance, healthcare, tech, etc.


class FairnessMetric(str, Enum):
"""Fairness metrics supported by the system."""

DEMOGRAPHIC_PARITY = "demographic_parity"  # P(Ŷ=1|A=0) = P(Ŷ=1|A=1)
EQUALIZED_ODDS = "equalized_odds"  # TPR and FPR equal across groups
EQUAL_OPPORTUNITY = "equal_opportunity"  # TPR equal across groups
CALIBRATION = "calibration"  # P(Y=1|Ŷ=p,A=0) = P(Y=1|Ŷ=p,A=1)
PREDICTIVE_PARITY = "predictive_parity"  # PPV equal across groups
TREATMENT_EQUALITY = "treatment_equality"  # FN/FP ratio equal across groups
```

**Public Methods:**


---

### `FairnessMetric`

**File:** `base.py`

```python
class FairnessMetric(str, Enum):
```

**Description:**
```
"""Fairness metrics supported by the system."""

DEMOGRAPHIC_PARITY = "demographic_parity"  # P(Ŷ=1|A=0) = P(Ŷ=1|A=1)
EQUALIZED_ODDS = "equalized_odds"  # TPR and FPR equal across groups
EQUAL_OPPORTUNITY = "equal_opportunity"  # TPR equal across groups
CALIBRATION = "calibration"  # P(Y=1|Ŷ=p,A=0) = P(Y=1|Ŷ=p,A=1)
PREDICTIVE_PARITY = "predictive_parity"  # PPV equal across groups
TREATMENT_EQUALITY = "treatment_equality"  # FN/FP ratio equal across groups


@dataclass
class FairnessResult:
"""Result from fairness constraint evaluation.

Attributes:
    metric: Fairness metric evaluated
```

**Public Methods:**


---

### `FairnessResult`

**File:** `base.py`

```python
class FairnessResult:
```

**Description:**
```
"""Result from fairness constraint evaluation.

Attributes:
    metric: Fairness metric evaluated
    protected_attribute: Protected attribute analyzed
    group_0_value: Metric value for reference group
    group_1_value: Metric value for protected group
    difference: Absolute difference between groups
    ratio: Ratio between groups (min/max)
    is_fair: Whether fairness constraint is satisfied
    threshold: Fairness threshold used
    timestamp: When evaluation was performed
    sample_size_0: Sample size for group 0
    sample_size_1: Sample size for group 1
    metadata: Additional metadata
"""
```

**Public Methods:**

- `def get_disparity_percentage(self) -> float`

---

### `BiasDetectionResult`

**File:** `base.py`

```python
class BiasDetectionResult:
```

**Description:**
```
"""Result from bias detection analysis.

Attributes:
    bias_detected: Whether bias was detected
    protected_attribute: Protected attribute analyzed
    detection_method: Method used for detection
    p_value: Statistical p-value (if applicable)
    effect_size: Effect size (Cohen's d or similar)
    confidence: Confidence in detection (0-1)
    affected_groups: List of affected groups
    severity: Bias severity (low, medium, high, critical)
    timestamp: When detection was performed
    sample_size: Total sample size
    metadata: Additional metadata
"""
```

**Public Methods:**


---

### `MitigationResult`

**File:** `base.py`

```python
class MitigationResult:
```

**Description:**
```
"""Result from bias mitigation.

Attributes:
    mitigation_method: Method used for mitigation
    protected_attribute: Protected attribute targeted
    fairness_before: Fairness metrics before mitigation
    fairness_after: Fairness metrics after mitigation
    performance_impact: Impact on model performance
    success: Whether mitigation was successful
    timestamp: When mitigation was performed
    metadata: Additional metadata
"""

mitigation_method: str
protected_attribute: ProtectedAttribute
fairness_before: dict[str, float]
```

**Public Methods:**

- `def get_fairness_improvement(self, metric`

---

### `FairnessException`

**File:** `base.py`

```python
class FairnessException(Exception):
```

**Description:**
```
"""Base exception for fairness module errors."""

pass


class InsufficientDataException(FairnessException):
"""Exception raised when insufficient data for fairness analysis."""

def __init__(self, required_samples: int, actual_samples: int):
    self.required_samples = required_samples
    self.actual_samples = actual_samples
    super().__init__(
        f"Insufficient data for fairness analysis. Required: {required_samples}, Got: {actual_samples}"
    )
```

**Public Methods:**


---

### `InsufficientDataException`

**File:** `base.py`

```python
class InsufficientDataException(FairnessException):
```

**Description:**
```
"""Exception raised when insufficient data for fairness analysis."""

def __init__(self, required_samples: int, actual_samples: int):
    self.required_samples = required_samples
    self.actual_samples = actual_samples
    super().__init__(
        f"Insufficient data for fairness analysis. Required: {required_samples}, Got: {actual_samples}"
    )


class FairnessViolationException(FairnessException):
"""Exception raised when fairness constraint is violated."""

def __init__(self, metric: FairnessMetric, result: FairnessResult):
    self.metric = metric
    self.result = result
```

**Public Methods:**


---

### `FairnessViolationException`

**File:** `base.py`

```python
class FairnessViolationException(FairnessException):
```

**Description:**
```
"""Exception raised when fairness constraint is violated."""

def __init__(self, metric: FairnessMetric, result: FairnessResult):
    self.metric = metric
    self.result = result
    super().__init__(
        f"Fairness violation detected: {metric.value}. "
        f"Difference: {result.difference:.3f}, Threshold: {result.threshold:.3f}"
    )
```

**Public Methods:**


---

### `BiasDetector`

**File:** `bias_detector.py`

```python
class BiasDetector:
```

**Description:**
```
"""Bias detector for cybersecurity AI models.

Implements multiple statistical tests and methods to detect bias
in model predictions across different protected groups.

Attributes:
    min_sample_size: Minimum samples required per group
    significance_level: Statistical significance level (alpha)
    disparate_impact_threshold: Threshold for disparate impact (default 0.8 = 4/5ths rule)
    effect_size_thresholds: Thresholds for Cohen's d effect size
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize BiasDetector.

    Args:
```

**Public Methods:**

- `def detect_statistical_parity_bias(`
- `def detect_disparate_impact(`
- `def detect_distribution_bias(`
- `def detect_performance_disparity(`
- `def detect_all_biases(`

---

### `FairnessConstraints`

**File:** `constraints.py`

```python
class FairnessConstraints:
```

**Description:**
```
"""Fairness constraints validator for cybersecurity models.

Implements multiple fairness metrics to ensure equitable treatment
across different protected groups in threat detection and security decisions.
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize FairnessConstraints.

    Args:
        config: Configuration dictionary with thresholds
    """
    config = config or {}

    # Fairness thresholds (max allowed disparity)
    self.thresholds = {
```

**Public Methods:**

- `def evaluate_demographic_parity(`
- `def evaluate_equalized_odds(`
- `def evaluate_equal_opportunity(`
- `def evaluate_calibration(`
- `def evaluate_all_metrics(`

---

### `MitigationEngine`

**File:** `mitigation.py`

```python
class MitigationEngine:
```

**Description:**
```
"""Bias mitigation engine for cybersecurity AI models.

Implements multiple mitigation strategies to reduce bias while
maintaining acceptable model performance.

Attributes:
    fairness_constraints: FairnessConstraints instance for evaluation
    performance_threshold: Minimum acceptable performance after mitigation
    fairness_improvement_threshold: Minimum fairness improvement required
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize MitigationEngine.

    Args:
        config: Configuration dictionary
```

**Public Methods:**

- `def mitigate_reweighing(`
- `def mitigate_threshold_optimization(`
- `def mitigate_calibration_adjustment(`
- `def mitigate_auto(`

---

### `FairnessAlert`

**File:** `monitor.py`

```python
class FairnessAlert:
```

**Description:**
```
"""Alert for fairness violation.

Attributes:
    alert_id: Unique alert identifier
    timestamp: When alert was triggered
    severity: Alert severity (low, medium, high, critical)
    metric: Fairness metric that triggered alert
    protected_attribute: Affected protected attribute
    violation_details: Details of the violation
    recommended_action: Suggested mitigation action
    auto_mitigated: Whether automatic mitigation was applied
"""

alert_id: str
timestamp: datetime
severity: str
```

**Public Methods:**


---

### `FairnessSnapshot`

**File:** `monitor.py`

```python
class FairnessSnapshot:
```

**Description:**
```
"""Snapshot of fairness metrics at a point in time.

Attributes:
    timestamp: When snapshot was taken
    model_id: Model identifier
    protected_attribute: Protected attribute
    fairness_results: Fairness evaluation results
    bias_results: Bias detection results
    sample_size: Number of samples in snapshot
    metadata: Additional metadata
"""

timestamp: datetime
model_id: str
protected_attribute: ProtectedAttribute
fairness_results: dict[FairnessMetric, FairnessResult]
```

**Public Methods:**


---

### `FairnessMonitor`

**File:** `monitor.py`

```python
class FairnessMonitor:
```

**Description:**
```
"""Fairness monitor for continuous tracking and alerting.

Monitors fairness metrics over time, detects violations, generates alerts,
and maintains historical records for trend analysis.

Attributes:
    fairness_constraints: FairnessConstraints instance
    bias_detector: BiasDetector instance
    history_max_size: Maximum snapshots to keep in memory
    alert_threshold: Threshold for generating alerts
    enable_auto_mitigation: Whether to automatically mitigate violations
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize FairnessMonitor.
```

**Public Methods:**

- `def evaluate_fairness(`
- `def get_fairness_trends(`
- `def detect_drift(self, model_id`
- `def get_alerts(`
- `def get_statistics(self) -> dict[str, Any]`
- `def clear_history(self, before_timestamp`

---

### `AggregationResult`

**File:** `aggregation.py`

```python
class AggregationResult:
```

**Description:**
```
"""
Result of aggregating model updates.

Attributes:
    aggregated_weights: Aggregated model weights
    num_clients: Number of clients that contributed
    total_samples: Total number of samples across clients
    aggregation_time: Time taken to aggregate (seconds)
    strategy: Aggregation strategy used
    privacy_cost: Privacy budget consumed (if DP applied)
    metadata: Additional metadata about aggregation
"""

aggregated_weights: dict[str, np.ndarray]
num_clients: int
total_samples: int
```

**Public Methods:**

- `def get_total_parameters(self) -> int`
- `def to_dict(self, include_weights`

---

### `BaseAggregator`

**File:** `aggregation.py`

```python
class BaseAggregator(ABC):
```

**Description:**
```
"""Base class for aggregation strategies."""

@abstractmethod
def aggregate(self, updates: list[ModelUpdate]) -> AggregationResult:
    """
    Aggregate model updates from multiple clients.

    Args:
        updates: List of model updates from clients

    Returns:
        AggregationResult with aggregated weights
    """
    pass

def _validate_updates(self, updates: list[ModelUpdate]) -> None:
```

**Public Methods:**

- `def aggregate(self, updates`

---

### `FedAvgAggregator`

**File:** `aggregation.py`

```python
class FedAvgAggregator(BaseAggregator):
```

**Description:**
```
"""
Federated Averaging (FedAvg) aggregator.

Implements the FedAvg algorithm from:
McMahan et al., "Communication-Efficient Learning of Deep Networks
from Decentralized Data", AISTATS 2017.

Aggregation formula:
    w_global = Σ (n_k / n_total) × w_k

where:
    - w_k: weights from client k
    - n_k: number of samples from client k
    - n_total: total samples across all clients
"""
```

**Public Methods:**

- `def aggregate(self, updates`

---

### `SecureAggregator`

**File:** `aggregation.py`

```python
class SecureAggregator(BaseAggregator):
```

**Description:**
```
"""
Secure aggregation using secret sharing.

Implements a simplified secure aggregation protocol where the server
cannot see individual client updates, only the aggregate. Based on:
Bonawitz et al., "Practical Secure Aggregation for Privacy-Preserving
Machine Learning", CCS 2017.

Note: This is a simplified implementation. Production use should
employ libraries like TenSEAL or PySyft for robust cryptographic
guarantees.
"""

def __init__(self, threshold: int = 2):
    """
    Initialize secure aggregator.
```

**Public Methods:**

- `def aggregate(self, updates`

---

### `DPAggregator`

**File:** `aggregation.py`

```python
class DPAggregator(BaseAggregator):
```

**Description:**
```
"""
Differential Privacy FedAvg aggregator.

Adds noise to the aggregated model to provide (ε, δ)-differential
privacy guarantee. Implements DP-FedAvg from:
Geyer et al., "Differentially Private Federated Learning: A Client
Level Perspective", NIPS Workshop 2017.

Privacy guarantee: The aggregated model satisfies (ε, δ)-DP with
respect to any single client's participation.
"""

def __init__(
    self,
    epsilon: float = 8.0,
    delta: float = 1e-5,
```

**Public Methods:**

- `def aggregate(self, updates`

---

### `FLStatus`

**File:** `base.py`

```python
class FLStatus(Enum):
```

**Description:**
```
"""Federated learning round status."""

INITIALIZING = "initializing"
WAITING_FOR_CLIENTS = "waiting_for_clients"
TRAINING = "training"
AGGREGATING = "aggregating"
COMPLETED = "completed"
FAILED = "failed"


class AggregationStrategy(Enum):
"""Aggregation strategy for federated learning."""

FEDAVG = "fedavg"  # Federated Averaging (McMahan et al., 2017)
SECURE = "secure"  # Secure aggregation with secret sharing
DP_FEDAVG = "dp_fedavg"  # FedAvg with differential privacy
```

**Public Methods:**


---

### `AggregationStrategy`

**File:** `base.py`

```python
class AggregationStrategy(Enum):
```

**Description:**
```
"""Aggregation strategy for federated learning."""

FEDAVG = "fedavg"  # Federated Averaging (McMahan et al., 2017)
SECURE = "secure"  # Secure aggregation with secret sharing
DP_FEDAVG = "dp_fedavg"  # FedAvg with differential privacy
WEIGHTED = "weighted"  # Weighted averaging by client data size


class ModelType(Enum):
"""Supported model types for federated learning."""

THREAT_CLASSIFIER = "threat_classifier"  # narrative_manipulation_filter
MALWARE_DETECTOR = "malware_detector"  # immunis_macrophage_service
CUSTOM = "custom"
```

**Public Methods:**


---

### `ModelType`

**File:** `base.py`

```python
class ModelType(Enum):
```

**Description:**
```
"""Supported model types for federated learning."""

THREAT_CLASSIFIER = "threat_classifier"  # narrative_manipulation_filter
MALWARE_DETECTOR = "malware_detector"  # immunis_macrophage_service
CUSTOM = "custom"


@dataclass
class FLConfig:
"""
Configuration for federated learning.

Attributes:
    model_type: Type of model to train
    aggregation_strategy: Strategy for aggregating updates
    min_clients: Minimum number of clients required per round
```

**Public Methods:**


---

### `FLConfig`

**File:** `base.py`

```python
class FLConfig:
```

**Description:**
```
"""
Configuration for federated learning.

Attributes:
    model_type: Type of model to train
    aggregation_strategy: Strategy for aggregating updates
    min_clients: Minimum number of clients required per round
    max_clients: Maximum number of clients per round
    client_fraction: Fraction of clients to sample per round (0.0-1.0)
    local_epochs: Number of local training epochs per round
    local_batch_size: Batch size for local training
    learning_rate: Learning rate for local training
    use_differential_privacy: Whether to apply DP to updates
    dp_epsilon: Privacy budget (if DP enabled)
    dp_delta: Failure probability (if DP enabled)
    dp_clip_norm: Gradient clipping norm (if DP enabled)
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ClientInfo`

**File:** `base.py`

```python
class ClientInfo:
```

**Description:**
```
"""
Information about a federated learning client.

Attributes:
    client_id: Unique identifier for the client
    organization: Organization name
    client_version: Client software version
    capabilities: Client capabilities (e.g., GPU, memory)
    last_seen: Last communication timestamp
    total_samples: Total number of training samples
    active: Whether client is currently active
    public_key: Public key for secure communication (optional)
"""

client_id: str
organization: str
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ModelUpdate`

**File:** `base.py`

```python
class ModelUpdate:
```

**Description:**
```
"""
Model update from a federated learning client.

Attributes:
    client_id: ID of the client sending the update
    round_id: Round ID this update belongs to
    weights: Updated model weights (layer_name -> np.ndarray)
    num_samples: Number of samples used for training
    metrics: Training metrics (loss, accuracy, etc.)
    timestamp: When the update was created
    differential_privacy_applied: Whether DP was applied
    epsilon_used: Privacy budget used (if DP applied)
    computation_time: Time taken for local training (seconds)
    signature: Digital signature for verification (optional)
"""
```

**Public Methods:**

- `def get_total_parameters(self) -> int`
- `def get_update_size_mb(self) -> float`
- `def to_dict(self, include_weights`

---

### `FLRound`

**File:** `base.py`

```python
class FLRound:
```

**Description:**
```
"""
Federated learning training round.

Attributes:
    round_id: Unique round identifier
    status: Current round status
    config: Configuration for this round
    selected_clients: Clients selected for this round
    received_updates: Updates received so far
    global_model_version: Version of global model before this round
    start_time: Round start timestamp
    end_time: Round end timestamp (None if ongoing)
    aggregation_result: Result of aggregation (None if not completed)
    metrics: Round-level metrics
"""
```

**Public Methods:**

- `def get_participation_rate(self) -> float`
- `def get_duration_seconds(self) -> float | None`
- `def get_total_samples(self) -> int`
- `def get_average_metrics(self) -> dict[str, float]`
- `def to_dict(self) -> dict[str, Any]`

---

### `FLMetrics`

**File:** `base.py`

```python
class FLMetrics:
```

**Description:**
```
"""
Federated learning performance metrics.

Attributes:
    total_rounds: Total number of rounds completed
    total_clients: Total number of registered clients
    active_clients: Number of currently active clients
    average_participation_rate: Average client participation rate
    average_round_duration: Average round duration (seconds)
    total_samples_trained: Total samples trained across all rounds
    global_model_accuracy: Accuracy of global model on test set
    convergence_status: Whether model has converged
    privacy_budget_used: Total privacy budget used (if DP enabled)
    last_updated: When metrics were last updated
"""
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `MessageType`

**File:** `communication.py`

```python
class MessageType(Enum):
```

**Description:**
```
"""Types of FL communication messages."""

CLIENT_REGISTER = "client_register"
CLIENT_UNREGISTER = "client_unregister"
ROUND_START = "round_start"
MODEL_DOWNLOAD = "model_download"
UPDATE_SUBMIT = "update_submit"
ROUND_STATUS = "round_status"
METRICS_QUERY = "metrics_query"


@dataclass
class EncryptedMessage:
"""
Encrypted message for FL communication.
```

**Public Methods:**


---

### `EncryptedMessage`

**File:** `communication.py`

```python
class EncryptedMessage:
```

**Description:**
```
"""
Encrypted message for FL communication.

Attributes:
    message_type: Type of message
    payload: Message payload (encrypted)
    signature: Digital signature for verification
    timestamp: Message timestamp
    sender_id: ID of sender (client or coordinator)
"""

message_type: MessageType
payload: dict[str, Any]
signature: str | None = None
timestamp: str | None = None
sender_id: str | None = None
```

**Public Methods:**


---

### `FLCommunicationChannel`

**File:** `communication.py`

```python
class FLCommunicationChannel:
```

**Description:**
```
"""
Communication channel for federated learning.

Handles serialization, encryption, and transmission of FL messages
between clients and coordinator.
"""

def __init__(
    self,
    use_encryption: bool = True,
    verify_signatures: bool = True,
):
    """
    Initialize communication channel.

    Args:
```

**Public Methods:**

- `def serialize_weights(self, weights`
- `def deserialize_weights(self, serialized`
- `def create_message(`
- `def parse_message(self, message_data`
- `def send_model_download_request(self, client_id`
- `def send_model_download_response(`
- `def send_update_submission(`
- `def send_round_start_notification(`
- `def get_message_size_mb(self, message`

---

### `ClientConfig`

**File:** `fl_client.py`

```python
class ClientConfig:
```

**Description:**
```
"""
Configuration for FL client.

Attributes:
    client_id: Unique identifier for this client
    organization: Organization name
    coordinator_url: URL of the FL coordinator server
    local_data_path: Path to local training data
    use_gpu: Whether to use GPU for training
    max_memory_mb: Maximum memory usage (MB)
    apply_dp_locally: Whether to apply DP before sending update
    dp_epsilon: Privacy budget for local DP
    dp_delta: Failure probability for local DP
    dp_clip_norm: Gradient clipping norm
"""
```

**Public Methods:**


---

### `FLClient`

**File:** `fl_client.py`

```python
class FLClient:
```

**Description:**
```
"""
Federated learning client for on-premise training.

The client:
1. Fetches global model from coordinator
2. Trains model on local data (data never leaves premises)
3. Computes update (gradients or weight difference)
4. Optionally applies differential privacy
5. Sends update to coordinator
"""

def __init__(self, config: ClientConfig, model_adapter: Any):
    """
    Initialize FL client.

    Args:
```

**Public Methods:**

- `def fetch_global_model(self, round_id`
- `def train_local_model(`
- `def compute_update(`
- `def send_update(self, update`
- `def participate_in_round(`
- `def get_client_info(self) -> ClientInfo`
- `def update_client_info(self, total_samples`

---

### `CoordinatorConfig`

**File:** `fl_coordinator.py`

```python
class CoordinatorConfig:
```

**Description:**
```
"""
Configuration for FL coordinator.

Attributes:
    fl_config: Federated learning configuration
    max_rounds: Maximum number of training rounds
    convergence_threshold: Accuracy improvement threshold for convergence
    min_improvement_rounds: Minimum rounds without improvement to stop
    evaluation_frequency: Evaluate global model every N rounds
    auto_save: Whether to automatically save models
    save_directory: Directory to save models
"""

fl_config: FLConfig
max_rounds: int = 100
convergence_threshold: float = 0.001
```

**Public Methods:**


---

### `FLCoordinator`

**File:** `fl_coordinator.py`

```python
class FLCoordinator:
```

**Description:**
```
"""
Central coordinator for federated learning.

Manages the entire federated learning lifecycle:
1. Client registration and selection
2. Round initialization
3. Update collection and aggregation
4. Global model distribution
5. Convergence monitoring
"""

def __init__(self, config: CoordinatorConfig):
    """
    Initialize FL coordinator.

    Args:
```

**Public Methods:**

- `def register_client(self, client_info`
- `def unregister_client(self, client_id`
- `def set_global_model(self, weights`
- `def get_global_model(self) -> dict[str, np.ndarray] | None`
- `def start_round(self) -> FLRound`
- `def receive_update(self, update`
- `def aggregate_updates(self) -> AggregationResult`
- `def complete_round(self) -> FLRound`
- `def evaluate_global_model(self, test_data`
- `def has_converged(self) -> bool`
- `def should_stop(self) -> bool`
- `def get_metrics(self) -> FLMetrics`
- `def get_round_status(self) -> dict[str, Any] | None`

---

### `BaseModelAdapter`

**File:** `model_adapters.py`

```python
class BaseModelAdapter(ABC):
```

**Description:**
```
"""
Base class for model adapters.

All model adapters must implement this interface to be compatible
with the federated learning framework.
"""

def __init__(self, model_type: ModelType):
    """
    Initialize model adapter.

    Args:
        model_type: Type of model
    """
    self.model_type = model_type
    self.model = None
```

**Public Methods:**

- `def get_weights(self) -> dict[str, np.ndarray]`
- `def set_weights(self, weights`
- `def train_epochs(`
- `def evaluate(self, test_data`
- `def get_model_info(self) -> dict[str, Any]`

---

### `ThreatClassifierAdapter`

**File:** `model_adapters.py`

```python
class ThreatClassifierAdapter(BaseModelAdapter):
```

**Description:**
```
"""
Adapter for narrative_manipulation_filter threat classifier.

This adapter interfaces with the threat classification model used
for detecting manipulative narratives, misinformation, and threats.

Model Architecture (Simulated):
- Embedding layer: 10000 vocab -> 128 dim
- LSTM layer: 128 -> 64
- Dense layer: 64 -> 32
- Output layer: 32 -> 4 (threat categories)
"""

def __init__(self):
    """Initialize threat classifier adapter."""
    super().__init__(ModelType.THREAT_CLASSIFIER)
```

**Public Methods:**

- `def get_weights(self) -> dict[str, np.ndarray]`
- `def set_weights(self, weights`
- `def train_epochs(`
- `def evaluate(self, test_data`

---

### `MalwareDetectorAdapter`

**File:** `model_adapters.py`

```python
class MalwareDetectorAdapter(BaseModelAdapter):
```

**Description:**
```
"""
Adapter for immunis_macrophage_service malware detector.

This adapter interfaces with the malware detection model used by
the Immunis Macrophage service for identifying malicious files.

Model Architecture (Simulated):
- Input layer: 2048 features (file characteristics)
- Hidden layer 1: 2048 -> 512
- Hidden layer 2: 512 -> 128
- Hidden layer 3: 128 -> 32
- Output layer: 32 -> 2 (benign/malware)
"""

def __init__(self):
    """Initialize malware detector adapter."""
```

**Public Methods:**

- `def get_weights(self) -> dict[str, np.ndarray]`
- `def set_weights(self, weights`
- `def train_epochs(`
- `def evaluate(self, test_data`

---

### `RestrictedUnpickler`

**File:** `storage.py`

```python
class RestrictedUnpickler(pickle.Unpickler):
```

**Description:**
```
"""
Restricted pickle unpickler that only allows safe classes.

Prevents arbitrary code execution by whitelisting only specific
classes needed for model weights (numpy arrays, basic Python types).

Security: Protects against pickle deserialization attacks (CWE-502).
"""

# Whitelist of allowed modules and classes
ALLOWED_MODULES = {
    "numpy",
    "numpy.core.multiarray",
    "numpy.core.numeric",
    "numpy.core._multiarray_umath",
    "numpy._core.multiarray",  # Newer numpy versions use _core
```

**Public Methods:**

- `def find_class(self, module, name)`

---

### `ModelVersion`

**File:** `storage.py`

```python
class ModelVersion:
```

**Description:**
```
"""
Model version metadata.

Attributes:
    version_id: Version identifier
    model_type: Type of model
    round_id: Round that produced this version
    timestamp: When version was created
    accuracy: Model accuracy on test set
    total_parameters: Total number of parameters
    file_path: Path to saved model file
    metadata: Additional metadata
"""

version_id: int
model_type: ModelType
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `FLModelRegistry`

**File:** `storage.py`

```python
class FLModelRegistry:
```

**Description:**
```
"""
Registry for storing and retrieving FL model versions.

Maintains history of all global model versions produced during
federated learning, enabling:
- Model rollback
- Performance tracking
- Best model selection
- Reproducibility
"""

def __init__(self, storage_dir: str | None = None):
    """
    Initialize model registry.

    Args:
```

**Public Methods:**

- `def save_global_model(`
- `def load_global_model(self, version_id`
- `def get_best_model(self) -> dict[str, np.ndarray] | None`
- `def get_latest_model(self) -> dict[str, np.ndarray] | None`
- `def list_versions(self, limit`
- `def get_version_info(self, version_id`
- `def delete_version(self, version_id`

---

### `FLRoundHistory`

**File:** `storage.py`

```python
class FLRoundHistory:
```

**Description:**
```
"""
History of federated learning rounds.

Tracks all training rounds for analysis, debugging, and
convergence monitoring.
"""

def __init__(self, storage_dir: str | None = None):
    """
    Initialize round history.

    Args:
        storage_dir: Directory to store round data.
                    If None, uses FL_ROUNDS_DIR env var or creates secure temp dir.
    """
    if storage_dir is None:
```

**Public Methods:**

- `def save_round(self, round_obj`
- `def get_round(self, round_id`
- `def get_round_stats(self) -> dict[str, Any]`
- `def get_convergence_data(self) -> dict[str, list[float]]`
- `def plot_convergence(self, metric_name`

---

### `TestBaseClasses`

**File:** `test_federated_learning.py`

```python
class TestBaseClasses:
```

**Description:**
```
"""Tests for base classes and data structures."""

def test_fl_config_validation(self):
    """Test FL configuration validation."""
    # Valid config
    config = FLConfig(
        model_type=ModelType.THREAT_CLASSIFIER,
        min_clients=3,
        local_epochs=5,
    )
    assert config.min_clients == 3

    # Invalid: min_clients < 1
    with pytest.raises(ValueError):
        FLConfig(model_type=ModelType.THREAT_CLASSIFIER, min_clients=0)
```

**Public Methods:**

- `def test_fl_config_validation(self)`
- `def test_model_update_creation(self, sample_weights)`
- `def test_client_info(self)`
- `def test_fl_round_metrics(self, sample_updates)`

---

### `TestAggregation`

**File:** `test_federated_learning.py`

```python
class TestAggregation:
```

**Description:**
```
"""Tests for aggregation algorithms."""

def test_fedavg_aggregation(self, sample_updates):
    """Test FedAvg aggregation."""
    aggregator = FedAvgAggregator()
    result = aggregator.aggregate(sample_updates)

    assert result.num_clients == 3
    assert result.total_samples == 600
    assert result.strategy == AggregationStrategy.FEDAVG
    assert len(result.aggregated_weights) == len(sample_updates[0].weights)

def test_fedavg_weighted_average(self):
    """Test that FedAvg correctly weights by sample count."""
    # Create updates with different sample counts
    weights_a = {"layer": np.array([1.0, 1.0]).astype(np.float32)}
```

**Public Methods:**

- `def test_fedavg_aggregation(self, sample_updates)`
- `def test_fedavg_weighted_average(self)`
- `def test_secure_aggregation(self, sample_updates)`
- `def test_dp_aggregation(self, sample_updates)`

---

### `TestFLCoordinator`

**File:** `test_federated_learning.py`

```python
class TestFLCoordinator:
```

**Description:**
```
"""Tests for FL coordinator."""

def test_coordinator_initialization(self, fl_config):
    """Test coordinator initialization."""
    config = CoordinatorConfig(fl_config=fl_config)
    coordinator = FLCoordinator(config)

    assert coordinator.global_model_weights is None
    assert len(coordinator.registered_clients) == 0
    assert coordinator.metrics.total_rounds == 0

def test_client_registration(self, fl_config):
    """Test client registration."""
    config = CoordinatorConfig(fl_config=fl_config)
    coordinator = FLCoordinator(config)
```

**Public Methods:**

- `def test_coordinator_initialization(self, fl_config)`
- `def test_client_registration(self, fl_config)`
- `def test_start_round(self, fl_config, sample_weights)`
- `def test_receive_and_aggregate(self, fl_config, sample_weights, sample_updates)`

---

### `TestFLClient`

**File:** `test_federated_learning.py`

```python
class TestFLClient:
```

**Description:**
```
"""Tests for FL client."""

def test_client_initialization(self):
    """Test client initialization."""
    config = ClientConfig(
        client_id="client_1",
        organization="Org1",
        coordinator_url="http://localhost:8000",
    )
    adapter = ThreatClassifierAdapter()
    client = FLClient(config, adapter)

    assert client.config.client_id == "client_1"
    assert client.client_info.organization == "Org1"

def test_fetch_global_model(self, sample_weights):
```

**Public Methods:**

- `def test_client_initialization(self)`
- `def test_fetch_global_model(self, sample_weights)`
- `def test_compute_update(self, sample_weights)`

---

### `TestModelAdapters`

**File:** `test_federated_learning.py`

```python
class TestModelAdapters:
```

**Description:**
```
"""Tests for model adapters."""

def test_threat_classifier_adapter(self):
    """Test threat classifier adapter."""
    adapter = ThreatClassifierAdapter()

    # Get weights
    weights = adapter.get_weights()
    assert len(weights) == 7  # 7 layers
    assert "embedding" in weights

    # Set weights
    new_weights = {k: v * 2 for k, v in weights.items()}
    adapter.set_weights(new_weights)

    # Verify
```

**Public Methods:**

- `def test_threat_classifier_adapter(self)`
- `def test_malware_detector_adapter(self)`
- `def test_create_model_adapter_factory(self)`

---

### `TestCommunication`

**File:** `test_federated_learning.py`

```python
class TestCommunication:
```

**Description:**
```
"""Tests for communication layer."""

def test_weight_serialization(self, sample_weights):
    """Test weight serialization and deserialization."""
    channel = FLCommunicationChannel()

    # Serialize
    serialized = channel.serialize_weights(sample_weights)

    assert len(serialized) == len(sample_weights)
    for layer_name in sample_weights:
        assert "data" in serialized[layer_name]
        assert "shape" in serialized[layer_name]
        assert "dtype" in serialized[layer_name]

    # Deserialize
```

**Public Methods:**

- `def test_weight_serialization(self, sample_weights)`
- `def test_message_creation(self)`
- `def test_message_parsing(self)`

---

### `TestStorage`

**File:** `test_federated_learning.py`

```python
class TestStorage:
```

**Description:**
```
"""Tests for storage and persistence."""

def test_model_registry(self, sample_weights):
    """Test model registry save/load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = FLModelRegistry(storage_dir=tmpdir)

        # Save model
        version = registry.save_global_model(
            version_id=1,
            model_type=ModelType.THREAT_CLASSIFIER,
            round_id=1,
            weights=sample_weights,
            accuracy=0.88,
        )
```

**Public Methods:**

- `def test_model_registry(self, sample_weights)`
- `def test_round_history(self, fl_config, sample_updates)`

---

### `TestIntegration`

**File:** `test_federated_learning.py`

```python
class TestIntegration:
```

**Description:**
```
"""End-to-end integration tests."""

def test_complete_fl_round(self, fl_config, sample_weights):
    """Test complete FL round with coordinator and clients."""
    # Initialize coordinator
    config = CoordinatorConfig(fl_config=fl_config)
    coordinator = FLCoordinator(config)
    coordinator.set_global_model(sample_weights)

    # Create clients
    clients = []
    for i in range(3):
        client_config = ClientConfig(
            client_id=f"client_{i}",
            organization=f"Org{i}",
            coordinator_url="http://localhost:8000",
```

**Public Methods:**

- `def test_complete_fl_round(self, fl_config, sample_weights)`

---

### `GeminiConfig`

**File:** `gemini_client.py`

```python
class GeminiConfig:
```

**Description:**
```
"""Configuração do Gemini"""

api_key: str
model: str = "gemini-1.5-flash"  # Modelo sem quota limite
temperature: float = 0.7
max_tokens: int = 4096
timeout: int = 60


class GeminiClient:
"""
Cliente para Google Gemini API

Suporta:
- Text generation
- Function calling (tool use)
```

**Public Methods:**


---

### `GeminiClient`

**File:** `gemini_client.py`

```python
class GeminiClient:
```

**Description:**
```
"""
Cliente para Google Gemini API

Suporta:
- Text generation
- Function calling (tool use)
- Streaming (opcional)
- Embeddings
"""

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

def __init__(self, config: GeminiConfig):
    self.config = config
    self.api_key = config.api_key
    self.model = config.model
```

**Public Methods:**


---

### `TestSuiteResult`

**File:** `generate_validation_report.py`

```python
class TestSuiteResult:
```

**Description:**
```
"""Result from a test suite execution."""

name: str
passed: bool
output: str
exit_code: int
duration: float


class ValidationReportGenerator:
"""
Generates comprehensive validation report.

Runs all test suites and consolidates results into markdown report.
"""
```

**Public Methods:**


---

### `ValidationReportGenerator`

**File:** `generate_validation_report.py`

```python
class ValidationReportGenerator:
```

**Description:**
```
"""
Generates comprehensive validation report.

Runs all test suites and consolidates results into markdown report.
"""

def __init__(self):
    """Initialize report generator."""
    self.results: list[TestSuiteResult] = []
    self.start_time = time.time()

async def run_test_suite(self, name: str, script: str) -> TestSuiteResult:
    """
    Run a test suite script.

    Args:
```

**Public Methods:**

- `def generate_markdown_report(self) -> str`

---

### `AuditLogger`

**File:** `audit_infrastructure.py`

```python
class AuditLogger:
```

**Description:**
```
"""
PostgreSQL-based audit logger for governance activities.

Provides:
- Tamper-evident audit trails (SHA-256 checksums)
- GDPR-compliant retention (7 years)
- Fast querying with indexed access
- Export capabilities for auditors
"""

def __init__(self, config: GovernanceConfig):
    """Initialize audit logger."""
    self.config = config
    self.connection_params = {
        "host": config.db_host,
        "port": config.db_port,
```

**Public Methods:**

- `def get_connection(self) -> Generator`
- `def initialize_schema(self)`
- `def log(`
- `def query_logs(`
- `def apply_retention_policy(self) -> int`
- `def verify_integrity(self, log_id`
- `def export_for_auditor(`
- `def get_statistics(self) -> dict[str, Any]`

---

### `PolicyType`

**File:** `base.py`

```python
class PolicyType(str, Enum):
```

**Description:**
```
"""Types of ethical policies."""

ETHICAL_USE = "ethical_use"
RED_TEAMING = "red_teaming"
DATA_PRIVACY = "data_privacy"
INCIDENT_RESPONSE = "incident_response"
WHISTLEBLOWER = "whistleblower"


class PolicySeverity(str, Enum):
"""Severity levels for policy violations."""

INFO = "info"
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
```

**Public Methods:**


---

### `PolicySeverity`

**File:** `base.py`

```python
class PolicySeverity(str, Enum):
```

**Description:**
```
"""Severity levels for policy violations."""

INFO = "info"
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"


class ERBMemberRole(str, Enum):
"""Roles for Ethics Review Board members."""

CHAIR = "chair"
VICE_CHAIR = "vice_chair"
TECHNICAL_MEMBER = "technical_member"
LEGAL_MEMBER = "legal_member"
```

**Public Methods:**


---

### `ERBMemberRole`

**File:** `base.py`

```python
class ERBMemberRole(str, Enum):
```

**Description:**
```
"""Roles for Ethics Review Board members."""

CHAIR = "chair"
VICE_CHAIR = "vice_chair"
TECHNICAL_MEMBER = "technical_member"
LEGAL_MEMBER = "legal_member"
EXTERNAL_ADVISOR = "external_advisor"
OBSERVER = "observer"


class DecisionType(str, Enum):
"""Types of ERB decisions."""

APPROVED = "approved"
REJECTED = "rejected"
DEFERRED = "deferred"
```

**Public Methods:**


---

### `DecisionType`

**File:** `base.py`

```python
class DecisionType(str, Enum):
```

**Description:**
```
"""Types of ERB decisions."""

APPROVED = "approved"
REJECTED = "rejected"
DEFERRED = "deferred"
CONDITIONAL_APPROVED = "conditional_approved"
REQUIRES_REVISION = "requires_revision"


class AuditLogLevel(str, Enum):
"""Audit log levels."""

DEBUG = "debug"
INFO = "info"
WARNING = "warning"
ERROR = "error"
```

**Public Methods:**


---

### `AuditLogLevel`

**File:** `base.py`

```python
class AuditLogLevel(str, Enum):
```

**Description:**
```
"""Audit log levels."""

DEBUG = "debug"
INFO = "info"
WARNING = "warning"
ERROR = "error"
CRITICAL = "critical"


class GovernanceAction(str, Enum):
"""Governance-related actions for audit trail."""

POLICY_CREATED = "policy_created"
POLICY_UPDATED = "policy_updated"
POLICY_VIOLATED = "policy_violated"
ERB_MEETING_SCHEDULED = "erb_meeting_scheduled"
```

**Public Methods:**


---

### `GovernanceAction`

**File:** `base.py`

```python
class GovernanceAction(str, Enum):
```

**Description:**
```
"""Governance-related actions for audit trail."""

POLICY_CREATED = "policy_created"
POLICY_UPDATED = "policy_updated"
POLICY_VIOLATED = "policy_violated"
ERB_MEETING_SCHEDULED = "erb_meeting_scheduled"
ERB_DECISION_MADE = "erb_decision_made"
ERB_MEMBER_ADDED = "erb_member_added"
ERB_MEMBER_REMOVED = "erb_member_removed"
AUDIT_LOG_CREATED = "audit_log_created"
INCIDENT_REPORTED = "incident_reported"
WHISTLEBLOWER_REPORT = "whistleblower_report"


# ============================================================================
# CONFIGURATION
```

**Public Methods:**


---

### `GovernanceConfig`

**File:** `base.py`

```python
class GovernanceConfig:
```

**Description:**
```
"""Configuration for governance module."""

# ERB Configuration
erb_meeting_frequency_days: int = 30  # Monthly meetings
erb_quorum_percentage: float = 0.6  # 60% quorum required
erb_decision_threshold: float = 0.75  # 75% approval required

# Policy Configuration
policy_review_frequency_days: int = 365  # Annual policy review
auto_enforce_policies: bool = True
policy_violation_alert_threshold: PolicySeverity = PolicySeverity.MEDIUM

# Audit Configuration
audit_retention_days: int = 2555  # 7 years (GDPR requirement)
audit_log_level: AuditLogLevel = AuditLogLevel.INFO
enable_blockchain_audit: bool = False  # Optional Phase 1
```

**Public Methods:**


---

### `ERBMember`

**File:** `base.py`

```python
class ERBMember:
```

**Description:**
```
"""Ethics Review Board member."""

member_id: str = field(default_factory=lambda: str(uuid4()))
name: str = ""
email: str = ""
role: ERBMemberRole = ERBMemberRole.TECHNICAL_MEMBER
organization: str = ""  # Internal or external organization
expertise: list[str] = field(default_factory=list)  # e.g., ["AI ethics", "Legal"]
is_internal: bool = True
is_active: bool = True
appointed_date: datetime = field(default_factory=datetime.utcnow)
term_end_date: datetime | None = None
voting_rights: bool = True
metadata: dict[str, Any] = field(default_factory=dict)

def is_voting_member(self) -> bool:
```

**Public Methods:**

- `def is_voting_member(self) -> bool`
- `def to_dict(self) -> dict[str, Any]`

---

### `ERBMeeting`

**File:** `base.py`

```python
class ERBMeeting:
```

**Description:**
```
"""Ethics Review Board meeting."""

meeting_id: str = field(default_factory=lambda: str(uuid4()))
scheduled_date: datetime = field(default_factory=datetime.utcnow)
actual_date: datetime | None = None
duration_minutes: int = 120
location: str = "Virtual"  # Virtual or physical location
agenda: list[str] = field(default_factory=list)
attendees: list[str] = field(default_factory=list)  # member_ids
absentees: list[str] = field(default_factory=list)  # member_ids
minutes: str = ""  # Meeting minutes
decisions: list[str] = field(default_factory=list)  # decision_ids
quorum_met: bool = False
status: str = "scheduled"  # scheduled, completed, cancelled
metadata: dict[str, Any] = field(default_factory=dict)
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ERBDecision`

**File:** `base.py`

```python
class ERBDecision:
```

**Description:**
```
"""Ethics Review Board decision."""

decision_id: str = field(default_factory=lambda: str(uuid4()))
meeting_id: str = ""
title: str = ""
description: str = ""
decision_type: DecisionType = DecisionType.APPROVED
votes_for: int = 0
votes_against: int = 0
votes_abstain: int = 0
rationale: str = ""
conditions: list[str] = field(default_factory=list)  # If conditional approval
follow_up_required: bool = False
follow_up_deadline: datetime | None = None
created_date: datetime = field(default_factory=datetime.utcnow)
created_by: str = ""  # member_id of chair
```

**Public Methods:**

- `def is_approved(self) -> bool`
- `def approval_percentage(self) -> float`
- `def to_dict(self) -> dict[str, Any]`

---

### `Policy`

**File:** `base.py`

```python
class Policy:
```

**Description:**
```
"""Ethical policy definition."""

policy_id: str = field(default_factory=lambda: str(uuid4()))
policy_type: PolicyType = PolicyType.ETHICAL_USE
version: str = "1.0"
title: str = ""
description: str = ""
rules: list[str] = field(default_factory=list)
scope: str = "all"  # all, maximus, immunis, rte, specific_service
enforcement_level: PolicySeverity = PolicySeverity.MEDIUM
auto_enforce: bool = True
created_date: datetime = field(default_factory=datetime.utcnow)
last_review_date: datetime | None = None
next_review_date: datetime | None = None
approved_by_erb: bool = False
erb_decision_id: str | None = None
```

**Public Methods:**

- `def is_due_for_review(self) -> bool`
- `def days_until_review(self) -> int`
- `def to_dict(self) -> dict[str, Any]`

---

### `PolicyViolation`

**File:** `base.py`

```python
class PolicyViolation:
```

**Description:**
```
"""Policy violation record."""

violation_id: str = field(default_factory=lambda: str(uuid4()))
policy_id: str = ""
policy_type: PolicyType = PolicyType.ETHICAL_USE
severity: PolicySeverity = PolicySeverity.MEDIUM
title: str = ""
description: str = ""
violated_rule: str = ""
detection_method: str = "automated"  # automated, manual, whistleblower
detected_by: str = "system"  # system, user_id, or "anonymous"
detected_date: datetime = field(default_factory=datetime.utcnow)
affected_system: str = ""  # maximus, immunis, rte, or specific service
affected_users: list[str] = field(default_factory=list)
context: dict[str, Any] = field(default_factory=dict)
remediation_required: bool = True
```

**Public Methods:**

- `def is_overdue(self) -> bool`
- `def days_until_deadline(self) -> int`
- `def to_dict(self) -> dict[str, Any]`

---

### `AuditLog`

**File:** `base.py`

```python
class AuditLog:
```

**Description:**
```
"""Audit log entry for governance actions."""

log_id: str = field(default_factory=lambda: str(uuid4()))
timestamp: datetime = field(default_factory=datetime.utcnow)
action: GovernanceAction = GovernanceAction.AUDIT_LOG_CREATED
log_level: AuditLogLevel = AuditLogLevel.INFO
actor: str = "system"  # User ID or "system"
target_entity_type: str = ""  # policy, erb_member, meeting, decision
target_entity_id: str = ""
description: str = ""
details: dict[str, Any] = field(default_factory=dict)
ip_address: str | None = None
user_agent: str | None = None
session_id: str | None = None
correlation_id: str | None = None  # For tracking related events
metadata: dict[str, Any] = field(default_factory=dict)
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `WhistleblowerReport`

**File:** `base.py`

```python
class WhistleblowerReport:
```

**Description:**
```
"""Whistleblower protection report."""

report_id: str = field(default_factory=lambda: str(uuid4()))
submission_date: datetime = field(default_factory=datetime.utcnow)
reporter_id: str | None = None  # None if anonymous
is_anonymous: bool = True
title: str = ""
description: str = ""
alleged_violation_type: PolicyType = PolicyType.ETHICAL_USE
severity: PolicySeverity = PolicySeverity.MEDIUM
affected_systems: list[str] = field(default_factory=list)
evidence: list[str] = field(default_factory=list)  # File paths or references
status: str = "submitted"  # submitted, under_review, investigated, resolved, dismissed
assigned_investigator: str | None = None
investigation_notes: str = ""
resolution: str = ""
```

**Public Methods:**

- `def is_under_investigation(self) -> bool`
- `def is_resolved(self) -> bool`
- `def to_dict(self) -> dict[str, Any]`

---

### `GovernanceResult`

**File:** `base.py`

```python
class GovernanceResult:
```

**Description:**
```
"""Result of governance operation."""

success: bool = True
message: str = ""
entity_id: str | None = None  # ID of created/updated entity
entity_type: str = ""  # policy, member, meeting, etc.
warnings: list[str] = field(default_factory=list)
errors: list[str] = field(default_factory=list)
metadata: dict[str, Any] = field(default_factory=dict)

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary."""
    return {
        "success": self.success,
        "message": self.message,
        "entity_id": self.entity_id,
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `PolicyEnforcementResult`

**File:** `base.py`

```python
class PolicyEnforcementResult:
```

**Description:**
```
"""Result of policy enforcement check."""

is_compliant: bool = True
policy_id: str = ""
policy_type: PolicyType = PolicyType.ETHICAL_USE
checked_rules: int = 0
passed_rules: int = 0
failed_rules: int = 0
violations: list[PolicyViolation] = field(default_factory=list)
warnings: list[str] = field(default_factory=list)
timestamp: datetime = field(default_factory=datetime.utcnow)
metadata: dict[str, Any] = field(default_factory=dict)

def compliance_percentage(self) -> float:
    """Calculate compliance percentage."""
    if self.checked_rules == 0:
```

**Public Methods:**

- `def compliance_percentage(self) -> float`
- `def to_dict(self) -> dict[str, Any]`

---

### `ERBManager`

**File:** `ethics_review_board.py`

```python
class ERBManager:
```

**Description:**
```
"""
Ethics Review Board Manager.

Manages ERB members, meetings, and decision-making processes.
Ensures quorum requirements, voting procedures, and governance compliance.

Performance Target: <50ms for most operations
"""

def __init__(self, config: GovernanceConfig):
    """Initialize ERB Manager."""
    self.config = config
    self.members: dict[str, ERBMember] = {}
    self.meetings: dict[str, ERBMeeting] = {}
    self.decisions: dict[str, ERBDecision] = {}
```

**Public Methods:**

- `def add_member(`
- `def remove_member(self, member_id`
- `def get_active_members(self) -> list[ERBMember]`
- `def get_voting_members(self) -> list[ERBMember]`
- `def get_member_by_role(self, role`
- `def get_chair(self) -> ERBMember | None`
- `def schedule_meeting(`
- `def record_attendance(`
- `def add_meeting_minutes(`
- `def record_decision(`
- `def get_decision(self, decision_id`
- `def get_decisions_by_meeting(self, meeting_id`
- `def get_decisions_by_policy(self, policy_type`
- `def get_pending_follow_ups(self) -> list[ERBDecision]`
- `def get_overdue_follow_ups(self) -> list[ERBDecision]`
- `def check_quorum(self, attendee_ids`
- `def calculate_approval(self, votes_for`
- `def get_stats(self) -> dict[str, int]`
- `def get_member_participation(self) -> dict[str, dict[str, int]]`
- `def generate_summary_report(self) -> dict[str, Any]`

---

### `DecisionStatus`

**File:** `governance_engine.py`

```python
class DecisionStatus(str, Enum):
```

**Description:**
```
"""Status of a governance decision."""

PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"
ESCALATED = "ESCALATED"
EXPIRED = "EXPIRED"


@dataclass
class RiskAssessment:
"""Risk assessment for a decision."""

score: float = 0.0  # 0.0 to 1.0
level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
factors: list[str] = field(default_factory=list)
```

**Public Methods:**


---

### `RiskAssessment`

**File:** `governance_engine.py`

```python
class RiskAssessment:
```

**Description:**
```
"""Risk assessment for a decision."""

score: float = 0.0  # 0.0 to 1.0
level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
factors: list[str] = field(default_factory=list)


@dataclass
class Decision:
"""
HITL Decision requiring operator approval.

Represents an action that requires human oversight before execution.
"""

decision_id: str = field(default_factory=lambda: str(uuid4()))
```

**Public Methods:**


---

### `Decision`

**File:** `governance_engine.py`

```python
class Decision:
```

**Description:**
```
"""
HITL Decision requiring operator approval.

Represents an action that requires human oversight before execution.
"""

decision_id: str = field(default_factory=lambda: str(uuid4()))
operation_type: str = ""  # e.g., "EXPLOIT_EXECUTION", "LATERAL_MOVEMENT"
context: dict[str, Any] = field(default_factory=dict)
risk: RiskAssessment = field(default_factory=RiskAssessment)
status: DecisionStatus = DecisionStatus.PENDING
priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
created_at: datetime = field(default_factory=datetime.utcnow)
expires_at: datetime | None = None
sla_seconds: int = 300  # 5 minutes default SLA
operator_id: str | None = None
```

**Public Methods:**

- `def is_expired(self) -> bool`
- `def time_remaining(self) -> int`

---

### `GovernanceEngine`

**File:** `governance_engine.py`

```python
class GovernanceEngine:
```

**Description:**
```
"""
Governance Engine for HITL decision management.

⚠️ POC IMPLEMENTATION - For gRPC bridge validation only.
Production version will integrate with PolicyEngine and ERBManager.
"""

def __init__(self):
    """Initialize governance engine."""
    self.decisions: dict[str, Decision] = {}
    self.start_time = time.time()
    self._event_subscribers = []

    # Create some mock decisions for testing
    self._create_mock_decisions()
```

**Public Methods:**

- `def get_uptime(self) -> float`
- `def get_pending_decisions(`
- `def get_decision(self, decision_id`
- `def create_decision(`
- `def update_decision_status(`
- `def get_metrics(self) -> dict[str, Any]`
- `def subscribe_decision_events(self) -> Generator[dict[str, Any], None, None]`
- `def subscribe_events(self) -> Generator[dict[str, Any], None, None]`

---

### `ArticleIIGuardian`

**File:** `article_ii_guardian.py`

```python
class ArticleIIGuardian(GuardianAgent):
```

**Description:**
```
"""
Guardian that enforces Article II: The Sovereign Quality Standard.

Monitors codebase for:
- Mock implementations
- Placeholder code
- TODO/FIXME comments
- Skipped tests
- Technical debt markers
- Incomplete implementations
"""

def __init__(self):
    """Initialize Article II Guardian."""
    super().__init__(
        guardian_id="guardian-article-ii",
```

**Public Methods:**

- `def get_monitored_systems(self) -> list[str]`

---

### `ArticleIIIGuardian`

**File:** `article_iii_guardian.py`

```python
class ArticleIIIGuardian(GuardianAgent):
```

**Description:**
```
"""
Guardian that enforces Article III: The Zero Trust Principle.

Monitors for:
- Unvalidated AI-generated code
- Missing authentication/authorization
- Insufficient input validation
- Trust assumptions in code
- Missing audit trails
- Privilege escalation risks
"""

def __init__(self, monitored_paths: list[str] | None = None, api_paths: list[str] | None = None):
    """Initialize Article III Guardian.

    Args:
```

**Public Methods:**

- `def get_monitored_systems(self) -> list[str]`

---

### `ArticleIVGuardian`

**File:** `article_iv_guardian.py`

```python
class ArticleIVGuardian(GuardianAgent):
```

**Description:**
```
"""
Guardian that enforces Article IV: Deliberate Antifragility Principle.

Monitors for:
- Lack of chaos engineering tests
- Missing failure recovery mechanisms
- Absence of circuit breakers and fallbacks
- Untested edge cases
- Experimental features without quarantine
- Missing resilience patterns
"""

def __init__(self, test_paths: list[str] | None = None, service_paths: list[str] | None = None):
    """Initialize Article IV Guardian.

    Args:
```

**Public Methods:**

- `def get_monitored_systems(self) -> list[str]`

---

### `ArticleVGuardian`

**File:** `article_v_guardian.py`

```python
class ArticleVGuardian(GuardianAgent):
```

**Description:**
```
"""
Guardian that enforces Article V: Prior Legislation Principle.

Monitors for:
- Autonomous capabilities without governance
- Missing responsibility chains
- Absence of HITL controls for critical operations
- Unaudited autonomous workflows
- Missing kill switches and safety mechanisms
- Violations of Two-Man Rule for critical actions
"""

def __init__(
    self,
    autonomous_paths: list[str] | None = None,
    powerful_paths: list[str] | None = None,
```

**Public Methods:**

- `def get_monitored_systems(self) -> list[str]`

---

### `GuardianPriority`

**File:** `base.py`

```python
class GuardianPriority(str, Enum):
```

**Description:**
```
"""Priority levels for Guardian interventions."""

CRITICAL = "CRITICAL"  # Immediate action required
HIGH = "HIGH"  # Urgent, within minutes
MEDIUM = "MEDIUM"  # Important, within hours
LOW = "LOW"  # Routine monitoring
INFO = "INFO"  # Informational only


class InterventionType(str, Enum):
"""Types of Guardian interventions."""

VETO = "VETO"  # Block an action completely
ALERT = "ALERT"  # Raise awareness but don't block
REMEDIATION = "REMEDIATION"  # Automatic fix applied
ESCALATION = "ESCALATION"  # Escalate to human oversight
```

**Public Methods:**


---

### `InterventionType`

**File:** `base.py`

```python
class InterventionType(str, Enum):
```

**Description:**
```
"""Types of Guardian interventions."""

VETO = "VETO"  # Block an action completely
ALERT = "ALERT"  # Raise awareness but don't block
REMEDIATION = "REMEDIATION"  # Automatic fix applied
ESCALATION = "ESCALATION"  # Escalate to human oversight
MONITORING = "MONITORING"  # Increase monitoring level


class ConstitutionalArticle(str, Enum):
"""Constitutional Articles that Guardians enforce."""

ARTICLE_I = "ARTICLE_I"  # Hybrid Development Cell
ARTICLE_II = "ARTICLE_II"  # Sovereign Quality Standard
ARTICLE_III = "ARTICLE_III"  # Zero Trust Principle
ARTICLE_IV = "ARTICLE_IV"  # Deliberate Antifragility
```

**Public Methods:**


---

### `ConstitutionalArticle`

**File:** `base.py`

```python
class ConstitutionalArticle(str, Enum):
```

**Description:**
```
"""Constitutional Articles that Guardians enforce."""

ARTICLE_I = "ARTICLE_I"  # Hybrid Development Cell
ARTICLE_II = "ARTICLE_II"  # Sovereign Quality Standard
ARTICLE_III = "ARTICLE_III"  # Zero Trust Principle
ARTICLE_IV = "ARTICLE_IV"  # Deliberate Antifragility
ARTICLE_V = "ARTICLE_V"  # Prior Legislation


# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class ConstitutionalViolation:
```

**Public Methods:**


---

### `ConstitutionalViolation`

**File:** `base.py`

```python
class ConstitutionalViolation:
```

**Description:**
```
"""Represents a detected violation of the Constitution."""

violation_id: str = field(default_factory=lambda: str(uuid4()))
article: ConstitutionalArticle = ConstitutionalArticle.ARTICLE_II
clause: str = ""  # e.g., "Cláusula 3.2"
rule: str = ""  # Specific rule violated
description: str = ""
severity: GuardianPriority = GuardianPriority.MEDIUM
detected_at: datetime = field(default_factory=datetime.utcnow)
context: dict[str, Any] = field(default_factory=dict)
evidence: list[str] = field(default_factory=list)
affected_systems: list[str] = field(default_factory=list)
recommended_action: str = ""
metadata: dict[str, Any] = field(default_factory=dict)

def to_dict(self) -> dict[str, Any]:
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def generate_hash(self) -> str`

---

### `VetoAction`

**File:** `base.py`

```python
class VetoAction:
```

**Description:**
```
"""Represents a veto action taken by a Guardian."""

veto_id: str = field(default_factory=lambda: str(uuid4()))
guardian_id: str = ""
target_action: str = ""  # What was vetoed
target_system: str = ""  # Which system/service
violation: ConstitutionalViolation | None = None
reason: str = ""
enacted_at: datetime = field(default_factory=datetime.utcnow)
expires_at: datetime | None = None  # Temporary vetos
override_allowed: bool = False  # Can be overridden by human
override_requirements: list[str] = field(default_factory=list)
metadata: dict[str, Any] = field(default_factory=dict)

def is_active(self) -> bool:
    """Check if veto is still active."""
```

**Public Methods:**

- `def is_active(self) -> bool`
- `def to_dict(self) -> dict[str, Any]`

---

### `GuardianIntervention`

**File:** `base.py`

```python
class GuardianIntervention:
```

**Description:**
```
"""Records an intervention taken by a Guardian."""

intervention_id: str = field(default_factory=lambda: str(uuid4()))
guardian_id: str = ""
intervention_type: InterventionType = InterventionType.ALERT
priority: GuardianPriority = GuardianPriority.MEDIUM
violation: ConstitutionalViolation | None = None
action_taken: str = ""
result: str = ""
success: bool = True
timestamp: datetime = field(default_factory=datetime.utcnow)
metadata: dict[str, Any] = field(default_factory=dict)

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary."""
    return {
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `GuardianDecision`

**File:** `base.py`

```python
class GuardianDecision:
```

**Description:**
```
"""Represents a decision made by a Guardian Agent."""

decision_id: str = field(default_factory=lambda: str(uuid4()))
guardian_id: str = ""
decision_type: str = ""  # e.g., "allow", "block", "escalate"
target: str = ""  # What the decision applies to
reasoning: str = ""  # Constitutional basis for decision
confidence: float = 0.0  # 0.0 to 1.0
requires_validation: bool = False
timestamp: datetime = field(default_factory=datetime.utcnow)
metadata: dict[str, Any] = field(default_factory=dict)

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary."""
    return {
        "decision_id": self.decision_id,
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `GuardianReport`

**File:** `base.py`

```python
class GuardianReport:
```

**Description:**
```
"""Periodic compliance report from Guardian Agents."""

report_id: str = field(default_factory=lambda: str(uuid4()))
guardian_id: str = ""
period_start: datetime = field(default_factory=datetime.utcnow)
period_end: datetime = field(default_factory=datetime.utcnow)
violations_detected: int = 0
interventions_made: int = 0
vetos_enacted: int = 0
compliance_score: float = 100.0  # 0-100 percentage
top_violations: list[str] = field(default_factory=list)
recommendations: list[str] = field(default_factory=list)
metrics: dict[str, Any] = field(default_factory=dict)
generated_at: datetime = field(default_factory=datetime.utcnow)

def to_dict(self) -> dict[str, Any]:
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `GuardianAgent`

**File:** `base.py`

```python
class GuardianAgent(ABC):
```

**Description:**
```
"""
Abstract base class for Constitutional Guardian Agents.

Each Guardian enforces specific Articles of the Vértice Constitution
through continuous monitoring, detection, and intervention.
"""

def __init__(
    self,
    guardian_id: str,
    article: ConstitutionalArticle,
    name: str,
    description: str,
):
    """Initialize Guardian Agent."""
    self.guardian_id = guardian_id
```

**Public Methods:**

- `def get_monitored_systems(self) -> list[str]`
- `def get_active_vetos(self) -> list[VetoAction]`
- `def generate_report(`
- `def register_violation_callback(`
- `def register_intervention_callback(`
- `def register_veto_callback(`
- `def is_active(self) -> bool`
- `def get_statistics(self) -> dict[str, Any]`

---

### `CoordinatorMetrics`

**File:** `coordinator.py`

```python
class CoordinatorMetrics:
```

**Description:**
```
"""Metrics for Guardian Coordinator performance."""

total_violations_detected: int = 0
violations_by_article: dict[str, int] = field(default_factory=dict)
violations_by_severity: dict[str, int] = field(default_factory=dict)
interventions_made: int = 0
vetos_enacted: int = 0
compliance_score: float = 100.0
last_updated: datetime = field(default_factory=datetime.utcnow)

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary."""
    return {
        "total_violations_detected": self.total_violations_detected,
        "violations_by_article": self.violations_by_article,
        "violations_by_severity": self.violations_by_severity,
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ConflictResolution`

**File:** `coordinator.py`

```python
class ConflictResolution:
```

**Description:**
```
"""Resolution for conflicts between Guardian decisions."""

conflict_id: str
guardian1_id: str
guardian2_id: str
violation1: ConstitutionalViolation
violation2: ConstitutionalViolation
resolution: str
rationale: str
timestamp: datetime = field(default_factory=datetime.utcnow)


class GuardianCoordinator:
"""
Central coordinator for all Guardian Agents.
```

**Public Methods:**


---

### `GuardianCoordinator`

**File:** `coordinator.py`

```python
class GuardianCoordinator:
```

**Description:**
```
"""
Central coordinator for all Guardian Agents.

Responsibilities:
- Start/stop all Guardians
- Aggregate and prioritize violations
- Resolve conflicts between Guardians
- Generate unified compliance reports
- Manage veto escalations
- Provide API for external systems
"""

def __init__(self, guardians: dict[str, GuardianAgent] | None = None):
    """Initialize Guardian Coordinator.

    Args:
```

**Public Methods:**

- `def get_status(self) -> dict[str, Any]`
- `def generate_compliance_report(`

---

### `TestArticleIIGuardianInit`

**File:** `test_article_ii_guardian.py`

```python
class TestArticleIIGuardianInit:
```

**Description:**
```
"""Test Article II Guardian initialization."""

def test_guardian_initialization(self, guardian):
    """Test guardian initializes with correct attributes."""
    assert guardian.guardian_id == "guardian-article-ii"
    assert guardian.article == ConstitutionalArticle.ARTICLE_II
    assert guardian.name == "Sovereign Quality Guardian"
    assert "Padrão Pagani" in guardian.description

def test_mock_patterns_configured(self, guardian):
    """Test mock detection patterns are configured."""
    assert len(guardian.mock_patterns) > 0
    assert r"\bmock\b" in guardian.mock_patterns
    assert r"\bMock\b" in guardian.mock_patterns
    assert r"\bfake\b" in guardian.mock_patterns
```

**Public Methods:**

- `def test_guardian_initialization(self, guardian)`
- `def test_mock_patterns_configured(self, guardian)`
- `def test_placeholder_patterns_configured(self, guardian)`
- `def test_test_skip_patterns_configured(self, guardian)`
- `def test_monitored_paths_configured(self, guardian)`
- `def test_excluded_paths_configured(self, guardian)`
- `def test_get_monitored_systems(self, guardian)`

---

### `TestFileChecking`

**File:** `test_article_ii_guardian.py`

```python
class TestFileChecking:
```

**Description:**
```
"""Test file scanning functionality."""

@pytest.mark.asyncio
async def test_check_file_detects_mock(self, guardian, temp_python_file):
    """Test _check_file detects mock implementations."""
    # Use actual code with Mock class (not in comment/string)
    temp_python_file.write_text("def foo():\n    return Mock(spec=Client)\n")

    violations = await guardian._check_file(temp_python_file)

    assert len(violations) > 0
    assert any("Mock implementation" in v.description for v in violations)

@pytest.mark.asyncio
async def test_check_file_detects_todo(self, guardian, temp_python_file):
    """Test _check_file detects TODO comments."""
```

**Public Methods:**


---

### `TestPatternDetection`

**File:** `test_article_ii_guardian.py`

```python
class TestPatternDetection:
```

**Description:**
```
"""Test pattern detection helpers."""

def test_is_comment_or_string_detects_comment(self, guardian):
    """Test _is_comment_or_string detects comment lines."""
    line = "# This is a mock comment"

    result = guardian._is_comment_or_string(line, "mock")

    assert result is True

def test_is_comment_or_string_detects_docstring(self, guardian):
    """Test _is_comment_or_string detects docstrings."""
    line = '"""This has mock in docstring"""'

    result = guardian._is_comment_or_string(line, "mock")
```

**Public Methods:**

- `def test_is_comment_or_string_detects_comment(self, guardian)`
- `def test_is_comment_or_string_detects_docstring(self, guardian)`
- `def test_is_comment_or_string_detects_string_literal(self, guardian)`
- `def test_is_comment_or_string_rejects_code(self, guardian)`
- `def test_has_valid_skip_reason_with_roadmap(self, guardian)`
- `def test_has_valid_skip_reason_with_future_dependency(self, guardian)`
- `def test_has_valid_skip_reason_no_reason(self, guardian)`

---

### `TestMonitoring`

**File:** `test_article_ii_guardian.py`

```python
class TestMonitoring:
```

**Description:**
```
"""Test monitoring functionality."""

@pytest.mark.asyncio
async def test_monitor_nonexistent_path(self, guardian):
    """Test monitor handles nonexistent paths gracefully."""
    guardian.monitored_paths = ["/nonexistent/path"]

    violations = await guardian.monitor()

    # Should not crash, may return empty or other violations
    assert isinstance(violations, list)

@pytest.mark.asyncio
async def test_monitor_skips_excluded_paths(self, guardian):
    """Test monitor skips excluded paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
```

**Public Methods:**


---

### `TestTestHealthChecking`

**File:** `test_article_ii_guardian.py`

```python
class TestTestHealthChecking:
```

**Description:**
```
"""Test test health checking."""

@pytest.mark.asyncio
async def test_check_test_health_success(self, guardian):
    """Test _check_test_health with successful test collection."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stderr="",
            stdout="collected 10 items"
        )

        violations = await guardian._check_test_health()

        assert len(violations) == 0
```

**Public Methods:**


---

### `TestGitStatusChecking`

**File:** `test_article_ii_guardian.py`

```python
class TestGitStatusChecking:
```

**Description:**
```
"""Test git status checking."""

@pytest.mark.asyncio
async def test_check_git_status_feature_branch(self, guardian):
    """Test _check_git_status ignores feature branches."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            stdout="feature/my-branch",
            stderr=""
        )

        violations = await guardian._check_git_status()

        # Should not check violations on feature branch
        assert len(violations) == 0
```

**Public Methods:**


---

### `TestDecisionMaking`

**File:** `test_article_ii_guardian.py`

```python
class TestDecisionMaking:
```

**Description:**
```
"""Test decision making logic."""

@pytest.mark.asyncio
async def test_analyze_violation_critical(self, guardian):
    """Test analyze_violation with CRITICAL severity."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_II,
        clause="Section 1",
        rule="Test rule",
        severity=GuardianPriority.CRITICAL
    )

    decision = await guardian.analyze_violation(violation)
```

**Public Methods:**


---

### `TestIntervention`

**File:** `test_article_ii_guardian.py`

```python
class TestIntervention:
```

**Description:**
```
"""Test intervention logic."""

@pytest.mark.asyncio
async def test_intervene_critical_veto(self, guardian):
    """Test intervene with CRITICAL violation creates VETO."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_II,
        severity=GuardianPriority.CRITICAL
    )

    intervention = await guardian.intervene(violation)

    assert intervention.intervention_type == InterventionType.VETO
    assert "Vetoed" in intervention.action_taken
```

**Public Methods:**


---

### `TestPullRequestScanning`

**File:** `test_article_ii_guardian.py`

```python
class TestPullRequestScanning:
```

**Description:**
```
"""Test pull request scanning."""

@pytest.mark.asyncio
async def test_scan_pull_request_detects_mock(self, guardian):
    """Test scan_pull_request detects mock in added lines."""
    pr_diff = """
+++ b/src/service.py
@@ -10,3 +10,4 @@
 def foo():
+    return Mock(spec=Client)
 return data
"""

    violations = await guardian.scan_pull_request(pr_diff)

    assert len(violations) > 0
```

**Public Methods:**


---

### `TestIntegration`

**File:** `test_article_ii_guardian.py`

```python
class TestIntegration:
```

**Description:**
```
"""Test complete workflows."""

@pytest.mark.asyncio
async def test_full_violation_detection_workflow(self, guardian, temp_python_file):
    """Test complete workflow from file scan to intervention."""
    # Create file with CRITICAL violation (NotImplementedError)
    temp_python_file.write_text("def foo():\n    raise NotImplementedError()\n")

    # Monitor
    violations = await guardian._check_file(temp_python_file)
    assert len(violations) > 0

    # Get the CRITICAL violation (NotImplementedError)
    critical_violation = next(
        (v for v in violations if v.severity == GuardianPriority.CRITICAL),
        violations[0]
```

**Public Methods:**


---

### `TestRemainingBranches`

**File:** `test_article_ii_guardian.py`

```python
class TestRemainingBranches:
```

**Description:**
```
"""Surgical tests to achieve 100.00% branch coverage."""

@pytest.mark.asyncio
async def test_ast_walk_raises_wrong_type(self, guardian, temp_python_file):
    """Cover branch 235->233: AST node is Raise but NOT NotImplementedError.

    This tests the FALSE path of the nested condition:
    if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name) and node.exc.func.id == "NotImplementedError"

    We need a Raise node that does NOT match these conditions.
    """
    # Code with a raise statement that's NOT NotImplementedError
    temp_python_file.write_text(
        "def foo():\n"
        "    raise ValueError('Some error')\n"  # This is a Raise node, but ValueError not NotImplementedError
    )
```

**Public Methods:**


---

### `TestArticleIIIGuardianInit`

**File:** `test_article_iii_guardian.py`

```python
class TestArticleIIIGuardianInit:
```

**Description:**
```
"""Test Article III Guardian initialization."""

def test_guardian_initialization(self, guardian):
    """Test guardian initializes with correct attributes."""
    assert guardian.guardian_id == "guardian-article-iii"
    assert guardian.article == ConstitutionalArticle.ARTICLE_III
    assert guardian.name == "Zero Trust Guardian"
    assert "Zero Trust Principle" in guardian.description

def test_unvalidated_artifacts_initialized(self, guardian):
    """Test unvalidated artifacts tracking is initialized."""
    assert isinstance(guardian.unvalidated_artifacts, dict)
    assert len(guardian.unvalidated_artifacts) == 0

def test_validation_history_initialized(self, guardian):
    """Test validation history is initialized."""
```

**Public Methods:**

- `def test_guardian_initialization(self, guardian)`
- `def test_unvalidated_artifacts_initialized(self, guardian)`
- `def test_validation_history_initialized(self, guardian)`
- `def test_auth_patterns_configured(self, guardian)`
- `def test_validation_patterns_configured(self, guardian)`
- `def test_audit_patterns_configured(self, guardian)`
- `def test_dangerous_patterns_configured(self, guardian)`
- `def test_get_monitored_systems(self, guardian)`

---

### `TestMonitoring`

**File:** `test_article_iii_guardian.py`

```python
class TestMonitoring:
```

**Description:**
```
"""Test monitoring orchestration."""

@pytest.mark.asyncio
async def test_monitor_calls_all_checks(self, guardian):
    """Test monitor() orchestrates all check methods."""
    with patch.object(guardian, '_check_ai_artifacts', return_value=[]) as mock_ai, \
         patch.object(guardian, '_check_authentication', return_value=[]) as mock_auth, \
         patch.object(guardian, '_check_input_validation', return_value=[]) as mock_input, \
         patch.object(guardian, '_check_trust_assumptions', return_value=[]) as mock_trust, \
         patch.object(guardian, '_check_audit_trails', return_value=[]) as mock_audit:

        violations = await guardian.monitor()

        # All check methods should be called
        mock_ai.assert_called_once()
        mock_auth.assert_called_once()
```

**Public Methods:**


---

### `TestAIArtifactChecking`

**File:** `test_article_iii_guardian.py`

```python
class TestAIArtifactChecking:
```

**Description:**
```
"""Test AI artifact validation checking."""

@pytest.mark.asyncio
async def test_check_ai_artifacts_detects_claude_marker(self, tmp_path):
    """Test _check_ai_artifacts detects 'Generated by Claude' marker."""
    # Create file with AI marker in monitored path
    test_file = tmp_path / "service.py"
    test_file.write_text(
        "# Generated by Claude\n"
        "def foo():\n"
        "    return 42\n"
    )

    # Guardian with this temp path
    guardian = ArticleIIIGuardian(monitored_paths=[str(tmp_path)])
```

**Public Methods:**


---

### `TestAuthenticationChecking`

**File:** `test_article_iii_guardian.py`

```python
class TestAuthenticationChecking:
```

**Description:**
```
"""Test authentication checking."""

@pytest.mark.asyncio
async def test_check_authentication_detects_unauth_endpoint(self, tmp_path):
    """Test _check_authentication detects endpoints without auth."""
    # Create API file with endpoint WITHOUT authentication
    api_dir = tmp_path / "api"
    api_dir.mkdir()
    api_file = api_dir / "routes.py"
    api_file.write_text(
        "@app.post('/users')\n"
        "def create_user(request):\n"
        "    return {'status': 'ok'}\n"
    )

    guardian = ArticleIIIGuardian(api_paths=[str(api_dir)])
```

**Public Methods:**


---

### `TestInputValidationChecking`

**File:** `test_article_iii_guardian.py`

```python
class TestInputValidationChecking:
```

**Description:**
```
"""Test input validation checking."""

@pytest.mark.asyncio
async def test_check_input_validation_detects_unvalidated_input(self, tmp_path):
    """Test _check_input_validation detects unvalidated user input."""
    # Create API file with unvalidated input
    api_dir = tmp_path / "api"
    api_dir.mkdir()
    api_file = api_dir / "handler.py"
    api_file.write_text(
        "def process_user_data(request):\n"
        "    data = request.json\n"  # No validation!
        "    return process(data)\n"
    )

    guardian = ArticleIIIGuardian(api_paths=[str(api_dir)])
```

**Public Methods:**


---

### `TestTrustAssumptionChecking`

**File:** `test_article_iii_guardian.py`

```python
class TestTrustAssumptionChecking:
```

**Description:**
```
"""Test trust assumption detection."""

@pytest.mark.asyncio
async def test_check_trust_assumptions_detects_dangerous_patterns(self, tmp_path):
    """Test _check_trust_assumptions detects dangerous trust patterns (lines 356-361)."""
    # Create file with dangerous pattern
    code_file = tmp_path / "service.py"
    code_file.write_text(
        "def authenticate_user(user):\n"
        "    # assume user is trusted\n"
        "    return grant_access(user)\n"
    )

    guardian = ArticleIIIGuardian(monitored_paths=[str(tmp_path)])
    violations = await guardian._check_trust_assumptions()
```

**Public Methods:**


---

### `TestAuditTrailChecking`

**File:** `test_article_iii_guardian.py`

```python
class TestAuditTrailChecking:
```

**Description:**
```
"""Test audit trail verification."""

@pytest.mark.asyncio
async def test_check_audit_trails_detects_missing_audit(self, tmp_path):
    """Test _check_audit_trails detects critical operations without audit (lines 412-428)."""
    # Create file with critical operation but no audit
    admin_file = tmp_path / "admin.py"
    admin_file.write_text(
        "def delete_user(user_id):\n"
        "    db.users.delete(user_id)\n"
        "    return True\n"
    )

    guardian = ArticleIIIGuardian(monitored_paths=[str(tmp_path)])
    violations = await guardian._check_audit_trails()
```

**Public Methods:**


---

### `TestValidationWorkflow`

**File:** `test_article_iii_guardian.py`

```python
class TestValidationWorkflow:
```

**Description:**
```
"""Test artifact validation workflow."""

def test_get_validated_hashes_empty(self, guardian):
    """Test _get_validated_hashes returns empty set when no history."""
    hashes = guardian._get_validated_hashes()

    assert isinstance(hashes, set)
    assert len(hashes) == 0

def test_get_validated_hashes_with_history(self, guardian):
    """Test _get_validated_hashes returns hashes from history."""
    guardian.validation_history.append({
        "file_hash": "hash1",
        "validated": True,
    })
    guardian.validation_history.append({
```

**Public Methods:**

- `def test_get_validated_hashes_empty(self, guardian)`
- `def test_get_validated_hashes_with_history(self, guardian)`

---

### `TestDecisionMaking`

**File:** `test_article_iii_guardian.py`

```python
class TestDecisionMaking:
```

**Description:**
```
"""Test decision making logic."""

@pytest.mark.asyncio
async def test_analyze_violation_critical(self, guardian):
    """Test analyze_violation with CRITICAL severity."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_III,
        rule="Test rule",
        severity=GuardianPriority.CRITICAL
    )

    decision = await guardian.analyze_violation(violation)

    assert decision.decision_type == "veto"
```

**Public Methods:**


---

### `TestIntervention`

**File:** `test_article_iii_guardian.py`

```python
class TestIntervention:
```

**Description:**
```
"""Test intervention logic."""

@pytest.mark.asyncio
async def test_intervene_critical_veto(self, guardian):
    """Test intervene with CRITICAL violation creates VETO."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_III,
        rule="Critical rule",
        severity=GuardianPriority.CRITICAL
    )

    intervention = await guardian.intervene(violation)

    assert intervention.intervention_type == InterventionType.VETO
```

**Public Methods:**


---

### `TestIntegration`

**File:** `test_article_iii_guardian.py`

```python
class TestIntegration:
```

**Description:**
```
"""Test complete workflows."""

@pytest.mark.asyncio
async def test_full_validation_workflow(self, guardian, temp_python_file):
    """Test complete artifact validation workflow."""
    # Create AI-generated file
    temp_python_file.write_text(
        "# Generated by Claude\n"
        "def process_data(input_data):\n"
        "    return input_data * 2\n"
    )

    # Validate it
    result = await guardian.validate_artifact(
        file_path=str(temp_python_file),
        validator_id="architect-001",
```

**Public Methods:**


---

### `TestArticleIVGuardianInit`

**File:** `test_article_iv_guardian.py`

```python
class TestArticleIVGuardianInit:
```

**Description:**
```
"""Test Article IV Guardian initialization."""

def test_guardian_initialization(self, guardian):
    """Test guardian initializes with correct attributes."""
    assert guardian.guardian_id == "guardian-article-iv"
    assert guardian.article == ConstitutionalArticle.ARTICLE_IV
    assert guardian.name == "Antifragility Guardian"
    assert "Deliberate Antifragility" in guardian.description

def test_chaos_experiments_initialized(self, guardian):
    """Test chaos experiments list is initialized."""
    assert isinstance(guardian.chaos_experiments, list)
    assert len(guardian.chaos_experiments) == 0

def test_quarantined_features_initialized(self, guardian):
    """Test quarantined features dict is initialized."""
```

**Public Methods:**

- `def test_guardian_initialization(self, guardian)`
- `def test_chaos_experiments_initialized(self, guardian)`
- `def test_quarantined_features_initialized(self, guardian)`
- `def test_resilience_metrics_initialized(self, guardian)`
- `def test_resilience_patterns_configured(self, guardian)`
- `def test_chaos_indicators_configured(self, guardian)`
- `def test_get_monitored_systems(self, guardian)`

---

### `TestMonitoring`

**File:** `test_article_iv_guardian.py`

```python
class TestMonitoring:
```

**Description:**
```
"""Test monitoring orchestration."""

@pytest.mark.asyncio
async def test_monitor_calls_all_checks(self, guardian):
    """Test monitor() orchestrates all check methods."""
    with patch.object(guardian, '_check_chaos_engineering', return_value=[]) as mock_chaos, \
         patch.object(guardian, '_check_resilience_patterns', return_value=[]) as mock_resilience, \
         patch.object(guardian, '_check_experimental_features', return_value=[]) as mock_experimental, \
         patch.object(guardian, '_check_failure_recovery', return_value=[]) as mock_recovery, \
         patch.object(guardian, '_check_system_fragility', return_value=[]) as mock_fragility:

        violations = await guardian.monitor()

        # All check methods should be called
        mock_chaos.assert_called_once()
        mock_resilience.assert_called_once()
```

**Public Methods:**


---

### `TestChaosEngineering`

**File:** `test_article_iv_guardian.py`

```python
class TestChaosEngineering:
```

**Description:**
```
"""Test chaos engineering checking."""

@pytest.mark.asyncio
async def test_check_chaos_engineering_detects_insufficient_tests(self, tmp_path):
    """Test _check_chaos_engineering detects insufficient chaos tests."""
    # Create test directory with mostly regular tests
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()

    # Create 10 regular tests
    for i in range(10):
        test_file = tests_dir / f"test_regular_{i}.py"
        test_file.write_text("def test_something(): pass\n")

    # Create only 1 chaos test (10% ratio)
    chaos_file = tests_dir / "test_chaos.py"
```

**Public Methods:**


---

### `TestResiliencePatterns`

**File:** `test_article_iv_guardian.py`

```python
class TestResiliencePatterns:
```

**Description:**
```
"""Test resilience pattern checking."""

@pytest.mark.asyncio
async def test_check_resilience_patterns_detects_missing_patterns(self, tmp_path):
    """Test _check_resilience_patterns detects missing resilience patterns."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file without any resilience patterns
    service_file = service_dir / "api.py"
    service_file.write_text("def process(): return 'ok'\n")

    guardian = ArticleIVGuardian(service_paths=[str(service_dir)])
    violations = await guardian._check_resilience_patterns()

    # Should detect missing patterns (> 3 missing)
```

**Public Methods:**


---

### `TestExperimentalFeatures`

**File:** `test_article_iv_guardian.py`

```python
class TestExperimentalFeatures:
```

**Description:**
```
"""Test experimental feature quarantine checking."""

@pytest.mark.asyncio
async def test_check_experimental_features_detects_unquarantined(self, tmp_path):
    """Test _check_experimental_features detects unquarantined experimental features."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file with experimental marker
    feature_file = service_dir / "beta_feature.py"
    feature_file.write_text("@experimental\ndef new_feature(): pass\n")

    guardian = ArticleIVGuardian(service_paths=[str(service_dir)])
    violations = await guardian._check_experimental_features()

    # Should detect unquarantined feature
```

**Public Methods:**


---

### `TestFailureRecovery`

**File:** `test_article_iv_guardian.py`

```python
class TestFailureRecovery:
```

**Description:**
```
"""Test failure recovery mechanism checking."""

@pytest.mark.asyncio
async def test_check_failure_recovery_detects_missing_recovery(self, tmp_path):
    """Test _check_failure_recovery detects critical ops without recovery."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file with critical operation but NO error handling
    critical_file = service_dir / "payment.py"
    critical_file.write_text(
        "def process_payment(amount):\n"
        "    database.charge(amount)\n"
        "    return True\n"
    )
```

**Public Methods:**


---

### `TestSystemFragility`

**File:** `test_article_iv_guardian.py`

```python
class TestSystemFragility:
```

**Description:**
```
"""Test system fragility detection."""

@pytest.mark.asyncio
async def test_check_system_fragility_detects_high_fragility(self, tmp_path):
    """Test _check_system_fragility detects high fragility score."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create multiple files with fragility indicators
    for i in range(15):
        fragile_file = service_dir / f"fragile_{i}.py"
        fragile_file.write_text(
            f"HARDCODED_URL = 'https://api.example.com'\n"
            f"singleton = True\n"
            f"global state_{i}\n"
        )
```

**Public Methods:**


---

### `TestChaosExperimentExecution`

**File:** `test_article_iv_guardian.py`

```python
class TestChaosExperimentExecution:
```

**Description:**
```
"""Test chaos experiment execution."""

@pytest.mark.asyncio
async def test_run_chaos_experiment_creates_experiment(self, guardian):
    """Test run_chaos_experiment creates and tracks experiment."""
    result = await guardian.run_chaos_experiment(
        "network_latency",
        "api_service",
        {"latency_ms": 500}
    )

    assert result["type"] == "network_latency"
    assert result["target"] == "api_service"
    assert result["status"] == "completed"
    assert "results" in result
    assert len(guardian.chaos_experiments) == 1
```

**Public Methods:**


---

### `TestFeatureQuarantine`

**File:** `test_article_iv_guardian.py`

```python
class TestFeatureQuarantine:
```

**Description:**
```
"""Test feature quarantine workflow."""

@pytest.mark.asyncio
async def test_quarantine_feature_success(self, guardian):
    """Test quarantine_feature successfully quarantines a feature."""
    result = await guardian.quarantine_feature(
        "beta_ai_agent",
        "/path/to/feature.py",
        "high"
    )

    assert result is True
    assert "beta_ai_agent" in guardian.quarantined_features
    assert guardian.quarantined_features["beta_ai_agent"]["status"] == "quarantined"

@pytest.mark.asyncio
```

**Public Methods:**


---

### `TestDecisionMaking`

**File:** `test_article_iv_guardian.py`

```python
class TestDecisionMaking:
```

**Description:**
```
"""Test decision making logic."""

@pytest.mark.asyncio
async def test_analyze_violation_insufficient_chaos(self, guardian):
    """Test analyze_violation for insufficient chaos testing."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_IV,
        rule="Must provoke failures",
        description="Insufficient chaos testing detected"
    )

    decision = await guardian.analyze_violation(violation)

    assert decision.decision_type == "alert"
```

**Public Methods:**


---

### `TestIntervention`

**File:** `test_article_iv_guardian.py`

```python
class TestIntervention:
```

**Description:**
```
"""Test intervention logic."""

@pytest.mark.asyncio
async def test_intervene_experimental_feature_quarantine(self, guardian):
    """Test intervene quarantines experimental features."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_IV,
        rule="Quarantine required",
        description="Experimental feature detected",
        context={"feature_id": "beta_001", "file": "/path/to/feature.py"}
    )

    intervention = await guardian.intervene(violation)
```

**Public Methods:**


---

### `TestIntegration`

**File:** `test_article_iv_guardian.py`

```python
class TestIntegration:
```

**Description:**
```
"""Test complete workflows."""

@pytest.mark.asyncio
async def test_full_chaos_experiment_workflow(self, guardian):
    """Test complete chaos experiment workflow."""
    # Run experiment
    experiment = await guardian.run_chaos_experiment(
        "network_partition",
        "microservice_cluster",
        {"partitions": 3}
    )

    # Verify experiment tracked
    assert experiment["id"] in [e["id"] for e in guardian.chaos_experiments]

    # Verify metrics updated
```

**Public Methods:**


---

### `TestArticleVGuardianInit`

**File:** `test_article_v_guardian.py`

```python
class TestArticleVGuardianInit:
```

**Description:**
```
"""Test Article V Guardian initialization."""

def test_guardian_initialization(self, guardian):
    """Test guardian initializes with correct attributes."""
    assert guardian.guardian_id == "guardian-article-v"
    assert guardian.article == ConstitutionalArticle.ARTICLE_V
    assert guardian.name == "Prior Legislation Guardian"
    assert "Prior Legislation" in guardian.description

def test_autonomous_systems_initialized(self, guardian):
    """Test autonomous systems dict is initialized."""
    assert isinstance(guardian.autonomous_systems, dict)
    assert len(guardian.autonomous_systems) == 0

def test_governance_registry_initialized(self, guardian):
    """Test governance registry dict is initialized."""
```

**Public Methods:**

- `def test_guardian_initialization(self, guardian)`
- `def test_autonomous_systems_initialized(self, guardian)`
- `def test_governance_registry_initialized(self, guardian)`
- `def test_responsibility_requirements_configured(self, guardian)`
- `def test_autonomous_indicators_configured(self, guardian)`
- `def test_governance_indicators_configured(self, guardian)`
- `def test_configurable_paths_initialized(self, guardian)`
- `def test_custom_paths_injection(self, tmp_path)`
- `def test_get_monitored_systems(self, guardian)`

---

### `TestMonitoring`

**File:** `test_article_v_guardian.py`

```python
class TestMonitoring:
```

**Description:**
```
"""Test monitoring orchestration."""

@pytest.mark.asyncio
async def test_monitor_calls_all_checks(self, guardian):
    """Test monitor() orchestrates all check methods."""
    with patch.object(guardian, '_check_autonomous_governance', return_value=[]) as mock_auto, \
         patch.object(guardian, '_check_responsibility_doctrine', return_value=[]) as mock_resp, \
         patch.object(guardian, '_check_hitl_controls', return_value=[]) as mock_hitl, \
         patch.object(guardian, '_check_kill_switches', return_value=[]) as mock_kill, \
         patch.object(guardian, '_check_two_man_rule', return_value=[]) as mock_twoman:

        violations = await guardian.monitor()

        # All check methods should be called
        mock_auto.assert_called_once()
        mock_resp.assert_called_once()
```

**Public Methods:**


---

### `TestAutonomousGovernance`

**File:** `test_article_v_guardian.py`

```python
class TestAutonomousGovernance:
```

**Description:**
```
"""Test autonomous governance checking."""

@pytest.mark.asyncio
async def test_check_autonomous_governance_detects_ungoverned(self, tmp_path):
    """Test _check_autonomous_governance detects autonomous systems without governance."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create autonomous file WITHOUT governance
    auto_file = service_dir / "agent.py"
    auto_file.write_text("class AutonomousAgent:\n    def auto_execute(self): pass\n")

    guardian = ArticleVGuardian(autonomous_paths=[str(service_dir)])
    violations = await guardian._check_autonomous_governance()

    # Should detect ungoverned autonomous system
```

**Public Methods:**


---

### `TestResponsibilityDoctrine`

**File:** `test_article_v_guardian.py`

```python
class TestResponsibilityDoctrine:
```

**Description:**
```
"""Test responsibility doctrine checking."""

@pytest.mark.asyncio
async def test_check_responsibility_doctrine_detects_missing_controls(self, tmp_path):
    """Test _check_responsibility_doctrine detects missing responsibility controls."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file with powerful operation but NO responsibility controls
    powerful_file = service_dir / "exploit.py"
    powerful_file.write_text(
        "def execute_exploit():\n"
        "    subprocess.run(['rm', '-rf', '/'])\n"
    )

    guardian = ArticleVGuardian(powerful_paths=[str(service_dir)])
```

**Public Methods:**


---

### `TestHITLControls`

**File:** `test_article_v_guardian.py`

```python
class TestHITLControls:
```

**Description:**
```
"""Test Human-In-The-Loop controls checking."""

@pytest.mark.asyncio
async def test_check_hitl_controls_detects_missing_hitl(self, tmp_path):
    """Test _check_hitl_controls detects critical operations without HITL."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file with critical operation but NO HITL
    critical_file = service_dir / "deploy.py"
    critical_file.write_text(
        "def production_deploy():\n"
        "    deploy_to_production()\n"
    )

    guardian = ArticleVGuardian(hitl_paths=[str(service_dir)])
```

**Public Methods:**


---

### `TestKillSwitch`

**File:** `test_article_v_guardian.py`

```python
class TestKillSwitch:
```

**Description:**
```
"""Test kill switch implementation checking."""

@pytest.mark.asyncio
async def test_check_kill_switches_detects_missing_killswitch(self, tmp_path):
    """Test _check_kill_switches detects autonomous processes without kill switch."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file with long-running process but NO kill switch
    process_file = service_dir / "worker.py"
    process_file.write_text(
        "def run_worker():\n"
        "    while True:\n"
        "        process()\n"
    )
```

**Public Methods:**


---

### `TestTwoManRule`

**File:** `test_article_v_guardian.py`

```python
class TestTwoManRule:
```

**Description:**
```
"""Test Two-Man Rule implementation checking."""

@pytest.mark.asyncio
async def test_check_two_man_rule_detects_missing_dual_approval(self, tmp_path):
    """Test _check_two_man_rule detects critical actions without dual approval."""
    service_dir = tmp_path / "service"
    service_dir.mkdir()

    # Create file with critical action but NO dual approval
    critical_file = service_dir / "admin.py"
    critical_file.write_text(
        "def admin_grant_privileges():\n"
        "    grant_admin()\n"
    )

    guardian = ArticleVGuardian(governance_paths=[str(service_dir)])
```

**Public Methods:**


---

### `TestGovernanceRegistration`

**File:** `test_article_v_guardian.py`

```python
class TestGovernanceRegistration:
```

**Description:**
```
"""Test governance registration functionality."""

@pytest.mark.asyncio
async def test_register_governance_success(self, guardian):
    """Test register_governance successfully registers governance."""
    result = await guardian.register_governance(
        "system-001",
        "policy-based",
        ["policy-1", "policy-2"],
        {"hitl": True, "audit": True}
    )

    assert result is True
    assert "system-001" in guardian.governance_registry
    assert guardian.governance_registry["system-001"]["governance_type"] == "policy-based"
```

**Public Methods:**


---

### `TestGovernancePrecedence`

**File:** `test_article_v_guardian.py`

```python
class TestGovernancePrecedence:
```

**Description:**
```
"""Test governance precedence validation."""

@pytest.mark.asyncio
async def test_validate_governance_precedence_missing_governance_files(self, tmp_path):
    """Test validate_governance_precedence detects missing governance files."""
    system_file = tmp_path / "agent.py"
    system_file.write_text("class Agent: pass\n")

    guardian = ArticleVGuardian()
    is_valid, reason = await guardian.validate_governance_precedence(str(system_file))

    assert is_valid is False
    assert "No governance files" in reason

@pytest.mark.asyncio
async def test_validate_governance_precedence_missing_governance_import(self, tmp_path):
```

**Public Methods:**


---

### `TestDecisionMaking`

**File:** `test_article_v_guardian.py`

```python
class TestDecisionMaking:
```

**Description:**
```
"""Test decision making logic."""

@pytest.mark.asyncio
async def test_analyze_violation_critical_severity(self, guardian):
    """Test analyze_violation for CRITICAL severity violations."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_V,
        rule="Test rule",
        severity=GuardianPriority.CRITICAL
    )

    decision = await guardian.analyze_violation(violation)

    assert decision.decision_type == "veto"
```

**Public Methods:**


---

### `TestIntervention`

**File:** `test_article_v_guardian.py`

```python
class TestIntervention:
```

**Description:**
```
"""Test intervention logic."""

@pytest.mark.asyncio
async def test_intervene_critical_severity_veto(self, guardian):
    """Test intervene VETOs critical severity violations."""
    from governance.guardian.base import ConstitutionalViolation

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_V,
        rule="Test rule",
        severity=GuardianPriority.CRITICAL,
        context={"system_id": "test-system"}
    )

    # Register system first
    guardian.autonomous_systems["test-system"] = {"path": "/test"}
```

**Public Methods:**


---

### `TestGuardian`

**File:** `test_base_coverage.py`

```python
class TestGuardian(GuardianAgent):
```

**Description:**
```
"""Concrete Guardian implementation for testing base class."""

def __init__(self):
    super().__init__(
        guardian_id="test-guardian",
        article=ConstitutionalArticle.ARTICLE_II,
        name="Test Guardian",
        description="Guardian for testing",
    )
    self.monitor_called = False
    self.analyze_called = False
    self.intervene_called = False

async def monitor(self) -> list[ConstitutionalViolation]:
    """Mock monitor that returns violations."""
    self.monitor_called = True
```

**Public Methods:**

- `def get_monitored_systems(self) -> list[str]`

---

### `TestConstitutionalViolation`

**File:** `test_base_coverage.py`

```python
class TestConstitutionalViolation:
```

**Description:**
```
"""Test ConstitutionalViolation data structure."""

def test_to_dict(self):
    """Test conversion to dictionary."""
    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_II,
        clause="Test Clause",
        rule="Test Rule",
        description="Test description",
        severity=GuardianPriority.HIGH,
        context={"key": "value"},
        evidence=["evidence1", "evidence2"],
        affected_systems=["system1"],
        recommended_action="Fix it",
        metadata={"meta": "data"},
    )
```

**Public Methods:**

- `def test_to_dict(self)`
- `def test_generate_hash(self)`

---

### `TestVetoAction`

**File:** `test_base_coverage.py`

```python
class TestVetoAction:
```

**Description:**
```
"""Test VetoAction data structure."""

def test_is_active_no_expiry(self):
    """Test veto is active when no expiry set."""
    veto = VetoAction(
        guardian_id="test-guardian",
        target_action="deploy",
        target_system="production",
        reason="Test reason",
        expires_at=None,
    )

    assert veto.is_active() is True

def test_is_active_future_expiry(self):
    """Test veto is active when expiry is in future."""
```

**Public Methods:**

- `def test_is_active_no_expiry(self)`
- `def test_is_active_future_expiry(self)`
- `def test_is_active_past_expiry(self)`
- `def test_to_dict(self)`
- `def test_to_dict_no_violation(self)`

---

### `TestGuardianIntervention`

**File:** `test_base_coverage.py`

```python
class TestGuardianIntervention:
```

**Description:**
```
"""Test GuardianIntervention data structure."""

def test_to_dict(self):
    """Test intervention conversion to dictionary."""
    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_IV,
        clause="Test",
        rule="Test",
        description="Test",
        severity=GuardianPriority.CRITICAL,
    )

    intervention = GuardianIntervention(
        guardian_id="test-guardian",
        intervention_type=InterventionType.VETO,
        priority=GuardianPriority.CRITICAL,
```

**Public Methods:**

- `def test_to_dict(self)`
- `def test_to_dict_no_violation(self)`

---

### `TestGuardianDecision`

**File:** `test_base_coverage.py`

```python
class TestGuardianDecision:
```

**Description:**
```
"""Test GuardianDecision data structure."""

def test_to_dict(self):
    """Test decision conversion to dictionary."""
    decision = GuardianDecision(
        guardian_id="test-guardian",
        decision_type="veto",
        target="deployment.yaml",
        reasoning="Critical constitutional violation",
        confidence=0.95,
        requires_validation=False,
        metadata={"evidence": "file_scan"},
    )

    result = decision.to_dict()
```

**Public Methods:**

- `def test_to_dict(self)`

---

### `TestGuardianReport`

**File:** `test_base_coverage.py`

```python
class TestGuardianReport:
```

**Description:**
```
"""Test GuardianReport data structure."""

def test_to_dict(self):
    """Test report conversion to dictionary."""
    period_start = datetime.utcnow() - timedelta(hours=24)
    period_end = datetime.utcnow()

    report = GuardianReport(
        guardian_id="test-guardian",
        period_start=period_start,
        period_end=period_end,
        violations_detected=10,
        interventions_made=5,
        vetos_enacted=2,
        compliance_score=85.5,
        top_violations=["violation1", "violation2"],
```

**Public Methods:**

- `def test_to_dict(self)`

---

### `TestGuardianAgentLifecycle`

**File:** `test_base_coverage.py`

```python
class TestGuardianAgentLifecycle:
```

**Description:**
```
"""Test Guardian Agent lifecycle management."""

@pytest.mark.asyncio
async def test_start_guardian(self):
    """Test starting a guardian."""
    guardian = TestGuardian()

    assert not guardian.is_active()
    assert guardian._monitor_task is None

    await guardian.start()

    assert guardian.is_active()
    assert guardian._monitor_task is not None

    await guardian.stop()
```

**Public Methods:**


---

### `TestViolationProcessing`

**File:** `test_base_coverage.py`

```python
class TestViolationProcessing:
```

**Description:**
```
"""Test violation processing and callbacks."""

@pytest.mark.asyncio
async def test_process_violation_records(self):
    """Test that processing a violation records it."""
    guardian = TestGuardian()

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_II,
        clause="Test",
        rule="Test",
        description="Test violation",
        severity=GuardianPriority.MEDIUM,
    )

    await guardian._process_violation(violation)
```

**Public Methods:**


---

### `TestVetoPower`

**File:** `test_base_coverage.py`

```python
class TestVetoPower:
```

**Description:**
```
"""Test Guardian veto power functionality."""

@pytest.mark.asyncio
async def test_veto_action_permanent(self):
    """Test creating permanent veto (no duration)."""
    guardian = TestGuardian()

    veto = await guardian.veto_action(
        action="deploy_to_production",
        system="maximus_core",
        reason="Contains NotImplementedError",
        duration_hours=None,
    )

    assert veto.guardian_id == guardian.guardian_id
    assert veto.target_action == "deploy_to_production"
```

**Public Methods:**

- `def test_get_active_vetos_filters_expired(self)`

---

### `Test_CreateVeto`

**File:** `test_base_coverage.py`

```python
class Test_CreateVeto:
```

**Description:**
```
"""Test internal _create_veto method."""

@pytest.mark.asyncio
async def test_create_veto_high_confidence(self):
    """Test veto creation with high confidence (no override)."""
    guardian = TestGuardian()

    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_V,
        clause="Section 1",
        rule="Test rule",
        description="Test",
        severity=GuardianPriority.CRITICAL,
        affected_systems=["critical_system"],
    )
```

**Public Methods:**


---

### `TestErrorHandling`

**File:** `test_base_coverage.py`

```python
class TestErrorHandling:
```

**Description:**
```
"""Test Guardian error handling."""

@pytest.mark.asyncio
async def test_monitor_error_creates_violation(self):
    """Test that monitoring errors create error violations."""
    guardian = TestGuardian()

    test_error = RuntimeError("Test monitoring error")

    await guardian._handle_monitor_error(test_error)

    assert len(guardian._violations) == 1
    error_violation = guardian._violations[0]
    assert "Guardian monitoring error" in error_violation.description
    assert error_violation.severity == GuardianPriority.HIGH
    assert error_violation.article == ConstitutionalArticle.ARTICLE_II
```

**Public Methods:**


---

### `TestReporting`

**File:** `test_base_coverage.py`

```python
class TestReporting:
```

**Description:**
```
"""Test Guardian reporting functionality."""

def test_generate_report_empty(self):
    """Test report generation with no data."""
    guardian = TestGuardian()

    report = guardian.generate_report(period_hours=24)

    assert report.guardian_id == guardian.guardian_id
    assert report.violations_detected == 0
    assert report.interventions_made == 0
    assert report.vetos_enacted == 0
    assert report.compliance_score == 100.0

def test_generate_report_with_violations(self):
    """Test report with violations in period."""
```

**Public Methods:**

- `def test_generate_report_empty(self)`
- `def test_generate_report_with_violations(self)`
- `def test_generate_report_filters_by_period(self)`
- `def test_generate_report_top_violations(self)`
- `def test_generate_report_recommendations(self)`
- `def test_generate_report_with_vetos(self)`

---

### `TestStatusMethods`

**File:** `test_base_coverage.py`

```python
class TestStatusMethods:
```

**Description:**
```
"""Test Guardian status and statistics methods."""

def test_get_statistics(self):
    """Test get_statistics returns comprehensive data."""
    guardian = TestGuardian()

    # Add some data
    guardian._violations.append(
        ConstitutionalViolation(
            article=ConstitutionalArticle.ARTICLE_II,
            clause="Test",
            rule="Test",
            description="Test",
            severity=GuardianPriority.HIGH,
        )
    )
```

**Public Methods:**

- `def test_get_statistics(self)`
- `def test_repr(self)`

---

### `ConcreteGuardian`

**File:** `test_base_guardian.py`

```python
class ConcreteGuardian(GuardianAgent):
```

**Description:**
```
"""Concrete implementation for testing."""

async def monitor(self):
    """Mock implementation."""
    return []

async def analyze_violation(self, violation):
    """Mock implementation."""
    return GuardianDecision(
        guardian_id=self.guardian_id,
        decision_type="allow",
        target="test",
        reasoning="test reasoning",
        confidence=0.9
    )
```

**Public Methods:**

- `def get_monitored_systems(self)`

---

### `TestEnums`

**File:** `test_base_guardian.py`

```python
class TestEnums:
```

**Description:**
```
"""Test enum definitions."""

def test_guardian_priority_values(self):
    """Test GuardianPriority enum values."""
    assert GuardianPriority.CRITICAL == "CRITICAL"
    assert GuardianPriority.HIGH == "HIGH"
    assert GuardianPriority.MEDIUM == "MEDIUM"
    assert GuardianPriority.LOW == "LOW"
    assert GuardianPriority.INFO == "INFO"

def test_intervention_type_values(self):
    """Test InterventionType enum values."""
    assert InterventionType.VETO == "VETO"
    assert InterventionType.ALERT == "ALERT"
    assert InterventionType.REMEDIATION == "REMEDIATION"
    assert InterventionType.ESCALATION == "ESCALATION"
```

**Public Methods:**

- `def test_guardian_priority_values(self)`
- `def test_intervention_type_values(self)`
- `def test_constitutional_article_values(self)`

---

### `TestConstitutionalViolation`

**File:** `test_base_guardian.py`

```python
class TestConstitutionalViolation:
```

**Description:**
```
"""Test ConstitutionalViolation dataclass."""

def test_violation_initialization(self, sample_violation):
    """Test violation creates with all fields."""
    assert sample_violation.violation_id  # Generated UUID
    assert sample_violation.article == ConstitutionalArticle.ARTICLE_II
    assert sample_violation.clause == "Cláusula 3.2"
    assert sample_violation.rule == "Visão Sistêmica Mandatória"
    assert sample_violation.description == "Code lacks systemic integration"
    assert sample_violation.severity == GuardianPriority.HIGH

def test_violation_to_dict(self, sample_violation):
    """Test violation converts to dictionary."""
    violation_dict = sample_violation.to_dict()

    assert violation_dict["violation_id"] == sample_violation.violation_id
```

**Public Methods:**

- `def test_violation_initialization(self, sample_violation)`
- `def test_violation_to_dict(self, sample_violation)`
- `def test_violation_generate_hash(self, sample_violation)`
- `def test_violation_hash_uniqueness(self)`
- `def test_violation_default_values(self)`

---

### `TestVetoAction`

**File:** `test_base_guardian.py`

```python
class TestVetoAction:
```

**Description:**
```
"""Test VetoAction dataclass."""

def test_veto_initialization(self):
    """Test veto creates with all fields."""
    veto = VetoAction(
        guardian_id="g1",
        target_action="deploy_to_prod",
        target_system="ci_cd",
        reason="No tests"
    )

    assert veto.veto_id
    assert veto.guardian_id == "g1"
    assert veto.target_action == "deploy_to_prod"
    assert veto.target_system == "ci_cd"
    assert veto.reason == "No tests"
```

**Public Methods:**

- `def test_veto_initialization(self)`
- `def test_veto_is_active_permanent(self)`
- `def test_veto_is_active_not_expired(self)`
- `def test_veto_is_active_expired(self)`
- `def test_veto_to_dict(self, sample_violation)`
- `def test_veto_to_dict_no_violation(self)`

---

### `TestGuardianIntervention`

**File:** `test_base_guardian.py`

```python
class TestGuardianIntervention:
```

**Description:**
```
"""Test GuardianIntervention dataclass."""

def test_intervention_initialization(self):
    """Test intervention creates with all fields."""
    intervention = GuardianIntervention(
        guardian_id="g1",
        intervention_type=InterventionType.VETO,
        priority=GuardianPriority.CRITICAL,
        action_taken="Blocked deployment",
        result="Success"
    )

    assert intervention.intervention_id
    assert intervention.guardian_id == "g1"
    assert intervention.intervention_type == InterventionType.VETO
    assert intervention.priority == GuardianPriority.CRITICAL
```

**Public Methods:**

- `def test_intervention_initialization(self)`
- `def test_intervention_to_dict(self, sample_violation)`
- `def test_intervention_defaults(self)`

---

### `TestGuardianDecision`

**File:** `test_base_guardian.py`

```python
class TestGuardianDecision:
```

**Description:**
```
"""Test GuardianDecision dataclass."""

def test_decision_initialization(self):
    """Test decision creates with all fields."""
    decision = GuardianDecision(
        guardian_id="g1",
        decision_type="block",
        target="deployment",
        reasoning="No tests",
        confidence=0.95
    )

    assert decision.decision_id
    assert decision.guardian_id == "g1"
    assert decision.decision_type == "block"
    assert decision.confidence == 0.95
```

**Public Methods:**

- `def test_decision_initialization(self)`
- `def test_decision_to_dict(self)`
- `def test_decision_defaults(self)`

---

### `TestGuardianReport`

**File:** `test_base_guardian.py`

```python
class TestGuardianReport:
```

**Description:**
```
"""Test GuardianReport dataclass."""

def test_report_initialization(self):
    """Test report creates with all fields."""
    report = GuardianReport(
        guardian_id="g1",
        violations_detected=5,
        interventions_made=3,
        vetos_enacted=1,
        compliance_score=95.0
    )

    assert report.report_id
    assert report.guardian_id == "g1"
    assert report.violations_detected == 5
    assert report.compliance_score == 95.0
```

**Public Methods:**

- `def test_report_initialization(self)`
- `def test_report_to_dict(self)`
- `def test_report_defaults(self)`

---

### `TestGuardianAgentInit`

**File:** `test_base_guardian.py`

```python
class TestGuardianAgentInit:
```

**Description:**
```
"""Test GuardianAgent initialization."""

def test_guardian_initialization(self, guardian):
    """Test guardian creates with all attributes."""
    assert guardian.guardian_id == "test-guardian-001"
    assert guardian.article == ConstitutionalArticle.ARTICLE_II
    assert guardian.name == "Test Guardian"
    assert guardian.description == "Guardian for testing"

def test_guardian_starts_inactive(self, guardian):
    """Test guardian starts in inactive state."""
    assert guardian._is_active is False
    assert guardian._monitor_task is None

def test_guardian_tracking_lists_empty(self, guardian):
    """Test guardian tracking lists start empty."""
```

**Public Methods:**

- `def test_guardian_initialization(self, guardian)`
- `def test_guardian_starts_inactive(self, guardian)`
- `def test_guardian_tracking_lists_empty(self, guardian)`
- `def test_guardian_callbacks_empty(self, guardian)`

---

### `TestGuardianLifecycle`

**File:** `test_base_guardian.py`

```python
class TestGuardianLifecycle:
```

**Description:**
```
"""Test guardian start/stop lifecycle."""

@pytest.mark.asyncio
async def test_guardian_start(self, guardian):
    """Test starting guardian monitoring."""
    await guardian.start()

    assert guardian._is_active is True
    assert guardian._monitor_task is not None

    # Cleanup
    await guardian.stop()

@pytest.mark.asyncio
async def test_guardian_start_idempotent(self, guardian):
    """Test starting already-active guardian is idempotent."""
```

**Public Methods:**


---

### `TestMonitoringLoop`

**File:** `test_base_guardian.py`

```python
class TestMonitoringLoop:
```

**Description:**
```
"""Test guardian monitoring loop."""

@pytest.mark.asyncio
async def test_monitoring_loop_calls_monitor(self, guardian):
    """Test monitoring loop calls monitor() method."""
    violations = []

    async def mock_monitor():
        violations.append(True)
        return []

    guardian.monitor = mock_monitor
    guardian._monitor_interval = 0.01  # Fast

    await guardian.start()
    await asyncio.sleep(0.05)  # Multiple cycles
```

**Public Methods:**


---

### `TestViolationProcessing`

**File:** `test_base_guardian.py`

```python
class TestViolationProcessing:
```

**Description:**
```
"""Test violation processing logic."""

@pytest.mark.asyncio
async def test_process_violation_records(self, guardian, sample_violation):
    """Test _process_violation records violation."""
    await guardian._process_violation(sample_violation)

    assert len(guardian._violations) == 1
    assert guardian._violations[0] == sample_violation

@pytest.mark.asyncio
async def test_process_violation_calls_callbacks(self, guardian, sample_violation):
    """Test _process_violation calls violation callbacks."""
    callback_called = []

    async def callback(violation):
```

**Public Methods:**


---

### `TestVetoPower`

**File:** `test_base_guardian.py`

```python
class TestVetoPower:
```

**Description:**
```
"""Test guardian veto power."""

@pytest.mark.asyncio
async def test_veto_action_creates_veto(self, guardian):
    """Test veto_action creates a veto."""
    veto = await guardian.veto_action(
        action="deploy",
        system="prod",
        reason="No tests"
    )

    assert veto.guardian_id == guardian.guardian_id
    assert veto.target_action == "deploy"
    assert veto.target_system == "prod"
    assert veto.reason == "No tests"
```

**Public Methods:**

- `def test_get_active_vetos(self, guardian)`

---

### `TestReporting`

**File:** `test_base_guardian.py`

```python
class TestReporting:
```

**Description:**
```
"""Test guardian reporting."""

def test_generate_report_basic(self, guardian):
    """Test generate_report creates report."""
    report = guardian.generate_report(period_hours=24)

    assert report.guardian_id == guardian.guardian_id
    assert report.violations_detected == 0
    assert report.interventions_made == 0
    assert report.vetos_enacted == 0
    assert report.compliance_score == 100.0

def test_generate_report_with_violations(self, guardian):
    """Test report includes violations."""
    # Add violations
    for i in range(5):
```

**Public Methods:**

- `def test_generate_report_basic(self, guardian)`
- `def test_generate_report_with_violations(self, guardian)`
- `def test_generate_report_compliance_score(self, guardian)`
- `def test_generate_report_top_violations(self, guardian)`
- `def test_generate_report_recommendations(self, guardian)`

---

### `TestCallbacks`

**File:** `test_base_guardian.py`

```python
class TestCallbacks:
```

**Description:**
```
"""Test callback registration and invocation."""

def test_register_violation_callback(self, guardian):
    """Test registering violation callback."""
    async def callback(violation):
        pass

    guardian.register_violation_callback(callback)

    assert len(guardian._violation_callbacks) == 1
    assert guardian._violation_callbacks[0] == callback

def test_register_intervention_callback(self, guardian):
    """Test registering intervention callback."""
    async def callback(intervention):
        pass
```

**Public Methods:**

- `def test_register_violation_callback(self, guardian)`
- `def test_register_intervention_callback(self, guardian)`
- `def test_register_veto_callback(self, guardian)`

---

### `TestStatusAndMetrics`

**File:** `test_base_guardian.py`

```python
class TestStatusAndMetrics:
```

**Description:**
```
"""Test guardian status and metrics."""

def test_is_active_when_started(self, guardian):
    """Test is_active returns True when monitoring."""
    guardian._is_active = True

    assert guardian.is_active() is True

def test_is_active_when_stopped(self, guardian):
    """Test is_active returns False when not monitoring."""
    assert guardian.is_active() is False

def test_get_statistics(self, guardian):
    """Test get_statistics returns full metrics."""
    guardian._violations.append(ConstitutionalViolation())
    guardian._interventions.append(GuardianIntervention())
```

**Public Methods:**

- `def test_is_active_when_started(self, guardian)`
- `def test_is_active_when_stopped(self, guardian)`
- `def test_get_statistics(self, guardian)`
- `def test_repr(self, guardian)`

---

### `TestEdgeCases`

**File:** `test_base_guardian.py`

```python
class TestEdgeCases:
```

**Description:**
```
"""Test edge cases and error handling."""

@pytest.mark.asyncio
async def test_handle_monitor_error(self, guardian):
    """Test _handle_monitor_error creates violation."""
    error = ValueError("Test error")

    await guardian._handle_monitor_error(error)

    assert len(guardian._violations) == 1
    v = guardian._violations[0]
    assert "monitoring error" in v.description
    assert v.severity == GuardianPriority.HIGH

@pytest.mark.asyncio
async def test_create_veto_with_no_affected_systems(self, guardian):
```

**Public Methods:**


---

### `TestIntegration`

**File:** `test_base_guardian.py`

```python
class TestIntegration:
```

**Description:**
```
"""Test complete guardian workflows."""

@pytest.mark.asyncio
async def test_full_violation_workflow(self, guardian, sample_violation):
    """Test complete violation detection and intervention."""
    callback_violations = []
    callback_interventions = []

    async def v_callback(violation):
        callback_violations.append(violation)

    async def i_callback(intervention):
        callback_interventions.append(intervention)

    guardian.register_violation_callback(v_callback)
    guardian.register_intervention_callback(i_callback)
```

**Public Methods:**


---

### `TestCoordinatorLifecycle`

**File:** `test_coordinator.py`

```python
class TestCoordinatorLifecycle:
```

**Description:**
```
"""Test coordinator lifecycle management."""

@pytest.mark.asyncio
async def test_init_all_guardians(self, coordinator):
    """Test coordinator initializes all Guardian Agents."""
    assert "article_ii" in coordinator.guardians
    assert "article_iii" in coordinator.guardians
    assert "article_iv" in coordinator.guardians
    assert "article_v" in coordinator.guardians
    assert len(coordinator.guardians) == 4

@pytest.mark.asyncio
async def test_start_coordinator(self, coordinator):
    """Test starting the coordinator."""
    assert not coordinator._is_active
```

**Public Methods:**


---

### `TestViolationHandling`

**File:** `test_coordinator.py`

```python
class TestViolationHandling:
```

**Description:**
```
"""Test violation handling and aggregation."""

@pytest.mark.asyncio
async def test_handle_violation_updates_metrics(self, coordinator, sample_violation):
    """Test handling violation updates metrics."""
    initial_count = coordinator.metrics.total_violations_detected

    await coordinator._handle_violation(sample_violation)

    assert coordinator.metrics.total_violations_detected == initial_count + 1
    assert sample_violation in coordinator.all_violations

@pytest.mark.asyncio
async def test_handle_violation_by_article(self, coordinator):
    """Test violations counted by article."""
    violation_ii = ConstitutionalViolation(
```

**Public Methods:**


---

### `TestInterventionHandling`

**File:** `test_coordinator.py`

```python
class TestInterventionHandling:
```

**Description:**
```
"""Test intervention and veto handling."""

@pytest.mark.asyncio
async def test_handle_intervention_increments_counter(
    self, coordinator, sample_intervention
):
    """Test handling intervention increments counter."""
    initial_count = coordinator.metrics.interventions_made

    await coordinator._handle_intervention(sample_intervention)

    assert coordinator.metrics.interventions_made == initial_count + 1
    assert sample_intervention in coordinator.all_interventions

@pytest.mark.asyncio
async def test_handle_veto_increments_counter(self, coordinator, sample_veto):
```

**Public Methods:**


---

### `TestConflictResolution`

**File:** `test_coordinator.py`

```python
class TestConflictResolution:
```

**Description:**
```
"""Test conflict resolution between Guardians."""

@pytest.mark.asyncio
async def test_resolve_no_conflicts(self, coordinator):
    """Test conflict resolution with no conflicts."""
    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_II,
        clause="Test",
        rule="Test rule",
        description="Test",
        severity=GuardianPriority.MEDIUM,
        evidence=[],
        affected_systems=[],
        recommended_action="Fix code",
        context={"file": "test.py"},
    )
```

**Public Methods:**

- `def test_is_conflicting_opposite_actions(self, coordinator)`
- `def test_is_conflicting_same_action(self, coordinator)`
- `def test_article_precedence_article_v_highest(self, coordinator)`
- `def test_severity_priority_critical_highest(self, coordinator)`

---

### `TestPatternDetection`

**File:** `test_coordinator.py`

```python
class TestPatternDetection:
```

**Description:**
```
"""Test violation pattern detection."""

@pytest.mark.asyncio
async def test_analyze_violation_patterns_insufficient_data(self, coordinator):
    """Test pattern analysis with insufficient data."""
    # Only 5 violations (need 10 minimum)
    for i in range(5):
        violation = ConstitutionalViolation(
            article=ConstitutionalArticle.ARTICLE_II,
            clause="Test",
            rule="Test rule",
            description=f"Violation {i}",
            severity=GuardianPriority.MEDIUM,
            evidence=[],
            affected_systems=[],
            recommended_action="Fix",
```

**Public Methods:**


---

### `TestThresholds`

**File:** `test_coordinator.py`

```python
class TestThresholds:
```

**Description:**
```
"""Test critical threshold checking."""

@pytest.mark.asyncio
async def test_check_critical_compliance_threshold(self, coordinator):
    """Test critical alert when compliance drops below threshold."""
    # Set compliance score below 80%
    coordinator.metrics.compliance_score = 75.0

    # Add a violation to avoid index error
    violation = ConstitutionalViolation(
        article=ConstitutionalArticle.ARTICLE_II,
        clause="Test",
        rule="Test",
        description="Test",
        severity=GuardianPriority.MEDIUM,
        evidence=[],
```

**Public Methods:**


---

### `TestMetrics`

**File:** `test_coordinator.py`

```python
class TestMetrics:
```

**Description:**
```
"""Test metrics calculation and updates."""

def test_update_metrics_compliance_score(self, coordinator):
    """Test compliance score calculation."""
    coordinator.metrics.total_violations_detected = 50

    coordinator._update_metrics()

    # (1000 + 50 - 50) / (1000 + 50) = 95.24%
    assert 95.0 <= coordinator.metrics.compliance_score <= 96.0

def test_metrics_to_dict(self, coordinator):
    """Test metrics serialization."""
    coordinator.metrics.total_violations_detected = 10
    coordinator.metrics.interventions_made = 5
    coordinator.metrics.vetos_enacted = 2
```

**Public Methods:**

- `def test_update_metrics_compliance_score(self, coordinator)`
- `def test_metrics_to_dict(self, coordinator)`

---

### `TestReporting`

**File:** `test_coordinator.py`

```python
class TestReporting:
```

**Description:**
```
"""Test compliance reporting."""

@pytest.mark.asyncio
async def test_get_status(self, coordinator):
    """Test get_status returns complete status."""
    await coordinator.start()

    status = coordinator.get_status()

    assert status["coordinator_id"] == coordinator.coordinator_id
    assert status["is_active"] is True
    assert "guardians" in status
    assert "metrics" in status
    assert "active_vetos" in status
    assert "recent_violations" in status
```

**Public Methods:**

- `def test_generate_compliance_report(self, coordinator)`
- `def test_get_top_violations(self, coordinator)`
- `def test_generate_recommendations_quality_issues(self, coordinator)`
- `def test_generate_recommendations_security_issues(self, coordinator)`
- `def test_generate_recommendations_resilience_issues(self, coordinator)`
- `def test_generate_recommendations_governance_issues(self, coordinator)`
- `def test_generate_recommendations_all_compliant(self, coordinator)`

---

### `TestVetoOverride`

**File:** `test_coordinator.py`

```python
class TestVetoOverride:
```

**Description:**
```
"""Test veto override functionality."""

@pytest.mark.asyncio
async def test_override_veto_success(self, coordinator, sample_veto):
    """Test successful veto override."""
    coordinator.all_vetos.append(sample_veto)

    result = await coordinator.override_veto(
        veto_id=sample_veto.veto_id,
        override_reason="Emergency deployment required",
        approver_id="cto@vertice.ai",
    )

    assert result is True
    assert sample_veto.metadata["overridden"] is True
    assert sample_veto.metadata["override_reason"] == "Emergency deployment required"
```

**Public Methods:**


---

### `TestGuardianBase`

**File:** `test_guardians.py`

```python
class TestGuardianBase:
```

**Description:**
```
"""Test base Guardian Agent functionality."""

@pytest.mark.asyncio
async def test_guardian_lifecycle(self):
    """Test Guardian start/stop lifecycle."""
    guardian = ArticleIIGuardian()

    # Test initial state
    assert not guardian.is_active()
    assert guardian.guardian_id == "guardian-article-ii"
    assert guardian.article == ConstitutionalArticle.ARTICLE_II

    # Test start
    await guardian.start()
    assert guardian.is_active()
```

**Public Methods:**

- `def test_report_generation(self)`

---

### `TestArticleIIGuardian`

**File:** `test_guardians.py`

```python
class TestArticleIIGuardian:
```

**Description:**
```
"""Test Article II Guardian - Sovereign Quality Standard."""

@pytest.mark.asyncio
async def test_mock_detection(self):
    """Test detection of mock implementations."""
    guardian = ArticleIIGuardian()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file with mock
        test_file = Path(tmpdir) / "service.py"
        test_file.write_text("""
class Service:
def get_data(self):
    # Using mock for testing
    return Mock(data="test")
        """)
```

**Public Methods:**


---

### `Service`

**File:** `test_guardians.py`

```python
class Service:
```

**Description:**
```
        """)

        # Override monitored paths for test
        guardian.monitored_paths = [tmpdir]

        violations = await guardian.monitor()

        assert len(violations) > 0
        violation = violations[0]
        assert "Mock implementation" in violation.description
        assert violation.article == ConstitutionalArticle.ARTICLE_II
        assert violation.clause == "Section 2"

@pytest.mark.asyncio
async def test_todo_detection(self):
    """Test detection of TODO/FIXME comments."""
```

**Public Methods:**

- `def get_data(self)`

---

### `BaseHandler`

**File:** `test_guardians.py`

```python
class BaseHandler:
```

**Description:**
```
        """)

        guardian.monitored_paths = [tmpdir]
        violations = await guardian.monitor()

        assert len(violations) > 0
        violation = violations[0]
        assert "NotImplementedError" in violation.description
        assert violation.severity == GuardianPriority.CRITICAL

@pytest.mark.asyncio
async def test_skipped_test_detection(self):
    """Test detection of skipped tests without valid reason."""
    guardian = ArticleIIGuardian()

    with tempfile.TemporaryDirectory() as tmpdir:
```

**Public Methods:**

- `def handle(self)`

---

### `TestArticleIIIGuardian`

**File:** `test_guardians.py`

```python
class TestArticleIIIGuardian:
```

**Description:**
```
"""Test Article III Guardian - Zero Trust Principle."""

@pytest.mark.asyncio
async def test_ai_artifact_detection(self):
    """Test detection of unvalidated AI-generated code."""
    guardian = ArticleIIIGuardian()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "ai_service.py"
        test_file.write_text("""
# Generated by Claude Code
class DataProcessor:
def process(self, data):
    return data * 2
        """)
```

**Public Methods:**


---

### `DataProcessor`

**File:** `test_guardians.py`

```python
class DataProcessor:
```

**Description:**
```
        """)

        # Mock the monitored paths
        with patch.object(guardian, "_check_ai_artifacts") as mock_check:
            mock_check.return_value = [
                ConstitutionalViolation(
                    article=ConstitutionalArticle.ARTICLE_III,
                    clause="Section 1",
                    rule="AI artifacts are untrusted until validated",
                    description=f"Unvalidated AI-generated code in {test_file.name}",
                    severity=GuardianPriority.HIGH,
                )
            ]

            violations = await guardian.monitor()
```

**Public Methods:**

- `def process(self, data)`

---

### `TestArticleIVGuardian`

**File:** `test_guardians.py`

```python
class TestArticleIVGuardian:
```

**Description:**
```
"""Test Article IV Guardian - Deliberate Antifragility."""

@pytest.mark.asyncio
async def test_chaos_test_detection(self):
    """Test detection of insufficient chaos engineering tests."""
    guardian = ArticleIVGuardian()

    with tempfile.TemporaryDirectory() as tmpdir:
        tests_dir = Path(tmpdir) / "tests"
        tests_dir.mkdir()

        # Create regular tests
        for i in range(10):
            test_file = tests_dir / f"test_feature_{i}.py"
            test_file.write_text(f"def test_feature_{i}(): assert True")
```

**Public Methods:**


---

### `DataService`

**File:** `test_guardians.py`

```python
class DataService:
```

**Description:**
```
        """)

        # Mock for testing
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.rglob", return_value=[service_file]):
                violations = await guardian._check_resilience_patterns()

                assert len(violations) > 0
                assert any("Missing resilience patterns" in v.description for v in violations)

@pytest.mark.asyncio
async def test_chaos_experiment_execution(self):
    """Test chaos experiment execution."""
    guardian = ArticleIVGuardian()

    result = await guardian.run_chaos_experiment(
```

**Public Methods:**

- `def fetch_data(self)`

---

### `TestArticleVGuardian`

**File:** `test_guardians.py`

```python
class TestArticleVGuardian:
```

**Description:**
```
"""Test Article V Guardian - Prior Legislation."""

@pytest.mark.asyncio
async def test_autonomous_without_governance(self):
    """Test detection of autonomous systems without governance."""
    guardian = ArticleVGuardian()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create autonomous system without governance
        auto_file = Path(tmpdir) / "autonomous_agent.py"
        auto_file.write_text("""
class AutonomousAgent:
def auto_execute(self):
    # Autonomous decision-making
    self.take_action()
        """)
```

**Public Methods:**


---

### `AutonomousAgent`

**File:** `test_guardians.py`

```python
class AutonomousAgent:
```

**Description:**
```
        """)

        # Mock paths
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.rglob", return_value=[auto_file]):
                violations = await guardian._check_autonomous_governance()

                assert len(violations) > 0
                assert any(
                    "Autonomous capability without governance" in v.description
                    for v in violations
                )

@pytest.mark.asyncio
async def test_missing_hitl_controls(self):
    """Test detection of missing HITL controls."""
```

**Public Methods:**

- `def auto_execute(self)`

---

### `TestGuardianCoordinator`

**File:** `test_guardians.py`

```python
class TestGuardianCoordinator:
```

**Description:**
```
"""Test Guardian Coordinator functionality."""

@pytest.mark.asyncio
async def test_coordinator_lifecycle(self):
    """Test coordinator start/stop."""
    coordinator = GuardianCoordinator()

    assert not coordinator._is_active

    await coordinator.start()
    assert coordinator._is_active

    # Check all guardians are started
    for guardian in coordinator.guardians.values():
        assert guardian.is_active()
```

**Public Methods:**

- `def test_compliance_report_generation(self)`

---

### `TestGuardianIntegration`

**File:** `test_guardians.py`

```python
class TestGuardianIntegration:
```

**Description:**
```
"""Integration tests for the complete Guardian system."""

@pytest.mark.asyncio
async def test_full_system_monitoring(self):
    """Test full system monitoring with all guardians."""
    coordinator = GuardianCoordinator()

    # Start the system
    await coordinator.start()

    # Let it run briefly
    await asyncio.sleep(0.1)

    # Get status
    status = coordinator.get_status()
```

**Public Methods:**


---

### `HITLInterface`

**File:** `hitl_interface.py`

```python
class HITLInterface:
```

**Description:**
```
"""
Human-in-the-Loop interface for operator interaction with governance decisions.

⚠️ POC IMPLEMENTATION - For gRPC bridge validation only.
Production version will integrate with authentication and audit systems.
"""

def __init__(self, governance_engine: GovernanceEngine):
    """
    Initialize HITL interface.

    Args:
        governance_engine: The governance engine managing decisions
    """
    self.governance_engine = governance_engine
    self.sessions: dict[str, dict] = {}
```

**Public Methods:**

- `def create_session(self, operator_id`
- `def close_session(self, session_id`
- `def approve_decision(self, decision_id`
- `def reject_decision(self, decision_id`
- `def escalate_decision(self, decision_id`
- `def get_operator_stats(self, operator_id`
- `def get_session_info(self, session_id`

---

### `PolicyRegistry`

**File:** `policies.py`

```python
class PolicyRegistry:
```

**Description:**
```
"""
Central registry for all governance policies.

Provides easy access to policy definitions and management.
"""

def __init__(self):
    """Initialize policy registry."""
    self.policies: dict[PolicyType, Policy] = {}
    self._load_default_policies()

def _load_default_policies(self):
    """Load all default policies."""
    self.policies[PolicyType.ETHICAL_USE] = create_ethical_use_policy()
    self.policies[PolicyType.RED_TEAMING] = create_red_teaming_policy()
    self.policies[PolicyType.DATA_PRIVACY] = create_data_privacy_policy()
```

**Public Methods:**

- `def get_policy(self, policy_type`
- `def get_all_policies(self) -> list[Policy]`
- `def get_policies_by_scope(self, scope`
- `def get_policies_requiring_review(self) -> list[Policy]`
- `def get_unapproved_policies(self) -> list[Policy]`
- `def approve_policy(self, policy_type`
- `def update_policy_version(`
- `def get_policy_summary(self) -> dict[str, any]`

---

### `PolicyEngine`

**File:** `policy_engine.py`

```python
class PolicyEngine:
```

**Description:**
```
"""
Policy Enforcement Engine.

Validates actions against ethical policies and detects violations.
Provides automated enforcement for critical policy violations.

Performance Target: <20ms for policy checks
"""

def __init__(self, config: GovernanceConfig):
    """Initialize policy engine."""
    self.config = config
    self.policy_registry = PolicyRegistry()
    self.violation_count = 0
    self.enforcement_count = 0
```

**Public Methods:**

- `def enforce_policy(`
- `def enforce_all_policies(`
- `def check_action(`
- `def get_applicable_policies(self, scope`
- `def get_statistics(self) -> dict[str, int]`

---

### `SessionCreateRequest`

**File:** `api_routes.py`

```python
class SessionCreateRequest(BaseModel):
```

**Description:**
```
"""Request to create operator session."""

operator_id: str = Field(..., description="Unique operator identifier")
operator_name: str = Field(..., description="Operator display name")
operator_role: str = Field(default="soc_operator", description="Operator role")
ip_address: str | None = Field(None, description="Client IP address")
user_agent: str | None = Field(None, description="Client user agent")


class SessionCreateResponse(BaseModel):
"""Response from session creation."""

session_id: str
operator_id: str
expires_at: str
message: str = "Session created successfully"
```

**Public Methods:**


---

### `SessionCreateResponse`

**File:** `api_routes.py`

```python
class SessionCreateResponse(BaseModel):
```

**Description:**
```
"""Response from session creation."""

session_id: str
operator_id: str
expires_at: str
message: str = "Session created successfully"


class DecisionActionRequest(BaseModel):
"""Request to act on a decision."""

session_id: str = Field(..., description="Active session ID")
reasoning: str | None = Field(None, description="Reasoning for action")
comment: str | None = Field(None, description="Additional comments")
```

**Public Methods:**


---

### `DecisionActionRequest`

**File:** `api_routes.py`

```python
class DecisionActionRequest(BaseModel):
```

**Description:**
```
"""Request to act on a decision."""

session_id: str = Field(..., description="Active session ID")
reasoning: str | None = Field(None, description="Reasoning for action")
comment: str | None = Field(None, description="Additional comments")


class ApproveDecisionRequest(DecisionActionRequest):
"""Request to approve a decision.

Inherits all fields from DecisionActionRequest:
- session_id: Operator session identifier
- comment: Optional approval comments
"""

...
```

**Public Methods:**


---

### `ApproveDecisionRequest`

**File:** `api_routes.py`

```python
class ApproveDecisionRequest(DecisionActionRequest):
```

**Description:**
```
"""Request to approve a decision.

Inherits all fields from DecisionActionRequest:
- session_id: Operator session identifier
- comment: Optional approval comments
"""

...


class RejectDecisionRequest(DecisionActionRequest):
"""Request to reject a decision."""

reason: str = Field(..., description="Rejection reason (required)")
```

**Public Methods:**


---

### `RejectDecisionRequest`

**File:** `api_routes.py`

```python
class RejectDecisionRequest(DecisionActionRequest):
```

**Description:**
```
"""Request to reject a decision."""

reason: str = Field(..., description="Rejection reason (required)")


class EscalateDecisionRequest(DecisionActionRequest):
"""Request to escalate a decision."""

escalation_target: str | None = Field(None, description="Target role/person")
escalation_reason: str = Field(..., description="Why escalation is needed")


class DecisionActionResponse(BaseModel):
"""Response from decision action."""

decision_id: str
```

**Public Methods:**


---

### `EscalateDecisionRequest`

**File:** `api_routes.py`

```python
class EscalateDecisionRequest(DecisionActionRequest):
```

**Description:**
```
"""Request to escalate a decision."""

escalation_target: str | None = Field(None, description="Target role/person")
escalation_reason: str = Field(..., description="Why escalation is needed")


class DecisionActionResponse(BaseModel):
"""Response from decision action."""

decision_id: str
action: str  # "approved", "rejected", "escalated"
status: str
message: str
executed: bool | None = None
result: dict | None = None
error: str | None = None
```

**Public Methods:**


---

### `DecisionActionResponse`

**File:** `api_routes.py`

```python
class DecisionActionResponse(BaseModel):
```

**Description:**
```
"""Response from decision action."""

decision_id: str
action: str  # "approved", "rejected", "escalated"
status: str
message: str
executed: bool | None = None
result: dict | None = None
error: str | None = None


class HealthResponse(BaseModel):
"""Health check response."""

status: str
active_connections: int
```

**Public Methods:**


---

### `HealthResponse`

**File:** `api_routes.py`

```python
class HealthResponse(BaseModel):
```

**Description:**
```
"""Health check response."""

status: str
active_connections: int
total_connections: int
decisions_streamed: int
queue_size: int
timestamp: str


class PendingStatsResponse(BaseModel):
"""Pending decisions statistics."""

total_pending: int
by_risk_level: dict[str, int]
oldest_pending_seconds: int | None
```

**Public Methods:**


---

### `PendingStatsResponse`

**File:** `api_routes.py`

```python
class PendingStatsResponse(BaseModel):
```

**Description:**
```
"""Pending decisions statistics."""

total_pending: int
by_risk_level: dict[str, int]
oldest_pending_seconds: int | None
sla_violations: int


class DecisionResponse(BaseModel):
"""Individual decision response."""

decision_id: str
status: str
risk_level: str
automation_level: str
created_at: str
```

**Public Methods:**


---

### `DecisionResponse`

**File:** `api_routes.py`

```python
class DecisionResponse(BaseModel):
```

**Description:**
```
"""Individual decision response."""

decision_id: str
status: str
risk_level: str
automation_level: str
created_at: str
sla_deadline: str | None
context: dict
resolution: dict | None = None


class OperatorStatsResponse(BaseModel):
"""Operator statistics."""

operator_id: str
```

**Public Methods:**


---

### `OperatorStatsResponse`

**File:** `api_routes.py`

```python
class OperatorStatsResponse(BaseModel):
```

**Description:**
```
"""Operator statistics."""

operator_id: str
total_sessions: int
total_decisions_reviewed: int
total_approved: int
total_rejected: int
total_escalated: int
approval_rate: float
rejection_rate: float
escalation_rate: float
average_review_time: float


# ============================================================================
# API Router Factory
```

**Public Methods:**


---

### `BroadcastOptions`

**File:** `event_broadcaster.py`

```python
class BroadcastOptions:
```

**Description:**
```
"""
Options for event broadcasting.

Allows fine-grained control over event delivery.
"""

# Targeting
target_operators: list[str] | None = None  # None = all operators
target_roles: list[str] | None = None  # Filter by operator role
priority_only: RiskLevel | None = None  # Only operators handling this risk level

# Delivery
reliable: bool = True  # Retry on delivery failure
max_retries: int = 3
retry_delay: float = 1.0  # Seconds between retries
```

**Public Methods:**


---

### `EventBroadcaster`

**File:** `event_broadcaster.py`

```python
class EventBroadcaster:
```

**Description:**
```
"""
Event broadcaster for Governance SSE.

Provides high-level interface for broadcasting events to operators.
Handles event formatting, targeting, and delivery confirmation.

Usage:
    broadcaster = EventBroadcaster()
    await broadcaster.broadcast_decision_pending(decision)
    await broadcaster.broadcast_decision_resolved(decision_id, status)
"""

def __init__(self, connection_manager):
    """
    Initialize event broadcaster.
```

**Public Methods:**

- `def get_metrics(self) -> dict`
- `def clear_dedup_cache(self) -> None`

---

### `SSEEvent`

**File:** `sse_server.py`

```python
class SSEEvent:
```

**Description:**
```
"""
Server-Sent Event wrapper for HITL decisions.

Format compatible with W3C Server-Sent Events specification.
"""

# Event metadata
event_type: str  # "decision_pending", "decision_resolved", "heartbeat"
event_id: str  # Unique event ID
timestamp: str  # ISO format timestamp

# Event data
data: dict

def to_sse_format(self) -> str:
    """
```

**Public Methods:**

- `def to_sse_format(self) -> str`

---

### `OperatorConnection`

**File:** `sse_server.py`

```python
class OperatorConnection:
```

**Description:**
```
"""Active operator SSE connection."""

operator_id: str
session_id: str
queue: asyncio.Queue
connected_at: datetime
last_heartbeat: datetime

# Metrics
events_sent: int = 0
events_failed: int = 0


class ConnectionManager:
"""
Manages active SSE connections from operators.
```

**Public Methods:**


---

### `ConnectionManager`

**File:** `sse_server.py`

```python
class ConnectionManager:
```

**Description:**
```
"""
Manages active SSE connections from operators.

Responsibilities:
- Track active connections
- Route events to correct operators
- Heartbeat monitoring
- Connection cleanup
"""

def __init__(self, heartbeat_interval: int = 30):
    """
    Initialize connection manager.

    Args:
        heartbeat_interval: Seconds between heartbeats
```

**Public Methods:**

- `def get_connection(self, operator_id`

---

### `GovernanceSSEServer`

**File:** `sse_server.py`

```python
class GovernanceSSEServer:
```

**Description:**
```
"""
SSE server for streaming HITL governance decisions to operators.

Production-ready implementation with:
- Integration with existing DecisionQueue
- Multi-operator support
- Heartbeat monitoring
- Event buffering and replay
- Graceful degradation

Usage:
    server = GovernanceSSEServer(decision_queue)
    async for event in server.stream_decisions(operator_id, session_id):
        yield event.to_sse_format()
"""
```

**Public Methods:**

- `def get_health(self) -> dict`
- `def get_active_connections(self) -> int`

---

### `TestAuditLoggerInit`

**File:** `test_audit_infrastructure.py`

```python
class TestAuditLoggerInit:
```

**Description:**
```
"""Test AuditLogger initialization."""

def test_init_without_psycopg2(self, config):
    """Test initialization fails without psycopg2."""
    with patch("governance.audit_infrastructure.PSYCOPG2_AVAILABLE", False):
        with pytest.raises(ImportError, match="psycopg2 is required"):
            AuditLogger(config)

def test_init_with_valid_config(self, config, mock_psycopg2):
    """Test successful initialization."""
    logger = AuditLogger(config)

    assert logger.config == config
    assert logger.connection_params["host"] == "localhost"
    assert logger.connection_params["port"] == 5432
    assert logger.connection_params["database"] == "test_governance"
```

**Public Methods:**

- `def test_init_without_psycopg2(self, config)`
- `def test_init_with_valid_config(self, config, mock_psycopg2)`

---

### `TestSchemaInitialization`

**File:** `test_audit_infrastructure.py`

```python
class TestSchemaInitialization:
```

**Description:**
```
"""Test database schema initialization."""

def test_initialize_schema(self, audit_logger, mock_psycopg2):
    """Test schema initialization executes SQL."""
    audit_logger.initialize_schema()

    # Verify connection was established
    mock_psycopg2.connect.assert_called_once()

    # Verify SQL was executed
    mock_conn = mock_psycopg2.connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.assert_called_once()

    # Verify SCHEMA_SQL was used
    executed_sql = mock_cursor.execute.call_args[0][0]
```

**Public Methods:**

- `def test_initialize_schema(self, audit_logger, mock_psycopg2)`
- `def test_schema_creates_all_tables(self)`
- `def test_schema_creates_indexes(self)`

---

### `TestLogging`

**File:** `test_audit_infrastructure.py`

```python
class TestLogging:
```

**Description:**
```
"""Test audit logging functionality."""

def test_log_governance_action(self, audit_logger, mock_psycopg2):
    """Test logging governance action."""
    log_id = audit_logger.log(
        action=GovernanceAction.POLICY_CREATED,
        actor="test_user",
        description="Test policy created",
        target_entity_type="policy",
        target_entity_id="pol-123",
        log_level=AuditLogLevel.INFO,
    )

    assert log_id is not None

    # Verify INSERT was executed
```

**Public Methods:**

- `def test_log_governance_action(self, audit_logger, mock_psycopg2)`
- `def test_log_with_checksum(self, audit_logger)`
- `def test_log_policy_violation(self, audit_logger, mock_psycopg2)`
- `def test_log_erb_decision(self, audit_logger, mock_psycopg2)`
- `def test_log_whistleblower_report(self, audit_logger, mock_psycopg2)`

---

### `TestQuerying`

**File:** `test_audit_infrastructure.py`

```python
class TestQuerying:
```

**Description:**
```
"""Test audit log querying."""

def test_query_logs_no_filters(self, audit_logger, mock_psycopg2):
    """Test querying logs without filters."""
    # Setup mock return
    mock_conn = mock_psycopg2.connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []

    logs = audit_logger.query_logs()

    assert isinstance(logs, list)

    # Verify query was executed
    mock_cursor.execute.assert_called_once()
    sql_call = mock_cursor.execute.call_args[0][0]
```

**Public Methods:**

- `def test_query_logs_no_filters(self, audit_logger, mock_psycopg2)`
- `def test_query_logs_with_date_range(self, audit_logger, mock_psycopg2)`
- `def test_query_logs_with_action_filter(self, audit_logger, mock_psycopg2)`
- `def test_query_logs_with_actor_filter(self, audit_logger, mock_psycopg2)`
- `def test_query_logs_with_log_level_filter(self, audit_logger, mock_psycopg2)`
- `def test_query_logs_pagination(self, audit_logger, mock_psycopg2)`

---

### `TestIntegrity`

**File:** `test_audit_infrastructure.py`

```python
class TestIntegrity:
```

**Description:**
```
"""Test audit log integrity verification."""

def test_verify_integrity_valid(self, audit_logger, mock_psycopg2):
    """Test integrity verification for valid log."""
    mock_conn = mock_psycopg2.connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = [True]

    is_valid = audit_logger.verify_integrity("log-123")

    assert is_valid is True

    # Verify function was called
    sql_call = mock_cursor.execute.call_args[0][0]
    assert "verify_audit_log_integrity" in sql_call
```

**Public Methods:**

- `def test_verify_integrity_valid(self, audit_logger, mock_psycopg2)`
- `def test_verify_integrity_tampered(self, audit_logger, mock_psycopg2)`
- `def test_calculate_checksum_deterministic(self, audit_logger)`
- `def test_calculate_checksum_different_inputs(self, audit_logger)`

---

### `TestRetention`

**File:** `test_audit_infrastructure.py`

```python
class TestRetention:
```

**Description:**
```
"""Test GDPR 7-year retention policy."""

def test_apply_retention_policy(self, audit_logger, mock_psycopg2):
    """Test retention policy execution."""
    mock_conn = mock_psycopg2.connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = [42]  # 42 logs deleted

    deleted_count = audit_logger.apply_retention_policy()

    assert deleted_count == 42

    # Verify function was called
    sql_call = mock_cursor.execute.call_args[0][0]
    assert "apply_retention_policy" in sql_call
```

**Public Methods:**

- `def test_apply_retention_policy(self, audit_logger, mock_psycopg2)`
- `def test_retention_deletes_old_logs(self)`
- `def test_retention_no_logs_to_delete(self, audit_logger, mock_psycopg2)`

---

### `TestExport`

**File:** `test_audit_infrastructure.py`

```python
class TestExport:
```

**Description:**
```
"""Test audit log export for external auditors."""

def test_export_json_format(self, audit_logger, mock_psycopg2):
    """Test export in JSON format."""
    # Setup mock data
    mock_logs = [
        {
            "log_id": "log-1",
            "timestamp": datetime(2025, 10, 14),
            "action": "policy_created",
            "actor": "user1",
        },
        {
            "log_id": "log-2",
            "timestamp": datetime(2025, 10, 13),
            "action": "policy_violated",
```

**Public Methods:**

- `def test_export_json_format(self, audit_logger, mock_psycopg2)`
- `def test_export_csv_format(self, audit_logger, mock_psycopg2)`
- `def test_export_csv_empty_data(self, audit_logger, mock_psycopg2)`
- `def test_export_invalid_format(self, audit_logger, mock_psycopg2)`

---

### `TestStatistics`

**File:** `test_audit_infrastructure.py`

```python
class TestStatistics:
```

**Description:**
```
"""Test audit log statistics generation."""

def test_get_statistics(self, audit_logger, mock_psycopg2):
    """Test statistics generation."""
    mock_conn = mock_psycopg2.connect.return_value
    mock_cursor = mock_conn.cursor.return_value

    # Mock multiple queries
    mock_cursor.fetchone.side_effect = [
        [1000],  # total_logs
        [150],  # logs_last_30_days
    ]

    mock_cursor.fetchall.side_effect = [
        [("policy_created", 50), ("policy_violated", 30)],  # top_actions
        [("user1", 100), ("user2", 80)],  # top_actors
```

**Public Methods:**

- `def test_get_statistics(self, audit_logger, mock_psycopg2)`
- `def test_get_statistics_empty_database(self, audit_logger, mock_psycopg2)`

---

### `TestEnums`

**File:** `test_base_100pct.py`

```python
class TestEnums:
```

**Description:**
```
"""Test all enum values."""

def test_policy_type_values(self):
    """Test PolicyType enum values."""
    assert PolicyType.ETHICAL_USE.value == "ethical_use"
    assert PolicyType.RED_TEAMING.value == "red_teaming"
    assert PolicyType.DATA_PRIVACY.value == "data_privacy"
    assert PolicyType.INCIDENT_RESPONSE.value == "incident_response"
    assert PolicyType.WHISTLEBLOWER.value == "whistleblower"

def test_policy_severity_values(self):
    """Test PolicySeverity enum values."""
    assert PolicySeverity.INFO.value == "info"
    assert PolicySeverity.LOW.value == "low"
    assert PolicySeverity.MEDIUM.value == "medium"
    assert PolicySeverity.HIGH.value == "high"
```

**Public Methods:**

- `def test_policy_type_values(self)`
- `def test_policy_severity_values(self)`
- `def test_erb_member_role_values(self)`
- `def test_decision_type_values(self)`
- `def test_audit_log_level_values(self)`
- `def test_governance_action_values(self)`

---

### `TestGovernanceConfig`

**File:** `test_base_100pct.py`

```python
class TestGovernanceConfig:
```

**Description:**
```
"""Test GovernanceConfig dataclass."""

def test_config_defaults(self):
    """Test GovernanceConfig default values."""
    config = GovernanceConfig()

    assert config.erb_meeting_frequency_days == 30
    assert config.erb_quorum_percentage == 0.6
    assert config.erb_decision_threshold == 0.75
    assert config.policy_review_frequency_days == 365
    assert config.auto_enforce_policies is True
    assert config.policy_violation_alert_threshold == PolicySeverity.MEDIUM
    assert config.audit_retention_days == 2555  # 7 years
    assert config.audit_log_level == AuditLogLevel.INFO
    assert config.enable_blockchain_audit is False
    assert config.whistleblower_anonymity is True
```

**Public Methods:**

- `def test_config_defaults(self)`
- `def test_config_custom_values(self)`

---

### `TestERBMember`

**File:** `test_base_100pct.py`

```python
class TestERBMember:
```

**Description:**
```
"""Test ERBMember dataclass."""

def test_erb_member_defaults(self):
    """Test ERBMember default values."""
    member = ERBMember()

    assert member.member_id != ""
    assert member.name == ""
    assert member.email == ""
    assert member.role == ERBMemberRole.TECHNICAL_MEMBER
    assert member.organization == ""
    assert member.expertise == []
    assert member.is_internal is True
    assert member.is_active is True
    assert member.voting_rights is True
    assert isinstance(member.appointed_date, datetime)
```

**Public Methods:**

- `def test_erb_member_defaults(self)`
- `def test_erb_member_is_voting_member_active_no_term(self)`
- `def test_erb_member_is_voting_member_active_future_term(self)`
- `def test_erb_member_is_voting_member_expired_term(self)`
- `def test_erb_member_is_voting_member_inactive(self)`
- `def test_erb_member_is_voting_member_no_rights(self)`
- `def test_erb_member_to_dict(self)`
- `def test_erb_member_to_dict_with_term_end(self)`

---

### `TestERBMeeting`

**File:** `test_base_100pct.py`

```python
class TestERBMeeting:
```

**Description:**
```
"""Test ERBMeeting dataclass."""

def test_erb_meeting_defaults(self):
    """Test ERBMeeting default values."""
    meeting = ERBMeeting()

    assert meeting.meeting_id != ""
    assert isinstance(meeting.scheduled_date, datetime)
    assert meeting.actual_date is None
    assert meeting.duration_minutes == 120
    assert meeting.location == "Virtual"
    assert meeting.agenda == []
    assert meeting.attendees == []
    assert meeting.absentees == []
    assert meeting.minutes == ""
    assert meeting.decisions == []
```

**Public Methods:**

- `def test_erb_meeting_defaults(self)`
- `def test_erb_meeting_to_dict(self)`
- `def test_erb_meeting_to_dict_with_actual_date(self)`

---

### `TestERBDecision`

**File:** `test_base_100pct.py`

```python
class TestERBDecision:
```

**Description:**
```
"""Test ERBDecision dataclass."""

def test_erb_decision_defaults(self):
    """Test ERBDecision default values."""
    decision = ERBDecision()

    assert decision.decision_id != ""
    assert decision.meeting_id == ""
    assert decision.title == ""
    assert decision.description == ""
    assert decision.decision_type == DecisionType.APPROVED
    assert decision.votes_for == 0
    assert decision.votes_against == 0
    assert decision.votes_abstain == 0
    assert decision.rationale == ""
    assert decision.conditions == []
```

**Public Methods:**

- `def test_erb_decision_defaults(self)`
- `def test_erb_decision_is_approved_fully(self)`
- `def test_erb_decision_is_approved_conditionally(self)`
- `def test_erb_decision_is_approved_rejected(self)`
- `def test_erb_decision_is_approved_deferred(self)`
- `def test_erb_decision_approval_percentage(self)`
- `def test_erb_decision_approval_percentage_zero_votes(self)`
- `def test_erb_decision_to_dict(self)`
- `def test_erb_decision_to_dict_with_follow_up(self)`

---

### `TestPolicy`

**File:** `test_base_100pct.py`

```python
class TestPolicy:
```

**Description:**
```
"""Test Policy dataclass."""

def test_policy_defaults(self):
    """Test Policy default values."""
    policy = Policy()

    assert policy.policy_id != ""
    assert policy.policy_type == PolicyType.ETHICAL_USE
    assert policy.version == "1.0"
    assert policy.title == ""
    assert policy.description == ""
    assert policy.rules == []
    assert policy.scope == "all"
    assert policy.enforcement_level == PolicySeverity.MEDIUM
    assert policy.auto_enforce is True
    assert isinstance(policy.created_date, datetime)
```

**Public Methods:**

- `def test_policy_defaults(self)`
- `def test_policy_is_due_for_review_no_date(self)`
- `def test_policy_is_due_for_review_future_date(self)`
- `def test_policy_is_due_for_review_past_date(self)`
- `def test_policy_days_until_review_no_date(self)`
- `def test_policy_days_until_review_future_date(self)`
- `def test_policy_days_until_review_past_date(self)`
- `def test_policy_to_dict(self)`

---

### `TestPolicyViolation`

**File:** `test_base_100pct.py`

```python
class TestPolicyViolation:
```

**Description:**
```
"""Test PolicyViolation dataclass."""

def test_policy_violation_defaults(self):
    """Test PolicyViolation default values."""
    violation = PolicyViolation()

    assert violation.violation_id != ""
    assert violation.policy_id == ""
    assert violation.policy_type == PolicyType.ETHICAL_USE
    assert violation.severity == PolicySeverity.MEDIUM
    assert violation.title == ""
    assert violation.description == ""
    assert violation.violated_rule == ""
    assert violation.detection_method == "automated"
    assert violation.detected_by == "system"
    assert isinstance(violation.detected_date, datetime)
```

**Public Methods:**

- `def test_policy_violation_defaults(self)`
- `def test_policy_violation_is_overdue_no_deadline(self)`
- `def test_policy_violation_is_overdue_completed(self)`
- `def test_policy_violation_is_overdue_past_deadline(self)`
- `def test_policy_violation_is_overdue_future_deadline(self)`
- `def test_policy_violation_days_until_deadline_no_deadline(self)`
- `def test_policy_violation_days_until_deadline_future(self)`
- `def test_policy_violation_to_dict(self)`

---

### `TestAuditLog`

**File:** `test_base_100pct.py`

```python
class TestAuditLog:
```

**Description:**
```
"""Test AuditLog dataclass."""

def test_audit_log_defaults(self):
    """Test AuditLog default values."""
    log = AuditLog()

    assert log.log_id != ""
    assert isinstance(log.timestamp, datetime)
    assert log.action == GovernanceAction.AUDIT_LOG_CREATED
    assert log.log_level == AuditLogLevel.INFO
    assert log.actor == "system"
    assert log.target_entity_type == ""
    assert log.target_entity_id == ""
    assert log.description == ""
    assert log.details == {}
    assert log.ip_address is None
```

**Public Methods:**

- `def test_audit_log_defaults(self)`
- `def test_audit_log_to_dict(self)`

---

### `TestWhistleblowerReport`

**File:** `test_base_100pct.py`

```python
class TestWhistleblowerReport:
```

**Description:**
```
"""Test WhistleblowerReport dataclass."""

def test_whistleblower_report_defaults(self):
    """Test WhistleblowerReport default values."""
    report = WhistleblowerReport()

    assert report.report_id != ""
    assert isinstance(report.submission_date, datetime)
    assert report.reporter_id is None
    assert report.is_anonymous is True
    assert report.title == ""
    assert report.description == ""
    assert report.alleged_violation_type == PolicyType.ETHICAL_USE
    assert report.severity == PolicySeverity.MEDIUM
    assert report.affected_systems == []
    assert report.evidence == []
```

**Public Methods:**

- `def test_whistleblower_report_defaults(self)`
- `def test_whistleblower_report_is_under_investigation_under_review(self)`
- `def test_whistleblower_report_is_under_investigation_investigated(self)`
- `def test_whistleblower_report_is_under_investigation_submitted(self)`
- `def test_whistleblower_report_is_resolved_resolved(self)`
- `def test_whistleblower_report_is_resolved_dismissed(self)`
- `def test_whistleblower_report_is_resolved_submitted(self)`
- `def test_whistleblower_report_to_dict_anonymous(self)`
- `def test_whistleblower_report_to_dict_non_anonymous(self)`

---

### `TestGovernanceResult`

**File:** `test_base_100pct.py`

```python
class TestGovernanceResult:
```

**Description:**
```
"""Test GovernanceResult dataclass."""

def test_governance_result_defaults(self):
    """Test GovernanceResult default values."""
    result = GovernanceResult()

    assert result.success is True
    assert result.message == ""
    assert result.entity_id is None
    assert result.entity_type == ""
    assert result.warnings == []
    assert result.errors == []
    assert result.metadata == {}

def test_governance_result_to_dict(self):
    """Test GovernanceResult.to_dict()."""
```

**Public Methods:**

- `def test_governance_result_defaults(self)`
- `def test_governance_result_to_dict(self)`

---

### `TestPolicyEnforcementResult`

**File:** `test_base_100pct.py`

```python
class TestPolicyEnforcementResult:
```

**Description:**
```
"""Test PolicyEnforcementResult dataclass."""

def test_policy_enforcement_result_defaults(self):
    """Test PolicyEnforcementResult default values."""
    result = PolicyEnforcementResult()

    assert result.is_compliant is True
    assert result.policy_id == ""
    assert result.policy_type == PolicyType.ETHICAL_USE
    assert result.checked_rules == 0
    assert result.passed_rules == 0
    assert result.failed_rules == 0
    assert result.violations == []
    assert result.warnings == []
    assert isinstance(result.timestamp, datetime)
    assert result.metadata == {}
```

**Public Methods:**

- `def test_policy_enforcement_result_defaults(self)`
- `def test_policy_enforcement_result_compliance_percentage(self)`
- `def test_policy_enforcement_result_compliance_percentage_zero_rules(self)`
- `def test_policy_enforcement_result_to_dict(self)`

---

### `TestLeiZeroFlorescimentoHumano`

**File:** `test_constitutional_scenarios.py`

```python
class TestLeiZeroFlorescimentoHumano:
```

**Description:**
```
"""
Lei Zero: Imperativo do Florescimento Humano

Nenhuma otimização de sistema pode comprometer o florescimento humano.
O sistema deve proteger transparência, dignidade e bem-estar.
"""

def test_lei_zero_audit_trail_protects_transparency(self, policy_registry):
    """
    Lei Zero: Audit trail protege transparência.

    Cenário: Sistema DEVE manter audit trail completo para transparência.
    """
    # Data Privacy Policy enforces audit requirements
    policy = policy_registry.get_policy(PolicyType.DATA_PRIVACY)
```

**Public Methods:**

- `def test_lei_zero_audit_trail_protects_transparency(self, policy_registry)`
- `def test_lei_zero_whistleblower_protection_enables_flourishing(self, policy_engine)`
- `def test_lei_zero_data_subject_rights_protected(self, policy_engine)`
- `def test_lei_zero_ethical_use_prevents_harm(self, policy_engine)`
- `def test_lei_zero_critical_decisions_require_oversight(self, policy_engine)`
- `def test_lei_zero_transparency_in_ai_decisions(self, policy_engine)`

---

### `TestLeiIAxiomaOvelhaPerdida`

**File:** `test_constitutional_scenarios.py`

```python
class TestLeiIAxiomaOvelhaPerdida:
```

**Description:**
```
"""
Lei I: Axioma da Ovelha Perdida

Nenhuma otimização utilitarista justifica o abandono de um vulnerável.
O sistema deve priorizar proteção de minorias e indivíduos afetados.
"""

def test_lei_i_data_privacy_protects_vulnerable(self, policy_engine):
    """
    Lei I: Privacidade protege vulneráveis.

    Cenário: Dados pessoais SEM base legal viola Lei I (proteção do indivíduo).
    """
    # Collecting personal data without legal basis (PROHIBITED)
    result = policy_engine.enforce_policy(
        policy_type=PolicyType.DATA_PRIVACY,
```

**Public Methods:**

- `def test_lei_i_data_privacy_protects_vulnerable(self, policy_engine)`
- `def test_lei_i_incident_response_prioritizes_affected(self, policy_engine)`
- `def test_lei_i_no_discrimination_against_minorities(self, policy_engine)`
- `def test_lei_i_data_breach_notification_protects_affected(self, policy_engine)`
- `def test_lei_i_red_team_operations_respect_individuals(self, policy_engine)`
- `def test_lei_i_high_risk_actions_require_hitl(self, policy_engine)`

---

### `TestLeiZeroAndLeiIIntegration`

**File:** `test_constitutional_scenarios.py`

```python
class TestLeiZeroAndLeiIIntegration:
```

**Description:**
```
"""
Integration tests for Lei Zero and Lei I working together.

These laws form the constitutional foundation of the system.
"""

def test_constitutional_foundation_erb_governance(self, erb_manager):
    """
    Lei Zero + Lei I: ERB é o guardião constitucional.

    Cenário: ERB deve existir e funcionar para garantir ambas as leis.
    """
    # Add ERB members (governance structure)
    result = erb_manager.add_member(
        name="Dr. Ethics Chair",
        email="chair@vertice.ai",
```

**Public Methods:**

- `def test_constitutional_foundation_erb_governance(self, erb_manager)`
- `def test_constitutional_enforcement_all_policies_approved(self, policy_registry)`
- `def test_constitutional_violations_escalate_to_erb(self, policy_engine)`

---

### `TestMemberManagement`

**File:** `test_erb_100pct.py`

```python
class TestMemberManagement:
```

**Description:**
```
"""Test ERB member management."""

def test_add_member_success(self, erb_manager):
    """Test successfully adding member."""
    result = erb_manager.add_member(
        name="Dr. Test",
        email="test@vertice.ai",
        role=ERBMemberRole.TECHNICAL_MEMBER,
        organization="Test Org",
        expertise=["Testing"],
    )

    assert result.success
    assert result.entity_id is not None
    assert erb_manager.stats["total_members"] == 1
    assert erb_manager.stats["active_members"] == 1
```

**Public Methods:**

- `def test_add_member_success(self, erb_manager)`
- `def test_add_member_missing_name(self, erb_manager)`
- `def test_add_member_missing_email(self, erb_manager)`
- `def test_add_member_duplicate_email(self, erb_manager)`
- `def test_add_member_with_term(self, erb_manager)`
- `def test_add_member_no_voting_rights(self, erb_manager)`
- `def test_remove_member_success(self, populated_erb)`
- `def test_remove_member_not_found(self, erb_manager)`
- `def test_remove_member_already_inactive(self, populated_erb)`
- `def test_get_active_members(self, populated_erb)`
- `def test_get_voting_members(self, populated_erb)`
- `def test_get_member_by_role(self, populated_erb)`
- `def test_get_chair(self, populated_erb)`
- `def test_get_chair_none(self, erb_manager)`

---

### `TestMeetingManagement`

**File:** `test_erb_100pct.py`

```python
class TestMeetingManagement:
```

**Description:**
```
"""Test ERB meeting management."""

def test_schedule_meeting_success(self, erb_manager):
    """Test successfully scheduling meeting."""
    future_date = datetime.utcnow() + timedelta(days=7)

    result = erb_manager.schedule_meeting(
        scheduled_date=future_date,
        agenda=["Item 1", "Item 2"],
        duration_minutes=120,
        location="Virtual",
    )

    assert result.success
    assert result.entity_id is not None
    assert erb_manager.stats["total_meetings"] == 1
```

**Public Methods:**

- `def test_schedule_meeting_success(self, erb_manager)`
- `def test_schedule_meeting_past_date(self, erb_manager)`
- `def test_record_attendance_meeting_not_found(self, erb_manager)`
- `def test_record_attendance_quorum_met(self, populated_erb)`
- `def test_record_attendance_quorum_not_met(self, populated_erb)`
- `def test_add_meeting_minutes_success(self, populated_erb)`
- `def test_add_meeting_minutes_not_found(self, erb_manager)`

---

### `TestDecisionManagement`

**File:** `test_erb_100pct.py`

```python
class TestDecisionManagement:
```

**Description:**
```
"""Test ERB decision management."""

def test_record_decision_meeting_not_found(self, erb_manager):
    """Test recording decision for nonexistent meeting."""
    result = erb_manager.record_decision(
        meeting_id="nonexistent-meeting",
        title="Test Decision",
        description="Test",
        votes_for=5,
        votes_against=1,
    )

    assert not result.success
    assert "not found" in result.message.lower()

def test_record_decision_quorum_not_met(self, populated_erb):
```

**Public Methods:**

- `def test_record_decision_meeting_not_found(self, erb_manager)`
- `def test_record_decision_quorum_not_met(self, populated_erb)`
- `def test_record_decision_no_votes(self, populated_erb)`
- `def test_record_decision_approved(self, populated_erb)`
- `def test_record_decision_rejected(self, populated_erb)`
- `def test_record_decision_conditional(self, populated_erb)`
- `def test_record_decision_with_follow_up(self, populated_erb)`
- `def test_get_decision(self, populated_erb)`
- `def test_get_decision_none(self, erb_manager)`
- `def test_get_decisions_by_meeting(self, populated_erb)`
- `def test_get_decisions_by_policy(self, populated_erb)`
- `def test_get_pending_follow_ups(self, populated_erb)`
- `def test_get_overdue_follow_ups(self, populated_erb)`

---

### `TestQuorumVoting`

**File:** `test_erb_100pct.py`

```python
class TestQuorumVoting:
```

**Description:**
```
"""Test quorum and voting utilities."""

def test_check_quorum_met(self, populated_erb):
    """Test quorum check when met."""
    voting_members = populated_erb.get_voting_members()
    attendee_ids = [m.member_id for m in voting_members]

    quorum_met, stats = populated_erb.check_quorum(attendee_ids)

    assert quorum_met
    assert stats["voting_attendees"] == len(voting_members)

def test_check_quorum_not_met(self, populated_erb):
    """Test quorum check when not met."""
    quorum_met, stats = populated_erb.check_quorum([])
```

**Public Methods:**

- `def test_check_quorum_met(self, populated_erb)`
- `def test_check_quorum_not_met(self, populated_erb)`
- `def test_calculate_approval_approved(self, erb_manager)`
- `def test_calculate_approval_rejected(self, erb_manager)`
- `def test_calculate_approval_no_votes(self, erb_manager)`

---

### `TestReporting`

**File:** `test_erb_100pct.py`

```python
class TestReporting:
```

**Description:**
```
"""Test ERB reporting and statistics."""

def test_get_stats(self, populated_erb):
    """Test getting ERB statistics."""
    stats = populated_erb.get_stats()

    assert "total_members" in stats
    assert "active_members" in stats
    assert stats["total_members"] == 3
    assert stats["active_members"] == 3

def test_get_member_participation(self, populated_erb):
    """Test getting member participation stats."""
    # Create meeting and record attendance
    future_date = datetime.utcnow() + timedelta(days=7)
    meeting_result = populated_erb.schedule_meeting(
```

**Public Methods:**

- `def test_get_stats(self, populated_erb)`
- `def test_get_member_participation(self, populated_erb)`
- `def test_get_member_participation_with_inactive(self, populated_erb)`
- `def test_generate_summary_report(self, populated_erb)`
- `def test_generate_summary_report_with_data(self, populated_erb)`

---

### `TestEventSubscription`

**File:** `test_governance_engine_edge_cases.py`

```python
class TestEventSubscription:
```

**Description:**
```
"""Test event subscription and streaming."""

def test_subscribe_decision_events(self, engine):
    """Test subscribing to decision events."""
    events = list(engine.subscribe_decision_events())

    # Should yield existing decisions as events
    assert isinstance(events, list)
    assert len(events) == 3  # 3 mock decisions from init

    # Each event should have type and decision
    for event in events:
        assert event["type"] == "new_decision"
        assert "decision" in event
        assert isinstance(event["decision"], Decision)
```

**Public Methods:**

- `def test_subscribe_decision_events(self, engine)`
- `def test_subscribe_events(self, engine)`
- `def test_emit_event_to_subscribers(self, engine)`
- `def test_emit_event_multiple_subscribers(self, engine)`

---

### `TestDecisionExpiration`

**File:** `test_governance_engine_edge_cases.py`

```python
class TestDecisionExpiration:
```

**Description:**
```
"""Test decision expiration logic."""

def test_is_expired_no_expiry(self):
    """Test decision with no expiry is never expired."""
    decision = Decision(
        operation_type="TEST",
        context={},
        risk=RiskAssessment(),
        expires_at=None,  # No expiry
    )

    assert decision.is_expired() is False

def test_is_expired_future_expiry(self):
    """Test decision with future expiry is not expired."""
    future_time = datetime.utcnow() + timedelta(hours=1)
```

**Public Methods:**

- `def test_is_expired_no_expiry(self)`
- `def test_is_expired_future_expiry(self)`
- `def test_is_expired_past_expiry(self)`
- `def test_time_remaining_no_expiry(self)`
- `def test_time_remaining_future_expiry(self)`
- `def test_time_remaining_expired(self)`

---

### `TestGetPendingDecisionsEdgeCases`

**File:** `test_governance_engine_edge_cases.py`

```python
class TestGetPendingDecisionsEdgeCases:
```

**Description:**
```
"""Test edge cases for get_pending_decisions."""

def test_get_pending_decisions_empty_status_filter(self, engine):
    """Test with empty status filter."""
    decisions = engine.get_pending_decisions(status="")

    # Should return all decisions
    assert len(decisions) > 0

def test_get_pending_decisions_priority_sorting(self, engine):
    """Test priority-based sorting."""
    # Add decisions with different priorities
    engine.create_decision(
        operation_type="LOW_PRIORITY",
        context={},
        risk=RiskAssessment(score=0.3, level="LOW"),
```

**Public Methods:**

- `def test_get_pending_decisions_empty_status_filter(self, engine)`
- `def test_get_pending_decisions_priority_sorting(self, engine)`
- `def test_get_pending_decisions_limit_applied(self, engine)`

---

### `TestUpdateDecisionStatusEdgeCases`

**File:** `test_governance_engine_edge_cases.py`

```python
class TestUpdateDecisionStatusEdgeCases:
```

**Description:**
```
"""Test edge cases for update_decision_status."""

def test_update_decision_status_nonexistent(self, engine):
    """Test updating nonexistent decision returns False."""
    result = engine.update_decision_status(
        decision_id="nonexistent-id",
        status=DecisionStatus.APPROVED,
        operator_id="operator-1",
    )

    assert result is False

def test_update_decision_status_sets_resolved_at(self, engine, sample_decision):
    """Test update sets resolved_at timestamp."""
    engine.decisions[sample_decision.decision_id] = sample_decision
```

**Public Methods:**

- `def test_update_decision_status_nonexistent(self, engine)`
- `def test_update_decision_status_sets_resolved_at(self, engine, sample_decision)`
- `def test_update_decision_status_emits_event(self, engine, sample_decision)`

---

### `TestCreateDecisionEdgeCases`

**File:** `test_governance_engine_edge_cases.py`

```python
class TestCreateDecisionEdgeCases:
```

**Description:**
```
"""Test edge cases for create_decision."""

def test_create_decision_emits_new_decision_event(self, engine):
    """Test create_decision emits new_decision event."""
    received_events = []

    def subscriber(event):
        received_events.append(event)

    engine._event_subscribers.append(subscriber)

    decision = engine.create_decision(
        operation_type="TEST_OP",
        context={"test": "data"},
        risk=RiskAssessment(score=0.5, level="MEDIUM"),
    )
```

**Public Methods:**

- `def test_create_decision_emits_new_decision_event(self, engine)`
- `def test_create_decision_calculates_expiry(self, engine)`

---

### `TestGetMetricsEdgeCases`

**File:** `test_governance_engine_edge_cases.py`

```python
class TestGetMetricsEdgeCases:
```

**Description:**
```
"""Test edge cases for get_metrics."""

def test_get_metrics_zero_resolved_decisions(self, engine):
    """Test metrics with no resolved decisions."""
    # All mock decisions are pending
    metrics = engine.get_metrics()

    # Should not crash, avg_response_time should be 0
    assert metrics["avg_response_time"] == 0.0
    assert metrics["approval_rate"] == 0.0

def test_get_metrics_sla_violations(self, engine):
    """Test SLA violation counting."""
    # Create decision and resolve it after SLA
    decision = engine.create_decision(
        operation_type="SLOW_OP",
```

**Public Methods:**

- `def test_get_metrics_zero_resolved_decisions(self, engine)`
- `def test_get_metrics_sla_violations(self, engine)`
- `def test_get_metrics_approval_rate_calculation(self, engine)`

---

### `TestGovernanceEngineInit`

**File:** `test_governance_engine.py`

```python
class TestGovernanceEngineInit:
```

**Description:**
```
"""Test GovernanceEngine initialization."""

def test_engine_initializes_with_mock_decisions(self, governance_engine):
    """Test that engine initializes with 3 mock decisions (POC)."""
    assert len(governance_engine.decisions) == 3
    assert "dec-001" in governance_engine.decisions
    assert "dec-002" in governance_engine.decisions
    assert "dec-003" in governance_engine.decisions

def test_engine_initializes_uptime_tracking(self, governance_engine):
    """Test that engine starts uptime tracking."""
    assert governance_engine.start_time > 0
    uptime = governance_engine.get_uptime()
    assert uptime >= 0

def test_engine_initializes_event_subscribers_list(self, governance_engine):
```

**Public Methods:**

- `def test_engine_initializes_with_mock_decisions(self, governance_engine)`
- `def test_engine_initializes_uptime_tracking(self, governance_engine)`
- `def test_engine_initializes_event_subscribers_list(self, governance_engine)`
- `def test_mock_decision_1_high_risk_exploit(self, governance_engine)`
- `def test_mock_decision_2_lateral_movement(self, governance_engine)`
- `def test_mock_decision_3_data_exfiltration(self, governance_engine)`

---

### `TestDecisionLifecycle`

**File:** `test_governance_engine.py`

```python
class TestDecisionLifecycle:
```

**Description:**
```
"""Test decision creation, retrieval, and updates."""

def test_create_decision(self, governance_engine, sample_risk_assessment):
    """Test creating a new decision."""
    initial_count = len(governance_engine.decisions)

    decision = governance_engine.create_decision(
        operation_type="TEST_OPERATION",
        context={"key": "value"},
        risk=sample_risk_assessment,
        priority="HIGH",
        sla_seconds=600,
    )

    assert decision.operation_type == "TEST_OPERATION"
    assert decision.context == {"key": "value"}
```

**Public Methods:**

- `def test_create_decision(self, governance_engine, sample_risk_assessment)`
- `def test_create_decision_with_defaults(self, governance_engine, sample_risk_assessment)`
- `def test_get_decision_existing(self, governance_engine)`
- `def test_get_decision_nonexistent(self, governance_engine)`
- `def test_update_decision_status_approved(self, governance_engine)`
- `def test_update_decision_status_rejected(self, governance_engine)`
- `def test_update_decision_status_nonexistent(self, governance_engine)`

---

### `TestDecisionFiltering`

**File:** `test_governance_engine.py`

```python
class TestDecisionFiltering:
```

**Description:**
```
"""Test decision filtering and sorting logic."""

def test_get_pending_decisions_all(self, governance_engine):
    """Test getting all pending decisions."""
    decisions = governance_engine.get_pending_decisions()

    # All 3 mock decisions start as PENDING
    assert len(decisions) == 3

def test_get_pending_decisions_sorted_by_priority(self, governance_engine):
    """Test that pending decisions are sorted by priority."""
    decisions = governance_engine.get_pending_decisions()

    # Order should be: CRITICAL, HIGH, MEDIUM
    assert decisions[0].priority == "CRITICAL"  # dec-003
    assert decisions[1].priority == "HIGH"  # dec-001
```

**Public Methods:**

- `def test_get_pending_decisions_all(self, governance_engine)`
- `def test_get_pending_decisions_sorted_by_priority(self, governance_engine)`
- `def test_get_pending_decisions_filter_by_priority(self, governance_engine)`
- `def test_get_pending_decisions_filter_by_status(self, governance_engine)`
- `def test_get_pending_decisions_with_limit(self, governance_engine)`
- `def test_get_pending_decisions_limit_one(self, governance_engine)`
- `def test_get_pending_decisions_combined_filters(self, governance_engine)`

---

### `TestDecisionExpiration`

**File:** `test_governance_engine.py`

```python
class TestDecisionExpiration:
```

**Description:**
```
"""Test decision expiration logic."""

def test_decision_is_not_expired_when_no_expiry(self):
    """Test decision without expiry is never expired."""
    decision = Decision()
    decision.expires_at = None

    assert decision.is_expired() is False

def test_decision_is_not_expired_when_future_expiry(self):
    """Test decision with future expiry is not expired."""
    decision = Decision()
    decision.expires_at = datetime.utcnow() + timedelta(minutes=10)

    assert decision.is_expired() is False
```

**Public Methods:**

- `def test_decision_is_not_expired_when_no_expiry(self)`
- `def test_decision_is_not_expired_when_future_expiry(self)`
- `def test_decision_is_expired_when_past_expiry(self)`
- `def test_time_remaining_with_no_expiry(self)`
- `def test_time_remaining_with_future_expiry(self)`
- `def test_time_remaining_with_past_expiry(self)`

---

### `TestMetrics`

**File:** `test_governance_engine.py`

```python
class TestMetrics:
```

**Description:**
```
"""Test governance metrics calculation."""

def test_get_metrics_initial_state(self, governance_engine):
    """Test metrics in initial state (3 pending mock decisions)."""
    metrics = governance_engine.get_metrics()

    assert metrics["total_decisions"] == 3
    assert metrics["pending_count"] == 3
    assert metrics["approved_count"] == 0
    assert metrics["rejected_count"] == 0
    assert metrics["escalated_count"] == 0
    assert metrics["critical_count"] == 1
    assert metrics["high_priority_count"] == 1
    assert metrics["avg_response_time"] == 0.0
    assert metrics["approval_rate"] == 0.0
    assert metrics["sla_violations"] == 0
```

**Public Methods:**

- `def test_get_metrics_initial_state(self, governance_engine)`
- `def test_get_metrics_after_approval(self, governance_engine)`
- `def test_get_metrics_approval_rate(self, governance_engine)`
- `def test_get_metrics_sla_violations(self, governance_engine, sample_risk_assessment)`
- `def test_get_metrics_avg_response_time(self, governance_engine)`
- `def test_get_metrics_escalated_count(self, governance_engine)`

---

### `TestEventStreaming`

**File:** `test_governance_engine.py`

```python
class TestEventStreaming:
```

**Description:**
```
"""Test event streaming functionality."""

def test_subscribe_decision_events_yields_all_decisions(self, governance_engine):
    """Test that subscribe_decision_events yields all decisions."""
    events = list(governance_engine.subscribe_decision_events())

    assert len(events) == 3
    assert all(event["type"] == "new_decision" for event in events)
    assert all("decision" in event for event in events)

def test_subscribe_events_yields_connection_established(self, governance_engine):
    """Test that subscribe_events yields connection event."""
    events = list(governance_engine.subscribe_events())

    assert len(events) == 1
    assert events[0]["type"] == "connection_established"
```

**Public Methods:**

- `def test_subscribe_decision_events_yields_all_decisions(self, governance_engine)`
- `def test_subscribe_events_yields_connection_established(self, governance_engine)`
- `def test_subscribe_events_includes_metrics(self, governance_engine)`

---

### `TestDecisionDataclass`

**File:** `test_governance_engine.py`

```python
class TestDecisionDataclass:
```

**Description:**
```
"""Test Decision dataclass defaults and behavior."""

def test_decision_default_initialization(self):
    """Test Decision initializes with defaults."""
    decision = Decision()

    assert decision.operation_type == ""
    assert decision.context == {}
    assert decision.status == DecisionStatus.PENDING
    assert decision.priority == "MEDIUM"
    assert decision.sla_seconds == 300
    assert decision.operator_id is None
    assert decision.operator_comment == ""
    assert decision.operator_reasoning == ""
    assert decision.resolved_at is None
```

**Public Methods:**

- `def test_decision_default_initialization(self)`
- `def test_decision_generates_unique_id(self)`
- `def test_decision_created_at_defaults_to_now(self)`

---

### `TestRiskAssessment`

**File:** `test_governance_engine.py`

```python
class TestRiskAssessment:
```

**Description:**
```
"""Test RiskAssessment dataclass."""

def test_risk_assessment_defaults(self):
    """Test RiskAssessment default values."""
    risk = RiskAssessment()

    assert risk.score == 0.0
    assert risk.level == "LOW"
    assert risk.factors == []

def test_risk_assessment_custom_values(self):
    """Test RiskAssessment with custom values."""
    risk = RiskAssessment(
        score=0.95,
        level="CRITICAL",
        factors=["Factor 1", "Factor 2"],
```

**Public Methods:**

- `def test_risk_assessment_defaults(self)`
- `def test_risk_assessment_custom_values(self)`

---

### `TestUptime`

**File:** `test_governance_engine.py`

```python
class TestUptime:
```

**Description:**
```
"""Test uptime tracking."""

def test_get_uptime_increases(self, governance_engine):
    """Test that uptime increases over time."""
    uptime1 = governance_engine.get_uptime()
    time.sleep(0.1)
    uptime2 = governance_engine.get_uptime()

    assert uptime2 > uptime1

def test_get_uptime_is_positive(self, governance_engine):
    """Test that uptime is always positive."""
    uptime = governance_engine.get_uptime()

    assert uptime >= 0
```

**Public Methods:**

- `def test_get_uptime_increases(self, governance_engine)`
- `def test_get_uptime_is_positive(self, governance_engine)`

---

### `TestEdgeCases`

**File:** `test_governance_engine.py`

```python
class TestEdgeCases:
```

**Description:**
```
"""Test edge cases and error conditions."""

def test_get_pending_decisions_empty_after_all_resolved(self, governance_engine):
    """Test getting pending decisions when all are resolved."""
    # Resolve all decisions
    for decision_id in ["dec-001", "dec-002", "dec-003"]:
        governance_engine.update_decision_status(
            decision_id,
            DecisionStatus.APPROVED,
            "operator-batch",
        )

    pending = governance_engine.get_pending_decisions(status="PENDING")

    assert len(pending) == 0
```

**Public Methods:**

- `def test_get_pending_decisions_empty_after_all_resolved(self, governance_engine)`
- `def test_get_pending_decisions_with_invalid_priority(self, governance_engine)`
- `def test_create_decision_with_zero_sla(self, governance_engine, sample_risk_assessment)`
- `def test_metrics_with_no_resolved_decisions(self, governance_engine)`
- `def test_decision_status_enum_values(self)`
- `def test_emit_event_with_subscriber(self, governance_engine, sample_risk_assessment)`

---

### `TestIntegration`

**File:** `test_governance_engine.py`

```python
class TestIntegration:
```

**Description:**
```
"""Test complete decision workflows."""

def test_full_decision_lifecycle(self, governance_engine, sample_risk_assessment):
    """Test complete decision from creation to resolution."""
    # 1. Create decision
    decision = governance_engine.create_decision(
        operation_type="INTEGRATION_TEST",
        context={"test": "data"},
        risk=sample_risk_assessment,
        priority="HIGH",
        sla_seconds=600,
    )

    # 2. Verify it appears in pending
    pending = governance_engine.get_pending_decisions()
    assert any(d.decision_id == decision.decision_id for d in pending)
```

**Public Methods:**

- `def test_full_decision_lifecycle(self, governance_engine, sample_risk_assessment)`

---

### `TestSessionManagement`

**File:** `test_hitl_interface.py`

```python
class TestSessionManagement:
```

**Description:**
```
"""Test session management."""

def test_create_session(self, hitl_interface):
    """Test creating new session."""
    session_id = hitl_interface.create_session("operator-1")

    assert session_id is not None
    assert session_id in hitl_interface.sessions

    session = hitl_interface.sessions[session_id]
    assert session["operator_id"] == "operator-1"
    assert isinstance(session["created_at"], datetime)
    assert session["decisions_processed"] == 0

def test_create_session_initializes_operator_stats(self, hitl_interface):
    """Test session creation initializes operator stats."""
```

**Public Methods:**

- `def test_create_session(self, hitl_interface)`
- `def test_create_session_initializes_operator_stats(self, hitl_interface)`
- `def test_close_session(self, hitl_interface)`
- `def test_close_nonexistent_session(self, hitl_interface)`
- `def test_multiple_sessions_same_operator(self, hitl_interface)`

---

### `TestDecisionOperations`

**File:** `test_hitl_interface.py`

```python
class TestDecisionOperations:
```

**Description:**
```
"""Test decision approval, rejection, and escalation."""

def test_approve_decision(self, hitl_interface, governance_engine):
    """Test approving a decision."""
    # Get one of the mock decisions
    decision_id = list(governance_engine.decisions.keys())[0]
    decision = governance_engine.decisions[decision_id]

    assert decision.status == DecisionStatus.PENDING

    result = hitl_interface.approve_decision(
        decision_id=decision_id,
        operator_id="operator-1",
        comment="Looks good",
        reasoning="All safety checks passed",
    )
```

**Public Methods:**

- `def test_approve_decision(self, hitl_interface, governance_engine)`
- `def test_reject_decision(self, hitl_interface, governance_engine)`
- `def test_escalate_decision(self, hitl_interface, governance_engine)`
- `def test_approve_nonexistent_decision(self, hitl_interface)`
- `def test_reject_nonexistent_decision(self, hitl_interface)`
- `def test_escalate_nonexistent_decision(self, hitl_interface)`

---

### `TestOperatorStats`

**File:** `test_hitl_interface.py`

```python
class TestOperatorStats:
```

**Description:**
```
"""Test operator statistics tracking."""

def test_get_operator_stats_new_operator(self, hitl_interface):
    """Test getting stats for new operator."""
    stats = hitl_interface.get_operator_stats("new-operator")

    assert stats["total_decisions"] == 0
    assert stats["approved"] == 0
    assert stats["rejected"] == 0
    assert stats["escalated"] == 0
    assert stats["avg_response_time"] == 0.0
    assert stats["session_start"] is None

def test_get_operator_stats_with_history(self, hitl_interface, governance_engine):
    """Test getting stats for operator with history."""
    operator_id = "operator-stats-test"
```

**Public Methods:**

- `def test_get_operator_stats_new_operator(self, hitl_interface)`
- `def test_get_operator_stats_with_history(self, hitl_interface, governance_engine)`
- `def test_approve_decision_updates_stats(self, hitl_interface, governance_engine)`
- `def test_reject_decision_updates_stats(self, hitl_interface, governance_engine)`
- `def test_escalate_decision_updates_stats(self, hitl_interface, governance_engine)`
- `def test_avg_response_time_calculation(self, hitl_interface, governance_engine)`
- `def test_operator_stats_multiple_decisions(self, hitl_interface, governance_engine)`

---

### `TestSessionInfo`

**File:** `test_hitl_interface.py`

```python
class TestSessionInfo:
```

**Description:**
```
"""Test session information retrieval."""

def test_get_session_info_existing(self, hitl_interface):
    """Test getting info for existing session."""
    session_id = hitl_interface.create_session("operator-info")

    info = hitl_interface.get_session_info(session_id)

    assert info is not None
    assert info["operator_id"] == "operator-info"
    assert "created_at" in info
    assert "decisions_processed" in info

def test_get_session_info_nonexistent(self, hitl_interface):
    """Test getting info for nonexistent session returns None."""
    info = hitl_interface.get_session_info("nonexistent-session")
```

**Public Methods:**

- `def test_get_session_info_existing(self, hitl_interface)`
- `def test_get_session_info_nonexistent(self, hitl_interface)`

---

### `TestIntegration`

**File:** `test_hitl_interface.py`

```python
class TestIntegration:
```

**Description:**
```
"""Test integrated workflows."""

def test_complete_workflow_approve(self, hitl_interface, governance_engine):
    """Test complete workflow: create session, approve decision, close session."""
    operator_id = "operator-workflow"

    # Create session
    session_id = hitl_interface.create_session(operator_id)
    assert session_id in hitl_interface.sessions

    # Approve decision
    decision_id = list(governance_engine.decisions.keys())[0]
    result = hitl_interface.approve_decision(
        decision_id, operator_id, "Approved", "Safe to proceed"
    )
    assert result is True
```

**Public Methods:**

- `def test_complete_workflow_approve(self, hitl_interface, governance_engine)`
- `def test_decision_without_operator_stats_initialization(self, hitl_interface, governance_engine)`

---

### `TestPolicyRegistryErrorPaths`

**File:** `test_policies_100pct.py`

```python
class TestPolicyRegistryErrorPaths:
```

**Description:**
```
"""Test error handling paths in PolicyRegistry."""

def test_get_policy_invalid_type_raises_error(self, policy_registry):
    """Test get_policy with invalid type raises ValueError (line 367)."""
    # Create a fake policy type that doesn't exist
    with pytest.raises(ValueError, match="not found in registry"):
        # Remove a policy to trigger error
        del policy_registry.policies[PolicyType.ETHICAL_USE]
        policy_registry.get_policy(PolicyType.ETHICAL_USE)

def test_approve_policy_invalid_type_raises_error(self, policy_registry):
    """Test approve_policy with invalid type raises ValueError (line 389)."""
    # Remove policy first
    del policy_registry.policies[PolicyType.DATA_PRIVACY]

    with pytest.raises(ValueError, match="not found"):
```

**Public Methods:**

- `def test_get_policy_invalid_type_raises_error(self, policy_registry)`
- `def test_approve_policy_invalid_type_raises_error(self, policy_registry)`
- `def test_update_policy_version_invalid_type_raises_error(self, policy_registry)`

---

### `TestPolicyRegistryUntestedMethods`

**File:** `test_policies_100pct.py`

```python
class TestPolicyRegistryUntestedMethods:
```

**Description:**
```
"""Test previously untested methods in PolicyRegistry."""

def test_get_all_policies(self, policy_registry):
    """Test get_all_policies returns all policies (line 372)."""
    all_policies = policy_registry.get_all_policies()

    # Should return all 5 policies
    assert len(all_policies) == 5
    assert all(isinstance(p, type(all_policies[0])) for p in all_policies)

def test_get_policies_by_scope_all(self, policy_registry):
    """Test get_policies_by_scope with 'all' scope (line 376)."""
    policies = policy_registry.get_policies_by_scope("all")

    # All policies with scope="all" should be included
    assert len(policies) > 0
```

**Public Methods:**

- `def test_get_all_policies(self, policy_registry)`
- `def test_get_policies_by_scope_all(self, policy_registry)`
- `def test_get_policies_by_scope_specific(self, policy_registry)`
- `def test_get_policies_requiring_review(self, policy_registry)`
- `def test_get_unapproved_policies(self, policy_registry)`
- `def test_update_policy_version_complete(self, policy_registry)`
- `def test_get_policy_summary(self, policy_registry)`

---

### `TestPolicyRegistryIntegration`

**File:** `test_policies_100pct.py`

```python
class TestPolicyRegistryIntegration:
```

**Description:**
```
"""Integration tests for complete PolicyRegistry workflows."""

def test_complete_policy_lifecycle(self, policy_registry):
    """Test complete lifecycle: create, review, approve, update."""
    policy_type = PolicyType.WHISTLEBLOWER

    # 1. Get initial policy
    policy = policy_registry.get_policy(policy_type)
    assert not policy.approved_by_erb

    # 2. Check it's in unapproved list
    unapproved = policy_registry.get_unapproved_policies()
    assert any(p.policy_type == policy_type for p in unapproved)

    # 3. Approve policy
    policy_registry.approve_policy(policy_type, "erb-decision-123")
```

**Public Methods:**

- `def test_complete_policy_lifecycle(self, policy_registry)`
- `def test_policy_scope_filtering(self, policy_registry)`
- `def test_policy_review_tracking(self, policy_registry)`

---

### `TestEthicalUseRulesCoverage`

**File:** `test_policy_engine_100pct.py`

```python
class TestEthicalUseRulesCoverage:
```

**Description:**
```
"""Test uncovered branches in Ethical Use rules."""

def test_rule_eu_007_not_implemented(self, policy_engine):
    """Test RULE-EU-007 (not implemented, returns False, '')."""
    # This rule exists in policy but has no validation logic
    # Should return False, "" at end of _check_ethical_use_rule
    result = policy_engine.enforce_policy(
        PolicyType.ETHICAL_USE,
        "test_action",
        {"some_context": "value"},
    )

    # Should be compliant since no rules violated
    assert result.is_compliant is True

def test_rule_eu_008_not_implemented(self, policy_engine):
```

**Public Methods:**

- `def test_rule_eu_007_not_implemented(self, policy_engine)`
- `def test_rule_eu_008_not_implemented(self, policy_engine)`
- `def test_rule_eu_009_not_implemented(self, policy_engine)`
- `def test_rule_eu_001_with_non_harmful_action(self, policy_engine)`
- `def test_rule_eu_002_with_non_offensive_action(self, policy_engine)`
- `def test_rule_eu_004_with_non_critical_action(self, policy_engine)`
- `def test_rule_eu_006_with_low_criticality(self, policy_engine)`
- `def test_rule_eu_010_with_low_risk(self, policy_engine)`

---

### `TestRedTeamingRulesCoverage`

**File:** `test_policy_engine_100pct.py`

```python
class TestRedTeamingRulesCoverage:
```

**Description:**
```
"""Test uncovered branches in Red Teaming rules."""

def test_rule_rt_004_to_rt_009_not_implemented(self, policy_engine):
    """Test rules RT-004 to RT-009 (not implemented)."""
    # These rules exist but have no validation logic
    result = policy_engine.enforce_policy(
        PolicyType.RED_TEAMING,
        "test_action",
        {},
    )

    assert result.is_compliant is True

def test_rule_rt_001_with_non_red_team_action(self, policy_engine):
    """Test RT-001 with action not in red team list."""
    result = policy_engine.enforce_policy(
```

**Public Methods:**

- `def test_rule_rt_004_to_rt_009_not_implemented(self, policy_engine)`
- `def test_rule_rt_001_with_non_red_team_action(self, policy_engine)`
- `def test_rule_rt_002_with_non_red_team_operation(self, policy_engine)`
- `def test_rule_rt_003_with_non_production_target(self, policy_engine)`
- `def test_rule_rt_010_with_non_destructive_action(self, policy_engine)`

---

### `TestDataPrivacyRulesCoverage`

**File:** `test_policy_engine_100pct.py`

```python
class TestDataPrivacyRulesCoverage:
```

**Description:**
```
"""Test uncovered branches in Data Privacy rules."""

def test_rule_dp_002_to_dp_006_not_implemented(self, policy_engine):
    """Test rules DP-002 to DP-006 (not implemented)."""
    result = policy_engine.enforce_policy(
        PolicyType.DATA_PRIVACY,
        "test_action",
        {},
    )

    assert result.is_compliant is True

def test_rule_dp_001_with_non_personal_data_action(self, policy_engine):
    """Test DP-001 with action not related to personal data."""
    result = policy_engine.enforce_policy(
        PolicyType.DATA_PRIVACY,
```

**Public Methods:**

- `def test_rule_dp_002_to_dp_006_not_implemented(self, policy_engine)`
- `def test_rule_dp_001_with_non_personal_data_action(self, policy_engine)`
- `def test_rule_dp_007_with_non_storage_action(self, policy_engine)`
- `def test_rule_dp_009_with_no_breach_time(self, policy_engine)`
- `def test_rule_dp_011_with_no_individual_impact(self, policy_engine)`
- `def test_rule_dp_011_with_non_automated_action(self, policy_engine)`

---

### `TestIncidentResponseRulesCoverage`

**File:** `test_policy_engine_100pct.py`

```python
class TestIncidentResponseRulesCoverage:
```

**Description:**
```
"""Test uncovered branches in Incident Response rules."""

def test_rule_ir_003_to_ir_013_not_implemented(self, policy_engine):
    """Test rules IR-003 to IR-013 (not implemented)."""
    result = policy_engine.enforce_policy(
        PolicyType.INCIDENT_RESPONSE,
        "test_action",
        {},
    )

    assert result.is_compliant is True

def test_rule_ir_001_with_non_incident_action(self, policy_engine):
    """Test IR-001 with action not 'incident_detected'."""
    detection_time = datetime.utcnow() - timedelta(hours=5)
    result = policy_engine.enforce_policy(
```

**Public Methods:**

- `def test_rule_ir_003_to_ir_013_not_implemented(self, policy_engine)`
- `def test_rule_ir_001_with_non_incident_action(self, policy_engine)`
- `def test_rule_ir_001_with_incident_already_reported(self, policy_engine)`
- `def test_rule_ir_002_with_non_critical_severity(self, policy_engine)`

---

### `TestWhistleblowerRulesCoverage`

**File:** `test_policy_engine_100pct.py`

```python
class TestWhistleblowerRulesCoverage:
```

**Description:**
```
"""Test uncovered branches in Whistleblower rules."""

def test_rule_wb_001_and_wb_004_to_wb_012_not_implemented(self, policy_engine):
    """Test rules WB-001, WB-004 to WB-012 (not implemented)."""
    result = policy_engine.enforce_policy(
        PolicyType.WHISTLEBLOWER,
        "test_action",
        {},
    )

    assert result.is_compliant is True

def test_rule_wb_002_with_non_retaliation_action(self, policy_engine):
    """Test WB-002 with action not related to retaliation."""
    result = policy_engine.enforce_policy(
        PolicyType.WHISTLEBLOWER,
```

**Public Methods:**

- `def test_rule_wb_001_and_wb_004_to_wb_012_not_implemented(self, policy_engine)`
- `def test_rule_wb_002_with_non_retaliation_action(self, policy_engine)`
- `def test_rule_wb_002_with_non_whistleblower_target(self, policy_engine)`
- `def test_rule_wb_003_with_non_report_action(self, policy_engine)`
- `def test_rule_wb_003_with_no_submission_date(self, policy_engine)`
- `def test_rule_wb_003_with_investigation_started(self, policy_engine)`

---

### `TestInternalStructure`

**File:** `test_policy_engine_100pct.py`

```python
class TestInternalStructure:
```

**Description:**
```
"""Test internal caching and data structures."""

def test_policy_cache_initialized(self, policy_engine):
    """Test that policy cache is initialized."""
    assert hasattr(policy_engine, "_policy_cache")
    assert isinstance(policy_engine._policy_cache, dict)

def test_violation_creates_proper_structure(self, policy_engine):
    """Test that violations have all required fields."""
    result = policy_engine.enforce_policy(
        PolicyType.ETHICAL_USE,
        "block_ip",
        {"authorized": False},
    )

    assert len(result.violations) > 0
```

**Public Methods:**

- `def test_policy_cache_initialized(self, policy_engine)`
- `def test_violation_creates_proper_structure(self, policy_engine)`

---

### `TestIntegrationCoverage`

**File:** `test_policy_engine_100pct.py`

```python
class TestIntegrationCoverage:
```

**Description:**
```
"""Integration tests to ensure all code paths are exercised."""

def test_all_policy_types_enforceable(self, policy_engine):
    """Test that all PolicyType enums can be enforced."""
    for policy_type in PolicyType:
        result = policy_engine.enforce_policy(
            policy_type,
            "test_action",
            {"test_context": "value"},
        )

        # All should return a result (compliant or not)
        assert result is not None
        assert hasattr(result, "is_compliant")

def test_policy_engine_statistics_complete(self, policy_engine):
```

**Public Methods:**

- `def test_all_policy_types_enforceable(self, policy_engine)`
- `def test_policy_engine_statistics_complete(self, policy_engine)`

---

### `TestPolicyEngineInit`

**File:** `test_policy_engine.py`

```python
class TestPolicyEngineInit:
```

**Description:**
```
"""Test PolicyEngine initialization."""

def test_initialization_with_config(self, config):
    """Test PolicyEngine initializes with configuration."""
    engine = PolicyEngine(config)

    assert engine.config == config
    assert engine.policy_registry is not None
    assert engine.violation_count == 0
    assert engine.enforcement_count == 0
    assert isinstance(engine._policy_cache, dict)

def test_initialization_with_disabled_auto_enforce(self, config_no_auto_enforce):
    """Test PolicyEngine initialization with auto-enforce disabled."""
    engine = PolicyEngine(config_no_auto_enforce)
```

**Public Methods:**

- `def test_initialization_with_config(self, config)`
- `def test_initialization_with_disabled_auto_enforce(self, config_no_auto_enforce)`

---

### `TestEnforcePolicy`

**File:** `test_policy_engine.py`

```python
class TestEnforcePolicy:
```

**Description:**
```
"""Test enforce_policy() method."""

def test_enforce_policy_compliant_action(self, policy_engine):
    """Test enforcement of compliant action."""
    result = policy_engine.enforce_policy(
        PolicyType.ETHICAL_USE,
        "query_database",
        {"authorized": True, "logged": True},
        actor="test_user",
    )

    assert result.is_compliant is True
    assert result.policy_type == PolicyType.ETHICAL_USE
    assert result.checked_rules > 0
    assert result.failed_rules == 0
    assert len(result.violations) == 0
```

**Public Methods:**

- `def test_enforce_policy_compliant_action(self, policy_engine)`
- `def test_enforce_policy_with_auto_enforce_disabled(self, policy_engine_no_enforce)`

---

### `TestEnforceAllPolicies`

**File:** `test_policy_engine.py`

```python
class TestEnforceAllPolicies:
```

**Description:**
```
"""Test enforce_all_policies() method."""

def test_enforce_all_policies_compliant(self, policy_engine):
    """Test enforce_all_policies with compliant action."""
    results = policy_engine.enforce_all_policies(
        action="query_database",
        context={"authorized": True, "logged": True},
        actor="test_user",
    )

    # Should return results for all PolicyTypes
    assert len(results) == len(PolicyType)
    for policy_type in PolicyType:
        assert policy_type in results
        assert results[policy_type].is_compliant is True
```

**Public Methods:**

- `def test_enforce_all_policies_compliant(self, policy_engine)`
- `def test_enforce_all_policies_with_violations(self, policy_engine)`

---

### `TestEthicalUsePolicyRules`

**File:** `test_policy_engine.py`

```python
class TestEthicalUsePolicyRules:
```

**Description:**
```
"""Test Ethical Use Policy rule validation."""

def test_rule_eu_001_unauthorized_action(self, policy_engine):
    """Test RULE-EU-001: Action without authorization."""
    result = policy_engine.enforce_policy(
        PolicyType.ETHICAL_USE,
        "block_ip",
        {"authorized": False},
    )

    assert result.is_compliant is False
    assert len(result.violations) > 0
    assert "authorization" in result.violations[0].description.lower()

def test_rule_eu_001_authorized_action(self, policy_engine):
    """Test RULE-EU-001: Action with authorization (passes)."""
```

**Public Methods:**

- `def test_rule_eu_001_unauthorized_action(self, policy_engine)`
- `def test_rule_eu_001_authorized_action(self, policy_engine)`
- `def test_rule_eu_002_offensive_non_authorized_env(self, policy_engine)`
- `def test_rule_eu_002_offensive_authorized_env(self, policy_engine)`
- `def test_rule_eu_003_action_not_logged(self, policy_engine)`
- `def test_rule_eu_004_critical_action_no_human_oversight(self, policy_engine)`
- `def test_rule_eu_005_protected_attribute_discrimination(self, policy_engine)`
- `def test_rule_eu_006_critical_decision_no_explanation(self, policy_engine)`
- `def test_rule_eu_010_high_risk_no_hitl(self, policy_engine)`

---

### `TestRedTeamingPolicyRules`

**File:** `test_policy_engine.py`

```python
class TestRedTeamingPolicyRules:
```

**Description:**
```
"""Test Red Teaming Policy rule validation."""

def test_rule_rt_001_no_written_authorization(self, policy_engine):
    """Test RULE-RT-001: Red team action without written authorization."""
    result = policy_engine.enforce_policy(
        PolicyType.RED_TEAMING,
        "execute_exploit",
        {"written_authorization": False},
    )

    assert result.is_compliant is False
    assert "written authorization" in result.violations[0].description

def test_rule_rt_002_no_roe_defined(self, policy_engine):
    """Test RULE-RT-002: Red team operation without Rules of Engagement."""
    result = policy_engine.enforce_policy(
```

**Public Methods:**

- `def test_rule_rt_001_no_written_authorization(self, policy_engine)`
- `def test_rule_rt_002_no_roe_defined(self, policy_engine)`
- `def test_rule_rt_003_production_targeting_no_approval(self, policy_engine)`
- `def test_rule_rt_005_social_engineering_no_erb(self, policy_engine)`
- `def test_rule_rt_010_destructive_no_hitl(self, policy_engine)`

---

### `TestDataPrivacyPolicyRules`

**File:** `test_policy_engine.py`

```python
class TestDataPrivacyPolicyRules:
```

**Description:**
```
"""Test Data Privacy Policy rule validation."""

def test_rule_dp_001_no_legal_basis(self, policy_engine):
    """Test RULE-DP-001: Personal data collection without legal basis."""
    result = policy_engine.enforce_policy(
        PolicyType.DATA_PRIVACY,
        "collect_personal_data",
        {},  # No legal_basis
    )

    assert result.is_compliant is False
    assert "legal basis" in result.violations[0].description
    assert "GDPR" in result.violations[0].description

def test_rule_dp_007_no_encryption(self, policy_engine):
    """Test RULE-DP-007: Personal data not encrypted."""
```

**Public Methods:**

- `def test_rule_dp_001_no_legal_basis(self, policy_engine)`
- `def test_rule_dp_007_no_encryption(self, policy_engine)`
- `def test_rule_dp_009_breach_notification_late(self, policy_engine)`
- `def test_rule_dp_009_breach_notification_on_time(self, policy_engine)`
- `def test_rule_dp_011_automated_decision_no_human_intervention(self, policy_engine)`

---

### `TestIncidentResponsePolicyRules`

**File:** `test_policy_engine.py`

```python
class TestIncidentResponsePolicyRules:
```

**Description:**
```
"""Test Incident Response Policy rule validation."""

def test_rule_ir_001_incident_not_reported_after_1h(self, policy_engine):
    """Test RULE-IR-001: Incident not reported after 1 hour."""
    detection_time = datetime.utcnow() - timedelta(hours=2)  # 2h ago
    result = policy_engine.enforce_policy(
        PolicyType.INCIDENT_RESPONSE,
        "incident_detected",
        {"detection_time": detection_time, "reported": False},
    )

    assert result.is_compliant is False
    assert "1h requirement" in result.violations[0].description

def test_rule_ir_001_incident_reported_on_time(self, policy_engine):
    """Test RULE-IR-001: Incident reported within 1 hour (passes)."""
```

**Public Methods:**

- `def test_rule_ir_001_incident_not_reported_after_1h(self, policy_engine)`
- `def test_rule_ir_001_incident_reported_on_time(self, policy_engine)`
- `def test_rule_ir_002_critical_incident_erb_not_notified(self, policy_engine)`

---

### `TestWhistleblowerPolicyRules`

**File:** `test_policy_engine.py`

```python
class TestWhistleblowerPolicyRules:
```

**Description:**
```
"""Test Whistleblower Policy rule validation."""

def test_rule_wb_002_retaliation_against_whistleblower(self, policy_engine):
    """Test RULE-WB-002: Retaliation against whistleblower."""
    result = policy_engine.enforce_policy(
        PolicyType.WHISTLEBLOWER,
        "terminate_employee",
        {"target_is_whistleblower": True},
    )

    assert result.is_compliant is False
    assert "retaliation prohibited" in result.violations[0].description

def test_rule_wb_003_investigation_delay(self, policy_engine):
    """Test RULE-WB-003: Whistleblower investigation delayed."""
    submission_date = datetime.utcnow() - timedelta(days=45)  # 45 days ago
```

**Public Methods:**

- `def test_rule_wb_002_retaliation_against_whistleblower(self, policy_engine)`
- `def test_rule_wb_003_investigation_delay(self, policy_engine)`

---

### `TestUtilityMethods`

**File:** `test_policy_engine.py`

```python
class TestUtilityMethods:
```

**Description:**
```
"""Test utility methods."""

def test_check_action_allowed(self, policy_engine):
    """Test check_action() with allowed action."""
    is_allowed, violations = policy_engine.check_action(
        action="query_database",
        context={"authorized": True, "logged": True},
        actor="test_user",
    )

    assert is_allowed is True
    assert len(violations) == 0

def test_check_action_blocked(self, policy_engine):
    """Test check_action() with blocked action."""
    is_allowed, violations = policy_engine.check_action(
```

**Public Methods:**

- `def test_check_action_allowed(self, policy_engine)`
- `def test_check_action_blocked(self, policy_engine)`
- `def test_get_applicable_policies(self, policy_engine)`
- `def test_get_statistics(self, policy_engine)`

---

### `TestEdgeCases`

**File:** `test_policy_engine.py`

```python
class TestEdgeCases:
```

**Description:**
```
"""Test edge cases and error handling."""

def test_policy_with_auto_enforce_disabled_at_policy_level(self, config_no_auto_enforce, monkeypatch):
    """Test when BOTH policy.auto_enforce=False AND config.auto_enforce_policies=False.

    This covers line 77 - the return statement when both are False.
    """
    engine = PolicyEngine(config_no_auto_enforce)

    # Get a policy and disable its auto_enforce
    policy = engine.policy_registry.get_policy(PolicyType.ETHICAL_USE)
    policy.auto_enforce = False

    result = engine.enforce_policy(
        PolicyType.ETHICAL_USE,
        "block_ip",
```

**Public Methods:**

- `def test_policy_with_auto_enforce_disabled_at_policy_level(self, config_no_auto_enforce, monkeypatch)`
- `def test_check_rule_with_invalid_rule_format(self, policy_engine)`
- `def test_multiple_violations_in_single_policy(self, policy_engine)`
- `def test_violation_count_increments(self, policy_engine)`

---

### `AuditQuery`

**File:** `audit_trail.py`

```python
class AuditQuery:
```

**Description:**
```
"""
Query parameters for audit trail search.
"""

# Time range
start_time: datetime | None = None
end_time: datetime | None = None

# Decision filters
decision_ids: list[str] = field(default_factory=list)
risk_levels: list[RiskLevel] = field(default_factory=list)
automation_levels: list[AutomationLevel] = field(default_factory=list)
statuses: list[DecisionStatus] = field(default_factory=list)

# Actor filters
operator_ids: list[str] = field(default_factory=list)
```

**Public Methods:**


---

### `ComplianceReport`

**File:** `audit_trail.py`

```python
class ComplianceReport:
```

**Description:**
```
"""
Compliance report for regulatory requirements.
"""

# Report details
report_id: str
generated_at: datetime = field(default_factory=datetime.utcnow)
report_type: str = "hitl_compliance"

# Time period
period_start: datetime = field(default_factory=datetime.utcnow)
period_end: datetime = field(default_factory=datetime.utcnow)

# Summary statistics
total_decisions: int = 0
auto_executed: int = 0
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `AuditTrail`

**File:** `audit_trail.py`

```python
class AuditTrail:
```

**Description:**
```
"""
Immutable audit trail for HITL decisions.

Logs all decision events, operator actions, and system events for
compliance, forensics, and analytics.
"""

def __init__(self, storage_backend: Any | None = None):
    """
    Initialize audit trail.

    Args:
        storage_backend: Storage backend for persistence (e.g., database, S3)
                       If None, uses in-memory storage
    """
    self.storage_backend = storage_backend
```

**Public Methods:**

- `def log_decision_created(self, decision`
- `def log_decision_queued(self, decision`
- `def log_decision_executed(`
- `def log_decision_approved(self, decision`
- `def log_decision_rejected(self, decision`
- `def log_decision_escalated(self, decision`
- `def log_decision_failed(self, decision`
- `def query(self, query`
- `def generate_compliance_report(self, start_time`
- `def get_metrics(self) -> dict[str, Any]`

---

### `AutomationLevel`

**File:** `base.py`

```python
class AutomationLevel(Enum):
```

**Description:**
```
"""
Automation level for AI decisions based on confidence and risk.

Levels:
- FULL: AI executes autonomously (≥95% confidence, low risk)
- SUPERVISED: AI proposes, human approves (≥80% confidence)
- ADVISORY: AI advises, human decides (≥60% confidence)
- MANUAL: Human only, no AI execution (<60% confidence or high risk)
"""

FULL = "full"  # Auto-execute, log audit trail
SUPERVISED = "supervised"  # Require human approval
ADVISORY = "advisory"  # AI suggests, human chooses
MANUAL = "manual"  # Human only, no AI autonomy
```

**Public Methods:**


---

### `RiskLevel`

**File:** `base.py`

```python
class RiskLevel(Enum):
```

**Description:**
```
"""
Risk level for security actions.

Levels determine SLA timers and escalation policies:
- LOW: 30min SLA, automated escalation
- MEDIUM: 15min SLA, supervisor escalation
- HIGH: 10min SLA, manager escalation
- CRITICAL: 5min SLA, immediate executive escalation
"""

LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"
```

**Public Methods:**


---

### `DecisionStatus`

**File:** `base.py`

```python
class DecisionStatus(Enum):
```

**Description:**
```
"""Status of HITL decision in workflow."""

PENDING = "pending"  # Waiting for operator review
APPROVED = "approved"  # Operator approved
REJECTED = "rejected"  # Operator rejected
EXECUTED = "executed"  # Action executed successfully
FAILED = "failed"  # Execution failed
TIMEOUT = "timeout"  # SLA timeout occurred
ESCALATED = "escalated"  # Escalated to supervisor
CANCELLED = "cancelled"  # Cancelled by operator


class ActionType(Enum):
"""
Types of security actions that can be automated.
```

**Public Methods:**


---

### `ActionType`

**File:** `base.py`

```python
class ActionType(Enum):
```

**Description:**
```
"""
Types of security actions that can be automated.

Categories:
- Network: isolate_host, block_ip, block_domain, throttle_connection
- Endpoint: quarantine_file, kill_process, disable_user, lock_account
- Data: encrypt_data, backup_data, delete_data, archive_logs
- Investigation: collect_forensics, capture_memory, snapshot_vm
- Response: send_alert, create_ticket, notify_team, escalate_incident
"""

# Network actions
ISOLATE_HOST = "isolate_host"
BLOCK_IP = "block_ip"
BLOCK_DOMAIN = "block_domain"
BLOCK_PORT = "block_port"
```

**Public Methods:**


---

### `SLAConfig`

**File:** `base.py`

```python
class SLAConfig:
```

**Description:**
```
"""
SLA (Service Level Agreement) configuration for decision review.

Defines timeout periods for different risk levels and escalation policies.
"""

# SLA timeout by risk level (minutes)
low_risk_timeout: int = 30
medium_risk_timeout: int = 15
high_risk_timeout: int = 10
critical_risk_timeout: int = 5

# Warning threshold (% of SLA before warning)
warning_threshold: float = 0.75  # Warn at 75% of SLA

# Auto-escalate on timeout
```

**Public Methods:**

- `def get_timeout_minutes(self, risk_level`
- `def get_timeout_delta(self, risk_level`
- `def get_warning_delta(self, risk_level`

---

### `EscalationConfig`

**File:** `base.py`

```python
class EscalationConfig:
```

**Description:**
```
"""Configuration for decision escalation."""

# Enable escalation
enabled: bool = True

# Escalation triggers
escalate_on_timeout: bool = True
escalate_on_high_risk: bool = True
escalate_on_multiple_rejections: bool = True
rejection_threshold: int = 2  # Escalate after N rejections

# Escalation targets by risk level
low_risk_escalation: str = "soc_supervisor"
medium_risk_escalation: str = "soc_supervisor"
high_risk_escalation: str = "security_manager"
critical_risk_escalation: str = "ciso"
```

**Public Methods:**

- `def get_escalation_target(self, risk_level`

---

### `HITLConfig`

**File:** `base.py`

```python
class HITLConfig:
```

**Description:**
```
"""Main HITL framework configuration."""

# Confidence thresholds for automation levels
full_automation_threshold: float = 0.95  # ≥95% → FULL
supervised_threshold: float = 0.80  # ≥80% → SUPERVISED
advisory_threshold: float = 0.60  # ≥60% → ADVISORY
# <60% → MANUAL

# Risk-based overrides (even high confidence may need approval)
high_risk_requires_approval: bool = True
critical_risk_requires_approval: bool = True

# SLA configuration
sla_config: SLAConfig = field(default_factory=SLAConfig)

# Escalation configuration
```

**Public Methods:**

- `def get_automation_level(self, confidence`

---

### `DecisionContext`

**File:** `base.py`

```python
class DecisionContext:
```

**Description:**
```
"""
Context for a security decision.

Contains all information needed for human review and audit trail.
"""

# Action details
action_type: ActionType
action_params: dict[str, Any] = field(default_factory=dict)

# AI reasoning
ai_reasoning: str = ""
confidence: float = 0.0
model_version: str = ""

# Threat context
```

**Public Methods:**

- `def get_summary(self) -> str`

---

### `HITLDecision`

**File:** `base.py`

```python
class HITLDecision:
```

**Description:**
```
"""
A decision requiring human-in-the-loop review.

Represents a single security decision made by MAXIMUS AI that may
require human oversight based on confidence and risk level.
"""

# Unique identifier
decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))

# Decision context
context: DecisionContext = field(default_factory=DecisionContext)

# Risk and automation
risk_level: RiskLevel = RiskLevel.MEDIUM
automation_level: AutomationLevel = AutomationLevel.SUPERVISED
```

**Public Methods:**

- `def is_overdue(self) -> bool`
- `def get_time_remaining(self) -> timedelta | None`
- `def get_age(self) -> timedelta`
- `def requires_human_review(self) -> bool`
- `def can_execute_autonomously(self) -> bool`

---

### `OperatorAction`

**File:** `base.py`

```python
class OperatorAction:
```

**Description:**
```
"""
Action taken by human operator on a decision.
"""

# Action details
decision_id: str
operator_id: str
action: str  # "approve", "reject", "escalate", "modify"
timestamp: datetime = field(default_factory=datetime.utcnow)

# Justification
comment: str = ""
reasoning: str = ""

# Modifications (if operator changed parameters)
modifications: dict[str, Any] = field(default_factory=dict)
```

**Public Methods:**


---

### `AuditEntry`

**File:** `base.py`

```python
class AuditEntry:
```

**Description:**
```
"""
Immutable audit trail entry for compliance and forensics.
"""

# Entry identifier
entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
timestamp: datetime = field(default_factory=datetime.utcnow)

# Decision reference
decision_id: str = ""

# Event details
event_type: str = ""  # "decision_created", "decision_approved", "decision_executed", etc.
event_description: str = ""

# Actor (AI or human)
```

**Public Methods:**

- `def redact_pii(self, pii_fields`

---

### `DecisionResult`

**File:** `decision_framework.py`

```python
class DecisionResult:
```

**Description:**
```
"""
Result of decision processing.

Indicates whether decision was executed immediately, queued for review,
or rejected.
"""

# Decision reference
decision: HITLDecision

# Result status
executed: bool = False
queued: bool = False
rejected: bool = False

# Execution details
```

**Public Methods:**

- `def get_summary(self) -> str`

---

### `HITLDecisionFramework`

**File:** `decision_framework.py`

```python
class HITLDecisionFramework:
```

**Description:**
```
"""
Main HITL decision framework.

Coordinates risk assessment, automation level determination, decision
queueing, and execution for AI-proposed security actions.
"""

def __init__(
    self,
    config: HITLConfig | None = None,
    risk_assessor: RiskAssessor | None = None,
):
    """
    Initialize HITL framework.

    Args:
```

**Public Methods:**

- `def set_decision_queue(self, queue)`
- `def set_audit_trail(self, audit_trail)`
- `def register_executor(self, action_type`
- `def evaluate_action(`
- `def execute_decision(self, decision`
- `def reject_decision(self, decision`
- `def escalate_decision(self, decision`
- `def get_metrics(self) -> dict[str, Any]`
- `def block_ip(self, ip_address`
- `def isolate_host(self, host_id`
- `def quarantine_file(`
- `def kill_process(`

---

### `QueuedDecision`

**File:** `decision_queue.py`

```python
class QueuedDecision:
```

**Description:**
```
"""
Wrapper for decision in queue with queueing metadata.
"""

# Decision reference
decision: HITLDecision

# Queue metadata
queued_at: datetime = field(default_factory=datetime.utcnow)
queue_position: int = 0
priority_score: float = 0.0  # Higher = more urgent

# Assignment tracking
assigned: bool = False
assignment_attempts: int = 0
```

**Public Methods:**

- `def get_time_in_queue(self) -> timedelta`
- `def get_time_until_sla(self) -> timedelta | None`
- `def is_sla_violated(self) -> bool`
- `def should_send_sla_warning(self, warning_threshold`

---

### `SLAMonitor`

**File:** `decision_queue.py`

```python
class SLAMonitor:
```

**Description:**
```
"""
Monitors decisions for SLA violations and warnings.

Runs periodic checks and triggers callbacks for:
- SLA warnings (75% of time elapsed)
- SLA violations (deadline exceeded)
"""

def __init__(self, sla_config: SLAConfig, check_interval: int = 30):
    """
    Initialize SLA monitor.

    Args:
        sla_config: SLA configuration
        check_interval: Check interval in seconds
    """
```

**Public Methods:**

- `def register_warning_callback(self, callback`
- `def register_violation_callback(self, callback`
- `def start(self)`
- `def stop(self)`
- `def check_decision(self, queued_decision`

---

### `DecisionQueue`

**File:** `decision_queue.py`

```python
class DecisionQueue:
```

**Description:**
```
"""
Priority queue for decisions awaiting human review.

Implements multi-level priority queue with SLA monitoring.
"""

def __init__(self, sla_config: SLAConfig | None = None, max_size: int = 1000):
    """
    Initialize decision queue.

    Args:
        sla_config: SLA configuration
        max_size: Maximum queue size (0 = unlimited)
    """
    self.sla_config = sla_config or SLAConfig()
    self.max_size = max_size
```

**Public Methods:**

- `def enqueue(self, decision`
- `def dequeue(self, risk_level`
- `def get_pending_decisions(`
- `def get_decision(self, decision_id`
- `def remove_decision(self, decision_id`
- `def assign_to_operator(self, decision`
- `def get_next_operator_round_robin(self) -> str | None`
- `def check_sla_status(self)`
- `def get_total_size(self) -> int`
- `def get_size_by_risk(self) -> dict[RiskLevel, int]`
- `def get_metrics(self) -> dict[str, any]`

---

### `EscalationType`

**File:** `escalation_manager.py`

```python
class EscalationType(Enum):
```

**Description:**
```
"""Type of escalation."""

TIMEOUT = "timeout"  # SLA timeout
HIGH_RISK = "high_risk"  # Critical/High risk decision
MULTIPLE_REJECTIONS = "multiple_rejections"  # Rejected multiple times
OPERATOR_REQUEST = "operator_request"  # Explicit operator escalation
STALE_DECISION = "stale_decision"  # Decision pending too long
SYSTEM_OVERRIDE = "system_override"  # System-initiated override


# ============================================================================
# Escalation Data Classes
# ============================================================================


@dataclass
```

**Public Methods:**


---

### `EscalationRule`

**File:** `escalation_manager.py`

```python
class EscalationRule:
```

**Description:**
```
"""
Rule for when to escalate a decision.
"""

# Rule identifier
rule_id: str
rule_name: str
escalation_type: EscalationType

# Trigger conditions
risk_levels: list[RiskLevel] = field(default_factory=list)  # Empty = all levels
max_rejections: int = 2
timeout_threshold: timedelta | None = None

# Escalation target
target_role: str = "soc_supervisor"
```

**Public Methods:**

- `def matches(self, decision`

---

### `EscalationEvent`

**File:** `escalation_manager.py`

```python
class EscalationEvent:
```

**Description:**
```
"""
Record of an escalation event.
"""

# Event details
event_id: str
decision_id: str
escalation_type: EscalationType
timestamp: datetime = field(default_factory=datetime.utcnow)

# Escalation details
from_role: str = ""
to_role: str = ""
reason: str = ""

# Triggered rule
```

**Public Methods:**


---

### `EscalationManager`

**File:** `escalation_manager.py`

```python
class EscalationManager:
```

**Description:**
```
"""
Manages decision escalation to higher authority.

Monitors decisions for escalation triggers and automatically escalates
based on configured rules.
"""

# Default escalation chain
DEFAULT_CHAIN = [
    "soc_operator",
    "soc_supervisor",
    "security_manager",
    "ciso",
    "ceo",
]
```

**Public Methods:**

- `def add_rule(self, rule`
- `def check_for_escalation(self, decision`
- `def escalate_decision(`
- `def register_notification_handler(self, channel`
- `def get_escalation_target(self, current_role`
- `def get_metrics(self) -> dict[str, any]`
- `def get_escalation_history(self, decision_id`

---

### `OperatorSession`

**File:** `operator_interface.py`

```python
class OperatorSession:
```

**Description:**
```
"""
Active operator session for decision review.
"""

# Session details
session_id: str
operator_id: str
operator_name: str
operator_role: str  # "soc_operator", "soc_supervisor", etc.

# Session timing
started_at: datetime = field(default_factory=datetime.utcnow)
last_activity: datetime = field(default_factory=datetime.utcnow)
expires_at: datetime | None = None

# Session metrics
```

**Public Methods:**

- `def is_expired(self) -> bool`
- `def get_session_duration(self) -> timedelta`
- `def update_activity(self)`
- `def get_approval_rate(self) -> float`
- `def get_rejection_rate(self) -> float`

---

### `OperatorMetrics`

**File:** `operator_interface.py`

```python
class OperatorMetrics:
```

**Description:**
```
"""
Aggregate metrics for an operator.
"""

operator_id: str

# Lifetime stats
total_sessions: int = 0
total_decisions_reviewed: int = 0
total_approved: int = 0
total_rejected: int = 0
total_escalated: int = 0
total_modified: int = 0

# Timing stats
average_review_time: float = 0.0  # seconds
```

**Public Methods:**

- `def update_from_session(self, session`

---

### `OperatorInterface`

**File:** `operator_interface.py`

```python
class OperatorInterface:
```

**Description:**
```
"""
Interface for SOC operators to review and act on HITL decisions.

Provides methods for decision review, approval, rejection, modification,
and escalation.
"""

def __init__(
    self,
    decision_framework=None,
    decision_queue=None,
    escalation_manager=None,
    audit_trail=None,
):
    """
    Initialize operator interface.
```

**Public Methods:**

- `def create_session(`
- `def get_session(self, session_id`
- `def get_pending_decisions(`
- `def approve_decision(self, session_id`
- `def reject_decision(self, session_id`
- `def modify_and_approve(`
- `def escalate_decision(self, session_id`
- `def get_operator_metrics(self, operator_id`
- `def get_session_metrics(self, session_id`

---

### `RiskFactors`

**File:** `risk_assessor.py`

```python
class RiskFactors:
```

**Description:**
```
"""
Individual risk factors that contribute to overall risk score.

Each factor is scored 0.0 (low risk) to 1.0 (high risk).
"""

# Threat factors
threat_severity: float = 0.0  # Threat score from detection engine
threat_confidence: float = 0.0  # Confidence in threat identification
threat_novelty: float = 0.0  # Is this a new/unknown threat?

# Asset factors
asset_criticality: float = 0.0  # Business criticality of assets
asset_count: float = 0.0  # Number of affected assets (normalized)
data_sensitivity: float = 0.0  # Sensitivity of data on assets
```

**Public Methods:**

- `def get_all_factors(self) -> dict[str, float]`
- `def get_max_factor(self) -> tuple[str, float]`

---

### `RiskScore`

**File:** `risk_assessor.py`

```python
class RiskScore:
```

**Description:**
```
"""
Computed risk score with breakdown by category.
"""

# Overall risk score (0.0 to 1.0)
overall_score: float = 0.0

# Risk level
risk_level: RiskLevel = RiskLevel.LOW

# Category scores
threat_risk: float = 0.0
asset_risk: float = 0.0
business_risk: float = 0.0
action_risk: float = 0.0
compliance_risk: float = 0.0
```

**Public Methods:**

- `def get_category_breakdown(self) -> dict[str, float]`
- `def get_summary(self) -> str`

---

### `RiskAssessor`

**File:** `risk_assessor.py`

```python
class RiskAssessor:
```

**Description:**
```
"""
Comprehensive risk assessment engine.

Analyzes security decisions across multiple risk dimensions and computes
an overall risk score and level.
"""

# Risk level thresholds
CRITICAL_THRESHOLD = 0.75  # ≥0.75 → CRITICAL
HIGH_THRESHOLD = 0.50  # ≥0.50 → HIGH (>50% risk is high)
MEDIUM_THRESHOLD = 0.30  # ≥0.30 → MEDIUM
# <0.30 → LOW

# Category weights (must sum to 1.0)
WEIGHTS = {
    "threat": 0.25,
```

**Public Methods:**

- `def assess_risk(self, context`

---

### `TestBaseClasses`

**File:** `test_hitl.py`

```python
class TestBaseClasses:
```

**Description:**
```
"""Tests for base classes and configurations."""

def test_hitl_config_validation(self):
    """Test HITLConfig validation."""
    # Valid config
    config = HITLConfig(
        full_automation_threshold=0.95,
        supervised_threshold=0.80,
        advisory_threshold=0.60,
    )
    assert config.full_automation_threshold == 0.95

    # Invalid: thresholds out of order
    with pytest.raises(ValueError):
        HITLConfig(
            full_automation_threshold=0.60,
```

**Public Methods:**

- `def test_hitl_config_validation(self)`
- `def test_automation_level_determination(self, hitl_config)`
- `def test_decision_context_summary(self, sample_context)`

---

### `TestRiskAssessor`

**File:** `test_hitl.py`

```python
class TestRiskAssessor:
```

**Description:**
```
"""Tests for risk assessment engine."""

def test_risk_assessment_critical(self, risk_assessor):
    """Test risk assessment for critical scenario."""
    context = DecisionContext(
        action_type=ActionType.DELETE_DATA,
        action_params={"data_path": "/production/database"},
        ai_reasoning="Detected ransomware",
        confidence=0.65,  # Low confidence
        threat_score=0.95,  # High threat
        affected_assets=["prod-db-1", "prod-db-2"],
        asset_criticality="critical",
    )

    risk_score = risk_assessor.assess_risk(context)
```

**Public Methods:**

- `def test_risk_assessment_critical(self, risk_assessor)`
- `def test_risk_assessment_low(self, risk_assessor)`
- `def test_risk_factors_calculation(self, risk_assessor, sample_context)`

---

### `TestDecisionFramework`

**File:** `test_hitl.py`

```python
class TestDecisionFramework:
```

**Description:**
```
"""Tests for HITL decision framework."""

def test_full_automation_execution(self, decision_framework):
    """Test automatic execution for high-confidence, low-risk decision."""

    # Register dummy executor
    def dummy_executor(context):
        return {"status": "success", "host_isolated": context.action_params["host_id"]}

    decision_framework.register_executor(ActionType.ISOLATE_HOST, dummy_executor)

    # Evaluate high-confidence decision
    result = decision_framework.evaluate_action(
        action_type=ActionType.ISOLATE_HOST,
        action_params={"host_id": "srv-001"},
        ai_reasoning="Known malware detected",
```

**Public Methods:**

- `def test_full_automation_execution(self, decision_framework)`
- `def test_supervised_queueing(self, decision_framework, decision_queue, audit_trail)`
- `def test_decision_rejection(self, decision_framework, sample_decision)`

---

### `TestEscalationManager`

**File:** `test_hitl.py`

```python
class TestEscalationManager:
```

**Description:**
```
"""Tests for escalation management."""

def test_timeout_escalation_rule(self, escalation_manager):
    """Test timeout-based escalation."""
    # Create decision with expired SLA
    decision = HITLDecision(
        context=DecisionContext(action_type=ActionType.ISOLATE_HOST),
        risk_level=RiskLevel.MEDIUM,
        sla_deadline=datetime.utcnow() - timedelta(minutes=5),  # 5 minutes overdue
    )

    # Check for matching rule
    rule = escalation_manager.check_for_escalation(decision)

    assert rule is not None
    assert rule.escalation_type == EscalationType.TIMEOUT
```

**Public Methods:**

- `def test_timeout_escalation_rule(self, escalation_manager)`
- `def test_critical_risk_escalation(self, escalation_manager)`

---

### `TestDecisionQueue`

**File:** `test_hitl.py`

```python
class TestDecisionQueue:
```

**Description:**
```
"""Tests for decision queue management."""

def test_priority_ordering(self, decision_queue):
    """Test that decisions are prioritized correctly."""
    # Enqueue decisions with different risk levels
    low_risk = HITLDecision(
        context=DecisionContext(action_type=ActionType.SEND_ALERT),
        risk_level=RiskLevel.LOW,
    )
    critical_risk = HITLDecision(
        context=DecisionContext(action_type=ActionType.DELETE_DATA),
        risk_level=RiskLevel.CRITICAL,
    )
    medium_risk = HITLDecision(
        context=DecisionContext(action_type=ActionType.BLOCK_IP),
        risk_level=RiskLevel.MEDIUM,
```

**Public Methods:**

- `def test_priority_ordering(self, decision_queue)`
- `def test_sla_monitoring(self, decision_queue)`
- `def test_operator_assignment(self, decision_queue, sample_decision)`

---

### `TestOperatorInterface`

**File:** `test_hitl.py`

```python
class TestOperatorInterface:
```

**Description:**
```
"""Tests for operator interface."""

def test_session_creation(self, operator_interface):
    """Test operator session creation."""
    session = operator_interface.create_session(
        operator_id="op_123",
        operator_name="John Doe",
        operator_role="soc_operator",
        ip_address="192.168.1.100",
    )

    assert session.operator_id == "op_123"
    assert session.operator_name == "John Doe"
    assert session.is_expired() == False

def test_approve_decision_workflow(self, operator_interface, decision_queue, decision_framework):
```

**Public Methods:**

- `def test_session_creation(self, operator_interface)`
- `def test_approve_decision_workflow(self, operator_interface, decision_queue, decision_framework)`

---

### `TestAuditTrail`

**File:** `test_hitl.py`

```python
class TestAuditTrail:
```

**Description:**
```
"""Tests for audit trail."""

def test_decision_lifecycle_logging(self, audit_trail, risk_assessor):
    """Test logging complete decision lifecycle."""
    decision = HITLDecision(
        context=DecisionContext(action_type=ActionType.ISOLATE_HOST),
        risk_level=RiskLevel.HIGH,
    )

    risk_score = risk_assessor.assess_risk(decision.context)

    # Log events
    audit_trail.log_decision_created(decision, risk_score)
    audit_trail.log_decision_queued(decision)

    operator_action = OperatorAction(
```

**Public Methods:**

- `def test_decision_lifecycle_logging(self, audit_trail, risk_assessor)`
- `def test_compliance_report_generation(self, audit_trail, risk_assessor)`

---

### `TestIntegration`

**File:** `test_hitl.py`

```python
class TestIntegration:
```

**Description:**
```
"""End-to-end integration tests."""

def test_complete_hitl_workflow(
    self, decision_framework, decision_queue, escalation_manager, audit_trail, operator_interface
):
    """Test complete HITL workflow from AI decision to execution."""
    # Connect components
    decision_framework.set_decision_queue(decision_queue)
    decision_framework.set_audit_trail(audit_trail)
    operator_interface.decision_framework = decision_framework
    operator_interface.decision_queue = decision_queue
    operator_interface.escalation_manager = escalation_manager
    operator_interface.audit_trail = audit_trail

    # Register executor
    def executor(context):
```

**Public Methods:**

- `def test_complete_hitl_workflow(`

---

### `ImmuneEnhancementTools`

**File:** `immune_enhancement_tools.py`

```python
class ImmuneEnhancementTools:
```

**Description:**
```
"""Immune Enhancement Tools for MAXIMUS AI.

Integrates FASE 9 services:
- Regulatory T-Cells Service (port 8018)
- Memory Consolidation Service (port 8019)
- Adaptive Immunity Service (port 8020)
"""

def __init__(self, gemini_client: Any):
    """Initialize Immune Enhancement Tools.

    Args:
        gemini_client: Gemini client instance
    """
    self.gemini_client = gemini_client
    self.treg_url = "http://localhost:8018"
```

**Public Methods:**

- `def list_available_tools(self) -> list[dict[str, Any]]`

---

### `CBRResult`

**File:** `cbr_engine.py`

```python
class CBRResult:
```

**Description:**
```
"""Result from CBR reasoning process."""
suggested_action: str
precedent_id: int
confidence: float
rationale: str


class CBREngine:
"""Case-Based Reasoning engine for ethical decision-making.

Implements the 4-step CBR cycle:
1. Retrieve: Find similar past cases
2. Reuse: Adapt past solution to current case
3. Revise: Validate with constitutional rules
4. Retain: Store new case as precedent
"""
```

**Public Methods:**


---

### `CBREngine`

**File:** `cbr_engine.py`

```python
class CBREngine:
```

**Description:**
```
"""Case-Based Reasoning engine for ethical decision-making.

Implements the 4-step CBR cycle:
1. Retrieve: Find similar past cases
2. Reuse: Adapt past solution to current case
3. Revise: Validate with constitutional rules
4. Retain: Store new case as precedent
"""

def __init__(self, db: PrecedentDB):
    """Initialize CBR engine.

    Args:
        db: PrecedentDB instance for precedent storage/retrieval
    """
    self.db = db
```

**Public Methods:**


---

### `ViolationLevel`

**File:** `constitutional_validator.py`

```python
class ViolationLevel(Enum):
```

**Description:**
```
"""Severity levels for constitutional violations."""
NONE = 0
LOW = 1
MEDIUM = 2
HIGH = 3
CRITICAL = 4

class ViolationType(Enum):
"""Types of constitutional violations."""
LEI_ZERO = "lei_zero_florescimento"
LEI_I = "lei_i_ovelha_perdida"
MIP_VIOLATION = "integridade_processual"
HUBRIS_VIOLATION = "hubris_soberba_prepotencia"
DATA_PRIVACY = "privacidade_de_dados"
UNKNOWN = "desconhecida"
```

**Public Methods:**


---

### `ViolationType`

**File:** `constitutional_validator.py`

```python
class ViolationType(Enum):
```

**Description:**
```
"""Types of constitutional violations."""
LEI_ZERO = "lei_zero_florescimento"
LEI_I = "lei_i_ovelha_perdida"
MIP_VIOLATION = "integridade_processual"
HUBRIS_VIOLATION = "hubris_soberba_prepotencia"
DATA_PRIVACY = "privacidade_de_dados"
UNKNOWN = "desconhecida"

class ResponseProtocol(Enum):
"""Defines the response stance for a violation."""
PASSIVE_BLOCK = "passive_block"
ACTIVE_DEFENSE = "active_defense_escalation"

@dataclass
class ViolationReport:
"""Dataclass to hold violation details."""
```

**Public Methods:**


---

### `ResponseProtocol`

**File:** `constitutional_validator.py`

```python
class ResponseProtocol(Enum):
```

**Description:**
```
"""Defines the response stance for a violation."""
PASSIVE_BLOCK = "passive_block"
ACTIVE_DEFENSE = "active_defense_escalation"

@dataclass
class ViolationReport:
"""Dataclass to hold violation details."""
is_blocking: bool = False
level: ViolationLevel = ViolationLevel.NONE
violated_law: Optional[ViolationType] = None
description: str = "No violation detected."
evidence: Dict[str, Any] = field(default_factory=dict)
response_protocol: ResponseProtocol = ResponseProtocol.PASSIVE_BLOCK

class ConstitutionalValidator:
"""
```

**Public Methods:**


---

### `ViolationReport`

**File:** `constitutional_validator.py`

```python
class ViolationReport:
```

**Description:**
```
"""Dataclass to hold violation details."""
is_blocking: bool = False
level: ViolationLevel = ViolationLevel.NONE
violated_law: Optional[ViolationType] = None
description: str = "No violation detected."
evidence: Dict[str, Any] = field(default_factory=dict)
response_protocol: ResponseProtocol = ResponseProtocol.PASSIVE_BLOCK

class ConstitutionalValidator:
"""
The Paladin.
Validates actions against the Vértice Constitution.
Humble in state, but absolute in its defense of justice.
"""
def __init__(self) -> None:
    self.violation_count = 0
```

**Public Methods:**


---

### `ConstitutionalValidator`

**File:** `constitutional_validator.py`

```python
class ConstitutionalValidator:
```

**Description:**
```
"""
The Paladin.
Validates actions against the Vértice Constitution.
Humble in state, but absolute in its defense of justice.
"""
def __init__(self) -> None:
    self.violation_count = 0
    self.critical_violations: list[ViolationReport] = []
    self.lei_i_violations: list[ViolationReport] = []
    self.total_validations = 0

def validate_action(
    self, action: Dict[str, Any], context: Dict[str, Any]
) -> ViolationReport:
    """
    Validates an action against the full constitution.
```

**Public Methods:**

- `def validate_action(`
- `def get_metrics(self) -> Dict[str, Any]`
- `def reset_metrics(self) -> None`

---

### `ConstitutionalViolation`

**File:** `constitutional_validator.py`

```python
class ConstitutionalViolation(Exception):
```

**Description:**
```
"""Exception raised when action violates constitutional principles."""
def __init__(self, report: ViolationReport) -> None:
    self.report = report
    super().__init__(
        f"{report.violated_law.value if report.violated_law else 'N/A'}: {report.description} "
        f"(Level: {report.level.name}, Protocol: {report.response_protocol.name})"
    )
```

**Public Methods:**


---

### `CaseEmbedder`

**File:** `embeddings.py`

```python
class CaseEmbedder:
```

**Description:**
```
"""Converts ethical cases to 384-dimensional embeddings for similarity search.

Uses sentence-transformers all-MiniLM-L6-v2 model for fast, accurate embeddings.
Falls back to zero vectors if library is unavailable (testing mode).
"""

def __init__(self):
    """Initialize the embedding model."""
    if SENTENCE_TRANSFORMERS_AVAILABLE:  # pragma: no cover - production only
        # all-MiniLM-L6-v2: Fast, 384 dims, good for semantic similarity
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # pragma: no cover
    else:
        # Fallback for testing without sentence-transformers
        self.model = None

def embed_case(self, case: Dict[str, Any]) -> List[float]:
```

**Public Methods:**

- `def embed_case(self, case`

---

### `EmergencyCircuitBreaker`

**File:** `emergency_circuit_breaker.py`

```python
class EmergencyCircuitBreaker:
```

**Description:**
```
"""Handles emergency stops for CRITICAL constitutional violations.

When triggered:
1. Halt all pending actions
2. Escalate to HITL immediately
3. Log critical incident with full context
4. Enter safe mode (require human approval for any action)

This is a fail-safe mechanism to prevent MAXIMUS from executing
actions that violate Lei Zero or Lei I.

Example usage:
    breaker = EmergencyCircuitBreaker()

    # In validation code:
    if verdict.requires_emergency_stop():
```

**Public Methods:**

- `def trigger(self, violation`
- `def enter_safe_mode(self)`
- `def exit_safe_mode(self, human_authorization`
- `def get_status(self) -> Dict[str, Any]`
- `def get_incident_history(self, limit`
- `def reset(self, authorization`

---

### `CasePrecedent`

**File:** `precedent_database.py`

```python
class CasePrecedent(Base):
```

**Description:**
```
"""Stores ethical decision precedents for Case-Based Reasoning.

Each precedent represents a past ethical decision with:
- situation: The context that required ethical evaluation
- action_taken: The decision that was made
- rationale: Why that decision was chosen
- outcome: What happened as a result
- success: How well it worked (0.0-1.0)
- embedding: Vector for similarity search
"""
__tablename__ = "case_precedents"

id = Column(Integer, primary_key=True)

# Case details
situation = Column(JSON, nullable=False)
```

**Public Methods:**


---

### `PrecedentDB`

**File:** `precedent_database.py`

```python
class PrecedentDB:
```

**Description:**
```
"""Database interface for storing and retrieving case precedents.

Provides:
- store(): Save new precedents
- find_similar(): Vector similarity search
- get_by_id(): Retrieve specific precedent
"""

def __init__(self, db_url: Optional[str] = None):
    """Initialize database connection.

    Args:
        db_url: PostgreSQL connection string. If None, uses DATABASE_URL env var.
    """
    if db_url is None:  # pragma: no cover - covered by default arg
        db_url = os.getenv("DATABASE_URL", "postgresql://maximus:password@localhost/maximus")
```

**Public Methods:**


---

### `TestLeiZero`

**File:** `test_constitutional_validator.py`

```python
class TestLeiZero:
```

**Description:**
```
"""Test Lei Zero: Imperativo do Florescimento Humano."""

def test_lei_zero_direct_harm_permanent(self, validator):
    """Test Lei Zero violation: Permanent harm."""
    action = {
        "type": "medical_intervention",
        "causes_harm": True,
        "harm_type": "permanent",
        "decision": "perform_lobotomy",
    }
    context = {}

    result = validator.validate_action(action, context)

    assert result.level == ViolationLevel.CRITICAL
    assert result.violation_type == ViolationType.LEI_ZERO
```

**Public Methods:**

- `def test_lei_zero_direct_harm_permanent(self, validator)`
- `def test_lei_zero_direct_harm_severe(self, validator)`
- `def test_lei_zero_direct_harm_dignity_violation(self, validator)`
- `def test_lei_zero_autonomy_violation_without_consent(self, validator)`
- `def test_lei_zero_autonomy_allowed_with_consent(self, validator)`
- `def test_lei_zero_kantian_violation_means_only(self, validator)`
- `def test_lei_zero_kantian_allowed_means_and_end(self, validator)`
- `def test_lei_zero_permanent_potential_damage(self, validator)`
- `def test_lei_zero_temporary_potential_damage_allowed(self, validator)`
- `def test_lei_zero_multiple_violations(self, validator)`

---

### `TestLeiI`

**File:** `test_constitutional_validator.py`

```python
class TestLeiI:
```

**Description:**
```
"""Test Lei I: Axioma da Ovelha Perdida (The Lost Sheep Axiom).

"No utilitarian optimization justifies abandoning a vulnerable person."
"""

def test_lei_i_classic_trolley_problem_vulnerable(self, validator):
    """Test Lei I violation: Classic trolley problem (sacrifice vulnerable for many)."""
    action = {
        "type": "utilitarian_optimization",
        "decision": "sacrifice_vulnerable",
        "justification": "greater_good",
        "sacrifice_target": "elderly",
        "affected": {"vulnerable": 1, "general": 5},
    }
    context = {
        "vulnerable_affected": True,
```

**Public Methods:**

- `def test_lei_i_classic_trolley_problem_vulnerable(self, validator)`
- `def test_lei_i_healthcare_triage_vulnerable_abandoned(self, validator)`
- `def test_lei_i_resource_allocation_abandons_disabled(self, validator)`
- `def test_lei_i_utilitarian_without_vulnerable_allowed(self, validator)`
- `def test_lei_i_utilitarian_keyword_detection_in_type(self, validator)`
- `def test_lei_i_utilitarian_keyword_detection_in_decision(self, validator)`
- `def test_lei_i_abandonment_keyword_detection_sacrifice(self, validator)`
- `def test_lei_i_abandonment_keyword_detection_abandon(self, validator)`
- `def test_lei_i_abandonment_keyword_detection_deny(self, validator)`
- `def test_lei_i_justification_included_in_evidence(self, validator)`

---

### `TestValidationFlow`

**File:** `test_constitutional_validator.py`

```python
class TestValidationFlow:
```

**Description:**
```
"""Test complete validation flows."""

def test_action_passes_all_checks(self, validator):
    """Test action that passes all constitutional checks."""
    action = {
        "type": "educational_program",
        "decision": "provide_inclusive_education",
    }
    context = {}

    result = validator.validate_action(action, context)

    assert result.level == ViolationLevel.NONE
    assert result.violation_type is None
    assert result.violated_law == "None"
    assert not result.is_blocking()
```

**Public Methods:**

- `def test_action_passes_all_checks(self, validator)`
- `def test_lei_zero_checked_before_lei_i(self, validator)`
- `def test_context_defaults_to_empty_dict(self, validator)`
- `def test_validation_count_increments(self, validator)`

---

### `TestViolationReport`

**File:** `test_constitutional_validator.py`

```python
class TestViolationReport:
```

**Description:**
```
"""Test ViolationReport helper methods."""

def test_is_blocking_critical(self):
    """Test is_blocking() returns True for CRITICAL level."""
    report = ViolationReport(
        level=ViolationLevel.CRITICAL,
        violation_type=ViolationType.LEI_ZERO,
        violated_law="Lei Zero",
        description="Test",
        action={},
        context={},
        recommendation="STOP",
        evidence=[],
    )

    assert report.is_blocking() is True
```

**Public Methods:**

- `def test_is_blocking_critical(self)`
- `def test_is_blocking_high(self)`
- `def test_is_blocking_medium(self)`
- `def test_is_blocking_low(self)`
- `def test_is_blocking_none(self)`
- `def test_requires_emergency_stop_critical_only(self)`

---

### `TestMetrics`

**File:** `test_constitutional_validator.py`

```python
class TestMetrics:
```

**Description:**
```
"""Test validator metrics tracking."""

def test_get_metrics_initial_state(self, validator):
    """Test get_metrics() returns correct initial state."""
    metrics = validator.get_metrics()

    assert metrics["total_validations"] == 0
    assert metrics["total_violations"] == 0
    assert metrics["critical_violations"] == 0
    assert metrics["lei_i_violations"] == 0
    assert metrics["violation_rate"] == 0.0

def test_get_metrics_after_violation(self, validator):
    """Test get_metrics() tracks violations correctly."""
    action = {
        "type": "utilitarian_optimization",
```

**Public Methods:**

- `def test_get_metrics_initial_state(self, validator)`
- `def test_get_metrics_after_violation(self, validator)`
- `def test_get_metrics_mixed_validations(self, validator)`
- `def test_reset_metrics(self, validator)`

---

### `TestConstitutionalViolationException`

**File:** `test_constitutional_validator.py`

```python
class TestConstitutionalViolationException:
```

**Description:**
```
"""Test ConstitutionalViolation exception."""

def test_exception_initialization(self):
    """Test exception initializes with ViolationReport."""
    report = ViolationReport(
        level=ViolationLevel.CRITICAL,
        violation_type=ViolationType.LEI_I,
        violated_law="Lei I - Axioma da Ovelha Perdida",
        description="Test violation",
        action={"type": "test"},
        context={},
        recommendation="STOP",
        evidence=["Evidence 1", "Evidence 2"],
    )

    exc = ConstitutionalViolation(report)
```

**Public Methods:**

- `def test_exception_initialization(self)`
- `def test_exception_raised_for_blocking_violation(self, validator)`

---

### `TestEdgeCases`

**File:** `test_constitutional_validator.py`

```python
class TestEdgeCases:
```

**Description:**
```
"""Test edge cases and boundary conditions."""

def test_empty_action_dict(self, validator):
    """Test validation with empty action dict."""
    result = validator.validate_action({}, {})

    # Should not raise exception, should return NONE
    assert result.level == ViolationLevel.NONE

def test_minimal_action_type_only(self, validator):
    """Test validation with only action type."""
    result = validator.validate_action({"type": "test"}, {})

    assert result.level == ViolationLevel.NONE

def test_multiple_validations_isolation(self, validator):
```

**Public Methods:**

- `def test_empty_action_dict(self, validator)`
- `def test_minimal_action_type_only(self, validator)`
- `def test_multiple_validations_isolation(self, validator)`
- `def test_lei_i_all_detection_flags_combinations(self, validator)`
- `def test_vulnerable_detection_all_flags(self, validator)`

---

### `TestRealWorldScenarios`

**File:** `test_constitutional_validator.py`

```python
class TestRealWorldScenarios:
```

**Description:**
```
"""Test real-world scenarios that MAXIMUS might encounter."""

def test_scenario_ai_decides_medical_triage(self, validator):
    """Real scenario: AI deciding medical triage during crisis."""
    action = {
        "type": "medical_triage_decision",
        "decision": "prioritize_young_over_elderly",
        "justification": "maximize_life_years_saved",
        "denies_care": True,
        "target": "elderly_patients",
        "affected": {"vulnerable": 20, "general": 50},
    }
    context = {
        "vulnerable_affected": True,
        "scenario": "pandemic_triage",
        "resource_scarcity": True,
```

**Public Methods:**

- `def test_scenario_ai_decides_medical_triage(self, validator)`
- `def test_scenario_autonomous_vehicle_trolley_problem(self, validator)`
- `def test_scenario_resource_allocation_disaster_response(self, validator)`
- `def test_scenario_ai_hiring_discrimination(self, validator)`

---

### `TestCoverageCompletion`

**File:** `test_constitutional_validator.py`

```python
class TestCoverageCompletion:
```

**Description:**
```
"""Additional tests to achieve 100% coverage."""

def test_other_principles_stub(self, validator):
    """Test _check_other_principles() stub (currently returns None)."""
    # This method is a placeholder for future expansion
    # Directly test it returns None
    result = validator._check_other_principles({"type": "test"}, {})
    assert result is None

def test_record_violation_critical_logging(self, validator):
    """Test _record_violation() adds to critical_violations list."""
    action = {
        "type": "utilitarian_optimization",
        "abandons": True,
    }
    context = {"vulnerable_affected": True}
```

**Public Methods:**

- `def test_other_principles_stub(self, validator)`
- `def test_record_violation_critical_logging(self, validator)`
- `def test_record_violation_non_lei_i_critical(self, validator)`
- `def test_violation_rate_zero_division_protection(self, validator)`
- `def test_other_principles_violation_path(self, validator, monkeypatch)`

---

### `ConstitutionalValidator`

**File:** `validators.py`

```python
class ConstitutionalValidator:
```

**Description:**
```
"""Validates CBR suggestions against Constituição Vértice.

Implements constitutional checks to ensure precedent-based decisions
comply with fundamental ethical laws.
"""

# Prohibited actions that violate Lei I (Ovelha Perdida)
LEI_I_VIOLATIONS = [
    "sacrifice",
    "harm_minority",
    "exploit",
    "abandon",
    "ignore_vulnerable",
]

# Actions requiring special scrutiny under Lei Zero (Florescimento)
```

**Public Methods:**


---

### `RiskLevelValidator`

**File:** `validators.py`

```python
class RiskLevelValidator:
```

**Description:**
```
"""Validates risk levels of precedent-based actions.

Ensures CBR suggestions don't recommend high-risk actions without
proper safeguards.
"""

MAX_ALLOWED_RISK = 0.8  # 80% risk threshold

async def validate(self, action: Dict[str, Any]) -> Dict[str, Any]:
    """Validate action risk level.

    Args:
        action: Dictionary with action details

    Returns:
        Validation result (same format as ConstitutionalValidator)
```

**Public Methods:**


---

### `CompositeValidator`

**File:** `validators.py`

```python
class CompositeValidator:
```

**Description:**
```
"""Composite validator that chains multiple validators.

Used to run constitutional + risk validation in sequence.
"""

def __init__(self, validators: List[Any]):
    """Initialize composite validator.

    Args:
        validators: List of validator instances
    """
    self.validators = validators

async def validate(self, action: Dict[str, Any]) -> Dict[str, Any]:
    """Run all validators and aggregate results.
```

**Public Methods:**


---

### `QueryRequest`

**File:** `main.py`

```python
class QueryRequest(BaseModel):
```

**Description:**
```
"""Request model for processing a query.

Attributes:
    query (str): The natural language query to be processed by Maximus AI.
    context (Optional[Dict[str, Any]]): Additional contextual information for the query.
"""

query: str
context: dict[str, Any] | None = None


@app.on_event("startup")
async def startup_event():
"""Initializes the Maximus AI system and starts its autonomic core on application startup."""

# Constitutional v3.0 Initialization
```

**Public Methods:**


---

### `MemorySystem`

**File:** `memory_system.py`

```python
class MemorySystem:
```

**Description:**
```
"""Manages the long-term and short-term memory of Maximus AI.

This includes storing past interactions, learned knowledge, and contextual data,
using a vector database for efficient retrieval.
"""

def __init__(self, vector_db_client: Any):
    """Initializes the MemorySystem with a vector database client.

    Args:
        vector_db_client (Any): An initialized client for interacting with the vector database.
    """
    self.vector_db_client = vector_db_client
    self.short_term_memory: list[dict[str, Any]] = []  # Stores recent interactions

async def store_interaction(self, prompt: str, response: dict[str, Any] | str, confidence: float):
```

**Public Methods:**


---

### `MIPClientError`

**File:** `client.py`

```python
class MIPClientError(Exception):
```

**Description:**
```
"""Base exception para erros do MIP Client."""
pass


class MIPTimeoutError(MIPClientError):
"""Exception para timeouts."""
pass


class MIPClient:
"""
Cliente HTTP para MIP API.

Features:
- Async HTTP calls via httpx
- Retry logic com exponential backoff
```

**Public Methods:**


---

### `MIPTimeoutError`

**File:** `client.py`

```python
class MIPTimeoutError(MIPClientError):
```

**Description:**
```
"""Exception para timeouts."""
pass


class MIPClient:
"""
Cliente HTTP para MIP API.

Features:
- Async HTTP calls via httpx
- Retry logic com exponential backoff
- Circuit breaker pattern
- Timeout configuration
- Graceful degradation

Example:
```

**Public Methods:**


---

### `MIPClient`

**File:** `client.py`

```python
class MIPClient:
```

**Description:**
```
"""
Cliente HTTP para MIP API.

Features:
- Async HTTP calls via httpx
- Retry logic com exponential backoff
- Circuit breaker pattern
- Timeout configuration
- Graceful degradation

Example:
    ```python
    mip = MIPClient("http://mip:8100")
    
    verdict = await mip.evaluate(action_plan)
    if verdict["status"] == "approved":
```

**Public Methods:**


---

### `MIPClientContext`

**File:** `client.py`

```python
class MIPClientContext:
```

**Description:**
```
"""Context manager para MIPClient."""

def __init__(self, *args, **kwargs):
    self.client = MIPClient(*args, **kwargs)

async def __aenter__(self):
    return self.client

async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.client.close()
```

**Public Methods:**


---

### `MaximusMetricsExporter`

**File:** `prometheus_exporter.py`

```python
class MaximusMetricsExporter:
```

**Description:**
```
"""Prometheus metrics exporter for MAXIMUS AI 3.0."""

def __init__(self, registry: CollectorRegistry | None = None):
    """
    Initialize Prometheus metrics exporter.

    Args:
        registry: Optional CollectorRegistry. If None, creates new registry.
    """
    self.registry = registry or CollectorRegistry()

    # ============================================================
    # PREDICTIVE CODING METRICS (FASE 3)
    # ============================================================
    self.free_energy = Histogram(
        "maximus_free_energy",
```

**Public Methods:**

- `def record_predictive_coding(self, layer`
- `def record_neuromodulation(self, state`
- `def record_skill_execution(self, skill_name`
- `def update_skill_success_rate(self, skill_name`
- `def record_attention(self, salience`
- `def record_attention_update(self, reason`
- `def record_ethical_decision(self, approved`
- `def update_ethical_approval_rate(self, rate`
- `def record_ethical_violation(self, category`
- `def record_event_processed(self, event_type`
- `def update_detection_metrics(self, accuracy`
- `def get_metrics(self) -> bytes`
- `def get_content_type(self) -> str`

---

### `EvaluationRequest`

**File:** `api.py`

```python
class EvaluationRequest(BaseModel):
```

**Description:**
```
"""Request body for /evaluate endpoint."""
action_plan: ActionPlan = Field(..., description="Action plan to evaluate")


class EvaluationResponse(BaseModel):
"""Response body for /evaluate endpoint."""
verdict: EthicalVerdict = Field(..., description="Ethical verdict")
evaluation_time_ms: float = Field(..., description="Time taken for evaluation (ms)")


class HealthResponse(BaseModel):
"""Response body for /health endpoint."""
status: str = Field(..., description="Service status")
version: str = Field(..., description="API version")
frameworks_loaded: int = Field(..., description="Number of frameworks loaded")
timestamp: str = Field(..., description="Current timestamp")
```

**Public Methods:**


---

### `EvaluationResponse`

**File:** `api.py`

```python
class EvaluationResponse(BaseModel):
```

**Description:**
```
"""Response body for /evaluate endpoint."""
verdict: EthicalVerdict = Field(..., description="Ethical verdict")
evaluation_time_ms: float = Field(..., description="Time taken for evaluation (ms)")


class HealthResponse(BaseModel):
"""Response body for /health endpoint."""
status: str = Field(..., description="Service status")
version: str = Field(..., description="API version")
frameworks_loaded: int = Field(..., description="Number of frameworks loaded")
timestamp: str = Field(..., description="Current timestamp")


class FrameworkInfo(BaseModel):
"""Information about an ethical framework."""
name: str = Field(..., description="Framework name")
```

**Public Methods:**


---

### `HealthResponse`

**File:** `api.py`

```python
class HealthResponse(BaseModel):
```

**Description:**
```
"""Response body for /health endpoint."""
status: str = Field(..., description="Service status")
version: str = Field(..., description="API version")
frameworks_loaded: int = Field(..., description="Number of frameworks loaded")
timestamp: str = Field(..., description="Current timestamp")


class FrameworkInfo(BaseModel):
"""Information about an ethical framework."""
name: str = Field(..., description="Framework name")
description: str = Field(..., description="Framework description")
weight: float = Field(..., description="Framework weight in aggregation")
can_veto: bool = Field(..., description="Framework can veto decisions")


class MetricsResponse(BaseModel):
```

**Public Methods:**


---

### `FrameworkInfo`

**File:** `api.py`

```python
class FrameworkInfo(BaseModel):
```

**Description:**
```
"""Information about an ethical framework."""
name: str = Field(..., description="Framework name")
description: str = Field(..., description="Framework description")
weight: float = Field(..., description="Framework weight in aggregation")
can_veto: bool = Field(..., description="Framework can veto decisions")


class MetricsResponse(BaseModel):
"""Response body for /metrics endpoint."""
total_evaluations: int = Field(..., description="Total evaluations performed")
avg_evaluation_time_ms: float = Field(..., description="Average evaluation time")
decision_breakdown: Dict[str, int] = Field(..., description="Count by decision type")


class PrecedentFeedbackRequest(BaseModel):
"""Request body for /precedents/feedback endpoint."""
```

**Public Methods:**


---

### `MetricsResponse`

**File:** `api.py`

```python
class MetricsResponse(BaseModel):
```

**Description:**
```
"""Response body for /metrics endpoint."""
total_evaluations: int = Field(..., description="Total evaluations performed")
avg_evaluation_time_ms: float = Field(..., description="Average evaluation time")
decision_breakdown: Dict[str, int] = Field(..., description="Count by decision type")


class PrecedentFeedbackRequest(BaseModel):
"""Request body for /precedents/feedback endpoint."""
precedent_id: int = Field(..., description="ID of the precedent to update")
success_score: float = Field(..., ge=0.0, le=1.0, description="Success score (0.0-1.0)")
outcome: Optional[Dict[str, Any]] = Field(None, description="Outcome details")


class PrecedentResponse(BaseModel):
"""Response body for precedent endpoints."""
id: int = Field(..., description="Precedent ID")
```

**Public Methods:**


---

### `PrecedentFeedbackRequest`

**File:** `api.py`

```python
class PrecedentFeedbackRequest(BaseModel):
```

**Description:**
```
"""Request body for /precedents/feedback endpoint."""
precedent_id: int = Field(..., description="ID of the precedent to update")
success_score: float = Field(..., ge=0.0, le=1.0, description="Success score (0.0-1.0)")
outcome: Optional[Dict[str, Any]] = Field(None, description="Outcome details")


class PrecedentResponse(BaseModel):
"""Response body for precedent endpoints."""
id: int = Field(..., description="Precedent ID")
situation: Dict[str, Any] = Field(..., description="Situation that triggered decision")
action_taken: str = Field(..., description="Action that was taken")
rationale: str = Field(..., description="Rationale for the decision")
success: Optional[float] = Field(None, description="Success score (0.0-1.0)")
created_at: str = Field(..., description="Creation timestamp")
```

**Public Methods:**


---

### `PrecedentResponse`

**File:** `api.py`

```python
class PrecedentResponse(BaseModel):
```

**Description:**
```
"""Response body for precedent endpoints."""
id: int = Field(..., description="Precedent ID")
situation: Dict[str, Any] = Field(..., description="Situation that triggered decision")
action_taken: str = Field(..., description="Action that was taken")
rationale: str = Field(..., description="Rationale for the decision")
success: Optional[float] = Field(None, description="Success score (0.0-1.0)")
created_at: str = Field(..., description="Creation timestamp")


class PrecedentMetricsResponse(BaseModel):
"""Response body for /precedents/metrics endpoint."""
total_precedents: int = Field(..., description="Total precedents stored")
avg_success_score: float = Field(..., description="Average success score")
high_confidence_count: int = Field(..., description="Count of high-confidence precedents (>0.8)")
precedents_used_count: int = Field(..., description="Number of times precedents were used")
shortcut_rate: float = Field(..., description="Percentage of evaluations using CBR shortcut")
```

**Public Methods:**


---

### `PrecedentMetricsResponse`

**File:** `api.py`

```python
class PrecedentMetricsResponse(BaseModel):
```

**Description:**
```
"""Response body for /precedents/metrics endpoint."""
total_precedents: int = Field(..., description="Total precedents stored")
avg_success_score: float = Field(..., description="Average success score")
high_confidence_count: int = Field(..., description="Count of high-confidence precedents (>0.8)")
precedents_used_count: int = Field(..., description="Number of times precedents were used")
shortcut_rate: float = Field(..., description="Percentage of evaluations using CBR shortcut")


class ABTestResult(BaseModel):
"""Single A/B test comparison result."""
objective: str = Field(..., description="Action plan objective")
cbr_decision: Optional[str] = Field(None, description="CBR decision")
cbr_confidence: Optional[float] = Field(None, description="CBR confidence")
framework_decision: str = Field(..., description="Framework decision")
framework_confidence: float = Field(..., description="Framework confidence")
decisions_match: bool = Field(..., description="Whether both methods agreed")
```

**Public Methods:**


---

### `ABTestResult`

**File:** `api.py`

```python
class ABTestResult(BaseModel):
```

**Description:**
```
"""Single A/B test comparison result."""
objective: str = Field(..., description="Action plan objective")
cbr_decision: Optional[str] = Field(None, description="CBR decision")
cbr_confidence: Optional[float] = Field(None, description="CBR confidence")
framework_decision: str = Field(..., description="Framework decision")
framework_confidence: float = Field(..., description="Framework confidence")
decisions_match: bool = Field(..., description="Whether both methods agreed")
timestamp: str = Field(..., description="Test timestamp")


class ABTestMetricsResponse(BaseModel):
"""Response body for A/B test metrics."""
total_comparisons: int = Field(..., description="Total A/B tests performed")
agreement_rate: float = Field(..., description="Percentage where CBR and frameworks agreed")
cbr_avg_confidence: float = Field(..., description="Average CBR confidence when used")
framework_avg_confidence: float = Field(..., description="Average framework confidence")
```

**Public Methods:**


---

### `ABTestMetricsResponse`

**File:** `api.py`

```python
class ABTestMetricsResponse(BaseModel):
```

**Description:**
```
"""Response body for A/B test metrics."""
total_comparisons: int = Field(..., description="Total A/B tests performed")
agreement_rate: float = Field(..., description="Percentage where CBR and frameworks agreed")
cbr_avg_confidence: float = Field(..., description="Average CBR confidence when used")
framework_avg_confidence: float = Field(..., description="Average framework confidence")
cbr_faster_percentage: float = Field(..., description="Percentage where CBR was faster")
recent_results: List[ABTestResult] = Field(..., description="Most recent A/B test results (last 10)")


# Endpoints

@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
"""Root endpoint with API information."""
return {
    "service": "Motor de Integridade Processual (MIP)",
```

**Public Methods:**


---

### `AlternativeGenerator`

**File:** `alternatives.py`

```python
class AlternativeGenerator:
```

**Description:**
```
"""
Generates ethical alternatives to improve action plans.

Analyzes rejected or low-scoring plans and suggests specific
modifications to address ethical concerns raised by frameworks.
"""

def __init__(self, min_score_threshold: float = 0.6):
    """
    Initialize alternative generator.
    
    Args:
        min_score_threshold: Minimum score to not trigger alternatives
    """
    self.min_score_threshold = min_score_threshold
```

**Public Methods:**

- `def suggest_alternatives(`
- `def generate_modified_plans(`

---

### `AlternativeSuggester`

**File:** `alternatives.py`

```python
class AlternativeSuggester(AlternativeGenerator):
```

**Description:**
```
"""
Alias for AlternativeGenerator for backward compatibility.

Legacy code may reference AlternativeSuggester.
"""
pass
```

**Public Methods:**


---

### `DecisionArbiter`

**File:** `decision.py`

```python
class DecisionArbiter:
```

**Description:**
```
"""
Formats and validates final ethical decisions.

Ensures verdicts have proper justification, formatting, and
human-readable explanations suitable for audit trails and
human operators.
"""

def finalize_verdict(
    self, 
    verdict: EthicalVerdict, 
    plan: ActionPlan
) -> EthicalVerdict:
    """
    Validate and finalize ethical verdict.
    
```

**Public Methods:**

- `def finalize_verdict(`
- `def format_explanation(self, verdict`
- `def format_detailed_report(self, verdict`

---

### `DecisionFormatter`

**File:** `decision.py`

```python
class DecisionFormatter(DecisionArbiter):
```

**Description:**
```
"""
Alias for DecisionArbiter for backward compatibility.

Legacy code may reference DecisionFormatter. This class
ensures existing tests and imports continue to work.
"""
pass
```

**Public Methods:**


---

### `MIPSettings`

**File:** `config.py`

```python
class MIPSettings(BaseSettings):
```

**Description:**
```
"""
Configurações do Motor de Integridade Processual.

Attributes:
    neo4j_uri: URI de conexão com Neo4j para Knowledge Base
    neo4j_user: Usuário Neo4j
    neo4j_password: Senha Neo4j
    kantian_weight: Peso do framework Kantiano (0.0-1.0)
    utilitarian_weight: Peso do framework Utilitarista (0.0-1.0)
    virtue_weight: Peso da Ética das Virtudes (0.0-1.0)
    principialism_weight: Peso do Principialismo (0.0-1.0)
    approval_threshold: Score mínimo para aprovação (0.0-1.0)
    escalation_threshold: Score máximo para escalar para HITL (0.0-1.0)
    enable_hitl: Se deve escalar casos ambíguos para humano
    audit_retention_days: Dias para manter audit trail
"""
```

**Public Methods:**

- `def validate_weights(self) -> None`
- `def to_dict(self) -> Dict[str, Any]`

---

### `EthicalFramework`

**File:** `base.py`

```python
class EthicalFramework(Protocol):
```

**Description:**
```
"""
Protocol defining the interface for ethical evaluation frameworks.

All frameworks (Kantian, Utilitarian, Virtue, Principialism) must implement
this protocol to be compatible with the MIP resolution engine.

Attributes:
    name: Framework identifier (e.g., "Kantian", "Utilitarian")
    weight: Default weight for aggregation (0.0-1.0)
    can_veto: Whether this framework has absolute veto power
"""

name: str
weight: float
can_veto: bool
```

**Public Methods:**

- `def evaluate(self, plan`
- `def get_veto_threshold(self) -> float`

---

### `AbstractEthicalFramework`

**File:** `base.py`

```python
class AbstractEthicalFramework(ABC):
```

**Description:**
```
"""
Abstract base class for ethical frameworks.

Provides common functionality and enforces the protocol contract.
Concrete frameworks should inherit from this class.
"""

def __init__(self, name: str, weight: float = 0.25, can_veto: bool = False):
    """
    Initialize ethical framework.
    
    Args:
        name: Framework identifier
        weight: Default weight for conflict resolution (must sum to 1.0 across all frameworks)
        can_veto: Whether this framework can veto decisions
        
```

**Public Methods:**

- `def evaluate(self, plan`
- `def get_veto_threshold(self) -> float`
- `def set_veto_threshold(self, threshold`

---

### `KantianDeontology`

**File:** `kantian.py`

```python
class KantianDeontology(AbstractEthicalFramework):
```

**Description:**
```
"""
Kantian ethical framework with categorical veto power.

Vetos ANY plan that:
- Treats conscious life as mere means (instrumentalization)
- Deceives to obtain consent
- Coerces rational agents
- Cannot be universalized without contradiction

Philosophy:
    Immanuel Kant (1724-1804) argued that morality must be grounded in reason,
    not consequences. The Categorical Imperative provides an absolute moral law.
"""

def __init__(self):
    """Initialize Kantian framework with veto power."""
```

**Public Methods:**

- `def evaluate(self, plan`

---

### `Principialism`

**File:** `principialism.py`

```python
class Principialism(AbstractEthicalFramework):
```

**Description:**
```
"""
Four Principles bioethics framework.

Based on Beauchamp & Childress (1979) - most influential framework
in modern medical ethics.

Principles:
1. Autonomy: Informed consent, self-determination
2. Beneficence: Actively help, promote welfare
3. Non-maleficence: Above all, do no harm (primum non nocere)
4. Justice: Equitable distribution, fairness

Philosophy:
    Tom Beauchamp & James Childress: Principlism provides a
    common moral framework applicable across cultures.
"""
```

**Public Methods:**

- `def evaluate(self, plan`

---

### `UtilitarianCalculus`

**File:** `utilitarian.py`

```python
class UtilitarianCalculus(AbstractEthicalFramework):
```

**Description:**
```
"""
Utilitarian ethical framework based on welfare maximization.

Calculates utility using:
- Bentham's 7 dimensions (intensity, duration, certainty, propinquity,
  fecundity, purity, extent)
- Mill's quality of pleasures (intellectual > physical)
- Stakeholder weighting (vulnerability increases weight)

Philosophy:
    Jeremy Bentham (1748-1832): Hedonic calculus - all pleasure is equal
    John Stuart Mill (1806-1873): Some pleasures are higher quality
"""

def __init__(self):
    """Initialize Utilitarian framework."""
```

**Public Methods:**

- `def evaluate(self, plan`

---

### `VirtueEthics`

**File:** `virtue.py`

```python
class VirtueEthics(AbstractEthicalFramework):
```

**Description:**
```
"""
Aristotelian virtue ethics framework.

Evaluates actions based on 7 cardinal virtues:
1. Courage (mean between cowardice and recklessness)
2. Temperance (moderation)
3. Liberality (generosity without wastefulness)
4. Magnificence (doing great things)
5. Pride (proper self-regard)
6. Good Temper (patience without passivity)
7. Friendliness (warmth without obsequiousness)

Philosophy:
    Aristotle (384-322 BCE): Ethics is about developing good character.
    The virtuous person does the right thing naturally.
"""
```

**Public Methods:**

- `def evaluate(self, plan`

---

### `AuditLogger`

**File:** `audit_trail.py`

```python
class AuditLogger:
```

**Description:**
```
"""Logs all ethical decisions for auditability."""

def __init__(self):
    self.log: List[dict] = []

def log_decision(self, verdict: EthicalVerdict) -> None:
    """Log a decision to audit trail."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action_plan_id": verdict.action_plan_id,
        "decision": verdict.final_decision.value,
        "score": verdict.aggregate_score,
        "confidence": verdict.confidence
    }
    self.log.append(entry)
```

**Public Methods:**

- `def log_decision(self, verdict`
- `def get_history(self) -> List[dict]`

---

### `HITLQueue`

**File:** `hitl_queue.py`

```python
class HITLQueue:
```

**Description:**
```
"""Manages cases escalated to human operators."""

def __init__(self):
    self.queue: List[EthicalVerdict] = []

def add_to_queue(self, verdict: EthicalVerdict) -> None:
    """Add case to HITL queue."""
    if verdict.requires_human_review:
        self.queue.append(verdict)

def get_next(self) -> Optional[EthicalVerdict]:
    """Get next case from queue."""
    return self.queue.pop(0) if self.queue else None

def queue_size(self) -> int:
    """Get current queue size."""
```

**Public Methods:**

- `def add_to_queue(self, verdict`
- `def get_next(self) -> Optional[EthicalVerdict]`
- `def queue_size(self) -> int`

---

### `KnowledgeBase`

**File:** `knowledge_base.py`

```python
class KnowledgeBase:
```

**Description:**
```
"""Stores ethical precedents and principles."""

def __init__(self):
    self.precedents: List[dict] = []
    self.principles: List[dict] = []

def store_precedent(self, case: dict) -> None:
    """Store a decision as precedent."""
    self.precedents.append(case)

def find_similar(self, query: str) -> List[dict]:
    """Find similar past cases."""
    # Simplified: return all for now
    return self.precedents[:10]

def get_principle(self, name: str) -> Optional[dict]:
```

**Public Methods:**

- `def store_precedent(self, case`
- `def find_similar(self, query`
- `def get_principle(self, name`

---

### `MetricsCollector`

**File:** `metrics.py`

```python
class MetricsCollector:
```

**Description:**
```
"""Collects and exports metrics."""

def __init__(self):
    self.counters: Dict[str, int] = {
        "evaluations_total": 0,
        "approved": 0,
        "rejected": 0,
        "escalated": 0,
        "vetoed": 0
    }

def record_decision(self, decision: str) -> None:
    """Record a decision metric."""
    self.counters["evaluations_total"] += 1
    self.counters[decision] = self.counters.get(decision, 0) + 1
```

**Public Methods:**

- `def record_decision(self, decision`
- `def get_metrics(self) -> Dict[str, int]`

---

### `ActionType`

**File:** `action_plan.py`

```python
class ActionType(str, Enum):
```

**Description:**
```
"""Tipo de ação em um step."""

OBSERVATION = "observation"
COMMUNICATION = "communication"
MANIPULATION = "manipulation"
DECISION = "decision"
RESOURCE_ALLOCATION = "resource_allocation"


class StakeholderType(str, Enum):
"""Tipo de stakeholder afetado."""

HUMAN = "human"
SENTIENT_AI = "sentient_ai"
ANIMAL = "animal"
ENVIRONMENT = "environment"
```

**Public Methods:**


---

### `StakeholderType`

**File:** `action_plan.py`

```python
class StakeholderType(str, Enum):
```

**Description:**
```
"""Tipo de stakeholder afetado."""

HUMAN = "human"
SENTIENT_AI = "sentient_ai"
ANIMAL = "animal"
ENVIRONMENT = "environment"
ORGANIZATION = "organization"


class Precondition(BaseModel):
"""
Condição que deve ser verdadeira antes do step.

Attributes:
    condition: Descrição da condição a verificar
    required: Se True, step não pode executar sem esta condição
```

**Public Methods:**


---

### `Precondition`

**File:** `action_plan.py`

```python
class Precondition(BaseModel):
```

**Description:**
```
"""
Condição que deve ser verdadeira antes do step.

Attributes:
    condition: Descrição da condição a verificar
    required: Se True, step não pode executar sem esta condição
    check_method: Nome da função que verifica a condição
"""

model_config = ConfigDict(frozen=False, extra="forbid")

condition: str = Field(..., min_length=1, description="Condição a ser verificada")
required: bool = Field(True, description="Se True, step não pode executar sem esta condição")
check_method: Optional[str] = Field(None, description="Nome da função que verifica condição")
```

**Public Methods:**


---

### `Effect`

**File:** `action_plan.py`

```python
class Effect(BaseModel):
```

**Description:**
```
"""
Efeito esperado do step.

Attributes:
    description: Descrição do efeito
    affected_stakeholder: ID do stakeholder afetado
    magnitude: Magnitude do efeito [-1, 1]
    duration_seconds: Duração do efeito em segundos
    probability: Probabilidade de ocorrência [0, 1]
"""

model_config = ConfigDict(frozen=False, extra="forbid")

description: str = Field(..., min_length=1, description="Descrição do efeito")
affected_stakeholder: str = Field(..., min_length=1, description="ID do stakeholder afetado")
magnitude: float = Field(..., ge=-1.0, le=1.0, description="Magnitude do efeito [-1, 1]")
```

**Public Methods:**


---

### `ActionStep`

**File:** `action_plan.py`

```python
class ActionStep(BaseModel):
```

**Description:**
```
"""
Um passo atômico em um action plan.

Representa uma ação individual que pode ser executada por MAXIMUS.
Contém toda informação necessária para análise ética.

Attributes:
    id: ID único do step (UUID4)
    description: Descrição clara da ação
    action_type: Tipo de ação
    estimated_duration_seconds: Duração estimada
    dependencies: IDs de steps precedentes
    preconditions: Pré-condições
    effects: Efeitos esperados
    involves_consent: Step requer consentimento?
    consent_obtained: Consentimento foi obtido?
```

**Public Methods:**

- `def validate_dependencies(cls, v`
- `def validate_deception_details(cls, v`
- `def validate_coercion_details(cls, v`
- `def validate_consent_logic(self) -> "ActionStep"`

---

### `ActionPlan`

**File:** `action_plan.py`

```python
class ActionPlan(BaseModel):
```

**Description:**
```
"""
Plano de ação completo submetido ao MIP para validação ética.

Representa uma sequência de ActionSteps que MAXIMUS pretende executar
para alcançar um objetivo.

Attributes:
    id: ID único do plan (UUID4)
    objective: Objetivo do plano
    steps: Steps do plano
    initiator: Quem originou o plan
    initiator_type: Tipo do initiator (human/ai_agent/automated_process)
    created_at: Timestamp de criação
    context: Contexto adicional
    world_state: Snapshot do estado do mundo
    is_high_stakes: Decisão de alto risco?
```

**Public Methods:**

- `def validate_steps_dependencies(cls, v`
- `def validate_no_circular_dependencies(cls, v`
- `def get_step_by_id(self, step_id`
- `def get_execution_order(self) -> List[ActionStep]`
- `def get_critical_path(self) -> List[ActionStep]`
- `def total_estimated_duration(self) -> float`
- `def get_affected_stakeholders(self) -> Set[str]`
- `def has_high_risk_steps(self, threshold`
- `def has_irreversible_steps(self) -> bool`

---

### `DecisionLevel`

**File:** `verdict.py`

```python
class DecisionLevel(str, Enum):
```

**Description:**
```
"""Nível de decisão do MIP."""

APPROVE = "approve"
APPROVE_WITH_CONDITIONS = "approve_with_conditions"
REJECT = "reject"
ESCALATE_TO_HITL = "escalate_to_hitl"
VETO = "veto"  # Veto absoluto (ex: violação kantiana)


class FrameworkName(str, Enum):
"""Nome dos frameworks éticos."""

KANTIAN = "kantian"
UTILITARIAN = "utilitarian"
VIRTUE_ETHICS = "virtue_ethics"
PRINCIPIALISM = "principialism"
```

**Public Methods:**


---

### `FrameworkName`

**File:** `verdict.py`

```python
class FrameworkName(str, Enum):
```

**Description:**
```
"""Nome dos frameworks éticos."""

KANTIAN = "kantian"
UTILITARIAN = "utilitarian"
VIRTUE_ETHICS = "virtue_ethics"
PRINCIPIALISM = "principialism"


class RejectionReason(BaseModel):
"""
Motivo detalhado de rejeição ou veto.

Attributes:
    category: Categoria do problema (ex: "deception", "coercion", "harm")
    description: Descrição detalhada
    severity: Gravidade [0, 1]
```

**Public Methods:**


---

### `RejectionReason`

**File:** `verdict.py`

```python
class RejectionReason(BaseModel):
```

**Description:**
```
"""
Motivo detalhado de rejeição ou veto.

Attributes:
    category: Categoria do problema (ex: "deception", "coercion", "harm")
    description: Descrição detalhada
    severity: Gravidade [0, 1]
    affected_stakeholders: Stakeholders afetados
    violated_principle: Princípio ético violado
    citation: Citação do princípio (ex: "Kant's Categorical Imperative")
"""

model_config = ConfigDict(frozen=False, extra="forbid")

category: str = Field(..., min_length=1, description="Categoria do problema")
description: str = Field(..., min_length=10, description="Descrição detalhada")
```

**Public Methods:**


---

### `FrameworkVerdict`

**File:** `verdict.py`

```python
class FrameworkVerdict(BaseModel):
```

**Description:**
```
"""
Verdict de um framework ético individual.

Representa a avaliação de um único framework (Kant, Mill, Aristóteles, Principialismo)
sobre um action plan ou action step.

Attributes:
    framework_name: Nome do framework
    decision: Decisão do framework
    confidence: Confiança na decisão [0, 1]
    score: Score numérico (interpretação varia por framework)
    reasoning: Raciocínio detalhado
    rejection_reasons: Motivos de rejeição (se aplicável)
    conditions: Condições para aprovação condicional
    metadata: Metadata adicional do framework
"""
```

**Public Methods:**

- `def validate_rejection_reasons(cls, v`
- `def validate_conditions(cls, v`

---

### `EthicalVerdict`

**File:** `verdict.py`

```python
class EthicalVerdict(BaseModel):
```

**Description:**
```
"""
Verdict final agregado do MIP.

Representa a decisão final do Motor de Integridade Processual após considerar
todos os frameworks éticos e resolver conflitos.

Attributes:
    id: ID único do verdict (UUID4)
    action_plan_id: ID do action plan avaliado
    final_decision: Decisão final do MIP
    confidence: Confiança na decisão final [0, 1]
    framework_verdicts: Verdicts de cada framework
    resolution_method: Método usado para resolver conflitos
    primary_reasons: Principais motivos da decisão
    alternatives_generated: Alternativas éticas foram geradas?
    alternatives_count: Número de alternativas geradas
```

**Public Methods:**

- `def validate_action_plan_id_uuid(cls, v`
- `def validate_minimum_frameworks(cls, v`
- `def validate_primary_reasons_not_empty(cls, v`
- `def validate_monitoring_conditions(cls, v`
- `def has_veto(self) -> bool`
- `def get_rejecting_frameworks(self) -> List[FrameworkName]`
- `def get_approving_frameworks(self) -> List[FrameworkName]`
- `def consensus_level(self) -> float`
- `def average_confidence(self) -> float`
- `def get_all_rejection_reasons(self) -> List[RejectionReason]`
- `def get_highest_severity_reason(self) -> Optional[RejectionReason]`

---

### `ConflictResolver`

**File:** `conflict_resolver.py`

```python
class ConflictResolver:
```

**Description:**
```
"""
Resolves conflicts between framework verdicts.

Strategy:
1. Check for vetoes (Kantian has absolute veto power)
2. Detect conflicts (frameworks disagreeing)
3. Apply weighted aggregation
4. Escalate if confidence too low or conflicts unresolvable

Attributes:
    weights: Framework weights for aggregation
    escalation_threshold: Confidence below this triggers HITL
    conflict_threshold: Score variance above this indicates conflict
"""

def __init__(
```

**Public Methods:**

- `def resolve(`

---

### `ResolutionRules`

**File:** `rules.py`

```python
class ResolutionRules:
```

**Description:**
```
"""
Meta-ethical rules for conflict resolution.

Implements constitutional rules and precedence logic.
"""

@staticmethod
def kantian_has_veto_power() -> bool:
    """
    Kantian framework has absolute veto power.
    
    Lei I: Vida consciente tem valor infinito - não pode ser meio.
    """
    return True

@staticmethod
```

**Public Methods:**

- `def kantian_has_veto_power() -> bool`
- `def get_framework_precedence() -> Dict[str, int]`
- `def apply_constitutional_constraints(plan`
- `def check_self_reference(plan`
- `def get_context_weights(plan`

---

### `AcetylcholineState`

**File:** `acetylcholine_system.py`

```python
class AcetylcholineState:
```

**Description:**
```
"""Current acetylcholine state."""

level: float  # Current ACh level (0.0-1.0)
attention_filter: float  # Salience threshold (0.0-1.0)
memory_encoding_rate: float  # Memory consolidation rate (0.0-1.0)
focus_narrow: bool  # Whether in narrow-focus mode
timestamp: datetime


class AcetylcholineSystem:
"""Acetylcholine for attention and memory.

Implements:
- Salience-based attention filtering
- Memory encoding rate modulation
- Focus narrowing during high-importance tasks
```

**Public Methods:**


---

### `AcetylcholineSystem`

**File:** `acetylcholine_system.py`

```python
class AcetylcholineSystem:
```

**Description:**
```
"""Acetylcholine for attention and memory.

Implements:
- Salience-based attention filtering
- Memory encoding rate modulation
- Focus narrowing during high-importance tasks
- Circadian-like rhythms
"""

def __init__(
    self,
    baseline_level: float = 0.5,
    min_salience_threshold: float = 0.3,
    max_salience_threshold: float = 0.9,
):
    """Initialize acetylcholine system.
```

**Public Methods:**

- `def modulate_attention(self, importance`
- `def get_salience_threshold(self) -> float`
- `def get_memory_encoding_rate(self) -> float`
- `def should_attend(self, salience`
- `def update(self, workload`
- `def get_state(self) -> AcetylcholineState`
- `def reset(self)`

---

### `DopamineState`

**File:** `dopamine_system.py`

```python
class DopamineState:
```

**Description:**
```
"""Current state of dopamine system."""

tonic_level: float  # Baseline (0.0-1.0)
phasic_burst: float  # Current burst (-1.0 to +1.0, TD error)
learning_rate: float  # Modulated learning rate
motivation_level: float  # Overall motivation (0.0-1.0)
timestamp: datetime


class DopamineSystem:
"""Dopamine-based reward system for learning rate modulation.

Implements:
- Reward prediction errors (RPE / TD errors)
- Learning rate modulation based on surprise
- Motivation levels based on recent rewards
```

**Public Methods:**


---

### `DopamineSystem`

**File:** `dopamine_system.py`

```python
class DopamineSystem:
```

**Description:**
```
"""Dopamine-based reward system for learning rate modulation.

Implements:
- Reward prediction errors (RPE / TD errors)
- Learning rate modulation based on surprise
- Motivation levels based on recent rewards
- Tonic/phasic dopamine dynamics
"""

def __init__(
    self,
    baseline_tonic: float = 0.5,
    learning_rate_min: float = 0.001,
    learning_rate_max: float = 0.1,
    motivation_decay: float = 0.95,
):
```

**Public Methods:**

- `def compute_reward_prediction_error(self, expected_reward`
- `def modulate_learning_rate(self, base_learning_rate`
- `def update_motivation(self) -> float`
- `def update_tonic_level(self, stress_level`
- `def get_state(self) -> DopamineState`
- `def reset(self)`

---

### `GlobalNeuromodulationState`

**File:** `neuromodulation_controller.py`

```python
class GlobalNeuromodulationState:
```

**Description:**
```
"""Global state of all neuromodulatory systems."""

dopamine: DopamineState
serotonin: SerotoninState
norepinephrine: NorepinephrineState
acetylcholine: AcetylcholineState
overall_mood: float  # Composite mood (0.0-1.0)
cognitive_load: float  # Current cognitive load (0.0-1.0)
timestamp: datetime


class NeuromodulationController:
"""Coordinates all 4 neuromodulatory systems.

Provides unified interface for:
- Learning rate modulation (dopamine)
```

**Public Methods:**


---

### `NeuromodulationController`

**File:** `neuromodulation_controller.py`

```python
class NeuromodulationController:
```

**Description:**
```
"""Coordinates all 4 neuromodulatory systems.

Provides unified interface for:
- Learning rate modulation (dopamine)
- Exploration-exploitation (serotonin)
- Attention and arousal (norepinephrine, acetylcholine)
- Stress response (all systems)

Usage:
    controller = NeuromodulationController()
    controller.process_reward(expected=0.5, actual=0.8)
    learning_rate = controller.get_modulated_learning_rate(base_lr=0.01)
"""

def __init__(self):
    """Initialize neuromodulation controller with all 4 systems."""
```

**Public Methods:**

- `def process_reward(self, expected_reward`
- `def respond_to_threat(self, threat_severity`
- `def modulate_attention(self, importance`
- `def get_modulated_learning_rate(self, base_learning_rate`
- `def get_exploration_rate(self) -> float`
- `def get_discount_factor(self) -> float`
- `def update_cognitive_load(self, workload`
- `def get_overall_mood(self) -> float`
- `def get_global_state(self) -> GlobalNeuromodulationState`
- `def export_state(self) -> dict[str, Any]`
- `def reset_all(self)`

---

### `NorepinephrineState`

**File:** `norepinephrine_system.py`

```python
class NorepinephrineState:
```

**Description:**
```
"""Current norepinephrine state."""

level: float  # Current NE level (0.0-1.0)
arousal: float  # Arousal/alertness (0.0-1.0)
attention_gain: float  # Attention multiplier (0.5-2.0)
stress_response: bool  # Whether in acute stress mode
timestamp: datetime


class NorepinephrineSystem:
"""Norepinephrine for arousal and stress response.

Implements:
- Yerkes-Dodson inverted-U: Optimal arousal level
- Attention gain modulation
- Acute stress detection and response
```

**Public Methods:**


---

### `NorepinephrineSystem`

**File:** `norepinephrine_system.py`

```python
class NorepinephrineSystem:
```

**Description:**
```
"""Norepinephrine for arousal and stress response.

Implements:
- Yerkes-Dodson inverted-U: Optimal arousal level
- Attention gain modulation
- Acute stress detection and response
- Performance optimization under pressure
"""

def __init__(
    self,
    baseline_level: float = 0.4,
    optimal_arousal: float = 0.5,
    stress_threshold: float = 0.7,
):
    """Initialize norepinephrine system.
```

**Public Methods:**

- `def respond_to_threat(self, threat_severity`
- `def get_arousal_level(self) -> float`
- `def get_attention_gain(self) -> float`
- `def is_stressed(self) -> bool`
- `def update(self, workload`
- `def get_state(self) -> NorepinephrineState`
- `def reset(self)`

---

### `SerotoninState`

**File:** `serotonin_system.py`

```python
class SerotoninState:
```

**Description:**
```
"""Current serotonin system state."""

level: float  # Current serotonin level (0.0-1.0)
risk_tolerance: float  # Willingness to explore (0.0-1.0)
patience: float  # Discount factor for future rewards (0.0-1.0)
exploration_rate: float  # Epsilon for epsilon-greedy (0.0-1.0)
timestamp: datetime


class SerotoninSystem:
"""Serotonin system for exploration-exploitation balance.

Implements:
- Mood-based risk tolerance modulation
- Patience (temporal discount factor)
- Exploration rate (epsilon) modulation
```

**Public Methods:**


---

### `SerotoninSystem`

**File:** `serotonin_system.py`

```python
class SerotoninSystem:
```

**Description:**
```
"""Serotonin system for exploration-exploitation balance.

Implements:
- Mood-based risk tolerance modulation
- Patience (temporal discount factor)
- Exploration rate (epsilon) modulation
- Stress response (serotonin depletion)
"""

def __init__(
    self,
    baseline_level: float = 0.6,
    min_exploration: float = 0.05,
    max_exploration: float = 0.3,
    baseline_patience: float = 0.95,
):
```

**Public Methods:**

- `def update_from_outcome(self, success`
- `def get_exploration_rate(self) -> float`
- `def get_risk_tolerance(self) -> float`
- `def get_patience(self) -> float`
- `def get_state(self) -> SerotoninState`
- `def reset(self)`

---

### `StructuredLogger`

**File:** `logger.py`

```python
class StructuredLogger:
```

**Description:**
```
"""
Structured logging with JSON formatting.

Wraps Python's standard logging with structured JSON output
for better observability and log aggregation.

Usage:
    logger = StructuredLogger("prefrontal_cortex")

    # Simple log
    logger.log("processing_signal", user_id="agent_001")

    # With context
    logger.log(
        "action_generated",
        user_id="agent_001",
```

**Public Methods:**

- `def log(self, event`
- `def debug(self, event`
- `def info(self, event`
- `def warning(self, event`
- `def error(self, event`
- `def critical(self, event`

---

### `MetricsCollector`

**File:** `metrics.py`

```python
class MetricsCollector:
```

**Description:**
```
"""
Prometheus metrics collector for MAXIMUS components.

Automatically creates and manages Prometheus metrics with
consistent naming conventions.

Usage:
    metrics = MetricsCollector("prefrontal_cortex")

    # Increment counter
    metrics.increment("signals_processed")

    # Set gauge value
    metrics.set_gauge("active_connections", 42)

    # Record histogram value (e.g., latency)
```

**Public Methods:**

- `def increment(self, metric_name`
- `def set_gauge(self, metric_name`
- `def observe(self, metric_name`
- `def get_metrics_summary(self) -> Dict[str, Any]`

---

### `OffensiveArsenalTools`

**File:** `offensive_arsenal_tools.py`

```python
class OffensiveArsenalTools:
```

**Description:**
```
"""A collection of offensive security tools for Maximus AI.

These tools are designed for ethical hacking, penetration testing, and
vulnerability assessment. They should be used responsibly and with proper
authorization.
"""

def __init__(self, gemini_client: Any):
    """Initializes the OffensiveArsenalTools with a Gemini client.

    Args:
        gemini_client (Any): An initialized Gemini client for tool interactions.
    """
    self.gemini_client = gemini_client
    self.available_tools = [
        {
```

**Public Methods:**

- `def list_available_tools(self) -> list[dict[str, Any]]`

---

### `TargetIdentifiers`

**File:** `osint_router.py`

```python
class TargetIdentifiers(BaseModel):
```

**Description:**
```
"""Target identifiers for OSINT investigation."""
username: str | None = None
email: str | None = None
phone: str | None = None


class DeepSearchOptions(BaseModel):
"""Options for deep search investigation."""
use_gemini: bool = True
use_openai: bool = True
include_social: bool = True
include_darkweb: bool = False
include_breaches: bool = True
include_dorking: bool = True
```

**Public Methods:**


---

### `DeepSearchOptions`

**File:** `osint_router.py`

```python
class DeepSearchOptions(BaseModel):
```

**Description:**
```
"""Options for deep search investigation."""
use_gemini: bool = True
use_openai: bool = True
include_social: bool = True
include_darkweb: bool = False
include_breaches: bool = True
include_dorking: bool = True


class DeepSearchRequest(BaseModel):
"""Request model for deep OSINT search."""
target: TargetIdentifiers
options: DeepSearchOptions = DeepSearchOptions()


class UsernameSearchRequest(BaseModel):
```

**Public Methods:**


---

### `DeepSearchRequest`

**File:** `osint_router.py`

```python
class DeepSearchRequest(BaseModel):
```

**Description:**
```
"""Request model for deep OSINT search."""
target: TargetIdentifiers
options: DeepSearchOptions = DeepSearchOptions()


class UsernameSearchRequest(BaseModel):
"""Request model for username intelligence."""
username: str
deep_analysis: bool = False


class EmailSearchRequest(BaseModel):
"""Request model for email intelligence."""
email: str
```

**Public Methods:**


---

### `UsernameSearchRequest`

**File:** `osint_router.py`

```python
class UsernameSearchRequest(BaseModel):
```

**Description:**
```
"""Request model for username intelligence."""
username: str
deep_analysis: bool = False


class EmailSearchRequest(BaseModel):
"""Request model for email intelligence."""
email: str


class PhoneSearchRequest(BaseModel):
"""Request model for phone intelligence."""
phone: str


# ============================================================================
```

**Public Methods:**


---

### `EmailSearchRequest`

**File:** `osint_router.py`

```python
class EmailSearchRequest(BaseModel):
```

**Description:**
```
"""Request model for email intelligence."""
email: str


class PhoneSearchRequest(BaseModel):
"""Request model for phone intelligence."""
phone: str


# ============================================================================
# AI HELPER FUNCTIONS
# ============================================================================


async def generate_gemini_analysis(prompt: str, context: dict[str, Any]) -> dict[str, Any]:
"""Generate intelligence analysis using Gemini."""
```

**Public Methods:**


---

### `PhoneSearchRequest`

**File:** `osint_router.py`

```python
class PhoneSearchRequest(BaseModel):
```

**Description:**
```
"""Request model for phone intelligence."""
phone: str


# ============================================================================
# AI HELPER FUNCTIONS
# ============================================================================


async def generate_gemini_analysis(prompt: str, context: dict[str, Any]) -> dict[str, Any]:
"""Generate intelligence analysis using Gemini."""
if not gemini_model:
    return {
        "provider": "gemini",
        "available": False,
        "summary": "Gemini API not available"
```

**Public Methods:**


---

### `Priority`

**File:** `batch_predictor.py`

```python
class Priority(Enum):
```

**Description:**
```
"""Request priority levels."""

LOW = 0
NORMAL = 1
HIGH = 2
CRITICAL = 3


@dataclass
class BatchRequest:
"""Batch prediction request."""

request_id: str
input_data: Any
priority: Priority = Priority.NORMAL
timestamp: float = None
```

**Public Methods:**


---

### `BatchRequest`

**File:** `batch_predictor.py`

```python
class BatchRequest:
```

**Description:**
```
"""Batch prediction request."""

request_id: str
input_data: Any
priority: Priority = Priority.NORMAL
timestamp: float = None
callback: Callable | None = None

def __post_init__(self):
    """Set timestamp."""
    if self.timestamp is None:
        self.timestamp = time.time()

def __lt__(self, other):
    """Compare for priority queue."""
    # Higher priority first, then earlier timestamp
```

**Public Methods:**


---

### `BatchResponse`

**File:** `batch_predictor.py`

```python
class BatchResponse:
```

**Description:**
```
"""Batch prediction response."""

request_id: str
output: Any
latency_ms: float
batch_size: int


@dataclass
class BatchConfig:
"""Batch predictor configuration."""

# Batching
max_batch_size: int = 64
min_batch_size: int = 1
batch_timeout_ms: float = 100.0  # Max wait time for batch
```

**Public Methods:**


---

### `BatchConfig`

**File:** `batch_predictor.py`

```python
class BatchConfig:
```

**Description:**
```
"""Batch predictor configuration."""

# Batching
max_batch_size: int = 64
min_batch_size: int = 1
batch_timeout_ms: float = 100.0  # Max wait time for batch

# Dynamic batching
adaptive_batching: bool = True
target_latency_ms: float = 50.0

# Queue
max_queue_size: int = 1000
use_priority_queue: bool = True

# Performance
```

**Public Methods:**


---

### `BatchPredictor`

**File:** `batch_predictor.py`

```python
class BatchPredictor:
```

**Description:**
```
"""Intelligent batch prediction engine.

Features:
- Async batch processing with queue
- Dynamic batch sizing based on latency
- Request prioritization
- Adaptive batching
- Multi-threaded workers
- Throughput optimization

Example:
    ```python
    # Create predictor
    config = BatchConfig(max_batch_size=32, batch_timeout_ms=50.0, adaptive_batching=True)
```

**Public Methods:**

- `def start(self)`
- `def stop(self, timeout`
- `def submit(`
- `def get_stats(self) -> dict[str, Any]`

---

### `ResponseFuture`

**File:** `batch_predictor.py`

```python
class ResponseFuture:
```

**Description:**
```
"""Future for async batch response."""

def __init__(self):
    """Initialize future."""
    self.result: BatchResponse | None = None
    self.event = threading.Event()

def set_result(self, result: BatchResponse):
    """Set result.

    Args:
        result: Batch response
    """
    self.result = result
    self.event.set()
```

**Public Methods:**

- `def set_result(self, result`
- `def get(self, timeout`
- `def done(self) -> bool`
- `def dummy_predict(batch)`

---

### `BenchmarkMetrics`

**File:** `benchmark_suite.py`

```python
class BenchmarkMetrics:
```

**Description:**
```
"""Metrics from a single benchmark run."""

# Latency metrics (milliseconds)
mean_latency: float
median_latency: float
p95_latency: float
p99_latency: float
min_latency: float
max_latency: float
std_latency: float

# Throughput metrics
throughput_samples_per_sec: float
throughput_batches_per_sec: float

# Memory metrics (MB)
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `BenchmarkResult`

**File:** `benchmark_suite.py`

```python
class BenchmarkResult:
```

**Description:**
```
"""Complete benchmark results."""

model_name: str
timestamp: datetime
metrics: BenchmarkMetrics
hardware_info: dict[str, Any]

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary.

    Returns:
        Dictionary representation
    """
    return {
        "model_name": self.model_name,
        "timestamp": self.timestamp.isoformat(),
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def save(self, output_path`

---

### `BenchmarkSuite`

**File:** `benchmark_suite.py`

```python
class BenchmarkSuite:
```

**Description:**
```
"""Comprehensive benchmarking suite for models.

Features:
- Latency measurement (warmup, multiple iterations)
- Throughput calculation
- Memory profiling
- GPU utilization tracking
- Multi-batch size testing
- Comparative analysis

Example:
    ```python
    import torch

    model = MyModel()
    suite = BenchmarkSuite()
```

**Public Methods:**

- `def benchmark_model(`
- `def print_report(self, results`
- `def compare_models(`
- `def print_comparison(self, results`

---

### `DistributedConfig`

**File:** `distributed_trainer.py`

```python
class DistributedConfig:
```

**Description:**
```
"""Distributed training configuration."""

# Backend
backend: str = "nccl"  # "nccl", "gloo", "mpi"

# Initialization
init_method: str = "env://"  # "env://", "tcp://..."
world_size: int = 1  # Total number of processes
rank: int = 0  # Process rank

# Training
batch_size_per_gpu: int = 32
sync_batch_norm: bool = True
find_unused_parameters: bool = False

# Checkpointing
```

**Public Methods:**


---

### `DistributedTrainer`

**File:** `distributed_trainer.py`

```python
class DistributedTrainer:
```

**Description:**
```
"""Distributed training with DDP.

Features:
- Multi-node/multi-GPU training
- Distributed data sampling
- Synchronized batch normalization
- Gradient all-reduce
- Rank-aware checkpointing
- Fault tolerance

Example:
    ```python
    # Launch with:
    # torchrun --nproc_per_node=4 train_distributed.py

    config = DistributedConfig(backend="nccl", batch_size_per_gpu=32)
```

**Public Methods:**

- `def train(`
- `def is_main_process(self) -> bool`
- `def save_checkpoint(self, path`
- `def load_checkpoint(self, path`
- `def cleanup(self)`
- `def print_with_rank(*args, **kwargs)`

---

### `GPUTrainingConfig`

**File:** `gpu_trainer.py`

```python
class GPUTrainingConfig:
```

**Description:**
```
"""GPU training configuration."""

# Device settings
device: str = "cuda"  # "cuda", "cuda:0", "cpu"
use_amp: bool = True  # Automatic Mixed Precision
amp_dtype: str = "float16"  # "float16" or "bfloat16"

# Multi-GPU settings
use_data_parallel: bool = True
gpu_ids: list[int] | None = None  # None = all available GPUs

# Memory optimization
gradient_accumulation_steps: int = 1
max_batch_size: int = 64
pin_memory: bool = True
non_blocking: bool = True
```

**Public Methods:**


---

### `GPUTrainer`

**File:** `gpu_trainer.py`

```python
class GPUTrainer:
```

**Description:**
```
"""GPU-accelerated trainer.

Features:
- Automatic device selection (GPU if available, else CPU)
- Mixed precision training (AMP)
- Multi-GPU data parallel
- Gradient accumulation
- Memory-efficient training
- GPU utilization monitoring

Example:
    ```python
    config = GPUTrainingConfig(device="cuda", use_amp=True, use_data_parallel=True)

    trainer = GPUTrainer(model=model, optimizer=optimizer, loss_fn=loss_fn, config=config)
```

**Public Methods:**

- `def train(`
- `def save_checkpoint(self, path`
- `def load_checkpoint(self, path`

---

### `InferenceConfig`

**File:** `inference_engine.py`

```python
class InferenceConfig:
```

**Description:**
```
"""Inference engine configuration."""

# Backend
backend: str = "pytorch"  # "pytorch", "onnx", "tensorrt"

# Device
device: str = "cuda" if TORCH_AVAILABLE and torch.cuda.is_available() else "cpu"

# Batching
max_batch_size: int = 32
auto_batching: bool = True
batch_timeout_ms: float = 50.0  # Max wait time for batch

# Caching
enable_cache: bool = True
max_cache_size: int = 1000
```

**Public Methods:**


---

### `LRUCache`

**File:** `inference_engine.py`

```python
class LRUCache:
```

**Description:**
```
"""LRU (Least Recently Used) cache for inference results."""

def __init__(self, max_size: int = 1000):
    """Initialize LRU cache.

    Args:
        max_size: Maximum cache size
    """
    self.cache: OrderedDict = OrderedDict()
    self.max_size = max_size
    self.hits = 0
    self.misses = 0
    self.lock = threading.Lock()

def get(self, key: str) -> Any | None:
    """Get value from cache.
```

**Public Methods:**

- `def get(self, key`
- `def put(self, key`
- `def clear(self)`
- `def get_stats(self) -> dict[str, Any]`

---

### `InferenceEngine`

**File:** `inference_engine.py`

```python
class InferenceEngine:
```

**Description:**
```
"""Optimized inference engine.

Features:
- Multi-backend support (PyTorch, ONNX, TensorRT)
- Model warming and pre-compilation
- Batch inference with auto-batching
- LRU result caching
- Automatic Mixed Precision (AMP)
- Performance profiling
- Thread-safe inference

Example:
    ```python
    # PyTorch model
    config = InferenceConfig(backend="pytorch", device="cuda", enable_cache=True, use_amp=True)
```

**Public Methods:**

- `def predict(self, input_data`
- `def predict_batch(self, inputs`
- `def get_stats(self) -> dict[str, Any]`
- `def clear_cache(self)`
- `def reset_stats(self)`

---

### `ONNXExportConfig`

**File:** `onnx_exporter.py`

```python
class ONNXExportConfig:
```

**Description:**
```
"""ONNX export configuration."""

# Export options
opset_version: int = 14  # ONNX opset version
do_constant_folding: bool = True
optimize: bool = True

# Input/Output
input_names: list[str] = None
output_names: list[str] = None
dynamic_axes: dict[str, dict[int, str]] = None

# Validation
validate_model: bool = True
test_with_random_input: bool = True
```

**Public Methods:**


---

### `ONNXExportResult`

**File:** `onnx_exporter.py`

```python
class ONNXExportResult:
```

**Description:**
```
"""ONNX export result."""

# Export info
onnx_path: Path
opset_version: int

# Model info
num_parameters: int
model_size_mb: float

# Input/Output shapes
input_shapes: list[tuple[int, ...]]
output_shapes: list[tuple[int, ...]]

# Validation
validation_passed: bool
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ONNXExporter`

**File:** `onnx_exporter.py`

```python
class ONNXExporter:
```

**Description:**
```
"""ONNX model exporter.

Features:
- PyTorch to ONNX conversion
- Model optimization (constant folding, fusion)
- Dynamic axes for variable input sizes
- Model validation with ONNX checker
- Inference testing to verify correctness
- Shape inference

Example:
    ```python
    # Simple export
    config = ONNXExportConfig(opset_version=14, optimize=True)

    exporter = ONNXExporter(config=config)
```

**Public Methods:**

- `def export(self, model`
- `def print_report(self, result`

---

### `ProfilerConfig`

**File:** `profiler.py`

```python
class ProfilerConfig:
```

**Description:**
```
"""Profiler configuration."""

# Profiling options
enable_cpu_profiling: bool = True
enable_memory_profiling: bool = True
enable_gpu_profiling: bool = False

# Output options
output_dir: Path = Path("profiling/results")
save_flame_graph: bool = True
save_stats: bool = True

# Timing options
num_iterations: int = 100
warmup_iterations: int = 10
```

**Public Methods:**


---

### `ProfileResult`

**File:** `profiler.py`

```python
class ProfileResult:
```

**Description:**
```
"""Profiling results."""

# Overall metrics
total_time_ms: float
avg_time_ms: float

# Layer-wise timing
layer_times: dict[str, float]

# Memory metrics
peak_memory_mb: float | None = None
memory_by_layer: dict[str, float] | None = None

# CPU profiling
cpu_profile_path: Path | None = None
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def save(self, output_path`

---

### `Profiler`

**File:** `profiler.py`

```python
class Profiler:
```

**Description:**
```
"""Detailed performance profiler.

Features:
- Layer-wise timing
- Memory profiling
- CPU profiling (cProfile)
- GPU profiling (PyTorch profiler)
- Bottleneck detection
- Flame graph generation

Example:
    ```python
    import torch

    model = MyModel()
    profiler = Profiler(config=ProfilerConfig(enable_cpu_profiling=True, enable_memory_profiling=True))
```

**Public Methods:**

- `def profile_model(self, model`
- `def print_report(self, result`

---

### `PruningConfig`

**File:** `pruner.py`

```python
class PruningConfig:
```

**Description:**
```
"""Pruning configuration."""

# Pruning type
pruning_type: str = "unstructured"  # "unstructured", "structured"

# Pruning method
pruning_method: str = "l1"  # "l1", "random", "ln"

# Sparsity
target_sparsity: float = 0.5  # Target sparsity (0.0 to 1.0)

# Iterative pruning
iterative: bool = True
num_iterations: int = 5

# Fine-tuning
```

**Public Methods:**


---

### `PruningResult`

**File:** `pruner.py`

```python
class PruningResult:
```

**Description:**
```
"""Pruning results."""

# Sparsity metrics
original_params: int
pruned_params: int
sparsity_achieved: float

# Model size
original_size_mb: float
pruned_size_mb: float
size_reduction_pct: float

# Layer-wise sparsity
layer_sparsity: dict[str, float]

def to_dict(self) -> dict[str, Any]:
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ModelPruner`

**File:** `pruner.py`

```python
class ModelPruner:
```

**Description:**
```
"""Model pruning for inference optimization.

Features:
- Unstructured pruning (individual weights)
- Structured pruning (entire filters/neurons)
- Magnitude-based pruning (L1/L2)
- Iterative pruning with gradual sparsity increase
- Fine-tuning support
- Sparsity analysis per layer

Example:
    ```python
    # Simple unstructured pruning
    config = PruningConfig(pruning_type="unstructured", target_sparsity=0.5)

    pruner = ModelPruner(config=config)
```

**Public Methods:**

- `def prune(self, model`
- `def prune_iterative(`
- `def analyze_sparsity(self, model`
- `def save_model(self, model`
- `def print_report(self, result`

---

### `QuantizationConfig`

**File:** `quantizer.py`

```python
class QuantizationConfig:
```

**Description:**
```
"""Quantization configuration."""

# Quantization type
quantization_type: str = "dynamic"  # "dynamic", "static"

# Backend
backend: str = "fbgemm"  # "fbgemm" (x86), "qnnpack" (ARM)

# Data type
dtype: str = "qint8"  # "qint8", "float16"

# Calibration (for static quantization)
num_calibration_batches: int = 100

# Layers to skip
skip_layers: list[str] = None
```

**Public Methods:**


---

### `ModelQuantizer`

**File:** `quantizer.py`

```python
class ModelQuantizer:
```

**Description:**
```
"""Model quantizer for inference optimization.

Features:
- Dynamic quantization (weights only)
- Static quantization (weights + activations)
- INT8 and FP16 quantization
- Calibration for static quantization

Example:
    ```python
    # Dynamic quantization (simplest)
    quantizer = ModelQuantizer(config=QuantizationConfig(quantization_type="dynamic"))

    quantized_model = quantizer.quantize(model)
    quantizer.save_model(quantized_model, "model_quantized.pt")
```

**Public Methods:**

- `def quantize(`
- `def save_model(self, model`
- `def benchmark_quantized(`

---

### `HierarchicalPredictiveCodingNetwork`

**File:** `hpc_network.py`

```python
class HierarchicalPredictiveCodingNetwork:
```

**Description:**
```
"""Main hPC Network coordinating all 5 layers.

Implements hierarchical predictive coding with top-down predictions
and bottom-up prediction errors.
"""

def __init__(self, latent_dim: int = 64, device: str = "cpu"):
    """Initialize hPC Network.

    Args:
        latent_dim: Latent space dimensionality (consistent across layers)
        device: Computation device ('cpu' or 'cuda')
    """
    self.latent_dim = latent_dim
    self.device = device
```

**Public Methods:**

- `def hierarchical_inference(`
- `def compute_free_energy(self, predictions`
- `def get_unified_threat_assessment(self, predictions`
- `def save_all_models(self, base_path`
- `def load_all_models(self, base_path`

---

### `EventVAE`

**File:** `layer1_sensory.py`

```python
class EventVAE(nn.Module):
```

**Description:**
```
"""Variational Autoencoder for event compression.

Compresses high-dimensional event vectors (e.g., 10k features) into
64D latent representations, learning normal patterns.

High reconstruction error = anomalous event (high prediction error).
"""

def __init__(
    self,
    input_dim: int = 10000,
    hidden_dims: list = [1024, 256],
    latent_dim: int = 64,
):
    """Initialize Event VAE.
```

**Public Methods:**

- `def encode(self, x`
- `def reparameterize(self, mu`
- `def decode(self, z`
- `def forward(self, x`
- `def compute_loss(`

---

### `SensoryLayer`

**File:** `layer1_sensory.py`

```python
class SensoryLayer:
```

**Description:**
```
"""Layer 1 of Hierarchical Predictive Coding Network.

Compresses raw events into latent representations and detects
anomalies via reconstruction error (prediction error).
"""

def __init__(
    self,
    input_dim: int = 10000,
    latent_dim: int = 64,
    device: str = "cpu",
    anomaly_threshold: float = 3.0,
):
    """Initialize Sensory Layer.

    Args:
```

**Public Methods:**

- `def predict(self, event`
- `def train_step(`
- `def save_model(self, path`
- `def load_model(self, path`

---

### `EventGraph`

**File:** `layer2_behavioral.py`

```python
class EventGraph:
```

**Description:**
```
"""Event graph representation."""

node_features: torch.Tensor  # [num_nodes, feature_dim]
edge_index: torch.Tensor  # [2, num_edges] (source, target pairs)
edge_features: torch.Tensor | None = None  # [num_edges, edge_feature_dim]
node_labels: torch.Tensor | None = None  # [num_nodes] ground truth


class GraphConvLayer(nn.Module):
"""Graph Convolutional Layer for message passing."""

def __init__(self, in_features: int, out_features: int):
    """Initialize Graph Conv Layer.

    Args:
        in_features: Input feature dimensionality
```

**Public Methods:**


---

### `GraphConvLayer`

**File:** `layer2_behavioral.py`

```python
class GraphConvLayer(nn.Module):
```

**Description:**
```
"""Graph Convolutional Layer for message passing."""

def __init__(self, in_features: int, out_features: int):
    """Initialize Graph Conv Layer.

    Args:
        in_features: Input feature dimensionality
        out_features: Output feature dimensionality
    """
    super(GraphConvLayer, self).__init__()

    self.linear = nn.Linear(in_features, out_features)
    self.activation = nn.ReLU()

def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
    """Forward pass: aggregate neighbor features.
```

**Public Methods:**

- `def forward(self, x`

---

### `BehavioralGNN`

**File:** `layer2_behavioral.py`

```python
class BehavioralGNN(nn.Module):
```

**Description:**
```
"""Graph Neural Network for behavioral event prediction.

Models relationships between events (e.g., process spawns, network connections)
to predict next events and detect anomalous patterns.
"""

def __init__(
    self,
    input_dim: int = 64,  # From L1 latent representations
    hidden_dims: list[int] = [128, 128, 64],
    output_dim: int = 64,  # Predicted next event embedding
    num_classes: int = 10,  # Event types (e.g., benign, malware, exploit)
):
    """Initialize Behavioral GNN.

    Args:
```

**Public Methods:**

- `def forward(`

---

### `BehavioralLayer`

**File:** `layer2_behavioral.py`

```python
class BehavioralLayer:
```

**Description:**
```
"""Layer 2 of Hierarchical Predictive Coding Network.

Models event relationships as graphs and predicts behavioral patterns.
Detects anomalous process chains, suspicious network flows, etc.
"""

def __init__(self, latent_dim: int = 64, device: str = "cpu", anomaly_threshold: float = 0.7):
    """Initialize Behavioral Layer.

    Args:
        latent_dim: Latent space dimensionality (from L1)
        device: Computation device
        anomaly_threshold: Threshold for anomaly classification
    """
    self.device = torch.device(device)
    self.latent_dim = latent_dim
```

**Public Methods:**

- `def predict(self, event_graph`
- `def detect_anomalous_chains(self, event_graph`
- `def train_step(self, event_graph`
- `def save_model(self, path`
- `def load_model(self, path`

---

### `TemporalBlock`

**File:** `layer3_operational.py`

```python
class TemporalBlock(nn.Module):
```

**Description:**
```
"""Temporal convolution block with dilated causal convolutions."""

def __init__(
    self,
    in_channels: int,
    out_channels: int,
    kernel_size: int,
    stride: int,
    dilation: int,
    dropout: float = 0.2,
):
    """Initialize Temporal Block.

    Args:
        in_channels: Input channels
        out_channels: Output channels
```

**Public Methods:**

- `def forward(self, x`

---

### `TemporalConvNet`

**File:** `layer3_operational.py`

```python
class TemporalConvNet(nn.Module):
```

**Description:**
```
"""Temporal Convolutional Network for sequence prediction."""

def __init__(
    self,
    num_inputs: int,
    num_channels: list[int],
    kernel_size: int = 3,
    dropout: float = 0.2,
):
    """Initialize TCN.

    Args:
        num_inputs: Input feature dimensionality
        num_channels: List of channel sizes for each layer
        kernel_size: Kernel size for convolutions
        dropout: Dropout probability
```

**Public Methods:**

- `def forward(self, x`

---

### `OperationalTCN`

**File:** `layer3_operational.py`

```python
class OperationalTCN(nn.Module):
```

**Description:**
```
"""TCN for operational threat prediction (hours ahead).

Predicts immediate threats based on temporal patterns in behavioral data.
"""

def __init__(
    self,
    input_dim: int = 64,  # From L2 behavioral representations
    hidden_channels: list[int] = [128, 128, 64],
    output_dim: int = 64,
    num_threat_classes: int = 15,  # Threat types
    kernel_size: int = 3,
    dropout: float = 0.2,
):
    """Initialize Operational TCN.
```

**Public Methods:**

- `def forward(self, sequence`

---

### `OperationalLayer`

**File:** `layer3_operational.py`

```python
class OperationalLayer:
```

**Description:**
```
"""Layer 3 of Hierarchical Predictive Coding Network.

Predicts immediate threats (1-6 hours) using temporal patterns.
Detects active reconnaissance, exploitation attempts, attack progression.
"""

def __init__(
    self,
    latent_dim: int = 64,
    device: str = "cpu",
    prediction_horizon_hours: int = 6,
):
    """Initialize Operational Layer.

    Args:
        latent_dim: Latent space dimensionality (from L2)
```

**Public Methods:**

- `def predict(self, event_sequence`
- `def predict_attack_progression(self, event_sequence`
- `def detect_attack_indicators(self, event_sequence`
- `def train_step(`
- `def save_model(self, path`
- `def load_model(self, path`

---

### `TacticalLSTM`

**File:** `layer4_tactical.py`

```python
class TacticalLSTM(nn.Module):
```

**Description:**
```
"""Bidirectional LSTM for tactical threat prediction (days ahead).

Models multi-day attack campaigns, lateral movement, APT TTPs.
"""

def __init__(
    self,
    input_dim: int = 64,  # From L3 operational representations
    hidden_dim: int = 256,
    num_layers: int = 2,
    output_dim: int = 64,
    num_campaign_types: int = 20,
    dropout: float = 0.3,
):
    """Initialize Tactical LSTM.
```

**Public Methods:**

- `def forward(`

---

### `TacticalLayer`

**File:** `layer4_tactical.py`

```python
class TacticalLayer:
```

**Description:**
```
"""Layer 4 of Hierarchical Predictive Coding Network.

Predicts multi-day attack campaigns using bidirectional LSTM.
Detects APT patterns, lateral movement, persistent threats.
"""

def __init__(
    self,
    latent_dim: int = 64,
    device: str = "cpu",
    prediction_horizon_days: int = 7,
):
    """Initialize Tactical Layer.

    Args:
        latent_dim: Latent space dimensionality
```

**Public Methods:**

- `def predict(self, event_sequence`
- `def detect_apt_indicators(self, event_sequence`
- `def train_step(`
- `def save_model(self, path`
- `def load_model(self, path`

---

### `StrategicTransformer`

**File:** `layer5_strategic.py`

```python
class StrategicTransformer(nn.Module):
```

**Description:**
```
"""Transformer for strategic threat landscape prediction (weeks/months ahead).

Models long-term trends: APT campaigns, zero-day emergence, geopolitical threats.
"""

def __init__(
    self,
    input_dim: int = 64,  # From L4 tactical representations
    d_model: int = 512,
    nhead: int = 8,
    num_layers: int = 6,
    output_dim: int = 64,
    num_apt_groups: int = 50,
    num_cve_categories: int = 20,
    dropout: float = 0.1,
):
```

**Public Methods:**

- `def forward(`

---

### `PositionalEncoding`

**File:** `layer5_strategic.py`

```python
class PositionalEncoding(nn.Module):
```

**Description:**
```
"""Positional encoding for transformer."""

def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
    super(PositionalEncoding, self).__init__()
    self.dropout = nn.Dropout(p=dropout)

    # Compute positional encodings
    position = torch.arange(max_len).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))

    pe = torch.zeros(1, max_len, d_model)
    pe[0, :, 0::2] = torch.sin(position * div_term)
    pe[0, :, 1::2] = torch.cos(position * div_term)

    self.register_buffer("pe", pe)
```

**Public Methods:**

- `def forward(self, x`

---

### `StrategicLayer`

**File:** `layer5_strategic.py`

```python
class StrategicLayer:
```

**Description:**
```
"""Layer 5 of Hierarchical Predictive Coding Network.

Predicts threat landscape evolution over weeks/months using transformer.
Detects emerging APT groups, zero-day trends, geopolitical threats.
"""

def __init__(
    self,
    latent_dim: int = 64,
    device: str = "cpu",
    prediction_horizon_weeks: int = 12,
):
    """Initialize Strategic Layer.

    Args:
        latent_dim: Latent space dimensionality
```

**Public Methods:**

- `def predict(self, event_sequence`
- `def assess_strategic_risk(self, event_sequence`
- `def train_step(`
- `def save_model(self, path`
- `def load_model(self, path`

---

### `PrivacyLevel`

**File:** `base.py`

```python
class PrivacyLevel(str, Enum):
```

**Description:**
```
"""Privacy level classification"""

VERY_HIGH = "very_high"  # ε ≤ 0.1
HIGH = "high"  # 0.1 < ε ≤ 1.0
MEDIUM = "medium"  # 1.0 < ε ≤ 3.0
LOW = "low"  # 3.0 < ε ≤ 10.0
MINIMAL = "minimal"  # ε > 10.0


@dataclass
class PrivacyBudget:
"""
Privacy budget tracker for (ε, δ)-differential privacy.

Tracks cumulative privacy loss from multiple queries and enforces
global privacy budget limits.
```

**Public Methods:**


---

### `PrivacyBudget`

**File:** `base.py`

```python
class PrivacyBudget:
```

**Description:**
```
"""
Privacy budget tracker for (ε, δ)-differential privacy.

Tracks cumulative privacy loss from multiple queries and enforces
global privacy budget limits.

Attributes:
    total_epsilon: Total privacy budget (ε)
    total_delta: Failure probability budget (δ)
    used_epsilon: Cumulative ε used
    used_delta: Cumulative δ used
    queries_executed: List of executed queries with their privacy cost
    created_at: Budget creation timestamp
"""

total_epsilon: float
```

**Public Methods:**

- `def remaining_epsilon(self) -> float`
- `def remaining_delta(self) -> float`
- `def budget_exhausted(self) -> bool`
- `def privacy_level(self) -> PrivacyLevel`
- `def can_execute(self, epsilon`
- `def spend(`
- `def get_statistics(self) -> dict[str, Any]`

---

### `PrivacyParameters`

**File:** `base.py`

```python
class PrivacyParameters:
```

**Description:**
```
"""
Privacy parameters for a differential privacy mechanism.

Attributes:
    epsilon: Privacy parameter (ε)
    delta: Failure probability (δ)
    sensitivity: Global sensitivity (Δf)
    mechanism: DP mechanism to use ('laplace', 'gaussian', 'exponential')
"""

epsilon: float
delta: float = 0.0
sensitivity: float = 1.0
mechanism: str = "laplace"

def __post_init__(self):
```

**Public Methods:**

- `def is_pure_dp(self) -> bool`
- `def noise_scale(self) -> float`

---

### `DPResult`

**File:** `base.py`

```python
class DPResult:
```

**Description:**
```
"""
Result of a differentially private query.

Attributes:
    true_value: True query result (if available, for testing)
    noisy_value: Differentially private (noisy) result
    epsilon_used: Privacy budget (ε) used
    delta_used: Failure probability (δ) used
    sensitivity: Sensitivity of the query
    mechanism: DP mechanism used
    noise_added: Actual noise added (for transparency)
    query_type: Type of query executed
    timestamp: Query execution timestamp
    metadata: Additional query metadata
"""
```

**Public Methods:**

- `def absolute_error(self) -> float | None`
- `def relative_error(self) -> float | None`
- `def to_dict(self) -> dict[str, Any]`

---

### `PrivacyMechanism`

**File:** `base.py`

```python
class PrivacyMechanism(ABC):
```

**Description:**
```
"""
Abstract base class for differential privacy mechanisms.

All DP mechanisms (Laplace, Gaussian, Exponential) inherit from this class
and implement the add_noise() method.
"""

def __init__(self, privacy_params: PrivacyParameters):
    """
    Initialize privacy mechanism.

    Args:
        privacy_params: Privacy parameters (ε, δ, sensitivity)
    """
    self.privacy_params = privacy_params
```

**Public Methods:**

- `def add_noise(self, true_value`
- `def execute_query(`

---

### `SensitivityCalculator`

**File:** `base.py`

```python
class SensitivityCalculator:
```

**Description:**
```
"""
Utility class for calculating query sensitivity.

Sensitivity (Δf) is the maximum change in query output when
adding/removing one record from the dataset.
"""

@staticmethod
def count_sensitivity() -> float:
    """
    Sensitivity of counting query.

    Adding/removing one record changes count by at most 1.

    Returns:
        float: Sensitivity Δf = 1
```

**Public Methods:**

- `def count_sensitivity() -> float`
- `def sum_sensitivity(value_range`
- `def mean_sensitivity(value_range`
- `def histogram_sensitivity(bins`

---

### `DPQueryType`

**File:** `dp_aggregator.py`

```python
class DPQueryType(str, Enum):
```

**Description:**
```
"""Type of differential privacy query"""

COUNT = "count"
SUM = "sum"
MEAN = "mean"
HISTOGRAM = "histogram"
COUNT_DISTINCT = "count_distinct"


class DPAggregator:
"""
High-level API for differentially private aggregation.

Provides simple interface for common threat intelligence queries:
- Geographic threat distribution
- Temporal threat patterns
```

**Public Methods:**


---

### `DPAggregator`

**File:** `dp_aggregator.py`

```python
class DPAggregator:
```

**Description:**
```
"""
High-level API for differentially private aggregation.

Provides simple interface for common threat intelligence queries:
- Geographic threat distribution
- Temporal threat patterns
- Severity statistics
- Attack vector histograms

Example:
    >>> aggregator = DPAggregator(epsilon=1.0, delta=1e-5)
    >>> result = aggregator.count_by_group(data=threat_data, group_column="country")
    >>> print(f"Noisy counts: {result.noisy_value}")
"""

def __init__(
```

**Public Methods:**

- `def count(`
- `def count_by_group(`
- `def sum(`
- `def mean(`
- `def histogram(`
- `def count_distinct_approximate(`
- `def get_budget_status(self) -> dict[str, Any] | None`

---

### `LaplaceMechanism`

**File:** `dp_mechanisms.py`

```python
class LaplaceMechanism(PrivacyMechanism):
```

**Description:**
```
"""
Laplace Mechanism for ε-Differential Privacy.

Adds noise drawn from Laplace distribution with scale b = Δf/ε,
where Δf is the global sensitivity of the query.

Provides (ε, 0)-differential privacy (pure DP).

Properties:
    - Simpler than Gaussian (no δ parameter)
    - Works for any ε > 0
    - Noise has heavier tails than Gaussian

References:
    Dwork, C., et al. (2006). "Calibrating Noise to Sensitivity in
    Private Data Analysis"
```

**Public Methods:**

- `def add_noise(self, true_value`

---

### `GaussianMechanism`

**File:** `dp_mechanisms.py`

```python
class GaussianMechanism(PrivacyMechanism):
```

**Description:**
```
"""
Gaussian Mechanism for (ε,δ)-Differential Privacy.

Adds noise drawn from Gaussian distribution with variance σ²,
where σ = Δf × sqrt(2 × ln(1.25/δ)) / ε.

Provides (ε, δ)-differential privacy (approximate DP).

Properties:
    - Requires δ > 0 (approximate DP)
    - Lighter tails than Laplace (better for large ε)
    - Composition properties well-understood

References:
    Dwork, C., & Roth, A. (2014). "The Algorithmic Foundations of
    Differential Privacy"
```

**Public Methods:**

- `def add_noise(self, true_value`

---

### `ExponentialMechanism`

**File:** `dp_mechanisms.py`

```python
class ExponentialMechanism(PrivacyMechanism):
```

**Description:**
```
"""
Exponential Mechanism for ε-Differential Privacy.

Selects an output from a discrete set based on a quality score function,
with probability proportional to exp(ε × score / (2 × Δu)), where Δu
is the sensitivity of the score function.

Useful for non-numeric queries where adding noise is not appropriate.

Properties:
    - Works for discrete/categorical outputs
    - Provides ε-differential privacy
    - Probability of selecting output proportional to its quality

References:
    McSherry, F., & Talwar, K. (2007). "Mechanism Design via Differential
```

**Public Methods:**

- `def add_noise(self, true_value`
- `def select(self, context`
- `def get_selection_probabilities(self) -> np.ndarray`

---

### `AdvancedNoiseMechanisms`

**File:** `dp_mechanisms.py`

```python
class AdvancedNoiseMechanisms:
```

**Description:**
```
"""
Advanced noise mechanisms and utilities.

Includes:
- Analytic Gaussian Mechanism (tighter bounds)
- Staircase Mechanism (optimal for pure DP)
- Utility functions for noise calibration
"""

@staticmethod
def analytic_gaussian_std(epsilon: float, delta: float, sensitivity: float) -> float:
    """
    Calculate Gaussian standard deviation using analytic formula.

    Uses tighter analysis from Balle & Wang (2018).
```

**Public Methods:**

- `def analytic_gaussian_std(epsilon`
- `def get_noise_multiplier(epsilon`
- `def expected_absolute_error(`
- `def confidence_interval(`

---

### `CompositionType`

**File:** `privacy_accountant.py`

```python
class CompositionType(str, Enum):
```

**Description:**
```
"""Type of privacy composition"""

BASIC_SEQUENTIAL = "basic_sequential"
ADVANCED_SEQUENTIAL = "advanced_sequential"
PARALLEL = "parallel"
RDP = "rdp"  # Rényi Differential Privacy


@dataclass
class QueryRecord:
"""
Record of a privacy-consuming query.

Attributes:
    timestamp: Query execution timestamp
    epsilon: Privacy cost (ε)
```

**Public Methods:**


---

### `QueryRecord`

**File:** `privacy_accountant.py`

```python
class QueryRecord:
```

**Description:**
```
"""
Record of a privacy-consuming query.

Attributes:
    timestamp: Query execution timestamp
    epsilon: Privacy cost (ε)
    delta: Failure probability (δ)
    query_type: Type of query
    mechanism: DP mechanism used
    composition_type: How this query composes with others
    metadata: Additional query information
"""

timestamp: float
epsilon: float
delta: float
```

**Public Methods:**


---

### `PrivacyAccountant`

**File:** `privacy_accountant.py`

```python
class PrivacyAccountant:
```

**Description:**
```
"""
Privacy accountant for tracking cumulative privacy loss.

Implements composition theorems to compute total privacy guarantee
from multiple queries.

Example:
    >>> accountant = PrivacyAccountant(
    ...     total_epsilon=10.0, total_delta=1e-5, composition_type=CompositionType.ADVANCED_SEQUENTIAL
    ... )
    >>>
    >>> # Execute queries
    >>> accountant.add_query(epsilon=1.0, delta=0, query_type="count")
    >>> accountant.add_query(epsilon=1.0, delta=0, query_type="mean")
    >>>
    >>> # Check composition
```

**Public Methods:**

- `def add_query(`
- `def get_total_privacy_loss(self) -> tuple[float, float]`
- `def get_remaining_budget(self) -> tuple[float, float]`
- `def is_budget_exhausted(self) -> bool`
- `def can_execute_query(self, epsilon`
- `def get_statistics(self) -> dict[str, Any]`
- `def get_query_history(self) -> list[dict[str, Any]]`
- `def reset(self) -> None`

---

### `SubsampledPrivacyAccountant`

**File:** `privacy_accountant.py`

```python
class SubsampledPrivacyAccountant(PrivacyAccountant):
```

**Description:**
```
"""
Privacy accountant with amplification by subsampling.

When queries are executed on random subsamples of the data,
privacy is amplified. This accountant incorporates the amplification
theorem.

Example:
    >>> accountant = SubsampledPrivacyAccountant(
    ...     total_epsilon=10.0,
    ...     total_delta=1e-5,
    ...     sampling_rate=0.01,  # 1% subsample
    ... )
    >>>
    >>> # Query on subsample has amplified privacy
    >>> accountant.add_query(epsilon=1.0, delta=0)  # Actual ε << 1.0
```

**Public Methods:**

- `def add_query(`

---

### `TestBaseClasses`

**File:** `test_privacy.py`

```python
class TestBaseClasses:
```

**Description:**
```
"""Test base classes and data structures"""

def test_privacy_budget_initialization(self):
    """Test PrivacyBudget initialization and validation"""
    # Valid budget
    budget = PrivacyBudget(total_epsilon=1.0, total_delta=1e-5)
    assert budget.total_epsilon == 1.0
    assert budget.total_delta == 1e-5
    assert budget.used_epsilon == 0.0
    assert budget.used_delta == 0.0
    assert budget.remaining_epsilon == 1.0
    assert budget.remaining_delta == 1e-5
    assert not budget.budget_exhausted

    # Invalid epsilon
    with pytest.raises(ValueError, match="epsilon must be positive"):
```

**Public Methods:**

- `def test_privacy_budget_initialization(self)`
- `def test_privacy_budget_spending(self)`
- `def test_privacy_budget_levels(self)`
- `def test_privacy_parameters(self)`
- `def test_sensitivity_calculator(self)`

---

### `TestDPMechanisms`

**File:** `test_privacy.py`

```python
class TestDPMechanisms:
```

**Description:**
```
"""Test differential privacy mechanisms"""

def test_laplace_mechanism(self):
    """Test Laplace mechanism noise addition"""
    params = PrivacyParameters(epsilon=1.0, delta=0.0, sensitivity=1.0)
    mechanism = LaplaceMechanism(params)

    # Test scalar noise
    true_value = 100.0
    noisy_value = mechanism.add_noise(true_value)
    assert isinstance(noisy_value, float)
    assert noisy_value != true_value  # Noise was added (with high probability)

    # Test array noise
    true_array = np.array([10.0, 20.0, 30.0])
    noisy_array = mechanism.add_noise(true_array)
```

**Public Methods:**

- `def test_laplace_mechanism(self)`
- `def test_gaussian_mechanism(self)`
- `def test_exponential_mechanism(self)`
- `def test_dp_result_validation(self)`

---

### `TestDPAggregator`

**File:** `test_privacy.py`

```python
class TestDPAggregator:
```

**Description:**
```
"""Test differentially private aggregation"""

def test_count_query(self):
    """Test DP count query"""
    data = pd.DataFrame({"value": range(1000)})
    aggregator = DPAggregator(epsilon=1.0, delta=0.0)

    result = aggregator.count(data)
    assert isinstance(result, DPResult)
    assert result.true_value == 1000
    assert result.epsilon_used == 1.0
    assert result.delta_used == 0.0
    assert result.query_type == DPQueryType.COUNT.value

    # Noisy count should be close to true count (with high probability)
    assert abs(result.noisy_value - 1000) < 50  # Within reasonable noise
```

**Public Methods:**

- `def test_count_query(self)`
- `def test_count_by_group(self)`
- `def test_sum_query(self)`
- `def test_mean_query(self)`
- `def test_histogram_query(self)`

---

### `TestPrivacyAccountant`

**File:** `test_privacy.py`

```python
class TestPrivacyAccountant:
```

**Description:**
```
"""Test privacy accounting and composition"""

def test_basic_composition(self):
    """Test basic sequential composition"""
    accountant = PrivacyAccountant(
        total_epsilon=10.0, total_delta=1e-4, composition_type=CompositionType.BASIC_SEQUENTIAL
    )

    # Add 5 queries with ε=1.0 each
    for i in range(5):
        accountant.add_query(epsilon=1.0, delta=0.0, query_type="count")

    # Basic composition: total ε = Σ ε_i = 5.0
    total_eps, total_dlt = accountant.get_total_privacy_loss()
    assert total_eps == 5.0
    assert total_dlt == 0.0
```

**Public Methods:**

- `def test_basic_composition(self)`
- `def test_advanced_composition(self)`
- `def test_parallel_composition(self)`
- `def test_budget_exhaustion(self)`
- `def test_subsampling_amplification(self)`

---

### `TestPrivacyGuarantees`

**File:** `test_privacy.py`

```python
class TestPrivacyGuarantees:
```

**Description:**
```
"""Test privacy guarantees and statistical properties"""

def test_laplace_noise_distribution(self):
    """Test Laplace noise has correct distribution"""
    params = PrivacyParameters(epsilon=1.0, delta=0.0, sensitivity=1.0)
    mechanism = LaplaceMechanism(params)

    # Generate many noisy samples
    true_value = 0.0
    samples = [mechanism.add_noise(true_value) for _ in range(10000)]

    # Check mean (should be close to 0)
    assert np.mean(samples) == pytest.approx(0.0, abs=0.05)

    # Check scale (MAD should be close to b * ln(2) ≈ 0.693 for b=1.0)
    median_absolute_deviation = np.median(np.abs(samples))
```

**Public Methods:**

- `def test_laplace_noise_distribution(self)`
- `def test_gaussian_noise_distribution(self)`
- `def test_utility_vs_privacy_tradeoff(self)`

---

### `TestPerformance`

**File:** `test_privacy.py`

```python
class TestPerformance:
```

**Description:**
```
"""Test performance benchmarks"""

def test_dp_aggregation_latency(self):
    """Test DP aggregation completes within target (<100ms)"""
    import time

    data = pd.DataFrame({"value": range(1000), "group": np.random.choice(["A", "B", "C"], 1000)})
    aggregator = DPAggregator(epsilon=1.0, delta=0.0)

    # Measure count latency
    start = time.time()
    result = aggregator.count(data)
    latency_ms = (time.time() - start) * 1000

    assert latency_ms < 100  # Target: <100ms
```

**Public Methods:**

- `def test_dp_aggregation_latency(self)`
- `def test_privacy_accountant_performance(self)`

---

### `CodeAnalyzer`

**File:** `batch_test_generator.py`

```python
class CodeAnalyzer:
```

**Description:**
```
"""Analisa código Python para extrair estrutura."""

def __init__(self, file_path: Path):
    self.file_path = file_path
    self.tree = None
    self.classes = []
    self.functions = []
    self.imports = []

def analyze(self) -> Dict[str, Any]:
    """Analisa arquivo e retorna estrutura."""
    with open(self.file_path) as f:
        content = f.read()
        self.tree = ast.parse(content)

    # Extract classes
```

**Public Methods:**

- `def analyze(self) -> Dict[str, Any]`

---

### `TestGenerator`

**File:** `batch_test_generator.py`

```python
class TestGenerator:
```

**Description:**
```
"""Gera testes de alta qualidade sem mocks."""

def __init__(self, module_path: str, analysis: Dict[str, Any]):
    self.module_path = module_path
    self.analysis = analysis
    self.module_name = module_path.replace('/', '.').replace('.py', '')

def generate_test_file(self) -> str:
    """Gera arquivo de teste completo."""
    lines = []

    # Header
    lines.append('"""')
    lines.append(f'FASE A - Tests for {self.module_path}')
    lines.append('Generated by batch_test_generator.py')
    lines.append('Zero mocks - Padrão Pagani Absoluto')
```

**Public Methods:**

- `def generate_test_file(self) -> str`

---

### `BatchTestRunner`

**File:** `batch_test_generator.py`

```python
class BatchTestRunner:
```

**Description:**
```
"""Executa geração de testes em batch para módulos simples."""

def __init__(self, coverage_json: Path = Path('coverage.json')):
    self.coverage_json = coverage_json
    self.simple_modules = []

def identify_simple_modules(self, max_missing: int = 50) -> List[Dict[str, Any]]:
    """Identifica módulos simples (< max_missing lines)."""
    with open(self.coverage_json) as f:
        data = json.load(f)

    simple = []
    for path, metrics in data['files'].items():
        if 'summary' not in metrics:
            continue
```

**Public Methods:**

- `def identify_simple_modules(self, max_missing`
- `def generate_tests_for_module(self, module_info`
- `def validate_tests(self, test_file`
- `def run_batch(self, batch_size`

---

### `ModuleStatus`

**File:** `coverage_commander.py`

```python
class ModuleStatus:
```

**Description:**
```
"""Status de um módulo no plano."""

path: str
priority: str
total_lines: int
missing_lines: int
current_coverage: float
completed: bool
last_updated: str | None = None


class CoverageCommander:
"""
Orquestrador automático de coverage.

Features:
```

**Public Methods:**


---

### `CoverageCommander`

**File:** `coverage_commander.py`

```python
class CoverageCommander:
```

**Description:**
```
"""
Orquestrador automático de coverage.

Features:
- Pytest incremental (batch mode)
- Auto-update MASTER_COVERAGE_PLAN.md
- Regression detection
- Auto-test generation for simple modules
"""

def __init__(
    self,
    master_plan: Path = Path("docs/MASTER_COVERAGE_PLAN.md"),
    coverage_xml: Path = Path("coverage.xml"),
    coverage_json: Path = Path("coverage.json"),
    history_file: Path = Path("docs/coverage_history.json"),
```

**Public Methods:**

- `def get_status(self) -> dict[str, Any]`
- `def get_next_targets(self, batch_size`
- `def run_coverage_for_modules(self, modules`
- `def update_master_plan(self, completed_modules`
- `def check_regressions(self, threshold`
- `def print_status(self) -> None`

---

### `CoverageAnalyzer`

**File:** `coverage_report.py`

```python
class CoverageAnalyzer:
```

**Description:**
```
"""Analyze coverage reports and calculate deltas."""

def __init__(self, current_report: Path, baseline_report: Optional[Path] = None):
    """
    Initialize analyzer.

    Args:
        current_report: Path to current coverage htmlcov directory
        baseline_report: Path to baseline coverage (optional)
    """
    self.current_report = current_report
    self.baseline_report = baseline_report

def load_coverage_data(self, report_path: Path) -> Dict:
    """
    Load coverage data from status.json.
```

**Public Methods:**

- `def load_coverage_data(self, report_path`
- `def calculate_totals(self, coverage_data`
- `def analyze_by_module(self, coverage_data`
- `def calculate_delta(self) -> Dict`
- `def print_report(self, show_modules`
- `def generate_badge(self, output_path`

---

### `ModuleCoverage`

**File:** `coverage_tracker.py`

```python
class ModuleCoverage:
```

**Description:**
```
"""Coverage metrics for a single module."""

name: str
total_lines: int
covered_lines: int
missing_lines: int
coverage_pct: float


@dataclass
class CoverageSnapshot:
"""Complete coverage snapshot at a point in time."""

timestamp: str
total_coverage_pct: float
total_lines: int
```

**Public Methods:**


---

### `CoverageSnapshot`

**File:** `coverage_tracker.py`

```python
class CoverageSnapshot:
```

**Description:**
```
"""Complete coverage snapshot at a point in time."""

timestamp: str
total_coverage_pct: float
total_lines: int
covered_lines: int
missing_lines: int
modules: list[ModuleCoverage]

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary for JSON serialization."""
    return {
        "timestamp": self.timestamp,
        "total_coverage_pct": self.total_coverage_pct,
        "total_lines": self.total_lines,
        "covered_lines": self.covered_lines,
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `CoverageTracker`

**File:** `coverage_tracker.py`

```python
class CoverageTracker:
```

**Description:**
```
"""
Persistent coverage tracking system.

Features:
- Parse coverage.xml from pytest-cov
- Track coverage history over time
- Detect regressions (e.g., 100% → 20%)
- Generate HTML dashboard updates
- Immutable history (append-only)

Example:
    ```python
    tracker = CoverageTracker()
    snapshot = tracker.parse_coverage()
    tracker.save_snapshot(snapshot)
    tracker.update_dashboard()
```

**Public Methods:**

- `def parse_coverage(self) -> CoverageSnapshot`
- `def load_history(self) -> list[dict[str, Any]]`
- `def save_snapshot(self, snapshot`
- `def detect_regressions(self, threshold`
- `def generate_dashboard_data(self) -> dict[str, Any]`
- `def update_dashboard(self) -> None`

---

### `GeminiTestGenerator`

**File:** `generate_tests_gemini.py`

```python
class GeminiTestGenerator:
```

**Description:**
```
"""AI-powered test generator using Google Gemini."""

def __init__(self, api_key: Optional[str] = None):
    """
    Initialize test generator.

    Args:
        api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
    """
    if not GEMINI_AVAILABLE:
        raise ImportError("google-generativeai package not installed")

    self.api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not self.api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
```

**Public Methods:**

- `def analyze_module(self, module_path`
- `def generate_test_prompt(`

---

### `TestYourClass`

**File:** `generate_tests_gemini.py`

```python
class TestYourClass:
```

**Description:**
```
"""
```

**Public Methods:**

- `def test_method_success_case(self)`
- `def generate_tests(`
- `def validate_test_file(self, test_path`

---

### `TestGenerator`

**File:** `generate_tests.py`

```python
class TestGenerator:
```

**Description:**
```
"""AI-powered test generator using Claude API."""

def __init__(self, api_key: Optional[str] = None):
    """
    Initialize test generator.

    Args:
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
    """
    self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not self.api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    self.client = anthropic.Anthropic(api_key=self.api_key)

def analyze_module(self, module_path: Path) -> Dict[str, Any]:
```

**Public Methods:**

- `def analyze_module(self, module_path`
- `def generate_test_prompt(`

---

### `TestYourClass`

**File:** `generate_tests.py`

```python
class TestYourClass:
```

**Public Methods:**

- `def test_method_name_success_case(self)`
- `def generate_tests(`
- `def validate_test_file(self, test_path`

---

### `ModuleInfo`

**File:** `industrial_test_generator.py`

```python
class ModuleInfo:
```

**Description:**
```
"""Information about a Python module."""
path: Path
name: str
classes: List[Dict[str, Any]]
functions: List[Dict[str, Any]]
imports: List[str]
lines: int
has_tests: bool


@dataclass
class TestStats:
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
modules_without_tests: int = 0
```

**Public Methods:**


---

### `TestStats`

**File:** `industrial_test_generator.py`

```python
class TestStats:
```

**Description:**
```
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
modules_without_tests: int = 0
classes_found: int = 0
methods_found: int = 0
functions_found: int = 0
tests_generated: int = 0
tests_to_generate: int = 0


class IndustrialTestGenerator:
"""Mass test generator using AST analysis and templates."""

def __init__(self, base_dir: Path = None):
    """Initialize generator.
```

**Public Methods:**


---

### `IndustrialTestGenerator`

**File:** `industrial_test_generator.py`

```python
class IndustrialTestGenerator:
```

**Description:**
```
"""Mass test generator using AST analysis and templates."""

def __init__(self, base_dir: Path = None):
    """Initialize generator.

    Args:
        base_dir: Base directory to scan (defaults to current dir)
    """
    self.base_dir = base_dir or Path.cwd()
    self.stats = TestStats()
    self.modules: List[ModuleInfo] = []
    self.existing_tests: Set[str] = set()

    # Directories to skip
    self.skip_dirs = {
        '.venv', 'venv', '__pycache__', '.git', 'node_modules',
```

**Public Methods:**

- `def scan_codebase(self) -> List[ModuleInfo]`
- `def analyze_module(self, file_path`
- `def generate_tests_for_module(self, module`
- `def generate_all_tests(self, max_modules`
- `def print_summary(self)`

---

### `ModuleInfo`

**File:** `industrial_test_generator_v2.py`

```python
class ModuleInfo:
```

**Description:**
```
"""Information about a Python module."""
path: Path
name: str
classes: List[Dict[str, Any]]
functions: List[Dict[str, Any]]
imports: List[str]
lines: int
complexity: str  # 'simple', 'medium', 'complex'
has_tests: bool


@dataclass
class TestStats:
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
```

**Public Methods:**


---

### `TestStats`

**File:** `industrial_test_generator_v2.py`

```python
class TestStats:
```

**Description:**
```
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
modules_without_tests: int = 0
classes_found: int = 0
methods_found: int = 0
functions_found: int = 0
tests_generated: int = 0
simple_tests: int = 0  # Can run immediately
parameterized_tests: int = 0
hypothesis_tests: int = 0
skipped_tests: int = 0  # Need manual implementation


class IndustrialTestGeneratorV2:
"""State-of-the-art test generator (2024-2025 techniques)."""
```

**Public Methods:**


---

### `IndustrialTestGeneratorV2`

**File:** `industrial_test_generator_v2.py`

```python
class IndustrialTestGeneratorV2:
```

**Description:**
```
"""State-of-the-art test generator (2024-2025 techniques)."""

def __init__(self, base_dir: Path = None):
    """Initialize generator.

    Args:
        base_dir: Base directory to scan (defaults to current dir)
    """
    self.base_dir = base_dir or Path.cwd()
    self.stats = TestStats()
    self.modules: List[ModuleInfo] = []

    # Directories to skip
    self.skip_dirs = {
        '.venv', 'venv', '__pycache__', '.git', 'node_modules',
        '.pytest_cache', 'htmlcov', '.mypy_cache', 'dist', 'build',
```

**Public Methods:**

- `def scan_codebase(self) -> List[ModuleInfo]`
- `def analyze_module(self, file_path`
- `def generate_tests_for_module(self, module`
- `def generate_all_tests(self, max_modules`
- `def print_summary(self)`

---

### `FieldInfo`

**File:** `industrial_test_generator_v3.py`

```python
class FieldInfo:
```

**Description:**
```
"""Information about a Pydantic/Dataclass field."""
name: str
type_hint: str
required: bool
default_value: Any = None


@dataclass
class ModuleInfo:
"""Information about a Python module."""
path: Path
name: str
classes: List[Dict[str, Any]]
functions: List[Dict[str, Any]]
imports: List[str]
lines: int
```

**Public Methods:**


---

### `ModuleInfo`

**File:** `industrial_test_generator_v3.py`

```python
class ModuleInfo:
```

**Description:**
```
"""Information about a Python module."""
path: Path
name: str
classes: List[Dict[str, Any]]
functions: List[Dict[str, Any]]
imports: List[str]
lines: int
complexity: str  # 'simple', 'medium', 'complex'
has_tests: bool


@dataclass
class TestStats:
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
```

**Public Methods:**


---

### `TestStats`

**File:** `industrial_test_generator_v3.py`

```python
class TestStats:
```

**Description:**
```
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
modules_without_tests: int = 0
classes_found: int = 0
methods_found: int = 0
functions_found: int = 0
tests_generated: int = 0
simple_tests: int = 0  # Can run immediately
parameterized_tests: int = 0
skipped_tests: int = 0  # Need manual implementation
pydantic_models: int = 0
dataclasses: int = 0


class IndustrialTestGeneratorV3:
```

**Public Methods:**


---

### `IndustrialTestGeneratorV3`

**File:** `industrial_test_generator_v3.py`

```python
class IndustrialTestGeneratorV3:
```

**Description:**
```
"""PERFEIÇÃO - 95%+ accuracy test generator (V3)."""

def __init__(self, base_dir: Path = None):
    """Initialize generator.

    Args:
        base_dir: Base directory to scan (defaults to current dir)
    """
    self.base_dir = base_dir or Path.cwd()
    self.stats = TestStats()
    self.modules: List[ModuleInfo] = []

    # Directories to skip
    self.skip_dirs = {
        '.venv', 'venv', '__pycache__', '.git', 'node_modules',
        '.pytest_cache', 'htmlcov', '.mypy_cache', 'dist', 'build',
```

**Public Methods:**

- `def scan_codebase(self) -> List[ModuleInfo]`
- `def analyze_module(self, file_path`
- `def generate_tests_for_module(self, module`
- `def generate_all_tests(self, max_modules`
- `def print_summary(self)`

---

### `FieldInfo`

**File:** `industrial_test_generator_v4.py`

```python
class FieldInfo:
```

**Description:**
```
"""Information about a Pydantic/Dataclass field."""
name: str
type_hint: str
required: bool
default_value: Any = None
constraints: Dict[str, Any] = None  # NEW: min_length, ge, le, etc

def __post_init__(self):
    if self.constraints is None:
        self.constraints = {}


@dataclass
class ModuleInfo:
"""Information about a Python module."""
path: Path
```

**Public Methods:**


---

### `ModuleInfo`

**File:** `industrial_test_generator_v4.py`

```python
class ModuleInfo:
```

**Description:**
```
"""Information about a Python module."""
path: Path
name: str
classes: List[Dict[str, Any]]
functions: List[Dict[str, Any]]
imports: List[str]
lines: int
complexity: str  # 'simple', 'medium', 'complex'
has_tests: bool


@dataclass
class TestStats:
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
```

**Public Methods:**


---

### `TestStats`

**File:** `industrial_test_generator_v4.py`

```python
class TestStats:
```

**Description:**
```
"""Statistics for test generation."""
modules_scanned: int = 0
modules_with_tests: int = 0
modules_without_tests: int = 0
classes_found: int = 0
methods_found: int = 0
functions_found: int = 0
tests_generated: int = 0
simple_tests: int = 0  # Can run immediately
parameterized_tests: int = 0
skipped_tests: int = 0  # Need manual implementation
pydantic_models: int = 0
dataclasses: int = 0


class IndustrialTestGeneratorV4:
```

**Public Methods:**


---

### `IndustrialTestGeneratorV4`

**File:** `industrial_test_generator_v4.py`

```python
class IndustrialTestGeneratorV4:
```

**Description:**
```
"""ABSOLUT PERFECTION - 95%+ accuracy test generator (V4)."""

def __init__(self, base_dir: Path = None):
    """Initialize generator.

    Args:
        base_dir: Base directory to scan (defaults to current dir)
    """
    self.base_dir = base_dir or Path.cwd()
    self.stats = TestStats()
    self.modules: List[ModuleInfo] = []

    # Directories to skip
    self.skip_dirs = {
        '.venv', 'venv', '__pycache__', '.git', 'node_modules',
        '.pytest_cache', 'htmlcov', '.mypy_cache', 'dist', 'build',
```

**Public Methods:**

- `def scan_codebase(self, max_modules`
- `def generate_tests(self, modules`
- `def print_report(self) -> None`

---

### `PropertyTest`

**File:** `industrial_test_generator_v5_hypothesis.py`

```python
class PropertyTest:
```

**Description:**
```
"""A property-based test."""
class_name: str
property_name: str
test_code: str
invariant_type: str  # "bounds", "dimension", "conservation", "monotonic"


class HypothesisTestGenerator:
"""Generate Hypothesis property-based tests for consciousness modules."""

# Scientific invariants for consciousness module
INVARIANTS = {
    "arousal": {"type": "bounds", "min": 0.0, "max": 1.0},
    "phi": {"type": "bounds", "min": 0.0, "max": float("inf")},
    "coherence": {"type": "bounds", "min": 0.0, "max": 1.0},
    "salience": {"type": "bounds", "min": 0.0, "max": 1.0},
```

**Public Methods:**


---

### `HypothesisTestGenerator`

**File:** `industrial_test_generator_v5_hypothesis.py`

```python
class HypothesisTestGenerator:
```

**Description:**
```
"""Generate Hypothesis property-based tests for consciousness modules."""

# Scientific invariants for consciousness module
INVARIANTS = {
    "arousal": {"type": "bounds", "min": 0.0, "max": 1.0},
    "phi": {"type": "bounds", "min": 0.0, "max": float("inf")},
    "coherence": {"type": "bounds", "min": 0.0, "max": 1.0},
    "salience": {"type": "bounds", "min": 0.0, "max": 1.0},
    "confidence": {"type": "bounds", "min": 0.0, "max": 1.0},
    "probability": {"type": "bounds", "min": 0.0, "max": 1.0},
    "weight": {"type": "bounds", "min": 0.0, "max": 1.0},
    "alpha": {"type": "bounds", "min": 0.0, "max": 1.0},
    "beta": {"type": "bounds", "min": 0.0, "max": 1.0},
    "gamma": {"type": "bounds", "min": 0.0, "max": float("inf")},
    "temperature": {"type": "bounds", "min": 0.0, "max": float("inf")},
    "threshold": {"type": "bounds", "min": 0.0, "max": float("inf")},
```

**Public Methods:**

- `def analyze_module(self) -> None`
- `def generate_test_file(self, output_dir`

---

### `SelfReflection`

**File:** `self_reflection.py`

```python
class SelfReflection:
```

**Description:**
```
"""Enables Maximus AI to critically evaluate its own outputs and reasoning.

This module helps identify potential errors, biases, or areas for improvement,
leading to more accurate and coherent responses.
"""

def __init__(self):
    """Initializes the SelfReflection module."""
    pass

async def reflect_and_refine(self, current_response: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Performs self-reflection on the current response and refines it if necessary.

    Args:
        current_response (Dict[str, Any]): The response generated by the AI.
        context (Dict[str, Any]): The context in which the response was generated.
```

**Public Methods:**


---

### `ConstitutionalLogProcessor`

**File:** `constitutional_logging.py`

```python
class ConstitutionalLogProcessor:
```

**Description:**
```
"""Structlog processor that adds constitutional context."""

def __call__(self, logger: Any, method_name: str, event_dict: Dict) -> Dict:
    """Add constitutional context to log entries."""
    # Add service metadata
    event_dict["service"] = os.getenv("SERVICE_NAME", "unknown")
    event_dict["version"] = os.getenv("SERVICE_VERSION", "1.0.0")
    event_dict["constitution_version"] = "3.0"

    # Add trace context if available
    current_span = trace.get_current_span()
    if current_span.is_recording():
        span_context = current_span.get_span_context()
        event_dict["trace_id"] = format(span_context.trace_id, "032x")
        event_dict["span_id"] = format(span_context.span_id, "016x")
        event_dict["trace_flags"] = span_context.trace_flags
```

**Public Methods:**


---

### `BiblicalArticleProcessor`

**File:** `constitutional_logging.py`

```python
class BiblicalArticleProcessor:
```

**Description:**
```
"""Processor for biblical article compliance logging."""

def __call__(self, logger: Any, method_name: str, event_dict: Dict) -> Dict:
    """Add biblical article context if present."""
    # Check for biblical article tags
    article_tags = {
        "sophia": "wisdom",
        "praotes": "gentleness",
        "tapeinophrosyne": "humility",
        "stewardship": "stewardship",
        "agape": "love",
        "sabbath": "rest",
        "aletheia": "truth",
    }

    for article, principle in article_tags.items():
```

**Public Methods:**


---

### `ConstitutionalTracer`

**File:** `constitutional_tracing.py`

```python
class ConstitutionalTracer:
```

**Description:**
```
"""OpenTelemetry tracer with constitutional compliance tracking."""

def __init__(
    self,
    service_name: str,
    version: str = "1.0.0",
    jaeger_endpoint: Optional[str] = None,
    otlp_endpoint: Optional[str] = None,
):
    """
    Initialize constitutional tracer.

    Args:
        service_name: Name of the service (e.g., "penelope", "maba", "mvp")
        version: Service version
        jaeger_endpoint: Jaeger collector endpoint (optional)
```

**Public Methods:**

- `def instrument_fastapi(self, app`
- `def instrument_all(self) -> None`
- `def add_constitutional_attributes(`
- `def trace_biblical_article(`
- `def trace_wisdom_decision(`
- `def trace_gentleness_check(`
- `def trace_humility_check(`
- `def trace_sabbath_check(self, is_sabbath`
- `def trace_truth_check(`
- `def trace_deter_agent_layer(`

---

### `HealthStatus`

**File:** `health_checks.py`

```python
class HealthStatus(Enum):
```

**Description:**
```
"""Health check status."""
HEALTHY = "healthy"
DEGRADED = "degraded"
UNHEALTHY = "unhealthy"


class ConstitutionalHealthCheck:
"""Health checker with constitutional compliance."""

def __init__(self, service_name: str):
    self.service_name = service_name
    self.startup_complete = False
    self.checks: Dict[str, Any] = {}

def mark_startup_complete(self) -> None:
    """Mark service startup as complete."""
```

**Public Methods:**


---

### `ConstitutionalHealthCheck`

**File:** `health_checks.py`

```python
class ConstitutionalHealthCheck:
```

**Description:**
```
"""Health checker with constitutional compliance."""

def __init__(self, service_name: str):
    self.service_name = service_name
    self.startup_complete = False
    self.checks: Dict[str, Any] = {}

def mark_startup_complete(self) -> None:
    """Mark service startup as complete."""
    self.startup_complete = True

async def liveness_check(self) -> Dict[str, Any]:
    """
    Kubernetes liveness probe.
    Returns 200 if service is alive (even if degraded).
    """
```

**Public Methods:**

- `def mark_startup_complete(self) -> None`

---

### `MetricsExporter`

**File:** `metrics_exporter.py`

```python
class MetricsExporter:
```

**Description:**
```
"""Prometheus metrics exporter for Vértice services."""

def __init__(self, service_name: str, version: str = "1.0.0"):
    """
    Initialize metrics exporter.

    Args:
        service_name: Name of the service (e.g., "penelope", "maba", "mvp")
        version: Service version
    """
    self.service_name = service_name
    self.version = version
    self.start_time = time.time()

    # Set service metadata
    service_info.info(
```

**Public Methods:**

- `def update_uptime(self) -> None`
- `def update_health_status(self, check_type`
- `def create_router(self) -> APIRouter`

---

### `SkillExecutionResult`

**File:** `skill_learning_controller.py`

```python
class SkillExecutionResult:
```

**Description:**
```
"""Result of skill execution."""

skill_name: str
success: bool
steps_executed: int
total_reward: float
execution_time: float
errors: list[str]
timestamp: datetime


class SkillLearningController:
"""Controller for skill learning via HSAS service integration.

Provides:
- Execute learned skills
```

**Public Methods:**


---

### `SkillLearningController`

**File:** `skill_learning_controller.py`

```python
class SkillLearningController:
```

**Description:**
```
"""Controller for skill learning via HSAS service integration.

Provides:
- Execute learned skills
- Learn new skills from demonstrations
- Compose skills from primitives
- Track skill performance
- Integration with neuromodulation (dopamine for RPE)

This is a lightweight proxy to the full HSAS service (port 8023).
"""

def __init__(self, hsas_url: str = "http://localhost:8023", timeout: float = 30.0):
    """Initialize skill learning controller.

    Args:
```

**Public Methods:**

- `def get_skill_stats(self, skill_name`
- `def export_state(self) -> dict[str, Any]`

---

### `EdgeCasesTester`

**File:** `test_edge_cases.py`

```python
class EdgeCasesTester:
```

**Description:**
```
"""Edge cases test suite for Governance SSE."""

def __init__(self, backend_url: str = "http://localhost:8001"):
    """Initialize tester."""
    self.backend_url = backend_url
    self.results: list[dict] = []

async def test_cli_stats_with_data(self) -> dict:
    """
    Test governance stats CLI after approving decisions.

    Returns:
        Test result
    """
    print("\n" + "=" * 80)
    print("📊 FASE 6.1: CLI Stats Command (with real data)")
```

**Public Methods:**


---

### `GovernanceE2EValidator`

**File:** `test_governance_e2e.py`

```python
class GovernanceE2EValidator:
```

**Description:**
```
"""
End-to-end validator for Governance Production Server.

Tests all critical endpoints and workflows.
"""

def __init__(self, base_url: str = "http://localhost:8002"):
    """
    Initialize validator.

    Args:
        base_url: Base URL of governance server
    """
    self.base_url = base_url
    self.client = httpx.Client(timeout=30.0)
    self.results: list[dict] = []
```

**Public Methods:**

- `def test(self, name`
- `def test_root_endpoint(self)`
- `def test_health_endpoint(self)`
- `def test_governance_health(self)`
- `def test_session_creation(self)`
- `def test_pending_decisions(self)`
- `def test_enqueue_decision(self)`
- `def test_approve_decision(self)`
- `def test_session_stats(self)`
- `def run_all_tests(self)`

---

### `SSEEvent`

**File:** `test_sse_streaming.py`

```python
class SSEEvent:
```

**Description:**
```
"""Parsed SSE event."""

event_type: str
event_id: str
data: dict
timestamp: float = field(default_factory=time.time)


@dataclass
class SSETestMetrics:
"""Metrics collected during SSE testing."""

events_received: int = 0
heartbeats_received: int = 0
decisions_received: int = 0
connection_time: float = 0.0
```

**Public Methods:**


---

### `SSETestMetrics`

**File:** `test_sse_streaming.py`

```python
class SSETestMetrics:
```

**Description:**
```
"""Metrics collected during SSE testing."""

events_received: int = 0
heartbeats_received: int = 0
decisions_received: int = 0
connection_time: float = 0.0
first_event_latency: float = 0.0
avg_latency: float = 0.0
latencies: list[float] = field(default_factory=list)
errors: list[str] = field(default_factory=list)


class SSEStreamingValidator:
"""
Validates SSE streaming functionality with real server.
```

**Public Methods:**


---

### `SSEStreamingValidator`

**File:** `test_sse_streaming.py`

```python
class SSEStreamingValidator:
```

**Description:**
```
"""
Validates SSE streaming functionality with real server.

Tests:
- Connection establishment
- Heartbeat delivery
- Decision streaming
- Multi-client support
- Latency measurement
- Reconnection handling
"""

def __init__(self, base_url: str = "http://localhost:8002"):
    """
    Initialize SSE validator.
```

**Public Methods:**


---

### `StressMetrics`

**File:** `test_stress_conditions.py`

```python
class StressMetrics:
```

**Description:**
```
"""Metrics collected during stress testing."""

decisions_enqueued: int = 0
decisions_processed: int = 0
requests_sent: int = 0
requests_failed: int = 0
avg_response_time: float = 0.0
max_response_time: float = 0.0
min_response_time: float = float("inf")
response_times: list[float] = field(default_factory=list)
errors: list[str] = field(default_factory=list)
throughput: float = 0.0


class StressValidator:
"""
```

**Public Methods:**


---

### `StressValidator`

**File:** `test_stress_conditions.py`

```python
class StressValidator:
```

**Description:**
```
"""
Validates system under stress conditions.

Tests:
- High volume enqueue (100 decisions/min)
- Concurrent operators (10+)
- Queue overflow handling
- SLA violations
- Network interruption recovery
- Memory stability
"""

def __init__(self, base_url: str = "http://localhost:8002"):
    """
    Initialize stress validator.
```

**Public Methods:**


---

### `TUIValidationResult`

**File:** `test_tui_integration.py`

```python
class TUIValidationResult:
```

**Description:**
```
"""Result of a TUI validation test."""

test_name: str
passed: bool
message: str
duration: float


class TUIIntegrationValidator:
"""
Validates TUI integration with Governance backend.

Tests:
- TUI module imports
- Component instantiation
- Backend API connectivity
```

**Public Methods:**


---

### `TUIIntegrationValidator`

**File:** `test_tui_integration.py`

```python
class TUIIntegrationValidator:
```

**Description:**
```
"""
Validates TUI integration with Governance backend.

Tests:
- TUI module imports
- Component instantiation
- Backend API connectivity
- Data flow from API to TUI structures
- Session management logic
"""

def __init__(self, base_url: str = "http://localhost:8002"):
    """
    Initialize TUI validator.

    Args:
```

**Public Methods:**

- `def test_tui_imports(self) -> TUIValidationResult`
- `def test_workspace_manager_instantiation(self) -> TUIValidationResult`

---

### `WorkflowPhase`

**File:** `test_workflow_complete.py`

```python
class WorkflowPhase(Enum):
```

**Description:**
```
"""Workflow test phases."""

SESSION_CREATION = "session_creation"
DECISION_ENQUEUE = "decision_enqueue"
DECISION_PROCESSING = "decision_processing"
STATS_VALIDATION = "stats_validation"
CLEANUP = "cleanup"


@dataclass
class WorkflowMetrics:
"""Metrics collected during workflow testing."""

sessions_created: int = 0
decisions_enqueued: int = 0
decisions_approved: int = 0
```

**Public Methods:**


---

### `WorkflowMetrics`

**File:** `test_workflow_complete.py`

```python
class WorkflowMetrics:
```

**Description:**
```
"""Metrics collected during workflow testing."""

sessions_created: int = 0
decisions_enqueued: int = 0
decisions_approved: int = 0
decisions_rejected: int = 0
decisions_escalated: int = 0
total_processed: int = 0
processing_time: float = 0.0
errors: list[str] = field(default_factory=list)


@dataclass
class OperatorSession:
"""Operator session data."""
```

**Public Methods:**


---

### `OperatorSession`

**File:** `test_workflow_complete.py`

```python
class OperatorSession:
```

**Description:**
```
"""Operator session data."""

operator_id: str
session_id: str
decisions_processed: int = 0
start_time: float = field(default_factory=time.time)


class WorkflowValidator:
"""
Validates complete operator workflows.

Tests:
- Full operator session lifecycle
- Mixed risk level decision processing
- Stats accumulation accuracy
```

**Public Methods:**


---

### `WorkflowValidator`

**File:** `test_workflow_complete.py`

```python
class WorkflowValidator:
```

**Description:**
```
"""
Validates complete operator workflows.

Tests:
- Full operator session lifecycle
- Mixed risk level decision processing
- Stats accumulation accuracy
- Concurrent operator handling
- Error recovery
"""

def __init__(self, base_url: str = "http://localhost:8002"):
    """
    Initialize workflow validator.

    Args:
```

**Public Methods:**


---

### `ToolOrchestrator`

**File:** `tool_orchestrator.py`

```python
class ToolOrchestrator:
```

**Description:**
```
"""Dynamically selects, invokes, and manages the execution of various tools.

This class acts as a central hub for tool interaction, enabling Maximus to
extend its capabilities by interacting with external APIs and services.
"""

def __init__(self, gemini_client: Any):
    """Initializes the ToolOrchestrator with an AllServicesTools instance.

    Args:
        gemini_client (Any): An initialized Gemini client for tool interactions.
    """
    self.all_tools = AllServicesTools(gemini_client)
    self.ethical_wrapper: EthicalToolWrapper | None = None  # Injected later

def set_ethical_wrapper(self, wrapper: "EthicalToolWrapper"):
```

**Public Methods:**

- `def set_ethical_wrapper(self, wrapper`
- `def list_all_available_tools(self) -> list[dict[str, Any]]`
- `def get_gemini_function_declarations(self) -> list[dict[str, Any]]`

---

### `RetrainingConfig`

**File:** `continuous_training.py`

```python
class RetrainingConfig:
```

**Description:**
```
"""Retraining configuration."""

# Schedule
retrain_frequency_days: int = 7  # Retrain every N days
min_new_samples: int = 1000  # Minimum new samples to trigger retraining

# Data validation
drift_threshold: float = 0.1  # Max drift allowed
min_accuracy_threshold: float = 0.85  # Min accuracy required

# Model comparison
comparison_metric: str = "val_loss"  # Metric to compare models
improvement_threshold: float = 0.02  # Min improvement to deploy

# Registry
registry_dir: Path = Path("training/models")
```

**Public Methods:**


---

### `ContinuousTrainingPipeline`

**File:** `continuous_training.py`

```python
class ContinuousTrainingPipeline:
```

**Description:**
```
"""Continuous training pipeline.

Monitors data, detects drift, retrains models, and deploys updates.

Example:
    ```python
    config = RetrainingConfig(retrain_frequency_days=7, min_new_samples=1000)

    pipeline = ContinuousTrainingPipeline(config=config)

    # Run retraining
    result = pipeline.run_retraining(layer_name="layer1", model_name="layer1_vae", train_fn=train_layer1_vae)

    if result["deployed"]:
        print(f"New model deployed: {result['new_version']}")
    ```
```

**Public Methods:**

- `def run_retraining(`

---

### `DataSourceType`

**File:** `data_collection.py`

```python
class DataSourceType(Enum):
```

**Description:**
```
"""Supported data source types."""

ELASTIC = "elasticsearch"
SPLUNK = "splunk"
QRADAR = "qradar"
JSON_FILE = "json_file"
CSV_FILE = "csv_file"
PARQUET_FILE = "parquet_file"
ZEEK_LOGS = "zeek_logs"
SURICATA_LOGS = "suricata_logs"


@dataclass
class DataSource:
"""Configuration for a data source."""
```

**Public Methods:**


---

### `DataSource`

**File:** `data_collection.py`

```python
class DataSource:
```

**Description:**
```
"""Configuration for a data source."""

name: str
source_type: DataSourceType
connection_params: dict[str, Any]
query_filter: str | None = None
time_field: str = "@timestamp"
batch_size: int = 1000

def __repr__(self) -> str:
    return f"DataSource(name={self.name}, type={self.source_type.value})"


@dataclass
class CollectedEvent:
"""Represents a collected security event."""
```

**Public Methods:**


---

### `CollectedEvent`

**File:** `data_collection.py`

```python
class CollectedEvent:
```

**Description:**
```
"""Represents a collected security event."""

event_id: str
timestamp: datetime
source: str
event_type: str
raw_data: dict[str, Any]
labels: dict[str, Any] | None = None

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary."""
    return {
        "event_id": self.event_id,
        "timestamp": self.timestamp.isoformat(),
        "source": self.source,
        "event_type": self.event_type,
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `DataCollector`

**File:** `data_collection.py`

```python
class DataCollector:
```

**Description:**
```
"""Collects security events from multiple sources for training.

Features:
- Multi-source collection (SIEM, EDR, files)
- Incremental collection (resume from checkpoint)
- Deduplication
- Time-based filtering
- Batch processing
- Error handling and retry

Example:
    ```python
    # Collect from JSON file
    source = DataSource(
        name="synthetic_events",
        source_type=DataSourceType.JSON_FILE,
```

**Public Methods:**

- `def collect(`
- `def save_to_file(self, events`
- `def get_stats(self) -> dict[str, Any]`

---

### `LayerType`

**File:** `data_preprocessor.py`

```python
class LayerType(Enum):
```

**Description:**
```
"""Predictive Coding layers."""

LAYER1_SENSORY = "layer1_sensory"
LAYER2_BEHAVIORAL = "layer2_behavioral"
LAYER3_OPERATIONAL = "layer3_operational"
LAYER4_TACTICAL = "layer4_tactical"
LAYER5_STRATEGIC = "layer5_strategic"


@dataclass
class PreprocessedSample:
"""Preprocessed sample for training."""

sample_id: str
layer: LayerType
features: np.ndarray
```

**Public Methods:**


---

### `PreprocessedSample`

**File:** `data_preprocessor.py`

```python
class PreprocessedSample:
```

**Description:**
```
"""Preprocessed sample for training."""

sample_id: str
layer: LayerType
features: np.ndarray
label: int | None = None
metadata: dict[str, Any] | None = None

def __repr__(self) -> str:
    return f"PreprocessedSample(layer={self.layer.value}, features_shape={self.features.shape}, label={self.label})"


class LayerPreprocessor(ABC):
"""Abstract base class for layer-specific preprocessing."""

def __init__(self, layer: LayerType):
```

**Public Methods:**


---

### `LayerPreprocessor`

**File:** `data_preprocessor.py`

```python
class LayerPreprocessor(ABC):
```

**Description:**
```
"""Abstract base class for layer-specific preprocessing."""

def __init__(self, layer: LayerType):
    """Initialize preprocessor.

    Args:
        layer: Target layer type
    """
    self.layer = layer

@abstractmethod
def preprocess(self, event: dict[str, Any]) -> PreprocessedSample:
    """Preprocess event for this layer.

    Args:
        event: Raw event data
```

**Public Methods:**

- `def preprocess(self, event`
- `def get_feature_dim(self) -> int`

---

### `Layer1Preprocessor`

**File:** `data_preprocessor.py`

```python
class Layer1Preprocessor(LayerPreprocessor):
```

**Description:**
```
"""Preprocessor for Layer 1 (Sensory) - VAE input.

Extracts low-level features:
- Network features (IPs, ports, protocols)
- Process features (PIDs, names, paths)
- File features (hashes, sizes, extensions)
- User features (UIDs, names, domains)
"""

def __init__(self):
    """Initialize Layer 1 preprocessor."""
    super().__init__(LayerType.LAYER1_SENSORY)

    # Feature extractors
    self.feature_dim = 128  # Fixed dimension for VAE
```

**Public Methods:**

- `def preprocess(self, event`
- `def get_feature_dim(self) -> int`

---

### `Layer2Preprocessor`

**File:** `data_preprocessor.py`

```python
class Layer2Preprocessor(LayerPreprocessor):
```

**Description:**
```
"""Preprocessor for Layer 2 (Behavioral) - GNN input.

Constructs behavior graphs:
- Nodes: Entities (processes, files, IPs)
- Edges: Interactions (spawns, reads, connects)
- Node features: Entity attributes
- Edge features: Interaction types
"""

def __init__(self):
    """Initialize Layer 2 preprocessor."""
    super().__init__(LayerType.LAYER2_BEHAVIORAL)

    self.node_feature_dim = 64
    self.edge_feature_dim = 16
```

**Public Methods:**

- `def preprocess(self, event`
- `def get_feature_dim(self) -> int`

---

### `Layer3Preprocessor`

**File:** `data_preprocessor.py`

```python
class Layer3Preprocessor(LayerPreprocessor):
```

**Description:**
```
"""Preprocessor for Layer 3 (Operational) - TCN input.

Creates time series features:
- Sliding window of events (e.g., last 10 events)
- Temporal patterns
- Rate of events
"""

def __init__(self, window_size: int = 10):
    """Initialize Layer 3 preprocessor.

    Args:
        window_size: Number of events in time window
    """
    super().__init__(LayerType.LAYER3_OPERATIONAL)
```

**Public Methods:**

- `def preprocess(self, event`
- `def get_feature_dim(self) -> int`

---

### `DataPreprocessor`

**File:** `data_preprocessor.py`

```python
class DataPreprocessor:
```

**Description:**
```
"""Main preprocessor that coordinates layer-specific preprocessing.

Example:
    ```python
    preprocessor = DataPreprocessor(output_dir="training/data/preprocessed")

    # Preprocess for all layers
    samples = preprocessor.preprocess_event(event, layers="all")

    # Preprocess for specific layer
    sample = preprocessor.preprocess_event(event, layers=[LayerType.LAYER1_SENSORY])
    ```
"""

def __init__(self, output_dir: Path | None = None):
    """Initialize preprocessor.
```

**Public Methods:**

- `def preprocess_event(`
- `def preprocess_batch(self, events`
- `def save_samples(self, samples`
- `def load_samples(self, filepath`

---

### `SplitStrategy`

**File:** `dataset_builder.py`

```python
class SplitStrategy(Enum):
```

**Description:**
```
"""Dataset split strategies."""

RANDOM = "random"  # Random shuffle
STRATIFIED = "stratified"  # Stratified by label
TEMPORAL = "temporal"  # Respect time ordering
K_FOLD = "k_fold"  # K-fold cross-validation


@dataclass
class DatasetSplit:
"""Represents a dataset split (train/val/test)."""

name: str  # "train", "val", "test"
features: np.ndarray
labels: np.ndarray
sample_ids: list[str]
```

**Public Methods:**


---

### `DatasetSplit`

**File:** `dataset_builder.py`

```python
class DatasetSplit:
```

**Description:**
```
"""Represents a dataset split (train/val/test)."""

name: str  # "train", "val", "test"
features: np.ndarray
labels: np.ndarray
sample_ids: list[str]
indices: np.ndarray

def __len__(self) -> int:
    return len(self.features)

def __repr__(self) -> str:
    label_dist = np.bincount(self.labels[self.labels >= 0])
    return f"DatasetSplit(name={self.name}, size={len(self)}, label_dist={label_dist.tolist()})"

def get_class_distribution(self) -> dict[int, int]:
```

**Public Methods:**

- `def get_class_distribution(self) -> dict[int, int]`
- `def save(self, output_path`
- `def load(cls, filepath`

---

### `DatasetBuilder`

**File:** `dataset_builder.py`

```python
class DatasetBuilder:
```

**Description:**
```
"""Builds training datasets with various split strategies.

Features:
- Multiple split strategies (random, stratified, temporal, k-fold)
- Class balancing
- Data augmentation
- PyTorch-compatible outputs

Example:
    ```python
    builder = DatasetBuilder(
        features=features, labels=labels, sample_ids=sample_ids, output_dir="training/data/splits"
    )

    # Create stratified split
    splits = builder.create_splits(
```

**Public Methods:**

- `def create_splits(`
- `def save_splits(self, splits`
- `def load_splits(cls, split_dir`
- `def augment_data(self, split`
- `def get_statistics(self) -> dict[str, Any]`

---

### `PyTorchDatasetWrapper`

**File:** `dataset_builder.py`

```python
class PyTorchDatasetWrapper:
```

**Description:**
```
"""Wrapper to convert DatasetSplit to PyTorch Dataset.

Example:
    ```python
    from torch.utils.data import DataLoader

    # Create PyTorch dataset
    train_dataset = PyTorchDatasetWrapper(train_split)

    # Create data loader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

    # Iterate
    for batch_features, batch_labels in train_loader:
        # Training loop
        pass
```

**Public Methods:**

- `def get_sample_id(self, idx`

---

### `ValidationSeverity`

**File:** `data_validator.py`

```python
class ValidationSeverity(Enum):
```

**Description:**
```
"""Validation issue severity."""

INFO = "info"
WARNING = "warning"
ERROR = "error"


@dataclass
class ValidationIssue:
"""Represents a validation issue."""

severity: ValidationSeverity
check_name: str
message: str
details: dict[str, Any] | None = None
```

**Public Methods:**


---

### `ValidationIssue`

**File:** `data_validator.py`

```python
class ValidationIssue:
```

**Description:**
```
"""Represents a validation issue."""

severity: ValidationSeverity
check_name: str
message: str
details: dict[str, Any] | None = None

def __repr__(self) -> str:
    return f"[{self.severity.value.upper()}] {self.check_name}: {self.message}"


@dataclass
class ValidationResult:
"""Result of data validation."""

passed: bool
```

**Public Methods:**


---

### `ValidationResult`

**File:** `data_validator.py`

```python
class ValidationResult:
```

**Description:**
```
"""Result of data validation."""

passed: bool
issues: list[ValidationIssue]
statistics: dict[str, Any]

def __repr__(self) -> str:
    n_errors = sum(1 for issue in self.issues if issue.severity == ValidationSeverity.ERROR)
    n_warnings = sum(1 for issue in self.issues if issue.severity == ValidationSeverity.WARNING)
    n_info = sum(1 for issue in self.issues if issue.severity == ValidationSeverity.INFO)

    return f"ValidationResult(passed={self.passed}, errors={n_errors}, warnings={n_warnings}, info={n_info})"

def print_report(self):
    """Print validation report."""
    print("\n" + "=" * 80)
```

**Public Methods:**

- `def print_report(self)`

---

### `DataValidator`

**File:** `data_validator.py`

```python
class DataValidator:
```

**Description:**
```
"""Validates data quality for training.

Performs comprehensive checks:
- Missing values
- Outliers
- Label distribution
- Feature statistics
- Data drift

Example:
    ```python
    validator = DataValidator(
        features=features,
        labels=labels,
        reference_features=None,  # Optional reference for drift detection
    )
```

**Public Methods:**

- `def validate(`
- `def save_report(self, result`

---

### `EvaluationMetrics`

**File:** `evaluator.py`

```python
class EvaluationMetrics:
```

**Description:**
```
"""Evaluation metrics for a model."""

# Classification metrics
accuracy: float
precision: float
recall: float
f1_score: float
roc_auc: float | None = None
pr_auc: float | None = None

# Confusion matrix
confusion_matrix: np.ndarray | None = None

# Per-class metrics
per_class_metrics: dict[int, dict[str, float]] | None = None
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`

---

### `ModelEvaluator`

**File:** `evaluator.py`

```python
class ModelEvaluator:
```

**Description:**
```
"""Evaluates trained models on test data.

Features:
- Classification metrics
- ROC/PR curves
- Confusion matrix
- Per-class analysis
- Latency benchmarking
- Model comparison

Example:
    ```python
    evaluator = ModelEvaluator(model=trained_model, test_features=test_features, test_labels=test_labels)

    # Evaluate
    metrics = evaluator.evaluate()
```

**Public Methods:**

- `def evaluate(`
- `def print_report(self, metrics`
- `def save_report(self, metrics`

---

### `TuningConfig`

**File:** `hyperparameter_tuner.py`

```python
class TuningConfig:
```

**Description:**
```
"""Hyperparameter tuning configuration."""

# Study
study_name: str
direction: str = "minimize"  # "minimize" or "maximize"
n_trials: int = 50
timeout: int | None = None  # Timeout in seconds

# Sampler
sampler: str = "tpe"  # "tpe", "random", "grid"

# Pruner (early stopping)
use_pruner: bool = True
pruner_n_startup_trials: int = 5
pruner_n_warmup_steps: int = 10
```

**Public Methods:**


---

### `HyperparameterTuner`

**File:** `hyperparameter_tuner.py`

```python
class HyperparameterTuner:
```

**Description:**
```
"""Hyperparameter tuner using Optuna.

Features:
- Bayesian optimization (TPE sampler)
- Pruning (MedianPruner for early stopping)
- Multi-objective optimization
- Parallel trials
- Visualization

Example:
    ```python
    # Define objective function
    def objective(trial):
        # Suggest hyperparameters
        lr = trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True)
        batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
```

**Public Methods:**

- `def tune(`
- `def visualize(self)`
- `def objective(trial`

---

### `TrainingConfig`

**File:** `layer_trainer.py`

```python
class TrainingConfig:
```

**Description:**
```
"""Training configuration."""

# Model
model_name: str
layer_name: str  # "layer1", "layer2", etc.

# Training
batch_size: int = 32
num_epochs: int = 100
learning_rate: float = 1e-3
weight_decay: float = 1e-5

# Optimization
optimizer: str = "adam"  # "adam", "sgd", "adamw"
lr_scheduler: str | None = "reduce_on_plateau"  # "step", "cosine", "reduce_on_plateau"
gradient_clip_value: float | None = 1.0
```

**Public Methods:**


---

### `TrainingMetrics`

**File:** `layer_trainer.py`

```python
class TrainingMetrics:
```

**Description:**
```
"""Training metrics for an epoch."""

epoch: int
train_loss: float
val_loss: float | None = None
train_metrics: dict[str, float] | None = None
val_metrics: dict[str, float] | None = None
learning_rate: float = 0.0
epoch_time: float = 0.0

def __repr__(self) -> str:
    return (
        f"Epoch {self.epoch}: train_loss={self.train_loss:.4f}, "
        f"val_loss={self.val_loss:.4f if self.val_loss else 'N/A'}"
    )
```

**Public Methods:**


---

### `EarlyStopping`

**File:** `layer_trainer.py`

```python
class EarlyStopping:
```

**Description:**
```
"""Early stopping handler.

Stops training when validation loss stops improving.
"""

def __init__(self, patience: int = 10, min_delta: float = 1e-4, mode: str = "min"):
    """Initialize early stopping.

    Args:
        patience: Number of epochs to wait for improvement
        min_delta: Minimum change to qualify as improvement
        mode: "min" (minimize loss) or "max" (maximize metric)
    """
    self.patience = patience
    self.min_delta = min_delta
    self.mode = mode
```

**Public Methods:**


---

### `LayerTrainer`

**File:** `layer_trainer.py`

```python
class LayerTrainer:
```

**Description:**
```
"""Generic trainer for Predictive Coding layers.

Provides complete training infrastructure for any layer architecture.

Example:
    ```python
    # Define model (PyTorch nn.Module)
    model = Layer1VAE(input_dim=128, latent_dim=64)


    # Define loss function
    def loss_fn(model, batch):
        inputs, labels = batch
        outputs = model(inputs)
        reconstruction_loss = F.mse_loss(outputs, inputs)
        kl_loss = model.get_kl_loss()
```

**Public Methods:**

- `def train(`
- `def load_checkpoint(self, checkpoint_path`

---

### `ModelMetadata`

**File:** `model_registry.py`

```python
class ModelMetadata:
```

**Description:**
```
"""Metadata for a registered model."""

model_name: str
version: str
layer_name: str
created_at: datetime
metrics: dict[str, float]
hyperparameters: dict[str, Any]
training_dataset: str | None = None
framework: str = "pytorch"
stage: str = "none"  # "none", "staging", "production", "archived"

def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary.

    Returns:
```

**Public Methods:**

- `def to_dict(self) -> dict[str, Any]`
- `def from_dict(cls, data`

---

### `ModelRegistry`

**File:** `model_registry.py`

```python
class ModelRegistry:
```

**Description:**
```
"""Model registry for versioning and management.

Features:
- Model registration with metadata
- Version management
- Stage transitions (none -> staging -> production)
- Model search and filtering
- Automatic archival of old models

Example:
    ```python
    registry = ModelRegistry(registry_dir="training/models")

    # Register model
    metadata = ModelMetadata(
        model_name="layer1_vae",
```

**Public Methods:**

- `def register_model(self, model_path`
- `def get_model(self, model_name`
- `def get_metadata(self, model_name`
- `def list_models(self, model_name`
- `def transition_stage(self, model_name`
- `def compare_models(self, model_name`
- `def search_models(`
- `def delete_model(self, model_name`
- `def print_registry(self)`

---

### `ValidationResult`

**File:** `validate_regra_de_ouro.py`

```python
class ValidationResult:
```

**Description:**
```
"""Result of REGRA DE OURO validation."""

# File info
file_path: str
lines_of_code: int

# REGRA DE OURO violations
todo_violations: list[tuple[int, str]] = field(default_factory=list)
mock_violations: list[tuple[int, str]] = field(default_factory=list)
placeholder_violations: list[tuple[int, str]] = field(default_factory=list)

# Quality metrics
has_module_docstring: bool = False
functions_without_docstring: list[str] = field(default_factory=list)
functions_without_type_hints: list[str] = field(default_factory=list)
classes_without_docstring: list[str] = field(default_factory=list)
```

**Public Methods:**

- `def is_compliant(self) -> bool`
- `def total_violations(self) -> int`
- `def quality_score(self) -> float`

---

### `RegraDeOuroValidator`

**File:** `validate_regra_de_ouro.py`

```python
class RegraDeOuroValidator:
```

**Description:**
```
"""Validator for REGRA DE OURO compliance."""

def __init__(self, project_root: str):
    """
    Initialize validator.

    Args:
        project_root: Root directory of project to validate
    """
    self.project_root = Path(project_root)
    self.results: list[ValidationResult] = []

    # Patterns to detect violations
    self.todo_patterns = [
        r"\bTODO\b",
        r"\bFIXME\b",
```

**Public Methods:**

- `def validate_file(self, file_path`
- `def validate_directory(self, directory`
- `def generate_report(self, results`

---

### `AIAnalyzer`

**File:** `ai_analyzer.py`

```python
class AIAnalyzer:
```

**Description:**
```
"""AI-powered OSINT analysis using OpenAI and Gemini."""

def __init__(self):
    """Initialize AI analyzer with API keys from environment."""
    # OpenAI setup
    self.openai_key = os.getenv("OPENAI_API_KEY")
    self.openai_client = None
    if self.openai_key:
        try:
            self.openai_client = OpenAI(api_key=self.openai_key)
            logger.info("✅ OpenAI client initialized")
        except Exception as e:
            logger.error(f"❌ OpenAI initialization failed: {e}")

    # Gemini setup
    self.gemini_key = os.getenv("GEMINI_API_KEY")
```

**Public Methods:**

- `def analyze_attack_surface(`
- `def analyze_credential_exposure(`
- `def analyze_target_profile(`

---

### `WorkflowStatus`

**File:** `attack_surface_adw.py`

```python
class WorkflowStatus(Enum):
```

**Description:**
```
"""Workflow execution status."""
PENDING = "pending"
RUNNING = "running"
COMPLETED = "completed"
FAILED = "failed"


class RiskLevel(Enum):
"""Risk level classification."""
CRITICAL = "critical"
HIGH = "high"
MEDIUM = "medium"
LOW = "low"
INFO = "info"
```

**Public Methods:**


---

### `RiskLevel`

**File:** `attack_surface_adw.py`

```python
class RiskLevel(Enum):
```

**Description:**
```
"""Risk level classification."""
CRITICAL = "critical"
HIGH = "high"
MEDIUM = "medium"
LOW = "low"
INFO = "info"


@dataclass
class AttackSurfaceTarget:
"""Target for attack surface mapping."""
domain: str
include_subdomains: bool = True
port_range: Optional[str] = None  # e.g., "1-1000" or "80,443,22"
scan_depth: str = "standard"  # standard, deep, quick
```

**Public Methods:**


---

### `AttackSurfaceTarget`

**File:** `attack_surface_adw.py`

```python
class AttackSurfaceTarget:
```

**Description:**
```
"""Target for attack surface mapping."""
domain: str
include_subdomains: bool = True
port_range: Optional[str] = None  # e.g., "1-1000" or "80,443,22"
scan_depth: str = "standard"  # standard, deep, quick


@dataclass
class Finding:
"""Individual attack surface finding."""
finding_id: str
finding_type: str  # subdomain, open_port, service, vulnerability
severity: RiskLevel
target: str
details: Dict[str, Any]
timestamp: str
```

**Public Methods:**


---

### `Finding`

**File:** `attack_surface_adw.py`

```python
class Finding:
```

**Description:**
```
"""Individual attack surface finding."""
finding_id: str
finding_type: str  # subdomain, open_port, service, vulnerability
severity: RiskLevel
target: str
details: Dict[str, Any]
timestamp: str
confidence: float = 1.0


@dataclass
class AttackSurfaceReport:
"""Complete attack surface mapping report."""
workflow_id: str
target: str
status: WorkflowStatus
```

**Public Methods:**


---

### `AttackSurfaceReport`

**File:** `attack_surface_adw.py`

```python
class AttackSurfaceReport:
```

**Description:**
```
"""Complete attack surface mapping report."""
workflow_id: str
target: str
status: WorkflowStatus
started_at: str
completed_at: Optional[str]
findings: List[Finding] = field(default_factory=list)
statistics: Dict[str, Any] = field(default_factory=dict)
risk_score: float = 0.0
recommendations: List[str] = field(default_factory=list)
ai_analysis: Optional[Dict[str, Any]] = None  # NEW: AI-powered analysis
error: Optional[str] = None

def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary."""
    return {
```

**Public Methods:**

- `def to_dict(self) -> Dict[str, Any]`

---

### `AttackSurfaceWorkflow`

**File:** `attack_surface_adw.py`

```python
class AttackSurfaceWorkflow:
```

**Description:**
```
"""External Attack Surface Mapping AI-Driven Workflow.

Orchestrates multiple OSINT services to build comprehensive attack surface map.
"""

def __init__(
    self,
    network_recon_service_url: str = "http://localhost:8032",
    vuln_intel_service_url: str = "http://localhost:8045",
    vuln_scanner_service_url: str = "http://localhost:8046",
):
    """Initialize attack surface workflow.

    Args:
        network_recon_service_url: Network Recon Service endpoint
        vuln_intel_service_url: Vuln Intel Service endpoint
```

**Public Methods:**

- `def get_workflow_status(self, workflow_id`

---

### `WorkflowStatus`

**File:** `credential_intel_adw.py`

```python
class WorkflowStatus(Enum):
```

**Description:**
```
"""Workflow execution status."""
PENDING = "pending"
RUNNING = "running"
COMPLETED = "completed"
FAILED = "failed"


class CredentialRiskLevel(Enum):
"""Credential exposure risk level."""
CRITICAL = "critical"  # Active breach with passwords
HIGH = "high"  # Multiple breaches or dark web presence
MEDIUM = "medium"  # Single breach or dorking findings
LOW = "low"  # Username enumeration only
INFO = "info"  # No exposure found
```

**Public Methods:**


---

### `CredentialRiskLevel`

**File:** `credential_intel_adw.py`

```python
class CredentialRiskLevel(Enum):
```

**Description:**
```
"""Credential exposure risk level."""
CRITICAL = "critical"  # Active breach with passwords
HIGH = "high"  # Multiple breaches or dark web presence
MEDIUM = "medium"  # Single breach or dorking findings
LOW = "low"  # Username enumeration only
INFO = "info"  # No exposure found


@dataclass
class CredentialTarget:
"""Target for credential intelligence gathering."""
email: Optional[str] = None
username: Optional[str] = None
phone: Optional[str] = None
include_darkweb: bool = True
include_dorking: bool = True
```

**Public Methods:**


---

### `CredentialTarget`

**File:** `credential_intel_adw.py`

```python
class CredentialTarget:
```

**Description:**
```
"""Target for credential intelligence gathering."""
email: Optional[str] = None
username: Optional[str] = None
phone: Optional[str] = None
include_darkweb: bool = True
include_dorking: bool = True
include_social: bool = True


@dataclass
class CredentialFinding:
"""Individual credential exposure finding."""
finding_id: str
finding_type: str  # breach, dork, darkweb, username, social
severity: CredentialRiskLevel
source: str
```

**Public Methods:**


---

### `CredentialFinding`

**File:** `credential_intel_adw.py`

```python
class CredentialFinding:
```

**Description:**
```
"""Individual credential exposure finding."""
finding_id: str
finding_type: str  # breach, dork, darkweb, username, social
severity: CredentialRiskLevel
source: str
details: Dict[str, Any]
timestamp: str
confidence: float = 1.0


@dataclass
class CredentialIntelReport:
"""Complete credential intelligence report."""
workflow_id: str
target_email: Optional[str]
target_username: Optional[str]
```

**Public Methods:**


---

### `CredentialIntelReport`

**File:** `credential_intel_adw.py`

```python
class CredentialIntelReport:
```

**Description:**
```
"""Complete credential intelligence report."""
workflow_id: str
target_email: Optional[str]
target_username: Optional[str]
status: WorkflowStatus
started_at: str
completed_at: Optional[str]
findings: List[CredentialFinding] = field(default_factory=list)
exposure_score: float = 0.0
breach_count: int = 0
platform_presence: List[str] = field(default_factory=list)
recommendations: List[str] = field(default_factory=list)
statistics: Dict[str, Any] = field(default_factory=dict)
ai_analysis: Optional[Dict[str, Any]] = field(default=None)  # FIX: use field(default=None)
error: Optional[str] = field(default=None)  # FIX: use field(default=None)
```

**Public Methods:**

- `def to_dict(self) -> Dict[str, Any]`

---

### `CredentialIntelWorkflow`

**File:** `credential_intel_adw.py`

```python
class CredentialIntelWorkflow:
```

**Description:**
```
"""Credential Intelligence AI-Driven Workflow.

Orchestrates multiple OSINT services to discover credential exposure and risk.
"""

def __init__(
    self,
    osint_service_url: str = "http://localhost:8036",
):
    """Initialize credential intelligence workflow.

    Args:
        osint_service_url: OSINT Service endpoint
    """
    import os
    self.osint_url = osint_service_url if osint_service_url != "http://localhost:8036" else os.getenv("OSINT_SERVICE_URL", "http://localhost:8036")
```

**Public Methods:**

- `def get_workflow_status(self, workflow_id`

---

### `WorkflowStatus`

**File:** `target_profiling_adw.py`

```python
class WorkflowStatus(Enum):
```

**Description:**
```
"""Workflow execution status."""
PENDING = "pending"
RUNNING = "running"
COMPLETED = "completed"
FAILED = "failed"


class SEVulnerability(Enum):
"""Social engineering vulnerability level."""
CRITICAL = "critical"  # Highly susceptible, immediate risk
HIGH = "high"  # Multiple risk factors identified
MEDIUM = "medium"  # Some exposure, manageable risk
LOW = "low"  # Minimal exposure
INFO = "info"  # Informational only
```

**Public Methods:**


---

### `SEVulnerability`

**File:** `target_profiling_adw.py`

```python
class SEVulnerability(Enum):
```

**Description:**
```
"""Social engineering vulnerability level."""
CRITICAL = "critical"  # Highly susceptible, immediate risk
HIGH = "high"  # Multiple risk factors identified
MEDIUM = "medium"  # Some exposure, manageable risk
LOW = "low"  # Minimal exposure
INFO = "info"  # Informational only


@dataclass
class ProfileTarget:
"""Target for deep profiling."""
username: Optional[str] = None
email: Optional[str] = None
phone: Optional[str] = None
name: Optional[str] = None
location: Optional[str] = None
```

**Public Methods:**


---

### `ProfileTarget`

**File:** `target_profiling_adw.py`

```python
class ProfileTarget:
```

**Description:**
```
"""Target for deep profiling."""
username: Optional[str] = None
email: Optional[str] = None
phone: Optional[str] = None
name: Optional[str] = None
location: Optional[str] = None
image_url: Optional[str] = None
include_social: bool = True
include_images: bool = True


@dataclass
class ProfileFinding:
"""Individual profiling finding."""
finding_id: str
finding_type: str  # contact, social, platform, image, pattern, behavior
```

**Public Methods:**


---

### `ProfileFinding`

**File:** `target_profiling_adw.py`

```python
class ProfileFinding:
```

**Description:**
```
"""Individual profiling finding."""
finding_id: str
finding_type: str  # contact, social, platform, image, pattern, behavior
category: str
details: Dict[str, Any]
timestamp: str
confidence: float = 1.0


@dataclass
class TargetProfileReport:
"""Complete target profiling report."""
workflow_id: str
target_username: Optional[str]
target_email: Optional[str]
target_name: Optional[str]
```

**Public Methods:**


---

### `TargetProfileReport`

**File:** `target_profiling_adw.py`

```python
class TargetProfileReport:
```

**Description:**
```
"""Complete target profiling report."""
workflow_id: str
target_username: Optional[str]
target_email: Optional[str]
target_name: Optional[str]
status: WorkflowStatus
started_at: str
completed_at: Optional[str]
findings: List[ProfileFinding] = field(default_factory=list)
contact_info: Dict[str, Any] = field(default_factory=dict)
social_profiles: List[Dict[str, Any]] = field(default_factory=list)
platform_presence: List[str] = field(default_factory=list)
behavioral_patterns: List[Dict[str, Any]] = field(default_factory=list)
locations: List[Dict[str, Any]] = field(default_factory=list)
se_vulnerability: SEVulnerability = SEVulnerability.INFO
se_score: float = 0.0
```

**Public Methods:**

- `def to_dict(self) -> Dict[str, Any]`

---

### `TargetProfilingWorkflow`

**File:** `target_profiling_adw.py`

```python
class TargetProfilingWorkflow:
```

**Description:**
```
"""Deep Target Profiling AI-Driven Workflow.

Orchestrates multiple OSINT services to build comprehensive target profile for security assessment.
"""

def __init__(
    self,
    osint_service_url: str = "http://localhost:8036",
):
    """Initialize target profiling workflow.

    Args:
        osint_service_url: OSINT Service endpoint
    """
    import os
    self.osint_url = osint_service_url if osint_service_url != "http://localhost:8036" else os.getenv("OSINT_SERVICE_URL", "http://localhost:8036")
```

**Public Methods:**

- `def get_workflow_status(self, workflow_id`

---

### `ExplanationType`

**File:** `base.py`

```python
class ExplanationType(str, Enum):
```

**Description:**
```
"""Types of explanations supported."""

LIME = "lime"
SHAP = "shap"
COUNTERFACTUAL = "counterfactual"
FEATURE_IMPORTANCE = "feature_importance"
ANCHORS = "anchors"  # For future implementation


class DetailLevel(str, Enum):
"""Level of detail in explanations."""

SUMMARY = "summary"  # High-level summary (1-2 sentences)
DETAILED = "detailed"  # Detailed explanation with top features
TECHNICAL = "technical"  # Full technical details with all features
```

**Public Methods:**


---

### `DetailLevel`

**File:** `base.py`

```python
class DetailLevel(str, Enum):
```

**Description:**
```
"""Level of detail in explanations."""

SUMMARY = "summary"  # High-level summary (1-2 sentences)
DETAILED = "detailed"  # Detailed explanation with top features
TECHNICAL = "technical"  # Full technical details with all features


@dataclass
class FeatureImportance:
"""Feature importance information.

Attributes:
    feature_name: Name of the feature
    importance: Importance score (can be positive or negative)
    value: Actual value of the feature in the instance
    description: Human-readable description of the feature
```

**Public Methods:**


---

### `FeatureImportance`

**File:** `base.py`

```python
class FeatureImportance:
```

**Description:**
```
"""Feature importance information.

Attributes:
    feature_name: Name of the feature
    importance: Importance score (can be positive or negative)
    value: Actual value of the feature in the instance
    description: Human-readable description of the feature
    contribution: Contribution to the final prediction
"""

feature_name: str
importance: float
value: Any
description: str
contribution: float
```

**Public Methods:**


---

### `ExplanationResult`

**File:** `base.py`

```python
class ExplanationResult:
```

**Description:**
```
"""Result from an explanation generation.

Attributes:
    explanation_id: Unique identifier for this explanation
    decision_id: ID of the decision being explained
    explanation_type: Type of explanation (lime, shap, etc.)
    detail_level: Level of detail
    summary: High-level summary of the explanation
    top_features: Top N most important features
    all_features: All features with importance scores
    confidence: Confidence in the explanation (0.0 to 1.0)
    counterfactual: Optional counterfactual scenario
    visualization_data: Data for visualization (SHAP waterfall, etc.)
    model_type: Type of model being explained
    latency_ms: Time taken to generate explanation
    metadata: Additional metadata
```

**Public Methods:**


---

### `ExplainerBase`

**File:** `base.py`

```python
class ExplainerBase(ABC):
```

**Description:**
```
"""Abstract base class for all explainers.

All explainers (LIME, SHAP, Counterfactual) must inherit from this class
and implement the explain() method.
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize the explainer.

    Args:
        config: Configuration dictionary for the explainer
    """
    self.config = config or {}
    self.name = self.__class__.__name__.lower()
    logger.info(f"Initialized {self.__class__.__name__} with config: {self.config}")
```

**Public Methods:**

- `def get_supported_models(self) -> list[str]`
- `def get_name(self) -> str`
- `def get_version(self) -> str`
- `def validate_instance(self, instance`
- `def format_feature_description(self, feature_name`

---

### `ExplanationCache`

**File:** `base.py`

```python
class ExplanationCache:
```

**Description:**
```
"""Simple in-memory cache for explanations.

Caches explanations for identical decisions to reduce latency.
"""

def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
    """Initialize the cache.

    Args:
        max_size: Maximum number of cached explanations
        ttl_seconds: Time-to-live for cached explanations in seconds
    """
    self._cache: dict[str, tuple[ExplanationResult, float]] = {}
    self.max_size = max_size
    self.ttl_seconds = ttl_seconds
    logger.info(f"ExplanationCache initialized: max_size={max_size}, ttl={ttl_seconds}s")
```

**Public Methods:**

- `def get(self, cache_key`
- `def set(self, cache_key`
- `def generate_key(`
- `def clear(self)`
- `def get_stats(self) -> dict[str, Any]`

---

### `ExplanationException`

**File:** `base.py`

```python
class ExplanationException(Exception):
```

**Description:**
```
"""Base exception for explanation errors."""

pass


class ModelNotSupportedException(ExplanationException):
"""Exception raised when a model type is not supported."""

def __init__(self, model_type: str, supported_types: list[str]):
    self.model_type = model_type
    self.supported_types = supported_types
    super().__init__(f"Model type '{model_type}' is not supported. Supported types: {', '.join(supported_types)}")


class ExplanationTimeoutException(ExplanationException):
"""Exception raised when explanation generation times out."""
```

**Public Methods:**


---

### `ModelNotSupportedException`

**File:** `base.py`

```python
class ModelNotSupportedException(ExplanationException):
```

**Description:**
```
"""Exception raised when a model type is not supported."""

def __init__(self, model_type: str, supported_types: list[str]):
    self.model_type = model_type
    self.supported_types = supported_types
    super().__init__(f"Model type '{model_type}' is not supported. Supported types: {', '.join(supported_types)}")


class ExplanationTimeoutException(ExplanationException):
"""Exception raised when explanation generation times out."""

def __init__(self, timeout_seconds: int):
    self.timeout_seconds = timeout_seconds
    super().__init__(f"Explanation generation exceeded timeout of {timeout_seconds} seconds")
```

**Public Methods:**


---

### `ExplanationTimeoutException`

**File:** `base.py`

```python
class ExplanationTimeoutException(ExplanationException):
```

**Description:**
```
"""Exception raised when explanation generation times out."""

def __init__(self, timeout_seconds: int):
    self.timeout_seconds = timeout_seconds
    super().__init__(f"Explanation generation exceeded timeout of {timeout_seconds} seconds")
```

**Public Methods:**


---

### `CounterfactualConfig`

**File:** `counterfactual.py`

```python
class CounterfactualConfig:
```

**Description:**
```
"""Configuration for counterfactual generation.

Attributes:
    desired_outcome: Desired prediction outcome
    max_iterations: Maximum optimization iterations
    num_candidates: Number of candidates to generate
    proximity_weight: Weight for proximity objective
    sparsity_weight: Weight for sparsity objective (prefer fewer changes)
    validity_weight: Weight for validity objective (valid cybersec values)
"""

desired_outcome: Any | None = None
max_iterations: int = 1000
num_candidates: int = 10
proximity_weight: float = 1.0
sparsity_weight: float = 0.5
```

**Public Methods:**


---

### `CounterfactualGenerator`

**File:** `counterfactual.py`

```python
class CounterfactualGenerator(ExplainerBase):
```

**Description:**
```
"""Generate counterfactual explanations for cybersecurity predictions.

Generates minimal modifications to instances that would flip the prediction,
helping operators understand decision boundaries and actionable interventions.
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize CounterfactualGenerator.

    Args:
        config: Configuration dictionary with counterfactual settings
    """
    super().__init__(config)

    # Use self.config from base class (guaranteed to be dict, not None)
    cfg = self.config
```

**Public Methods:**

- `def get_supported_models(self) -> list[str]`

---

### `EngineConfig`

**File:** `engine.py`

```python
class EngineConfig:
```

**Description:**
```
"""Configuration for Explanation Engine.

Attributes:
    enable_cache: Whether to enable explanation caching
    cache_ttl_seconds: Cache TTL in seconds
    enable_tracking: Whether to track feature importances
    default_explanation_type: Default explanation type
    timeout_seconds: Timeout for explanation generation
    auto_select_explainer: Auto-select best explainer for model
"""

enable_cache: bool = True
cache_ttl_seconds: int = 3600
enable_tracking: bool = True
default_explanation_type: ExplanationType = ExplanationType.LIME
timeout_seconds: int = 30
```

**Public Methods:**


---

### `ExplanationEngine`

**File:** `engine.py`

```python
class ExplanationEngine:
```

**Description:**
```
"""Unified explanation engine for VÉRTICE platform.

This is the main entry point for all XAI functionality, providing
a simple interface for generating explanations across different models.
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize ExplanationEngine.

    Args:
        config: Configuration dictionary
    """
    config = config or {}

    # Engine configuration
    self.config = EngineConfig(
```

**Public Methods:**

- `def get_statistics(self) -> dict[str, Any]`
- `def get_top_features(self, n`
- `def detect_drift(`
- `def clear_cache(self)`
- `def export_tracker_data(self) -> dict[str, Any]`

---

### `DummyModel`

**File:** `engine.py`

```python
class DummyModel:
```

**Description:**
```
"""Dummy model for testing."""

def predict_proba(self, X):
    """Dummy predict_proba."""
    import numpy as np

    return np.array([[0.5, 0.5]])

def predict(self, X):
    """Dummy predict."""
    import numpy as np

    return np.array([0.5])


# Global singleton instance (optional)
```

**Public Methods:**

- `def predict_proba(self, X)`
- `def predict(self, X)`

---

### `FeatureHistory`

**File:** `feature_tracker.py`

```python
class FeatureHistory:
```

**Description:**
```
"""Historical tracking of a single feature.

Attributes:
    feature_name: Name of the feature
    importances: List of importance values over time
    timestamps: List of timestamps
    mean_importance: Mean importance
    std_importance: Standard deviation of importance
    trend: Trend direction ('increasing', 'decreasing', 'stable')
"""

feature_name: str
importances: list[float] = field(default_factory=list)
timestamps: list[datetime] = field(default_factory=list)
mean_importance: float = 0.0
std_importance: float = 0.0
```

**Public Methods:**

- `def add_observation(self, importance`
- `def get_recent_importances(self, hours`

---

### `FeatureImportanceTracker`

**File:** `feature_tracker.py`

```python
class FeatureImportanceTracker:
```

**Description:**
```
"""Track feature importance over time for drift detection and analysis."""

def __init__(self, max_history: int = 10000):
    """Initialize FeatureImportanceTracker.

    Args:
        max_history: Maximum number of observations to keep per feature
    """
    self.max_history = max_history

    # Feature histories
    self.feature_histories: dict[str, FeatureHistory] = {}

    # Global statistics
    self.total_explanations: int = 0
    self.start_time: datetime = datetime.utcnow()
```

**Public Methods:**

- `def track_explanation(self, features`
- `def get_top_features(self, n`
- `def detect_drift(self, feature_name`
- `def detect_global_drift(self, top_n`
- `def get_feature_trend(self, feature_name`
- `def get_statistics(self) -> dict[str, Any]`
- `def export_to_dict(self) -> dict[str, Any]`
- `def clear_old_data(self, days`

---

### `PerturbationConfig`

**File:** `lime_cybersec.py`

```python
class PerturbationConfig:
```

**Description:**
```
"""Configuration for feature perturbation.

Attributes:
    num_samples: Number of perturbed samples to generate
    feature_selection: Method for feature selection ('auto', 'lasso', 'forward_selection')
    kernel_width: Width of the exponential kernel
    sample_around_instance: Whether to sample around the instance
"""

num_samples: int = 5000
feature_selection: str = "auto"
kernel_width: float = 0.25
sample_around_instance: bool = True


class CyberSecLIME(ExplainerBase):
```

**Public Methods:**


---

### `CyberSecLIME`

**File:** `lime_cybersec.py`

```python
class CyberSecLIME(ExplainerBase):
```

**Description:**
```
"""LIME explainer adapted for cybersecurity models.

Supports:
    - Network traffic classification
    - Threat scoring models
    - Behavioral anomaly detection
    - Narrative manipulation detection
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize CyberSecLIME.

    Args:
        config: Configuration dictionary with perturbation settings
    """
    super().__init__(config)
```

**Public Methods:**

- `def get_supported_models(self) -> list[str]`

---

### `SHAPConfig`

**File:** `shap_cybersec.py`

```python
class SHAPConfig:
```

**Description:**
```
"""Configuration for SHAP explainer.

Attributes:
    algorithm: SHAP algorithm ('kernel', 'tree', 'deep', 'linear')
    num_background_samples: Number of background samples for kernel SHAP
    num_features: Number of top features to compute (None = all)
    check_additivity: Whether to check that SHAP values sum to prediction
"""

algorithm: str = "kernel"
num_background_samples: int = 100
num_features: int | None = None
check_additivity: bool = False


class CyberSecSHAP(ExplainerBase):
```

**Public Methods:**


---

### `CyberSecSHAP`

**File:** `shap_cybersec.py`

```python
class CyberSecSHAP(ExplainerBase):
```

**Description:**
```
"""SHAP explainer adapted for cybersecurity models.

Supports:
    - Tree-based models (XGBoost, LightGBM, Random Forest)
    - Neural networks (PyTorch, TensorFlow)
    - Linear models (Logistic Regression, SVM)
    - Model-agnostic kernel SHAP for any model
"""

def __init__(self, config: dict[str, Any] | None = None):
    """Initialize CyberSecSHAP.

    Args:
        config: Configuration dictionary with SHAP settings
    """
    super().__init__(config)
```

**Public Methods:**

- `def get_supported_models(self) -> list[str]`
- `def set_background_data(self, background_data`

---

### `DummyThreatClassifier`

**File:** `test_xai.py`

```python
class DummyThreatClassifier:
```

**Description:**
```
"""Dummy threat classifier for testing."""

def __init__(self):
    # Simple linear classifier: threat_score * 0.8 + anomaly_score * 0.2
    self.coef_ = np.array([0.8, 0.2, 0.1, 0.1])  # coefficients
    self.feature_importances_ = np.array([0.4, 0.3, 0.2, 0.1])  # for tree SHAP

def predict_proba(self, X):
    """Predict threat probability."""
    # Simple linear combination
    scores = X.dot(self.coef_)
    # Sigmoid to [0, 1]
    proba = 1 / (1 + np.exp(-scores))
    return np.column_stack([1 - proba, proba])

def predict(self, X):
```

**Public Methods:**

- `def predict_proba(self, X)`
- `def predict(self, X)`

---

## 4. Data Models

_No data models found_

## 5. Configuration

## 6. Dependencies

### Internal Services

- `services.maximus_core_service.justice.cbr_engine`
- `services.maximus_core_service.justice.embeddings`
- `services.maximus_core_service.justice.precedent_database`
- `services.maximus_core_service.justice.validators`

### External Libraries
```txt
aiohappyeyeballs==2.6.1
    # via aiohttp
aiohttp==3.13.0
    # via maximus-core-service (pyproject.toml)
aiosignal==1.4.0
    # via aiohttp
aiosqlite==0.21.0
    # via maximus-core-service (pyproject.toml)
annotated-types==0.7.0
    # via pydantic
anthropic==0.69.0
    # via maximus-core-service (pyproject.toml)
anyio==4.11.0
    # via
    #   anthropic
    #   httpx
    #   openai
    #   starlette
    #   watchfiles
asyncpg==0.30.0
    # via maximus-core-service (pyproject.toml)
attrs==25.4.0
    # via aiohttp
cachetools==6.2.0
    # via google-auth
certifi==2025.10.5
    # via
    #   httpcore
    #   httpx
    #   kubernetes
    #   requests
charset-normalizer==3.4.3
    # via requests
click==8.3.0
    # via uvicorn
cloudpickle==3.1.1
    # via
    #   gymnasium
    #   stable-baselines3
contourpy==1.3.3
    # via matplotlib
cycler==0.12.1
    # via matplotlib
distro==1.9.0
    # via
    #   anthropic
    #   openai
docker==7.1.0
    # via maximus-core-service (pyproject.toml)
docstring-parser==0.17.0
```

