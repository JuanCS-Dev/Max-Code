# MAXIMUS Grafana Dashboards

**Created**: 2025-11-10
**Status**: Production-ready

---

## 📊 Available Dashboards

### 1. MAXIMUS Services Overview (`maximus-services.json`)
**UID**: `maximus-services`
**Purpose**: Monitor all MAXIMUS microservices health and performance

**Metrics**:
- Request rate (req/s)
- Response time (P95, P99)
- Total requests
- Error rate
- Active services count
- Average response time
- Service health status table

**Alerts**:
- Error rate > 5%
- Response time P95 > 1s

---

### 2. Database & Cache Metrics (`database-metrics.json`)
**UID**: `maximus-database`
**Purpose**: Monitor PostgreSQL and Redis performance

**Metrics**:

**PostgreSQL**:
- Query rate (rows returned/fetched per second)
- Active connections
- Database size
- Connection pool utilization

**Redis**:
- Cache hit rate %
- Memory usage
- Total keys

**Alerts**:
- Connection pool > 95%
- Cache hit rate < 50%

---

### 3. Consciousness Metrics (`consciousness-metrics.json`)
**UID**: `maximus-consciousness`
**Purpose**: Monitor MAXIMUS consciousness state and arousal

**Metrics**:
- Arousal level over time (0.0-1.0)
- Current arousal (real-time)
- ESGT events count (1h)
- System health gauge
- Consciousness snapshots (24h)
- Average arousal (24h)
- Recent ESGT events table

**Alerts**:
- Arousal level > 0.8 (High Arousal)

---

## 🚀 Import Dashboards

### Option 1: Grafana UI (Manual)
1. Open Grafana: http://localhost:3002
2. Login (admin/maximus2024)
3. Go to: Dashboards → Import
4. Upload JSON file or paste content
5. Select Prometheus datasource
6. Click "Import"

### Option 2: API (Automated)
```bash
# Import all dashboards
for dashboard in *.json; do
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -d @"$dashboard" \
    http://localhost:3002/api/dashboards/db
done
```

### Option 3: Provisioning (Recommended)
Add to `observability/docker-compose.yml`:

```yaml
grafana:
  volumes:
    - ./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
    - ./grafana/datasources:/etc/grafana/provisioning/datasources:ro
```

---

## 📈 Dashboard Features

### Common Features (All Dashboards)
- ✅ Auto-refresh (30s default)
- ✅ Time range selector
- ✅ Variable templating
- ✅ Alert rules
- ✅ Export/share links
- ✅ Mobile-responsive

### Visualization Types
- **Graph**: Time-series line charts
- **Stat**: Single value with trend
- **Gauge**: Radial gauge with thresholds
- **Table**: Sortable data tables

---

## 🔗 Prometheus Queries

### Service Metrics
```promql
# Request rate
rate(http_requests_total{job="maximus"}[5m])

# Response time P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / 
sum(rate(http_requests_total[5m])) * 100
```

### Database Metrics
```promql
# PostgreSQL query rate
rate(pg_stat_database_tup_returned{datname="maximus"}[5m])

# Redis hit rate
rate(redis_keyspace_hits_total[5m]) / 
(rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m])) * 100
```

### Consciousness Metrics
```promql
# Arousal level
maximus_arousal_level

# ESGT events (1h)
increase(maximus_esgt_events_total[1h])

# Average arousal (24h)
avg_over_time(maximus_arousal_level[24h])
```

---

## 🎨 Color Schemes

### Thresholds
- **Green**: Healthy (0-79%)
- **Yellow**: Warning (80-94%)
- **Red**: Critical (95-100%)

### Service Status
- **Green (UP)**: Service responding
- **Red (DOWN)**: Service not responding

---

## 🔔 Alert Configuration

### Email Notifications
1. Go to: Alerting → Contact points
2. Add email address
3. Test notification

### Slack Integration
1. Create Slack webhook
2. Add to Contact points
3. Select dashboards to alert

---

## 📊 Expected Baseline Metrics

### Normal Operation
- Request rate: 10-100 req/s
- Response time P95: 50-150ms
- Error rate: < 1%
- Active services: 2/2 (Core + PENELOPE)
- Cache hit rate: 70-90%
- Arousal level: 0.3-0.6

### Under Load
- Request rate: 100-500 req/s
- Response time P95: 150-300ms
- Error rate: < 3%
- Arousal level: 0.6-0.8

### Critical
- Error rate: > 5%
- Response time P95: > 1s
- Arousal level: > 0.8

---

## 🛠️ Customization

### Add Custom Panel
1. Click "+ Add panel"
2. Select visualization type
3. Write PromQL query
4. Configure legend and thresholds
5. Save dashboard

### Variables
Add dashboard variables for:
- `$service` - Filter by service
- `$namespace` - Filter by namespace
- `$timerange` - Custom time ranges

---

## 📚 Resources

- [Grafana Docs](https://grafana.com/docs/)
- [Prometheus Query Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [PromQL Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)

---

**Soli Deo Gloria** 🙏
