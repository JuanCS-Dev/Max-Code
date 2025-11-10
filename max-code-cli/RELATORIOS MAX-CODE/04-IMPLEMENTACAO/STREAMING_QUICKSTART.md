# 🚀 Enhanced Streaming - Quick Start Guide

**Status:** ✅ Production Ready  
**Version:** 3.0.0  
**Implementation:** World-Class

---

## 📋 Prerequisites

- Python 3.9+
- Claude API key (Anthropic)
- Rich library (for UI)
- AsyncIO support

---

## ⚡ 5-Minute Quick Start

### 1. Install Dependencies

```bash
cd "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"

# Install required packages (if not already installed)
pip install anthropic rich asyncio
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-key-here"

# Or add to .env file
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

### 3. Run Demo

```bash
# Quick test
python -m cli.main demo-streaming "Create a hello world function"

# Or run showcase
python examples/streaming_showcase.py
```

---

## 🎯 Basic Usage

### CLI Commands

```bash
# Single agent demo
max-code demo-streaming "Create binary search function"

# Specify agent
max-code demo-streaming --agent test "Write unit tests"

# Disable thinking display
max-code demo-streaming --no-thinking "Generate code"

# Demo all agents
max-code demo-streaming-all "Implement bubble sort"
```

### Python API

```python
from agents.code_agent import CodeAgent
from sdk.agent_task import AgentTask

# Create agent
agent = CodeAgent()

# Create task
task = AgentTask(
    id="quickstart-001",
    description="Create a factorial function",
    parameters={'language': 'python'}
)

# Execute with streaming (sync)
result = agent.execute_with_thinking_sync(task)

# Print result
print(result.output['code'])
```

### Async API

```python
import asyncio
from agents.code_agent import CodeAgent
from sdk.agent_task import AgentTask

async def main():
    agent = CodeAgent()
    task = AgentTask(
        id="async-001",
        description="Create fibonacci function",
        parameters={'language': 'python'}
    )
    
    result = await agent.execute_with_thinking(task)
    print(result.output['code'])

asyncio.run(main())
```

---

## 🎨 Visual Preview

When you run streaming, you'll see:

```
┌─ ⚡ CODE AGENT ──────────────────────────────┐
│ 🔍 ANALYZING • 1.2s                          │
│                                              │
│ 💭 Thinking Process:                         │
│   ✓ Connecting to Claude API... (0.3s)     │
│   ✓ Processing request... (0.5s)           │
│   ● Reasoning about approach...            │
│                                              │
│ 🔧 Tool Usage:                               │
│   ⚙ read_file {"path": "main.py"}          │
│                                              │
│ Tokens: 42 | Speed: 35.0 tok/s | Chunks: 8 │
│                                              │
│ 📝 Output:                                   │
│   def hello_world():                        │
│       print("Hello, World!")                │
└──────────────────────────────────────────────┘
```

---

## 🧪 Testing

### Run Tests

```bash
# All streaming tests
pytest tests/test_streaming_thinking.py -v

# Specific test
pytest tests/test_streaming_thinking.py::TestEnhancedThinkingDisplay -v

# With coverage
pytest tests/test_streaming_thinking.py --cov=core.streaming
```

### Manual Testing

```bash
# Test thinking display
python examples/streaming_showcase.py

# Test specific agent
max-code demo-streaming --agent code "Hello world"
max-code demo-streaming --agent test "Write tests"
max-code demo-streaming --agent fix "Fix bug"
```

---

## 🔧 Configuration

### Custom Display Settings

```python
from core.streaming import ThinkingDisplayConfig, EnhancedThinkingDisplay

config = ThinkingDisplayConfig(
    show_thinking=True,
    show_tools=True,
    show_metrics=True,
    refresh_rate=10.0,
)

display = EnhancedThinkingDisplay(
    agent_name="code",
    config=config
)
```

### Custom Agent Integration

```python
from core.streaming import ClaudeAgentIntegration

integration = ClaudeAgentIntegration()

result = await integration.execute_with_thinking(
    prompt="Your prompt here",
    agent_name="custom",
    system="Your system prompt",
)
```

---

## 📊 Features

✅ **Multi-phase Thinking** - See reasoning process  
✅ **Tool Tracking** - Monitor tool invocations  
✅ **Performance Metrics** - Real-time tokens/sec  
✅ **Agent-Specific Styling** - Unique visual identity  
✅ **Code Preview** - Live syntax highlighting  
✅ **Error Handling** - Graceful degradation  
✅ **Guardian Integration** - Constitutional validation  
✅ **Async/Sync Support** - Both patterns supported  

---

## 🐛 Troubleshooting

### Display Not Showing

**Problem:** Nothing displays when running streaming.

**Solution:**
```python
# Check if Rich is installed
pip install rich

# Verify console output
from rich.console import Console
console = Console()
console.print("[green]Test[/green]")
```

### API Key Issues

**Problem:** "API key not found" error.

**Solution:**
```bash
# Check environment
echo $ANTHROPIC_API_KEY

# Set in current session
export ANTHROPIC_API_KEY="your-key"

# Or add to .env
echo "ANTHROPIC_API_KEY=your-key" >> .env
```

### Import Errors

**Problem:** `ModuleNotFoundError` when importing.

**Solution:**
```bash
# Ensure you're in correct directory
cd "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Add to PYTHONPATH if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Streaming Too Slow/Fast

**Problem:** Display updates too slowly or too fast.

**Solution:**
```python
config = ThinkingDisplayConfig(
    refresh_rate=5.0,      # Lower = slower updates
    animation_speed=0.5,   # Slower animation
)
```

---

## 📚 Next Steps

1. **Read Full Documentation**  
   → `docs/STREAMING_THINKING.md`

2. **Explore Examples**  
   → `examples/streaming_showcase.py`

3. **Run Tests**  
   → `pytest tests/test_streaming_thinking.py -v`

4. **Integrate Other Agents**  
   → Add streaming to test_agent, fix_agent, etc.

5. **Customize Display**  
   → Modify `ThinkingDisplayConfig` for your needs

---

## 🎓 Learn More

- **Architecture:** See flow diagrams in `docs/STREAMING_THINKING.md`
- **API Reference:** Complete API docs in documentation
- **Performance:** Benchmarks and optimization tips
- **Best Practices:** Integration patterns and examples

---

## 💡 Pro Tips

1. **Use async when possible** - Better performance
2. **Customize colors** - Match your terminal theme
3. **Disable for CI/CD** - Use `--no-thinking` flag
4. **Monitor metrics** - Watch tokens/sec for bottlenecks
5. **Handle errors gracefully** - Always have fallback to standard execution

---

## 🆘 Support

**Need Help?**
- Check `docs/STREAMING_THINKING.md` for details
- Run `examples/streaming_showcase.py` for live demo
- Review test suite for usage patterns
- Open issue on GitHub

**Common Commands:**
```bash
# Help
max-code demo-streaming --help

# Test
python examples/streaming_showcase.py

# Debug
python -m pytest tests/test_streaming_thinking.py -v -s
```

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Dependencies installed (`pip install anthropic rich`)
- [ ] API key configured (`ANTHROPIC_API_KEY` set)
- [ ] Demo runs successfully (`max-code demo-streaming "test"`)
- [ ] Tests pass (`pytest tests/test_streaming_thinking.py`)
- [ ] Showcase executes (`python examples/streaming_showcase.py`)

---

## 🎉 Success!

If you can see the beautiful streaming output with thinking process, **you're all set!**

```
┌─ ⚡ CODE AGENT ──────────────────────────────┐
│ ✅ COMPLETING • 3.5s                         │
│                                              │
│ 💭 Thinking Process:                         │
│   ✓ Connecting to Claude API... (0.3s)     │
│   ✓ Processing request... (0.8s)           │
│   ✓ Reasoning about approach... (1.2s)     │
│   ✓ Generating output... (1.0s)            │
│   ✓ Finalizing response... (0.2s)          │
│                                              │
│ ✓ Setup Complete - World-Class Streaming!   │
└──────────────────────────────────────────────┘
```

**Welcome to world-class streaming! 🚀**

---

**Implementation:** ✅ WORLD CLASS  
**Status:** Production Ready  
**Padrão:** Pagani - Zero Compromises

**Soli Deo Gloria** 🙏
