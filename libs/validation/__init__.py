"""
Input validation library for Maximus AI services.
Provides Pydantic schemas for request/response validation.
"""

from .schemas import (
    HealthResponse,
    ServiceType,
    BrowserActionRequest,
    NarrativeRequest,
    ConsciousnessRequest,
    ErrorResponse,
    SuccessResponse,
)

__all__ = [
    "HealthResponse",
    "ServiceType",
    "BrowserActionRequest",
    "NarrativeRequest",
    "ConsciousnessRequest",
    "ErrorResponse",
    "SuccessResponse",
]
