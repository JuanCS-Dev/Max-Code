# 🚀 04-DEPLOYMENT - Deployment & Operations

**Deploy and operate MAXIMUS AI in production environments.**

---

## 📂 Directory Structure

```
04-DEPLOYMENT/
├── docker/           # Docker and Docker Compose
├── kubernetes/       # Kubernetes manifests
├── config/           # Configuration management
└── infrastructure/   # IaC and provisioning
```

---

## 🐳 Docker Deployment

### [Docker Compose Guide](docker/DOCKER_COMPOSE_GUIDE.md)
**Deploy all services with Docker Compose**

**Includes:**
- Service configurations
- Port mappings
- Environment variables
- Volume mounts
- Network setup

**Quick Start:**
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

**Services & Ports:**
| Service | Port | Description |
|---------|------|-------------|
| core | 8150 | Central orchestration |
| eureka | 8151 | Code analysis |
| oraculo | 8152 | Risk assessment |
| penelope | 8153 | Self-healing |
| maba | 8154 | Knowledge graphs |
| nis | 8155 | Network security |
| orchestrator | 8156 | Workflows |
| dlq_monitor | 8157 | DLQ monitoring |
| postgres | 5432 | Database |
| redis | 6379 | Cache/queues |
| kafka | 9092 | Message broker |
| neo4j | 7474/7687 | Graph database |

---

## ☸️ Kubernetes Deployment

### Manifests
- Service deployments
- ConfigMaps and Secrets
- Ingress configuration
- Persistent volumes
- HorizontalPodAutoscalers

### Quick Deploy
```bash
# Apply all manifests
kubectl apply -f kubernetes/

# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services
```

---

## ⚙️ Configuration

### Environment Variables

**Global Configuration:**
```bash
# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/maximus
REDIS_URL=redis://redis:6379

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Monitoring
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000
```

**Service-Specific:**
Each service has additional configuration in `.env.example` files.

### Secrets Management
- Use Docker secrets for sensitive data
- Kubernetes secrets for K8s deployments
- Environment variable injection
- Vault integration (optional)

---

## 📊 Monitoring & Observability

### Prometheus
- Metrics collection
- Service health monitoring
- Alert rules
- **Port:** 9090

### Grafana
- Dashboards
- Visualization
- Alerting
- **Port:** 3000

### Health Checks
All services expose `/health` endpoint:
```bash
curl http://localhost:8150/health
# {"status": "healthy", "service": "maximus_core"}
```

---

## 🔄 Scaling

### Docker Compose
```bash
# Scale specific service
docker-compose up -d --scale eureka=3
```

### Kubernetes
```yaml
# Edit HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: eureka
spec:
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

---

## 🛠️ Maintenance Operations

### Database Backups
```bash
# PostgreSQL backup
docker exec maximus-postgres pg_dump -U postgres maximus > backup.sql

# Restore
docker exec -i maximus-postgres psql -U postgres maximus < backup.sql
```

### Rolling Updates
```bash
# Docker Compose
docker-compose up -d --no-deps --build <service>

# Kubernetes
kubectl rollout restart deployment/<service>
kubectl rollout status deployment/<service>
```

### Logs Management
```bash
# Docker logs
docker-compose logs -f --tail=100 <service>

# Kubernetes logs
kubectl logs -f deployment/<service>
kubectl logs -f <pod-name> --previous  # Previous container
```

---

## 🚨 Troubleshooting

### Service Won't Start
1. Check logs: `docker-compose logs <service>`
2. Verify environment variables
3. Check database connectivity
4. Verify port availability

### Database Connection Issues
1. Check database is running: `docker ps | grep postgres`
2. Verify connection string
3. Check network connectivity
4. Review database logs

### Performance Issues
1. Check resource usage: `docker stats`
2. Review Prometheus metrics
3. Check database query performance
4. Scale services if needed

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Secrets properly set
- [ ] Database migrations ready
- [ ] Monitoring configured

### Deployment
- [ ] Infrastructure provisioned
- [ ] Services deployed
- [ ] Health checks passing
- [ ] Monitoring active
- [ ] Logs accessible

### Post-Deployment
- [ ] Smoke tests passed
- [ ] Monitoring alerts configured
- [ ] Backup scheduled
- [ ] Documentation updated
- [ ] Team notified

---

## 🔐 Security

### Best Practices
- Use secrets management
- Enable SSL/TLS
- Network policies (K8s)
- Regular security updates
- Access control (RBAC)

### Hardening
- Minimal container images
- Non-root users
- Read-only filesystems
- Resource limits
- Security scanning

---

## 📚 Infrastructure as Code

### Terraform
- Cloud resource provisioning
- VPC and networking
- Database clusters
- Kubernetes clusters

### Ansible
- Server configuration
- Application deployment
- Secret management
- Configuration updates

---

**[← Back to Main](../README.md)** | **[Next: Status Reports →](../05-STATUS-REPORTS/)**
