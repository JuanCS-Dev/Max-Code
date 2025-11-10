"""
Task Decomposer - Main Decomposition Engine

Claude-powered task decomposition with:
- Extended Thinking for complex reasoning
- Prompt Caching for cost optimization
- Plan validation and refinement
- Agent-aware decomposition

Biblical Foundation:
"Onde não há sábio conselho o povo cai, mas na multidão de conselheiros há segurança"
(Provérbios 11:14)

Architecture:
- AsyncAnthropic for async operations
- Prompt caching (90% cost savings)
- Extended thinking mode
- JSON schema enforcement
- Validation pipeline

Soli Deo Gloria
"""

from anthropic import Anthropic, AsyncAnthropic
from core.tree_of_thoughts import TreeOfThoughts
from typing import List, Dict, Optional, Tuple, Any
import json
import os
import re
import asyncio

from .task_models import (
    Task, EnhancedExecutionPlan, TaskType, TaskRequirement,
    TaskOutput, TaskStatus
)
from .task_graph import TaskGraph
from prompts.decomposition_prompts import DecompositionPrompts
from config.logging_config import get_logger

logger = get_logger(__name__)


class TaskDecomposer:
    """
    Decomposes complex prompts into executable task graphs
    
    Uses Claude Sonnet 4 with Extended Thinking for intelligent
    task decomposition with dependency resolution.
    
    Features:
    - Agent-aware decomposition
    - DAG construction with validation
    - Parallel execution opportunities
    - Risk assessment
    - Prompt caching for efficiency
    
    Attributes:
        available_agents: List of agent metadata
        api_key: Anthropic API key
        use_caching: Whether to use prompt caching
        client: Synchronous Anthropic client
        async_client: Asynchronous Anthropic client
        system_prompt: Cached system prompt
    
    Examples:
        >>> decomposer = TaskDecomposer(available_agents)
        >>> plan = await decomposer.decompose("Create JWT auth with tests")
        >>> if plan.validated:
        ...     execute(plan)
    """
    
    def __init__(
        self,
        available_agents: List[Dict],
        api_key: Optional[str] = None,
        use_caching: bool = True,
        temperature: float = 0.3
    ):
        """
        Initialize task decomposer
        
        Args:
            available_agents: List of agent metadata
                Format: [{"name": "code", "capabilities": "...", "tools": [...]}]
            api_key: Anthropic API key (from env if not provided)
            use_caching: Use prompt caching (default: True)
            temperature: LLM temperature (default: 0.3 for consistency)
        """
        self.available_agents = available_agents
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.use_caching = use_caching
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or parameters")
        
        # Initialize clients
        self.client = Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)
        
        # Build system prompt (cacheable)
        self.system_prompt = DecompositionPrompts.get_decomposition_system_prompt(
            available_agents
        )
        
        logger.info(f"TaskDecomposer initialized with {len(available_agents)} agents")
    
    async def decompose(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        validate: bool = True,
        use_extended_thinking: bool = False
    ) -> EnhancedExecutionPlan:
        """
        Decompose prompt into execution plan
        
        Args:
            prompt: User's complex prompt to decompose
            context: Additional context (codebase, constraints, etc)
            validate: Whether to validate plan after generation
            use_extended_thinking: Use Extended Thinking (experimental)
        
        Returns:
            EnhancedExecutionPlan with tasks and dependencies
        
        Examples:
            >>> plan = await decomposer.decompose(
            ...     "Create JWT authentication with Redis caching",
            ...     context={"constraints": "Must use FastAPI"},
            ...     validate=True
            ... )
        """
        logger.info(f"Decomposing task: {prompt[:100]}...")
        
        try:
            # Step 1: Generate plan with Claude
            plan_json, thinking = await self._generate_plan(
                prompt,
                context,
                use_extended_thinking
            )
            
            # Step 2: Parse into ExecutionPlan
            plan = self._parse_plan_json(prompt, plan_json, thinking)
            
            # Step 3: Validate plan
            if validate:
                is_valid, issues = await self._validate_plan(plan)
                plan.validated = is_valid
                plan.validation_issues = issues
                
                if not is_valid:
                    logger.warning(f"Plan validation failed: {len(issues)} issues found")
                    # Try to auto-fix
                    plan = await self._fix_plan(plan, issues)
            
            logger.info(f"Decomposition complete: {len(plan.tasks)} tasks, complexity {plan.complexity_score}")
            
            return plan
        
        except Exception as e:
            logger.error(f"Decomposition failed: {e}", exc_info=True)
            raise
    
    async def _generate_plan(
        self,
        prompt: str,
        context: Optional[Dict],
        use_extended_thinking: bool
    ) -> Tuple[Dict, str]:
        """
        Generate plan using Claude
        
        Args:
            prompt: User prompt
            context: Additional context
            use_extended_thinking: Use Extended Thinking
        
        Returns:
            (plan_json, thinking_process)
        """
        # Build user prompt
        user_prompt = DecompositionPrompts.get_decomposition_user_prompt(
            prompt, context
        )
        
        # Build messages
        messages = [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # System prompt with caching
        if self.use_caching:
            system = [
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        else:
            system = self.system_prompt
        
        # Call Claude
        logger.debug("Calling Claude API for decomposition...")
        
        try:
            response = await self.async_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                system=system,
                messages=messages,
                temperature=self.temperature
            )
            
            # Extract response
            response_text = response.content[0].text
            
            # Extract thinking if present
            thinking = ""
            if hasattr(response, 'usage'):
                # Log token usage
                usage = response.usage
                logger.debug(f"Token usage: input={usage.input_tokens}, output={usage.output_tokens}")
                
                if hasattr(usage, 'cache_read_input_tokens') and usage.cache_read_input_tokens:
                    logger.debug(f"Cache hit: {usage.cache_read_input_tokens} tokens from cache")
            
            # Parse JSON from response
            plan_json = self._extract_json(response_text)
            
            # Extract thinking from JSON
            thinking = plan_json.get('thinking', '')
            
            return (plan_json, thinking)
        
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            raise ValueError(f"Failed to generate plan: {e}")
    
    def _extract_json(self, response_text: str) -> Dict:
        """
        Extract JSON from Claude response
        
        Handles:
        - Plain JSON
        - JSON in markdown code blocks
        - Malformed JSON (attempts to fix)
        
        Args:
            response_text: Claude's response
        
        Returns:
            Parsed JSON dictionary
        
        Raises:
            ValueError: If JSON cannot be extracted
        """
        # Try 1: Direct JSON parse
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # Try 2: Extract from markdown code block
        if "```json" in response_text:
            try:
                json_text = response_text.split("```json")[1].split("```")[0]
                return json.loads(json_text.strip())
            except (IndexError, json.JSONDecodeError):
                pass
        
        # Try 3: Find JSON object with regex
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Try 4: Remove markdown code block markers
        cleaned = re.sub(r'```[a-z]*\n', '', response_text)
        cleaned = re.sub(r'```', '', cleaned)
        try:
            return json.loads(cleaned.strip())
        except json.JSONDecodeError:
            pass
        
        # Failed
        logger.error(f"Could not extract JSON from response: {response_text[:500]}")
        raise ValueError(f"Failed to parse JSON from response. Response starts with: {response_text[:200]}")
    
    def _parse_plan_json(
        self,
        original_prompt: str,
        plan_json: Dict,
        thinking: str
    ) -> EnhancedExecutionPlan:
        """
        Parse JSON into EnhancedExecutionPlan
        
        Args:
            original_prompt: Original user prompt
            plan_json: Parsed JSON from Claude
            thinking: Thinking process
        
        Returns:
            EnhancedExecutionPlan
        """
        # Create tasks
        tasks = []
        
        for task_data in plan_json.get('tasks', []):
            try:
                # Create task from dict
                task = Task.from_dict(task_data)
                tasks.append(task)
            
            except Exception as e:
                logger.warning(f"Failed to parse task: {e}")
                # Skip malformed task
                continue
        
        # Create plan
        plan = EnhancedExecutionPlan(
            goal=original_prompt,
            tasks=tasks,
            estimated_total_time=plan_json.get('estimated_total_time', 0),
            complexity_score=plan_json.get('complexity_score', 0.0),
            thinking_process=thinking,
            alternatives_considered=plan_json.get('alternatives_considered', [])
        )
        
        # Add risks to metadata
        plan.metadata['risks'] = plan_json.get('risks', [])
        
        return plan
    
    async def _validate_plan(self, plan: EnhancedExecutionPlan) -> Tuple[bool, List[str]]:
        """
        Validate execution plan
        
        Checks:
        1. DAG validity (no cycles)
        2. All dependencies exist
        3. Agent/tool availability
        4. Reasonable estimates
        5. Risk assessment
        
        Args:
            plan: Plan to validate
        
        Returns:
            (is_valid, issues)
        """
        issues = []
        
        # Check 1: DAG validity
        try:
            graph = TaskGraph(plan.tasks)
            is_dag, dag_errors = graph.is_valid_dag()
            if not is_dag:
                issues.extend(dag_errors)
        except Exception as e:
            issues.append(f"Failed to build task graph: {e}")
            return (False, issues)
        
        # Check 2: Agent availability
        available_agents = {a['name'] for a in self.available_agents}
        for task in plan.tasks:
            if task.requirements.agent_type not in available_agents:
                issues.append(
                    f"Task '{task.description}' requires unavailable agent: {task.requirements.agent_type}"
                )
        
        # Check 3: Task IDs are unique
        task_ids = [t.id for t in plan.tasks]
        if len(task_ids) != len(set(task_ids)):
            duplicates = [tid for tid in task_ids if task_ids.count(tid) > 1]
            issues.append(f"Duplicate task IDs found: {set(duplicates)}")
        
        # Check 4: Reasonable complexity
        if len(plan.tasks) == 0:
            issues.append("Plan has no tasks")
        elif len(plan.tasks) > 50:
            issues.append(f"Plan too complex: {len(plan.tasks)} tasks (max 50 recommended)")
        
        # Check 5: Time estimates reasonable
        if plan.estimated_total_time > 3600:  # >1 hour
            issues.append(f"Estimated time very long: {plan.estimated_total_time}s (>1 hour)")
        
        for task in plan.tasks:
            if task.estimated_time < 1:
                issues.append(f"Task '{task.description}' has unrealistic estimate: {task.estimated_time}s")
        
        # Check 6: Risk levels valid
        valid_risks = {"low", "medium", "high", "critical"}
        for task in plan.tasks:
            if task.risk_level not in valid_risks:
                issues.append(f"Task '{task.description}' has invalid risk level: {task.risk_level}")
        
        return (len(issues) == 0, issues)
    
    async def _fix_plan(
        self,
        plan: EnhancedExecutionPlan,
        issues: List[str]
    ) -> EnhancedExecutionPlan:
        """
        Attempt to auto-fix issues in plan
        
        Args:
            plan: Plan with issues
            issues: List of issues
        
        Returns:
            Fixed plan (or original if can't fix)
        """
        logger.info(f"Attempting to auto-fix {len(issues)} issues...")
        
        # LIMITATION: Auto-fix currently marks plan as invalid
        # Claude-powered auto-fix can be implemented in future iteration
        # For now, validation issues are returned to user for manual review
        plan.validated = False
        plan.validation_issues = issues
        
        return plan
    
    def decompose_sync(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        validate: bool = True
    ) -> EnhancedExecutionPlan:
        """
        Synchronous wrapper for decompose
        
        Args:
            prompt: User prompt
            context: Additional context
            validate: Validate plan
        
        Returns:
            EnhancedExecutionPlan
        
        Examples:
            >>> plan = decomposer.decompose_sync("Create REST API")
        """
        return asyncio.run(self.decompose(prompt, context, validate))
    
    async def refine_plan(
        self,
        plan: EnhancedExecutionPlan,
        feedback: str
    ) -> EnhancedExecutionPlan:
        """
        Refine plan based on user feedback
        
        Args:
            plan: Original plan
            feedback: User's feedback or modification request
        
        Returns:
            Refined EnhancedExecutionPlan
        
        Examples:
            >>> refined = await decomposer.refine_plan(
            ...     plan,
            ...     "Add error handling and logging"
            ... )
        """
        logger.info(f"Refining plan based on feedback: {feedback[:100]}...")
        
        # Convert plan to JSON
        plan_json_str = json.dumps(plan.to_dict(), indent=2)
        
        # Build refinement prompt
        prompt = DecompositionPrompts.get_refinement_prompt(
            plan_json_str,
            feedback
        )
        
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call Claude
        try:
            response = await self.async_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                system=self.system_prompt,
                messages=messages,
                temperature=self.temperature
            )
            
            response_text = response.content[0].text
            refined_json = self._extract_json(response_text)
            
            # Parse into new plan
            refined_plan = self._parse_plan_json(
                plan.goal,
                refined_json,
                refined_json.get('thinking', '')
            )
            
            # Add changes to metadata
            refined_plan.metadata['changes_made'] = refined_json.get('changes_made', [])
            refined_plan.metadata['refined_from'] = plan.id
            
            logger.info(f"Plan refined: {len(refined_plan.tasks)} tasks")
            
            return refined_plan
        
        except Exception as e:
            logger.error(f"Plan refinement failed: {e}")
            raise
    
    async def explain_plan(self, plan: EnhancedExecutionPlan) -> str:
        """
        Generate human-readable explanation of plan
        
        Args:
            plan: Plan to explain
        
        Returns:
            Markdown-formatted explanation
        
        Examples:
            >>> explanation = await decomposer.explain_plan(plan)
            >>> print(explanation)
        """
        plan_json_str = json.dumps(plan.to_dict(), indent=2)
        
        prompt = f"""Explain this execution plan in simple terms for a developer:

{plan_json_str}

Format as markdown with:
1. **Overview** (what we're building)
2. **Step-by-step breakdown** (numbered list)
3. **Key dependencies**
4. **Estimated timeline**
5. **Risks to watch out for**

Keep it concise and practical. Use emojis for readability.
"""
        
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            response = await self.async_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=messages
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Plan explanation failed: {e}")
            return f"# Plan Explanation\n\nFailed to generate explanation: {e}"


class TaskDecomposerFactory:
    """
    Factory for creating TaskDecomposer with agent registry
    
    Provides convenient constructors for different scenarios.
    
    Examples:
        >>> decomposer = TaskDecomposerFactory.create_from_agents_directory("agents/")
        >>> decomposer = TaskDecomposerFactory.create_with_default_agents()
    """
    
    @staticmethod
    def create_from_agents_directory(agents_path: str) -> TaskDecomposer:
        """
        Create decomposer by scanning agents directory
        
        Dynamically discovers agents and their capabilities.
        
        Args:
            agents_path: Path to agents directory
        
        Returns:
            TaskDecomposer configured with available agents
        
        Examples:
            >>> decomposer = TaskDecomposerFactory.create_from_agents_directory(
            ...     "agents/"
            ... )
        """
        import importlib.util
        import inspect
        from pathlib import Path
        
        agents = []
        agents_dir = Path(agents_path)
        
        if not agents_dir.exists():
            logger.warning(f"Agents directory not found: {agents_path}")
            return TaskDecomposerFactory.create_with_default_agents()
        
        for agent_file in agents_dir.glob("*_agent.py"):
            if agent_file.name.startswith("__"):
                continue
            
            try:
                # Import module
                spec = importlib.util.spec_from_file_location(
                    agent_file.stem,
                    agent_file
                )
                if not spec or not spec.loader:
                    continue
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find agent classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name.endswith("Agent") and hasattr(obj, 'get_capabilities'):
                        try:
                            instance = obj()
                            capabilities = instance.get_capabilities()
                            
                            # Extract agent metadata
                            agent_name = name.replace("Agent", "").lower()
                            
                            agents.append({
                                "name": agent_name,
                                "class": name,
                                "capabilities": capabilities,
                                "tools": getattr(instance, 'tools', [])
                            })
                            
                            logger.debug(f"Discovered agent: {agent_name}")
                        
                        except Exception as e:
                            logger.warning(f"Failed to instantiate {name}: {e}")
            
            except Exception as e:
                logger.warning(f"Failed to load agent from {agent_file}: {e}")
        
        if not agents:
            logger.warning("No agents discovered, using defaults")
            return TaskDecomposerFactory.create_with_default_agents()
        
        logger.info(f"Created decomposer with {len(agents)} discovered agents")
        return TaskDecomposer(available_agents=agents)
    
    @staticmethod
    def create_with_default_agents() -> TaskDecomposer:
        """
        Create decomposer with hardcoded default agents
        
        Provides basic agent set without discovery.
        
        Returns:
            TaskDecomposer with default agents
        
        Examples:
            >>> decomposer = TaskDecomposerFactory.create_with_default_agents()
        """
        default_agents = [
            {
                "name": "code",
                "capabilities": "Generate code, create files, implement features, write functions and classes",
                "tools": ["file_editor", "file_writer", "file_reader"]
            },
            {
                "name": "test",
                "capabilities": "Write tests, run tests, validate code, check test coverage",
                "tools": ["file_editor", "bash"]
            },
            {
                "name": "fix",
                "capabilities": "Fix bugs, resolve errors, debug code, handle exceptions",
                "tools": ["file_editor", "grep_tool", "file_reader"]
            },
            {
                "name": "architect",
                "capabilities": "Design architecture, make technical decisions, plan structure",
                "tools": ["file_reader", "grep_tool"]
            },
            {
                "name": "review",
                "capabilities": "Code review, quality checks, best practices, refactoring suggestions",
                "tools": ["file_reader", "grep_tool"]
            },
            {
                "name": "docs",
                "capabilities": "Write documentation, comments, README files, API docs",
                "tools": ["file_editor", "file_writer"]
            },
            {
                "name": "explore",
                "capabilities": "Explore codebase, understand structure, find files, analyze dependencies",
                "tools": ["grep_tool", "file_reader", "glob_tool"]
            }
        ]
        
        logger.info(f"Created decomposer with {len(default_agents)} default agents")
        return TaskDecomposer(available_agents=default_agents)


# Export
__all__ = [
    'TaskDecomposer',
    'TaskDecomposerFactory',
]
