"""
Root conftest.py - Shared fixtures for E2E tests

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""
import pytest
import sys
import time
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# ============================================================================
# BACKEND HEALTH CHECK
# ============================================================================

@pytest.fixture(scope="session")
def backend_health():
    """Check if MAXIMUS backend is available"""
    from core.maximus_integration.shared_client import get_shared_client, MaximusService
    
    client = get_shared_client()
    results = client.health_check_all(timeout=5)
    
    health_map = {}
    for service in MaximusService:
        service_result = next((r for r in results if r["service"] == service.value), None)
        if service_result:
            health_map[service.value] = service_result.get("status") == "healthy"
        else:
            health_map[service.value] = False
    
    return {
        "available": health_map,
        "all_healthy": all(health_map.values()),
        "count_healthy": sum(health_map.values()),
        "count_total": len(health_map),
        "results": results
    }


@pytest.fixture(scope="session")
def require_backend(backend_health):
    """Skip test if backend not available"""
    if backend_health["count_healthy"] == 0:
        pytest.skip("No MAXIMUS services available")


@pytest.fixture(scope="session")
def require_service(backend_health):
    """Factory to skip test if specific service unavailable"""
    def _require(service_name: str):
        if not backend_health["available"].get(service_name, False):
            pytest.skip(f"Service '{service_name}' not available")
    return _require


# ============================================================================
# CLI RUNNER
# ============================================================================

@pytest.fixture
def cli_runner():
    """Click CLI test runner"""
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture
def invoke_command(cli_runner):
    """Helper to invoke CLI commands"""
    def _invoke(command: str, args: list = None, catch_exceptions: bool = True):
        """Invoke CLI command"""
        # Import command modules
        if command == "health":
            from cli.health_command import health as cmd
        elif command == "logs":
            from cli.logs_command import logs as cmd
        elif command == "analyze":
            from cli.analyze_command import analyze as cmd
        elif command == "risk":
            from cli.risk_command import risk as cmd
        elif command == "workflow":
            from cli.workflow_command import workflow as cmd
        elif command == "heal":
            from cli.heal_command import heal as cmd
        elif command == "security":
            from cli.security_command import security as cmd
        else:
            raise ValueError(f"Unknown command: {command}")
        
        return cli_runner.invoke(cmd, args or [], catch_exceptions=catch_exceptions)
    
    return _invoke


# ============================================================================
# TIMING AND METRICS
# ============================================================================

@pytest.fixture
def timer():
    """Context manager for timing operations"""
    class Timer:
        def __init__(self):
            self.start = None
            self.end = None
            self.elapsed = None
        
        def __enter__(self):
            self.start = time.time()
            return self
        
        def __exit__(self, *args):
            self.end = time.time()
            self.elapsed = self.end - self.start
    
    return Timer


@pytest.fixture
def metrics_collector():
    """Collect metrics during tests"""
    class MetricsCollector:
        def __init__(self):
            self.metrics = []
        
        def record(self, name: str, value: Any, unit: str = None):
            """Record a metric"""
            self.metrics.append({
                "name": name,
                "value": value,
                "unit": unit,
                "timestamp": datetime.now().isoformat()
            })
        
        def get_summary(self) -> Dict:
            """Get summary of collected metrics"""
            return {
                "count": len(self.metrics),
                "metrics": self.metrics
            }
        
        def save(self, filepath: Path):
            """Save metrics to file"""
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w") as f:
                json.dump(self.get_summary(), f, indent=2)
    
    return MetricsCollector()


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_code_path(tmp_path):
    """Create sample code directory for testing"""
    code_dir = tmp_path / "sample_code"
    code_dir.mkdir()
    
    # Create sample Python file
    (code_dir / "main.py").write_text("""#!/usr/bin/env python3
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    print(fibonacci(10))

if __name__ == "__main__":
    main()
""")
    
    # Create file with security issues
    (code_dir / "vulnerable.py").write_text("""import pickle
import os

def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)  # Unsafe deserialization

def execute_command(cmd):
    os.system(cmd)  # Command injection risk
""")
    
    return code_dir


@pytest.fixture
def report_dir():
    """Directory for test reports"""
    report_path = Path("tests/reports")
    report_path.mkdir(exist_ok=True, parents=True)
    return report_path


@pytest.fixture
def benchmark_dir():
    """Directory for benchmark data"""
    benchmark_path = Path("tests/benchmarks")
    benchmark_path.mkdir(exist_ok=True, parents=True)
    return benchmark_path
