"""
Base client for all MAXIMUS ecosystem services.

This module provides shared functionality for all service clients:
- HTTP request handling with retries
- Connection pooling
- Error handling
- Logging

Following Anthropic SDK patterns.
"""

import os
import asyncio
import time
import logging
from typing import Any, Dict, Optional, Union, Tuple
from abc import ABC

import httpx
from pydantic import BaseModel
import structlog

# Configure structlog for production-quality logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)


class BaseMaximusError(Exception):
    """Base exception for all MAXIMUS client errors"""
    pass


class BaseMaximusConnectionError(BaseMaximusError):
    """Raised when unable to connect to service"""
    pass


class BaseMaximusAPIError(BaseMaximusError):
    """Raised when API returns an error response"""

    def __init__(self, message: str, status_code: int, response: Dict[str, Any]):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class BaseMaximusTimeoutError(BaseMaximusError):
    """Raised when request times out"""
    pass


class BaseMaximusClient(ABC):
    """
    Base class for all MAXIMUS service clients.

    Provides shared HTTP request handling with:
    - Connection pooling
    - Automatic retries
    - Error handling
    - Type-safe responses

    Following Anthropic SDK patterns.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        verify: Union[str, bool] = True,
        cert: Optional[Tuple[str, str]] = None,
    ):
        """
        Initialize base client.

        Args:
            base_url: Service base URL (e.g., http://localhost:8100 or https://localhost:8100)
            timeout: Request timeout in seconds (default: 30.0)
            max_retries: Number of retry attempts (default: 3)
            api_key: Optional API key for authentication
            jwt_token: Optional JWT token for authentication
            verify: TLS certificate verification:
                - True: Verify with system CA bundle (default)
                - False: Skip verification (insecure, dev only)
                - str: Path to CA cert file (e.g., "certs/ca-cert.pem")
            cert: Client certificate for mTLS (cert_file, key_file)
        """
        self.base_url = base_url or self._get_default_base_url()
        self.timeout = timeout or 30.0
        self.max_retries = max_retries
        self.api_key = api_key or os.getenv(self._get_api_key_env_var())
        self.jwt_token = jwt_token or os.getenv("JWT_TOKEN")
        self.verify = verify
        self.cert = cert

        # Structured logger
        self.logger = structlog.get_logger(self.__class__.__name__)

        # Log authentication method
        if self.jwt_token:
            self.logger.info("auth_method", method="jwt")
        elif self.api_key:
            self.logger.info("auth_method", method="api_key")
        else:
            self.logger.warning("auth_method", method="none")

        # Log TLS configuration
        if self.base_url.startswith("https://"):
            if isinstance(verify, str):
                self.logger.info("tls_enabled", verify_mode="custom_ca", ca_file=verify)
            elif verify:
                self.logger.info("tls_enabled", verify_mode="system_ca")
            else:
                self.logger.warning("tls_enabled", verify_mode="disabled", security="INSECURE")

            if cert:
                self.logger.info("mtls_enabled", client_cert=cert[0])

        # HTTP client with connection pooling and TLS
        self._http_client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(
                max_connections=200,  # Increased from 100
                max_keepalive_connections=50,  # Increased from 20
            ),
            verify=verify,  # TLS verification
            cert=cert,      # mTLS client certificate
        )

    def _get_default_base_url(self) -> str:
        """Get default base URL for this service. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement _get_default_base_url()")

    def _get_api_key_env_var(self) -> str:
        """Get API key environment variable name. Override in subclasses."""
        return "MAXIMUS_API_KEY"

    def _get_connection_error_class(self):
        """Get connection error class. Override in subclasses."""
        return BaseMaximusConnectionError

    def _get_api_error_class(self):
        """Get API error class. Override in subclasses."""
        return BaseMaximusAPIError

    def _get_timeout_error_class(self):
        """Get timeout error class. Override in subclasses."""
        return BaseMaximusTimeoutError

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Union[Dict[str, Any], Any]:
        """
        Make HTTP request with retry logic and error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments passed to httpx.request()

        Returns:
            Response JSON data

        Raises:
            BaseMaximusConnectionError: Connection failed after retries
            BaseMaximusAPIError: API returned error status
            BaseMaximusTimeoutError: Request timed out
        """
        # Import tracing (lazy to avoid circular import)
        try:
            from .tracing import get_tracing
            tracing = get_tracing(service_name=self.__class__.__name__)
        except Exception:
            tracing = None

        # Start distributed tracing span
        span_attrs = {
            "http.method": method,
            "http.url": f"{self.base_url}{endpoint}",
            "service.name": self.__class__.__name__,
        }

        if tracing:
            span_context = tracing.span("api_request", span_attrs)
            span_context.__enter__()
        else:
            span_context = None

        start_time = time.time()

        # Log request start
        self.logger.info(
            "api_request_start",
            method=method,
            endpoint=endpoint,
            base_url=self.base_url,
            timeout=self.timeout,
        )

        # Add authentication headers
        headers = kwargs.get("headers", {})

        # Priority: JWT > API Key
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key

        kwargs["headers"] = headers

        # Retry logic
        for attempt in range(self.max_retries):
            try:
                response = await self._http_client.request(
                    method=method,
                    url=endpoint,
                    **kwargs
                )

                # Calculate duration
                duration_ms = (time.time() - start_time) * 1000

                # Raise for HTTP errors (4xx, 5xx)
                response.raise_for_status()

                # Log success
                self.logger.info(
                    "api_request_success",
                    method=method,
                    endpoint=endpoint,
                    status_code=response.status_code,
                    duration_ms=round(duration_ms, 2),
                    attempt=attempt + 1,
                )

                # Add tracing attributes
                if tracing:
                    tracing.set_attribute("http.status_code", response.status_code)
                    tracing.set_attribute("http.response_time_ms", round(duration_ms, 2))
                    tracing.set_attribute("retry.attempt", attempt + 1)

                # Close tracing span
                if span_context:
                    span_context.__exit__(None, None, None)

                # Return JSON response
                return response.json()

            except httpx.ConnectError as e:
                duration_ms = (time.time() - start_time) * 1000

                if attempt == self.max_retries - 1:
                    # Log final failure
                    self.logger.error(
                        "api_request_connection_failed",
                        method=method,
                        endpoint=endpoint,
                        attempts=self.max_retries,
                        duration_ms=round(duration_ms, 2),
                        error=str(e),
                    )

                    error_class = self._get_connection_error_class()
                    raise error_class(
                        f"Failed to connect to {self.base_url}{endpoint} after {self.max_retries} attempts"
                    ) from e

                # Log retry
                self.logger.warning(
                    "api_request_retry",
                    method=method,
                    endpoint=endpoint,
                    attempt=attempt + 1,
                    max_retries=self.max_retries,
                    reason="connection_error",
                )

                await asyncio.sleep(0.5 * (attempt + 1))

            except httpx.TimeoutException as e:
                duration_ms = (time.time() - start_time) * 1000

                # Log timeout
                self.logger.error(
                    "api_request_timeout",
                    method=method,
                    endpoint=endpoint,
                    timeout=self.timeout,
                    duration_ms=round(duration_ms, 2),
                    error=str(e),
                )

                # Close span on error
                if span_context:
                    span_context.__exit__(type(e), e, e.__traceback__)

                error_class = self._get_timeout_error_class()
                raise error_class(
                    f"Request to {endpoint} timed out after {self.timeout}s"
                ) from e

            except httpx.HTTPStatusError as e:
                duration_ms = (time.time() - start_time) * 1000

                try:
                    response_data = e.response.json()
                except Exception:
                    response_data = {"detail": e.response.text}

                # Log API error
                self.logger.error(
                    "api_request_http_error",
                    method=method,
                    endpoint=endpoint,
                    status_code=e.response.status_code,
                    duration_ms=round(duration_ms, 2),
                    response=response_data,
                )

                # Close span on error
                if span_context:
                    span_context.__exit__(type(e), e, e.__traceback__)

                error_class = self._get_api_error_class()
                raise error_class(
                    f"API error {e.response.status_code}: {response_data}",
                    status_code=e.response.status_code,
                    response=response_data
                ) from e

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup resources"""
        await self.close()

    async def close(self):
        """Close HTTP client and cleanup resources"""
        await self._http_client.aclose()


class BaseSyncMaximusClient(ABC):
    """
    Synchronous wrapper for BaseMaximusClient.

    Provides sync API for backward compatibility.
    Uses asyncio.run() internally.
    """

    def __init__(self, **kwargs):
        """Initialize with same args as async client"""
        self._async_client_class = self._get_async_client_class()
        self._client = self._async_client_class(**kwargs)

    def _get_async_client_class(self):
        """Get async client class. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement _get_async_client_class()")

    def __enter__(self):
        """Sync context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit"""
        self.close()

    def close(self):
        """Close client"""
        asyncio.run(self._client.close())
