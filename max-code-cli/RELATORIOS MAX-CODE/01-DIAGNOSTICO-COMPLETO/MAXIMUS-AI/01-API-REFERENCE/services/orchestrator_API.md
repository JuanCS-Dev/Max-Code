# ORCHESTRATOR - API Reference

**Gerado:** 2025-11-07 20:46:00
**Método:** Análise automática do código fonte

---

## 1. Service Overview

### Statistics
- Python Files: 11
- Lines of Code: 2364
- Test Files: 3

### Entry Point
```
services/orchestrator/main.py
```

### Directory Structure
```
.
.scripts
.shared
.tests
```

---

## 2. API Endpoints

### `main.py` - Line 139
```python
@app.get("/health")
async def health_check() -> Dict[str, str]:
```

**Description:**
```
"""Performs a health check of the Orchestrator Service.

Returns:
    Dict[str, str]: A dictionary indicating the service status.
"""
return {"status": "healthy", "message": "Orchestrator Service is operational."}


@app.post("/orchestrate", response_model=WorkflowStatus)
```

### `main.py` - Line 149
```python
@app.post("/orchestrate", response_model=WorkflowStatus)
async def orchestrate_workflow(request: OrchestrationRequest) -> WorkflowStatus:
```

**Description:**
```
"""Initiates a complex workflow across multiple Maximus services.

Args:
    request (OrchestrationRequest): The request body containing workflow details.

Returns:
    WorkflowStatus: The initial status of the initiated workflow.
"""
workflow_id = str(uuid.uuid4())
```

### `main.py` - Line 176
```python
@app.get("/workflow/{workflow_id}/status", response_model=WorkflowStatus)
async def get_workflow_status(workflow_id: str) -> WorkflowStatus:
```

**Description:**
```
"""Retrieves the current status of a specific workflow.

Args:
    workflow_id (str): The ID of the workflow.

Returns:
    WorkflowStatus: The current status and details of the workflow.

Raises:
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

_No HTTP endpoints found_

## 3. Classes and Methods

### `OrchestrationRequest`

**File:** `main.py`

```python
class OrchestrationRequest(BaseModel):
```

**Description:**
```
"""Request model for initiating a complex orchestration workflow.

Attributes:
    workflow_name (str): The name of the workflow to execute (e.g., 'threat_hunting', 'system_optimization').
    parameters (Optional[Dict[str, Any]]): Parameters for the workflow.
    priority (int): The priority of the workflow (1-10, 10 being highest).
"""

workflow_name: str
parameters: Optional[Dict[str, Any]] = None
priority: int = 5


class WorkflowStatus(BaseModel):
"""Response model for workflow status.
```

**Public Methods:**


---

### `WorkflowStatus`

**File:** `main.py`

```python
class WorkflowStatus(BaseModel):
```

**Description:**
```
"""Response model for workflow status.

Attributes:
    workflow_id (str): Unique identifier for the workflow.
    status (str): Current status of the workflow (e.g., 'running', 'completed', 'failed').
    current_step (Optional[str]): The current step being executed.
    progress (float): Progress percentage (0.0 to 1.0).
    results (Optional[Dict[str, Any]]): Final results if completed.
    error (Optional[str]): Error message if failed.
"""

workflow_id: str
status: str
current_step: Optional[str] = None
progress: float = 0.0
results: Optional[Dict[str, Any]] = None
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

## 4. Data Models

_No data models found_

## 5. Configuration

## 6. Dependencies

### Internal Services

_No internal service dependencies_

### External Libraries
```txt
annotated-types==0.7.0
    # via pydantic
anyio==4.11.0
    # via
    #   httpx
    #   starlette
certifi==2025.10.5
    # via
    #   httpcore
    #   httpx
click==8.3.0
    # via uvicorn
fastapi==0.118.2
    # via maximus-orchestrator-service (pyproject.toml)
h11==0.16.0
    # via
    #   httpcore
    #   uvicorn
httpcore==1.0.9
    # via httpx
httpx==0.28.1
    # via maximus-orchestrator-service (pyproject.toml)
idna==3.10
    # via
    #   anyio
    #   httpx
pydantic==2.12.0
    # via
    #   maximus-orchestrator-service (pyproject.toml)
    #   fastapi
pydantic-core==2.41.1
    # via pydantic
python-dotenv==1.1.1
    # via maximus-orchestrator-service (pyproject.toml)
sniffio==1.3.1
    # via anyio
starlette>=0.49.1
    # via fastapi
typing-extensions==4.15.0
    # via
    #   anyio
    #   fastapi
    #   pydantic
    #   pydantic-core
    #   starlette
    #   typing-inspection
typing-inspection==0.4.2
    # via pydantic
uvicorn==0.37.0
    # via maximus-orchestrator-service (pyproject.toml)
```

