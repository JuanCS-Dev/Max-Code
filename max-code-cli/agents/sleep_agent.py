"""
Sleep Agent - End-of-Day Workflow
Port: 8170
Capability: SESSION_MANAGEMENT

Specialized agent for /dormir command that handles complete end-of-day workflow:
- Save project snapshot (state preservation)
- Create status file (current work state)
- Git commit (save changes)
- Git push (backup to remote)
- Cleanup activities
- Enable exact resumption the next day

v2.1: Added Pydantic input validation (FASE 3.2)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
import asyncio
import json
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError
from sdk.base_agent import BaseAgent, AgentCapability, AgentTask, AgentResult
from core.maximus_integration import MaximusClient
from agents.validation_schemas import SleepAgentParameters, validate_task_parameters


class SleepAgent(BaseAgent):
    """End-of-day workflow automation with state preservation"""

    def __init__(self, agent_id: str = "sleep_agent", enable_maximus: bool = True):
        super().__init__(
            agent_id=agent_id,
            agent_name="Sleep Agent (State Preservation)",
            port=8170
        )
        self.maximus_client = MaximusClient() if enable_maximus else None
        self.snapshot_dir = Path("./.snapshots")
        self.snapshot_dir.mkdir(exist_ok=True)

    def get_capabilities(self) -> List[AgentCapability]:
        return [AgentCapability.PLANNING, AgentCapability.CODE_GENERATION]

    def execute(self, task: AgentTask) -> AgentResult:
        return asyncio.run(self._execute_async(task))

    async def _execute_async(self, task: AgentTask) -> AgentResult:
        """Execute end-of-day workflow"""
        # Validate input parameters
        try:
            params = validate_task_parameters('sleep', task.parameters or {})
            print(f"   ✅ Parameters validated")
        except ValidationError as e:
            print(f"   ❌ Invalid parameters: {e}")
            return AgentResult(
                task_id=task.id,
                success=False,
                output={'error': 'Invalid parameters', 'details': e.errors()},
                metrics={'validation_failed': True}
            )

        print(f"   😴 Starting end-of-day workflow...")

        workflow_results = {}

        # Phase 1: Create snapshot
        print(f"   📸 Phase 1: Creating project snapshot...")
        snapshot_data = await self._create_snapshot(task)
        workflow_results['snapshot'] = snapshot_data

        # Phase 2: Create status file
        print(f"   📋 Phase 2: Creating status file...")
        status_file = await self._create_status_file(task, snapshot_data)
        workflow_results['status_file'] = status_file

        # Phase 3: Git operations
        print(f"   🔄 Phase 3: Git commit and push...")
        git_result = await self._git_operations(snapshot_data)
        workflow_results['git'] = git_result

        # Phase 4: Cleanup
        print(f"   🧹 Phase 4: Cleanup operations...")
        cleanup_result = await self._cleanup_operations()
        workflow_results['cleanup'] = cleanup_result

        # Phase 5: MAXIMUS integration (optional)
        if self.maximus_client:
            try:
                if await self.maximus_client.health_check():
                    print(f"   🤖 Phase 5: MAXIMUS session summary...")
                    summary = await self._maximus_summary(snapshot_data)
                    workflow_results['maximus_summary'] = summary
            except (ConnectionError, TimeoutError, AttributeError, Exception):
                print(f"      ⚠️ MAXIMUS offline - skipping summary")

        # Generate final report
        report = self._generate_report(workflow_results)

        print(f"\n   ✅ End-of-day workflow completed!")
        print(f"   📊 Summary: {report['summary']}")

        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                'workflow_results': workflow_results,
                'report': report,
                'timestamp': datetime.now().isoformat()
            },
            metrics={
                'mode': 'hybrid' if self.maximus_client else 'standalone',
                'phases_completed': len(workflow_results)
            }
        )

    async def _create_snapshot(self, task: AgentTask) -> Dict[str, Any]:
        """Create comprehensive project snapshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_file = self.snapshot_dir / f"snapshot_{timestamp}.json"

        snapshot_data = {
            'timestamp': timestamp,
            'task_context': {
                'description': task.description,
                'parameters': task.parameters,
                'task_id': task.id
            },
            'project_state': await self._collect_project_state(),
            'test_results': await self._collect_test_results(),
            'coverage_metrics': await self._collect_coverage_metrics()
        }

        # Save snapshot
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot_data, f, indent=2)

        return {
            'file': str(snapshot_file),
            'timestamp': timestamp,
            'size': snapshot_file.stat().st_size
        }

    async def _collect_project_state(self) -> Dict[str, Any]:
        """Collect current project state"""
        import subprocess

        state = {
            'git_branch': 'unknown',
            'git_status': 'unknown',
            'modified_files': [],
            'untracked_files': []
        }

        try:
            # Get git branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                state['git_branch'] = result.stdout.strip()

            # Get git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line:
                        status_code = line[:2]
                        filename = line[3:]
                        if status_code.strip() in ['M', 'MM']:
                            state['modified_files'].append(filename)
                        elif status_code.strip() == '??':
                            state['untracked_files'].append(filename)
        except (subprocess.SubprocessError, subprocess.TimeoutExpired, OSError):
            pass

        return state

    async def _collect_test_results(self) -> Dict[str, Any]:
        """Collect latest test results"""
        coverage_file = Path('./.coverage')

        results = {
            'coverage_exists': coverage_file.exists(),
            'last_modified': None
        }

        if coverage_file.exists():
            results['last_modified'] = datetime.fromtimestamp(
                coverage_file.stat().st_mtime
            ).isoformat()

        return results

    async def _collect_coverage_metrics(self) -> Dict[str, Any]:
        """Collect code coverage metrics"""
        import subprocess

        metrics = {
            'total_coverage': 'unknown',
            'statement_coverage': 'unknown'
        }

        try:
            result = subprocess.run(
                ['pytest', '--cov', '--cov-report=term-missing', '--co', '-q'],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Parse coverage from output (simplified)
            metrics['test_collection'] = 'success' if result.returncode == 0 else 'failed'
        except (subprocess.SubprocessError, subprocess.TimeoutExpired, OSError, FileNotFoundError):
            pass

        return metrics

    async def _create_status_file(
        self,
        task: AgentTask,
        snapshot_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Create comprehensive status file for next day resumption"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_file = Path("./STATUS.md")

        content = f"""# Max-Code CLI - Work Session Status
Generated: {timestamp}

## Current Task
{task.description}

## Project State
- Snapshot: `{snapshot_data['file']}`
- Timestamp: {snapshot_data['timestamp']}

## Next Steps
1. Resume from snapshot: Load `{snapshot_data['file']}`
2. Review pending tasks
3. Continue implementation

## Quick Commands
```bash
# Load snapshot
python3 -c "import json; print(json.load(open('{snapshot_data['file']}')))"

# Run tests
pytest -v

# Check coverage
pytest --cov --cov-report=term-missing
```

---
*Generated by Sleep Agent (/dormir)*
"""

        status_file.write_text(content)

        return {
            'file': str(status_file),
            'size': status_file.stat().st_size
        }

    async def _git_operations(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform git commit and push operations"""
        import subprocess

        results = {
            'add': False,
            'commit': False,
            'push': False,
            'errors': []
        }

        try:
            # Git add
            result = subprocess.run(
                ['git', 'add', '.'],
                capture_output=True,
                text=True,
                timeout=10
            )
            results['add'] = result.returncode == 0

            if results['add']:
                # Git commit
                commit_msg = f"🌙 End-of-day checkpoint - {snapshot_data['timestamp']}\n\nAuto-generated by Sleep Agent (/dormir)"
                result = subprocess.run(
                    ['git', 'commit', '-m', commit_msg],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                results['commit'] = result.returncode == 0

                if results['commit']:
                    # Git push
                    result = subprocess.run(
                        ['git', 'push'],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    results['push'] = result.returncode == 0
                    if not results['push']:
                        results['errors'].append(result.stderr)
        except Exception as e:
            results['errors'].append(str(e))

        return results

    async def _cleanup_operations(self) -> Dict[str, Any]:
        """Perform cleanup operations"""
        cleanup_tasks = {
            'temp_files_removed': 0,
            'cache_cleared': False
        }

        # Remove __pycache__ directories
        import shutil
        pycache_count = 0
        for pycache in Path('.').rglob('__pycache__'):
            try:
                shutil.rmtree(pycache)
                pycache_count += 1
            except (OSError, PermissionError):
                pass

        cleanup_tasks['temp_files_removed'] = pycache_count
        cleanup_tasks['cache_cleared'] = pycache_count > 0

        return cleanup_tasks

    async def _maximus_summary(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get MAXIMUS session summary"""
        try:
            # Use MAXIMUS to analyze session and provide insights
            analysis_result = await self.maximus_client.analyze_code(
                code=json.dumps(snapshot_data, indent=2),
                context={'task': 'session_summary'}
            )

            return {
                'insights': analysis_result.get('insights', []),
                'recommendations': analysis_result.get('recommendations', [])
            }
        except (ConnectionError, TimeoutError, AttributeError, Exception):
            return {'error': 'MAXIMUS summary failed'}

    def _generate_report(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final end-of-day report"""
        phases_completed = len(workflow_results)

        summary_parts = []

        if 'snapshot' in workflow_results:
            summary_parts.append("✓ Snapshot created")

        if 'status_file' in workflow_results:
            summary_parts.append("✓ Status file saved")

        if 'git' in workflow_results:
            git = workflow_results['git']
            if git.get('push'):
                summary_parts.append("✓ Changes pushed to remote")
            elif git.get('commit'):
                summary_parts.append("⚠ Committed (push failed)")
            else:
                summary_parts.append("⚠ Git operations incomplete")

        if 'cleanup' in workflow_results:
            cleanup = workflow_results['cleanup']
            summary_parts.append(f"✓ Cleanup ({cleanup.get('temp_files_removed', 0)} items)")

        if 'maximus_summary' in workflow_results:
            summary_parts.append("✓ MAXIMUS summary generated")

        return {
            'summary': ', '.join(summary_parts),
            'phases_completed': phases_completed,
            'ready_for_resume': phases_completed >= 3  # At least snapshot, status, git
        }


if __name__ == "__main__":
    # Test the sleep agent
    agent = SleepAgent()

    test_task = AgentTask(
        id="test_sleep",
        description="Test end-of-day workflow",
        parameters={"current_work": "Creating sleep agent"}
    )

    result = agent.execute(test_task)

    print("\n" + "="*60)
    print("SLEEP AGENT TEST RESULT")
    print("="*60)
    print(f"Success: {result.success}")
    print(f"Phases completed: {result.metrics.get('phases_completed')}")
    print(f"\nReport:")
    print(f"  {result.output['report']['summary']}")
    print(f"  Ready for resume: {result.output['report']['ready_for_resume']}")
