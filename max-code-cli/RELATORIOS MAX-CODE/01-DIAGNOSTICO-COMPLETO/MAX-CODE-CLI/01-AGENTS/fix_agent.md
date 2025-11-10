# FIX_AGENT - Agent Documentation

**File:** `agents/fix_agent.py`
**Lines:** 200
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Fix Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8165
Capability: DEBUGGING

v2.0: Quick Fix + PENELOPE Root Cause Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Real Claude-powered debugging (FASE 3.5)
v3.1: DETER-AGENT Guardian - OBRIGA Claude a obedecer Constitution


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import PENELOPEClient
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import FixAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class FixAgent(BaseAgent):
    Bug fixing with root cause analysis + Constitutional enforcement"""
```

## 2. Classes

### `FixAgent`
```python
class FixAgent(BaseAgent):
```

## 3. Public Methods

- `get_capabilities()`
- `execute()`

## 4. Dependencies
```python
import sys, os
from typing import List
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import PENELOPEClient
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import FixAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
```
