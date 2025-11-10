# REVIEW_AGENT - Agent Documentation

**File:** `agents/review_agent.py`
**Lines:** 339
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Review Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8164
Capability: CODE_REVIEW

v2.0: Constitutional (P1-P6) + MAXIMUS Ethical Review (4 frameworks)
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Deep Claude-powered code review (FASE 3.5)
      - Security analysis (OWASP Top 10)
      - Performance optimization suggestions
      - Best practices validation
      - Architecture review
      - Maintainability score
v3.1: DETER-AGENT Guardian - OBRIGA Claude a obedecer Constitution


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient, DecisionFusion, MaximusCache
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import ReviewAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

```

## 2. Classes

### `ReviewAgent`
```python
class ReviewAgent(BaseAgent):
```

## 3. Public Methods

- `get_capabilities()`
- `execute()`

## 4. Dependencies
```python
import sys, os
from typing import List, Dict, Any
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient, DecisionFusion, MaximusCache
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import ReviewAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
```
