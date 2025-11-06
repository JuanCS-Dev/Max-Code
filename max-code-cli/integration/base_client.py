"""Base HTTP Client - Circuit Breaker + Retry"""

import logging
import time
from typing import Optional
from enum import Enum

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if HTTPX_AVAILABLE:
    class CircuitState(str, Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"

    class CircuitBreaker:
        def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
            self.failure_threshold = failure_threshold
            self.recovery_timeout = recovery_timeout
            self._failure_count = 0
            self._last_failure_time: Optional[float] = None
            self._state = CircuitState.CLOSED

        @property
        def state(self) -> CircuitState:
            if (self._state == CircuitState.OPEN and self._last_failure_time and
                time.time() - self._last_failure_time >= self.recovery_timeout):
                self._state = CircuitState.HALF_OPEN
            return self._state

        def call(self, func, *args, **kwargs):
            if self.state == CircuitState.OPEN:
                raise Exception("Circuit breaker OPEN")
            try:
                result = func(*args, **kwargs)
                if self._state == CircuitState.HALF_OPEN:
                    logger.info("Circuit → CLOSED")
                self._failure_count = 0
                self._state = CircuitState.CLOSED
                return result
            except Exception as e:
                self._failure_count += 1
                self._last_failure_time = time.time()
                if self._failure_count >= self.failure_threshold:
                    self._state = CircuitState.OPEN
                    logger.warning(f"Circuit → OPEN ({self._failure_count} failures)")
                raise

    class BaseHTTPClient:
        def __init__(self, base_url: str, timeout: float = 30.0, max_retries: int = 3):
            self.base_url = base_url.rstrip('/')
            self.client = httpx.Client(
                base_url=self.base_url,
                timeout=httpx.Timeout(connect=5.0, read=timeout, write=timeout, pool=5.0),
                follow_redirects=True
            )
            self.circuit_breaker = CircuitBreaker()
            self.max_retries = max_retries

        def _request_with_retry(self, method: str, endpoint: str, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    logger.debug(f"{method} {endpoint} (attempt {attempt + 1}/{self.max_retries})")
                    response = self.client.request(method, endpoint, **kwargs)
                    response.raise_for_status()
                    logger.debug(f"{method} {endpoint} - Success ({response.status_code})")
                    return response
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        backoff = 2 ** attempt
                        logger.warning(f"{method} {endpoint} failed (attempt {attempt + 1}): {e}. Retrying in {backoff}s...")
                        time.sleep(backoff)
                    else:
                        logger.error(f"{method} {endpoint} failed after {self.max_retries} attempts: {e}")
                        raise

        def get(self, endpoint: str, **kwargs):
            return self.circuit_breaker.call(self._request_with_retry, "GET", endpoint, **kwargs)

        def post(self, endpoint: str, **kwargs):
            return self.circuit_breaker.call(self._request_with_retry, "POST", endpoint, **kwargs)

        def close(self):
            self.client.close()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()
else:
    class BaseHTTPClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required")
