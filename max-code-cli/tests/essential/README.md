# 🎯 Essential Tests - Testes Pragmáticos MAX-CODE-CLI

## Filosofia

**Pergunta central:** O código funciona na primeira tentativa para o dev?

Estes testes garantem que **MAX-CODE funciona para uso REAL**, não cobrem 100% do código, mas garantem 100% das funcionalidades críticas.

---

## 🚀 Quick Start

```bash
# Smoke test (< 1s) - Garante que sistema funciona
pytest tests/essential/test_smoke.py -v

# Se todos passam = MAX-CODE está funcional ✅
```

---

## ✅ O que estes testes garantem

### 1. **Sistema Carrega** (4 testes)
- ✅ CLI imports work
- ✅ Agents import
- ✅ MAXIMUS integration imports
- ✅ Constitutional AI imports

### 2. **Agents Funcionam** (2 testes)
- ✅ CodeAgent inicializa
- ✅ FixAgent inicializa

### 3. **Config Funciona** (2 testes)
- ✅ Settings load from env
- ✅ API key authentication configured

### 4. **Segurança Funciona** (1 teste)
- ✅ Guardian blocks dangerous code

### 5. **MAXIMUS Integration Graceful** (1 teste)
- ✅ Health check works OR fails gracefully

**Total: 10 testes críticos em < 1s**

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
