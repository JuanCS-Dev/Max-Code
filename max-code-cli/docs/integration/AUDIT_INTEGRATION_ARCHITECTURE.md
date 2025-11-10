# Audit Integration Architecture - Design Document

**Author:** Senior Dev/Project Leader (Boris-style)
**Date:** 2025-11-10
**Status:** 🔬 ARCHITECTURAL ANALYSIS
**Version:** 1.0

---

## Executive Summary

Integration of Truth Engine + Vital System + Independent Auditor into the existing ExecutionEngine requires a **flawless, zero-breaking-change** approach. This document provides complete architectural analysis before any code is written.

**Philosophy:**
> "Measure twice, cut once. Analyze thrice, code once."
> — Senior Dev Wisdom

---

## 1. CURRENT ARCHITECTURE ANALYSIS

### 1.1 ExecutionEngine (core/execution_engine.py)

**Purpose:** Robust multi-step execution with retry/recovery

**Key Components:**
```python
class ExecutionEngine:
    - execute_plan(plan, display) -> Dict
    - _execute_sequential(plan, graph, display) -> List[Dict]
    - _execute_parallel(plan, graph, display) -> List[Dict]
    - _execute_task_with_retry(task, display) -> Dict
    - _execute_task(task) -> Dict
```

**Current Flow:**
```
1. Validate plan (DAG check)
2. Execute (sequential OR parallel)
   2.1. For each task:
        - Mark running
        - Call on_task_start callback
        - Execute with retry
        - Mark completed/failed
        - Call on_task_complete/on_task_fail
3. Build final result
4. Call on_plan_complete
```

**Integration Points (CALLBACKS):**
- ✅ `on_task_start`: Called before task execution
- ✅ `on_task_complete`: Called after successful task
- ✅ `on_task_fail`: Called after task failure
- ✅ `on_plan_complete`: Called after plan completion

**Critical Observation:**
The callback system is PERFECT for audit integration. We can hook the auditor WITHOUT modifying core execution logic.

---

### 1.2 Independent Auditor (core/audit/independent_auditor.py)

**Purpose:** Meta-level verification of agent executions

**Key Method:**
```python
async def audit_execution(
    task: Task,
    result: AgentResult
) -> AuditReport
```

**Input Types (Auditor):**
- `Task`: Has `prompt`, `context`, `metadata`
- `AgentResult`: Has `success`, `output`, `files_changed`, `tests_run`, `error`

**Current Flow:**
```
1. Collect context (ContextOrchestrator)
2. Verify truth (TruthEngine)
3. Apply vital metabolism (VitalSystemMonitor)
4. Generate dashboard
5. Generate honest report
6. Compress to EPL
7. Check critical state
```

**Critical Observation:**
Auditor operates at META-LEVEL. It should audit the ENTIRE plan execution, not individual tasks. This is a KEY architectural decision.

---

### 1.3 Task Models (core/task_models.py)

**ExecutionEngine Uses:**
- `Task`: Enhanced task with dependencies
- `EnhancedExecutionPlan`: Plan with multiple tasks
- `TaskOutput`: Output from task execution
- `TaskStatus`: PENDING, READY, RUNNING, COMPLETED, FAILED, etc.

**Auditor Uses (DIFFERENT!):**
- `Task`: Simple task with just `prompt`, `context`, `metadata`
- `AgentResult`: Result with `success`, `output`, `files_changed`

**PROBLEM IDENTIFIED:**
Type mismatch! Auditor's `Task` and ExecutionEngine's `Task` are DIFFERENT classes with same name.

**Solution Required:**
We need an ADAPTER to convert between ExecutionEngine types and Auditor types.

---

## 2. INTEGRATION CHALLENGES

### Challenge 1: Type Incompatibility ⚠️

**Issue:**
```python
# ExecutionEngine expects:
from core.task_models import Task  # Rich task with dependencies

# Auditor expects:
@dataclass
class Task:  # Simple task with prompt
    prompt: str
    context: Dict
```

**Impact:** HIGH
**Resolution:** Create adapter layer

---

### Challenge 2: Granularity Mismatch 🎯

**Issue:**
- ExecutionEngine works at TASK level (individual steps)
- Auditor works at PLAN level (entire execution)

**Question:** Should we audit:
- A) Each task individually? (Fine-grained)
- B) The entire plan? (Coarse-grained)
- C) Both?

**Analysis:**

**Option A: Per-Task Auditing**
- ✅ Detailed verification
- ✅ Early failure detection
- ❌ Too granular (overhead)
- ❌ Doesn't capture plan-level truth

**Option B: Plan-Level Auditing**
- ✅ Holistic view
- ✅ Captures actual deliverables
- ✅ Matches user's mental model
- ❌ Late failure detection

**Option C: Hybrid**
- ✅ Best of both
- ❌ Complex implementation
- ❌ Potential for confusion

**RECOMMENDATION:** Option B (Plan-Level)

**Rationale:**
1. User cares about: "Did my request get fulfilled?"
2. Truth verification needs actual files (not intermediate steps)
3. Vital metabolism should reflect FINAL outcome
4. Matches Independent Auditor's design philosophy (meta-level)

---

### Challenge 3: Async Flow 🔄

**Issue:**
```python
# ExecutionEngine:
async def execute_plan(plan) -> Dict

# Auditor:
async def audit_execution(task, result) -> AuditReport
```

Both are async - GOOD! No blocking issues.

---

### Challenge 4: Data Conversion 🔄

**Need to convert:**
```python
EnhancedExecutionPlan → (Task + AgentResult)
```

**Mapping:**
```
Task:
  prompt         ← plan.goal
  context        ← plan metadata
  metadata       ← plan.constitutional_approval, etc.

AgentResult:
  success        ← result["success"]
  output         ← summary of all task outputs
  files_changed  ← collect from all tasks
  tests_run      ← check if any task ran tests
  error          ← result["error"] if any
```

---

## 3. PROPOSED INTEGRATION ARCHITECTURE

### 3.1 High-Level Design

```
┌─────────────────────────────────────────────────────┐
│  CLI Layer (cli/task_command.py)                    │
│  - User provides natural language task              │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  TaskPlanner (core/task_planner.py)                 │
│  - SOFIA → DREAM → Constitutional                   │
│  - Creates EnhancedExecutionPlan                    │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  ExecutionEngine (core/execution_engine.py)         │
│  - Execute plan (sequential/parallel)               │
│  - Retry + recovery                                 │
│  - Callbacks: on_plan_complete                      │
└───────────────────┬─────────────────────────────────┘
                    │
                    │ (via callback)
                    ▼
┌─────────────────────────────────────────────────────┐
│  🆕 AuditIntegration (NEW!)                         │
│  - Adapter: ExecutionEngine types → Auditor types   │
│  - Triggered on plan completion                     │
│  - Handles critical vital failures gracefully       │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  IndependentAuditor (core/audit/)                   │
│  - Truth verification                               │
│  - Vital metabolism                                 │
│  - Honest reporting                                 │
│  - Critical state check                             │
└─────────────────────────────────────────────────────┘
```

---

### 3.2 New Component: AuditIntegration

**File:** `core/audit/integration.py`

**Purpose:** Bridge between ExecutionEngine and IndependentAuditor

**Responsibilities:**
1. Type adaptation (ExecutionEngine → Auditor)
2. Callback registration
3. Graceful error handling
4. Display formatting

**API:**
```python
class AuditIntegration:
    """
    Bridge between ExecutionEngine and IndependentAuditor

    Usage:
        auditor = IndependentAuditor()
        integration = AuditIntegration(auditor)
        engine = ExecutionEngine()
        integration.attach_to_engine(engine)
    """

    def __init__(self, auditor: IndependentAuditor):
        self.auditor = auditor
        self.last_report: Optional[AuditReport] = None

    def attach_to_engine(self, engine: ExecutionEngine):
        """Attach auditor to execution engine callbacks"""
        engine.on_plan_complete = self._on_plan_complete

    async def _on_plan_complete(self, result: Dict):
        """Callback: Audit plan after completion"""
        # 1. Convert types
        task, agent_result = self._convert_types(result)

        # 2. Audit
        try:
            report = await self.auditor.audit_execution(task, agent_result)
            self.last_report = report

            # 3. Display
            self._display_report(report)

        except CriticalVitalFailure as e:
            # Handle gracefully
            self._display_critical_failure(e)
            raise  # Re-raise to stop execution

    def _convert_types(self, result: Dict) -> Tuple[Task, AgentResult]:
        """Convert ExecutionEngine result to Auditor types"""
        # Implementation details below
        pass

    def _display_report(self, report: AuditReport):
        """Display audit report with Rich UI"""
        pass

    def _display_critical_failure(self, error: CriticalVitalFailure):
        """Display critical vital failure"""
        pass
```

---

### 3.3 Type Conversion Logic

```python
def _convert_types(self, result: Dict) -> Tuple[Task, AgentResult]:
    """
    Convert ExecutionEngine result to Auditor types

    Input (ExecutionEngine result):
    {
        "success": bool,
        "completed_tasks": int,
        "failed_tasks": int,
        "total_tasks": int,
        "execution_time": float,
        "tasks": [
            {
                "success": bool,
                "task_id": str,
                "data": Any,
                "error": str (optional)
            }
        ]
    }

    Output (Auditor types):
    - Task(prompt, context, metadata)
    - AgentResult(success, output, files_changed, tests_run, error)
    """

    # Extract plan info (need to access self.current_plan)
    plan = self.engine.current_plan

    # Build Task (simple)
    task = AuditorTask(
        prompt=plan.goal,
        context={
            "complexity": plan.complexity,
            "estimated_time": plan.estimated_time,
            "total_tasks": result["total_tasks"]
        },
        metadata={
            "constitutional_approved": plan.constitutional_approved,
            "constitutional_score": plan.constitutional_score,
            "sofia_analysis": plan.sofia_analysis,
            "dream_check": plan.dream_check
        }
    )

    # Build AgentResult (aggregate)
    files_changed = []
    tests_run = False
    output_parts = []

    for task_result in result["tasks"]:
        # Collect files (if available in task data)
        if "files" in task_result.get("data", {}):
            files_changed.extend(task_result["data"]["files"])

        # Check tests
        if "tests" in task_result.get("data", {}):
            tests_run = True

        # Collect outputs
        if task_result["success"]:
            output_parts.append(f"✅ Task {task_result['task_id']}")
        else:
            output_parts.append(f"❌ Task {task_result['task_id']}: {task_result.get('error', 'Unknown')}")

    output = "\n".join(output_parts)

    agent_result = AgentResult(
        success=result["success"],
        output=output,
        files_changed=files_changed,
        tests_run=tests_run,
        error=result.get("error"),
        metadata={
            "completed_tasks": result["completed_tasks"],
            "failed_tasks": result["failed_tasks"],
            "execution_time": result["execution_time"]
        }
    )

    return task, agent_result
```

---

## 4. ZERO-BREAKING-CHANGE GUARANTEE

### 4.1 Existing Code NOT Modified

**Files that remain UNTOUCHED:**
- ✅ `core/execution_engine.py` - Only use public callback API
- ✅ `core/task_models.py` - No changes to existing types
- ✅ `core/audit/independent_auditor.py` - Unchanged
- ✅ `core/truth_engine/` - Unchanged
- ✅ `core/vital_system/` - Unchanged

**ONLY additions:**
- 🆕 `core/audit/integration.py` - NEW file (adapter)
- 🆕 `tests/test_audit_integration.py` - NEW test file
- 🔧 `cli/task_command.py` - MINOR modification (opt-in flag)

---

### 4.2 Backward Compatibility

**Current usage (without audit):**
```python
engine = ExecutionEngine()
result = await engine.execute_plan(plan)
# Works as before!
```

**New usage (with audit):**
```python
auditor = IndependentAuditor()
integration = AuditIntegration(auditor)
engine = ExecutionEngine()
integration.attach_to_engine(engine)
result = await engine.execute_plan(plan)
# Result structure unchanged!
# Audit happens silently via callback
```

**CLI usage (opt-in):**
```bash
# Without audit (default)
max-code task "Create calculator"

# With audit (opt-in)
max-code task "Create calculator" --audit
max-code task "Create calculator" --audit --show-vitals
```

---

## 5. ERROR HANDLING STRATEGY

### 5.1 Critical Vital Failure

**Scenario:** Protection < 20% during audit

**Strategy:**
```python
try:
    report = await auditor.audit_execution(task, result)
except CriticalVitalFailure as e:
    # Display critical state
    console.print(Panel(
        f"[red bold]CRITICAL VITAL FAILURE[/red bold]\n\n"
        f"{e}\n\n"
        f"System has been degraded by repeated failures.\n"
        f"Please review and fix issues before continuing.",
        border_style="red",
        title="⚠️  SYSTEM CRITICAL"
    ))

    # Offer recovery options
    console.print("\n[yellow]Recovery options:[/yellow]")
    console.print("1. Review vital dashboard: max-code vitals")
    console.print("2. Check audit history: max-code audit history")
    console.print("3. Wait for vital recovery (automatic)")

    # Do NOT crash - allow graceful degradation
    return
```

---

### 5.2 Audit Failure (Non-Critical)

**Scenario:** Audit fails but vitals OK

**Strategy:**
```python
try:
    report = await auditor.audit_execution(task, result)
except Exception as e:
    # Log but don't block
    logger.error(f"Audit failed: {e}")

    # Show warning
    console.print("[yellow]⚠️  Audit verification failed[/yellow]")
    console.print(f"[dim]Error: {e}[/dim]")
    console.print("[dim]Execution result still available below.[/dim]\n")

    # Continue with execution result
    return result
```

---

## 6. DISPLAY INTEGRATION

### 6.1 Audit Report Display

**Goal:** Beautiful, informative display matching max-code style

**Layout:**
```
┌─ 🔍 Independent Audit Report ─────────────────────────┐
│                                                        │
│ 📊 Truth Verification                                 │
│ ├─ Completeness:    85% (6/7 requirements)           │
│ ├─ Mocked:          0                                 │
│ ├─ Missing:         1 (sqrt function)                │
│ ├─ Tests:           5/5 passing                      │
│ └─ Coverage:        92%                               │
│                                                        │
│ 💊 Vital System Status                               │
│ ┌─────────────────────────────────────────────────┐  │
│ │ Vital        Current  Change  Status            │  │
│ │ ─────────────────────────────────────────────── │  │
│ │ Protection   85%      +5%     🟢 Healthy        │  │
│ │ Growth       78%      +8%     🟢 Healthy        │  │
│ │ Nutrition    82%      +3%     🟢 Healthy        │  │
│ │ Healing      80%      +2%     🟢 Healthy        │  │
│ │ Work         88%      +10%    🟢 Healthy        │  │
│ │ Survival     90%      +5%     🟢 Healthy        │  │
│ │ Rhythm       85%      +7%     🟢 Healthy        │  │
│ └─────────────────────────────────────────────────┘  │
│                                                        │
│ 📝 Honest Assessment                                  │
│ Task partially completed. 6 of 7 functions            │
│ implemented correctly with full test coverage.        │
│ Missing: sqrt function (documented as TODO).          │
│                                                        │
│ 🎯 EPL Summary                                        │
│ 🎯6/7✅ | 🧪5/5✅ | 📊92% | 🛡️+5%                    │
│                                                        │
│ ⚡ Efficiency                                         │
│ Compression: 70x | Tokens saved: 2,340                │
└────────────────────────────────────────────────────────┘
```

---

### 6.2 Critical Failure Display

**Layout:**
```
┌─ ⚠️  CRITICAL VITAL FAILURE ──────────────────────────┐
│                                                        │
│ The system has reached a CRITICAL state due to        │
│ repeated integrity violations.                        │
│                                                        │
│ 🚨 Critical Vitals                                    │
│ ├─ Protection:  15% (CRITICAL < 20%)                 │
│ └─ Survival:    18% (CRITICAL < 20%)                 │
│                                                        │
│ 📉 Degradation History                                │
│ ├─ 3 consecutive dishonest reports                   │
│ ├─ 5 tasks claimed success with 0% delivery          │
│ └─ 0 tests run in last 10 executions                 │
│                                                        │
│ 🛠️  Recovery Actions                                  │
│ 1. Review audit history: max-code audit history       │
│ 2. Check vital trends: max-code vitals --detailed    │
│ 3. Allow automatic recovery (wait 30-60 minutes)     │
│ 4. Honest execution will restore vitals              │
│                                                        │
│ ⏸️  Execution paused for system protection            │
└────────────────────────────────────────────────────────┘
```

---

## 7. TESTING STRATEGY

### 7.1 Unit Tests

**File:** `tests/test_audit_integration.py`

**Coverage:**
```python
class TestAuditIntegration:
    def test_initialization()
    def test_attach_to_engine()
    def test_type_conversion_success()
    def test_type_conversion_failure()
    def test_type_conversion_partial()

class TestAuditCallback:
    async def test_audit_on_plan_complete_success()
    async def test_audit_on_plan_complete_failure()
    async def test_audit_critical_vital_failure()
    async def test_audit_non_critical_error()

class TestDisplayIntegration:
    def test_display_report_healthy()
    def test_display_report_degraded()
    def test_display_critical_failure()

class TestEndToEnd:
    async def test_full_integration_honest_success()
    async def test_full_integration_dishonest_success()
    async def test_full_integration_honest_failure()
```

**Target:** 100% coverage (25+ tests)

---

### 7.2 Integration Tests

**Scenarios:**
1. Execute simple plan → Audit → Display
2. Execute plan with failures → Audit → Display
3. Execute plan triggering critical → Catch → Display
4. Execute without audit (backward compat)

---

## 8. IMPLEMENTATION PLAN

### Phase 1: Core Adapter (2h)
- [ ] Create `core/audit/integration.py`
- [ ] Implement `AuditIntegration` class
- [ ] Implement type conversion
- [ ] Add basic error handling

### Phase 2: Display Integration (1h)
- [ ] Implement `_display_report()`
- [ ] Implement `_display_critical_failure()`
- [ ] Match max-code UI style
- [ ] Test display formatting

### Phase 3: CLI Integration (1h)
- [ ] Add `--audit` flag to task command
- [ ] Add `--show-vitals` flag
- [ ] Wire up integration
- [ ] Test CLI flow

### Phase 4: Testing (2h)
- [ ] Write 25+ unit tests
- [ ] Write integration tests
- [ ] Achieve 100% coverage
- [ ] Test all error paths

### Phase 5: Documentation (1h)
- [ ] Update CLI help text
- [ ] Add audit examples
- [ ] Document vital system
- [ ] Create user guide

**Total Estimated Time:** 7 hours

---

## 9. RISKS & MITIGATION

### Risk 1: Type Conversion Bugs
**Impact:** HIGH
**Probability:** MEDIUM
**Mitigation:**
- Comprehensive type conversion tests
- Fallback to safe defaults
- Clear error messages

### Risk 2: Performance Overhead
**Impact:** MEDIUM
**Probability:** LOW
**Mitigation:**
- Audit is opt-in (default off)
- Async execution (non-blocking)
- EPL compression minimizes token cost

### Risk 3: Critical State False Positives
**Impact:** HIGH
**Probability:** LOW
**Mitigation:**
- Well-tuned vital thresholds (already tested)
- Graceful degradation (warn, don't crash)
- Manual override option

---

## 10. SUCCESS CRITERIA

### Must Have ✅
- [ ] Zero modifications to existing core files
- [ ] 100% backward compatible
- [ ] 100% test coverage
- [ ] Graceful error handling
- [ ] Beautiful UI display

### Should Have 🎯
- [ ] CLI opt-in flag working
- [ ] Critical failure recovery guide
- [ ] User documentation complete

### Nice to Have 🌟
- [ ] Vital trends visualization
- [ ] Audit history command
- [ ] EPL compression metrics

---

## 11. NEXT STEPS

1. **Get approval** on this architecture
2. **Create branch**: `feature/audit-integration`
3. **Implement Phase 1**: Core adapter
4. **Test incrementally**: After each phase
5. **Review & iterate**: Before merging

---

## 12. SIGN-OFF

**Architecture Reviewed By:** Senior Dev/Project Leader
**Status:** ✅ READY FOR IMPLEMENTATION
**Approval Required:** Yes (awaiting user confirmation)

**Key Principles Applied:**
- Zero-breaking-change guarantee
- Callback-based integration (non-invasive)
- Type safety through adaptation
- Graceful error handling
- Beautiful UI/UX
- 100% test coverage
- Constitutional compliance

**Soli Deo Gloria** 🙏

---

**END OF ARCHITECTURAL ANALYSIS**
