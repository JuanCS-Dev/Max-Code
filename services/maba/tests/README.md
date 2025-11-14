# MABA Test Suite

**Day 4: Complete test coverage for MABA service**

## Coverage Target

- **Statements**: 85%+
- **Branches**: 80%+
- **Functions**: 90%+
- **Lines**: 85%+

## Test Structure

```
tests/
├── unit/              # 70% - Fast, isolated tests
│   ├── test_models.py         # Database models
│   ├── test_database.py       # Database functions
│   ├── test_browser_controller.py # Browser automation
│   └── test_cognitive_map.py  # Learning service
├── integration/       # 20% - Component interaction
│   ├── test_api_routes.py     # API endpoints
│   └── test_learning_flow.py  # End-to-end learning
├── e2e/              # 10% - Full workflows
│   └── test_full_workflows.py # Complete user journeys
└── performance/      # Benchmarks
    └── test_benchmarks.py     # Performance tests
```

## Running Tests

### All tests with coverage
```bash
pytest

# With detailed output
pytest -v

# With coverage HTML report
pytest --cov-report=html
open htmlcov/index.html
```

### By category
```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests
pytest -m integration

# E2E tests (requires running services)
pytest -m e2e

# Performance benchmarks
pytest -m performance
```

### Parallel execution
```bash
# Run tests in parallel for speed
pytest -n auto

# Run 4 workers
pytest -n 4
```

### Specific tests
```bash
# Single file
pytest tests/unit/test_models.py

# Single class
pytest tests/unit/test_models.py::TestBrowserSession

# Single test
pytest tests/unit/test_models.py::TestBrowserSession::test_create_browser_session

# By keyword
pytest -k "learning"
```

## Test Markers

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.performance` - Performance benchmarks
- `@pytest.mark.slow` - Slow tests (skip with `-m "not slow"`)
- `@pytest.mark.database` - Tests requiring database
- `@pytest.mark.browser` - Tests requiring browser/Playwright

## Fixtures

See `conftest.py` for available fixtures:

- **Database**: `db_session`, `db_with_sample_data`
- **Browser**: `mock_browser`, `mock_browser_controller`
- **API**: `test_client`, `authenticated_client`
- **Cognitive Map**: `cognitive_map_service`
- **Test Data**: `sample_urls`, `sample_selectors`, `faker_instance`

## Writing Tests

### Unit Test Example
```python
@pytest.mark.unit
@pytest.mark.database
async def test_create_page(db_session):
    page = CognitiveMapPage(
        url="https://test.com",
        url_hash=CognitiveMapPage.hash_url("https://test.com"),
        domain="test.com",
    )
    db_session.add(page)
    await db_session.commit()
    
    assert page.id is not None
```

### Integration Test Example
```python
@pytest.mark.integration
async def test_learning_flow(db_session, cognitive_map_service):
    action = BrowserAction(...)
    await cognitive_map_service.learn_from_action(action)
    
    recommendations = await cognitive_map_service.recommend_selector(...)
    assert len(recommendations) > 0
```

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Manual workflow dispatch

### GitHub Actions
```yaml
- name: Run tests
  run: pytest --cov --cov-fail-under=85
```

## Coverage Reports

After running tests, view coverage:

```bash
# Terminal report
pytest --cov-report=term-missing

# HTML report
pytest --cov-report=html
open htmlcov/index.html

# XML report (for CI)
pytest --cov-report=xml
```

## Performance Benchmarks

Run performance tests:

```bash
pytest -m performance -v

# With detailed timing
pytest -m performance --durations=10
```

Expected performance:
- DB queries: < 100ms
- Cognitive map learning: < 500ms
- API requests: < 200ms
- Browser navigation: < 5s
- Browser clicks: < 1s

## Troubleshooting

### Import Errors
```bash
# Ensure PYTHONPATH includes services/maba
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Errors
Tests use in-memory SQLite by default. No setup required.

### Async Warnings
Use `pytest-asyncio` markers:
```python
@pytest.mark.asyncio
async def test_async_function():
    ...
```

### Slow Tests
Skip slow tests during development:
```bash
pytest -m "not slow"
```

## Philosophy

> "If it's not tested, it doesn't work."
> 
> "Coverage is a minimum, not a target."
> 
> "Tests are executable documentation."

**Red, Green, Refactor** - in that order.
