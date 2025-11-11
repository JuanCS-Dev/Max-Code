"""
Real-time performance monitoring for MAXIMUS services.
"""

import asyncio
import time
from typing import Dict, List
import httpx
import structlog

logger = structlog.get_logger(__name__)


async def measure_latency(url: str, samples: int = 100) -> Dict[str, float]:
    """Measure endpoint latency."""
    latencies: List[float] = []

    async with httpx.AsyncClient() as client:
        for _ in range(samples):
            start = time.time()
            try:
                response = await client.get(url, timeout=5.0)
                duration = (time.time() - start) * 1000  # ms
                if response.status_code == 200:
                    latencies.append(duration)
            except Exception as e:
                logger.error("latency_measurement_error", url=url, error=str(e))

    if not latencies:
        return {}

    latencies.sort()
    return {
        "p50": latencies[len(latencies) // 2],
        "p95": latencies[int(len(latencies) * 0.95)],
        "p99": latencies[int(len(latencies) * 0.99)],
        "avg": sum(latencies) / len(latencies),
        "min": min(latencies),
        "max": max(latencies),
    }


async def monitor_services():
    """Monitor all MAXIMUS services."""
    services = {
        "Core": "http://localhost:8100/health",
        "PENELOPE": "http://localhost:8154/health",
        "MABA": "http://localhost:8152/health",
        "NIS": "http://localhost:8153/health",
    }

    print("⚡ Performance Monitor - MAXIMUS Services\n")

    for name, url in services.items():
        print(f"📊 {name}...")
        metrics = await measure_latency(url, samples=50)

        if metrics:
            print(f"   P50: {metrics['p50']:.2f}ms")
            print(f"   P95: {metrics['p95']:.2f}ms")
            print(f"   P99: {metrics['p99']:.2f}ms")
            print(f"   Avg: {metrics['avg']:.2f}ms")
            print(f"   Min: {metrics['min']:.2f}ms")
            print(f"   Max: {metrics['max']:.2f}ms\n")
        else:
            print(f"   ⚠️  Service not responding\n")


if __name__ == "__main__":
    asyncio.run(monitor_services())
