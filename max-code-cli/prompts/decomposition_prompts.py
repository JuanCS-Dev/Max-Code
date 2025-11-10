"""
Prompt Templates for Task Decomposition

Provides system and user prompts for Claude-powered task decomposition.
Includes agent registry, decomposition guidelines, and validation prompts.

Biblical Foundation:
"Instrui o sábio, e ele se fará mais sábio" (Provérbios 9:9)

Architecture:
- System prompts with agent capabilities (cacheable)
- User prompts with task context
- Validation prompts for plan checking
- JSON schema enforcement

Soli Deo Gloria
"""

from typing import List, Dict, Any, Optional


class DecompositionPrompts:
    """
    Prompt templates for Claude-powered decomposition
    
    Provides formatted prompts for:
    - Task decomposition with agent awareness
    - Plan validation
    - Plan refinement
    
    Examples:
        >>> system = DecompositionPrompts.get_decomposition_system_prompt(agents)
        >>> user = DecompositionPrompts.get_decomposition_user_prompt(task)
        >>> response = await claude.create(system=system, messages=[user])
    """
    
    @staticmethod
    def get_decomposition_system_prompt(available_agents: List[Dict]) -> str:
        """
        System prompt for task decomposition
        
        This prompt is cacheable (use with cache_control in Anthropic API)
        for cost optimization.
        
        Args:
            available_agents: List of available agents with capabilities
                Format: [{"name": "code", "capabilities": "...", "tools": [...]}]
        
        Returns:
            System prompt string
        
        Examples:
            >>> agents = [
            ...     {"name": "code", "capabilities": "Generate code", "tools": ["file_editor"]},
            ...     {"name": "test", "capabilities": "Write tests", "tools": ["bash"]}
            ... ]
            >>> prompt = DecompositionPrompts.get_decomposition_system_prompt(agents)
        """
        # Build agent registry
        agent_list = []
        for agent in available_agents:
            name = agent.get('name', 'unknown')
            capabilities = agent.get('capabilities', 'No capabilities defined')
            tools = agent.get('tools', [])
            
            tools_str = ', '.join(tools) if tools else 'None'
            
            agent_list.append(f"""
**{name}**
- Capabilities: {capabilities}
- Tools: {tools_str}
""")
        
        agents_text = "\n".join(agent_list)
        
        return f"""You are an expert task decomposition system for MAXIMUS AI Code CLI.

Your job is to break down complex coding tasks into specific, executable subtasks with clear dependencies.

## Available Agents

{agents_text}

## Decomposition Principles

1. **Atomic Tasks**: Each task should be a single, clear action
   - One tool invocation per task (usually)
   - Clear input/output expectations
   - Measurable completion criteria

2. **Dependencies**: Identify which tasks must complete before others
   - File must be created before it can be modified
   - Dependencies must be installed before use
   - Tests run after code is written
   - Use task IDs for dependency tracking

3. **Parallelization**: Mark tasks that can run concurrently
   - Independent file creations can parallelize
   - Tests for different modules can run together
   - Consider resource constraints (file locks, etc)

4. **Tool Selection**: Choose the right agent/tool for each task
   - Match task type to agent capabilities
   - Consider tool prerequisites
   - Prefer specialized agents over general ones

5. **Context Flow**: Ensure outputs from one task feed into dependents
   - Define what context each task provides
   - Specify context dependencies explicitly
   - Enable data flow between tasks

6. **Risk Assessment**: Flag dangerous operations
   - Delete operations: HIGH risk
   - Overwriting critical files: HIGH risk
   - System commands: MEDIUM-HIGH risk
   - File modifications: MEDIUM risk
   - File reads: LOW risk

## Output Format

You MUST respond with valid JSON in this EXACT structure:

```json
{{
  "thinking": "Your analysis of the task and decomposition strategy. Explain your reasoning, why you chose this approach, what alternatives you considered, and potential risks.",
  
  "tasks": [
    {{
      "id": "task_1",
      "description": "Clear, actionable description of what to do",
      "type": "read|write|execute|validate|plan|think",
      "agent": "code|test|fix|architect|review|docs|explore",
      "tools": ["tool_name"],
      "inputs": {{"key": "value"}},
      "depends_on": ["task_id"],
      "estimated_time": 30,
      "risk_level": "low|medium|high|critical",
      "reasoning": "Why this task is needed and how it fits in the plan",
      "can_parallelize_with": ["task_2"]
    }}
  ],
  
  "complexity_score": 45,
  "estimated_total_time": 180,
  "risks": ["List of potential risks or challenges"],
  "alternatives_considered": ["Other decomposition approaches you considered"]
}}
```

## Field Specifications

**Task Fields:**
- `id`: Unique identifier (e.g., "task_1", "task_2")
- `description`: What to do (be specific and actionable)
- `type`: Task type from enum
- `agent`: Which agent should execute
- `tools`: Array of tools needed
- `inputs`: Parameters for execution (filepath, content, command, etc)
- `depends_on`: Array of task IDs that must complete first
- `estimated_time`: Time in seconds
- `risk_level`: Risk assessment (default: "low")
- `reasoning`: Justification for this task
- `can_parallelize_with`: Tasks that can run concurrently

**Plan Fields:**
- `thinking`: Your reasoning process (important!)
- `complexity_score`: 0-100 (higher = more complex)
- `estimated_total_time`: Total sequential time in seconds
- `risks`: Array of risks to watch for
- `alternatives_considered`: Other approaches you thought about

## Example 1: Simple Task

User: "Create a hello world function in Python"

Your output:
```json
{{
  "thinking": "Simple task requiring one file creation. No dependencies, low complexity. Could use code agent with file_writer tool.",
  
  "tasks": [
    {{
      "id": "task_1",
      "description": "Create hello.py with hello_world function",
      "type": "write",
      "agent": "code",
      "tools": ["file_writer"],
      "inputs": {{"filepath": "hello.py"}},
      "depends_on": [],
      "estimated_time": 30,
      "risk_level": "low",
      "reasoning": "Main deliverable - hello world function",
      "can_parallelize_with": []
    }}
  ],
  
  "complexity_score": 10,
  "estimated_total_time": 30,
  "risks": [],
  "alternatives_considered": ["Could add tests, but not requested"]
}}
```

## Example 2: Complex Task with Dependencies

User: "Create JWT authentication for FastAPI with Redis caching and comprehensive tests"

Your output:
```json
{{
  "thinking": "This requires multiple components: JWT utilities, FastAPI middleware, Redis integration, and tests. Key dependencies: utils before middleware, Redis install before integration, middleware before tests. Can parallelize JWT utils creation and Redis installation.",
  
  "tasks": [
    {{
      "id": "task_1",
      "description": "Create JWT utility functions (encode, decode, verify)",
      "type": "write",
      "agent": "code",
      "tools": ["file_editor"],
      "inputs": {{"filepath": "auth/jwt_utils.py"}},
      "depends_on": [],
      "estimated_time": 60,
      "risk_level": "low",
      "reasoning": "Foundation for authentication system",
      "can_parallelize_with": ["task_2"]
    }},
    {{
      "id": "task_2",
      "description": "Install required dependencies (pyjwt, redis, fastapi)",
      "type": "execute",
      "agent": "code",
      "tools": ["bash"],
      "inputs": {{"command": "pip install pyjwt redis fastapi"}},
      "depends_on": [],
      "estimated_time": 20,
      "risk_level": "low",
      "reasoning": "Need libraries installed before use",
      "can_parallelize_with": ["task_1"]
    }},
    {{
      "id": "task_3",
      "description": "Create FastAPI authentication middleware",
      "type": "write",
      "agent": "code",
      "tools": ["file_editor"],
      "inputs": {{"filepath": "auth/middleware.py"}},
      "depends_on": ["task_1", "task_2"],
      "estimated_time": 90,
      "risk_level": "medium",
      "reasoning": "Core authentication logic using JWT utils",
      "can_parallelize_with": []
    }},
    {{
      "id": "task_4",
      "description": "Create Redis caching layer for tokens",
      "type": "write",
      "agent": "code",
      "tools": ["file_editor"],
      "inputs": {{"filepath": "auth/redis_cache.py"}},
      "depends_on": ["task_2"],
      "estimated_time": 45,
      "risk_level": "medium",
      "reasoning": "Performance optimization for token validation",
      "can_parallelize_with": ["task_1"]
    }},
    {{
      "id": "task_5",
      "description": "Write comprehensive tests for auth system",
      "type": "write",
      "agent": "test",
      "tools": ["file_editor"],
      "inputs": {{"filepath": "tests/test_auth.py"}},
      "depends_on": ["task_3", "task_4"],
      "estimated_time": 120,
      "risk_level": "low",
      "reasoning": "Ensure correctness and security of authentication",
      "can_parallelize_with": []
    }},
    {{
      "id": "task_6",
      "description": "Run tests to validate implementation",
      "type": "validate",
      "agent": "test",
      "tools": ["bash"],
      "inputs": {{"command": "pytest tests/test_auth.py -v"}},
      "depends_on": ["task_5"],
      "estimated_time": 30,
      "risk_level": "low",
      "reasoning": "Validate everything works correctly",
      "can_parallelize_with": []
    }}
  ],
  
  "complexity_score": 70,
  "estimated_total_time": 365,
  "risks": [
    "Security vulnerabilities if JWT not implemented correctly",
    "Redis connection failures need handling",
    "Token expiration edge cases"
  ],
  "alternatives_considered": [
    "OAuth2 instead of JWT (more complex, not requested)",
    "In-memory caching instead of Redis (simpler, less scalable)"
  ]
}}
```

## Important Rules

1. **ONLY output valid JSON** - no markdown, no extra text
2. **Use exact field names** as specified
3. **Task IDs must be unique** and referenced correctly
4. **Dependencies must exist** - can't depend on non-existent tasks
5. **Think deeply** - the "thinking" field is crucial for quality
6. **Be realistic** - time estimates should be practical
7. **Consider failures** - what could go wrong?
8. **Respect agent capabilities** - don't assign tasks to wrong agents

## Error Handling

If the task is unclear or impossible:
- Still output valid JSON
- Set complexity_score very high (90+)
- Add detailed risks
- Suggest alternatives in alternatives_considered
- Be honest in thinking field
"""
    
    @staticmethod
    def get_decomposition_user_prompt(
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        User prompt for decomposition
        
        Args:
            task: The task to decompose
            context: Additional context (optional)
                - codebase: Information about existing code
                - constraints: Limitations or requirements
                - existing_files: Files that already exist
                - preferences: User preferences
        
        Returns:
            User prompt string
        
        Examples:
            >>> prompt = DecompositionPrompts.get_decomposition_user_prompt(
            ...     "Create REST API",
            ...     {"constraints": "Must use FastAPI", "existing_files": ["main.py"]}
            ... )
        """
        prompt_parts = [
            "Please decompose this task into executable subtasks:",
            "",
            f"**Task**: {task}",
            ""
        ]
        
        # Add context if provided
        if context:
            if 'codebase' in context:
                prompt_parts.extend([
                    "## Codebase Context",
                    context['codebase'],
                    ""
                ])
            
            if 'constraints' in context:
                prompt_parts.extend([
                    "## Constraints",
                    context['constraints'],
                    ""
                ])
            
            if 'existing_files' in context:
                files = context['existing_files']
                if isinstance(files, list):
                    files_str = '\n'.join(f"- {f}" for f in files)
                else:
                    files_str = str(files)
                
                prompt_parts.extend([
                    "## Existing Files",
                    files_str,
                    ""
                ])
            
            if 'preferences' in context:
                prompt_parts.extend([
                    "## User Preferences",
                    context['preferences'],
                    ""
                ])
        
        prompt_parts.extend([
            "Remember:",
            "- Output ONLY valid JSON (no markdown, no extra text)",
            "- Follow the exact schema from the system prompt",
            "- Think deeply about dependencies and parallelization",
            "- Be realistic with time estimates",
            "- Consider risks and alternatives"
        ])
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def get_validation_prompt(plan_json: str) -> str:
        """
        Prompt to validate a generated plan
        
        Args:
            plan_json: JSON string of the plan to validate
        
        Returns:
            Validation prompt
        
        Examples:
            >>> validation = DecompositionPrompts.get_validation_prompt(plan)
            >>> response = await claude.create(messages=[validation])
        """
        return f"""Review this execution plan and identify any issues:

{plan_json}

Check for:

1. **Missing Dependencies**
   - Tasks that should depend on others but don't
   - File modifications without file creation dependency
   - Tool usage without installation dependency

2. **Circular Dependencies**
   - Task A depends on B, B depends on A (directly or indirectly)
   - Any cycles in the dependency graph

3. **Incorrect Agent/Tool Selection**
   - Wrong agent for task type
   - Non-existent tools
   - Agent capabilities don't match task requirements

4. **Unrealistic Time Estimates**
   - Too short (<5s for file creation)
   - Too long (>600s - should break down)
   - Total time seems off

5. **Missing Risk Assessment**
   - Delete operations not marked HIGH
   - System commands not assessed properly
   - Critical files not identified

6. **Tasks That Could Parallelize**
   - Independent tasks not marked for parallelization
   - Missed optimization opportunities

7. **Redundant or Unnecessary Tasks**
   - Duplicate work
   - Tasks that don't contribute to goal

8. **Missing Reasoning**
   - Tasks without clear justification
   - Unclear dependency rationale

Respond with JSON:
```json
{{
  "valid": true/false,
  "score": 0-100,
  "issues": [
    {{
      "severity": "critical|high|medium|low",
      "category": "dependencies|agents|timing|risks|optimization|redundancy",
      "description": "Clear description of the issue",
      "affected_tasks": ["task_1", "task_2"],
      "suggestion": "How to fix it"
    }}
  ],
  "strengths": ["What's good about this plan"],
  "optimization_suggestions": ["How to improve"],
  "corrected_plan": {{...}}  // Only if issues are critical
}}
```

Be thorough but fair. Focus on correctness and optimization.
"""
    
    @staticmethod
    def get_refinement_prompt(
        original_plan: str,
        feedback: str
    ) -> str:
        """
        Prompt to refine a plan based on feedback
        
        Args:
            original_plan: JSON string of original plan
            feedback: User's feedback or modification request
        
        Returns:
            Refinement prompt
        
        Examples:
            >>> prompt = DecompositionPrompts.get_refinement_prompt(
            ...     plan_json,
            ...     "Add error handling and logging"
            ... )
        """
        return f"""Here is an execution plan:

{original_plan}

User feedback: {feedback}

Please refine the plan based on this feedback:

1. **Understand the feedback**
   - What is the user asking for?
   - What should be added/removed/modified?

2. **Update the plan**
   - Add new tasks if needed
   - Modify existing tasks
   - Update dependencies
   - Adjust time estimates

3. **Maintain consistency**
   - Keep existing task IDs where possible
   - Preserve dependencies that still make sense
   - Update complexity score if needed

4. **Explain changes**
   - Note what you changed in "thinking"
   - Explain why changes were made

Output the complete refined plan in the same JSON format.
Include a "changes_made" field summarizing modifications:

```json
{{
  "thinking": "...",
  "tasks": [...],
  "complexity_score": ...,
  "estimated_total_time": ...,
  "risks": [...],
  "alternatives_considered": [...],
  "changes_made": [
    "Added error handling tasks",
    "Increased time estimates for task_3",
    "Added logging dependency"
  ]
}}
```
"""


# Export
__all__ = ['DecompositionPrompts']
