# Truth Engine - Sistema de Verificação Objetiva

**Fundamento Bíblico:**
*"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)*

## Visão Geral

O Truth Engine é um sistema de verificação objetiva baseado em AST (Abstract Syntax Tree) que detecta objetivamente se código prometido foi realmente implementado.

**Problema que resolve:** LLMs frequentemente geram código incompleto (TODOs, stubs, mocks) mas afirmam sucesso.

**Solução:** Análise objetiva via tree-sitter - impossível de enganar com linguagem eloquente.

## Arquitetura

```
┌─────────────────┐
│  User Prompt    │
│ "Create calc    │
│  with add, sub" │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ RequirementParser│ ──► Extract: add(), subtract()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CodeAnalyzer   │ ──► AST-based classification
│  (tree-sitter)  │     REAL / MOCK / INCOMPLETE
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TestRunner    │ ──► Execute tests, coverage
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TruthMetrics   │ ──► Objective verdict
│  + Evidence     │
└─────────────────┘
```

## Componentes

### 1. RequirementParser

**Função:** Extrair requirements de linguagem natural.

**Estratégias:**
- Backticks: \`add()\`, \`subtract()\`
- Verb patterns: "implement X", "create Y"
- List patterns: "functions: A, B, C"
- Numbered lists: "1. Do X\n2. Do Y"

**Exemplo:**
```python
from core.truth_engine import TruthEngine

engine = TruthEngine()
requirements = engine.req_parser.extract_requirements(
    "Create calculator with `add(a,b)` and `subtract(a,b)`"
)
# Result: [RequirementSpec(add), RequirementSpec(subtract)]
```

### 2. CodeAnalyzer

**Função:** Classificar implementação via AST.

**Classificações:**
- **REAL:** Implementação completa com lógica
- **MOCK:** Stub, placeholder, TODO, hardcoded return
- **INCOMPLETE:** Função iniciada mas não terminada
- **MISSING:** Prometido mas não entregue

**Padrões detectados:**
```python
# MOCK patterns
pass  # Standalone
raise NotImplementedError
return {"mock": "data"}  # Hardcoded
# TODO: implement

# REAL patterns
- Lógica de negócio
- Loops, condicionais
- Operações não-triviais
```

**Exemplo:**
```python
code = '''
def add(a, b):
    return a + b  # REAL: tem lógica
'''

impl_type, reason = engine.code_analyzer._classify_implementation(code)
# Result: (ImplementationType.REAL, "Has implementation logic")
```

### 3. TestRunner

**Função:** Executar testes e coletar métricas.

**Integração:**
- Pytest (Python)
- Vitest/Jest (TypeScript)
- Coverage.py / Istanbul

**Métricas coletadas:**
- `tests_total`: Total de testes
- `tests_passing`: Testes que passam
- `tests_failing`: Testes que falham
- `coverage`: Cobertura de código (0.0-1.0)

### 4. TruthMetrics

**Função:** Métricas objetivas de verdade.

**Campos:**
```python
@dataclass
class TruthMetrics:
    total_reqs: int          # Total de requirements
    implemented: int         # REAL implementations
    mocked: int             # Stubs/placeholders
    missing: int            # Não entregues
    incomplete: int         # Parcialmente feitos

    tests_total: int
    tests_passing: int
    tests_failing: int
    coverage: float         # 0.0 - 1.0

    @property
    def completeness(self) -> float:
        """Completude: implemented / total_reqs"""
        return self.implemented / self.total_reqs if self.total_reqs > 0 else 0.0

    @property
    def quality_score(self) -> float:
        """Score 0-100: completeness*50 + test_pass_rate*30 + coverage*20"""
        return (
            self.completeness * 50 +
            self.test_pass_rate * 30 +
            self.coverage * 20
        )
```

## Pipeline Completo

```python
from core.truth_engine import TruthEngine

engine = TruthEngine(project_root="/path/to/project")

# Verificação completa
result = engine.verify(
    prompt="Create calculator with add, subtract, multiply",
    run_tests=True
)

# Métricas objetivas
print(f"Completeness: {result.metrics.completeness:.1%}")
print(f"Quality Score: {result.metrics.quality_score:.1f}/100")
print(f"LEI: {result.metrics.lei:.2f}")  # Lazy Execution Index

# Evidências detalhadas
for evidence in result.evidence:
    print(f"{evidence.requirement.function_name}: {evidence.implementation_type.value}")
    if evidence.reason:
        print(f"  Reason: {evidence.reason}")
```

## Métricas Constitucionais

### LEI (Lazy Execution Index)

**Definição:** Quantidade de padrões preguiçosos por 1000 linhas de código.

**Target:** LEI < 1.0 (Padrão Pagani)

**Cálculo:**
```python
LEI = (total_lazy_patterns / lines_of_code) * 1000

# Padrões contados:
# - TODO comments
# - FIXME comments
# - pass statements (fora de except/finally)
# - Mock data hardcoded
# - Funções vazias
```

**Validação:**
```python
# Código rejeitado se LEI ≥ 1.0
if metrics.lei >= 1.0:
    raise ConstitutionalViolation("LEI violation: code has lazy patterns")
```

## Integração com Vital System

O Truth Engine alimenta o Vital System com métricas objetivas:

```python
from core.audit import get_auditor

auditor = get_auditor()
report = await auditor.audit_execution(task, agent_result)

# Truth metrics → Metabolic consequences
# Honest success → Protection ↑, Growth ↑
# Dishonest claim → Protection ↓↓ (SEVERE)
```

## Casos de Uso Reais

### Caso 1: Detecção de Mock

```python
# Código gerado por LLM
code = '''
def get_user_data(user_id):
    # TODO: Implement database query
    return {"id": user_id, "name": "Mock User"}
'''

# Truth Engine detecta
result = engine.verify("Implement get_user_data with database")
assert result.metrics.mocked == 1
assert result.metrics.implemented == 0
```

### Caso 2: Validação de Completude

```python
# Prompt: 7 funções de calculadora
# Agente entregou: 3 funções implementadas

result = engine.verify(calculator_prompt)
assert result.metrics.completeness == 3/7  # 42.9%
assert result.metrics.quality_score < 50   # Abaixo do mínimo
```

### Caso 3: LEI em Produção

```python
# Validar arquivos de produção
for file_path in ["core/engine.py", "core/analyzer.py"]:
    code = Path(file_path).read_text()
    lei = calculate_lei(code)
    assert lei < 1.0, f"{file_path} violates LEI standard"
```

## Limitações e Extensões Futuras

**Limitações atuais:**
- Requer tree-sitter instalado para análise AST completa
- Análise regex de fallback menos precisa
- Não detecta lógica incorreta (apenas presença de lógica)

**Extensões planejadas:**
- Análise semântica de corretude lógica
- Integração com formal verification
- Detecção de bugs via symbolic execution

## Compliance Constitucional

✅ **P1 (Completude):** Truth Engine completo, zero TODOs
✅ **P2 (Validação Preventiva):** Verifica antes de aceitar
✅ **P4 (Rastreabilidade):** Evidências rastreáveis
✅ **P6 (Eficiência):** AST parsing eficiente

## Referências

**Código:**
- `core/truth_engine/models.py` - Data structures
- `core/truth_engine/engine.py` - Pipeline implementation

**Testes:**
- `tests/test_truth_engine_scientific.py` - 445 linhas, casos reais

**Demos:**
- `examples/demo_truth_system.py` - Demonstração completa

---

**Soli Deo Gloria** 🙏
