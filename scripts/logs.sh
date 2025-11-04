#!/bin/bash
# MAXIMUS AI - Logs Viewer
# View logs for all or specific services

PROJECT_ROOT="/media/juan/DATA1/projects/MAXIMUS AI"
cd "$PROJECT_ROOT"

SERVICE=$1

if [ -z "$SERVICE" ]; then
    echo "📜 MAXIMUS AI - Logs (All Services)"
    echo "================================================"
    echo ""
    docker-compose logs --tail=100 -f
else
    echo "📜 MAXIMUS AI - Logs: $SERVICE"
    echo "================================================"
    echo ""
    docker-compose logs --tail=100 -f "$SERVICE"
fi
