"""
JWT Authentication Module for Maximus AI Services
==================================================

Simple JWT authentication for protecting API endpoints.

Constitution Compliance:
- P1 (Completude): Full implementation, no placeholders
- P2 (Validação): Token validation with proper error handling
- P3 (Ceticismo): Critical validation of all tokens

Features:
- JWT token creation and verification
- API key fallback for internal service-to-service communication
- Configurable expiration times
- FastAPI integration with Security dependencies

Usage:
    from libs.auth import verify_token, create_access_token
    from fastapi import Depends

    # Protect endpoint
    @app.get("/protected")
    async def protected_route(token_data: dict = Depends(verify_token)):
        return {"user": token_data.get("sub")}

    # Create token
    token = create_access_token({"sub": "user123", "role": "admin"})

Security Notes:
- JWT_SECRET MUST be set to a strong random value in production
- Tokens expire after 60 minutes by default (configurable)
- API keys are comma-separated in INTERNAL_API_KEYS env var
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

try:
    import jwt
    from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    jwt = None
    ExpiredSignatureError = Exception
    InvalidTokenError = Exception

from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

class JWTConfig:
    """JWT Configuration from environment variables."""

    # JWT Secret Key (MUST be changed in production)
    SECRET_KEY = os.getenv("JWT_SECRET", "CHANGE_ME_TO_A_STRONG_RANDOM_SECRET")

    # Algorithm
    ALGORITHM = "HS256"

    # Token expiration (minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # Internal API Keys for service-to-service communication
    INTERNAL_API_KEYS = [
        key.strip()
        for key in os.getenv("INTERNAL_API_KEYS", "").split(",")
        if key.strip()
    ]

    # Warning if using default secret
    @classmethod
    def check_security(cls):
        """Check if using secure configuration."""
        if cls.SECRET_KEY == "CHANGE_ME_TO_A_STRONG_RANDOM_SECRET":
            logger.warning(
                "⚠️  SECURITY WARNING: Using default JWT_SECRET! "
                "Set JWT_SECRET environment variable to a strong random value."
            )
            return False
        return True


# Check security on import
JWTConfig.check_security()

# Security scheme
security = HTTPBearer(auto_error=True)
optional_security = HTTPBearer(auto_error=False)


# ============================================================================
# TOKEN CREATION
# ============================================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token.

    Args:
        data: Payload data to encode in token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string

    Raises:
        RuntimeError: If PyJWT not installed

    Example:
        >>> token = create_access_token({"sub": "user123", "role": "admin"})
        >>> token = create_access_token(
        ...     {"sub": "service_maba"},
        ...     expires_delta=timedelta(hours=24)
        ... )
    """
    if not JWT_AVAILABLE:
        raise RuntimeError(
            "PyJWT not installed. Install with: pip install pyjwt"
        )

    to_encode = data.copy()

    # Set expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
    })

    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        JWTConfig.SECRET_KEY,
        algorithm=JWTConfig.ALGORITHM
    )

    logger.debug(f"Created JWT token for subject: {data.get('sub', 'unknown')}")

    return encoded_jwt


# ============================================================================
# TOKEN VERIFICATION
# ============================================================================

def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    Verify JWT token from Authorization header.

    FastAPI dependency that extracts and validates JWT token.
    Use with Depends() to protect endpoints.

    Args:
        credentials: HTTP Bearer credentials from request

    Returns:
        Decoded token payload (dict)

    Raises:
        HTTPException: 401 if token invalid/expired, 403 if PyJWT missing

    Example:
        @app.get("/protected")
        async def protected(token_data: dict = Depends(verify_token)):
            user_id = token_data.get("sub")
            return {"user": user_id}
    """
    if not JWT_AVAILABLE:
        logger.error("PyJWT not installed - cannot verify tokens")
        raise HTTPException(
            status_code=503,
            detail="Authentication service unavailable (PyJWT not installed)"
        )

    token = credentials.credentials

    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            JWTConfig.SECRET_KEY,
            algorithms=[JWTConfig.ALGORITHM]
        )

        logger.debug(f"Token verified for subject: {payload.get('sub', 'unknown')}")

        return payload

    except ExpiredSignatureError:
        logger.warning("Token expired")
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_optional_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(optional_security)
) -> Optional[Dict[str, Any]]:
    """
    Get token if present, but don't fail if missing.

    Use for endpoints that work with or without authentication.

    Args:
        credentials: Optional HTTP Bearer credentials

    Returns:
        Decoded token payload or None if no token provided

    Example:
        @app.get("/public-or-private")
        async def flexible(token_data: Optional[dict] = Depends(get_optional_token)):
            if token_data:
                return {"message": "authenticated", "user": token_data.get("sub")}
            return {"message": "anonymous"}
    """
    if not credentials:
        return None

    try:
        return verify_token(credentials)
    except HTTPException:
        return None


# ============================================================================
# API KEY AUTHENTICATION (Internal Services)
# ============================================================================

def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> bool:
    """
    Verify API key for internal service-to-service communication.

    Alternative to JWT for internal services. API keys are configured
    in INTERNAL_API_KEYS environment variable (comma-separated).

    Args:
        credentials: HTTP Bearer credentials from request

    Returns:
        True if API key valid

    Raises:
        HTTPException: 403 if API key invalid

    Example:
        @app.post("/internal/sync")
        async def internal_sync(authenticated: bool = Depends(verify_api_key)):
            # Only accessible with valid API key
            return {"status": "synced"}
    """
    api_key = credentials.credentials

    # Check if API key matches any configured keys
    if api_key in JWTConfig.INTERNAL_API_KEYS and api_key:
        logger.debug("API key verified")
        return True

    logger.warning(f"Invalid API key attempted")
    raise HTTPException(
        status_code=403,
        detail="Invalid API key",
        headers={"WWW-Authenticate": "Bearer"}
    )


def verify_token_or_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    Accept either JWT token or API key.

    Try JWT first, fall back to API key validation.
    Useful for endpoints that accept both user tokens and service API keys.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        Token payload dict (or {"type": "api_key"} for API keys)

    Raises:
        HTTPException: 401/403 if neither valid
    """
    # Try JWT first
    if JWT_AVAILABLE:
        try:
            return verify_token(credentials)
        except HTTPException:
            pass

    # Fall back to API key
    try:
        verify_api_key(credentials)
        return {"type": "api_key", "authenticated": True}
    except HTTPException:
        pass

    # Both failed
    raise HTTPException(
        status_code=401,
        detail="Invalid authentication credentials (neither JWT nor API key valid)",
        headers={"WWW-Authenticate": "Bearer"}
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_service_token(service_name: str, expires_hours: int = 24) -> str:
    """
    Create long-lived token for service-to-service communication.

    Args:
        service_name: Name of the service (e.g., "maba", "nis")
        expires_hours: Token expiration in hours (default 24)

    Returns:
        JWT token string

    Example:
        >>> token = create_service_token("maba", expires_hours=48)
    """
    return create_access_token(
        data={
            "sub": f"service_{service_name}",
            "type": "service",
            "service": service_name
        },
        expires_delta=timedelta(hours=expires_hours)
    )


def decode_token_unsafe(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode token WITHOUT verification (for debugging only).

    ⚠️  WARNING: Do NOT use for authentication!
    This is for debugging/logging purposes only.

    Args:
        token: JWT token string

    Returns:
        Decoded payload or None if invalid
    """
    if not JWT_AVAILABLE:
        return None

    try:
        # Decode without verification
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return payload
    except Exception as e:
        logger.debug(f"Failed to decode token: {e}")
        return None


# ============================================================================
# HEALTH CHECK HELPER
# ============================================================================

def check_auth_health() -> Dict[str, Any]:
    """
    Check authentication system health.

    Returns:
        Health status dict

    Example:
        >>> health = check_auth_health()
        >>> health["jwt_available"]
        True
    """
    return {
        "jwt_available": JWT_AVAILABLE,
        "jwt_library": "PyJWT" if JWT_AVAILABLE else "not installed",
        "secret_configured": JWTConfig.SECRET_KEY != "CHANGE_ME_TO_A_STRONG_RANDOM_SECRET",
        "api_keys_configured": len(JWTConfig.INTERNAL_API_KEYS) > 0,
        "token_expire_minutes": JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES,
    }


# ============================================================================
# FASTAPI INTEGRATION HELPERS
# ============================================================================

def get_current_user_id(token_data: dict = Security(verify_token)) -> str:
    """
    Extract user ID from verified token.

    Convenience dependency that returns just the user ID.

    Args:
        token_data: Verified token payload

    Returns:
        User ID (subject) from token

    Raises:
        HTTPException: 401 if subject missing

    Example:
        @app.get("/me")
        async def get_me(user_id: str = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token missing subject (user ID)"
        )
    return user_id


def require_role(required_role: str):
    """
    Create dependency that requires specific role.

    Args:
        required_role: Role name required (e.g., "admin")

    Returns:
        FastAPI dependency function

    Example:
        admin_required = require_role("admin")

        @app.delete("/users/{user_id}")
        async def delete_user(
            user_id: str,
            token_data: dict = Depends(admin_required)
        ):
            # Only admins can access this
            pass
    """
    def role_checker(token_data: dict = Security(verify_token)) -> dict:
        user_role = token_data.get("role")
        if user_role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Requires role: {required_role}"
            )
        return token_data

    return role_checker
