# MAX-CODE-CLI - Development Guide

**For contributors and developers**

---

## Project Structure

```
max-code-cli/
├── agents/          # 9 specialized AI agents
├── cli/             # Command-line interface
├── core/            # Core functionality (109 files)
├── ui/              # UI components (29 files)
├── integration/     # Backend clients (8 files)
├── sdk/             # Agent development kit
├── tests/           # Test suite (42 files)
└── docs/            # This documentation
```

## Development Setup

```bash
# Clone and setup
cd max-code-cli
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (if exists)
pip install -r requirements-dev.txt
```

## Running Tests

```bash
# All tests
pytest tests/

# Specific test
pytest tests/test_agents.py

# With coverage
pytest --cov=. tests/
```

## Creating a New Agent

See [SDK Reference](../sdk/SDK_REFERENCE.md) for the complete template.

## Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Add tests for new features
- Update documentation

## Architecture Principles

1. **Constitutional AI** - All agents validate against P1-P6
2. **Padrão Pagani** - Real, Complete, Usable
3. **DDD & SOLID** - Domain-driven design
4. **Biomimetic** - Inspired by biological systems

