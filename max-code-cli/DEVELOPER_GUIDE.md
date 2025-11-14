# 🚀 MAX-CODE CLI - DEVELOPER GUIDE

**Status:** Production Ready ✅  
**Standard:** Boris Cherny Engineering Excellence  
**Philosophy:** "Make the right thing easy to do"

---

## 📑 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [Development Commands](#development-commands)
3. [Interactive Shell (REPL)](#interactive-shell-repl)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Pre-commit Hooks](#pre-commit-hooks)
6. [Testing](#testing)
7. [Code Quality](#code-quality)
8. [Security](#security)
9. [Workflow Examples](#workflow-examples)

---

## 🚀 QUICK START

### One-Command Setup

```bash
cd max-code-cli
./setup-dev.sh
```

This installs everything you need:
- ✅ Production dependencies
- ✅ Development dependencies
- ✅ Pre-commit hooks
- ✅ Runs initial tests

**Time:** ~5 minutes

---

## 💻 DEVELOPMENT COMMANDS

### Via CLI (max-code dev)

```bash
# Testing
max-code dev test              # All tests with coverage
max-code dev test --unit       # Unit tests only
max-code dev test --fast       # Tests without coverage
max-code dev coverage          # Generate coverage reports

# Code Quality
max-code dev lint              # Run linters (flake8, black, isort)
max-code dev lint --fix        # Auto-fix formatting issues
max-code dev format            # Format code with black and isort
max-code dev typecheck         # Run mypy type checking

# Security
max-code dev security          # Quick security scan
max-code dev security --full   # Comprehensive security scan
max-code dev audit             # Run comprehensive audit script

# Combined
max-code dev ci                # Run all CI checks locally
max-code dev pre-push          # All checks before pushing
max-code dev stats             # Show project statistics
```

### Via Makefile

```bash
# Quick Commands
make test          # Run tests with coverage
make lint          # Check code quality
make format        # Format code
make type-check    # Run mypy
make security      # Security scan
make audit         # Comprehensive audit

# Combined
make ci            # Run CI checks locally
make pre-push      # Validate before pushing
make all           # Run all quality checks

# Setup
make dev-setup     # Complete development setup
make install       # Install production dependencies
make install-dev   # Install development dependencies
make install-hooks # Install pre-commit hooks

# Cleanup
make clean         # Remove build artifacts
```

### Via Interactive Shell (REPL)

```bash
max-code          # Start interactive shell

# Inside REPL:
/test              # Run tests
/lint --fix        # Lint and fix code
/format            # Format code
/typecheck         # Type checking
/security --full   # Security scan
/audit             # Comprehensive audit
/coverage          # Coverage reports
/ci                # CI checks
/pre-push          # Pre-push validation
```

---

## 🐚 INTERACTIVE SHELL (REPL)

### Starting the Shell

```bash
max-code
```

### Available Commands

#### Development Commands (Phase 4)
- `/test [--unit]` - Run tests with coverage
- `/lint [--fix]` - Run linters (with optional auto-fix)
- `/format` - Format code with black and isort
- `/typecheck` - Run mypy type checking
- `/security [--full]` - Security scan
- `/audit` - Comprehensive audit script
- `/coverage` - Generate coverage reports
- `/ci` - Run CI checks locally
- `/pre-push` - Validate before pushing

#### File Operations
- `/read <file>` - Read file contents
- `/write <file> <content>` - Write content to file
- `/edit <file>` - Edit file
- `/search <pattern>` - Search for pattern in files
- `/grep <pattern>` - Grep for pattern

#### Code Operations
- `/run <command>` - Run bash command
- `/bash <command>` - Execute bash command
- `/git <command>` - Git operations
- `/git-status` - Git status
- `/git-diff` - Git diff
- `/git-log` - Git log

#### Web Operations
- `/search-web <query>` - Search the web
- `/web-fetch <url>` - Fetch URL content

#### Shortcuts
- `Ctrl+P` - Command Palette
- `Ctrl+S` - SOFIA Planning
- `Ctrl+D` - DREAM Mode (critical analysis)
- `Ctrl+Q` - Quick Help
- `Ctrl+A` - Agent Dashboard

### Examples

```bash
# Run tests in REPL
/test --unit

# Fix code quality issues
/lint --fix

# Run CI checks before push
/ci

# Search for a function
/search "def calculate_total"

# Read a file
/read sdk/base_agent.py

# Git operations
/git-status
/git-diff

# Natural language
"Find all TODO comments in the code"
"Run the tests for base_agent"
"Format the code and run linters"
```

---

## 🔄 CI/CD PIPELINE

### GitHub Actions Workflow

Located at: `.github/workflows/ci.yml`

**6 Parallel Jobs:**

1. **Code Quality** - black, flake8, isort
2. **Type Checking** - mypy (strict mode)
3. **Security** - pip-audit, bandit
4. **Testing** - pytest, coverage (Python 3.11, 3.12)
5. **Audit** - audit-cli.sh
6. **Build** - package validation

### Triggers

- Push to: `main`, `develop`, `claude/**`
- Pull requests to: `main`, `develop`
- Manual dispatch

### Artifacts (30-day retention)

- Coverage reports (HTML)
- Security reports (JSON)
- Audit reports (Markdown)

### Running Locally

```bash
# Run all CI checks
max-code dev ci
# or
make ci
```

---

## 🎣 PRE-COMMIT HOOKS

### Installation

```bash
pip install pre-commit
pre-commit install
```

Or via setup:

```bash
./setup-dev.sh
# or
make install-hooks
```

### Configured Hooks (20+ checks)

**File Hygiene:**
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML syntax
- Large file detection (max 1MB)
- Merge conflict detection
- Private key detection

**Code Quality:**
- black (formatting)
- isort (import sorting)
- flake8 (linting with plugins)
- mypy (type checking - critical files only)
- pydocstyle (Google-style docstrings)

**Security:**
- bandit (security scan)

**Shell:**
- shellcheck (shell script linting)

### Manual Execution

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

---

## 🧪 TESTING

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── unit/                          # Fast, isolated tests
│   ├── test_base_agent.py        # SDK tests
│   ├── test_agent_pool.py
│   └── test_cli_helpers.py
└── integration/                   # Slower integration tests
    └── test_cli_integration.py
```

### Running Tests

```bash
# All tests with coverage
pytest

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_base_agent.py

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Coverage report
pytest --cov=sdk --cov=cli --cov=config --cov-report=html
```

### Coverage Targets

- **SDK:** 95%+
- **CLI:** 80%+
- **Config:** 80%+
- **Overall:** 80%+ (enforced in CI)

### Coverage Reports

```bash
# Generate all reports
make coverage

# View HTML report
open htmlcov/index.html
```

---

## 🎨 CODE QUALITY

### Type Safety (mypy)

**Configuration:** `mypy.ini`

```bash
# Run type checking
mypy sdk/ cli/ config/

# Or via shortcuts
make type-check
max-code dev typecheck
/typecheck  # in REPL
```

**Standards:**
- 100% type hints (SDK, config)
- Strict mode enabled
- No Any types (where possible)
- Return types required

### Formatting (black)

**Line length:** 100

```bash
# Check formatting
black --check sdk/ cli/ config/ tests/

# Format code
black sdk/ cli/ config/ tests/

# Or via shortcuts
make format
max-code dev format
/format  # in REPL
```

### Import Sorting (isort)

**Profile:** black-compatible

```bash
# Check imports
isort --check-only sdk/ cli/ config/ tests/

# Sort imports
isort sdk/ cli/ config/ tests/
```

### Linting (flake8)

**Max complexity:** 10  
**Plugins:** docstrings, bugbear, comprehensions

```bash
# Run linters
flake8 sdk/ cli/ config/

# Or via shortcuts
make lint
max-code dev lint
/lint  # in REPL

# Auto-fix formatting
max-code dev lint --fix
/lint --fix  # in REPL
```

---

## 🔒 SECURITY

### Dependency Scanning (pip-audit)

```bash
# Quick scan
pip-audit --desc

# With fix suggestions
pip-audit --desc --fix-dry-run

# Or via shortcuts
make security
max-code dev security
/security  # in REPL

# Full scan
max-code dev security --full
/security --full  # in REPL
```

### Code Security (bandit)

```bash
# Quick scan
bandit -r sdk/ cli/ config/ -ll -i

# Full scan with report
bandit -r sdk/ cli/ config/ -f json -o bandit-report.json
```

### Security Updates

**File:** `requirements.secure.txt`

Contains security-hardened versions fixing all known CVEs:

```bash
# Install secure dependencies
pip install -r requirements.secure.txt

# Verify no vulnerabilities
pip-audit --desc
```

**Current Status:** All 7 remaining CVEs have documented fix versions

---

## 🔄 WORKFLOW EXAMPLES

### Before Starting Work

```bash
# Pull latest changes
git pull origin main

# Setup environment (if first time)
./setup-dev.sh

# Or manual setup
make dev-setup
```

### During Development

```bash
# Format code frequently
make format

# Run tests
make test

# Check types
make type-check
```

### Before Committing

```bash
# Pre-commit hooks run automatically
git add .
git commit -m "feat: add new feature"

# Or run manually
pre-commit run --all-files
```

### Before Pushing

```bash
# Run all checks
make pre-push

# Or via CLI
max-code dev pre-push

# Or via REPL
/pre-push

# If all pass, push
git push origin feature-branch
```

### Creating a PR

```bash
# Run local CI
make ci

# Create PR
gh pr create --title "feat: add feature" --body "Description"

# CI will run automatically on GitHub
```

---

## 📊 PROJECT STATISTICS

```bash
# View project stats
max-code dev stats

# Or
python -c "
from pathlib import Path
py_files = list(Path('.').rglob('*.py'))
print(f'Python files: {len(py_files)}')
print(f'Total lines: {sum(1 for f in py_files for _ in open(f))}')
"
```

---

## 🎯 BORIS CHERNY COMPLIANCE

### Type Safety ✅
- **SDK:** 100% type hints
- **Config:** 100% type hints
- **CLI:** 95%+ type hints
- **mypy:** Strict mode enforced

### Testing ✅
- **SDK coverage:** 95%+
- **Overall coverage:** 80%+ (enforced)
- **Unit tests:** 20+
- **Integration tests:** 5+

### Documentation ✅
- **Google-style docstrings** (SDK)
- **Working code examples** (10+)
- **Comprehensive phase summaries** (4 phases)
- **Developer guide** (this document)

### Error Handling ✅
- **Specific exception types**
- **Structured logging** (no print statements in SDK)
- **Error context** in logs
- **Validation** in constructors

### Zero Technical Debt ✅
- **No print() statements** (SDK)
- **No broad exceptions** (critical path)
- **No untyped functions** (SDK)
- **All CVEs documented** with fix versions

---

## 🆘 TROUBLESHOOTING

### Tests Failing

```bash
# Run with verbose output
pytest -v --tb=long

# Run specific test
pytest tests/unit/test_base_agent.py::TestBaseAgent::test_agent_initialization -v

# Debug mode
pytest --pdb  # drops into debugger on failure
```

### Type Errors

```bash
# Run mypy with verbose output
mypy sdk/ --show-error-codes --pretty

# Ignore specific error
# type: ignore[error-code]
```

### Pre-commit Hook Failing

```bash
# See what failed
pre-commit run --all-files

# Fix formatting issues
black .
isort .

# Skip hooks (NOT RECOMMENDED)
git commit --no-verify
```

### Import Errors

```bash
# Ensure all dependencies installed
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Check sys.path
python -c "import sys; print('\n'.join(sys.path))"
```

---

## 📚 ADDITIONAL RESOURCES

- **Phase Summaries:**
  - `PHASE_1_SUMMARY.md` - Audit & Security
  - `PHASE_2_SUMMARY.md` - Testing & Error Handling
  - `PHASE_3_SUMMARY.md` - Documentation
  - `PHASE_4_SUMMARY.md` - CI/CD & Final Polish

- **Configuration Files:**
  - `.github/workflows/ci.yml` - CI/CD pipeline
  - `.pre-commit-config.yaml` - Pre-commit hooks
  - `.coveragerc` - Coverage configuration
  - `mypy.ini` - Type checking configuration
  - `pytest.ini` - Test configuration
  - `Makefile` - Development commands

- **Security:**
  - `requirements.secure.txt` - Security-hardened dependencies
  - `AUDIT_REPORT_COMPLETE.md` - Comprehensive audit report

---

**"Make the right thing easy to do."** - Boris Cherny

**Soli Deo Gloria** 🙏
