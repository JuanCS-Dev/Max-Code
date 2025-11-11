# FASE 2.1: TUI ↔ BACKEND INTEGRATION - ENDPOINT MAPPING
**Max-Code CLI + MAXIMUS AI Backend**
**Generated**: 2025-11-10 23:06 UTC
**Methodology**: Padrão Pagani - Zero Technical Debt

---

## 🎯 EXECUTIVE SUMMARY

**Backend Status**: 2/7 services operational
**Critical Finding**: Port configuration mismatch between TUI and Backend
**Air Gaps Identified**: 5 services unavailable, potential integration breaks

---

## 📊 SERVICE INVENTORY

### Active Services (2/7)

| Service | Port | Status | Health Check | Components |
|---------|------|--------|--------------|------------|
| **MAXIMUS Core** | 8100 | ✅ UP | `/health` | Consciousness, TIG Fabric, ESGT Coordinator, Prefrontal Cortex, ToM Engine, Decision Queue |
| **PENELOPE** | 8154 | ✅ UP | `/health` | Sophia Engine, Praotes Validator, Tapeinophrosyne Monitor, Wisdom Base, Observability Client |

### Inactive Services (5/7)

| Service | Expected Port (Config) | Status | Impact |
|---------|----------------------|--------|--------|
| **NIS** (Narrative Intelligence) | 8152 | ❌ DOWN | Medium - Story generation unavailable |
| **MABA** (Browser Assistant) | 8151 | ❌ DOWN | Medium - Web search unavailable |
| **Orchestrator** | 8027 | ❌ DOWN | Medium - Workflow coordination unavailable |
| **Oraculo** | 8026 | ❌ DOWN | Low - Prediction service unavailable |
| **Atlas** | 8007 | ❌ DOWN | Low - Context service unavailable |

---

## 🚨 CRITICAL AIR GAP #1: PORT MISMATCH

### Problem Description
**Severity**: P0 - CRITICAL

The TUI client configuration has **hardcoded default ports** that do NOT match the actual backend deployment:

| Service | TUI Config (settings.py) | Actual Backend Port | Status |
|---------|-------------------------|-------------------|--------|
| **MAXIMUS Core** | 8153 | 8100 | ❌ MISMATCH |
| **PENELOPE** | 8150 | 8154 | ❌ MISMATCH |
| NIS | 8152 | N/A (down) | ⚠️ Unknown |
| MABA | 8151 | N/A (down) | ⚠️ Unknown |

**Impact**:
- TUI will attempt to connect to **wrong ports** (8153, 8150)
- Backend services on **correct ports** (8100, 8154) will be unreachable
- All MAXIMUS Core and PENELOPE features will FAIL silently
- Demo would have broken on first integration call

**Root Cause**:
```python
# config/settings.py:21-28
core_url: str = Field(
    default="http://localhost:8153",  # ❌ WRONG - Backend is on 8100
    env="MAXIMUS_CORE_URL",
)

penelope_url: str = Field(
    default="http://localhost:8150",  # ❌ WRONG - Backend is on 8154
    env="MAXIMUS_PENELOPE_URL",
)
```

**Solution Required**:
1. **IMMEDIATE**: Update `config/settings.py` defaults to match backend:
   - `core_url: default="http://localhost:8100"`
   - `penelope_url: default="http://localhost:8154"`
2. **VERIFY**: Test with environment variables override
3. **DOCUMENT**: Add README note about port configuration
4. **TEST**: Run E2E integration tests after fix

**Files Affected**:
- `config/settings.py` (lines 21-28)
- `config/profiles.py` (lines 42-43)
- All integration tests expecting old ports

---

## 🔌 MAXIMUS CLIENT SDK - ENDPOINT INVENTORY

### Client: `core/maximus_integration/client.py` (MaximusClient)

**Base URL**: http://localhost:8100 (CORRECTED from 8153)

| Method | Endpoint | HTTP | Purpose | Return Type |
|--------|----------|------|---------|-------------|
| `health_check()` | `/health` | GET | Check service availability | `bool` |
| `analyze_systemic_impact()` | `/api/v1/mape-k/analyze` | POST | MAPE-K systemic risk analysis | `SystemicAnalysis` |
| `ethical_review()` | `/api/v1/ethical/review` | POST | 4-framework ethical evaluation | `EthicalVerdict` |
| `predict_edge_cases()` | `/api/v1/predictive-coding/edge-cases` | POST | Predictive coding edge case detection | `List[EdgeCase]` |
| `heal_code()` | `/api/v1/penelope/heal` | POST | PENELOPE code healing suggestions | `HealingSuggestion` |
| `search_web()` | `/api/v1/maba/search` | POST | MABA web search | `MABASearchResult` |
| `generate_narrative()` | `/api/v1/nis/narrative` | POST | NIS story generation | `Narrative` |

**Request/Response Schemas**:

#### 1. Systemic Impact Analysis
```python
# Request
{
    "action": {"type": str, "file": str, "changes": str},
    "context": {"codebase": str, "dependencies": List[str]}
}

# Response (SystemicAnalysis)
{
    "systemic_risk_score": float,  # 0.0-1.0
    "side_effects": List[str],
    "mitigation_strategies": List[str],
    "affected_components": List[str],
    "confidence": float,
    "reasoning": str
}
```

#### 2. Ethical Review
```python
# Request
{
    "action": {"description": str, "context": str},
    "frameworks": List[EthicalFramework]  # ["kantian", "virtue", "consequentialist", "principlism"]
}

# Response (EthicalVerdict)
{
    "kantian_score": float,  # 0-100
    "virtue_score": float,
    "consequentialist_score": float,
    "principlism_score": float,
    "verdict": str,  # "APPROVED" | "REJECTED" | "CONDITIONAL"
    "reasoning": str,
    "issues": List[str],
    "recommendations": List[str]
}
```

#### 3. Edge Case Prediction
```python
# Request
{
    "code": str,
    "context": {"language": str, "framework": str}
}

# Response
List[EdgeCase]:
{
    "scenario": str,
    "probability": float,  # 0.0-1.0
    "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "suggested_test": str,
    "reasoning": str
}
```

#### 4. Code Healing (PENELOPE)
```python
# Request
{
    "code": str,
    "error": {"message": str, "stack_trace": str},
    "context": str
}

# Response (HealingSuggestion)
{
    "root_cause": str,
    "fix_suggestions": List[FixOption],
    "confidence": float,
    "analysis": str
}

# FixOption:
{
    "description": str,
    "code": str,
    "confidence": float,
    "side_effects": List[str]
}
```

#### 5. Web Search (MABA)
```python
# Request
{
    "query": str,
    "context": str,
    "max_results": int
}

# Response (MABASearchResult)
{
    "results": List[SearchResult],
    "confidence": float,
    "query_understanding": str
}

# SearchResult:
{
    "title": str,
    "url": str,
    "snippet": str,
    "relevance": float
}
```

#### 6. Narrative Generation (NIS)
```python
# Request
{
    "data": Dict[str, Any],
    "style": str,  # "technical", "executive", "story"
    "context": str
}

# Response (Narrative)
{
    "story": str,
    "key_insights": List[str],
    "visualization_data": Dict[str, Any],
    "confidence": float
}
```

---

## 🔄 CLIENT CONFIGURATION

### Retry Policy (Exponential Backoff)
```python
# config/settings.py:69-79
timeout_seconds: int = 30  # Default: 30s
max_retries: int = 3       # Default: 3 attempts
backoff_factor: float = 1.5  # Multiplier: 1.5x each retry
```

**Retry Timing**:
- Attempt 1: Immediate
- Attempt 2: 1.5s delay
- Attempt 3: 2.25s delay
- Total max time: 30s + (1.5s + 2.25s) = 33.75s

### Error Handling
```python
# Custom exceptions defined in client.py:
MaximusOfflineError    # Backend unreachable
MaximusTimeoutError    # Request exceeded timeout
MaximusAPIError        # Backend returned error (4xx, 5xx)
```

### Authentication
```python
# Optional OAuth token
auth_token: Optional[str] = os.getenv("CLAUDE_CODE_OAUTH_TOKEN")
# Sent as: Authorization: Bearer {token}
```

---

## 🧪 PENELOPE CLIENT - ENDPOINT INVENTORY

### Client: `core/maximus_integration/penelope_client.py` (PENELOPEClient)

**Base URL**: http://localhost:8154 (CORRECTED from 8150)

| Method | Endpoint | HTTP | Purpose | Return Type |
|--------|----------|------|---------|-------------|
| `health_check()` | `/health` | GET | Service health | `Dict` |
| `heal()` | `/heal` | POST | Code healing with 7 Fruits framework | `Dict` |
| `validate_virtues()` | `/validate` | POST | Virtue-based validation (Sophia, Praotes, Tapeinophrosyne) | `Dict` |

**Health Check Response** (Actual from Backend):
```json
{
  "status": "healthy",
  "components": {
    "sophia_engine": "ok",
    "praotes_validator": "ok",
    "tapeinophrosyne_monitor": "ok",
    "wisdom_base": "ok",
    "observability_client": "ok"
  },
  "virtues_status": {
    "sophia": "ok",
    "praotes": "ok",
    "tapeinophrosyne": "ok"
  },
  "sabbath_mode": false,
  "timestamp": "2025-11-10T23:05:51.510021+00:00"
}
```

---

## 🔍 NIS CLIENT - ENDPOINT INVENTORY (UNAVAILABLE)

### Client: `core/maximus_integration/nis_client.py` (NISClient)

**Base URL**: http://localhost:8152 (Expected)
**Status**: ❌ DOWN

| Method | Endpoint | HTTP | Purpose | Return Type |
|--------|----------|------|---------|-------------|
| `health_check()` | `/health` | GET | Service health | `Dict` |
| `generate_narrative()` | `/narrative` | POST | Story generation | `Dict` |

**Impact**: Narrative generation features unavailable in TUI.

---

## 🌐 MABA CLIENT - ENDPOINT INVENTORY (UNAVAILABLE)

### Client: `core/maximus_integration/maba_client.py` (MABAClient)

**Base URL**: http://localhost:8151 (Expected)
**Status**: ❌ DOWN

| Method | Endpoint | HTTP | Purpose | Return Type |
|--------|----------|------|---------|-------------|
| `health_check()` | `/health` | GET | Service health | `Dict` |
| `search()` | `/search` | POST | Web search | `Dict` |
| `browse()` | `/browse` | POST | Automated browsing | `Dict` |

**Impact**: Web search and browser automation unavailable in TUI.

---

## 🔗 SHARED CLIENT - SERVICE REGISTRY

### Client: `core/maximus_integration/shared_client.py` (SharedClient)

**Purpose**: Unified client for multiple MAXIMUS services with service discovery.

**Supported Services**:
```python
class MaximusService(Enum):
    CORE = "core"
    PENELOPE = "penelope"
    NIS = "nis"
    MABA = "maba"
    EUREKA = "eureka"  # Service registry (port 8151)
```

**Service Discovery**: Attempts to query Eureka registry at http://localhost:8151 for dynamic service URLs.

**Air Gap**: Eureka registry unavailable → service discovery disabled → falls back to static configuration.

---

## 🚦 INTEGRATION HEALTH MATRIX

### Request Flow Validation

| Feature | TUI Component | Backend Endpoint | Port | Status | Validated |
|---------|---------------|------------------|------|--------|-----------|
| Systemic Analysis | Task Decomposition | `/api/v1/mape-k/analyze` | 8100 | ⚠️ Port mismatch | ❌ NO |
| Ethical Review | Confirmation Dialog | `/api/v1/ethical/review` | 8100 | ⚠️ Port mismatch | ❌ NO |
| Edge Cases | Plan Preview | `/api/v1/predictive-coding/edge-cases` | 8100 | ⚠️ Port mismatch | ❌ NO |
| Code Healing | Error Handler | `/api/v1/penelope/heal` | 8154 | ⚠️ Port mismatch | ❌ NO |
| Web Search | Research Agent | `/api/v1/maba/search` | 8151 | ❌ Service down | ❌ NO |
| Narrative Gen | Docs Generator | `/api/v1/nis/narrative` | 8152 | ❌ Service down | ❌ NO |

**Validation Status**: 0/6 features validated with real backend.

---

## 🐛 AIR GAPS IDENTIFIED

### P0 - CRITICAL (Blocks all integration)

1. **Port Mismatch - MAXIMUS Core**
   - Config: 8153 → Actual: 8100
   - Files: `config/settings.py:21`, `config/profiles.py:42`
   - Impact: All Core features fail (systemic analysis, ethical review, edge cases)

2. **Port Mismatch - PENELOPE**
   - Config: 8150 → Actual: 8154
   - Files: `config/settings.py:28`, `config/profiles.py:43`
   - Impact: Code healing fails

### P1 - HIGH (Missing features)

3. **NIS Service Unavailable**
   - Expected: http://localhost:8152
   - Impact: Narrative generation unavailable

4. **MABA Service Unavailable**
   - Expected: http://localhost:8151
   - Impact: Web search and browser automation unavailable

5. **Service Discovery Disabled**
   - Eureka registry (8151) unreachable
   - Impact: Static configuration only, no dynamic service discovery

### P2 - MEDIUM (Operational concerns)

6. **No Endpoint Version Validation**
   - API paths hardcoded (`/api/v1/...`)
   - Risk: Breaking changes if backend updates to v2
   - Recommendation: Add version negotiation

7. **No Circuit Breaker Implementation**
   - Client has retry logic but no circuit breaker
   - Risk: Cascading failures if backend degrades
   - Recommendation: Implement circuit breaker pattern

8. **Missing Request/Response Logging**
   - No structured logging of API calls
   - Impact: Difficult to debug integration issues
   - Recommendation: Add request/response logging middleware

---

## 📋 VALIDATION CHECKLIST (Post-Fix)

After fixing P0 issues, validate:

- [ ] TUI can connect to MAXIMUS Core (8100)
- [ ] TUI can connect to PENELOPE (8154)
- [ ] Health checks return 200 OK
- [ ] Systemic analysis request succeeds
- [ ] Ethical review request succeeds
- [ ] Edge case prediction succeeds
- [ ] Code healing request succeeds
- [ ] Timeout handling works (simulate slow backend)
- [ ] Retry logic works (simulate transient failure)
- [ ] Error messages are user-friendly
- [ ] Graceful degradation when services down
- [ ] Performance: p95 latency <100ms

---

## 🎯 NEXT STEPS (PHASE 2.2)

1. **Fix P0 Issues**:
   - Update `config/settings.py` defaults
   - Update `config/profiles.py` defaults
   - Test with environment variable overrides

2. **E2E Integration Tests**:
   - Write tests for each endpoint
   - Test with real backend (8100, 8154)
   - Validate request/response schemas
   - Measure latency (p95, p99)

3. **Air Gap Resolution**:
   - Document NIS/MABA unavailability
   - Implement graceful degradation UI
   - Add "Feature unavailable" messages

4. **Performance Baseline**:
   - Measure current latency
   - Set SLA targets (p95 <100ms)
   - Optimize slow endpoints

---

**Generated**: 2025-11-10 23:06 UTC
**Status**: PHASE 2.1 COMPLETE - P0 Air Gaps Identified
**Next**: PHASE 2.2 - E2E Integration Testing

**Soli Deo Gloria** 🙏
