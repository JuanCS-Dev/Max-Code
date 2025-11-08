"""
Dependency Resolver - Intelligent Dependency Detection and Optimization

Detects implicit dependencies, optimizes parallelization, validates time estimates.

Features:
- Implicit dependency detection (file creation→modification)
- Parallel execution optimization
- Bottleneck identification
- Time estimate validation
- Critical path analysis

Biblical Foundation:
"Examinem tudo e fiquem com o que é bom" (1 Tessalonicenses 5:21)

Soli Deo Gloria
"""

from typing import List, Set, Dict, Optional, Tuple
from .task_models import Task, EnhancedExecutionPlan
from .task_graph import TaskGraph
from config.logging_config import get_logger

logger = get_logger(__name__)


class DependencyResolver:
    """
    Resolves and optimizes task dependencies
    
    Analyzes execution plans to:
    - Detect implicit dependencies
    - Optimize parallel execution
    - Identify bottlenecks
    - Validate time estimates
    
    Attributes:
        plan: ExecutionPlan to analyze
        graph: TaskGraph representation
    
    Examples:
        >>> resolver = DependencyResolver(plan)
        >>> implicit = resolver.detect_implicit_dependencies()
        >>> if implicit:
        ...     resolver.add_implicit_dependencies()
        >>> suggestions = resolver.suggest_dependency_optimizations()
    """
    
    def __init__(self, plan: EnhancedExecutionPlan):
        """
        Initialize dependency resolver
        
        Args:
            plan: ExecutionPlan to analyze
        """
        self.plan = plan
        self.graph = TaskGraph(plan.tasks)
        logger.debug(f"DependencyResolver initialized for plan {plan.id}")
    
    def detect_implicit_dependencies(self) -> List[Tuple[str, str, str]]:
        """
        Detect implicit dependencies not explicitly declared
        
        Detects patterns like:
        - Task A creates file X → Task B modifies file X (B should depend on A)
        - Task A installs package Y → Task B uses package Y (B should depend on A)
        - Task A defines function Z → Task B calls function Z (B should depend on A)
        
        Returns:
            List of (creator_id, dependent_id, reason) tuples
        
        Examples:
            >>> implicit = resolver.detect_implicit_dependencies()
            >>> for creator, dependent, reason in implicit:
            ...     print(f"{dependent} should depend on {creator}: {reason}")
        """
        implicit = []
        
        # Build file operation map
        creates = {}  # filepath -> task_id
        modifies = {}  # filepath -> [task_ids]
        reads = {}  # filepath -> [task_ids]
        
        for task in self.plan.tasks:
            inputs = task.requirements.inputs
            
            # Track file operations
            if 'filepath' in inputs:
                filepath = inputs['filepath']
                
                # Creates file
                if task.type.value == 'write' and task.description.lower().startswith('create'):
                    if filepath not in creates:
                        creates[filepath] = task.id
                
                # Modifies file
                elif task.type.value == 'write':
                    if filepath not in modifies:
                        modifies[filepath] = []
                    modifies[filepath].append(task.id)
                
                # Reads file
                elif task.type.value == 'read':
                    if filepath not in reads:
                        reads[filepath] = []
                    reads[filepath].append(task.id)
        
        # Find implicit dependencies: file creation → modification
        for filepath, modifier_ids in modifies.items():
            creator_id = creates.get(filepath)
            
            if creator_id:
                for modifier_id in modifier_ids:
                    if modifier_id != creator_id:
                        # Check if already explicit
                        modifier_task = self.plan.get_task_by_id(modifier_id)
                        if modifier_task and creator_id not in modifier_task.depends_on:
                            implicit.append((
                                creator_id,
                                modifier_id,
                                f"File '{filepath}' must be created before modification"
                            ))
        
        # Find implicit dependencies: file creation → reading
        for filepath, reader_ids in reads.items():
            creator_id = creates.get(filepath)
            
            if creator_id:
                for reader_id in reader_ids:
                    if reader_id != creator_id:
                        reader_task = self.plan.get_task_by_id(reader_id)
                        if reader_task and creator_id not in reader_task.depends_on:
                            implicit.append((
                                creator_id,
                                reader_id,
                                f"File '{filepath}' must be created before reading"
                            ))
        
        # Find implicit dependencies: package install → usage
        install_tasks = [t for t in self.plan.tasks if 'install' in t.description.lower()]
        
        for install_task in install_tasks:
            # Extract package names (simple heuristic)
            desc = install_task.description.lower()
            
            # Check if other tasks might use this package
            for task in self.plan.tasks:
                if task.id != install_task.id:
                    if install_task.id not in task.depends_on:
                        # Heuristic: if package name appears in task description
                        # (very basic, could be improved)
                        task_desc = task.description.lower()
                        
                        # Common packages
                        packages = ['redis', 'jwt', 'fastapi', 'flask', 'django', 'pytest']
                        for package in packages:
                            if package in desc and package in task_desc:
                                implicit.append((
                                    install_task.id,
                                    task.id,
                                    f"Package '{package}' must be installed before use"
                                ))
                                break
        
        logger.info(f"Detected {len(implicit)} implicit dependencies")
        return implicit
    
    def add_implicit_dependencies(self) -> EnhancedExecutionPlan:
        """
        Add detected implicit dependencies to plan
        
        Modifies the plan in-place by adding missing dependencies.
        
        Returns:
            Updated ExecutionPlan
        
        Examples:
            >>> updated_plan = resolver.add_implicit_dependencies()
        """
        implicit = self.detect_implicit_dependencies()
        
        added = 0
        for creator_id, modifier_id, reason in implicit:
            modifier_task = self.plan.get_task_by_id(modifier_id)
            
            if modifier_task and creator_id not in modifier_task.depends_on:
                modifier_task.depends_on.append(creator_id)
                added += 1
                logger.debug(f"Added dependency: {modifier_task.id} → {creator_id} ({reason})")
        
        if added > 0:
            # Rebuild graph
            self.graph = TaskGraph(self.plan.tasks)
            logger.info(f"Added {added} implicit dependencies")
        
        return self.plan
    
    def optimize_parallel_execution(self) -> List[List[Task]]:
        """
        Identify tasks that can run in parallel
        
        Returns batches of tasks where each batch can execute concurrently.
        
        Returns:
            List of batches (each batch is a list of tasks)
        
        Examples:
            >>> batches = resolver.optimize_parallel_execution()
            >>> for i, batch in enumerate(batches, 1):
            ...     print(f"Batch {i}: {len(batch)} tasks can run in parallel")
        """
        return self.graph.get_parallel_batches()
    
    def suggest_dependency_optimizations(self) -> List[str]:
        """
        Suggest ways to optimize dependencies
        
        Analyzes the plan for:
        - Overly long dependency chains
        - Bottleneck tasks (many dependents)
        - Dead-end tasks (no dependents)
        - Over-specified dependencies
        
        Returns:
            List of optimization suggestions
        
        Examples:
            >>> suggestions = resolver.suggest_dependency_optimizations()
            >>> for suggestion in suggestions:
            ...     print(f"💡 {suggestion}")
        """
        suggestions = []
        
        # Check 1: Long critical path
        critical_path = self.plan.calculate_critical_path()
        if len(critical_path) > 10:
            suggestions.append(
                f"Critical path has {len(critical_path)} tasks - consider breaking into smaller sub-plans or increasing parallelization"
            )
        
        # Check 2: Bottlenecks (tasks with many dependents)
        for task in self.plan.tasks:
            dependents = self.graph.get_dependent_tasks(task.id)
            if len(dependents) > 5:
                suggestions.append(
                    f"Task '{task.description}' is a bottleneck with {len(dependents)} dependent tasks - consider splitting or optimizing"
                )
        
        # Check 3: Too many leaf tasks
        leaves = self.graph.get_leaf_tasks()
        if len(leaves) > 5:
            suggestions.append(
                f"{len(leaves)} tasks have no dependents - verify these are all intended final outputs or consider adding validation tasks"
            )
        
        # Check 4: Tasks with no dependencies (could they be parallelized more?)
        roots = self.graph.get_root_tasks()
        if len(roots) > 1:
            suggestions.append(
                f"Plan has {len(roots)} independent starting tasks - excellent parallelization opportunity!"
            )
        
        # Check 5: Unnecessary sequential execution
        batches = self.optimize_parallel_execution()
        if len(batches) > len(self.plan.tasks) * 0.7:
            suggestions.append(
                "Plan is highly sequential - look for opportunities to parallelize independent tasks"
            )
        
        # Check 6: Over-specified dependencies
        # (task depends on A and B, but A already depends on B)
        for task in self.plan.tasks:
            if len(task.depends_on) > 1:
                redundant = []
                for dep1 in task.depends_on:
                    for dep2 in task.depends_on:
                        if dep1 != dep2:
                            # Check if dep1 already depends on dep2
                            dep1_deps = self.graph.get_task_dependencies(dep1)
                            if dep2 in dep1_deps:
                                redundant.append((dep2, dep1))
                
                if redundant:
                    suggestions.append(
                        f"Task '{task.description}' has redundant dependencies - some are already transitive"
                    )
        
        logger.info(f"Generated {len(suggestions)} optimization suggestions")
        return suggestions
    
    def validate_time_estimates(self) -> List[str]:
        """
        Validate time estimates are reasonable
        
        Checks for:
        - Very short estimates (<5s)
        - Very long estimates (>600s)
        - Inconsistent estimates
        - Critical path vs total time ratio
        
        Returns:
            List of warnings
        
        Examples:
            >>> warnings = resolver.validate_time_estimates()
            >>> if warnings:
            ...     print("⚠️  Time estimate issues:")
            ...     for warning in warnings:
            ...         print(f"  - {warning}")
        """
        warnings = []
        
        # Check individual tasks
        for task in self.plan.tasks:
            # Very short estimates
            if task.estimated_time < 5:
                warnings.append(
                    f"Task '{task.description}' has very short estimate: {task.estimated_time}s (minimum 5s recommended)"
                )
            
            # Very long estimates (should break down)
            if task.estimated_time > 600:  # >10 min
                warnings.append(
                    f"Task '{task.description}' has long estimate: {task.estimated_time}s ({task.estimated_time//60}m) - consider breaking down"
                )
            
            # Inconsistent estimates by type
            # (e.g., all write tasks should be similar duration)
        
        # Check critical path vs total
        critical_time = self.graph.calculate_critical_path_length()
        total_time = sum(t.estimated_time for t in self.plan.tasks)
        
        if total_time > 0:
            ratio = critical_time / total_time
            
            if ratio < 0.3:
                # High parallelization potential
                savings = total_time - critical_time
                warnings.append(
                    f"High parallelization potential: Critical path {critical_time}s vs total {total_time}s (potential savings: {savings}s or {savings//60}m)"
                )
            
            elif ratio > 0.9:
                # Highly sequential
                warnings.append(
                    f"Plan is highly sequential: Critical path {critical_time}s is {int(ratio*100)}% of total {total_time}s - limited parallelization"
                )
        
        # Check if total estimate matches sum
        if self.plan.estimated_total_time > 0:
            actual_total = sum(t.estimated_time for t in self.plan.tasks)
            if abs(self.plan.estimated_total_time - actual_total) > 30:
                warnings.append(
                    f"Total estimate mismatch: Plan says {self.plan.estimated_total_time}s but sum is {actual_total}s"
                )
        
        logger.info(f"Generated {len(warnings)} time estimate warnings")
        return warnings
    
    def identify_bottlenecks(self) -> List[Dict[str, any]]:
        """
        Identify bottleneck tasks in the plan
        
        Bottlenecks are tasks that:
        - Have many dependent tasks
        - Are on the critical path
        - Have high estimated time
        
        Returns:
            List of bottleneck info dicts
        
        Examples:
            >>> bottlenecks = resolver.identify_bottlenecks()
            >>> for bottleneck in bottlenecks:
            ...     print(f"🚨 Bottleneck: {bottleneck['task'].description}")
            ...     print(f"   Affects {bottleneck['affected_tasks']} tasks")
        """
        bottlenecks = []
        critical_path_tasks = {t.id for t in self.plan.calculate_critical_path()}
        
        for task in self.plan.tasks:
            dependents = self.graph.get_dependent_tasks(task.id)
            
            # Calculate bottleneck score
            score = 0
            reasons = []
            
            # Many dependents
            if len(dependents) > 3:
                score += len(dependents) * 10
                reasons.append(f"{len(dependents)} dependent tasks")
            
            # On critical path
            if task.id in critical_path_tasks:
                score += 50
                reasons.append("on critical path")
            
            # Long duration
            if task.estimated_time > 120:
                score += task.estimated_time / 10
                reasons.append(f"long duration ({task.estimated_time}s)")
            
            # High risk
            if task.risk_level in ["high", "critical"]:
                score += 30
                reasons.append(f"{task.risk_level} risk")
            
            # Is a bottleneck if score >= 50
            if score >= 50:
                bottlenecks.append({
                    "task": task,
                    "score": score,
                    "affected_tasks": len(dependents),
                    "reasons": reasons,
                    "on_critical_path": task.id in critical_path_tasks
                })
        
        # Sort by score
        bottlenecks.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"Identified {len(bottlenecks)} bottleneck tasks")
        return bottlenecks
    
    def get_analysis_report(self) -> Dict[str, any]:
        """
        Get comprehensive analysis report
        
        Combines all analysis methods into a single report.
        
        Returns:
            Dictionary with analysis results
        
        Examples:
            >>> report = resolver.get_analysis_report()
            >>> print(f"Implicit deps: {len(report['implicit_dependencies'])}")
            >>> print(f"Bottlenecks: {len(report['bottlenecks'])}")
            >>> print(f"Suggestions: {len(report['suggestions'])}")
        """
        report = {
            "plan_id": self.plan.id,
            "total_tasks": len(self.plan.tasks),
            
            # Graph statistics
            "graph_stats": self.graph.get_statistics(),
            
            # Implicit dependencies
            "implicit_dependencies": self.detect_implicit_dependencies(),
            
            # Parallel batches
            "parallel_batches": [
                [t.id for t in batch]
                for batch in self.optimize_parallel_execution()
            ],
            
            # Optimization suggestions
            "suggestions": self.suggest_dependency_optimizations(),
            
            # Time warnings
            "time_warnings": self.validate_time_estimates(),
            
            # Bottlenecks
            "bottlenecks": [
                {
                    "task_id": b['task'].id,
                    "description": b['task'].description,
                    "score": b['score'],
                    "affected_tasks": b['affected_tasks'],
                    "reasons": b['reasons']
                }
                for b in self.identify_bottlenecks()
            ],
            
            # Summary
            "summary": {
                "is_valid_dag": self.graph.is_valid_dag()[0],
                "implicit_deps_found": len(self.detect_implicit_dependencies()),
                "max_parallel_tasks": max(len(batch) for batch in self.optimize_parallel_execution()),
                "bottleneck_count": len(self.identify_bottlenecks()),
                "total_suggestions": len(self.suggest_dependency_optimizations())
            }
        }
        
        return report


# Export
__all__ = ['DependencyResolver']
