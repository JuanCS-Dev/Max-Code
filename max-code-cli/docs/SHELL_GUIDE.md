# 🚀 MAX-CODE Shell Guide

**The most beautiful CLI you've ever used.**

---

## 📋 Quick Start

```bash
# Start enhanced shell
max-code

# Or explicitly
max-code shell

# Authenticate (first time)
max-code auth login
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut  | Action                                    |
|-----------|-------------------------------------------|
| `Ctrl+P`  | Open command palette (fuzzy search)       |
| `Ctrl+A`  | Show agent dashboard                      |
| `Ctrl+D`  | Toggle DREAM mode (critical analysis)     |
| `Ctrl+C`  | Cancel current operation                  |
| `Ctrl+R`  | Search command history                    |
| `↑`/`↓`   | Navigate history                          |
| `Tab`     | Autocomplete commands                     |

---

## 🎯 Commands

### Special Commands

```bash
/help          # Show all available commands
/exit          # Exit shell (or /quit)
/clear         # Clear screen
/dashboard     # Show agent dashboard
/theme <name>  # Change theme (neon, fire, ocean, matrix, cyberpunk)
```

### Agent Shortcuts

All 8 specialized agents available via shortcuts:

```bash
/sophia <msg>   # 👑 Sophia - The Architect (system design)
/code <msg>     # 💻 Code generation agent
/test <msg>     # 🧪 Test generation agent (TDD)
/review <msg>   # 🔍 Code review agent
/fix <msg>      # 🔧 Bug fixing agent
/docs <msg>     # 📚 Documentation agent
/explore <msg>  # 🗺️  Codebase exploration agent
/plan <msg>     # 📋 Planning agent
```

**Examples:**

```bash
/sophia design a microservices architecture for e-commerce
/code implement user authentication with JWT
/test write tests for UserService class
/review analyze this PR for security issues
/fix debug why my API returns 500
/docs generate README for this project
/explore find all API endpoints in the codebase
/plan create roadmap for v2.0
```

### Special Modes

```bash
/sofia-plan <msg>   # 🎯 Strategic planning mode (architect + planning)
/dream [msg]        # 💭 Critical analysis mode (skeptical review)
```

---

## 🧠 Special Modes Explained

### SOFIA Plan Mode

**Purpose:** Strategic planning and architecture design
**Use when:** You need high-level design, system architecture, or strategic decisions

**Example:**

```bash
max-code ❯ /sofia-plan design a scalable microservices architecture

🎯 SOFIA Plan Mode
Strategic planning and architecture design

👑 Sophia - The Architect

I'll design a scalable microservices architecture with:

**Core Services:**
1. API Gateway (Kong/nginx)
2. User Service (authentication, profiles)
3. Product Catalog Service
4. Order Management Service
5. Payment Service
6. Notification Service

**Infrastructure:**
- Container orchestration: Kubernetes
- Service mesh: Istio
- Message broker: RabbitMQ
- Databases: PostgreSQL (relational), Redis (cache), MongoDB (documents)

[... detailed plan continues ...]
```

### DREAM Mode

**Purpose:** Critical analysis, identify issues, skeptical review
**Use when:** You want a "devil's advocate" perspective, need to find flaws, or want improvement suggestions

**Activation:**
- Press `Ctrl+D` to toggle (affects all subsequent messages)
- Or use `/dream <message>` for one-time analysis

**Example:**

```bash
max-code 💭 ❯ this architecture looks solid

💭 DREAM Mode - Critical Analysis

While the architecture has several strengths, I see potential issues:

⚠️  Critical Concerns:
1. Single point of failure in API Gateway
   → Consider: Multiple gateways with load balancing
2. Tight coupling between Order and Payment services
   → Risk: Cascading failures under load
3. No circuit breaker patterns implemented
   → Impact: One slow service can bring down entire system

💡 Improvement Proposals:
1. Implement resilience patterns (circuit breaker, retry, timeout)
2. Add service mesh (Istio/Linkerd) for observability
3. Consider CQRS for read-heavy services like Product Catalog

[... continues with detailed analysis ...]
```

---

## 💬 Natural Language

Just type naturally - no command prefix needed:

```bash
max-code ❯ explain how async/await works in JavaScript

⚡ Thinking...

Async/await is syntactic sugar over JavaScript promises that makes
asynchronous code look and behave more like synchronous code...

[... full response ...]
```

**DREAM mode active:**

```bash
max-code 💭 ❯ is using microservices always the best choice?

💭 DREAM Mode - Critical Analysis

No. Microservices are NOT always the best choice. Here's the uncomfortable truth:

**When microservices are WRONG:**
1. Small teams (<10 developers) - Operational overhead will kill productivity
2. Monoliths working fine - Don't fix what isn't broken
3. Tight coupling requirements - Fighting the architecture
4. Limited DevOps maturity - You'll drown in complexity

**Better alternatives:**
- Modular monolith (90% of startups should start here)
- Serverless functions (if AWS-locked is acceptable)
- Traditional monolith + strategic extraction

[... continues with critical perspective ...]
```

---

## 🎨 Themes

Change visual theme for personalization:

```bash
/theme neon        # 🟣 Cyberpunk neon (default)
/theme fire        # 🔴 Warm fire tones
/theme ocean       # 🔵 Cool ocean blues
/theme matrix      # 🟢 Matrix green
/theme cyberpunk   # 🟣 Blade Runner aesthetic
```

**Preview:**

| Theme      | Primary    | Accent     | Vibe                |
|------------|------------|------------|---------------------|
| neon       | Purple     | Deep purple| Cyberpunk clean     |
| fire       | Orange-red | Deep red   | Warm, energetic     |
| ocean      | Cyan       | Blue       | Cool, calming       |
| matrix     | Lime green | Dark green | Hacker aesthetic    |
| cyberpunk  | Hot pink   | Purple     | Blade Runner vibes  |

---

## 📊 Agent Dashboard

Press `Ctrl+A` to see agent activity:

```
┌─ Agent Dashboard ──────────────────────────────────────────────────┐
│                                                                     │
│  👑 SOPHIA          █████████░ 12 tasks    Last: 2min ago         │
│  💻 CODE            ██████░░░░  8 tasks    Last: 5min ago         │
│  🧪 TEST            ████░░░░░░  5 tasks    Last: 10min ago        │
│  🔍 REVIEW          ███████░░░ 10 tasks    Last: 1min ago         │
│  🔧 FIX             ██░░░░░░░░  3 tasks    Last: 15min ago        │
│  📚 DOCS            █████░░░░░  6 tasks    Last: 8min ago         │
│  🗺️  EXPLORE        ████████░░ 11 tasks    Last: 3min ago         │
│  📋 PLAN            ██████░░░░  7 tasks    Last: 6min ago         │
│                                                                     │
│  Total tasks: 62    Average response: 2.3s                         │
│                                                                     │
│  Press any key to continue...                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Command Palette

Press `Ctrl+P` for fuzzy search command discovery:

```
┌─ Command Palette ──────────────────────────────────────────────────┐
│                                                                     │
│  Search: arc█                                                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ 👑 /sophia        Sophia - The Architect                      │ │
│  │                   System design and architecture              │ │
│  │                                                               │ │
│  │ 🗺️  /explore       Codebase exploration agent                 │ │
│  │                   Navigate and understand code                │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ↑↓ Navigate  ⏎ Select  Esc Cancel                                │
└─────────────────────────────────────────────────────────────────────┘
```

**Features:**
- Fuzzy search (typos OK)
- Category filtering
- Real-time preview
- Keyboard navigation

---

## 🔐 Authentication

### OAuth Flow (Recommended)

Opens browser for seamless authentication:

```bash
max-code auth login

🔐 Opening browser for authentication...
📍 If browser doesn't open, visit: https://...

⏳ Waiting for authentication...
✅ Authentication successful!
💾 Token saved to ~/.claude/.credentials.json
```

### API Key (Fallback)

```bash
# Set environment variable
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Or add to .env
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> .env
```

---

## ⚡ Tips & Tricks

### 1. History Search

Press `Ctrl+R` and type to fuzzy-search your command history:

```bash
(reverse-i-search)`arch': /sophia design microservices architecture
```

### 2. Multi-line Input

For complex queries, use `\` for line continuation:

```bash
max-code ❯ /sophia design a system \
that handles 1M requests/second \
with <10ms latency
```

### 3. Combining Modes

Use DREAM mode with specific agents:

```bash
max-code 💭 ❯ /review analyze security of this auth implementation
```

### 4. Context from Files

Reference code files in your queries:

```bash
max-code ❯ /review the authentication logic in api/auth.py
```

### 5. Chaining Commands

```bash
max-code ❯ /sophia design user service
max-code ❯ /code implement the User model
max-code ❯ /test write tests for User model
max-code ❯ /review check for security issues
```

---

## 🐛 Troubleshooting

### Shell Won't Start

```bash
# Check authentication
max-code auth status

# Verify installation
max-code --version

# Check dependencies
pip install -r requirements.txt
```

### Authentication Failed

```bash
# Clear credentials and retry
rm ~/.claude/.credentials.json
max-code auth login
```

### Slow Responses

```bash
# Check API status
max-code health

# Verify network
curl https://api.anthropic.com/v1/health
```

### Commands Not Working

```bash
# Ensure shell is up-to-date
git pull origin main
pip install -e .

# Restart shell
/exit
max-code
```

---

## 📈 Performance

**Startup Time:** <200ms
**Command Response:** <100ms
**Agent Invocation:** <2s (network dependent)
**Streaming:** 20-50 chars/second (smooth, not robotic)

---

## 🏗️ Architecture

```
max-code shell
  ├─ Enhanced REPL (cli/repl_enhanced.py)
  │  ├─ Command Palette (Ctrl+P)
  │  ├─ Agent Shortcuts (8 agents)
  │  ├─ SOFIA/DREAM modes
  │  └─ Natural language processing
  │
  ├─ UI Components
  │  ├─ Banner (cinematographic welcome)
  │  ├─ Streaming (with spinner)
  │  ├─ Dashboard (agent stats)
  │  └─ Themes (5 visual styles)
  │
  ├─ Agents (8 specialized)
  │  ├─ Sophia (Architect)
  │  ├─ Code Generator
  │  ├─ Test Generator
  │  ├─ Code Reviewer
  │  ├─ Bug Fixer
  │  ├─ Documentor
  │  ├─ Explorer
  │  └─ Planner
  │
  └─ Core
     ├─ OAuth Flow (browser-based)
     ├─ LLM Client (unified interface)
     └─ Constitutional AI (P1-P6)
```

---

## 🎯 Design Philosophy

> "Like a Pagani, not a tuned Civic"

**Principles:**
- **Minimalista MAS memorável** - Clean but unforgettable
- **Cinematográfico MAS discreto** - Subtle effects, not slot machine
- **Profissional MAS com personalidade** - Functional with character

**Anti-patterns avoided:**
- ❌ Rainbow text vomit
- ❌ Excessive ASCII art
- ❌ Slow/blocking animations
- ❌ Feature bloat

**Result:**
> "Damn. This is the most beautiful CLI I've ever used."

---

## 📚 Further Reading

- [Constitutional AI v3.0](./CONSTITUIÇÃO_VÉRTICE_v3.0.md)
- [Agent System Architecture](./AGENTS.md)
- [OAuth Authentication](./AUTH.md)
- [Contributing Guide](./CONTRIBUTING.md)

---

## 🙏 Biblical Foundation

> "Porque Deus não é Deus de confusão, senão de paz"
> (1 Coríntios 14:33)

Order and clarity in all things.

**Soli Deo Gloria** 🙏

---

**Version:** 1.0.0-alpha
**Last Updated:** 2025-11-07
**Status:** 🟢 Production Ready
