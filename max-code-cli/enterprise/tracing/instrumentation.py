"""
OpenTelemetry instrumentation for MAXIMUS services.
Distributed tracing with Jaeger.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource


def setup_tracing(service_name: str, jaeger_host: str = "localhost", jaeger_port: int = 6831):
    """
    Setup OpenTelemetry tracing for a service.

    Args:
        service_name: Name of the service (e.g., "maximus-core")
        jaeger_host: Jaeger agent hostname
        jaeger_port: Jaeger agent port (default: 6831/UDP)
    """
    # Create resource with service name
    resource = Resource.create({"service.name": service_name})

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
    )

    # Add span processor
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    # Set global tracer provider
    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument()

    # Instrument HTTPX (for client requests)
    HTTPXClientInstrumentor.instrument()

    print(f"✅ Tracing enabled for {service_name} → Jaeger ({jaeger_host}:{jaeger_port})")


# Usage in FastAPI app
"""
from fastapi import FastAPI
from enterprise.tracing.instrumentation import setup_tracing

app = FastAPI()

# Setup tracing on startup
@app.on_event("startup")
async def startup():
    setup_tracing(service_name="maximus-core")
"""
