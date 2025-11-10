# Max-Code CLI UI/UX - User Guide

**Version:** 1.0.0
**Date:** 2025-11-04
**Framework:** Constitutional AI v3.0

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Banner Systems](#banner-systems)
3. [Formatting & Output](#formatting--output)
4. [Progress Indicators](#progress-indicators)
5. [Agent Display](#agent-display)
6. [Interactive Menus](#interactive-menus)
7. [Tree of Thoughts](#tree-of-thoughts)
8. [Streaming Output](#streaming-output)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

```bash
# The UI module is already included in Max-Code CLI
cd "/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli"
python3 -m ui.demo  # Run the demo
```

### Quick Example

```python
from ui import get_banner, get_formatter

# Show banner
banner = get_banner()
banner.show(version="3.0")

# Format messages
fmt = get_formatter()
fmt.print_success("Max-Code CLI initialized!")
```

---

## Banner Systems

### PyFiglet Style (Default)

Bold, beautiful ASCII art with neon gradient.

```python
from ui.banner import MaxCodeBanner

banner = MaxCodeBanner()
banner.show(
    version="3.0",
    context={'model': 'Claude Sonnet 4.5'},
    style='default'  # or 'isometric', 'banner', 'bold'
)
```

**Styles Available:**
- `default` - BLOCK font (Gemini-inspired) ⭐
- `isometric` - 3D isometric blocks
- `banner` - Bold banner style
- `bold` - Colossal letters
- `tech` - Tech/doom style
- `cyber` - Graffiti/cyber style

### vCLI-Go Style

Professional, production-focused with detailed info.

```python
from ui.banner_vcli_style import show_banner

show_banner(version="3.0", build_date="2025-11-04")
```

---

## Formatting & Output

### Semantic Messages

```python
from ui.formatter import MaxCodeFormatter

fmt = MaxCodeFormatter()

# Success
fmt.print_success("Operation completed!")

# Error
fmt.print_error("Connection failed", "Check network")

# Warning
fmt.print_warning("Memory usage high")

# Info
fmt.print_info("Processing 1000 items")

# Debug
fmt.print_debug("Variable x = 42")
```

### Agent Messages

```python
# Message from specific agent
fmt.print_agent_message(
    "Sophia",
    "Architecture analysis complete",
    "Analyzing"  # Action verb
)
```

### Code Highlighting

```python
code = '''
def hello():
    print("Hello World!")
'''

fmt.print_code(code, language="python")
```

### Tables

```python
data = [
    {"Name": "Agent 1", "Status": "Active"},
    {"Name": "Agent 2", "Status": "Idle"},
]

fmt.print_table(data, title="Agents")
```

### Constitutional Status

```python
status = {
    'p1': True,
    'p2': True,
    'p3': False,
    'p4': True,
    'p5': True,
    'p6': True,
}

fmt.print_constitutional_status(status)
```

---

## Progress Indicators

### Simple Spinner

```python
from ui.progress import MaxCodeProgress

progress = MaxCodeProgress()

with progress.spinner("Loading..."):
    # Do work
    time.sleep(2)
```

### Progress Bar

```python
with progress.bar(total=100, description="Processing") as bar:
    for i in range(100):
        # Do work
        bar.advance(1)
```

### Multi-Progress (Parallel Operations)

```python
tasks = [
    {'name': 'Download', 'total': 100, 'color': 'cyan'},
    {'name': 'Process', 'total': 80, 'color': 'green'},
    {'name': 'Upload', 'total': 50, 'color': 'yellow'},
]

with progress.multi_progress(tasks) as bars:
    # Update individual bars
    bars['Download'].advance(10)
    bars['Process'].advance(5)
    bars['Upload'].advance(2)
```

### Agent Activity

```python
agents_data = [
    {'name': 'Sophia', 'status': 'active', 'task': 'Analysis', 'progress': 75},
    {'name': 'Code', 'status': 'idle', 'task': 'Waiting', 'progress': 0},
]

progress.show_agent_activity(agents_data)
```

---

## Agent Display

### Dashboard

```python
from ui.agents import AgentDisplay, Agent, AgentStatus

display = AgentDisplay()

agents = [
    Agent("Sophia", "Architect", AgentStatus.ACTIVE, "Analyzing", 75),
    Agent("Code", "Developer", AgentStatus.ACTIVE, "Coding", 50),
    Agent("Test", "Validator", AgentStatus.IDLE, "Waiting", 0),
]

display.show_dashboard(agents)
```

### Timeline

```python
from datetime import datetime

events = [
    AgentEvent(datetime.now(), "Sophia", "Started analysis"),
    AgentEvent(datetime.now(), "Code", "Implementing feature"),
]

display.show_timeline(events)
```

### Communication Flow

```python
messages = [
    AgentMessage("Sophia", "Code", "request", "received", datetime.now()),
    AgentMessage("Code", "Test", "update", "sent", datetime.now()),
]

display.show_communication(messages)
```

---

## Interactive Menus

### Selection Menu

```python
from ui.menus import SelectionMenu, MenuItem

menu = SelectionMenu()

items = [
    MenuItem("Option 1", "value1", "First option", "cyan"),
    MenuItem("Option 2", "value2", "Second option", "green"),
    MenuItem("Option 3", "value3", "Third option", "yellow"),
]

selected = menu.select(items, title="Choose Option")
if selected:
    print(f"You selected: {selected.label}")
```

### Multi-Select

```python
selected_items = menu.select_multiple(
    items,
    title="Select Features",
    min_choices=1,
    max_choices=3
)
```

### Configuration Editor

```python
from ui.menus import ConfigMenu

config_menu = ConfigMenu()

config = {
    "model": "claude-sonnet-4.5",
    "temperature": 0.7,
    "max_tokens": 4096,
}

descriptions = {
    "model": "AI model to use",
    "temperature": "Sampling temperature (0-1)",
    "max_tokens": "Maximum tokens per response",
}

new_config = config_menu.edit_config(config, descriptions=descriptions)
```

### Command Palette

```python
from ui.menus import CommandPalette, Command

palette = CommandPalette()

commands = [
    Command("analyze", "Analyze code", "Ctrl+A"),
    Command("generate", "Generate code", "Ctrl+G"),
    Command("test", "Run tests", "Ctrl+T"),
]

selected_cmd = palette.show(commands)
if selected_cmd:
    selected_cmd.callback()  # Execute command
```

---

## Tree of Thoughts

### Visualize Reasoning Tree

```python
from ui.tree_of_thoughts import ThoughtTree, ThoughtNode, BranchStatus

tree = ThoughtTree()

root = ThoughtNode("root", "Implement authentication", 7.5, BranchStatus.ACTIVE)

children = {
    "root": [
        ThoughtNode("oauth", "OAuth 2.0", 8.5, BranchStatus.BEST, "root", 1),
        ThoughtNode("jwt", "JWT tokens", 7.5, BranchStatus.ACTIVE, "root", 1),
        ThoughtNode("sessions", "Sessions", 6.0, BranchStatus.PRUNED, "root", 1),
    ]
}

tree.show_tree(root, children)
```

### Reasoning Steps

```python
from ui.tree_of_thoughts import ReasoningSteps, ReasoningStep

reasoning = ReasoningSteps()

steps = [
    ReasoningStep(1, "Analyze requirements", "Need secure solution", 8.0, "continue", "Clear"),
    ReasoningStep(2, "Evaluate options", "OAuth is best", 8.5, "select", "Best choice"),
]

reasoning.show_steps(steps)
```

### Constitutional Analysis

```python
from ui.tree_of_thoughts import ConstitutionalAnalysis, ConstitutionalScore

analysis = ConstitutionalAnalysis()

scores = [
    ConstitutionalScore("P1", "Transcendence", 8.0, "Enables user goals", color="violet"),
    ConstitutionalScore("P2", "Reasoning", 9.0, "Well-reasoned", color="blue"),
    ConstitutionalScore("P3", "Care", 8.5, "Protects users", color="green"),
]

analysis.show_analysis(scores)
analysis.show_radar_chart(scores)
```

---

## Streaming Output

### Text Streaming

```python
from ui.streaming import StreamingDisplay

stream = StreamingDisplay()

def text_generator():
    for word in "Hello from Max-Code!".split():
        yield word + " "

stream.stream_text(text_generator(), prefix="Output:", style="cyan")
```

### Live Log Viewer

```python
from ui.streaming import LiveLogViewer, LogEntry, LogLevel
from datetime import datetime

log_viewer = LiveLogViewer()

def log_generator():
    yield LogEntry(datetime.now(), LogLevel.INFO, "Starting...", "System")
    yield LogEntry(datetime.now(), LogLevel.ERROR, "Error occurred", "Test")

log_viewer.view_logs_table(log_generator())
```

### Multi-Stream Progress

```python
from ui.streaming import ProgressStream, StreamUpdate

progress_stream = ProgressStream()

def progress_generator():
    for i in range(100):
        yield StreamUpdate("download", "Downloading", i, 100, "active")

progress_stream.stream_progress(progress_generator())
```

---

## Configuration

### Environment Variables

```bash
# Disable banner
export MAX_CODE_NO_BANNER=1

# Disable colors
export NO_COLOR=1

# Quiet mode
export MAX_CODE_QUIET=1
```

### Command Line Flags

```bash
max-code --no-banner    # Skip banner
max-code --quiet        # Minimal output
max-code --verbose      # Detailed output
```

---

## Troubleshooting

### Banner Not Showing

**Problem:** Banner doesn't display

**Solutions:**
1. Check if `NO_COLOR` is set: `echo $NO_COLOR`
2. Check if `MAX_CODE_NO_BANNER` is set
3. Verify terminal supports colors: `echo $TERM`

### Colors Not Working

**Problem:** Output is plain text

**Solutions:**
1. Unset `NO_COLOR`: `unset NO_COLOR`
2. Check terminal capabilities
3. Use a modern terminal (iTerm2, Windows Terminal, etc.)

### Performance Issues

**Problem:** UI is slow

**Solutions:**
1. Use `fast_import` for faster loading:
   ```python
   from ui.fast_import import fast_banner
   banner = fast_banner()
   ```
2. Reduce live update frequency
3. Limit table row count

### Import Errors

**Problem:** `ModuleNotFoundError`

**Solutions:**
1. Install dependencies:
   ```bash
   pip install rich rich-gradient pyfiglet yaspin
   ```
2. Check Python path
3. Verify installation

---

## Best Practices

### Performance

1. Use lazy imports for faster startup
2. Limit live updates to 10-20 FPS
3. Truncate long text
4. Use tables for small datasets (<500 rows)

### User Experience

1. Show progress for operations >1 second
2. Provide clear error messages
3. Use semantic colors consistently
4. Keep text concise and scannable

### Accessibility

1. Respect `NO_COLOR` environment
2. Provide text alternatives for symbols
3. Use high contrast colors
4. Support terminal resizing

---

## Examples

See `ui/demo.py` for comprehensive examples of all features!

```bash
python3 ui/demo.py
```

---

## Support

**Documentation:** `/docs/ui/`
**Examples:** `/ui/demo.py`
**Tests:** `/tests/`
**Issues:** GitHub Issues

---

*Framework: Constitutional AI v3.0*
*Model: Claude Sonnet 4.5*
*Date: 2025-11-04*
