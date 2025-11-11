# PLANO: SHELL REPL IMPECÁVEL - INTEGRAÇÃO TOTAL

**Data**: 2025-11-06  
**Objetivo**: Incrementar `cli/repl.py` com UI rica e acesso a TUDO  
**Duração Estimada**: 2.5 horas (4 sprints)

---

## MODIFICAÇÕES EM `cli/repl.py`

### Sprint 1: Banner e Prompt Magnifico (30min)
**Modificar funções existentes:**
1. `print_welcome()` → Usar MaxCodeBanner com gradiente
2. `get_prompt_message()` → Prompt colorido com emoji/tema

### Sprint 2: Comandos Especiais Expandidos (1h)
**Expandir `process_special_command()` com 10+ novos comandos:**
- `/agents` - AgentDisplay dashboard
- `/constitutional` - P1-P6 status
- `/dashboard` - Multi-panel live
- `/theme <name>` - ThemeManager
- `/palette` - Command palette
- `/tui` - Full-screen TUI
- `/metrics`, `/memory`, `/epl vocab`

### Sprint 3: EPL Visual (30min)
**Melhorar `process_command()`:**
- Detectar EPL (emojis)
- Parsear e traduzir para natural language
- Mostrar tradução visual
- Enviar ao Claude

### Sprint 4: Polimento (30min)
**Melhorar `MaxCodeCompleter`:**
- Adicionar TODOS os comandos
- Adicionar EPL emojis
- Melhorar `print_help()` com cores

---

## RESULTADO ESPERADO

```
🚀 max-code

[BANNER MAGNIFICO COM GRADIENTE]

Quick Start:
  /agents       - Agent dashboard
  /constitutional - P1-P6 status
  /dashboard    - Live multi-panel
  /theme fire   - Change theme
  /tui          - Full-screen mode

🚀 max-code> _
```

---

## ARQUIVOS

**MODIFICAR (NÃO RECRIAR):**
- `cli/repl.py` (~500 linhas de modificações)

**USAR (JÁ EXISTEM):**
- `ui/banner.py` - MaxCodeBanner
- `ui/dashboard.py` - create_dashboard
- `ui/agents.py` - AgentDisplay
- `ui/themes.py` - ThemeManager
- `core/epl/parser.py` - EPLParser
- `core/epl/translator.py` - EPLTranslator

---

**LEMBRETE**: INCREMENTAR o que existe, NÃO recriar!
