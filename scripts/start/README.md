# Service Startup Scripts

Helper scripts for starting individual MAXIMUS services locally during development.

## Available Scripts

### start_core.sh
Starts the Maximus Core consciousness service (port 8150).

```bash
./scripts/start/start_core.sh
```

### start_penelope.sh
Starts the PENELOPE Christian healing service (port 8151).

```bash
./scripts/start/start_penelope.sh
```

## Usage

These scripts are convenience wrappers for local development. For production deployment, use:

```bash
# Full stack with Docker Compose
docker-compose up -d

# Individual service
cd services/penelope
python main.py
```

## Requirements

- Python 3.11+
- Virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)
- Environment variables configured (`.env` file)

## See Also

- [Main README](../../README.md) - Full documentation
- [Services Documentation](../../docs/services/) - Service-specific docs
- [Development Guide](../../docs/guides/) - Development workflows

---

**Last Updated:** 2025-11-14
