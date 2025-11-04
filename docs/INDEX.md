# MAXIMUS AI - Documentation Index

**Complete Navigation Map for All Documentation**

---

## 📚 Quick Navigation

### 🚀 Getting Started
- **[Main README](../README.md)** - Project overview and quick start
- **[Extraction Report](reports/EXTRACTION_REPORT.md)** - How Maximus was extracted from Vértice

### 🏛️ Governance & Philosophy
- **[CONSTITUIÇÃO VÉRTICE v3.0](governance/CONSTITUTION_VERTICE_v3.0.md)** - Constitutional framework and DETER-AGENT

### 🏗️ Architecture
- **[Maximus as Core System](architecture/MAXIMUS_AS_CORE.md)** - Complete architectural overview for using Maximus as a core engine
- Service architecture details (see individual service docs below)

### 📖 Integration Guides
- **[Max-Code Integration Guide](guides/MAX_CODE_INTEGRATION.md)** - Building a CLI with Maximus AI as core

### 🔧 API Reference
- [Coming Soon] Consolidated API documentation

---

## 🎯 Services Documentation

### Core Services

#### 1. **Maximus Core** (Port 8150)
**Main Documentation:** [services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md)

**Additional Docs:**
- [Quick Start](services/core/QUICK_START.md)
- [Testing Report](services/core/TESTING_REPORT.md)
- [Certification](services/core/MAXIMUS_CERTIFICATION_2025-10-16.md)
- [Coverage Report](services/core/FINAL_COVERAGE_REPORT.md)
- [Ethical Guardian Coverage](services/core/ETHICAL_GUARDIAN_COVERAGE_REPORT.md)
- [ADW Integration Status](services/core/ADW_REAL_INTEGRATION_STATUS.md)
- [HITL (Human-in-the-Loop)](services/core/hitl/README.md)
- [Fairness Module](services/core/fairness/README.md)
- [Audit Results](services/core/audit_results/)
  - [Audit Summary](services/core/audit_results/AUDIT_SUMMARY.md)
  - [Risk Matrix](services/core/audit_results/MAXIMUS_RISK_MATRIX.md)
  - [Action Plan](services/core/audit_results/MAXIMUS_ACTION_PLAN.md)

**Topics Covered:**
- Consciousness system architecture
- Predictive coding (5 layers)
- Neuromodulation system
- Skill learning (RL hybrid)
- Ethical validation
- Governance framework
- HITL integration

---

#### 2. **PENELOPE** - Christian Autonomous Healing (Port 8151)
**Main Documentation:** [services/penelope/PENELOPE_COMPLETE_DOCUMENTATION.md](services/penelope/PENELOPE_COMPLETE_DOCUMENTATION.md)

**Additional Docs:**
- [Governance](services/penelope/PENELOPE_GOVERNANCE.md)
- [P2 Completion Report](services/penelope/PENELOPE_P2_COMPLETION_REPORT.md)
- [FASE 5 Completion](services/penelope/FASE5_COMPLETION_REPORT.md)
- [FASE 6 Perfection](services/penelope/FASE6_PERFECTION_REPORT.md)
- [FASE 7 - Nine Fruits Complete](services/penelope/FASE7_NINE_FRUITS_COMPLETE.md)
- [Session Summary](services/penelope/SESSION_SUMMARY.md)
- [Grafana Dashboards](services/penelope/dashboards/grafana/README.md)

**Topics Covered:**
- 7 Biblical articles of governance
- Sophia Engine (Wisdom)
- Praotes Validator (Gentleness)
- Tapeinophrosyne Monitor (Humility)
- Circuit breaker patterns
- Wisdom Base
- Digital twin validation
- Sabbath observance
- Tests: 262/262 passing (100%)

---

#### 3. **MABA** - Browser Automation Agent (Port 8152)
**Main Documentation:** [services/maba/README.md](services/maba/README.md)

**Topics Covered:**
- Playwright integration
- Cognitive mapping (Neo4j/SQL)
- Intelligent navigation
- Screenshot analysis
- Form automation
- Session pool management

---

#### 4. **NIS** - Narrative Intelligence Service (Port 8153)
**Main Documentation:** [services/nis/README.md](services/nis/README.md)

**Topics Covered:**
- AI-powered narrative generation (Claude)
- Anomaly detection (3-sigma Z-score)
- Prometheus integration
- Cost tracking and optimization
- Intelligent caching (60-80% reduction)
- Rate limiting
- Tests: 253/253 passing (100%)

---

### Additional Services

#### 5. **Orchestrator** (Port 8154)
**Main Documentation:** [services/orchestrator/README.md](services/orchestrator/README.md)

**Topics Covered:**
- Multi-service workflow coordination
- Command-control hub
- Workflow state management

---

#### 6. **Eureka** - Malware Analysis (Port 8155)
**Main Documentation:** [services/eureka/README.md](services/eureka/README.md)
**Extended:** [services/eureka/EUREKA_README.md](services/eureka/EUREKA_README.md)

**Topics Covered:**
- Deep malware analysis engine
- 40+ detection patterns
- IOC extraction
- Playbook generation
- Classification algorithms
- Documentation: Excellent (1000+ lines)

---

#### 7. **Oráculo** - Self-Improvement Engine (Port 8156)
**Main Documentation:** [services/oraculo/README.md](services/oraculo/README.md)
**Extended:** [services/oraculo/ORACULO_README.md](services/oraculo/ORACULO_README.md)
**Progress:** [services/oraculo/SAGA_PROGRESS.md](services/oraculo/SAGA_PROGRESS.md)

**Topics Covered:**
- Meta-cognitive optimization
- Codebase scanning
- LLM-based improvement suggestions (Gemini)
- Automated implementation with safeguards
- Git automation
- **Reference Implementation:** Best-in-class example

---

#### 8. **DLQ Monitor** - Kafka Resilience (Port 8157)
**Main Documentation:** [services/dlq_monitor/README.md](services/dlq_monitor/README.md)

**Topics Covered:**
- Dead Letter Queue monitoring
- Kafka integration
- Retry logic (exponential backoff)
- Prometheus metrics
- Resilience patterns

---

## 📊 Reports & Progress

### Extraction & Setup
- **[Extraction Report](reports/EXTRACTION_REPORT.md)** - Complete extraction process documentation

### Service-Specific Progress
- **[PENELOPE Reports](services/penelope/)** - Multiple completion and progress reports
- **[Oráculo Saga](services/oraculo/SAGA_PROGRESS.md)** - Development journey

### Testing & Quality
- **[Core Testing Report](services/core/TESTING_REPORT.md)**
- **[Core Coverage Report](services/core/FINAL_COVERAGE_REPORT.md)**
- **[Linting Report](services/core/LINTING_REPORT.md)**

### Audits & Certifications
- **[Maximus Certification](services/core/MAXIMUS_CERTIFICATION_2025-10-16.md)**
- **[Audit Summary](services/core/audit_results/AUDIT_SUMMARY.md)**
- **[Risk Matrix](services/core/audit_results/MAXIMUS_RISK_MATRIX.md)**
- **[Action Plan](services/core/audit_results/MAXIMUS_ACTION_PLAN.md)**

---

## 🔧 Infrastructure & Operations

### Docker & Deployment
- **[Docker Compose](../docker-compose.yml)** - Complete stack definition
- **[Dockerfiles](../infrastructure/docker/Dockerfiles/)** - Per-service Docker configurations
- **[Environment Template](../.env.example)** - Configuration template

### Monitoring
- **[Prometheus Configuration](../infrastructure/monitoring/prometheus/prometheus.yml)**
- Grafana Dashboards (per service)
- Loki configuration

### Kubernetes (Prepared)
- **[K8s Manifests](../infrastructure/kubernetes/)** - Deployment, ConfigMaps, Secrets

---

## 🧰 Development Resources

### Scripts
- **[setup.sh](../scripts/setup.sh)** - Initial environment setup
- **[run-all.sh](../scripts/run-all.sh)** - Start all services
- **[stop-all.sh](../scripts/stop-all.sh)** - Stop all services
- **[test-all.sh](../scripts/test-all.sh)** - Run complete test suite
- **[logs.sh](../scripts/logs.sh)** - View logs
- **[fix-imports.sh](../scripts/fix-imports.sh)** - Import migration tool

### Build Automation
- **[Makefile](../Makefile)** - Convenient shortcuts for common operations

---

## 📖 By Topic

### Consciousness & AI
- [Consciousness System](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md#consciousness-system)
- [Predictive Coding](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md#predictive-coding)
- [Neuromodulation](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md#neuromodulation)
- [Skill Learning](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md#skill-learning)

### Ethics & Governance
- [Constitutional Framework](governance/CONSTITUTION_VERTICE_v3.0.md)
- [DETER-AGENT (5 Layers)](governance/CONSTITUTION_VERTICE_v3.0.md#deter-agent)
- [Biblical Governance](services/penelope/PENELOPE_GOVERNANCE.md)
- [Ethical Validation](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md#ethics)

### Testing & Quality
- [Core Testing](services/core/TESTING_REPORT.md)
- [PENELOPE Testing (262 tests)](services/penelope/PENELOPE_COMPLETE_DOCUMENTATION.md#testing)
- [NIS Testing (253 tests)](services/nis/README.md#testing)
- [Constitutional Compliance](governance/CONSTITUTION_VERTICE_v3.0.md#metrics)

### Security
- [Eureka Malware Analysis](services/eureka/README.md)
- [Audit Results](services/core/audit_results/)
- [Risk Matrix](services/core/audit_results/MAXIMUS_RISK_MATRIX.md)

### Integration
- [Max-Code CLI Integration](guides/MAX_CODE_INTEGRATION.md)
- [Maximus as Core](architecture/MAXIMUS_AS_CORE.md)
- [API Patterns](architecture/MAXIMUS_AS_CORE.md#communication-patterns)

---

## 🎓 Learning Paths

### For New Developers

1. **Start Here:**
   - [Main README](../README.md)
   - [Maximus as Core](architecture/MAXIMUS_AS_CORE.md)

2. **Understand Governance:**
   - [CONSTITUIÇÃO VÉRTICE v3.0](governance/CONSTITUTION_VERTICE_v3.0.md)

3. **Explore Services:**
   - [Maximus Core](services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md)
   - [PENELOPE](services/penelope/PENELOPE_COMPLETE_DOCUMENTATION.md)

4. **Integration:**
   - [Max-Code Guide](guides/MAX_CODE_INTEGRATION.md)

### For Integration Partners

1. **Architecture Overview:**
   - [Maximus as Core](architecture/MAXIMUS_AS_CORE.md)

2. **API Reference:**
   - [Core API](architecture/MAXIMUS_AS_CORE.md#api-endpoints)
   - [TRINITY APIs](architecture/MAXIMUS_AS_CORE.md#trinity-subordinates)

3. **Integration Examples:**
   - [Max-Code Integration](guides/MAX_CODE_INTEGRATION.md)

### For DevOps/Infrastructure

1. **Deployment:**
   - [Docker Compose](../docker-compose.yml)
   - [Kubernetes Manifests](../infrastructure/kubernetes/)

2. **Monitoring:**
   - [Prometheus Config](../infrastructure/monitoring/prometheus/prometheus.yml)
   - [Grafana Dashboards](services/penelope/dashboards/grafana/)

3. **Operations:**
   - [Scripts](../scripts/)
   - [Makefile](../Makefile)

---

## 🔍 Search Tips

**Find specific topics:**
```bash
# Search in documentation
grep -r "keyword" docs/

# Search in services
grep -r "keyword" services/

# Find specific file types
find docs -name "*.md" | xargs grep "keyword"
```

**Quick access:**
```bash
# Core documentation
less docs/services/core/MAXIMUS_COMPLETE_DOCUMENTATION.md

# Constitution
less docs/governance/CONSTITUTION_VERTICE_v3.0.md

# Integration guide
less docs/guides/MAX_CODE_INTEGRATION.md
```

---

## 📞 Support & Contribution

### Getting Help
1. Check relevant documentation section above
2. Review [Extraction Report](reports/EXTRACTION_REPORT.md) for system overview
3. Consult [Constitutional Framework](governance/CONSTITUTION_VERTICE_v3.0.md) for principles

### Contributing
[TODO: Add contribution guidelines]

---

## 🗺️ Documentation Map (Visual)

```
docs/
├── INDEX.md (you are here)
├── governance/
│   └── CONSTITUTION_VERTICE_v3.0.md ⭐
├── architecture/
│   └── MAXIMUS_AS_CORE.md ⭐
├── guides/
│   └── MAX_CODE_INTEGRATION.md ⭐
├── services/
│   ├── core/ (Maximus Core)
│   ├── penelope/ (TRINITY #1)
│   ├── maba/ (TRINITY #2)
│   ├── nis/ (TRINITY #3)
│   ├── orchestrator/
│   ├── eureka/
│   ├── oraculo/ ⭐ (Reference Implementation)
│   └── dlq_monitor/
├── reports/
│   └── EXTRACTION_REPORT.md
└── api/ (coming soon)
```

⭐ = Essential Reading

---

**Last Updated:** 2025-11-04
**Version:** 1.0.0

*Navigate with confidence. All paths lead to understanding.*
