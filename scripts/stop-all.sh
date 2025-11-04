#!/bin/bash
# MAXIMUS AI - Stop All Services

PROJECT_ROOT="/media/juan/DATA1/projects/MAXIMUS AI"
cd "$PROJECT_ROOT"

echo "🛑 Stopping MAXIMUS AI Stack"
echo "================================================"
echo ""

docker-compose down

echo ""
echo "✅ All services stopped"
echo ""
echo "To remove volumes as well (⚠️  deletes data):"
echo "  docker-compose down -v"
echo ""
