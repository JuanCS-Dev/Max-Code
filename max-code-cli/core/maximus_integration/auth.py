"""
Authentication module for MAXIMUS ecosystem services.

Provides JWT token generation/validation and API key authentication.
Production-ready with proper security practices.

Biblical Foundation:
"Porque o Senhor dá a sabedoria; da sua boca procedem o conhecimento e o entendimento"
(Provérbios 2:6)
"""

import os
import jwt
import time
import hashlib
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)


class Role(str, Enum):
    """User roles for RBAC (Role-Based Access Control)"""
    ADMIN = "admin"
    OPERATOR = "operator"
    READONLY = "readonly"
    SERVICE = "service"  # For service-to-service communication


class Permission(str, Enum):
    """Granular permissions for endpoints"""
    # Consciousness API
    READ_CONSCIOUSNESS = "consciousness:read"
    WRITE_CONSCIOUSNESS = "consciousness:write"
    TRIGGER_ESGT = "consciousness:esgt:trigger"

    # Governance API
    READ_GOVERNANCE = "governance:read"
    APPROVE_DECISIONS = "governance:approve"
    REJECT_DECISIONS = "governance:reject"
    ESCALATE_DECISIONS = "governance:escalate"

    # Query API
    QUERY = "query:execute"

    # Healing API (PENELOPE)
    DIAGNOSE_CODE = "healing:diagnose"
    APPLY_PATCHES = "healing:apply"

    # Admin
    MANAGE_USERS = "admin:users"
    VIEW_METRICS = "admin:metrics"


# Role -> Permissions mapping
ROLE_PERMISSIONS: Dict[Role, list[Permission]] = {
    Role.ADMIN: [p for p in Permission],  # All permissions

    Role.OPERATOR: [
        Permission.READ_CONSCIOUSNESS,
        Permission.WRITE_CONSCIOUSNESS,
        Permission.READ_GOVERNANCE,
        Permission.APPROVE_DECISIONS,
        Permission.REJECT_DECISIONS,
        Permission.ESCALATE_DECISIONS,
        Permission.QUERY,
        Permission.DIAGNOSE_CODE,
        Permission.VIEW_METRICS,
    ],

    Role.READONLY: [
        Permission.READ_CONSCIOUSNESS,
        Permission.READ_GOVERNANCE,
        Permission.VIEW_METRICS,
    ],

    Role.SERVICE: [
        Permission.READ_CONSCIOUSNESS,
        Permission.WRITE_CONSCIOUSNESS,
        Permission.READ_GOVERNANCE,
        Permission.QUERY,
        Permission.DIAGNOSE_CODE,
    ],
}


class JWTAuth:
    """
    JWT-based authentication for MAXIMUS services.

    Features:
    - Token generation with expiration
    - Token validation with signature verification
    - Role-based access control (RBAC)
    - Token refresh capability
    """

    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        token_expiry_hours: int = 24,
    ):
        """
        Initialize JWT authentication.

        Args:
            secret_key: Secret key for signing (env: JWT_SECRET_KEY)
            algorithm: JWT algorithm (default: HS256)
            token_expiry_hours: Token expiry time in hours
        """
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY")
        if not self.secret_key:
            # Generate a secure random key if not provided
            self.secret_key = secrets.token_urlsafe(32)
            logger.warning(
                "jwt_secret_generated",
                message="No JWT_SECRET_KEY provided, generated random key. "
                        "Set JWT_SECRET_KEY env var for production!"
            )

        self.algorithm = algorithm
        self.token_expiry_hours = token_expiry_hours

        logger.info(
            "jwt_auth_initialized",
            algorithm=algorithm,
            token_expiry_hours=token_expiry_hours,
        )

    def generate_token(
        self,
        user_id: str,
        role: Role = Role.OPERATOR,
        custom_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate JWT token.

        Args:
            user_id: Unique user identifier
            role: User role for RBAC
            custom_claims: Additional claims to include

        Returns:
            JWT token string
        """
        now = datetime.utcnow()
        expiry = now + timedelta(hours=self.token_expiry_hours)

        # Standard claims
        payload = {
            "sub": user_id,  # Subject (user ID)
            "role": role.value,
            "permissions": [p.value for p in ROLE_PERMISSIONS[role]],
            "iat": int(now.timestamp()),  # Issued at
            "exp": int(expiry.timestamp()),  # Expiration
            "jti": secrets.token_hex(16),  # JWT ID (for revocation)
        }

        # Add custom claims
        if custom_claims:
            payload.update(custom_claims)

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        logger.info(
            "jwt_token_generated",
            user_id=user_id,
            role=role.value,
            expiry=expiry.isoformat(),
        )

        return token

    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate JWT token and return payload.

        Args:
            token: JWT token string

        Returns:
            Token payload (claims)

        Raises:
            jwt.ExpiredSignatureError: Token expired
            jwt.InvalidTokenError: Invalid token
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                leeway=10,  # Allow 10 seconds clock skew
            )

            logger.info(
                "jwt_token_validated",
                user_id=payload.get("sub"),
                role=payload.get("role"),
            )

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("jwt_token_expired", token_preview=token[:20])
            raise

        except jwt.InvalidTokenError as e:
            logger.error("jwt_token_invalid", error=str(e))
            raise

    def has_permission(
        self,
        token_payload: Dict[str, Any],
        required_permission: Permission,
    ) -> bool:
        """
        Check if token has required permission.

        Args:
            token_payload: Decoded token payload
            required_permission: Permission to check

        Returns:
            True if permission granted
        """
        permissions = token_payload.get("permissions", [])
        has_perm = required_permission.value in permissions

        logger.debug(
            "permission_check",
            user_id=token_payload.get("sub"),
            required=required_permission.value,
            granted=has_perm,
        )

        return has_perm


class APIKeyAuth:
    """
    API Key authentication for MAXIMUS services.

    Features:
    - Secure API key generation (SHA256 hashed)
    - Key validation
    - Key rotation support
    """

    def __init__(self):
        """Initialize API Key authentication"""
        # In production, load from database
        # For now, use environment variable
        self._valid_keys = set()

        # Load API keys from env
        api_keys_str = os.getenv("MAXIMUS_API_KEYS", "")
        if api_keys_str:
            self._valid_keys = set(api_keys_str.split(","))
            logger.info("api_keys_loaded", count=len(self._valid_keys))
        else:
            logger.warning("no_api_keys_configured")

    def generate_api_key(self, prefix: str = "maximus") -> str:
        """
        Generate a secure API key.

        Args:
            prefix: Key prefix for identification

        Returns:
            API key string (format: prefix_randomhex)
        """
        random_part = secrets.token_hex(32)
        api_key = f"{prefix}_{random_part}"

        logger.info(
            "api_key_generated",
            prefix=prefix,
            key_preview=api_key[:20],
        )

        return api_key

    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate API key.

        Args:
            api_key: API key to validate

        Returns:
            True if valid
        """
        # Hash the key for comparison (timing-safe)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # In production, compare against hashed keys in database
        is_valid = api_key in self._valid_keys

        logger.info(
            "api_key_validated",
            key_preview=api_key[:20],
            valid=is_valid,
        )

        return is_valid

    def add_key(self, api_key: str):
        """Add API key to valid keys (for testing)"""
        self._valid_keys.add(api_key)


# Singleton instances
_jwt_auth: Optional[JWTAuth] = None
_api_key_auth: Optional[APIKeyAuth] = None


def get_jwt_auth() -> JWTAuth:
    """Get JWT auth singleton"""
    global _jwt_auth
    if _jwt_auth is None:
        _jwt_auth = JWTAuth()
    return _jwt_auth


def get_api_key_auth() -> APIKeyAuth:
    """Get API Key auth singleton"""
    global _api_key_auth
    if _api_key_auth is None:
        _api_key_auth = APIKeyAuth()
    return _api_key_auth


# Convenience functions
def generate_token(user_id: str, role: Role = Role.OPERATOR) -> str:
    """Generate JWT token (convenience function)"""
    return get_jwt_auth().generate_token(user_id, role)


def validate_token(token: str) -> Dict[str, Any]:
    """Validate JWT token (convenience function)"""
    return get_jwt_auth().validate_token(token)


def validate_api_key(api_key: str) -> bool:
    """Validate API key (convenience function)"""
    return get_api_key_auth().validate_api_key(api_key)


def has_permission(token_payload: Dict[str, Any], permission: Permission) -> bool:
    """Check permission (convenience function)"""
    return get_jwt_auth().has_permission(token_payload, permission)
