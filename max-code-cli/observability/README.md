# MAXIMUS Observability Stack

Production-ready observability with Prometheus + Grafana.

## Quick Start

### 1. Start Observability Stack
```bash
cd /media/juan/DATA2/projects/MAXIMUS\ AI/max-code-cli/observability
docker-compose up -d
```

### 2. Add Metrics to FastAPI Services

```python
from fastapi import FastAPI
from observability.metrics_middleware import metrics_middleware, get_metrics

app = FastAPI()

# Add metrics middleware
app.middleware("http")(metrics_middleware)

# Add /metrics endpoint
@app.get("/metrics")
async def metrics():
    from observability.metrics_middleware import get_metrics
    return Response(content=get_metrics(), media_type="text/plain")
```

### 3. Access Services

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `maximus2024`

## Metrics Collected

- `maximus_requests_total`: Total HTTP requests
- `maximus_errors_total`: Total errors (4xx/5xx)
- `maximus_request_duration_seconds`: Average request duration

## Next Steps

1. Configure Grafana dashboards
2. Add custom metrics (arousal, TIG, etc.)
3. Set up alerting rules
4. Export dashboards to JSON

## Production Considerations

- Use persistent volumes for data
- Configure retention policies
- Add authentication to Prometheus
- Set up remote write for long-term storage
