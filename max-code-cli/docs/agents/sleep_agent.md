# SLEEP_AGENT - Agent Documentation

**File:** `agents/sleep_agent.py`
**Lines:** 421
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Sleep Agent - End-of-Day Workflow
Port: 8170
Capability: SESSION_MANAGEMENT

Specialized agent for /dormir command that handles complete end-of-day workflow:
- Save project snapshot (state preservation)
- Create status file (current work state)
- Git commit (save changes)
- Git push (backup to remote)
- Cleanup activities
- Enable exact resumption the next day

v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
import json
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from agents.validation_schemas import SleepAgentParameters, validate_task_parameters
from config.logging_config import get_logger

```

## 2. Classes

### `SleepAgent`
```python
class SleepAgent(BaseAgent):
```

## 3. Public Methods

- `get_capabilities()`
- `execute()`

## 4. Dependencies
```python
import sys, os
from typing import List, Dict, Any
import asyncio
import json
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from agents.validation_schemas import SleepAgentParameters, validate_task_parameters
from config.logging_config import get_logger
```
