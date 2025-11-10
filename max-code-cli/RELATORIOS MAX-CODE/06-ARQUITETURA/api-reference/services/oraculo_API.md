# ORACULO - API Reference

**Gerado:** 2025-11-07 20:45:59
**Método:** Análise automática do código fonte

---

## 1. Service Overview

### Statistics
- Python Files: 55
- Lines of Code: 11459
- Test Files: 21

### Entry Point
```
services/oraculo/main.py
```

### Directory Structure
```
.
.api_endpoints
.enrichment
.filtering
.htmlcov
.kafka_integration
.llm
.models
.queue
.scripts
.shared
.tests
.tests/e2e
.tests/integration
.tests/unit
.threat_feeds
.websocket
```

---

## 2. API Endpoints

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

### `websocket_endpoints.py` - Line 120
```python
@router.get("/ws/status")
async def websocket_status() -> dict:
```

**Description:**
```
"""
Get WebSocket stream manager status.

Returns:
    Metrics including active connections, messages broadcast, uptime.
"""
if not _stream_manager:
    return {
        "status": "unavailable",
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

### `api.py` - Line 149
```python
@app.get("/health")
async def health_check() -> Dict[str, Any]:
```

**Description:**
```
"""Performs a health check of the Oraculo Service.

Includes APVStreamManager status for degraded mode visibility.
AG-RUNTIME-001: Exposes Kafka connection status.

Returns:
    Dict[str, Any]: A dictionary indicating the service status and capabilities.
"""
health_status = config.get_health_status()
```

### `api.py` - Line 168
```python
@app.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
```

**Description:**
```
"""Get service capabilities and feature flags.

Returns:
    Dict[str, Any]: Current capabilities and configuration.
"""
return {
    "capabilities": config.get_capabilities(),
    "configuration": {
        "llm_model": config.openai_model if config.check_llm_availability() else None,
```

### `api.py` - Line 185
```python
@app.post("/predict")
async def get_prediction(request: PredictionRequest) -> Dict[str, Any]:
```

**Description:**
```
"""Generates a predictive insight based on the provided data.

Args:
    request (PredictionRequest): The request body containing data and prediction parameters.

Returns:
    Dict[str, Any]: A dictionary containing the prediction results and confidence.
"""
print(f"[API] Generating {request.prediction_type} prediction for {request.time_horizon}.")
```

### `api.py` - Line 208
```python
@app.post("/analyze_code")
async def analyze_code_endpoint(request: CodeAnalysisRequest) -> Dict[str, Any]:
```

**Description:**
```
"""Analyzes code for vulnerabilities, performance issues, or refactoring opportunities.

Args:
    request (CodeAnalysisRequest): The request body containing the code and analysis parameters.

Returns:
    Dict[str, Any]: A dictionary containing the code analysis results.
"""
print(f"[API] Analyzing {request.language} code for {request.analysis_type}.")
```

### `api.py` - Line 227
```python
@app.post("/auto_implement")
async def auto_implement_code_endpoint(
```

**Description:**
```
"""Requests automated code implementation based on a task description.

Args:
    request (ImplementationRequest): The request body containing the task description and context.

Returns:
    Dict[str, Any]: A dictionary containing the generated code and implementation details.
```

_No HTTP endpoints found_

## 3. Classes and Methods

### `PredictionRequest`

**File:** `api.py`

```python
class PredictionRequest(BaseModel):
```

**Description:**
```
"""Request model for submitting data for predictive analysis.

Attributes:
    data (Dict[str, Any]): The data to analyze for predictions.
    prediction_type (str): The type of prediction requested (e.g., 'threat_level', 'resource_demand').
    time_horizon (str): The time horizon for the prediction (e.g., '24h', '7d').
"""

data: Dict[str, Any]
prediction_type: str
time_horizon: str


class CodeAnalysisRequest(BaseModel):
"""Request model for submitting code for analysis.
```

**Public Methods:**


---

### `CodeAnalysisRequest`

**File:** `api.py`

```python
class CodeAnalysisRequest(BaseModel):
```

**Description:**
```
"""Request model for submitting code for analysis.

Attributes:
    code (str): The code snippet to analyze.
    language (str): The programming language of the code.
    analysis_type (str): The type of analysis (e.g., 'vulnerability', 'performance', 'refactoring').
"""

code: str
language: str
analysis_type: str


class ImplementationRequest(BaseModel):
"""Request model for requesting automated code implementation.
```

**Public Methods:**


---

### `ImplementationRequest`

**File:** `api.py`

```python
class ImplementationRequest(BaseModel):
```

**Description:**
```
"""Request model for requesting automated code implementation.

Attributes:
    task_description (str): A description of the coding task.
    context (Optional[Dict[str, Any]]): Additional context or existing code.
    target_language (str): The target programming language.
"""

task_description: str
context: Optional[Dict[str, Any]] = None
target_language: str


@app.on_event("startup")
async def startup_event():
"""Performs startup tasks for the Oraculo Service."""
```

**Public Methods:**


---

### `AutoImplementer`

**File:** `auto_implementer.py`

```python
class AutoImplementer:
```

**Description:**
```
"""Translates high-level task descriptions and strategic suggestions into
concrete code implementations or configuration changes.

Leverages advanced code generation techniques, large language models (LLMs),
and potentially integration with development tools.
"""

def __init__(self):
    """Initializes the AutoImplementer."""
    self.implementation_history: List[Dict[str, Any]] = []
    self.last_implementation_time: Optional[datetime] = None
    self.current_status: str = "ready_for_implementation"

    # LLM integration (optional)
    self.llm_enabled = os.getenv("ENABLE_LLM_CODEGEN", "true").lower() == "true"
    self.llm_client: Optional[OpenAICodeGenerator] = None
```

**Public Methods:**


---

### `CodeScanner`

**File:** `code_scanner.py`

```python
class CodeScanner:
```

**Description:**
```
"""Performs static analysis of code snippets or entire codebases to identify
vulnerabilities, performance bottlenecks, code smells, or refactoring opportunities.

Leverages static analysis tools, abstract syntax tree (AST) parsing,
and potentially machine learning models trained on code patterns.
"""

def __init__(self):
    """Initializes the CodeScanner."""
    self.scan_history: List[Dict[str, Any]] = []
    self.last_scan_time: Optional[datetime] = None
    self.current_status: str = "ready_to_scan"

async def scan_code(self, code: str, language: str, analysis_type: str) -> Dict[str, Any]:
    """Scans a given code snippet for specified analysis types.
```

**Public Methods:**


---

### `OraculoConfig`

**File:** `config.py`

```python
class OraculoConfig:
```

**Description:**
```
"""Configuration manager for Oráculo service."""

def __init__(self):
    """Initialize configuration from environment variables."""
    # Feature flags
    self.enable_kafka = os.getenv("ENABLE_KAFKA", "true").lower() == "true"
    self.enable_websocket = os.getenv("ENABLE_WEBSOCKET", "true").lower() == "true"
    self.enable_llm_codegen = os.getenv("ENABLE_LLM_CODEGEN", "true").lower() == "true"

    # Kafka settings
    self.kafka_brokers = os.getenv("KAFKA_BROKERS", "localhost:9092")
    self.kafka_topic = os.getenv("KAFKA_TOPIC", "maximus.adaptive-immunity.apv")

    # OpenAI settings
    self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
```

**Public Methods:**

- `def check_kafka_availability(self) -> bool`
- `def check_llm_availability(self) -> bool`
- `def get_capabilities(self) -> Dict[str, bool]`
- `def add_degradation(self, degradation`
- `def get_health_status(self) -> Dict[str, Any]`

---

### `PackageDependency`

**File:** `dependency_graph.py`

```python
class PackageDependency:
```

**Description:**
```
"""
Represents a package dependency with version constraints.

Example:
    PackageDependency(name="django", version_spec=">=4.2,<5.0", ecosystem="PyPI")
"""
name: str
version_spec: str
ecosystem: str = "PyPI"
is_dev: bool = False

def matches_version(self, version: str) -> bool:
    """
    Check if a specific version matches this dependency's constraints.
    
    Simplified version matching:
```

**Public Methods:**

- `def matches_version(self, version`

---

### `ServiceDependencies`

**File:** `dependency_graph.py`

```python
class ServiceDependencies:
```

**Description:**
```
"""
Dependencies for a single service.

Attributes:
    service_name: Name of the service (e.g., "maximus_oraculo")
    path: Path to service directory
    dependencies: Production dependencies
    dev_dependencies: Development dependencies
"""
service_name: str
path: Path
dependencies: List[PackageDependency] = field(default_factory=list)
dev_dependencies: List[PackageDependency] = field(default_factory=list)

@property
def all_dependencies(self) -> List[PackageDependency]:
```

**Public Methods:**

- `def all_dependencies(self) -> List[PackageDependency]`
- `def has_package(self, package_name`
- `def get_package_version(self, package_name`

---

### `DependencyGraphBuilder`

**File:** `dependency_graph.py`

```python
class DependencyGraphBuilder:
```

**Description:**
```
"""
Builds and maintains dependency graph for MAXIMUS services.

Usage:
    >>> builder = DependencyGraphBuilder(repo_root="/path/to/maximus")
    >>> await builder.build_graph()
    >>> services = builder.get_services_using_package("django")
    >>> print(f"Django used by: {[s.service_name for s in services]}")

Theoretical Foundation:
- Dependency Graph: Directed graph of package dependencies
- Service Mesh: Microservices architecture dependency tracking
- Version Constraints: Semantic versioning and constraint resolution
"""

def __init__(self, repo_root: Path):
```

**Public Methods:**

- `def build_graph(self) -> None`
- `def get_services_using_package(self, package_name`
- `def get_all_services(self) -> List[ServiceDependencies]`
- `def get_all_packages(self) -> Set[str]`
- `def get_stats(self) -> Dict[str, Union[int, float]]`

---

### `RelevanceMatch`

**File:** `relevance_filter.py`

```python
class RelevanceMatch:
```

**Description:**
```
"""
Represents a relevant vulnerability match.

Attributes:
    cve_id: CVE identifier
    package_name: Affected package
    ecosystem: Package ecosystem (PyPI, npm, etc.)
    affected_services: Services using the vulnerable package
    version_match: Whether version constraints match
    severity_score: CVSS base score (if available)
"""
cve_id: str
package_name: str
ecosystem: str
affected_services: List[str]
version_match: bool
```

**Public Methods:**


---

### `RelevanceFilter`

**File:** `relevance_filter.py`

```python
class RelevanceFilter:
```

**Description:**
```
"""
Filters vulnerabilities based on dependency graph relevance.

Key Responsibilities:
- Cross-reference CVEs with dependency graph
- Match version constraints (using packaging.specifiers)
- Filter out irrelevant vulnerabilities
- Prioritize by number of affected services

Theoretical Foundation:
- Version Constraint Resolution: PEP 440 semantics
- Graph Traversal: O(1) lookup via inverted index
- Relevance Scoring: Affected services count + CVSS

Usage:
    >>> graph = DependencyGraphBuilder(repo_root)
```

**Public Methods:**

- `def filter_vulnerabilities(`
- `def get_most_critical(`
- `def get_stats(self, matches`

---

### `APVPublisher`

**File:** `apv_publisher.py`

```python
class APVPublisher:
```

**Description:**
```
"""
Publishes APVs to Kafka topics.

Features:
- Async Kafka producer (aiokafka)
- JSON serialization
- Delivery guarantees (at-least-once)
- Error handling with DLQ
- Metrics collection

Theoretical Foundation:
- Event Streaming: Kafka as event bus
- At-Least-Once Delivery: acks=all
- Dead Letter Queue: For failed messages

Usage:
```

**Public Methods:**

- `def get_stats(self) -> Dict[str, int]`

---

### `CodeGenerationResult`

**File:** `openai_client.py`

```python
class CodeGenerationResult:
```

**Description:**
```
"""Result from LLM code generation."""

code: str
model: str
tokens_used: int
cost_usd: float
latency_ms: float
success: bool
error: Optional[str] = None


class OpenAICodeGenerator:
"""OpenAI client for code generation with production features."""

# Pricing per 1K tokens (as of 2025)
PRICING = {
```

**Public Methods:**


---

### `OpenAICodeGenerator`

**File:** `openai_client.py`

```python
class OpenAICodeGenerator:
```

**Description:**
```
"""OpenAI client for code generation with production features."""

# Pricing per 1K tokens (as of 2025)
PRICING = {
    "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4": {"input": 0.03, "output": 0.06},
}

def __init__(
    self,
    api_key: Optional[str] = None,
    model: str = "gpt-4-turbo-preview",
    max_tokens: int = 4096,
    temperature: float = 0.2,
    max_retries: int = 3,
```

**Public Methods:**

- `def get_metrics(self) -> Dict[str, Any]`

---

### `PriorityLevel`

**File:** `apv.py`

```python
class PriorityLevel(str, Enum):
```

**Description:**
```
"""
Priority levels for APV triage.

Based on CVSS score + MAXIMUS context (affected services, exploitability).
"""
CRITICAL = "critical"
HIGH = "high"
MEDIUM = "medium"
LOW = "low"


class RemediationStrategy(str, Enum):
"""
Available remediation strategies.

Strategy selection based on:
```

**Public Methods:**


---

### `RemediationStrategy`

**File:** `apv.py`

```python
class RemediationStrategy(str, Enum):
```

**Description:**
```
"""
Available remediation strategies.

Strategy selection based on:
- Availability of fixed version (dependency_upgrade)
- Code pattern detectability (code_patch)
- Zero-day status (coagulation_waf)
- Complexity threshold (manual_review)
"""
DEPENDENCY_UPGRADE = "dependency_upgrade"
CODE_PATCH = "code_patch"
COAGULATION_WAF = "coagulation_waf"
MANUAL_REVIEW = "manual_review"


class RemediationComplexity(str, Enum):
```

**Public Methods:**


---

### `RemediationComplexity`

**File:** `apv.py`

```python
class RemediationComplexity(str, Enum):
```

**Description:**
```
"""Estimated complexity of remediation."""
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"


class CVSSScore(BaseModel):
"""
CVSS (Common Vulnerability Scoring System) score.

Normalized representation supporting CVSS 3.1 and 4.0.
"""
version: str = Field(..., description="CVSS version (3.1, 4.0)")
base_score: float = Field(..., ge=0.0, le=10.0, description="Base score (0.0-10.0)")
severity: str = Field(..., description="Severity: NONE, LOW, MEDIUM, HIGH, CRITICAL")
```

**Public Methods:**


---

### `CVSSScore`

**File:** `apv.py`

```python
class CVSSScore(BaseModel):
```

**Description:**
```
"""
CVSS (Common Vulnerability Scoring System) score.

Normalized representation supporting CVSS 3.1 and 4.0.
"""
version: str = Field(..., description="CVSS version (3.1, 4.0)")
base_score: float = Field(..., ge=0.0, le=10.0, description="Base score (0.0-10.0)")
severity: str = Field(..., description="Severity: NONE, LOW, MEDIUM, HIGH, CRITICAL")
vector_string: str = Field(..., description="CVSS vector string")

# Optional detailed metrics
exploitability_score: Optional[float] = Field(None, ge=0.0, le=10.0)
impact_score: Optional[float] = Field(None, ge=0.0, le=10.0)

@field_validator('severity')
@classmethod
```

**Public Methods:**

- `def validate_severity(cls, v`

---

### `ASTGrepPattern`

**File:** `apv.py`

```python
class ASTGrepPattern(BaseModel):
```

**Description:**
```
"""
ast-grep pattern for deterministic vulnerability confirmation.

Used by Eureka to scan codebase and confirm vulnerability presence.
"""
language: str = Field(default="python", description="Target language")
pattern: str = Field(..., description="ast-grep pattern string")
severity: str = Field(..., description="Match severity")
description: Optional[str] = Field(None, description="Pattern explanation")

@field_validator('language')
@classmethod
def validate_language(cls, v: str) -> str:
    """Validate supported languages."""
    supported = ['python', 'javascript', 'typescript', 'go', 'rust', 'java']
    if v.lower() not in supported:
```

**Public Methods:**

- `def validate_language(cls, v`

---

### `AffectedPackage`

**File:** `apv.py`

```python
class AffectedPackage(BaseModel):
```

**Description:**
```
"""
Package affected by vulnerability.

Tracks ecosystem, name, affected versions, and fixed versions.
"""
ecosystem: str = Field(..., description="Package ecosystem")
name: str = Field(..., description="Package name")
affected_versions: List[str] = Field(..., description="Affected version ranges")
fixed_versions: List[str] = Field(default_factory=list, description="Fixed versions")

# Optional fields
purl: Optional[str] = Field(None, description="Package URL (purl)")
introduced: Optional[str] = Field(None, description="Version where vuln was introduced")
last_affected: Optional[str] = Field(None, description="Last affected version")

@field_validator('ecosystem')
```

**Public Methods:**

- `def validate_ecosystem(cls, v`
- `def has_fix(self) -> bool`

---

### `APV`

**File:** `apv.py`

```python
class APV(BaseModel):
```

**Description:**
```
"""
Actionable Prioritized Vulnerability (APV).

Core data structure for MAXIMUS Adaptive Immunity System.
Extends CVE JSON 5.1.1 with actionable remediation fields.

Flow:
1. Oráculo ingests CVE from threat feeds (OSV.dev, NVD)
2. Oráculo enriches with CVSS, CWE, signatures
3. Oráculo filters by relevance (dependency graph)
4. Oráculo generates APV object
5. APV published to Kafka
6. Eureka consumes and remediates

Theoretical Foundation:
- IIT (Integrated Information Theory): APV as integrated information unit
```

**Public Methods:**

- `def calculate_smart_defaults(self) -> 'APV'`
- `def is_critical(self) -> bool`
- `def requires_immediate_action(self) -> bool`
- `def has_automated_fix(self) -> bool`
- `def affected_services(self) -> List[str]`
- `def to_kafka_message(self) -> Dict[str, Any]`
- `def to_database_record(self) -> Dict[str, Any]`

---

### `OraculoEngine`

**File:** `oraculo_engine.py`

```python
class OraculoEngine:
```

**Description:**
```
"""
Main orchestration engine for Oráculo Threat Sentinel.

Responsibilities:
- Orchestrate end-to-end CVE → APV → Kafka pipeline
- Manage threat feed clients
- Coordinate dependency graph
- Filter for relevance
- Generate APVs
- Publish to Kafka
- Collect metrics

Theoretical Foundation:
- Pipeline Pattern: Sequential data transformation
- Event-Driven Architecture: Kafka as event bus
- Circuit Breaker: Fail fast on feed unavailability
```

**Public Methods:**

- `def get_metrics(self) -> Dict[str, Any]`

---

### `OraculoEngine`

**File:** `oraculo.py`

```python
class OraculoEngine:
```

**Description:**
```
"""Provides predictive insights, probabilistic forecasts, and strategic guidance
based on complex data analysis and advanced modeling.

Applies predictive analytics, machine learning models, and simulation techniques.
"""

def __init__(self):
    """Initializes the OraculoEngine."""
    self.prediction_history: List[Dict[str, Any]] = []
    self.last_prediction_time: Optional[datetime] = None
    self.current_status: str = "ready_for_predictions"

async def generate_prediction(
    self, data: Dict[str, Any], prediction_type: str, time_horizon: str
) -> Dict[str, Any]:
    """Generates a predictive insight based on the provided data.
```

**Public Methods:**


---

### `InMemoryAPVQueue`

**File:** `memory_queue.py`

```python
class InMemoryAPVQueue:
```

**Description:**
```
"""
In-memory circular queue for APVs when Kafka is unavailable.

Features:
- Circular buffer (drops oldest when full)
- Thread-safe (deque operations are atomic)
- Statistics tracking
- Flush-to-Kafka support (for recovery)

Use Case:
When Kafka is unavailable, APVs are buffered in memory until:
1. Kafka reconnects (flush to Kafka)
2. Memory fills up (oldest APVs are dropped)
3. Service restarts (APVs are lost)

Trade-offs:
```

**Public Methods:**

- `def send(self, apv`
- `def get_all(self) -> List[Dict[str, Any]]`
- `def clear(self)`
- `def get_stats(self) -> Dict[str, Any]`
- `def is_full(self) -> bool`
- `def size(self) -> int`

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

### `SuggestionGenerator`

**File:** `suggestion_generator.py`

```python
class SuggestionGenerator:
```

**Description:**
```
"""Formulates actionable recommendations, strategic insights, and potential
solutions based on the predictive analysis and guidance provided by the Oraculo Engine.

Translates complex analytical results into clear, concise, and actionable suggestions.
"""

def __init__(self):
    """Initializes the SuggestionGenerator."""
    self.generated_suggestions: List[Dict[str, Any]] = []
    self.last_generation_time: Optional[datetime] = None
    self.current_status: str = "ready_to_suggest"

async def generate_suggestions(
    self, analysis_result: Dict[str, Any], context: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Generates actionable suggestions based on an analysis result.
```

**Public Methods:**


---

### `ThreatFeedError`

**File:** `base_feed.py`

```python
class ThreatFeedError(Exception):
```

**Description:**
```
"""Base exception for threat feed operations."""
pass


class RateLimitError(ThreatFeedError):
"""Raised when rate limit is exceeded."""
pass


class FeedUnavailableError(ThreatFeedError):
"""Raised when feed is temporarily unavailable."""
pass


class BaseFeedClient(ABC):
"""
```

**Public Methods:**


---

### `RateLimitError`

**File:** `base_feed.py`

```python
class RateLimitError(ThreatFeedError):
```

**Description:**
```
"""Raised when rate limit is exceeded."""
pass


class FeedUnavailableError(ThreatFeedError):
"""Raised when feed is temporarily unavailable."""
pass


class BaseFeedClient(ABC):
"""
Abstract base class for threat feed clients.

All threat feed implementations (OSV, NVD, Docker Security, etc.)
must inherit from this class and implement the required methods.
```

**Public Methods:**


---

### `FeedUnavailableError`

**File:** `base_feed.py`

```python
class FeedUnavailableError(ThreatFeedError):
```

**Description:**
```
"""Raised when feed is temporarily unavailable."""
pass


class BaseFeedClient(ABC):
"""
Abstract base class for threat feed clients.

All threat feed implementations (OSV, NVD, Docker Security, etc.)
must inherit from this class and implement the required methods.

Provides:
- Consistent error handling
- Retry logic patterns
- Rate limiting interface
- Logging standardization
```

**Public Methods:**


---

### `BaseFeedClient`

**File:** `base_feed.py`

```python
class BaseFeedClient(ABC):
```

**Description:**
```
"""
Abstract base class for threat feed clients.

All threat feed implementations (OSV, NVD, Docker Security, etc.)
must inherit from this class and implement the required methods.

Provides:
- Consistent error handling
- Retry logic patterns
- Rate limiting interface
- Logging standardization

Theoretical Foundation:
- Adapter Pattern: Normalize different feed APIs
- Circuit Breaker: Fail fast when feed is down
- Rate Limiting: Respect API quotas
```

**Public Methods:**

- `def get_stats(self) -> Dict[str, Any]`

---

### `OSVClient`

**File:** `osv_client.py`

```python
class OSVClient(BaseFeedClient):
```

**Description:**
```
"""
Client for OSV.dev API.

OSV.dev provides:
- Comprehensive vulnerability database
- Machine-readable format (OSV Schema)
- Package-based queries
- CVE cross-referencing

Features:
- Async HTTP client (aiohttp)
- Automatic retries with exponential backoff
- Rate limiting (100 req/min default)
- Connection pooling
- Timeout handling
```

**Public Methods:**


---

### `WebSocketConnection`

**File:** `apv_stream_manager.py`

```python
class WebSocketConnection:
```

**Description:**
```
"""
Represents an active WebSocket connection.

Attributes:
    connection_id: Unique identifier for this connection
    websocket: FastAPI WebSocket instance
    connected_at: Timestamp when connection established
    messages_sent: Count of messages broadcast to this connection
"""

connection_id: str
websocket: WebSocket
connected_at: datetime = field(default_factory=datetime.utcnow)
messages_sent: int = 0
```

**Public Methods:**


---

### `StreamMessage`

**File:** `apv_stream_manager.py`

```python
class StreamMessage:
```

**Description:**
```
"""
Message envelope for WebSocket streaming.

Supports multiple message types:
- apv: New APV detected
- patch: Remediation patch applied
- metrics: System metrics snapshot
- heartbeat: Keep-alive ping
"""

type: str  # "apv" | "patch" | "metrics" | "heartbeat"
timestamp: str
payload: Dict


class APVStreamManager:
```

**Public Methods:**


---

### `APVStreamManager`

**File:** `apv_stream_manager.py`

```python
class APVStreamManager:
```

**Description:**
```
"""
Manages WebSocket APV streaming to frontend clients.

Responsibilities:
1. Maintain pool of active WebSocket connections
2. Subscribe to Kafka APV topic
3. Broadcast APVs to all connected clients
4. Handle connection errors and cleanup
5. Provide metrics on streaming status

Usage:
    manager = APVStreamManager(kafka_bootstrap_servers="localhost:9092")
    await manager.start()
    
    # In WebSocket endpoint
    connection_id = await manager.connect(websocket)
```

**Public Methods:**

- `def get_metrics(self) -> Dict`

---

## 4. Data Models

_No data models found_

## 5. Configuration

### Environment Variables (from config.py)

```python
        self.enable_kafka = os.getenv("ENABLE_KAFKA", "true").lower() == "true"
        self.enable_websocket = os.getenv("ENABLE_WEBSOCKET", "true").lower() == "true"
        self.enable_llm_codegen = os.getenv("ENABLE_LLM_CODEGEN", "true").lower() == "true"
        self.kafka_brokers = os.getenv("KAFKA_BROKERS", "localhost:9092")
        self.kafka_topic = os.getenv("KAFKA_TOPIC", "maximus.adaptive-immunity.apv")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
```

## 6. Dependencies

### Internal Services

_No internal service dependencies_

### External Libraries
```txt
openai>=1.0.0
aiokafka==0.10.0
async-timeout==5.0.1
annotated-types==0.7.0
    # via pydantic
packaging==24.2
anyio==4.11.0
    # via starlette
click==8.3.0
    # via uvicorn
fastapi==0.118.1
    # via maximus-oraculo (pyproject.toml)
h11==0.16.0
    # via uvicorn
idna==3.10
    # via anyio
pydantic==2.12.0
    # via fastapi
pydantic-core==2.41.1
    # via pydantic
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
    # via maximus-oraculo (pyproject.toml)
prometheus-client
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

