# Investigação Completa: Autenticação Claude Code sem API Keys

## Status da Investigação: CONCLUÍDA ✓

**Data:** 2025-11-04  
**Nível de Detalhe:** Muito Completo (Very Thorough)  
**Conclusão Principal:** TOTALMENTE VIÁVEL - OAuth 2.0 + PKCE implementável

---

## Arquivos Gerados

### 1. CLAUDE_CODE_AUTH_INVESTIGATION.md (17KB)
**Conteúdo:** Documentação técnica completa
- Arquitetura de autenticação
- Fluxo OAuth 2.0 + PKCE detalhado
- Estrutura de armazenamento de tokens
- Endpoints e URLs importantes
- Limitações críticas
- Estratégia de implementação para Max-Code
- Implementações de referência encontradas

**Uso:** Documentação base para entender a tecnologia

---

### 2. RESUMO_TECNICO_AUTH.txt (visual/ASCII)
**Conteúdo:** Resumo executivo formatado
- Conclusão principal com checkmarks
- Arquitetura visual
- Formatos e constantes
- Prioridade de autenticação
- Estrutura de .credentials.json
- Fluxo técnico passo-a-passo (10 fases)
- Implementações de referência
- Limitações críticas
- Estratégia recomendada (curto/médio/longo prazo)
- Comandos úteis
- Próximos passos com prioridades

**Uso:** Compartilhar com time, relatórios, apresentações

---

### 3. IMPLEMENTATION_GUIDE.md (código Python completo)
**Conteúdo:** Guia prático de implementação
- Arquitetura da solução
- Estrutura de arquivos recomendada
- 6 módulos implementados:
  - config.py (constantes)
  - oauth.py (fluxo completo)
  - credentials.py (storage/retrieval)
  - token_manager.py (refresh automático)
  - http_client.py (interceptor)
  - commands/login.py (CLI)
- Integração com sistema existente
- Exemplos de uso
- Unit tests
- Deployment checklist
- Troubleshooting

**Uso:** Blueprint para codificação da solução

---

## Descobertas Principais

### 1. Autenticação OAuth 2.0 + PKCE
- Implementação padrão aberta
- Não requer API key
- Funciona com Claude Pro/Max subscription
- Tokens salvos localmente em `~/.claude/.credentials.json`

### 2. Tokens Utilizados
```
Access Token:   sk-ant-oat01-...  (8-12 horas)
Refresh Token:  sk-ant-ort01-...  (~1 ano)
Setup Token:    sk-ant-oat01-...  (~1 ano, para CI/CD)
```

### 3. Endpoints Críticos
```
Authorization:  https://claude.ai/oauth/authorize
Token Exchange: https://console.anthropic.com/v1/oauth/token
API Messages:   https://api.anthropic.com/v1/messages
```

### 4. Client ID Público
```
9d1c250a-e61b-44d9-88ed-5944d1962f5e
(Registrado para Claude Code - pode exigir negociação)
```

### 5. Prioridade de Autenticação
1. `ANTHROPIC_API_KEY` (env) ← TEM PRIORIDADE
2. `CLAUDE_CODE_OAUTH_TOKEN` (env)
3. `~/.claude/.credentials.json` (arquivo)
4. Cloud provider auth (AWS/Google)

**Implicação:** Para usar OAuth, remova ANTHROPIC_API_KEY

### 6. Implementações de Referência Encontradas
1. **grll/claude-code-login** - OAuth completo em TypeScript
2. **sst/opencode** - IDE com OAuth funcional
3. **RavenStorm-bit/claude-token-refresh** - Auto-refresh
4. **cabinlab/claude-code-sdk-docker** - Docker com Pro/Max
5. **claude_max wrapper** - Remove API key para forçar OAuth

---

## Limitações Críticas

### 1. Tokens Restritos para Claude Code ⚠️
Tokens OAuth gerados para Claude Code:
- Funcionam APENAS com Claude Code
- Retornam erro se usados com SDK padrão
- **Solução:** Pedir Anthropic liberar OR registrar cliente próprio

### 2. Client ID Pode Estar Locked ⚠️
9d1c250a-e61b-44d9-88ed-5944d1962f5e:
- Pode estar registrado APENAS para Claude Code
- Outra app pode receber erro ao usar
- **Solução:** Registrar cliente próprio com Anthropic

### 3. Autenticação Remota (SSH/WSL) ⚠️
OAuth callback com servidor local:
- Não funciona bem em SSH
- WSL pode ter limitações
- **Solução:** Device flow ou setup-token pré-gerado

### 4. macOS Keychain Issues ⚠️
- Tokens em Keychain, SSH sem acesso
- Requer unlock manual por sessão
- **Solução:** File-based com encryption

### 5. Token Expiration ⚠️
- Access token: 8-12 horas
- Refresh token: ~1 ano (depois re-auth)
- **Solução:** Auto-refresh automático

---

## Viabilidade e Próximos Passos

### Curto Prazo (MVP)
1. ✓ Implementar OAuth 2.0 + PKCE (código pronto)
2. ✓ Armazenar tokens em `~/.max-code/.credentials.json`
3. ✓ Auto-refresh de tokens
4. ✓ Testar com `claude setup-token` (workaround imediato)

### Médio Prazo
1. Contatar Anthropic:
   - Registrar client_id próprio
   - Negociar token restrictions
   - Ou liberar para uso com APIs
2. Implementar device flow (SSH/WSL)
3. Suporte AWS Bedrock/Vertex fallback

### Longo Prazo
1. CLI wrapper (grll/claude-code-login style)
2. Suporte multi-plataforma (Windows/Mac/Linux)
3. Integração com IDEs (VS Code, etc)
4. Proxy server (se restrições não forem levantadas)

---

## Comandos Úteis para Teste

```bash
# Verificar token atual
cat ~/.claude/.credentials.json | jq .

# Extrair access token
jq -r '.claudeAiOauth.accessToken' ~/.claude/.credentials.json

# Gerar token longa duração
claude setup-token

# Forçar OAuth fallback
unset ANTHROPIC_API_KEY
claude /login

# Testar requisição com token
TOKEN=$(jq -r '.claudeAiOauth.accessToken' ~/.claude/.credentials.json)
curl -H "Authorization: Bearer $TOKEN" \
  https://api.anthropic.com/v1/messages \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":100,"messages":[...]}'
```

---

## Recomendações para Max-Code

### Curto Termo
- Usar `claude setup-token` como workaround (1 ano válido)
- Implementar wrapper que injeta `CLAUDE_CODE_OAUTH_TOKEN`
- Testar com usuários Pro/Max

### Médio Termo
- Implementar OAuth completo (código pronto em IMPLEMENTATION_GUIDE.md)
- Contactar Anthropic sobre permissões de token
- Registrar cliente próprio

### Longo Termo
- Suporte multi-provider (Anthropic, AWS Bedrock, Google Vertex)
- Integração com ecosistema (IDEs, CI/CD, etc)
- Proxy authentication se necessário

---

## Fontes de Pesquisa

### Documentação Oficial
- https://docs.claude.com/en/docs/claude-code/quickstart
- https://docs.claude.com/en/docs/claude-code/iam
- https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan

### Repositórios de Referência
- https://github.com/grll/claude-code-login
- https://github.com/sst/opencode
- https://github.com/RavenStorm-bit/claude-token-refresh
- https://github.com/cabinlab/claude-code-sdk-docker

### Artigos e Análises
- https://www.reidbarber.com/blog/reverse-engineering-claude-code
- https://idsc2025.substack.com/p/how-i-built-claude_max-to-unlock
- GitHub Issues (anthropics/claude-code)

---

## Contatos/Passos Recomendados

1. **Estudar Implementation Guide** (IMPLEMENTATION_GUIDE.md)
2. **Revisar claude-code-login** (referência TypeScript)
3. **Contactar Anthropic:**
   - Email: support@anthropic.com
   - Assunto: "OAuth Client Registration for Max-Code"
   - Perguntar sobre: client_id registro + token restrictions lifting
4. **Implementar MVP** com setup-token como fallback
5. **Testar com Max subscribers**

---

## Status Final

✅ **Investigação Concluída**  
✅ **Documentação Completa Gerada**  
✅ **Código de Referência Pronto**  
✅ **Limitações Mapeadas**  
✅ **Próximos Passos Claros**  

**Recomendação:** Começar implementação imediatamente com código em IMPLEMENTATION_GUIDE.md

---

Gerado: 2025-11-04  
Investigador: Claude Code Analysis System  
Arquivos: 3 documentos (17KB + guia de código)
