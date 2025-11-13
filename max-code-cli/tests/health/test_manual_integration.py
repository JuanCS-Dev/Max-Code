"""
MANUAL INTEGRATION TESTS - Real Services

Testes REAIS que assumem que os serviços já estão rodando.

⚠️ PRÉ-REQUISITO: Iniciar serviços ANTES de rodar este teste:
```bash
# Terminal 1
cd "/media/juan/DATA/projects/MAXIMUS AI"
./start_core.sh

# Terminal 2
./start_penelope.sh

# Terminal 3 - Rodar testes
cd max-code-cli
pytest -v tests/health/test_manual_integration.py
```

Este é um teste HONESTO - se os serviços não estiverem rodando, FALHA.

Biblical Foundation:
"Mas o que vem da terra é terreno e fala da terra; o que vem do céu está acima de todos."
(João 3:31)
"""

import pytest
import asyncio
import time

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.health_check import (
    HealthChecker,
    ServiceStatus,
    MAXIMUS_SERVICES,
)


@pytest.mark.manual
@pytest.mark.asyncio
async def test_check_if_services_are_running():
    """
    PRÉ-CHECK: Verifica se pelo menos Core e Penelope estão rodando

    Se falhar aqui: INICIE OS SERVIÇOS!
    """
    checker = HealthChecker(timeout=5.0)

    result_core = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
    result_penelope = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])

    if result_core.status != ServiceStatus.HEALTHY:
        pytest.fail(f"""
🚨 MAXIMUS CORE NÃO ESTÁ RODANDO!

Erro: {result_core.error}

Para iniciar:
cd "/media/juan/DATA/projects/MAXIMUS AI"
./start_core.sh
        """)

    if result_penelope.status != ServiceStatus.HEALTHY:
        pytest.fail(f"""
🚨 PENELOPE NÃO ESTÁ RODANDO!

Erro: {result_penelope.error}

Para iniciar:
cd "/media/juan/DATA/projects/MAXIMUS AI"
./start_penelope.sh
        """)

    print("\n✅ PRÉ-CHECK PASSED - Serviços estão rodando!")
    print(f"   Core:     {result_core.status.value} ({result_core.latency_ms:.2f}ms)")
    print(f"   Penelope: {result_penelope.status.value} ({result_penelope.latency_ms:.2f}ms)")


@pytest.mark.manual
@pytest.mark.asyncio
async def test_real_connectivity_no_mocks():
    """
    TEST #1: Conectividade REAL - SEM MOCKS

    Este teste FAZ requisições HTTP reais.
    Se falhar: serviços estão com problema.
    """
    checker = HealthChecker(timeout=5.0)

    # REAL network request
    result_core = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
    result_penelope = await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])

    # HONEST assertions
    assert result_core.status == ServiceStatus.HEALTHY, \
        f"Core failed: {result_core.error}"
    assert result_penelope.status == ServiceStatus.HEALTHY, \
        f"Penelope failed: {result_penelope.error}"

    # REAL latency (not mocked)
    assert result_core.latency_ms is not None
    assert result_core.latency_ms > 0
    assert result_penelope.latency_ms is not None
    assert result_penelope.latency_ms > 0

    print(f"\n✅ REAL CONNECTIVITY - ZERO MOCKS")
    print(f"   Core:     {result_core.latency_ms:.2f}ms (REAL)")
    print(f"   Penelope: {result_penelope.latency_ms:.2f}ms (REAL)")


@pytest.mark.manual
@pytest.mark.asyncio
async def test_real_latency_measurement():
    """
    TEST #2: Medição de Latência REAL

    Compara latência medida com tempo real decorrido.
    Tolerância: ±20%
    """
    checker = HealthChecker(timeout=5.0)

    # Measure with real time
    start = time.time()
    result = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
    elapsed_ms = (time.time() - start) * 1000

    # Calculate bounds (20% tolerance)
    tolerance = 0.20
    lower = elapsed_ms * (1 - tolerance)
    upper = elapsed_ms * (1 + tolerance)

    print(f"\n✅ REAL LATENCY MEASUREMENT")
    print(f"   Measured:  {result.latency_ms:.2f}ms")
    print(f"   Actual:    {elapsed_ms:.2f}ms")
    print(f"   Bounds:    {lower:.2f}ms - {upper:.2f}ms")

    # Honest assertion - measured should match actual
    assert lower <= result.latency_ms <= upper, \
        f"Latency mismatch: measured {result.latency_ms:.2f}ms, actual {elapsed_ms:.2f}ms"


@pytest.mark.manual
@pytest.mark.asyncio
async def test_real_parallel_speedup():
    """
    TEST #3: Speedup Paralelo REAL

    Verifica se health checks paralelos são realmente mais rápidos.
    Esperado: >=1.5x speedup para 2 serviços
    """
    checker = HealthChecker(timeout=5.0)

    # Sequential
    start = time.time()
    await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
    await checker.check_service("penelope", MAXIMUS_SERVICES["penelope"])
    sequential_time = time.time() - start

    # Parallel
    start = time.time()
    await checker.check_all_services(services=["maximus_core", "penelope"])
    parallel_time = time.time() - start

    speedup = sequential_time / parallel_time

    print(f"\n✅ REAL PARALLEL SPEEDUP")
    print(f"   Sequential: {sequential_time:.3f}s")
    print(f"   Parallel:   {parallel_time:.3f}s")
    print(f"   Speedup:    {speedup:.2f}x")

    # Honest assertion - parallel MUST be faster
    assert speedup >= 1.3, \
        f"Parallel not faster! Speedup: {speedup:.2f}x (expected >=1.3x)"


@pytest.mark.manual
@pytest.mark.asyncio
async def test_real_summary_statistics():
    """
    TEST #4: Estatísticas Reais

    Calcula estatísticas com dados REAIS dos serviços.
    """
    checker = HealthChecker(timeout=5.0)

    health_map = await checker.check_all_services(services=["maximus_core", "penelope"])
    summary = checker.get_summary(health_map)

    # Both should be healthy
    assert summary["healthy"] == 2, \
        f"Expected 2 healthy, got {summary['healthy']}"
    assert summary["down"] == 0, \
        f"Expected 0 down, got {summary['down']}"
    assert summary["all_healthy"] is True

    # Should have average latency
    assert summary["avg_latency_ms"] is not None
    assert summary["avg_latency_ms"] > 0

    # No critical services down
    assert len(summary["critical_down"]) == 0

    print(f"\n✅ REAL SUMMARY STATISTICS")
    print(f"   Healthy: {summary['healthy']}/2")
    print(f"   Avg latency: {summary['avg_latency_ms']:.2f}ms (REAL)")


@pytest.mark.manual
@pytest.mark.asyncio
async def test_real_multiple_checks_consistency():
    """
    TEST #5: Consistência de Múltiplas Checagens

    Roda 5 health checks consecutivos e verifica consistência.
    Latência não deve variar mais que 100ms entre checks.
    """
    checker = HealthChecker(timeout=5.0)

    latencies = []
    for i in range(5):
        result = await checker.check_service("maximus_core", MAXIMUS_SERVICES["maximus_core"])
        assert result.status == ServiceStatus.HEALTHY, \
            f"Check {i+1} failed: {result.error}"
        latencies.append(result.latency_ms)

    # Calculate variance
    avg = sum(latencies) / len(latencies)
    max_dev = max(abs(lat - avg) for lat in latencies)

    print(f"\n✅ CONSISTENCY CHECK (5 runs)")
    print(f"   Latencies: {', '.join(f'{lat:.2f}ms' for lat in latencies)}")
    print(f"   Average:   {avg:.2f}ms")
    print(f"   Max dev:   {max_dev:.2f}ms")

    # Latency should be stable (within 100ms)
    assert max_dev < 100, \
        f"Latency too unstable: max deviation {max_dev:.2f}ms"


print("\n" + "="*80)
print("⚠️  MANUAL INTEGRATION TESTS")
print("="*80)
print("Prerequisites:")
print("  1. Start Core:     ./start_core.sh")
print("  2. Start Penelope: ./start_penelope.sh")
print("  3. Run tests:      pytest -v -m manual tests/health/test_manual_integration.py")
print("="*80)
