"""
MAXIMUS Integration Package

Connect max-code-cli to MAXIMUS 103 microservices ecosystem.

Components:
- MaximusClient: HTTP client with JWT + retry
- ConstitutionalValidator: Lei Zero + Lei I validation
- ImmuneScanner: 8-cell biomimetic security
- ConsciousnessChecker: GWT awareness metrics

Research-based implementation (Jan 2025):
- Hybrid: Claude for reasoning, OpenAI for parallel ops
- Connection pooling (100 max)
- Circuit breakers + exponential backoff
- JWT authentication
"""
from .backend_client import MaximusClient, MaximusError, ServiceUnavailable
from .service_registry import MAXIMUS_SERVICES, ServiceTier, get_service_config
from .constitutional_validator import ConstitutionalValidator, ValidationResult
from .immune_scanner import ImmuneScanner, SecurityReport, CellType
from .consciousness_checker import ConsciousnessChecker, ConsciousnessReport

__all__ = [
    "MaximusClient",
    "MaximusError",
    "ServiceUnavailable",
    "MAXIMUS_SERVICES",
    "ServiceTier",
    "get_service_config",
    "ConstitutionalValidator",
    "ValidationResult",
    "ImmuneScanner",
    "SecurityReport",
    "CellType",
    "ConsciousnessChecker",
    "ConsciousnessReport",
]
