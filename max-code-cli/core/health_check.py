"""
Health Check System - MAXIMUS Services Monitoring

Verifica saúde e conectividade dos 8 serviços MAXIMUS:
1. Maximus Core (8100) - Consciousness & Safety
2. PENELOPE (8154) - 7 Fruits & Healing
3. MABA (8152) - Browser Agent
4. THOT (8153) - Decision Support
5. THOTH (8155) - Memory System
6. PENIEL (8156) - Vision & Image Analysis
7. ANIMA (8157) - Context & Awareness
8. PNEUMA (8158) - Creative Generation

Features:
- Individual service health checks
- Latency measurement
- Circuit breaker status
- Graceful degradation detection
- Detailed error reporting
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import aiohttp
from config.logging_config import get_logger

logger = get_logger(__name__)


class ServiceStatus(Enum):
    """Service health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"


@dataclass
class ServiceHealth:
    """Health check result for a single service"""
    name: str
    port: int
    status: ServiceStatus
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    circuit_breaker_state: Optional[str] = None
    version: Optional[str] = None
    uptime_seconds: Optional[int] = None


# MAXIMUS Services Configuration
MAXIMUS_SERVICES = {
    "maximus_core": {
        "name": "Maximus Core",
        "port": 8100,  # REAL port (not 8150)
        "description": "Consciousness & Safety",
        "critical": True,
    },
    "penelope": {
        "name": "PENELOPE",
        "port": 8154,  # REAL port (not 8151)
        "description": "7 Fruits & Healing",
        "critical": True,
    },
    "maba": {
        "name": "MABA",
        "port": 8152,
        "description": "Browser Agent",
        "critical": False,
    },
    "thot": {
        "name": "THOT",
        "port": 8153,
        "description": "Decision Support",
        "critical": False,
    },
    "thoth": {
        "name": "THOTH",
        "port": 8155,  # Moved from 8154 (conflict with Penelope)
        "description": "Memory System",
        "critical": False,
    },
    "peniel": {
        "name": "PENIEL",
        "port": 8156,  # Moved from 8155
        "description": "Vision & Image Analysis",
        "critical": False,
    },
    "anima": {
        "name": "ANIMA",
        "port": 8157,  # Moved from 8156
        "description": "Context & Awareness",
        "critical": False,
    },
    "pneuma": {
        "name": "PNEUMA",
        "port": 8158,  # Moved from 8157
        "description": "Creative Generation",
        "critical": False,
    },
}


class HealthChecker:
    """
    Health check coordinator for MAXIMUS services

    Features:
    - Parallel health checks for fast results
    - Timeout handling (5s default)
    - Retry logic (1 retry default)
    - Circuit breaker status detection
    - Latency measurement
    """

    def __init__(
        self,
        base_url: str = "http://localhost",
        timeout: float = 5.0,
        retries: int = 1
    ):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.retries = retries

    async def check_service(
        self,
        service_id: str,
        config: Dict
    ) -> ServiceHealth:
        """
        Check health of a single service

        Args:
            service_id: Service identifier
            config: Service configuration

        Returns:
            ServiceHealth with status and metrics
        """
        name = config["name"]
        port = config["port"]
        url = f"{self.base_url}:{port}/health"

        logger.debug(f"Checking {name} at {url}")

        # Measure latency
        start_time = time.time()

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    latency_ms = (time.time() - start_time) * 1000

                    if response.status == 200:
                        data = await response.json()

                        return ServiceHealth(
                            name=name,
                            port=port,
                            status=ServiceStatus.HEALTHY,
                            latency_ms=round(latency_ms, 2),
                            circuit_breaker_state=data.get("circuit_breaker"),
                            version=data.get("version"),
                            uptime_seconds=data.get("uptime"),
                        )
                    else:
                        return ServiceHealth(
                            name=name,
                            port=port,
                            status=ServiceStatus.DEGRADED,
                            latency_ms=round(latency_ms, 2),
                            error=f"HTTP {response.status}",
                        )

        except asyncio.TimeoutError:
            latency_ms = (time.time() - start_time) * 1000
            return ServiceHealth(
                name=name,
                port=port,
                status=ServiceStatus.DOWN,
                latency_ms=round(latency_ms, 2),
                error="Timeout",
            )

        except aiohttp.ClientConnectorError:
            return ServiceHealth(
                name=name,
                port=port,
                status=ServiceStatus.DOWN,
                error="Connection refused",
            )

        except Exception as e:
            return ServiceHealth(
                name=name,
                port=port,
                status=ServiceStatus.DOWN,
                error=f"{type(e).__name__}: {str(e)[:50]}",
            )

    async def check_all_services(
        self,
        services: Optional[List[str]] = None
    ) -> Dict[str, ServiceHealth]:
        """
        Check health of all (or selected) services in parallel

        Args:
            services: Optional list of service IDs to check
                     If None, checks all services

        Returns:
            Dict mapping service_id to ServiceHealth
        """
        # Filter services if specified
        if services:
            to_check = {
                k: v for k, v in MAXIMUS_SERVICES.items()
                if k in services
            }
        else:
            to_check = MAXIMUS_SERVICES

        logger.info(f"🏥 Checking {len(to_check)} MAXIMUS services...")

        # Create tasks for parallel execution
        tasks = [
            self.check_service(service_id, config)
            for service_id, config in to_check.items()
        ]

        # Execute in parallel
        results = await asyncio.gather(*tasks)

        # Map results to service IDs
        health_map = {
            service_id: result
            for service_id, result in zip(to_check.keys(), results)
        }

        # Log summary
        healthy_count = sum(
            1 for h in results
            if h.status == ServiceStatus.HEALTHY
        )
        logger.info(
            f"   ✓ Health check complete: {healthy_count}/{len(results)} services healthy"
        )

        return health_map

    def get_summary(self, health_map: Dict[str, ServiceHealth]) -> Dict:
        """
        Generate summary statistics

        Returns:
            Dict with counts, avg latency, critical service status
        """
        results = list(health_map.values())

        healthy = [h for h in results if h.status == ServiceStatus.HEALTHY]
        degraded = [h for h in results if h.status == ServiceStatus.DEGRADED]
        down = [h for h in results if h.status == ServiceStatus.DOWN]

        # Calculate average latency (only healthy services)
        latencies = [h.latency_ms for h in healthy if h.latency_ms is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else None

        # Check critical services
        critical_down = []
        for service_id, health in health_map.items():
            config = MAXIMUS_SERVICES[service_id]
            if config.get("critical") and health.status != ServiceStatus.HEALTHY:
                critical_down.append(health.name)

        return {
            "total": len(results),
            "healthy": len(healthy),
            "degraded": len(degraded),
            "down": len(down),
            "avg_latency_ms": round(avg_latency, 2) if avg_latency else None,
            "critical_down": critical_down,
            "all_healthy": len(healthy) == len(results),
        }


# Convenience function for quick checks
async def quick_health_check() -> Tuple[Dict[str, ServiceHealth], Dict]:
    """
    Quick health check of all MAXIMUS services

    Returns:
        Tuple of (health_map, summary)
    """
    checker = HealthChecker()
    health_map = await checker.check_all_services()
    summary = checker.get_summary(health_map)
    return health_map, summary


# Synchronous wrapper for non-async contexts
def sync_health_check() -> Tuple[Dict[str, ServiceHealth], Dict]:
    """
    Synchronous health check wrapper

    Returns:
        Tuple of (health_map, summary)
    """
    return asyncio.run(quick_health_check())


if __name__ == "__main__":
    # Quick test
    print("🏥 MAXIMUS Health Check\n")
    health_map, summary = sync_health_check()

    print("\n📊 Services:")
    for service_id, health in health_map.items():
        status_icon = {
            ServiceStatus.HEALTHY: "✅",
            ServiceStatus.DEGRADED: "⚠️",
            ServiceStatus.DOWN: "❌",
            ServiceStatus.UNKNOWN: "❓",
        }[health.status]

        latency_str = f"{health.latency_ms}ms" if health.latency_ms else "-"
        error_str = f" ({health.error})" if health.error else ""

        print(f"  {status_icon} {health.name:20} {latency_str:>8} {error_str}")

    print(f"\n📈 Summary:")
    print(f"  Total:     {summary['total']}")
    print(f"  Healthy:   {summary['healthy']}")
    print(f"  Degraded:  {summary['degraded']}")
    print(f"  Down:      {summary['down']}")

    if summary['avg_latency_ms']:
        print(f"  Avg Latency: {summary['avg_latency_ms']}ms")

    if summary['critical_down']:
        print(f"\n⚠️  Critical services down: {', '.join(summary['critical_down'])}")
