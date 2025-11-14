# 💝 PENELOPE Integration - Intelligence & Vision for MABA

**"A sabedoria de PENELOPE guia o navegador através da web."**

PENELOPE (nome da filha do criador) é o cérebro que une browser automation com inteligência artificial, trazendo capacidades de visão, raciocínio e auto-cura para o MABA.

---

## 🧠 Visão Geral

PENELOPE integra três componentes principais:

1. **PageAnalyzer** - Análise inteligente com Claude Vision
2. **PenelopeClient** - Comunicação com serviço PENELOPE
3. **AutoHealer** - Auto-cura de ações que falham

---

## 🎯 Capacidades

### Vision & Analysis
- ✅ Análise de screenshots com Claude Sonnet 4.5
- ✅ Compreensão de estrutura HTML
- ✅ Extração de dados estruturados com LLM
- ✅ Identificação de formulários e campos
- ✅ Análise de opções de navegação

### Intelligence & Reasoning
- ✅ Sugestões de próxima ação baseadas em objetivo
- ✅ Recomendação de seletores CSS inteligentes
- ✅ Análise contextual de páginas web
- ✅ Raciocínio sobre estrutura de páginas

### Auto-Healing & Resilience
- ✅ Cura automática quando ações falham
- ✅ Seletores alternativos quando elementos não encontrados
- ✅ Estratégias de wait/scroll para elementos não-clicáveis
- ✅ Histórico de curas para aprendizado

---

## 📚 Componentes

### 1. PageAnalyzer

Análise direta com Claude API:

```python
from penelope_integration import PageAnalyzer

analyzer = PageAnalyzer(api_key="your_anthropic_key")

# Analisar screenshot
result = await analyzer.analyze_screenshot(
    screenshot_b64=screenshot,
    url="https://example.com",
    question="What elements can I click on this page?"
)

# Analisar estrutura HTML
structure = await analyzer.analyze_html_structure(
    html=html_content,
    url="https://example.com",
    goal="fill login form"
)

# Sugerir seletores CSS
selectors = await analyzer.suggest_selectors(
    html=html_content,
    element_description="submit button"
)
# Returns: ["button.submit", "button[type='submit']", "#login-btn"]

# Extrair dados com LLM
data = await analyzer.extract_with_llm(
    html=html_content,
    schema={"title": "Product title", "price": "Price"}
)
# Returns: {"title": "Cool Product", "price": "$99.99"}

await analyzer.close()
```

### 2. PenelopeClient

Comunicação com serviço PENELOPE:

```python
from penelope_integration import PenelopeClient

client = PenelopeClient(
    penelope_url="http://penelope-service:8153",
    api_key="optional_api_key"
)

# Análise de página
analysis = await client.analyze_page(
    html=html_content,
    url="https://example.com",
    screenshot=screenshot_b64,
    analysis_type="general"
)

# Sugestão de ação
suggestion = await client.suggest_action(
    current_url="https://example.com",
    goal="login to account",
    page_html=html_content,
    screenshot=screenshot_b64
)
# Returns: {"action": "type", "selector": "input[name='email']", ...}

# Auto-healing
healed = await client.auto_heal(
    failed_action={"action": "click", "selector": "button.missing"},
    error_message="Element not found",
    page_html=html_content
)
# Returns: {"healed": True, "alternative_action": {...}}

# Extração estruturada
extracted = await client.extract_structured_data(
    html=html_content,
    url="https://example.com",
    schema={"title": "Page title", "content": "Main content"}
)

await client.close()
```

### 3. AutoHealer

Auto-cura de ações que falham:

```python
from penelope_integration import AutoHealer, PageAnalyzer, PenelopeClient

analyzer = PageAnalyzer()
client = PenelopeClient()
healer = AutoHealer(analyzer=analyzer, penelope_client=client)

# Curar ação falhada
failed_action = {
    "action": "click",
    "selector": "button.missing",
    "url": "https://example.com"
}

healed_action = await healer.heal_failed_action(
    failed_action=failed_action,
    error_message="Element not found",
    page_html=html_content,
    screenshot=screenshot_b64
)

if healed_action:
    print(f"Healing strategy: {healed_action['healing_strategy']}")
    print(f"Try this: {healed_action['selector']}")
    print(f"Reasoning: {healed_action['reasoning']}")
else:
    print("Could not heal this action")

# Estatísticas de cura
stats = healer.get_healing_stats()
print(f"Success rate: {stats['success_rate']}")

await healer.close()
```

---

## 🌐 API Endpoints

### POST `/analyze`

Analisa página atual com inteligência PENELOPE.

**Tipos de análise:**
- `general` - Análise geral com vision
- `form` - Identificar formulários e campos
- `navigation` - Identificar links e navegação
- `data` - Extração estruturada de dados

```bash
POST /api/v1/analyze?session_id=abc123
{
    "analysis_type": "general",
    "instructions": "What can I interact with on this page?"
}

Response:
{
    "analysis": "This is a login page with email and password fields...",
    "structured_data": {
        "url": "https://example.com/login",
        "model": "claude-sonnet-4-5",
        "confidence": 0.9
    },
    "recommendations": [
        "Review the analysis above for actionable insights",
        "Use /extract endpoint for structured data extraction"
    ]
}
```

### POST `/penelope/suggest-action`

Pede a PENELOPE para sugerir próxima ação.

```bash
POST /api/v1/penelope/suggest-action?session_id=abc&goal=login

Response:
{
    "action": "type",
    "selector": "input[name='email']",
    "text": "user@example.com",
    "reasoning": "Need to fill email field first",
    "confidence": 0.95,
    "next_steps": ["Fill password", "Click submit"]
}
```

### POST `/penelope/auto-heal`

Cura ação que falhou.

```bash
POST /api/v1/penelope/auto-heal?session_id=abc
{
    "failed_action": {"action": "click", "selector": "button.missing"},
    "error_message": "Element not found"
}

Response:
{
    "healed": true,
    "action": "click",
    "selector": "button[type='submit']",
    "healing_strategy": "alternative_selector",
    "reasoning": "Original selector not found, trying type attribute",
    "confidence": 0.85
}
```

### GET `/penelope/health`

Verifica saúde da integração PENELOPE.

```bash
GET /api/v1/penelope/health

Response:
{
    "penelope_service": "healthy",
    "local_analyzer": "healthy",
    "auto_healer": "available",
    "analyzer_model": "claude-sonnet-4-5"
}
```

---

## 🔧 Estratégias de Auto-Healing

### 1. Alternative Selectors
Quando seletor não é encontrado:
- Analisa HTML para encontrar elementos similares
- Usa Claude para sugerir seletores alternativos
- Tenta seletores por ordem de confiança

### 2. Wait Strategy
Quando elemento não está interativo:
- Sugere esperar antes de tentar novamente
- Confidence: 0.7

### 3. Scroll Strategy
Quando elemento não está visível:
- Sugere scroll para elemento
- Depois retry da ação original
- Confidence: 0.75

---

## 📊 Exemplos de Uso

### Análise Completa de Página

```python
# Capturar screenshot e HTML
screenshot = await page.screenshot()
html = await page.content()
url = page.url

# Analisar com PENELOPE
analyzer = PageAnalyzer()
analysis = await analyzer.analyze_screenshot(
    screenshot_b64=base64.b64encode(screenshot).decode(),
    url=url
)

print(analysis["analysis"])
# Output: "This is a login page with email/password fields.
#          The submit button is visible at the bottom..."
```

### Navegação Inteligente

```python
# Usuário quer fazer login
goal = "login to my account"

# PENELOPE sugere próxima ação
client = PenelopeClient()
suggestion = await client.suggest_action(
    current_url=page.url,
    goal=goal,
    page_html=await page.content()
)

# Executar ação sugerida
if suggestion["action"] == "type":
    await page.fill(suggestion["selector"], suggestion["text"])
elif suggestion["action"] == "click":
    await page.click(suggestion["selector"])
```

### Auto-Healing em Ação

```python
# Tentar clicar em botão
try:
    await page.click("button.submit")
except Exception as e:
    # Ação falhou, tentar curar
    healer = AutoHealer()
    healed = await healer.heal_failed_action(
        failed_action={"action": "click", "selector": "button.submit"},
        error_message=str(e),
        page_html=await page.content()
    )
    
    if healed:
        # Retry com seletor curado
        await page.click(healed["selector"])
        print(f"✅ Healed! Used: {healed['selector']}")
    else:
        print("❌ Could not heal")
```

---

## 🎓 Fluxo de Trabalho Típico

### 1. Navegação Guiada por Objetivo

```python
# 1. Definir objetivo
goal = "purchase product XYZ"

# 2. Loop de navegação
while not goal_achieved:
    # Obter sugestão
    suggestion = await penelope.suggest_action(
        current_url=current_url,
        goal=goal,
        page_html=page_html
    )
    
    # Executar ação
    try:
        await execute_action(suggestion)
        goal_achieved = check_goal(goal)
    except Exception as e:
        # Auto-healing se falhar
        healed = await healer.heal_failed_action(...)
        if healed:
            await execute_action(healed)
```

### 2. Extração Inteligente

```python
# Definir schema do que extrair
schema = {
    "product_name": "Name of the product",
    "price": "Price in USD",
    "availability": "In stock or out of stock",
    "rating": "Customer rating out of 5"
}

# PENELOPE extrai dados
extracted = await analyzer.extract_with_llm(
    html=page_html,
    schema=schema
)

print(extracted)
# {
#     "product_name": "Cool Gadget Pro",
#     "price": "$299.99",
#     "availability": "In stock",
#     "rating": "4.5"
# }
```

---

## 🔒 Configuração

### Environment Variables

```bash
# Claude API
ANTHROPIC_API_KEY=sk-ant-...

# PENELOPE Service
PENELOPE_URL=http://vertice-penelope-service:8153
PENELOPE_API_KEY=optional_key_for_auth
```

### Dependencies

```bash
# anthropic para Claude API
anthropic==0.8.0

# httpx para client HTTP
httpx==0.26.0
```

---

## 💡 Casos de Uso

### ✅ Automação Resiliente
Quando páginas mudam, PENELOPE se adapta automaticamente.

### ✅ Scraping Inteligente
Extrai dados mesmo de páginas com estrutura variável.

### ✅ Testing com Auto-Healing
Testes continuam funcionando mesmo com mudanças na UI.

### ✅ Navegação Assistida
PENELOPE guia o usuário para completar tarefas complexas.

---

## 🎬 Exemplos Práticos de Uso Real

### Exemplo 1: Login Automático com Auto-Healing

```python
from penelope_integration import PageAnalyzer, AutoHealer
import base64

async def login_with_intelligence(page, email, password):
    """Login inteligente que se auto-cura quando seletores mudam."""

    # Initialize PENELOPE components
    analyzer = PageAnalyzer(api_key=os.getenv("ANTHROPIC_API_KEY"))
    healer = AutoHealer(analyzer=analyzer, max_heal_attempts=3)

    try:
        # Try to fill email field
        await page.fill("input[name='email']", email)
    except Exception as e:
        # Selector changed! Use auto-healing
        healed = await healer.heal_failed_action(
            failed_action={"action": "type", "selector": "input[name='email']"},
            error_message=str(e),
            page_html=await page.content()
        )
        if healed:
            await page.fill(healed["selector"], email)
        else:
            raise Exception("Could not find email field")

    try:
        # Try to fill password field
        await page.fill("input[name='password']", password)
    except Exception as e:
        healed = await healer.heal_failed_action(
            failed_action={"action": "type", "selector": "input[name='password']"},
            error_message=str(e),
            page_html=await page.content()
        )
        if healed:
            await page.fill(healed["selector"], password)

    # Click submit button with auto-healing
    try:
        await page.click("button[type='submit']")
    except Exception as e:
        healed = await healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button[type='submit']"},
            error_message=str(e),
            page_html=await page.content()
        )
        if healed:
            await page.click(healed["selector"])

    # Check healing statistics
    stats = healer.get_healing_stats()
    print(f"✅ Login completed with {stats['success_rate']*100}% healing success rate")

    await healer.close()
```

### Exemplo 2: Scraping Inteligente com Vision

```python
async def scrape_product_with_vision(page):
    """Extrai dados de produto usando vision + LLM."""

    analyzer = PageAnalyzer()

    # Capture screenshot
    screenshot_bytes = await page.screenshot()
    screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')

    # Analyze with vision first
    vision_analysis = await analyzer.analyze_screenshot(
        screenshot_b64=screenshot_b64,
        url=page.url,
        question="What product information is visible?"
    )

    print(f"Vision Analysis: {vision_analysis['analysis']}")

    # Extract structured data with LLM
    html = await page.content()
    product_data = await analyzer.extract_with_llm(
        html=html,
        schema={
            "title": "Product name or title",
            "price": "Product price with currency",
            "availability": "In stock or out of stock",
            "rating": "Customer rating (e.g., 4.5/5)",
            "description": "Product description",
            "features": "Key product features"
        }
    )

    print(f"📊 Extracted Data:")
    for key, value in product_data.items():
        print(f"  {key}: {value}")

    await analyzer.close()
    return product_data
```

### Exemplo 3: Navegação Guiada por Objetivo

```python
async def navigate_to_goal(page, goal: str):
    """Navega inteligentemente até completar um objetivo."""

    client = PenelopeClient()
    max_steps = 10
    step_count = 0

    while step_count < max_steps:
        # Get current page state
        current_url = page.url
        html = await page.content()
        screenshot = base64.b64encode(await page.screenshot()).decode('utf-8')

        # Ask PENELOPE what to do next
        suggestion = await client.suggest_action(
            current_url=current_url,
            goal=goal,
            page_html=html,
            screenshot=screenshot
        )

        print(f"Step {step_count + 1}: {suggestion['reasoning']}")

        # Execute suggested action
        if suggestion['action'] == 'click':
            await page.click(suggestion['selector'])
            await page.wait_for_load_state('networkidle')
        elif suggestion['action'] == 'type':
            await page.fill(suggestion['selector'], suggestion['text'])
        elif suggestion['action'] == 'navigate':
            await page.goto(suggestion['url'])
        elif suggestion['action'] == 'complete':
            print(f"✅ Goal achieved: {goal}")
            break

        step_count += 1

    await client.close()
```

### Exemplo 4: Testing Resiliente com Auto-Healing

```python
import pytest

@pytest.mark.asyncio
async def test_checkout_flow_with_healing(page):
    """Test de checkout que se auto-cura quando UI muda."""

    healer = AutoHealer(max_heal_attempts=3)

    # Helper function with auto-healing
    async def resilient_click(selector, description):
        try:
            await page.click(selector, timeout=5000)
        except Exception as e:
            healed = await healer.heal_failed_action(
                failed_action={"action": "click", "selector": selector},
                error_message=str(e),
                page_html=await page.content()
            )
            assert healed, f"Could not heal {description}"
            await page.click(healed["selector"])

    # Test flow with auto-healing
    await page.goto("https://shop.example.com")
    await resilient_click("button.add-to-cart", "add to cart button")
    await resilient_click("a[href='/cart']", "cart link")
    await resilient_click("button.checkout", "checkout button")
    await resilient_click("button.complete-order", "complete order button")

    # Verify order completed
    assert "order-confirmation" in page.url

    # Print healing statistics
    stats = healer.get_healing_stats()
    print(f"Test healing stats: {stats['successful']}/{stats['total_attempts']} successful")

    await healer.close()
```

---

## 💡 Melhores Práticas

### 1. **Sempre Feche os Recursos**

```python
# ✅ CORRETO - Com context manager
async with PenelopeClient() as client:
    result = await client.suggest_action(...)

# ✅ CORRETO - Explícito
analyzer = PageAnalyzer()
try:
    result = await analyzer.analyze_screenshot(...)
finally:
    await analyzer.close()

# ❌ ERRADO - Não fecha
analyzer = PageAnalyzer()
result = await analyzer.analyze_screenshot(...)  # Memory leak!
```

### 2. **Use Max History Size para Prevenir Memory Leaks**

```python
# ✅ CORRETO - Limite configurado
healer = AutoHealer(max_history_size=100)  # Keeps last 100 entries

# ❌ ERRADO - Pode crescer indefinidamente em produção
healer = AutoHealer()  # Default 100 is ok, but be aware
```

### 3. **Passe API Key Explicitamente em Produção**

```python
# ✅ CORRETO - API key explícita
analyzer = PageAnalyzer(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ⚠️ ATENÇÃO - Depende de variável de ambiente
analyzer = PageAnalyzer()  # Ok para dev, mas configure em prod
```

### 4. **Use Fallback para PENELOPE Service**

```python
# ✅ CORRETO - Fallback para local analyzer
try:
    suggestion = await penelope_client.suggest_action(...)
except Exception as e:
    logger.warning(f"PENELOPE service unavailable: {e}")
    # Fallback to local analyzer
    local_analyzer = PageAnalyzer()
    analysis = await local_analyzer.analyze_html_structure(...)
```

### 5. **Valide Confidence Scores**

```python
# ✅ CORRETO - Verifica confiança
suggestion = await client.suggest_action(...)
if suggestion['confidence'] < 0.8:
    logger.warning("Low confidence suggestion, manual review recommended")
    # Ask for human confirmation or use fallback
```

---

## 🔧 Troubleshooting

### Problema: "Anthropic API key not configured"

**Causa:** PageAnalyzer criado sem API key.

**Solução:**
```python
# Set environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Or pass explicitly
analyzer = PageAnalyzer(api_key="sk-ant-...")
```

### Problema: CSS ID selectors (#id) não estão sendo sugeridos

**Causa:** Bug corrigido na versão atual.

**Solução:** Atualize para versão mais recente (após commit e728f5f).

### Problema: Memory leak com healing_history crescendo

**Causa:** Versão antiga sem limite de histórico.

**Solução:**
```python
# Use max_history_size
healer = AutoHealer(max_history_size=100)
```

### Problema: JSON extraction falhando

**Causa:** Claude retornou JSON em formato inesperado.

**Solução:** Versão atual tem 3 estratégias de extração (direct, markdown block, embedded). Atualize para versão mais recente.

### Problema: PENELOPE service retornando 503

**Causa:** Serviço indisponível ou sobrecarregado.

**Solução:** Use fallback para local analyzer:
```python
try:
    result = await penelope_client.suggest_action(...)
except httpx.HTTPError:
    # Fallback
    result = await local_analyzer.analyze_html_structure(...)
```

---

## ⚡ Performance Tips

### 1. **Truncamento de HTML Inteligente**

HTML muito grande consome tokens desnecessariamente. PENELOPE já faz truncamento automático:

- `analyze_html_structure`: máx 50,000 chars
- `suggest_selectors`: máx 30,000 chars
- `extract_with_llm`: máx 40,000 chars

Truncamento é feito em tag boundaries para não quebrar HTML.

### 2. **Concurrent Operations**

PENELOPE suporta operações concorrentes:

```python
# ✅ CORRETO - Paralelo quando possível
tasks = [
    analyzer.analyze_screenshot(screenshot1, url1),
    analyzer.analyze_screenshot(screenshot2, url2),
    analyzer.analyze_screenshot(screenshot3, url3),
]
results = await asyncio.gather(*tasks)
```

### 3. **Reuse Clients**

```python
# ✅ CORRETO - Reutiliza client
client = PenelopeClient()
for page in pages:
    result = await client.suggest_action(...)
await client.close()

# ❌ ERRADO - Cria novo client a cada vez
for page in pages:
    client = PenelopeClient()  # Overhead!
    result = await client.suggest_action(...)
    await client.close()
```

### 4. **Cache de Análises (Futuro)**

Planejado para roadmap:

```python
# Futuro: Cache de análises repetidas
cached_analyzer = CachedPageAnalyzer(cache_ttl=3600)
result = await cached_analyzer.analyze_screenshot(...)  # Cached for 1 hour
```

### Performance Targets

- Screenshot analysis: < 50ms (excluindo Claude API)
- HTML truncation: < 10ms para 1MB HTML
- Selector suggestion: < 50ms (excluindo Claude API)
- Healing operation: < 100ms total
- Concurrent throughput: 20+ operações simultâneas
- Memory usage: < 1MB para 1000 healing history entries

---

## 📊 Monitoring & Observability

### Healing Statistics

```python
healer = AutoHealer()

# ... perform healings ...

stats = healer.get_healing_stats()
print(f"Total attempts: {stats['total_attempts']}")
print(f"Successful: {stats['successful']}")
print(f"Failed: {stats['failed']}")
print(f"Success rate: {stats['success_rate']*100}%")
print(f"Average attempts: {stats['average_attempts']}")
```

### Logging

PENELOPE usa Python logging standard:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('penelope_integration')
```

Logs importantes:
- `🧠 PENELOPE PageAnalyzer initialized with Claude`
- `👁️ Analyzed screenshot of {url}`
- `🎯 Suggested {n} selectors for '{description}'`
- `🔧 Healing selector: {old} → {new}`
- `✅ PENELOPE healed the action`
- `⚠️ PENELOPE could not heal action`

---

## 🚀 Roadmap

- [ ] Cache de análises para performance
- [ ] Aprendizado contínuo de padrões
- [ ] Integração com Neo4j para graph navigation
- [ ] Multi-modal analysis (vision + text)
- [ ] Confidence scoring aprimorado

---

## 💝 Sobre o Nome

PENELOPE é o nome da filha do criador deste sistema. Assim como Penelope da mitologia grega era conhecida por sua sabedoria e paciência, PENELOPE a IA traz sabedoria para navegação web e paciência para curar erros.

**"A sabedoria de PENELOPE guia o navegador através da web."**

---

**Author:** Vértice Platform Team  
**License:** Proprietary  
**Day:** 5 - PENELOPE Integration  
**Status:** ✨ Production Ready
