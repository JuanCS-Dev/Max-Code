# Auto-Scaling (Kubernetes HPA)

Horizontal Pod Autoscaler for dynamic resource allocation.

## Features

- **CPU-based**: Scale at 70% CPU utilization
- **Memory-based**: Scale at 80% memory utilization
- **Smart policies**:
  - Scale up: 50% increase or +2 pods (max)
  - Scale down: 10% decrease (gradual)
  - Stabilization: 5min before scale-down

## Deploy

```bash
kubectl apply -f enterprise/autoscaling/hpa.yaml
```

## Monitor

```bash
kubectl get hpa -n maximus -w
```

## Test Auto-Scaling

```bash
# Generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://maximus-core:8100/query; done"
```
