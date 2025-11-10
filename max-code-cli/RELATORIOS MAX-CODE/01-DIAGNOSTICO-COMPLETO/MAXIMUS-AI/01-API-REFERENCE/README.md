# 🔌 01-API-REFERENCE - Complete API Documentation

**Comprehensive API documentation for all MAXIMUS services.**

---

## 📂 Directory Structure

```
01-API-REFERENCE/
├── services/          # Individual service APIs (8 services)
├── indexes/           # Class and function indexes
├── core/              # Core components documentation
├── libs/              # Shared libraries
└── cli/               # CLI interface docs
```

---

## 🔧 Services

### Core Services

#### [CORE](services/core_API.md)
**Central orchestration and coordination**
- 34,993 lines of code
- Entry point for system operations
- Service lifecycle management
- Configuration management

#### [EUREKA](services/eureka_API.md)
**Code analysis and discovery**
- 17,951 lines of code
- Static code analysis
- Vulnerability detection
- Dependency mapping

#### [ORACULO](services/oraculo_API.md)
**Risk assessment and prediction**
- 1,609 lines of code
- Security risk scoring
- Threat intelligence
- Predictive analytics

#### [PENELOPE](services/penelope_API.md)
**Self-healing and auto-remediation**
- 8,538 lines of code
- Automatic issue resolution
- System recovery
- Adaptive responses

#### [MABA](services/maba_API.md)
**Knowledge graph and behavior analysis**
- 7,734 lines of code
- Neo4j-based knowledge graphs
- Behavioral pattern detection
- Attack vector analysis

#### [NIS](services/nis_API.md)
**Network intrusion detection**
- 7,085 lines of code
- Real-time threat monitoring
- Anomaly detection
- Network security

#### [ORCHESTRATOR](services/orchestrator_API.md)
**Workflow coordination**
- 481 lines of code
- Multi-service workflows
- Task scheduling
- Resource management

#### [DLQ_MONITOR](services/dlq_monitor_API.md)
**Dead letter queue monitoring**
- 407 lines of code
- Failed message tracking
- Retry logic
- Error analytics

---

## 📚 Indexes

### [Class Index](indexes/CLASS_INDEX.md)
Complete alphabetical listing of all 2,278 classes in the system.

**Organized by:**
- Alphabetical order
- By service
- With file locations

### [Function Index](indexes/FUNCTION_INDEX.md)
Complete alphabetical listing of all 1,177 public functions.

**Organized by:**
- Alphabetical order
- By service
- With file locations

---

## 🎯 How to Use This Section

### Finding a Specific Service
Navigate to `services/<service-name>_API.md` for:
- Service overview and statistics
- API endpoints (if any)
- Classes and methods
- Data models
- Configuration
- Dependencies

### Finding a Class or Function
Use the indexes:
1. Open `indexes/CLASS_INDEX.md` or `indexes/FUNCTION_INDEX.md`
2. Search (Ctrl+F) for the name
3. See file location and service
4. Navigate to service API doc for details

### Understanding Service APIs
Each service API document includes:
- **Overview** - Purpose, statistics, entry point
- **Endpoints** - HTTP endpoints (if REST API)
- **Classes** - All classes with methods
- **Data Models** - Pydantic models, schemas
- **Configuration** - Environment variables
- **Dependencies** - Internal and external

---

## 💡 Tips

- **For integration:** Check service endpoints and data models
- **For development:** Review classes and methods
- **For debugging:** Check dependencies and configuration
- **For architecture:** See how services expose functionality

---

**[← Back to Main](../README.md)** | **[Next: Architecture →](../02-ARCHITECTURE/)**
