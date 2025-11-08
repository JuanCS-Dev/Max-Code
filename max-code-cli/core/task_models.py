"""
Enhanced Task Models with Dependency Support

Provides rich task models for complex prompt decomposition:
- Task: Enhanced version of ToolStep with dependencies
- TaskRequirement: What a task needs (agent, tools, inputs)
- TaskOutput: Structured output with context passing
- TaskStatus/TaskType: Enums for state management
- ExecutionPlan: Enhanced with DAG support

Biblical Foundation:
"Planejem cuidadosamente o que fazem" (Provérbios 4:26 NTLH)
"Os planos bem elaborados levam à fartura" (Provérbios 21:5)

Architecture:
- Backward compatible with ToolStep
- Integrates with existing ExecutionPlan
- Designed for DAG (NetworkX) operations
- Supports parallel execution

Soli Deo Gloria
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
from enum import Enum
from datetime import datetime
import uuid


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"        # Not ready (dependencies not met)
    READY = "ready"            # Ready to execute (dependencies met)
    RUNNING = "running"        # Currently executing
    COMPLETED = "completed"    # Successfully completed
    FAILED = "failed"          # Failed with error
    SKIPPED = "skipped"        # Skipped (dependency failed)
    CANCELLED = "cancelled"    # Cancelled by user


class TaskType(Enum):
    """Types of tasks for classification"""
    READ = "read"              # Read files, analyze code
    WRITE = "write"            # Create/modify files
    EXECUTE = "execute"        # Run commands, scripts
    VALIDATE = "validate"      # Check, test, verify
    PLAN = "plan"              # Sub-planning, strategy
    THINK = "think"            # Pure reasoning, analysis


@dataclass
class TaskRequirement:
    """
    What a task needs to execute
    
    Defines all prerequisites and resources needed for execution.
    
    Attributes:
        agent_type: Which agent should execute ("code", "test", "fix", etc)
        tools: List of tools needed (["file_editor", "grep_tool"])
        inputs: Input parameters ({"filepath": "main.py", "content": "..."})
        context_dependencies: IDs of tasks whose output is needed
    
    Examples:
        >>> req = TaskRequirement(
        ...     agent_type="code",
        ...     tools=["file_editor"],
        ...     inputs={"filepath": "main.py"},
        ...     context_dependencies=["task_1"]
        ... )
    """
    agent_type: str
    tools: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    context_dependencies: List[str] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate requirements
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        if not self.agent_type:
            errors.append("agent_type is required")
        
        if not isinstance(self.tools, list):
            errors.append("tools must be a list")
        
        if not isinstance(self.inputs, dict):
            errors.append("inputs must be a dict")
        
        return (len(errors) == 0, errors)


@dataclass
class TaskOutput:
    """
    Output from task execution
    
    Captures results and context for dependent tasks.
    
    Attributes:
        success: Whether task succeeded
        data: The actual output data (varies by task type)
        context: Context to pass to dependent tasks
        error: Error message if failed
        execution_time: Time taken in seconds
        logs: Execution logs (optional)
    
    Examples:
        >>> output = TaskOutput(
        ...     success=True,
        ...     data={"filepath": "main.py", "lines_written": 50},
        ...     context={"main_function": "calculate"}
        ... )
    """
    success: bool
    data: Any
    context: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    execution_time: float = 0.0
    logs: List[str] = field(default_factory=list)
    
    def add_log(self, message: str):
        """Add log message"""
        self.logs.append(f"[{datetime.now().isoformat()}] {message}")
    
    def get_context_value(self, key: str, default: Any = None) -> Any:
        """Get value from context"""
        return self.context.get(key, default)


@dataclass
class Task:
    """
    Enhanced task with dependency support
    
    Represents a single executable step in a decomposed plan.
    Enhanced version of ToolStep with:
    - Dependency tracking (depends_on)
    - Status management
    - Output capturing
    - Context passing
    - Risk assessment
    
    Attributes:
        id: Unique task identifier
        description: What this task does
        type: Task type (READ/WRITE/EXECUTE/etc)
        requirements: What's needed to execute
        depends_on: List of task IDs this depends on
        status: Current execution status
        priority: Execution priority (0=lowest)
        estimated_time: Estimated time in seconds
        output: Result of execution (if completed)
        started_at: When execution started
        completed_at: When execution finished
        reasoning: Why this task exists
        alternatives_considered: Other approaches considered
        risk_level: Risk assessment (low/medium/high/critical)
    
    Examples:
        >>> task = Task(
        ...     id="task_1",
        ...     description="Create main.py file",
        ...     type=TaskType.WRITE,
        ...     requirements=TaskRequirement(
        ...         agent_type="code",
        ...         tools=["file_writer"],
        ...         inputs={"filepath": "main.py"}
        ...     ),
        ...     depends_on=[],
        ...     estimated_time=30
        ... )
    """
    id: str = field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    description: str = ""
    type: TaskType = TaskType.WRITE
    requirements: TaskRequirement = field(default_factory=lambda: TaskRequirement(
        agent_type="code",
        tools=[],
        inputs={},
        context_dependencies=[]
    ))
    depends_on: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0
    estimated_time: int = 30
    output: Optional[TaskOutput] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    reasoning: str = ""
    alternatives_considered: List[str] = field(default_factory=list)
    risk_level: str = "low"
    
    def can_execute(self, completed_tasks: Set[str]) -> bool:
        """
        Check if all dependencies are met
        
        Args:
            completed_tasks: Set of completed task IDs
        
        Returns:
            True if ready to execute
        """
        return all(dep_id in completed_tasks for dep_id in self.depends_on)
    
    def mark_ready(self):
        """Mark task as ready to execute"""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.READY
    
    def mark_running(self):
        """Mark task as running"""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now()
    
    def mark_completed(self, output: TaskOutput):
        """
        Mark task as completed
        
        Args:
            output: Task output
        """
        self.status = TaskStatus.COMPLETED
        self.output = output
        self.completed_at = datetime.now()
    
    def mark_failed(self, error: str):
        """
        Mark task as failed
        
        Args:
            error: Error message
        """
        self.status = TaskStatus.FAILED
        self.output = TaskOutput(
            success=False,
            data=None,
            context={},
            error=error
        )
        self.completed_at = datetime.now()
    
    def mark_skipped(self, reason: str):
        """
        Mark task as skipped
        
        Args:
            reason: Why task was skipped
        """
        self.status = TaskStatus.SKIPPED
        self.output = TaskOutput(
            success=False,
            data=None,
            context={},
            error=f"Skipped: {reason}"
        )
        self.completed_at = datetime.now()
    
    def get_execution_time(self) -> float:
        """
        Get actual execution time
        
        Returns:
            Execution time in seconds (0 if not completed)
        """
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0
    
    def get_context(self) -> Dict[str, Any]:
        """Get context from output (for dependent tasks)"""
        if self.output:
            return self.output.context
        return {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type.value,
            "agent": self.requirements.agent_type,
            "tools": self.requirements.tools,
            "inputs": self.requirements.inputs,
            "depends_on": self.depends_on,
            "status": self.status.value,
            "priority": self.priority,
            "estimated_time": self.estimated_time,
            "risk_level": self.risk_level,
            "reasoning": self.reasoning,
            "execution_time": self.get_execution_time()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create Task from dictionary"""
        # Map type string to enum
        type_map = {
            'read': TaskType.READ,
            'write': TaskType.WRITE,
            'execute': TaskType.EXECUTE,
            'validate': TaskType.VALIDATE,
            'plan': TaskType.PLAN,
            'think': TaskType.THINK
        }
        task_type = type_map.get(data.get('type', 'write'), TaskType.WRITE)
        
        # Build requirements
        requirements = TaskRequirement(
            agent_type=data.get('agent', 'code'),
            tools=data.get('tools', []),
            inputs=data.get('inputs', {}),
            context_dependencies=data.get('context_dependencies', [])
        )
        
        return cls(
            id=data.get('id', ''),
            description=data.get('description', ''),
            type=task_type,
            requirements=requirements,
            depends_on=data.get('depends_on', []),
            priority=data.get('priority', 0),
            estimated_time=data.get('estimated_time', 30),
            risk_level=data.get('risk_level', 'low'),
            reasoning=data.get('reasoning', '')
        )


@dataclass
class EnhancedExecutionPlan:
    """
    Enhanced execution plan with DAG support
    
    Extends the existing ExecutionPlan concept with:
    - DAG-based task dependencies
    - Parallel execution support
    - Critical path analysis
    - Validation and optimization
    
    Note: This coexists with the existing ExecutionPlan in task_planner.py
    
    Attributes:
        id: Unique plan identifier
        goal: Original prompt/goal
        tasks: List of tasks with dependencies
        created_at: When plan was created
        estimated_total_time: Total estimated time (sequential)
        complexity_score: Complexity metric (0-100)
        thinking_process: Claude's decomposition reasoning
        alternatives_considered: Other decomposition approaches
        validated: Whether plan has been validated
        validation_issues: Issues found during validation
        metadata: Additional metadata
    
    Examples:
        >>> plan = EnhancedExecutionPlan(
        ...     goal="Create JWT authentication",
        ...     tasks=[task1, task2, task3],
        ...     estimated_total_time=180,
        ...     complexity_score=65.0
        ... )
    """
    id: str = field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    goal: str = ""
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    estimated_total_time: int = 0
    complexity_score: float = 0.0
    thinking_process: str = ""
    alternatives_considered: List[Dict] = field(default_factory=list)
    validated: bool = False
    validation_issues: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get task by ID
        
        Args:
            task_id: Task identifier
        
        Returns:
            Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_ready_tasks(self, completed_task_ids: Set[str]) -> List[Task]:
        """
        Get tasks ready to execute
        
        Args:
            completed_task_ids: Set of completed task IDs
        
        Returns:
            List of tasks whose dependencies are met (excluding already completed)
        """
        ready = []
        for task in self.tasks:
            # Skip already completed tasks
            if task.id in completed_task_ids:
                continue
            
            if task.status == TaskStatus.PENDING and task.can_execute(completed_task_ids):
                ready.append(task)
        return ready
    
    def get_task_depth(self, task: Task, memo: Optional[Dict[str, int]] = None) -> int:
        """
        Get depth of task in DAG (for visualization)
        
        Args:
            task: Task to analyze
            memo: Memoization cache
        
        Returns:
            Depth level (0 = root)
        """
        if memo is None:
            memo = {}
        
        if task.id in memo:
            return memo[task.id]
        
        if not task.depends_on:
            depth = 0
        else:
            dep_depths = []
            for dep_id in task.depends_on:
                dep_task = self.get_task_by_id(dep_id)
                if dep_task:
                    dep_depths.append(self.get_task_depth(dep_task, memo))
            depth = max(dep_depths, default=0) + 1
        
        memo[task.id] = depth
        return depth
    
    def calculate_critical_path(self) -> List[Task]:
        """
        Calculate critical path (longest path through DAG by time)
        
        Returns:
            List of tasks on critical path
        """
        max_chain = []
        max_time = 0
        
        for task in self.tasks:
            chain = self._get_chain_to_task(task)
            chain_time = sum(t.estimated_time for t in chain)
            if chain_time > max_time:
                max_time = chain_time
                max_chain = chain
        
        return max_chain
    
    def _get_chain_to_task(self, task: Task) -> List[Task]:
        """
        Get chain of dependencies to task
        
        Args:
            task: Target task
        
        Returns:
            List of tasks in dependency chain
        """
        if not task.depends_on:
            return [task]
        
        chains = []
        for dep_id in task.depends_on:
            dep_task = self.get_task_by_id(dep_id)
            if dep_task:
                chain = self._get_chain_to_task(dep_task)
                chains.append(chain)
        
        # Get longest chain by time
        longest_chain = max(
            chains,
            key=lambda c: sum(t.estimated_time for t in c),
            default=[]
        )
        return longest_chain + [task]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get plan statistics
        
        Returns:
            Dictionary with statistics
        """
        total_tasks = len(self.tasks)
        
        # Count by status
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = sum(
                1 for t in self.tasks if t.status == status
            )
        
        # Count by type
        type_counts = {}
        for task_type in TaskType:
            type_counts[task_type.value] = sum(
                1 for t in self.tasks if t.type == task_type
            )
        
        # Count by risk
        risk_counts = {
            "low": sum(1 for t in self.tasks if t.risk_level == "low"),
            "medium": sum(1 for t in self.tasks if t.risk_level == "medium"),
            "high": sum(1 for t in self.tasks if t.risk_level == "high"),
            "critical": sum(1 for t in self.tasks if t.risk_level == "critical")
        }
        
        # Calculate progress
        completed = status_counts.get("completed", 0)
        failed = status_counts.get("failed", 0)
        progress = (completed / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
            "progress": progress,
            "status_counts": status_counts,
            "type_counts": type_counts,
            "risk_counts": risk_counts,
            "estimated_time": self.estimated_total_time,
            "complexity": self.complexity_score
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "goal": self.goal,
            "tasks": [t.to_dict() for t in self.tasks],
            "created_at": self.created_at.isoformat(),
            "estimated_total_time": self.estimated_total_time,
            "complexity_score": self.complexity_score,
            "thinking_process": self.thinking_process,
            "alternatives_considered": self.alternatives_considered,
            "validated": self.validated,
            "validation_issues": self.validation_issues,
            "metadata": self.metadata,
            "statistics": self.get_statistics()
        }


# Helper function to convert ToolStep to Task (backward compatibility)
def toolstep_to_task(toolstep, task_id: Optional[str] = None) -> Task:
    """
    Convert ToolStep to Task
    
    Provides backward compatibility with existing code using ToolStep.
    
    Args:
        toolstep: ToolStep instance (from task_planner.py)
        task_id: Optional task ID (generated if not provided)
    
    Returns:
        Task instance
    """
    from core.task_planner import ToolStep
    
    if not isinstance(toolstep, ToolStep):
        raise ValueError("Expected ToolStep instance")
    
    # Infer task type from tool_name
    type_map = {
        "file_reader": TaskType.READ,
        "grep_tool": TaskType.READ,
        "file_writer": TaskType.WRITE,
        "file_editor": TaskType.WRITE,
        "bash": TaskType.EXECUTE,
        "test_runner": TaskType.VALIDATE
    }
    task_type = type_map.get(toolstep.tool_name, TaskType.WRITE)
    
    # Build requirements
    requirements = TaskRequirement(
        agent_type="code",  # Default
        tools=[toolstep.tool_name],
        inputs=toolstep.parameters,
        context_dependencies=[]
    )
    
    # Create task
    task = Task(
        id=task_id or f"task_{toolstep.step_number}",
        description=toolstep.description,
        type=task_type,
        requirements=requirements,
        depends_on=[],  # ToolStep doesn't have dependencies
        risk_level=toolstep.constitutional_risk.lower() if hasattr(toolstep, 'constitutional_risk') else "low"
    )
    
    # Transfer execution state
    if hasattr(toolstep, 'executed') and toolstep.executed:
        if hasattr(toolstep, 'result') and toolstep.result:
            task.mark_completed(TaskOutput(
                success=True,
                data=toolstep.result,
                context={}
            ))
        elif hasattr(toolstep, 'error') and toolstep.error:
            task.mark_failed(toolstep.error)
    
    return task


# Export
__all__ = [
    'TaskStatus',
    'TaskType',
    'TaskRequirement',
    'TaskOutput',
    'Task',
    'EnhancedExecutionPlan',
    'toolstep_to_task',
]
