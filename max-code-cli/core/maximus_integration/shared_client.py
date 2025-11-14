"""
Shared MAXIMUS Client - Simplified HTTP client for all services

Wrapper around existing MaximusClient for common operations across all 8 services.
Uses httpx (already installed) and integrates with config/settings.py.

Biblical Foundation:
"Portanto, tudo o que vós quereis que os homens vos façam, fazei-lho também vós"
(Mateus 7:12)
"""
import httpx
import time
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from enum import Enum

from config.settings import get_settings
from config.logging_config import get_logger

logger = get_logger(__name__)


# Service registry (aligned with config/settings.py)
class MaximusService(str, Enum):
    """Available MAXIMUS services"""
    CORE = "core"
    PENELOPE = "penelope"
    NIS = "nis"
    MABA = "maba"
    ORCHESTRATOR = "orchestrator"
    ORACULO = "oraculo"
    ATLAS = "atlas"
    EUREKA = "eureka"  # Service discovery


@dataclass
class ServiceResponse:
    """Response from MAXIMUS service"""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    service: Optional[str] = None


class SharedMaximusClient:
    """
    Simplified client for MAXIMUS services
    
    Wraps httpx with retry logic, timeout handling, and error recovery.
    Integrates with existing config/settings.py for service URLs.
    
    Examples:
        client = SharedMaximusClient()
        
        # Single service health check
        response = client.health_check(MaximusService.CORE)
        
        # All services health check
        results = client.health_check_all()
        
        # Custom request
        response = client.request(
            MaximusService.PENELOPE,
            "/analyze",
            method="POST",
            data={"text": "Hello"}
        )
    """
    
    def __init__(self):
        """Initialize client with settings from config"""
        self.settings = get_settings()
        self.maximus = self.settings.maximus
        self.timeout = self.maximus.timeout_seconds
        self.max_retries = self.maximus.max_retries
        
        # Map service enum to URL
        self.service_urls = {
            MaximusService.CORE: self.maximus.core_url,
            MaximusService.PENELOPE: self.maximus.penelope_url,
            MaximusService.NIS: self.maximus.nis_url,
            MaximusService.MABA: self.maximus.maba_url,
            MaximusService.ORCHESTRATOR: self.maximus.orchestrator_url,
            MaximusService.ORACULO: self.maximus.oraculo_url,
            MaximusService.ATLAS: self.maximus.atlas_url,
        }
        
        # Eureka (if exists in settings, otherwise default)
        if hasattr(self.maximus, 'eureka_url'):
            self.service_urls[MaximusService.EUREKA] = self.maximus.eureka_url
        else:
            self.service_urls[MaximusService.EUREKA] = "http://localhost:8151"
    
    def request(
        self,
        service: MaximusService,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict] = None
    ) -> ServiceResponse:
        """
        Make HTTP request to MAXIMUS service
        
        Args:
            service: Service to call (MaximusService enum)
            endpoint: API endpoint path (e.g., "/health", "/analyze")
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request body (for POST/PUT)
            params: Query parameters
            timeout: Request timeout (override default)
            headers: Additional HTTP headers
        
        Returns:
            ServiceResponse with success, data, error
        """
        # Validate service
        if service not in self.service_urls:
            return ServiceResponse(
                success=False,
                error=f"Unknown service: {service}",
                service=service.value
            )
        
        # Build URL
        base_url = self.service_urls[service]
        url = f"{base_url}{endpoint}"
        
        # Timeout
        request_timeout = timeout or self.timeout
        
        # Headers
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)
        
        # Retry loop
        last_error = None
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                
                with httpx.Client(timeout=request_timeout) as client:
                    response = client.request(
                        method,
                        url,
                        json=data,
                        params=params,
                        headers=req_headers
                    )
                    
                    elapsed_ms = (time.time() - start_time) * 1000
                    
                    # Success (2xx)
                    if 200 <= response.status_code < 300:
                        try:
                            response_data = response.json()
                        except (ValueError, TypeError, AttributeError) as e:
                            # JSON decode failed - return raw text
                            # Common with non-JSON responses
                            response_data = {"text": response.text}
                        
                        logger.debug(
                            f"{service.value} {method} {endpoint}: "
                            f"{response.status_code} ({elapsed_ms:.1f}ms)"
                        )
                        
                        return ServiceResponse(
                            success=True,
                            data=response_data,
                            status_code=response.status_code,
                            response_time_ms=round(elapsed_ms, 1),
                            service=service.value
                        )
                    
                    # Error (4xx, 5xx)
                    else:
                        error_text = response.text[:200]
                        logger.warning(
                            f"{service.value} {method} {endpoint}: "
                            f"{response.status_code} - {error_text}"
                        )
                        
                        return ServiceResponse(
                            success=False,
                            error=f"HTTP {response.status_code}: {error_text}",
                            status_code=response.status_code,
                            response_time_ms=round(elapsed_ms, 1),
                            service=service.value
                        )
            
            except httpx.TimeoutException as e:
                last_error = f"Request timeout after {request_timeout}s"
                logger.warning(f"{service.value} timeout (attempt {attempt+1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
            
            except httpx.ConnectError as e:
                last_error = f"Connection error: {str(e)}"
                logger.warning(f"{service.value} connection failed (attempt {attempt+1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(1 * (attempt + 1))
            
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                logger.error(f"{service.value} error: {e}", exc_info=True)
                if attempt < self.max_retries - 1:
                    time.sleep(1 * (attempt + 1))
        
        # All retries exhausted
        return ServiceResponse(
            success=False,
            error=last_error or "Max retries exceeded",
            status_code=503,
            service=service.value
        )
    
    def health_check(self, service: MaximusService, timeout: int = 10) -> ServiceResponse:
        """
        Quick health check for a service
        
        Args:
            service: Service to check
            timeout: Request timeout
        
        Returns:
            ServiceResponse with health data or error
        """
        return self.request(service, "/health", timeout=timeout)
    
    def health_check_all(self, timeout: int = 10) -> List[ServiceResponse]:
        """
        Check health of all services (sequential for simplicity)
        
        Args:
            timeout: Request timeout per service
        
        Returns:
            List of ServiceResponse objects
        """
        results = []
        
        for service in MaximusService:
            try:
                response = self.health_check(service, timeout=timeout)
                results.append(response)
            except Exception as e:
                logger.error(f"Error checking {service.value}: {e}")
                results.append(ServiceResponse(
                    success=False,
                    error=str(e),
                    service=service.value
                ))
        
        return results
    
    def get_service_url(self, service: MaximusService) -> str:
        """Get configured URL for a service"""
        return self.service_urls.get(service, "")
    
    def is_service_available(self, service: MaximusService, timeout: int = 5) -> bool:
        """
        Quick availability check
        
        Args:
            service: Service to check
            timeout: Request timeout
        
        Returns:
            True if service responds, False otherwise
        """
        response = self.health_check(service, timeout=timeout)
        return response.success


# Singleton instance
_client_instance: Optional[SharedMaximusClient] = None


def get_shared_client() -> SharedMaximusClient:
    """Get singleton SharedMaximusClient instance"""
    global _client_instance
    if _client_instance is None:
        _client_instance = SharedMaximusClient()
    return _client_instance


# Export public API
__all__ = [
    "SharedMaximusClient",
    "MaximusService",
    "ServiceResponse",
    "get_shared_client"
]
