# 🛠️ MAX-CODE-CLI - Development Setup

**Constitutional AI v3.0 - P1: Zero Trust, Maximum Validation**

Este guia configura um ambiente completo de desenvolvimento com TODOS os 8 microsserviços MAXIMUS rodando.

---

## 📋 Pré-requisitos

### Software Obrigatório

- **Docker** 24.0+
- **Docker Compose** 2.20+
- **Python** 3.11+
- **Node.js** 20+ (para microsserviços)
- **Git**

### Verificar Instalação

```bash
docker --version        # Docker version 24.0.0+
docker compose version  # Docker Compose version v2.20.0+
python3 --version       # Python 3.11.0+
node --version          # v20.0.0+
```

---

## 🚀 Quick Start (5 minutos)

### 1. Clone & Install

```bash
# Clone repository
git clone https://github.com/maximus-ai/max-code-cli.git
cd max-code-cli

# Install Python dependencies
pip install -e .
pip install -r requirements-dev.txt
```

### 2. Environment Variables

```bash
# Copy .env template
cp .env.example .env

# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY=sk-ant-...
# - GOOGLE_API_KEY=AIza...
nano .env
```

### 3. Start MAXIMUS Services

```bash
# Start all 8 microsservices
./scripts/start_services.sh

# Wait for services to be healthy (takes ~30s)
./scripts/wait_for_services.sh

# Verify all services running
./scripts/health_check.sh
```

### 4. Run MAX-CODE

```bash
# Start CLI
max-code

# Or run directly
python -m cli.main
```

---

## 🐳 Docker Compose - 8 Microsserviços MAXIMUS

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    MAX-CODE-CLI (Host)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │      Docker Network           │
        │    (maximus-network)          │
        └───────────────┬───────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
┌───▼────┐  ┌──────▼───────┐  ┌─────▼──────┐
│ Core   │  │  Penelope    │  │    MABA    │
│ :8150  │  │   :8154      │  │   :8152    │
└────────┘  └──────────────┘  └────────────┘
    │                   │                   │
┌───▼────┐  ┌──────▼───────┐  ┌─────▼──────┐
│  NIS   │  │   Eureka     │  │   DLQ      │
│ :8153  │  │   :8155      │  │   :8157    │
└────────┘  └──────────────┘  └────────────┘
    │                   │
┌───▼────────┐  ┌──────▼───────┐
│Orchestrator│  │   Oráculo    │
│   :8027    │  │    :8026     │
└────────────┘  └──────────────┘
```

### Services & Ports

| Service | Port | Purpose | Status Endpoint |
|---------|------|---------|----------------|
| **maximus-core** | 8150 | Consciousness & Safety | `/health` |
| **penelope** | 8154 | 7 Fruits Ethics | `/health` |
| **maba** | 8152 | Browser Agent | `/health` |
| **nis** | 8153 | Neural Interface | `/health` |
| **eureka** | 8155 | Discovery | `/health` |
| **dlq** | 8157 | Dead Letter Queue | `/health` |
| **orchestrator** | 8027 | MAPE-K Loop | `/health` |
| **oraculo** | 8026 | Prediction | `/health` |

### docker-compose.yml

```yaml
# MAXIMUS Services - Docker Compose
version: '3.9'

networks:
  maximus-network:
    driver: bridge

services:
  # Service 1: MAXIMUS Core (Consciousness & Safety)
  maximus-core:
    image: maximus-core:latest
    container_name: maximus-core
    ports:
      - "8150:8150"
    environment:
      - NODE_ENV=development
      - PORT=8150
      - ENABLE_CONSCIOUSNESS=true
    networks:
      - maximus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8150/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
    restart: unless-stopped

  # Service 2: PENELOPE (Ethics - 7 Fruits)
  penelope:
    image: maximus-penelope:latest
    container_name: penelope
    ports:
      - "8154:8154"
    environment:
      - NODE_ENV=development
      - PORT=8154
      - ENABLE_7_FRUITS=true
    networks:
      - maximus-network
    depends_on:
      maximus-core:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8154/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Service 3: MABA (Browser Agent)
  maba:
    image: maximus-maba:latest
    container_name: maba
    ports:
      - "8152:8152"
    environment:
      - NODE_ENV=development
      - PORT=8152
    networks:
      - maximus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8152/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Service 4: NIS (Neural Interface System)
  nis:
    image: maximus-nis:latest
    container_name: nis
    ports:
      - "8153:8153"
    environment:
      - NODE_ENV=development
      - PORT=8153
    networks:
      - maximus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8153/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Service 5: Eureka (Discovery Service)
  eureka:
    image: maximus-eureka:latest
    container_name: eureka
    ports:
      - "8155:8155"
    environment:
      - NODE_ENV=development
      - PORT=8155
    networks:
      - maximus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8155/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Service 6: DLQ (Dead Letter Queue)
  dlq:
    image: maximus-dlq:latest
    container_name: dlq
    ports:
      - "8157:8157"
    environment:
      - NODE_ENV=development
      - PORT=8157
    networks:
      - maximus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8157/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Service 7: Orchestrator (MAPE-K Loop)
  orchestrator:
    image: maximus-orchestrator:latest
    container_name: orchestrator
    ports:
      - "8027:8027"
    environment:
      - NODE_ENV=development
      - PORT=8027
    networks:
      - maximus-network
    depends_on:
      maximus-core:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8027/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Service 8: Oráculo (Prediction Service)
  oraculo:
    image: maximus-oraculo:latest
    container_name: oraculo
    ports:
      - "8026:8026"
    environment:
      - NODE_ENV=development
      - PORT=8026
    networks:
      - maximus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8026/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped
```

---

## 📜 Scripts Úteis

### start_services.sh

```bash
#!/bin/bash
# Start all MAXIMUS services

set -e

echo "🚀 Starting MAXIMUS Services..."

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    exit 1
fi

# Start services
docker compose up -d

echo "✅ Services starting..."
echo "📊 Check status: docker compose ps"
echo "📝 View logs: docker compose logs -f"
```

### wait_for_services.sh

```bash
#!/bin/bash
# Wait for all services to be healthy

set -e

services=(
    "http://localhost:8150/health:maximus-core"
    "http://localhost:8154/health:penelope"
    "http://localhost:8152/health:maba"
    "http://localhost:8153/health:nis"
    "http://localhost:8155/health:eureka"
    "http://localhost:8157/health:dlq"
    "http://localhost:8027/health:orchestrator"
    "http://localhost:8026/health:oraculo"
)

echo "⏳ Waiting for services to be healthy..."

for service in "${services[@]}"; do
    IFS=':' read -r url name <<< "$service"

    echo -n "  Waiting for $name..."

    max_attempts=30
    attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo " ✅"
            break
        fi

        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done

    if [ $attempt -eq $max_attempts ]; then
        echo " ❌ TIMEOUT"
        echo "❌ Service $name failed to start"
        exit 1
    fi
done

echo "✅ All services healthy!"
```

### health_check.sh

```bash
#!/bin/bash
# Check health of all services

set -e

services=(
    "8150:MAXIMUS Core"
    "8154:PENELOPE"
    "8152:MABA"
    "8153:NIS"
    "8155:Eureka"
    "8157:DLQ"
    "8027:Orchestrator"
    "8026:Oráculo"
)

echo "🏥 MAXIMUS Services Health Check"
echo "=================================="

for service in "${services[@]}"; do
    IFS=':' read -r port name <<< "$service"

    if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ $name (port $port) - UP"
    else
        echo "❌ $name (port $port) - DOWN"
    fi
done

echo ""
echo "📊 Docker Status:"
docker compose ps
```

### stop_services.sh

```bash
#!/bin/bash
# Stop all MAXIMUS services

set -e

echo "🛑 Stopping MAXIMUS Services..."

docker compose down

echo "✅ Services stopped"
```

---

## 🧪 Running Tests

### Unit Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run with coverage
pytest tests/unit/ --cov=. --cov-report=html
```

### Integration Tests (Require Running Services)

```bash
# Start services first
./scripts/start_services.sh
./scripts/wait_for_services.sh

# Run integration tests
pytest tests/integration/ -v -m integration

# Stop services
./scripts/stop_services.sh
```

### E2E Tests

```bash
# Start services
./scripts/start_services.sh
./scripts/wait_for_services.sh

# Run E2E tests
pytest tests/e2e/ -v -m e2e

# Stop services
./scripts/stop_services.sh
```

### Brutal Test Suites

```bash
# Brutal System Check
python tests/brutal_system_check.py

# Steve Jobs Suite (BULLYING MODE)
python tests/steve_jobs_suite.py
```

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check Docker status
docker compose ps

# View logs
docker compose logs -f

# Restart specific service
docker compose restart maximus-core

# Restart all services
docker compose restart
```

### Port Conflicts

```bash
# Check if ports are in use
lsof -i :8150
lsof -i :8154
# ... etc

# Kill process using port
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Out of Memory

```bash
# Check Docker memory usage
docker stats

# Increase Docker memory limit (Docker Desktop)
# Settings → Resources → Memory → 8GB+

# Prune unused Docker resources
docker system prune -a
```

### Services Crash on Startup

```bash
# View detailed logs
docker compose logs maximus-core --tail=100

# Check health endpoint manually
curl -v http://localhost:8150/health

# Rebuild images
docker compose build --no-cache
docker compose up -d
```

---

## 📦 Building Docker Images

Se você precisa construir as imagens localmente:

```bash
# Build all services
./scripts/build_images.sh

# Or build individually
cd maximus-core
docker build -t maximus-core:latest .

cd ../penelope
docker build -t maximus-penelope:latest .

# ... etc
```

---

## 🌐 Environment Variables

### Required

```bash
# .env file

# Anthropic API Key (Required)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Google API Key (Optional - for Gemini fallback)
GOOGLE_API_KEY=AIza...

# Service URLs (Override if needed)
MAXIMUS_CORE_URL=http://localhost:8150
PENELOPE_URL=http://localhost:8154
MABA_URL=http://localhost:8152
NIS_URL=http://localhost:8153
EUREKA_URL=http://localhost:8155
DLQ_URL=http://localhost:8157
ORCHESTRATOR_URL=http://localhost:8027
ORACULO_URL=http://localhost:8026
```

### Optional

```bash
# Development Mode
DEBUG=true
LOG_LEVEL=debug

# Feature Flags
ENABLE_EXTENDED_THINKING=true
ENABLE_PROMPT_CACHING=true
ENABLE_CONSTITUTIONAL_AI=true

# Testing
RUN_INTEGRATION_TESTS=true
SKIP_SLOW_TESTS=false
```

---

## 📚 Additional Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [API Documentation](./API_REFERENCE.md)
- [Testing Guide](./TESTING.md)
- [Integration Migration Guide](./docs-da-integracao/MIGRATION_GUIDE.md)
- [Constitutional AI v3.0](../CONSTITUIÇÃO_VÉRTICE_v3_0.md)

---

## 🚧 Known Issues

### Week 6 (Current)

1. **Integration Layer Deprecated**: `/integration/*.py` files are deprecated. Use `core/maximus_integration/*_v2.py` instead.
2. **Some Services May Not Exist Yet**: Not all 8 Docker images may be available yet. Check `docker images` for availability.
3. **Health Checks May Timeout**: First startup takes longer (~1 minute) due to image pulls and initialization.

---

## 🎯 Next Steps

After setup complete:

1. ✅ Verify all 8 services running: `./scripts/health_check.sh`
2. ✅ Run unit tests: `pytest tests/unit/ -v`
3. ✅ Run integration tests: `pytest tests/integration/ -v -m integration`
4. ✅ Start MAX-CODE CLI: `max-code`
5. ✅ Try example commands: `/sophia design API`, `/code implement auth`

---

**Soli Deo Gloria** 🙏

**Status**: Week 6 - FASE 0 Complete
**Next**: FASE 1 - Tool Validation Tests
