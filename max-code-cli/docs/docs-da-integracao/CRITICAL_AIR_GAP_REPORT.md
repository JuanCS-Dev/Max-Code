# 🚨 CRITICAL AIR GAP REPORT - TUI ↔ Backend API Mismatch
**Generated**: 2025-11-10 23:12 UTC
**Severity**: P0 - CRITICAL BLOCKER
**Impact**: 100% of TUI → Backend integration is BROKEN

---

## 🔴 EXECUTIVE SUMMARY

**STATUS**: CATASTROPHIC API MISMATCH

The Max-Code TUI client was developed against a **FICTITIOUS API SPECIFICATION** that does not match the **ACTUAL BACKEND IMPLEMENTATION**.

- **TUI expects**: `/api/v1/mape-k/*`, `/api/v1/ethical/*`, `/api/v1/predictive-coding/*`
- **Backend provides**: `/query`, `/api/consciousness/*`, `/api/v1/governance/*`

**Result**: Every single integration call from TUI to backend will return **404 Not Found**.

---

## 🔍 AIR GAP ANALYSIS

### P0-001: Port Configuration Mismatch
**Status**: ✅ FIXED

| Service | TUI Config (OLD) | Backend (ACTUAL) | Status |
|---------|------------------|------------------|--------|
| MAXIMUS Core | 8153 | 8100 | ✅ FIXED |
| PENELOPE | 8150 | 8154 | ✅ FIXED |

**Files Updated**:
- `config/settings.py:21` → Changed 8153 → 8100
- `config/settings.py:28` → Changed 8150 → 8154
- `config/profiles.py:42` → Changed 8150 → 8100

---

### P0-002: Complete API Path Mismatch
**Status**: ❌ NOT FIXED - REQUIRES MAJOR REFACTORING

#### TUI Client Expectations (`core/maximus_integration/client.py`)

| Method | Expected Endpoint | HTTP | Backend Status |
|--------|-------------------|------|----------------|
| `health_check()` | `/api/v1/health` | GET | ❌ 404 - Should be `/health` |
| `analyze_systemic_impact()` | `/api/v1/mape-k/analyze` | POST | ❌ 404 - DOES NOT EXIST |
| `ethical_review()` | `/api/v1/ethical/review` | POST | ❌ 404 - DOES NOT EXIST |
| `predict_edge_cases()` | `/api/v1/predictive-coding/edge-cases` | POST | ❌ 404 - DOES NOT EXIST |
| `heal_code()` | `/api/v1/penelope/heal` | POST | ❌ 404 - DOES NOT EXIST |
| `search_web()` | `/api/v1/maba/search` | POST | ❌ 404 - DOES NOT EXIST |
| `generate_narrative()` | `/api/v1/nis/narrative` | POST | ❌ 404 - DOES NOT EXIST |

**Total Endpoints in TUI Client**: 7
**Total Working**: 0 (0%)
**Total Broken**: 7 (100%)

#### Actual Backend API (MAXIMUS Core 8100)

**Available Endpoints** (from OpenAPI schema):
```
✅ /health                                      (Health check)
✅ /query                                       (Natural language query)
✅ /api/consciousness/state                     (Consciousness state)
✅ /api/consciousness/arousal                   (Arousal level)
✅ /api/consciousness/esgt/events               (ESGT events)
✅ /api/consciousness/esgt/trigger              (Trigger ESGT event)
✅ /api/consciousness/safety/status             (Safety status)
✅ /api/v1/governance/pending                   (HITL pending decisions)
✅ /api/v1/governance/decision/{id}/approve     (Approve decision)
✅ /api/v1/governance/decision/{id}/reject      (Reject decision)
✅ /api/v1/governance/stream/{operator_id}      (SSE governance events)
✅ /api/adw/*                                   (Adversarial Defense Warfare)
```

**Total Actual Endpoints**: 40+

**API Categories Available**:
1. **Consciousness API** - Arousal, ESGT, Safety, Reactive Fabric
2. **Governance API (HITL)** - Decision Queue, Approvals, Escalations
3. **ADW API** - Offensive/Defensive/Purple Team Workflows
4. **Query API** - Natural language query processing

**API Categories MISSING (that TUI expects)**:
1. **MAPE-K API** - Systemic impact analysis ❌
2. **Ethical API** - Multi-framework ethical review ❌
3. **Predictive Coding API** - Edge case prediction ❌
4. **PENELOPE API** - Code healing ❌ (PENELOPE is separate service)
5. **MABA API** - Web search ❌ (MABA is separate service, DOWN)
6. **NIS API** - Narrative generation ❌ (NIS is separate service, DOWN)

---

## 📊 IMPACT ASSESSMENT

### Features BROKEN in TUI

| Feature | TUI Component | Backend Endpoint Expected | Actual Status |
|---------|---------------|---------------------------|---------------|
| **Systemic Analysis** | Task Decomposition | `/api/v1/mape-k/analyze` | ❌ 404 Not Found |
| **Ethical Review** | Confirmation Dialog | `/api/v1/ethical/review` | ❌ 404 Not Found |
| **Edge Case Prediction** | Plan Preview | `/api/v1/predictive-coding/edge-cases` | ❌ 404 Not Found |
| **Code Healing** | Error Handler | `/api/v1/penelope/heal` | ❌ 404 (Wrong service) |
| **Web Search** | Research Agent | `/api/v1/maba/search` | ❌ Service DOWN |
| **Narrative Generation** | Docs Generator | `/api/v1/nis/narrative` | ❌ Service DOWN |

**Total Features**: 6
**Working**: 0 (0%)
**Broken**: 6 (100%)

### User Impact

**Before Fix**:
- User launches TUI: ✅ Works
- User runs `/health` command: ❌ FAILS (wrong endpoint path)
- User tries to analyze code: ❌ FAILS (endpoint doesn't exist)
- User tries ethical review: ❌ FAILS (endpoint doesn't exist)
- User tries edge case detection: ❌ FAILS (endpoint doesn't exist)

**Result**: TUI is a **BEAUTIFUL NON-FUNCTIONAL UI** - looks great, does nothing.

---

## 🔍 ROOT CAUSE ANALYSIS (5 WHYS)

**Problem**: TUI client calls endpoints that don't exist on backend.

1. **Why?** TUI was developed with hardcoded API paths (`/api/v1/mape-k/*`, etc.)
2. **Why?** No OpenAPI schema was consumed during TUI development
3. **Why?** Backend API wasn't finalized when TUI was built
4. **Why?** Development happened in parallel without integration contract
5. **Why?** No API design-first approach or contract testing

**Root Cause**: **Lack of API contract validation** between frontend (TUI) and backend.

---

## 🛠️ SOLUTION OPTIONS

### Option 1: Update TUI Client to Match Backend API (RECOMMENDED)
**Effort**: HIGH (4-6 hours)
**Risk**: LOW
**Impact**: Complete refactoring of integration layer

**Steps**:
1. Download OpenAPI schema: `http://localhost:8100/openapi.json`
2. Generate client stubs from schema (OpenAPI Generator)
3. Refactor `core/maximus_integration/client.py` to use ACTUAL endpoints:
   - Replace `/api/v1/health` → `/health`
   - Replace MAPE-K/Ethical/Predictive calls → Use `/query` with appropriate prompts
   - Add Consciousness API calls (`/api/consciousness/*`)
   - Add Governance API calls (`/api/v1/governance/*`)
4. Update all callers in TUI
5. Write integration tests against REAL backend
6. Validate E2E workflows

**Pros**:
- TUI works with actual backend
- Uses real Consciousness & Governance features
- Extensible for future API additions

**Cons**:
- Requires significant refactoring
- May need to redesign some TUI features
- MAPE-K/Ethical/Predictive features unavailable (need to implement in backend OR remove from TUI)

---

### Option 2: Implement Missing Endpoints in Backend
**Effort**: VERY HIGH (10-15 hours)
**Risk**: HIGH
**Impact**: Backend must implement features TUI expects

**Steps**:
1. Implement `/api/v1/mape-k/analyze` in backend
2. Implement `/api/v1/ethical/review` in backend
3. Implement `/api/v1/predictive-coding/edge-cases` in backend
4. Update PENELOPE to expose `/api/v1/penelope/heal`
5. Start NIS/MABA services and expose expected endpoints

**Pros**:
- TUI client requires no changes
- Backend gains new features

**Cons**:
- Very high effort
- Backend may already have equivalent features under different paths
- Duplicates functionality

---

### Option 3: Adapter/Proxy Layer (HYBRID)
**Effort**: MEDIUM (3-4 hours)
**Risk**: MEDIUM
**Impact**: Create adapter that maps TUI calls to backend endpoints

**Steps**:
1. Create FastAPI adapter service (port 8200)
2. Adapter receives TUI calls (`/api/v1/mape-k/*`)
3. Adapter translates to backend calls:
   - `/api/v1/mape-k/analyze` → `/query` with "analyze systemic impact of..."
   - `/api/v1/ethical/review` → `/query` with "perform ethical review of..."
4. TUI points to adapter (8200) instead of backend (8100)

**Pros**:
- No TUI changes needed
- No backend changes needed
- Flexible translation layer

**Cons**:
- Additional service to maintain
- Performance overhead (extra hop)
- Complexity

---

## 📝 RECOMMENDATION

**OPTION 1: Update TUI Client to Match Backend API**

**Rationale**:
1. Backend API is REAL and DEPLOYED
2. Backend has rich features (Consciousness, Governance, ADW)
3. TUI should adapt to backend, not vice-versa
4. Cleaner architecture (no adapter layer)
5. Opens TUI to use actual Consciousness/Governance features

**Implementation Plan**:

### Phase 1: Immediate Fixes (1 hour)
- [x] Fix port configuration (8100, 8154) ✅ DONE
- [ ] Fix health check endpoint: `/api/v1/health` → `/health`
- [ ] Test health checks work

### Phase 2: API Client Refactoring (3 hours)
- [ ] Download OpenAPI schema from backend
- [ ] Analyze available endpoints
- [ ] Map TUI features to available backend endpoints:
  - Systemic Analysis → Use `/query` with prompt
  - Ethical Review → Use `/query` with prompt
  - Edge Cases → Use `/query` with prompt
- [ ] Refactor `MaximusClient` class
- [ ] Update method signatures
- [ ] Update all callers in TUI

### Phase 3: New Feature Integration (2 hours)
- [ ] Add Consciousness API integration
  - `get_consciousness_state()` → `/api/consciousness/state`
  - `adjust_arousal()` → `/api/consciousness/arousal/adjust`
- [ ] Add Governance API integration
  - `get_pending_decisions()` → `/api/v1/governance/pending`
  - `approve_decision()` → `/api/v1/governance/decision/{id}/approve`
  - `stream_governance_events()` → `/api/v1/governance/stream/{operator_id}` (SSE)

### Phase 4: Testing & Validation (2 hours)
- [ ] Write integration tests for each endpoint
- [ ] Test with real backend
- [ ] Measure latency (p95, p99)
- [ ] Validate E2E workflows
- [ ] Update documentation

**Total Effort**: 8 hours
**Timeline**: 1 day of focused work

---

## 🔄 PENELOPE SERVICE ANALYSIS

**Port**: 8154
**Status**: ✅ UP
**OpenAPI**: Not analyzed yet

**Action Required**: Check PENELOPE OpenAPI schema to verify available endpoints.

```bash
curl http://localhost:8154/openapi.json | jq '.paths | keys'
```

---

## 📋 ACTION ITEMS (PRIORITIZED)

### P0 - IMMEDIATE (< 4 hours)
- [ ] **P0-002a**: Fix health check path in `MaximusClient`
  - File: `core/maximus_integration/client.py:320`
  - Change: `/api/v1/health` → `/health`
- [ ] **P0-002b**: Fix health check path in `PENELOPEClient`
  - File: `core/maximus_integration/penelope_client.py`
  - Verify: Check if PENELOPE uses `/health` or `/api/v1/health`
- [ ] **P0-002c**: Test health checks work with corrected paths
- [ ] **P0-002d**: Document actual backend API structure

### P1 - HIGH (1-2 days)
- [ ] **P1-001**: Refactor `analyze_systemic_impact()` to use `/query`
- [ ] **P1-002**: Refactor `ethical_review()` to use `/query`
- [ ] **P1-003**: Refactor `predict_edge_cases()` to use `/query`
- [ ] **P1-004**: Add Consciousness API methods
- [ ] **P1-005**: Add Governance API methods
- [ ] **P1-006**: Write integration tests for all endpoints

### P2 - MEDIUM (1 week)
- [ ] **P2-001**: Remove unused methods (if features don't exist in backend)
- [ ] **P2-002**: Update TUI components to use new API methods
- [ ] **P2-003**: Add SSE streaming for governance events
- [ ] **P2-004**: Performance optimization (reduce latency)

---

## 🎯 SUCCESS CRITERIA

**Phase 1 Complete** when:
- [ ] `client.health_check()` returns True with backend
- [ ] Latency p95 < 100ms
- [ ] No 404 errors

**Phase 2 Complete** when:
- [ ] All 7 methods in `MaximusClient` work OR are removed
- [ ] Integration tests pass with real backend
- [ ] Coverage: 100% of API calls tested

**Phase 3 Complete** when:
- [ ] TUI can use Consciousness API
- [ ] TUI can use Governance API (HITL)
- [ ] SSE streaming works

**Phase 4 Complete** when:
- [ ] E2E workflows validated
- [ ] Documentation updated
- [ ] Demo-ready

---

## 📚 APPENDIX

### Actual Backend Endpoints (MAXIMUS Core 8100)

#### Health & Query
- `GET /health` - Health check
- `POST /query` - Natural language query processing

#### Consciousness API
- `GET /api/consciousness/state` - Get consciousness state
- `GET /api/consciousness/arousal` - Get arousal level
- `POST /api/consciousness/arousal/adjust` - Adjust arousal
- `GET /api/consciousness/esgt/events` - Get ESGT events
- `POST /api/consciousness/esgt/trigger` - Trigger ESGT event
- `GET /api/consciousness/metrics` - Consciousness metrics
- `GET /api/consciousness/reactive-fabric/events` - Reactive fabric events
- `POST /api/consciousness/reactive-fabric/orchestration` - Orchestrate reactive fabric
- `GET /api/consciousness/safety/status` - Safety status
- `POST /api/consciousness/safety/emergency-shutdown` - Emergency shutdown
- `GET /api/consciousness/safety/violations` - Safety violations
- `GET /api/consciousness/stream/sse` - SSE stream

#### Governance API (HITL)
- `GET /api/v1/governance/health` - Governance health
- `GET /api/v1/governance/pending` - Get pending decisions
- `POST /api/v1/governance/session/create` - Create operator session
- `GET /api/v1/governance/session/{operator_id}/stats` - Session stats
- `GET /api/v1/governance/stream/{operator_id}` - SSE governance stream
- `GET /api/v1/governance/decision/{decision_id}` - Get decision
- `POST /api/v1/governance/decision/{decision_id}/approve` - Approve
- `POST /api/v1/governance/decision/{decision_id}/reject` - Reject
- `POST /api/v1/governance/decision/{decision_id}/escalate` - Escalate
- `POST /api/v1/governance/decision/{decision_id}/watch` - Watch decision
- `POST /api/v1/governance/test/enqueue` - Test: enqueue decision

#### ADW API (Adversarial Defense Warfare)
- `GET /api/adw/health` - ADW health
- `GET /api/adw/overview` - ADW overview
- `GET /api/adw/offensive/status` - Offensive status
- `GET /api/adw/offensive/campaigns` - List campaigns
- `POST /api/adw/offensive/campaign` - Create campaign
- `GET /api/adw/defensive/status` - Defensive status
- `GET /api/adw/defensive/threats` - List threats
- `POST /api/adw/defensive/coagulation` - Coagulation response
- `GET /api/adw/purple/metrics` - Purple team metrics
- `POST /api/adw/purple/cycle` - Run purple team cycle
- `POST /api/adw/workflows/target-profile` - Target profiling
- `POST /api/adw/workflows/credential-intel` - Credential intel
- `POST /api/adw/workflows/attack-surface` - Attack surface scan
- `GET /api/adw/workflows/{workflow_id}/status` - Workflow status
- `GET /api/adw/workflows/{workflow_id}/report` - Workflow report

---

**Generated**: 2025-11-10 23:12 UTC
**Status**: P0 AIR GAP DOCUMENTED - AWAITING FIX
**Next**: Implement Option 1 (Update TUI Client)

**Soli Deo Gloria** 🙏
