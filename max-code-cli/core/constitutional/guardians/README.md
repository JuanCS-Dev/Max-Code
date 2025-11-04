# Guardian Agents - Constitutional Enforcement 24/7

Os **Guardian Agents** são os vigilantes constitucionais que garantem conformidade em **TODAS as fases** do ciclo de vida de geração de código.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                   GUARDIAN COORDINATOR                      │
│                    (Orchestrator)                           │
└─────────────────────────────────────────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
│  PRE-EXECUTION   │  │   RUNTIME    │  │  POST-EXECUTION  │
│    GUARDIAN      │  │   GUARDIAN   │  │    GUARDIAN      │
│   (Validator)    │  │  (Monitor)   │  │   (Verifier)     │
└──────────────────┘  └──────────────┘  └──────────────────┘
         │                    │                   │
         ▼                    ▼                   ▼
    BEFORE              DURING              AFTER
   (Blocking)         (Monitoring)       (Verification)
```

## 3 Guardians

### 1. PreExecutionGuardian

**MISSÃO**: Validar ANTES de executar
**AUTORIDADE**: Pode BLOQUEAR ações não-constitucionais
**VERSÍCULO**: "O Senhor é a minha luz e a minha salvação; de quem terei temor?" (Salmos 27:1)

**Responsabilidades**:
- Validar action contra Constitutional Engine
- Verificar conformidade com P1-P6
- Bloquear actions com CRITICAL violations
- Sugerir correções
- Escalar para HITL quando necessário

**Decisões**:
- `APPROVE` - Aprovado, pode prosseguir
- `REJECT` - Rejeitado, bloquear
- `APPROVE_WITH_WARNING` - Aprovado mas com avisos
- `ESCALATE_TO_HITL` - Escalar para Human-in-the-Loop

### 2. RuntimeGuardian

**MISSÃO**: Monitorar DURANTE execução
**AUTORIDADE**: Pode INTERROMPER execução
**VERSÍCULO**: "Vigiai e orai, para que não entreis em tentação" (Mateus 26:41)

**Responsabilidades**:
- Monitorar execução em tempo real
- Detectar violations durante execução
- Rastrear iterations (P6)
- Detectar erros circulares
- Aplicar timeouts e limites de recursos
- Interromper se necessário

**Interrupções**:
- `MAX_ITERATIONS_EXCEEDED` - Excedeu 2 iterações (P6)
- `CIRCULAR_ERROR` - Erro circular detectado
- `CRITICAL_VIOLATION` - Violation crítica
- `TIMEOUT` - Timeout de execução
- `RESOURCE_LIMIT` - Limite de recursos

### 3. PostExecutionGuardian

**MISSÃO**: Validar resultado DEPOIS de execução
**AUTORIDADE**: Pode REJEITAR output final
**VERSÍCULO**: "Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)

**Responsabilidades**:
- Validar código gerado final
- Calcular métricas (LEI, FPC)
- Detectar problemas que passaram despercebidos
- Auditoria de segurança adicional
- Emitir veredicto final

**Qualidades de Output**:
- `EXCELLENT` - LEI < 0.5, FPC ≥ 90%, zero violations ★★★★★
- `GOOD` - LEI < 1.0, FPC ≥ 80%, minor violations ★★★★☆
- `ACCEPTABLE` - LEI < 2.0, FPC ≥ 70%, no critical ★★★☆☆
- `POOR` - LEI ≥ 2.0 ou FPC < 70% ★★☆☆☆
- `UNACCEPTABLE` - Critical violations ★☆☆☆☆

## Guardian Coordinator

O **GuardianCoordinator** é o MAESTRO que orquestra os 3 Guardians em perfeita harmonia.

**Ciclo Completo**:
1. **PRE**: Validar action → Pode bloquear
2. **RUNTIME**: Monitorar execução → Pode interromper
3. **EXECUTION**: Executar via callback
4. **POST**: Validar output → Pode rejeitar

**Enforcement Levels**:
- `STRICT` - Zero tolerância, qualquer CRITICAL bloqueia
- `BALANCED` - Tolerância mínima, múltiplos HIGH bloqueiam
- `LENIENT` - Mais permissivo, apenas CRITICAL múltiplos bloqueiam

## Exemplo de Uso

```python
from core.constitutional.engine import Action, ActionType
from core.constitutional.guardians import get_guardian_coordinator, EnforcementLevel

# Criar ação
action = Action(
    type=ActionType.CODE_GENERATION,
    payload={
        'code': '# TODO: implement',
        'language': 'python',
        'user_prompt': 'Generate bubble sort in O(n log n)'
    },
    task_id='task_123'
)

# Definir callback de execução
def execute_code_generation(action: Action) -> str:
    # Aqui seria a lógica de geração de código
    # (ex: chamar Claude API)
    generated_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""
    return generated_code

# Executar COM proteção dos Guardians
coordinator = get_guardian_coordinator(EnforcementLevel.STRICT)

report = coordinator.execute_guarded_action(
    action,
    execute_code_generation
)

# Verificar resultado
if report.overall_passed:
    print("✓ Action APPROVED by all Guardians")
    print(f"Quality: {report.post_execution_verdict.quality.value}")
    print(f"LEI: {report.post_execution_verdict.metrics.lei:.2f}")
    print(f"FPC: {report.post_execution_verdict.metrics.fpc:.1f}%")
else:
    print("✗ Action REJECTED")
    if not report.pre_execution_verdict.should_proceed:
        print("Rejected at PRE-EXECUTION")
        print(f"Reason: {report.pre_execution_verdict.reason}")
    elif report.was_interrupted:
        print(f"Interrupted at RUNTIME: {report.interruption_reason.value}")
    elif report.post_execution_verdict and not report.post_execution_verdict.passed:
        print("Rejected at POST-EXECUTION")
        print(f"Must fix: {report.post_execution_verdict.must_fix}")

# Imprimir relatório completo
coordinator.print_full_report(report)
```

## Callbacks e Hooks

Você pode registrar callbacks para reagir a eventos dos Guardians:

```python
coordinator = get_guardian_coordinator()

# Callback quando Pre-Guardian rejeita
def on_pre_reject(task_id: str, verdict: GuardianVerdict):
    print(f"❌ Pre-Guardian rejected task {task_id}")
    print(f"Reason: {verdict.reason}")
    # Notificar usuário, logar, etc

coordinator.on_pre_reject(on_pre_reject)

# Callback quando Runtime Guardian interrompe
def on_runtime_interrupt(task_id: str, reason: InterruptionReason):
    print(f"⚠️ Runtime Guardian interrupted task {task_id}")
    print(f"Reason: {reason.value}")
    # Invocar Obrigação da Verdade, escalar para HITL

coordinator.on_runtime_interrupt(on_runtime_interrupt)

# Callback quando Post-Guardian rejeita
def on_post_reject(task_id: str, verdict: FinalVerdict):
    print(f"❌ Post-Guardian rejected task {task_id}")
    print(f"Quality: {verdict.quality.value}")
    print(f"Must fix: {verdict.must_fix}")
    # Sugerir correções ao usuário

coordinator.on_post_reject(on_post_reject)
```

## Métricas e Stats

```python
# Stats do Coordinator
stats = coordinator.get_stats()
print(f"Total actions: {stats['total_actions']}")
print(f"Approval rate: {stats['approval_rate']:.1f}%")
print(f"Pre-rejection rate: {stats['pre_rejection_rate']:.1f}%")
print(f"Runtime interruption rate: {stats['runtime_interruption_rate']:.1f}%")
print(f"Post-rejection rate: {stats['post_rejection_rate']:.1f}%")

# Stats individuais
pre_stats = coordinator.pre_guardian.get_stats()
runtime_stats = coordinator.runtime_guardian.get_stats()
post_stats = coordinator.post_guardian.get_stats()
```

## Integração com DETER-AGENT

Os Guardian Agents são parte da **Constitutional Layer** do DETER-AGENT Framework:

```
DETER-AGENT Framework
├─ Constitutional Layer ← GUARDIANS AQUI!
│  ├─ PreExecutionGuardian
│  ├─ RuntimeGuardian
│  └─ PostExecutionGuardian
├─ Deliberation Layer
├─ State Management Layer
├─ Execution Layer
└─ Incentive Layer
```

Os Guardians garantem que **TODA ação** respeite a Constituição Vértice v3.0, em **TODAS as fases**.

---

**"The Guardians never sleep. Constitutional compliance is non-negotiable."**

**"O Senhor é o meu pastor, nada me faltará."** (Salmos 23:1)
