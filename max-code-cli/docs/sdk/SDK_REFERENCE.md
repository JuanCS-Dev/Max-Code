# MAX-CODE-CLI - SDK Reference

**Generated:** 2025-11-07 21:31:00

---

## Agent Development SDK

This SDK provides the foundation for creating custom agents.

## SDK Components

### agent_orchestrator.py

**Lines:** 72

**Classes:**
- `AgentOrchestrator:`

### agent_pool.py

**Lines:** 40

**Classes:**
- `AgentPool:`

### agent_registry.py

**Lines:** 40

**Classes:**
- `AgentRegistry:`

### base_agent.py

**Lines:** 275

**Classes:**
- `AgentCapability`
- `AgentTask:`
- `AgentResult:`
- `BaseAgent`


## Creating a New Agent

### Basic Template

```python
from sdk.base_agent import BaseAgent
from sdk.agent_task import AgentTask
from sdk.agent_result import AgentResult

class MyCustomAgent(BaseAgent):
    """
    Your custom agent description.
    """
    
    def __init__(self):
        super().__init__(
            name="my_custom_agent",
            description="What your agent does",
            version="1.0.0"
        )
    
    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute the agent's main logic."""
        try:
            # Your implementation
            result = await self._process(task)
            
            return AgentResult(
                success=True,
                output=result,
                agent_name=self.name
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent_name=self.name
            )
    
    async def _process(self, task: AgentTask):
        """Your custom processing logic."""
        pass
```

