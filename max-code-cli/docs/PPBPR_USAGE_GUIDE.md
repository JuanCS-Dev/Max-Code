# P.P.B.P.R Usage Guide 📚

**Prompt → Paper → Blueprint → Plan → Refine**

Automated research-to-implementation methodology.

---

## Quick Start

### 1. Set API Key

```bash
export GEMINI_API_KEY="your-key-here"
```

Or add to `.env`:
```
GEMINI_API_KEY=your-key-here
```

### 2. Run Basic Research

```bash
max-code ppbpr run "Constitutional AI v3.0 principles for production systems"
```

### 3. Check Output

```bash
ls outputs/ppbpr/
# paper_*.md - Research paper with citations
# blueprint_*.md - Architecture design
# plan_*.md - Implementation roadmap
```

---

## Research Depths

### Basic (Quick Overview)
```bash
max-code ppbpr run "Redis caching strategies" --depth basic
```
- **Time:** ~1-2 minutes
- **Output:** 2,000 words
- **Sources:** 1+ minimum
- **Use:** Quick literature review

### Moderate (Balanced)
```bash
max-code ppbpr run "CI/CD pipelines" --depth moderate
```
- **Time:** ~2-3 minutes
- **Output:** 5,000 words
- **Sources:** 2+ minimum
- **Use:** Standard research projects

### Comprehensive (Deep Dive) ⭐
```bash
max-code ppbpr run "Medical diagnostic AI systems" --depth comprehensive
```
- **Time:** ~5-10 minutes
- **Output:** 10,000+ words
- **Sources:** 3+ minimum
- **Use:** Major projects, PhD-level research

---

## Advanced Options

### Custom Output Directory

```bash
max-code ppbpr run "Kubernetes architecture" \
  --output ./research/k8s \
  --depth comprehensive
```

### JSON Format

```bash
max-code ppbpr run "GraphQL vs REST" \
  --format json \
  --output ./api-research
```

### Skip Constitutional Validation

```bash
# Not recommended - skips P1-P6 validation
max-code ppbpr run "Docker best practices" \
  --skip-validation
```

### Verbose Output

```bash
max-code ppbpr run "Blockchain consensus" \
  --verbose \
  --depth comprehensive
```

---

## Python API Usage

### Basic Usage

```python
import asyncio
from pathlib import Path
from core.ppbpr.orchestrator import PPBPROrchestrator

async def research():
    orchestrator = PPBPROrchestrator()

    deliverable = await orchestrator.run(
        prompt="AI-powered medical diagnosis systems",
        research_depth="comprehensive"
    )

    print(f"Quality Score: {deliverable.quality_score:.2f}")
    print(f"Paper: {len(deliverable.paper.split())} words")
    print(f"Execution Time: {deliverable.execution_time_seconds:.1f}s")

    # Save outputs
    deliverable.save_to_file(
        output_dir=Path("./outputs/medical-ai"),
        format="markdown"
    )

asyncio.run(research())
```

### Advanced Configuration

```python
from core.ppbpr.orchestrator import PPBPROrchestrator

# Custom configuration
orchestrator = PPBPROrchestrator(
    enable_quality_gates=True,      # Validate at each step
    enable_constitutional=True       # P1-P6 validation
)

deliverable = await orchestrator.run(
    prompt="Your research topic here",
    research_depth="comprehensive"
)

# Access individual components
print("Research:", deliverable.research.content)
print("Paper:", deliverable.paper)
print("Blueprint:", deliverable.blueprint)
print("Plan:", deliverable.plan)

# Quality metrics
print(f"Research Quality: {deliverable.research.quality_score:.2f}")
print(f"Overall Quality: {deliverable.quality_score:.2f}")

# Constitutional report
for principle, passed in deliverable.constitutional_report.items():
    status = "✅" if passed else "❌"
    print(f"{status} {principle}")
```

### Gemini Client Direct Usage

```python
import asyncio
from core.ppbpr.gemini_client import GeminiResearchTool

async def quick_research():
    tool = GeminiResearchTool()

    result = await tool.research_topic(
        topic="Python async/await patterns",
        depth="basic"
    )

    print(f"Words: {result.word_count}")
    print(f"Sources: {len(result.sources)}")
    print(f"Quality: {result.quality_score:.2f}")
    print(f"\nContent:\n{result.content}")

asyncio.run(quick_research())
```

---

## Example Prompts

### Software Engineering

```bash
# Microservices Architecture
max-code ppbpr run "Microservices architecture patterns, service mesh, API gateways, event-driven design, deployment strategies, monitoring and observability best practices"

# Database Design
max-code ppbpr run "NoSQL vs SQL databases, CAP theorem, consistency models, sharding strategies, replication patterns, query optimization for high-scale applications"

# Security
max-code ppbpr run "Zero-trust security architecture, Constitutional AI governance, cryptographic verification, threat modeling, secure coding patterns, defense in depth"
```

### AI/ML Projects

```bash
# ML System Design
max-code ppbpr run "Production ML systems architecture, model serving, A/B testing, feature stores, model monitoring, MLOps best practices, cost optimization"

# LLM Applications
max-code ppbpr run "LLM application architecture, RAG systems, vector databases, prompt engineering, fine-tuning strategies, hallucination mitigation, cost-effective deployment"
```

### Medical/Healthcare

```bash
# Medical AI
max-code ppbpr run "AI-powered differential diagnosis, clinical decision support systems, multi-modal medical data integration, FHIR/HL7 standards, FDA approval pathway, HIPAA compliance"

# Telemedicine
max-code ppbpr run "Telemedicine platform architecture, real-time video consultation, EHR integration, prescription management, LGPD/GDPR compliance, scalability for 1M+ users"
```

---

## Understanding Output

### Research Paper Structure

```markdown
# Research Paper

**Generated:** 2025-11-11T23:30:00

**Prompt:** Your original prompt

---

## 1. Executive Summary
- Key findings overview
- Main recommendations
- Impact assessment

## 2. Introduction & Context
- Problem statement
- Current landscape
- Objectives

## 3. Technical Background
- Core concepts
- Related technologies
- Industry context

## 4. Analysis of Approaches
- Multiple solution approaches
- Trade-offs analysis
- Comparative evaluation

## 5. Recommendations
- Best practices
- Implementation strategies
- Risk mitigation

## 6. Implementation Considerations
- Technical requirements
- Resource needs
- Timeline estimates

## 7. Conclusion
- Summary of findings
- Future directions

## 8. References
[1] Source Title
    https://source-url.com
```

### Blueprint Structure (Phase 2)

Currently placeholder - will integrate Sophia (ArchitectAgent) for:
- Component architecture
- Design patterns
- Technology stack
- Scalability strategy
- Security considerations

### Plan Structure (Phase 2)

Currently placeholder - will integrate PlanAgent for:
- Phase breakdown
- Task list with dependencies
- Timeline estimates
- Resource allocation
- Risk mitigation

---

## Quality Metrics

### Research Quality Score (0-1)

Calculated from:
- **Content Length (40%):** Words generated
- **Source Count (40%):** Number of references
- **Source Diversity (20%):** Unique domains

**Targets:**
- Basic: ≥0.3
- Moderate: ≥0.5
- Comprehensive: ≥0.7

### Overall Quality Score (0-1)

Weighted average:
- Research Quality: 30%
- Paper Quality: 30%
- Blueprint Confidence: 20%
- Plan Completeness: 20%

---

## Troubleshooting

### API Key Not Configured

```
❌ Error: GEMINI_API_KEY not configured
```

**Solution:**
```bash
export GEMINI_API_KEY="your-key-here"
# Or add to .env file
```

### Content Blocked by Safety Filters

```
❌ Content blocked by safety filters
```

**Solution:** Rephrase your query to be more neutral/academic

### Low Quality Score

```
⚠️ Quality Score: 0.20 (low)
```

**Possible causes:**
- No sources extracted (API limitation)
- Short content (<500 words)
- Limited topic coverage

**Solution:**
- Use `--depth comprehensive`
- Provide more detailed prompt
- Add specific areas to research

### Timeout

```
❌ Request timeout after 60s
```

**Solution:**
- Reduce prompt complexity
- Use `--depth basic` or `moderate`
- Check network connection

---

## Best Practices

### 1. Write Detailed Prompts

❌ **Bad:**
```
"Machine learning"
```

✅ **Good:**
```
"Machine learning model deployment architecture including model serving frameworks (TensorFlow Serving, TorchServe), A/B testing strategies, monitoring and observability, cost optimization, and scalability patterns for production systems handling 1M+ requests/day"
```

### 2. Specify Research Areas

Structure your prompt with clear sections:
```
# Main Topic

## Research Objectives
1. Area 1
2. Area 2
3. Area 3

## Expected Outputs
- Architecture diagram
- Technology recommendations
- Implementation roadmap
```

### 3. Use Comprehensive Depth for Important Projects

```bash
# For major projects, PhD-level research
max-code ppbpr run "..." --depth comprehensive
```

### 4. Save Outputs with Descriptive Names

```bash
max-code ppbpr run "..." --output ./research/project-name-2025-11
```

### 5. Review Constitutional Report

Check which principles passed:
- P1 - Zero Trust
- P2 - Completude
- P3 - Visão Sistêmica
- P4 - Obrigação da Verdade
- P5 - Soberania da Intenção
- P6 - Antifragilidade

---

## Cost Estimation

### Gemini 2.5 Flash Pricing

| Depth | Tokens | Cost per Run |
|-------|--------|--------------|
| Basic | ~4K | ~$0.0006 |
| Moderate | ~10K | ~$0.0015 |
| Comprehensive | ~20K | ~$0.003 |

**Monthly estimates (100 runs):**
- Basic: $0.06/month
- Moderate: $0.15/month
- Comprehensive: $0.30/month

**Very affordable!** 🎉

---

## Next Steps

### After Research Complete

1. **Review Paper:** Read the research findings
2. **Validate Recommendations:** Cross-check with your domain knowledge
3. **Use Blueprint:** (Phase 2) System architecture design
4. **Follow Plan:** (Phase 2) Implementation roadmap
5. **Iterate:** Refine and improve based on findings

### Phase 2 Integration (Coming Soon)

- **Sophia Integration:** Real architecture blueprints
- **PlanAgent Integration:** Detailed implementation plans
- **Enhanced Grounding:** Better source extraction
- **Multi-Step Refinement:** Iterative improvement loops

---

## Examples from Real Usage

### Example 1: Constitutional AI Research

```bash
max-code ppbpr run "Constitutional AI v3.0 implementation for multi-agent systems" \
  --depth comprehensive \
  --output ./research/constitutional-ai
```

**Output:**
- 8,500 word research paper
- P1-P6 principles analysis
- Multi-agent orchestration patterns
- Quality gates implementation
- Validation strategies
- Production deployment guide

### Example 2: Medical Diagnostic AI (Current Test)

```bash
max-code ppbpr run "AI-powered medical differential diagnosis..." \
  --depth comprehensive \
  --output ./outputs/ppbpr/medical_diagnostic
```

**Prompt includes:**
- Clinical domain analysis
- Multi-modal data integration
- AI/ML architecture
- Performance requirements
- Regulatory compliance
- Implementation roadmap

**Expected output:**
- 10,000+ word comprehensive analysis
- Technology stack recommendations
- Two-mode system architecture
- Validation strategies
- Cost-benefit analysis

---

## Support & Documentation

- **Main Docs:** `/docs/PPBPR_PHASE1_COMPLETE.md`
- **Code Examples:** `/examples/ppbpr_*.py`
- **Issues:** GitHub Issues
- **Questions:** Open discussion in repo

---

**Soli Deo Gloria!** 🙏

*Automated research for the glory of God and service to humanity.*
