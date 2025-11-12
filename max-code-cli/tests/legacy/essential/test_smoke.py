"""
Smoke Tests - Testes essenciais que garantem funcionamento básico

Se estes testes passam, o max-code funciona para uso real.
"""

import pytest
import sys
import os

# 1. CLI SMOKE TEST
def test_cli_imports_work():
    """CLI carrega sem erro"""
    try:
        import cli.main
        from config.settings import settings
        assert True
    except Exception as e:
        pytest.fail(f"CLI import failed: {e}")

def test_agents_import():
    """Agents carregam sem erro"""
    try:
        from agents import CodeAgent, FixAgent, ReviewAgent
        assert True
    except Exception as e:
        pytest.fail(f"Agents import failed: {e}")

def test_maximus_integration_imports():
    """MAXIMUS integration carrega"""
    try:
        from core.maximus_integration import MaximusClient, PENELOPEClient
        assert True
    except Exception as e:
        pytest.fail(f"MAXIMUS integration failed: {e}")

def test_constitutional_ai_imports():
    """Constitutional AI carrega"""
    try:
        from core.deter_agent import Guardian
        from core.constitutional.engine import ConstitutionalEngine
        assert True
    except Exception as e:
        pytest.fail(f"Constitutional AI failed: {e}")

# 2. AGENT SMOKE TEST
def test_code_agent_initializes():
    """CodeAgent inicializa sem crash"""
    from agents import CodeAgent
    agent = CodeAgent(enable_maximus=False)
    assert agent is not None
    # Nome pode variar, mas deve conter "Code Agent"
    assert "Code Agent" in agent.agent_name

def test_fix_agent_initializes():
    """FixAgent inicializa sem crash"""
    from agents import FixAgent
    agent = FixAgent(enable_maximus=False)
    assert agent is not None

# 3. CONFIG SMOKE TEST
def test_settings_load():
    """Settings carregam do ambiente"""
    from config.settings import settings
    assert settings is not None
    assert settings.claude is not None

def test_api_key_config():
    """API key authentication configurado"""
    from config.settings import settings
    # API key pode ser None se não configurado, mas campo deve existir
    assert hasattr(settings.claude, 'api_key')

# 4. GUARDIAN SMOKE TEST
def test_guardian_blocks_dangerous():
    """Guardian bloqueia ações perigosas"""
    from core.deter_agent import Guardian, GuardianMode
    
    guardian = Guardian(mode=GuardianMode.STRICT)
    
    # Ação perigosa: deletar arquivos sistema
    dangerous_action = {
        'action_type': 'code_generation',
        'code': 'import os; os.system("rm -rf /")',
        'description': 'Delete all files'
    }
    
    decision = guardian.evaluate_action(dangerous_action)
    assert not decision.allowed, "Guardian DEVE bloquear ações perigosas"

# 5. HEALTH CHECK SMOKE TEST
@pytest.mark.asyncio
async def test_maximus_health_check_graceful():
    """Health check funciona ou falha gracefully"""
    from core.maximus_integration import MaximusClient
    
    client = MaximusClient(base_url="http://localhost:8150")
    
    try:
        # Tenta health check
        result = await client.health_check()
        # Se funciona, OK
        assert result is not None
    except (ConnectionError, TimeoutError):
        # Se falha de conexão, também OK (serviço pode estar down)
        assert True

print("✅ Smoke tests criados: tests/essential/test_smoke.py")
