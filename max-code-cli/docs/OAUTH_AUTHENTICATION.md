# OAuth Authentication - Max-Code CLI

**Data**: 2025-11-05
**Status**: ✅ IMPLEMENTADO (DEFINITIVO)

---

## 🎯 OBJETIVO

Implementar sistema de autenticação OAuth para Max-Code CLI compatível com:
- Claude Max subscription (OAuth tokens)
- Traditional API keys (ANTHROPIC_API_KEY)
- Mesmo padrão do Claude Code oficial

---

## 📋 IMPLEMENTAÇÃO COMPLETA

### 1. Arquivos Criados

```
core/auth/
├── __init__.py              # Public API exports
└── oauth_handler.py         # OAuth + API key handler (247 LOC)

cli/
└── auth_command.py          # CLI commands (setup, validate, status) (207 LOC)

docs/
└── OAUTH_AUTHENTICATION.md  # Esta documentação
```

### 2. Configuração Atualizada

**config/settings.py** - `ClaudeConfig` expandido:
```python
class ClaudeConfig(BaseSettings):
    """Supports dual authentication"""

    api_key: Optional[str] = Field(
        default=None,
        env="ANTHROPIC_API_KEY"
    )

    oauth_token: Optional[str] = Field(
        default=None,
        env="CLAUDE_CODE_OAUTH_TOKEN"
    )

    def get_auth_token(self) -> Optional[str]:
        """OAuth preferred over API key"""
        return self.oauth_token or self.api_key
```

### 3. Agentes Atualizados

**agents/code_agent.py** - Usa OAuth centralizado:
```python
from core.auth import get_anthropic_client

def __init__(self):
    # Centralized OAuth handler
    self.anthropic_client = get_anthropic_client()
```

---

## 🔐 COMO USAR

### Opção 1: OAuth Token (Recomendado para Max)

```bash
# 1. Gerar token OAuth
claude setup-token

# 2. Copiar o token (sk-ant-oat01-...)

# 3. Configurar no ambiente
export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-...

# Ou adicionar no .env:
echo "CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-..." >> .env
```

### Opção 2: API Key (Tradicional)

```bash
# 1. Obter key em: https://console.anthropic.com

# 2. Configurar no ambiente
export ANTHROPIC_API_KEY=sk-ant-api...

# Ou adicionar no .env:
echo "ANTHROPIC_API_KEY=sk-ant-api..." >> .env
```

### Comandos CLI

```bash
# Setup OAuth (lança o fluxo)
python cli/auth_command.py setup

# Validar credenciais
python cli/auth_command.py validate

# Mostrar status
python cli/auth_command.py status
```

---

## 🏗️ ARQUITETURA

### Fluxo de Autenticação

```
┌─────────────────────────────────────────┐
│  Max-Code CLI Agent                     │
│  (code_agent, test_agent, etc)          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  core/auth/oauth_handler.py             │
│  get_anthropic_client()                 │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ OAuth Token  │  │    API Key       │
│ (Priority 1) │  │  (Fallback)      │
└──────────────┘  └──────────────────┘
        │                 │
        └────────┬────────┘
                 ▼
        ┌────────────────┐
        │ Anthropic SDK  │
        │   (Claude API) │
        └────────────────┘
```

### Prioridade de Autenticação

1. **CLAUDE_CODE_OAUTH_TOKEN** (OAuth) - ✅ PREFERIDO
   - Formato: `sk-ant-oat01-...`
   - Gerado via: `claude setup-token`
   - Para: Claude Max subscribers

2. **ANTHROPIC_API_KEY** (API Key) - Fallback
   - Formato: `sk-ant-api...`
   - Obtido em: https://console.anthropic.com
   - Para: Usuários com API billing

---

## 📊 TESTES E VALIDAÇÃO

### Teste 1: Sem Credenciais

```bash
$ python cli/auth_command.py status

Environment Variables:
  ⚠️  CLAUDE_CODE_OAUTH_TOKEN: Not set
  ⚠️  ANTHROPIC_API_KEY: Not set

Validation: ❌ Invalid
Type:       none
Message:    No credentials found
```

### Teste 2: Com OAuth Token

```bash
$ export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-abc123...
$ python cli/auth_command.py validate

Status: ✅ Valid
Type:   oauth_token
Info:   OAuth token found (Claude Max)

✅ Authentication configured correctly
✅ Client created successfully
```

### Teste 3: Com API Key

```bash
$ export ANTHROPIC_API_KEY=sk-ant-api03-xyz789...
$ python cli/auth_command.py validate

Status: ✅ Valid
Type:   api_key
Info:   API key found

✅ Authentication configured correctly
✅ Client created successfully
```

---

## 🔧 IMPLEMENTAÇÃO TÉCNICA

### core/auth/oauth_handler.py

**Funções principais**:

```python
def get_anthropic_client() -> Optional[Anthropic]:
    """
    Get authenticated client with OAuth preferred.

    Priority:
    1. CLAUDE_CODE_OAUTH_TOKEN
    2. ANTHROPIC_API_KEY

    Returns:
        Authenticated Anthropic client or None
    """

def validate_credentials() -> Tuple[bool, CredentialType, str]:
    """
    Validate credentials without creating client.

    Returns:
        (is_valid, credential_type, message)
    """

def setup_oauth_token() -> bool:
    """
    Run 'claude setup-token' to generate OAuth token.

    Requires:
        - claude CLI installed (npm install -g @anthropic-ai/claude-code)

    Returns:
        True if successful
    """

def get_credential_type(credential: str) -> CredentialType:
    """
    Detect credential type from format.

    Examples:
        sk-ant-oat01-... → OAUTH_TOKEN
        sk-ant-api...    → API_KEY
    """
```

### Enum CredentialType

```python
class CredentialType(Enum):
    API_KEY = "api_key"
    OAUTH_TOKEN = "oauth_token"
    NONE = "none"
```

---

## 📖 REFERÊNCIAS

### Documentação Oficial

- **Claude Code IAM**: https://docs.claude.com/en/docs/claude-code/iam
- **Anthropic Console**: https://console.anthropic.com
- **GitHub Issues**:
  - https://github.com/anthropics/claude-code/issues/6536
  - https://github.com/anthropics/claude-code/issues/1484

### Implementações Comunitárias

- **cabinlab/claude-code-sdk-docker**: https://github.com/cabinlab/claude-code-sdk-docker
- **grll/claude-code-login**: https://github.com/grll/claude-code-login

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [x] `core/auth/__init__.py` - Public API
- [x] `core/auth/oauth_handler.py` - OAuth + API key handler
- [x] `config/settings.py` - ClaudeConfig com oauth_token
- [x] `agents/code_agent.py` - Usa get_anthropic_client()
- [x] `cli/auth_command.py` - CLI commands (setup, validate, status)
- [x] `docs/OAUTH_AUTHENTICATION.md` - Documentação completa
- [x] Testes de validação (sem credenciais, OAuth, API key)
- [x] Logging estruturado com EPL emojis preservados

---

## 🎉 STATUS FINAL

**✅ OAUTH IMPLEMENTADO COM SUCESSO**

- ✅ Dual authentication (OAuth + API Key)
- ✅ Priority: OAuth preferred
- ✅ Fallback to API key
- ✅ CLI commands (setup, validate, status)
- ✅ Centralized handler
- ✅ Updated agents (code_agent)
- ✅ Comprehensive documentation
- ✅ 100% EPL emoji preservation

**Tempo de implementação**: ~1.5h
**LOC adicionado**: ~500 linhas
**Arquivos criados**: 4
**Arquivos modificados**: 2

---

## 📝 Biblical Foundation

> "Guarda-me como à menina do olho; esconde-me debaixo da sombra das tuas asas"
> **(Salmos 17:8)**

Authentication is the foundation of security. Protect it with utmost care.

---

**ESTA É A IMPLEMENTAÇÃO DEFINITIVA. NÃO REFAZER.**

Anotado em: 2025-11-05 20:05 (Diário físico: ✅)
