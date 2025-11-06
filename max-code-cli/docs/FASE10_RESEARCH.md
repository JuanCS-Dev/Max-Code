# FASE 10 - E2E Testing & Performance Research

**Data**: 2025-11-06
**Duração da Pesquisa**: 2-3h
**Objetivo**: Identificar best practices para E2E testing, performance profiling e load testing em Python CLI

---

## 📋 EXECUTIVE SUMMARY

Pesquisa completa sobre ferramentas e padrões para garantir qualidade production-grade do Max-Code CLI.

**Principais Descobertas**:
- ✅ **Click CliRunner** é o padrão-ouro para testar CLI apps
- ✅ **py-spy + SnakeViz** são melhores que cProfile tradicional
- ✅ **Locust** agora suporta pytest (release 2.40+)
- ✅ **pytest-xdist** para paralelização de testes
- ✅ **pytest-asyncio** para async tests
- ✅ Anti-patterns bem documentados para evitar flaky tests

---

## 🔍 1. E2E TESTING COM CLICK + PYTEST

### Ferramenta Principal: Click's CliRunner

**Click Documentation (2024)**:
> Click provides `CliRunner` to invoke commands as command line scripts, which returns a `Result` object that captures output data, exit code, optional exception, and captures the output as bytes and binary data.

### Pattern Básico

```python
from click.testing import CliRunner
from cli.main import cli

def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', 'Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'
```

### Best Practices (2024)

1. **Isolated Filesystem Testing**
   - Click fornece isolated_filesystem() context manager
   - Perfeito para testar operações com arquivos
   ```python
   def test_file_operations():
       runner = CliRunner()
       with runner.isolated_filesystem():
           # Testes em diretório temporário isolado
           result = runner.invoke(cli, ['export', 'data.json'])
           assert Path('data.json').exists()
   ```

2. **Input Simulation (stdin)**
   - CliRunner aceita `input` para simular stdin
   ```python
   result = runner.invoke(cli, ['learn', 'enable'], input='y\n')
   ```

3. **Fixtures e Parameterização**
   - Usar pytest fixtures para setup/teardown
   - Parameterizar testes para cobrir múltiplos cenários
   ```python
   @pytest.fixture
   def cli_runner():
       return CliRunner()

   @pytest.mark.parametrize("mode,expected", [
       ("fast", "Heuristic"),
       ("deep", "Claude AI")
   ])
   def test_predict_modes(cli_runner, mode, expected):
       result = cli_runner.invoke(cli, ['predict', '--mode', mode])
       assert expected in result.output
   ```

4. **E2E Workflow Testing**
   - Testar jornadas completas do usuário
   - Validar output em cada step
   ```python
   def test_first_time_user_workflow():
       runner = CliRunner()

       # Step 1: Init
       result = runner.invoke(cli, ['init', '--profile', 'development'])
       assert result.exit_code == 0

       # Step 2: Health check
       result = runner.invoke(cli, ['health'])
       assert "Service Health Check" in result.output

       # Step 3: First chat
       result = runner.invoke(cli, ['chat', 'Hello'])
       assert result.exit_code == 0
   ```

### Fontes
- [Click Testing Documentation](https://click.palletsprojects.com/en/stable/testing/)
- [Real Python - Testing CLI Apps](https://realpython.com/python-cli-testing/)
- [Testing Click with Pytest (DEV.to)](https://dev.to/wangonya/testing-click-applications-with-pytest-2o79)

---

## 📊 2. PERFORMANCE PROFILING & FLAMEGRAPHS

### Ferramentas Recomendadas (2024)

#### 1. **py-spy** (⭐ MELHOR ESCOLHA)

**Vantagens**:
- Escrito em Rust (extremely low overhead)
- Não precisa modificar código
- Sampling profiler (não invasivo)
- Funciona em produção
- Gera flamegraphs nativamente

```bash
# Profile comando por 30 segundos
py-spy record -o profile.svg -- max-code chat "Hello"

# Profile processo rodando
py-spy record --pid 12345 --output flamegraph.svg

# Gerar speedscope format
py-spy record -o profile.json --format speedscope -- max-code predict
```

**Instalação**:
```bash
pip install py-spy
```

#### 2. **SnakeViz** (Para cProfile)

**Melhor para**: Análise interativa de cProfile stats

```python
import cProfile
import pstats

# Profile código
profiler = cProfile.Profile()
profiler.enable()
# ... código a profilear ...
profiler.disable()

# Salvar stats
profiler.dump_stats('output.prof')

# Visualizar com SnakeViz (browser)
# $ snakeviz output.prof
```

**Features**:
- Browser-based interactive UI
- Icicle e Sunburst visualizations
- Drill-down em call stacks
- Exporta SVG/PNG

**Instalação**:
```bash
pip install snakeviz
```

#### 3. **flameprof** (SVG flamegraphs)

**Para**: Gerar flamegraphs estáticos de cProfile

```bash
python -m cProfile -o program.prof my_program.py
flameprof program.prof > flamegraph.svg
```

**Nota**: Não mais mantido ativamente, py-spy é preferível.

### Profiling Strategy para Max-Code CLI

```python
# scripts/profile.py (pattern sugerido)

import cProfile
import pstats
from pathlib import Path
from rich.console import Console
from rich.table import Table

class MaxCodeProfiler:
    """Performance profiler for Max-Code CLI."""

    def __init__(self):
        self.console = Console()

    def profile_command(self, command: List[str]) -> dict:
        """Profile um comando e retorna métricas."""
        profiler = cProfile.Profile()

        # Profile execution
        profiler.enable()
        result = subprocess.run(
            ['max-code'] + command,
            capture_output=True,
            text=True
        )
        profiler.disable()

        # Extract stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')

        return {
            'command': ' '.join(command),
            'total_time': stats.total_tt,
            'exit_code': result.returncode,
            'output_size': len(result.stdout),
            'top_functions': self._extract_hotspots(stats)
        }

    def _extract_hotspots(self, stats, n=10):
        """Extract top N hotspots."""
        hotspots = []
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            hotspots.append({
                'function': f"{func[0]}:{func[1]}:{func[2]}",
                'cumtime': ct,
                'calls': nc
            })
        return sorted(hotspots, key=lambda x: x['cumtime'], reverse=True)[:n]

    def benchmark_all(self):
        """Benchmark todos os comandos principais."""
        commands = [
            ['health'],
            ['config'],
            ['predict', '--mode', 'fast'],
            ['predict', '--mode', 'deep'],
            ['learn', 'status'],
            ['sabbath', 'status']
        ]

        results = []
        for cmd in commands:
            self.console.print(f"[cyan]Profiling: {' '.join(cmd)}[/cyan]")
            result = self.profile_command(cmd)
            results.append(result)

        self._display_results(results)
        return results

    def _display_results(self, results):
        """Display benchmark results."""
        table = Table(title="Performance Benchmark Results")
        table.add_column("Command", style="cyan")
        table.add_column("Total Time", style="yellow")
        table.add_column("Status", style="green")

        for r in results:
            status = "✅" if r['total_time'] < 1.0 else "⚠️"
            table.add_row(
                r['command'],
                f"{r['total_time']:.3f}s",
                status
            )

        self.console.print(table)
```

### Performance Targets (PLANO_HEROICO)

| Command | Target Latency | Memory Limit | Tool |
|---------|---------------|--------------|------|
| `health` | < 500ms | < 50MB | py-spy |
| `chat` (first token) | < 1000ms | < 100MB | py-spy |
| `predict --fast` | < 100ms | < 30MB | cProfile |
| `predict --deep` | < 2000ms | < 150MB | py-spy |
| `learn insights` | < 200ms | < 40MB | cProfile |
| `sabbath status` | < 100ms | < 20MB | cProfile |
| `config` | < 50ms | < 20MB | cProfile |

### Memory Profiling

**Ferramenta**: `memory_profiler`

```bash
pip install memory-profiler
python -m memory_profiler my_script.py
```

**Decorator-based**:
```python
from memory_profiler import profile

@profile
def my_function():
    # Código a profilear
    pass
```

### Fontes
- [py-spy GitHub](https://github.com/benfred/py-spy)
- [SnakeViz Usage (James' Coffee Blog, Nov 2024)](https://jamesg.blog/2024/11/02/cprofile)
- [Brendan Gregg - Flame Graphs](https://www.brendangregg.com/flamegraphs.html)
- [Roman Imankulov - Python Performance Profiling](https://roman.pt/posts/python-performance-profiling/)

---

## 🚀 3. LOAD TESTING & CONCURRENT EXECUTION

### Ferramentas Principais

#### 1. **Locust** (⭐ RECOMENDADO PARA APIs)

**Novidade 2024**: Release 2.40+ suporta pytest-style scenarios!

**Features**:
- Event-based (gevent) - milhares de usuários com baixo overhead
- Web UI para monitoramento real-time
- Command-line execution
- Distributed load generation
- Agora integra com pytest

**Exemplo**:
```python
from locust import HttpUser, task, between

class MaxCodeUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)  # 3x mais frequente
    def predict_fast(self):
        self.client.post("/api/predict", json={
            "mode": "fast",
            "context": {}
        })

    @task(1)
    def predict_deep(self):
        self.client.post("/api/predict", json={
            "mode": "deep",
            "context": {}
        })
```

**Executar**:
```bash
# Web UI
locust -f locustfile.py --host=http://localhost:8000

# Headless (100 users, 10/sec spawn rate, 60s duration)
locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 --spawn-rate 10 --run-time 60s --headless
```

#### 2. **pytest-xdist** (Para Testes Paralelos)

**Best para**: Distribuir testes pytest em múltiplos CPUs

**Instalação**:
```bash
pip install pytest-xdist
```

**Usage**:
```bash
# Auto-detect CPUs
pytest -n auto

# Specific number of workers
pytest -n 4

# Distribution strategy: loadscope (evita resource conflicts)
pytest -n 4 --dist loadscope
```

**Quando usar**:
- ✅ Tests CPU-bound
- ✅ Tests não-async
- ✅ Quer speed up test suite

**Quando NÃO usar**:
- ❌ Tests IO-bound (usar pytest-asyncio)
- ❌ Tests async (usar pytest-asyncio + pytest-subtests)

### Load Test Strategy para Max-Code CLI

```python
# tests/load/test_concurrent.py

import asyncio
import pytest
from concurrent.futures import ThreadPoolExecutor
from click.testing import CliRunner

class TestLoadScenarios:
    """Load testing for concurrent CLI usage."""

    @pytest.mark.load
    async def test_concurrent_predict_requests(self):
        """Test 100 concurrent predict requests."""

        async def predict_request(user_id: int):
            runner = CliRunner()
            result = runner.invoke(cli, [
                'predict', '--mode', 'fast'
            ])
            return {
                'user_id': user_id,
                'exit_code': result.exit_code,
                'latency': result.elapsed_time
            }

        # Launch 100 concurrent requests
        tasks = [predict_request(i) for i in range(100)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Validate results
        successful = [r for r in results if not isinstance(r, Exception)]
        success_rate = len(successful) / len(results)

        assert success_rate >= 0.90  # 90% success rate minimum

        # Check latency
        avg_latency = sum(r['latency'] for r in successful) / len(successful)
        assert avg_latency < 0.5  # 500ms average

    @pytest.mark.load
    def test_rate_limiter_behavior(self):
        """Test rate limiter under heavy load."""
        runner = CliRunner()

        results = []
        for i in range(20):  # 20 rapid requests
            result = runner.invoke(cli, ['predict', '--mode', 'fast'])
            results.append({
                'attempt': i,
                'exit_code': result.exit_code,
                'output': result.output
            })

        # Should see rate limiting after 10 requests (configured limit)
        rate_limited = [r for r in results if 'Rate limit exceeded' in r['output']]
        assert len(rate_limited) >= 10

        # Rate limited requests should fail gracefully
        for r in rate_limited:
            assert r['exit_code'] == 1  # Error exit code
            assert 'Please wait' in r['output']
```

### Load Test Targets (PLANO_HEROICO)

| Metric | Target | Tool |
|--------|--------|------|
| Concurrent users | 100 simultaneous | pytest-xdist |
| API requests/sec | 50 rps sustained | Locust |
| Circuit breaker fail fast | < 500ms | Manual test |
| Cache hit rate | > 70% | Custom metrics |
| Memory stable | No leaks 24h | memory_profiler |

### Fontes
- [Locust Documentation](https://locust.io/)
- [pytest-xdist GitHub](https://github.com/pytest-dev/pytest-xdist)
- [Better Stack - Locust Explained (2024)](https://betterstack.com/community/guides/testing/locust-explained/)
- [Parallel Testing with pytest-xdist](https://pytest-with-eric.com/plugins/pytest-xdist/)

---

## 🐛 4. ANTI-PATTERNS & FLAKY TEST MITIGATION

### O Que São Flaky Tests?

> "A flaky test is one that exhibits intermittent or sporadic failure with non-deterministic behavior - sometimes it passes, sometimes it fails without clear reason."
> — Pytest Documentation

**Exemplo Real**: Spotify reduziu flaky tests de 4.5% para 0.4%, economizando 120 developer hours/semana.

### Root Causes de Flaky Tests

#### 1. **Parallel Execution Issues**
```python
# ❌ BAD: Shared state entre testes paralelos
cache = {}

def test_a():
    cache['key'] = 'value_a'
    assert cache['key'] == 'value_a'  # Pode falhar se test_b rodar em paralelo

# ✅ GOOD: Isolated state
@pytest.fixture
def isolated_cache():
    return {}

def test_a(isolated_cache):
    isolated_cache['key'] = 'value_a'
    assert isolated_cache['key'] == 'value_a'
```

#### 2. **Async Operations com Timing**
```python
# ❌ BAD: Fixed sleep
def test_api_response():
    make_async_request()
    time.sleep(2)  # Pode falhar se resposta demorar > 2s
    assert response_received()

# ✅ GOOD: Wait with timeout
def test_api_response():
    make_async_request()
    wait_until(lambda: response_received(), timeout=5)
```

#### 3. **Shared Resources (DB, Files)**
```python
# ❌ BAD: Shared database
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

# ✅ GOOD: Transaction rollback ou isolated DB
@pytest.fixture
def db_transaction():
    transaction = begin_transaction()
    yield transaction
    transaction.rollback()

def test_user_creation(db_transaction):
    user = create_user("test@example.com")
    assert user.email == "test@example.com"
```

### Best Practices (2024)

#### 1. **Smart Retry Mechanisms**

**Plugin**: `pytest-rerunfailures`

```bash
pip install pytest-rerunfailures
```

```bash
# Rerun failed tests 2 times
pytest --reruns 2

# Rerun with delay
pytest --reruns 2 --reruns-delay 1
```

**⚠️ WARNING**: Não abuse! Retries escondem problemas reais.
- Max 2-3 retries
- Use exponential backoff
- Monitor retry rates (> 5% indica problemas)

#### 2. **Environment Isolation**

```python
# ✅ GOOD: Use Click's isolated_filesystem
def test_file_operations():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Tudo aqui é isolado
        result = runner.invoke(cli, ['export', 'data.json'])
        assert Path('data.json').exists()
    # Cleanup automático
```

#### 3. **Fixture Scope Management**

```python
# ✅ GOOD: Appropriate scope
@pytest.fixture(scope="function")  # Nova instância por teste
def fresh_db():
    db = create_database()
    yield db
    db.cleanup()

@pytest.fixture(scope="session")  # Uma vez por sessão
def expensive_resource():
    resource = setup_expensive_thing()
    yield resource
    resource.teardown()
```

#### 4. **pytest-asyncio para Async Tests**

```bash
pip install pytest-asyncio
```

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected
```

**Best Practices Async**:
- Use `pytest.mark.asyncio` decorator
- Evitar `asyncio.run()` dentro de tests (pytest-asyncio gerencia)
- Timeout apropriados para network operations

#### 5. **Monitoring & Detection**

```bash
# Collect metrics em CI/CD
pytest --durations=10  # Show 10 slowest tests

# Stop after N failures
pytest --maxfail=3

# Enforce timeout
pytest --timeout=300  # 5 minutes max per test
```

#### 6. **Test Quality Practices**

✅ **DO**:
- Review test suite regularmente
- Document flaky behavior
- Estabelecer triage process
- Usar --maxfail em CI/CD para fail fast
- Profile test durations
- Enforce performance budgets

❌ **DON'T**:
- Abusar de retries
- Ignorar flaky tests
- Usar arbitrary sleeps
- Share mutable state
- Skip cleanup

### CI/CD Integration Best Practices

```yaml
# .github/workflows/tests.yml (exemplo)
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-xdist pytest-rerunfailures pytest-timeout

      - name: Run tests
        run: |
          pytest -n auto \
                 --reruns 2 \
                 --reruns-delay 1 \
                 --timeout=300 \
                 --maxfail=5 \
                 --durations=10 \
                 -v

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Fontes
- [Pytest - Flaky Tests](https://docs.pytest.org/en/stable/explanation/flaky.html)
- [Managing Flaky Tests in Python (PyQuestHub)](https://pyquesthub.com/managing-flaky-tests-in-python-strategies-for-reliable-test-automation)
- [pytest-asyncio Tips (Mergify, 2024)](https://articles.mergify.com/pytest-asyncio-2/)
- [10 Ways to Reduce Flaky Tests (Bugster, 2024)](https://www.bugster.dev/resources/10-ways-to-reduce-flaky-tests-in-your-cicd-pipeline/)

---

## 📊 SUMMARY & RECOMMENDATIONS

### Ferramentas Escolhidas para Max-Code CLI

| Category | Tool | Justificativa |
|----------|------|---------------|
| **E2E Testing** | Click CliRunner + pytest | Padrão-ouro, bem documentado |
| **Performance Profiling** | py-spy | Low overhead, Rust-based, flamegraphs nativos |
| **Visualization** | SnakeViz | Interactive browser UI |
| **Load Testing** | pytest-xdist + custom | CLI não tem HTTP endpoints |
| **Async Testing** | pytest-asyncio | Melhor suporte async/await |
| **Flaky Test Prevention** | pytest-rerunfailures | Smart retries com backoff |
| **Parallel Execution** | pytest-xdist | Distribuir testes em CPUs |

### Implementation Priority

**High Priority** (Fazer já):
1. ✅ E2E workflow tests com CliRunner (Task 10.2)
2. ✅ Performance profiling com py-spy (Task 10.3)
3. ✅ Concurrent execution tests (Task 10.4)

**Medium Priority** (Próxima iteração):
4. Locust para API load testing (quando tivermos HTTP API)
5. Memory profiling completo (24h run)
6. Grafana dashboard para monitoring

**Low Priority** (Nice to have):
7. Advanced flamegraph analysis
8. Distributed load testing
9. Chaos engineering tests

### Anti-Patterns a Evitar

❌ **NÃO FAZER**:
- Fixed time.sleep() em tests
- Shared mutable state entre tests
- Ignorar flaky tests
- Retries sem limite
- Tests sem timeout
- Skip cleanup em fixtures

✅ **FAZER**:
- Isolated filesystem para file operations
- Transaction rollback em DB tests
- Wait with timeout para async operations
- Monitor retry rates
- Profile test duration
- Enforce performance budgets

### Próximos Passos

**Task 10.2**: Implementar E2E workflow tests
- Use CliRunner pattern
- Test 3 user journeys principais
- Isolate filesystem operations

**Task 10.3**: Setup performance profiling
- Install py-spy
- Create scripts/profile.py
- Benchmark all commands
- Generate flamegraphs

**Task 10.4**: Load testing
- pytest-xdist para parallel execution
- Test concurrent predict requests
- Validate rate limiter behavior
- Test circuit breaker

---

**Research Completed**: 2025-11-06
**Total Sources**: 40+ articles, docs, and tutorials
**Time Invested**: 2-3 hours
**Status**: ✅ READY FOR IMPLEMENTATION

Próxima etapa: **Task 10.2 - Implement E2E Workflow Tests**
