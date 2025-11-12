#!/bin/bash
# Wait for all MAXIMUS services to be healthy
# Constitutional AI v3.0 - FASE 0.3

set -e

services=(
    "http://localhost:8150/health:maximus-core"
    "http://localhost:8154/health:penelope"
    "http://localhost:8152/health:maba"
    "http://localhost:8153/health:nis"
    "http://localhost:8155/health:eureka"
    "http://localhost:8157/health:dlq"
    "http://localhost:8027/health:orchestrator"
    "http://localhost:8026/health:oraculo"
)

echo "⏳ Waiting for MAXIMUS services to be healthy..."
echo ""

all_healthy=true

for service in "${services[@]}"; do
    IFS=':' read -r url name <<< "$service"

    echo -n "  $name..."

    max_attempts=30
    attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo " ✅ UP"
            break
        fi

        attempt=$((attempt + 1))

        if [ $attempt -eq $max_attempts ]; then
            echo " ❌ TIMEOUT"
            all_healthy=false
            break
        fi

        sleep 2
        echo -n "."
    done
done

echo ""

if [ "$all_healthy" = true ]; then
    echo "✅ All services healthy!"
    echo ""
    echo "🎯 Next steps:"
    echo "   - Run tests: pytest tests/integration/ -v -m integration"
    echo "   - Start CLI: max-code"
    exit 0
else
    echo "❌ Some services failed to start"
    echo ""
    echo "🐛 Troubleshooting:"
    echo "   - Check logs: docker compose logs -f"
    echo "   - Check status: docker compose ps"
    echo "   - View errors: docker compose logs <service-name>"
    exit 1
fi
