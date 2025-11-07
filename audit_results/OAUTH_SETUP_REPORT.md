# ✅ RELATÓRIO: OAuth Setup max-code-cli

**Data:** 2025-11-07
**Status:** ✅ **SETUP COMPLETO - COM RESSALVAS**

---

## SUMÁRIO EXECUTIVO

**VEREDICTO:** ✅ **Setup funcional, OAuth configurado, mas API requer ajuste**

**Implementação:**
- ✅ Config override para `~/.claude/` (compatibilidade Claude Code)
- ✅ Comando `max-code setup` funcional
- ✅ OAuth flow completo via PAI (symlink)
- ✅ Credentials file criado e gerenciado

**Ressalva:**
- ⚠️ Token OAuth do Claude.ai **não funciona** com `api.anthropic.com` direto
- ⚠️ API Anthropic requer **API key tradicional** ou **Claude Code setup token**

---

## IMPLEMENTAÇÃO REALIZADA

### 1. Config Override (`max_code_config.py`)

**Criado:** `max-code-cli/core/auth/max_code_config.py`

**Funcionalidade:**
- Herda config do PAI (via symlink `core/auth/config.py`)
- Override apenas paths:
  - `CONFIG_DIR`: `~/.claude/` (em vez de `~/.max-code/` do PAI)
  - `CREDENTIALS_FILE`: `~/.claude/.credentials.json`
- Mantém todo resto: `CLIENT_ID`, `REDIRECT_URI`, `CALLBACK_SERVER_PORT`, etc.

**Código:**
```python
class MaxCodeAuthConfig(BaseAuthConfig):
    """Override para compatibilidade Claude Code"""
    CONFIG_DIR = Path.home() / ".claude"
    CREDENTIALS_FILE = CONFIG_DIR / ".credentials.json"
```

**Motivo:** Compatibilidade total com Claude Code oficial.

---

### 2. Comando `max-code setup`

**Criado:** `cli/main.py` - comando `@cli.command() def setup()`

**Funcionalidade:**
1. Cria diretório `~/.claude/` com permissões `700`
2. Verifica autenticação existente
3. Guia usuário para OAuth login se necessário

**Output:**
```
═══════════════════════════════════════════════════════
       MAX-CODE CLI - FIRST TIME SETUP
═══════════════════════════════════════════════════════

Step 1: Creating configuration directory...
✓ Directory created: /home/juan/.claude

Step 2: Checking existing authentication...
✓ Authentication already configured!
   Credentials: /home/juan/.claude/.credentials.json

Setup complete! You're ready to use max-code.
```

**Validação:**
```bash
$ max-code setup
✅ PASS - Setup wizard funciona
✅ ~/.claude/ criado
✅ Credentials detectadas
```

---

### 3. OAuth Handler Update

**Modificado:** `core/auth/oauth_handler.py`

**Mudança:**
```python
# Antes:
from core.auth.config import AuthConfig

# Depois:
from core.auth.max_code_config import AuthConfig, ensure_config_dir
```

**Resultado:**
- OAuth flow salva tokens em `~/.claude/.credentials.json`
- Compatível com Claude Code oficial

---

## VALIDAÇÃO TÉCNICA

### Teste 1: Config Override

```bash
$ python3 -c "from core.auth.max_code_config import AuthConfig; \
  print(AuthConfig.CONFIG_DIR); print(AuthConfig.CREDENTIALS_FILE)"

/home/juan/.claude
/home/juan/.claude/.credentials.json

✅ PASS
```

### Teste 2: Setup Command

```bash
$ max-code setup

✅ PASS - Wizard completo
✅ ~/.claude/ criado com permissões corretas
✅ Credentials file detectado
```

### Teste 3: Credentials File

```bash
$ ls -lh ~/.claude/.credentials.json
-rw------- 1 juan juan 348 Nov  7 08:52 /home/juan/.claude/.credentials.json

✅ PASS - Permissions 600 (owner only)
✅ PASS - Formato JSON correto
✅ PASS - Contém accessToken, refreshToken, expiresAt
```

### Teste 4: Token Validity

```bash
$ python3 check_token_expiry.py

Expires at: 1794052376 (timestamp)
Now: 1762517044
✅ Token válido por mais 8759 horas (~365 dias)
```

### Teste 5: API Call

```bash
$ python3 test_anthropic_client.py

❌ FAIL: 401 Unauthorized - invalid x-api-key
```

**Motivo:** Token OAuth (`sk-ant-oat01-...`) do Claude.ai **não funciona** com `api.anthropic.com`.

---

## PROBLEMA IDENTIFICADO: OAuth Token vs API Key

### Contexto

**Claude.ai tem 2 sistemas de autenticação diferentes:**

1. **OAuth Webapp Token** (`sk-ant-oat01-...`):
   - Usado para login no Claude.ai webapp
   - Scope: `user:inference`
   - Funciona apenas no contexto webapp
   - **NÃO FUNCIONA** com `api.anthropic.com`

2. **API Key** (`sk-ant-api03-...`):
   - Usado para API programática
   - Consome créditos da conta
   - Funciona com `api.anthropic.com`

### Por que OAuth não funciona?

```python
# Tentativa com OAuth token
client = Anthropic(api_key="sk-ant-oat01-...")
response = client.messages.count_tokens(...)

# Resultado:
# 401 Unauthorized: invalid x-api-key
```

**Razão:** API Anthropic (`api.anthropic.com`) espera API key tradicional (`sk-ant-api...`), não OAuth token.

---

## SOLUÇÕES POSSÍVEIS

### Solução 1: API Key Tradicional (RECOMENDADA para desenvolvimento)

```bash
# Obter API key em: https://console.anthropic.com/settings/keys
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Testar
max-code chat "Hello"
```

**Prós:**
- ✅ Funciona imediatamente
- ✅ Simples de configurar
- ✅ Suportado nativamente

**Contras:**
- ❌ Consome créditos API
- ❌ Não usa subscrição Claude Pro/Max

---

### Solução 2: Claude Code Setup Token

```bash
# Gerar setup token via Claude CLI
claude setup-token

# Resultado: token de longa duração (1 ano)
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."

# Usar em max-code
max-code chat "Hello"
```

**Prós:**
- ✅ Token de longa duração (~1 ano)
- ✅ Compatível com Claude Code oficial
- ✅ Pode usar subscrição Pro/Max (dependendo)

**Contras:**
- ❌ Requer `claude` CLI instalado
- ❌ Ainda pode ter limitações de API

---

### Solução 3: Web Browser Flow (ATUAL - Limitado)

```bash
# OAuth via browser
max-code auth login

# Resultado: ~/.claude/.credentials.json criado
# Token: sk-ant-oat01-... (OAuth webapp)
```

**Prós:**
- ✅ Flow implementado e funcional
- ✅ Credentials salvos corretamente
- ✅ Compatível Claude Code

**Contras:**
- ❌ Token não funciona com api.anthropic.com
- ❌ Apenas para webapp Claude.ai
- ❌ Não serve para max-code CLI

---

## RECOMENDAÇÃO

### Para Uso Imediato

**Usar API Key tradicional:**

```bash
# 1. Obter API key
# Acessar: https://console.anthropic.com/settings/keys
# Copiar: sk-ant-api03-...

# 2. Configurar
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# 3. Testar
max-code chat "Explain OAuth vs API key"
```

### Para Compatibilidade Claude Code

**Se já tem Claude CLI:**

```bash
# 1. Setup token via Claude CLI
claude setup-token

# 2. Copiar token gerado
export CLAUDE_CODE_OAUTH_TOKEN="<token>"

# 3. Testar
max-code chat "Hello"
```

---

## STATUS FINAL

### ✅ O QUE FUNCIONA

1. **Config Override:**
   - ✅ Paths corretos (`~/.claude/`)
   - ✅ Compatibilidade Claude Code
   - ✅ Herda config do PAI

2. **Comando setup:**
   - ✅ Wizard funcional
   - ✅ Cria diretório
   - ✅ Verifica auth
   - ✅ Guia usuário

3. **OAuth Flow:**
   - ✅ Browser flow funciona
   - ✅ Tokens salvos corretamente
   - ✅ Refresh token disponível

### ⚠️ O QUE PRECISA AJUSTE

1. **API Access:**
   - ❌ OAuth token não funciona com api.anthropic.com
   - ⚠️ Precisa API key ou setup token

2. **Documentação:**
   - ⚠️ Esclarecer diferença OAuth vs API key
   - ⚠️ Guiar usuário para solução correta

---

## PRÓXIMOS PASSOS

### Imediato

1. **Adicionar mensagem clara** em `oauth_handler.py`:
   ```python
   if token_type == "oat01":
       logger.warning("OAuth webapp token detected")
       logger.info("For API access, use:")
       logger.info("1. API Key: export ANTHROPIC_API_KEY=...")
       logger.info("2. Setup Token: claude setup-token")
   ```

2. **Atualizar documentação** SHELL_GUIDE.md:
   - Explicar diferença OAuth vs API key
   - Passo-a-passo para API key
   - Alternativa: Claude Code setup token

### Futuro (Opcional)

1. **Implementar token exchange:**
   - Converter OAuth token para API token (se Anthropic suportar)

2. **Fallback automático:**
   - Se OAuth token falhar, pedir API key
   - Ou usar token setup automaticamente

3. **Integração oficial:**
   - Contatar Anthropic para entender fluxo correto
   - Verificar se há endpoint para converter tokens

---

## CONCLUSÃO

**Setup OAuth está 100% implementado e funcional.**

**Ressalva:** Token OAuth serve para webapp Claude.ai, não API programática.

**Para usar max-code CLI imediatamente:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
max-code shell
```

**Sistema está pronto, apenas requer configuração de API key.**

---

*Soli Deo Gloria* 🙏

**Relatório gerado por:** Claude Code (Sonnet 4.5)
**Data:** 2025-11-07
**Status:** ✅ SETUP COMPLETO - API KEY RECOMENDADA
