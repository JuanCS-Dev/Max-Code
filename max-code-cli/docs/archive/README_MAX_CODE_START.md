# 🚀 max-code-start - MAXIMUS Services Manager

**Version**: 1.0
**Created**: 2025-11-10
**Status**: Production-Ready

---

## 📖 Overview

Interactive CLI dashboard for managing MAXIMUS services. Start, stop, and monitor all max-code dependencies with a beautiful terminal UI.

---

## 🎯 Features

- ✅ **Interactive Dashboard** - Real-time service health monitoring
- ✅ **Color-coded Status** - Green (UP), Yellow (STARTING), Red (DOWN)
- ✅ **Smart Service Groups**:
  - Essential Services (Redis + PostgreSQL)
  - Full Stack (All 6 services)
- ✅ **One-command Operations** - Start/stop with single keystroke
- ✅ **Health Checks** - Automatic verification for all services

---

## 🚀 Quick Start

### Run the Manager
```bash
max-code-start
```

That's it! The script is globally accessible from anywhere.

---

## 📋 Menu Options

```
╔══════════════════════════════════════════════════════════════╗
║            MAXIMUS Services Manager v1.0                     ║
║                 Max-Code CLI Operations                      ║
╚══════════════════════════════════════════════════════════════╝

═══ Service Status ═══

● Redis Cache (6379) UP
● PostgreSQL (5432) UP
● Prometheus (9091) UP
● Grafana (3002) UP
● MABA Agent (8152) UP
● NIS Service (8153) UP

Summary: 6/6 services healthy
✓ All systems operational

═══ Menu ═══

  1) Start Essential Services (Redis + PostgreSQL)
  2) Start All Services (Full Stack)
  3) Stop All Services
  4) Refresh Dashboard
  5) Exit

Select option [1-5]:
```

---

## 🎮 Usage

### Option 1: Start Essential Services
**What it does**: Starts only Redis and PostgreSQL
**Use case**: Minimum requirements for max-code CLI to function
**Services**:
- Redis (6379) - Cache
- PostgreSQL (5432) - Database

```bash
# Select option: 1
```

### Option 2: Start All Services
**What it does**: Starts complete MAXIMUS stack
**Use case**: Full observability and all features enabled
**Services**:
- Redis (6379) - Cache
- PostgreSQL (5432) - Database
- Prometheus (9091) - Metrics
- Grafana (3002) - Dashboards
- MABA (8152) - Browser Agent
- NIS (8153) - Network Intelligence

```bash
# Select option: 2
```

### Option 3: Stop All Services
**What it does**: Gracefully stops all MAXIMUS services
**Use case**: Clean shutdown, free resources

```bash
# Select option: 3
```

### Option 4: Refresh Dashboard
**What it does**: Updates service status in real-time
**Use case**: Check current state without taking action

```bash
# Select option: 4
```

### Option 5: Exit
**What it does**: Exits the manager
**Use case**: Return to shell

---

## 🔍 Service Details

### Essential Services

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| Redis | 6379 | Cache & session storage | `redis-cli ping` |
| PostgreSQL | 5432 | Primary database | `pg_isready` |

### Full Stack Services

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| Prometheus | 9091 | Metrics collection | `/healthy` endpoint |
| Grafana | 3002 | Dashboards & alerts | `/api/health` endpoint |
| MABA | 8152 | Browser automation | `/health` endpoint |
| NIS | 8153 | Network intelligence | `/health` endpoint |

---

## 🎨 Color Legend

- 🟢 **Green (UP)**: Service is healthy and responding
- 🟡 **Yellow (STARTING)**: Service is starting up or degraded
- 🔴 **Red (DOWN)**: Service is stopped or unreachable

---

## ⚙️ Installation

The script is already installed and configured as a global command:

```bash
# Location
/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/max-code-start

# Alias in ~/.bashrc
alias max-code-start="/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/max-code-start"

# Symlink (optional)
/usr/local/bin/max-code-start → max-code-start script
```

### Manual Installation (if needed)
```bash
# Make executable
chmod +x /media/juan/DATA2/projects/MAXIMUS\ AI/max-code-cli/max-code-start

# Add alias to .bashrc
echo 'alias max-code-start="/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/max-code-start"' >> ~/.bashrc

# Reload
source ~/.bashrc
```

---

## 🐛 Troubleshooting

### Script not found
```bash
# Check if script exists
ls -la "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/max-code-start"

# Reload .bashrc
source ~/.bashrc

# Check alias
alias | grep max-code-start
```

### Services not starting
```bash
# Check Docker is running
docker ps

# Check docker-compose files
ls -la persistence/docker-compose.yml
ls -la observability/docker-compose.yml

# Manual start
docker-compose -f persistence/docker-compose.yml up -d
```

### Permission denied
```bash
# Make script executable
chmod +x "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli/max-code-start"
```

---

## 📊 Architecture

```
max-code-start
│
├── Essential Services
│   ├── Redis (6379)
│   └── PostgreSQL (5432)
│
└── Full Stack
    ├── Essential Services (above)
    ├── Prometheus (9091)
    ├── Grafana (3002)
    ├── MABA (8152)
    └── NIS (8153)
```

---

## 🔗 Related Commands

```bash
# View running containers
docker ps | grep maximus

# Check service logs
docker logs maximus-redis
docker logs maximus-postgres

# Manual service control
docker-compose -f persistence/docker-compose.yml up -d
docker-compose -f observability/docker-compose.yml up -d

# Stop individual service
docker stop maximus-redis
```

---

## 📝 Examples

### Scenario 1: Quick Development
```bash
# Start only what's needed
max-code-start
# Select: 1 (Essential Services)
```

### Scenario 2: Full Testing
```bash
# Start everything
max-code-start
# Select: 2 (All Services)
```

### Scenario 3: Clean Shutdown
```bash
# Stop all services
max-code-start
# Select: 3 (Stop All)
```

### Scenario 4: Status Check
```bash
# Just check status
max-code-start
# Select: 4 (Refresh)
# Select: 5 (Exit)
```

---

## 🚀 Performance

- **Startup Time**:
  - Essential: ~5 seconds
  - Full Stack: ~10 seconds
- **Shutdown Time**: ~3 seconds
- **Memory Usage**:
  - Essential: ~150MB
  - Full Stack: ~500MB

---

## 🔐 Security

- All services run in isolated Docker containers
- No privileged mode required
- PostgreSQL password: `maximus2024` (change in production!)
- Redis password: `maximus2024` (change in production!)
- Grafana admin: `admin/maximus2024` (change in production!)

---

## 📚 Resources

- **Main Documentation**: `docs/docs-da-integracao/00_INDEX.md`
- **Service Configs**: 
  - `persistence/docker-compose.yml`
  - `observability/docker-compose.yml`
- **Dashboards**: `observability/grafana/dashboards/`

---

## ✨ Tips

1. **Use Option 1 for daily work** - Essential services are enough for most development
2. **Use Option 2 for demos** - Full stack shows complete observability
3. **Use Option 4 regularly** - Monitor service health during development
4. **Keep terminal open** - Dashboard auto-refreshes when you return to menu

---

## 🎯 Roadmap

Future enhancements:
- [ ] Auto-restart failed services
- [ ] Custom service groups
- [ ] Export logs from dashboard
- [ ] Service dependency graph
- [ ] Historical uptime stats

---

## 📞 Support

For issues or questions:
1. Check service logs: `docker logs <container-name>`
2. Review docker-compose files
3. Verify Docker daemon is running
4. Check disk space: `df -h`

---

## 🙏 Credits

**Created with**: Padrão Pagani (100% Excellence)
**Biblical Foundation**: "Com sabedoria se edifica a casa" (Provérbios 24:3)

---

**Soli Deo Gloria** 🙏
