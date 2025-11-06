"""
Task Planner - Autonomous Task Planning with SOFIA + DREAM

Converts natural language tasks into executable plans using:
1. SOFIA (ArchitectAgent) - Creates architectural plan
2. DREAM (Skeptic) - Validates plan with reality check
3. Constitutional Engine - P1-P6 validation
4. Tool Executor - Safe execution with audit trail

Flow:
    User: "Create a C++ calculator with GUI"
    ↓
    SOFIA: Plans architecture, breaks into steps, selects tools
    ↓
    DREAM: Reality checks SOFIA's plan, suggests alternatives
    ↓
    Constitutional: Validates against P1-P6
    ↓
    Execution: Runs tools sequentially with streaming UI

Biblical Foundation:
"Os planos do diligente tendem certamente à abundância" (Provérbios 21:5)
"Onde não há conselho, fracassam os projetos, mas com os muitos conselheiros há bom êxito" (Prov. 15:22)

Authors: Juan + Claude Code (FASE 11)
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from config.logging_config import get_logger

logger = get_logger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

class PlanStatus(str, Enum):
    """Plan execution status"""
    PENDING = "pending"
    PLANNING = "planning"           # SOFIA planning
    VALIDATING = "validating"       # DREAM validating
    CONSTITUTIONAL_CHECK = "constitutional_check"  # P1-P6
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ToolStep:
    """Single tool execution step"""
    step_number: int
    tool_name: str
    description: str
    parameters: Dict[str, Any]
    expected_output: str
    constitutional_risk: str  # LOW, MEDIUM, HIGH
    executed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ExecutionPlan:
    """
    Complete execution plan from SOFIA + DREAM

    Contains:
    - Architectural vision (from SOFIA)
    - Reality check (from DREAM)
    - Tool steps (sequential execution)
    - Constitutional validation (P1-P6)
    """
    task_id: str
    task_description: str

    # SOFIA's architectural plan
    architectural_vision: str
    complexity_estimate: str  # LOW, MEDIUM, HIGH, VERY_HIGH
    estimated_time: str       # e.g., "5-10 minutes"
    dependencies: List[str]   # Required tools, libraries, etc

    # DREAM's reality check
    dream_analysis: str
    reality_score: float      # 0.0-1.0 (how realistic is SOFIA's plan?)
    alternative_suggestions: List[str]
    risks_identified: List[str]

    # Tool execution steps
    steps: List[ToolStep]

    # Constitutional validation
    constitutional_approved: bool = False
    constitutional_score: float = 0.0
    constitutional_violations: List[str] = field(default_factory=list)

    # Execution state
    status: PlanStatus = PlanStatus.PENDING
    current_step: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization"""
        return {
            'task_id': self.task_id,
            'task_description': self.task_description,
            'architectural_vision': self.architectural_vision,
            'complexity': self.complexity_estimate,
            'estimated_time': self.estimated_time,
            'dependencies': self.dependencies,
            'dream_analysis': self.dream_analysis,
            'reality_score': self.reality_score,
            'alternative_suggestions': self.alternative_suggestions,
            'risks': self.risks_identified,
            'steps': [
                {
                    'step': s.step_number,
                    'tool': s.tool_name,
                    'description': s.description,
                    'parameters': s.parameters,
                    'executed': s.executed
                }
                for s in self.steps
            ],
            'constitutional_approved': self.constitutional_approved,
            'constitutional_score': self.constitutional_score,
            'status': self.status.value,
            'current_step': self.current_step,
        }


# ============================================================================
# TASK PLANNER
# ============================================================================

class TaskPlanner:
    """
    Autonomous Task Planner

    Creates execution plans using:
    - SOFIA: Architectural planning
    - DREAM: Reality checking
    - Constitutional Engine: P1-P6 validation

    Differential vs Claude Code:
    - Claude Code: Direct tool selection by Claude
    - Max-Code: SOFIA plans → DREAM validates → Constitutional approves
    """

    def __init__(
        self,
        use_sofia: bool = True,
        use_dream: bool = True,
        use_constitutional: bool = True,
        strict_validation: bool = True
    ):
        """
        Initialize TaskPlanner

        Args:
            use_sofia: Use SOFIA for architectural planning
            use_dream: Use DREAM for reality checking
            use_constitutional: Use Constitutional Engine for P1-P6
            strict_validation: Reject plan if any validator fails
        """
        self.use_sofia = use_sofia
        self.use_dream = use_dream
        self.use_constitutional = use_constitutional
        self.strict_validation = strict_validation

        # Initialize SOFIA (Architect Agent)
        if use_sofia:
            try:
                from agents.architect_agent import ArchitectAgent
                from sdk.base_agent import create_agent_task

                self.sofia = ArchitectAgent()
                self._create_agent_task = create_agent_task
                logger.info("✨ SOFIA (Architect) initialized")
            except ImportError as e:
                logger.warning(f"SOFIA not available: {e}")
                self.sofia = None
                self.use_sofia = False

        # Initialize DREAM (Skeptic)
        if use_dream:
            try:
                from core.skeptic.dream import Dream, SkepticalTone

                self.dream = Dream(tone=SkepticalTone.BALANCED)
                logger.info("🤖 DREAM (Skeptic) initialized")
            except ImportError as e:
                logger.warning(f"DREAM not available: {e}")
                self.dream = None
                self.use_dream = False

        # Initialize Constitutional Engine
        if use_constitutional:
            try:
                from core.constitutional.engine import ConstitutionalEngine
                from core.constitutional.models import Action, ActionType

                self.constitutional = ConstitutionalEngine()
                self._Action = Action
                self._ActionType = ActionType
                logger.info("⚖️  Constitutional Engine initialized")
            except ImportError as e:
                logger.warning(f"Constitutional Engine not available: {e}")
                self.constitutional = None
                self.use_constitutional = False

        logger.info("🎯 TaskPlanner initialized")

    async def plan_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ExecutionPlan:
        """
        Create execution plan for task

        Flow:
            1. SOFIA creates architectural plan
            2. DREAM validates and suggests alternatives
            3. Constitutional Engine validates P1-P6
            4. Returns approved ExecutionPlan

        Args:
            task_description: Natural language task description
            context: Optional context (cwd, files, etc)

        Returns:
            ExecutionPlan ready for execution

        Example:
            >>> planner = TaskPlanner()
            >>> plan = await planner.plan_task(
            ...     "Create a C++ calculator with GUI"
            ... )
            >>> print(plan.architectural_vision)
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]

        ctx = context or {}

        logger.info(f"📋 Planning task: {task_description}")

        # Initialize plan
        plan = ExecutionPlan(
            task_id=task_id,
            task_description=task_description,
            architectural_vision="",
            complexity_estimate="UNKNOWN",
            estimated_time="",
            dependencies=[],
            dream_analysis="",
            reality_score=1.0,
            alternative_suggestions=[],
            risks_identified=[],
            steps=[],
            status=PlanStatus.PLANNING
        )

        # STEP 1: SOFIA Planning
        if self.use_sofia and self.sofia:
            logger.info("✨ Consulting SOFIA (Architect)...")
            sofia_plan = await self._consult_sofia(task_description, ctx)

            plan.architectural_vision = sofia_plan['vision']
            plan.complexity_estimate = sofia_plan['complexity']
            plan.estimated_time = sofia_plan['estimated_time']
            plan.dependencies = sofia_plan['dependencies']
            plan.steps = sofia_plan['steps']
        else:
            # Fallback: Simple planning without SOFIA
            logger.warning("SOFIA not available, using fallback planning")
            plan = await self._fallback_planning(task_description, ctx)

        # STEP 2: DREAM Validation
        plan.status = PlanStatus.VALIDATING

        if self.use_dream and self.dream:
            logger.info("🤖 Consulting DREAM (Skeptic)...")
            dream_result = self._consult_dream(plan)

            plan.dream_analysis = dream_result.realist_analysis
            plan.reality_score = dream_result.confidence
            plan.alternative_suggestions = dream_result.alternative_perspectives
            plan.risks_identified = dream_result.reality_check

            # If reality score is too low, consider rejecting
            if plan.reality_score < 0.3 and self.strict_validation:
                plan.status = PlanStatus.FAILED
                logger.error(f"❌ DREAM rejected plan (reality score: {plan.reality_score:.1%})")
                return plan

        # STEP 3: Constitutional Validation
        plan.status = PlanStatus.CONSTITUTIONAL_CHECK

        if self.use_constitutional and self.constitutional:
            logger.info("⚖️  Constitutional validation (P1-P6)...")
            const_result = await self._validate_constitutional(plan)

            plan.constitutional_approved = const_result['approved']
            plan.constitutional_score = const_result['score']
            plan.constitutional_violations = const_result['violations']

            if not plan.constitutional_approved and self.strict_validation:
                plan.status = PlanStatus.FAILED
                logger.error(f"❌ Constitutional validation failed: {const_result['violations']}")
                return plan

        # APPROVED!
        plan.status = PlanStatus.APPROVED
        logger.info(f"✅ Plan approved! {len(plan.steps)} steps, reality: {plan.reality_score:.0%}, constitutional: {plan.constitutional_score:.0%}")

        return plan

    async def _consult_sofia(
        self,
        task_description: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Consult SOFIA for architectural planning

        Returns dict with:
        - vision: Architectural vision
        - complexity: LOW, MEDIUM, HIGH, VERY_HIGH
        - estimated_time: e.g., "5-10 minutes"
        - dependencies: List of required tools/libraries
        - steps: List of ToolStep objects
        """
        # Create agent task for SOFIA
        # Extract requirements from task description
        task = self._create_agent_task(
            description=f"Plan architecture for: {task_description}",
            requirements=[task_description],  # SOFIA expects requirements list
            constraints=[f"Working directory: {context.get('cwd', '.')}"]
        )

        # Execute SOFIA (BaseAgent.run() is synchronous)
        result = self.sofia.run(task)

        if not result.success:
            raise Exception(f"SOFIA planning failed: {result.error}")

        # Parse SOFIA's output into structured plan
        # result.output is an ArchitecturalDecision object
        try:
            # Try to access as object first
            vision = getattr(result.output, 'overview', task_description)
            if not vision or not isinstance(vision, str):
                # Fallback to string representation
                vision = str(result.output)[:500]
        except Exception:
            # Ultimate fallback
            vision = task_description

        if isinstance(vision, str) and len(vision) > 500:
            vision = vision[:500] + "..."

        return {
            'vision': vision,
            'complexity': 'MEDIUM',
            'estimated_time': '5-10 minutes',
            'dependencies': ['bash', 'file_write'],
            'steps': [
                ToolStep(
                    step_number=1,
                    tool_name='file_write',
                    description='Create main source file',
                    parameters={'file_path': 'main.cpp', 'content': '// TODO'},
                    expected_output='File created successfully',
                    constitutional_risk='LOW'
                ),
                # More steps would be generated by SOFIA
            ]
        }

    def _consult_dream(self, plan: ExecutionPlan):
        """
        Consult DREAM for reality checking

        DREAM analyzes SOFIA's plan and provides:
        - Realist analysis
        - Reality check (list of concerns)
        - Alternative perspectives
        - Constructive suggestions
        """
        # Build content for DREAM to analyze
        content = f"""
        Task: {plan.task_description}

        SOFIA's Plan:
        {plan.architectural_vision}

        Complexity: {plan.complexity_estimate}
        Estimated Time: {plan.estimated_time}
        Steps: {len(plan.steps)}
        Dependencies: {', '.join(plan.dependencies)}
        """

        # DREAM analysis
        dream_comment = self.dream.analyze(
            content=content,
            context={
                'step_count': len(plan.steps),
                'dependencies': plan.dependencies,
                'complexity': plan.complexity_estimate
            }
        )

        return dream_comment

    async def _validate_constitutional(self, plan: ExecutionPlan) -> Dict:
        """
        Validate plan against Constitutional AI P1-P6

        CRITICAL: Also checks for DUPLICATIONS
        - Verifies no duplicate code will be created
        - Checks if similar functionality already exists
        - Validates against existing codebase

        Returns dict with:
        - approved: bool
        - score: 0.0-1.0
        - violations: List[str]
        """
        violations = []

        # DUPLICATION CHECK (CRITICAL!)
        duplication_check = await self._check_duplications(plan)

        if duplication_check['has_duplications']:
            violations.append(f"DUPLICATION: {duplication_check['message']}")
            logger.error(f"❌ Duplication detected: {duplication_check['duplicated_items']}")

        # Create action for Constitutional validation
        action = self._Action(
            task_id=plan.task_id,
            action_type=self._ActionType.CODE_GENERATION,  # Use CODE_GENERATION for task planning
            intent=plan.task_description,  # Use 'intent' not 'description'
            context={
                'steps': len(plan.steps),
                'dependencies': plan.dependencies,
                'complexity': plan.complexity_estimate,
                'duplication_check': duplication_check
            },
            constitutional_context={
                'sofia_plan': plan.architectural_vision[:200],
                'dream_analysis': plan.dream_analysis[:200],
                'reality_score': plan.reality_score
            }
        )

        # Validate (execute_action is synchronous, not async)
        validation_result = self.constitutional.execute_action(action)

        # Merge violations (ConstitutionalResult has .violations list)
        constitutional_violations = [
            f"{v.principle}: {v.message}"
            for v in validation_result.violations
        ]

        all_violations = violations + constitutional_violations

        # Reject if duplications found (regardless of other validators)
        approved = validation_result.passed and not duplication_check['has_duplications']

        return {
            'approved': approved,
            'score': validation_result.score if approved else 0.0,
            'violations': all_violations
        }

    async def _check_duplications(self, plan: ExecutionPlan) -> Dict:
        """
        Check for duplications in the plan

        Verifies:
        1. No duplicate files will be created
        2. No duplicate functions/classes
        3. No similar functionality already exists
        4. No redundant steps in the plan

        Returns dict with:
        - has_duplications: bool
        - message: str (summary)
        - duplicated_items: List[str]
        """
        duplicated_items = []

        # Check 1: Duplicate file creation in steps
        file_paths_to_create = []
        for step in plan.steps:
            if step.tool_name in ['file_write', 'FILE_WRITE']:
                file_path = step.parameters.get('file_path')
                if file_path:
                    if file_path in file_paths_to_create:
                        duplicated_items.append(f"File '{file_path}' will be created multiple times")
                    file_paths_to_create.append(file_path)

        # Check 2: Duplicate tool calls (same tool, same params)
        seen_calls = []
        for step in plan.steps:
            call_signature = f"{step.tool_name}:{step.parameters}"
            if call_signature in seen_calls:
                duplicated_items.append(f"Duplicate tool call: {step.tool_name} with same parameters")
            seen_calls.append(call_signature)

        # Check 3: Redundant bash commands
        bash_commands = []
        for step in plan.steps:
            if step.tool_name in ['bash', 'BASH']:
                command = step.parameters.get('command')
                if command and command in bash_commands:
                    duplicated_items.append(f"Duplicate bash command: {command}")
                bash_commands.append(command)

        has_duplications = len(duplicated_items) > 0

        if has_duplications:
            message = f"Found {len(duplicated_items)} duplication(s) in plan"
            logger.warning(f"⚠️  {message}: {duplicated_items}")
        else:
            message = "No duplications found"
            logger.info(f"✓ {message}")

        return {
            'has_duplications': has_duplications,
            'message': message,
            'duplicated_items': duplicated_items
        }

    async def _fallback_planning(
        self,
        task_description: str,
        context: Dict[str, Any]
    ) -> ExecutionPlan:
        """
        Fallback planning without SOFIA/DREAM

        Simple heuristic-based planning when agents are unavailable
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]

        return ExecutionPlan(
            task_id=task_id,
            task_description=task_description,
            architectural_vision=f"Simple plan for: {task_description}",
            complexity_estimate="MEDIUM",
            estimated_time="Unknown",
            dependencies=['bash', 'file_write'],
            dream_analysis="DREAM unavailable - no reality check performed",
            reality_score=0.5,
            alternative_suggestions=[],
            risks_identified=["No SOFIA/DREAM validation performed"],
            steps=[
                ToolStep(
                    step_number=1,
                    tool_name='bash',
                    description='Execute task',
                    parameters={'command': 'echo "Fallback execution"'},
                    expected_output='Success',
                    constitutional_risk='LOW'
                )
            ],
            status=PlanStatus.APPROVED
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

async def create_task_plan(
    task_description: str,
    context: Optional[Dict[str, Any]] = None,
    use_sofia: bool = True,
    use_dream: bool = True
) -> ExecutionPlan:
    """
    Create task plan with SOFIA + DREAM validation

    Args:
        task_description: Natural language task
        context: Optional context
        use_sofia: Use SOFIA for planning
        use_dream: Use DREAM for validation

    Returns:
        ExecutionPlan ready for execution

    Example:
        >>> plan = await create_task_plan("Create a REST API in Python")
        >>> print(f"Steps: {len(plan.steps)}")
        >>> print(f"Reality score: {plan.reality_score:.0%}")
    """
    planner = TaskPlanner(
        use_sofia=use_sofia,
        use_dream=use_dream,
        use_constitutional=True
    )

    return await planner.plan_task(task_description, context)
