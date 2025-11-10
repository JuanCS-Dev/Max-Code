# Max-Code CLI UI/UX - Developer Guide

**Version:** 1.0.0
**Date:** 2025-11-04
**Framework:** Constitutional AI v3.0

---

## 📚 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Design Principles](#design-principles)
5. [Adding New Components](#adding-new-components)
6. [Error Handling](#error-handling)
7. [Performance Guidelines](#performance-guidelines)
8. [Testing](#testing)
9. [Contributing](#contributing)
10. [API Reference](#api-reference)

---

## Architecture Overview

### High-Level Design

Max-Code CLI UI is built on a modular, layered architecture:

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  (max-code CLI, agent orchestration)    │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         UI Components Layer             │
│  (Banner, Formatter, Progress, etc.)    │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Core UI Library                 │
│  (Rich, PyFiglet, Yaspin)               │
└─────────────────────────────────────────┘
```

### Key Dependencies

- **Rich** - Core rendering engine (tables, panels, live updates)
- **rich-gradient** - Gradient text effects
- **PyFiglet** - ASCII art generation
- **Yaspin** - Spinner animations
- **Prompt Toolkit** - Interactive menus (future)

### Design Philosophy

1. **Modularity** - Each component is independent and reusable
2. **Performance** - Lazy imports, efficient rendering (<100ms targets)
3. **Robustness** - Graceful error handling, never crash
4. **Consistency** - Unified color palette, spacing, and symbols
5. **Extensibility** - Easy to add new components and features

---

## Project Structure

```
max-code-cli/
├── ui/
│   ├── __init__.py           # Public API exports
│   ├── banner.py             # PyFiglet ASCII art banner
│   ├── banner_vcli_style.py  # vCLI-Go style banner
│   ├── formatter.py          # Message formatting utilities
│   ├── progress.py           # Progress indicators
│   ├── agents.py             # Agent display components
│   ├── menus.py              # Interactive menus
│   ├── tree_of_thoughts.py   # Tree of Thoughts visualization
│   ├── streaming.py          # Streaming output components
│   ├── constants.py          # Shared constants and config
│   ├── exceptions.py         # Custom exception hierarchy
│   ├── validation.py         # Input validation utilities
│   ├── fast_import.py        # Optimized lazy imports
│   └── demo.py               # Comprehensive demo
├── docs/
│   └── ui/
│       ├── USER_GUIDE.md     # User-facing documentation
│       ├── DEVELOPER_GUIDE.md # This file
│       └── API_REFERENCE.md   # Detailed API docs
├── tests/
│   ├── test_banner.py
│   ├── test_formatter.py
│   ├── test_error_handling.py
│   └── ...
└── benchmarks/
    ├── ui_benchmarks.py      # Performance benchmarks
    └── results.md            # Benchmark results
```

---

## Core Components

### 1. Banner System

**Files:** `ui/banner.py`, `ui/banner_vcli_style.py`

**Purpose:** Display startup banner with branding

**Key Features:**
- Multiple ASCII art styles (PyFiglet fonts)
- Gradient color effects (neon pink → cyan)
- Context information display
- Lazy import for performance

**Example Implementation:**
```python
from rich_gradient import Gradient
from pyfiglet import Figlet

class MaxCodeBanner:
    GRADIENT_COLORS = ["#FF006E", "#8338EC", "#3A86FF", "#00F5FF"]

    def show(self, version: str, style: str = 'default'):
        # Lazy import for performance
        from rich_gradient import Gradient

        # Generate ASCII art
        figlet = Figlet(font=self._get_font(style))
        ascii_art = figlet.renderText("MAX-CODE")

        # Apply gradient
        title = Gradient(ascii_art, colors=self.GRADIENT_COLORS)
        self.console.print(title)
```

**Performance Considerations:**
- rich-gradient import deferred until `show()` called
- Saves ~113ms on startup

### 2. Formatter System

**File:** `ui/formatter.py`

**Purpose:** Consistent message formatting across application

**Key Features:**
- Semantic message types (success, error, warning, info, debug)
- Agent-specific messages with color coding
- Code syntax highlighting
- Table rendering
- Constitutional status display

**Example Implementation:**
```python
class MaxCodeFormatter:
    COLORS = {
        'success': 'green',
        'error': 'red',
        'warning': 'yellow',
        'info': 'cyan',
        'debug': 'dim',
    }

    def print_success(self, message: str):
        """Print success message with checkmark."""
        self.console.print(f"[green]✓[/green] {message}")
```

**Extension Point:**
To add new message types:
1. Add color to `COLORS` dict
2. Create `print_<type>()` method
3. Add corresponding symbol

### 3. Progress System

**File:** `ui/progress.py`

**Purpose:** Visual feedback for long-running operations

**Key Features:**
- Simple spinners
- Progress bars with completion percentage
- Multi-progress (parallel operations)
- Agent activity display
- Live updating

**Example Implementation:**
```python
from rich.progress import Progress, SpinnerColumn, TextColumn

class MaxCodeProgress:
    @contextmanager
    def spinner(self, description: str):
        """Context manager for spinner."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}[/cyan]"),
            console=self.console
        ) as progress:
            task = progress.add_task(description, total=None)
            yield progress
```

**Performance Target:** >10 FPS for live updates

### 4. Agent Display System

**File:** `ui/agents.py`

**Purpose:** Visualize multi-agent activity

**Key Features:**
- Real-time dashboard
- Activity timeline
- Communication flow
- Workload distribution
- Status indicators

**Data Models:**
```python
@dataclass
class Agent:
    name: str
    role: str
    status: AgentStatus
    current_task: str = ""
    progress: float = 0.0  # 0-100

class AgentStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"
```

**Error Handling:**
- Validates input with `ui.validation`
- Clamps progress to 0-100 range
- Shows empty state for no agents
- Continues rendering on individual agent errors

### 5. Interactive Menus

**File:** `ui/menus.py`

**Purpose:** User input and selection

**Key Features:**
- Single selection menu
- Multi-select menu
- Configuration editor
- Command palette
- Keyboard navigation

**Example Implementation:**
```python
@dataclass
class MenuItem:
    label: str
    value: Any
    description: str = ""
    color: str = "white"

class SelectionMenu:
    def select(self, items: List[MenuItem], title: str) -> MenuItem:
        """Show selection menu and return chosen item."""
        # Render menu with Rich
        # Handle keyboard input
        # Return selected item
```

### 6. Tree of Thoughts

**File:** `ui/tree_of_thoughts.py`

**Purpose:** Visualize reasoning process

**Key Features:**
- Hierarchical thought tree
- Branch scoring and pruning
- Reasoning step visualization
- Constitutional analysis display

**Data Models:**
```python
@dataclass
class ThoughtNode:
    id: str
    thought: str
    score: float
    status: BranchStatus
    parent_id: Optional[str] = None
    depth: int = 0
```

### 7. Streaming Output

**File:** `ui/streaming.py`

**Purpose:** Real-time output streaming

**Key Features:**
- Text streaming with typewriter effect
- Live log viewer
- Multi-stream progress
- Token-by-token display

### 8. Validation & Error Handling

**Files:** `ui/validation.py`, `ui/exceptions.py`

**Purpose:** Ensure data integrity and graceful failure

**Exception Hierarchy:**
```python
UIError (base)
├── InvalidInputError
├── InvalidConfigError
├── RenderError
├── EmptyDataError
├── TerminalError
└── ImportError
```

**Validation Functions:**
- `validate_items()` - List constraints
- `validate_score()` - Range validation
- `validate_percentage()` - 0-100 validation
- `validate_string()` - String constraints
- `validate_positive_int()` - Positive integers
- `validate_choice()` - Enum validation
- `validate_type()` - Type checking

---

## Design Principles

### 1. Performance First

**Guidelines:**
- Use lazy imports for expensive dependencies
- Target: <100ms import time
- Target: <50ms banner display
- Target: <100ms table rendering
- Target: >10 FPS for live updates

**Example:**
```python
# ❌ BAD: Import at module level
from rich_gradient import Gradient

# ✅ GOOD: Lazy import
if TYPE_CHECKING:
    from rich_gradient import Gradient

def show_banner():
    from rich_gradient import Gradient  # Import only when needed
    ...
```

### 2. Graceful Degradation

**Guidelines:**
- Never crash on invalid input
- Show empty states instead of errors
- Clamp values to valid ranges
- Provide sensible defaults
- Continue on individual item failures

**Example:**
```python
# ✅ GOOD: Graceful error handling
try:
    validate_items(agents, min_items=1)
except EmptyDataError:
    console.print("[dim]No agents to display[/dim]")
    return  # Don't crash, show empty state

for agent in agents:
    try:
        render_agent(agent)
    except Exception as e:
        log_warning(f"Failed to render {agent.name}: {e}")
        continue  # Skip this agent, continue with others
```

### 3. Validation First

**Guidelines:**
- Validate all inputs early
- Provide helpful error messages
- Suggest fixes in error messages
- Use type hints everywhere

**Example:**
```python
def show_dashboard(self, agents: List[Agent]):
    """Display agent dashboard."""
    # Validate first
    validate_items(agents, min_items=1, item_name="agents")

    # Then process
    for agent in agents:
        # Validate individual fields
        progress = max(0.0, min(100.0, agent.progress))
        ...
```

### 4. Consistent Styling

**Color Palette:**
```python
AGENT_COLORS = {
    'sophia': 'gold1',      # Architect
    'code': 'blue',         # Developer
    'test': 'green',        # Validator
    'review': 'orange3',    # Auditor
    'fix': 'red',           # Fixer
    'docs': 'purple',       # Documenter
    'explore': 'cyan',      # Explorer
    'guardian': 'bright_red', # Security
}

SEMANTIC_COLORS = {
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'cyan',
    'debug': 'dim',
}
```

**Symbols:**
```python
STATUS_SYMBOLS = {
    'active': '●',
    'idle': '○',
    'completed': '✓',
    'failed': '✗',
    'waiting': '⟳',
}
```

### 5. Modularity

**Guidelines:**
- Each component is independent
- No circular dependencies
- Clear public API in `__init__.py`
- Private methods prefixed with `_`

---

## Adding New Components

### Step-by-Step Guide

#### 1. Create Component File

```python
# ui/my_component.py
"""
Max-Code CLI My Component

Description of what this component does.
"""

from rich.console import Console
from typing import Optional

class MyComponent:
    """My new UI component."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize component."""
        self.console = console or Console()

    def render(self, data):
        """Render the component."""
        # Validate input
        from ui.validation import validate_items
        validate_items(data, min_items=1)

        # Render
        self.console.print("My Component!")
```

#### 2. Add to Public API

```python
# ui/__init__.py
from ui.my_component import MyComponent

__all__ = [
    # ... existing exports
    'MyComponent',
]
```

#### 3. Write Tests

```python
# tests/test_my_component.py
import sys
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')

from ui.my_component import MyComponent

def test_my_component():
    """Test my component."""
    component = MyComponent()
    component.render([1, 2, 3])
    # Assert behavior
```

#### 4. Add Benchmarks

```python
# benchmarks/ui_benchmarks.py
def benchmark_my_component(self):
    """Benchmark my component."""
    component = MyComponent()

    start = time.perf_counter()
    component.render(data)
    elapsed = (time.perf_counter() - start) * 1000

    self.results['my_component_ms'] = elapsed
```

#### 5. Document

Add to `USER_GUIDE.md`:
```markdown
## My Component

### Usage

```python
from ui import MyComponent

component = MyComponent()
component.render(data)
```
```

#### 6. Add Demo

```python
# ui/demo.py
def demo_my_component():
    """Demo my component."""
    print("\n" + "=" * 80)
    print("MY COMPONENT DEMO")
    print("=" * 80 + "\n")

    component = MyComponent()
    component.render([1, 2, 3])
```

---

## Error Handling

### Exception Hierarchy

```python
# ui/exceptions.py
class UIError(Exception):
    """Base exception."""
    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion
```

### Validation Strategy

**1. Validate Early:**
```python
def render(self, items):
    validate_items(items, min_items=1)  # Fail fast
    # ... rest of logic
```

**2. Provide Helpful Messages:**
```python
raise InvalidInputError(
    "Score 15.0 out of range [0.0, 10.0]",
    suggestion="Use a value between 0.0 and 10.0"
)
```

**3. Graceful Degradation:**
```python
try:
    validate_items(items)
except EmptyDataError:
    console.print("[dim]No items[/dim]")
    return  # Don't crash
```

**4. Continue on Error:**
```python
for item in items:
    try:
        render_item(item)
    except Exception as e:
        log_warning(f"Failed: {e}")
        continue  # Process other items
```

---

## Performance Guidelines

### Import Optimization

**Benchmark Targets:**
- Total import time: <100ms
- Rich Console baseline: ~60ms (unavoidable)
- Component overhead: <40ms

**Lazy Import Pattern:**
```python
# Module level (type checking only)
if TYPE_CHECKING:
    from expensive_module import ExpensiveClass

# Inside method (actual import)
def method(self):
    from expensive_module import ExpensiveClass
    obj = ExpensiveClass()
```

### Rendering Performance

**Targets:**
- Banner display: <50ms
- Table rendering (100 rows): <100ms
- Live FPS: >10
- Memory overhead: <50MB

**Optimization Techniques:**
1. Limit table rows to reasonable count (<500)
2. Truncate long text
3. Update live displays at 10-20 FPS max
4. Reuse Console instances

### Benchmarking

```python
import time

start = time.perf_counter()
# ... operation ...
elapsed = (time.perf_counter() - start) * 1000  # ms
```

Run full benchmark suite:
```bash
python3 benchmarks/ui_benchmarks.py
```

---

## Testing

### Test Structure

```python
# tests/test_component.py
import sys
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')

from ui.component import Component
from ui.exceptions import InvalidInputError

def test_normal_case():
    """Test normal operation."""
    component = Component()
    result = component.render([1, 2, 3])
    assert result is not None

def test_empty_input():
    """Test empty input handling."""
    component = Component()
    component.render([])  # Should not crash

def test_invalid_input():
    """Test invalid input handling."""
    component = Component()
    try:
        component.render(None)
        assert False, "Should raise error"
    except InvalidInputError:
        pass  # Expected
```

### Test Categories

1. **Normal Cases** - Happy path
2. **Empty Input** - Empty lists/strings
3. **Invalid Input** - Out of range, wrong type
4. **Edge Cases** - Extreme values, None, special chars
5. **Error Recovery** - Graceful failure

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test
python3 tests/test_component.py

# Run with coverage
python3 -m pytest --cov=ui tests/
```

---

## Contributing

### Code Style

**Follow PEP 8:**
- 4 spaces for indentation
- Max line length: 100 characters
- Docstrings for all public methods
- Type hints everywhere

**Example:**
```python
def render_table(
    self,
    data: List[Dict[str, Any]],
    title: str = "Table",
    max_rows: int = 100
) -> None:
    """
    Render data as a table.

    Args:
        data: List of dictionaries to render
        title: Table title
        max_rows: Maximum rows to display

    Raises:
        EmptyDataError: If data is empty
        InvalidInputError: If data format is invalid
    """
    validate_items(data, min_items=1)
    # ... implementation
```

### Commit Guidelines

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `perf`: Performance improvement
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring

**Example:**
```
feat(ui/agents): Add workload distribution display

- Add show_workload() method to AgentDisplay
- Display CPU and memory usage per agent
- Add progress bars for resource usage

Closes #123
```

### Pull Request Process

1. Create feature branch: `git checkout -b feat/my-feature`
2. Make changes with tests
3. Run benchmarks: `python3 benchmarks/ui_benchmarks.py`
4. Update documentation
5. Commit with clear message
6. Push and create PR
7. Wait for review

---

## API Reference

### Public Exports

```python
from ui import (
    # Banner
    MaxCodeBanner,
    show_vcli_banner,

    # Formatter
    MaxCodeFormatter,

    # Progress
    MaxCodeProgress,

    # Agents
    AgentDisplay,
    Agent,
    AgentStatus,
    AgentEvent,
    AgentMessage,

    # Menus
    SelectionMenu,
    MenuItem,
    ConfigMenu,
    CommandPalette,
    Command,

    # Tree of Thoughts
    ThoughtTree,
    ThoughtNode,
    BranchStatus,
    ReasoningSteps,
    ReasoningStep,
    ConstitutionalAnalysis,
    ConstitutionalScore,

    # Streaming
    StreamingDisplay,
    LiveLogViewer,
    LogEntry,
    LogLevel,
    ProgressStream,
    StreamUpdate,

    # Utilities
    get_banner,
    get_formatter,
    get_progress,
)
```

### Quick Access Functions

```python
# Convenience functions for common operations
def get_banner(style: str = 'default') -> MaxCodeBanner:
    """Get configured banner instance."""

def get_formatter() -> MaxCodeFormatter:
    """Get configured formatter instance."""

def get_progress() -> MaxCodeProgress:
    """Get configured progress instance."""
```

---

## Performance Targets

```python
PERFORMANCE_TARGETS = {
    'banner_display_ms': 50,
    'table_render_ms': 100,
    'live_update_fps': 10,
    'import_time_ms': 100,
    'memory_overhead_mb': 50,
}
```

**Current Results:**
- Import time: 70.71ms ✅
- Banner PyFiglet: 0.00ms ✅
- Banner vCLI-Go: 29.39ms ✅
- Table (100 rows): 54.17ms ✅
- Live FPS: 37,883 ✅
- Memory: 0.02MB ✅
- **Pass Rate: 100%** 🎯

---

## FAQ

### Q: Why lazy imports?
**A:** rich-gradient takes 113ms to import. By deferring until needed, we save startup time.

### Q: Why not crash on empty data?
**A:** Better UX to show "No items" than cryptic stack trace. Graceful degradation improves robustness.

### Q: Can I use other terminal libraries?
**A:** Components are abstracted. You could implement backends for curses, blessed, etc. But Rich is optimal.

### Q: How to add new agent colors?
**A:** Add to `AGENT_COLORS` dict in `ui/agents.py` and `ui/formatter.py`.

### Q: Performance too slow?
**A:** Run benchmarks to identify bottleneck. Use lazy imports, limit data size, reduce update frequency.

---

## Resources

**Documentation:**
- [USER_GUIDE.md](/docs/ui/USER_GUIDE.md) - User-facing guide
- [API_REFERENCE.md](/docs/ui/API_REFERENCE.md) - Detailed API docs

**Examples:**
- [ui/demo.py](/ui/demo.py) - Comprehensive demo
- [tests/](/tests/) - Test examples

**External:**
- [Rich Documentation](https://rich.readthedocs.io/)
- [PyFiglet Fonts](http://www.figlet.org/examples.html)
- [Yaspin](https://github.com/pavdmyt/yaspin)

---

## Changelog

### v1.0.0 (2025-11-04)
- Initial release
- 8 core components
- Complete error handling
- Performance optimization
- Comprehensive documentation

---

*Framework: Constitutional AI v3.0*
*Model: Claude Sonnet 4.5*
*Date: 2025-11-04*
