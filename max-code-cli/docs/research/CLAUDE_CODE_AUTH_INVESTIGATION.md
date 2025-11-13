# Investigação Completa: Autenticação do Claude Code (CLI da Anthropic)

## Sumário Executivo

O Claude Code (CLI oficial da Anthropic) implementa autenticação de sessão sem usar API keys diretas para planos Pro/Max através de **OAuth 2.0 com PKCE (Proof Key for Code Exchange)**. A implementação armazena tokens localStorage no diretório `~/.claude/` em arquivo `.credentials.json`.

---

## 1. ARQUITETURA DE AUTENTICAÇÃO

### 1.1 Métodos de Autenticação Disponíveis

Claude Code suporta 4 tipos de autenticação:

1. **API Key Authentication** (Traditional)
   - Usa `ANTHROPIC_API_KEY` env variable
   - Header: `x-api-key: <key>`
   - Gera custos de billing imediato

2. **OAuth 2.0 com PKCE** (Para Pro/Max)
   - Usa `CLAUDE_CODE_OAUTH_TOKEN` env variable
   - Armazenado em `~/.claude/.credentials.json`
   - Token format: `sk-ant-oat01-<token>`

3. **Subscription Authentication** (Pro/Max Plans)
   - Realiza OAuth flow via browser
   - Armazena tokens localmente
   - Sem custos adicionais de API

4. **Cloud Provider Auth** (Bedrock/Vertex)
   - AWS Bedrock credentials
   - Google Vertex AI credentials

### 1.2 Prioridade de Autenticação

```
1. ANTHROPIC_API_KEY (env) ← API Key tem PRIORIDADE
2. OAuth tokens (~/.claude/.credentials.json)
3. Subscription authentication
4. Cloud provider auth
```

**Implicação:** Para usar OAuth/Subscription, remova a env var ANTHROPIC_API_KEY!

---

## 2. ESTRUTURA DE ARMAZENAMENTO DE TOKENS

### 2.1 Localização do Arquivo de Credenciais

**Linux/Ubuntu:**
```
~/.claude/.credentials.json
```

**macOS:**
```
Keychain (encrypted)
Service: "Claude Code-credentials"
```

**Windows:**
```
Windows Credential Manager
```

### 2.2 Formato do Arquivo .credentials.json

```json
{
  "claudeAiOauth": {
    "accessToken": "sk-ant-oat01-...",
    "refreshToken": "sk-ant-ort01-...",
    "expiresAt": 1234567890000,
    "scopes": ["user:inference", "user:profile"],
    "subscriptionType": "pro" | "max" | "free"
  }
}
```

### 2.3 Formato dos Tokens

| Token | Prefixo | Duração | Uso |
|-------|---------|---------|-----|
| Access Token | `sk-ant-oat01-` | 8-12 horas | Requisições API |
| Refresh Token | `sk-ant-ort01-` | ~1 ano | Renovar access token |
| Setup Token (long-lived) | `sk-ant-oat01-` | ~1 ano | CI/CD environments |

**Importante:** Tokens OAuth do Claude Code são **restritos para uso exclusivo com Claude Code**. Tentativas de usar com outras APIs retornam:
```
"This credential is only authorized for use with Claude Code and cannot be used for other API requests"
```

---

## 3. FLUXO DE AUTENTICAÇÃO OAuth 2.0 + PKCE

### 3.1 Arquitetura de Serviços

```
┌─────────────────────────────────────────────────────────────┐
│                   Claude Code CLI                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │   OAuth Service  │  │  Data/State Mgmt │               │
│  │                  │  │                  │               │
│  │- Authorization   │  │- Config files    │               │
│  │- Token exchange  │  │- Credentials     │               │
│  │- Token refresh   │  │- Session state   │               │
│  └──────────────────┘  └──────────────────┘               │
│           │                      │                         │
│           └──────────┬───────────┘                         │
│                      │                                    │
│           ┌──────────▼──────────┐                         │
│           │  Claude API Service │                         │
│           │                     │                         │
│           │ - API requests      │                         │
│           │ - Token management  │                         │
│           │ - Retries/Backoff   │                         │
│           └──────────┬──────────┘                         │
│                      │                                    │
└──────────────────────┼────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │  Anthropic API / claude.ai  │
         └─────────────────────────────┘
```

### 3.2 Fluxo de Login Interativo (/login)

```
User runs: claude
    ↓
[1] Sistema verifica ~/.claude/.credentials.json
    ↓
[2] Se não existir: Abre browser em claude.ai/oauth/authorize
    ↓
[3] Sistema inicia servidor local HTTP para receber callback
    (Default: http://localhost:5678/)
    ↓
[4] User faz login no navegador
    ↓
[5] claude.ai redireciona para: http://localhost:5678/?code=<AUTH_CODE>&state=<STATE>
    ↓
[6] CLI intercepta callback local
    ↓
[7] CLI executa token exchange (POST)
    Authorization endpoint + Auth code → Access/Refresh tokens
    ↓
[8] Salva tokens em ~/.claude/.credentials.json
    ↓
[9] CLI usa access token para requisições
```

### 3.3 Componentes da Requisição OAuth PKCE

**Fase 1: Authorization URL**
```
https://claude.ai/oauth/authorize
  ?client_id=9d1c250a-e61b-44d9-88ed-5944d1962f5e
  &redirect_uri=http://localhost:5678/callback
  &response_type=code
  &scope=user:inference user:profile
  &code_challenge=<BASE64_SHA256(code_verifier)>
  &code_challenge_method=S256
  &state=<RANDOM_STATE>
```

**Fase 2: Token Exchange (POST)**
```
POST https://console.anthropic.com/v1/oauth/token
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "code": "<AUTH_CODE_FROM_CALLBACK>",
  "client_id": "9d1c250a-e61b-44d9-88ed-5944d1962f5e",
  "code_verifier": "<ORIGINAL_CODE_VERIFIER>",
  "redirect_uri": "http://localhost:5678/callback"
}
```

**Response:**
```json
{
  "access_token": "sk-ant-oat01-...",
  "refresh_token": "sk-ant-ort01-...",
  "expires_in": 3600,
  "token_type": "Bearer",
  "scope": "user:inference user:profile"
}
```

### 3.4 Renovação de Token (Refresh)

**Endpoint:** `https://console.anthropic.com/v1/oauth/token`

**Request:**
```json
{
  "grant_type": "refresh_token",
  "refresh_token": "sk-ant-ort01-...",
  "client_id": "9d1c250a-e61b-44d9-88ed-5944d1962f5e"
}
```

**Triggers automáticos:**
- Quando access token expira
- Quando API retorna status 401
- A cada 5 minutos se token próximo de expiração

---

## 4. REQUISIÇÕES DE API COM OAUTH TOKEN

### 4.1 Headers HTTP

```http
Authorization: Bearer sk-ant-oat01-...
anthropic-version: 2023-06-01
content-type: application/json
anthropic-beta: oauth-2025-04-20
```

### 4.2 Endpoints da API

**Messages Endpoint:**
```
POST https://api.anthropic.com/v1/messages
```

**Exemplo de Request:**
```bash
curl https://api.anthropic.com/v1/messages \
  --header "Authorization: Bearer sk-ant-oat01-..." \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**IMPORTANTE:** NÃO usa header `x-api-key` quando usando OAuth!

---

## 5. VARIÁVEIS DE AMBIENTE

### 5.1 Configuração OAuth via Env Vars

```bash
# Injetar token de longa duração (gerado via setup-token)
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."

# Alternativa: Remover API key para forçar OAuth fallback
unset ANTHROPIC_API_KEY

# Resultado: Claude Code usa oauth automatically
```

### 5.2 Comando para Gerar Long-Lived Token

```bash
# Gera token válido por ~1 ano
claude setup-token

# Saída:
# Your OAuth token: sk-ant-oat01-...

# Usar em CI/CD:
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."
```

---

## 6. ESTRUTURA DE DIRETÓRIOS ~/.claude/

```
~/.claude/
├── .credentials.json          # Tokens OAuth (principal!)
├── settings.json              # User preferences
├── settings.local.json        # Local project settings
├── file-history/              # File access history
├── projects/                  # Project metadata
├── session-env/               # Session environment snapshots
├── shell-snapshots/           # Shell history snapshots
├── debug/                     # Debug logs
├── todos/                     # Task tracking
├── statsig/                   # Feature flags & analytics
└── history.jsonl              # Command history
```

**Arquivo crítico:** `~/.claude/.credentials.json` (permissões: 600)

---

## 7. IMPLEMENTAÇÕES DE REFERÊNCIA

### 7.1 Repositórios Relevantes

1. **grll/claude-code-login** (GitHub)
   - OAuth 2.0 + PKCE authentication tool
   - Linguagem: TypeScript + Bun
   - Suporta GitHub Actions
   - Armazena tokens em repository secrets

2. **sst/opencode** (GitHub)
   - OAuth implementation
   - OAuth tokens armazenados em `~/.local/share/opencode/auth.json`
   - Suporta `CLAUDE_REFRESH_TOKEN` e `CLAUDE_ACCESS_TOKEN` env vars

3. **RavenStorm-bit/claude-token-refresh** (GitHub)
   - Automatiza refresh de tokens expirados
   - Sem re-autenticação manual

4. **cabinlab/claude-code-sdk-docker**
   - Docker containers com autenticação Pro/Max
   - Suporta long-lived tokens

### 7.2 Estratégia de Replicação (Solução claude_max)

**Problema:** Claude Code `--print` mode ignora OAuth, apenas usa API key

**Solução:** Forçar fallback removendo `ANTHROPIC_API_KEY`

```bash
#!/bin/bash
# claude_max wrapper script

# Remove API key para forçar OAuth fallback
unset ANTHROPIC_API_KEY

# Usa OAuth automatically
claude "$@"
```

---

## 8. ENDPOINTS E URLs IMPORTANTES

| Endpoint | URL | Método | Uso |
|----------|-----|--------|-----|
| Authorization | `https://claude.ai/oauth/authorize` | GET | Iniciar fluxo OAuth |
| Token Exchange | `https://console.anthropic.com/v1/oauth/token` | POST | Trocar código por tokens |
| Messages API | `https://api.anthropic.com/v1/messages` | POST | Enviar mensagens |
| Callback | `http://localhost:5678/callback` | GET | Receber auth code |
| Auth Status | `claude auth status` | CLI | Verificar autenticação |

---

## 9. SCOPES OAuth

```
user:inference     # Permissão para fazer inferências (usar modelos)
user:profile       # Acessar perfil do usuário
org:create_api_key # Criar API keys (requer owner/admin)
```

---

## 10. LIMITAÇÕES E RESTRIÇÕES

### 10.1 Restrições de Tokens Claude Code

- Tokens OAuth do Claude Code são **restritos exclusivamente para Claude Code**
- Não podem ser usados em bibliotecas SDK padrão
- Não aceitam conexões diretas na API padrão

### 10.2 Timeout de Tokens

- **Access Token:** 8-12 horas
- **Refresh Token:** ~1 ano
- **Setup Token:** ~1 ano

### 10.3 Problemas Conhecidos

1. **macOS Keychain:** Requer unlock a cada sessão SSH
2. **Token Persistence:** Alguns relatos de tokens não persistindo após login bem-sucedido
3. **Autenticação remota:** WSL e SSH têm limitações com OAuth flow

---

## 11. ESTRATÉGIA DE IMPLEMENTAÇÃO PARA MAX-CODE

### 11.1 Arquitetura Recomendada

```
Max-Code Auth Module
│
├─ OAuth Flow Handler
│  ├─ Authorization URL generator
│  ├─ Local callback server (port 5678)
│  ├─ Token exchange logic
│  └─ PKCE code verifier generation
│
├─ Credential Storage
│  ├─ ~/.max-code/.credentials.json
│  ├─ Encryption on disk (if needed)
│  └─ Permission lock (600)
│
├─ Token Management
│  ├─ Auto-refresh on 401
│  ├─ Expiration check
│  ├─ Token validation
│  └─ Error handling
│
└─ API Integration
   ├─ Authorization header builder
   ├─ Request wrapper
   ├─ Retry logic
   └─ Token refresh interceptor
```

### 11.2 Passos de Implementação

1. **Setup OAuth Flow**
   - Registrar app/client ID (se necessário com Anthropic)
   - Implementar PKCE (gerador code_verifier/code_challenge)
   - Criar local callback HTTP server

2. **Token Storage**
   - JSON file com permissões restritas (mode 600)
   - Opcionalmente: encryption at rest (AES-256)
   - Backup/recovery mechanism

3. **Request Interceptor**
   - Wrapper para todas as requisições HTTP
   - Adiciona `Authorization: Bearer <token>`
   - Detecta 401 e dispara refresh

4. **CLI Commands**
   - `/login` - Inicia OAuth flow
   - `/logout` - Remove tokens
   - `auth status` - Verifica autenticação

### 11.3 Código Pseudo-Python

```python
class MaxCodeAuth:
    def __init__(self):
        self.creds_file = os.path.expanduser("~/.max-code/.credentials.json")
        self.client_id = "YOUR_CLIENT_ID"
        self.auth_endpoint = "https://claude.ai/oauth/authorize"
        self.token_endpoint = "https://console.anthropic.com/v1/oauth/token"
    
    def login(self):
        # 1. Gera PKCE
        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)
        
        # 2. Inicia callback server
        server = LocalCallbackServer(port=5678)
        
        # 3. Abre browser
        auth_url = self._build_auth_url(code_challenge)
        webbrowser.open(auth_url)
        
        # 4. Aguarda callback
        auth_code = server.wait_for_callback()
        
        # 5. Troca código por tokens
        tokens = self._exchange_code(auth_code, code_verifier)
        
        # 6. Salva credenciais
        self._save_credentials(tokens)
    
    def get_auth_header(self):
        creds = self._load_credentials()
        
        # Verifica se token expirou
        if self._is_expired(creds['expiresAt']):
            creds = self.refresh_token(creds)
        
        return {
            "Authorization": f"Bearer {creds['accessToken']}",
            "anthropic-version": "2023-06-01"
        }
    
    def refresh_token(self, creds):
        response = requests.post(
            self.token_endpoint,
            json={
                "grant_type": "refresh_token",
                "refresh_token": creds['refreshToken'],
                "client_id": self.client_id
            }
        )
        new_creds = response.json()
        self._save_credentials(new_creds)
        return new_creds
    
    def _save_credentials(self, creds):
        os.makedirs(os.path.dirname(self.creds_file), exist_ok=True)
        with open(self.creds_file, 'w') as f:
            json.dump(creds, f)
        os.chmod(self.creds_file, 0o600)
```

---

## 12. CONCLUSÕES E RECOMENDAÇÕES

### 12.1 Viabilidade

✅ **Altamente viável** replicar autenticação sem API key

**Por quê:**
- OAuth 2.0 é padrão aberto
- PKCE é amplamente documentado
- Client ID público disponível: `9d1c250a-e61b-44d9-88ed-5944d1962f5e`
- Múltiplas implementações de referência disponíveis

### 12.2 Principais Desafios

1. **Autorização do Anthropic:** Possível que o client ID esteja registrado apenas para Claude Code
   - Solução: Registrar seu próprio client ID com Anthropic

2. **Restrições de Token:** Tokens Claude Code não funcionam fora do Claude Code
   - Solução: Anthropic pode liberar restrições ou usar tokens genéricos

3. **Autenticação Remota:** OAuth callback é complicado em SSH/WSL
   - Solução: Setup token pré-gerado ou code device flow

### 12.3 Próximos Passos

1. **Contatar Anthropic** para OAuth client registration/permissions
2. **Estudar OpenCode** para referência de implementação com OAuth
3. **Implementar PKCE** como base
4. **Testar token refresh** automático
5. **Documentar escopo e limites**

---

## APÊNDICE: Comandos Úteis

```bash
# Verificar autenticação atual
claude auth status

# Fazer logout
claude logout

# Fazer login novo
claude /login

# Gerar token longa duração
claude setup-token

# Verificar arquivo de credenciais
cat ~/.claude/.credentials.json | jq .

# Testar requisição com token
export TOKEN=$(jq -r '.claudeAiOauth.accessToken' ~/.claude/.credentials.json)
curl https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":100,"messages":[{"role":"user","content":"test"}]}'

# Verificar expiração do token
cat ~/.claude/.credentials.json | jq '.claudeAiOauth.expiresAt | strftime("%Y-%m-%d %H:%M:%S")'
```

