#!/bin/bash
# MAXIMUS AI - Run All Services
# Starts the complete Maximus AI stack

set -e

PROJECT_ROOT="/media/juan/DATA1/projects/MAXIMUS AI"
cd "$PROJECT_ROOT"

echo "🚀 Starting MAXIMUS AI Stack"
echo "================================================"
echo ""

# Start all services
echo "Starting all services..."
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 20

echo ""
echo "================================================"
echo "📊 Service Status"
echo "================================================"
echo ""

docker-compose ps

echo ""
echo "================================================"
echo "🏥 Health Checks"
echo "================================================"
echo ""

services=("maximus-core:8150" "penelope:8151" "maba:8152" "nis:8153" "orchestrator:8154" "eureka:8155" "oraculo:8156" "dlq-monitor:8157")

for service in "${services[@]}"; do
    name=$(echo $service | cut -d':' -f1)
    port=$(echo $service | cut -d':' -f2)

    if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✓ $name (port $port) - HEALTHY"
    else
        echo "⚠️ $name (port $port) - NOT READY (may still be starting...)"
    fi
done

echo ""
echo "================================================"
echo "✅ MAXIMUS AI Started!"
echo "================================================"
echo ""
echo "Access points:"
echo "  - Maximus Core: http://localhost:8150"
echo "  - PENELOPE: http://localhost:8151"
echo "  - MABA: http://localhost:8152"
echo "  - NIS (MVP): http://localhost:8153"
echo "  - Grafana: http://localhost:3000"
echo "  - Prometheus: http://localhost:9090"
echo ""
echo "Useful commands:"
echo "  - View logs: ./scripts/logs.sh [service_name]"
echo "  - Stop all: docker-compose down"
echo "  - Restart: docker-compose restart [service_name]"
echo ""
