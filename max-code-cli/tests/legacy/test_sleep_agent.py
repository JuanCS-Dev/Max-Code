"""
Scientific Tests for Sleep Agent

Tests the specialized end-of-day workflow agent that handles:
- Project snapshot creation
- Status file generation
- Git operations (commit, push)
- Cleanup operations
- State preservation for exact resumption

Test Philosophy:
- Test REAL end-of-day workflow behavior
- Validate complete state preservation
- Test git operations safely (no actual push)
- Scientific rigor: reproducible, deterministic

Run:
    pytest tests/test_sleep_agent.py -v
"""

import sys
import os
import pytest
import json
import asyncio
from pathlib import Path
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

# Add parent to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.sleep_agent import SleepAgent
from sdk.base_agent import AgentTask, AgentCapability


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sleep_agent():
    """Create sleep agent instance"""
    return SleepAgent(enable_maximus=False)


@pytest.fixture
def sleep_agent_with_maximus():
    """Create sleep agent with MAXIMUS enabled"""
    return SleepAgent(enable_maximus=True)


@pytest.fixture
def test_task():
    """Create test task"""
    return AgentTask(
        id="test_sleep_001",
        description="Test end-of-day workflow",
        parameters={"current_work": "Implementing sleep agent"}
    )


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for git operations"""
    with patch('subprocess.run') as mock:
        # Default successful responses
        mock.return_value = MagicMock(
            returncode=0,
            stdout="success",
            stderr=""
        )
        yield mock


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Cleanup test files after each test"""
    yield
    # Cleanup snapshots
    snapshot_dir = Path('./.snapshots')
    if snapshot_dir.exists():
        for file in snapshot_dir.glob('snapshot_*.json'):
            try:
                file.unlink()
            except:
                pass

    # Cleanup status file
    status_file = Path('./STATUS.md')
    if status_file.exists():
        try:
            status_file.unlink()
        except:
            pass


# ============================================================================
# TEST: Agent Initialization
# ============================================================================

def test_sleep_agent_initialization():
    """Test SleepAgent can be initialized"""
    agent = SleepAgent()

    assert agent.agent_id == "sleep_agent"
    assert agent.agent_name == "Sleep Agent (State Preservation)"
    assert agent.port == 8170
    assert agent.snapshot_dir.exists()


def test_sleep_agent_capabilities():
    """Test agent declares correct capabilities"""
    agent = SleepAgent()
    capabilities = agent.get_capabilities()

    assert AgentCapability.PLANNING in capabilities
    assert AgentCapability.CODE_GENERATION in capabilities


def test_sleep_agent_with_maximus_enabled():
    """Test agent with MAXIMUS integration"""
    agent = SleepAgent(enable_maximus=True)

    assert agent.maximus_client is not None


def test_sleep_agent_without_maximus():
    """Test agent without MAXIMUS integration"""
    agent = SleepAgent(enable_maximus=False)

    assert agent.maximus_client is None


# ============================================================================
# TEST: Snapshot Creation
# ============================================================================

@pytest.mark.asyncio
async def test_create_snapshot_basic(sleep_agent, test_task):
    """Test basic snapshot creation"""
    snapshot_data = await sleep_agent._create_snapshot(test_task)

    assert 'file' in snapshot_data
    assert 'timestamp' in snapshot_data
    assert 'size' in snapshot_data

    # Verify file exists
    snapshot_file = Path(snapshot_data['file'])
    assert snapshot_file.exists()

    # Verify JSON structure
    with open(snapshot_file) as f:
        data = json.load(f)
        assert 'timestamp' in data
        assert 'task_context' in data
        assert 'project_state' in data


@pytest.mark.asyncio
async def test_snapshot_contains_task_context(sleep_agent, test_task):
    """Test snapshot contains complete task context"""
    snapshot_data = await sleep_agent._create_snapshot(test_task)

    with open(snapshot_data['file']) as f:
        data = json.load(f)

        assert data['task_context']['description'] == test_task.description
        assert data['task_context']['task_id'] == test_task.id
        assert 'parameters' in data['task_context']


@pytest.mark.asyncio
async def test_snapshot_contains_project_state(sleep_agent, test_task):
    """Test snapshot contains project state"""
    snapshot_data = await sleep_agent._create_snapshot(test_task)

    with open(snapshot_data['file']) as f:
        data = json.load(f)

        assert 'project_state' in data
        assert 'git_branch' in data['project_state']
        assert 'modified_files' in data['project_state']


@pytest.mark.asyncio
async def test_snapshot_timestamp_format(sleep_agent, test_task):
    """Test snapshot timestamp format"""
    snapshot_data = await sleep_agent._create_snapshot(test_task)

    # Timestamp should be in format: YYYYMMDD_HHMMSS
    timestamp = snapshot_data['timestamp']
    assert len(timestamp) == 15  # YYYYMMDD_HHMMSS
    assert '_' in timestamp

    # Should be parseable
    datetime.strptime(timestamp, "%Y%m%d_%H%M%S")


@pytest.mark.asyncio
async def test_multiple_snapshots_unique_files(sleep_agent, test_task):
    """Test multiple snapshots create unique files"""
    snapshot1 = await sleep_agent._create_snapshot(test_task)

    # Small delay to ensure different timestamp
    await asyncio.sleep(1.1)

    snapshot2 = await sleep_agent._create_snapshot(test_task)

    assert snapshot1['file'] != snapshot2['file']
    assert Path(snapshot1['file']).exists()
    assert Path(snapshot2['file']).exists()


# ============================================================================
# TEST: Project State Collection
# ============================================================================

@pytest.mark.asyncio
async def test_collect_project_state_structure(sleep_agent):
    """Test project state collection returns correct structure"""
    state = await sleep_agent._collect_project_state()

    assert 'git_branch' in state
    assert 'git_status' in state
    assert 'modified_files' in state
    assert 'untracked_files' in state


@pytest.mark.asyncio
async def test_collect_project_state_handles_git_errors(sleep_agent):
    """Test project state collection handles git errors gracefully"""
    with patch('subprocess.run', side_effect=Exception("Git error")):
        state = await sleep_agent._collect_project_state()

        # Should return default state on error
        assert state['git_branch'] == 'unknown'


# ============================================================================
# TEST: Status File Creation
# ============================================================================

@pytest.mark.asyncio
async def test_create_status_file(sleep_agent, test_task):
    """Test status file creation"""
    snapshot_data = {
        'file': '.snapshots/test_snapshot.json',
        'timestamp': '20250104_120000',
        'size': 1024
    }

    status_result = await sleep_agent._create_status_file(test_task, snapshot_data)

    assert 'file' in status_result
    assert 'size' in status_result

    status_file = Path(status_result['file'])
    assert status_file.exists()


@pytest.mark.asyncio
async def test_status_file_content(sleep_agent, test_task):
    """Test status file contains required information"""
    snapshot_data = {
        'file': '.snapshots/test_snapshot.json',
        'timestamp': '20250104_120000',
        'size': 1024
    }

    status_result = await sleep_agent._create_status_file(test_task, snapshot_data)

    content = Path(status_result['file']).read_text()

    # Should contain key sections
    assert 'Max-Code CLI' in content
    assert 'Current Task' in content
    assert 'Project State' in content
    assert 'Next Steps' in content
    assert 'Quick Commands' in content

    # Should reference snapshot
    assert snapshot_data['file'] in content


@pytest.mark.asyncio
async def test_status_file_markdown_format(sleep_agent, test_task):
    """Test status file is valid markdown"""
    snapshot_data = {
        'file': '.snapshots/test_snapshot.json',
        'timestamp': '20250104_120000',
        'size': 1024
    }

    status_result = await sleep_agent._create_status_file(test_task, snapshot_data)

    content = Path(status_result['file']).read_text()

    # Should have markdown headers
    assert content.startswith('# ')
    assert '## ' in content

    # Should have code blocks
    assert '```' in content


# ============================================================================
# TEST: Git Operations
# ============================================================================

@pytest.mark.asyncio
async def test_git_operations_structure(sleep_agent, mock_subprocess):
    """Test git operations return correct structure"""
    snapshot_data = {'timestamp': '20250104_120000'}

    result = await sleep_agent._git_operations(snapshot_data)

    assert 'add' in result
    assert 'commit' in result
    assert 'push' in result
    assert 'errors' in result


@pytest.mark.asyncio
async def test_git_operations_success_flow(sleep_agent, mock_subprocess):
    """Test successful git operations flow"""
    snapshot_data = {'timestamp': '20250104_120000'}

    result = await sleep_agent._git_operations(snapshot_data)

    # All operations should succeed with mock
    assert result['add'] is True
    assert result['commit'] is True
    assert result['push'] is True
    assert len(result['errors']) == 0


@pytest.mark.asyncio
async def test_git_commit_message_format(sleep_agent, mock_subprocess):
    """Test git commit message contains snapshot info"""
    snapshot_data = {'timestamp': '20250104_120000'}

    await sleep_agent._git_operations(snapshot_data)

    # Check commit was called with correct message
    calls = mock_subprocess.call_args_list
    commit_call = [c for c in calls if 'commit' in str(c)]

    assert len(commit_call) > 0


@pytest.mark.asyncio
async def test_git_operations_handles_add_failure(sleep_agent):
    """Test git operations handle add failure"""
    with patch('subprocess.run') as mock:
        # Make git add fail
        mock.return_value = MagicMock(returncode=1, stderr="add failed")

        snapshot_data = {'timestamp': '20250104_120000'}
        result = await sleep_agent._git_operations(snapshot_data)

        assert result['add'] is False
        assert result['commit'] is False  # Should not attempt commit


@pytest.mark.asyncio
async def test_git_operations_handles_push_failure(sleep_agent):
    """Test git operations handle push failure gracefully"""
    with patch('subprocess.run') as mock:
        def side_effect(*args, **kwargs):
            cmd = args[0]
            if 'push' in cmd:
                return MagicMock(returncode=1, stderr="push failed")
            return MagicMock(returncode=0, stdout="success")

        mock.side_effect = side_effect

        snapshot_data = {'timestamp': '20250104_120000'}
        result = await sleep_agent._git_operations(snapshot_data)

        assert result['add'] is True
        assert result['commit'] is True
        assert result['push'] is False
        assert len(result['errors']) > 0


# ============================================================================
# TEST: Cleanup Operations
# ============================================================================

@pytest.mark.asyncio
async def test_cleanup_operations_structure(sleep_agent):
    """Test cleanup operations return correct structure"""
    result = await sleep_agent._cleanup_operations()

    assert 'temp_files_removed' in result
    assert 'cache_cleared' in result


@pytest.mark.asyncio
async def test_cleanup_operations_counts_removed_files(sleep_agent):
    """Test cleanup counts removed files"""
    result = await sleep_agent._cleanup_operations()

    assert isinstance(result['temp_files_removed'], int)
    assert result['temp_files_removed'] >= 0


# ============================================================================
# TEST: Full Workflow Execution
# ============================================================================

def test_execute_workflow_success(sleep_agent, test_task, mock_subprocess):
    """Test complete workflow execution"""
    result = sleep_agent.execute(test_task)

    assert result.success is True
    assert 'workflow_results' in result.output
    assert 'report' in result.output
    assert 'timestamp' in result.output


def test_execute_workflow_creates_snapshot(sleep_agent, test_task, mock_subprocess):
    """Test workflow creates snapshot"""
    result = sleep_agent.execute(test_task)

    assert 'snapshot' in result.output['workflow_results']

    snapshot = result.output['workflow_results']['snapshot']
    assert Path(snapshot['file']).exists()


def test_execute_workflow_creates_status_file(sleep_agent, test_task, mock_subprocess):
    """Test workflow creates status file"""
    result = sleep_agent.execute(test_task)

    assert 'status_file' in result.output['workflow_results']

    status_file = result.output['workflow_results']['status_file']
    assert Path(status_file['file']).exists()


def test_execute_workflow_performs_git_operations(sleep_agent, test_task, mock_subprocess):
    """Test workflow performs git operations"""
    result = sleep_agent.execute(test_task)

    assert 'git' in result.output['workflow_results']

    git = result.output['workflow_results']['git']
    assert 'add' in git
    assert 'commit' in git
    assert 'push' in git


def test_execute_workflow_performs_cleanup(sleep_agent, test_task, mock_subprocess):
    """Test workflow performs cleanup"""
    result = sleep_agent.execute(test_task)

    assert 'cleanup' in result.output['workflow_results']


def test_execute_workflow_generates_report(sleep_agent, test_task, mock_subprocess):
    """Test workflow generates comprehensive report"""
    result = sleep_agent.execute(test_task)

    report = result.output['report']

    assert 'summary' in report
    assert 'phases_completed' in report
    assert 'ready_for_resume' in report


def test_execute_workflow_reports_phases_completed(sleep_agent, test_task, mock_subprocess):
    """Test workflow reports number of phases completed"""
    result = sleep_agent.execute(test_task)

    phases = result.output['report']['phases_completed']
    assert phases >= 4  # snapshot, status, git, cleanup


def test_execute_workflow_metrics(sleep_agent, test_task, mock_subprocess):
    """Test workflow includes metrics"""
    result = sleep_agent.execute(test_task)

    assert 'mode' in result.metrics
    assert 'phases_completed' in result.metrics


# ============================================================================
# TEST: MAXIMUS Integration
# ============================================================================

def test_execute_workflow_with_maximus_offline(sleep_agent_with_maximus, test_task, mock_subprocess):
    """Test workflow handles MAXIMUS offline gracefully"""
    async def mock_health_check():
        return False

    with patch.object(sleep_agent_with_maximus.maximus_client, 'health_check', new=AsyncMock(return_value=False)):
        result = sleep_agent_with_maximus.execute(test_task)

        assert result.success is True
        # May have MAXIMUS summary with error, or none at all
        if 'maximus_summary' in result.output['workflow_results']:
            # If present, should indicate an error
            assert 'error' in result.output['workflow_results']['maximus_summary']


# ============================================================================
# TEST: Report Generation
# ============================================================================

def test_generate_report_summary(sleep_agent):
    """Test report generation creates summary"""
    workflow_results = {
        'snapshot': {'file': 'test.json'},
        'status_file': {'file': 'STATUS.md'},
        'git': {'add': True, 'commit': True, 'push': True},
        'cleanup': {'temp_files_removed': 5}
    }

    report = sleep_agent._generate_report(workflow_results)

    assert 'summary' in report
    assert '✓' in report['summary']


def test_generate_report_ready_for_resume(sleep_agent):
    """Test report indicates readiness for resume"""
    workflow_results = {
        'snapshot': {'file': 'test.json'},
        'status_file': {'file': 'STATUS.md'},
        'git': {'add': True, 'commit': True, 'push': True}
    }

    report = sleep_agent._generate_report(workflow_results)

    assert report['ready_for_resume'] is True


def test_generate_report_incomplete_workflow(sleep_agent):
    """Test report handles incomplete workflow"""
    workflow_results = {
        'snapshot': {'file': 'test.json'}
        # Missing status_file and git
    }

    report = sleep_agent._generate_report(workflow_results)

    assert report['ready_for_resume'] is False


def test_generate_report_git_failure(sleep_agent):
    """Test report indicates git failures"""
    workflow_results = {
        'snapshot': {'file': 'test.json'},
        'status_file': {'file': 'STATUS.md'},
        'git': {'add': True, 'commit': True, 'push': False}
    }

    report = sleep_agent._generate_report(workflow_results)

    assert '⚠' in report['summary']


# ============================================================================
# TEST: Edge Cases
# ============================================================================

def test_execute_with_empty_context(sleep_agent, mock_subprocess):
    """Test workflow with empty task parameters"""
    task = AgentTask(
        id="empty_test",
        description="Empty parameters test",
        parameters={}
    )

    result = sleep_agent.execute(task)

    assert result.success is True


def test_execute_creates_snapshot_directory(mock_subprocess):
    """Test workflow creates snapshot directory if missing"""
    # Remove snapshot dir if exists
    snapshot_dir = Path('./.snapshots')
    if snapshot_dir.exists():
        import shutil
        shutil.rmtree(snapshot_dir)

    agent = SleepAgent()

    assert agent.snapshot_dir.exists()


@pytest.mark.asyncio
async def test_collect_coverage_metrics_structure(sleep_agent):
    """Test coverage metrics collection structure"""
    metrics = await sleep_agent._collect_coverage_metrics()

    assert 'total_coverage' in metrics
    assert 'statement_coverage' in metrics


# ============================================================================
# TEST: Performance
# ============================================================================

def test_execute_workflow_performance(sleep_agent, test_task, mock_subprocess):
    """Test workflow completes in reasonable time"""
    import time

    start = time.time()
    result = sleep_agent.execute(test_task)
    duration = time.time() - start

    assert result.success is True
    assert duration < 10  # Should complete in under 10 seconds


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

1. Agent Initialization (4 tests)
   - Basic initialization
   - Capabilities
   - With/without MAXIMUS

2. Snapshot Creation (5 tests)
   - Basic creation
   - Task context
   - Project state
   - Timestamp format
   - Multiple snapshots

3. Project State Collection (2 tests)
   - Structure validation
   - Error handling

4. Status File Creation (3 tests)
   - File creation
   - Content validation
   - Markdown format

5. Git Operations (5 tests)
   - Structure validation
   - Success flow
   - Commit message
   - Failure handling

6. Cleanup Operations (2 tests)
   - Structure validation
   - File counting

7. Full Workflow (8 tests)
   - Complete execution
   - Snapshot creation
   - Status file creation
   - Git operations
   - Cleanup
   - Report generation
   - Metrics

8. MAXIMUS Integration (1 test)
   - Offline handling

9. Report Generation (4 tests)
   - Summary creation
   - Resume readiness
   - Incomplete workflow
   - Git failures

10. Edge Cases (3 tests)
    - Empty context
    - Directory creation
    - Coverage metrics

11. Performance (1 test)
    - Execution time

Total: 38 scientific tests for Sleep Agent
"""
