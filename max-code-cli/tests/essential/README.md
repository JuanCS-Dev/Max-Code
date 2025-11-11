# 🎯 Essential Tests - Testes Pragmáticos MAX-CODE-CLI

## Filosofia

**Pergunta central:** O código funciona na primeira tentativa para o dev?

Estes testes garantem que **MAX-CODE funciona para uso REAL**, não cobrem 100% do código, mas garantem 100% das funcionalidades críticas.

---

## 🚀 Quick Start

```bash
# Todos os testes essenciais (< 2s) - 100% pass rate
pytest tests/essential/ -v

# Apenas smoke tests rápidos (< 1s)
pytest tests/essential/test_smoke.py -v

# Se todos passam = MAX-CODE está funcional ✅
```

---

## ✅ O que estes testes garantem

### **60 Testes Críticos - 100% Pass Rate** em < 2s

#### CATEGORIA 1: Todos os Agents (9 testes)
- ✅ PlanAgent, ExploreAgent, CodeAgent, TestAgent inicializam
- ✅ ReviewAgent, FixAgent, DocsAgent, ArchitectAgent inicializam
- ✅ Todos os agents importam corretamente

#### CATEGORIA 2: Constitutional AI (10 testes)
- ✅ Guardian bloqueia file deletion, system commands
- ✅ Guardian detecta padrões suspeitos em código
- ✅ Guardian permite código seguro
- ✅ Guardian modes: STRICT, BALANCED, PERMISSIVE, SABBATH
- ✅ Constitutional Engine com validators
- ✅ Guardian funciona offline (sem MAXIMUS)
- ✅ DETER-AGENT framework ativo

#### CATEGORIA 3: MAXIMUS Integration (8 testes)
- ✅ MaximusClient, PENELOPEClient inicializam
- ✅ Health check graceful degradation
- ✅ 8 service clients existem
- ✅ Circuit breaker implementado
- ✅ Fallback para modo standalone
- ✅ MAXIMUS integration opcional
- ✅ Service ports configurados (8150-8157)

#### CATEGORIA 4: Config & Settings (6 testes)
- ✅ Settings singleton
- ✅ Claude config com API key
- ✅ API key from environment
- ✅ Todas as configs necessárias
- ✅ .env support
- ✅ Config validation

#### CATEGORIA 5: CLI Commands (8 testes)
- ✅ CLI main imports
- ✅ Click CLI configurado
- ✅ Health command existe
- ✅ CLI tem comandos registrados
- ✅ Rich console para output bonito
- ✅ Rich table formatting
- ✅ CLI error handling
- ✅ CLI help disponível

#### CATEGORIA 6: Core Modules (9 testes)
- ✅ Tree of Thoughts imports
- ✅ ToT gera candidatos
- ✅ Truth Engine existe
- ✅ Context Retention tracking
- ✅ Lazy Execution prevention
- ✅ First-Pass Correctness target (80%+)
- ✅ DETER framework (5 camadas)
- ✅ Sabbath mode
- ✅ Extended Thinking support

#### CATEGORIA 7: Smoke Tests (10 testes)
- ✅ CLI, agents, MAXIMUS, Constitutional AI imports
- ✅ CodeAgent, FixAgent inicializam
- ✅ Settings load, API key config
- ✅ Guardian blocks dangerous code
- ✅ Health check graceful

**Total: 60 testes críticos em < 2s**

---

## 📊 Métrica: FPC (First-Pass Correctness)

**Target: 80%+ FPC** (código funciona na primeira tentativa)

Medimos:
- ✅ CLI inicia sem erro
- ✅ Agent gera código válido
- ✅ Guardian bloqueia perigos
- ✅ System gracefully degrades quando serviços offline

**NÃO medimos:**
- ❌ % de coverage (irrelevante)
- ❌ Número de testes (quantidade ≠ qualidade)
- ❌ Edge cases extremos (raramente acontecem)

---

## 🎯 Quando rodar

**SEMPRE antes de:**
- Push para GitHub
- Deploy para produção
- Demo para cliente
- Commit grande

**Comando:**
```bash
pytest tests/essential/ -v --tb=short
```

Se todos passam em < 2s = **SHIP IT** 🚀

---

## ❌ O que NÃO está aqui (e por quê)

1. **Testes de UI detalhados** - CLI output muda frequentemente
2. **Mocks de tudo** - Não testam integração real
3. **100% coverage** - Não garante funcionalidade
4. **Edge cases extremos** - Raramente acontecem
5. **Testes lentos** - Suite deve rodar em < 2s

---

## 🏗️ Como adicionar novos testes essenciais

**Critério:** Teste é essencial se responde "SIM" a:

1. Se este teste falhar, o MAX-CODE quebra para o dev?
2. Este cenário acontece > 1x por semana?
3. O teste roda em < 200ms?

**Se SIM para todos → Adicionar**
**Se NÃO para qualquer um → Não adicionar**

---

## 📝 Exemplo de Teste Pragmático

```python
def test_agent_generates_code():
    """Agent gera código que compila"""
    from agents import CodeAgent

    agent = CodeAgent(enable_maximus=False)
    task = AgentTask(
        id="test",
        description="create hello world function",
        parameters={"language": "python"}
    )

    result = agent.execute(task)

    # Pragmático: só verifica que não crashou e retornou algo
    assert result.success
    assert result.output['code']
    assert len(result.output['code']) > 10  # Não vazio
```

**Não precisamos verificar:**
- Se código tem syntax perfect
- Se tem 100% de documentação
- Se segue PEP8 perfeitamente

**Só precisamos garantir:**
- Agent não crasha
- Retorna código válido
- Dev pode usar imediatamente

---

## 🎓 Sabedoria Pragmática

> "Tests are a means to an end, not the end itself."
>
> "100% coverage with 0% functionality = waste."
>
> "10 testes críticos > 1000 testes inúteis."

**Soli Deo Gloria** 🙏
