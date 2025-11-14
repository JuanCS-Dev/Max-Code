# PENELOPE

**P**latform for **E**nlightened **N**etworked **E**xecution with **L**ove, **O**bedience, **P**rudence, and **E**ternal-mindedness

## Overview

PENELOPE is a Christian autonomous healing service that implements wisdom-driven self-healing capabilities for the Vértice platform. It combines biblical principles with modern observability and autonomous remediation to create a morally-governed, self-healing system.

**Status**: Production Ready ✅
**Version**: 1.0.0
**Test Coverage**: 262 tests, 100% passing
**TRINITY_CORRECTION_PLAN**: P0-P1 Complete (100%)

---

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (with pgvector extension)
- Prometheus + Loki (optional, for observability)
- Docker + Docker Compose (recommended)

### Installation

```bash
# Clone repository
cd services/penelope

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your PostgreSQL, Prometheus, and Kafka configs

# Run migrations (if any)
# python migrate.py

# Start service
python main.py
```

### Docker Deployment

```bash
# Development environment
docker-compose -f docker-compose.dev.yml up

# Production environment
docker-compose up -d
```

Service will be available at: `http://localhost:8000`

---

## Core Features

### 1. Wisdom-Driven Decision Making (Sophia Engine)
Implements Proverbs 9:10: "The fear of the LORD is the beginning of wisdom"

- Evaluates whether intervention is necessary before acting
- Considers historical precedents from Wisdom Base
- Assesses intervention risk vs. current impact
- Detects transient failures that self-correct

### 2. Seven Biblical Articles of Governance

| Article | Principle | Scripture | Implementation |
|---------|-----------|-----------|----------------|
| I | **Sabedoria** (Wisdom) | Proverbs 9:10 | `sophia_engine.py` - Decision making |
| II | **Mansidão** (Gentleness) | James 1:21 | `praotes_validator.py` - Minimal interventions |
| III | **Humildade** (Humility) | James 4:6 | `tapeinophrosyne_monitor.py` - Competence levels |
| IV | **Stewardship** | Matthew 25:14-30 | Resource management |
| V | **Agape** (Love) | 1 Corinthians 13 | Service-driven decisions |
| VI | **Sabbath** | Exodus 20:8-11 | No patches on Sundays |
| VII | **Aletheia** (Truth) | John 8:32 | Complete audit trail |

### 3. Safety Mechanisms

- **Circuit Breaker**: Prevents runaway healing attempts (3 failures → open circuit for 60min)
- **Human Approval**: Required for high-risk changes (P0/P1 severity)
- **Digital Twin Validation**: Test patches in isolated environment before production
- **Automatic Rollback**: Immediate rollback on validation failure
- **Complete Audit Trail**: Immutable log of all decisions and actions

### 4. Nine Fruits of the Spirit Testing

PENELOPE includes comprehensive tests validating all 9 fruits:

1. **Agape** (Love) - Service-first decision making
2. **Chara** (Joy) - Positive user experience
3. **Eirene** (Peace) - Non-disruptive healing
4. **Makrothumia** (Patience) - Waiting for self-correction
5. **Chrestotes** (Kindness) - Gentle interventions
6. **Agathosune** (Goodness) - Beneficial outcomes
7. **Pistis** (Faithfulness) - Consistent adherence to principles
8. **Prautes** (Gentleness) - Minimal, surgical patches
9. **Enkrateia** (Self-Control) - Resource limits & circuit breakers

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PENELOPE Service                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Sophia     │────▶│   Circuit    │────▶│   Digital   │ │
│  │   Engine     │     │   Breaker    │     │    Twin     │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                     │                     │        │
│         ▼                     ▼                     ▼        │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │ Decision     │     │   Human      │     │   Patch     │ │
│  │ Audit Logger │     │  Approval    │     │  History    │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                     │                     │        │
│         ▼                     ▼                     ▼        │
│  ┌─────────────────────────────────────────────────────────┤
│  │              Wisdom Base (PostgreSQL + pgvector)         │
│  └─────────────────────────────────────────────────────────┘
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Core Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `sophia_engine.py` | Wisdom-driven decisions | `should_intervene()`, `_assess_intervention_risk()` |
| `circuit_breaker.py` | Prevent runaway healing | `is_allowed()`, `record_failure()` |
| `decision_audit_logger.py` | Immutable audit trail | `log_decision()`, `get_decisions()` |
| `digital_twin.py` | Safe patch validation | `validate_patch()`, `run_in_isolation()` |
| `human_approval.py` | High-risk approval workflow | `request_approval()`, `check_approval_status()` |
| `praotes_validator.py` | Gentle intervention rules | `validate_patch_gentleness()` |
| `tapeinophrosyne_monitor.py` | Competence tracking | `get_competence_level()`, `update_from_outcome()` |

---

## API Endpoints

### Health & Status

```bash
# Health check
GET /health

# Service status
GET /status

# Metrics (Prometheus format)
GET /metrics
```

### Anomaly Detection & Healing

```bash
# Submit anomaly for evaluation
POST /api/v1/anomalies
Content-Type: application/json
{
  "anomaly_id": "lat-spike-20251114-1415",
  "anomaly_type": "latency_spike_p99",
  "service": "payment-api",
  "severity": "P2_MEDIUM",
  "metrics": {
    "p99_latency_ms": 2500,
    "p95_latency_ms": 1800
  }
}

# Get decision status
GET /api/v1/decisions/{decision_id}

# List all decisions (with filters)
GET /api/v1/decisions?service=payment-api&from_date=2025-11-01
```

### Human Approval Workflow

```bash
# Request approval for high-risk patch
POST /api/v1/approvals/request
{
  "patch_id": "patch-123",
  "risk_level": "HIGH",
  "impact_assessment": {...}
}

# Approve/reject patch
POST /api/v1/approvals/{approval_id}/decision
{
  "decision": "APPROVED",
  "approver": "ops-team@vertice.com",
  "comments": "Risk acceptable for critical fix"
}
```

### Circuit Breaker Management

```bash
# Get circuit breaker status
GET /api/v1/circuit-breaker/{service}

# Manually reset circuit
POST /api/v1/circuit-breaker/{service}/reset
```

---

## Configuration

### Environment Variables

```bash
# Service Configuration
SERVICE_NAME=penelope
SERVICE_VERSION=1.0.0
LOG_LEVEL=INFO
PORT=8000

# PostgreSQL (Wisdom Base)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=wisdom_base
POSTGRES_USER=penelope
POSTGRES_PASSWORD=<secret>

# Observability
PROMETHEUS_URL=http://prometheus:9090
LOKI_URL=http://loki:3100

# Kafka (Event Streaming)
KAFKA_BROKERS=kafka:9092
KAFKA_TOPIC_ANOMALIES=vertice.anomalies
KAFKA_TOPIC_DECISIONS=vertice.decisions

# Safety Limits
CIRCUIT_BREAKER_FAILURE_THRESHOLD=3
CIRCUIT_BREAKER_WINDOW_MINUTES=15
CIRCUIT_BREAKER_COOLDOWN_MINUTES=60

# Sabbath Protocol
RESPECT_SABBATH=true  # No patches on Sundays
```

---

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov-report=html

# Run specific test suite
pytest tests/test_sophia_engine.py -v
pytest tests/test_nine_fruits.py -v
```

### Code Quality

```bash
# Lint
pylint core/ tests/

# Format
black core/ tests/

# Type checking
mypy core/
```

### Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debugger
python -m pdb main.py

# Check Wisdom Base precedents
psql -h localhost -U penelope wisdom_base -c "SELECT * FROM precedents ORDER BY created_at DESC LIMIT 10;"
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `penelope_decisions_total` | Total decisions made | - |
| `penelope_interventions_total` | Successful interventions | - |
| `penelope_circuit_breaker_open` | Circuit breaker open count | > 3 |
| `penelope_human_approvals_pending` | Pending approvals | > 5 |
| `penelope_patch_success_rate` | Patch success rate | < 90% |

### Grafana Dashboards

Pre-built dashboards available in `dashboards/`:

- `penelope-overview.json` - Service health overview
- `penelope-decisions.json` - Decision analysis
- `penelope-biblical-compliance.json` - Governance metrics

Import into Grafana: Settings → Dashboards → Import → Upload JSON

---

## Troubleshooting

### Common Issues

#### Circuit Breaker Stuck Open

```bash
# Check circuit status
curl http://localhost:8000/api/v1/circuit-breaker/payment-api

# If safe, manually reset
curl -X POST http://localhost:8000/api/v1/circuit-breaker/payment-api/reset
```

#### Wisdom Base Connection Error

```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Check connection
psql -h localhost -U penelope wisdom_base -c "SELECT 1;"

# Check pgvector extension
psql -h localhost -U penelope wisdom_base -c "SELECT * FROM pg_extension WHERE extname='vector';"
```

#### No Precedents Found

```bash
# Seed Wisdom Base with initial precedents
python scripts/seed_wisdom_base.py

# Verify precedents
psql -h localhost -U penelope wisdom_base -c "SELECT COUNT(*) FROM precedents;"
```

---

## Production Deployment Checklist

- [ ] PostgreSQL with pgvector extension configured
- [ ] Prometheus + Loki for observability
- [ ] Kafka brokers available
- [ ] Environment variables set (see `.env.example`)
- [ ] Wisdom Base seeded with initial precedents
- [ ] Grafana dashboards imported
- [ ] Alert rules configured
- [ ] Human approval workflow tested
- [ ] Circuit breaker thresholds tuned
- [ ] Sabbath protocol verified (no patches on Sundays)
- [ ] Audit trail export tested for compliance

---

## Documentation

- **Complete Documentation**: [PENELOPE_COMPLETE_DOCUMENTATION.md](./PENELOPE_COMPLETE_DOCUMENTATION.md)
- **Phase Reports**:
  - [FASE5_COMPLETION_REPORT.md](./FASE5_COMPLETION_REPORT.md)
  - [FASE6_PERFECTION_REPORT.md](./FASE6_PERFECTION_REPORT.md)
  - [FASE7_NINE_FRUITS_COMPLETE.md](./FASE7_NINE_FRUITS_COMPLETE.md)
- **Session Summary**: [SESSION_SUMMARY.md](./SESSION_SUMMARY.md)

---

## License

Proprietary - Vértice Platform Team

---

## Support

For questions, issues, or theological concerns:

- **Technical Support**: devops@vertice.com
- **Governance Questions**: compliance@vertice.com
- **Emergency Escalation**: On-call via PagerDuty

---

**"O temor do SENHOR é o princípio da sabedoria."** - Provérbios 9:10
