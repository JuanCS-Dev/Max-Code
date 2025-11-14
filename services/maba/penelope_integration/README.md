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
