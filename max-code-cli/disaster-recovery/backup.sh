#!/bin/bash
# MAXIMUS Disaster Recovery - Backup Script
# P0-008: Production-Ready Backup

set -e

BACKUP_DIR="/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="maximus_backup_${TIMESTAMP}"

mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

echo "🔐 MAXIMUS Backup Started: $TIMESTAMP"

# 1. PostgreSQL Backup
echo "1️⃣ Backing up PostgreSQL..."
docker exec maximus-postgres pg_dumpall -U maximus > "$BACKUP_DIR/$BACKUP_NAME/postgres.sql"
echo "   ✅ PostgreSQL: $(du -h "$BACKUP_DIR/$BACKUP_NAME/postgres.sql" | cut -f1)"

# 2. Redis Backup
echo "2️⃣ Backing up Redis..."
docker exec maximus-redis redis-cli -a maximus2024 --no-auth-warning SAVE
docker cp maximus-redis:/data/dump.rdb "$BACKUP_DIR/$BACKUP_NAME/redis.rdb"
echo "   ✅ Redis: $(du -h "$BACKUP_DIR/$BACKUP_NAME/redis.rdb" | cut -f1)"

# 3. Prometheus Data
echo "3️⃣ Backing up Prometheus..."
docker exec maximus-prometheus tar czf /tmp/prometheus.tar.gz -C /prometheus .
docker cp maximus-prometheus:/tmp/prometheus.tar.gz "$BACKUP_DIR/$BACKUP_NAME/"
echo "   ✅ Prometheus: $(du -h "$BACKUP_DIR/$BACKUP_NAME/prometheus.tar.gz" | cut -f1)"

# 4. Grafana Data
echo "4️⃣ Backing up Grafana..."
docker exec maximus-grafana tar czf /tmp/grafana.tar.gz -C /var/lib/grafana .
docker cp maximus-grafana:/tmp/grafana.tar.gz "$BACKUP_DIR/$BACKUP_NAME/"
echo "   ✅ Grafana: $(du -h "$BACKUP_DIR/$BACKUP_NAME/grafana.tar.gz" | cut -f1)"

# 5. Create metadata
cat > "$BACKUP_DIR/$BACKUP_NAME/metadata.json" <<EOF
{
  "backup_name": "$BACKUP_NAME",
  "timestamp": "$TIMESTAMP",
  "version": "1.0",
  "components": ["postgres", "redis", "prometheus", "grafana"],
  "hostname": "$(hostname)",
  "user": "$(whoami)"
}
EOF

# 6. Compress everything
echo "5️⃣ Compressing backup..."
cd "$BACKUP_DIR"
tar czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"

FINAL_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
echo ""
echo "✅ Backup Complete!"
echo "   File: $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
echo "   Size: $FINAL_SIZE"
echo ""
echo "📋 Restore command:"
echo "   ./disaster-recovery/restore.sh ${BACKUP_NAME}.tar.gz"
