"""
Simple Service Clients - MABA, NIS, Eureka, DLQ Monitor

Minimalist clients for remaining MAXIMUS services.
All follow same pattern: health + metrics + basic operations.
"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

from integration.base_client import BaseHTTPClient

logger = logging.getLogger(__name__)


if HTTPX_AVAILABLE:
    # ========================================================================
    # MABA Client (port 8152) - Browser Agent
    # ========================================================================
    class MABAClient(BaseHTTPClient):
        """MABA (Browser Agent) Client - port 8152."""

        def __init__(self, base_url: str = "http://localhost:8152", **kwargs):
            super().__init__(base_url=base_url, **kwargs)

        def health(self) -> Dict[str, Any]:
            """Health check."""
            return self.get("/health").json()

        def metrics(self) -> str:
            """Get Prometheus metrics."""
            return self.get("/metrics").text


    # ========================================================================
    # NIS Client (port 8153) - Narrative Intelligence
    # ========================================================================
    class NISClient(BaseHTTPClient):
        """NIS (Narrative Intelligence) Client - port 8153."""

        def __init__(self, base_url: str = "http://localhost:8153", **kwargs):
            super().__init__(base_url=base_url, **kwargs)

        def health(self) -> Dict[str, Any]:
            """Health check."""
            return self.get("/health").json()

        def metrics(self) -> str:
            """Get Prometheus metrics."""
            return self.get("/metrics").text


    # ========================================================================
    # Eureka Client (port 8155) - Insights & Discovery
    # ========================================================================
    class InsightRequest(BaseModel):
        """Request for insight generation."""
        data: Dict[str, Any]
        data_type: str
        context: Optional[Dict[str, Any]] = None


    class EurekaClient(BaseHTTPClient):
        """Eureka (Insights) Client - port 8155."""

        def __init__(self, base_url: str = "http://localhost:8155", **kwargs):
            super().__init__(base_url=base_url, **kwargs)

        def health(self) -> Dict[str, Any]:
            """Health check."""
            return self.get("/health").json()

        def generate_insight(
            self,
            data: Dict[str, Any],
            data_type: str,
            context: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Any]:
            """Generate insights from data."""
            request = InsightRequest(data=data, data_type=data_type, context=context)
            return self.post("/generate_insight", json=request.model_dump()).json()

        def detect_pattern(self, data: Dict[str, Any], pattern_definition: Dict[str, Any]) -> Dict[str, Any]:
            """Detect patterns in data."""
            payload = {"data": data, "pattern_definition": pattern_definition}
            return self.post("/detect_pattern", json=payload).json()

        def extract_iocs(self, text: str) -> Dict[str, Any]:
            """Extract Indicators of Compromise."""
            return self.post("/extract_iocs", json={"text": text}).json()


    # ========================================================================
    # DLQ Monitor Client (port 8157) - Dead Letter Queue
    # ========================================================================
    class DLQMonitorClient(BaseHTTPClient):
        """DLQ Monitor Client - port 8157."""

        def __init__(self, base_url: str = "http://localhost:8157", **kwargs):
            super().__init__(base_url=base_url, **kwargs)

        def health(self) -> Dict[str, Any]:
            """Health check."""
            return self.get("/health").json()

else:
    # Fallback classes when httpx not available
    class MABAClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required")

    class NISClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required")

    class EurekaClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required")

    class DLQMonitorClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required")
