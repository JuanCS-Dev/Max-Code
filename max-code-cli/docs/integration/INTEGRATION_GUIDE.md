# MAX-CODE-CLI - Integration Guide

**Generated:** 2025-11-07 21:31:00

---

## Backend Services Integration

This guide documents all backend service integrations.

## Service Clients

### atlas

- **File:** `integration/atlas_client.py`
- **Lines:** 189

**Classes:**
- `AtlasClient`

**Methods:**
- `get_current_context()`
- `create_context()`
- `switch_context()`
- `update_context()`
- `get_environment_state()`
- `track_event()`
- `get_event_history()`
- `get_spatial_map()`
- `compute_distance()`
- `get_context_metrics()`

---

### base

- **File:** `integration/base_client.py`
- **Lines:** 105

**Classes:**

**Methods:**
- `state()`
- `call()`
- `get()`
- `post()`
- `close()`

---

### maximus

- **File:** `integration/maximus_client.py`
- **Lines:** 193

**Classes:**
- `ConsciousnessStateResponse`
- `SalienceInput`
- `ESGTEventResponse`
- `ArousalAdjustment`
- `SafetyStatusResponse`

**Methods:**
- `is_healthy()`
- `set_sabbath_mode()`
- `get_consciousness_state()`
- `trigger_esgt()`
- `get_esgt_events()`
- `adjust_arousal()`
- `get_safety_status()`

---

### oraculo

- **File:** `integration/oraculo_client.py`
- **Lines:** 326

**Classes:**
- `PredictionRequest`
- `CodeAnalysisRequest`
- `ImplementationRequest`
- `HealthStatusResponse`
- `CapabilitiesResponse`
- `PredictionResult`
- `PredictionResponse`
- `CodeAnalysisResult`
- `CodeAnalysisResponse`
- `ImplementationResult`
- `ImplementationResponse`

**Methods:**
- `is_healthy()`
- `get_health()`
- `get_capabilities()`
- `predict()`
- `analyze_code()`
- `auto_implement()`

---

### orchestrator

- **File:** `integration/orchestrator_client.py`
- **Lines:** 109

**Classes:**
- `OrchestrationRequest`
- `WorkflowStatus`

**Methods:**
- `health()`
- `orchestrate()`
- `get_workflow_status()`

---

### penelope

- **File:** `integration/penelope_client.py`
- **Lines:** 356

**Classes:**
- `FruitStatus`
- `FruitsStatusResponse`
- `VirtueMetrics`
- `VirtuesMetricsResponse`
- `HealingEvent`
- `HealingHistoryResponse`
- `DiagnoseRequest`
- `Precedent`
- `CausalChainStep`
- `DiagnoseResponse`
- `Patch`
- `PatchesResponse`
- `WisdomPrecedent`
- `WisdomBaseResponse`

**Methods:**
- `is_healthy()`
- `record_feedback()`
- `get_fruits_status()`
- `get_virtues_metrics()`
- `get_healing_history()`
- `diagnose_anomaly()`
- `get_patches()`
- `query_wisdom_base()`

---

