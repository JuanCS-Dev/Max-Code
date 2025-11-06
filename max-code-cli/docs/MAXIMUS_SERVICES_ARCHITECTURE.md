# MAXIMUS AI Services Architecture

**Date**: 2025-11-06
**Status**: Production Architecture Mapped
**Purpose**: Integration guide for max-code-cli

---

## 🏗️ Service Portfolio

| Service | Port | Purpose | Tech Stack |
|---------|------|---------|------------|
| **maximus-core** | 8150 | Consciousness, ESGT, Safety | FastAPI, PostgreSQL, Redis |
| **penelope** | 8151 | 7 Fruits, Healing, Wisdom | FastAPI, PostgreSQL, Redis |
| **maba** | 8152 | Memory, Knowledge Graph | FastAPI, Neo4j, PostgreSQL |
| **nis** | 8153 | NLP, Cost Tracking | FastAPI, Redis, Prometheus |
| **orchestrator** | 8154 | Workflow Coordination | FastAPI |
| **eureka** | 8155 | Service Discovery | FastAPI |
| **oraculo** | 8156 | Predictions, Forecasting | FastAPI, Gemini API |
| **dlq-monitor** | 8157 | Dead Letter Queue | FastAPI |

---

## 📡 MAXIMUS Core API (Port 8150)

### Consciousness Endpoints

```
GET    /api/v1/consciousness/state                    # Get consciousness state
POST   /api/v1/consciousness/esgt/trigger             # Trigger ESGT ignition
GET    /api/v1/consciousness/esgt/events              # List ESGT events
GET    /api/v1/consciousness/arousal                  # Get arousal state
POST   /api/v1/consciousness/arousal/adjust           # Adjust arousal level
GET    /api/v1/consciousness/metrics                  # Prometheus metrics
GET    /api/v1/consciousness/stream/sse               # SSE stream
WS     /api/v1/consciousness/ws                       # WebSocket stream
```

### Safety Protocol (FASE VII)

```
GET    /api/v1/consciousness/safety/status            # Safety status
GET    /api/v1/consciousness/safety/violations        # List violations
POST   /api/v1/consciousness/safety/emergency-shutdown  # Kill switch
```

### Reactive Fabric

```
GET    /api/v1/consciousness/reactive-fabric/metrics       # Fabric metrics
GET    /api/v1/consciousness/reactive-fabric/events        # Fabric events
GET    /api/v1/consciousness/reactive-fabric/orchestration # Orchestration status
```

### Response Models

```python
class ConsciousnessStateResponse(BaseModel):
    timestamp: str
    esgt_active: bool
    arousal_level: float
    arousal_classification: str
    tig_metrics: dict
    recent_events_count: int
    system_health: str

class SalienceInput(BaseModel):
    novelty: float  # [0-1]
    relevance: float  # [0-1]
    urgency: float  # [0-1]
    context: dict

class ArousalAdjustment(BaseModel):
    delta: float  # [-0.5, +0.5]
    duration_seconds: float  # [0.1, 60.0]
    source: str
```

---

## 🍇 Penelope API (Port 8151)

### 7 Fruits of the Spirit

```
GET    /api/v1/fruits/status                          # Fruits evaluation status
GET    /api/v1/virtues/metrics                        # Virtues metrics
```

### Healing System

```
GET    /api/v1/healing/history                        # Healing history
POST   /api/v1/diagnose                               # Diagnose anomaly
GET    /api/v1/patches                                # List patches
```

### Wisdom Base

```
GET    /api/v1/wisdom                                 # Query wisdom base
```

### Audio (NOT IMPLEMENTED)

```
POST   /api/v1/audio/synthesize                       # Synthesize audio (501)
```

---

## 🔮 Oraculo API (Port 8156)

### Predictions

```
GET    /health                                        # Health check
GET    /capabilities                                  # Service capabilities
POST   /predict                                       # Get prediction
POST   /analyze_code                                  # Analyze code
POST   /auto_implement                                # Auto-implement code
```

### Request Models

```python
class PredictionRequest(BaseModel):
    context: dict
    horizon: int  # Prediction horizon

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    context: Optional[dict]
```

---

## 🎭 Orchestrator API (Port 8154)

### Workflow Coordination

```
GET    /health                                        # Health check
POST   /workflow/create                               # Create workflow
GET    /workflow/{id}/status                          # Workflow status
POST   /workflow/{id}/execute                         # Execute workflow
```

---

## 📚 MABA API (Port 8152)

### Memory & Knowledge Graph

```
GET    /health                                        # Health check
POST   /memory/store                                  # Store memory
GET    /memory/retrieve                               # Retrieve memory
POST   /graph/query                                   # Query knowledge graph
```

---

## 🧠 NIS API (Port 8153)

### NLP & Cost Tracking

```
GET    /health                                        # Health check
POST   /nlp/analyze                                   # Analyze text
GET    /cost/metrics                                  # Cost metrics
GET    /cache/stats                                   # Cache statistics
```

---

## 🔍 Eureka API (Port 8155)

### Service Discovery

```
GET    /health                                        # Health check
GET    /services                                      # List services
POST   /register                                      # Register service
DELETE /unregister/{service_id}                       # Unregister service
```

---

## 🏥 Infrastructure

### PostgreSQL (Port 5432)
- User: `maximus`
- Database: `maximus`
- Used by: core, penelope, maba

### Redis (Port 6379)
- Cache layer
- Used by: all services

### Neo4j (Port 7687/7474)
- Knowledge graph
- Used by: maba

### Prometheus (Port 9090)
- Metrics collection
- Used by: all services

### Grafana (Port 3000)
- Dashboards
- User: `admin` (default)

---

## 🔐 Authentication

All services use:
- `ANTHROPIC_API_KEY` for Claude API
- `GEMINI_API_KEY` for Oraculo (Gemini)
- Internal service-to-service: no auth (trusted network)

---

## 🚀 Client Implementation Strategy

### 1. BaseHTTPClient
- httpx (async + HTTP/2)
- Circuit breaker (5 failures → 30s open)
- Retry logic (3 attempts, exponential backoff)
- Timeout: 5s connect, 30s read

### 2. Service Clients
- MaximusClient → maximus-core:8150
- PenelopeClient → penelope:8151
- OraculoClient → oraculo:8156
- OrchestratorClient → orchestrator:8154
- MABAClient → maba:8152
- NISClient → nis:8153
- EurekaClient → eureka:8155

### 3. Response Models
- Pydantic models matching API responses
- Type-safe validation
- Auto-documentation

---

## 📊 Health Check Protocol

All services expose `/health` endpoint:

```json
{
  "status": "healthy",
  "service": "maximus-core",
  "version": "1.0.0",
  "uptime": 12345,
  "dependencies": {
    "postgres": "connected",
    "redis": "connected"
  }
}
```

---

## 🎯 Integration Priorities

**Phase 1 (FASE 6):**
1. ✅ MaximusClient (Consciousness) - Core functionality
2. ✅ PenelopeClient (7 Fruits, Healing) - Ethics
3. ✅ OraculoClient (Predictions) - Foresight
4. ⏳ OrchestratorClient (Workflows) - Coordination
5. ⏳ MABAClient (Memory) - Context

**Phase 2 (FASE 7-8):**
- Health check system
- Integration with CLI commands
- E2E testing

---

**Architecture Source**: `/media/juan/DATA2/projects/MAXIMUS AI/docker-compose.yml`
**API Source**: Service directories under `services/*/api.py` or `api/routes.py`
