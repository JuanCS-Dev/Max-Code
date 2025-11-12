#!/bin/bash
# Stop all MAXIMUS services
# Constitutional AI v3.0 - FASE 0.3

set -e

echo "🛑 Stopping MAXIMUS Services..."

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    echo "💡 Tip: Run from project root directory"
    exit 1
fi

# Stop and remove containers
docker compose down

echo ""
echo "✅ Services stopped and containers removed"
echo ""
echo "📝 Note: Docker volumes and networks preserved"
echo "🧹 To clean everything: docker compose down -v"
echo ""
