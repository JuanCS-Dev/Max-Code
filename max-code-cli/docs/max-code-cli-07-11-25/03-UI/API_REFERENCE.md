# Max-Code CLI UI/UX - API Reference

**Version:** 1.0.0
**Date:** 2025-11-04
**Framework:** Constitutional AI v3.0

---

## Table of Contents

1. [Banner API](#banner-api)
2. [Formatter API](#formatter-api)
3. [Progress API](#progress-api)
4. [Agents API](#agents-api)
5. [Menus API](#menus-api)
6. [Tree of Thoughts API](#tree-of-thoughts-api)
7. [Streaming API](#streaming-api)
8. [Validation API](#validation-api)
9. [Exceptions API](#exceptions-api)
10. [Constants](#constants)

---

## Banner API

### `MaxCodeBanner`

Display ASCII art banner with gradient effects.

```python
from ui.banner import MaxCodeBanner

banner = MaxCodeBanner(console: Optional[Console] = None)
```

#### Methods

##### `show(version: str, context: Optional[Dict[str, Any]] = None, style: str = 'default') -> None`

Display the banner.

**Parameters:**
- `version` (str): Version string (e.g., "3.0")
- `context` (Dict[str, Any], optional): Additional context to display
  - `model` (str): AI model name
  - `build_date` (str): Build date
  - `framework` (str): Framework name
- `style` (str): PyFiglet font style
  - `'default'` - BLOCK font (Gemini-inspired)
  - `'isometric'` - Isometric blocks
  - `'banner'` - Bold banner
  - `'bold'` - Colossal letters
  - `'tech'` - Tech/doom style
  - `'cyber'` - Graffiti/cyber style

**Example:**
```python
banner = MaxCodeBanner()
banner.show(
    version="3.0",
    context={'model': 'Claude Sonnet 4.5'},
    style='default'
)
```

#### Attributes

- `GRADIENT_COLORS` (List[str]): Color gradient (neon pink → cyan)
- `console` (Console): Rich console instance

---

### `show_vcli_banner()`

Display vCLI-Go style professional banner.

```python
from ui.banner_vcli_style import show_vcli_banner

show_vcli_banner(
    version: str = "3.0.0",
    build_date: Optional[str] = None,
    model: str = "Claude Sonnet 4.5",
    framework: str = "Constitutional AI v3.0"
) -> None
```

**Parameters:**
- `version` (str): Version string
- `build_date` (str, optional): Build date (YYYY-MM-DD)
- `model` (str): AI model name
- `framework` (str): Framework name

**Example:**
```python
show_vcli_banner(version="3.0.0", build_date="2025-11-04")
```

---

## Formatter API

### `MaxCodeFormatter`

Semantic message formatting with consistent styling.

```python
from ui.formatter import MaxCodeFormatter

fmt = MaxCodeFormatter(console: Optional[Console] = None)
```

#### Methods

##### Success Messages

```python
fmt.print_success(message: str) -> None
```

Print success message with green checkmark.

##### Error Messages

```python
fmt.print_error(message: str, detail: Optional[str] = None) -> None
```

Print error message with red X symbol.

**Parameters:**
- `message` (str): Main error message
- `detail` (str, optional): Additional detail

##### Warning Messages

```python
fmt.print_warning(message: str) -> None
```

Print warning message with yellow warning symbol.

##### Info Messages

```python
fmt.print_info(message: str) -> None
```

Print info message with cyan info symbol.

##### Debug Messages

```python
fmt.print_debug(message: str) -> None
```

Print dimmed debug message.

##### Agent Messages

```python
fmt.print_agent_message(
    agent_name: str,
    message: str,
    action: str = "Processing"
) -> None
```

Print message from specific agent with color coding.

**Parameters:**
- `agent_name` (str): Agent name (Sophia, Code, Test, etc.)
- `message` (str): Message text
- `action` (str): Action verb (Analyzing, Coding, etc.)

##### Code Display

```python
fmt.print_code(
    code: str,
    language: str = "python",
    theme: str = "monokai"
) -> None
```

Display syntax-highlighted code block.

**Parameters:**
- `code` (str): Source code
- `language` (str): Language for syntax highlighting
- `theme` (str): Color theme

##### Table Display

```python
fmt.print_table(
    data: List[Dict[str, Any]],
    title: str = "",
    max_rows: int = 100
) -> None
```

Display data as formatted table.

**Parameters:**
- `data` (List[Dict]): List of dictionaries (keys become columns)
- `title` (str): Table title
- `max_rows` (int): Maximum rows to display

##### Constitutional Status

```python
fmt.print_constitutional_status(
    principles: Dict[str, bool]
) -> None
```

Display Constitutional AI principle status.

**Parameters:**
- `principles` (Dict[str, bool]): Principle status (e.g., {'p1': True, 'p2': False})

#### Attributes

- `AGENT_COLORS` (Dict[str, str]): Agent color mapping
- `SEMANTIC_COLORS` (Dict[str, str]): Semantic color mapping
- `console` (Console): Rich console instance

---

## Progress API

### `MaxCodeProgress`

Progress indicators for long-running operations.

```python
from ui.progress import MaxCodeProgress

progress = MaxCodeProgress(console: Optional[Console] = None)
```

#### Methods

##### Simple Spinner

```python
@contextmanager
progress.spinner(description: str) -> Generator[Progress, None, None]
```

Context manager for simple spinner.

**Example:**
```python
with progress.spinner("Loading..."):
    time.sleep(2)
```

##### Progress Bar

```python
@contextmanager
progress.bar(
    total: int,
    description: str = "Processing"
) -> Generator[Task, None, None]
```

Context manager for progress bar.

**Example:**
```python
with progress.bar(total=100, description="Processing") as bar:
    for i in range(100):
        bar.advance(1)
```

##### Multi-Progress

```python
@contextmanager
progress.multi_progress(
    tasks: List[Dict[str, Any]]
) -> Generator[Dict[str, Task], None, None]
```

Context manager for multiple parallel progress bars.

**Parameters:**
- `tasks` (List[Dict]): Task definitions
  - `name` (str): Task name
  - `total` (int): Total steps
  - `color` (str): Bar color

**Example:**
```python
tasks = [
    {'name': 'Download', 'total': 100, 'color': 'cyan'},
    {'name': 'Process', 'total': 80, 'color': 'green'},
]

with progress.multi_progress(tasks) as bars:
    bars['Download'].advance(10)
    bars['Process'].advance(5)
```

##### Agent Activity

```python
progress.show_agent_activity(
    agents: List[Dict[str, Any]],
    duration: float = 5.0
) -> None
```

Display live agent activity.

**Parameters:**
- `agents` (List[Dict]): Agent data
  - `name` (str): Agent name
  - `status` (str): Status (active/idle/completed)
  - `task` (str): Current task
  - `progress` (float): Progress (0-100)
- `duration` (float): Display duration in seconds

---

## Agents API

### Data Classes

#### `AgentStatus`

```python
from ui.agents import AgentStatus

class AgentStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"
```

#### `Agent`

```python
from ui.agents import Agent

@dataclass
class Agent:
    name: str
    role: str
    status: AgentStatus
    current_task: str = ""
    progress: float = 0.0  # 0-100
    time_elapsed: float = 0.0  # seconds
    cpu_usage: float = 0.0  # 0-100
    memory_usage: float = 0.0  # MB
```

#### `AgentEvent`

```python
from ui.agents import AgentEvent

@dataclass
class AgentEvent:
    timestamp: datetime
    agent_name: str
    action: str
    duration: Optional[float] = None  # seconds
```

#### `AgentMessage`

```python
from ui.agents import AgentMessage

@dataclass
class AgentMessage:
    sender: str
    receiver: str
    message_type: str
    status: str  # sent/received/acknowledged
    timestamp: datetime
```

### `AgentDisplay`

Agent activity visualization.

```python
from ui.agents import AgentDisplay

display = AgentDisplay(console: Optional[Console] = None)
```

#### Methods

##### Dashboard

```python
display.show_dashboard(
    agents: List[Agent],
    title: str = "AGENT DASHBOARD"
) -> None
```

Display real-time agent dashboard.

**Raises:**
- `EmptyDataError`: If agents list is empty

##### Live Dashboard

```python
display.show_dashboard_live(
    agents_generator: Generator[List[Agent], None, None],
    refresh_rate: float = 0.5
) -> None
```

Display live-updating dashboard.

**Parameters:**
- `agents_generator`: Generator yielding agent lists
- `refresh_rate` (float): Refresh interval in seconds

##### Timeline

```python
display.show_timeline(
    events: List[AgentEvent],
    title: str = "AGENT TIMELINE",
    max_events: int = 10
) -> None
```

Display agent activity timeline.

##### Communication Flow

```python
display.show_communication(
    messages: List[AgentMessage],
    title: str = "AGENT COMMUNICATION FLOW"
) -> None
```

Display inter-agent communication.

##### Workload Distribution

```python
display.show_workload(
    agents: List[Agent],
    title: str = "AGENT WORKLOAD"
) -> None
```

Display agent workload and resource usage.

---

## Menus API

### Data Classes

#### `MenuItem`

```python
from ui.menus import MenuItem

@dataclass
class MenuItem:
    label: str
    value: Any
    description: str = ""
    color: str = "white"
```

#### `Command`

```python
from ui.menus import Command

@dataclass
class Command:
    id: str
    label: str
    keybind: str = ""
    description: str = ""
    callback: Optional[Callable] = None
```

### `SelectionMenu`

Interactive selection menus.

```python
from ui.menus import SelectionMenu

menu = SelectionMenu(console: Optional[Console] = None)
```

#### Methods

##### Single Selection

```python
menu.select(
    items: List[MenuItem],
    title: str = "Select Option"
) -> Optional[MenuItem]
```

Show selection menu and return chosen item.

##### Multi-Selection

```python
menu.select_multiple(
    items: List[MenuItem],
    title: str = "Select Options",
    min_choices: int = 1,
    max_choices: Optional[int] = None
) -> List[MenuItem]
```

Show multi-selection menu.

**Parameters:**
- `items` (List[MenuItem]): Menu items
- `title` (str): Menu title
- `min_choices` (int): Minimum selections required
- `max_choices` (int, optional): Maximum selections allowed

### `ConfigMenu`

Configuration editor.

```python
from ui.menus import ConfigMenu

config_menu = ConfigMenu(console: Optional[Console] = None)
```

#### Methods

```python
config_menu.edit_config(
    config: Dict[str, Any],
    descriptions: Optional[Dict[str, str]] = None
) -> Dict[str, Any]
```

Interactive configuration editor.

**Parameters:**
- `config` (Dict): Current configuration
- `descriptions` (Dict[str, str], optional): Field descriptions

**Returns:**
- Modified configuration dictionary

### `CommandPalette`

Command palette for quick actions.

```python
from ui.menus import CommandPalette

palette = CommandPalette(console: Optional[Console] = None)
```

#### Methods

```python
palette.show(
    commands: List[Command]
) -> Optional[Command]
```

Show command palette and return selected command.

---

## Tree of Thoughts API

### Data Classes

#### `BranchStatus`

```python
from ui.tree_of_thoughts import BranchStatus

class BranchStatus(Enum):
    ACTIVE = "active"
    BEST = "best"
    PRUNED = "pruned"
    EXPLORING = "exploring"
```

#### `ThoughtNode`

```python
from ui.tree_of_thoughts import ThoughtNode

@dataclass
class ThoughtNode:
    id: str
    thought: str
    score: float
    status: BranchStatus
    parent_id: Optional[str] = None
    depth: int = 0
```

#### `ReasoningStep`

```python
from ui.tree_of_thoughts import ReasoningStep

@dataclass
class ReasoningStep:
    step: int
    thought: str
    reasoning: str
    score: float
    action: str  # continue/select/prune
    rationale: str
```

#### `ConstitutionalScore`

```python
from ui.tree_of_thoughts import ConstitutionalScore

@dataclass
class ConstitutionalScore:
    principle: str
    name: str
    score: float
    rationale: str
    color: str = "cyan"
```

### `ThoughtTree`

Visualize reasoning tree.

```python
from ui.tree_of_thoughts import ThoughtTree

tree = ThoughtTree(console: Optional[Console] = None)
```

#### Methods

```python
tree.show_tree(
    root: ThoughtNode,
    children: Dict[str, List[ThoughtNode]],
    title: str = "TREE OF THOUGHTS"
) -> None
```

Display hierarchical thought tree.

**Parameters:**
- `root` (ThoughtNode): Root node
- `children` (Dict): Mapping of parent ID to child nodes
- `title` (str): Tree title

### `ReasoningSteps`

Display reasoning process.

```python
from ui.tree_of_thoughts import ReasoningSteps

reasoning = ReasoningSteps(console: Optional[Console] = None)
```

#### Methods

```python
reasoning.show_steps(
    steps: List[ReasoningStep],
    title: str = "REASONING STEPS"
) -> None
```

Display step-by-step reasoning.

### `ConstitutionalAnalysis`

Constitutional AI analysis display.

```python
from ui.tree_of_thoughts import ConstitutionalAnalysis

analysis = ConstitutionalAnalysis(console: Optional[Console] = None)
```

#### Methods

##### Show Analysis

```python
analysis.show_analysis(
    scores: List[ConstitutionalScore],
    title: str = "CONSTITUTIONAL ANALYSIS"
) -> None
```

Display constitutional scores.

##### Radar Chart

```python
analysis.show_radar_chart(
    scores: List[ConstitutionalScore]
) -> None
```

Display scores as ASCII radar chart.

---

## Streaming API

### Data Classes

#### `LogLevel`

```python
from ui.streaming import LogLevel

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
```

#### `LogEntry`

```python
from ui.streaming import LogEntry

@dataclass
class LogEntry:
    timestamp: datetime
    level: LogLevel
    message: str
    source: str = ""
```

#### `StreamUpdate`

```python
from ui.streaming import StreamUpdate

@dataclass
class StreamUpdate:
    stream_id: str
    description: str
    current: int
    total: int
    status: str  # active/completed/failed
```

### `StreamingDisplay`

Real-time text streaming.

```python
from ui.streaming import StreamingDisplay

stream = StreamingDisplay(console: Optional[Console] = None)
```

#### Methods

```python
stream.stream_text(
    text_generator: Generator[str, None, None],
    prefix: str = "",
    style: str = "white"
) -> None
```

Stream text with typewriter effect.

**Parameters:**
- `text_generator`: Generator yielding text chunks
- `prefix` (str): Prefix before text
- `style` (str): Text style

### `LiveLogViewer`

Live log viewer.

```python
from ui.streaming import LiveLogViewer

log_viewer = LiveLogViewer(console: Optional[Console] = None)
```

#### Methods

##### Table View

```python
log_viewer.view_logs_table(
    log_generator: Generator[LogEntry, None, None],
    max_entries: int = 50
) -> None
```

View logs in table format.

##### Stream View

```python
log_viewer.view_logs_stream(
    log_generator: Generator[LogEntry, None, None]
) -> None
```

View logs as continuous stream.

### `ProgressStream`

Multi-stream progress.

```python
from ui.streaming import ProgressStream

progress_stream = ProgressStream(console: Optional[Console] = None)
```

#### Methods

```python
progress_stream.stream_progress(
    update_generator: Generator[StreamUpdate, None, None]
) -> None
```

Stream progress updates for multiple operations.

---

## Validation API

### Functions

#### `validate_items()`

```python
from ui.validation import validate_items

validate_items(
    items: List[Any],
    min_items: int = 1,
    max_items: Optional[int] = None,
    item_name: str = "items"
) -> None
```

Validate list constraints.

**Raises:**
- `EmptyDataError`: If items list is empty
- `InvalidInputError`: If constraints not met

#### `validate_score()`

```python
from ui.validation import validate_score

validate_score(
    score: float,
    min_score: float = 0.0,
    max_score: float = 10.0
) -> None
```

Validate score range.

**Raises:**
- `InvalidInputError`: If score out of range

#### `validate_percentage()`

```python
from ui.validation import validate_percentage

validate_percentage(percentage: float) -> None
```

Validate percentage (0-100).

**Raises:**
- `InvalidInputError`: If not valid percentage

#### `validate_string()`

```python
from ui.validation import validate_string

validate_string(
    text: str,
    min_length: int = 1,
    max_length: Optional[int] = None,
    field_name: str = "text"
) -> None
```

Validate string constraints.

**Raises:**
- `InvalidInputError`: If constraints not met

#### `validate_positive_int()`

```python
from ui.validation import validate_positive_int

validate_positive_int(
    value: int,
    field_name: str = "value",
    allow_zero: bool = False
) -> None
```

Validate positive integer.

**Raises:**
- `InvalidInputError`: If not positive integer

#### `validate_choice()`

```python
from ui.validation import validate_choice

validate_choice(
    value: Any,
    choices: List[Any],
    field_name: str = "value"
) -> None
```

Validate value is in allowed choices.

**Raises:**
- `InvalidInputError`: If value not in choices

#### `validate_type()`

```python
from ui.validation import validate_type

validate_type(
    value: Any,
    expected_type: type,
    field_name: str = "value"
) -> None
```

Validate value type.

**Raises:**
- `InvalidInputError`: If wrong type

---

## Exceptions API

### Exception Hierarchy

```python
from ui.exceptions import (
    UIError,
    InvalidInputError,
    InvalidConfigError,
    RenderError,
    EmptyDataError,
    TerminalError,
    ImportError,
)
```

#### `UIError`

Base exception for all UI errors.

```python
class UIError(Exception):
    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion
```

**Attributes:**
- `message` (str): Error message
- `suggestion` (str, optional): Helpful suggestion for fixing

#### `InvalidInputError`

Raised when user input is invalid.

#### `InvalidConfigError`

Raised when configuration is invalid.

#### `RenderError`

Raised when rendering fails.

#### `EmptyDataError`

Raised when required data is empty.

#### `TerminalError`

Raised when terminal operation fails.

#### `ImportError`

Raised when required dependency is missing.

---

## Constants

### Performance Targets

```python
from ui.constants import PERFORMANCE_TARGETS

PERFORMANCE_TARGETS = {
    'banner_display_ms': 50,
    'table_render_ms': 100,
    'live_update_fps': 10,
    'import_time_ms': 100,
    'memory_overhead_mb': 50,
}
```

### Agent Colors

```python
from ui.constants import AGENT_COLORS

AGENT_COLORS = {
    'sophia': 'gold1',
    'code': 'blue',
    'test': 'green',
    'review': 'orange3',
    'fix': 'red',
    'docs': 'purple',
    'explore': 'cyan',
    'guardian': 'bright_red',
    'sleep': 'deep_sky_blue1',
}
```

### Semantic Colors

```python
from ui.constants import SEMANTIC_COLORS

SEMANTIC_COLORS = {
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'cyan',
    'debug': 'dim',
}
```

### Status Symbols

```python
from ui.constants import STATUS_SYMBOLS

STATUS_SYMBOLS = {
    'active': '●',
    'idle': '○',
    'completed': '✓',
    'failed': '✗',
    'waiting': '⟳',
}
```

---

## Quick Start Examples

### Basic Usage

```python
# Import
from ui import get_banner, get_formatter, get_progress

# Banner
banner = get_banner()
banner.show(version="3.0")

# Messages
fmt = get_formatter()
fmt.print_success("Ready!")
fmt.print_info("Processing...")

# Progress
progress = get_progress()
with progress.spinner("Loading..."):
    time.sleep(2)
```

### Agent Dashboard

```python
from ui import AgentDisplay, Agent, AgentStatus

display = AgentDisplay()

agents = [
    Agent("Sophia", "Architect", AgentStatus.ACTIVE, "Analyzing", 75),
    Agent("Code", "Developer", AgentStatus.ACTIVE, "Coding", 50),
]

display.show_dashboard(agents)
```

### Interactive Menu

```python
from ui import SelectionMenu, MenuItem

menu = SelectionMenu()

items = [
    MenuItem("Option 1", "val1", "First choice", "cyan"),
    MenuItem("Option 2", "val2", "Second choice", "green"),
]

selected = menu.select(items, title="Choose:")
print(f"Selected: {selected.value}")
```

### Error Handling

```python
from ui.validation import validate_items
from ui.exceptions import EmptyDataError

try:
    validate_items(data, min_items=1)
    process_data(data)
except EmptyDataError as e:
    print(f"Error: {e.message}")
    if e.suggestion:
        print(f"Suggestion: {e.suggestion}")
```

---

## Version History

### v1.0.0 (2025-11-04)
- Initial release
- 8 core components
- Complete API coverage
- Error handling system
- Performance optimization
- Comprehensive documentation

---

*Framework: Constitutional AI v3.0*
*Model: Claude Sonnet 4.5*
*Date: 2025-11-04*
