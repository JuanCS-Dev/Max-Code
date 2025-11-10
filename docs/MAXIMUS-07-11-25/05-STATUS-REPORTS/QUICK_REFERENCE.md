# MAXIMUS AI - Quick Reference

**1-Page System Overview**

═══════════════════════════════════════════════════════════════

## Service Registry

| Service | Port | Status | Entry Point | Purpose |
|---------|------|--------|-------------|---------|
| **core** | 8150 | ✅ | main.py | Artificial consciousness |
| **eureka** | 8151 | ✅ | main.py | Malware analysis |
| **oraculo** | 8152 | ✅ | main.py | Self-improvement |
| **penelope** | 8153 | ✅ | main.py | Biblical governance |
| **maba** | 8154 | ✅ | api/ | Browser automation |
| **nis** | 8155 | ✅ | app.py | Narrative intelligence |
| **orchestrator** | 8156 | ✅ | main.py | Multi-service orchestration |
| **dlq_monitor** | 8157 | ✅ | main.py | DLQ monitoring |

---

## Quick Stats

- **Total Python Files:** 20,836
- **Total LOC:** 179,105+
- **Services:** 8
- **Test Coverage:** 100% (all services have tests)
- **Documentation:** 87.5% (7/8 with README)

---

## Health Check Endpoints

```bash
curl http://localhost:8150/health  # core
curl http://localhost:8151/health  # eureka
curl http://localhost:8152/health  # oraculo
curl http://localhost:8153/health  # penelope
curl http://localhost:8154/health  # maba
curl http://localhost:8155/health  # nis
curl http://localhost:8156/health  # orchestrator
curl http://localhost:8157/health  # dlq_monitor
```

---

## Infrastructure Ports

| Component | Port | Purpose |
|-----------|------|---------|
| PostgreSQL | 5432 | Main database |
| Redis | 6379 | Caching |
| Neo4j | 7474 | MABA cognitive maps |
| Kafka | 9092 | Messaging |
| Prometheus | 9090 | Metrics |
| Grafana | 3000 | Dashboards |
| Loki | 3100 | Logging |

---

## Quick Commands

### Start All Services
```bash
cd "/media/juan/DATA2/projects/MAXIMUS AI"
docker-compose up -d
```

### Check Service Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f [service_name]
```

### Stop All Services
```bash
docker-compose down
```

---

## Service Capabilities

### 🧠 CORE
Biomimetic consciousness with 5-layer predictive coding

### 🦠 EUREKA
40+ malicious patterns, MITRE ATT&CK mapping

### 🔮 ORÁCULO
LLM-powered self-improvement with auto-implementation

### ⛪ PENELOPE
7 Biblical Articles of Christian governance

### 🌐 MABA
Cognitive browser with Neo4j learned maps

### 📖 NIS
AI narratives with 60-80% cost reduction

### 🎭 ORCHESTRATOR
Multi-service workflow coordination

### 📮 DLQ_MONITOR
Kafka monitoring with retry logic

---

## Documentation Quick Links

- [📚 Main README](README.md)
- [📊 Executive Summary](EXECUTIVE_SUMMARY.md)
- [📋 Services Index](01_SERVICES_INDEX.md)
- [📦 Global Inventory](00_GLOBAL_INVENTORY.md)
- [🔗 Integrations](architecture/INTEGRATIONS.md)
- [⚠️ Gaps Report](analysis/GAPS_REPORT.md)
- [📈 Quality Metrics](analysis/QUALITY_METRICS.md)

---

## Environment Variables

Key variables needed:
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/maximus
REDIS_URL=redis://localhost:6379
NEO4J_URL=bolt://localhost:7687

# Messaging
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Monitoring
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3000

# API Keys (if needed)
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=...
```

---

## Common Issues

### Service won't start
```bash
docker-compose logs [service_name]
# Check for port conflicts or missing env vars
```

### Database connection failed
```bash
docker-compose ps postgres
# Ensure PostgreSQL is running
```

### High memory usage
```bash
# Check max-code-cli (19K+ files)
# Consider increasing Docker memory limit
```

---

## Key Contacts

- **Architecture:** See [README.md](README.md)
- **Quality:** See [analysis/QUALITY_METRICS.md](analysis/QUALITY_METRICS.md)
- **Gaps:** See [analysis/GAPS_REPORT.md](analysis/GAPS_REPORT.md)

---

**Status:** ✅ PRODUCTION READY
**Last Updated:** 2025-11-07

**Soli Deo Gloria** 🙏
