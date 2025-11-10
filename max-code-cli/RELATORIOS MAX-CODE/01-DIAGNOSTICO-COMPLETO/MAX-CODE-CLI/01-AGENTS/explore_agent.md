# EXPLORE_AGENT - Agent Documentation

**File:** `agents/explore_agent.py`
**Lines:** 272
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Explore Agent - Port 8161 + DETER-AGENT Guardian
Capability: EXPLORATION

v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Elite codebase exploration (FASE 3.5)
      - Intelligent file discovery
      - Architecture analysis
      - Dependency mapping
      - Pattern recognition
      - Technology stack detection
      - Code metrics and insights
v3.1: DETER-AGENT Guardian - OBRIGA Claude a obedecer Constitution


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
from pathlib import Path
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import ExploreAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)
```

## 2. Classes

### `ExploreAgent`
```python
class ExploreAgent(BaseAgent):
```

## 3. Public Methods

- `get_capabilities()`
- `execute()`

## 4. Dependencies
```python
import sys, os
from typing import List, Dict, Any
import asyncio
from pathlib import Path
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import ExploreAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
```
