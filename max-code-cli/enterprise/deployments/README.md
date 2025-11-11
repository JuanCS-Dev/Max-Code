# Service Deployments

Complete deployment manifests for all 8 MAXIMUS services.

## Services

1. **MAXIMUS Core** (8100) - 3 replicas
2. **PENELOPE** (8154) - 2 replicas
3. **MABA** (8152) - 2 replicas
4. **NIS** (8153) - 2 replicas
5. **TIG Fabric** (8150) - 1 replica
6. **Reactive Orchestrator** (8151) - 2 replicas
7. **Safety Monitor** (8155) - 2 replicas
8. **HITL Dashboard** (8156) - 2 replicas

## Deploy All

```bash
kubectl apply -f enterprise/deployments/all-services.yaml
```

## Check Status

```bash
kubectl get pods -n maximus
kubectl get services -n maximus
```

## Scale Service

```bash
kubectl scale deployment maximus-core --replicas=5 -n maximus
```
