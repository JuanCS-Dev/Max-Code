# 🛠️ 06-SDK - Agent Development Kit

**Complete SDK for creating custom agents**

---

## Main Document

**[SDK_REFERENCE.md](SDK_REFERENCE.md)** - SDK reference

### SDK Components:
- **BaseAgent** - Base agent class
- **AgentTask** - Task model
- **AgentResult** - Result model
- **Agent Template** - Complete example

### Creating a New Agent:
```python
from sdk.base_agent import BaseAgent
from sdk.agent_task import AgentTask
from sdk.agent_result import AgentResult

class MyAgent(BaseAgent):
    async def execute(self, task: AgentTask) -> AgentResult:
        # Your implementation
        pass
```

---

**[← Back to Main](../README.md)** | **[Next: Guides →](../07-GUIDES/)**
