"""
Lightweight metrics middleware for MAXIMUS services.
Compatible with Prometheus scraping.
"""

from fastapi import Request, Response
from time import time
import structlog

logger = structlog.get_logger(__name__)


class MetricsCollector:
    """Collect basic metrics for Prometheus."""

    def __init__(self):
        self.request_count = 0
        self.request_duration_sum = 0.0
        self.error_count = 0

    def record_request(self, duration: float, status_code: int):
        """Record request metrics."""
        self.request_count += 1
        self.request_duration_sum += duration
        if status_code >= 400:
            self.error_count += 1

    def format_metrics(self) -> str:
        """Format metrics in Prometheus format."""
        avg_duration = (
            self.request_duration_sum / self.request_count
            if self.request_count > 0
            else 0
        )

        return f"""# HELP maximus_requests_total Total requests
# TYPE maximus_requests_total counter
maximus_requests_total {self.request_count}

# HELP maximus_errors_total Total errors (4xx/5xx)
# TYPE maximus_errors_total counter
maximus_errors_total {self.error_count}

# HELP maximus_request_duration_seconds Average request duration
# TYPE maximus_request_duration_seconds gauge
maximus_request_duration_seconds {avg_duration:.4f}
"""


# Global metrics collector
_metrics = MetricsCollector()


async def metrics_middleware(request: Request, call_next):
    """Middleware to collect request metrics."""
    start_time = time()

    try:
        response: Response = await call_next(request)
        duration = time() - start_time

        # Record metrics
        _metrics.record_request(duration, response.status_code)

        # Log to structured logger
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )

        return response

    except Exception as e:
        duration = time() - start_time
        _metrics.record_request(duration, 500)

        logger.error(
            "http_request_error",
            method=request.method,
            path=request.url.path,
            error=str(e),
            duration_ms=round(duration * 1000, 2),
        )
        raise


def get_metrics() -> str:
    """Get metrics in Prometheus format."""
    return _metrics.format_metrics()
