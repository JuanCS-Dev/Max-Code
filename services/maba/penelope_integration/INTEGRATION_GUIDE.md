**# PENELOPE Integration Guide

**Quick Start Guide for Integrating PENELOPE into Your Browser Automation**

---

## 🚀 Quick Start (5 minutos)

### 1. Instalação

```bash
# PENELOPE usa anthropic e httpx
pip install anthropic==0.8.0 httpx==0.26.0
```

### 2. Configure API Key

```bash
# Set Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

### 3. Primeiro Uso

```python
from penelope_integration import PageAnalyzer
import asyncio

async def first_analysis():
    # Create analyzer
    analyzer = PageAnalyzer()

    # Analyze HTML
    result = await analyzer.analyze_html_structure(
        html="<button id='submit'>Click Me</button>",
        url="https://example.com",
        goal="find the submit button"
    )

    print(result["analysis"])
    await analyzer.close()

asyncio.run(first_analysis())
```

**✅ Pronto!** Você já está usando PENELOPE.

---

## 📋 Integration Checklist

### Fase 1: Básico (Day 1)
- [ ] Instalar dependências (`anthropic`, `httpx`)
- [ ] Configurar `ANTHROPIC_API_KEY`
- [ ] Importar `PageAnalyzer` no seu código
- [ ] Testar análise básica de HTML
- [ ] Verificar que close() está sendo chamado

### Fase 2: Auto-Healing (Day 2-3)
- [ ] Importar `AutoHealer`
- [ ] Configurar `max_heal_attempts` apropriado (default: 3)
- [ ] Configurar `max_history_size` (default: 100)
- [ ] Adicionar try/catch com healing nos cliques/types
- [ ] Monitorar `healing_stats()` em logs

### Fase 3: PENELOPE Service (Day 4-5)
- [ ] Configurar URL do serviço PENELOPE
- [ ] Importar `PenelopeClient`
- [ ] Implementar fallback para local analyzer
- [ ] Testar suggest_action endpoint
- [ ] Testar auto_heal endpoint

### Fase 4: Production (Day 6-7)
- [ ] Adicionar monitoring de healing success rate
- [ ] Configurar alertas para low confidence (<0.8)
- [ ] Implementar circuit breaker para PENELOPE service
- [ ] Adicionar testes E2E com healing
- [ ] Documentar seletores que mudaram frequentemente

---

## 🏗️ Architecture Patterns

### Pattern 1: Local Analyzer Only

**Use quando:** Você não tem PENELOPE service deployed.

```python
from penelope_integration import PageAnalyzer, AutoHealer

class BrowserAutomation:
    def __init__(self):
        self.analyzer = PageAnalyzer(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.healer = AutoHealer(analyzer=self.analyzer, max_heal_attempts=3)

    async def resilient_click(self, page, selector):
        try:
            await page.click(selector)
        except Exception as e:
            healed = await self.healer.heal_failed_action(
                failed_action={"action": "click", "selector": selector},
                error_message=str(e),
                page_html=await page.content()
            )
            if healed:
                await page.click(healed["selector"])
            else:
                raise

    async def cleanup(self):
        await self.healer.close()
```

**Pros:**
- ✅ Simple
- ✅ Sem dependências externas
- ✅ Funciona offline (com internet para Claude API)

**Cons:**
- ❌ Cada instância chama Claude API diretamente
- ❌ Sem cache compartilhado
- ❌ Custo pode ser maior

---

### Pattern 2: PENELOPE Service com Fallback

**Use quando:** Você tem PENELOPE service mas quer resiliência.

```python
from penelope_integration import PageAnalyzer, PenelopeClient, AutoHealer

class BrowserAutomation:
    def __init__(self):
        self.local_analyzer = PageAnalyzer(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.penelope_client = PenelopeClient(
            penelope_url=os.getenv("PENELOPE_URL", "http://penelope:8153")
        )
        self.healer = AutoHealer(
            analyzer=self.local_analyzer,
            penelope_client=self.penelope_client,
            max_heal_attempts=3
        )

    async def suggest_next_action(self, page, goal):
        """Try PENELOPE service first, fallback to local."""
        try:
            # Try PENELOPE service
            suggestion = await self.penelope_client.suggest_action(
                current_url=page.url,
                goal=goal,
                page_html=await page.content()
            )
            return suggestion
        except Exception as e:
            logger.warning(f"PENELOPE service failed: {e}, using local analyzer")
            # Fallback to local
            analysis = await self.local_analyzer.analyze_html_structure(
                html=await page.content(),
                url=page.url,
                goal=goal
            )
            return {"analysis": analysis["analysis"], "source": "local"}

    async def cleanup(self):
        await self.healer.close()
```

**Pros:**
- ✅ Performance do service quando disponível
- ✅ Resiliente a falhas de service
- ✅ Cache compartilhado (service-side)

**Cons:**
- ❌ Mais complexo
- ❌ Requer deploy do PENELOPE service

---

### Pattern 3: Service Only (Sem Fallback)

**Use quando:** PENELOPE service é critical e SLA é alto.

```python
from penelope_integration import PenelopeClient

class BrowserAutomation:
    def __init__(self):
        self.penelope = PenelopeClient(
            penelope_url=os.getenv("PENELOPE_URL"),
            timeout=30  # 30s timeout
        )

    async def execute_goal(self, page, goal, max_steps=10):
        """Execute goal using only PENELOPE service."""
        for step in range(max_steps):
            suggestion = await self.penelope.suggest_action(
                current_url=page.url,
                goal=goal,
                page_html=await page.content()
            )

            if suggestion.get("action") == "complete":
                return True

            await self.execute_action(page, suggestion)

        return False

    async def cleanup(self):
        await self.penelope.close()
```

**Pros:**
- ✅ Simples
- ✅ Centralized intelligence
- ✅ Fácil de escalar

**Cons:**
- ❌ Single point of failure
- ❌ Requer PENELOPE service com HA

---

## 🔌 Integration Examples

### Django/FastAPI Integration

```python
from fastapi import FastAPI, Depends
from penelope_integration import PageAnalyzer, AutoHealer

app = FastAPI()

# Singleton analyzer
_analyzer: PageAnalyzer | None = None
_healer: AutoHealer | None = None

def get_penelope_analyzer():
    global _analyzer, _healer
    if not _analyzer:
        _analyzer = PageAnalyzer(api_key=os.getenv("ANTHROPIC_API_KEY"))
        _healer = AutoHealer(analyzer=_analyzer)
    return _healer

@app.post("/api/scrape")
async def scrape_page(
    url: str,
    schema: dict,
    healer: AutoHealer = Depends(get_penelope_analyzer)
):
    # Your scraping logic with PENELOPE
    ...

@app.on_event("shutdown")
async def shutdown():
    global _analyzer, _healer
    if _healer:
        await _healer.close()
    _analyzer = None
    _healer = None
```

### Celery Task Integration

```python
from celery import Celery
from penelope_integration import PageAnalyzer

app = Celery('tasks')

@app.task
def analyze_webpage(url: str, html: str):
    """Celery task para análise de página."""
    import asyncio

    async def run_analysis():
        analyzer = PageAnalyzer()
        try:
            result = await analyzer.analyze_html_structure(
                html=html,
                url=url
            )
            return result
        finally:
            await analyzer.close()

    return asyncio.run(run_analysis())
```

### Pytest Integration

```python
import pytest
from penelope_integration import AutoHealer

@pytest.fixture
async def auto_healer():
    """Fixture que cria e cleanup AutoHealer."""
    healer = AutoHealer(max_heal_attempts=3)
    yield healer
    await healer.close()

@pytest.mark.asyncio
async def test_login_flow(page, auto_healer):
    """Test com auto-healing."""
    async def click_with_healing(selector):
        try:
            await page.click(selector)
        except Exception as e:
            healed = await auto_healer.heal_failed_action(
                failed_action={"action": "click", "selector": selector},
                error_message=str(e),
                page_html=await page.content()
            )
            assert healed, f"Could not heal: {selector}"
            await page.click(healed["selector"])

    await page.goto("https://example.com/login")
    await click_with_healing("button.login")
```

---

## 🔐 Security Best Practices

### 1. **API Key Management**

```python
# ✅ CORRETO - Use secrets management
from config import get_secret

analyzer = PageAnalyzer(api_key=get_secret("ANTHROPIC_API_KEY"))

# ❌ ERRADO - Hardcoded
analyzer = PageAnalyzer(api_key="sk-ant-hardcoded")  # NEVER!
```

### 2. **HTML Sanitization**

```python
# ✅ CORRETO - Limite tamanho antes de enviar
MAX_HTML_SIZE = 100_000  # 100KB

async def safe_analyze(html: str, url: str):
    if len(html) > MAX_HTML_SIZE:
        logger.warning(f"HTML too large: {len(html)} bytes, truncating")
        html = html[:MAX_HTML_SIZE]

    return await analyzer.analyze_html_structure(html=html, url=url)
```

### 3. **Rate Limiting**

```python
from aiolimiter import AsyncLimiter

# 60 requests per minute to Claude API
rate_limiter = AsyncLimiter(max_rate=60, time_period=60)

async def rate_limited_analysis(html: str, url: str):
    async with rate_limiter:
        return await analyzer.analyze_html_structure(html=html, url=url)
```

### 4. **Timeout Protection**

```python
import asyncio

async def analyze_with_timeout(html: str, url: str, timeout: int = 30):
    """Análise com timeout protection."""
    try:
        return await asyncio.wait_for(
            analyzer.analyze_html_structure(html=html, url=url),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        logger.error(f"Analysis timeout after {timeout}s")
        raise
```

---

## 📊 Monitoring & Alerting

### Metrics to Track

```python
from prometheus_client import Counter, Histogram, Gauge

# Healing metrics
healing_attempts = Counter('penelope_healing_attempts_total', 'Total healing attempts')
healing_success = Counter('penelope_healing_success_total', 'Successful healings')
healing_failures = Counter('penelope_healing_failures_total', 'Failed healings')
healing_duration = Histogram('penelope_healing_duration_seconds', 'Healing duration')

# Analysis metrics
analysis_duration = Histogram('penelope_analysis_duration_seconds', 'Analysis duration')
api_errors = Counter('penelope_api_errors_total', 'Claude API errors', ['error_type'])

# Wrap healing
async def monitored_heal(failed_action, error_message, page_html):
    healing_attempts.inc()

    start = time.time()
    try:
        result = await healer.heal_failed_action(
            failed_action=failed_action,
            error_message=error_message,
            page_html=page_html
        )

        if result:
            healing_success.inc()
        else:
            healing_failures.inc()

        return result
    finally:
        healing_duration.observe(time.time() - start)
```

### Alert Rules

```yaml
# Prometheus alert rules
groups:
  - name: penelope_alerts
    rules:
      - alert: PenelopeHighFailureRate
        expr: rate(penelope_healing_failures_total[5m]) / rate(penelope_healing_attempts_total[5m]) > 0.5
        for: 5m
        annotations:
          summary: "PENELOPE healing failure rate > 50%"

      - alert: PenelopeAPIErrors
        expr: rate(penelope_api_errors_total[5m]) > 10
        for: 2m
        annotations:
          summary: "High Claude API error rate"

      - alert: PenelopeSlowAnalysis
        expr: histogram_quantile(0.95, rate(penelope_analysis_duration_seconds_bucket[5m])) > 5
        for: 5m
        annotations:
          summary: "95th percentile analysis time > 5s"
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# Test individual components
@pytest.mark.asyncio
async def test_analyzer_validates_inputs():
    analyzer = PageAnalyzer(api_key="test-key")

    with pytest.raises(ValueError, match="HTML content is required"):
        await analyzer.suggest_selectors(html="", element_description="button")
```

### Integration Tests

```python
# Test with mocked Claude API
@pytest.mark.asyncio
async def test_healing_workflow():
    analyzer = PageAnalyzer(api_key="test-key")
    analyzer.client = AsyncMock()  # Mock Claude client

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="button.submit\n#send")]
    analyzer.client.messages.create = AsyncMock(return_value=mock_response)

    healer = AutoHealer(analyzer=analyzer)

    result = await healer.heal_failed_action(
        failed_action={"action": "click", "selector": "button.missing"},
        error_message="not found",
        page_html="<button class='submit'>Click</button>"
    )

    assert result["selector"] in ["button.submit", "#send"]
```

### E2E Tests

```python
# Test with real browser
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_real_browser_healing(browser):
    page = await browser.new_page()
    healer = AutoHealer()

    await page.goto("https://example.com")

    # Intentionally use wrong selector
    try:
        await page.click("button.nonexistent")
    except Exception as e:
        # Should heal
        healed = await healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button.nonexistent"},
            error_message=str(e),
            page_html=await page.content()
        )

        assert healed is not None
        await page.click(healed["selector"])
```

---

## 🐛 Common Pitfalls

### Pitfall 1: Forgetting to Close Resources

```python
# ❌ WRONG
async def bad_example():
    analyzer = PageAnalyzer()
    result = await analyzer.analyze_html_structure(...)
    return result  # analyzer never closed!

# ✅ CORRECT
async def good_example():
    analyzer = PageAnalyzer()
    try:
        result = await analyzer.analyze_html_structure(...)
        return result
    finally:
        await analyzer.close()
```

### Pitfall 2: Not Handling Low Confidence

```python
# ❌ WRONG - Blindly trust suggestion
suggestion = await client.suggest_action(...)
await page.click(suggestion["selector"])  # Might be wrong!

# ✅ CORRECT - Check confidence
suggestion = await client.suggest_action(...)
if suggestion["confidence"] < 0.8:
    logger.warning("Low confidence, asking for human confirmation")
    # Implement human-in-the-loop or fallback
else:
    await page.click(suggestion["selector"])
```

### Pitfall 3: Unbounded Healing Attempts

```python
# ❌ WRONG - Infinite loop possible
while True:
    try:
        await page.click(selector)
        break
    except Exception as e:
        healed = await healer.heal_failed_action(...)
        selector = healed["selector"] if healed else selector

# ✅ CORRECT - Limited attempts
for attempt in range(3):
    try:
        await page.click(selector)
        break
    except Exception as e:
        if attempt == 2:  # Last attempt
            raise
        healed = await healer.heal_failed_action(...)
        selector = healed["selector"] if healed else selector
```

---

## 📚 Additional Resources

- [Main README](./README.md) - Comprehensive documentation
- [PENELOPE Service API](http://penelope-service:8153/docs) - Service documentation
- [Anthropic Claude Docs](https://docs.anthropic.com/) - Claude API reference
- [Test Examples](../tests/e2e/test_penelope_integration.py) - E2E test examples
- [Performance Benchmarks](../tests/performance/test_penelope_benchmarks.py) - Benchmark suite

---

## ❓ FAQs

**Q: PENELOPE funciona sem internet?**
A: Não. PENELOPE precisa de acesso à Claude API (cloud).

**Q: Quanto custa usar PENELOPE?**
A: Depende do uso da Claude API. Monitore tokens via Anthropic dashboard.

**Q: PENELOPE substitui Playwright/Selenium?**
A: Não. PENELOPE é um layer de inteligência sobre browser automation.

**Q: PENELOPE pode aprender com meus dados?**
A: Não por padrão. Use healing_history para patterns locais.

**Q: PENELOPE funciona em produção?**
A: Sim! Está production-ready com testes, validação e error handling.

---

**Author:** Vértice Platform Team
**License:** Proprietary
**Version:** 1.0.0 (Day 5 - Production Ready) 💝
