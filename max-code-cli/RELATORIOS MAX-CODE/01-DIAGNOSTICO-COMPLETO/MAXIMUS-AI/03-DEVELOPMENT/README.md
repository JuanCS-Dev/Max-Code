# 💻 03-DEVELOPMENT - Developer Guides

**Everything you need to develop, test, and contribute to MAXIMUS AI.**

---

## 📂 Directory Structure

```
03-DEVELOPMENT/
├── setup/            # Environment setup guides
├── testing/          # Testing guides and best practices
├── contributing/     # Contribution guidelines
└── guides/           # Additional development guides
```

---

## 🚀 Getting Started

### [Local Setup Guide](setup/LOCAL_SETUP.md)
**Get your development environment running in 15 minutes**

**Covers:**
- Prerequisites and system requirements
- Installing dependencies
- Configuring environment variables
- Starting infrastructure (Docker)
- Running database migrations
- Starting services
- Verifying health checks

**Quick Start:**
```bash
# 1. Clone repository
git clone <repository-url>
cd "MAXIMUS AI"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start infrastructure
docker-compose up -d postgres redis kafka neo4j

# 4. Start a service
cd services/eureka
python main.py
```

---

## 🧪 Testing

### [Testing Guide](testing/TESTING_GUIDE.md)
**Complete guide to testing MAXIMUS services**

**Includes:**
- Test structure (874+ test files)
- Running tests (unit, integration, E2E)
- Writing tests (AAA pattern)
- Fixtures and mocking
- Coverage requirements (80%+ target)
- CI/CD integration

**Quick Commands:**
```bash
# Run all tests
pytest

# Run specific service tests
pytest services/eureka/tests/

# With coverage
pytest --cov=services --cov-report=html

# Parallel execution
pytest -n auto
```

---

## 📝 Contributing

### Guidelines
- Code standards and style guides
- Pull request process
- Code review checklist
- Commit message conventions

### Best Practices
- **DDD & SOLID** principles
- **Type hints** for all functions
- **Docstrings** for all public APIs
- **Tests** for all new features
- **Documentation** updates

---

## 🛠️ Development Tools

### Required
- **Python 3.11+**
- **Docker & Docker Compose**
- **Git**

### Recommended
- **VS Code** with Python extension
- **PyCharm Professional**
- **Postman** for API testing
- **DBeaver** for database access

### Linting & Formatting
```bash
# Format code
black .
isort .

# Lint
pylint src/
ruff check .

# Type checking
mypy src/
```

---

## 🎯 Common Development Tasks

### Adding a New Feature
1. Create feature branch
2. Write tests (TDD approach)
3. Implement feature
4. Update documentation
5. Run full test suite
6. Create pull request

### Debugging a Service
1. Check service logs
2. Verify environment variables
3. Check database connections
4. Use health endpoints
5. Review integration points

### Working with Multiple Services
1. Use Docker Compose for dependencies
2. Run services individually in terminals
3. Check service dependencies map
4. Use async messaging for decoupling

---

## 📚 Additional Guides

### Service-Specific Development
Each service has unique considerations:
- **EUREKA** - Working with code analysis engines
- **ORACULO** - Risk scoring algorithms
- **PENELOPE** - Self-healing logic
- **MABA** - Neo4j graph operations
- **NIS** - Network monitoring

### Database Development
- PostgreSQL schema management
- Redis caching strategies
- Neo4j graph modeling
- Database migrations (Alembic)

### API Development
- FastAPI best practices
- Request/response validation
- Error handling
- Authentication/Authorization

---

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -i :8150
kill -9 <PID>
```

**Database connection failed:**
```bash
docker ps | grep postgres
docker-compose restart postgres
```

**Import errors:**
```bash
pip install -r requirements.txt
# or
pip install -e .
```

**Tests failing:**
```bash
pytest -v --tb=short  # Verbose with short traceback
pytest --lf           # Run last failed
pytest -k test_name   # Run specific test
```

---

## 📊 Development Metrics

### Codebase
- **1,916 Python files**
- **497,410 lines of code**
- **8 services**
- **2,278 classes**
- **1,177 public functions**

### Testing
- **874+ test files**
- **80%+ coverage target**
- **Unit, integration, E2E tests**

---

## 🎓 Learning Resources

### Internal
- [API Reference](../01-API-REFERENCE/)
- [Architecture](../02-ARCHITECTURE/)
- [Status Reports](../05-STATUS-REPORTS/)

### External
- FastAPI documentation
- Python type hints guide
- Docker best practices
- Pytest documentation

---

**[← Back to Main](../README.md)** | **[Next: Deployment →](../04-DEPLOYMENT/)**
