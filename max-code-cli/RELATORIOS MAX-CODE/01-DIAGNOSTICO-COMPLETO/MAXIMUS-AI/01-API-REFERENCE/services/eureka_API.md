# EUREKA - API Reference

**Gerado:** 2025-11-07 20:45:53
**Método:** Análise automática do código fonte

---

## 1. Service Overview

### Statistics
- Python Files: 81
- Lines of Code: 17951
- Test Files: 26

### Entry Point
```
services/eureka/main.py
```

### Directory Structure
```
.
.api
.confirmation
.consumers
.data
.eureka_models
.eureka_models/confirmation
.git_integration
.integrations
.llm
.middleware
.models
.models/confirmation
.orchestration
.scripts
.shared
.strategies
.tests
.tests/integration
.tests/unit
.tracking
```

---

## 2. API Endpoints

### `api_server.py` - Line 80
```python
@app.get("/health")
async def health_check():
```

**Description:**
```
"""Health check endpoint for container orchestration."""
return {"status": "healthy", "service": "maximus_eureka"}


@app.on_event("shutdown")
async def shutdown_event():
"""Performs shutdown tasks for the Eureka Service."""
print("👋 Shutting down MAXIMUS Eureka API Service...")
print("🛑 API Service stopped")
```

### `api_server.py` - Line 93
```python
@app.get("/")
async def root():
```

**Description:**
```
"""Root endpoint."""
return {
    "service": "MAXIMUS Eureka",
    "version": "5.5.1",
    "phase": "5.5 - ML Intelligence Monitoring + Rate Limiting",
    "status": "operational",
    "endpoints": {
        "ml_metrics": "/api/v1/eureka/ml-metrics",
        "ml_health": "/api/v1/eureka/ml-metrics/health",
```

### `api_server.py` - Line 111
```python
@app.get("/api/v1/eureka/rate-limit/metrics")
async def rate_limit_metrics():
```

**Description:**
```
"""
Get rate limiting metrics.

Returns current rate limiter statistics:
- Total hits
- Total blocks  
- Block rate
- Active clients
- Configuration
```

### `ml_metrics.py` - Line 264
```python
@router.get("/ml-metrics", response_model=MLMetricsResponse)
async def get_ml_metrics(
```

**Description:**
```
"""
Get ML prediction metrics and analytics.

Aggregates telemetry from Eureka patch generation pipeline to provide:
```

### `ml_metrics.py` - Line 441
```python
@router.get("/ml-metrics/health")
async def ml_metrics_health() -> Dict[str, str]:
```

**Description:**
```
"""
Health check for ML metrics endpoint.

Returns:
    Status message
"""
return {
    "status": "healthy",
    "message": "ML Metrics API operational",
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

### `test_rate_limiter.py` - Line 144
```python
        @app.get("/")
        async def root():
```

### `test_rate_limiter.py` - Line 148
```python
        @app.get("/health")
        async def health():
```

### `test_rate_limiter.py` - Line 152
```python
        @app.get("/api/test")
        async def test_endpoint():
```

**Description:**
```
    """Middleware should add rate limit headers."""
    limiter = SlidingWindowRateLimiter(default_limit=10, window_seconds=60)
    app = self.create_app(limiter)
    client = TestClient(app)
```

### `test_rate_limiter.py` - Line 238
```python
        @app.get("/api/v1/data")
        async def get_data():
```

### `test_rate_limiter.py` - Line 264
```python
        @app.get("/api/v1/data")
        async def get_data():
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

### `rate_limiter.py` - Line 273
```python
        @app.get("/expensive-operation")
        @rate_limit(limit=10, window_seconds=60)
```

**Description:**
```
"""
def decorator(func: Callable) -> Callable:
    @wraps(func)
```

### `seed_few_shot_db.py` - Line 224
```python
        vulnerable_code='@app.route("/delete", methods=["POST"])ndef delete_account():n    user.delete()',
        fixed_code='@app.route("/delete", methods=["POST"])\n@csrf.exempt  # Or use CSRF protection middleware\ndef delete_account():\n    if not verify_csrf_token(request.form.get("csrf_token")):\n        abort(403)\n    user.delete()',
```

### `seed_few_shot_db.py` - Line 225
```python
        fixed_code='@app.route("/delete", methods=["POST"])n@csrf.exempt  # Or use CSRF protection middlewarendef delete_account():n    if not verify_csrf_token(request.form.get("csrf_token")):n        abort(403)n    user.delete()',
        explanation="Missing CSRF protection on state-changing endpoint. Verify CSRF token.",
```

### `seed_few_shot_db.py` - Line 304
```python
        vulnerable_code='@app.route("/admin/users")ndef list_users():n    return jsonify(User.query.all())',
        fixed_code='from flask_login import login_required\n@app.route("/admin/users")\n@login_required\ndef list_users():\n    if not current_user.is_admin:\n        abort(403)\n    return jsonify(User.query.all())',
```

### `seed_few_shot_db.py` - Line 305
```python
        fixed_code='from flask_login import login_requiredn@app.route("/admin/users")n@login_requiredndef list_users():n    if not current_user.is_admin:n        abort(403)n    return jsonify(User.query.all())',
        explanation="Missing authentication on sensitive endpoint. Require login + role check.",
```

### `api.py` - Line 100
```python
@app.get("/health")
async def health_check() -> dict[str, str]:
```

**Description:**
```
"""Performs a health check of the Eureka Service.

Returns:
    Dict[str, str]: A dictionary indicating the service status.
"""
return {"status": "healthy", "message": "Eureka Service is operational."}


@app.post("/generate_insight")
```

### `api.py` - Line 110
```python
@app.post("/generate_insight")
async def generate_insight_endpoint(request: InsightRequest) -> dict[str, Any]:
```

**Description:**
```
"""Submits data for insight generation and returns novel discoveries.

Args:
    request (InsightRequest): The request body containing data for analysis.

Returns:
    Dict[str, Any]: A dictionary containing the generated insights and discoveries.
"""
print(f"[API] Generating insight for {request.data_type} data.")
```

### `api.py` - Line 147
```python
@app.post("/detect_pattern")
async def detect_pattern_endpoint(request: PatternDetectionRequest) -> dict[str, Any]:
```

**Description:**
```
"""Detects specific patterns within provided data.

Args:
    request (PatternDetectionRequest): The request body containing data and pattern definition.

Returns:
    Dict[str, Any]: A dictionary containing the pattern detection results.
"""
print("[API] Detecting patterns in data.")
```

### `api.py` - Line 166
```python
@app.post("/extract_iocs")
async def extract_iocs_endpoint(data: dict[str, Any]) -> dict[str, Any]:
```

**Description:**
```
"""Extracts Indicators of Compromise (IoCs) from provided data.

Args:
    data (Dict[str, Any]): The data from which to extract IoCs.

Returns:
    Dict[str, Any]: A dictionary containing the extracted IoCs.
"""
print("[API] Extracting IoCs from data.")
```

### `api.py` - Line 185
```python
@app.get("/metrics/rate-limiter")
async def rate_limiter_metrics() -> dict[str, Any]:
```

**Description:**
```
"""
Get rate limiter metrics.

Sprint 6 - Issue #11

Returns:
    Dict with rate limiter statistics:
    - total_hits: Total requests processed
    - total_blocks: Total requests blocked
```

_No HTTP endpoints found_

## 3. Classes and Methods

### `TimeframeEnum`

**File:** `ml_metrics.py`

```python
class TimeframeEnum(str, Enum):
```

**Description:**
```
"""Supported timeframes for metrics aggregation."""
ONE_HOUR = "1h"
TWENTY_FOUR_HOURS = "24h"
SEVEN_DAYS = "7d"
THIRTY_DAYS = "30d"


class UsageBreakdown(BaseModel):
"""
ML vs Wargaming usage breakdown.

Attributes:
    ml_count: Number of patches using ML prediction
    wargaming_count: Number of patches using full wargaming
    total: Total patches processed
    ml_usage_rate: Percentage using ML (0-100)
```

**Public Methods:**


---

### `UsageBreakdown`

**File:** `ml_metrics.py`

```python
class UsageBreakdown(BaseModel):
```

**Description:**
```
"""
ML vs Wargaming usage breakdown.

Attributes:
    ml_count: Number of patches using ML prediction
    wargaming_count: Number of patches using full wargaming
    total: Total patches processed
    ml_usage_rate: Percentage using ML (0-100)
"""
ml_count: int = Field(..., description="Patches using ML prediction")
wargaming_count: int = Field(..., description="Patches using wargaming")
total: int = Field(..., description="Total patches")
ml_usage_rate: float = Field(..., ge=0.0, le=100.0, description="ML usage %")


class ConfidenceBucket(BaseModel):
```

**Public Methods:**


---

### `ConfidenceBucket`

**File:** `ml_metrics.py`

```python
class ConfidenceBucket(BaseModel):
```

**Description:**
```
"""
Confidence score histogram bucket.

Attributes:
    bucket_min: Minimum confidence (inclusive)
    bucket_max: Maximum confidence (exclusive)
    count: Number of predictions in bucket
"""
bucket_min: float = Field(..., ge=0.0, le=1.0)
bucket_max: float = Field(..., ge=0.0, le=1.0)
count: int = Field(..., ge=0)


class TimeSeriesPoint(BaseModel):
"""
Single point in time series data.
```

**Public Methods:**


---

### `TimeSeriesPoint`

**File:** `ml_metrics.py`

```python
class TimeSeriesPoint(BaseModel):
```

**Description:**
```
"""
Single point in time series data.

Attributes:
    timestamp: ISO timestamp
    value: Metric value
"""
timestamp: datetime
value: float


class ConfusionMatrixData(BaseModel):
"""
Confusion matrix for ML predictions.

Attributes:
```

**Public Methods:**


---

### `ConfusionMatrixData`

**File:** `ml_metrics.py`

```python
class ConfusionMatrixData(BaseModel):
```

**Description:**
```
"""
Confusion matrix for ML predictions.

Attributes:
    true_positive: ML predicted success, actual success
    false_positive: ML predicted success, actual failure
    false_negative: ML predicted failure, actual success
    true_negative: ML predicted failure, actual failure
"""
true_positive: int = Field(..., ge=0)
false_positive: int = Field(..., ge=0)
false_negative: int = Field(..., ge=0)
true_negative: int = Field(..., ge=0)

@property
def precision(self) -> float:
```

**Public Methods:**

- `def precision(self) -> float`
- `def recall(self) -> float`
- `def f1_score(self) -> float`
- `def accuracy(self) -> float`

---

### `RecentPrediction`

**File:** `ml_metrics.py`

```python
class RecentPrediction(BaseModel):
```

**Description:**
```
"""
Single ML prediction record for live feed.

Attributes:
    id: Prediction ID
    timestamp: When prediction was made
    cve_id: CVE being remediated
    confidence: ML confidence score (0.0-1.0)
    predicted_success: ML prediction (True=success, False=failure)
    actual_success: Ground truth result (None if not validated yet)
    time_saved_seconds: Time saved vs full wargaming
    used_ml: Whether ML bypass was used
"""
id: str
timestamp: datetime
cve_id: str
```

**Public Methods:**


---

### `MLMetricsResponse`

**File:** `ml_metrics.py`

```python
class MLMetricsResponse(BaseModel):
```

**Description:**
```
"""
Complete ML metrics response.

Aggregates all Phase 5.5 KPIs for dashboard display.

Attributes:
    timeframe: Requested timeframe
    generated_at: When metrics were generated
    usage_breakdown: ML vs Wargaming counts
    avg_confidence: Average confidence score (0.0-1.0)
    confidence_trend: Confidence change vs previous period (%)
    confidence_distribution: Histogram of confidence scores
    time_savings_percent: % time saved using ML vs wargaming
    time_savings_absolute_minutes: Absolute time saved (minutes)
    time_savings_trend: Time savings change vs previous period (%)
    confusion_matrix: ML prediction accuracy matrix
```

**Public Methods:**


---

### `InsightRequest`

**File:** `api.py`

```python
class InsightRequest(BaseModel):
```

**Description:**
```
"""Request model for submitting data for insight generation.

Attributes:
    data (Dict[str, Any]): The data to analyze for insights.
    data_type (str): The type of data (e.g., 'logs', 'network_traffic', 'threat_intel').
    context (Optional[Dict[str, Any]]): Additional context for the analysis.
"""

data: dict[str, Any]
data_type: str
context: dict[str, Any] | None = None


class PatternDetectionRequest(BaseModel):
"""Request model for detecting specific patterns.
```

**Public Methods:**


---

### `PatternDetectionRequest`

**File:** `api.py`

```python
class PatternDetectionRequest(BaseModel):
```

**Description:**
```
"""Request model for detecting specific patterns.

Attributes:
    data (Dict[str, Any]): The data to analyze for patterns.
    pattern_definition (Dict[str, Any]): The definition of the pattern to detect.
"""

data: dict[str, Any]
pattern_definition: dict[str, Any]


@app.on_event("startup")
async def startup_event():
"""Performs startup tasks for the Eureka Service."""
print("💡 Starting Maximus Eureka Service...")
print("✅ Maximus Eureka Service started successfully.")
```

**Public Methods:**


---

### `ASTGrepConfig`

**File:** `ast_grep_engine.py`

```python
class ASTGrepConfig:
```

**Description:**
```
"""
Configuration for ast-grep engine.

Attributes:
    ast_grep_binary: Path to ast-grep executable
    timeout_seconds: Maximum execution time per search
    max_matches: Maximum matches to return per search
    enable_debug: Enable ast-grep debug output
"""

ast_grep_binary: str = "ast-grep"
timeout_seconds: int = 5
max_matches: int = 100
enable_debug: bool = False
```

**Public Methods:**


---

### `ASTGrepMatch`

**File:** `ast_grep_engine.py`

```python
class ASTGrepMatch(BaseModel):
```

**Description:**
```
"""
Single match result from ast-grep pattern search.

Represents one location in codebase where pattern matched.

Attributes:
    file_path: Absolute path to file containing match
    line_start: Starting line number of match
    line_end: Ending line number of match
    column_start: Starting column number
    column_end: Ending column number
    matched_text: Code text that matched pattern
    context_before: Lines before match (optional)
    context_after: Lines after match (optional)
"""
```

**Public Methods:**


---

### `ASTGrepEngine`

**File:** `ast_grep_engine.py`

```python
class ASTGrepEngine:
```

**Description:**
```
"""
Wrapper for ast-grep CLI tool.

Executes ast-grep patterns against codebase to confirm vulnerability presence.
Handles subprocess execution, timeout, error handling, and result parsing.

Design Philosophy:
    Thin wrapper that delegates to ast-grep CLI while providing:
    - Async execution via asyncio.subprocess
    - Structured error handling
    - Timeout protection
    - JSON result parsing
    - Validation of ast-grep installation

Usage:
    >>> engine = ASTGrepEngine()
```

**Public Methods:**


---

### `ConfirmationConfig`

**File:** `vulnerability_confirmer.py`

```python
class ConfirmationConfig:
```

**Description:**
```
"""
Configuration for vulnerability confirmation.

Attributes:
    codebase_root: Root directory of codebase to scan
    max_files_per_scan: Maximum files to scan per confirmation
    cache_enabled: Enable Redis caching of confirmation results
    cache_ttl_seconds: TTL for cached results
    ast_grep_timeout: Timeout for ast-grep execution
"""

def __init__(
    self,
    codebase_root: Path,
    max_files_per_scan: int = 1000,
    cache_enabled: bool = True,
```

**Public Methods:**


---

### `VulnerabilityConfirmer`

**File:** `vulnerability_confirmer.py`

```python
class VulnerabilityConfirmer:
```

**Description:**
```
"""
Confirms vulnerability presence in codebase using AST analysis.

Orchestrates file discovery, pattern matching, and result aggregation
to produce high-confidence confirmation of APV-reported vulnerabilities.

Design Philosophy:
    Two-phase approach: (1) file discovery via heuristics, (2) syntactic
    confirmation via ast-grep. This balances performance (narrow file set)
    with accuracy (precise pattern matching).

Usage:
    >>> config = ConfirmationConfig(codebase_root=Path("/app"))
    >>> confirmer = VulnerabilityConfirmer(config)
    >>> result = await confirmer.confirm_vulnerability(apv)
    >>> if result.is_confirmed:
```

**Public Methods:**


---

### `APVConsumerConfig`

**File:** `apv_consumer.py`

```python
class APVConsumerConfig:
```

**Description:**
```
"""
Configuration for APV Kafka consumer.

Attributes:
    kafka_bootstrap_servers: Kafka broker addresses
    kafka_topic: Topic containing APVs from Oráculo
    kafka_group_id: Consumer group ID for load balancing
    kafka_dlq_topic: Dead Letter Queue for failed APVs
    max_poll_records: Max records per poll (batch size)
    enable_auto_commit: Auto-commit offsets (False for manual control)
    auto_offset_reset: Offset reset policy ('earliest' or 'latest')
    session_timeout_ms: Consumer session timeout
    heartbeat_interval_ms: Heartbeat interval
    redis_cache_url: Redis URL for deduplication cache
    redis_ttl_seconds: TTL for deduplication entries
"""
```

**Public Methods:**


---

### `APVConsumer`

**File:** `apv_consumer.py`

```python
class APVConsumer:
```

**Description:**
```
"""
Kafka consumer for APVs from Oráculo Threat Sentinel.

Implements at-least-once delivery with idempotency guarantees.
Processes APVs asynchronously, invoking confirmation and remediation pipeline.

Design Philosophy:
    Reactive consumer that bridges detection (Oráculo) and remediation (Eureka).
    Handles failures gracefully via Dead Letter Queue, ensuring no APV is lost
    while preventing infinite retry loops.

Usage:
    >>> config = APVConsumerConfig()
    >>> consumer = APVConsumer(config, process_apv_handler)
    >>> await consumer.start()
    >>> # Consumer runs until stopped
```

**Public Methods:**

- `def is_running(self) -> bool`
- `def stats(self) -> dict[str, Any]`

---

### `DifficultyLevel`

**File:** `few_shot_database.py`

```python
class DifficultyLevel(str, Enum):
```

**Description:**
```
"""Fix difficulty levels"""
EASY = "easy"      # Single line change, obvious fix
MEDIUM = "medium"  # Multi-line, requires understanding
HARD = "hard"      # Complex logic, subtle issues


@dataclass
class VulnerabilityFix:
"""Represents a single vulnerability fix example"""

id: Optional[int]
cwe_id: str
cve_id: Optional[str]
language: str
vulnerable_code: str
fixed_code: str
```

**Public Methods:**


---

### `VulnerabilityFix`

**File:** `few_shot_database.py`

```python
class VulnerabilityFix:
```

**Description:**
```
"""Represents a single vulnerability fix example"""

id: Optional[int]
cwe_id: str
cve_id: Optional[str]
language: str
vulnerable_code: str
fixed_code: str
explanation: str
difficulty: DifficultyLevel
created_at: Optional[datetime] = None

def to_few_shot_prompt(self) -> str:
    """Format as few-shot example for LLM"""
    return f"""
## Example Fix ({self.cwe_id})
```

**Public Methods:**

- `def to_few_shot_prompt(self) -> str`

---

### `FewShotDatabase`

**File:** `few_shot_database.py`

```python
class FewShotDatabase:
```

**Description:**
```
"""
SQLite database manager for vulnerability fix examples.

Schema:
    - vulnerability_fixes: Main table with fix examples
    - Indexes: cwe_id, language, difficulty

Usage:
    >>> db = FewShotDatabase("data/few_shot_examples.db")
    >>> db.initialize()
    >>> examples = db.get_examples_by_cwe("CWE-89", language="python", limit=5)
    >>> for ex in examples:
    ...     print(ex.to_few_shot_prompt())
"""

SCHEMA = """
```

**Public Methods:**

- `def initialize(self) -> None`
- `def add_example(self, example`
- `def add_examples_bulk(self, examples`
- `def get_examples_by_cwe(`
- `def get_random_examples(`
- `def count_examples(`
- `def get_statistics(self) -> Dict[str, int]`

---

### `ConfirmationStatus`

**File:** `confirmation_result.py`

```python
class ConfirmationStatus(str, Enum):
```

**Description:**
```
"""
Status of vulnerability confirmation attempt.

Epistemic states reflecting confidence in vulnerability presence:
    - CONFIRMED: High-confidence evidence via ast-grep pattern match
    - FALSE_POSITIVE: CVE referenced but pattern not found in code
    - ERROR: Confirmation process failed (infrastructure/tooling issue)
    - PENDING: Confirmation queued but not yet executed
"""

CONFIRMED = "confirmed"
FALSE_POSITIVE = "false_positive"
ERROR = "error"
PENDING = "pending"
```

**Public Methods:**


---

### `VulnerableLocation`

**File:** `confirmation_result.py`

```python
class VulnerableLocation(BaseModel):
```

**Description:**
```
"""
Precise code location where vulnerability pattern was detected.

Provides surgical targeting for remediation strategies, avoiding
broad-spectrum changes that risk introducing regressions.

Attributes:
    file_path: Absolute path to vulnerable file
    line_start: First line of vulnerable code block
    line_end: Last line of vulnerable code block
    code_snippet: Matched code (max 500 chars for context)
    pattern_matched: ast-grep pattern that matched
    confidence_score: Match confidence 0.0-1.0 (1.0 = exact match)
"""

model_config = ConfigDict(frozen=True)
```

**Public Methods:**


---

### `ConfirmationMetadata`

**File:** `confirmation_result.py`

```python
class ConfirmationMetadata(BaseModel):
```

**Description:**
```
"""
Metadata about confirmation process execution.

Enables observability, debugging, and continuous improvement of
confirmation accuracy through pattern refinement.

Attributes:
    confirmed_at: Timestamp of confirmation completion
    ast_grep_version: Version of ast-grep used
    patterns_tested: Number of ast-grep patterns attempted
    files_scanned: Number of files analyzed
    execution_time_ms: Time taken for confirmation (milliseconds)
"""

model_config = ConfigDict(frozen=True)
```

**Public Methods:**


---

### `ConfirmationResult`

**File:** `confirmation_result.py`

```python
class ConfirmationResult(BaseModel):
```

**Description:**
```
"""
Complete result of vulnerability confirmation process.

Bridges gap between abstract CVE description and concrete code instances.
Informs remediation strategy selection through status and location data.

Design Philosophy:
    Immutable result object that can be cached, replayed, and audited.
    Contains both positive findings (vulnerable locations) and metadata
    for negative findings (false positives).

Attributes:
    apv_id: ID of APV being confirmed (links to Oráculo APV)
    cve_id: CVE identifier (e.g., "CVE-2024-27351")
    status: Confirmation outcome
    vulnerable_locations: List of confirmed vulnerable code locations
```

**Public Methods:**

- `def is_confirmed(self) -> bool`
- `def location_count(self) -> int`
- `def requires_remediation(self) -> bool`

---

### `PatchStatus`

**File:** `patch.py`

```python
class PatchStatus(str, Enum):
```

**Description:**
```
"""
Patch application status.

Lifecycle:
    PENDING → VALIDATING → APPLIED → MERGED (success)
                        ↘ FAILED → ROLLED_BACK (failure)
"""
PENDING = "pending"
VALIDATING = "validating"
APPLIED = "applied"
MERGED = "merged"
FAILED = "failed"
ROLLED_BACK = "rolled_back"


class Patch(BaseModel):
```

**Public Methods:**


---

### `Patch`

**File:** `patch.py`

```python
class Patch(BaseModel):
```

**Description:**
```
"""
Generated patch for vulnerability remediation.

Contains unified diff and metadata for Git application.
Immutable after generation - modifications require new Patch.

Design Philosophy:
    Patch is value object representing proposed change. Separates patch
    generation (strategies) from patch application (Git integration).
    This enables testing patches without Git operations.

Attributes:
    patch_id: Unique identifier (format: patch-{cve_id}-{timestamp})
    cve_id: CVE being remediated
    strategy_used: Strategy that generated this patch
    diff_content: Unified diff in git format
```

**Public Methods:**


---

### `RemediationResult`

**File:** `patch.py`

```python
class RemediationResult(BaseModel):
```

**Description:**
```
"""
Complete remediation result including patch and execution metadata.

Captures entire remediation attempt for auditing and metrics.

Attributes:
    apv: Original APV from Oráculo
    patch: Generated patch (if successful)
    status: Current status of remediation
    error_message: Error description (if failed)
    started_at: When remediation started
    completed_at: When remediation completed
    time_to_patch_seconds: Total time from APV to patch
    strategy_attempts: Strategies attempted in order (for fallback tracking)
"""
```

**Public Methods:**


---

### `EurekaEngine`

**File:** `eureka.py`

```python
class EurekaEngine:
```

**Description:**
```
"""Identifies novel insights, makes unexpected connections, and generates
breakthrough discoveries from vast amounts of data.

Applies advanced analytical techniques, cross-references information from
disparate data sources, and generates hypotheses.
"""

def __init__(self):
    """Initializes the EurekaEngine."""
    self.discovery_history: list[dict[str, Any]] = []
    self.last_discovery_time: datetime | None = None
    self.current_status: str = "seeking_insights"

async def analyze_data(
    self,
    data: dict[str, Any],
```

**Public Methods:**


---

### `GitOperationsError`

**File:** `git_operations.py`

```python
class GitOperationsError(Exception):
```

**Description:**
```
"""Base exception for Git operations failures."""

pass


class GitOperations:
"""
Core Git operations engine for automated patch application.

Provides high-level Git workflow automation with safety checks,
structured commit messages, and comprehensive error handling.

Responsibilities:
    - Create isolated remediation branches
    - Apply patches with validation
    - Create structured commits
```

**Public Methods:**


---

### `GitOperations`

**File:** `git_operations.py`

```python
class GitOperations:
```

**Description:**
```
"""
Core Git operations engine for automated patch application.

Provides high-level Git workflow automation with safety checks,
structured commit messages, and comprehensive error handling.

Responsibilities:
    - Create isolated remediation branches
    - Apply patches with validation
    - Create structured commits
    - Push branches to remote
    - Rollback failed operations

Attributes:
    config: Git configuration (repo path, remote, credentials)
    repo: GitPython Repo instance
```

**Public Methods:**


---

### `GitApplyResult`

**File:** `models.py`

```python
class GitApplyResult(BaseModel):
```

**Description:**
```
"""
Result of a git apply operation.

Captures the outcome of applying a patch to a Git repository,
including success status, commit SHA, files changed, and any
conflicts encountered.

Attributes:
    success: Whether patch was applied successfully
    commit_sha: Git commit SHA if committed (None if not yet committed)
    files_changed: List of file paths modified by patch
    conflicts: List of files with merge conflicts (empty if none)
    error_message: Error description if success=False
    
Example:
    >>> result = GitApplyResult(
```

**Public Methods:**


---

### `PushResult`

**File:** `models.py`

```python
class PushResult(BaseModel):
```

**Description:**
```
"""
Result of a git push operation.

Captures outcome of pushing a branch to remote repository,
including success status and remote reference.

Attributes:
    success: Whether push succeeded
    branch: Local branch name that was pushed
    remote_ref: Remote reference (e.g. 'origin/remediation/CVE-123')
    error_message: Error description if success=False
    
Example:
    >>> result = PushResult(
    ...     success=True,
    ...     branch="remediation/CVE-2024-1234",
```

**Public Methods:**


---

### `PRResult`

**File:** `models.py`

```python
class PRResult(BaseModel):
```

**Description:**
```
"""
Result of GitHub Pull Request creation.

Captures outcome of PR creation via GitHub API, including
PR number and URL for tracking.

Attributes:
    success: Whether PR was created successfully
    pr_number: GitHub PR number (None if creation failed)
    pr_url: Full URL to PR on GitHub (None if creation failed)
    error_message: Error description if success=False
    
Example:
    >>> result = PRResult(
    ...     success=True,
    ...     pr_number=42,
```

**Public Methods:**


---

### `ValidationResult`

**File:** `models.py`

```python
class ValidationResult(BaseModel):
```

**Description:**
```
"""
Result of safety validation checks.

Aggregates results from multiple validation checks (syntax,
imports, formatting, etc.) into a single pass/fail result
with detailed failure and warning information.

Attributes:
    passed: Whether all validations passed
    checks_run: List of validation check names executed
    failures: List of failed check descriptions
    warnings: List of warning messages (non-blocking)
    
Example:
    >>> result = ValidationResult(
    ...     passed=True,
```

**Public Methods:**


---

### `ConflictReport`

**File:** `models.py`

```python
class ConflictReport(BaseModel):
```

**Description:**
```
"""
Merge conflict detection report.

Analyzes patch for potential merge conflicts with target branch,
providing list of conflicting files and resolution suggestions.

Attributes:
    has_conflicts: Whether any conflicts were detected
    conflicting_files: List of files with conflicts
    resolution_suggestions: AI-generated suggestions for conflict resolution
    
Example:
    >>> report = ConflictReport(
    ...     has_conflicts=True,
    ...     conflicting_files=["src/app.py"],
    ...     resolution_suggestions=["Rebase on latest main"]
```

**Public Methods:**


---

### `GitConfig`

**File:** `models.py`

```python
class GitConfig(BaseModel):
```

**Description:**
```
"""
Git integration configuration.

Centralized configuration for Git operations, including
repository paths, remote URLs, authentication, and commit metadata.

Attributes:
    repo_path: Absolute path to local Git repository
    remote_url: URL of remote repository
    default_branch: Default base branch (usually 'main' or 'develop')
    branch_prefix: Prefix for remediation branches (e.g. 'remediation')
    github_token: GitHub Personal Access Token (excluded from serialization)
    commit_author: Name used in commit metadata
    commit_email: Email used in commit metadata
    
Security:
```

**Public Methods:**

- `def repo_exists(self) -> bool`

---

### `PRCreatorError`

**File:** `pr_creator.py`

```python
class PRCreatorError(Exception):
```

**Description:**
```
"""Base exception for PR creation failures."""

pass


# PR Body Jinja2 Template
PR_BODY_TEMPLATE = """# 🛡️ Auto-Remediation: {{ cve_id }}

## 🚨 Vulnerability Summary

**Severity**: {{ severity_badge }}  
**CVE**: [{{ cve_id }}]({{ cve_url }})  
**Strategy**: `{{ strategy }}`  
**Confidence**: **{{ confidence }}%**

{{ description }}
```

**Public Methods:**


---

### `PRCreator`

**File:** `pr_creator.py`

```python
class PRCreator:
```

**Description:**
```
"""
GitHub Pull Request creation service.

Handles PR creation via GitHub API with rich contextual metadata,
labels, and assignees for effective Human-in-the-Loop review.

Responsibilities:
    - Authenticate with GitHub
    - Create PRs with templated bodies
    - Assign labels based on severity/strategy
    - Set reviewers/assignees
    - Handle API errors gracefully

Attributes:
    config: Git configuration (includes GitHub token)
    github: PyGithub client instance
```

**Public Methods:**

- `def close(self) -> None`

---

### `SafetyChecksError`

**File:** `safety_checks.py`

```python
class SafetyChecksError(Exception):
```

**Description:**
```
"""Base exception for safety check failures."""

pass


class SafetyChecks:
"""
Safety validation layer for Git operations.

Performs pre-apply and post-apply validations to ensure patches
are well-formed, syntactically correct, and don't introduce obvious errors.

Responsibilities:
    - Validate patch format (unified diff)
    - Check Python syntax post-apply
    - Verify imports are resolvable
```

**Public Methods:**


---

### `SafetyChecks`

**File:** `safety_checks.py`

```python
class SafetyChecks:
```

**Description:**
```
"""
Safety validation layer for Git operations.

Performs pre-apply and post-apply validations to ensure patches
are well-formed, syntactically correct, and don't introduce obvious errors.

Responsibilities:
    - Validate patch format (unified diff)
    - Check Python syntax post-apply
    - Verify imports are resolvable
    - Detect merge conflicts
    - Run basic linting (optional)

Attributes:
    codebase_root: Root path of codebase
    
```

**Public Methods:**


---

### `AttackVectorType`

**File:** `coagulation_client.py`

```python
class AttackVectorType(str, Enum):
```

**Description:**
```
"""Attack vector categories"""
SQL_INJECTION = "sql_injection"
XSS = "xss"
COMMAND_INJECTION = "command_injection"
PATH_TRAVERSAL = "path_traversal"
SSRF = "ssrf"
XXE = "xxe"
CSRF = "csrf"
FILE_UPLOAD = "file_upload"
AUTHENTICATION_BYPASS = "authentication_bypass"
GENERIC = "generic"


@dataclass
class CoagulationRule:
"""Represents a temporary WAF rule"""
```

**Public Methods:**


---

### `CoagulationRule`

**File:** `coagulation_client.py`

```python
class CoagulationRule:
```

**Description:**
```
"""Represents a temporary WAF rule"""

rule_id: str
apv_id: str
cve_id: str
attack_vector: AttackVectorType
pattern: str
action: str  # "block", "alert", "log"
ttl_seconds: int
created_at: datetime
expires_at: datetime
active: bool = True

def to_dict(self) -> Dict:
    """Convert to dictionary for API"""
    return {
```

**Public Methods:**

- `def to_dict(self) -> Dict`

---

### `CoagulationClient`

**File:** `coagulation_client.py`

```python
class CoagulationClient:
```

**Description:**
```
"""
Client for RTE Service to deploy temporary WAF rules.

Integrates with RTE Service (Reflex Triage Engine) to create
firewall rules that block attack vectors while patches are in progress.

Usage:
    >>> client = CoagulationClient(rte_url="http://rte-service:8002")
    >>> rule = await client.create_temporary_rule(
    ...     apv=apv_object,
    ...     attack_vector=AttackVectorType.SQL_INJECTION,
    ...     duration=timedelta(hours=24)
    ... )
    >>> print(f"Rule {rule.rule_id} active until {rule.expires_at}")
"""
```

**Public Methods:**

- `def detect_attack_vector_from_cwe(cwe_id`

---

### `CoagulationError`

**File:** `coagulation_client.py`

```python
class CoagulationError(Exception):
```

**Description:**
```
"""Raised when coagulation operations fail"""
pass


# Convenience function
async def create_waf_rule_for_apv(
apv: "APV",  # Type hint as string to avoid circular import
rte_url: str = "http://rte-service:8002",
duration: timedelta = timedelta(hours=24)
) -> CoagulationRule:
"""
Quick function to create WAF rule from APV.

Args:
    apv: APV object (from Oráculo)
    rte_url: RTE Service URL
```

**Public Methods:**


---

### `IoCExtractor`

**File:** `ioc_extractor.py`

```python
class IoCExtractor:
```

**Description:**
```
"""Automatically identifies and extracts various types of Indicators of Compromise (IoCs)
from unstructured or semi-structured data.

Leverages regular expressions, pattern matching, and potentially natural
language processing techniques.
"""

def __init__(self):
    """Initializes the IoCExtractor with common IoC patterns."""
    self.ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    self.domain_pattern = re.compile(
        r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\b"
    )
    self.hash_pattern = re.compile(r"\b[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}\b")  # MD5, SHA1, SHA256
    self.url_pattern = re.compile(
        r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
```

**Public Methods:**

- `def extract_iocs(self, data`
- `def validate_ioc(self, ioc_type`

---

### `LLMProvider`

**File:** `base_client.py`

```python
class LLMProvider(str, Enum):
```

**Description:**
```
"""Supported LLM providers."""
CLAUDE = "claude"
GPT4 = "gpt4"
LOCAL = "local"


@dataclass
class LLMMessage:
"""
Single message in conversation.

Attributes:
    role: Message role (user, assistant, system)
    content: Message text content
"""
role: str  # "user" | "assistant" | "system"
```

**Public Methods:**


---

### `LLMMessage`

**File:** `base_client.py`

```python
class LLMMessage:
```

**Description:**
```
"""
Single message in conversation.

Attributes:
    role: Message role (user, assistant, system)
    content: Message text content
"""
role: str  # "user" | "assistant" | "system"
content: str


@dataclass
class LLMResponse:
"""
LLM completion response.
```

**Public Methods:**


---

### `LLMResponse`

**File:** `base_client.py`

```python
class LLMResponse:
```

**Description:**
```
"""
LLM completion response.

Attributes:
    content: Generated text
    model: Model used (e.g., "claude-3-5-sonnet-20241022")
    tokens_used: Total tokens (input + output)
    finish_reason: Completion reason (stop, length, etc)
    raw_response: Original provider response for debugging
"""
content: str
model: str
tokens_used: int
finish_reason: str
raw_response: Optional[Dict[str, Any]] = None
```

**Public Methods:**


---

### `LLMError`

**File:** `base_client.py`

```python
class LLMError(Exception):
```

**Description:**
```
"""Base exception for LLM errors."""
pass


class LLMRateLimitError(LLMError):
"""Rate limit exceeded."""
pass


class LLMAuthenticationError(LLMError):
"""Authentication failed."""
pass


class LLMInvalidRequestError(LLMError):
"""Invalid request parameters."""
```

**Public Methods:**


---

### `LLMRateLimitError`

**File:** `base_client.py`

```python
class LLMRateLimitError(LLMError):
```

**Description:**
```
"""Rate limit exceeded."""
pass


class LLMAuthenticationError(LLMError):
"""Authentication failed."""
pass


class LLMInvalidRequestError(LLMError):
"""Invalid request parameters."""
pass


class BaseLLMClient(ABC):
"""
```

**Public Methods:**


---

### `LLMAuthenticationError`

**File:** `base_client.py`

```python
class LLMAuthenticationError(LLMError):
```

**Description:**
```
"""Authentication failed."""
pass


class LLMInvalidRequestError(LLMError):
"""Invalid request parameters."""
pass


class BaseLLMClient(ABC):
"""
Abstract base for LLM clients.

Subclasses implement provider-specific logic while maintaining
consistent interface for strategies.
```

**Public Methods:**


---

### `LLMInvalidRequestError`

**File:** `base_client.py`

```python
class LLMInvalidRequestError(LLMError):
```

**Description:**
```
"""Invalid request parameters."""
pass


class BaseLLMClient(ABC):
"""
Abstract base for LLM clients.

Subclasses implement provider-specific logic while maintaining
consistent interface for strategies.

Common features provided:
- Retry logic with exponential backoff
- Rate limiting
- Token counting
- Error handling
```

**Public Methods:**


---

### `BaseLLMClient`

**File:** `base_client.py`

```python
class BaseLLMClient(ABC):
```

**Description:**
```
"""
Abstract base for LLM clients.

Subclasses implement provider-specific logic while maintaining
consistent interface for strategies.

Common features provided:
- Retry logic with exponential backoff
- Rate limiting
- Token counting
- Error handling

Usage:
    >>> client = ClaudeClient(api_key="...")
    >>> response = await client.complete(
    ...     messages=[LLMMessage(role="user", content="Fix this code...")],
```

**Public Methods:**

- `def provider(self) -> LLMProvider`
- `def count_tokens(self, text`
- `def estimate_cost(`

---

### `BreakingSeverity`

**File:** `breaking_changes_analyzer.py`

```python
class BreakingSeverity(str, Enum):
```

**Description:**
```
"""Breaking change severity levels"""
CRITICAL = "critical"  # Will definitely break code
HIGH = "high"          # Likely to break code
MEDIUM = "medium"      # May break code
LOW = "low"            # Unlikely to break code
INFO = "info"          # Not breaking, informational


@dataclass
class BreakingChange:
"""Represents a single breaking change"""

severity: BreakingSeverity
category: str  # e.g., "API signature", "Behavior change", "Deprecation"
description: str
affected_apis: List[str]
```

**Public Methods:**


---

### `BreakingChange`

**File:** `breaking_changes_analyzer.py`

```python
class BreakingChange:
```

**Description:**
```
"""Represents a single breaking change"""

severity: BreakingSeverity
category: str  # e.g., "API signature", "Behavior change", "Deprecation"
description: str
affected_apis: List[str]
migration_steps: List[str]
confidence: float  # 0.0-1.0


@dataclass
class BreakingChangesReport:
"""Complete breaking changes analysis report"""

package: str
from_version: str
```

**Public Methods:**


---

### `BreakingChangesReport`

**File:** `breaking_changes_analyzer.py`

```python
class BreakingChangesReport:
```

**Description:**
```
"""Complete breaking changes analysis report"""

package: str
from_version: str
to_version: str
analyzed_at: datetime
breaking_changes: List[BreakingChange]
has_breaking_changes: bool
overall_risk: BreakingSeverity
estimated_migration_time: str  # e.g., "2-4 hours", "1 day"
llm_model: str
tokens_used: int
cost_usd: float

@property
def critical_count(self) -> int:
```

**Public Methods:**

- `def critical_count(self) -> int`
- `def high_count(self) -> int`
- `def summary(self) -> str`

---

### `BreakingChangesAnalyzer`

**File:** `breaking_changes_analyzer.py`

```python
class BreakingChangesAnalyzer:
```

**Description:**
```
"""
Analyze version diffs using LLM to detect breaking changes.

Uses Google Gemini 2.5 Pro for cost-effective analysis.

Usage:
    >>> analyzer = BreakingChangesAnalyzer(api_key=os.getenv("GEMINI_API_KEY"))
    >>> report = await analyzer.analyze_diff(
    ...     package="requests",
    ...     from_version="2.28.0",
    ...     to_version="2.31.0",
    ...     diff_content=version_diff
    ... )
    >>> print(report.summary())
"""
```

**Public Methods:**


---

### `AnalysisError`

**File:** `breaking_changes_analyzer.py`

```python
class AnalysisError(Exception):
```

**Description:**
```
"""Raised when breaking changes analysis fails"""
pass


# Convenience function for quick analysis
async def analyze_breaking_changes(
package: str,
from_version: str,
to_version: str,
diff_content: str,
api_key: Optional[str] = None
) -> BreakingChangesReport:
"""
Quick function to analyze breaking changes.

Args:
```

**Public Methods:**


---

### `ClaudeClient`

**File:** `claude_client.py`

```python
class ClaudeClient(BaseLLMClient):
```

**Description:**
```
"""
Claude LLM client using Anthropic SDK.

Features:
- Async API calls with retry logic
- Exponential backoff on rate limits
- Token counting via Claude tokenizer
- Cost estimation
- Error handling and logging

Usage:
    >>> client = ClaudeClient(
    ...     api_key=os.environ["ANTHROPIC_API_KEY"],
    ...     model="claude-3-5-sonnet-20241022",
    ... )
    >>> response = await client.complete(
```

**Public Methods:**

- `def provider(self) -> LLMProvider`
- `def count_tokens(self, text`
- `def estimate_cost(`

---

### `SlidingWindowRateLimiter`

**File:** `rate_limiter.py`

```python
class SlidingWindowRateLimiter:
```

**Description:**
```
"""
Sliding window rate limiter.

Tracks requests per client in time windows.
Memory-efficient with automatic cleanup.

Biological Analogy: Immune system regulation
- Too many requests = overwhelming immune response
- Rate limiting = homeostatic control
- Burst tolerance = adaptive response to real threats
"""

def __init__(
    self,
    default_limit: int = 100,
    window_seconds: int = 60,
```

**Public Methods:**

- `def set_endpoint_limit(`
- `def is_allowed(self, client_id`
- `def get_metrics(self) -> Dict`

---

### `RateLimitMiddleware`

**File:** `rate_limiter.py`

```python
class RateLimitMiddleware(BaseHTTPMiddleware):
```

**Description:**
```
"""
FastAPI middleware for rate limiting.

Automatically applies rate limits to all endpoints.
Adds rate limit headers to responses.
"""

def __init__(
    self,
    app,
    limiter: SlidingWindowRateLimiter,
    get_client_id: Optional[Callable[[Request], str]] = None,
    exclude_paths: Optional[list] = None
):
    """
    Initialize middleware.
```

**Public Methods:**

- `def decorator(func`

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

### `ConfirmationStatus`

**File:** `confirmation_result.py`

```python
class ConfirmationStatus(str, Enum):
```

**Description:**
```
"""
Status of vulnerability confirmation attempt.

Epistemic states reflecting confidence in vulnerability presence:
    - CONFIRMED: High-confidence evidence via ast-grep pattern match
    - FALSE_POSITIVE: CVE referenced but pattern not found in code
    - ERROR: Confirmation process failed (infrastructure/tooling issue)
    - PENDING: Confirmation queued but not yet executed
"""

CONFIRMED = "confirmed"
FALSE_POSITIVE = "false_positive"
ERROR = "error"
PENDING = "pending"
```

**Public Methods:**


---

### `VulnerableLocation`

**File:** `confirmation_result.py`

```python
class VulnerableLocation(BaseModel):
```

**Description:**
```
"""
Precise code location where vulnerability pattern was detected.

Provides surgical targeting for remediation strategies, avoiding
broad-spectrum changes that risk introducing regressions.

Attributes:
    file_path: Absolute path to vulnerable file
    line_start: First line of vulnerable code block
    line_end: Last line of vulnerable code block
    code_snippet: Matched code (max 500 chars for context)
    pattern_matched: ast-grep pattern that matched
    confidence_score: Match confidence 0.0-1.0 (1.0 = exact match)
"""

model_config = ConfigDict(frozen=True)
```

**Public Methods:**


---

### `ConfirmationMetadata`

**File:** `confirmation_result.py`

```python
class ConfirmationMetadata(BaseModel):
```

**Description:**
```
"""
Metadata about confirmation process execution.

Enables observability, debugging, and continuous improvement of
confirmation accuracy through pattern refinement.

Attributes:
    confirmed_at: Timestamp of confirmation completion
    ast_grep_version: Version of ast-grep used
    patterns_tested: Number of ast-grep patterns attempted
    files_scanned: Number of files analyzed
    execution_time_ms: Time taken for confirmation (milliseconds)
"""

model_config = ConfigDict(frozen=True)
```

**Public Methods:**


---

### `ConfirmationResult`

**File:** `confirmation_result.py`

```python
class ConfirmationResult(BaseModel):
```

**Description:**
```
"""
Complete result of vulnerability confirmation process.

Bridges gap between abstract CVE description and concrete code instances.
Informs remediation strategy selection through status and location data.

Design Philosophy:
    Immutable result object that can be cached, replayed, and audited.
    Contains both positive findings (vulnerable locations) and metadata
    for negative findings (false positives).

Attributes:
    apv_id: ID of APV being confirmed (links to Oráculo APV)
    cve_id: CVE identifier (e.g., "CVE-2024-27351")
    status: Confirmation outcome
    vulnerable_locations: List of confirmed vulnerable code locations
```

**Public Methods:**

- `def is_confirmed(self) -> bool`
- `def location_count(self) -> int`
- `def requires_remediation(self) -> bool`

---

### `EurekaMetrics`

**File:** `eureka_orchestrator.py`

```python
class EurekaMetrics:
```

**Description:**
```
"""
Operational metrics for Eureka orchestrator.

Tracks pipeline performance across confirmation AND remediation phases.
"""

# Counters
apvs_received: int = 0
apvs_confirmed: int = 0
apvs_false_positive: int = 0
apvs_failed: int = 0

# Phase 3: Remediation metrics
patches_generated: int = 0
patches_failed: int = 0
strategy_dependency_upgrade: int = 0
```

**Public Methods:**

- `def record_processing(self, duration`
- `def record_patch(self, patch`
- `def avg_processing_time(self) -> float`
- `def success_rate(self) -> float`
- `def to_dict(self) -> dict[str, Any]`

---

### `EurekaOrchestrator`

**File:** `eureka_orchestrator.py`

```python
class EurekaOrchestrator:
```

**Description:**
```
"""
Orchestrates Eureka vulnerability confirmation pipeline.

Phase 2 (Current): APV Consumer → Vulnerability Confirmation
Phase 3 (Future): Add Remediation Strategy Selection + Patch Generation
Phase 4 (Future): Add Git Integration + PR Creation

The orchestrator provides:
- Centralized lifecycle management (start/stop)
- Error handling and recovery
- Metrics collection and reporting
- Graceful degradation on component failures

Usage:
    >>> config_consumer = APVConsumerConfig()
    >>> config_confirmer = ConfirmationConfig(codebase_root=Path("/app"))
```

**Public Methods:**

- `def get_metrics(self) -> dict[str, Any]`
- `def is_running(self) -> bool`

---

### `PatternDetector`

**File:** `pattern_detector.py`

```python
class PatternDetector:
```

**Description:**
```
"""Identifies recurring sequences, anomalies, or significant structures within
various data streams.

Leverages statistical methods, machine learning algorithms, and rule-based
engines to make sense of complex data and detect deviations.
"""

def __init__(self):
    """Initializes the PatternDetector with predefined patterns (mock)."""
    self.predefined_patterns: dict[str, Any] = {
        "anomaly_spike": {
            "type": "statistical",
            "threshold": 3.0,
            "metric": "cpu_usage",
        },
        "sequential_login_failure": {
```

**Public Methods:**

- `def detect_patterns(self, data`

---

### `PlaybookGenerator`

**File:** `playbook_generator.py`

```python
class PlaybookGenerator:
```

**Description:**
```
"""Dynamically creates or suggests response playbooks based on novel insights,
detected patterns, or critical discoveries made by the Eureka Engine.

Proposes tailored, actionable sequences of defensive or investigative steps.
"""

def __init__(self):
    """Initializes the PlaybookGenerator."""
    self.generated_playbooks: list[dict[str, Any]] = []
    self.last_generation_time: datetime | None = None
    self.current_status: str = "ready_to_generate"

def generate_playbook(self, insight: dict[str, Any]) -> dict[str, Any]:
    """Generates a response playbook based on a given insight or discovery.

    Args:
```

**Public Methods:**

- `def generate_playbook(self, insight`

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

### `StrategyError`

**File:** `base_strategy.py`

```python
class StrategyError(Exception):
```

**Description:**
```
"""Base exception for strategy errors."""

pass


class StrategyFailedError(StrategyError):
"""Raised when strategy fails to generate valid patch."""

pass


class StrategyNotApplicableError(StrategyError):
"""Raised when strategy cannot handle given APV."""

pass
```

**Public Methods:**


---

### `StrategyFailedError`

**File:** `base_strategy.py`

```python
class StrategyFailedError(StrategyError):
```

**Description:**
```
"""Raised when strategy fails to generate valid patch."""

pass


class StrategyNotApplicableError(StrategyError):
"""Raised when strategy cannot handle given APV."""

pass


class BaseStrategy(ABC):
"""
Abstract base for all remediation strategies.

Implements Template Method pattern where subclasses override specific steps
```

**Public Methods:**


---

### `StrategyNotApplicableError`

**File:** `base_strategy.py`

```python
class StrategyNotApplicableError(StrategyError):
```

**Description:**
```
"""Raised when strategy cannot handle given APV."""

pass


class BaseStrategy(ABC):
"""
Abstract base for all remediation strategies.

Implements Template Method pattern where subclasses override specific steps
while base class orchestrates overall flow and provides common utilities.

Subclass Responsibilities:
    - Implement strategy_type property
    - Implement can_handle() logic
    - Implement apply_strategy() patch generation
```

**Public Methods:**


---

### `BaseStrategy`

**File:** `base_strategy.py`

```python
class BaseStrategy(ABC):
```

**Description:**
```
"""
Abstract base for all remediation strategies.

Implements Template Method pattern where subclasses override specific steps
while base class orchestrates overall flow and provides common utilities.

Subclass Responsibilities:
    - Implement strategy_type property
    - Implement can_handle() logic
    - Implement apply_strategy() patch generation
    - Optionally override estimate_complexity()

Usage:
    >>> strategy = DependencyUpgradeStrategy()
    >>> if await strategy.can_handle(apv, confirmation):
    ...     patch = await strategy.apply_strategy(apv, confirmation)
```

**Public Methods:**

- `def strategy_type(self) -> RemediationStrategy`
- `def estimate_complexity(self, apv`

---

### `CodePatchLLMStrategy`

**File:** `code_patch_llm.py`

```python
class CodePatchLLMStrategy(BaseStrategy):
```

**Description:**
```
"""
LLM-guided code patching strategy.

Uses LLM (Claude, GPT-4) to generate patches for vulnerabilities
when ast-grep patterns available but no maintainer fix exists.

Algorithm:
1. Check if ast_grep_patterns exist in APV
2. Extract vulnerable code locations from confirmation
3. Read surrounding code context (±20 lines)
4. Construct structured prompt with vuln + code + context
5. Call LLM with low temperature (0.3) for determinism
6. Extract unified diff from LLM response
7. Validate diff format and confidence score
8. Return Patch with confidence 0.6-0.8
```

**Public Methods:**

- `def strategy_type(self) -> RemediationStrategy`

---

### `DependencyUpgradeStrategy`

**File:** `dependency_upgrade.py`

```python
class DependencyUpgradeStrategy(BaseStrategy):
```

**Description:**
```
"""
Generates dependency upgrade patches.

Handles:
- Python: pyproject.toml, requirements.txt, Pipfile
- JavaScript: package.json, yarn.lock
- Go: go.mod
- Java: pom.xml, build.gradle
- Rust: Cargo.toml

Phase 3 scope: Python (pyproject.toml) implementation
Future: Expand to other ecosystems

Usage:
    >>> strategy = DependencyUpgradeStrategy(codebase_root=Path("/app"))
    >>> if await strategy.can_handle(apv, confirmation):
```

**Public Methods:**

- `def strategy_type(self) -> RemediationStrategy`

---

### `NoStrategyAvailableError`

**File:** `strategy_selector.py`

```python
class NoStrategyAvailableError(Exception):
```

**Description:**
```
"""Raised when no strategy can handle APV."""

pass


class StrategySelector:
"""
Selects remediation strategy based on APV characteristics.

Selection Logic:
    1. Check each strategy's can_handle() in priority order
    2. Return first strategy that can handle
    3. Raise NoStrategyAvailableError if none applicable

Priority Order (injected via constructor):
    Typically: DependencyUpgrade → CodePatchLLM → CoagulationWAF → ManualReview
```

**Public Methods:**


---

### `StrategySelector`

**File:** `strategy_selector.py`

```python
class StrategySelector:
```

**Description:**
```
"""
Selects remediation strategy based on APV characteristics.

Selection Logic:
    1. Check each strategy's can_handle() in priority order
    2. Return first strategy that can handle
    3. Raise NoStrategyAvailableError if none applicable

Priority Order (injected via constructor):
    Typically: DependencyUpgrade → CodePatchLLM → CoagulationWAF → ManualReview

Usage:
    >>> strategies = [
    ...     DependencyUpgradeStrategy(),
    ...     CodePatchLLMStrategy(llm_client),
    ...     ManualReviewStrategy(),
```

**Public Methods:**

- `def get_strategies(self) -> List[BaseStrategy]`

---

### `LLMModel`

**File:** `llm_cost_tracker.py`

```python
class LLMModel(str, Enum):
```

**Description:**
```
"""Supported LLM models"""
CLAUDE_3_7_SONNET = "claude-3-7-sonnet"
CLAUDE_3_5_SONNET = "claude-3-5-sonnet"
GPT_4_TURBO = "gpt-4-turbo"
GPT_4O = "gpt-4o"
GEMINI_2_5_PRO = "gemini-2-5-pro"
GEMINI_2_0_FLASH = "gemini-2-0-flash-exp"


# Prometheus Metrics
llm_tokens_total = Counter(
'llm_tokens_total',
'Total LLM tokens used',
['model', 'type', 'strategy']  # type = input/output
)
```

**Public Methods:**


---

### `CostRecord`

**File:** `llm_cost_tracker.py`

```python
class CostRecord:
```

**Description:**
```
"""Single cost record"""

timestamp: datetime
model: LLMModel
strategy: str  # e.g., "dependency_upgrade", "code_patch_llm"
input_tokens: int
output_tokens: int
cost_usd: float
metadata: Dict

def to_dict(self) -> Dict:
    """Convert to dictionary"""
    return {
        **asdict(self),
        "timestamp": self.timestamp.isoformat(),
        "model": self.model.value
```

**Public Methods:**

- `def to_dict(self) -> Dict`

---

### `LLMCostTracker`

**File:** `llm_cost_tracker.py`

```python
class LLMCostTracker:
```

**Description:**
```
"""
Track LLM API costs and enforce budget limits.

Monitors token usage, calculates costs, exports metrics, and
enforces monthly budget limits.

Usage:
    >>> tracker = LLMCostTracker(monthly_budget=50.0)
    >>> record = await tracker.track_request(
    ...     model=LLMModel.CLAUDE_3_7_SONNET,
    ...     strategy="code_patch_llm",
    ...     input_tokens=1500,
    ...     output_tokens=800,
    ...     metadata={"apv_id": "apv_001"}
    ... )
    >>> print(f"Cost: ${record.cost_usd:.4f}")
```

**Public Methods:**

- `def get_monthly_cost(self, month`
- `def get_daily_cost(self, date`
- `def get_cost_by_strategy(`
- `def get_cost_by_model(`
- `def check_budget_status(self) -> Dict`
- `def generate_monthly_report(self, month`

---

### `BudgetExceededError`

**File:** `llm_cost_tracker.py`

```python
class BudgetExceededError(Exception):
```

**Description:**
```
"""Raised when monthly budget is exceeded"""
pass


# Convenience function
def get_cost_tracker(
monthly_budget: Optional[float] = None
) -> LLMCostTracker:
"""
Get global cost tracker instance.

Args:
    monthly_budget: Optional budget override

Returns:
    LLMCostTracker singleton
```

**Public Methods:**


---

## 4. Data Models

### `models.py`

#### `GitApplyResult`

```python
    Attributes:
        success: Whether patch was applied successfully
        commit_sha: Git commit SHA if committed (None if not yet committed)
        files_changed: List of file paths modified by patch
        conflicts: List of files with merge conflicts (empty if none)
        error_message: Error description if success=False
    Example:
    success: bool = Field(
    commit_sha: Optional[str] = Field(
    files_changed: list[str] = Field(
    conflicts: list[str] = Field(
```

#### `PushResult`

```python
    Attributes:
        success: Whether push succeeded
        branch: Local branch name that was pushed
        remote_ref: Remote reference (e.g. 'origin/remediation/CVE-123')
        error_message: Error description if success=False
    Example:
    success: bool = Field(
    branch: str = Field(
    remote_ref: Optional[str] = Field(
    error_message: Optional[str] = Field(
```

#### `PRResult`

```python
    Attributes:
        success: Whether PR was created successfully
        pr_number: GitHub PR number (None if creation failed)
        pr_url: Full URL to PR on GitHub (None if creation failed)
        error_message: Error description if success=False
    Example:
        ...     pr_url="https://github.com/org/repo/pull/42"
    success: bool = Field(
    pr_number: Optional[int] = Field(
    pr_url: Optional[HttpUrl] = Field(
    error_message: Optional[str] = Field(
```

#### `ValidationResult`

```python
    Attributes:
        passed: Whether all validations passed
        checks_run: List of validation check names executed
        failures: List of failed check descriptions
        warnings: List of warning messages (non-blocking)
    Example:
    passed: bool = Field(
    checks_run: list[str] = Field(
    failures: list[str] = Field(
    warnings: list[str] = Field(
```

#### `ConflictReport`

```python
    Attributes:
        has_conflicts: Whether any conflicts were detected
        conflicting_files: List of files with conflicts
        resolution_suggestions: AI-generated suggestions for conflict resolution
    Example:
    has_conflicts: bool = Field(
    conflicting_files: list[str] = Field(
    resolution_suggestions: list[str] = Field(
```

#### `GitConfig`

```python
    Attributes:
        repo_path: Absolute path to local Git repository
        remote_url: URL of remote repository
        default_branch: Default base branch (usually 'main' or 'develop')
        branch_prefix: Prefix for remediation branches (e.g. 'remediation')
        github_token: GitHub Personal Access Token (excluded from serialization)
        commit_author: Name used in commit metadata
        commit_email: Email used in commit metadata
    Security:
    Example:
        ...     remote_url="https://github.com/org/repo",
    repo_path: Path = Field(
    remote_url: HttpUrl = Field(
    default_branch: str = Field(
```

### `test_patch_models.py`

### `test_git_models.py`

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
    #   starlette
    #   watchfiles
click==8.3.0
    # via uvicorn
fastapi==0.118.1
    # via maximus-eureka (pyproject.toml)
h11==0.16.0
    # via uvicorn
httptools==0.6.4
    # via uvicorn
idna==3.10
    # via anyio
pydantic==2.12.0
    # via
    #   maximus-eureka (pyproject.toml)
    #   fastapi
pydantic-core==2.41.1
    # via pydantic
python-dotenv==1.1.1
    # via uvicorn
pyyaml==6.0.3
    # via uvicorn
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
    # via maximus-eureka (pyproject.toml)
uvloop==0.21.0
    # via uvicorn
watchfiles==1.1.0
    # via uvicorn
websockets==15.0.1
    # via uvicorn
aiokafka>=0.8.0
async-timeout>=4.0.0
```

