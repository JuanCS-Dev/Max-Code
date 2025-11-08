"""
Task Graph Management with DAG Operations

Manages task dependencies as Directed Acyclic Graph (DAG).
Uses NetworkX for graph operations.

Operations:
- DAG validation (cycle detection)
- Topological sorting (execution order)
- Parallel batch detection
- Critical path calculation
- Graph visualization (ASCII, Mermaid)

Biblical Foundation:
"Que tudo seja feito com decência e ordem" (1 Coríntios 14:40)

Architecture:
- NetworkX DiGraph for DAG representation
- Immutable graph (rebuild when tasks change)
- Rich visualizations
- Efficient algorithms

Soli Deo Gloria
"""

import networkx as nx
from typing import List, Set, Dict, Tuple, Optional
from .task_models import Task, EnhancedExecutionPlan


class TaskGraph:
    """
    Manages task dependencies as DAG
    
    Uses NetworkX for efficient graph operations.
    Provides validation, ordering, and visualization.
    
    Attributes:
        tasks: Dictionary of tasks by ID
        graph: NetworkX DiGraph
    
    Examples:
        >>> graph = TaskGraph([task1, task2, task3])
        >>> is_valid, errors = graph.is_valid_dag()
        >>> if is_valid:
        ...     order = graph.get_execution_order()
        ...     batches = graph.get_parallel_batches()
    """
    
    def __init__(self, tasks: List[Task]):
        """
        Initialize task graph
        
        Args:
            tasks: List of tasks with dependencies
        """
        self.tasks = {task.id: task for task in tasks}
        self.graph = nx.DiGraph()
        self._build_graph()
    
    def _build_graph(self):
        """Build NetworkX graph from tasks"""
        # Add nodes
        for task_id in self.tasks:
            self.graph.add_node(task_id)
        
        # Add edges (dependencies)
        for task_id, task in self.tasks.items():
            for dep_id in task.depends_on:
                if dep_id in self.tasks:
                    # Edge: dependency → task (dep must complete before task)
                    self.graph.add_edge(dep_id, task_id)
    
    def is_valid_dag(self) -> Tuple[bool, List[str]]:
        """
        Check if graph is valid DAG
        
        Validates:
        1. No cycles (directed acyclic)
        2. All dependencies exist
        3. No isolated components (optional)
        
        Returns:
            (is_valid, error_messages)
        
        Examples:
            >>> is_valid, errors = graph.is_valid_dag()
            >>> if not is_valid:
            ...     for error in errors:
            ...         print(f"Error: {error}")
        """
        errors = []
        
        # Check 1: Is it a DAG? (no cycles)
        if not nx.is_directed_acyclic_graph(self.graph):
            try:
                # Find a cycle to report
                cycle = nx.find_cycle(self.graph)
                cycle_tasks = [self.tasks[node].description for node, _ in cycle]
                errors.append(f"Circular dependency detected: {' → '.join(cycle_tasks)}")
            except nx.NetworkXNoCycle:
                errors.append("Graph contains cycles but could not identify specific cycle")
        
        # Check 2: All dependencies exist
        for task_id, task in self.tasks.items():
            for dep_id in task.depends_on:
                if dep_id not in self.tasks:
                    errors.append(
                        f"Task '{task.description}' depends on non-existent task '{dep_id}'"
                    )
        
        # Check 3: No self-loops
        if list(nx.selfloop_edges(self.graph)):
            errors.append("Graph contains self-loops (task depending on itself)")
        
        return (len(errors) == 0, errors)
    
    def get_execution_order(self) -> List[Task]:
        """
        Get topologically sorted execution order
        
        Returns tasks in valid execution order where all dependencies
        of a task are completed before the task itself.
        
        Returns:
            List of tasks in execution order
        
        Raises:
            ValueError: If graph is not a valid DAG
        
        Examples:
            >>> order = graph.get_execution_order()
            >>> for i, task in enumerate(order, 1):
            ...     print(f"{i}. {task.description}")
        """
        is_valid, errors = self.is_valid_dag()
        if not is_valid:
            raise ValueError(f"Cannot order invalid DAG: {'; '.join(errors)}")
        
        # Topological sort
        ordered_ids = list(nx.topological_sort(self.graph))
        
        return [self.tasks[task_id] for task_id in ordered_ids]
    
    def get_parallel_batches(self) -> List[List[Task]]:
        """
        Group tasks into batches that can run in parallel
        
        Each batch contains tasks that:
        - Have all dependencies met
        - Can execute concurrently
        
        Returns:
            List of batches, where each batch is a list of tasks
        
        Examples:
            >>> batches = graph.get_parallel_batches()
            >>> for i, batch in enumerate(batches, 1):
            ...     print(f"Batch {i} ({len(batch)} tasks):")
            ...     for task in batch:
            ...         print(f"  - {task.description}")
        """
        batches = []
        remaining = set(self.tasks.keys())
        completed = set()
        
        while remaining:
            # Find tasks with all dependencies met
            ready = []
            for task_id in remaining:
                task = self.tasks[task_id]
                if all(dep in completed for dep in task.depends_on):
                    ready.append(task)
            
            if not ready:
                # Should not happen in valid DAG
                # Remaining tasks have unmet dependencies
                break
            
            batches.append(ready)
            
            # Mark as completed
            for task in ready:
                completed.add(task.id)
                remaining.remove(task.id)
        
        return batches
    
    def get_task_dependencies(self, task_id: str) -> Set[str]:
        """
        Get all dependencies (transitive) for a task
        
        Returns all tasks that must complete before the given task,
        including indirect dependencies.
        
        Args:
            task_id: Task identifier
        
        Returns:
            Set of task IDs (dependencies)
        
        Examples:
            >>> deps = graph.get_task_dependencies("task_3")
            >>> print(f"Task 3 depends on: {deps}")
        """
        if task_id not in self.graph:
            return set()
        
        # NetworkX ancestors = all nodes with path to this node
        return set(nx.ancestors(self.graph, task_id))
    
    def get_dependent_tasks(self, task_id: str) -> Set[str]:
        """
        Get all tasks that depend on this task (transitive)
        
        Returns all tasks that require the given task to complete,
        including indirect dependents.
        
        Args:
            task_id: Task identifier
        
        Returns:
            Set of task IDs (dependents)
        
        Examples:
            >>> dependents = graph.get_dependent_tasks("task_1")
            >>> print(f"If task 1 fails, {len(dependents)} tasks affected")
        """
        if task_id not in self.graph:
            return set()
        
        # NetworkX descendants = all nodes reachable from this node
        return set(nx.descendants(self.graph, task_id))
    
    def get_root_tasks(self) -> List[Task]:
        """
        Get tasks with no dependencies (roots of DAG)
        
        Returns:
            List of root tasks
        
        Examples:
            >>> roots = graph.get_root_tasks()
            >>> print(f"Start with {len(roots)} root tasks")
        """
        roots = []
        for task_id, task in self.tasks.items():
            if not task.depends_on:
                roots.append(task)
        return roots
    
    def get_leaf_tasks(self) -> List[Task]:
        """
        Get tasks with no dependents (leaves of DAG)
        
        Returns:
            List of leaf tasks
        
        Examples:
            >>> leaves = graph.get_leaf_tasks()
            >>> print(f"Plan completes when {len(leaves)} tasks done")
        """
        leaves = []
        for task_id, task in self.tasks.items():
            if not self.get_dependent_tasks(task_id):
                leaves.append(task)
        return leaves
    
    def calculate_critical_path_length(self) -> int:
        """
        Calculate length of critical path (longest path)
        
        The critical path determines the minimum time to complete
        all tasks (assuming infinite parallelism).
        
        Returns:
            Sum of estimated times on longest path (seconds)
        
        Examples:
            >>> critical_time = graph.calculate_critical_path_length()
            >>> total_time = sum(t.estimated_time for t in tasks)
            >>> savings = total_time - critical_time
            >>> print(f"Parallelization saves {savings}s")
        """
        try:
            # Create weighted graph
            weighted_graph = nx.DiGraph()
            for task_id, task in self.tasks.items():
                weighted_graph.add_node(task_id)
            
            for task_id, task in self.tasks.items():
                for dep_id in task.depends_on:
                    weighted_graph.add_edge(dep_id, task_id, weight=self.tasks[dep_id].estimated_time)
            
            # Find longest path using bellman-ford (negated weights)
            # We need to add weights to all nodes, including leaves
            if len(weighted_graph.nodes) == 0:
                return 0
            
            # Use topological sort to calculate longest path
            topo_order = list(nx.topological_sort(weighted_graph))
            distances = {node: 0 for node in weighted_graph.nodes}
            
            for node in topo_order:
                node_time = self.tasks[node].estimated_time
                for successor in weighted_graph.successors(node):
                    distances[successor] = max(
                        distances[successor],
                        distances[node] + node_time
                    )
            
            # Max distance + time of final task
            if not distances:
                return 0
            
            max_node = max(distances.items(), key=lambda x: x[1])
            return max_node[1] + self.tasks[max_node[0]].estimated_time
        
        except nx.NetworkXError:
            # Not a DAG or other error - fallback to sum all
            return sum(task.estimated_time for task in self.tasks.values())
    
    def get_critical_path_tasks(self) -> List[Task]:
        """
        Get tasks on critical path
        
        Returns:
            List of tasks on longest path
        """
        try:
            longest_path = nx.dag_longest_path(self.graph)
            return [self.tasks[task_id] for task_id in longest_path]
        except nx.NetworkXError:
            return []
    
    def visualize_ascii(self) -> str:
        """
        Generate ASCII art visualization of DAG
        
        Simple text representation grouped by depth level.
        
        Returns:
            ASCII visualization string
        
        Examples:
            >>> print(graph.visualize_ascii())
            Task Dependency Graph:
            
            Level 0:
              - Create file.py
              - Install dependencies
            
            Level 1:
              - Modify file.py (depends on: Create file.py)
        """
        lines = []
        lines.append("Task Dependency Graph:")
        lines.append("")
        
        # Group by depth
        depths = {}
        for task_id, task in self.tasks.items():
            depth = self._get_task_depth(task_id)
            if depth not in depths:
                depths[depth] = []
            depths[depth].append(task)
        
        # Print by depth
        for depth in sorted(depths.keys()):
            level_tasks = depths[depth]
            lines.append(f"Level {depth}:")
            
            for task in level_tasks:
                # Show dependencies
                if task.depends_on:
                    dep_names = [
                        self.tasks[d].description[:30] + "..." if len(self.tasks[d].description) > 30
                        else self.tasks[d].description
                        for d in task.depends_on
                        if d in self.tasks
                    ]
                    deps_str = f" (depends on: {', '.join(dep_names)})"
                else:
                    deps_str = ""
                
                # Task description
                desc = task.description
                if len(desc) > 50:
                    desc = desc[:47] + "..."
                
                lines.append(f"  - {desc}{deps_str}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _get_task_depth(self, task_id: str, memo: Optional[Dict] = None) -> int:
        """
        Get depth of task in graph (0 = root)
        
        Args:
            task_id: Task identifier
            memo: Memoization cache
        
        Returns:
            Depth level
        """
        if memo is None:
            memo = {}
        
        if task_id in memo:
            return memo[task_id]
        
        task = self.tasks[task_id]
        
        if not task.depends_on:
            depth = 0
        else:
            dep_depths = [
                self._get_task_depth(dep, memo)
                for dep in task.depends_on
                if dep in self.tasks
            ]
            depth = max(dep_depths, default=0) + 1
        
        memo[task_id] = depth
        return depth
    
    def export_mermaid(self) -> str:
        """
        Export as Mermaid diagram
        
        Can be rendered in markdown or Mermaid live editor.
        
        Returns:
            Mermaid diagram markdown
        
        Examples:
            >>> mermaid = graph.export_mermaid()
            >>> with open("plan.md", "w") as f:
            ...     f.write(mermaid)
        """
        lines = ["```mermaid", "graph TD"]
        
        # Add nodes with labels
        for task_id, task in self.tasks.items():
            # Truncate long descriptions
            label = task.description[:40]
            if len(task.description) > 40:
                label += "..."
            
            # Escape quotes
            label = label.replace('"', "'")
            
            # Add risk indicator
            risk_icons = {
                "low": "🟢",
                "medium": "🟡",
                "high": "🔴",
                "critical": "🚨"
            }
            risk_icon = risk_icons.get(task.risk_level, "")
            
            lines.append(f'    {task_id}["{risk_icon} {label}"]')
        
        # Add edges (dependencies)
        for task_id, task in self.tasks.items():
            for dep_id in task.depends_on:
                if dep_id in self.tasks:
                    lines.append(f"    {dep_id} --> {task_id}")
        
        lines.append("```")
        
        return "\n".join(lines)
    
    def export_dot(self) -> str:
        """
        Export as DOT (Graphviz) format
        
        Can be rendered with Graphviz tools.
        
        Returns:
            DOT format string
        """
        from io import StringIO
        output = StringIO()
        
        # Write DOT
        nx.drawing.nx_pydot.write_dot(self.graph, output)
        
        return output.getvalue()
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get graph statistics
        
        Returns:
            Dictionary with graph metrics
        """
        is_valid, _ = self.is_valid_dag()
        
        stats = {
            "total_tasks": len(self.tasks),
            "is_valid_dag": is_valid,
            "root_tasks": len(self.get_root_tasks()),
            "leaf_tasks": len(self.get_leaf_tasks()),
            "max_depth": max(
                (self._get_task_depth(tid) for tid in self.tasks),
                default=0
            ),
            "critical_path_length": self.calculate_critical_path_length(),
            "total_sequential_time": sum(t.estimated_time for t in self.tasks.values()),
            "parallel_batches": len(self.get_parallel_batches())
        }
        
        # Calculate parallelization benefit
        if stats["total_sequential_time"] > 0:
            savings = stats["total_sequential_time"] - stats["critical_path_length"]
            stats["time_savings_percent"] = (savings / stats["total_sequential_time"]) * 100
        else:
            stats["time_savings_percent"] = 0
        
        return stats


class TaskGraphBuilder:
    """
    Builder for creating TaskGraph from various sources
    
    Examples:
        >>> builder = TaskGraphBuilder()
        >>> builder.add_task(task1)
        >>> builder.add_task(task2)
        >>> builder.add_dependency(task2.id, task1.id)
        >>> graph = builder.build()
    """
    
    def __init__(self):
        """Initialize builder"""
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task) -> 'TaskGraphBuilder':
        """
        Add task to builder
        
        Args:
            task: Task to add
        
        Returns:
            Self (for chaining)
        """
        self.tasks[task.id] = task
        return self
    
    def add_tasks(self, tasks: List[Task]) -> 'TaskGraphBuilder':
        """
        Add multiple tasks
        
        Args:
            tasks: List of tasks
        
        Returns:
            Self (for chaining)
        """
        for task in tasks:
            self.tasks[task.id] = task
        return self
    
    def add_dependency(self, task_id: str, depends_on_id: str) -> 'TaskGraphBuilder':
        """
        Add dependency between tasks
        
        Args:
            task_id: Dependent task ID
            depends_on_id: Dependency task ID
        
        Returns:
            Self (for chaining)
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if depends_on_id not in task.depends_on:
                task.depends_on.append(depends_on_id)
        return self
    
    def build(self) -> TaskGraph:
        """
        Build TaskGraph
        
        Returns:
            TaskGraph instance
        """
        return TaskGraph(list(self.tasks.values()))
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate before building
        
        Returns:
            (is_valid, errors)
        """
        graph = self.build()
        return graph.is_valid_dag()


# Export
__all__ = [
    'TaskGraph',
    'TaskGraphBuilder',
]
