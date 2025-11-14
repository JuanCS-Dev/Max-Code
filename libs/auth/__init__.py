"""
Authentication library for Maximus AI services.
Provides JWT-based authentication for API endpoints.
"""

from .jwt_auth import (
    create_access_token,
    verify_token,
    verify_api_key,
    get_optional_token,
    JWTConfig,
)

__all__ = [
    "create_access_token",
    "verify_token",
    "verify_api_key",
    "get_optional_token",
    "JWTConfig",
]
