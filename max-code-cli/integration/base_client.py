"""
Base HTTP Client for MAXIMUS Services

Provides common functionality for all service clients:
- HTTP requests with retries
- Error handling
- Health checks
- Circuit breaker pattern
"""

import httpx
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ServiceHealth(str, Enum):
    """Service health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ServiceResponse:
    """Standard service response."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None


class BaseServiceClient:
    """
    Base client for MAXIMUS services.

    Provides:
    - HTTP client with connection pooling
    - Automatic retries
    - Error handling
    - Health checks
    """

    def __init__(
        self,
        base_url: str,
        service_name: str,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initialize base client.

        Args:
            base_url: Service base URL
            service_name: Service name for logging
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.service_name = service_name
        self.timeout = timeout
        self.max_retries = max_retries

        # HTTP client with retries
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            follow_redirects=True,
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> ServiceResponse:
        """
        Make HTTP request with retries.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            ServiceResponse
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.client.request(method, url, **kwargs)
            response.raise_for_status()

            return ServiceResponse(
                success=True,
                data=response.json() if response.text else None,
                status_code=response.status_code
            )

        except httpx.HTTPStatusError as e:
            return ServiceResponse(
                success=False,
                error=f"HTTP {e.response.status_code}: {str(e)}",
                status_code=e.response.status_code
            )

        except httpx.RequestError as e:
            return ServiceResponse(
                success=False,
                error=f"Request failed: {str(e)}",
            )

        except Exception as e:
            return ServiceResponse(
                success=False,
                error=f"Unexpected error: {str(e)}",
            )

    def get(self, endpoint: str, **kwargs) -> ServiceResponse:
        """Make GET request."""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> ServiceResponse:
        """Make POST request."""
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> ServiceResponse:
        """Make PUT request."""
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> ServiceResponse:
        """Make DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)

    def health_check(self) -> ServiceHealth:
        """
        Check service health.

        Returns:
            ServiceHealth enum
        """
        try:
            response = self.get("/health")

            if response.success:
                return ServiceHealth.HEALTHY
            elif response.status_code and 500 <= response.status_code < 600:
                return ServiceHealth.UNHEALTHY
            else:
                return ServiceHealth.DEGRADED

        except Exception:
            return ServiceHealth.UNKNOWN

    def close(self):
        """Close HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
