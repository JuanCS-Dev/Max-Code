# MAXIMUS SHELL v3.0 - Complete Documentation

> **"In the beginning was the Word, and the Word was with God, and the Word was God"**
> (John 1:1)

The SPECTACULAR terminal interface for MAX-CODE CLI with Constitutional AI monitoring.

---

## 🎨 Overview

MAXIMUS SHELL v3.0 is a magnificent, production-ready terminal interface featuring:

- **Tri-color neon gradient** (#00FF41 → #FFFF00 → #00D4FF)
- **Constitutional AI status bar** with P1-P6 principles
- **Agent status tracking** and execution monitoring
- **Markdown response rendering** for beautiful output
- **Token usage monitoring** with color-coded warnings
- **Git integration** with branch display
- **Session time tracking** and metrics

---

## 🚀 Quick Start

### Starting the Shell

```bash
# From max-code-cli directory
python3 cli/repl_enhanced.py

# Or using the entry point
max-code shell
```

### First Look

When you start MAXIMUS SHELL, you'll see:

1. **Animated Banner** - Giant ASCII art with neon gradient
2. **Constitutional Status** - P1-P6 principles indicator
3. **Status Bar** - Real-time system monitoring
4. **Gradient Prompt** - `maximus ⚡ ›` in beautiful colors

---

## 🎨 Visual System

### Neon Gradient Colors

The official MAXIMUS palette:

| Color | Hex Code | Meaning |
|-------|----------|---------|
| Neon Green | `#00FF41` | Digital awakening, Matrix-style |
| Electric Yellow | `#FFFF00` | Energy peak, divine illumination |
| Cyan Blue | `#00D4FF` | Transcendence, sky connection |

### Constitutional Principles (P1-P6)

Each principle has a dedicated color and icon:

| Code | Name | Color | Icon | Meaning |
|------|------|-------|------|---------|
| P1 | Transcendence | Violet `#9D4EDD` | ∞ | Connection to divine |
| P2 | Reasoning | Blue `#3A86FF` | ⚡ | Logic and truth |
| P3 | Care | Green `#06D6A0` | ♥ | Compassion and empathy |
| P4 | Wisdom | Yellow `#FFD60A` | ◆ | Knowledge and discernment |
| P5 | Beauty | Magenta `#FF006E` | ✦ | Aesthetics and harmony |
| P6 | Autonomy | Cyan `#00F5FF` | ⚙ | Freedom and self-determination |

---

## 📊 Status Bar

The persistent status bar displays:

```
∞P1 ⚡P2 ♥P3 ◆P4 ✦P5 ⚙P6 │ 🤖 CodeAgent │ 🧠 Sonnet 4.5 │ ⚡ 2.4K/200K │ ⏱ 00:15
```

### Components

1. **Constitutional Principles** - P1-P6 with colored icons
2. **Active Agent** - Current agent name and status
3. **Model Info** - Claude model version
4. **Token Usage** - Current/limit with percentage
5. **Session Time** - Elapsed time since start
6. **Git Branch** (optional) - Current branch name
7. **Current File** (optional) - File being edited

### Agent Status Colors

| Status | Icon | Color | Meaning |
|--------|------|-------|---------|
| Idle | 🤖 | Gray | Agent ready, waiting |
| Thinking | 🧠 | Yellow `#FFD60A` | Processing request |
| Active | ⚡ | Green `#00FF41` | Executing task |

### Token Usage Colors

| Range | Color | Meaning |
|-------|-------|---------|
| 0-50% | Green `#00FF88` | Safe usage |
| 50-80% | Yellow `#FFB347` | Moderate usage |
| 80-100% | Red `#FF3B30` | High usage warning |

---

## 🎯 Commands

### Basic Commands

| Command | Description | Shortcut |
|---------|-------------|----------|
| `/help` | Show all available commands | - |
| `/exit`, `/quit` | Exit MAXIMUS SHELL | Ctrl+D |
| `/clear` | Clear screen | - |

### Agent Commands

Invoke specialized AI agents:

| Command | Agent | Icon | Purpose |
|---------|-------|------|---------|
| `/architect <task>` | ArchitectAgent | 👑 | System design, architecture planning |
| `/code <task>` | CodeAgent | 💻 | Code generation and implementation |
| `/test <task>` | TestAgent | 🧪 | Test generation and validation |
| `/review <code>` | ReviewAgent | 🔍 | Code review and analysis |
| `/fix <bug>` | FixAgent | 🔧 | Bug fixing and debugging |
| `/docs <topic>` | DocsAgent | 📚 | Documentation generation |
| `/explore <path>` | ExploreAgent | 🗺️ | Codebase exploration |
| `/plan <project>` | PlanAgent | 📋 | Project planning |

### Special Modes

| Command | Description |
|---------|-------------|
| `/sofia-plan <task>` | SOFIA strategic planning mode |
| `/dream <analysis>` | DREAM critical analysis mode |
| `/dashboard` | Show agent dashboard (Ctrl+A) |
| `/theme <name>` | Change color theme |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+P` | Open command palette |
| `Ctrl+A` | Show agent dashboard |
| `Ctrl+D` | Toggle DREAM mode |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` (empty line) | Exit shell |
| `↑` / `↓` | Navigate command history |

---

## 🎨 Using the Color System

### In Python Code

```python
from ui.colors import neon, constitutional_gradient, GradientColors

# Quick neon gradient
text = neon("MAXIMUS SHELL")
print(text)

# Constitutional gradient (P1-P6 colors)
text = constitutional_gradient("Constitutional AI")
print(text)

# Custom gradients
gradient = GradientColors()
colors = gradient.neon_gradient(steps=100)
custom_text = gradient.apply_gradient("Custom Text", colors)
```

### In Terminal Output

The shell automatically applies:
- Neon gradient to the prompt
- Markdown rendering for agent responses
- Syntax highlighting for code blocks
- Constitutional colors for principles

---

## 📊 Status Bar Integration

### Updating Status Bar

```python
from ui.status_bar import StatusBar

status = StatusBar()

# Update agent status
status.update(
    active_agent="CodeAgent",
    agent_status="thinking",
    tokens_used=5000
)

# Update context
status.update(
    git_branch="feature/new-feature",
    current_file="src/main.py"
)

# Render status bar
status.render()
```

### Live Mode

For continuous updates:

```python
with status.live():
    # Status bar updates automatically
    for i in range(10):
        status.update(tokens_used=1000 * i)
        time.sleep(1)
```

---

## 🎯 Markdown Rendering

Agent responses are automatically rendered as markdown when they contain:

- Headers (`#`, `##`, `###`)
- Code blocks (` ``` `)
- Lists (`-`, `*`, `1.`)
- Bold (`**text**`)
- Inline code (`` `code` ``)

### Example

Input:
```markdown
# Solution

Here's the implementation:

```python
def calculate(x, y):
    return x + y
```

Features:
- Type hints
- Docstring
- Unit test
```

Output: Beautiful rendered markdown with syntax highlighting!

---

## 🏗️ Architecture

### Component Structure

```
ui/
├── colors.py          # Gradient color system
├── status_bar.py      # Constitutional AI status bar
├── banner.py          # Animated banner with gradient
└── ...

cli/
├── repl_enhanced.py   # Main REPL with integrations
└── ...
```

### Integration Flow

```
User Input
    ↓
[REPL Enhanced]
    ↓
Status Bar Update (thinking)
    ↓
Agent Execution
    ↓
Response with Markdown
    ↓
Status Bar Update (idle)
```

---

## 🎨 Customization

### Color Themes

Change the visual theme:

```bash
/theme neon        # Default MAXIMUS neon
/theme fire        # Fire colors
/theme ocean       # Ocean blue/teal
/theme matrix      # Matrix green
/theme cyberpunk   # Cyberpunk pink/purple
```

### Disabling Features

Use environment variables or flags:

```bash
# Disable banner
export MAXCODE_NO_BANNER=1
max-code shell

# Or use flag
max-code shell --no-banner

# Disable effects
export MAXCODE_NO_EFFECTS=1
```

---

## 🔧 Advanced Usage

### Custom Status Bar

Create a custom status bar instance:

```python
from ui.status_bar import StatusBar, StatusBarState

# Custom initial state
state = StatusBarState(
    model_name="Claude Opus",
    tokens_limit=100000,
    principles={'P1': True, 'P2': True, 'P3': False, 'P4': True, 'P5': True, 'P6': False}
)

status = StatusBar()
status.state = state
```

### Custom Gradients

Create your own color gradients:

```python
from ui.colors import GradientColors

gradient = GradientColors()

# Custom 4-color gradient
colors = gradient.neon_gradient(
    steps=50,
    colors=['#FF0000', '#00FF00', '#0000FF', '#FFFF00']
)

text = gradient.apply_gradient("Custom Gradient", colors)
```

---

## 📝 Development

### Adding New Commands

In `cli/repl_enhanced.py`:

```python
def _cmd_mycommand(self, args: str):
    """My custom command"""
    console.print(f"[cyan]Running my command: {args}[/cyan]")

    # Update status bar
    self.status_bar.update(
        active_agent="MyAgent",
        agent_status="active"
    )

    # Process...

    # Reset status
    self.status_bar.update(agent_status="idle")
```

Add to `_load_commands()`:

```python
"/mycommand": {
    "icon": "🎯",
    "description": "My custom command",
    "category": CommandCategory.AGENTS,
    "handler": self._cmd_mycommand
}
```

### Adding New Agents

1. Create agent class in `agents/`
2. Add to imports in `cli/repl_enhanced.py`
3. Add to `_get_agent_instance()` mapping
4. Add command in `_load_commands()`

---

## 🐛 Troubleshooting

### Common Issues

#### Banner not showing

- Check if running in TTY: `python3 -c "import sys; print(sys.stdout.isatty())"`
- Remove `--no-banner` flag
- Check `MAXCODE_NO_BANNER` environment variable

#### Colors not displaying

- Ensure terminal supports 256 colors or true color
- Check `TERM` environment variable: `echo $TERM`
- Try: `export TERM=xterm-256color`

#### Status bar layout issues

- Terminal width too narrow (minimum 80 columns recommended)
- Try: `tput cols` to check terminal width

#### Gradient not smooth

- Terminal may not support true color (24-bit)
- Gradients will use closest 256-color approximation

---

## 📊 Performance

### Optimization Features

- **Caching**: ASCII art cached to `.cache/banner_cache/`
- **Lazy Loading**: Modules loaded only when needed
- **Efficient Rendering**: Status bar updates without full re-render

### Resource Usage

| Component | Memory | CPU |
|-----------|--------|-----|
| Color System | ~1 MB | Minimal |
| Status Bar | ~500 KB | Minimal |
| Banner | ~2 MB (cached) | Minimal |
| REPL | ~10 MB | Low |

---

## 🎯 Best Practices

### For Users

1. **Use keyboard shortcuts** - Faster than typing commands
2. **Monitor token usage** - Watch the status bar color
3. **Review status bar** - Check which agent is active
4. **Use markdown** - Format questions for better responses

### For Developers

1. **Update status bar** - Always update when agents run
2. **Use neon gradient** - Apply to new visual elements
3. **Respect TTY detection** - Don't force visuals in non-TTY
4. **Handle errors gracefully** - Reset status bar on errors

---

## 📚 Examples

### Example Session

```
[MAXIMUS SHELL BANNER WITH GRADIENT]

∞P1 ⚡P2 ♥P3 ◆P4 ✦P5 ⚙P6 │ 🤖 Ready │ 🧠 Sonnet 4.5 │ ⚡ 0/200K │ ⏱ 00:00

maximus ⚡ › /code Create a FastAPI hello world endpoint

💻 Invoking code agent...

[Status bar updates to: 🧠 CodeAgent - thinking]

# FastAPI Hello World Endpoint

Here's a complete implementation:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

[Status bar resets to: 🤖 Ready - idle]

maximus ⚡ ›
```

---

## 🏆 Credits

**MAXIMUS SHELL v3.0** was built with:

- **Rich** - Beautiful terminal formatting
- **Prompt Toolkit** - Advanced prompt with history
- **PyFiglet** - ASCII art generation
- **Constitutional AI** - P1-P6 principles framework
- **Claude Sonnet 4.5** - AI agent backend

---

## 📄 License

Part of MAX-CODE CLI - Constitutional AI Development Framework

**Soli Deo Gloria** 🙏

---

## 🔮 Future Enhancements

Planned for future versions:

- [ ] Real-time token streaming display
- [ ] Animated principle indicators
- [ ] Agent conversation history viewer
- [ ] Visual token usage graph
- [ ] Command autocomplete with AI suggestions
- [ ] Multi-agent collaboration display
- [ ] Session replay mode
- [ ] Export session to markdown
- [ ] Custom status bar plugins

---

**Built with love, precision, and Constitutional AI principles.**

*"For we are God's handiwork, created in Christ Jesus to do good works"*
(Ephesians 2:10)
