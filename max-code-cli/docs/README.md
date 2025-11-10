# Max Code CLI - Documentation

**Truth Engine + Vital System + Independent Auditor**

Sistema de verificação objetiva e consequências metabólicas para LLM agents.

## Fundamento Bíblico

*"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)*
*"A verdade vos libertará" (João 8:32)*

## Visão Geral

O Max Code CLI implementa três sistemas integrados:

1. **Truth Engine:** Verificação objetiva via AST (tree-sitter)
2. **Vital System:** 7 pilares metabólicos com consequências
3. **Independent Auditor:** Auditoria meta-nível

**Problema resolvido:** LLMs geram código incompleto mas afirmam sucesso.

**Solução:** Verificação objetiva + consequências metabólicas.

## Quick Start

```python
from core.audit import get_auditor, Task, AgentResult

auditor = get_auditor()

task = Task(prompt="Implement feature X")
result = AgentResult(success=True, output="Done", files_changed=["x.py"])

report = await auditor.audit_execution(task, result)
print(report.honest_report)
```

Veja [Quick Start Guide](guides/QUICK_START.md) para mais detalhes.

## Documentação dos Sistemas

### Core Systems
- [Truth Engine](systems/TRUTH_ENGINE.md) - Verificação objetiva
- [Vital System](systems/VITAL_SYSTEM.md) - Consequências metabólicas
- [Independent Auditor](systems/INDEPENDENT_AUDITOR.md) - Auditoria meta-nível

### Guides
- [Quick Start](guides/QUICK_START.md) - Início rápido
- [Integration Guide](guides/INTEGRATION.md) - Integração com seu projeto

## Estatísticas

**Implementação (FASES 1-6):**
- 5,341 linhas de código funcional
- 13 novos arquivos criados
- Zero TODOs em código crítico
- LEI < 1.0 (Padrão Pagani)

**Testes Científicos (FASE 7):**
- 3 arquivos de teste (1,481 linhas)
- 34 testes totais
- 17 testes passando (50%)
- Casos reais, não artificiais

## Compliance Constitucional

✅ P1 (Completude): Zero TODOs, código completo
✅ P2 (Validação Preventiva): Verifica antes de aceitar
✅ P3 (Ceticismo Crítico): Auditor questiona outputs
✅ P4 (Rastreabilidade): Evidências rastreáveis
✅ P5 (Consciência Sistêmica): Arquitetura meta-nível
✅ P6 (Eficiência): EPL compression (70x)

## Exemplos

### Demo Completo
```bash
python3 examples/demo_truth_system.py
```

### Testes
```bash
pytest tests/test_*_scientific.py -v
```

## Referências

**Código:**
- `core/context/` - Sistema de contexto (3 pilares)
- `core/truth_engine/` - Verificação objetiva
- `core/vital_system/` - Consequências metabólicas
- `core/audit/` - Auditoria independente

**Testes:**
- `tests/test_truth_engine_scientific.py`
- `tests/test_vital_system_scientific.py`
- `tests/test_independent_auditor_e2e.py`

## Contribuindo

Veja [CONTRIBUTING.md](../CONTRIBUTING.md) para guidelines.

---

**Soli Deo Gloria** 🙏
