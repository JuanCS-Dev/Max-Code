#!/bin/bash
# Configure Kong API Gateway for MAXIMUS services
set -e

KONG_ADMIN="http://localhost:8001"

echo "🔧 Configuring Kong API Gateway..."

# 1. Create MAXIMUS Core Service
curl -i -X POST $KONG_ADMIN/services \
  --data name=maximus-core \
  --data url=http://host.docker.internal:8100

# 2. Add route for Core
curl -i -X POST $KONG_ADMIN/services/maximus-core/routes \
  --data "paths[]=/api/consciousness" \
  --data "paths[]=/api/v1/governance" \
  --data "paths[]=/query" \
  --data name=maximus-core-route

# 3. Create PENELOPE Service
curl -i -X POST $KONG_ADMIN/services \
  --data name=penelope \
  --data url=http://host.docker.internal:8154

# 4. Add route for PENELOPE
curl -i -X POST $KONG_ADMIN/services/penelope/routes \
  --data "paths[]=/api/v1/healing" \
  --data "paths[]=/api/v1/penelope" \
  --data name=penelope-route

# 5. Enable Rate Limiting (100 req/min per IP)
curl -i -X POST $KONG_ADMIN/services/maximus-core/plugins \
  --data name=rate-limiting \
  --data config.minute=100 \
  --data config.policy=local

curl -i -X POST $KONG_ADMIN/services/penelope/plugins \
  --data name=rate-limiting \
  --data config.minute=100 \
  --data config.policy=local

# 6. Enable API Key Authentication
curl -i -X POST $KONG_ADMIN/services/maximus-core/plugins \
  --data name=key-auth \
  --data config.key_names=X-API-Key

curl -i -X POST $KONG_ADMIN/services/penelope/plugins \
  --data name=key-auth \
  --data config.key_names=X-API-Key

# 7. Enable CORS
curl -i -X POST $KONG_ADMIN/services/maximus-core/plugins \
  --data name=cors \
  --data config.origins="*" \
  --data config.methods=GET,POST,PUT,DELETE \
  --data config.headers=Accept,Content-Type,X-API-Key \
  --data config.max_age=3600

# 8. Enable Request/Response Logging
curl -i -X POST $KONG_ADMIN/services/maximus-core/plugins \
  --data name=file-log \
  --data config.path=/tmp/kong-access.log

# 9. Enable Prometheus Metrics
curl -i -X POST $KONG_ADMIN/plugins \
  --data name=prometheus

# 10. Create Consumer (API Key)
curl -i -X POST $KONG_ADMIN/consumers \
  --data username=maximus-cli

curl -i -X POST $KONG_ADMIN/consumers/maximus-cli/key-auth \
  --data key=maximus_production_key_2024

echo ""
echo "✅ Kong configured!"
echo ""
echo "📋 Test Gateway:"
echo "   curl http://localhost:8000/api/consciousness/state \\"
echo "     -H 'X-API-Key: maximus_production_key_2024'"
echo ""
echo "📊 Kong Admin: http://localhost:8001"
echo "📊 Konga UI: http://localhost:1337"
echo "📊 Prometheus: http://localhost:8000/metrics"
