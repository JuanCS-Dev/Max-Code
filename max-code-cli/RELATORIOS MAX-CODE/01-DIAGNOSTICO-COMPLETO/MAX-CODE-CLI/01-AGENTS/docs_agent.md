# DOCS_AGENT - Agent Documentation

**File:** `agents/docs_agent.py`
**Lines:** 238
**Generated:** 2025-11-07 21:30:39

---

## 1. Overview

```python

Docs Agent - ENHANCED with MAXIMUS + DETER-AGENT Guardian
Port: 8166
Capability: DOCUMENTATION

v2.0: Standard Docs + NIS Narrative Intelligence
v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Elite documentation generation (FASE 3.5)
      - API documentation (endpoints, parameters, responses)
      - User guides (tutorials, examples)
      - Architecture diagrams (mermaid markdown)
      - Code examples with explanations
      - Troubleshooting sections
      - NIS narrative intelligence integration
v3.1: DETER-AGENT Guardian - OBRIGA Claude a obedecer Constitution


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import NISClient
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import DocsAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
```

## 2. Classes

### `DocsAgent`
```python
class DocsAgent(BaseAgent):
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
from core.maximus_integration import NISClient
from core.auth import get_anthropic_client
from core.deter_agent import Guardian, GuardianMode
from agents.validation_schemas import DocsAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings
```
