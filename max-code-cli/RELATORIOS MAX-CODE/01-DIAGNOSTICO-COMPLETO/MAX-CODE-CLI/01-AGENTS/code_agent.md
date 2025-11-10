# CODE_AGENT - Agent Documentation

**File:** `agents/code_agent.py`
**Lines:** 322
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Code Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8162
Capability: CODE_GENERATION

v2.0: Code Generation + MAXIMUS Security Analysis
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Real Claude-powered code generation (FASE 3.5)
v3.1: DETER-AGENT Guardian integration (FASE 4.0)
      - Constitutional validation (P1-P6)
      - Deliberation quality check
      - Execution risk analysis


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Optional
import asyncio
from pydantic import ValidationError
from anthropic import Anthropic
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import CodeAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)
```

## 2. Classes

### `CodeAgent`
```python
class CodeAgent(BaseAgent):
```

## 3. Public Methods

- `get_capabilities()`
- `execute()`

## 4. Dependencies
```python
import sys, os
from typing import List, Optional
import asyncio
from pydantic import ValidationError
from anthropic import Anthropic
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import CodeAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
```
