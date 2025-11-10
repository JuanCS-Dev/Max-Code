# MAXIMUS - Docker Compose Guide

**Gerado:** 2025-11-07 20:45:00

---

## Services Configuration

```yaml
version: "3.8"

services:
  # ============================================================================
  # INFRASTRUCTURE SERVICES
  # ============================================================================

  postgres:
    image: postgres:15-alpine
    container_name: maximus-postgres
    environment:
      POSTGRES_USER: maximus
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-maximus_dev_password}
      POSTGRES_DB: maximus
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U maximus"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - maximus-network

  redis:
    image: redis:7-alpine
    container_name: maximus-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - maximus-network

  neo4j:
    image: neo4j:5.28-community
    container_name: maximus-neo4j
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD:-maximus_neo4j_password}
      NEO4J_PLUGINS: '["apoc"]'
      NEO4J_dbms_security_procedures_unrestricted: apoc.*
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p ${NEO4J_PASSWORD:-maximus_neo4j_password} 'RETURN 1'"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - maximus-network

  # ============================================================================
  # MONITORING STACK
  # ============================================================================

  prometheus:
    image: prom/prometheus:v2.47.0
    container_name: maximus-prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    volumes:
      - ./infrastructure/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - maximus-network
    depends_on:
      - maximus-core

  grafana:
    image: grafana/grafana:10.1.0
    container_name: maximus-grafana
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./infrastructure/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./infrastructure/monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    networks:
      - maximus-network
    depends_on:
      - prometheus

  loki:
    image: grafana/loki:2.9.0
    container_name: maximus-loki
    command: -config.file=/etc/loki/local-config.yaml
    ports:
      - "3100:3100"
    volumes:
      - loki_data:/loki
    networks:
      - maximus-network

  # ============================================================================
  # MAXIMUS CORE SERVICE
  # ============================================================================

  maximus-core:
    build:
      context: ./services/core
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.core
    container_name: maximus-core
    environment:
      - SERVICE_NAME=maximus-core
      - SERVICE_PORT=8150
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=maximus
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-maximus_dev_password}
      - POSTGRES_DB=maximus
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - CONSTITUTION_VERSION=3.0
      - FRAMEWORK=DETER-AGENT
    ports:
      - "8150:8150"
    volumes:
      - ./services/core:/app
      - ./libs:/app/libs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8150/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - maximus-network
    restart: unless-stopped

  # ============================================================================
  # TRINITY SUBORDINATES
  # ============================================================================

  penelope:
    build:
      context: ./services/penelope
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.penelope
    container_name: maximus-penelope
    environment:
      - SERVICE_NAME=penelope
      - SERVICE_PORT=8151
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=maximus
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-maximus_dev_password}
      - POSTGRES_DB=maximus
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - SABBATH_ENABLED=true
      - CONSTITUTION_VERSION=3.0
    ports:
      - "8151:8151"
    volumes:
      - ./services/penelope:/app
      - ./libs:/app/libs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      maximus-core:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8151/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - maximus-network
    restart: unless-stopped

  maba:
    build:
      context: ./services/maba
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.maba
    container_name: maximus-maba
    environment:
      - SERVICE_NAME=maba
      - SERVICE_PORT=8152
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=maximus
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-maximus_dev_password}
      - POSTGRES_DB=maximus
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD:-maximus_neo4j_password}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - HEADLESS_BROWSER=true
    ports:
      - "8152:8152"
    volumes:
      - ./services/maba:/app
      - ./libs:/app/libs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      maximus-core:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8152/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - maximus-network
    restart: unless-stopped

  nis:
    build:
      context: ./services/nis
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.nis
    container_name: maximus-nis
    environment:
      - SERVICE_NAME=nis
      - SERVICE_PORT=8153
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - PROMETHEUS_URL=http://prometheus:9090
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - CACHE_ENABLED=true
      - COST_TRACKING_ENABLED=true
      - CONSTITUTION_VERSION=3.0
    ports:
      - "8153:8153"
    volumes:
      - ./services/nis:/app
      - ./libs:/app/libs
    depends_on:
      redis:
        condition: service_healthy
      prometheus:
        condition: service_started
      maximus-core:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8153/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - maximus-network
    restart: unless-stopped

  # ============================================================================
  # ADDITIONAL MAXIMUS SERVICES
  # ============================================================================

  orchestrator:
    build:
      context: ./services/orchestrator
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.orchestrator
    container_name: maximus-orchestrator
    environment:
      - SERVICE_NAME=orchestrator
      - SERVICE_PORT=8154
      - MAXIMUS_CORE_URL=http://maximus-core:8150
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    ports:
      - "8154:8154"
    volumes:
      - ./services/orchestrator:/app
      - ./libs:/app/libs
    depends_on:
      - maximus-core
    networks:
      - maximus-network
    restart: unless-stopped

  eureka:
    build:
      context: ./services/eureka
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.eureka
    container_name: maximus-eureka
    environment:
      - SERVICE_NAME=eureka
      - SERVICE_PORT=8155
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    ports:
      - "8155:8155"
    volumes:
      - ./services/eureka:/app
      - ./libs:/app/libs
    depends_on:
      - maximus-core
    networks:
      - maximus-network
    restart: unless-stopped

  oraculo:
    build:
      context: ./services/oraculo
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.oraculo
    container_name: maximus-oraculo
    environment:
      - SERVICE_NAME=oraculo
      - SERVICE_PORT=8156
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    ports:
      - "8156:8156"
    volumes:
      - ./services/oraculo:/app
      - ./libs:/app/libs
    depends_on:
      - maximus-core
    networks:
      - maximus-network
    restart: unless-stopped

  dlq-monitor:
    build:
      context: ./services/dlq_monitor
      dockerfile: ../../infrastructure/docker/Dockerfiles/Dockerfile.dlq_monitor
    container_name: maximus-dlq-monitor
    environment:
      - SERVICE_NAME=dlq-monitor
      - SERVICE_PORT=8157
      - KAFKA_BOOTSTRAP_SERVERS=${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    ports:
      - "8157:8157"
    volumes:
      - ./services/dlq_monitor:/app
      - ./libs:/app/libs
    depends_on:
      - maximus-core
    networks:
      - maximus-network
    restart: unless-stopped

networks:
  maximus-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  neo4j_data:
  neo4j_logs:
  prometheus_data:
  grafana_data:
  loki_data:
```

## Service Ports

| Service | Port | Internal Port |
|---------|------|---------------|
| postgres | 5432 | 5432 |
| environment | 5432 | 5432 |
| volumes | 5432 | 5432 |
| ports | 5432 | 5432 |
| healthcheck | 6379 | 6379 |
| networks | 6379 | 6379 |
| redis | 6379 | 6379 |
| volumes | 5432 | 5432 |
| ports | 5432 | 5432 |
| healthcheck | 6379 | 6379 |
| networks | 6379 | 6379 |
| environment | 5432 | 5432 |
| volumes | 5432 | 5432 |
| ports | 5432 | 5432 |
| healthcheck | 6379 | 6379 |
| networks | 6379 | 6379 |
| prometheus | 9090 | 9090 |
| command | 6379 | 6379 |
| volumes | 5432 | 5432 |
| ports | 5432 | 5432 |
| networks | 6379 | 6379 |
| depends_on | 3000 | 3000 |
| grafana | 3000 | 3000 |
| environment | 5432 | 5432 |
| volumes | 5432 | 5432 |
| ports | 5432 | 5432 |
| networks | 6379 | 6379 |
| depends_on | 3000 | 3000 |


## Environment Variables

### Common Infrastructure
```bash
# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/maximus
REDIS_URL=redis://redis:6379

# Message Broker
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Monitoring
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000
```

### Service-Specific Variables

## Dockerfiles

### core

```dockerfile
# 🐳 MAXIMUS Core Service - Production Dockerfile
#
# Version: 2.0 (uv + multi-stage)
# Base: vertice/python311-uv
# Performance: 5x faster build, 80% smaller
#
# Build: docker build -t maximus-core:latest .
# Run: docker run -p 8150:8150 maximus-core:latest

# ============================================================================
# BUILDER STAGE - Instala dependências com uv
# ============================================================================
FROM vertice/python311-uv:latest AS builder

LABEL stage="builder"

# Mudar para root temporariamente para instalar dependências
USER root

WORKDIR /build
...
# (88 total lines)
```

### dlq_monitor

```dockerfile
# Dockerfile for maximus_dlq_monitor_service
# Auto-generated by generate_compose_files.py
# Glory to YHWH! 🙏

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

...
# (33 total lines)
```

### eureka

```dockerfile
FROM vertice/python311-uv:latest AS builder
USER root
WORKDIR /build
COPY pyproject.toml requirements.txt ./
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && uv pip sync requirements.txt

FROM python:3.11-slim
LABEL maintainer="Juan & Claude" version="2.1.1"
RUN apt-get update && apt-get install -y --no-install-recommends curl libpq5 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:${PYTHONPATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN groupadd -r appuser && useradd -r -g appuser --uid 1000 appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8200/health || exit 1
...
# (26 total lines)
```

### maba

```dockerfile
# MABA (MAXIMUS Browser Agent) - Production Dockerfile
#
# Version: 1.0
# Base: python:3.11-slim + Playwright
#
# Build: docker build -t maba:latest .
# Run: docker run -p 8152:8152 maba:latest

# ============================================================================
# BUILDER STAGE - Install dependencies
# ============================================================================
FROM python:3.11-slim AS builder

LABEL stage="builder"

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
...
# (123 total lines)
```

### nis

```dockerfile
# MVP (MAXIMUS Vision Protocol) - Production Dockerfile
#
# Version: 1.0
# Base: python:3.11-slim
#
# Build: docker build -t mvp:latest .
# Run: docker run -p 8153:8153 mvp:latest

# ============================================================================
# BUILDER STAGE - Install dependencies
# ============================================================================
FROM python:3.11-slim AS builder

LABEL stage="builder"

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
...
# (92 total lines)
```

### oraculo

```dockerfile
FROM vertice/python311-uv:latest AS builder
USER root
WORKDIR /build
COPY pyproject.toml requirements.txt ./
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && uv pip sync requirements.txt

FROM python:3.11-slim
LABEL maintainer="Juan & Claude" version="2.0.0"
RUN apt-get update && apt-get install -y --no-install-recommends curl libpq5 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="/app/../../..:$PYTHONPATH"
RUN groupadd -r appuser && useradd -r -g appuser --uid 1000 appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8038/health || exit 1
EXPOSE 8038

# Constitutional v3.0 - Metrics port
EXPOSE 9090
...
# (22 total lines)
```

### orchestrator

```dockerfile
FROM vertice/python311-uv:latest AS builder
USER root
WORKDIR /build
COPY pyproject.toml requirements.txt ./
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && uv pip sync requirements.txt

FROM python:3.11-slim
LABEL maintainer="Juan & Claude" version="2.0.0"
RUN apt-get update && apt-get install -y --no-install-recommends curl libpq5 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN groupadd -r appuser && useradd -r -g appuser --uid 1000 appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8016/health || exit 1
EXPOSE 8016

# Constitutional v3.0 - Metrics port
EXPOSE 9090
...
# (22 total lines)
```

### penelope

```dockerfile
# PENELOPE (Self-Healing Service) - Production Dockerfile
#
# Version: 1.0 - Biblical Governance Edition
# Base: python:3.11-slim
#
# Build: docker build -t penelope:latest .
# Run: docker run -p 8154:8154 penelope:latest

# ============================================================================
# BUILDER STAGE - Install dependencies
# ============================================================================
FROM python:3.11-slim AS builder

LABEL stage="builder"

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
...
# (104 total lines)
```

