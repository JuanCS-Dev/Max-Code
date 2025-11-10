# MAXIMUS CLI - Foundation Quick Start

**5-Minute Guide to Using Foundation Components**

---

## 🚀 SharedMaximusClient

### Basic Usage
```python
from core.maximus_integration.shared_client import get_shared_client, MaximusService

# Get client (singleton)
client = get_shared_client()

# Health check single service
response = client.health_check(MaximusService.CORE)
if response.success:
    print(f"✓ {response.service}: {response.data}")
else:
    print(f"✗ {response.service}: {response.error}")

# Health check all services
results = client.health_check_all()
for result in results:
    status = "✓" if result.success else "✗"
    print(f"{status} {result.service}")
```

### Custom Request
```python
# POST request
response = client.request(
    MaximusService.PENELOPE,
    "/analyze",
    method="POST",
    data={"text": "Hello MAXIMUS"}
)

# GET with params
response = client.request(
    MaximusService.ORACULO,
    "/predict",
    params={"model": "gpt-4"}
)
```

### Available Services
```python
MaximusService.CORE         # http://localhost:8153
MaximusService.PENELOPE     # http://localhost:8150
MaximusService.NIS          # http://localhost:8152
MaximusService.MABA         # http://localhost:8151
MaximusService.ORCHESTRATOR # http://localhost:8027
MaximusService.ORACULO      # http://localhost:8026
MaximusService.ATLAS        # http://localhost:8007
MaximusService.EUREKA       # http://localhost:8151
```

---

## 🎨 UI Components

### Thinking Stream (Gemini-style)
```python
from ui.components import show_thinking_stream

show_thinking_stream([
    "Connecting to MAXIMUS Core",
    "Fetching health metrics",
    "Processing results"
])
# Output: Animated spinner with progressive steps
```

### Results Box
```python
from ui.components import show_results_box, create_table

table = create_table(
    "Services",
    [("Name", "left", "bold"), ("Status", "center", "")],
    [["Core", "✓ OK"], ["Penelope", "✓ OK"]]
)

show_results_box(
    "Health Check",
    {
        "Summary": "8/8 services healthy",
        "Details": table
    },
    status="success"  # or "warning", "error"
)
```

### Error Display
```python
from ui.components import show_error

show_error(
    "Connection Failed",
    "Could not connect to MAXIMUS Core",
    suggestions=[
        "Check if service is running: docker ps",
        "Verify URL in config"
    ],
    context={"service": "core", "url": "localhost:8153"}
)
```

### Table
```python
from ui.components import create_table
from rich.console import Console

table = create_table(
    "MAXIMUS Services",
    [
        ("Service", "left", "bold"),
        ("Status", "center", ""),
        ("Response Time", "right", "dim")
    ],
    [
        ["Core", "✓ OK", "45ms"],
        ["Penelope", "✓ OK", "52ms"],
        ["Oraculo", "⚠ SLOW", "1200ms"]
    ]
)

Console().print(table)
```

### Progress Bar
```python
from ui.components import show_progress_operation

def load_data():
    # ... load logic
    return data

def process_data():
    # ... process logic
    return result

results = show_progress_operation("Analysis", [
    ("Loading data", load_data),
    ("Processing", process_data)
])
```

### Confirmation
```python
from ui.components import confirm_action

if confirm_action("Restart all services?", default=False):
    restart_services()
else:
    print("Cancelled")
```

### JSON/YAML Formatting
```python
from ui.components import format_json, format_yaml
from rich.console import Console

data = {"status": "ok", "version": "1.0.0"}

# JSON
console = Console()
console.print(format_json(data))

# YAML
console.print(format_yaml(data))
```

---

## 🧪 Testing

### Run Tests
```bash
# All foundation tests
pytest tests/test_foundation.py -v

# Specific test
pytest tests/test_foundation.py::TestSharedMaximusClient::test_health_check -v

# With coverage
pytest tests/test_foundation.py --cov=core.maximus_integration --cov=ui.components
```

### Test in Python REPL
```python
# Test SharedMaximusClient
python3 -c "
from core.maximus_integration.shared_client import get_shared_client, MaximusService
client = get_shared_client()
print(client.health_check(MaximusService.CORE))
"

# Test UI Components
python3 -c "
from ui.components import show_thinking_stream
show_thinking_stream(['Step 1', 'Step 2', 'Step 3'], delay=0.5)
"
```

---

## 📝 Complete Example: Health Check Command

```python
# cli/health_command_enhanced.py
import click
from core.maximus_integration.shared_client import get_shared_client, MaximusService
from ui.components import show_thinking_stream, create_table, show_results_box

@click.command()
@click.option('--watch', is_flag=True, help='Watch mode (refresh every 5s)')
@click.option('--service', type=str, help='Check specific service only')
def health(watch, service):
    """Check health of MAXIMUS services"""
    
    # Show thinking
    show_thinking_stream([
        "Connecting to services",
        "Fetching health status",
        "Processing results"
    ])
    
    # Get client
    client = get_shared_client()
    
    # Single service or all
    if service:
        results = [client.health_check(MaximusService(service))]
    else:
        results = client.health_check_all(timeout=10)
    
    # Build table
    rows = []
    healthy_count = 0
    
    for result in results:
        if result.success:
            status = "✓ OK"
            healthy_count += 1
            uptime = result.data.get("uptime", "N/A") if result.data else "N/A"
        else:
            status = "✗ DOWN"
            uptime = "N/A"
        
        response_time = f"{result.response_time_ms}ms" if result.response_time_ms else "N/A"
        
        rows.append([result.service, status, response_time, uptime])
    
    table = create_table(
        "MAXIMUS Services Health",
        [
            ("Service", "left", "bold"),
            ("Status", "center", ""),
            ("Response Time", "right", "dim"),
            ("Uptime", "right", "dim")
        ],
        rows
    )
    
    # Show results
    status = "success" if healthy_count == len(results) else "warning"
    show_results_box(
        "Health Check Results",
        {
            "Summary": f"{healthy_count}/{len(results)} services healthy",
            "Details": table
        },
        status=status
    )

if __name__ == "__main__":
    health()
```

**Run it:**
```bash
python3 cli/health_command_enhanced.py
python3 cli/health_command_enhanced.py --service core
python3 cli/health_command_enhanced.py --watch
```

---

## 🔧 Configuration

### View Current Config
```python
from config.settings import get_settings

settings = get_settings()
print(f"Core URL: {settings.maximus.core_url}")
print(f"Timeout: {settings.maximus.timeout_seconds}s")
print(f"Max Retries: {settings.maximus.max_retries}")
```

### Override via Environment
```bash
export MAXIMUS_CORE_URL="http://192.168.1.100:8153"
export MAXIMUS_TIMEOUT=60
export MAXIMUS_MAX_RETRIES=5

python3 cli/health_command.py
```

---

## 📚 Documentation

- **Full Documentation**: `docs/FOUNDATION_SETUP.md`
- **Status Report**: `FOUNDATION_STATUS.md`
- **This Guide**: `FOUNDATION_QUICKSTART.md`

---

## ✅ Checklist for New Features

When building new features using foundation:

- [ ] Import `get_shared_client()` for MAXIMUS API calls
- [ ] Use `show_thinking_stream()` for loading states
- [ ] Use `show_results_box()` or `create_table()` for results
- [ ] Use `show_error()` for error handling
- [ ] Add tests to `tests/test_<feature>.py`
- [ ] Update documentation

---

**Quick Reference Card Complete**

**Soli Deo Gloria** 🙏
