# API Gateway (Kong) for MAXIMUS

Production-grade API Gateway with rate limiting, authentication, and observability.

## Features

### 1. Traffic Management
- Rate limiting (100 req/min per IP)
- Load balancing across services
- Request/response transformation

### 2. Security
- API key authentication
- CORS configuration
- TLS termination

### 3. Observability
- Request logging
- Prometheus metrics
- Admin API for monitoring

## Quick Start

### 1. Start Kong
```bash
cd api-gateway
docker-compose up -d
```

### 2. Configure Routes
```bash
# Wait for Kong to be ready (30 seconds)
sleep 30

# Apply configuration
./configure_kong.sh
```

### 3. Test Gateway
```bash
# Without API key (should fail)
curl http://localhost:8000/api/consciousness/state

# With API key (should work)
curl http://localhost:8000/api/consciousness/state \
  -H "X-API-Key: maximus_production_key_2024"
```

## Access Dashboards

- **Kong Admin API**: http://localhost:8001
- **Konga UI**: http://localhost:1337
- **Prometheus Metrics**: http://localhost:8000/metrics

## Kong Admin API Examples

### List Services
```bash
curl http://localhost:8001/services
```

### List Routes
```bash
curl http://localhost:8001/routes
```

### List Plugins
```bash
curl http://localhost:8001/plugins
```

### View Metrics
```bash
curl http://localhost:8000/metrics
```

## Rate Limiting

Default: 100 requests/minute per IP

To change:
```bash
curl -X PATCH http://localhost:8001/services/maximus-core/plugins/{plugin_id} \
  --data config.minute=200
```

## API Key Management

### Create New Consumer
```bash
curl -X POST http://localhost:8001/consumers \
  --data username=new-client

curl -X POST http://localhost:8001/consumers/new-client/key-auth \
  --data key=new_api_key_12345
```

### Revoke API Key
```bash
curl -X DELETE http://localhost:8001/consumers/maximus-cli/key-auth/{key_id}
```

## Production Checklist

- [ ] Enable HTTPS (TLS termination)
- [ ] Configure rate limiting per consumer
- [ ] Set up API key rotation
- [ ] Enable request logging to ELK/Loki
- [ ] Configure circuit breaker plugin
- [ ] Set up monitoring alerts
- [ ] Test failover scenarios
