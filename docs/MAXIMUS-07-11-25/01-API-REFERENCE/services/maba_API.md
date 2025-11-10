# MABA - API Reference

**Gerado:** 2025-11-07 20:45:54
**Método:** Análise automática do código fonte

---

## 1. Service Overview

### Statistics
- Python Files: 80
- Lines of Code: 28408
- Test Files: 24

### Entry Point
```
services/maba/main.py
```

### Directory Structure
```
.
.api
.config
.core
.docs
.htmlcov
.models
.scripts
.shared
.shared/devops_tools
.shared/messaging
.shared/middleware
.shared/models
.shared/security_tools
.shared/tests
.tests
```

---

## 2. API Endpoints

### `main.py` - Line 166
```python
@app.get("/health")
async def health_check() -> dict[str, Any]:
```

**Description:**
```
"""
Comprehensive health check endpoint.

Checks:
- MABA service status
- Browser controller health
- Cognitive map engine status
- Database connectivity
- Redis connectivity
```

### `main.py` - Line 198
```python
@app.get("/metrics")
async def metrics():
```

**Description:**
```
"""
Prometheus metrics endpoint.

Note: Metrics are served on a separate HTTP server on port 9090
by default. This endpoint provides a redirect for convenience.
"""
return {
    "message": "Metrics available on dedicated metrics port",
    "metrics_port": int(os.getenv("METRICS_PORT", 9090)),
```

### `main.py` - Line 213
```python
@app.get("/")
async def root():
```

**Description:**
```
"""Root endpoint with service information."""
return {
    "service": "MABA - MAXIMUS Browser Agent",
    "version": os.getenv("SERVICE_VERSION", "1.0.0"),
    "status": (
        "operational"
        if maba_service and maba_service.is_healthy()
        else "unavailable"
    ),
```

### `routes.py` - Line 51
```python
@router.post("/sessions")
async def create_browser_session(
```

**Description:**
```
"""
Create a new browser session.

Args:
    request: Browser session configuration

Returns:
```

### `routes.py` - Line 82
```python
@router.delete("/sessions/{session_id}")
async def close_browser_session(session_id: str, service=Depends(get_maba_service)):
```

**Description:**
```
"""
Close a browser session.

Args:
    session_id: Session ID to close

Returns:
    Success message
"""
```

### `routes.py` - Line 107
```python
@router.post("/navigate", response_model=BrowserActionResponse)
async def navigate(
```

**Description:**
```
"""
Navigate to a URL.

Args:
    request: Navigation request
    session_id: Browser session ID
```

### `routes.py` - Line 144
```python
@router.post("/click", response_model=BrowserActionResponse)
async def click(
```

**Description:**
```
"""
Click an element.

Args:
    request: Click request
    session_id: Browser session ID
```

### `routes.py` - Line 174
```python
@router.post("/type", response_model=BrowserActionResponse)
async def type_text(
```

**Description:**
```
"""
Type text into an element.

Args:
    request: Type request
    session_id: Browser session ID
```

### `routes.py` - Line 205
```python
@router.post("/screenshot", response_model=BrowserActionResponse)
async def screenshot(
```

**Description:**
```
"""
Take a screenshot.

Args:
    request: Screenshot request
    session_id: Browser session ID
```

### `routes.py` - Line 235
```python
@router.post("/extract", response_model=BrowserActionResponse)
async def extract_data(
```

**Description:**
```
"""
Extract data from current page.

Args:
    request: Extract request
    session_id: Browser session ID
```

### `routes.py` - Line 265
```python
@router.post("/cognitive-map/query", response_model=CognitiveMapQueryResponse)
async def query_cognitive_map(
```

**Description:**
```
"""
Query the cognitive map for learned information.

Args:
    request: Cognitive map query request

Returns:
```

### `routes.py` - Line 318
```python
@router.post("/analyze", response_model=PageAnalysisResponse)
async def analyze_page(
```

**Description:**
```
"""
Analyze current page with LLM.

This endpoint uses Claude to analyze the page content and provide
insights, recommendations, or structured data extraction.

NOTE: LLM-based page analysis is planned for future implementation.
```

### `routes.py` - Line 353
```python
@router.get("/stats")
async def get_stats(service=Depends(get_maba_service)):
```

**Description:**
```
"""
Get MABA statistics.

Returns:
    Statistics dict
"""
try:
    # Check if service has a get_stats method (for testing/mocking)
    if hasattr(service, "get_stats") and callable(service.get_stats):
```

### `vault_example.py` - Line 105
```python
    @app.get("/secrets/test")
    def test_vault(vault: VaultClient = Depends(get_vault_client)):
```

**Description:**
```
    """Endpoint that uses Vault"""
    try:
        # Get secret
        api_key = vault.get_secret("maximus_ai/anthropic", key="api_key")

        return {
            "status": "ok",
            "vault_connected": True,
            "api_key_length": len(api_key),
```

### `base_config.py` - Line 329
```python
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
```

**Description:**
```
    """Build Redis connection URL."""
    if not self.redis_host:
        return None
    auth = f":{self.redis_password}@" if self.redis_password else ""
    return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
```

### `test_vault_client.py` - Line 573
```python
    @patch("backend.shared.vault_client.get_vault_client")
    def test_get_api_key(self, mock_get_client):
```

**Description:**
```
    """Test get_api_key convenience function."""
    mock_client = MagicMock()
    mock_client.get_secret.return_value = "test-api-key"
    mock_get_client.return_value = mock_client

    result = get_api_key("virustotal", fallback_env="VT_API_KEY")

    assert result == "test-api-key"
    mock_client.get_secret.assert_called_once_with(
```

### `test_vault_client.py` - Line 587
```python
    @patch("backend.shared.vault_client.get_vault_client")
    def test_get_database_config(self, mock_get_client):
```

**Description:**
```
    """Test get_database_config convenience function."""
    mock_client = MagicMock()
    mock_client.get_secret.return_value = {"host": "localhost", "port": "5432"}
    mock_get_client.return_value = mock_client

    result = get_database_config("postgres")

    assert result == {"host": "localhost", "port": "5432"}
    mock_client.get_secret.assert_called_once_with("database/postgres")
```

### `test_vault_client.py` - Line 599
```python
    @patch("backend.shared.vault_client.get_vault_client")
    def test_get_jwt_secret(self, mock_get_client):
```

**Description:**
```
    """Test get_jwt_secret convenience function."""
    mock_client = MagicMock()
    mock_client.get_secret.return_value = "jwt-secret-key"
    mock_get_client.return_value = mock_client

    result = get_jwt_secret()

    assert result == "jwt-secret-key"
    mock_client.get_secret.assert_called_once_with(
```

### `rate_limiter.py` - Line 27
```python
    @app.get("/api/scan")
    @rate_limit(requests=10, window=60)  # 10 req/min
```

### `rate_limiter.py` - Line 356
```python
        @app.get("/api/expensive-operation")
        @rate_limit(requests=5, window=60)  # 5 req/min
```

**Description:**
```
"""

def decorator(func):
    @wraps(func)
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

### `websocket_gateway.py` - Line 321
```python
    @app.get("/health")
    async def health():
```

**Description:**
```
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "redis_connected": manager.redis_client is not None,
    }

return app
```

### `response_models.py` - Line 25
```python
    >>> @app.get("/users/{id}")
    >>> async def get_user(id: int) -> SuccessResponse:
```

**Description:**
```
"""

from datetime import datetime
from typing import Any, Generic, Literal, Optional, TypeVar
```

### `rate_limiter.py` - Line 236
```python
        @app.get("/api/endpoint")
        async def endpoint(request: Request):
```

**Description:**
```
"""
config = RateLimitConfig(max_requests=max_requests, window_seconds=window_seconds)

return RateLimiter(config=config, redis_url=redis_url)


if __name__ == "__main__":
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

### `BrowserController`

**File:** `browser_controller.py`

```python
class BrowserController:
```

**Description:**
```
"""
Playwright-based browser controller.

Manages browser instances, sessions, and provides high-level automation APIs.

Attributes:
    browser_type: Browser type (chromium, firefox, webkit)
    headless: Whether to run in headless mode
    max_instances: Maximum concurrent browser instances
    _playwright: Playwright instance
    _browser: Browser instance
    _sessions: Active browser sessions
"""

# Prometheus metrics
active_sessions = Gauge(
```

**Public Methods:**


---

### `CognitiveMapEngine`

**File:** `cognitive_map.py`

```python
class CognitiveMapEngine:
```

**Description:**
```
"""
Graph-based cognitive map for website learning.

Uses Neo4j to store and query learned website structures, enabling
intelligent navigation and automation based on past interactions.

Attributes:
    neo4j_uri: Neo4j connection URI
    neo4j_user: Neo4j username
    neo4j_password: Neo4j password
    _driver: Neo4j async driver
    _initialized: Initialization status
"""

# Prometheus metrics
pages_stored = Gauge(
```

**Public Methods:**


---

### `CognitiveMapSQL`

**File:** `cognitive_map_sql.py`

```python
class CognitiveMapSQL:
```

**Description:**
```
"""
PostgreSQL-based cognitive map for website learning.

Alternative to Neo4j implementation, uses PostgreSQL with JSONB
and GIN indexes for comparable performance with lower ops complexity.

Attributes:
    pool: AsyncPG connection pool
    _initialized: Initialization status
"""

# Prometheus metrics
pages_stored = Gauge(
    "maba_cognitive_map_sql_pages_total", "Total pages in cognitive map (SQL)"
)
```

**Public Methods:**


---

### `BrowserInstance`

**File:** `dynamic_browser_pool.py`

```python
class BrowserInstance:
```

**Description:**
```
"""Represents a browser instance with metrics."""

instance_id: str
created_at: datetime
session_count: int = 0
cpu_usage: float = 0.0
memory_usage: float = 0.0
is_healthy: bool = True

async def shutdown(self):
    """Shutdown browser instance."""
    logger.info(f"Shutting down browser instance: {self.instance_id}")
    # Implementation would close actual browser
    pass
```

**Public Methods:**


---

### `DynamicBrowserPool`

**File:** `dynamic_browser_pool.py`

```python
class DynamicBrowserPool:
```

**Description:**
```
"""Auto-scaling browser instance pool.

Scales up/down based on CPU metrics and demand, respects resource limits.

Biblical Principle: Proverbs 21:5 - "The plans of the diligent lead surely to abundance"
"""

def __init__(
    self,
    min_instances: int = 2,
    max_instances: int = 20,
    target_cpu_percent: float = 70.0,
    scale_up_threshold: float = 80.0,
    scale_down_threshold: float = 30.0,
    scale_check_interval: int = 30,
):
```

**Public Methods:**


---

### `LocatorStrategy`

**File:** `robust_element_locator.py`

```python
class LocatorStrategy(str, Enum):
```

**Description:**
```
"""Element locator strategies."""

CSS_SELECTOR = "css_selector"
DATA_TESTID = "data_testid"
ARIA_LABEL = "aria_label"
TEXT_CONTENT = "text_content"
XPATH = "xpath"
VISUAL_POSITION = "visual_position"


@dataclass
class ElementMatch:
"""Represents a matched element with metadata."""

selector: str
strategy: LocatorStrategy
```

**Public Methods:**


---

### `ElementMatch`

**File:** `robust_element_locator.py`

```python
class ElementMatch:
```

**Description:**
```
"""Represents a matched element with metadata."""

selector: str
strategy: LocatorStrategy
confidence: float  # 0.0-1.0
attributes: dict[str, Any]


# Prometheus metrics
element_locator_attempts = Counter(
"maba_element_locator_attempts_total",
"Element locator attempts by strategy",
["strategy", "success"],
)

element_locator_duration = Histogram(
```

**Public Methods:**


---

### `RobustElementLocator`

**File:** `robust_element_locator.py`

```python
class RobustElementLocator:
```

**Description:**
```
"""Multi-strategy element locator with intelligent fallbacks.

Tries multiple strategies to locate elements on dynamic web pages,
falling back gracefully when primary selectors fail.

Biblical Principle: Proverbs 24:6 - "In abundance of counselors there is victory"
"""

def __init__(
    self,
    enable_visual: bool = False,
    min_confidence: float = 0.7,
    timeout_ms: int = 5000,
):
    """Initialize robust element locator.
```

**Public Methods:**


---

### `SecurityPolicy`

**File:** `security_policy.py`

```python
class SecurityPolicy:
```

**Description:**
```
"""Domain whitelist and security controls for MABA.

Prevents navigation to unauthorized domains and internal networks.

Architecture:
- Whitelist: YAML config with allowed domains (supports wildcards)
- Blacklist: Hardcoded private networks and localhost
- Pattern matching: Supports wildcards like *.github.com
- Default: Permissive (*) if no config, with warning

Security Layers:
1. Blacklist check (private networks, localhost)
2. Whitelist check (configured allowed domains)
3. Logging and metrics for blocked attempts

Biblical Principle: Wisdom guards (Proverbs 2:11)
```

**Public Methods:**

- `def is_allowed(self, url`
- `def get_stats(self) -> dict[str, Any]`
- `def reload_whitelist(self) -> bool`

---

### `BrowserSession`

**File:** `session_manager.py`

```python
class BrowserSession:
```

**Description:**
```
"""Represents an active browser session."""

session_id: str
browser_instance_id: str
created_at: datetime
last_activity: datetime
metadata: dict[str, Any] = field(default_factory=dict)
is_active: bool = True

def update_activity(self):
    """Update last activity timestamp."""
    self.last_activity = datetime.utcnow()

@property
def idle_time(self) -> timedelta:
    """Get idle time since last activity."""
```

**Public Methods:**

- `def update_activity(self)`
- `def idle_time(self) -> timedelta`
- `def age(self) -> timedelta`

---

### `SessionManager`

**File:** `session_manager.py`

```python
class SessionManager:
```

**Description:**
```
"""Auto-timeout and graceful cleanup for browser sessions.

Manages session lifecycle, auto-timeout idle sessions, prevents memory leaks.

Biblical Principle: Ecclesiastes 3:1 - "For everything there is a season"
"""

def __init__(
    self,
    idle_timeout_seconds: int = 1800,  # 30 minutes
    cleanup_interval_seconds: int = 60,  # 1 minute
    max_session_age_seconds: int = 7200,  # 2 hours
):
    """Initialize session manager.

    Args:
```

**Public Methods:**


---

### `BrowserAction`

**File:** `models.py`

```python
class BrowserAction(str, Enum):
```

**Description:**
```
"""Supported browser actions."""

NAVIGATE = "navigate"
CLICK = "click"
TYPE = "type"
SCROLL = "scroll"
SCREENSHOT = "screenshot"
EXTRACT = "extract"
WAIT = "wait"
GO_BACK = "go_back"
GO_FORWARD = "go_forward"
REFRESH = "refresh"


class NavigationRequest(BaseModel):
"""Request to navigate to a URL."""
```

**Public Methods:**


---

### `NavigationRequest`

**File:** `models.py`

```python
class NavigationRequest(BaseModel):
```

**Description:**
```
"""Request to navigate to a URL."""

url: str = Field(..., description="Target URL")
wait_until: str = Field(
    default="networkidle",
    description="When to consider navigation complete (load, domcontentloaded, networkidle)",
)
timeout_ms: int = Field(
    default=30000, description="Navigation timeout in milliseconds"
)

@field_validator("url")
@classmethod
def validate_url(cls, v):
    """Validate URL format."""
    if not v.startswith(("http://", "https://")):
```

**Public Methods:**

- `def validate_url(cls, v)`

---

### `ClickRequest`

**File:** `models.py`

```python
class ClickRequest(BaseModel):
```

**Description:**
```
"""Request to click an element."""

selector: str = Field(..., description="CSS selector for element to click")
button: str = Field(
    default="left", description="Mouse button (left, right, middle)"
)
click_count: int = Field(default=1, description="Number of clicks")
timeout_ms: int = Field(default=30000, description="Timeout in milliseconds")


class TypeRequest(BaseModel):
"""Request to type text into an element."""

selector: str = Field(..., description="CSS selector for element")
text: str = Field(..., description="Text to type")
delay_ms: int = Field(
```

**Public Methods:**


---

### `TypeRequest`

**File:** `models.py`

```python
class TypeRequest(BaseModel):
```

**Description:**
```
"""Request to type text into an element."""

selector: str = Field(..., description="CSS selector for element")
text: str = Field(..., description="Text to type")
delay_ms: int = Field(
    default=0, description="Delay between key presses in milliseconds"
)


class ScreenshotRequest(BaseModel):
"""Request to take a screenshot."""

full_page: bool = Field(default=False, description="Capture full scrollable page")
selector: str | None = Field(
    default=None, description="CSS selector to screenshot specific element"
)
```

**Public Methods:**


---

### `ScreenshotRequest`

**File:** `models.py`

```python
class ScreenshotRequest(BaseModel):
```

**Description:**
```
"""Request to take a screenshot."""

full_page: bool = Field(default=False, description="Capture full scrollable page")
selector: str | None = Field(
    default=None, description="CSS selector to screenshot specific element"
)
format: str = Field(default="png", description="Image format (png, jpeg)")


class ExtractRequest(BaseModel):
"""Request to extract data from page."""

selectors: dict[str, str] = Field(
    ..., description="Map of field names to CSS selectors"
)
extract_all: bool = Field(
```

**Public Methods:**


---

### `ExtractRequest`

**File:** `models.py`

```python
class ExtractRequest(BaseModel):
```

**Description:**
```
"""Request to extract data from page."""

selectors: dict[str, str] = Field(
    ..., description="Map of field names to CSS selectors"
)
extract_all: bool = Field(
    default=False, description="Extract all matching elements"
)


class BrowserSessionRequest(BaseModel):
"""Request to create a new browser session."""

headless: bool = Field(default=True, description="Run browser in headless mode")
viewport_width: int = Field(default=1920, description="Viewport width")
viewport_height: int = Field(default=1080, description="Viewport height")
```

**Public Methods:**


---

### `BrowserSessionRequest`

**File:** `models.py`

```python
class BrowserSessionRequest(BaseModel):
```

**Description:**
```
"""Request to create a new browser session."""

headless: bool = Field(default=True, description="Run browser in headless mode")
viewport_width: int = Field(default=1920, description="Viewport width")
viewport_height: int = Field(default=1080, description="Viewport height")
user_agent: str | None = Field(default=None, description="Custom user agent")


class BrowserActionRequest(BaseModel):
"""Generic browser action request."""

action: BrowserAction = Field(..., description="Action to perform")
parameters: dict[str, Any] = Field(
    default_factory=dict, description="Action parameters"
)
session_id: str | None = Field(default=None, description="Browser session ID")
```

**Public Methods:**


---

### `BrowserActionRequest`

**File:** `models.py`

```python
class BrowserActionRequest(BaseModel):
```

**Description:**
```
"""Generic browser action request."""

action: BrowserAction = Field(..., description="Action to perform")
parameters: dict[str, Any] = Field(
    default_factory=dict, description="Action parameters"
)
session_id: str | None = Field(default=None, description="Browser session ID")


class BrowserActionResponse(BaseModel):
"""Browser action response."""

status: str = Field(..., description="Action status")
result: dict[str, Any] | None = Field(default=None, description="Action result")
error: str | None = Field(default=None, description="Error message if failed")
execution_time_ms: float | None = Field(
```

**Public Methods:**


---

### `BrowserActionResponse`

**File:** `models.py`

```python
class BrowserActionResponse(BaseModel):
```

**Description:**
```
"""Browser action response."""

status: str = Field(..., description="Action status")
result: dict[str, Any] | None = Field(default=None, description="Action result")
error: str | None = Field(default=None, description="Error message if failed")
execution_time_ms: float | None = Field(
    default=None, description="Execution time in milliseconds"
)
timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class CognitiveMapQueryRequest(BaseModel):
"""Request to query the cognitive map."""

domain: str | None = Field(
    default=None,
```

**Public Methods:**


---

### `CognitiveMapQueryRequest`

**File:** `models.py`

```python
class CognitiveMapQueryRequest(BaseModel):
```

**Description:**
```
"""Request to query the cognitive map."""

domain: str | None = Field(
    default=None,
    description="Website domain (optional, can be inferred from URL in parameters)",
)
query_type: str = Field(
    ..., description="Query type (find_element, get_path, etc.)"
)
parameters: dict[str, Any] = Field(
    default_factory=dict, description="Query parameters"
)


class CognitiveMapQueryResponse(BaseModel):
"""Cognitive map query response."""
```

**Public Methods:**


---

### `CognitiveMapQueryResponse`

**File:** `models.py`

```python
class CognitiveMapQueryResponse(BaseModel):
```

**Description:**
```
"""Cognitive map query response."""

found: bool = Field(..., description="Whether result was found")
result: dict[str, Any] | None = Field(default=None, description="Query result")
confidence: float = Field(..., description="Confidence score 0-1")


class PageAnalysisRequest(BaseModel):
"""Request to analyze a page with LLM."""

url: str | None = Field(
    default=None, description="URL to analyze (if not current page)"
)
analysis_type: str = Field(
    default="general",
    description="Type of analysis (general, form, navigation, data)",
```

**Public Methods:**


---

### `PageAnalysisRequest`

**File:** `models.py`

```python
class PageAnalysisRequest(BaseModel):
```

**Description:**
```
"""Request to analyze a page with LLM."""

url: str | None = Field(
    default=None, description="URL to analyze (if not current page)"
)
analysis_type: str = Field(
    default="general",
    description="Type of analysis (general, form, navigation, data)",
)
instructions: str | None = Field(
    default=None, description="Specific instructions for analysis"
)


class PageAnalysisResponse(BaseModel):
"""Page analysis response."""
```

**Public Methods:**


---

### `PageAnalysisResponse`

**File:** `models.py`

```python
class PageAnalysisResponse(BaseModel):
```

**Description:**
```
"""Page analysis response."""

analysis: str = Field(..., description="LLM analysis result")
structured_data: dict[str, Any] | None = Field(
    default=None, description="Structured extraction"
)
recommendations: list[str] = Field(
    default_factory=list, description="Recommended actions"
)


class MABAService(SubordinateServiceBase, MaximusIntegrationMixin):
"""
MABA (MAXIMUS Browser Agent) Service Implementation.

This class integrates browser automation capabilities with MAXIMUS Core,
```

**Public Methods:**


---

### `MABAService`

**File:** `models.py`

```python
class MABAService(SubordinateServiceBase, MaximusIntegrationMixin):
```

**Description:**
```
"""
MABA (MAXIMUS Browser Agent) Service Implementation.

This class integrates browser automation capabilities with MAXIMUS Core,
providing autonomous web navigation, data extraction, and interaction.

Attributes:
    browser_controller: Playwright browser controller
    cognitive_map: Graph-based learned website structure
"""

def __init__(
    self,
    service_name: str,
    service_version: str,
    maximus_endpoint: str | None = None,
```

**Public Methods:**


---

### `BenchmarkResults`

**File:** `benchmark_cognitive_map.py`

```python
class BenchmarkResults:
```

**Description:**
```
"""Container for benchmark results."""

def __init__(self, backend_name: str):
    self.backend_name = backend_name
    self.operations: dict[str, float] = {}
    self.total_time = 0.0

def add_operation(self, operation: str, duration: float):
    """Record operation duration."""
    self.operations[operation] = duration
    self.total_time += duration

def get_summary(self) -> dict[str, Any]:
    """Get benchmark summary."""
    return {
        "backend": self.backend_name,
```

**Public Methods:**

- `def add_operation(self, operation`
- `def get_summary(self) -> dict[str, Any]`

---

### `AuditConfig`

**File:** `audit_logger.py`

```python
class AuditConfig:
```

**Description:**
```
"""Audit logging configuration."""

# PostgreSQL connection (override via environment)
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "vertice_audit"
DB_USER = "vertice"
DB_PASSWORD = "changeme"

# Table name
TABLE_NAME = "audit_logs"

# Retention policy (days)
RETENTION_DAYS = 365  # 1 year

# Log to file as backup
```

**Public Methods:**


---

### `AuditLogger`

**File:** `audit_logger.py`

```python
class AuditLogger:
```

**Description:**
```
"""
Comprehensive audit logging system.

Logs security-relevant events to:
1. PostgreSQL (primary, queryable)
2. File (backup, SIEM ingestion)
3. Python logging (dev/debug)
"""

def __init__(
    self, db_config: dict[str, Any] | None = None, log_to_file: bool = True
):
    self.db_config = db_config or self._get_default_config()
    self.log_to_file = log_to_file
    self.db_connection = None
```

**Public Methods:**

- `def log(`
- `def log_auth_attempt(`
- `def log_logout(self, username`
- `def log_data_access(`
- `def log_config_change(`
- `def log_tool_execution(`
- `def log_security_event(`
- `def log_api_call(`
- `def close(self)`

---

### `Environment`

**File:** `base_config.py`

```python
class Environment(str, Enum):
```

**Description:**
```
"""Application environment types."""

DEVELOPMENT = "development"
STAGING = "staging"
PRODUCTION = "production"
TESTING = "testing"


# ============================================================================
# BASE SERVICE CONFIGURATION
# ============================================================================


class BaseServiceConfig(BaseSettings):
"""
Base configuration class for all Vértice microservices.
```

**Public Methods:**


---

### `BaseServiceConfig`

**File:** `base_config.py`

```python
class BaseServiceConfig(BaseSettings):
```

**Description:**
```
"""
Base configuration class for all Vértice microservices.

All service-specific configs should inherit from this class to ensure
consistent environment variable handling, validation, and documentation.

Common Environment Variables:
    VERTICE_ENV: Environment name (development/staging/production)
    SERVICE_NAME: Name of the microservice
    SERVICE_PORT: Port number for the service
    LOG_LEVEL: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
    DEBUG: Enable debug mode (true/false)
"""

model_config = SettingsConfigDict(
    # Environment file configuration
```

**Public Methods:**

- `def validate_log_level(cls, v`
- `def parse_cors_origins(cls, v`
- `def is_development(self) -> bool`
- `def is_production(self) -> bool`
- `def is_testing(self) -> bool`
- `def postgres_url(self) -> str | None`
- `def redis_url(self) -> str | None`
- `def model_dump_safe(self) -> dict[str, Any]`
- `def validate_required_vars(self, *var_names`

---

### `ServicePorts`

**File:** `constants.py`

```python
class ServicePorts:
```

**Description:**
```
"""Service port assignments for all Vértice microservices.

Port Range Allocation:
    8000-8099: Core & Intelligence Services
    8100-8199: Cognitive & Neural Services
    8200-8299: Data & Storage Services
    8300-8399: Offensive Security Arsenal
    8400-8499: Infrastructure Services
    9000+: Monitoring & Observability
"""

# Core Services (8000-8019)
API_GATEWAY: Final[int] = 8000
MAXIMUS_CORE: Final[int] = 8001
IP_INTELLIGENCE: Final[int] = 8002
THREAT_INTEL: Final[int] = 8003
```

**Public Methods:**


---

### `APIEndpoints`

**File:** `constants.py`

```python
class APIEndpoints:
```

**Description:**
```
"""Standard API endpoint patterns across services."""

# Health & Status
HEALTH: Final[str] = "/health"
READY: Final[str] = "/ready"
METRICS: Final[str] = "/metrics"

# Documentation
DOCS: Final[str] = "/docs"
REDOC: Final[str] = "/redoc"
OPENAPI: Final[str] = "/openapi.json"

# Common CRUD
LIST: Final[str] = "/"
CREATE: Final[str] = "/"
GET_BY_ID: Final[str] = "/{id}"
```

**Public Methods:**


---

### `ResponseCodes`

**File:** `constants.py`

```python
class ResponseCodes:
```

**Description:**
```
"""Standardized response codes for API responses."""

# Success Codes
SUCCESS: Final[str] = "SUCCESS"
CREATED: Final[str] = "CREATED"
UPDATED: Final[str] = "UPDATED"
DELETED: Final[str] = "DELETED"

# Error Codes - Validation
VALIDATION_ERROR: Final[str] = "VALIDATION_ERROR"
INVALID_INPUT: Final[str] = "INVALID_INPUT"
MISSING_FIELD: Final[str] = "MISSING_FIELD"
INVALID_FORMAT: Final[str] = "INVALID_FORMAT"

# Error Codes - Authentication/Authorization
UNAUTHORIZED: Final[str] = "UNAUTHORIZED"
```

**Public Methods:**


---

### `ThreatLevels`

**File:** `constants.py`

```python
class ThreatLevels:
```

**Description:**
```
"""Threat severity levels following NIST 800-61 guidelines."""

CRITICAL: Final[str] = "CRITICAL"  # Immediate action required
HIGH: Final[str] = "HIGH"  # Urgent response needed
MEDIUM: Final[str] = "MEDIUM"  # Response within 24h
LOW: Final[str] = "LOW"  # Routine handling
INFO: Final[str] = "INFO"  # Informational only

# Numeric scores for sorting/filtering
SCORES: Final[dict] = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "INFO": 1}


# ============================================================================
# SERVICE STATUS - Health Check States
# ============================================================================
```

**Public Methods:**


---

### `ServiceStatus`

**File:** `constants.py`

```python
class ServiceStatus:
```

**Description:**
```
"""Service health status values."""

HEALTHY: Final[str] = "healthy"
UNHEALTHY: Final[str] = "unhealthy"
DEGRADED: Final[str] = "degraded"
STARTING: Final[str] = "starting"
STOPPING: Final[str] = "stopping"
UNKNOWN: Final[str] = "unknown"


# ============================================================================
# MALWARE CLASSIFICATION - MITRE ATT&CK Aligned
# ============================================================================


class MalwareTypes:
```

**Public Methods:**


---

### `MalwareTypes`

**File:** `constants.py`

```python
class MalwareTypes:
```

**Description:**
```
"""Malware classification following MITRE ATT&CK."""

RANSOMWARE: Final[str] = "ransomware"
TROJAN: Final[str] = "trojan"
WORM: Final[str] = "worm"
VIRUS: Final[str] = "virus"
ROOTKIT: Final[str] = "rootkit"
SPYWARE: Final[str] = "spyware"
ADWARE: Final[str] = "adware"
BOTNET: Final[str] = "botnet"
RAT: Final[str] = "rat"  # Remote Access Trojan
KEYLOGGER: Final[str] = "keylogger"
CRYPTOMINER: Final[str] = "cryptominer"
BACKDOOR: Final[str] = "backdoor"
DROPPER: Final[str] = "dropper"
DOWNLOADER: Final[str] = "downloader"
```

**Public Methods:**


---

### `AttackTactics`

**File:** `constants.py`

```python
class AttackTactics:
```

**Description:**
```
"""MITRE ATT&CK tactics."""

RECONNAISSANCE: Final[str] = "reconnaissance"
RESOURCE_DEVELOPMENT: Final[str] = "resource_development"
INITIAL_ACCESS: Final[str] = "initial_access"
EXECUTION: Final[str] = "execution"
PERSISTENCE: Final[str] = "persistence"
PRIVILEGE_ESCALATION: Final[str] = "privilege_escalation"
DEFENSE_EVASION: Final[str] = "defense_evasion"
CREDENTIAL_ACCESS: Final[str] = "credential_access"
DISCOVERY: Final[str] = "discovery"
LATERAL_MOVEMENT: Final[str] = "lateral_movement"
COLLECTION: Final[str] = "collection"
COMMAND_AND_CONTROL: Final[str] = "command_and_control"
EXFILTRATION: Final[str] = "exfiltration"
IMPACT: Final[str] = "impact"
```

**Public Methods:**


---

### `NetworkProtocols`

**File:** `constants.py`

```python
class NetworkProtocols:
```

**Description:**
```
"""Common network protocols for scanning/analysis."""

TCP: Final[str] = "tcp"
UDP: Final[str] = "udp"
ICMP: Final[str] = "icmp"
HTTP: Final[str] = "http"
HTTPS: Final[str] = "https"
DNS: Final[str] = "dns"
FTP: Final[str] = "ftp"
SSH: Final[str] = "ssh"
TELNET: Final[str] = "telnet"
SMTP: Final[str] = "smtp"
POP3: Final[str] = "pop3"
IMAP: Final[str] = "imap"
SMB: Final[str] = "smb"
RDP: Final[str] = "rdp"
```

**Public Methods:**


---

### `TimeConstants`

**File:** `constants.py`

```python
class TimeConstants:
```

**Description:**
```
"""Time-related constants in seconds."""

SECOND: Final[int] = 1
MINUTE: Final[int] = 60
HOUR: Final[int] = 3600
DAY: Final[int] = 86400
WEEK: Final[int] = 604800

# Timeouts
DEFAULT_TIMEOUT: Final[int] = 30
LONG_RUNNING_TIMEOUT: Final[int] = 300
HTTP_TIMEOUT: Final[int] = 10
DATABASE_TIMEOUT: Final[int] = 5

# Cache TTLs
CACHE_SHORT: Final[int] = 300  # 5 minutes
```

**Public Methods:**


---

### `DatabaseNames`

**File:** `constants.py`

```python
class DatabaseNames:
```

**Description:**
```
"""Database names for different data stores."""

# PostgreSQL Databases
POSTGRES_MAIN: Final[str] = "vertice"
POSTGRES_AUTH: Final[str] = "vertice_auth"
POSTGRES_LOGS: Final[str] = "vertice_logs"

# Neo4j Databases
NEO4J_THREAT_GRAPH: Final[str] = "threat_graph"
NEO4J_KNOWLEDGE_BASE: Final[str] = "knowledge_base"

# Qdrant Collections
QDRANT_EMBEDDINGS: Final[str] = "threat_embeddings"
QDRANT_MEMORY: Final[str] = "maximus_memory"

# Redis Keyspaces
```

**Public Methods:**


---

### `FileExtensions`

**File:** `constants.py`

```python
class FileExtensions:
```

**Description:**
```
"""Supported file extensions for analysis."""

# Executables
PE: Final[list] = [".exe", ".dll", ".sys", ".scr"]
ELF: Final[list] = [".elf", ".so", ".bin"]
MACH_O: Final[list] = [".dylib", ".bundle"]

# Scripts
SCRIPTS: Final[list] = [".py", ".ps1", ".sh", ".bat", ".vbs", ".js"]

# Documents
OFFICE: Final[list] = [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]
PDF: Final[list] = [".pdf"]

# Archives
ARCHIVES: Final[list] = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"]
```

**Public Methods:**


---

### `RegexPatterns`

**File:** `constants.py`

```python
class RegexPatterns:
```

**Description:**
```
"""Common regex patterns for validation."""

# Network
IPV4: Final[str] = (
    r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)
IPV6: Final[str] = r"^(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|::1|::)$"
DOMAIN: Final[str] = (
    r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)
URL: Final[str] = r"^https?://[^\s/$.?#].[^\s]*$"
EMAIL: Final[str] = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Hashes
MD5: Final[str] = r"^[a-fA-F0-9]{32}$"
SHA1: Final[str] = r"^[a-fA-F0-9]{40}$"
```

**Public Methods:**


---

### `SystemLimits`

**File:** `constants.py`

```python
class SystemLimits:
```

**Description:**
```
"""System-wide limits and quotas."""

# Request Limits
MAX_REQUEST_SIZE: Final[int] = 100_000_000  # 100MB
MAX_FILE_UPLOAD: Final[int] = 500_000_000  # 500MB
MAX_BATCH_SIZE: Final[int] = 1000

# Rate Limits (per minute)
RATE_LIMIT_DEFAULT: Final[int] = 100
RATE_LIMIT_ANALYSIS: Final[int] = 10
RATE_LIMIT_SCAN: Final[int] = 5

# Pagination
PAGE_SIZE_DEFAULT: Final[int] = 50
PAGE_SIZE_MAX: Final[int] = 1000
```

**Public Methods:**


---

### `LogLevels`

**File:** `constants.py`

```python
class LogLevels:
```

**Description:**
```
"""Logging levels."""

DEBUG: Final[str] = "DEBUG"
INFO: Final[str] = "INFO"
WARNING: Final[str] = "WARNING"
ERROR: Final[str] = "ERROR"
CRITICAL: Final[str] = "CRITICAL"


# ============================================================================
# ENVIRONMENT NAMES
# ============================================================================


class Environments:
"""Environment names."""
```

**Public Methods:**


---

### `Environments`

**File:** `constants.py`

```python
class Environments:
```

**Description:**
```
"""Environment names."""

DEVELOPMENT: Final[str] = "development"
STAGING: Final[str] = "staging"
PRODUCTION: Final[str] = "production"
TESTING: Final[str] = "testing"


# ============================================================================
# USER ROLES - RBAC
# ============================================================================


class UserRoles:
"""User roles for Role-Based Access Control."""
```

**Public Methods:**


---

### `UserRoles`

**File:** `constants.py`

```python
class UserRoles:
```

**Description:**
```
"""User roles for Role-Based Access Control."""

ADMIN: Final[str] = "admin"
SOC_ANALYST: Final[str] = "soc_analyst"
SECURITY_ENGINEER: Final[str] = "security_engineer"
INCIDENT_RESPONDER: Final[str] = "incident_responder"
THREAT_HUNTER: Final[str] = "threat_hunter"
READ_ONLY: Final[str] = "read_only"


# Export all constants
__all__ = [
"ServicePorts",
"APIEndpoints",
"ResponseCodes",
"ThreatLevels",
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

### `ContainerStatus`

**File:** `container_health.py`

```python
class ContainerStatus(str, Enum):
```

**Description:**
```
"""Docker container status"""

RUNNING = "running"
PAUSED = "paused"
RESTARTING = "restarting"
REMOVING = "removing"
EXITED = "exited"
DEAD = "dead"
CREATED = "created"
UNKNOWN = "unknown"


class HealthStatus(str, Enum):
"""Container health check status"""

HEALTHY = "healthy"
```

**Public Methods:**


---

### `HealthStatus`

**File:** `container_health.py`

```python
class HealthStatus(str, Enum):
```

**Description:**
```
"""Container health check status"""

HEALTHY = "healthy"
UNHEALTHY = "unhealthy"
STARTING = "starting"
NONE = "none"  # No healthcheck defined


class ContainerMetrics(BaseModel):
"""Container resource metrics"""

cpu_percent: float | None = Field(None, ge=0.0, le=100.0)
memory_usage_mb: float | None = Field(None, ge=0.0)
memory_limit_mb: float | None = Field(None, ge=0.0)
memory_percent: float | None = Field(None, ge=0.0, le=100.0)
network_rx_mb: float | None = Field(None, ge=0.0)
```

**Public Methods:**


---

### `ContainerMetrics`

**File:** `container_health.py`

```python
class ContainerMetrics(BaseModel):
```

**Description:**
```
"""Container resource metrics"""

cpu_percent: float | None = Field(None, ge=0.0, le=100.0)
memory_usage_mb: float | None = Field(None, ge=0.0)
memory_limit_mb: float | None = Field(None, ge=0.0)
memory_percent: float | None = Field(None, ge=0.0, le=100.0)
network_rx_mb: float | None = Field(None, ge=0.0)
network_tx_mb: float | None = Field(None, ge=0.0)
block_read_mb: float | None = Field(None, ge=0.0)
block_write_mb: float | None = Field(None, ge=0.0)


class ContainerInfo(BaseModel):
"""Complete container information"""

id: str = Field(..., description="Container ID")
```

**Public Methods:**


---

### `ContainerInfo`

**File:** `container_health.py`

```python
class ContainerInfo(BaseModel):
```

**Description:**
```
"""Complete container information"""

id: str = Field(..., description="Container ID")
name: str = Field(..., description="Container name")
image: str = Field(..., description="Image name")
status: ContainerStatus
health: HealthStatus
uptime_seconds: int | None = Field(None, ge=0)
restart_count: int = Field(default=0, ge=0)
ports: dict[str, list[str]] = Field(default_factory=dict)
labels: dict[str, str] = Field(default_factory=dict)
metrics: ContainerMetrics | None = None
last_log_lines: list[str] = Field(default_factory=list)


class ClusterHealth(BaseModel):
```

**Public Methods:**


---

### `ClusterHealth`

**File:** `container_health.py`

```python
class ClusterHealth(BaseModel):
```

**Description:**
```
"""Overall cluster health summary"""

timestamp: datetime = Field(default_factory=datetime.utcnow)
total_containers: int = Field(..., ge=0)
running_containers: int = Field(..., ge=0)
healthy_containers: int = Field(..., ge=0)
unhealthy_containers: int = Field(..., ge=0)
stopped_containers: int = Field(..., ge=0)
total_cpu_percent: float = Field(..., ge=0.0)
total_memory_mb: float = Field(..., ge=0.0)
containers: list[ContainerInfo]


class ContainerHealthMonitor:
"""
Docker container health monitoring service.
```

**Public Methods:**


---

### `ContainerHealthMonitor`

**File:** `container_health.py`

```python
class ContainerHealthMonitor:
```

**Description:**
```
"""
Docker container health monitoring service.

Collects real-time metrics, status, and logs from all containers.
Designed for MAXIMUS distributed consciousness infrastructure.
"""

def __init__(self, docker_url: str = "unix://var/run/docker.sock"):
    """
    Initialize health monitor.

    Args:
        docker_url: Docker daemon socket URL
    """
    self.client = docker.DockerClient(base_url=docker_url)
```

**Public Methods:**

- `def close(self)`

---

### `ServiceStatus`

**File:** `enums.py`

```python
class ServiceStatus(str, Enum):
```

**Description:**
```
"""Health check status for microservices."""

HEALTHY = "healthy"
DEGRADED = "degraded"
UNHEALTHY = "unhealthy"
STARTING = "starting"
STOPPING = "stopping"
DOWN = "down"
MAINTENANCE = "maintenance"
UNKNOWN = "unknown"


class AnalysisStatus(str, Enum):
"""Status for asynchronous analysis jobs."""

PENDING = "pending"
```

**Public Methods:**


---

### `AnalysisStatus`

**File:** `enums.py`

```python
class AnalysisStatus(str, Enum):
```

**Description:**
```
"""Status for asynchronous analysis jobs."""

PENDING = "pending"
QUEUED = "queued"
RUNNING = "running"
COMPLETED = "completed"
FAILED = "failed"
CANCELLED = "cancelled"
TIMEOUT = "timeout"
PARTIAL = "partial"  # Partially completed with errors


class ScanStatus(str, Enum):
"""Status for security scans (port, vulnerability, malware)."""

PENDING = "pending"
```

**Public Methods:**


---

### `ScanStatus`

**File:** `enums.py`

```python
class ScanStatus(str, Enum):
```

**Description:**
```
"""Status for security scans (port, vulnerability, malware)."""

PENDING = "pending"
SCHEDULED = "scheduled"
RUNNING = "running"
COMPLETED = "completed"
FAILED = "failed"
CANCELLED = "cancelled"
PAUSED = "paused"
RESUMING = "resuming"


# ============================================================================
# THREAT & SECURITY ENUMS
# ============================================================================
```

**Public Methods:**


---

### `ThreatLevel`

**File:** `enums.py`

```python
class ThreatLevel(str, Enum):
```

**Description:**
```
"""Threat severity levels (NIST 800-61 aligned)."""

CRITICAL = "critical"  # Active exploitation, immediate action required
HIGH = "high"  # Confirmed threat, urgent response needed
MEDIUM = "medium"  # Potential threat, timely investigation
LOW = "low"  # Minimal risk, routine monitoring
INFO = "info"  # Informational, no action needed
UNKNOWN = "unknown"  # Insufficient data for classification


class ThreatType(str, Enum):
"""Types of cybersecurity threats."""

MALWARE = "malware"
RANSOMWARE = "ransomware"
PHISHING = "phishing"
```

**Public Methods:**


---

### `ThreatType`

**File:** `enums.py`

```python
class ThreatType(str, Enum):
```

**Description:**
```
"""Types of cybersecurity threats."""

MALWARE = "malware"
RANSOMWARE = "ransomware"
PHISHING = "phishing"
SPEAR_PHISHING = "spear_phishing"
APT = "apt"  # Advanced Persistent Threat
ZERO_DAY = "zero_day"
DDOS = "ddos"
BRUTE_FORCE = "brute_force"
SQL_INJECTION = "sql_injection"
XSS = "xss"  # Cross-Site Scripting
CSRF = "csrf"  # Cross-Site Request Forgery
MAN_IN_THE_MIDDLE = "mitm"
PRIVILEGE_ESCALATION = "privilege_escalation"
DATA_EXFILTRATION = "data_exfiltration"
```

**Public Methods:**


---

### `MalwareFamily`

**File:** `enums.py`

```python
class MalwareFamily(str, Enum):
```

**Description:**
```
"""Malware classification by family/type."""

TROJAN = "trojan"
WORM = "worm"
VIRUS = "virus"
ROOTKIT = "rootkit"
BACKDOOR = "backdoor"
SPYWARE = "spyware"
ADWARE = "adware"
RANSOMWARE = "ransomware"
KEYLOGGER = "keylogger"
RAT = "rat"  # Remote Access Trojan
BOTNET_CLIENT = "botnet_client"
CRYPTOMINER = "cryptominer"
DROPPER = "dropper"
LOADER = "loader"
```

**Public Methods:**


---

### `AttackTactic`

**File:** `enums.py`

```python
class AttackTactic(str, Enum):
```

**Description:**
```
"""MITRE ATT&CK Tactics (14 tactics from Enterprise Matrix)."""

RECONNAISSANCE = "reconnaissance"  # TA0043
RESOURCE_DEVELOPMENT = "resource_development"  # TA0042
INITIAL_ACCESS = "initial_access"  # TA0001
EXECUTION = "execution"  # TA0002
PERSISTENCE = "persistence"  # TA0003
PRIVILEGE_ESCALATION = "privilege_escalation"  # TA0004
DEFENSE_EVASION = "defense_evasion"  # TA0005
CREDENTIAL_ACCESS = "credential_access"  # TA0006
DISCOVERY = "discovery"  # TA0007
LATERAL_MOVEMENT = "lateral_movement"  # TA0008
COLLECTION = "collection"  # TA0009
COMMAND_AND_CONTROL = "command_and_control"  # TA0011
EXFILTRATION = "exfiltration"  # TA0010
IMPACT = "impact"  # TA0040
```

**Public Methods:**


---

### `AttackTechnique`

**File:** `enums.py`

```python
class AttackTechnique(str, Enum):
```

**Description:**
```
"""Sample MITRE ATT&CK Techniques (subset of 200+ techniques)."""

# Initial Access
T1566_PHISHING = "T1566"
T1190_EXPLOIT_PUBLIC_APP = "T1190"
T1133_EXTERNAL_REMOTE_SERVICES = "T1133"

# Execution
T1059_COMMAND_SCRIPTING = "T1059"
T1203_EXPLOITATION_FOR_CLIENT = "T1203"

# Persistence
T1543_CREATE_MODIFY_SYSTEM = "T1543"
T1547_BOOT_AUTOSTART = "T1547"

# Privilege Escalation
```

**Public Methods:**


---

### `IncidentStatus`

**File:** `enums.py`

```python
class IncidentStatus(str, Enum):
```

**Description:**
```
"""Incident response workflow states (NIST 800-61)."""

NEW = "new"
TRIAGED = "triaged"
INVESTIGATING = "investigating"
CONTAINED = "contained"
ERADICATING = "eradicating"
RECOVERING = "recovering"
RESOLVED = "resolved"
CLOSED = "closed"
FALSE_POSITIVE = "false_positive"
ESCALATED = "escalated"


class AlertPriority(str, Enum):
"""Alert priority for SOC triage (P0-P4 scale)."""
```

**Public Methods:**


---

### `AlertPriority`

**File:** `enums.py`

```python
class AlertPriority(str, Enum):
```

**Description:**
```
"""Alert priority for SOC triage (P0-P4 scale)."""

P0_CRITICAL = "p0_critical"  # Active breach, immediate response (SLA: 15min)
P1_HIGH = "p1_high"  # Confirmed threat, urgent (SLA: 1h)
P2_MEDIUM = "p2_medium"  # Potential threat, timely (SLA: 4h)
P3_LOW = "p3_low"  # Low risk, routine (SLA: 24h)
P4_INFO = "p4_info"  # Informational, no SLA


class EvidenceType(str, Enum):
"""Types of digital forensic evidence."""

NETWORK_TRAFFIC = "network_traffic"
SYSTEM_LOG = "system_log"
MEMORY_DUMP = "memory_dump"
DISK_IMAGE = "disk_image"
```

**Public Methods:**


---

### `EvidenceType`

**File:** `enums.py`

```python
class EvidenceType(str, Enum):
```

**Description:**
```
"""Types of digital forensic evidence."""

NETWORK_TRAFFIC = "network_traffic"
SYSTEM_LOG = "system_log"
MEMORY_DUMP = "memory_dump"
DISK_IMAGE = "disk_image"
FILE_SAMPLE = "file_sample"
REGISTRY_HIVE = "registry_hive"
BROWSER_ARTIFACT = "browser_artifact"
EMAIL = "email"
SCREENSHOT = "screenshot"
PACKET_CAPTURE = "packet_capture"
TIMELINE = "timeline"
HASH = "hash"
YARA_RULE = "yara_rule"
IOC = "ioc"  # Indicator of Compromise
```

**Public Methods:**


---

### `AssetType`

**File:** `enums.py`

```python
class AssetType(str, Enum):
```

**Description:**
```
"""Asset classification for inventory."""

SERVER = "server"
WORKSTATION = "workstation"
LAPTOP = "laptop"
MOBILE = "mobile"
NETWORK_DEVICE = "network_device"
IOT_DEVICE = "iot_device"
CONTAINER = "container"
VIRTUAL_MACHINE = "virtual_machine"
CLOUD_INSTANCE = "cloud_instance"
DATABASE = "database"
APPLICATION = "application"
WEB_SERVICE = "web_service"
UNKNOWN = "unknown"
```

**Public Methods:**


---

### `ProtocolType`

**File:** `enums.py`

```python
class ProtocolType(str, Enum):
```

**Description:**
```
"""Network protocols for traffic analysis."""

TCP = "tcp"
UDP = "udp"
ICMP = "icmp"
HTTP = "http"
HTTPS = "https"
DNS = "dns"
FTP = "ftp"
SSH = "ssh"
SMTP = "smtp"
TELNET = "telnet"
RDP = "rdp"
SMB = "smb"
SNMP = "snmp"
LDAP = "ldap"
```

**Public Methods:**


---

### `IPVersion`

**File:** `enums.py`

```python
class IPVersion(str, Enum):
```

**Description:**
```
"""IP protocol version."""

IPV4 = "ipv4"
IPV6 = "ipv6"


# ============================================================================
# DATA & COMPLIANCE ENUMS
# ============================================================================


class DataClassification(str, Enum):
"""Data sensitivity levels for DLP."""

PUBLIC = "public"
INTERNAL = "internal"
```

**Public Methods:**


---

### `DataClassification`

**File:** `enums.py`

```python
class DataClassification(str, Enum):
```

**Description:**
```
"""Data sensitivity levels for DLP."""

PUBLIC = "public"
INTERNAL = "internal"
CONFIDENTIAL = "confidential"
RESTRICTED = "restricted"
PII = "pii"  # Personally Identifiable Information
PHI = "phi"  # Protected Health Information
PCI = "pci"  # Payment Card Industry data
SECRET = "secret"
TOP_SECRET = "top_secret"


class ComplianceFramework(str, Enum):
"""Regulatory compliance frameworks."""
```

**Public Methods:**


---

### `ComplianceFramework`

**File:** `enums.py`

```python
class ComplianceFramework(str, Enum):
```

**Description:**
```
"""Regulatory compliance frameworks."""

GDPR = "gdpr"  # General Data Protection Regulation
LGPD = "lgpd"  # Lei Geral de Proteção de Dados (Brazil)
HIPAA = "hipaa"  # Health Insurance Portability
PCI_DSS = "pci_dss"  # Payment Card Industry
SOC2 = "soc2"  # Service Organization Control 2
ISO27001 = "iso27001"  # Information Security Management
NIST_CSF = "nist_csf"  # NIST Cybersecurity Framework
CIS = "cis"  # Center for Internet Security
FEDRAMP = "fedramp"  # Federal Risk Authorization
CMMC = "cmmc"  # Cybersecurity Maturity Model


# ============================================================================
# API & APPLICATION ENUMS
```

**Public Methods:**


---

### `ResponseStatus`

**File:** `enums.py`

```python
class ResponseStatus(str, Enum):
```

**Description:**
```
"""Standardized API response status codes."""

SUCCESS = "success"
ERROR = "error"
WARNING = "warning"
PARTIAL_SUCCESS = "partial_success"
VALIDATION_ERROR = "validation_error"
AUTHENTICATION_ERROR = "authentication_error"
AUTHORIZATION_ERROR = "authorization_error"
NOT_FOUND = "not_found"
RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
TIMEOUT = "timeout"
INTERNAL_ERROR = "internal_error"


class UserRole(str, Enum):
```

**Public Methods:**


---

### `UserRole`

**File:** `enums.py`

```python
class UserRole(str, Enum):
```

**Description:**
```
"""Role-Based Access Control (RBAC) roles."""

SUPERADMIN = "superadmin"  # Full system access
ADMIN = "admin"  # Administrative access
SOC_ANALYST = "soc_analyst"  # Security Operations Center
SECURITY_ENGINEER = "security_engineer"
INCIDENT_RESPONDER = "incident_responder"
THREAT_HUNTER = "threat_hunter"
COMPLIANCE_OFFICER = "compliance_officer"
AUDITOR = "auditor"  # Read-only audit access
USER = "user"  # Standard user
READONLY = "readonly"  # Read-only access
GUEST = "guest"  # Limited guest access


class Permission(str, Enum):
```

**Public Methods:**


---

### `Permission`

**File:** `enums.py`

```python
class Permission(str, Enum):
```

**Description:**
```
"""Granular permission types for RBAC."""

READ = "read"
WRITE = "write"
DELETE = "delete"
EXECUTE = "execute"
ADMIN = "admin"
AUDIT = "audit"


# ============================================================================
# AI & ANALYSIS ENUMS
# ============================================================================


class AnalysisEngine(str, Enum):
```

**Public Methods:**


---

### `AnalysisEngine`

**File:** `enums.py`

```python
class AnalysisEngine(str, Enum):
```

**Description:**
```
"""AI/ML analysis engines in Vértice platform."""

MAXIMUS_CORE = "maximus_core"  # Central AI reasoning
MAXIMUS_ORACULO = "maximus_oraculo"  # Self-improvement
MAXIMUS_PREDICT = "maximus_predict"  # Predictive analytics
NARRATIVE_FILTER = "narrative_filter"  # Misinformation detection
IMMUNIS_MACROPHAGE = "immunis_macrophage"  # YARA malware detection
REFLEX_TRIAGE = "reflex_triage"  # Automated triage
HCL_ANALYZER = "hcl_analyzer"  # Homeostatic Control Loop
STATIC_ANALYZER = "static_analyzer"
DYNAMIC_ANALYZER = "dynamic_analyzer"
BEHAVIORAL_ANALYZER = "behavioral_analyzer"


class ConfidenceLevel(str, Enum):
"""Confidence level for AI/ML predictions."""
```

**Public Methods:**


---

### `ConfidenceLevel`

**File:** `enums.py`

```python
class ConfidenceLevel(str, Enum):
```

**Description:**
```
"""Confidence level for AI/ML predictions."""

VERY_HIGH = "very_high"  # >95% confidence
HIGH = "high"  # 80-95%
MEDIUM = "medium"  # 60-80%
LOW = "low"  # 40-60%
VERY_LOW = "very_low"  # <40%
UNKNOWN = "unknown"


class DetectionMethod(str, Enum):
"""Method used for threat detection."""

SIGNATURE = "signature"  # Known signatures (YARA, Snort)
HEURISTIC = "heuristic"  # Behavior-based heuristics
ANOMALY = "anomaly"  # Statistical anomaly detection
```

**Public Methods:**


---

### `DetectionMethod`

**File:** `enums.py`

```python
class DetectionMethod(str, Enum):
```

**Description:**
```
"""Method used for threat detection."""

SIGNATURE = "signature"  # Known signatures (YARA, Snort)
HEURISTIC = "heuristic"  # Behavior-based heuristics
ANOMALY = "anomaly"  # Statistical anomaly detection
MACHINE_LEARNING = "machine_learning"
RULE_BASED = "rule_based"
CORRELATION = "correlation"  # Event correlation
THREAT_INTEL = "threat_intel"  # Threat intelligence feeds
SANDBOX = "sandbox"  # Dynamic analysis in sandbox
MANUAL = "manual"  # Manual investigation


# ============================================================================
# WORKFLOW & AUTOMATION ENUMS
# ============================================================================
```

**Public Methods:**


---

### `AutomationAction`

**File:** `enums.py`

```python
class AutomationAction(str, Enum):
```

**Description:**
```
"""Automated response actions."""

ALERT = "alert"
BLOCK_IP = "block_ip"
BLOCK_DOMAIN = "block_domain"
QUARANTINE_FILE = "quarantine_file"
KILL_PROCESS = "kill_process"
ISOLATE_HOST = "isolate_host"
DISABLE_ACCOUNT = "disable_account"
RESET_PASSWORD = "reset_password"
SNAPSHOT_MEMORY = "snapshot_memory"
COLLECT_EVIDENCE = "collect_evidence"
NOTIFY_SOC = "notify_soc"
ESCALATE = "escalate"
NONE = "none"
```

**Public Methods:**


---

### `QueuePriority`

**File:** `enums.py`

```python
class QueuePriority(str, Enum):
```

**Description:**
```
"""Task queue priority levels."""

CRITICAL = "critical"  # Priority 0 - immediate
HIGH = "high"  # Priority 1
NORMAL = "normal"  # Priority 2 (default)
LOW = "low"  # Priority 3
BACKGROUND = "background"  # Priority 4 - best effort


# ============================================================================
# OSINT & THREAT INTEL ENUMS
# ============================================================================


class OSINTSource(str, Enum):
"""Open Source Intelligence sources."""
```

**Public Methods:**


---

### `OSINTSource`

**File:** `enums.py`

```python
class OSINTSource(str, Enum):
```

**Description:**
```
"""Open Source Intelligence sources."""

VIRUSTOTAL = "virustotal"
ABUSEIPDB = "abuseipdb"
SHODAN = "shodan"
CENSYS = "censys"
GREYNOISE = "greynoise"
ALIENVAULT_OTX = "alienvault_otx"
MISP = "misp"
THREATFOX = "threatfox"
URLHAUS = "urlhaus"
MALWAREBAZAAR = "malwarebazaar"
HYBRID_ANALYSIS = "hybrid_analysis"
ANY_RUN = "any_run"
TWITTER = "twitter"
GITHUB = "github"
```

**Public Methods:**


---

### `ReputationScore`

**File:** `enums.py`

```python
class ReputationScore(str, Enum):
```

**Description:**
```
"""Reputation scoring for IPs, domains, files."""

MALICIOUS = "malicious"  # Confirmed malicious
SUSPICIOUS = "suspicious"  # High risk indicators
NEUTRAL = "neutral"  # No reputation data
TRUSTED = "trusted"  # Known good
WHITELISTED = "whitelisted"  # Explicitly trusted
UNKNOWN = "unknown"


# ============================================================================
# LOGGING & MONITORING ENUMS
# ============================================================================


class LogLevel(str, Enum):
```

**Public Methods:**


---

### `LogLevel`

**File:** `enums.py`

```python
class LogLevel(str, Enum):
```

**Description:**
```
"""Logging severity levels (Python logging standard)."""

DEBUG = "debug"
INFO = "info"
WARNING = "warning"
ERROR = "error"
CRITICAL = "critical"


class MetricType(str, Enum):
"""Types of performance metrics."""

COUNTER = "counter"
GAUGE = "gauge"
HISTOGRAM = "histogram"
SUMMARY = "summary"
```

**Public Methods:**


---

### `MetricType`

**File:** `enums.py`

```python
class MetricType(str, Enum):
```

**Description:**
```
"""Types of performance metrics."""

COUNTER = "counter"
GAUGE = "gauge"
HISTOGRAM = "histogram"
SUMMARY = "summary"


# ============================================================================
# EXPORT CONVENIENCE
# ============================================================================

__all__ = [
# Service & System
"ServiceStatus",
"AnalysisStatus",
```

**Public Methods:**


---

### `VerticeException`

**File:** `exceptions.py`

```python
class VerticeException(Exception):
```

**Description:**
```
"""Base exception for all Vértice platform custom exceptions.

All custom exceptions inherit from this class, providing consistent
error handling with rich context information.

Attributes:
    message: Human-readable error message
    error_code: Machine-readable error code for API responses
    status_code: HTTP status code (for FastAPI error handlers)
    details: Additional context and metadata about the error
"""

def __init__(
    self,
    message: str,
    error_code: str = "VERTICE_ERROR",
```

**Public Methods:**

- `def context(self) -> dict[str, Any]`

---

### `ValidationError`

**File:** `exceptions.py`

```python
class ValidationError(VerticeException):
```

**Description:**
```
"""Raised when input validation fails."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="VALIDATION_ERROR",
        status_code=400,
        details=details,
    )


class SchemaValidationError(ValidationError):
"""Raised when Pydantic schema validation fails."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(message=message, details=details)
```

**Public Methods:**


---

### `SchemaValidationError`

**File:** `exceptions.py`

```python
class SchemaValidationError(ValidationError):
```

**Description:**
```
"""Raised when Pydantic schema validation fails."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(message=message, details=details)
    self.error_code = "SCHEMA_VALIDATION_ERROR"


class InvalidInputError(ValidationError):
"""Raised when input parameters are invalid or malformed."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(message=message, details=details)
    self.error_code = "INVALID_INPUT"


class MissingFieldError(ValidationError):
```

**Public Methods:**


---

### `InvalidInputError`

**File:** `exceptions.py`

```python
class InvalidInputError(ValidationError):
```

**Description:**
```
"""Raised when input parameters are invalid or malformed."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(message=message, details=details)
    self.error_code = "INVALID_INPUT"


class MissingFieldError(ValidationError):
"""Raised when required fields are missing from request."""

def __init__(self, field_name: str, details: dict[str, Any] | None = None):
    message = f"Required field '{field_name}' is missing"
    super().__init__(message=message, details=details)
    self.error_code = "MISSING_FIELD"
```

**Public Methods:**


---

### `MissingFieldError`

**File:** `exceptions.py`

```python
class MissingFieldError(ValidationError):
```

**Description:**
```
"""Raised when required fields are missing from request."""

def __init__(self, field_name: str, details: dict[str, Any] | None = None):
    message = f"Required field '{field_name}' is missing"
    super().__init__(message=message, details=details)
    self.error_code = "MISSING_FIELD"


# ============================================================================
# SECURITY EXCEPTIONS
# ============================================================================


class SecurityException(VerticeException):
"""Base exception for security-related errors."""
```

**Public Methods:**


---

### `SecurityException`

**File:** `exceptions.py`

```python
class SecurityException(VerticeException):
```

**Description:**
```
"""Base exception for security-related errors."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=403, details=details
    )


class UnauthorizedError(SecurityException):
"""Raised when authentication fails or is missing."""

def __init__(
    self,
    message: str = "Authentication required",
```

**Public Methods:**


---

### `UnauthorizedError`

**File:** `exceptions.py`

```python
class UnauthorizedError(SecurityException):
```

**Description:**
```
"""Raised when authentication fails or is missing."""

def __init__(
    self,
    message: str = "Authentication required",
    details: dict[str, Any] | None = None,
):
    super().__init__(
        message=message,
        error_code="UNAUTHORIZED",
        details=details,
    )
    self.status_code = 401


class ForbiddenError(SecurityException):
```

**Public Methods:**


---

### `ForbiddenError`

**File:** `exceptions.py`

```python
class ForbiddenError(SecurityException):
```

**Description:**
```
"""Raised when user lacks required permissions."""

def __init__(
    self,
    message: str = "Insufficient permissions",
    details: dict[str, Any] | None = None,
):
    super().__init__(
        message=message,
        error_code="FORBIDDEN",
        details=details,
    )


class InvalidTokenError(UnauthorizedError):
"""Raised when authentication token is invalid or expired."""
```

**Public Methods:**


---

### `InvalidTokenError`

**File:** `exceptions.py`

```python
class InvalidTokenError(UnauthorizedError):
```

**Description:**
```
"""Raised when authentication token is invalid or expired."""

def __init__(
    self,
    message: str = "Invalid or expired token",
    details: dict[str, Any] | None = None,
):
    super().__init__(message=message, details=details)
    self.error_code = "INVALID_TOKEN"


class RateLimitExceeded(SecurityException):
"""Raised when API rate limit is exceeded."""

def __init__(
    self,
```

**Public Methods:**


---

### `RateLimitExceeded`

**File:** `exceptions.py`

```python
class RateLimitExceeded(SecurityException):
```

**Description:**
```
"""Raised when API rate limit is exceeded."""

def __init__(
    self,
    message: str = "Rate limit exceeded",
    details: dict[str, Any] | None = None,
):
    super().__init__(
        message=message,
        error_code="RATE_LIMIT_EXCEEDED",
        details=details,
    )
    self.status_code = 429


class SecurityViolationError(SecurityException):
```

**Public Methods:**


---

### `SecurityViolationError`

**File:** `exceptions.py`

```python
class SecurityViolationError(SecurityException):
```

**Description:**
```
"""Raised when a security policy is violated."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="SECURITY_VIOLATION",
        details=details,
    )


# ============================================================================
# SERVICE EXCEPTIONS
# ============================================================================


class ServiceException(VerticeException):
```

**Public Methods:**


---

### `ServiceException`

**File:** `exceptions.py`

```python
class ServiceException(VerticeException):
```

**Description:**
```
"""Base exception for service-level errors."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=503, details=details
    )


class ServiceUnavailableError(ServiceException):
"""Raised when a service is temporarily unavailable."""

def __init__(self, service_name: str, details: dict[str, Any] | None = None):
    message = f"Service '{service_name}' is currently unavailable"
    super().__init__(
```

**Public Methods:**


---

### `ServiceUnavailableError`

**File:** `exceptions.py`

```python
class ServiceUnavailableError(ServiceException):
```

**Description:**
```
"""Raised when a service is temporarily unavailable."""

def __init__(self, service_name: str, details: dict[str, Any] | None = None):
    message = f"Service '{service_name}' is currently unavailable"
    super().__init__(
        message=message,
        error_code="SERVICE_UNAVAILABLE",
        details=details,
    )


class ServiceTimeoutError(ServiceException):
"""Raised when a service request times out."""

def __init__(
    self,
```

**Public Methods:**


---

### `ServiceTimeoutError`

**File:** `exceptions.py`

```python
class ServiceTimeoutError(ServiceException):
```

**Description:**
```
"""Raised when a service request times out."""

def __init__(
    self,
    service_name: str,
    timeout_seconds: int,
    details: dict[str, Any] | None = None,
):
    message = f"Service '{service_name}' timed out after {timeout_seconds}s"
    super().__init__(
        message=message,
        error_code="SERVICE_TIMEOUT",
        details=details,
    )
    self.status_code = 504
```

**Public Methods:**


---

### `ServiceConfigurationError`

**File:** `exceptions.py`

```python
class ServiceConfigurationError(ServiceException):
```

**Description:**
```
"""Raised when service configuration is invalid or missing."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="SERVICE_CONFIGURATION_ERROR",
        details=details,
    )
    self.status_code = 500


# ============================================================================
# DATABASE EXCEPTIONS
# ============================================================================
```

**Public Methods:**


---

### `DatabaseException`

**File:** `exceptions.py`

```python
class DatabaseException(VerticeException):
```

**Description:**
```
"""Base exception for database-related errors."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=500, details=details
    )


class DatabaseConnectionError(DatabaseException):
"""Raised when database connection fails."""

def __init__(
    self,
    message: str = "Database connection failed",
```

**Public Methods:**


---

### `DatabaseConnectionError`

**File:** `exceptions.py`

```python
class DatabaseConnectionError(DatabaseException):
```

**Description:**
```
"""Raised when database connection fails."""

def __init__(
    self,
    message: str = "Database connection failed",
    details: dict[str, Any] | None = None,
):
    super().__init__(
        message=message,
        error_code="DATABASE_CONNECTION_ERROR",
        details=details,
    )


class DatabaseQueryError(DatabaseException):
"""Raised when a database query fails."""
```

**Public Methods:**


---

### `DatabaseQueryError`

**File:** `exceptions.py`

```python
class DatabaseQueryError(DatabaseException):
```

**Description:**
```
"""Raised when a database query fails."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="DATABASE_QUERY_ERROR",
        details=details,
    )


class DuplicateRecordError(DatabaseException):
"""Raised when attempting to create a duplicate record."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
```

**Public Methods:**


---

### `DuplicateRecordError`

**File:** `exceptions.py`

```python
class DuplicateRecordError(DatabaseException):
```

**Description:**
```
"""Raised when attempting to create a duplicate record."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="DUPLICATE_RECORD",
        details=details,
    )
    self.status_code = 409


class RecordNotFoundError(DatabaseException):
"""Raised when a database record is not found."""

def __init__(
    self,
```

**Public Methods:**


---

### `RecordNotFoundError`

**File:** `exceptions.py`

```python
class RecordNotFoundError(DatabaseException):
```

**Description:**
```
"""Raised when a database record is not found."""

def __init__(
    self,
    resource_type: str,
    resource_id: str,
    details: dict[str, Any] | None = None,
):
    message = f"{resource_type} with ID '{resource_id}' not found"
    super().__init__(
        message=message,
        error_code="RECORD_NOT_FOUND",
        details=details,
    )
    self.status_code = 404
```

**Public Methods:**


---

### `ExternalAPIException`

**File:** `exceptions.py`

```python
class ExternalAPIException(VerticeException):
```

**Description:**
```
"""Base exception for external API integration errors."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=502, details=details
    )


class ExternalAPIError(ExternalAPIException):
"""Raised when external API request fails."""

def __init__(
    self, api_name: str, status_code: int, details: dict[str, Any] | None = None
):
```

**Public Methods:**


---

### `ExternalAPIError`

**File:** `exceptions.py`

```python
class ExternalAPIError(ExternalAPIException):
```

**Description:**
```
"""Raised when external API request fails."""

def __init__(
    self, api_name: str, status_code: int, details: dict[str, Any] | None = None
):
    message = f"External API '{api_name}' returned error (status {status_code})"
    super().__init__(
        message=message,
        error_code="EXTERNAL_API_ERROR",
        details=details,
    )


class ExternalAPITimeoutError(ExternalAPIException):
"""Raised when external API request times out."""
```

**Public Methods:**


---

### `ExternalAPITimeoutError`

**File:** `exceptions.py`

```python
class ExternalAPITimeoutError(ExternalAPIException):
```

**Description:**
```
"""Raised when external API request times out."""

def __init__(self, api_name: str, details: dict[str, Any] | None = None):
    message = f"External API '{api_name}' request timed out"
    super().__init__(
        message=message,
        error_code="EXTERNAL_API_TIMEOUT",
        details=details,
    )
    self.status_code = 504


class APIQuotaExceededError(ExternalAPIException):
"""Raised when external API quota is exceeded."""

def __init__(self, api_name: str, details: dict[str, Any] | None = None):
```

**Public Methods:**


---

### `APIQuotaExceededError`

**File:** `exceptions.py`

```python
class APIQuotaExceededError(ExternalAPIException):
```

**Description:**
```
"""Raised when external API quota is exceeded."""

def __init__(self, api_name: str, details: dict[str, Any] | None = None):
    message = f"API quota exceeded for '{api_name}'"
    super().__init__(
        message=message,
        error_code="API_QUOTA_EXCEEDED",
        details=details,
    )
    self.status_code = 429


# ============================================================================
# BUSINESS LOGIC EXCEPTIONS
# ============================================================================
```

**Public Methods:**


---

### `BusinessLogicException`

**File:** `exceptions.py`

```python
class BusinessLogicException(VerticeException):
```

**Description:**
```
"""Base exception for business rule violations."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=422, details=details
    )


class InvalidOperationError(BusinessLogicException):
"""Raised when an operation violates business rules."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
```

**Public Methods:**


---

### `InvalidOperationError`

**File:** `exceptions.py`

```python
class InvalidOperationError(BusinessLogicException):
```

**Description:**
```
"""Raised when an operation violates business rules."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="INVALID_OPERATION",
        details=details,
    )


class StateTransitionError(BusinessLogicException):
"""Raised when an invalid state transition is attempted."""

def __init__(
    self,
    current_state: str,
```

**Public Methods:**


---

### `StateTransitionError`

**File:** `exceptions.py`

```python
class StateTransitionError(BusinessLogicException):
```

**Description:**
```
"""Raised when an invalid state transition is attempted."""

def __init__(
    self,
    current_state: str,
    attempted_state: str,
    details: dict[str, Any] | None = None,
):
    message = f"Cannot transition from '{current_state}' to '{attempted_state}'"
    super().__init__(
        message=message,
        error_code="INVALID_STATE_TRANSITION",
        details=details,
    )
```

**Public Methods:**


---

### `WorkflowException`

**File:** `exceptions.py`

```python
class WorkflowException(BusinessLogicException):
```

**Description:**
```
"""Raised when a workflow execution fails."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="WORKFLOW_ERROR",
        details=details,
    )


# ============================================================================
# RESOURCE EXCEPTIONS
# ============================================================================


class ResourceException(VerticeException):
```

**Public Methods:**


---

### `ResourceException`

**File:** `exceptions.py`

```python
class ResourceException(VerticeException):
```

**Description:**
```
"""Base exception for resource-related errors."""

def __init__(
    self,
    message: str,
    error_code: str,
    status_code: int,
    details: dict[str, Any] | None = None,
):
    super().__init__(
        message=message,
        error_code=error_code,
        status_code=status_code,
        details=details,
    )
```

**Public Methods:**


---

### `ResourceNotFoundError`

**File:** `exceptions.py`

```python
class ResourceNotFoundError(ResourceException):
```

**Description:**
```
"""Raised when a requested resource does not exist."""

def __init__(
    self,
    resource_type: str,
    identifier: str,
    details: dict[str, Any] | None = None,
):
    message = f"{resource_type} '{identifier}' not found"
    super().__init__(
        message=message,
        error_code="RESOURCE_NOT_FOUND",
        status_code=404,
        details=details,
    )
```

**Public Methods:**


---

### `ResourceConflictError`

**File:** `exceptions.py`

```python
class ResourceConflictError(ResourceException):
```

**Description:**
```
"""Raised when a resource operation conflicts with existing state."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="RESOURCE_CONFLICT",
        status_code=409,
        details=details,
    )


class ResourceExhaustedError(ResourceException):
"""Raised when system resources are exhausted."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
```

**Public Methods:**


---

### `ResourceExhaustedError`

**File:** `exceptions.py`

```python
class ResourceExhaustedError(ResourceException):
```

**Description:**
```
"""Raised when system resources are exhausted."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="RESOURCE_EXHAUSTED",
        status_code=429,
        details=details,
    )


class QuotaExceededError(ResourceException):
"""Raised when user quota is exceeded."""

def __init__(
    self, quota_type: str, limit: int, details: dict[str, Any] | None = None
```

**Public Methods:**


---

### `QuotaExceededError`

**File:** `exceptions.py`

```python
class QuotaExceededError(ResourceException):
```

**Description:**
```
"""Raised when user quota is exceeded."""

def __init__(
    self, quota_type: str, limit: int, details: dict[str, Any] | None = None
):
    message = f"Quota exceeded for '{quota_type}' (limit: {limit})"
    super().__init__(
        message=message,
        error_code="QUOTA_EXCEEDED",
        status_code=429,
        details=details,
    )


# ============================================================================
# ANALYSIS & AI EXCEPTIONS
```

**Public Methods:**


---

### `AnalysisException`

**File:** `exceptions.py`

```python
class AnalysisException(VerticeException):
```

**Description:**
```
"""Base exception for AI/ML analysis errors."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=500, details=details
    )


class AnalysisTimeoutError(AnalysisException):
"""Raised when analysis operation times out."""

def __init__(
    self,
    analysis_type: str,
```

**Public Methods:**


---

### `AnalysisTimeoutError`

**File:** `exceptions.py`

```python
class AnalysisTimeoutError(AnalysisException):
```

**Description:**
```
"""Raised when analysis operation times out."""

def __init__(
    self,
    analysis_type: str,
    timeout_seconds: int,
    details: dict[str, Any] | None = None,
):
    message = f"Analysis '{analysis_type}' timed out after {timeout_seconds}s"
    super().__init__(
        message=message,
        error_code="ANALYSIS_TIMEOUT",
        details=details,
    )
    self.status_code = 504
```

**Public Methods:**


---

### `ModelNotFoundError`

**File:** `exceptions.py`

```python
class ModelNotFoundError(AnalysisException):
```

**Description:**
```
"""Raised when a requested ML model is not found."""

def __init__(self, model_name: str, details: dict[str, Any] | None = None):
    message = f"AI model '{model_name}' not found or not loaded"
    super().__init__(
        message=message,
        error_code="MODEL_NOT_FOUND",
        details=details,
    )
    self.status_code = 404


class InsufficientDataError(AnalysisException):
"""Raised when insufficient data is available for analysis."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
```

**Public Methods:**


---

### `InsufficientDataError`

**File:** `exceptions.py`

```python
class InsufficientDataError(AnalysisException):
```

**Description:**
```
"""Raised when insufficient data is available for analysis."""

def __init__(self, message: str, details: dict[str, Any] | None = None):
    super().__init__(
        message=message,
        error_code="INSUFFICIENT_DATA",
        details=details,
    )
    self.status_code = 422


# ============================================================================
# MALWARE & THREAT EXCEPTIONS
# ============================================================================
```

**Public Methods:**


---

### `ThreatException`

**File:** `exceptions.py`

```python
class ThreatException(VerticeException):
```

**Description:**
```
"""Base exception for threat detection and analysis errors."""

def __init__(
    self, message: str, error_code: str, details: dict[str, Any] | None = None
):
    super().__init__(
        message=message, error_code=error_code, status_code=500, details=details
    )


class MalwareDetectedError(ThreatException):
"""Raised when malware is detected (blocking operation)."""

def __init__(
    self,
    malware_type: str,
```

**Public Methods:**


---

### `MalwareDetectedError`

**File:** `exceptions.py`

```python
class MalwareDetectedError(ThreatException):
```

**Description:**
```
"""Raised when malware is detected (blocking operation)."""

def __init__(
    self,
    malware_type: str,
    file_hash: str,
    details: dict[str, Any] | None = None,
):
    message = f"Malware detected: {malware_type} (hash: {file_hash})"
    super().__init__(
        message=message,
        error_code="MALWARE_DETECTED",
        details=details,
    )
    self.status_code = 403
```

**Public Methods:**


---

### `ScanFailedError`

**File:** `exceptions.py`

```python
class ScanFailedError(ThreatException):
```

**Description:**
```
"""Raised when a security scan fails."""

def __init__(self, scan_type: str, details: dict[str, Any] | None = None):
    message = f"Scan failed: {scan_type}"
    super().__init__(
        message=message,
        error_code="SCAN_FAILED",
        details=details,
    )


# ============================================================================
# EXPORT ALL EXCEPTIONS
# ============================================================================

__all__ = [
```

**Public Methods:**


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

### `ToolCategory`

**File:** `maximus_integration.py`

```python
class ToolCategory(str, Enum):
```

**Description:**
```
"""Tool categories for MAXIMUS integration."""

BROWSER = "browser"  # MABA tools
VISION = "vision"  # MVP tools
HEALING = "healing"  # PENELOPE tools
ANALYSIS = "analysis"
AUTOMATION = "automation"


class RiskLevel(str, Enum):
"""Risk levels for HITL decision requests."""

LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
CRITICAL = "CRITICAL"
```

**Public Methods:**


---

### `RiskLevel`

**File:** `maximus_integration.py`

```python
class RiskLevel(str, Enum):
```

**Description:**
```
"""Risk levels for HITL decision requests."""

LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
CRITICAL = "CRITICAL"


class MaximusIntegrationMixin:
"""
Mixin class providing MAXIMUS integration utilities.

This mixin should be used by subordinate services to register tools,
submit decisions to HITL, and maintain integration with MAXIMUS Core.

Usage:
```

**Public Methods:**


---

### `MaximusIntegrationMixin`

**File:** `maximus_integration.py`

```python
class MaximusIntegrationMixin:
```

**Description:**
```
"""
Mixin class providing MAXIMUS integration utilities.

This mixin should be used by subordinate services to register tools,
submit decisions to HITL, and maintain integration with MAXIMUS Core.

Usage:
    class MABAService(SubordinateServiceBase, MaximusIntegrationMixin):
        async def initialize(self):
            await self.register_tools_with_maximus(self.get_tool_manifest())
"""

async def register_tools_with_maximus(self, tools: list[dict[str, Any]]) -> bool:
    """
    Register tools with MAXIMUS Core.
```

**Public Methods:**

- `def create_tool_definition(`

---

### `EventRouter`

**File:** `event_router.py`

```python
class EventRouter:
```

**Description:**
```
"""
Intelligent event router for cross-system integration.

Routes and transforms events between:
- Reactive Fabric → Active Immune Core
- Active Immune Core → Reactive Fabric
- Both → Monitoring/Analytics

Applies business logic for routing decisions.
"""

def __init__(self):
    """Initialize event router."""
    self.events_routed = 0
    self.events_dropped = 0
    self.routing_rules: dict[EventTopic, dict[str, Any]] = {}
```

**Public Methods:**

- `def should_trigger_immune_response(`
- `def determine_immune_response_type(`
- `def enrich_threat_with_context(`
- `def transform_immune_response_for_reactive_fabric(`
- `def get_metrics(self) -> dict[str, Any]`

---

### `EventPriority`

**File:** `event_schemas.py`

```python
class EventPriority(str, Enum):
```

**Description:**
```
"""Event priority levels"""

LOW = "low"
NORMAL = "normal"
HIGH = "high"
CRITICAL = "critical"


class EventSource(str, Enum):
"""Event source services"""

REACTIVE_FABRIC = "reactive_fabric_core"
IMMUNE_SYSTEM = "active_immune_core"
ADAPTIVE_IMMUNE = "adaptive_immune_system"
MAXIMUS_CORE = "maximus_core_service"
API_GATEWAY = "api_gateway"
```

**Public Methods:**


---

### `EventSource`

**File:** `event_schemas.py`

```python
class EventSource(str, Enum):
```

**Description:**
```
"""Event source services"""

REACTIVE_FABRIC = "reactive_fabric_core"
IMMUNE_SYSTEM = "active_immune_core"
ADAPTIVE_IMMUNE = "adaptive_immune_system"
MAXIMUS_CORE = "maximus_core_service"
API_GATEWAY = "api_gateway"
MONITORING = "monitoring"


class SeverityLevel(str, Enum):
"""Threat severity levels"""

LOW = "low"
MEDIUM = "medium"
HIGH = "high"
```

**Public Methods:**


---

### `SeverityLevel`

**File:** `event_schemas.py`

```python
class SeverityLevel(str, Enum):
```

**Description:**
```
"""Threat severity levels"""

LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"


class EventBase(BaseModel):
"""
Base event schema for all ecosystem events.

All events must inherit from this base class to ensure
consistency and traceability.
"""
```

**Public Methods:**


---

### `EventBase`

**File:** `event_schemas.py`

```python
class EventBase(BaseModel):
```

**Description:**
```
"""
Base event schema for all ecosystem events.

All events must inherit from this base class to ensure
consistency and traceability.
"""

event_id: str = Field(default_factory=lambda: str(uuid4()))
event_type: str = Field(..., description="Event type identifier")
timestamp: datetime = Field(default_factory=datetime.utcnow)
source_service: EventSource = Field(..., description="Service that generated event")
priority: EventPriority = Field(default=EventPriority.NORMAL)
correlation_id: str | None = Field(None, description="For event chain tracing")
metadata: dict[str, Any] = Field(default_factory=dict)

class Config:
```

**Public Methods:**


---

### `ThreatDetectionEvent`

**File:** `event_schemas.py`

```python
class ThreatDetectionEvent(EventBase):
```

**Description:**
```
"""
Threat detected by Reactive Fabric honeypot.

Published to: maximus.threats.detected
Consumed by: Active Immune Core, SIEM, Analytics
"""

event_type: str = "threat.detected"
source_service: EventSource = EventSource.REACTIVE_FABRIC

# Threat details
honeypot_id: str = Field(..., description="Honeypot that detected threat")
honeypot_type: str = Field(..., description="Type of honeypot (ssh, http, etc)")
attacker_ip: str = Field(..., description="Attacker IP address")
attacker_port: int | None = None
attack_type: str = Field(..., description="Type of attack")
```

**Public Methods:**


---

### `HoneypotStatusEvent`

**File:** `event_schemas.py`

```python
class HoneypotStatusEvent(EventBase):
```

**Description:**
```
"""
Honeypot status change event.

Published to: maximus.honeypots.status
Consumed by: Monitoring, Reactive Fabric orchestrator
"""

event_type: str = "honeypot.status_change"
source_service: EventSource = EventSource.REACTIVE_FABRIC

honeypot_id: str
honeypot_type: str
status: str = Field(..., description="online, offline, degraded")
previous_status: str | None = None
uptime_seconds: int | None = None
error_message: str | None = None
```

**Public Methods:**


---

### `ImmuneResponseEvent`

**File:** `event_schemas.py`

```python
class ImmuneResponseEvent(EventBase):
```

**Description:**
```
"""
Immune system response to threat.

Published to: maximus.immune.responses
Consumed by: Reactive Fabric, Monitoring, Analytics
"""

event_type: str = "immune.response"
source_service: EventSource = EventSource.IMMUNE_SYSTEM

threat_id: str = Field(..., description="Original threat event ID")
responder_agent_id: str = Field(..., description="Agent that responded")
responder_agent_type: str = Field(..., description="nk_cell, neutrophil, etc")

response_action: str = Field(..., description="isolate, neutralize, observe")
response_status: str = Field(..., description="success, failed, partial")
```

**Public Methods:**


---

### `ClonalExpansionEvent`

**File:** `event_schemas.py`

```python
class ClonalExpansionEvent(EventBase):
```

**Description:**
```
"""
Clonal expansion event (adaptive immune response).

Published to: maximus.immune.cloning
Consumed by: Monitoring, Analytics, Homeostatic controller
"""

event_type: str = "immune.clonal_expansion"
source_service: EventSource = EventSource.IMMUNE_SYSTEM

parent_agent_id: str
clone_ids: list[str] = Field(..., description="IDs of created clones")
num_clones: int
especializacao: str = Field(..., description="Threat signature specialization")
trigger_threat_id: str = Field(..., description="Threat that triggered expansion")
lymphnode_id: str
```

**Public Methods:**


---

### `HomeostaticStateEvent`

**File:** `event_schemas.py`

```python
class HomeostaticStateEvent(EventBase):
```

**Description:**
```
"""
Homeostatic state change event.

Published to: maximus.immune.homeostasis
Consumed by: All immune components, Monitoring
"""

event_type: str = "immune.homeostatic_change"
source_service: EventSource = EventSource.IMMUNE_SYSTEM

lymphnode_id: str
area: str = Field(..., description="Regional area")

old_state: str | None = None
new_state: str = Field(..., description="repouso, vigilancia, atencao, inflamacao")
```

**Public Methods:**

- `def validate_temperature(cls, v`

---

### `SystemHealthEvent`

**File:** `event_schemas.py`

```python
class SystemHealthEvent(EventBase):
```

**Description:**
```
"""
System-wide health metrics.

Published to: maximus.system.health
Consumed by: Monitoring, Grafana, Alert manager
"""

event_type: str = "system.health"
source_service: EventSource = Field(..., description="Service reporting health")

health_status: str = Field(..., description="healthy, degraded, critical")

# Metrics
total_agents: int | None = None
active_agents: int | None = None
threats_detected_total: int | None = None
```

**Public Methods:**


---

### `IntegrationEvent`

**File:** `event_schemas.py`

```python
class IntegrationEvent(EventBase):
```

**Description:**
```
"""
Cross-system integration event.

Published to: maximus.integration.*
Consumed by: Multiple systems
"""

event_type: str = "integration.event"

action: str = Field(..., description="Action being performed")
target_system: str = Field(..., description="Target system")
payload: dict[str, Any] = Field(default_factory=dict)
requires_ack: bool = Field(default=False)
```

**Public Methods:**


---

### `UnifiedKafkaClient`

**File:** `kafka_client.py`

```python
class UnifiedKafkaClient:
```

**Description:**
```
"""
Unified Kafka client for the Vértice ecosystem.

Features:
- Single client for producing and consuming
- Type-safe event publishing with Pydantic schemas
- Event handler registration with routing
- Automatic retries with exponential backoff
- Graceful degradation mode
- Metrics and monitoring

Usage:
    # Initialize
    client = UnifiedKafkaClient(
        bootstrap_servers="kafka:9092",
        service_name="my_service"
```

**Public Methods:**

- `def is_available(self) -> bool`
- `def get_metrics(self) -> dict[str, Any]`

---

### `EventTopic`

**File:** `topics.py`

```python
class EventTopic(str, Enum):
```

**Description:**
```
"""
Unified Kafka topics for Vértice MAXIMUS ecosystem.

Naming convention: maximus.<domain>.<entity>.<action>
"""

# Threat detection pipeline
THREATS_DETECTED = "maximus.threats.detected"
THREATS_ENRICHED = "maximus.threats.enriched"
THREATS_ANALYZED = "maximus.threats.analyzed"

# Immune system responses
IMMUNE_RESPONSES = "maximus.immune.responses"
IMMUNE_CLONING = "maximus.immune.cloning"
IMMUNE_HOMEOSTASIS = "maximus.immune.homeostasis"
IMMUNE_ALERTS = "maximus.immune.alerts"
```

**Public Methods:**


---

### `TopicConfig`

**File:** `topics.py`

```python
class TopicConfig(BaseModel):
```

**Description:**
```
"""Kafka topic configuration"""

name: str
partitions: int = 3
replication_factor: int = 3
retention_ms: int = 604800000  # 7 days
compression_type: str = "gzip"
cleanup_policy: str = "delete"
description: str = ""

# Routing
producers: list[str] = []  # Services that produce to this topic
consumers: list[str] = []  # Services that consume from this topic


# Topic configurations registry
```

**Public Methods:**


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

### `RateLimitConfig`

**File:** `rate_limiter.py`

```python
class RateLimitConfig:
```

**Description:**
```
"""Rate limit configuration."""

# Default limits (requests per window in seconds)
DEFAULT_REQUESTS = 100
DEFAULT_WINDOW = 60  # 60 seconds = 1 minute

# Per-endpoint limits (override defaults)
ENDPOINT_LIMITS = {
    "/api/scan": (10, 60),  # 10 req/min for scans
    "/api/malware/analyze": (5, 60),  # 5 req/min for malware analysis
    "/api/exploit": (3, 60),  # 3 req/min for exploits
    "/api/osint": (20, 60),  # 20 req/min for OSINT
    "/api/threat-intel": (50, 60),  # 50 req/min for threat intel
}

# Header names
```

**Public Methods:**


---

### `TokenBucket`

**File:** `rate_limiter.py`

```python
class TokenBucket:
```

**Description:**
```
"""
Token bucket algorithm for rate limiting.

How it works:
1. Bucket starts with max_tokens
2. Each request consumes 1 token
3. Tokens refill at rate: max_tokens / window_seconds
4. If no tokens available: request denied (429)

Example:
    10 requests / 60 seconds = 0.1666 tokens/second refill rate
    If 5 tokens left at t=0, at t=30 you have 10 tokens (refilled)
"""

def __init__(
    self, redis_client: Redis | None, key: str, max_tokens: int, window_seconds: int
```

**Public Methods:**

- `def consume(self, tokens`

---

### `RateLimiter`

**File:** `rate_limiter.py`

```python
class RateLimiter(BaseHTTPMiddleware):
```

**Description:**
```
"""
FastAPI middleware for API rate limiting.

Usage:
    app.add_middleware(
        RateLimiter,
        redis_url="redis://localhost:6379",
        enabled=True
    )
"""

def __init__(
    self,
    app: ASGIApp,
    redis_url: str = "redis://localhost:6379",
    enabled: bool = True,
```

**Public Methods:**

- `def decorator(func)`

---

### `APVBase`

**File:** `apv_legacy.py`

```python
class APVBase(BaseModel):
```

**Description:**
```
"""Base APV model with common fields."""

priority: int = Field(
    ..., ge=1, le=10, description="Priority level (1=critical, 10=low)"
)
vulnerable_code_signature: str | None = Field(
    None, description="Regex or AST pattern for code matching"
)
vulnerable_code_type: str | None = Field(
    None, description="Type: 'regex', 'ast-grep', 'semgrep'"
)
affected_files: list[str] | None = Field(
    default_factory=list, description="Potential affected files"
)
exploitation_difficulty: str | None = Field(
    None, description="Difficulty: 'easy', 'medium', 'hard'"
```

**Public Methods:**

- `def validate_code_type(cls, v`
- `def validate_difficulty(cls, v`

---

### `APVCreate`

**File:** `apv_legacy.py`

```python
class APVCreate(APVBase):
```

**Description:**
```
"""Create APV request model."""

threat_id: UUID = Field(..., description="Reference to threat (CVE)")
dependency_id: UUID = Field(..., description="Reference to dependency")
apv_code: str = Field(
    ..., max_length=50, description="Unique APV code (APV-YYYYMMDD-NNN)"
)

@field_validator("apv_code")
@classmethod
def validate_apv_code(cls, v: str) -> str:
    """Validate APV code format."""
    if not v.startswith("APV-"):
        raise ValueError("apv_code must start with 'APV-'")
    return v
```

**Public Methods:**

- `def validate_apv_code(cls, v`

---

### `APVUpdate`

**File:** `apv_legacy.py`

```python
class APVUpdate(BaseModel):
```

**Description:**
```
"""Update APV request model (all fields optional)."""

priority: int | None = Field(None, ge=1, le=10)
status: str | None = None
vulnerable_code_signature: str | None = None
vulnerable_code_type: str | None = None
affected_files: list[str] | None = None
exploitation_difficulty: str | None = None
exploitability_score: float | None = Field(None, ge=0.0, le=10.0)
requires_human_review: bool | None = None
dispatched_to_eureka_at: datetime | None = None
confirmed_at: datetime | None = None
human_decision: str | None = None
human_decision_by: str | None = None
human_decision_at: datetime | None = None
human_decision_notes: str | None = None
```

**Public Methods:**

- `def validate_status(cls, v`
- `def validate_human_decision(cls, v`

---

### `APVModel`

**File:** `apv_legacy.py`

```python
class APVModel(APVBase):
```

**Description:**
```
"""Complete APV model (for internal use)."""

id: UUID
threat_id: UUID
dependency_id: UUID
apv_code: str
status: str = "pending"
dispatched_to_eureka_at: datetime | None = None
confirmed_at: datetime | None = None
human_decision: str | None = None
human_decision_by: str | None = None
human_decision_at: datetime | None = None
human_decision_notes: str | None = None
created_at: datetime
updated_at: datetime
```

**Public Methods:**


---

### `ThreatSummary`

**File:** `apv_legacy.py`

```python
class ThreatSummary(BaseModel):
```

**Description:**
```
"""Threat summary for APV response."""

cve_id: str
title: str
severity: str | None = None
cvss_score: float | None = None

class Config:
    from_attributes = True


class DependencySummary(BaseModel):
"""Dependency summary for APV response."""

project_name: str
package_name: str
```

**Public Methods:**


---

### `DependencySummary`

**File:** `apv_legacy.py`

```python
class DependencySummary(BaseModel):
```

**Description:**
```
"""Dependency summary for APV response."""

project_name: str
package_name: str
package_version: str
ecosystem: str

class Config:
    from_attributes = True


class APVResponse(APVModel):
"""API response model for APV (includes related data)."""

threat: ThreatSummary | None = None
dependency: DependencySummary | None = None
```

**Public Methods:**


---

### `APVResponse`

**File:** `apv_legacy.py`

```python
class APVResponse(APVModel):
```

**Description:**
```
"""API response model for APV (includes related data)."""

threat: ThreatSummary | None = None
dependency: DependencySummary | None = None

class Config:
    from_attributes = True


class APVDispatchMessage(BaseModel):
"""
RabbitMQ message format for dispatching APV to Eureka.

This is the contract between Oráculo and Eureka services.
"""
```

**Public Methods:**


---

### `APVDispatchMessage`

**File:** `apv_legacy.py`

```python
class APVDispatchMessage(BaseModel):
```

**Description:**
```
"""
RabbitMQ message format for dispatching APV to Eureka.

This is the contract between Oráculo and Eureka services.
"""

apv_id: UUID = Field(..., description="APV unique identifier")
apv_code: str = Field(..., description="APV code (APV-YYYYMMDD-NNN)")
priority: int = Field(..., ge=1, le=10, description="Priority level")

# Threat information
cve_id: str = Field(..., description="CVE identifier")
cve_title: str = Field(..., description="CVE title")
cve_description: str = Field(..., description="CVE description")
cvss_score: float | None = Field(None, description="CVSS score")
severity: str | None = Field(None, description="Severity level")
```

**Public Methods:**


---

### `APVStatusUpdate`

**File:** `apv_legacy.py`

```python
class APVStatusUpdate(BaseModel):
```

**Description:**
```
"""
RabbitMQ message format for status updates from Eureka → Oráculo.
"""

apv_id: UUID = Field(..., description="APV unique identifier")
apv_code: str = Field(..., description="APV code")
status: str = Field(..., description="New status")
confirmed: bool = Field(
    default=False, description="Vulnerability confirmed by AST scan"
)
confirmation_details: dict | None = Field(None, description="AST scan results")
updated_by: str = Field(default="eureka", description="Service that updated status")
updated_at: datetime = Field(default_factory=datetime.utcnow)

@field_validator("status")
@classmethod
```

**Public Methods:**

- `def validate_status(cls, v`

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
severity: str = Field(
    ..., description="Severity: NONE, LOW, MEDIUM, HIGH, CRITICAL"
)
vector_string: str = Field(..., description="CVSS vector string")

# Optional detailed metrics
exploitability_score: float | None = Field(None, ge=0.0, le=10.0)
impact_score: float | None = Field(None, ge=0.0, le=10.0)
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
description: str | None = Field(None, description="Pattern explanation")

@field_validator("language")
@classmethod
def validate_language(cls, v: str) -> str:
    """Validate supported languages."""
    supported = ["python", "javascript", "typescript", "go", "rust", "java"]
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
affected_versions: list[str] = Field(..., description="Affected version ranges")
fixed_versions: list[str] = Field(
    default_factory=list, description="Fixed versions"
)

# Optional fields
purl: str | None = Field(None, description="Package URL (purl)")
introduced: str | None = Field(
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

- `def calculate_smart_defaults(self) -> "APV"`
- `def is_critical(self) -> bool`
- `def requires_immediate_action(self) -> bool`
- `def has_automated_fix(self) -> bool`
- `def affected_services(self) -> list[str]`
- `def to_kafka_message(self) -> dict[str, Any]`
- `def to_database_record(self) -> dict[str, Any]`

---

### `BaseResponse`

**File:** `response_models.py`

```python
class BaseResponse(BaseModel):
```

**Description:**
```
"""Base response model with common fields."""

success: bool = Field(..., description="Indicates if the request was successful")
timestamp: datetime = Field(
    default_factory=datetime.utcnow,
    description="Response timestamp in UTC",
)
request_id: str | None = Field(
    default=None, description="Unique request identifier for tracing"
)

class Config:
    json_encoders = {datetime: lambda v: v.isoformat() + "Z"}


# ============================================================================
```

**Public Methods:**


---

### `SuccessResponse`

**File:** `response_models.py`

```python
class SuccessResponse(BaseResponse, Generic[T]):
```

**Description:**
```
"""Standard success response with generic data payload.

Use this for single object responses (GET /resource/{id}, POST, PUT, PATCH).

Attributes:
    success: Always True for success responses
    data: The actual response payload (flexible type)
    message: Optional human-readable success message
    meta: Optional metadata (processing time, version, etc.)
"""

success: Literal[True] = Field(
    default=True, description="Always True for success responses"
)
data: T = Field(..., description="Response payload")
message: str | None = Field(
```

**Public Methods:**


---

### `ListResponse`

**File:** `response_models.py`

```python
class ListResponse(BaseResponse, Generic[T]):
```

**Description:**
```
"""Standard response for list/collection endpoints.

Use this for GET /resources (list endpoints).

Attributes:
    success: Always True for success responses
    data: List of items
    message: Optional success message
    meta: Metadata about the collection
    pagination: Pagination information (if applicable)
"""

success: Literal[True] = Field(
    default=True, description="Always True for success responses"
)
data: list[T] = Field(..., description="List of items")
```

**Public Methods:**


---

### `PaginationMeta`

**File:** `response_models.py`

```python
class PaginationMeta(BaseModel):
```

**Description:**
```
"""Pagination metadata for list responses.

Provides information about the current page, total items, and navigation.
"""

page: int = Field(..., ge=1, description="Current page number (1-indexed)")
page_size: int = Field(..., ge=1, description="Number of items per page")
total_items: int = Field(..., ge=0, description="Total number of items")
total_pages: int = Field(..., ge=0, description="Total number of pages")
has_next: bool = Field(..., description="Whether there is a next page")
has_previous: bool = Field(..., description="Whether there is a previous page")
next_page: int | None = Field(
    default=None, description="Next page number (if available)"
)
previous_page: int | None = Field(
    default=None, description="Previous page number (if available)"
```

**Public Methods:**

- `def from_params(`

---

### `CreatedResponse`

**File:** `response_models.py`

```python
class CreatedResponse(SuccessResponse[T]):
```

**Description:**
```
"""Response for resource creation (POST).

Extends SuccessResponse with 201 status code semantics.
"""

message: str = Field(default="Resource created successfully")


class UpdatedResponse(SuccessResponse[T]):
"""Response for resource update (PUT/PATCH).

Extends SuccessResponse for update operations.
"""

message: str = Field(default="Resource updated successfully")
```

**Public Methods:**


---

### `UpdatedResponse`

**File:** `response_models.py`

```python
class UpdatedResponse(SuccessResponse[T]):
```

**Description:**
```
"""Response for resource update (PUT/PATCH).

Extends SuccessResponse for update operations.
"""

message: str = Field(default="Resource updated successfully")


class DeletedResponse(BaseResponse):
"""Response for resource deletion (DELETE).

Typically returns no data, just success confirmation.
"""

success: Literal[True] = Field(
    default=True, description="Always True for success responses"
```

**Public Methods:**


---

### `DeletedResponse`

**File:** `response_models.py`

```python
class DeletedResponse(BaseResponse):
```

**Description:**
```
"""Response for resource deletion (DELETE).

Typically returns no data, just success confirmation.
"""

success: Literal[True] = Field(
    default=True, description="Always True for success responses"
)
message: str = Field(default="Resource deleted successfully")
meta: dict[str, Any] | None = Field(default=None)


# ============================================================================
# ERROR RESPONSES
# ============================================================================
```

**Public Methods:**


---

### `ErrorDetail`

**File:** `response_models.py`

```python
class ErrorDetail(BaseModel):
```

**Description:**
```
"""Detailed error information.

Provides structured error data for API consumers.
"""

code: str = Field(..., description="Machine-readable error code")
message: str = Field(..., description="Human-readable error message")
field: str | None = Field(
    default=None, description="Field name for validation errors"
)
details: dict[str, Any] | None = Field(
    default=None, description="Additional error context"
)


class ErrorResponse(BaseResponse):
```

**Public Methods:**


---

### `ErrorResponse`

**File:** `response_models.py`

```python
class ErrorResponse(BaseResponse):
```

**Description:**
```
"""Standard error response.

Use this for all error cases (400, 401, 403, 404, 500, etc.).

Attributes:
    success: Always False for error responses
    error: Structured error information
    errors: Optional list of multiple errors (e.g., validation)
"""

success: Literal[False] = Field(
    default=False, description="Always False for error responses"
)
error: ErrorDetail = Field(..., description="Primary error information")
errors: list[ErrorDetail] | None = Field(
    default=None, description="Additional errors (validation, etc.)"
```

**Public Methods:**


---

### `ValidationErrorResponse`

**File:** `response_models.py`

```python
class ValidationErrorResponse(ErrorResponse):
```

**Description:**
```
"""Response for validation errors (422).

Includes detailed field-level validation errors.
"""

def __init__(self, errors: list[dict[str, Any]], **kwargs):
    """Create validation error response from error list.

    Args:
        errors: List of validation errors from Pydantic
        **kwargs: Additional fields
    """
    error_details = [
        ErrorDetail(
            code="VALIDATION_ERROR",
            message=err.get("msg", "Validation failed"),
```

**Public Methods:**


---

### `HealthStatus`

**File:** `response_models.py`

```python
class HealthStatus(BaseModel):
```

**Description:**
```
"""Service health status."""

status: str = Field(..., description="Health status (healthy/degraded/unhealthy)")
checks: dict[str, bool] = Field(
    default_factory=dict, description="Individual health checks"
)
version: str | None = Field(default=None, description="Service version")
uptime_seconds: float | None = Field(default=None, description="Service uptime")


class HealthResponse(BaseResponse):
"""Response for /health endpoints."""

success: bool = Field(default=True)
data: HealthStatus = Field(..., description="Health status information")
```

**Public Methods:**


---

### `HealthResponse`

**File:** `response_models.py`

```python
class HealthResponse(BaseResponse):
```

**Description:**
```
"""Response for /health endpoints."""

success: bool = Field(default=True)
data: HealthStatus = Field(..., description="Health status information")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def success_response(
data: Any, message: str | None = None, meta: dict[str, Any] | None = None
) -> dict[str, Any]:
"""Helper function to create success response dict.
```

**Public Methods:**


---

### `HTTPStatusCode`

**File:** `response_models.py`

```python
class HTTPStatusCode:
```

**Description:**
```
"""Standard HTTP status codes for consistent usage."""

# Success
OK = 200  # General success
CREATED = 201  # Resource created
ACCEPTED = 202  # Request accepted, processing
NO_CONTENT = 204  # Success with no response body

# Client Errors
BAD_REQUEST = 400  # Invalid request
UNAUTHORIZED = 401  # Authentication required
FORBIDDEN = 403  # Insufficient permissions
NOT_FOUND = 404  # Resource not found
CONFLICT = 409  # Resource conflict (duplicate)
UNPROCESSABLE_ENTITY = 422  # Validation error
TOO_MANY_REQUESTS = 429  # Rate limit exceeded
```

**Public Methods:**


---

### `RateLimitStrategy`

**File:** `rate_limiter.py`

```python
class RateLimitStrategy(str, Enum):
```

**Description:**
```
"""Rate limiting algorithm strategy"""

TOKEN_BUCKET = "token_bucket"  # Allows bursts
SLIDING_WINDOW = "sliding_window"  # More precise
FIXED_WINDOW = "fixed_window"  # Simple, less accurate


class RateLimitExceeded(Exception):
"""Raised when rate limit is exceeded"""

def __init__(self, retry_after: float):
    self.retry_after = retry_after
    super().__init__(f"Rate limit exceeded. Retry after {retry_after:.2f}s")


@dataclass
```

**Public Methods:**


---

### `RateLimitExceeded`

**File:** `rate_limiter.py`

```python
class RateLimitExceeded(Exception):
```

**Description:**
```
"""Raised when rate limit is exceeded"""

def __init__(self, retry_after: float):
    self.retry_after = retry_after
    super().__init__(f"Rate limit exceeded. Retry after {retry_after:.2f}s")


@dataclass
class RateLimitConfig:
"""Configuration for rate limiter"""

max_requests: int = field(default=100)
window_seconds: int = field(default=60)
strategy: RateLimitStrategy = field(default=RateLimitStrategy.SLIDING_WINDOW)
burst_multiplier: float = field(default=1.5)  # For token bucket
```

**Public Methods:**


---

### `RateLimitConfig`

**File:** `rate_limiter.py`

```python
class RateLimitConfig:
```

**Description:**
```
"""Configuration for rate limiter"""

max_requests: int = field(default=100)
window_seconds: int = field(default=60)
strategy: RateLimitStrategy = field(default=RateLimitStrategy.SLIDING_WINDOW)
burst_multiplier: float = field(default=1.5)  # For token bucket


@dataclass
class RateLimiter:
"""
Multi-strategy rate limiter with Redis backend.

Supports token bucket (burst-friendly) and sliding window (precise)
algorithms. Falls back to in-memory if Redis unavailable.
```

**Public Methods:**


---

### `RateLimiter`

**File:** `rate_limiter.py`

```python
class RateLimiter:
```

**Description:**
```
"""
Multi-strategy rate limiter with Redis backend.

Supports token bucket (burst-friendly) and sliding window (precise)
algorithms. Falls back to in-memory if Redis unavailable.

Attributes:
    config: Rate limit configuration
    redis_url: Redis connection URL (optional)
    key_prefix: Prefix for Redis keys
"""

config: RateLimitConfig
redis_url: str | None = None
key_prefix: str = "ratelimit"
```

**Public Methods:**


---

### `VulnerabilitySeverity`

**File:** `vulnerability_scanner.py`

```python
class VulnerabilitySeverity(str, Enum):
```

**Description:**
```
"""CVSSv3 severity classification"""

CRITICAL = "critical"  # 9.0-10.0
HIGH = "high"  # 7.0-8.9
MEDIUM = "medium"  # 4.0-6.9
LOW = "low"  # 0.1-3.9
UNKNOWN = "unknown"


class VulnerabilityRecord(BaseModel):
"""Individual vulnerability finding"""

package: str = Field(..., description="Vulnerable package name")
version: str = Field(..., description="Installed version")
vulnerability_id: str = Field(..., description="CVE-ID or advisory ID")
severity: VulnerabilitySeverity
```

**Public Methods:**


---

### `VulnerabilityRecord`

**File:** `vulnerability_scanner.py`

```python
class VulnerabilityRecord(BaseModel):
```

**Description:**
```
"""Individual vulnerability finding"""

package: str = Field(..., description="Vulnerable package name")
version: str = Field(..., description="Installed version")
vulnerability_id: str = Field(..., description="CVE-ID or advisory ID")
severity: VulnerabilitySeverity
cvss_score: float | None = Field(None, ge=0.0, le=10.0)
description: str
fix_available: bool = Field(default=False)
fixed_in: str | None = Field(None, description="First fixed version")
scanner: str = Field(..., description="Scanner that detected this")


class ScanResult(BaseModel):
"""Complete vulnerability scan result"""
```

**Public Methods:**


---

### `ScanResult`

**File:** `vulnerability_scanner.py`

```python
class ScanResult(BaseModel):
```

**Description:**
```
"""Complete vulnerability scan result"""

timestamp: datetime = Field(default_factory=datetime.utcnow)
total_packages: int = Field(..., ge=0)
vulnerable_packages: int = Field(..., ge=0)
vulnerabilities: list[VulnerabilityRecord] = Field(default_factory=list)
severity_breakdown: dict[VulnerabilitySeverity, int] = Field(default_factory=dict)
scan_duration_seconds: float = Field(..., ge=0.0)
scanners_used: list[str] = Field(default_factory=list)
scan_passed: bool = Field(..., description="No critical/high vulnerabilities found")


@dataclass
class VulnerabilityScanner:
"""
Multi-scanner vulnerability detection system.
```

**Public Methods:**


---

### `VulnerabilityScanner`

**File:** `vulnerability_scanner.py`

```python
class VulnerabilityScanner:
```

**Description:**
```
"""
Multi-scanner vulnerability detection system.

Orchestrates safety, pip-audit, and potentially Trivy for comprehensive
dependency vulnerability detection across Python ecosystem.

Attributes:
    requirements_path: Path to requirements.txt
    ignore_ids: CVE IDs to ignore (false positives, accepted risks)
    fail_on_severity: Minimum severity to fail the scan
"""

requirements_path: Path = field(default_factory=lambda: Path("requirements.txt"))
ignore_ids: list[str] = field(default_factory=list)
fail_on_severity: VulnerabilitySeverity = VulnerabilitySeverity.HIGH
```

**Public Methods:**


---

### `ServiceHealthStatus`

**File:** `subordinate_service.py`

```python
class ServiceHealthStatus:
```

**Description:**
```
"""Health status constants for subordinate services."""

HEALTHY = "healthy"
DEGRADED = "degraded"
UNHEALTHY = "unhealthy"
INITIALIZING = "initializing"


class SubordinateServiceBase(ABC):
"""
Base class for all MAXIMUS subordinate services.

All subordinate services must implement this interface to ensure
proper integration with MAXIMUS Core and the Vértice Platform.

Attributes:
```

**Public Methods:**


---

### `SubordinateServiceBase`

**File:** `subordinate_service.py`

```python
class SubordinateServiceBase(ABC):
```

**Description:**
```
"""
Base class for all MAXIMUS subordinate services.

All subordinate services must implement this interface to ensure
proper integration with MAXIMUS Core and the Vértice Platform.

Attributes:
    service_name: Unique service identifier (e.g., "maba", "mvp", "penelope")
    service_version: Semantic version string
    maximus_endpoint: URL to MAXIMUS Core Service
    _running: Service running state
    _initialized: Service initialization state
    _http_client: Shared HTTP client for MAXIMUS communication
"""

# Prometheus metrics (shared across all subordinate services)
```

**Public Methods:**

- `def get_uptime_seconds(self) -> float`
- `def is_healthy(self) -> bool`

---

### `ThalamusClient`

**File:** `thalamus_client.py`

```python
class ThalamusClient:
```

**Description:**
```
"""HTTP client for submitting sensory data to Digital Thalamus.

Attributes:
    thalamus_url: Base URL of Digital Thalamus service
    sensor_id: Unique identifier for this sensor
    sensor_type: Type of sensor (visual, auditory, etc.)
    client: HTTP client instance
"""

def __init__(
    self, thalamus_url: str, sensor_id: str, sensor_type: str, timeout: float = 10.0
):
    """Initialize Thalamus client.

    Args:
        thalamus_url: Base URL of Digital Thalamus (e.g., http://digital_thalamus_service:8012)
```

**Public Methods:**


---

### `ToolStatus`

**File:** `tool_protocol.py`

```python
class ToolStatus(str, Enum):
```

**Description:**
```
"""Tool execution status."""

SUCCESS = "success"
FAILED = "failed"
TIMEOUT = "timeout"
CANCELLED = "cancelled"
PENDING = "pending"


class ToolParameterType(str, Enum):
"""Supported parameter types."""

STRING = "string"
INTEGER = "integer"
NUMBER = "number"
BOOLEAN = "boolean"
```

**Public Methods:**


---

### `ToolParameterType`

**File:** `tool_protocol.py`

```python
class ToolParameterType(str, Enum):
```

**Description:**
```
"""Supported parameter types."""

STRING = "string"
INTEGER = "integer"
NUMBER = "number"
BOOLEAN = "boolean"
OBJECT = "object"
ARRAY = "array"


class ToolParameter(BaseModel):
"""
Tool parameter definition.

Attributes:
    name: Parameter name
```

**Public Methods:**


---

### `ToolParameter`

**File:** `tool_protocol.py`

```python
class ToolParameter(BaseModel):
```

**Description:**
```
"""
Tool parameter definition.

Attributes:
    name: Parameter name
    type: Parameter type
    description: Human-readable description
    required: Whether parameter is required
    default: Default value if not provided
    enum: List of allowed values (optional)
"""

name: str = Field(..., description="Parameter name")
type: ToolParameterType = Field(..., description="Parameter type")
description: str = Field(..., description="Parameter description")
required: bool = Field(default=False, description="Whether parameter is required")
```

**Public Methods:**


---

### `ToolInvocationRequest`

**File:** `tool_protocol.py`

```python
class ToolInvocationRequest(BaseModel):
```

**Description:**
```
"""
Tool invocation request.

Attributes:
    tool_name: Name of the tool to invoke
    parameters: Tool parameters
    request_id: Unique request identifier
    source_service: Service requesting the tool
    timeout_seconds: Execution timeout
"""

tool_name: str = Field(..., description="Tool name")
parameters: dict[str, Any] = Field(
    default_factory=dict, description="Tool parameters"
)
request_id: str | None = Field(default=None, description="Request ID")
```

**Public Methods:**

- `def validate_timeout(cls, v)`

---

### `ToolInvocationResponse`

**File:** `tool_protocol.py`

```python
class ToolInvocationResponse(BaseModel):
```

**Description:**
```
"""
Tool invocation response.

Attributes:
    status: Execution status
    result: Tool result (if successful)
    error: Error message (if failed)
    execution_time_ms: Execution time in milliseconds
    request_id: Original request ID
    timestamp: Response timestamp
"""

status: ToolStatus = Field(..., description="Execution status")
result: dict[str, Any] | None = Field(default=None, description="Tool result")
error: str | None = Field(default=None, description="Error message")
execution_time_ms: float = Field(..., description="Execution time in milliseconds")
```

**Public Methods:**

- `def error_requires_failed_status(cls, v, info)`

---

### `ToolBase`

**File:** `tool_protocol.py`

```python
class ToolBase(ABC):
```

**Description:**
```
"""
Base class for all MAXIMUS tools.

All tools must inherit from this class and implement the execute() method.
Tools are automatically registered with MAXIMUS and can be invoked via API.

Attributes:
    name: Unique tool identifier
    description: Human-readable description
    parameters: List of parameter definitions
    category: Tool category
    service_name: Service providing this tool
"""

# Prometheus metrics
invocations_total = Counter(
```

**Public Methods:**

- `def get_manifest(self) -> dict[str, Any]`

---

### `VaultConfig`

**File:** `vault_client.py`

```python
class VaultConfig:
```

**Description:**
```
"""Vault client configuration."""

# Vault server URL
ADDR = os.getenv("VAULT_ADDR", "http://localhost:8200")

# Authentication (AppRole)
ROLE_ID = os.getenv("VAULT_ROLE_ID")
SECRET_ID = os.getenv("VAULT_SECRET_ID")

# Or direct token (for dev/testing)
TOKEN = os.getenv("VAULT_TOKEN")

# Secrets path prefix
MOUNT_POINT = "vertice"

# Cache TTL (seconds)
```

**Public Methods:**


---

### `VaultClient`

**File:** `vault_client.py`

```python
class VaultClient:
```

**Description:**
```
"""
Client for HashiCorp Vault.

Handles authentication, token renewal, and secret retrieval.
"""

def __init__(
    self,
    addr: str | None = None,
    role_id: str | None = None,
    secret_id: str | None = None,
    token: str | None = None,
):
    self.addr = addr or VaultConfig.ADDR
    self.role_id = role_id or VaultConfig.ROLE_ID
    self.secret_id = secret_id or VaultConfig.SECRET_ID
```

**Public Methods:**

- `def get_secret(`
- `def set_secret(self, path`
- `def delete_secret(self, path`
- `def list_secrets(self, path`

---

### `DeploymentStage`

**File:** `vertice_canary.py`

```python
class DeploymentStage(Enum):
```

**Description:**
```
"""Canary deployment stages"""

BLUE = "blue"  # Current stable version
GREEN = "green"  # New version (0% traffic)
CANARY_5 = "canary_5"  # 5% traffic
CANARY_25 = "canary_25"  # 25% traffic
CANARY_50 = "canary_50"  # 50% traffic
CANARY_100 = "canary_100"  # 100% traffic (promoted)
ROLLBACK = "rollback"  # Rolled back to blue


@dataclass
class ServiceVersion:
"""Service version information"""

service_name: str
```

**Public Methods:**


---

### `ServiceVersion`

**File:** `vertice_canary.py`

```python
class ServiceVersion:
```

**Description:**
```
"""Service version information"""

service_name: str
version: str
endpoint: str
health_endpoint: str
deployed_at: float
error_rate: float = 0.0
request_count: int = 0
avg_latency_ms: float = 0.0


class CanaryDeploymentManager:
"""
Manages canary deployments with progressive traffic shifting.
```

**Public Methods:**


---

### `CanaryDeploymentManager`

**File:** `vertice_canary.py`

```python
class CanaryDeploymentManager:
```

**Description:**
```
"""
Manages canary deployments with progressive traffic shifting.

Usage:
    manager = CanaryDeploymentManager()
    manager.register_blue("my-service", "v1.0", "http://service-v1:8000")
    manager.register_green("my-service", "v2.0", "http://service-v2:8000")

    # Start canary with 5% traffic
    manager.start_canary("my-service")

    # Gradually promote if healthy
    manager.promote_canary("my-service")  # 5% → 25%
    manager.promote_canary("my-service")  # 25% → 50%
    manager.promote_canary("my-service")  # 50% → 100%
"""
```

**Public Methods:**

- `def register_blue(`
- `def register_green(`
- `def start_canary(self, service_name`
- `def promote_canary(self, service_name`
- `def rollback(self, service_name`
- `def get_endpoint(self, service_name`
- `def get_version_info(self, service_name`
- `def update_metrics(`

---

### `RegistryClient`

**File:** `vertice_registry_client.py`

```python
class RegistryClient:
```

**Description:**
```
"""Client for interacting with Vértice Service Registry."""

_http_client: httpx.AsyncClient | None = None

@classmethod
def _get_client(cls) -> httpx.AsyncClient:
    """Get or create HTTP client (singleton)."""
    if cls._http_client is None or cls._http_client.is_closed:
        cls._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(REGISTRATION_TIMEOUT), follow_redirects=True
        )
    return cls._http_client

@classmethod
def _get_headers(cls) -> dict[str, str]:
    """Return default headers for registry communication."""
```

**Public Methods:**


---

### `TracedOperation`

**File:** `vertice_tracing.py`

```python
class TracedOperation:
```

**Description:**
```
"""
Context manager for creating traced operations.

Usage:
    with TracedOperation("database_query", {"db.table": "users"}):
        # Your code here
        pass
"""

def __init__(self, span_name: str, attributes: dict[str, Any] | None = None):
    self.span_name = span_name
    self.attributes = attributes or {}
    self.span: Span | None = None

def __enter__(self):
    tracer = get_tracer()
```

**Public Methods:**


---

### `AsyncTracedOperation`

**File:** `vertice_tracing.py`

```python
class AsyncTracedOperation:
```

**Description:**
```
"""
Async context manager for creating traced operations.

Usage:
    async with AsyncTracedOperation("async_operation"):
        await some_async_function()
"""

def __init__(self, span_name: str, attributes: dict[str, Any] | None = None):
    self.span_name = span_name
    self.attributes = attributes or {}
    self.span: Span | None = None

async def __aenter__(self):
    tracer = get_tracer()
    self.span = tracer.start_span(self.span_name)
```

**Public Methods:**


---

### `MessageType`

**File:** `websocket_gateway.py`

```python
class MessageType(str, Enum):
```

**Description:**
```
"""WebSocket message types"""

# Client → Server
PING = "ping"
SUBSCRIBE = "subscribe"
UNSUBSCRIBE = "unsubscribe"

# Server → Client
PONG = "pong"
SUBSCRIBED = "subscribed"
UNSUBSCRIBED = "unsubscribed"

# Data streams
CONTAINER_STATUS = "container_status"
OSINT_PROGRESS = "osint_progress"
MAXIMUS_STREAM = "maximus_stream"
```

**Public Methods:**


---

### `Channel`

**File:** `websocket_gateway.py`

```python
class Channel(str, Enum):
```

**Description:**
```
"""Pub/Sub channels"""

CONTAINERS = "maximus:containers"
OSINT = "maximus:osint"
MAXIMUS_AI = "maximus:ai"
TASKS = "maximus:tasks"
THREATS = "maximus:threats"
CONSCIOUSNESS = "maximus:consciousness"
SYSTEM = "maximus:system"


class WebSocketMessage(BaseModel):
"""Standard WebSocket message format"""

type: MessageType
channel: Channel | None = None
```

**Public Methods:**


---

### `WebSocketMessage`

**File:** `websocket_gateway.py`

```python
class WebSocketMessage(BaseModel):
```

**Description:**
```
"""Standard WebSocket message format"""

type: MessageType
channel: Channel | None = None
data: dict | None = None
timestamp: datetime = Field(default_factory=datetime.utcnow)
client_id: str | None = None


class ConnectionManager:
"""
Manages WebSocket connections with Redis Pub/Sub integration.

Handles client connections, subscriptions, and message broadcasting
across distributed MAXIMUS instances.
"""
```

**Public Methods:**


---

### `ConnectionManager`

**File:** `websocket_gateway.py`

```python
class ConnectionManager:
```

**Description:**
```
"""
Manages WebSocket connections with Redis Pub/Sub integration.

Handles client connections, subscriptions, and message broadcasting
across distributed MAXIMUS instances.
"""

def __init__(self, redis_url: str | None = None):
    self.active_connections: dict[str, WebSocket] = {}
    self.subscriptions: dict[str, set[Channel]] = {}
    self.redis_url = redis_url
    self.redis_client: aioredis.Redis | None = None
    self.pubsub: aioredis.client.PubSub | None = None
    self._running = False

async def start(self):
```

**Public Methods:**

- `def disconnect(self, client_id`

---

### `MABAMessageType`

**File:** `websocket_routes.py`

```python
class MABAMessageType(str, Enum):
```

**Description:**
```
"""MABA-specific WebSocket message types"""

# Client → Server
PING = "ping"
SUBSCRIBE = "subscribe"
UNSUBSCRIBE = "unsubscribe"

# Server → Client
PONG = "pong"
SUBSCRIBED = "subscribed"
UNSUBSCRIBED = "unsubscribed"

# MABA Events
SESSION_CREATED = "session_created"  # New browser session
SESSION_CLOSED = "session_closed"  # Session terminated
PAGE_NAVIGATED = "page_navigated"  # Navegated to new page
```

**Public Methods:**


---

### `MABAChannel`

**File:** `websocket_routes.py`

```python
class MABAChannel(str, Enum):
```

**Description:**
```
"""MABA subscription channels"""

SESSIONS = "maba:sessions"
NAVIGATION = "maba:navigation"
COGNITIVE_MAP = "maba:cognitive_map"
LEARNING = "maba:learning"
SCREENSHOTS = "maba:screenshots"
STATS = "maba:stats"
ALL = "maba:all"


class MABAWebSocketMessage(BaseModel):
"""MABA WebSocket message format"""

type: MABAMessageType
channel: MABAChannel | None = None
```

**Public Methods:**


---

### `MABAWebSocketMessage`

**File:** `websocket_routes.py`

```python
class MABAWebSocketMessage(BaseModel):
```

**Description:**
```
"""MABA WebSocket message format"""

type: MABAMessageType
channel: MABAChannel | None = None
data: dict | None = None
timestamp: datetime = Field(default_factory=datetime.utcnow)


class MABAConnectionManager:
"""
Manages MABA WebSocket connections.

Handles client connections, subscriptions, and real-time event broadcasting
for browser sessions, navigation, and cognitive map updates.
"""
```

**Public Methods:**


---

### `MABAConnectionManager`

**File:** `websocket_routes.py`

```python
class MABAConnectionManager:
```

**Description:**
```
"""
Manages MABA WebSocket connections.

Handles client connections, subscriptions, and real-time event broadcasting
for browser sessions, navigation, and cognitive map updates.
"""

def __init__(self):
    self.active_connections: dict[str, WebSocket] = {}
    self.subscriptions: dict[str, set[MABAChannel]] = {}

async def connect(self, client_id: str, websocket: WebSocket):
    """Register new WebSocket connection"""
    await websocket.accept()
    self.active_connections[client_id] = websocket
    self.subscriptions[client_id] = set()
```

**Public Methods:**

- `def disconnect(self, client_id`

---

## 4. Data Models

### `test_response_models.py`

### `response_models.py`

#### `BaseResponse`

```python
    success: bool = Field(..., description="Indicates if the request was successful")
    timestamp: datetime = Field(
    request_id: str | None = Field(
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() + "Z"}
    Attributes:
        success: Always True for success responses
        data: The actual response payload (flexible type)
        message: Optional human-readable success message
        meta: Optional metadata (processing time, version, etc.)
    success: Literal[True] = Field(
    data: T = Field(..., description="Response payload")
    message: str | None = Field(
    meta: dict[str, Any] | None = Field(default=None, description="Additional metadata")
```

#### `PaginationMeta`

```python
    page: int = Field(..., ge=1, description="Current page number (1-indexed)")
    page_size: int = Field(..., ge=1, description="Number of items per page")
    total_items: int = Field(..., ge=0, description="Total number of items")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")
    next_page: int | None = Field(
    previous_page: int | None = Field(
        cls, page: int, page_size: int, total_items: int
    ) -> "PaginationMeta":
        Args:
            page: Current page number (1-indexed)
            page_size: Items per page
            total_items: Total number of items available
        Returns:
```

#### `ErrorDetail`

```python
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    field: str | None = Field(
    details: dict[str, Any] | None = Field(
    Attributes:
        success: Always False for error responses
        error: Structured error information
        errors: Optional list of multiple errors (e.g., validation)
    success: Literal[False] = Field(
    error: ErrorDetail = Field(..., description="Primary error information")
    errors: list[ErrorDetail] | None = Field(
```

#### `HealthStatus`

```python
    status: str = Field(..., description="Health status (healthy/degraded/unhealthy)")
    checks: dict[str, bool] = Field(
    version: str | None = Field(default=None, description="Service version")
    uptime_seconds: float | None = Field(default=None, description="Service uptime")
    success: bool = Field(default=True)
    data: HealthStatus = Field(..., description="Health status information")
    data: Any, message: str | None = None, meta: dict[str, Any] | None = None
) -> dict[str, Any]:
    Args:
        data: Response data
        message: Optional success message
        meta: Optional metadata
    Returns:
    data: list[Any],
```

### `test_models.py`

### `models.py`

#### `NavigationRequest`

```python
    url: str = Field(..., description="Target URL")
    wait_until: str = Field(
    timeout_ms: int = Field(
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
    selector: str = Field(..., description="CSS selector for element to click")
    button: str = Field(
    click_count: int = Field(default=1, description="Number of clicks")
    timeout_ms: int = Field(default=30000, description="Timeout in milliseconds")
    selector: str = Field(..., description="CSS selector for element")
    text: str = Field(..., description="Text to type")
    delay_ms: int = Field(
```

#### `ClickRequest`

```python
    selector: str = Field(..., description="CSS selector for element to click")
    button: str = Field(
    click_count: int = Field(default=1, description="Number of clicks")
    timeout_ms: int = Field(default=30000, description="Timeout in milliseconds")
    selector: str = Field(..., description="CSS selector for element")
    text: str = Field(..., description="Text to type")
    delay_ms: int = Field(
    full_page: bool = Field(default=False, description="Capture full scrollable page")
    selector: str | None = Field(
    format: str = Field(default="png", description="Image format (png, jpeg)")
    selectors: dict[str, str] = Field(
    extract_all: bool = Field(
```

#### `TypeRequest`

```python
    selector: str = Field(..., description="CSS selector for element")
    text: str = Field(..., description="Text to type")
    delay_ms: int = Field(
    full_page: bool = Field(default=False, description="Capture full scrollable page")
    selector: str | None = Field(
    format: str = Field(default="png", description="Image format (png, jpeg)")
    selectors: dict[str, str] = Field(
    extract_all: bool = Field(
    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport_width: int = Field(default=1920, description="Viewport width")
    viewport_height: int = Field(default=1080, description="Viewport height")
    user_agent: str | None = Field(default=None, description="Custom user agent")
```

#### `ScreenshotRequest`

```python
    full_page: bool = Field(default=False, description="Capture full scrollable page")
    selector: str | None = Field(
    format: str = Field(default="png", description="Image format (png, jpeg)")
    selectors: dict[str, str] = Field(
    extract_all: bool = Field(
    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport_width: int = Field(default=1920, description="Viewport width")
    viewport_height: int = Field(default=1080, description="Viewport height")
    user_agent: str | None = Field(default=None, description="Custom user agent")
    action: BrowserAction = Field(..., description="Action to perform")
    parameters: dict[str, Any] = Field(
    session_id: str | None = Field(default=None, description="Browser session ID")
```

#### `ExtractRequest`

```python
    selectors: dict[str, str] = Field(
    extract_all: bool = Field(
    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport_width: int = Field(default=1920, description="Viewport width")
    viewport_height: int = Field(default=1080, description="Viewport height")
    user_agent: str | None = Field(default=None, description="Custom user agent")
    action: BrowserAction = Field(..., description="Action to perform")
    parameters: dict[str, Any] = Field(
    session_id: str | None = Field(default=None, description="Browser session ID")
    status: str = Field(..., description="Action status")
    result: dict[str, Any] | None = Field(default=None, description="Action result")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: float | None = Field(
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
```

#### `BrowserSessionRequest`

```python
    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport_width: int = Field(default=1920, description="Viewport width")
    viewport_height: int = Field(default=1080, description="Viewport height")
    user_agent: str | None = Field(default=None, description="Custom user agent")
    action: BrowserAction = Field(..., description="Action to perform")
    parameters: dict[str, Any] = Field(
    session_id: str | None = Field(default=None, description="Browser session ID")
    status: str = Field(..., description="Action status")
    result: dict[str, Any] | None = Field(default=None, description="Action result")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: float | None = Field(
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    domain: str | None = Field(
    query_type: str = Field(
```

#### `BrowserActionRequest`

```python
    action: BrowserAction = Field(..., description="Action to perform")
    parameters: dict[str, Any] = Field(
    session_id: str | None = Field(default=None, description="Browser session ID")
    status: str = Field(..., description="Action status")
    result: dict[str, Any] | None = Field(default=None, description="Action result")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: float | None = Field(
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    domain: str | None = Field(
    query_type: str = Field(
    parameters: dict[str, Any] = Field(
    found: bool = Field(..., description="Whether result was found")
```

#### `BrowserActionResponse`

```python
    status: str = Field(..., description="Action status")
    result: dict[str, Any] | None = Field(default=None, description="Action result")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: float | None = Field(
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    domain: str | None = Field(
    query_type: str = Field(
    parameters: dict[str, Any] = Field(
    found: bool = Field(..., description="Whether result was found")
    result: dict[str, Any] | None = Field(default=None, description="Query result")
    confidence: float = Field(..., description="Confidence score 0-1")
    url: str | None = Field(
```

#### `CognitiveMapQueryRequest`

```python
    domain: str | None = Field(
    query_type: str = Field(
    parameters: dict[str, Any] = Field(
    found: bool = Field(..., description="Whether result was found")
    result: dict[str, Any] | None = Field(default=None, description="Query result")
    confidence: float = Field(..., description="Confidence score 0-1")
    url: str | None = Field(
    analysis_type: str = Field(
    instructions: str | None = Field(
```

#### `CognitiveMapQueryResponse`

```python
    found: bool = Field(..., description="Whether result was found")
    result: dict[str, Any] | None = Field(default=None, description="Query result")
    confidence: float = Field(..., description="Confidence score 0-1")
    url: str | None = Field(
    analysis_type: str = Field(
    instructions: str | None = Field(
    analysis: str = Field(..., description="LLM analysis result")
    structured_data: dict[str, Any] | None = Field(
    recommendations: list[str] = Field(
```

#### `PageAnalysisRequest`

```python
    url: str | None = Field(
    analysis_type: str = Field(
    instructions: str | None = Field(
    analysis: str = Field(..., description="LLM analysis result")
    structured_data: dict[str, Any] | None = Field(
    recommendations: list[str] = Field(
    Attributes:
        browser_controller: Playwright browser controller
        cognitive_map: Graph-based learned website structure
```

#### `PageAnalysisResponse`

```python
    analysis: str = Field(..., description="LLM analysis result")
    structured_data: dict[str, Any] | None = Field(
    recommendations: list[str] = Field(
    Attributes:
        browser_controller: Playwright browser controller
        cognitive_map: Graph-based learned website structure
        service_name: str,
        service_version: str,
        maximus_endpoint: str | None = None,
    ):
        self.browser_controller: BrowserController | None = None
        self.cognitive_map: CognitiveMapEngine | None = None
    async def initialize(self) -> bool:
        Returns:
```

_No data models found_

## 5. Configuration

## 6. Dependencies

### Internal Services

_No internal service dependencies_

### External Libraries
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
httpx==0.26.0
asyncpg==0.29.0
redis==5.0.0
python-dotenv==1.0.0
prometheus-client==0.19.0
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0
opentelemetry-instrumentation-fastapi==0.42b0
opentelemetry-instrumentation-httpx==0.42b0
opentelemetry-instrumentation-asyncpg==0.42b0
opentelemetry-instrumentation-redis==0.42b0
opentelemetry-exporter-jaeger==1.21.0
opentelemetry-exporter-otlp==1.21.0
anthropic==0.8.0
structlog==24.1.0
python-json-logger==2.0.7
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
pytest-mock==3.14.0
mypy>=1.8.0
ruff>=0.1.0
aiofiles==24.1.0
```

