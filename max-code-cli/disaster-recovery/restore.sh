#!/bin/bash
# MAXIMUS Disaster Recovery - Restore Script
# P0-008: Production-Ready Restore

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file.tar.gz>"
    exit 1
fi

BACKUP_FILE="$1"
BACKUP_DIR="/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/backups"
RESTORE_DIR="/tmp/maximus_restore_$$"

echo "🔄 MAXIMUS Restore Started"
echo "   Backup: $BACKUP_FILE"

# 1. Extract backup
echo "1️⃣ Extracting backup..."
mkdir -p "$RESTORE_DIR"
tar xzf "$BACKUP_DIR/$BACKUP_FILE" -C "$RESTORE_DIR"
BACKUP_NAME=$(basename "$BACKUP_FILE" .tar.gz)
cd "$RESTORE_DIR/$BACKUP_NAME"

# 2. Stop services
echo "2️⃣ Stopping services..."
cd "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"
docker compose -f persistence/docker-compose.yml down
docker compose -f observability/docker-compose.yml down

# 3. Remove volumes
echo "3️⃣ Cleaning volumes..."
docker volume rm persistence_postgres-data persistence_redis-data observability_prometheus-data observability_grafana-data 2>/dev/null || true

# 4. Start services
echo "4️⃣ Starting services..."
docker compose -f persistence/docker-compose.yml up -d
docker compose -f observability/docker-compose.yml up -d

echo "   Waiting for services (10s)..."
sleep 10

# 5. Restore PostgreSQL
echo "5️⃣ Restoring PostgreSQL..."
cat "$RESTORE_DIR/$BACKUP_NAME/postgres.sql" | docker exec -i maximus-postgres psql -U maximus
echo "   ✅ PostgreSQL restored"

# 6. Restore Redis
echo "6️⃣ Restoring Redis..."
docker cp "$RESTORE_DIR/$BACKUP_NAME/redis.rdb" maximus-redis:/data/dump.rdb
docker restart maximus-redis
echo "   ✅ Redis restored"

# 7. Restore Prometheus
echo "7️⃣ Restoring Prometheus..."
docker cp "$RESTORE_DIR/$BACKUP_NAME/prometheus.tar.gz" maximus-prometheus:/tmp/
docker exec maximus-prometheus tar xzf /tmp/prometheus.tar.gz -C /prometheus
docker restart maximus-prometheus
echo "   ✅ Prometheus restored"

# 8. Restore Grafana
echo "8️⃣ Restoring Grafana..."
docker cp "$RESTORE_DIR/$BACKUP_NAME/grafana.tar.gz" maximus-grafana:/tmp/
docker exec maximus-grafana tar xzf /tmp/grafana.tar.gz -C /var/lib/grafana
docker restart maximus-grafana
echo "   ✅ Grafana restored"

# 9. Cleanup
echo "9️⃣ Cleaning up..."
rm -rf "$RESTORE_DIR"

echo ""
echo "✅ Restore Complete!"
echo "   All services are running with restored data"
echo ""
echo "📋 Verify:"
echo "   docker ps | grep maximus"
echo "   psql -h localhost -U maximus -d maximus"
