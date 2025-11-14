# Contributing to Max-Code-CLI

Thank you for your interest in contributing! This project follows the **Boris Cherny Standard** for code quality.

> "If it doesn't have types, it's not production"
> — Boris Cherny

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Quality Standards](#code-quality-standards)
3. [Exception Handling Guidelines](#exception-handling-guidelines)
4. [Testing Requirements](#testing-requirements)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)

---

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- pip or uv

### Installation

```bash
# Clone the repository
git clone https://github.com/JuanCS-Dev/Max-Code.git
cd Max-Code/max-code-cli

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov=cli --cov=agents --cov-report=term

# Run specific test file
pytest tests/unit/test_exception_handling.py -v
```

---

## Code Quality Standards

### Boris Cherny Principles

This project adheres to strict code quality standards:

✅ **Type Safety Maximum**
- All public functions must have type hints
- No `Any` types without justification
- Use `Optional[T]` for nullable values

✅ **Código Limpo**
- Functions do one thing well
- Max function length: 50 lines
- Max file length: 500 lines (excluding tests)

✅ **Zero Code Smells**
- No magic numbers (use constants)
- No duplicate code (DRY principle)
- No dead code or commented-out code

✅ **Self-Documenting Code**
- Clear variable names (no `x`, `temp`, `data`)
- Docstrings for all public APIs
- Inline comments only for "why", not "what"

### Pre-commit Hooks

All code must pass pre-commit hooks before being committed:

```bash
# Run manually
pre-commit run --all-files

# Hooks include:
# - black (formatting)
# - isort (import sorting)
# - flake8 (linting)
# - mypy (type checking)
# - bare-except checker (custom)
# - trailing whitespace
# - end of file fixer
# - check yaml/json/toml
# - detect-secrets
```

---

## Exception Handling Guidelines

### ❌ NEVER Use Bare Excepts in Production Code

**BAD:**
```python
try:
    risky_operation()
except:  # ❌ FORBIDDEN
    pass
```

**GOOD:**
```python
try:
    risky_operation()
except (ValueError, TypeError) as e:  # ✅ Specific exceptions
    logger.error(f"Operation failed: {e}")
    raise
```

### Exception Hierarchy

Use specific exceptions from most to least specific:

1. **Built-in Specific:** `ValueError`, `KeyError`, `IndexError`
2. **Built-in General:** `OSError`, `RuntimeError`
3. **Custom Exceptions:** Define your own when needed
4. **Never:** `except:` or `except Exception:` (without re-raise)

### When Bare Excepts ARE Acceptable

Only in **test cleanup code**:

```python
# Test tearDown - ACCEPTABLE
def tearDown(self):
    try:
        self.temp_file.unlink()
    except:  # ✅ OK in test cleanup
        pass  # File may not exist - that's fine
```

### Exception Handling Patterns

#### 1. Fail Fast (Preferred)

```python
def process_user(user_id: str) -> User:
    """Process user - fail fast on errors."""
    if not user_id:
        raise ValueError("user_id cannot be empty")

    user = fetch_user(user_id)  # Let exceptions propagate
    return user
```

#### 2. Catch and Log

```python
def safe_process_user(user_id: str) -> Optional[User]:
    """Process user with error handling."""
    try:
        return process_user(user_id)
    except (ValueError, DatabaseError) as e:
        logger.error(f"Failed to process user {user_id}: {e}")
        return None
```

#### 3. Catch, Transform, Re-raise

```python
def api_call(endpoint: str) -> dict:
    """Make API call with error transformation."""
    try:
        response = requests.get(endpoint)
        return response.json()
    except requests.RequestException as e:
        raise APIError(f"API call failed: {e}") from e
```

### Common Exception Types by Use Case

| Use Case | Exception Type | Example |
|----------|---------------|---------|
| Invalid argument | `ValueError` | `raise ValueError("Invalid email format")` |
| Missing key | `KeyError` | `raise KeyError(f"Missing config: {key}")` |
| File not found | `FileNotFoundError` | `raise FileNotFoundError(f"File {path} not found")` |
| Permission denied | `PermissionError` | `raise PermissionError("Access denied")` |
| Network error | `OSError` | `except OSError as e: ...` |
| JSON parsing | `ValueError, TypeError` | `except (ValueError, TypeError): ...` |
| Type mismatch | `TypeError` | `raise TypeError("Expected str, got int")` |

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# ✅ GOOD: Log with context
try:
    result = parse_json(data)
except ValueError as e:
    logger.error(f"JSON parse failed for {filename}: {e}")
    raise

# ❌ BAD: Silent failure
try:
    result = parse_json(data)
except:
    pass  # Silent failure = debugging nightmare
```

---

## Testing Requirements

### Test Coverage Targets

- **Core modules:** 80%+ coverage
- **CLI commands:** 60%+ coverage
- **Agents:** 60%+ coverage
- **Overall:** 70%+ coverage

### Test Structure

```python
class TestMyFeature:
    """Test suite for MyFeature."""

    def test_normal_case(self):
        """Test: Normal successful operation."""
        result = my_feature.process("valid input")
        assert result.success is True

    def test_error_case(self):
        """Test: Invalid input raises ValueError."""
        with pytest.raises(ValueError, match="Invalid input"):
            my_feature.process("invalid input")

    def test_edge_case(self):
        """Test: Empty input handled gracefully."""
        result = my_feature.process("")
        assert result.success is False
```

### Test Naming Convention

- **Test files:** `test_<module>.py`
- **Test classes:** `Test<FeatureName>`
- **Test methods:** `test_<what_is_tested>`
- **Docstring:** One-line description starting with "Test:"

---

## Commit Guidelines

### Commit Message Format

```
type(scope): Brief description (imperative mood)

Detailed explanation if needed.
- Bullet points for multiple changes
- Explain the "why", not the "what"

Closes #123
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **refactor:** Code restructuring (no behavior change)
- **test:** Adding or fixing tests
- **docs:** Documentation changes
- **chore:** Maintenance (dependencies, configs)
- **perf:** Performance improvements

### Examples

```
feat(cli): Add --verbose flag to health command

Allows users to see detailed service health information.

- Added -v/--verbose argument
- Shows response times and error details
- Maintains backward compatibility

Closes #42
```

```
refactor(exceptions): Replace bare excepts with specific exceptions

P0 CRITICAL: Fixed 3 bare except blocks in production code.

Changes:
- core/maximus_integration/shared_client.py:162
  * Replace bare except with (ValueError, TypeError)
  * Add logging for non-JSON responses

Impact: Improved debuggability, type safety

Boris Cherny Standard: Applied ✅
```

---

## Pull Request Process

### Before Creating a PR

1. ✅ All tests pass: `pytest`
2. ✅ Coverage is adequate: `pytest --cov`
3. ✅ Pre-commit hooks pass: `pre-commit run --all-files`
4. ✅ Code is formatted: `black .`
5. ✅ Imports are sorted: `isort .`
6. ✅ No type errors: `mypy core/ cli/ agents/`

### PR Checklist

- [ ] Descriptive title and description
- [ ] Linked to relevant issue (if applicable)
- [ ] Added tests for new functionality
- [ ] Updated documentation (if needed)
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow guidelines
- [ ] All CI checks pass

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Added/updated tests
- [ ] Documentation updated
```

---

## Code Review Criteria

### What Reviewers Look For

1. **Correctness:** Does it work? Are edge cases handled?
2. **Readability:** Can I understand it in 6 months?
3. **Type Safety:** Are types specific and correct?
4. **Error Handling:** Specific exceptions, not bare excepts?
5. **Tests:** Are error paths tested?
6. **Documentation:** Is complex logic explained?
7. **Performance:** Any obvious inefficiencies?

### Review Response Time

- **Critical fixes:** Within 24 hours
- **Features:** Within 3-5 days
- **Documentation:** Within 1 week

---

## Architecture Guidelines

### Project Structure

```
max-code-cli/
├── cli/              # Command-line interface
├── core/             # Core business logic
├── agents/           # AI agents
├── sdk/              # SDK for agents
├── config/           # Configuration
├── tests/            # Test suites
├── docs/             # Documentation
└── scripts/          # Utility scripts
```

### Module Dependencies

- **cli/** → depends on **core/**, **agents/**
- **core/** → self-contained (no cli dependencies)
- **agents/** → depends on **core/**, **sdk/**
- **tests/** → can depend on anything

### Circular Dependencies

❌ **FORBIDDEN**
```python
# cli/main.py
from core.something import X

# core/something.py
from cli.main import Y  # ❌ CIRCULAR
```

---

## Questions?

- **Documentation:** See `docs/` directory
- **Examples:** See `examples/` directory
- **Issues:** https://github.com/JuanCS-Dev/Max-Code/issues
- **Discussions:** https://github.com/JuanCS-Dev/Max-Code/discussions

---

**Biblical Foundation:**

> "Tudo o que fizerem, façam de todo o coração, como para o Senhor, e não para os homens"
> (Colossenses 3:23)

**Soli Deo Gloria** 🙏
