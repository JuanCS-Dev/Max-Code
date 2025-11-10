# 🔍 Plan Preview System - Analysis Results

**Date:** 2025-11-08  
**Status:** Analysis Complete - Ready for Implementation

---

## 📊 EXISTING STRUCTURE

### ✅ Task Planning (Found)

**Location:** `core/task_planner.py`

**Components:**
1. **ExecutionPlan** dataclass (lines 70-136)
   - task_id, task_description
   - architectural_vision (from SOFIA)
   - dream_analysis (from DREAM)
   - steps: List[ToolStep]
   - constitutional_approved
   - status, current_step

2. **ToolStep** dataclass (lines 56-66)
   - step_number
   - tool_name
   - description
   - parameters
   - expected_output
   - constitutional_risk (LOW/MEDIUM/HIGH)
   - executed, result, error

3. **TaskPlanner** class (lines 142+)
   - plan_task() - Creates execution plan
   - Uses SOFIA (ArchitectAgent)
   - Uses DREAM (Skeptic)
   - Uses Constitutional Engine

### ✅ Plan Agent (Found)

**Location:** `agents/plan_agent.py`

**Features:**
- MAXIMUS-Enhanced planning
- Tree of Thoughts exploration
- Systemic impact analysis
- Decision fusion
- Fallback system

### ✅ Agent SDK (Found)

**Location:** `sdk/`

**Files:**
- base_agent.py - BaseAgent class
- agent_orchestrator.py - Orchestration
- agent_pool.py - Agent management
- agent_registry.py - Registration

---

## 🎯 IMPLEMENTATION STRATEGY

### What Already Exists ✅

1. **ExecutionPlan data structure** - Complete
2. **ToolStep model** - Complete
3. **TaskPlanner.plan_task()** - Creates plans
4. **Constitutional risk assessment** - Integrated
5. **SOFIA + DREAM validation** - Working

### What Needs to Be Created 🆕

1. **Plan Visualizer** (`core/plan_visualizer.py`)
   - Display ExecutionPlan with Rich UI
   - Steps table
   - Dependencies tree (if any)
   - Risk summary
   - Time estimates

2. **Confirmation Prompt** (`ui/plan_confirmation.py`)
   - Show plan preview
   - Ask user confirmation
   - Allow plan modifications
   - Integration with existing ConfirmationUI

3. **Agent Integration** (Modify existing agents)
   - Add `execute_with_preview()` method
   - Generate plan first
   - Show preview
   - Execute if confirmed

4. **CLI Integration** (Modify CLI commands)
   - Add `--preview` flag
   - Show plan before execution
   - Skip preview with `--no-preview`

---

## 🔑 KEY INSIGHTS

### 1. ExecutionPlan is Perfect ✅

The existing ExecutionPlan has everything we need:
- Steps with descriptions
- Tool names
- Risk levels (constitutional_risk)
- Dependencies (can be inferred from step_number)
- Time estimates (can add if missing)

### 2. Rich UI Already Used ✅

Confirmation system already uses Rich:
- Panels, Tables, Syntax highlighting
- Can reuse patterns
- Consistent visual style

### 3. TaskPlanner Integration Point ✅

TaskPlanner.plan_task() is perfect entry point:
- Already creates ExecutionPlan
- Already does SOFIA + DREAM + Constitutional
- Just need to add visualization before execution

### 4. Constitutional Risk Already Available ✅

ToolStep has constitutional_risk field:
- LOW, MEDIUM, HIGH
- Can use for color coding
- No need to recalculate

---

## 🎨 VISUAL DESIGN

### Plan Preview Output (Proposed)

```
┌─ 🎯 Execution Plan ─────────────────────────────────┐
│ Task: Create a C++ calculator with GUI              │
│                                                      │
│ SOFIA Analysis:                                     │
│ "Multi-file C++ project with Qt GUI. Need parser,  │
│  calculator logic, and UI components."              │
│                                                      │
│ DREAM Reality Check: 85% realistic                  │
│ "Qt may not be installed. Suggest CLI alternative" │
└──────────────────────────────────────────────────────┘

┌─ 📋 Execution Steps ────────────────────────────────┐
│ #  Description           Tool           Time  Risk  │
│ ─  ──────────────────── ─────────────── ───── ───── │
│ 1  Create main.cpp      file_writer     5s    🟢    │
│ 2  Create calculator.h  file_writer     3s    🟢    │
│ 3  Implement logic      code_agent      30s   🟡    │
│ 4  Create UI code       code_agent      45s   🟡    │
│ 5  Build project        bash_tool       10s   🔴    │
│ 6  Run tests            test_agent      15s   🟢    │
└──────────────────────────────────────────────────────┘

┌─ 📊 Summary ─────────────────────────────────────────┐
│ Total steps:     6                                   │
│ Estimated time:  1m 48s                              │
│ Parallel steps:  0 (sequential execution)           │
│                                                      │
│ Risk levels:                                        │
│   🟢 Low:      4                                     │
│   🟡 Medium:   1                                     │
│   🔴 High:     1                                     │
│                                                      │
│ Constitutional: ✅ APPROVED (score: 0.92)            │
└──────────────────────────────────────────────────────┘

Execute this plan? (y/n):
```

---

## 🔧 IMPLEMENTATION PLAN

### Step 1: Create Plan Visualizer ✅

**File:** `core/plan_visualizer.py`

**Classes:**
- `PlanVisualizer` - Display ExecutionPlan with Rich
  - show_plan(plan: ExecutionPlan)
  - _display_steps_table()
  - _display_summary()
  - _display_sofia_analysis()
  - _display_dream_check()

**Integration:**
- Use existing ExecutionPlan model
- No modifications needed to core/task_planner.py

### Step 2: Create Confirmation UI ✅

**File:** `ui/plan_confirmation.py`

**Classes:**
- `PlanConfirmationUI` - Extends ConfirmationUI
  - confirm_plan(plan: ExecutionPlan) -> bool
  - allow_modifications() -> Optional[dict]

**Integration:**
- Extends ui/confirmation.py (already implemented)
- Reuses Rich patterns

### Step 3: Integrate with Agents ✅

**Modify:** `sdk/base_agent.py` or agent-specific files

**Add method:**
```python
async def execute_with_preview(self, task: AgentTask) -> AgentResult:
    # 1. Plan
    plan = await self.task_planner.plan_task(task.description)
    
    # 2. Show preview
    visualizer = PlanVisualizer()
    visualizer.show_plan(plan)
    
    # 3. Confirm
    confirmed = visualizer.confirm_plan()
    
    # 4. Execute if confirmed
    if confirmed:
        return await self._execute_plan(plan)
```

### Step 4: Add CLI Flags ✅

**Modify:** CLI commands

**Add flags:**
- `--preview` / `--no-preview` (default: preview)
- `--auto-approve` / `-y` (skip confirmation)

---

## 📋 FILES TO CREATE

1. **core/plan_visualizer.py** (NEW) - ~300 lines
2. **ui/plan_confirmation.py** (NEW) - ~150 lines
3. **tests/test_plan_preview.py** (NEW) - ~200 lines

## 📋 FILES TO MODIFY

1. **sdk/base_agent.py** (MODIFY) - Add ~60 lines
2. **cli/commands/*.py** (MODIFY) - Add ~20 lines each

---

## ✅ SUCCESS CRITERIA

- [x] ExecutionPlan structure identified
- [x] TaskPlanner integration point found
- [x] SOFIA + DREAM + Constitutional available
- [x] Risk assessment already done
- [x] Rich UI patterns established
- [x] No breaking changes required
- [ ] Implementation (next phase)
- [ ] Tests (next phase)
- [ ] Validation (next phase)

---

**Status:** ✅ Analysis Complete  
**Next:** Proceed to implementation (FASE 2)

**Soli Deo Gloria** 🙏
