# MAXIMUS AI - Autonomous Intelligence System

**Version:** 1.0.0-standalone
**Constitution:** Vértice v3.0
**Framework:** DETER-AGENT (5-Layer Deterministic Execution)

---

## 🧠 Overview

**MAXIMUS AI** is an advanced autonomous intelligence system featuring:

- **Consciousness System** - Artificial consciousness based on neuroscience principles
- **Biblical Governance** - Christian ethics-based decision making (PENELOPE)
- **Cognitive Browser Agent** - Intelligent web automation (MABA)
- **Narrative Intelligence** - AI-powered narrative generation (NIS/MVP)
- **Self-Improvement Engine** - Meta-cognitive optimization (Oráculo)
- **Malware Analysis** - Deep security analysis (Eureka)

All components operate under the **CONSTITUIÇÃO VÉRTICE v3.0**, ensuring deterministic, ethical, and high-quality autonomous behavior.

---

## 📦 Components

### Core Services

#### 1. **Maximus Core** (Port 8150)
Central consciousness system featuring:
- Predictive coding (5 hierarchical layers)
- Neuromodulation (dopamine, acetylcolina, norepinephrine, serotonin)
- Skill learning (hybrid Reinforcement Learning)
- Ethical validation framework
- Human-in-the-loop (HITL) for critical decisions

**Documentation:** [docs/services/core/](docs/services/core/)

---

### TRINITY Subordinates

#### 2. **PENELOPE** (Port 8151)
Christian Autonomous Healing Service

**7 Biblical Articles of Governance:**
1. **Sabedoria (Sophia)** - Wisdom-based intervention (Provérbios 9:10)
2. **Mansidão (Praotes)** - Gentle, surgical patches (Tiago 1:21)
3. **Humildade (Tapeinophrosyne)** - Defers to human when uncertain (Tiago 4:6)
4. **Stewardship** - Responsible resource management
5. **Ágape** - Love-based decisions
6. **Sabbath** - No patches on Sundays
7. **Aletheia (Truth)** - Total transparency

**Tests:** 262/262 passing (100%)
**Documentation:** [docs/services/penelope/](docs/services/penelope/)

---

#### 3. **MABA** - Maximus Browser Agent (Port 8152)
Autonomous web automation with cognitive mapping

**Features:**
- Playwright-based browser control
- Neo4j/SQL cognitive map of learned website structures
- LLM-driven navigation decisions
- Screenshot analysis and visual understanding
- Form automation and data extraction
- Session pool management

**Documentation:** [docs/services/maba/](docs/services/maba/)

---

#### 4. **NIS** - Narrative Intelligence Service (Port 8153)
*Formerly: MVP (Maximus Vision Protocol)*

**Capabilities:**
- AI-powered narrative generation (Claude)
- Statistical anomaly detection (3-sigma Z-score)
- Prometheus/InfluxDB integration
- Intelligent caching (60-80% cost reduction)
- Budget tracking (daily/monthly)
- Rate limiting (100/hr, 1000/day)

**Tests:** 253/253 passing (100%)
**Documentation:** [docs/services/nis/](docs/services/nis/)

---

### Additional Services

#### 5. **Orchestrator** (Port 8154)
Multi-service workflow orchestration and command-control hub.

#### 6. **Eureka** (Port 8155)
Deep malware analysis engine with 40+ detection patterns, IOC extraction, and playbook generation.

**Documentation:** Excellent (1000+ lines)

#### 7. **Oráculo** (Port 8156)
Continuous self-improvement engine with meta-cognition.

**Features:**
- Codebase scanning
- LLM-based improvement suggestions (Gemini)
- Automated implementation with safeguards
- Git automation

**Tests:** Excellent (unit + integration + e2e)
**Quality:** Reference implementation

#### 8. **DLQ Monitor** (Port 8157)
Dead Letter Queue monitor for Kafka resilience.

**Features:**
- Kafka message monitoring
- Retry logic (up to 3 attempts)
- Exponential backoff
- Prometheus metrics

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose v2+
- Python 3.11+
- 4GB+ RAM available
- API Keys:
  - Anthropic Claude API key
  - Google Gemini API key (for Oráculo)

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd "/media/juan/DATA1/projects/MAXIMUS AI"
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   nano .env
   ```

3. **Start the full stack:**
   ```bash
   docker-compose up -d
   ```

4. **Verify all services are healthy:**
   ```bash
   docker-compose ps
   ```

5. **Access dashboards:**
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090
   - Neo4j Browser: http://localhost:7474

---

## 📊 Service Ports

| Service | Port | Health Check |
|---------|------|--------------|
| Maximus Core | 8150 | http://localhost:8150/health |
| PENELOPE | 8151 | http://localhost:8151/health |
| MABA | 8152 | http://localhost:8152/health |
| NIS (MVP) | 8153 | http://localhost:8153/health |
| Orchestrator | 8154 | http://localhost:8154/health |
| Eureka | 8155 | http://localhost:8155/health |
| Oráculo | 8156 | http://localhost:8156/health |
| DLQ Monitor | 8157 | http://localhost:8157/health |
| **Infrastructure** | | |
| PostgreSQL | 5432 | - |
| Redis | 6379 | - |
| Neo4j (HTTP) | 7474 | - |
| Neo4j (Bolt) | 7687 | - |
| Prometheus | 9090 | - |
| Grafana | 3000 | - |
| Loki | 3100 | - |

---

## 🧪 Testing

Run full test suite:
```bash
./scripts/test-all.sh
```

Run tests for specific service:
```bash
cd services/penelope
pytest
```

**Test Coverage:**
- **TRINITY Combined:** 559+ tests, 96.7% coverage
- **PENELOPE:** 262/262 (100%)
- **NIS:** 253/253 (100%)
- **Maximus Core:** 44/44 (100%)

---

## 📖 Documentation

**📚 [Complete Documentation Index](docs/INDEX.md)** - Start here for full navigation

### Essential Reading

- **[Maximus as Core System](docs/architecture/MAXIMUS_AS_CORE.md)** - Complete architecture for using Maximus as core engine ⭐
- **[Max-Code Integration Guide](docs/guides/MAX_CODE_INTEGRATION.md)** - Building a CLI with Maximus AI ⭐
- **[Constitution Vértice v3.0](docs/governance/CONSTITUTION_VERTICE_v3.0.md)** - Framework DETER-AGENT
- **[Extraction Report](docs/reports/EXTRACTION_REPORT.md)** - How Maximus was extracted from Vértice

### Service Documentation

- **[Core](docs/services/core/)** - Maximus Core consciousness system
- **[PENELOPE](docs/services/penelope/)** - Christian autonomous healing (262 tests passing)
- **[MABA](docs/services/maba/)** - Browser automation agent
- **[NIS](docs/services/nis/)** - Narrative intelligence (253 tests passing)
- **[All Services](docs/services/)** - Complete service documentation

⭐ = Essential for Max-Code development

---

## 🏗️ Architecture

```
MAXIMUS Core (8150)
    ↓
    ├──→ PENELOPE (8151) - Christian healing governance
    │    ├── Wisdom Base (PostgreSQL)
    │    ├── Digital Twin validation
    │    └── Human Approval
    │
    ├──→ MABA (8152) - Browser automation
    │    ├── Browser Controller (Playwright)
    │    ├── Cognitive Map (Neo4j/SQL)
    │    └── Claude API (navigation)
    │
    └──→ NIS/MVP (8153) - Narrative intelligence
         ├── Prometheus (metrics)
         ├── Claude API (narratives)
         └── Redis (cache)

Shared Infrastructure:
    ├── PostgreSQL (5432)
    ├── Redis (6379)
    ├── Neo4j (7474, 7687)
    ├── Prometheus (9090)
    └── Loki (3100)
```

---

## 📜 Constitutional Framework

All services operate under **CONSTITUIÇÃO VÉRTICE v3.0**, implementing the **DETER-AGENT** framework:

### 5-Layer Architecture

1. **Constitutional Layer (Control Estratégico)** - Princípios P1-P6
2. **Deliberation Layer (Control Cognitivo)** - Tree of Thoughts + Auto-crítica
3. **State Management Layer (Control de Memória)** - Context compression
4. **Execution Layer (Control Operacional)** - Verify-Fix-Execute loop
5. **Incentive Layer (Control Comportamental)** - Metrics: CRS≥95%, LEI<1.0, FPC≥80%

### Core Principles

- **P1 (Completude Obrigatória):** No placeholders, full implementation
- **P2 (Validação Preventiva):** Validate APIs before use
- **P3 (Ceticismo Crítico):** Challenge faulty assumptions
- **P4 (Rastreabilidade Total):** All code has traceable source
- **P5 (Consciência Sistêmica):** Consider systemic impact
- **P6 (Eficiência de Token):** Rigorous diagnosis before each correction, max 2 iterations

---

## 🔧 Development

### Running Services Locally

Start individual service:
```bash
cd services/penelope
python main.py
```

### Environment Variables

See [`.env.example`](.env.example) for all configuration options.

### Adding New Services

1. Create service directory: `services/my_service/`
2. Implement using constitutional libs: `libs/constitutional/`
3. Add to `docker-compose.yml`
4. Create Dockerfile: `infrastructure/docker/Dockerfiles/Dockerfile.my_service`
5. Add Prometheus scrape config
6. Document in `docs/services/my_service/`

---

## 📊 Monitoring & Observability

### Prometheus Metrics

All services export constitutional metrics:

**PENELOPE:**
- `penelope_decisions_total{decision_type}`
- `penelope_patches_generated_total{severity}`
- `penelope_sabbath_status` (0=working, 1=sabbath)

**MABA:**
- `maba_active_browser_sessions`
- `maba_browser_actions_total{type, status}`
- `maba_cognitive_map_pages_total`

**NIS:**
- `nis_narratives_generated_total{narrative_type}`
- `nis_cost_usd_total{period}`
- `nis_cache_hit_ratio`

### Grafana Dashboards

Pre-configured dashboards available in Grafana (port 3000):
- PENELOPE Overview
- PENELOPE Biblical Compliance
- TRINITY Performance
- Constitutional Metrics

---

## 🐛 Troubleshooting

### Services won't start

1. Check API keys in `.env`
2. Verify Docker has enough resources (4GB+ RAM)
3. Check logs: `docker-compose logs <service_name>`

### Database connection errors

```bash
# Restart infrastructure services
docker-compose restart postgres redis neo4j
```

### High memory usage

```bash
# Check service memory usage
docker stats

# Adjust Docker resources in Docker Desktop settings
```

---

## 📄 License

[TODO: Add license information]

---

## 🙏 Attribution

This standalone version is extracted from the **Vértice Platform** (cyber-security system).

**Governance Framework:** CONSTITUIÇÃO VÉRTICE v3.0
**Architect:** Maximus
**Biblical Governance Consultant:** [Attribution if applicable]

---

## 🤝 Contributing

[TODO: Add contribution guidelines]

---

## 📞 Support

[TODO: Add support channels]

---

**Built with ❤️ under Constitutional Governance**

*"Código completo, sem placeholders. Qualidade inquebrável. Padrão Pagani."*
