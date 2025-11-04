#!/bin/bash
# MAXIMUS AI - Setup Script
# Initializes the standalone Maximus AI environment

set -e

PROJECT_ROOT="/media/juan/DATA1/projects/MAXIMUS AI"
cd "$PROJECT_ROOT"

echo "🚀 MAXIMUS AI - Setup"
echo "================================================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi
echo "✓ Docker found: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose v2+."
    exit 1
fi
echo "✓ Docker Compose found"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python found: $PYTHON_VERSION"

echo ""
echo "================================================"
echo "📝 Configuration"
echo "================================================"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   - ANTHROPIC_API_KEY (required for Core, PENELOPE, MABA, NIS)"
    echo "   - GEMINI_API_KEY (required for Oráculo)"
    echo ""
    read -p "Press ENTER to open .env in nano editor (or Ctrl+C to edit manually later)..."
    nano .env || true
else
    echo "✓ .env file already exists"
fi

echo ""
echo "================================================"
echo "🐳 Docker Setup"
echo "================================================"
echo ""

# Pull base images
echo "Pulling Docker base images..."
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull neo4j:5.28-community
docker pull prom/prometheus:v2.47.0
docker pull grafana/grafana:10.1.0
docker pull grafana/loki:2.9.0

echo ""
echo "================================================"
echo "🗄️  Database Initialization"
echo "================================================"
echo ""

# Start only database services first
echo "Starting database services..."
docker-compose up -d postgres redis neo4j

echo "Waiting for databases to be ready..."
sleep 10

# Wait for PostgreSQL
echo -n "Waiting for PostgreSQL... "
until docker-compose exec -T postgres pg_isready -U maximus &> /dev/null; do
    echo -n "."
    sleep 2
done
echo " ✓"

# Wait for Redis
echo -n "Waiting for Redis... "
until docker-compose exec -T redis redis-cli ping &> /dev/null; do
    echo -n "."
    sleep 2
done
echo " ✓"

# Wait for Neo4j
echo -n "Waiting for Neo4j... "
sleep 15  # Neo4j takes longer to start
echo " ✓"

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Verify your .env has valid API keys"
echo "  2. Start all services: ./scripts/run-all.sh"
echo "  3. Check health: ./scripts/health-check.sh"
echo "  4. View logs: ./scripts/logs.sh"
echo ""
echo "Access points:"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo "  - Prometheus: http://localhost:9090"
echo "  - Neo4j Browser: http://localhost:7474"
echo ""
