"""
Test OpenTelemetry Tracing Integration

This script demonstrates distributed tracing across MAXIMUS API calls.
All traces are exported to Jaeger UI: http://localhost:16686

Week 9 - Advanced Observability (P2-006)
"""

import asyncio
from core.maximus_integration.client_v2 import MaximusClient
from core.maximus_integration.tracing import get_tracing

async def test_tracing():
    """Test distributed tracing with Jaeger."""
    
    print("🔍 Testing OpenTelemetry Distributed Tracing\n")
    print("=" * 60)
    
    # Initialize tracing
    tracing = get_tracing(service_name="maximus-test-client")
    print(f"✓ Tracing initialized: {tracing.service_name}")
    print(f"  Enabled: {tracing.enabled}")
    print(f"  Jaeger UI: http://localhost:16686")
    print()
    
    # Create client (tracing is automatic)
    async with MaximusClient() as client:
        print("Making API calls (traces will appear in Jaeger)...\n")
        
        try:
            # Test 1: Health check (will create a span)
            with tracing.span("health_check_test", {"test": "1"}):
                print("[1/3] Testing health endpoint...")
                health = await client.health()
                print(f"      ✓ Health: {health.get('status', 'unknown')}")
        
        except Exception as e:
            print(f"      ✗ Health check failed: {e}")
        
        print()
        
        try:
            # Test 2: Consciousness check (nested span)
            with tracing.span("consciousness_test", {"test": "2"}):
                print("[2/3] Testing consciousness endpoint...")
                consciousness = await client.consciousness.get_status()
                print(f"      ✓ Arousal: {consciousness.arousal_level:.2f}")
        
        except Exception as e:
            print(f"      ✗ Consciousness check failed: {e}")
        
        print()
        
        try:
            # Test 3: Query (complex operation with tracing)
            with tracing.span("query_test", {"test": "3", "query": "Hello"}):
                print("[3/3] Testing query endpoint...")
                # This will likely fail if backend not running, but trace is recorded
                result = await client.query("Hello MAXIMUS")
                print(f"      ✓ Query result: {result.result[:50]}...")
        
        except Exception as e:
            print(f"      ⚠ Query failed (expected if backend down): {type(e).__name__}")
    
    print()
    print("=" * 60)
    print("\n📊 View Traces:")
    print("   1. Open Jaeger UI: http://localhost:16686")
    print("   2. Select service: 'maximus-test-client'")
    print("   3. Click 'Find Traces'")
    print("   4. Explore the distributed trace timeline")
    print()
    print("Expected traces:")
    print("   • health_check_test")
    print("   • consciousness_test")
    print("   • query_test")
    print("   • Each with nested api_request spans")
    print()

if __name__ == "__main__":
    asyncio.run(test_tracing())
