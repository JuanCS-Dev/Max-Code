# MAXIMUS Data Persistence

Production-ready data persistence with PostgreSQL + Redis.

## Quick Start

```bash
cd /media/juan/DATA2/projects/MAXIMUS\ AI/max-code-cli/persistence
docker-compose up -d
```

## Services

- **PostgreSQL**: Port 5432 (maximus/maximus2024)
- **Redis**: Port 6379 (maximus2024)

## Schema

- `decisions` - HITL governance decisions
- `operator_sessions` - Operator authentication sessions
- `esgt_events` - Consciousness events
- `healing_patches` - PENELOPE patches
- `consciousness_snapshots` - Arousal/TIG snapshots

## Usage

```python
from persistence.db_client import get_db, get_cache

# Database
db = await get_db()
decisions = await db.fetch("SELECT * FROM pending_decisions")

# Cache
cache = await get_cache()
await cache.set("arousal", "0.75", ttl=60)
```

## Dependencies

```bash
pip install asyncpg redis[asyncio]
```
