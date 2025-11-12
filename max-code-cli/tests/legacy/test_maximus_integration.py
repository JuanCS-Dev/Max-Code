"""Tests for MAXIMUS Integration"""
import pytest, asyncio
from src.maximus import *

@pytest.fixture
def mock_client():
    """Mock MAXIMUS client"""
    class MockClient:
        async def call_service(self, service, data, timeout=30):
            if "constitutional" in service:
                return {"compliant": True}
            elif "immune" in service:
                return {"threats": []}
            elif "consciousness" in service:
                return {"aware": True, "overall_score": 0.85, "gw_broadcast": 0.9, "integration": 0.8, "self_model": 0.85, "narrative": 0.9, "analysis": "Test"}
            return {}
        async def close(self): pass
    return MockClient()

@pytest.mark.asyncio
async def test_constitutional_validation(mock_client):
    validator = ConstitutionalValidator(client=mock_client)
    result = await validator.validate("Test task")
    assert result.valid
    assert result.lei_zero_compliant
    assert result.lei_i_compliant

@pytest.mark.asyncio
async def test_immune_scan_8_cells(mock_client):
    scanner = ImmuneScanner(client=mock_client)
    report = await scanner.scan_with_8_cells("Test artifact")
    assert report.safe
    assert len(report.cell_results) == 8
    assert report.overall_risk == "low"

@pytest.mark.asyncio
async def test_consciousness_check(mock_client):
    checker = ConsciousnessChecker(client=mock_client)
    report = await checker.check_awareness("def test(): pass")
    assert report.aware
    assert report.overall_score > 0.7

def test_service_registry():
    config = get_service_config("constitutional-ai")
    assert config["tier"] == ServiceTier.CRITICAL
    assert config["model"] == "claude"

@pytest.mark.asyncio
async def test_backend_client_retry():
    client = MaximusClient(base_url="http://localhost:9999")
    with pytest.raises(MaximusError):
        await client.call_service("nonexistent", {}, timeout=1)
    await client.close()
