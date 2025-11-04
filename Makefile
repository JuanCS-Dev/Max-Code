.PHONY: help setup start stop restart logs test clean

help:
	@echo "MAXIMUS AI - Makefile Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup & Initialization:"
	@echo "  make setup     - Initial setup (databases, config)"
	@echo ""
	@echo "Service Management:"
	@echo "  make start     - Start all services"
	@echo "  make stop      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View logs (all services)"
	@echo ""
	@echo "Development:"
	@echo "  make test      - Run complete test suite"
	@echo "  make clean     - Clean build artifacts"
	@echo ""
	@echo "Monitoring:"
	@echo "  make status    - Show service status"
	@echo "  make health    - Check service health"
	@echo ""

setup:
	@./scripts/setup.sh

start:
	@./scripts/run-all.sh

stop:
	@./scripts/stop-all.sh

restart: stop start

logs:
	@./scripts/logs.sh

test:
	@./scripts/test-all.sh

status:
	@docker-compose ps

health:
	@echo "Checking service health..."
	@for port in 8150 8151 8152 8153 8154 8155 8156 8157; do \
		curl -sf http://localhost:$$port/health > /dev/null && echo "✓ Port $$port - HEALTHY" || echo "✗ Port $$port - UNREACHABLE"; \
	done

clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "✅ Clean complete"
