# MAX-CODE-CLI - Quick Start Guide

**Get up and running in 5 minutes**

---

## Installation

```bash
cd "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m cli --version
```

## First Run

### Interactive REPL (Recommended)

```bash
# Start the REPL
python -m cli repl

# You'll see the neon gradient interface:
maximus ⚡ › 
```

### Available Slash Commands

- `/code` - Generate code
- `/review` - Review code
- `/test` - Generate tests
- `/fix` - Fix bugs
- `/docs` - Generate documentation
- `/plan` - Create implementation plan
- `/explore` - Explore codebase
- `/help` - Show all commands

### Example Session

```
maximus ⚡ › /code Create a fibonacci function in Python

[Agent executes and generates code...]

maximus ⚡ › /test Generate tests for the fibonacci function

[Test agent generates comprehensive tests...]

maximus ⚡ › /review Review the fibonacci implementation

[Review agent provides feedback...]
```

## Key Features

### 1. Neon Gradient UI
- Tri-color gradient (#00FF41 → #FFFF00 → #00D4FF)
- Constitutional status bar (P1-P6 principles)
- Real-time agent status

### 2. Agent System
- **9 Specialized Agents** for different tasks
- Constitutional AI validation
- MAXIMUS backend integration

### 3. Backend Integration
- PENELOPE: Biblical governance
- MAXIMUS: AI consciousness
- ORACULO: Self-improvement
- 8 microservices connected

## Configuration

Edit `.env` file:

```bash
# LLM Configuration
ANTHROPIC_API_KEY=your-key-here

# Backend Services (optional)
MAXIMUS_CORE_URL=http://localhost:8150
PENELOPE_URL=http://localhost:8153

# Feature Flags
ENABLE_CONSTITUTIONAL_AI=true
ENABLE_STREAMING=true
```

## Next Steps

1. Explore [Agent Documentation](../agents/00_AGENTS_INDEX.md)
2. Read [CLI Reference](../cli/CLI_REFERENCE.md)
3. Check [Development Guide](DEVELOPMENT_GUIDE.md)

