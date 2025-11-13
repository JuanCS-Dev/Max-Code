"""
INTEGRATION TESTS - Real Services Running

Testes de integração REAIS com serviços rodando de verdade.
NÃO usa mocks. Testa conectividade, latência e comportamento real.

⚠️ ATENÇÃO: Estes testes iniciam serviços reais!
- Consome ~200-300MB RAM por serviço
- Inicia apenas Core + Penelope (2 serviços críticos)
- Timeout total: 60s
- Cleanup automático

Biblical Foundation:
"Mas todas as coisas devem ser feitas com decência e ordem."
(1 Coríntios 14:40)
"""

import pytest
import asyncio
import subprocess
import time
import os
import signal
import psutil
from pathlib import Path
import aiohttp

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.health_check import (
    HealthChecker,
    ServiceStatus,
    MAXIMUS_SERVICES,
)


# Services base path
SERVICES_PATH = Path("/media/juan/DATA/projects/MAXIMUS AI/services")

# Services to test (only critical ones for light resource usage)
CRITICAL_SERVICES = ["core", "penelope"]

# Timeout for service startup
STARTUP_TIMEOUT = 30  # seconds


class ServiceManager:
    """
    Manages real service lifecycle for integration tests

    Features:
    - Start services as subprocesses
    - Monitor memory usage
    - Wait for health endpoint
    - Cleanup on exit
    """

    def __init__(self):
        self.processes = {}
        self.initial_memory = None

    def get_memory_usage_mb(self):
        """Get current process memory usage in MB"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024

    async def start_service(self, service_name: str, port: int) -> bool:
        """
        Start a real MAXIMUS service

        Args:
            service_name: Service name (core, penelope)
            port: Service port

        Returns:
            True if started successfully
        """
        service_path = SERVICES_PATH / service_name / "main.py"

        if not service_path.exists():
            print(f"⚠️  Service {service_name} not found at {service_path}")
            return False

        # Set environment
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SERVICES_PATH.parent)

        # Start service as subprocess
        print(f"🚀 Starting {service_name} on port {port}...")
        process = subprocess.Popen(
            ["python3", str(service_path)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(SERVICES_PATH.parent),
        )

        self.processes[service_name] = {
            "process": process,
            "port": port,
            "pid": process.pid,
        }

        # Wait for health endpoint (with timeout)
        start_time = time.time()
        while time.time() - start_time < STARTUP_TIMEOUT:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://localhost:{port}/health", timeout=aiohttp.ClientTimeout(total=2)) as response:
                        if response.status == 200:
                            elapsed = time.time() - start_time
                            print(f"✅ {service_name} healthy after {elapsed:.1f}s")
                            return True
            except:
                pass

            await asyncio.sleep(1)

        print(f"❌ {service_name} failed to start in {STARTUP_TIMEOUT}s")
        return False

    def stop_service(self, service_name: str):
        """Stop a running service"""
        if service_name not in self.processes:
            return

        info = self.processes[service_name]
        process = info["process"]

        print(f"🛑 Stopping {service_name} (PID: {info['pid']})...")

        try:
            # Try graceful shutdown
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if not responding
            process.kill()
            process.wait()

        del self.processes[service_name]
        print(f"✅ {service_name} stopped")

    def stop_all(self):
        """Stop all running services"""
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)

    def get_running_services(self):
        """Get list of running service names"""
        return list(self.processes.keys())


@pytest.fixture(scope="module")
async def service_manager():
    """
    Pytest fixture to manage service lifecycle

    Starts services before tests, stops after
    """
    manager = ServiceManager()
    manager.initial_memory = manager.get_memory_usage_mb()

    print("\n" + "="*80)
    print("🏥 INTEGRATION TEST - Starting Real Services")
    print("="*80)
    print(f"📊 Initial memory: {manager.initial_memory:.1f} MB")

    # Start only critical services
    services_to_start = [
        ("core", 8150),
        ("penelope", 8151),
    ]

    started = []
    for service_name, port in services_to_start:
        success = await manager.start_service(service_name, port)
        if success:
            started.append(service_name)
        else:
            # Cleanup on failure
            manager.stop_all()
            pytest.skip(f"Failed to start {service_name}")

    if len(started) < len(services_to_start):
        manager.stop_all()
        pytest.skip("Not all services started successfully")

    current_memory = manager.get_memory_usage_mb()
    memory_delta = current_memory - manager.initial_memory
    print(f"📊 Memory after startup: {current_memory:.1f} MB (+{memory_delta:.1f} MB)")

    yield manager

    # Cleanup
    print("\n" + "="*80)
    print("🧹 CLEANUP - Stopping Services")
    print("="*80)
    manager.stop_all()

    final_memory = manager.get_memory_usage_mb()
    print(f"📊 Final memory: {final_memory:.1f} MB")
    print("="*80 + "\n")


# ============================================================================
# INTEGRATION TESTS - Real Services
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_service_connectivity(service_manager):
    """
    Test REAL connectivity to running services

    This is NOT a mock. Tests actual network requests.
    """
    checker = HealthChecker(timeout=5.0)

    # Check Core
    result_core = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])

    # Check Penelope
    result_penelope = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])

    # REAL assertions - services must actually be running
    assert result_core.status == ServiceStatus.HEALTHY, f"Core failed: {result_core.error}"
    assert result_penelope.status == ServiceStatus.HEALTHY, f"Penelope failed: {result_penelope.error}"

    # REAL latency measurements (not mocked)
    assert result_core.latency_ms is not None
    assert result_core.latency_ms > 0
    assert result_core.latency_ms < 5000  # Should respond in < 5s

    assert result_penelope.latency_ms is not None
    assert result_penelope.latency_ms > 0
    assert result_penelope.latency_ms < 5000

    print(f"\n✅ REAL CONNECTIVITY TEST PASSED")
    print(f"   Core latency: {result_core.latency_ms:.2f}ms")
    print(f"   Penelope latency: {result_penelope.latency_ms:.2f}ms")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_parallel_health_checks(service_manager):
    """
    Test parallel health checks on REAL services

    Measures actual parallel execution speedup
    """
    checker = HealthChecker(timeout=5.0)

    # Sequential check
    start_sequential = time.time()
    await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
    await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])
    sequential_time = time.time() - start_sequential

    # Parallel check
    start_parallel = time.time()
    await checker.check_all_services(services=["maximus_core", "penelope"])
    parallel_time = time.time() - start_parallel

    # Parallel should be faster than sequential
    speedup = sequential_time / parallel_time

    print(f"\n✅ REAL PARALLEL EXECUTION TEST PASSED")
    print(f"   Sequential: {sequential_time:.3f}s")
    print(f"   Parallel:   {parallel_time:.3f}s")
    print(f"   Speedup:    {speedup:.2f}x")

    # With 2 services, expect at least 1.3x speedup
    assert speedup > 1.3, f"Parallel execution not faster enough: {speedup:.2f}x"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_latency_measurement(service_manager):
    """
    Test REAL latency measurement accuracy

    Compares measured latency with actual elapsed time
    """
    checker = HealthChecker(timeout=5.0)

    # Measure latency
    start = time.time()
    result = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
    elapsed_ms = (time.time() - start) * 1000

    # Measured latency should be close to actual elapsed time
    # Allow 20% tolerance for overhead
    tolerance = 0.20
    lower_bound = elapsed_ms * (1 - tolerance)
    upper_bound = elapsed_ms * (1 + tolerance)

    print(f"\n✅ REAL LATENCY MEASUREMENT TEST")
    print(f"   Measured:  {result.latency_ms:.2f}ms")
    print(f"   Actual:    {elapsed_ms:.2f}ms")
    print(f"   Tolerance: ±{tolerance*100:.0f}%")

    # Latency should be within tolerance
    assert result.latency_ms >= lower_bound, f"Latency too low: {result.latency_ms:.2f}ms < {lower_bound:.2f}ms"
    assert result.latency_ms <= upper_bound, f"Latency too high: {result.latency_ms:.2f}ms > {upper_bound:.2f}ms"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_summary_statistics(service_manager):
    """
    Test summary statistics with REAL service data
    """
    checker = HealthChecker(timeout=5.0)

    # Check both services
    health_map = await checker.check_all_services(services=["maximus_core", "penelope"])
    summary = checker.get_summary(health_map)

    # Both critical services should be healthy
    assert summary["healthy"] == 2
    assert summary["down"] == 0
    assert summary["total"] == 2
    assert summary["all_healthy"] is True

    # Should have average latency
    assert summary["avg_latency_ms"] is not None
    assert summary["avg_latency_ms"] > 0

    # No critical services down
    assert len(summary["critical_down"]) == 0

    print(f"\n✅ REAL SUMMARY STATISTICS TEST PASSED")
    print(f"   Healthy: {summary['healthy']}/2")
    print(f"   Avg latency: {summary['avg_latency_ms']:.2f}ms")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_service_restart_recovery(service_manager):
    """
    Test service recovery after restart

    Simulates a service crash and restart
    """
    checker = HealthChecker(timeout=5.0)

    # Initial check - should be healthy
    result1 = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])
    assert result1.status == ServiceStatus.HEALTHY

    # Stop service
    print("\n🛑 Stopping Penelope to simulate crash...")
    service_manager.stop_service("penelope")

    # Wait a bit
    await asyncio.sleep(1)

    # Check - should be down
    result2 = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])
    assert result2.status == ServiceStatus.DOWN

    # Restart service
    print("🚀 Restarting Penelope...")
    success = await service_manager.start_service("penelope", 8151)
    assert success, "Failed to restart Penelope"

    # Check - should be healthy again
    result3 = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])
    assert result3.status == ServiceStatus.HEALTHY

    print(f"✅ REAL SERVICE RECOVERY TEST PASSED")
    print(f"   Before stop: {result1.status.value}")
    print(f"   After stop:  {result2.status.value}")
    print(f"   After start: {result3.status.value}")


print("✅ Integration test suite created!")
print("⚠️  These tests start REAL services - mark with @pytest.mark.integration")
print("🚀 Run with: pytest -v -m integration tests/health/test_integration_real_services.py")
