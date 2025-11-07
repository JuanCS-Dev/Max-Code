# MAXIMUS SHELL - Quick Start Guide

> 🚀 Get started with the SPECTACULAR terminal interface in 2 minutes!

---

## Installation

Already have MAX-CODE CLI? You're ready!

```bash
cd max-code-cli
python3 cli/repl_enhanced.py
```

---

## First Launch

When you start MAXIMUS SHELL, you'll see:

1. ✨ **Animated Banner** - Giant ASCII art with tri-color neon gradient
2. 🎯 **Constitutional Status** - P1-P6 principles (∞P1 ⚡P2 ♥P3 ◆P4 ✦P5 ⚙P6)
3. 📊 **Status Bar** - Real-time monitoring (agents, tokens, time)
4. 🌈 **Gradient Prompt** - `maximus ⚡ ›` in beautiful colors

---

## Essential Commands

### Get Help
```bash
/help              # Show all commands
```

### Invoke Agents
```bash
/code <task>       # Generate code
/review <code>     # Review code
/fix <bug>         # Fix bugs
/test <feature>    # Generate tests
/architect <plan>  # Design architecture
```

### Keyboard Shortcuts
- `Ctrl+P` - Command palette
- `Ctrl+A` - Agent dashboard
- `Ctrl+D` - Exit
- `↑`/`↓` - Command history

---

## Example Session

```bash
maximus ⚡ › /code Create a Python function to calculate Fibonacci

💻 Invoking code agent...

# Fibonacci Calculator

Here's an efficient implementation:

```python
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number using iteration."""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

maximus ⚡ › /test fibonacci function

🧪 Invoking test agent...

[Tests generated with pytest...]

maximus ⚡ › /exit
👋 Goodbye! Soli Deo Gloria 🙏
```

---

## Status Bar

The persistent status bar shows:

```
∞P1 ⚡P2 ♥P3 ◆P4 ✦P5 ⚙P6 │ 🧠 CodeAgent │ 🧠 Sonnet 4.5 │ ⚡ 2.4K/200K (1%) │ ⏱ 00:15
```

- **P1-P6**: Constitutional Principles (always active)
- **Agent**: Current agent name and status
- **Model**: Claude Sonnet 4.5
- **Tokens**: Usage with color warning (green → yellow → red)
- **Time**: Session duration

---

## Tips

1. **Watch the status bar** - Know which agent is working
2. **Monitor tokens** - Color changes when usage is high
3. **Use markdown** - Responses render beautifully
4. **Try shortcuts** - `Ctrl+P` is your friend
5. **Explore commands** - Type `/help` to see all options

---

## Need More?

- 📚 **Full Documentation**: [MAXIMUS_SHELL_v3.md](./MAXIMUS_SHELL_v3.md)
- 🎨 **Color System**: See color customization options
- 🔧 **Advanced Usage**: Custom gradients, status bar plugins
- 🐛 **Troubleshooting**: Common issues and solutions

---

**Welcome to MAXIMUS SHELL v3.0!** 🎉

*Built with Constitutional AI principles • Powered by Claude Sonnet 4.5*
