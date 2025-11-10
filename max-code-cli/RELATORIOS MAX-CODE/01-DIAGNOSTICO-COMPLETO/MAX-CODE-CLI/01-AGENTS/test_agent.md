# TEST_AGENT - Agent Documentation

**File:** `agents/test_agent.py`
**Lines:** 295
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Test Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8163
Capability: TESTING

v2.0: TDD (RED→GREEN→REFACTOR) + MAXIMUS Edge Case Prediction
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Real Claude-powered test generation (FASE 3.5)
v3.1: DETER-AGENT Guardian integration - OBRIGA Claude a obedecer Constitution


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
import asyncio
from pydantic import ValidationError
from anthropic import Anthropic
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import TestAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class TestAgent(BaseAgent):
    
```

## 2. Classes

### `TestAgent`
```python
class TestAgent(BaseAgent):
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
from anthropic import Anthropic
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import TestAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
import pytest
```
