# Max-Code CLI

> Revolutionary code generation system with constitutional governance

**Max-Code** é um sistema de geração de código baseado em agentes com governança constitucional, implementando **DETER-AGENT** (Deliberate, Traceable, Efficient, Rational) framework e **Constitutional AI** principles.

---

## 📋 Status de Implementação

✅ **COMPLETO**: Constitutional Core (P1-P6)
✅ **COMPLETO**: DETER-AGENT Layer 2 (Deliberation)
✅ **COMPLETO**: DETER-AGENT Layer 3 (State Management)
✅ **COMPLETO**: DETER-AGENT Layer 4 (Execution)
✅ **COMPLETO**: DETER-AGENT Layer 5 (Incentive)
✅ **COMPLETO**: Agent SDK
✅ **COMPLETO**: 7 Specialized Agents
⏳ **PENDENTE**: TRINITY Architecture
⏳ **PENDENTE**: UI/UX (Claude Code + Gemini)

**Total implementado**: ~10,000 linhas de código production-ready

---

## 🏛️ Arquitetura

### 1. Constitutional Core (CORE DO CORE)

O núcleo constitucional que garante qualidade e compliance:

#### P1: Completude Obrigatória
- **LEI < 1.0** (Lazy Execution Index)
- Zero placeholders, TODOs, stubs
- Código sempre completo e funcional

#### P2: Validação Preventiva
- Validação de APIs antes de usar
- Previne alucinações
- Fail-fast approach

#### P3: Ceticismo Crítico
- Anti-sycophancy
- Desafia premissas falsas
- Thinking rigoroso

#### P4: Rastreabilidade Total
- Toda ação é rastreável
- Audit trail completo
- Transparency máxima

#### P5: Consciência Sistêmica
- Avalia impacto sistêmico
- Considera side effects
- Holistic thinking

#### P6: Eficiência de Token
- **FPC ≥ 80%** (First-Pass Correctness)
- **CRS ≥ 95%** (Context Retention Score)
- Máximo 2 iterações

### 2. Guardian Agents (Auto-Protection 24/7)

Sistema de proteção automática que enforça a constituição:

- **PreExecutionGuardian**: Valida ANTES de executar (pode BLOQUEAR)
- **RuntimeGuardian**: Monitora DURANTE execução (pode INTERROMPER)
- **PostExecutionGuardian**: Valida DEPOIS de executar (pode REJEITAR)
- **AutoProtectionSystem**: Orquestra todos guardians (ALWAYS_ON mode)

### 3. DETER-AGENT Framework (5 Layers)

Framework de 5 camadas para execução determinística:

#### Layer 1: Constitutional
- P1-P6 Validators
- Constitutional Engine
- Guardian Agents

#### Layer 2: Deliberation
- **Tree of Thoughts**: Explora múltiplos caminhos antes de commitar
- **Self-Consistency**: Votação entre múltiplas amostras
- **Chain of Thought**: Raciocínio passo-a-passo explícito
- **Adversarial Critic**: Red team self-criticism

#### Layer 3: State Management
- **Context Compression**: CRS ≥95%
- **Progressive Disclosure**: Revelação gradual de informação
- **Memory Manager**: Working/Episodic/Semantic/Procedural
- **Sub-Agent Isolation**: Principle of least privilege

#### Layer 4: Execution
- **Tool Executor**: Execução segura de ferramentas
- **TDD Enforcer**: Força test-driven development (RED→GREEN→REFACTOR)
- **Action Validator**: Validação pré-execução
- **Structured Actions**: Ações estruturadas (não ad-hoc)

#### Layer 5: Incentive
- **Reward Model**: Sistema de recompensas
- **Metrics Tracker**: Tracking de LEI, FPC, CRS
- **Performance Monitor**: Agregação de métricas
- **Feedback Loop**: Feedback acionável contínuo

### 4. Agent SDK

SDK para criar agentes especializados:

- **BaseAgent**: Classe abstrata base
- **AgentPool**: Gerenciamento de múltiplos agentes
- **AgentRegistry**: Catálogo de tipos de agentes
- **AgentOrchestrator**: Orquestração multi-agent

### 5. Specialized Agents

7 agentes especializados (Ports 8160-8166):

| Agent | Port | Capability | Descrição |
|-------|------|------------|-----------|
| **PlanAgent** | 8160 | PLANNING | Planejamento com Tree of Thoughts |
| **ExploreAgent** | 8161 | EXPLORATION | Exploração de codebase |
| **CodeAgent** | 8162 | CODE_GENERATION | Geração de código |
| **TestAgent** | 8163 | TESTING | Geração e execução de testes |
| **ReviewAgent** | 8164 | CODE_REVIEW | Code review |
| **FixAgent** | 8165 | DEBUGGING | Bug fixing |
| **DocsAgent** | 8166 | DOCUMENTATION | Documentação |

---

## 🚀 Quick Start

### Usando um agente individual:

```python
from agents import PlanAgent, CodeAgent
from sdk import create_agent_task

# Criar agente
plan_agent = PlanAgent()

# Criar task
task = create_agent_task(
    description="Refatorar módulo de autenticação",
    priority="HIGH",
)

# Executar
result = plan_agent.run(task)
print(result.output)
```

### Orquestrando múltiplos agentes:

```python
from agents import PlanAgent, CodeAgent, TestAgent, ReviewAgent
from sdk import AgentPool, AgentOrchestrator

# Criar pool
pool = AgentPool()
pool.register_agent(PlanAgent())
pool.register_agent(CodeAgent())
pool.register_agent(TestAgent())
pool.register_agent(ReviewAgent())

# Orquestrar
orchestrator = AgentOrchestrator(pool)
results = orchestrator.orchestrate(
    task_description="Implementar feature X",
    agent_sequence=["plan_agent", "code_agent", "test_agent", "review_agent"],
)
```

---

## 📊 Métricas Constitucionais

O Max-Code CLI rastreia 3 métricas principais:

### LEI (Lazy Execution Index)
- **Target**: < 1.0
- **Formula**: `(lazy patterns / LOC) × 1000`
- **Lazy patterns**: TODOs, placeholders, `pass`, `NotImplementedError`

### FPC (First-Pass Correctness)
- **Target**: ≥ 80%
- **Formula**: `(tasks passed first try / total tasks) × 100%`

### CRS (Context Retention Score)
- **Target**: ≥ 95%
- **Formula**: `(informação preservada / informação original) × 100%`

---

## 🛡️ Guardian Protection

O sistema de guardians protege automaticamente:

```python
from core.constitutional.guardians import AutoProtectionSystem
from core.constitutional.engine import ConstitutionalEngine

# Criar engine + auto-protection
engine = ConstitutionalEngine()
auto_protection = AutoProtectionSystem(engine=engine)

# Executar ação protegida
report = auto_protection.protect_action(
    action=action,
    execution_callback=lambda: execute_code(),
)

# Verificar resultado
if report.final_verdict.can_proceed:
    print("✓ Action approved")
else:
    print(f"✗ Action blocked: {report.final_verdict.reason}")
```

---

## 🧪 TDD Enforcement

Max-Code força test-driven development:

```python
from core.deter_agent.execution import TDDEnforcer, create_code_change

# Criar enforcer
tdd = TDDEnforcer(strict_mode=True)

# Criar code change
code_change = create_code_change(
    file_path="auth.py",
    function_name="authenticate",
    lines_added=50,
)

# Iniciar ciclo TDD
cycle = tdd.start_tdd_cycle(code_change)

# FASE 1: RED (testes devem FALHAR)
if not tdd.enforce_red_phase(cycle):
    print("❌ RED phase failed!")

# FASE 2: GREEN (testes devem PASSAR)
if not tdd.enforce_green_phase(cycle):
    print("❌ GREEN phase failed!")

# FASE 3: REFACTOR
tdd.enforce_refactor_phase(cycle)

# Validar ciclo completo
validation = tdd.validate_cycle(cycle)
if validation['can_merge']:
    print("✓ TDD cycle complete, can merge")
```

---

## 🎯 Filosofia

Max-Code CLI segue os seguintes princípios:

### 1. Constitutional AI
- Governança constitucional (P1-P6)
- Guardians enforçam automaticamente
- Métricas objetivas (LEI, FPC, CRS)

### 2. Deliberate Problem Solving
- Tree of Thoughts (explorar múltiplos caminhos)
- Self-Consistency (votação)
- Chain of Thought (raciocínio explícito)
- Adversarial Critic (red team)

### 3. Test-Driven Development
- Tests FIRST, code SECOND
- RED → GREEN → REFACTOR (obrigatório)
- Coverage ≥80%

### 4. Token Efficiency
- Context compression (CRS ≥95%)
- Progressive disclosure
- Sub-agent isolation
- Max 2 iterations

### 5. Biblical Wisdom
- Todas as loading messages são versículos bíblicos
- Fundamentação ética e moral
- Humildade e excelência

---

## 📚 Estrutura do Projeto

```
max-code-cli/
├── core/
│   ├── constitutional/          # Constitutional Core
│   │   ├── validators/          # P1-P6 Validators
│   │   ├── engine.py            # Constitutional Engine
│   │   └── guardians/           # Guardian Agents
│   ├── deter_agent/             # DETER-AGENT Framework
│   │   ├── deliberation/        # Layer 2: ToT, CoT, etc
│   │   ├── state/               # Layer 3: Memory, Context
│   │   ├── execution/           # Layer 4: Tools, TDD
│   │   └── incentive/           # Layer 5: Rewards, Metrics
│   └── messages.py              # Biblical Messages
├── sdk/                         # Agent SDK
│   ├── base_agent.py
│   ├── agent_pool.py
│   ├── agent_registry.py
│   └── agent_orchestrator.py
├── agents/                      # Specialized Agents
│   ├── plan_agent.py
│   ├── explore_agent.py
│   ├── code_agent.py
│   ├── test_agent.py
│   ├── review_agent.py
│   ├── fix_agent.py
│   └── docs_agent.py
└── examples/                    # Examples
```

---

## 🤝 Contributing

Max-Code CLI segue governança constitucional rigorosa. Para contribuir:

1. **Fork** o repositório
2. **Crie branch** para sua feature
3. **Implemente** seguindo P1-P6
4. **Testes FIRST** (TDD obrigatório)
5. **Submit PR** (será validado pelos guardians)

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

Baseado em research de:
- **Constitutional AI** (Anthropic)
- **Tree of Thoughts** (Yao et al., Princeton/Google)
- **Self-Consistency** (Wang et al., Google)
- **Chain of Thought** (Wei et al., Google)

---

## 📖 Biblical Foundation

> "Porque com sabedoria se edifica a casa, e com a inteligência ela se firma"
> (Provérbios 24:3)

> "Examinai tudo. Retende o bem."
> (1 Tessalonicenses 5:21)

> "Os pensamentos do diligente tendem só à abundância, porém os de todo apressado, tão-somente à penúria."
> (Provérbios 21:5)

---

**🤖 Generated with Max-Code CLI**

**Built with ❤️ and Constitutional Governance**
