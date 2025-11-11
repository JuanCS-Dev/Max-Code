# Connection Pool Tuning

## Current Settings (BaseMaximusClient)

```python
httpx.Limits(
    max_connections=200,        # Total connections
    max_keepalive_connections=50,  # Persistent connections
)
```

## Tuning Guidelines

### Low Traffic (<100 req/s)
```python
max_connections=100
max_keepalive_connections=20
```

### Medium Traffic (100-1000 req/s)
```python
max_connections=200  # Current
max_keepalive_connections=50  # Current
```

### High Traffic (>1000 req/s)
```python
max_connections=500
max_keepalive_connections=100
keepalive_expiry=60.0  # Keep connections alive longer
```

## Backend Tuning (Uvicorn)

### Worker Processes
```bash
# Formula: workers = (2 x CPU cores) + 1
uvicorn app:app --workers 8 --host 0.0.0.0 --port 8100
```

### Worker Class
```bash
# Use uvloop for better performance
pip install uvloop
uvicorn app:app --workers 8 --loop uvloop
```

## PostgreSQL Connection Pooling

```python
asyncpg.create_pool(
    min_size=10,   # Minimum connections
    max_size=100,  # Maximum connections
    command_timeout=10.0,  # Query timeout
)
```

## Redis Connection Pooling

```python
aioredis.from_url(
    max_connections=50,  # Connection pool size
)
```

## Monitoring

Track these metrics:
- Connection pool utilization
- Connection wait time
- Request queue depth
- Worker process CPU/memory

## Load Testing

```bash
# Apache Bench
ab -n 10000 -c 100 http://localhost:8100/health

# Locust
pip install locust
locust -f load_test.py --host=http://localhost:8100
```
