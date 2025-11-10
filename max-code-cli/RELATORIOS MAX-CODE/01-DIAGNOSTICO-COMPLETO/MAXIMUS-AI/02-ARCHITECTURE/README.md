# 🏗️ 02-ARCHITECTURE - System Architecture

**Understanding MAXIMUS AI system design and service interactions.**

---

## 📂 Directory Structure

```
02-ARCHITECTURE/
├── integration/       # Service integration and dependencies
├── data-flow/        # Data flow diagrams and patterns
├── services/         # Individual service architectures
└── diagrams/         # Architecture diagrams
```

---

## 🔗 Service Integration

### [Service Dependencies](integration/SERVICE_DEPENDENCIES.md)
**Complete map of service interactions**

- Dependency graph (Mermaid diagram)
- Integration details for each service
- Client implementations
- Communication patterns

**Key Insights:**
- Which services depend on which
- How services communicate
- Integration clients used
- API contracts between services

---

## 🌊 Data Flow

### Patterns
- Request-response flows
- Event-driven architecture
- Message queue patterns
- Database access patterns

### Technologies
- **REST APIs** - Synchronous communication
- **Kafka** - Asynchronous messaging
- **Redis** - Caching and queues
- **PostgreSQL** - Persistent storage
- **Neo4j** - Graph relationships

---

## 🎯 Architecture Principles

### Design Patterns
- **Microservices** - Independent, scalable services
- **Event Sourcing** - Event-driven state changes
- **CQRS** - Command-query separation
- **Circuit Breaker** - Fault tolerance
- **Service Mesh** - Service-to-service communication

### Technology Choices
- **Python 3.11+** - Modern, type-hinted code
- **FastAPI** - High-performance APIs
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Prometheus/Grafana** - Observability

---

## 📊 Service Architecture Overview

### Core Layer
- **CORE** - Central orchestration
- **ORCHESTRATOR** - Workflow coordination

### Analysis Layer
- **EUREKA** - Code analysis
- **ORACULO** - Risk assessment
- **MABA** - Knowledge graphs

### Security Layer
- **NIS** - Network intrusion detection
- **PENELOPE** - Self-healing

### Support Layer
- **DLQ_MONITOR** - Error handling

---

## 🔍 Understanding Service Interactions

### Synchronous Calls
Services make direct HTTP calls for:
- Real-time responses needed
- Critical path operations
- User-facing APIs

### Asynchronous Messaging
Services use Kafka for:
- Event notifications
- Background processing
- Decoupled operations
- Scalability

### Shared Storage
Services access shared databases for:
- Configuration
- Shared state
- Cross-service queries

---

## 🎯 How to Use This Section

### For System Design
1. Start with [Service Dependencies](integration/SERVICE_DEPENDENCIES.md)
2. Understand communication patterns
3. Review individual service architectures
4. Check data flow diagrams

### For Integration Work
1. Identify services you need to integrate
2. Check dependency map
3. Review integration clients
4. Understand data contracts

### For Troubleshooting
1. Check service dependencies
2. Verify communication paths
3. Review error handling patterns
4. Check circuit breaker configurations

---

## 📝 Architecture Decision Records

(To be added: ADRs documenting major architectural decisions)

---

**[← Back to Main](../README.md)** | **[Next: Development →](../03-DEVELOPMENT/)**
