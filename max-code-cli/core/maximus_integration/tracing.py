"""
OpenTelemetry Tracing Integration for MAXIMUS

Provides distributed tracing for all API calls across MAXIMUS services.
Exports traces to Jaeger (localhost:16686)

Week 9 - Advanced Observability (P2-006)
"""

import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager

try:
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.trace import Status, StatusCode
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    trace = None

logger = logging.getLogger(__name__)


class TracingManager:
    """
    Manages OpenTelemetry tracing for MAXIMUS services.
    
    Features:
    - Automatic span creation for API calls
    - Exception tracking
    - Performance metrics
    - Jaeger export
    
    Example:
        tracing = TracingManager()
        with tracing.span("api_call", {"endpoint": "/health"}):
            response = await client.health()
    """
    
    def __init__(
        self,
        service_name: str = "maximus-client",
        jaeger_host: str = "localhost",
        jaeger_port: int = 6831,
        enabled: bool = True,
    ):
        """
        Initialize tracing manager.
        
        Args:
            service_name: Name of the service (for Jaeger UI)
            jaeger_host: Jaeger agent host
            jaeger_port: Jaeger agent port (UDP)
            enabled: Enable/disable tracing
        """
        self.enabled = enabled and TRACING_AVAILABLE
        self.service_name = service_name
        self._tracer: Optional[Any] = None
        
        if not TRACING_AVAILABLE:
            logger.warning(
                "OpenTelemetry not available. Install with: "
                "pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-jaeger"
            )
            return
        
        if self.enabled:
            self._setup_tracing(jaeger_host, jaeger_port)
    
    def _setup_tracing(self, jaeger_host: str, jaeger_port: int):
        """Setup OpenTelemetry with Jaeger exporter."""
        try:
            # Create resource with service name
            resource = Resource.create({"service.name": self.service_name})
            
            # Create tracer provider
            provider = TracerProvider(resource=resource)
            
            # Create Jaeger exporter
            jaeger_exporter = JaegerExporter(
                agent_host_name=jaeger_host,
                agent_port=jaeger_port,
            )
            
            # Add batch span processor
            provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
            
            # Set as global tracer provider
            trace.set_tracer_provider(provider)
            
            # Get tracer
            self._tracer = trace.get_tracer(__name__)
            
            logger.info(
                f"Tracing initialized: {self.service_name} -> {jaeger_host}:{jaeger_port}"
            )
        
        except Exception as e:
            logger.warning(f"Failed to initialize tracing: {e}")
            self.enabled = False
    
    @contextmanager
    def span(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
        kind: Optional[Any] = None,
    ):
        """
        Create a tracing span.
        
        Args:
            name: Span name (e.g., "api_call", "database_query")
            attributes: Span attributes (metadata)
            kind: Span kind (CLIENT, SERVER, etc.)
        
        Yields:
            Span object (if tracing enabled)
        
        Example:
            with tracing.span("fetch_user", {"user_id": 123}):
                user = await db.fetch_user(123)
        """
        if not self.enabled or not self._tracer:
            yield None
            return
        
        try:
            with self._tracer.start_as_current_span(
                name,
                kind=kind or trace.SpanKind.CLIENT,
            ) as span:
                # Add attributes
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, str(value))
                
                try:
                    yield span
                    
                    # Mark as successful
                    span.set_status(Status(StatusCode.OK))
                
                except Exception as e:
                    # Record exception
                    span.record_exception(e)
                    span.set_status(
                        Status(StatusCode.ERROR, description=str(e))
                    )
                    raise
        
        except Exception as e:
            logger.debug(f"Tracing span failed: {e}")
            yield None
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Add event to current span.
        
        Args:
            name: Event name
            attributes: Event attributes
        """
        if not self.enabled:
            return
        
        try:
            span = trace.get_current_span()
            if span and span.is_recording():
                span.add_event(name, attributes=attributes or {})
        except Exception as e:
            logger.debug(f"Failed to add event: {e}")
    
    def set_attribute(self, key: str, value: Any):
        """
        Set attribute on current span.
        
        Args:
            key: Attribute key
            value: Attribute value
        """
        if not self.enabled:
            return
        
        try:
            span = trace.get_current_span()
            if span and span.is_recording():
                span.set_attribute(key, str(value))
        except Exception as e:
            logger.debug(f"Failed to set attribute: {e}")


# Global tracing manager (singleton)
_global_tracing: Optional[TracingManager] = None


def get_tracing(
    service_name: str = "maximus-client",
    jaeger_host: str = "localhost",
    jaeger_port: int = 6831,
) -> TracingManager:
    """
    Get global tracing manager (singleton).
    
    Args:
        service_name: Service name for Jaeger
        jaeger_host: Jaeger host
        jaeger_port: Jaeger port
    
    Returns:
        TracingManager instance
    """
    global _global_tracing
    
    if _global_tracing is None:
        _global_tracing = TracingManager(
            service_name=service_name,
            jaeger_host=jaeger_host,
            jaeger_port=jaeger_port,
        )
    
    return _global_tracing


# Convenience function for creating spans
def trace_span(name: str, **attributes):
    """
    Decorator for tracing function calls.
    
    Example:
        @trace_span("process_data", data_type="user")
        async def process_user_data(data):
            # ... processing logic
            pass
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            tracing = get_tracing()
            with tracing.span(name, attributes):
                return await func(*args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            tracing = get_tracing()
            with tracing.span(name, attributes):
                return func(*args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
