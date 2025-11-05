# FASE 2: Anthropic SDK Patterns - Especificação Completa

**Data**: 2025-11-05
**Status**: 📋 ESPECIFICAÇÃO VALIDADA
**Fonte**: Documentação oficial Anthropic SDK 2025

---

## 🎯 OBJETIVO DA FASE 2

Implementar padrões do Anthropic Claude Agent SDK para alcançar:
- Paridade com Anthropic SDK oficial
- API limpa e Pythônica
- Lifecycle management determinístico
- Integração com ecossistema MCP

**Tempo estimado**: 18-24h (32h total acumulado)

---

## 2.1 @tool DECORATOR PATTERN (4h)

### Padrão Oficial Anthropic

**Python SDK** usa `@beta_tool`:
```python
from anthropic import Anthropic, beta_tool

@beta_tool
def get_weather(location: str) -> str:
    """Lookup the weather for a given city

    Args:
        location: The city and state, e.g. San Francisco, CA

    Returns:
        A dictionary containing the location, temperature, and weather condition.
    """
    # Implementation
    return {"location": location, "temp": 72, "condition": "sunny"}
```

**Claude Agent SDK** usa `@tool`:
```python
from claude_agent_sdk import tool

@tool("greet", "Greet a user", {"name": str})
async def greet_user(args):
    return {
        "content": [{
            "type": "text",
            "text": f"Hello, {args['name']}!"
        }]
    }
```

### O que implementar no Max-Code

1. **Decorator `@tool`**:
   - Nome, descrição, schema (dict ou Pydantic)
   - Type hints automáticos
   - Validação de input com Pydantic
   - Return type padronizado: `{"content": [{"type": "text", "text": "..."}]}`

2. **Registry System**:
   - Registro automático de tools ao usar decorator
   - Listagem de tools disponíveis
   - Tool discovery dinâmico

3. **Error Handling**:
   - Try/except automático
   - Return errors no formato padrão
   - Logging estruturado

### Estrutura de Arquivos

```
core/tools/
├── __init__.py
├── decorator.py          # @tool decorator
├── registry.py           # Tool registry
└── types.py              # ToolResult, ToolSchema
```

### Exemplo de Uso Final

```python
from core.tools import tool

@tool(
    name="read_file",
    description="Read contents of a file",
    schema={"path": str, "encoding": str}
)
async def read_file(args):
    path = args["path"]
    encoding = args.get("encoding", "utf-8")

    try:
        with open(path, "r", encoding=encoding) as f:
            content = f.read()
        return {
            "content": [{
                "type": "text",
                "text": f"File contents:\n{content}"
            }]
        }
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error reading file: {e}"
            }]
        }
```

---

## 2.2 HOOKS SYSTEM (6h)

### Padrão Oficial Anthropic

Claude Code hooks são comandos shell que executam em lifecycle events:

**Tipos de Hooks** (8 eventos):
1. **PreToolUse** - Antes de tool calls (PODE BLOQUEAR)
2. **PostToolUse** - Após tool calls (não bloqueia)
3. **UserPromptSubmit** - Quando usuário submete prompt
4. **Notification** - Quando Claude envia notificações
5. **Stop** - Quando Claude termina resposta
6. **SubagentStop** - Quando subagent Task termina
7. **PreCompact** - Antes de compaction
8. **SessionStart** - Início ou resumo de sessão
9. **SessionEnd** - Fim de sessão

### Configuração (settings.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Running bash command' >> ~/.claude/log.txt"
          }
        ]
      }
    ]
  }
}
```

### O que implementar no Max-Code

1. **Hook Events Enum**:
```python
from enum import Enum

class HookEvent(str, Enum):
    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    NOTIFICATION = "Notification"
    STOP = "Stop"
    SUBAGENT_STOP = "SubagentStop"
    PRE_COMPACT = "PreCompact"
    SESSION_START = "SessionStart"
    SESSION_END = "SessionEnd"
```

2. **Hook Manager**:
```python
class HookManager:
    def __init__(self, config_path: str):
        self.hooks = self._load_hooks(config_path)

    async def trigger(self, event: HookEvent, payload: dict) -> HookResult:
        """
        Trigger hooks for event.

        Returns:
            HookResult with success/failure and optional blocking
        """
        pass

    def register_hook(self, event: HookEvent, matcher: str, command: str):
        """Register hook programmatically"""
        pass
```

3. **Blocking Logic** (PreToolUse):
   - Exit code 0: Allow execution
   - Exit code != 0: Block execution, pass feedback to LLM

4. **Payload Structure**:
```python
@dataclass
class HookPayload:
    event: HookEvent
    tool_name: Optional[str] = None
    tool_input: Optional[dict] = None
    tool_response: Optional[dict] = None
    session_info: Optional[dict] = None
    source: Optional[str] = None  # "startup", "resume", "clear"
```

### Estrutura de Arquivos

```
core/hooks/
├── __init__.py
├── manager.py            # HookManager
├── types.py              # HookEvent, HookPayload, HookResult
└── executor.py           # Shell command executor
```

### Exemplo de Uso

```python
from core.hooks import HookManager, HookEvent

hook_manager = HookManager("~/.max-code/settings.json")

# Register hook programmatically
hook_manager.register_hook(
    event=HookEvent.PRE_TOOL_USE,
    matcher="Bash",
    command="echo 'Bash command: $TOOL_INPUT' >> ~/log.txt"
)

# Trigger hook
result = await hook_manager.trigger(
    event=HookEvent.PRE_TOOL_USE,
    payload={
        "tool_name": "Bash",
        "tool_input": {"command": "ls -la"}
    }
)

if not result.allow_execution:
    print(f"Hook blocked execution: {result.feedback}")
```

---

## 2.3 AUTO CONTEXT COMPACTION (8h)

### Padrão Anthropic

Claude Code auto-compacta quando contexto atinge ~75% (trigger configur

ável).

**Comportamento**:
1. Monitor context usage continuously
2. Trigger compaction at threshold (default: 75-80%)
3. Compress to ~50% using LLM summarization
4. Reserve 20% for compaction process

**User Issues 2025**:
- Users want configurável threshold
- Avoid premature compaction (waste tokens)
- Allow manual trigger

### O que implementar no Max-Code

1. **Context Monitor**:
```python
class ContextMonitor:
    def __init__(self, max_tokens: int = 200000, compact_threshold: float = 0.75):
        self.max_tokens = max_tokens
        self.compact_threshold = compact_threshold
        self.current_usage = 0

    def add_tokens(self, count: int):
        """Add tokens to current context"""
        self.current_usage += count

    def should_compact(self) -> bool:
        """Check if compaction should trigger"""
        return (self.current_usage / self.max_tokens) >= self.compact_threshold

    def get_usage_percent(self) -> float:
        """Get current usage percentage"""
        return (self.current_usage / self.max_tokens) * 100
```

2. **Context Compactor**:
```python
class ContextCompactor:
    async def compact(self, messages: List[Message], target_ratio: float = 0.5) -> List[Message]:
        """
        Compact context to target_ratio of current size.

        Uses LLM to summarize older messages while keeping recent intact.
        """
        # Keep last 20% of messages untouched (recent context)
        # Summarize middle 60% using LLM
        # Keep first 20% (important context like system prompt)
        pass
```

3. **Integration with Hooks**:
   - Trigger `PreCompact` hook before compaction
   - Allow user confirmation (if configured)
   - Log compaction events

### Estrutura de Arquivos

```
core/context/
├── __init__.py
├── monitor.py            # ContextMonitor
├── compactor.py          # ContextCompactor
└── strategies.py         # Compaction strategies (LLM summary, truncate, etc)
```

---

## 2.4 STREAMING SUPPORT (6h)

### Padrão Anthropic

**Agent SDK** retorna AsyncIterator:
```python
async for message in query(prompt="Hello"):
    print(message)
```

**Bidirectional streaming**:
```python
async with ClaudeSDKClient() as client:
    await client.query(message_stream())
    async for message in client.receive_response():
        print(message)
```

**Anthropic SDK** com `client.messages.stream()`:
```python
async with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Say hello!"}],
    model="claude-sonnet-4-5-20250929",
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
```

### O que implementar no Max-Code

1. **Async Agent Interface**:
```python
class StreamingAgent:
    async def execute_streaming(self, task: Task) -> AsyncIterator[Message]:
        """
        Execute task with streaming response.

        Yields messages as they arrive from LLM.
        """
        async for chunk in self._stream_llm_response(task):
            yield Message(
                role="assistant",
                content=chunk,
                timestamp=datetime.now()
            )
```

2. **Bidirectional Streaming**:
```python
async def interactive_conversation():
    async with AgentClient() as client:
        # Send streaming input
        await client.query(input_generator())

        # Receive streaming output
        async for message in client.receive_response():
            process_message(message)
```

3. **Integration with UI**:
   - Update Rich console in real-time
   - Progress bars for long operations
   - Token-by-token display

### Estrutura de Arquivos

```
core/streaming/
├── __init__.py
├── agent.py              # StreamingAgent
├── client.py             # Bidirectional client
└── ui.py                 # Streaming UI components
```

---

## 2.5 MCP INTEGRATION (8h)

### O que é MCP

**Model Context Protocol**: Open standard da Anthropic para conectar AI assistants a sistemas externos.

**Benefícios**:
- Integração padronizada (GitHub, Slack, Google Drive, Asana)
- Anthropic API gerencia conexões/auth automaticamente
- Sem código custom de integração
- OAuth flows gerenciados

### Padrão Anthropic

**Criar MCP Server**:
```typescript
const customServer = createSdkMcpServer({
  name: "my-custom-tools",
  version: "1.0.0",
  tools: [/* tool definitions */]
});
```

**API Anthropic** gerencia:
- Connection management
- Tool discovery
- Error handling
- Authentication (OAuth)

### O que implementar no Max-Code

1. **MCP Client**:
```python
class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.tools = {}

    async def connect(self):
        """Connect to MCP server and discover tools"""
        self.tools = await self._discover_tools()

    async def call_tool(self, tool_name: str, args: dict) -> dict:
        """Call remote MCP tool"""
        pass
```

2. **MCP Server** (para expor tools locais):
```python
class MCPServer:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools = []

    def register_tool(self, tool_func):
        """Register local tool for remote access"""
        pass

    async def serve(self, port: int):
        """Start MCP server"""
        pass
```

3. **Integrações Pre-built**:
   - GitHub (issues, PRs, commits)
   - Slack (messages, channels)
   - File systems (local, cloud)
   - Databases (PostgreSQL, MongoDB)

### Estrutura de Arquivos

```
core/mcp/
├── __init__.py
├── client.py             # MCP client
├── server.py             # MCP server
├── discovery.py          # Tool discovery
└── integrations/
    ├── github.py
    ├── slack.py
    └── filesystem.py
```

---

## 📊 ESTIMATIVAS DETALHADAS

| Tarefa | Tempo | Arquivos | LOC Est. | Complexidade |
|--------|-------|----------|----------|--------------|
| **2.1 @tool decorator** | 4h | 3 | ~400 | Média |
| **2.2 Hooks system** | 6h | 4 | ~600 | Alta |
| **2.3 Context compaction** | 8h | 4 | ~800 | Alta |
| **2.4 Streaming** | 6h | 3 | ~500 | Média |
| **2.5 MCP integration** | 8h | 6+ | ~1000 | Alta |
| **TOTAL** | **32h** | **20** | **~3300** | - |

---

## 🎯 ORDEM DE IMPLEMENTAÇÃO

### Semana 1 (16h)
1. **2.1 @tool decorator** (4h) - Base para tudo
2. **2.4 Streaming** (6h) - UX crítico
3. **2.2 Hooks** (6h) - Lifecycle management

### Semana 2 (16h)
4. **2.3 Context compaction** (8h) - Evita overflows
5. **2.5 MCP integration** (8h) - Ecosystem integration

---

## ✅ CRITÉRIOS DE SUCESSO

Cada implementação deve ter:
- ✅ Código production-grade (error handling, logging, types)
- ✅ Testes unitários (pytest)
- ✅ Documentação (docstrings + examples)
- ✅ Compatibilidade com padrão Anthropic
- ✅ Integration tests

---

## 📚 REFERÊNCIAS

- [Anthropic SDK Python](https://github.com/anthropics/anthropic-sdk-python)
- [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python)
- [Custom Tools - Claude Docs](https://docs.claude.com/en/docs/claude-code/sdk/custom-tools)
- [Hooks Guide - Claude Docs](https://docs.claude.com/en/docs/claude-code/hooks-guide)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [MCP - Claude Docs](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)

---

**Status**: ✅ ESPECIFICAÇÃO COMPLETA
**Próximo passo**: Começar implementação 2.1 (@tool decorator)
