#!/bin/bash
# Start all MAXIMUS services
# Constitutional AI v3.0 - FASE 0.3

set -e

echo "🚀 Starting MAXIMUS Services..."

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    echo "💡 Tip: Run from project root directory"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo "💡 Start Docker Desktop or Docker daemon"
    exit 1
fi

# Start services
echo "📦 Starting Docker Compose services..."
docker compose up -d

echo ""
echo "✅ Services starting in background..."
echo ""
echo "📊 Check status:  docker compose ps"
echo "📝 View logs:     docker compose logs -f"
echo "🏥 Health check:  ./scripts/health_check.sh"
echo "⏳ Wait healthy:  ./scripts/wait_for_services.sh"
echo ""
