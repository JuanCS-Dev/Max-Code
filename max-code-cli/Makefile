# Makefile for Max-Code CLI
# Boris Cherny Standard: Make the right thing easy to do
# "If it's hard to test, you won't test it"

.PHONY: help install install-dev test test-unit test-integration coverage lint format type-check security audit clean all ci

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Max-Code CLI - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================
# INSTALLATION
# ============================================================

install: ## Install production dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r requirements.secure.txt
	@echo "✅ Development environment ready"

install-hooks: ## Install pre-commit hooks
	pip install pre-commit
	cd .. && pre-commit install
	@echo "✅ Pre-commit hooks installed"

# ============================================================
# TESTING
# ============================================================

test: ## Run all tests with coverage
	pytest tests/ \
		--cov=sdk \
		--cov=cli \
		--cov=config \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=80 \
		-v

test-unit: ## Run only unit tests
	pytest tests/unit/ -v --tb=short

test-integration: ## Run only integration tests
	pytest tests/integration/ -v --tb=short || echo "⚠️  No integration tests yet"

test-fast: ## Run tests without coverage (faster)
	pytest tests/ -v --tb=short

# ============================================================
# COVERAGE
# ============================================================

coverage: ## Generate coverage report
	pytest tests/ \
		--cov=sdk \
		--cov=cli \
		--cov=config \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-report=xml \
		--cov-report=json
	@echo ""
	@echo "📊 Coverage reports generated:"
	@echo "  - Terminal: see above"
	@echo "  - HTML: htmlcov/index.html"
	@echo "  - XML: coverage.xml"
	@echo "  - JSON: coverage.json"

coverage-html: coverage ## Open coverage HTML report in browser
	@python -m webbrowser -t htmlcov/index.html || echo "Open htmlcov/index.html in your browser"

# ============================================================
# CODE QUALITY
# ============================================================

lint: ## Run all linters
	@echo "🔍 Running flake8..."
	flake8 sdk/ cli/ config/ --count --statistics
	@echo ""
	@echo "🔍 Checking imports with isort..."
	isort --check-only --diff sdk/ cli/ config/ tests/
	@echo ""
	@echo "✅ Linting complete"

format: ## Format code with black and isort
	@echo "🎨 Formatting code with black..."
	black sdk/ cli/ config/ tests/
	@echo ""
	@echo "🎨 Sorting imports with isort..."
	isort sdk/ cli/ config/ tests/
	@echo ""
	@echo "✅ Code formatted"

format-check: ## Check if code is formatted correctly
	black --check --diff sdk/ cli/ config/ tests/
	isort --check-only --diff sdk/ cli/ config/ tests/

type-check: ## Run type checking with mypy
	@echo "🔍 Type checking with mypy..."
	mypy sdk/ cli/ config/ --config-file=mypy.ini
	@echo "✅ Type check complete"

# ============================================================
# SECURITY
# ============================================================

security: ## Run security scans
	@echo "🔒 Running pip-audit..."
	pip-audit --desc || true
	@echo ""
	@echo "🔒 Running bandit..."
	bandit -r sdk/ cli/ config/ -ll -i
	@echo ""
	@echo "✅ Security scan complete"

security-full: ## Run comprehensive security scan
	@echo "🔒 Running pip-audit (detailed)..."
	pip-audit --desc --fix-dry-run || true
	@echo ""
	@echo "🔒 Running bandit (verbose)..."
	bandit -r sdk/ cli/ config/ -f json -o bandit-report.json
	bandit -r sdk/ cli/ config/
	@echo ""
	@echo "📊 Security report: bandit-report.json"

# ============================================================
# AUDIT
# ============================================================

audit: ## Run comprehensive audit script
	@echo "📋 Running audit script..."
	chmod +x audit-cli.sh
	./audit-cli.sh
	@echo ""
	@echo "📊 Audit report generated: AUDIT_REPORT_*.md"

# ============================================================
# CLEANUP
# ============================================================

clean: ## Clean up build artifacts and cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	find . -type f -name "coverage.json" -delete 2>/dev/null || true
	find . -type f -name "bandit-report.json" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================
# COMBINED TARGETS
# ============================================================

all: format lint type-check test ## Run all quality checks
	@echo ""
	@echo "🎉 All checks passed!"

ci: format-check lint type-check test security ## Run CI checks locally
	@echo ""
	@echo "🎉 CI checks complete!"

pre-push: clean all ## Run before pushing (recommended)
	@echo ""
	@echo "✅ Ready to push!"

# ============================================================
# DEVELOPMENT
# ============================================================

dev-setup: install-dev install-hooks ## Complete development setup
	@echo ""
	@echo "🎉 Development environment ready!"
	@echo ""
	@echo "Quick start:"
	@echo "  make test          - Run tests"
	@echo "  make coverage      - Generate coverage report"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make pre-push      - Run all checks before pushing"
