"""
Pydantic Validation Schemas for Maximus AI Services
====================================================

Input validation schemas using Pydantic for all API requests.

Constitution Compliance:
- P1 (Completude): Complete validation rules
- P2 (Validação): Validate all inputs before processing
- P3 (Ceticismo): Critical skepticism on all user inputs

Features:
- Type validation
- Range validation
- Pattern matching (regex)
- Payload size limits
- Whitelist validation
- Custom validators

Security:
- Prevents payload attacks (size limits)
- Prevents injection attacks (type validation)
- Prevents malicious URLs (HttpUrl type)
- Action whitelisting

Usage:
    from libs.validation import BrowserActionRequest
    from fastapi import FastAPI

    app = FastAPI()

    @app.post("/browser/action")
    async def browser_action(request: BrowserActionRequest):
        # Request is automatically validated
        url = request.url  # Already validated as HttpUrl
        action = request.action  # Already whitelisted
        return {"status": "ok"}
"""

import re
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator, HttpUrl, constr, conint


# ============================================================================
# ENUMS
# ============================================================================

class ServiceType(str, Enum):
    """Valid Maximus service types."""
    CORE = "core"
    MABA = "maba"
    NIS = "nis"
    PENELOPE = "penelope"
    ORCHESTRATOR = "orchestrator"
    EUREKA = "eureka"
    ORACULO = "oraculo"


class HealthStatus(str, Enum):
    """Health check status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class BrowserActionType(str, Enum):
    """Whitelisted browser actions for MABA."""
    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    SCREENSHOT = "screenshot"
    EXTRACT = "extract"
    SCROLL = "scroll"
    WAIT = "wait"


class NarrativeType(str, Enum):
    """Types of narratives for NIS."""
    ANOMALY = "anomaly"
    TREND = "trend"
    SUMMARY = "summary"
    ALERT = "alert"


class SeverityLevel(str, Enum):
    """Severity levels for alerts and events."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseRequest(BaseModel):
    """Base request schema with common fields."""

    request_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Optional request ID for tracking"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata"
    )

    @field_validator('metadata')
    @classmethod
    def validate_metadata_size(cls, v):
        """Limit metadata size to prevent payload attacks."""
        if v and len(str(v)) > 10000:  # 10KB limit
            raise ValueError("Metadata too large (max 10KB)")
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "request_id": "req-123-abc",
                "metadata": {"source": "web_ui"}
            }
        }


class BaseResponse(BaseModel):
    """Base response schema with common fields."""

    success: bool = Field(..., description="Whether the operation succeeded")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    service: Optional[ServiceType] = None

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "service": "core"
            }
        }


# ============================================================================
# HEALTH CHECK SCHEMAS
# ============================================================================

class HealthResponse(BaseResponse):
    """Standard health check response for all services."""

    status: HealthStatus = Field(..., description="Service health status")
    service: ServiceType = Field(..., description="Service name")
    version: constr(pattern=r'^\d+\.\d+\.\d+$') = Field(  # type: ignore
        ...,
        description="Service version (semver format)"
    )
    dependencies: Optional[Dict[str, str]] = Field(
        None,
        description="Status of service dependencies (postgres, redis, etc.)"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "status": "healthy",
                "service": "core",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00Z",
                "dependencies": {
                    "postgres": "healthy",
                    "redis": "healthy"
                }
            }
        }


# ============================================================================
# MABA (Browser Automation) SCHEMAS
# ============================================================================

class BrowserActionRequest(BaseRequest):
    """Request for MABA browser automation action."""

    url: HttpUrl = Field(..., description="Target URL for browser action")

    action: BrowserActionType = Field(
        ...,
        description="Browser action to perform (whitelisted)"
    )

    parameters: Optional[Dict[str, Any]] = Field(
        None,
        description="Action-specific parameters"
    )

    timeout_seconds: conint(ge=1, le=300) = Field(  # type: ignore
        default=30,
        description="Timeout in seconds (1-300)"
    )

    session_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Optional browser session ID for reuse"
    )

    @field_validator('parameters')
    @classmethod
    def validate_parameters_size(cls, v):
        """Limit parameter size to prevent payload attacks."""
        if v and len(str(v)) > 10000:  # 10KB limit
            raise ValueError("Parameters too large (max 10KB)")
        return v

    @field_validator('url')
    @classmethod
    def validate_url_safety(cls, v):
        """Basic URL safety checks."""
        url_str = str(v)

        # Block localhost/internal IPs (unless explicitly allowed)
        internal_patterns = [
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
            '192.168.',
            '10.',
            '172.16.',
        ]

        # Allow internal URLs only if they're explicitly Maximus services
        if any(pattern in url_str for pattern in internal_patterns):
            if 'maximus' not in url_str.lower():
                raise ValueError(
                    "Internal/localhost URLs not allowed (security policy)"
                )

        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "action": "navigate",
                "parameters": {"wait_until": "networkidle"},
                "timeout_seconds": 30,
                "session_id": "sess-abc-123"
            }
        }


class BrowserActionResponse(BaseResponse):
    """Response from MABA browser action."""

    action: BrowserActionType
    url: str
    duration_ms: int = Field(..., description="Action duration in milliseconds")
    result: Optional[Dict[str, Any]] = Field(
        None,
        description="Action-specific result data"
    )
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "action": "navigate",
                "url": "https://example.com",
                "duration_ms": 1523,
                "result": {"title": "Example Domain", "status_code": 200}
            }
        }


# ============================================================================
# NIS (Narrative Intelligence) SCHEMAS
# ============================================================================

class NarrativeRequest(BaseRequest):
    """Request for NIS narrative generation."""

    metric_name: constr(min_length=1, max_length=200) = Field(  # type: ignore
        ...,
        description="Name of the metric"
    )

    metric_value: float = Field(..., description="Current metric value")

    baseline_value: Optional[float] = Field(
        None,
        description="Expected/baseline value for comparison"
    )

    context: Optional[constr(max_length=5000)] = Field(  # type: ignore
        None,
        description="Additional context for narrative generation"
    )

    narrative_type: NarrativeType = Field(
        default=NarrativeType.ANOMALY,
        description="Type of narrative to generate"
    )

    severity: Optional[SeverityLevel] = Field(
        None,
        description="Severity level if known"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "metric_name": "cpu_usage_percent",
                "metric_value": 95.5,
                "baseline_value": 45.0,
                "context": "High CPU usage detected on production server",
                "narrative_type": "anomaly",
                "severity": "high"
            }
        }


class NarrativeResponse(BaseResponse):
    """Response from NIS narrative generation."""

    narrative: str = Field(..., description="Generated narrative text")
    metric_name: str
    metric_value: float
    narrative_type: NarrativeType
    cost_usd: Optional[float] = Field(None, description="API cost in USD")
    cached: bool = Field(default=False, description="Whether result was cached")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "narrative": "CPU usage has spiked to 95.5%, significantly above the baseline of 45%. This represents a 112% increase and may indicate a performance issue or resource leak.",
                "metric_name": "cpu_usage_percent",
                "metric_value": 95.5,
                "narrative_type": "anomaly",
                "cost_usd": 0.002,
                "cached": False
            }
        }


# ============================================================================
# CORE (Consciousness) SCHEMAS
# ============================================================================

class ConsciousnessRequest(BaseRequest):
    """Request for Maximus Core consciousness processing."""

    input_data: Dict[str, Any] = Field(
        ...,
        description="Input data for consciousness processing"
    )

    require_ethical_validation: bool = Field(
        default=False,
        description="Whether to require ethical validation (PENELOPE)"
    )

    priority: conint(ge=1, le=10) = Field(  # type: ignore
        default=5,
        description="Processing priority (1=lowest, 10=highest)"
    )

    context: Optional[str] = Field(
        None,
        max_length=10000,
        description="Additional context"
    )

    @field_validator('input_data')
    @classmethod
    def validate_input_size(cls, v):
        """Prevent payload attacks."""
        payload_size = len(str(v))
        if payload_size > 100000:  # 100KB limit
            raise ValueError(
                f"Input data too large: {payload_size} bytes (max 100KB)"
            )
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "input_data": {
                    "task": "analyze_security_event",
                    "event_data": {"type": "login_failure", "count": 5}
                },
                "require_ethical_validation": True,
                "priority": 8,
                "context": "Multiple failed login attempts from same IP"
            }
        }


class ConsciousnessResponse(BaseResponse):
    """Response from Maximus Core consciousness processing."""

    output_data: Dict[str, Any] = Field(
        ...,
        description="Processing results"
    )

    processing_time_ms: int = Field(..., description="Processing time in ms")

    ethical_validation: Optional[Dict[str, Any]] = Field(
        None,
        description="Ethical validation results if requested"
    )

    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0-1.0)"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "output_data": {
                    "recommendation": "block_ip",
                    "reason": "Brute force attack detected"
                },
                "processing_time_ms": 245,
                "ethical_validation": {"approved": True, "validator": "PENELOPE"},
                "confidence": 0.95
            }
        }


# ============================================================================
# GENERIC RESPONSE SCHEMAS
# ============================================================================

class ErrorResponse(BaseResponse):
    """Standard error response."""

    success: bool = Field(default=False)
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": False,
                "timestamp": "2024-01-15T10:30:00Z",
                "error": "Invalid input parameters",
                "error_code": "VALIDATION_ERROR",
                "details": {"field": "url", "reason": "Invalid URL format"}
            }
        }


class SuccessResponse(BaseResponse):
    """Generic success response."""

    success: bool = Field(default=True)
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "message": "Operation completed successfully",
                "data": {"id": "123", "status": "active"}
            }
        }


# ============================================================================
# PAGINATION SCHEMAS
# ============================================================================

class PaginationParams(BaseModel):
    """Standard pagination parameters."""

    page: conint(ge=1) = Field(default=1, description="Page number (1-indexed)")  # type: ignore
    page_size: conint(ge=1, le=100) = Field(default=20, description="Items per page (max 100)")  # type: ignore
    sort_by: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 20,
                "sort_by": "created_at",
                "sort_order": "desc"
            }
        }


class PaginatedResponse(BaseResponse):
    """Generic paginated response."""

    items: List[Any] = Field(..., description="Page items")
    total: int = Field(..., description="Total item count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total pages")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "items": [{"id": 1}, {"id": 2}],
                "total": 50,
                "page": 1,
                "page_size": 20,
                "total_pages": 3
            }
        }
