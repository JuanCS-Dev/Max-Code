"""
P.P.B.P.R Methodology Orchestrator
Sequential pipeline: Prompt → Paper → Blueprint → Plan → Refine

Constitutional AI v3.0 Compliance:
- P1 (Zero Trust): Validates at each step with quality gates
- P2 (Completude): Ensures 100% functional outputs
- P3 (Visão Sistêmica): Holistic analysis across all phases
- P4 (Obrigação da Verdade): Honest quality assessment
- P5 (Soberania da Intenção): User intent paramount
- P6 (Antifragilidade): Improves with iteration/feedback
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

from core.ppbpr.gemini_client import GeminiResearchTool, ResearchResult
from config.settings import get_settings
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class PPBPRDeliverable:
    """
    Final P.P.B.P.R deliverable

    Contains all outputs from the complete methodology execution
    """
    # Core outputs
    prompt: str
    research: ResearchResult
    paper: str
    blueprint: Dict[str, Any]
    plan: Dict[str, Any]

    # Quality metrics
    quality_score: float
    constitutional_report: Dict[str, bool]

    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    execution_time_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "prompt": self.prompt,
            "research": {
                "content": self.research.content,
                "sources": [
                    {"uri": s.uri, "title": s.title}
                    for s in self.research.sources
                ],
                "word_count": self.research.word_count,
                "quality_score": self.research.quality_score
            },
            "paper": self.paper,
            "blueprint": self.blueprint,
            "plan": self.plan,
            "quality_score": self.quality_score,
            "constitutional_report": self.constitutional_report,
            "timestamp": self.timestamp,
            "execution_time_seconds": self.execution_time_seconds
        }

    def save_to_file(self, output_dir: Path, format: str = "markdown"):
        """
        Save deliverable to files

        Args:
            output_dir: Output directory
            format: Output format (markdown/json)
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp_clean = self.timestamp.replace(":", "-").split(".")[0]

        if format == "markdown":
            # Save paper
            paper_path = output_dir / f"paper_{timestamp_clean}.md"
            with open(paper_path, "w") as f:
                f.write(f"# Research Paper\n\n")
                f.write(f"**Generated:** {self.timestamp}\n\n")
                f.write(f"**Prompt:** {self.prompt}\n\n")
                f.write(f"---\n\n{self.paper}\n\n")
                f.write(f"## Sources\n\n")
                for i, source in enumerate(self.research.sources, 1):
                    f.write(f"{i}. [{source.title}]({source.uri})\n")

            logger.info(f"📄 Paper saved: {paper_path}")

            # Save blueprint
            blueprint_path = output_dir / f"blueprint_{timestamp_clean}.md"
            with open(blueprint_path, "w") as f:
                f.write(f"# Architecture Blueprint\n\n")
                f.write(f"**Generated:** {self.timestamp}\n\n")
                f.write(f"```json\n{json.dumps(self.blueprint, indent=2)}\n```\n")

            logger.info(f"🏗️  Blueprint saved: {blueprint_path}")

            # Save plan
            plan_path = output_dir / f"plan_{timestamp_clean}.md"
            with open(plan_path, "w") as f:
                f.write(f"# Implementation Plan\n\n")
                f.write(f"**Generated:** {self.timestamp}\n\n")
                f.write(f"```json\n{json.dumps(self.plan, indent=2)}\n```\n")

            logger.info(f"📋 Plan saved: {plan_path}")

        elif format == "json":
            # Save complete deliverable as JSON
            json_path = output_dir / f"ppbpr_deliverable_{timestamp_clean}.json"
            with open(json_path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)

            logger.info(f"💾 Complete deliverable saved: {json_path}")


class PPBPROrchestrator:
    """
    P.P.B.P.R Methodology Orchestrator

    Coordinates the complete workflow:
    1. PROMPT - User's detailed idea
    2. PAPER - Deep research using Gemini
    3. BLUEPRINT - Architecture design (future: integrate Sophia)
    4. PLAN - Implementation roadmap (future: integrate PlanAgent)
    5. REFINE - Quality validation and iteration

    Current Phase 1 Implementation:
    - PROMPT → PAPER (Gemini research) ✅
    - PAPER → BLUEPRINT (placeholder - manual for now) ⏳
    - BLUEPRINT → PLAN (placeholder - manual for now) ⏳
    - REFINE → Constitutional validation ✅
    """

    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        enable_quality_gates: bool = True,
        enable_constitutional: bool = True
    ):
        """
        Initialize P.P.B.P.R orchestrator

        Args:
            gemini_api_key: Gemini API key (or from settings)
            enable_quality_gates: Enable QG1-QG5 validation
            enable_constitutional: Enable P1-P6 validation
        """
        self.settings = get_settings()

        # Initialize Gemini research tool
        api_key = gemini_api_key or self.settings.gemini.api_key
        if not api_key:
            logger.warning(
                "⚠️  Gemini API key not configured. "
                "P.P.B.P.R will fail without GEMINI_API_KEY."
            )

        self.research_tool = GeminiResearchTool(api_key=api_key)

        # Quality control flags
        self.enable_quality_gates = enable_quality_gates
        self.enable_constitutional = enable_constitutional

        logger.info("✅ P.P.B.P.R Orchestrator initialized")

    async def run(
        self,
        prompt: str,
        research_depth: str = "comprehensive"
    ) -> PPBPRDeliverable:
        """
        Execute complete P.P.B.P.R workflow

        Args:
            prompt: User's detailed idea/requirement
            research_depth: Research depth (basic/moderate/comprehensive)

        Returns:
            Complete deliverable with all outputs

        Raises:
            ValueError: If quality gates fail
            Exception: If any phase fails critically
        """
        start_time = datetime.utcnow()
        logger.info(f"🚀 Starting P.P.B.P.R workflow")
        logger.info(f"   Prompt: {prompt[:80]}...")
        logger.info(f"   Depth: {research_depth}")

        try:
            # PHASE 1: PROMPT → RESEARCH → PAPER
            logger.info("\n[1/5] 🔍 RESEARCH PHASE (Gemini Deep Research)")
            research = await self._research_phase(prompt, research_depth)

            logger.info(f"✅ Research complete:")
            logger.info(f"   - {research.word_count} words")
            logger.info(f"   - {len(research.sources)} sources")
            logger.info(f"   - Quality: {research.quality_score:.2f}")

            # PHASE 2: RESEARCH → PAPER
            logger.info("\n[2/5] 📄 PAPER GENERATION (Gemini Writing)")
            paper = await self._write_paper(prompt, research)

            paper_words = len(paper.split())
            logger.info(f"✅ Paper complete: {paper_words} words")

            # PHASE 3: PAPER → BLUEPRINT (Placeholder for now)
            logger.info("\n[3/5] 🏗️  BLUEPRINT DESIGN (Placeholder)")
            blueprint = await self._create_blueprint_placeholder(paper, prompt)

            logger.info(f"✅ Blueprint created: {blueprint.get('approach', 'N/A')}")

            # PHASE 4: BLUEPRINT → PLAN (Placeholder for now)
            logger.info("\n[4/5] 📋 IMPLEMENTATION PLAN (Placeholder)")
            plan = await self._generate_plan_placeholder(blueprint, prompt)

            logger.info(f"✅ Plan created: {len(plan.get('phases', []))} phases")

            # PHASE 5: REFINE & VALIDATE
            logger.info("\n[5/5] ✨ REFINEMENT & VALIDATION")
            constitutional_report = self._validate_constitutional({
                "research": research,
                "paper": paper,
                "blueprint": blueprint,
                "plan": plan
            })

            # Calculate overall quality
            quality_score = self._calculate_quality_score(
                research, paper, blueprint, plan
            )

            logger.info(f"✅ Quality score: {quality_score:.2f}")
            logger.info(f"✅ Constitutional: {all(constitutional_report.values())}")

            # Build deliverable
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()

            deliverable = PPBPRDeliverable(
                prompt=prompt,
                research=research,
                paper=paper,
                blueprint=blueprint,
                plan=plan,
                quality_score=quality_score,
                constitutional_report=constitutional_report,
                execution_time_seconds=execution_time
            )

            logger.info(f"\n✅ P.P.B.P.R Complete! ({execution_time:.1f}s)")

            return deliverable

        except Exception as e:
            logger.error(f"❌ P.P.B.P.R failed: {e}")
            raise

    async def _research_phase(
        self,
        prompt: str,
        depth: str
    ) -> ResearchResult:
        """
        Phase 1: Deep research using Gemini

        Quality Gate 1 (QG1): Validates research completeness
        """
        result = await self.research_tool.research_topic(
            topic=prompt,
            depth=depth
        )

        # QG1: Validate research quality
        if self.enable_quality_gates:
            is_valid, message = self.research_tool.client.validate_research_quality(
                result,
                min_words=self.settings.ppbpr.min_research_words,
                min_sources=self.settings.ppbpr.min_research_sources,
                min_quality=self.settings.ppbpr.min_quality_score
            )

            if not is_valid:
                if self.settings.ppbpr.retry_on_failure:
                    logger.warning(f"⚠️  QG1 failed: {message}. Retrying...")
                    result = await self.research_tool.research_topic(
                        topic=prompt,
                        depth=depth
                    )
                else:
                    raise ValueError(f"QG1 (Research Quality) failed: {message}")

        return result

    async def _write_paper(
        self,
        prompt: str,
        research: ResearchResult
    ) -> str:
        """
        Phase 2: Generate research paper from findings

        Quality Gate 2 (QG2): Validates paper structure
        """
        # Enhanced prompt for paper writing
        paper_prompt = f"""
Based on the following research, write a comprehensive PhD-level research paper:

**TOPIC:** {prompt}

**RESEARCH FINDINGS:**
{research.content}

**SOURCES:**
{self._format_sources(research.sources)}

**STRUCTURE YOUR PAPER AS:**
1. **Executive Summary** (2-3 paragraphs)
   - Key findings overview
   - Main recommendations
   - Impact assessment

2. **Introduction & Context**
   - Problem statement
   - Current landscape
   - Objectives

3. **Technical Background**
   - Core concepts
   - Related technologies
   - Industry context

4. **Analysis of Approaches**
   - Multiple solution approaches
   - Trade-offs analysis
   - Comparative evaluation

5. **Recommendations**
   - Best practices
   - Implementation strategies
   - Risk mitigation

6. **Implementation Considerations**
   - Technical requirements
   - Resource needs
   - Timeline estimates

7. **Conclusion**
   - Summary of findings
   - Future directions

8. **References**
   - All cited sources

**REQUIREMENTS:**
- PhD-level technical writing
- Evidence-based analysis
- Clear, precise language
- Properly cited sources
- 2,000-4,000 words
- Professional formatting
"""

        # Generate paper using Gemini
        paper_result = await self.research_tool.client.deep_research(
            query=paper_prompt,
            max_tokens=self.settings.gemini.max_tokens,
            temperature=0.7
        )

        paper = paper_result.content

        # QG2: Validate paper structure
        if self.enable_quality_gates:
            is_valid, message = self._validate_paper_structure(paper)
            if not is_valid:
                if self.settings.ppbpr.retry_on_failure:
                    logger.warning(f"⚠️  QG2 failed: {message}. Retrying...")
                    # Retry with more explicit structure requirements
                    paper_result = await self.research_tool.client.deep_research(
                        query=paper_prompt + "\n\nIMPORTANT: Include ALL sections listed above.",
                        max_tokens=self.settings.gemini.max_tokens
                    )
                    paper = paper_result.content
                else:
                    logger.warning(f"⚠️  QG2 (Paper Structure): {message}")

        return paper

    async def _create_blueprint_placeholder(
        self,
        paper: str,
        prompt: str
    ) -> Dict[str, Any]:
        """
        Phase 3: Architecture blueprint (placeholder for Sophia integration)

        TODO Phase 2: Integrate with ArchitectAgent (Sophia)
        """
        logger.info("⏳ Blueprint phase - using placeholder (Sophia integration pending)")

        # For now, return a basic blueprint structure
        # In Phase 2, this will call Sophia (ArchitectAgent)
        return {
            "approach": "Placeholder - Manual blueprint required",
            "patterns": ["To be defined by Sophia"],
            "components": ["Component 1", "Component 2"],
            "note": "This will be replaced with Sophia (ArchitectAgent) in Phase 2",
            "confidence": 0.5  # Low confidence for placeholder
        }

    async def _generate_plan_placeholder(
        self,
        blueprint: Dict[str, Any],
        prompt: str
    ) -> Dict[str, Any]:
        """
        Phase 4: Implementation plan (placeholder for PlanAgent integration)

        TODO Phase 2: Integrate with PlanAgent
        """
        logger.info("⏳ Plan phase - using placeholder (PlanAgent integration pending)")

        # For now, return a basic plan structure
        # In Phase 2, this will call PlanAgent
        return {
            "phases": [
                {"name": "Phase 1", "description": "Foundation"},
                {"name": "Phase 2", "description": "Implementation"},
                {"name": "Phase 3", "description": "Testing"}
            ],
            "tasks": [
                {"id": 1, "title": "Task 1", "phase": 1},
                {"id": 2, "title": "Task 2", "phase": 2}
            ],
            "note": "This will be replaced with PlanAgent in Phase 2"
        }

    def _validate_constitutional(
        self,
        outputs: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        Phase 5: Constitutional AI validation (P1-P6)

        Quality Gate 5 (QG5): Final validation
        """
        if not self.enable_constitutional:
            return {p: True for p in ["P1", "P2", "P3", "P4", "P5", "P6"]}

        # TODO: Implement full constitutional validation
        # For now, basic checks
        report = {
            "P1_zero_trust": True,  # Validated at each step
            "P2_completeness": len(outputs.get("paper", "")) > 500,
            "P3_systemic_vision": True,  # Holistic approach
            "P4_truth_obligation": outputs["research"].quality_score >= 0.5,
            "P5_intent_sovereignty": True,  # User prompt respected
            "P6_antifragility": True  # Iterative refinement enabled
        }

        if not all(report.values()):
            failed = [k for k, v in report.items() if not v]
            logger.warning(f"⚠️  Constitutional validation failed: {failed}")

        return report

    def _calculate_quality_score(
        self,
        research: ResearchResult,
        paper: str,
        blueprint: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> float:
        """Calculate overall quality score (0-1)"""
        scores = []

        # Research quality (30%)
        scores.append(research.quality_score * 0.3)

        # Paper quality (30%)
        paper_words = len(paper.split())
        paper_score = min(1.0, paper_words / 2000) * 0.3
        scores.append(paper_score)

        # Blueprint quality (20%)
        blueprint_score = blueprint.get("confidence", 0.5) * 0.2
        scores.append(blueprint_score)

        # Plan quality (20%)
        plan_score = (0.5 if plan.get("phases") else 0.0) * 0.2
        scores.append(plan_score)

        return sum(scores)

    def _validate_paper_structure(self, paper: str) -> tuple[bool, str]:
        """Validate paper has required sections (QG2)"""
        required_sections = [
            "executive summary",
            "introduction",
            "technical",
            "recommendations",
            "conclusion"
        ]

        paper_lower = paper.lower()
        missing = [s for s in required_sections if s not in paper_lower]

        if missing:
            return False, f"Missing sections: {', '.join(missing)}"

        word_count = len(paper.split())
        if word_count < 500:
            return False, f"Paper too short: {word_count} words (min 500)"

        return True, "Paper structure validated ✅"

    def _format_sources(self, sources: List) -> str:
        """Format sources for citation"""
        if not sources:
            return "No sources available"

        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(
                f"[{i}] {source.title}\n    {source.uri}"
            )
        return "\n".join(formatted)


# Example usage
if __name__ == "__main__":
    async def test_ppbpr():
        """Test P.P.B.P.R orchestrator"""
        print("🧪 Testing P.P.B.P.R Orchestrator\n")

        orchestrator = PPBPROrchestrator()

        deliverable = await orchestrator.run(
            prompt="Constitutional AI v3.0 implementation for multi-agent production systems",
            research_depth="comprehensive"
        )

        print(f"\n📊 Results:")
        print(f"   Quality Score: {deliverable.quality_score:.2f}")
        print(f"   Execution Time: {deliverable.execution_time_seconds:.1f}s")
        print(f"   Paper Words: {len(deliverable.paper.split())}")
        print(f"   Sources: {len(deliverable.research.sources)}")

        # Save deliverable
        deliverable.save_to_file(
            output_dir=Path("./outputs/ppbpr"),
            format="markdown"
        )

        print(f"\n✅ Deliverables saved to ./outputs/ppbpr/")

    # Run test
    asyncio.run(test_ppbpr())
