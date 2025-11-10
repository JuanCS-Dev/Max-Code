# MAXIMUS - Local Development Setup

**Gerado:** 2025-11-07 20:46:00

---

## Prerequisites

### System Requirements
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
  - Used by: core
- Redis 7+
  - Used by: core,dlq_monitor,eureka,maba,nis,oraculo,orchestrator,penelope
- Neo4j 5+ (for MABA)
- Kafka (for async messaging)

### Development Tools
- Git
- Python virtual environment (venv)
- Docker Desktop
- Make (optional)

---

## Setup Steps

### 1. Clone Repository
```bash
git clone <repository-url>
cd "MAXIMUS AI"
```

### 2. Install Python Dependencies

For each service individually:
```bash
cd services/<service-name>
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Or use the root requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

For each service:
```bash
cd services/<service-name>
cp .env.example .env
# Edit .env with your configuration
```

Key variables to set:
- Database URLs
- API Keys
- Service endpoints
- Feature flags

### 4. Start Infrastructure with Docker

```bash
docker-compose up -d postgres redis kafka neo4j prometheus grafana
```

Verify services are running:
```bash
docker-compose ps
```

### 5. Run Database Migrations

For services with migrations:
```bash
cd services/<service-name>
python migrate.py
# or
alembic upgrade head
```

### 6. Start Services

**Option 1: All services via Docker Compose**
```bash
docker-compose up -d
```

**Option 2: Individual service for development**
```bash
cd services/<service-name>
python main.py
# or
uvicorn main:app --reload --port 8150
```

### 7. Verify Service Health

Check all services:
```bash
# Core
curl http://localhost:8150/health

# Eureka
curl http://localhost:8151/health

# Oraculo
curl http://localhost:8152/health

# Penelope
curl http://localhost:8153/health

# MABA
curl http://localhost:8154/health

# NIS
curl http://localhost:8155/health

# Orchestrator
curl http://localhost:8156/health

# DLQ Monitor
curl http://localhost:8157/health
```

---

## Common Development Tasks

### Running Tests
```bash
cd services/<service-name>
pytest tests/
```

### Linting
```bash
cd services/<service-name>
pylint src/
# or
ruff check .
```

### Format Code
```bash
cd services/<service-name>
black .
isort .
```

### View Logs
```bash
# Docker logs
docker-compose logs -f <service-name>

# Application logs
tail -f logs/<service-name>.log
```

### Database Access
```bash
# PostgreSQL
docker exec -it maximus-postgres psql -U postgres -d maximus

# Redis
docker exec -it maximus-redis redis-cli

# Neo4j Browser
open http://localhost:7474
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8150
# Kill process
kill -9 <PID>
```

### Database Connection Issues
```bash
# Check if database is running
docker ps | grep postgres

# Restart database
docker-compose restart postgres
```

### Service Won't Start
```bash
# Check logs
docker-compose logs <service-name>

# Rebuild image
docker-compose build <service-name>
docker-compose up -d <service-name>
```

---

## Project Structure

```
MAXIMUS AI/
├── services/           # 8 microservices
│   ├── core/
│   ├── eureka/
│   ├── oraculo/
│   ├── penelope/
│   ├── maba/
│   ├── nis/
│   ├── orchestrator/
│   └── dlq_monitor/
├── libs/              # Shared libraries
├── cli/               # max-code-cli
├── infrastructure/    # Terraform, K8s configs
├── docs/              # Documentation
└── tests/             # Integration tests
```

---

**Next Steps:**
- Read [API Reference](../../api-reference/services/)
- Review [Testing Guide](../testing/TESTING_GUIDE.md)
- Check [Architecture Docs](../../architecture/)

