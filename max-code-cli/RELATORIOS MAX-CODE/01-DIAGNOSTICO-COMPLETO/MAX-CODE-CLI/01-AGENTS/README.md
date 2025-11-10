# 🤖 01-AGENTS - Complete Agent Documentation

**9 specialized AI agents documented**

---

## Available Agents

### 1. [architect_agent](architect_agent.md)
**Architecture decisions and system design**
- Makes high-level architectural decisions
- Designs system components
- Ensures best practices

### 2. [code_agent](code_agent.md)
**Code generation**
- Generates production-ready code
- Follows project standards
- Implements features

### 3. [docs_agent](docs_agent.md)
**Documentation generation**
- Creates comprehensive documentation
- Generates API references
- Writes user guides

### 4. [explore_agent](explore_agent.md)
**Codebase exploration**
- Analyzes existing code
- Maps dependencies
- Understands architecture

### 5. [fix_agent](fix_agent.md)
**Bug fixing**
- Identifies bugs
- Implements fixes
- Validates solutions

### 6. [plan_agent](plan_agent.md)
**Implementation planning**
- Creates detailed plans
- Breaks down tasks
- Defines dependencies

### 7. [review_agent](review_agent.md)
**Code review**
- Reviews code quality
- Identifies improvements
- Ensures standards compliance

### 8. [sleep_agent](sleep_agent.md)
**Task scheduling**
- Schedules tasks
- Manages workflows
- Handles timing

### 9. [test_agent](test_agent.md)
**Test generation**
- Generates comprehensive tests
- Creates test suites
- Ensures coverage

---

## Agent Architecture

All agents extend `BaseAgent` and implement:
- `execute(task: AgentTask) -> AgentResult`
- Constitutional validation (P1-P6)
- MAXIMUS integration

---

## Usage Example

```python
from agents.code_agent import CodeAgent

agent = CodeAgent()
task = AgentTask(
    id='task-001',
    description='Create a fibonacci function',
    agent_name='code_agent'
)

result = await agent.execute(task)
```

---

**[← Back to Main](../README.md)** | **[Next: CLI →](../02-CLI/)**
