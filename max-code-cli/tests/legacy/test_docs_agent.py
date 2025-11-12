"""
Comprehensive Scientific Test Suite for DocsAgent

Tests the Documentation Agent's capabilities including:
- Narrative intelligence integration
- Documentation generation quality
- Multiple documentation types (API docs, README, tutorials)
- Code-to-docs translation
- Documentation formatting
- Error handling and resilience
- NIS integration and fallback behavior

Following scientific testing principles:
- Falsifiability: Each test has clear pass/fail criteria
- Reproducibility: Tests produce consistent results
- Isolation: Tests are independent and don't affect each other
- Comprehensive coverage: Tests cover normal and edge cases
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from agents.docs_agent import DocsAgent
from sdk.base_agent import AgentTask, AgentCapability
from core.maximus_integration.nis_client import (
    NISClient, CodeChange, NarrativeStyle, Narrative,
    KeyInsight, VisualizationData
)


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

def test_docs_agent_initialization():
    """Test DocsAgent initializes with correct configuration"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    assert agent.agent_id == "docs_test"
    assert agent.agent_name == "Docs Agent (MAXIMUS-Enhanced)"
    assert agent.port == 8166
    assert agent.nis_client is None  # Disabled in this test
    print("✅ DocsAgent initialization works")


def test_docs_agent_initialization_with_maximus():
    """Test DocsAgent initializes with MAXIMUS/NIS enabled"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    assert agent.agent_id == "docs_test"
    assert agent.nis_client is not None
    assert isinstance(agent.nis_client, NISClient)
    print("✅ DocsAgent initialization with MAXIMUS works")


def test_docs_agent_capabilities():
    """Test DocsAgent reports correct capabilities"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)
    capabilities = agent.get_capabilities()

    assert len(capabilities) == 1
    assert AgentCapability.DOCUMENTATION in capabilities
    print("✅ DocsAgent capabilities reporting works")


# ============================================================================
# BASIC DOCUMENTATION GENERATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_basic_documentation_generation():
    """Test basic documentation generation without NIS"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-001",
        description="Generate documentation for code changes",
        parameters={
            "changes": [
                {
                    "file_path": "auth.py",
                    "change_type": "modified",
                    "lines_added": 50,
                    "lines_deleted": 20,
                }
            ]
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.task_id == "doc-001"
    assert "docs" in result.output
    assert result.output["narrative"] is None  # No NIS
    assert result.metrics["mode"] == "standalone"

    docs = result.output["docs"]
    assert "Documentation" in docs
    assert "1 files modified" in docs
    print("✅ Basic documentation generation works")


@pytest.mark.asyncio
async def test_documentation_with_no_changes():
    """Test documentation generation with no code changes"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-002",
        description="Generate documentation with no changes",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "0 files modified" in result.output["docs"]
    print("✅ Documentation with no changes works")


@pytest.mark.asyncio
async def test_documentation_with_multiple_changes():
    """Test documentation generation with multiple file changes"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-003",
        description="Generate documentation for multiple changes",
        parameters={
            "changes": [
                {"file_path": "auth.py", "change_type": "modified", "lines_added": 50, "lines_deleted": 20},
                {"file_path": "utils.py", "change_type": "added", "lines_added": 100, "lines_deleted": 0},
                {"file_path": "old_code.py", "change_type": "deleted", "lines_added": 0, "lines_deleted": 80},
            ]
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "3 files modified" in result.output["docs"]
    print("✅ Documentation with multiple changes works")


# ============================================================================
# NIS INTEGRATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_with_nis_integration():
    """Test documentation generation with NIS narrative integration"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    # Mock NIS client
    mock_narrative = Narrative(
        title="Authentication System Refactoring",
        story="# The Journey to Better Authentication\n\nThis change refactors the authentication system...",
        key_insights=[
            KeyInsight(category="security", insight="Improved password hashing", importance="HIGH")
        ],
        summary="Refactored authentication for better security",
        visualization_data=VisualizationData(
            change_distribution={"modified": 1},
            file_impact={"auth.py": 0.8},
            complexity_trend=[0.5, 0.6, 0.7]
        ),
        confidence=0.9,
        style=NarrativeStyle.STORY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-004",
        description="Generate documentation with NIS",
        parameters={
            "changes": [
                {"file_path": "auth.py", "change_type": "modified", "lines_added": 50, "lines_deleted": 20}
            ],
            "context": {"project": "user_service"}
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.metrics["mode"] == "hybrid"
    assert result.output["narrative"] is not None
    assert result.output["narrative"].title == "Authentication System Refactoring"
    assert "The Journey to Better Authentication" in result.output["docs"]
    print("✅ Documentation with NIS integration works")


@pytest.mark.asyncio
async def test_documentation_with_nis_offline():
    """Test documentation generation when NIS is offline (graceful fallback)"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    # Mock NIS as offline
    agent.nis_client.health_check = AsyncMock(return_value=False)

    task = AgentTask(
        id="doc-005",
        description="Generate documentation with NIS offline",
        parameters={
            "changes": [
                {"file_path": "auth.py", "change_type": "modified", "lines_added": 50, "lines_deleted": 20}
            ]
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.metrics["mode"] == "standalone"
    assert result.output["narrative"] is None
    assert "Documentation" in result.output["docs"]
    print("✅ Documentation with NIS offline (fallback) works")


@pytest.mark.asyncio
async def test_documentation_with_nis_error():
    """Test documentation generation when NIS throws error (resilience)"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    # Mock NIS to throw error
    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(side_effect=Exception("NIS error"))

    task = AgentTask(
        id="doc-006",
        description="Generate documentation with NIS error",
        parameters={
            "changes": [
                {"file_path": "auth.py", "change_type": "modified", "lines_added": 50, "lines_deleted": 20}
            ]
        }
    )

    result = await agent._execute_async(task)

    # Should still succeed despite NIS error
    assert result.success
    assert result.metrics["mode"] == "standalone"
    assert result.output["narrative"] is None
    print("✅ Documentation with NIS error (resilience) works")


# ============================================================================
# NARRATIVE STYLE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_story_style():
    """Test documentation generation with STORY narrative style"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="The Story of Our Code",
        story="# Once upon a time...\n\nA developer decided to improve the codebase...",
        key_insights=[],
        summary="A story-based explanation",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.85,
        style=NarrativeStyle.STORY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-007",
        description="Generate story-style documentation",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.output["narrative"].style == NarrativeStyle.STORY
    assert "Once upon a time" in result.output["docs"]
    print("✅ Documentation with STORY style works")


@pytest.mark.asyncio
async def test_documentation_technical_style():
    """Test documentation generation with TECHNICAL narrative style"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Technical Documentation",
        story="## Technical Overview\n\nThis change implements OAuth 2.0...",
        key_insights=[
            KeyInsight(category="architecture", insight="Added PKCE flow", importance="HIGH")
        ],
        summary="Technical implementation details",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.95,
        style=NarrativeStyle.TECHNICAL
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-008",
        description="Generate technical documentation",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.output["narrative"].style == NarrativeStyle.TECHNICAL
    print("✅ Documentation with TECHNICAL style works")


# ============================================================================
# DOCUMENTATION QUALITY TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_includes_key_insights():
    """Test documentation includes key insights from NIS"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Security Improvements",
        story="Enhanced security measures implemented.",
        key_insights=[
            KeyInsight(category="security", insight="Added rate limiting", importance="CRITICAL"),
            KeyInsight(category="security", insight="Implemented HTTPS only", importance="HIGH"),
            KeyInsight(category="performance", insight="Optimized queries", importance="MEDIUM")
        ],
        summary="Security-focused changes",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.9,
        style=NarrativeStyle.TECHNICAL
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-009",
        description="Generate documentation with insights",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    insights = result.output["narrative"].key_insights
    assert len(insights) == 3
    assert any(i.importance == "CRITICAL" for i in insights)
    assert any(i.category == "security" for i in insights)
    print("✅ Documentation includes key insights")


@pytest.mark.asyncio
async def test_documentation_confidence_score():
    """Test documentation includes confidence score"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Code Changes",
        story="Changes implemented.",
        key_insights=[],
        summary="Summary of changes",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.92,
        style=NarrativeStyle.SUMMARY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-010",
        description="Generate documentation with confidence",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.output["narrative"].confidence == 0.92
    assert result.output["narrative"].confidence > 0.9
    print("✅ Documentation includes confidence score")


# ============================================================================
# CODE-TO-DOCS TRANSLATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_code_change_types():
    """Test documentation handles different code change types"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-011",
        description="Document different change types",
        parameters={
            "changes": [
                {"file_path": "new_feature.py", "change_type": "added", "lines_added": 100, "lines_deleted": 0},
                {"file_path": "existing.py", "change_type": "modified", "lines_added": 30, "lines_deleted": 15},
                {"file_path": "deprecated.py", "change_type": "deleted", "lines_added": 0, "lines_deleted": 50}
            ]
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "3 files modified" in result.output["docs"]
    print("✅ Documentation handles different change types")


@pytest.mark.asyncio
async def test_documentation_with_context():
    """Test documentation generation uses provided context"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="E-commerce Payment Integration",
        story="Integrated Stripe payment gateway for the e-commerce platform.",
        key_insights=[],
        summary="Payment integration for online store",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.88,
        style=NarrativeStyle.STORY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-012",
        description="Document payment integration",
        parameters={
            "changes": [{"file_path": "payment.py", "change_type": "added", "lines_added": 200, "lines_deleted": 0}],
            "context": {
                "project": "e-commerce",
                "purpose": "Add Stripe payments",
                "team": "payments"
            }
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "Payment" in result.output["narrative"].title or "payment" in result.output["narrative"].story.lower()

    # Verify context was passed to NIS
    call_args = agent.nis_client.generate_narrative.call_args
    assert call_args[1]["context"]["project"] == "e-commerce"
    assert call_args[1]["context"]["purpose"] == "Add Stripe payments"
    print("✅ Documentation uses context correctly")


# ============================================================================
# DOCUMENTATION FORMATTING TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_output_structure():
    """Test documentation output has correct structure"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-013",
        description="Generate structured documentation",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert "docs" in result.output
    assert "narrative" in result.output
    assert isinstance(result.output["docs"], str)
    assert "metrics" in result.__dict__
    print("✅ Documentation output structure is correct")


@pytest.mark.asyncio
async def test_documentation_markdown_formatting():
    """Test documentation is formatted as valid markdown"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-014",
        description="Generate markdown documentation",
        parameters={
            "changes": [
                {"file_path": "test.py", "change_type": "modified", "lines_added": 10, "lines_deleted": 5}
            ]
        }
    )

    result = await agent._execute_async(task)

    assert result.success
    docs = result.output["docs"]

    # Check for markdown headers
    assert "# Documentation" in docs or "## Documentation" in docs
    assert "Changes:" in docs
    print("✅ Documentation markdown formatting works")


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_handles_invalid_task():
    """Test documentation handles missing parameters gracefully"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-015",
        description="Generate documentation",
        parameters={}  # Missing 'changes' key
    )

    result = await agent._execute_async(task)

    # Should still succeed with empty changes
    assert result.success
    assert "0 files modified" in result.output["docs"]
    print("✅ Documentation handles missing parameters")


@pytest.mark.asyncio
async def test_documentation_handles_malformed_changes():
    """Test documentation handles malformed change data"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-016",
        description="Generate documentation with malformed data",
        parameters={
            "changes": [
                {"file_path": "test.py"},  # Missing other fields
                {"change_type": "modified"},  # Missing file_path
            ]
        }
    )

    result = await agent._execute_async(task)

    # Should still succeed
    assert result.success
    assert "2 files modified" in result.output["docs"]
    print("✅ Documentation handles malformed changes")


@pytest.mark.asyncio
async def test_documentation_timeout_resilience():
    """Test documentation generation handles NIS timeout gracefully"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    # Mock NIS to timeout
    async def slow_health_check():
        await asyncio.sleep(0.1)
        return True

    agent.nis_client.health_check = slow_health_check
    agent.nis_client.generate_narrative = AsyncMock(side_effect=asyncio.TimeoutError())

    task = AgentTask(
        id="doc-017",
        description="Generate documentation with timeout",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    # Should fallback to standalone mode
    assert result.success
    assert result.metrics["mode"] == "standalone"
    print("✅ Documentation handles timeout gracefully")


# ============================================================================
# INTEGRATION AND WORKFLOW TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_workflow_phases():
    """Test documentation generation follows correct workflow phases"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Test",
        story="Test story",
        key_insights=[],
        summary="Test summary",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.8,
        style=NarrativeStyle.STORY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-018",
        description="Test workflow phases",
        parameters={"changes": []}
    )

    # Capture print output to verify phases
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = await agent._execute_async(task)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert result.success
    # Verify Phase 1 and Phase 2 were executed
    assert "Phase 1" in output
    assert "Phase 2" in output
    print("✅ Documentation workflow phases work correctly")


@pytest.mark.asyncio
async def test_documentation_visualization_data():
    """Test documentation includes visualization data"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Changes",
        story="Story",
        key_insights=[],
        summary="Summary",
        visualization_data=VisualizationData(
            change_distribution={"added": 100, "modified": 50, "deleted": 20},
            file_impact={"auth.py": 0.9, "utils.py": 0.3},
            complexity_trend=[0.3, 0.5, 0.7, 0.6],
            test_coverage=85.5
        ),
        confidence=0.9,
        style=NarrativeStyle.TECHNICAL
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-019",
        description="Test visualization data",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    viz_data = result.output["narrative"].visualization_data
    assert viz_data.change_distribution["added"] == 100
    assert viz_data.file_impact["auth.py"] == 0.9
    assert len(viz_data.complexity_trend) == 4
    assert viz_data.test_coverage == 85.5
    print("✅ Documentation includes visualization data")


# ============================================================================
# NARRATIVE INTELLIGENCE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_narrative_intelligence_code_translation():
    """Test narrative intelligence translates code changes into human story"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="From Monolith to Microservices",
        story="""# The Transformation Journey

## The Challenge
The team faced a growing monolithic application that was becoming difficult to maintain...

## The Solution
We decided to break down the monolith into microservices...

## The Outcome
The new architecture provides better scalability and maintainability.""",
        key_insights=[
            KeyInsight(category="architecture", insight="Improved modularity", importance="HIGH")
        ],
        summary="Architectural transformation story",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.95,
        style=NarrativeStyle.STORY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-020",
        description="Test narrative intelligence",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    story = result.output["narrative"].story

    # Verify story structure
    assert "Challenge" in story or "challenge" in story.lower()
    assert "Solution" in story or "solution" in story.lower()
    assert "Outcome" in story or "outcome" in story.lower()
    print("✅ Narrative intelligence code translation works")


@pytest.mark.asyncio
async def test_narrative_intelligence_tutorial_mode():
    """Test narrative intelligence generates tutorial-style documentation"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Step-by-Step OAuth Integration",
        story="""# OAuth 2.0 Integration Tutorial

## Step 1: Setup OAuth Client
First, register your application with the OAuth provider...

## Step 2: Implement Authorization Flow
Next, implement the authorization code flow...

## Step 3: Handle Token Refresh
Finally, add logic to refresh expired tokens...""",
        key_insights=[],
        summary="Tutorial for OAuth integration",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.92,
        style=NarrativeStyle.TUTORIAL
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-021",
        description="Test tutorial mode",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.output["narrative"].style == NarrativeStyle.TUTORIAL
    story = result.output["narrative"].story

    # Verify tutorial structure with steps
    assert "Step 1" in story
    assert "Step 2" in story
    assert "Step 3" in story
    print("✅ Narrative intelligence tutorial mode works")


@pytest.mark.asyncio
async def test_narrative_intelligence_changelog_mode():
    """Test narrative intelligence generates changelog-style documentation"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Version 2.0.0 Changelog",
        story="""# Changelog

## [2.0.0] - 2025-11-04

### Added
- OAuth 2.0 authentication
- Rate limiting middleware

### Changed
- Updated database schema
- Refactored authentication module

### Fixed
- Fixed memory leak in cache
- Resolved race condition in queue""",
        key_insights=[],
        summary="Changelog for version 2.0.0",
        visualization_data=VisualizationData(
            change_distribution={"added": 2, "modified": 2, "fixed": 2},
            file_impact={},
            complexity_trend=[]
        ),
        confidence=0.98,
        style=NarrativeStyle.CHANGELOG
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-022",
        description="Test changelog mode",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.output["narrative"].style == NarrativeStyle.CHANGELOG
    story = result.output["narrative"].story

    # Verify changelog structure
    assert "Added" in story or "added" in story.lower()
    assert "Changed" in story or "changed" in story.lower()
    assert "Fixed" in story or "fixed" in story.lower()
    print("✅ Narrative intelligence changelog mode works")


# ============================================================================
# METRICS AND TRACKING TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_documentation_metrics_standalone():
    """Test documentation metrics in standalone mode"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-023",
        description="Test standalone metrics",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.metrics is not None
    assert result.metrics["mode"] == "standalone"
    print("✅ Documentation metrics (standalone) work")


@pytest.mark.asyncio
async def test_documentation_metrics_hybrid():
    """Test documentation metrics in hybrid mode (with NIS)"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=True)

    mock_narrative = Narrative(
        title="Test",
        story="Test",
        key_insights=[],
        summary="Test",
        visualization_data=VisualizationData(
            change_distribution={}, file_impact={}, complexity_trend=[]
        ),
        confidence=0.8,
        style=NarrativeStyle.STORY
    )

    agent.nis_client.health_check = AsyncMock(return_value=True)
    agent.nis_client.generate_narrative = AsyncMock(return_value=mock_narrative)

    task = AgentTask(
        id="doc-024",
        description="Test hybrid metrics",
        parameters={"changes": []}
    )

    result = await agent._execute_async(task)

    assert result.success
    assert result.metrics is not None
    assert result.metrics["mode"] == "hybrid"
    print("✅ Documentation metrics (hybrid) work")


# ============================================================================
# ASYNC EXECUTION TESTS
# ============================================================================

def test_documentation_async_execution():
    """Test documentation executes asynchronously"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    task = AgentTask(
        id="doc-025",
        description="Test async execution",
        parameters={"changes": []}
    )

    # Execute using sync wrapper (creates new event loop)
    result = agent.execute(task)

    assert result.success
    assert result.task_id == "doc-025"
    print("✅ Documentation async execution works")


@pytest.mark.asyncio
async def test_documentation_concurrent_execution():
    """Test multiple documentation generations can run concurrently"""
    agent = DocsAgent(agent_id="docs_test", enable_maximus=False)

    tasks = [
        AgentTask(id=f"doc-{i}", description=f"Task {i}", parameters={"changes": []})
        for i in range(3)
    ]

    # Execute concurrently
    results = await asyncio.gather(*[agent._execute_async(task) for task in tasks])

    assert len(results) == 3
    assert all(r.success for r in results)
    assert [r.task_id for r in results] == ["doc-0", "doc-1", "doc-2"]
    print("✅ Documentation concurrent execution works")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPREHENSIVE SCIENTIFIC TEST SUITE FOR DOCSAGENT")
    print("="*70 + "\n")

    pytest.main([__file__, "-v", "-s"])
