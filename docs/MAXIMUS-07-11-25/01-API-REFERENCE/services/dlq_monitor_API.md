# DLQ_MONITOR - API Reference

**Gerado:** 2025-11-07 20:45:52
**Método:** Análise automática do código fonte

---

## 1. Service Overview

### Statistics
- Python Files: 11
- Lines of Code: 2399
- Test Files: 4

### Entry Point
```
services/dlq_monitor/main.py
```

### Directory Structure
```
.
.shared
.tests
.tests/unit
```

---

## 2. API Endpoints

### `main.py` - Line 355
```python
@app.get("/health")
async def health_check():
```

**Description:**
```
"""Health check endpoint."""
return {
    "status": "healthy" if dlq_monitor.running else "unhealthy",
    "service": "maximus-dlq-monitor",
    "kafka_connected": dlq_monitor.consumer is not None,
    "dlq_queue_size": dlq_message_count,
    "alert_threshold": DLQ_ALERT_THRESHOLD
}
```

### `main.py` - Line 367
```python
@app.get("/status")
async def get_status():
```

**Description:**
```
"""Get DLQ monitor status and metrics."""
return {
    "service": "maximus-dlq-monitor",
    "running": dlq_monitor.running,
    "kafka_bootstrap": KAFKA_BOOTSTRAP_SERVERS,
    "dlq_topic": DLQ_TOPIC,
    "retry_topic": RETRY_TOPIC,
    "max_retries": MAX_RETRIES,
    "current_queue_size": dlq_message_count,
```

### `main.py` - Line 383
```python
@app.get("/")
async def root():
```

**Description:**
```
"""Root endpoint."""
return {
    "service": "MAXIMUS DLQ Monitor",
    "version": "1.0.0",
    "description": "Monitoring Dead Letter Queue for failed APV messages",
    "endpoints": {
        "health": "/health",
        "status": "/status",
        "metrics": "/metrics"
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

### `test_constitutional_compliance.py` - Line 26
```python
    @app.get("/health/live")
    async def health_live():
```

### `test_constitutional_compliance.py` - Line 30
```python
    @app.get("/health/ready")
    async def health_ready():
```

**Description:**
```
"""Test that /metrics endpoint exists and returns Prometheus format."""
response = client.get("/metrics")
assert response.status_code == 200
```

_No HTTP endpoints found_

## 3. Classes and Methods

### `DLQMonitor`

**File:** `main.py`

```python
class DLQMonitor:
```

**Description:**
```
"""Dead Letter Queue Monitor with retry logic."""

def __init__(self):
    self.consumer = None
    self.producer = None
    self.running = False

async def start(self):
    """Start DLQ monitoring."""
    logger.info("Starting DLQ Monitor...")

    try:
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            DLQ_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
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
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
kafka-python>=2.0.2
prometheus-client>=0.19.0
python-dotenv>=1.0.0
opentelemetry-api
opentelemetry-sdk
opentelemetry-instrumentation-fastapi
opentelemetry-instrumentation-httpx
opentelemetry-instrumentation-asyncpg
opentelemetry-instrumentation-redis
opentelemetry-exporter-jaeger-thrift
opentelemetry-exporter-otlp-proto-grpc
python-json-logger
structlog
```

