# MAXIMUS AI - Architecture as Core System

**Version:** 1.0.0
**Role:** Core Intelligence Engine for Max-Code CLI
**Architecture:** Modular, Event-Driven, Constitutional

---

## 🎯 Overview

**MAXIMUS AI** is designed as a **modular core intelligence system** that can power various applications. The first implementation is **Max-Code** - a personalized CLI tool similar to Claude Code, but with Maximus AI as its brain.

### Core Philosophy

```
Max-Code CLI (Interface)
    ↓
MAXIMUS AI (Core Intelligence)
    ↓
TRINITY + Services (Specialized Capabilities)
    ↓
Constitutional Framework (Governance)
```

---

## 🏗️ Architectural Layers

### Layer 1: Core Intelligence (Maximus Core)

**Location:** `services/core/`
**Port:** 8150
**Role:** Central consciousness and decision-making engine

#### Capabilities:
- **Consciousness System** - Artificial consciousness based on neuroscience
  - Predictive coding (5 hierarchical layers)
  - Neuromodulation (dopamine, acetilcolina, norepinefrina, serotonina)
  - Skill learning (hybrid Reinforcement Learning)

- **Ethical Validation** - Validates decisions against ethical framework

- **Governance Core** - Enforces Constitutional principles (P1-P6)

- **Human-in-the-Loop (HITL)** - Escalates critical decisions to human

#### API Endpoints:
```
POST /api/v1/consciousness/predict    - Predictive coding inference
POST /api/v1/consciousness/learn      - Skill learning
POST /api/v1/ethics/validate          - Ethical validation
POST /api/v1/governance/check         - Constitutional compliance
GET  /api/v1/health                   - Health check
GET  /api/v1/metrics                  - Prometheus metrics
```

#### Integration Pattern for Max-Code:
```python
from libs.maximus_client import MaximusCore

core = MaximusCore(base_url="http://localhost:8150")

# Decision making
decision = await core.consciousness.predict(
    context=current_context,
    task=user_task,
    constraints=constitutional_constraints
)

# Ethical validation
is_valid = await core.ethics.validate(decision)

# Governance check
compliance = await core.governance.check(decision)
```

---

### Layer 2: TRINITY Subordinates (Specialized Agents)

#### 2.1. PENELOPE - Christian Autonomous Healing

**Location:** `services/penelope/`
**Port:** 8151
**Role:** Self-healing and code correction with biblical governance

**Use Case in Max-Code:**
- Autonomous bug fixing
- Code quality improvement
- Self-healing failed operations

**Integration:**
```python
from libs.maximus_client import PENELOPE

penelope = PENELOPE(base_url="http://localhost:8151")

# Auto-fix code issues
patch = await penelope.heal(
    code=buggy_code,
    error=error_trace,
    severity="MODERATE"  # SURGICAL, MODERATE, DEFER_TO_HUMAN
)

# Wisdom Base lookup
similar_issues = await penelope.wisdom_base.query(error_signature)
```

**Biblical Governance:**
- **Sabbath:** No auto-fixes on Sundays
- **Humility:** Defers to human when uncertain
- **Wisdom:** Learns from historical fixes

---

#### 2.2. MABA - Browser Automation Agent

**Location:** `services/maba/`
**Port:** 8152
**Role:** Intelligent web automation with cognitive mapping

**Use Case in Max-Code:**
- Fetch documentation from websites
- Automated testing of web UIs
- Scraping reference implementations

**Integration:**
```python
from libs.maximus_client import MABA

maba = MABA(base_url="http://localhost:8152")

# Intelligent navigation
session = await maba.create_session()
await maba.navigate(session, "https://docs.anthropic.com")

# Extract information
docs = await maba.extract(
    session,
    selector="article",
    schema={"title": "string", "content": "string"}
)

# Cognitive map queries
structure = await maba.cognitive_map.query("anthropic docs structure")
```

**Cognitive Mapping:**
- Learns website structures
- Remembers successful navigation paths
- Adapts to UI changes

---

#### 2.3. NIS - Narrative Intelligence Service

**Location:** `services/nis/`
**Port:** 8153
**Role:** AI-powered narrative generation and anomaly detection

**Use Case in Max-Code:**
- Generate commit messages
- Summarize code changes
- Explain complex code behavior

**Integration:**
```python
from libs.maximus_client import NIS

nis = NIS(base_url="http://localhost:8153")

# Generate narrative
narrative = await nis.generate(
    narrative_type="commit_message",
    context={
        "files_changed": ["main.py", "utils.py"],
        "diff": git_diff,
        "tests": test_results
    }
)

# Anomaly detection
anomalies = await nis.detect_anomalies(
    metrics=code_metrics,
    baseline=project_baseline
)
```

**Caching:**
- 60-80% cost reduction via intelligent caching
- Redis-backed
- Budget tracking

---

### Layer 3: Additional Services

#### 3.1. Orchestrator (Port 8154)

**Role:** Coordinates multi-service workflows

**Use Case in Max-Code:**
- Complex multi-step operations
- Parallel task execution
- Workflow state management

```python
from libs.maximus_client import Orchestrator

orchestrator = Orchestrator(base_url="http://localhost:8154")

# Define workflow
workflow = await orchestrator.create_workflow([
    {"service": "maba", "action": "fetch_docs"},
    {"service": "nis", "action": "summarize"},
    {"service": "core", "action": "validate"}
])

# Execute
result = await orchestrator.execute(workflow)
```

---

#### 3.2. Eureka - Malware Analysis (Port 8155)

**Role:** Deep security analysis and threat detection

**Use Case in Max-Code:**
- Security scanning of dependencies
- Code vulnerability detection
- Threat intelligence

---

#### 3.3. Oráculo - Self-Improvement (Port 8156)

**Role:** Meta-cognitive optimization and self-improvement

**Use Case in Max-Code:**
- Suggest codebase improvements
- Learn from usage patterns
- Auto-optimize configurations

**Best-in-class:** Reference implementation for quality

---

#### 3.4. DLQ Monitor - Resilience (Port 8157)

**Role:** Dead Letter Queue monitoring for Kafka

**Use Case in Max-Code:**
- Retry failed operations
- Event queue management
- Resilience patterns

---

## 📡 Communication Patterns

### 1. Synchronous HTTP/REST

**For:** Direct queries, immediate responses

```python
response = await http_client.post(
    "http://localhost:8150/api/v1/consciousness/predict",
    json={"context": context, "task": task}
)
```

### 2. Asynchronous Events (Future)

**For:** Long-running operations, notifications

```python
# Subscribe to events
await event_bus.subscribe("maximus.task.completed", callback)

# Publish event
await event_bus.publish("maximus.task.started", task_data)
```

### 3. Streaming (Future)

**For:** Real-time updates, progressive results

```python
async for chunk in core.consciousness.predict_stream(context):
    display_progress(chunk)
```

---

## 🔐 Authentication & Authorization

### Development Mode
- No authentication required
- Localhost only

### Production Mode (Future)
- API Key authentication
- Role-based access control (RBAC)
- Rate limiting per client

```python
from libs.maximus_client import MaximusCore

core = MaximusCore(
    base_url="https://maximus.production.com",
    api_key=os.getenv("MAXIMUS_API_KEY")
)
```

---

## 📊 Observability

### Metrics (Prometheus)

All services export metrics on `/metrics`:

**Core Metrics:**
- `maximus_consciousness_predictions_total`
- `maximus_ethics_validations_total`
- `maximus_governance_checks_total`

**TRINITY Metrics:**
- `penelope_patches_generated_total`
- `maba_browser_actions_total`
- `nis_narratives_generated_total`

### Logs (Structured JSON)

All services use constitutional logging:

```json
{
  "timestamp": "2025-11-04T08:00:00Z",
  "service": "maximus-core",
  "level": "INFO",
  "principle": "P2_VALIDATION",
  "message": "API validation successful",
  "context": {...}
}
```

### Tracing (OpenTelemetry)

Distributed tracing across services:

```
Max-Code CLI
  └─> Maximus Core (span: consciousness.predict)
      └─> PENELOPE (span: wisdom_base.query)
      └─> NIS (span: narrative.generate)
```

---

## 🧩 Modular Design

### Principle: Loose Coupling, High Cohesion

Each service can operate independently with graceful degradation:

```python
# Service discovery with fallback
try:
    penelope = discover_service("penelope")
except ServiceNotFound:
    logger.warning("PENELOPE unavailable, using fallback")
    penelope = FallbackHealer()
```

### Principle: Configuration Over Code

Services configured via environment variables:

```bash
# Enable/disable services
ENABLE_PENELOPE=true
ENABLE_MABA=false
ENABLE_NIS=true

# Feature flags
PENELOPE_SABBATH_ENABLED=true
MABA_HEADLESS=true
NIS_CACHE_ENABLED=true
```

---

## 🎯 Max-Code Integration Strategy

### Phase 1: Core Integration (Week 1)

1. **Max-Code CLI skeleton**
   - Argument parsing
   - Command routing
   - Output formatting

2. **Maximus Core client library**
   ```python
   # libs/maximus_client/
   ├── __init__.py
   ├── core.py          # MaximusCore client
   ├── penelope.py      # PENELOPE client
   ├── maba.py          # MABA client
   ├── nis.py           # NIS client
   └── orchestrator.py  # Orchestrator client
   ```

3. **Basic commands**
   ```bash
   max-code ask "How do I implement X?"
   max-code fix bug.py
   max-code commit  # Auto-generate message
   ```

### Phase 2: TRINITY Integration (Week 2)

1. **PENELOPE for auto-fixing**
   ```bash
   max-code heal --auto
   ```

2. **MABA for documentation**
   ```bash
   max-code docs fetch anthropic
   ```

3. **NIS for narratives**
   ```bash
   max-code explain complex_function.py
   ```

### Phase 3: Advanced Features (Week 3-4)

1. **Orchestrator workflows**
   ```bash
   max-code workflow run refactor_pipeline.yaml
   ```

2. **Oráculo suggestions**
   ```bash
   max-code suggest --analyze-codebase
   ```

3. **Interactive mode**
   ```bash
   max-code interactive
   > ask: how to...
   > fix: this bug
   > commit
   ```

---

## 🏛️ Constitutional Governance

All operations governed by **CONSTITUIÇÃO VÉRTICE v3.0**:

### DETER-AGENT Framework (5 Layers)

1. **Constitutional** - Principles P1-P6
2. **Deliberation** - Tree of Thoughts + Auto-crítica
3. **State Management** - Context compression
4. **Execution** - Verify-Fix-Execute loop (max 2 iterations)
5. **Incentive** - Metrics: CRS≥95%, LEI<1.0, FPC≥80%

### Enforcement in Max-Code

```python
from libs.constitutional import ConstitutionalValidator

validator = ConstitutionalValidator()

# Before executing
validation = await validator.check(
    operation=user_command,
    principles=["P1", "P2", "P3"]  # Relevant principles
)

if not validation.compliant:
    raise ConstitutionalViolation(validation.reason)
```

---

## 📈 Scalability

### Horizontal Scaling

Services can scale independently:

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: maximus-core
spec:
  replicas: 3  # Scale to 3 instances
```

### Vertical Scaling

Resource allocation per service:

```yaml
resources:
  limits:
    memory: "2Gi"
    cpu: "1000m"
  requests:
    memory: "1Gi"
    cpu: "500m"
```

### Load Balancing

Round-robin across instances:

```
Max-Code CLI
    ↓
Load Balancer (nginx/haproxy)
    ↓
┌─────────┬─────────┬─────────┐
│ Core #1 │ Core #2 │ Core #3 │
└─────────┴─────────┴─────────┘
```

---

## 🔒 Security Considerations

### 1. API Security
- HTTPS in production
- API key rotation
- Rate limiting per client

### 2. Data Privacy
- No PII storage without consent
- Encrypted storage for sensitive data
- GDPR compliance

### 3. Code Execution
- Sandboxed execution (PENELOPE patches)
- Input validation (all services)
- Output sanitization

### 4. Network Security
- Services on isolated network
- Firewall rules
- VPN for remote access

---

## 📚 Development Guidelines for Max-Code

### 1. Client Library Design

```python
# Simple, intuitive API
from maximus import Core, PENELOPE, MABA, NIS

# Initialize
maximus = Core()

# Use services
result = await maximus.ask("How to implement X?")
await maximus.fix("bug.py")
await maximus.commit()
```

### 2. Error Handling

```python
from maximus.exceptions import (
    MaximusConnectionError,
    ConstitutionalViolation,
    ServiceUnavailable
)

try:
    result = await maximus.ask(question)
except ServiceUnavailable:
    # Graceful degradation
    result = fallback_handler(question)
except ConstitutionalViolation as e:
    # Inform user of violation
    print(f"Cannot proceed: {e.reason}")
```

### 3. Configuration

```yaml
# ~/.max-code/config.yaml
maximus:
  base_url: "http://localhost:8150"
  timeout: 30
  retry: 3

services:
  penelope:
    enabled: true
    sabbath_respect: true
  maba:
    enabled: true
    headless: true
  nis:
    enabled: true
    cache: true

cli:
  interactive_mode: true
  auto_commit: false
  verbose: true
```

---

## 🎓 Best Practices

### 1. Idempotency

All operations should be idempotent:

```python
# Multiple calls produce same result
result1 = await core.validate(code)
result2 = await core.validate(code)
assert result1 == result2
```

### 2. Timeout Handling

Always set reasonable timeouts:

```python
from maximus import Core

core = Core(timeout=30)  # 30 seconds

try:
    result = await asyncio.wait_for(
        core.predict(context),
        timeout=60
    )
except asyncio.TimeoutError:
    logger.error("Operation timed out")
```

### 3. Graceful Degradation

Handle service unavailability:

```python
try:
    result = await penelope.heal(code)
except ServiceUnavailable:
    # Fallback to simpler healing
    result = simple_fix(code)
```

---

## 📊 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Core response time (p95) | <500ms | TBD |
| PENELOPE patch generation | <5s | TBD |
| MABA page navigation | <3s | TBD |
| NIS narrative generation | <2s | TBD |
| Uptime | 99.9% | TBD |
| Concurrent requests | 1000/s | TBD |

---

## 🚀 Deployment Architectures

### Development (Local)

```
┌─────────────┐
│  Max-Code   │
│    CLI      │
└──────┬──────┘
       │
┌──────▼──────┐
│  Maximus AI │
│  (Docker)   │
└─────────────┘
```

### Production (Cloud)

```
┌─────────────┐
│  Max-Code   │
│    CLI      │
└──────┬──────┘
       │ HTTPS
┌──────▼───────────┐
│  Load Balancer   │
└──────┬───────────┘
       │
┌──────▼──────────────────────┐
│    Kubernetes Cluster       │
│  ┌─────┬─────┬─────┬─────┐ │
│  │Core │PENE │MABA │ NIS │ │
│  │  x3 │ x2  │ x2  │ x2  │ │
│  └─────┴─────┴─────┴─────┘ │
└─────────────────────────────┘
```

---

## 📖 Further Reading

- [CONSTITUIÇÃO VÉRTICE v3.0](../governance/CONSTITUTION_VERTICE_v3.0.md)
- [Service Documentation](../services/)
- [API Reference](../api/)
- [Max-Code Integration Guide](../guides/MAX_CODE_INTEGRATION.md)

---

**MAXIMUS AI: Modular Core Intelligence for Next-Generation Development Tools**

*"Powered by consciousness, guided by constitution, built for the future."*
