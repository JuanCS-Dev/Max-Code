#!/bin/bash
# Check health of all MAXIMUS services
# Constitutional AI v3.0 - FASE 0.3

set -e

services=(
    "8150:MAXIMUS Core"
    "8154:PENELOPE"
    "8152:MABA"
    "8153:NIS"
    "8155:Eureka"
    "8157:DLQ"
    "8027:Orchestrator"
    "8026:Oráculo"
)

echo "🏥 MAXIMUS Services Health Check"
echo "=================================="
echo ""

healthy_count=0
total_count=0

for service in "${services[@]}"; do
    IFS=':' read -r port name <<< "$service"
    total_count=$((total_count + 1))

    if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ $name (port $port) - UP"
        healthy_count=$((healthy_count + 1))
    else
        echo "❌ $name (port $port) - DOWN"
    fi
done

echo ""
echo "📊 Summary: $healthy_count/$total_count services healthy"
echo ""

if [ "$healthy_count" -eq "$total_count" ]; then
    echo "✅ All services operational!"
    exit 0
elif [ "$healthy_count" -gt 0 ]; then
    echo "⚠️  Partial outage - some services down"
    exit 1
else
    echo "❌ Total outage - no services responding"
    exit 2
fi
