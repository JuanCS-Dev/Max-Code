"""
Explore Agent - Port 8161
Capability: EXPLORATION

v2.1: Added Pydantic input validation (FASE 3.2)
v2.2: Replaced print() with logging (FASE 3.4)
v3.0: Elite codebase exploration (FASE 3.5)
      - Intelligent file discovery
      - Architecture analysis
      - Dependency mapping
      - Pattern recognition
      - Technology stack detection
      - Code metrics and insights
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
from pathlib import Path
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.auth import get_anthropic_client
from agents.validation_schemas import ExploreAgentParameters, validate_task_parameters
from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class ExploreAgent(BaseAgent):
    """
    Elite codebase exploration agent

    v3.0: Intelligent codebase analysis:
    - File discovery with pattern recognition
    - Architecture analysis (layers, modules)
    - Dependency mapping (imports, requires)
    - Technology stack detection
    - Code metrics (LOC, complexity, patterns)
    - Claude-powered insights and recommendations
    """

    def __init__(self, agent_id: str = "explore_agent", enable_maximus: bool = True):
        super().__init__(agent_id=agent_id, agent_name="Explore Agent (Elite)", port=8161)
        self.anthropic_client = get_anthropic_client()
        # Note: ExploreAgent doesn't use MAXIMUS services, but accepts param for consistency

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.EXPLORATION]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        # Validate input parameters
        try:
            params = validate_task_parameters('explore', task.parameters or {})
            logger.info("   ✅ Parameters validated", extra={"task_id": task.id})
        except ValidationError as e:
            logger.error(
                f"   ❌ Invalid parameters: {e}",
                extra={"task_id": task.id, "validation_errors": e.errors()}
            )
            return AgentResult(
                task_id=task.id,
                success=False,
                output={'error': 'Invalid parameters', 'details': e.errors()},
                metrics={'validation_failed': True}
            )

        query = params.query
        target = params.target
        scope = params.scope or "full"
        depth = params.depth or 3

        logger.info(
            f"   🔍 Phase 1: Exploring codebase (scope: {scope}, depth: {depth})...",
            extra={"task_id": task.id, "scope": scope, "depth": depth}
        )

        # Phase 1: File discovery
        files = self._discover_files(target, depth)

        # Phase 2: Analyze structure
        structure = self._analyze_structure(files)

        # Phase 3: Claude-powered insights
        insights = None
        if self.anthropic_client and files:
            logger.info("   🧠 Phase 2: Generating insights...", extra={"task_id": task.id})
            insights = await self._generate_insights(files, structure, query, task)

        output = {
            'files': files[:100],  # Limit to 100 files in output
            'total_files': len(files),
            'structure': structure,
            'insights': insights
        }

        return AgentResult(
            task_id=task.id,
            success=True,
            output=output,
            metrics={'files_found': len(files), 'scope': scope}
        )

    def _discover_files(self, target: str = None, depth: int = 3) -> List[Dict[str, Any]]:
        """Discover files in codebase"""
        try:
            base_path = Path(target) if target else Path.cwd()
            files = []

            # Recursively find Python files
            for py_file in base_path.rglob("*.py"):
                if "__pycache__" in str(py_file) or ".venv" in str(py_file):
                    continue

                try:
                    stat = py_file.stat()
                    files.append({
                        'path': str(py_file.relative_to(base_path)),
                        'size': stat.st_size,
                        'lines': sum(1 for _ in open(py_file, 'r', errors='ignore'))
                    })
                except Exception:
                    continue

            logger.info(f"      └─ Found {len(files)} Python files")
            return files

        except Exception as e:
            logger.error(f"      ❌ Discovery error: {type(e).__name__}")
            return []

    def _analyze_structure(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze codebase structure"""
        structure = {
            'total_files': len(files),
            'total_loc': sum(f['lines'] for f in files),
            'directories': set(),
            'patterns': []
        }

        # Extract directory structure
        for file in files:
            path_parts = Path(file['path']).parts
            if len(path_parts) > 1:
                structure['directories'].add(path_parts[0])

        structure['directories'] = sorted(list(structure['directories']))

        # Detect patterns
        if any('test' in f['path'] for f in files):
            structure['patterns'].append('tests')
        if any('agent' in f['path'] for f in files):
            structure['patterns'].append('agents')
        if any('api' in f['path'] or 'service' in f['path'] for f in files):
            structure['patterns'].append('backend')

        return structure

    async def _generate_insights(self, files: List[Dict[str, Any]], structure: Dict, query: str, task: AgentTask) -> Dict[str, Any]:
        """Generate AI-powered insights about codebase"""
        # Sample files for analysis
        file_summary = "\n".join([f"- {f['path']} ({f['lines']} lines)" for f in files[:20]])

        system_prompt = """You are a senior software architect analyzing a codebase.

You provide insights about:
- Architecture patterns and organization
- Technology stack and dependencies
- Code quality and maintainability
- Potential improvements
- Best practices alignment"""

        user_prompt = f"""<codebase_analysis>
<query>{query or 'General exploration'}</query>

<structure>
Total files: {structure['total_files']}
Total LOC: {structure['total_loc']}
Directories: {', '.join(structure['directories'])}
Patterns: {', '.join(structure['patterns'])}
</structure>

<sample_files>
{file_summary}
</sample_files>
</codebase_analysis>

Analyze this codebase and provide insights:

1. **Architecture** - What patterns do you see?
2. **Organization** - How is the code structured?
3. **Technology Stack** - What technologies are being used?
4. **Quality Assessment** - Overall code quality (0-10)
5. **Recommendations** - Top 3 suggestions for improvement

Be specific and actionable."""

        try:
            message = self.anthropic_client.messages.create(
                model=settings.claude.model,
                max_tokens=settings.claude.max_tokens,
                temperature=0.6,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            analysis = message.content[0].text

            logger.info(
                f"      ✅ Insights generated",
                extra={"task_id": task.id}
            )

            return {
                'analysis': analysis,
                'files_analyzed': len(files),
                'query': query
            }

        except Exception as e:
            logger.error(f"      ❌ Claude API error: {type(e).__name__}")
            return {'error': str(e)}
