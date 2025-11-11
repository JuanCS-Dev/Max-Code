"""
Multi-step Execution Engine with Retry and Recovery

Robust execution engine for multi-step plans with:
- Sequential and parallel execution
- Retry with exponential backoff
- Error recovery strategies
- State persistence
- Progress tracking
- Graceful cancellation

Biblical Foundation:
"Tudo tem o seu tempo determinado" (Eclesiastes 3:1)

Soli Deo Gloria
"""
import asyncio
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime
from enum import Enum
import time
import random
import logging

from core.task_models import (
    Task, EnhancedExecutionPlan, TaskStatus, TaskOutput, TaskType
)
from core.task_graph import TaskGraph
from core.tool_integration import get_tool_integration

logger = logging.getLogger(__name__)


class ExecutionState(Enum):
    """Execution engine state"""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RetryStrategy(Enum):
    """Retry strategies"""
    NONE = "none"
    IMMEDIATE = "immediate"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"


class ExecutionEngine:
    """
    Robust execution engine for multi-step plans
    
    Features:
    - Sequential and parallel execution
    - Retry with exponential backoff
    - Error recovery strategies
    - State persistence
    - Progress tracking
    - Graceful cancellation
    
    Examples:
        >>> engine = ExecutionEngine()
        >>> result = await engine.execute_plan(plan)
        >>> stats = engine.get_execution_stats()
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        enable_parallel: bool = True
    ):
        """
        Initialize execution engine
        
        Args:
            max_retries: Max retry attempts per task
            retry_strategy: Retry strategy to use
            base_delay: Base delay for retries (seconds)
            max_delay: Max delay between retries (seconds)
            enable_parallel: Enable parallel execution
        """
        self.max_retries = max_retries
        self.retry_strategy = retry_strategy
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.enable_parallel = enable_parallel
        
        self.state = ExecutionState.IDLE
        self.current_plan: Optional[EnhancedExecutionPlan] = None
        self.completed_tasks: set[str] = set()
        self.failed_tasks: set[str] = set()
        
        # Tool integration
        self.tool_integration = get_tool_integration()
        
        # Callbacks
        self.on_task_start: Optional[Callable] = None
        self.on_task_complete: Optional[Callable] = None
        self.on_task_fail: Optional[Callable] = None
        self.on_plan_complete: Optional[Callable] = None
        
        # State persistence
        self.checkpoint_enabled = False
        self.checkpoint_file: Optional[str] = None
        
        logger.info("ExecutionEngine initialized")
    
    async def execute_plan(
        self,
        plan: EnhancedExecutionPlan,
        display: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Execute complete plan
        
        Args:
            plan: EnhancedExecutionPlan to execute
            display: Optional UI display
        
        Returns:
            Execution result dict with:
            - success: bool
            - completed_tasks: int
            - failed_tasks: int
            - total_tasks: int
            - execution_time: float
            - tasks: List[Dict]
        
        Examples:
            >>> result = await engine.execute_plan(plan)
            >>> print(f"Completed: {result['completed_tasks']}/{result['total_tasks']}")
        """
        self.state = ExecutionState.EXECUTING
        self.current_plan = plan
        self.completed_tasks = set()
        self.failed_tasks = set()
        
        start_time = time.time()
        
        try:
            # Validate plan
            graph = TaskGraph(plan.tasks)
            is_valid, errors = graph.is_valid_dag()
            
            if not is_valid:
                logger.error(f"Invalid plan: {errors}")
                return {
                    "success": False,
                    "error": f"Invalid plan: {'; '.join(errors)}",
                    "completed_tasks": 0,
                    "failed_tasks": 0,
                    "total_tasks": len(plan.tasks)
                }
            
            # Execute based on parallelization setting
            if self.enable_parallel:
                result = await self._execute_parallel(plan, graph, display)
            else:
                result = await self._execute_sequential(plan, graph, display)
            
            elapsed = time.time() - start_time
            
            # Build final result
            final_result = {
                "success": len(self.failed_tasks) == 0,
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_tasks": len(plan.tasks),
                "execution_time": elapsed,
                "tasks": result
            }
            
            self.state = ExecutionState.COMPLETED if final_result["success"] else ExecutionState.FAILED

            logger.info(f"Plan execution completed: {final_result['completed_tasks']}/{final_result['total_tasks']} tasks")

            # === AUDIT HOOK (FASE 4) ===
            # Optional audit callback for programmatic API usage
            if hasattr(self, 'on_plan_audit') and self.on_plan_audit:
                try:
                    from config.settings import get_settings
                    from core.audit import get_auditor
                    from core.audit.independent_auditor import Task, AgentResult

                    settings = get_settings()

                    if settings.enable_truth_audit:
                        # Build audit inputs
                        task = Task(
                            prompt=plan.goal,
                            context={},
                            metadata=final_result
                        )

                        agent_result = AgentResult(
                            success=final_result["success"],
                            output=str(final_result),
                            files_changed=[],
                            tests_run=False,
                            metadata=final_result
                        )

                        # Run audit
                        auditor = get_auditor()
                        audit_report = await auditor.audit_execution(task, agent_result)

                        # Call callback
                        self.on_plan_audit(audit_report)

                        # Add audit to result
                        final_result["audit_report"] = audit_report.to_dict()

                except Exception as e:
                    logger.error(f"Audit failed: {e}")
            # === END AUDIT HOOK ===

            # Callback
            if self.on_plan_complete:
                self.on_plan_complete(final_result)

            return final_result
        
        except Exception as e:
            self.state = ExecutionState.FAILED
            logger.error(f"Execution engine error: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Execution engine error: {str(e)}",
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_tasks": len(plan.tasks) if plan else 0
            }
    
    async def _execute_sequential(
        self,
        plan: EnhancedExecutionPlan,
        graph: TaskGraph,
        display: Optional[Any]
    ) -> List[Dict]:
        """Execute tasks sequentially in topological order"""
        ordered_tasks = graph.get_execution_order()
        results = []
        
        logger.info(f"Executing {len(ordered_tasks)} tasks sequentially")
        
        for task in ordered_tasks:
            result = await self._execute_task_with_retry(task, display)
            results.append(result)
            
            if not result["success"]:
                logger.warning(f"Task {task.id} failed, stopping sequential execution")
                break
        
        return results
    
    async def _execute_parallel(
        self,
        plan: EnhancedExecutionPlan,
        graph: TaskGraph,
        display: Optional[Any]
    ) -> List[Dict]:
        """Execute tasks in parallel batches"""
        batches = graph.get_parallel_batches()
        all_results = []
        
        logger.info(f"Executing {len(plan.tasks)} tasks in {len(batches)} parallel batches")
        
        for batch_num, batch in enumerate(batches, 1):
            logger.info(f"Executing batch {batch_num}/{len(batches)} ({len(batch)} tasks)")
            
            # Execute batch in parallel
            tasks_coroutines = [
                self._execute_task_with_retry(task, display)
                for task in batch
            ]
            
            batch_results = await asyncio.gather(*tasks_coroutines, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    # Exception during execution
                    task = batch[i]
                    all_results.append({
                        "success": False,
                        "task_id": task.id,
                        "error": str(result)
                    })
                else:
                    all_results.append(result)
            
            # Check if any failed
            failed_count = sum(1 for r in batch_results if isinstance(r, Exception) or not r.get("success", False))
            if failed_count > 0:
                logger.warning(f"Batch {batch_num}: {failed_count}/{len(batch)} tasks failed")
        
        return all_results
    
    async def _execute_task_with_retry(
        self,
        task: Task,
        display: Optional[Any]
    ) -> Dict[str, Any]:
        """
        Execute single task with retry logic
        
        Args:
            task: Task to execute
            display: Optional display
        
        Returns:
            Task execution result
        """
        attempt = 0
        last_error = None
        
        while attempt < self.max_retries:
            try:
                # Update task status
                task.mark_running()
                
                # Callback
                if self.on_task_start:
                    self.on_task_start(task)
                
                # Display update
                if display and hasattr(display, 'update_task_status'):
                    display.update_task_status(task, "running")
                
                # Execute
                result = await self._execute_task(task)
                
                # Check result
                if result["success"]:
                    # Success!
                    task_output = TaskOutput(
                        success=True,
                        data=result.get("data"),
                        context=result.get("context", {}),
                        execution_time=task.get_execution_time() if hasattr(task, 'get_execution_time') else 0
                    )
                    task.mark_completed(task_output)
                    self.completed_tasks.add(task.id)
                    
                    logger.info(f"Task {task.id} completed successfully")
                    
                    # Callback
                    if self.on_task_complete:
                        self.on_task_complete(task, result)
                    
                    # Display
                    if display and hasattr(display, 'update_task_status'):
                        display.update_task_status(task, "completed")
                    
                    return result
                else:
                    # Failed but might retry
                    last_error = result.get("error", "Unknown error")
                    
                    if attempt < self.max_retries - 1:
                        # Will retry
                        delay = self._calculate_retry_delay(attempt)
                        
                        logger.warning(f"Task {task.id} failed (attempt {attempt + 1}/{self.max_retries}), retrying in {delay:.1f}s")
                        
                        if display and hasattr(display, 'update_task_status'):
                            display.update_task_status(
                                task,
                                f"retrying (attempt {attempt + 2}/{self.max_retries})"
                            )
                        
                        await asyncio.sleep(delay)
                        attempt += 1
                        continue
                    else:
                        # Max retries reached
                        raise Exception(last_error)
            
            except Exception as e:
                last_error = str(e)
                attempt += 1
                
                if attempt < self.max_retries:
                    # Retry
                    delay = self._calculate_retry_delay(attempt - 1)
                    
                    logger.warning(f"Task {task.id} exception (attempt {attempt}/{self.max_retries}), retrying in {delay:.1f}s: {e}")
                    
                    if display and hasattr(display, 'update_task_status'):
                        display.update_task_status(
                            task,
                            f"retrying (attempt {attempt + 1}/{self.max_retries})"
                        )
                    
                    await asyncio.sleep(delay)
                else:
                    # Failed permanently
                    task.mark_failed(str(e))
                    self.failed_tasks.add(task.id)
                    
                    logger.error(f"Task {task.id} failed permanently after {attempt} attempts: {e}")
                    
                    # Callback
                    if self.on_task_fail:
                        self.on_task_fail(task, str(e))
                    
                    # Display
                    if display and hasattr(display, 'update_task_status'):
                        display.update_task_status(task, "failed")
                    
                    return {
                        "success": False,
                        "task_id": task.id,
                        "error": str(e),
                        "attempts": attempt
                    }
        
        # Should not reach here
        return {
            "success": False,
            "task_id": task.id,
            "error": last_error or "Unknown error",
            "attempts": attempt
        }
    
    async def _execute_task(self, task: Task) -> Dict[str, Any]:
        """
        Execute single task (core execution logic)
        
        Args:
            task: Task to execute
        
        Returns:
            Execution result
        """
        # Get context from completed dependencies
        context = self._gather_dependency_context(task)
        
        # Merge context into task inputs
        enriched_inputs = {**task.requirements.inputs, **context}
        
        # Update task inputs with context
        task.requirements.inputs = enriched_inputs
        
        # Execute based on task type
        if task.type == TaskType.THINK:
            # Pure reasoning task (no tool execution)
            return await self._execute_thinking_task(task)
        
        elif task.type == TaskType.PLAN:
            # Sub-planning task
            return await self._execute_planning_task(task)
        
        else:
            # Standard task with tool execution
            return await self._execute_tool_task(task)
    
    def _gather_dependency_context(self, task: Task) -> Dict[str, Any]:
        """
        Gather context from completed dependency tasks
        
        Args:
            task: Task needing context
        
        Returns:
            Context dict
        """
        context = {}
        
        if not self.current_plan:
            return context
        
        for dep_id in task.depends_on:
            dep_task = self.current_plan.get_task_by_id(dep_id)
            
            if dep_task and dep_task.output and dep_task.output.success:
                # Merge context from dependency
                if dep_task.output.context:
                    context.update(dep_task.output.context)
                
                # Add output data with task-specific key
                context[f"{dep_id}_output"] = dep_task.output.data
        
        return context
    
    async def _execute_thinking_task(self, task: Task) -> Dict[str, Any]:
        """Execute thinking/reasoning task"""
        try:
            from anthropic import AsyncAnthropic
            import os
            
            client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            # Call Claude for reasoning
            response = await client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": f"Think about this: {task.description}\n\nProvide your analysis and reasoning."
                }]
            )
            
            thinking = response.content[0].text
            
            logger.info(f"Thinking task {task.id} completed")
            
            return {
                "success": True,
                "task_id": task.id,
                "data": thinking,
                "context": {"thinking": thinking}
            }
        
        except Exception as e:
            logger.error(f"Thinking task {task.id} failed: {e}")
            return {
                "success": False,
                "task_id": task.id,
                "error": str(e)
            }
    
    async def _execute_planning_task(self, task: Task) -> Dict[str, Any]:
        """Execute sub-planning task"""
        try:
            # Use TaskDecomposer to create sub-plan
            from core.task_decomposer import TaskDecomposerFactory
            
            decomposer = TaskDecomposerFactory.create_with_default_agents()
            sub_plan = await decomposer.decompose(task.description)
            
            logger.info(f"Planning task {task.id} completed with {len(sub_plan.tasks)} sub-tasks")
            
            return {
                "success": True,
                "task_id": task.id,
                "data": sub_plan,
                "context": {"sub_plan": sub_plan}
            }
        
        except Exception as e:
            logger.error(f"Planning task {task.id} failed: {e}")
            return {
                "success": False,
                "task_id": task.id,
                "error": str(e)
            }
    
    async def _execute_tool_task(self, task: Task) -> Dict[str, Any]:
        """Execute task using tool"""
        try:
            # Execute via tool integration (run_in_executor for sync code)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: self.tool_integration.execute_task(task, validate=True)
            )
            
            # Add task context
            result_dict = {
                "success": result.type == "success",
                "task_id": task.id,
                "data": result.content[0].text if result.content else None
            }
            
            # If successful, prepare context for dependents
            if result_dict["success"]:
                result_dict["context"] = {
                    "task_output": result.content[0].text if result.content else None,
                    "task_type": task.type.value
                }
            else:
                result_dict["error"] = result.content[0].text if result.content else "Unknown error"
            
            return result_dict
        
        except Exception as e:
            logger.error(f"Tool task {task.id} failed: {e}")
            return {
                "success": False,
                "task_id": task.id,
                "error": str(e)
            }
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """
        Calculate retry delay based on strategy
        
        Args:
            attempt: Attempt number (0-indexed)
        
        Returns:
            Delay in seconds
        """
        if self.retry_strategy == RetryStrategy.NONE:
            return 0.0
        
        elif self.retry_strategy == RetryStrategy.IMMEDIATE:
            return 0.0
        
        elif self.retry_strategy == RetryStrategy.LINEAR:
            delay = self.base_delay * (attempt + 1)
        
        elif self.retry_strategy == RetryStrategy.EXPONENTIAL:
            delay = self.base_delay * (2 ** attempt)
        
        else:
            delay = self.base_delay
        
        # Add jitter (randomness to prevent thundering herd)
        jitter = random.uniform(0, min(delay * 0.1, 1.0))
        delay += jitter
        
        # Cap at max delay
        return min(delay, self.max_delay)
    
    def pause(self):
        """Pause execution"""
        self.state = ExecutionState.PAUSED
        logger.info("Execution paused")
    
    def resume(self):
        """Resume execution"""
        if self.state == ExecutionState.PAUSED:
            self.state = ExecutionState.EXECUTING
            logger.info("Execution resumed")
    
    def cancel(self):
        """Cancel execution"""
        self.state = ExecutionState.CANCELLED
        logger.info("Execution cancelled")
    
    def save_checkpoint(self, filepath: str):
        """
        Save execution state to checkpoint file
        
        Args:
            filepath: Path to checkpoint file
        """
        import json
        
        checkpoint = {
            "state": self.state.value,
            "completed_tasks": list(self.completed_tasks),
            "failed_tasks": list(self.failed_tasks),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.current_plan:
            # Save plan state
            checkpoint["plan"] = {
                "goal": self.current_plan.goal,
                "tasks": [
                    {
                        "id": t.id,
                        "status": t.status.value,
                        "output": {
                            "success": t.output.success if t.output else None,
                            "data": str(t.output.data)[:500] if t.output and t.output.data else None
                        } if t.output else None
                    }
                    for t in self.current_plan.tasks
                ]
            }
        
        with open(filepath, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        logger.info(f"Checkpoint saved to {filepath}")
    
    def load_checkpoint(self, filepath: str) -> bool:
        """
        Load execution state from checkpoint
        
        Args:
            filepath: Path to checkpoint file
        
        Returns:
            True if loaded successfully
        """
        import json
        
        try:
            with open(filepath, 'r') as f:
                checkpoint = json.load(f)
            
            self.state = ExecutionState(checkpoint["state"])
            self.completed_tasks = set(checkpoint["completed_tasks"])
            self.failed_tasks = set(checkpoint["failed_tasks"])
            
            logger.info(f"Checkpoint loaded from {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return False
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        Get current execution statistics
        
        Returns:
            Dict with execution stats
        
        Examples:
            >>> stats = engine.get_execution_stats()
            >>> print(f"Progress: {stats['progress']:.1f}%")
        """
        if not self.current_plan:
            return {
                "state": self.state.value,
                "total_tasks": 0,
                "completed": 0,
                "failed": 0,
                "remaining": 0,
                "progress": 0
            }
        
        total = len(self.current_plan.tasks)
        completed = len(self.completed_tasks)
        failed = len(self.failed_tasks)
        remaining = total - completed - failed
        
        return {
            "state": self.state.value,
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "remaining": remaining,
            "progress": (completed / total * 100) if total > 0 else 0
        }


class ExecutionPolicy:
    """
    Execution policy configuration
    
    Defines how engine should behave in various scenarios
    """
    
    def __init__(
        self,
        stop_on_first_failure: bool = False,
        skip_failed_dependencies: bool = False,
        allow_partial_success: bool = True,
        timeout_per_task: Optional[int] = None,
        timeout_total: Optional[int] = None
    ):
        """
        Initialize execution policy
        
        Args:
            stop_on_first_failure: Stop entire execution on first task failure
            skip_failed_dependencies: Skip tasks whose dependencies failed
            allow_partial_success: Consider execution successful if some tasks complete
            timeout_per_task: Timeout per task in seconds
            timeout_total: Total execution timeout in seconds
        """
        self.stop_on_first_failure = stop_on_first_failure
        self.skip_failed_dependencies = skip_failed_dependencies
        self.allow_partial_success = allow_partial_success
        self.timeout_per_task = timeout_per_task
        self.timeout_total = timeout_total


# ============================================================================
# Global instance (singleton)
# ============================================================================

_engine: Optional[ExecutionEngine] = None


def get_execution_engine() -> ExecutionEngine:
    """
    Get global ExecutionEngine instance (singleton)
    
    Returns:
        ExecutionEngine instance
    
    Examples:
        >>> engine = get_execution_engine()
        >>> result = await engine.execute_plan(plan)
    """
    global _engine
    if _engine is None:
        _engine = ExecutionEngine()
    return _engine
