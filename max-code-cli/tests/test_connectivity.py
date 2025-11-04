"""
MAXIMUS Services Connectivity Test

Tests connectivity to all MAXIMUS backend services:
- MAXIMUS Core
- Penelope
- Orchestrator
- Oraculo
- Atlas

This test validates that all service clients can reach their endpoints.
"""

import sys
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')

from config.settings import get_settings
from integration import (
    MaximusClient,
    PenelopeClient,
    OrchestratorClient,
    OraculoClient,
    AtlasClient
)


def test_maximus_core():
    """Test MAXIMUS Core connectivity."""
    print("\n══════════════════════════════════════════")
    print("TEST 1: MAXIMUS Core Connectivity")
    print("══════════════════════════════════════════")

    settings = get_settings()
    client = MaximusClient(settings.maximus.core_url)

    # Test health check
    print(f"Connecting to: {settings.maximus.core_url}")
    health = client.health_check()
    print(f"Health Status: {health.value}")

    if health.value == "healthy":
        print("✅ MAXIMUS Core is reachable and healthy")

        # Try getting consciousness state
        response = client.get_consciousness_state()
        if response.success:
            print(f"✅ Consciousness API working")
            if response.data:
                print(f"   ESGT Active: {response.data.get('esgt_active')}")
                print(f"   Arousal Level: {response.data.get('arousal_level')}")
        else:
            print(f"⚠️  Consciousness API error: {response.error}")
    else:
        print(f"❌ MAXIMUS Core not reachable: {health.value}")

    client.close()
    return health.value == "healthy"


def test_penelope():
    """Test Penelope connectivity."""
    print("\n══════════════════════════════════════════")
    print("TEST 2: Penelope Connectivity")
    print("══════════════════════════════════════════")

    settings = get_settings()
    client = PenelopeClient(settings.maximus.penelope_url)

    print(f"Connecting to: {settings.maximus.penelope_url}")
    health = client.health_check()
    print(f"Health Status: {health.value}")

    if health.value == "healthy":
        print("✅ Penelope is reachable and healthy")

        # Try checking Sabbath status
        response = client.check_sabbath_status()
        if response.success:
            print(f"✅ Sabbath API working")
            if response.data:
                print(f"   Is Sabbath: {response.data.get('is_sabbath')}")
        else:
            print(f"⚠️  Sabbath API error: {response.error}")
    else:
        print(f"❌ Penelope not reachable: {health.value}")

    client.close()
    return health.value == "healthy"


def test_orchestrator():
    """Test Orchestrator connectivity."""
    print("\n══════════════════════════════════════════")
    print("TEST 3: Orchestrator Connectivity")
    print("══════════════════════════════════════════")

    settings = get_settings()
    client = OrchestratorClient(settings.maximus.orchestrator_url)

    print(f"Connecting to: {settings.maximus.orchestrator_url}")
    health = client.health_check()
    print(f"Health Status: {health.value}")

    if health.value == "healthy":
        print("✅ Orchestrator is reachable and healthy")
    else:
        print(f"❌ Orchestrator not reachable: {health.value}")

    client.close()
    return health.value == "healthy"


def test_oraculo():
    """Test Oraculo connectivity."""
    print("\n══════════════════════════════════════════")
    print("TEST 4: Oraculo Connectivity")
    print("══════════════════════════════════════════")

    settings = get_settings()
    client = OraculoClient(settings.maximus.oraculo_url)

    print(f"Connecting to: {settings.maximus.oraculo_url}")
    health = client.health_check()
    print(f"Health Status: {health.value}")

    if health.value == "healthy":
        print("✅ Oraculo is reachable and healthy")
    else:
        print(f"❌ Oraculo not reachable: {health.value}")

    client.close()
    return health.value == "healthy"


def test_atlas():
    """Test Atlas connectivity."""
    print("\n══════════════════════════════════════════")
    print("TEST 5: Atlas Connectivity")
    print("══════════════════════════════════════════")

    settings = get_settings()
    client = AtlasClient(settings.maximus.atlas_url)

    print(f"Connecting to: {settings.maximus.atlas_url}")
    health = client.health_check()
    print(f"Health Status: {health.value}")

    if health.value == "healthy":
        print("✅ Atlas is reachable and healthy")
    else:
        print(f"❌ Atlas not reachable: {health.value}")

    client.close()
    return health.value == "healthy"


def main():
    """Run all connectivity tests."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + " " * 20 + "MAXIMUS SERVICES CONNECTIVITY TEST" + " " * 24 + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    results = {
        "MAXIMUS Core": test_maximus_core(),
        "Penelope": test_penelope(),
        "Orchestrator": test_orchestrator(),
        "Oraculo": test_oraculo(),
        "Atlas": test_atlas(),
    }

    # Summary
    print("\n╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "CONNECTIVITY SUMMARY" + " " * 28 + "║")
    print("╠" + "═" * 78 + "╣")

    total = len(results)
    healthy = sum(1 for v in results.values() if v)

    for service, status in results.items():
        status_icon = "✅" if status else "❌"
        status_text = "HEALTHY" if status else "UNREACHABLE"
        print(f"║  {status_icon}  {service:20} {status_text:30}   ║")

    print("╠" + "═" * 78 + "╣")
    print(f"║  Services Healthy: {healthy}/{total}" + " " * 57 + "║")
    print(f"║  Success Rate: {(healthy/total)*100:.1f}%" + " " * 61 + "║")
    print("╚" + "═" * 78 + "╝")

    if healthy == total:
        print("\n✨ ALL SERVICES HEALTHY! Ready for integration! ✨")
        return True
    elif healthy > 0:
        print(f"\n⚠️  {total - healthy} services unreachable. Partial functionality available.")
        return False
    else:
        print("\n❌ No services reachable. Check that MAXIMUS backend is running.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
