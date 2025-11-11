# Distributed Tracing (Jaeger)

Production-grade distributed tracing for MAXIMUS services.

## Start Jaeger

```bash
cd enterprise/tracing
docker-compose up -d
```

## Instrument Services

```python
from enterprise.tracing.instrumentation import setup_tracing

@app.on_event("startup")
async def startup():
    setup_tracing(service_name="maximus-core")
```

## Access Jaeger UI

http://localhost:16686

## Dependencies

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-httpx opentelemetry-exporter-jaeger
```
