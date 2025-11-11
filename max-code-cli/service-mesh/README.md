# Service Mesh (Istio) for MAXIMUS

Production-grade service mesh with traffic management, security, and observability.

## Features

### 1. Traffic Management
- Load balancing (LEAST_REQUEST)
- Circuit breaker (5 errors → 30s ejection)
- Canary deployments (10% v2 traffic)
- Connection pooling (200 max connections)

### 2. Security
- mTLS (STRICT mode - all traffic encrypted)
- Authorization policies (RBAC)
- Peer authentication
- TLS certificates managed by Istio

### 3. Observability
- Distributed tracing (Jaeger)
- Service mesh metrics (Prometheus)
- Service graph (Kiali)
- Grafana dashboards

## Installation

### 1. Install Istio
```bash
cd service-mesh
./install_istio.sh
```

### 2. Deploy MAXIMUS Services
```bash
kubectl apply -f manifests/maximus-mesh.yaml
kubectl apply -f manifests/gateway.yaml
kubectl apply -f manifests/traffic-management.yaml
kubectl apply -f manifests/security.yaml
kubectl apply -f manifests/observability.yaml
```

### 3. Access Services
```bash
# Get ingress gateway IP
export GATEWAY_IP=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Test
curl http://$GATEWAY_IP/health -H "Host: maximus.local"
```

## Dashboards

### Kiali (Service Mesh Visualization)
```bash
istioctl dashboard kiali
# http://localhost:20001/kiali
```

### Jaeger (Distributed Tracing)
```bash
istioctl dashboard jaeger
# http://localhost:16686
```

### Grafana (Metrics)
```bash
istioctl dashboard grafana
# http://localhost:3000
```

## Canary Deployment

Test v2 with canary header:
```bash
curl http://$GATEWAY_IP/query \
  -H "Host: maximus.local" \
  -H "x-canary: true" \
  -d '{"query": "test"}'
```

## Production Checklist

- [ ] Enable mTLS (STRICT mode)
- [ ] Configure authorization policies
- [ ] Set up distributed tracing
- [ ] Configure circuit breakers
- [ ] Test canary deployments
- [ ] Monitor service mesh metrics
- [ ] Set up alerts for circuit breaker trips
