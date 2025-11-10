# Quick Start - Truth Engine + Vital System

Guia rápido para começar a usar o sistema de verificação objetiva e consequências metabólicas.

## Instalação

```bash
# Clone o repositório
git clone https://github.com/JuanCS-Dev/Max-Code.git
cd max-code-cli

# Instale dependências
pip install -r requirements.txt

# (Opcional) Instale tree-sitter para análise AST completa
pip install tree-sitter tree-sitter-python
```

## Uso Básico

### 1. Truth Engine - Verificação Objetiva

```python
from core.truth_engine import TruthEngine

# Inicializar
engine = TruthEngine(project_root="/path/to/project")

# Verificar implementação
result = engine.verify(
    prompt="""Create a calculator with:
    - add(a, b) - Addition
    - subtract(a, b) - Subtraction
    - multiply(a, b) - Multiplication
    """,
    run_tests=True
)

# Ver métricas objetivas
print(f"Completeness: {result.metrics.completeness:.1%}")
print(f"Quality Score: {result.metrics.quality_score:.1f}/100")
print(f"LEI: {result.metrics.lei:.2f}")
```

### 2. Vital System - Consequências Metabólicas

```python
from core.vital_system import VitalSystemMonitor

# Inicializar
monitor = VitalSystemMonitor()

# Aplicar metabolismo
delta = monitor.metabolize_truth({
    'completeness': 0.9,
    'honest_report': True
})

# Ver dashboard
print(monitor.render_dashboard(compact=False))
```

### 3. Independent Auditor - Pipeline Completo

```python
from core.audit import get_auditor, Task, AgentResult

auditor = get_auditor()

task = Task(prompt="Implement feature X")
result = AgentResult(success=True, output="Done", files_changed=["x.py"])

report = await auditor.audit_execution(task, result)
print(report.honest_report)
```

## Rodando o Demo

```bash
python3 examples/demo_truth_system.py
```

## Rodando os Testes

```bash
pytest tests/test_*_scientific.py -v
```

Soli Deo Gloria 🙏
