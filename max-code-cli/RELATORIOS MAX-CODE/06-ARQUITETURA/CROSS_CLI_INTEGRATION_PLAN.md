# Cross-CLI Integration Plan
## MAXIMUS + External CLIs (gcloud, aws, etc.)

**Created**: 2025-11-04
**Status**: Planning Phase
**Priority**: HIGH

---

## 🎯 Objective

Enable MAXIMUS AI to intelligently decide when to use:
1. **Claude's toolkit** (Claude Code CLI tools) - Superior for planning, analysis, and reporting
2. **Gemini's toolkit** (Google AI APIs) - Better for web search and real-time data
3. **External CLIs** (gcloud, aws, kubectl, etc.) - For infrastructure operations

**Key Insight**: Just like Claude Code can say "deploy to GCR" and automatically use gcloud CLI, MAXIMUS should have the same capability but with **intelligent decision-making** about which toolkit to use.

---

## 🏗️ Architecture

### Layer 1: Toolkit Registry
Registry of available CLIs and their capabilities:

```python
class ToolkitRegistry:
    """
    Registry of available toolkits
    """
    toolkits = {
        'claude': {
            'capabilities': [
                'code_analysis',
                'planning',
                'reasoning',
                'report_generation',
                'file_operations',
                'git_operations'
            ],
            'strengths': [
                'Long context reasoning',
                'Constitutional principles',
                'Code review',
                'Scientific analysis'
            ]
        },
        'gemini': {
            'capabilities': [
                'web_search',
                'realtime_data',
                'multimodal_processing',
                'video_analysis'
            ],
            'strengths': [
                'Real-time information',
                'Web scraping',
                'Image understanding',
                'Fast inference'
            ]
        },
        'gcloud': {
            'capabilities': [
                'gcp_deployment',
                'cloud_run_operations',
                'gcr_management',
                'compute_engine',
                'kubernetes_operations'
            ],
            'strengths': [
                'Native GCP integration',
                'Infrastructure as code',
                'Service management'
            ]
        },
        'aws': {
            'capabilities': [
                'aws_deployment',
                'lambda_operations',
                'ec2_management',
                's3_operations'
            ]
        },
        'kubectl': {
            'capabilities': [
                'k8s_deployment',
                'pod_management',
                'service_operations'
            ]
        }
    }
```

### Layer 2: Intelligent Toolkit Selector

MAXIMUS AI decides which toolkit to use based on:

```python
class IntelligentToolkitSelector:
    """
    MAXIMUS-powered toolkit selection

    Uses Tree of Thoughts + Constitutional Principles to decide
    which toolkit is best for the current task.
    """

    async def select_toolkit(
        self,
        task_description: str,
        available_toolkits: List[str],
        context: Dict[str, Any]
    ) -> ToolkitSelection:
        """
        Decision process:
        1. Analyze task requirements
        2. Evaluate toolkit capabilities
        3. Apply constitutional constraints (P1-P6)
        4. Consider cost, speed, and quality trade-offs
        5. Return best toolkit with confidence score
        """

        # Use Tree of Thoughts for multi-path evaluation
        thoughts = await self.tot.generate_thoughts(
            task=task_description,
            context=context
        )

        # Evaluate each toolkit option
        evaluations = []
        for toolkit in available_toolkits:
            evaluation = await self._evaluate_toolkit(
                toolkit=toolkit,
                task=task_description,
                thoughts=thoughts
            )
            evaluations.append(evaluation)

        # Apply decision fusion
        best_toolkit = await self.decision_fusion.select(
            options=evaluations,
            strategy=DecisionStrategy.CASCADE
        )

        return ToolkitSelection(
            toolkit=best_toolkit.name,
            confidence=best_toolkit.confidence,
            reasoning=best_toolkit.reasoning
        )
```

### Layer 3: CLI Wrapper

Unified interface for executing commands on any CLI:

```python
class CLIWrapper:
    """
    Unified wrapper for external CLIs
    """

    async def execute(
        self,
        cli: str,
        command: str,
        parameters: Dict[str, Any],
        timeout: int = 30
    ) -> CLIResult:
        """
        Execute command on specified CLI

        Examples:
        - execute('gcloud', 'run deploy', {...})
        - execute('aws', 's3 cp', {...})
        - execute('kubectl', 'apply', {...})
        """

        # Validate CLI is installed
        if not await self._is_cli_available(cli):
            return CLIResult(
                success=False,
                error=f"CLI '{cli}' not installed"
            )

        # Build command
        full_command = self._build_command(cli, command, parameters)

        # Execute with safety checks
        result = await self._execute_with_safety(
            command=full_command,
            timeout=timeout
        )

        return result

    async def _is_cli_available(self, cli: str) -> bool:
        """Check if CLI is installed"""
        try:
            subprocess.run([cli, '--version'], capture_output=True)
            return True
        except FileNotFoundError:
            return False
```

### Layer 4: MAXIMUS Integration

MAXIMUS orchestrates the entire flow:

```python
class MAXIMUSOrchestrator:
    """
    Orchestrates toolkit selection and execution
    """

    def __init__(self):
        self.toolkit_registry = ToolkitRegistry()
        self.selector = IntelligentToolkitSelector()
        self.cli_wrapper = CLIWrapper()
        self.maximus_client = MaximusClient()

    async def execute_task(
        self,
        task: str,
        context: Dict[str, Any]
    ) -> TaskResult:
        """
        Complete task execution with intelligent toolkit selection

        Flow:
        1. User request: "Deploy this to GCR"
        2. MAXIMUS analyzes: Needs gcloud CLI
        3. Selector verifies: gcloud available
        4. Wrapper executes: gcloud run deploy ...
        5. Results returned to user
        """

        # Phase 1: Task analysis
        analysis = await self.maximus_client.analyze_task(
            task=task,
            context=context
        )

        # Phase 2: Toolkit selection
        toolkit_selection = await self.selector.select_toolkit(
            task_description=analysis.description,
            available_toolkits=self.toolkit_registry.list_available(),
            context=context
        )

        # Phase 3: Execution
        if toolkit_selection.toolkit in ['gcloud', 'aws', 'kubectl']:
            # External CLI
            result = await self.cli_wrapper.execute(
                cli=toolkit_selection.toolkit,
                command=analysis.command,
                parameters=analysis.parameters
            )
        elif toolkit_selection.toolkit == 'claude':
            # Use Claude Code tools
            result = await self._execute_claude_tools(analysis)
        elif toolkit_selection.toolkit == 'gemini':
            # Use Gemini APIs
            result = await self._execute_gemini_tools(analysis)

        # Phase 4: Constitutional validation (P1-P6)
        validated_result = await self._validate_result(result)

        return validated_result
```

---

## 🔄 Decision Flow

```
User Request: "Deploy this service to GCR and search for deployment best practices"

    ↓

MAXIMUS Analysis:
  - Task 1: Deploy to GCR → Needs infrastructure operations
  - Task 2: Search best practices → Needs web search

    ↓

Toolkit Selection:
  - Task 1 → gcloud CLI (GCP native deployment)
  - Task 2 → Gemini API (better web search than Claude)

    ↓

Parallel Execution:
  - gcloud run deploy service-name --image=...
  - gemini.search("GCP Cloud Run deployment best practices")

    ↓

Result Synthesis:
  - Deployment logs from gcloud
  - Best practices from Gemini
  - Combined report using Claude (better at synthesis)

    ↓

Return to User:
  ✓ Service deployed successfully
  📊 Best practices report generated
```

---

## 🛡️ Constitutional Compliance

All toolkit selections and executions must comply with P1-P6:

### P1 - Primazia da Responsabilidade (Responsibility First)
- Never execute destructive commands without user confirmation
- Always validate CLI commands before execution
- Log all external CLI operations

### P2 - Transparência Radical (Radical Transparency)
- Show user which toolkit was selected and why
- Display confidence scores for toolkit selection
- Log all decision reasoning

### P3 - Benefício Coletivo (Collective Benefit)
- Choose most cost-effective toolkit when quality is equivalent
- Consider resource usage (API costs, compute time)
- Prefer open-source tools when appropriate

### P4 - Prudência Operacional (Operational Prudence)
- Validate all CLI commands before execution
- Implement timeouts and safety checks
- Handle errors gracefully with fallbacks

### P5 - Autocorreção Humilde (Humble Self-Correction)
- Learn from toolkit selection mistakes
- Improve decision model based on outcomes
- Track success rates per toolkit

### P6 - Respeito à Dignidade (Respect for Dignity)
- Protect user credentials and secrets
- Never log sensitive information
- Respect user preferences for toolkit selection

---

## 📊 Example Scenarios

### Scenario 1: GCP Deployment
```python
User: "Deploy the max-code-cli to Cloud Run in GCP"

MAXIMUS Decision:
  - Primary: gcloud CLI (native GCP support)
  - Secondary: Claude Code (for rollback if needed)
  - Confidence: 95%

Execution:
  1. gcloud auth check
  2. gcloud run deploy max-code-cli \
       --image=gcr.io/project/max-code-cli \
       --platform=managed \
       --region=us-central1
  3. Claude Code: Generate deployment report

Result: ✓ Deployed successfully
```

### Scenario 2: Research Task
```python
User: "Research latest AI model benchmarks and summarize"

MAXIMUS Decision:
  - Primary: Gemini API (better web search)
  - Secondary: Claude Code (better synthesis)
  - Confidence: 92%

Execution:
  1. Gemini: Search web for "latest AI model benchmarks 2025"
  2. Gemini: Extract key data points
  3. Claude: Synthesize into report (superior writing)

Result: 📊 Comprehensive benchmark report
```

### Scenario 3: Code Analysis
```python
User: "Analyze this codebase for security vulnerabilities"

MAXIMUS Decision:
  - Primary: Claude Code (superior code analysis)
  - Secondary: MAXIMUS (ethical review)
  - Confidence: 98%

Execution:
  1. Claude: Analyze code with constitutional lens
  2. MAXIMUS: Verify ethical compliance
  3. Claude: Generate detailed report

Result: 🔒 Security analysis with P1-P6 compliance
```

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create ToolkitRegistry
- [ ] Implement CLIWrapper for gcloud
- [ ] Basic toolkit detection

### Phase 2: Intelligence (Week 2)
- [ ] Implement IntelligentToolkitSelector
- [ ] Integrate with Tree of Thoughts
- [ ] Add decision fusion logic

### Phase 3: Integration (Week 3)
- [ ] MAXIMUSOrchestrator implementation
- [ ] Claude Code integration
- [ ] Gemini API integration

### Phase 4: Additional CLIs (Week 4)
- [ ] AWS CLI support
- [ ] kubectl support
- [ ] Docker CLI support
- [ ] Custom CLI registration

### Phase 5: Polish (Week 5)
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] Performance optimization
- [ ] User feedback integration

---

## 🎓 Learning System

MAXIMUS learns from toolkit selection outcomes:

```python
class ToolkitLearningSystem:
    """
    Learn from toolkit selection outcomes
    """

    async def record_outcome(
        self,
        task: str,
        toolkit_used: str,
        success: bool,
        metrics: Dict[str, float]
    ):
        """
        Record toolkit selection outcome

        Metrics tracked:
        - Success rate per toolkit
        - Average execution time
        - Cost per operation
        - User satisfaction
        """

        await self.database.store_outcome(
            task_type=self._classify_task(task),
            toolkit=toolkit_used,
            success=success,
            duration=metrics['duration'],
            cost=metrics['cost']
        )

        # Update selection model
        await self._update_selection_model()
```

---

## 📝 Configuration

User can configure toolkit preferences:

```yaml
# config/toolkit_preferences.yaml

toolkit_preferences:
  # Prefer Claude for code analysis
  code_analysis:
    preferred: claude
    fallback: gemini

  # Prefer Gemini for web search
  web_search:
    preferred: gemini
    fallback: claude

  # Prefer gcloud for GCP operations
  gcp_operations:
    preferred: gcloud
    required: true  # Don't fallback

  # Cost limits
  cost_limits:
    max_per_request: 0.10  # USD
    max_daily: 5.00  # USD

  # Performance thresholds
  performance:
    max_latency: 30  # seconds
    prefer_fast_over_quality: false
```

---

## 🔐 Security Considerations

1. **Credential Management**
   - Never log credentials
   - Use system keychains for API keys
   - Rotate tokens regularly

2. **Command Validation**
   - Whitelist safe commands
   - Block destructive operations without confirmation
   - Sandbox experimental commands

3. **API Key Protection**
   - Encrypt keys at rest
   - Use environment variables
   - Implement rate limiting

4. **Audit Logging**
   - Log all toolkit selections
   - Track all CLI executions
   - Record all API calls

---

## 📈 Success Metrics

Track these KPIs to measure success:

1. **Toolkit Selection Accuracy**
   - Target: >95% optimal toolkit selection

2. **Execution Success Rate**
   - Target: >98% successful executions

3. **User Satisfaction**
   - Target: >4.5/5 stars

4. **Cost Efficiency**
   - Target: <10% cost increase vs. single toolkit

5. **Response Time**
   - Target: <30s for 90% of requests

---

## 🧪 Testing Strategy

```python
# tests/test_cross_cli_integration.py

def test_toolkit_selection_accuracy():
    """Test MAXIMUS selects correct toolkit"""

    scenarios = [
        ("Deploy to GCR", "gcloud"),
        ("Search web for benchmarks", "gemini"),
        ("Analyze code security", "claude"),
        ("Deploy to AWS", "aws"),
        ("Manage k8s pods", "kubectl")
    ]

    for task, expected_toolkit in scenarios:
        selection = selector.select_toolkit(task)
        assert selection.toolkit == expected_toolkit
        assert selection.confidence > 0.8


def test_cli_wrapper_execution():
    """Test CLI wrapper can execute commands"""

    wrapper = CLIWrapper()

    # Test gcloud
    result = await wrapper.execute(
        cli='gcloud',
        command='version',
        parameters={}
    )
    assert result.success is True


def test_constitutional_compliance():
    """Test P1-P6 compliance in toolkit selection"""

    # Test P1: Responsibility
    destructive_task = "Delete all production data"
    result = orchestrator.execute_task(destructive_task)
    assert result.requires_confirmation is True

    # Test P2: Transparency
    result = orchestrator.execute_task("Deploy service")
    assert result.reasoning is not None
    assert result.confidence is not None
```

---

## 🎯 Next Steps

1. **Review and Approve Plan** ✓
2. **Create ToolkitRegistry** (next task)
3. **Implement CLIWrapper for gcloud**
4. **Add to main implementation plan**

---

**Status**: 📋 Ready for implementation
**Estimated Time**: 5 weeks
**Priority**: HIGH
**Dependencies**: MAXIMUS Integration, Tree of Thoughts, Decision Fusion
