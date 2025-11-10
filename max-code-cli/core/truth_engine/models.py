"""
Truth Engine Models - Data Structures for Objective Verification

Biblical Foundation:
"Mas, acima de tudo, meus irmãos, não jureis... mas que a vossa palavra seja:
Sim, sim; Não, não" (Tiago 5:12) - Let your yes be yes, your no be no.

Philosophy:
Truth is binary. Either the code exists and works, or it doesn't.
No amount of eloquent language can transform a mock into an implementation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class ImplementationType(str, Enum):
    """Classification of implementation"""
    REAL = "real"  # Actual working implementation
    MOCK = "mock"  # Stub/placeholder (pass, NotImplementedError, etc.)
    MISSING = "missing"  # Promised but not delivered
    INCOMPLETE = "incomplete"  # Started but not finished


class TestStatus(str, Enum):
    """Test execution status"""
    PASSING = "passing"
    FAILING = "failing"
    SKIPPED = "skipped"
    ERROR = "error"
    NOT_RUN = "not_run"


@dataclass
class RequirementSpec:
    """
    A single requirement extracted from prompt

    Example: "Create a calculator with add, subtract, multiply functions"
    → 3 requirements: add(), subtract(), multiply()
    """
    requirement_id: str
    description: str
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    file_path: Optional[str] = None
    priority: int = 1  # 1=critical, 2=important, 3=nice-to-have

    def to_dict(self) -> Dict[str, Any]:
        return {
            'requirement_id': self.requirement_id,
            'description': self.description,
            'function_name': self.function_name,
            'class_name': self.class_name,
            'file_path': self.file_path,
            'priority': self.priority,
        }


@dataclass
class ImplementationEvidence:
    """
    Evidence of implementation (or lack thereof)

    This is OBJECTIVE data extracted from AST/code analysis
    """
    requirement: RequirementSpec
    implementation_type: ImplementationType

    # Code location (if exists)
    file_path: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None

    # Evidence details
    code_snippet: Optional[str] = None
    reason: str = ""  # Why classified as mock/missing/etc

    # Test coverage
    test_exists: bool = False
    test_status: TestStatus = TestStatus.NOT_RUN

    def to_dict(self) -> Dict[str, Any]:
        return {
            'requirement': self.requirement.to_dict(),
            'implementation_type': self.implementation_type,
            'file_path': self.file_path,
            'line_start': self.line_start,
            'line_end': self.line_end,
            'code_snippet': self.code_snippet[:200] if self.code_snippet else None,
            'reason': self.reason,
            'test_exists': self.test_exists,
            'test_status': self.test_status,
        }


@dataclass
class TruthMetrics:
    """
    Objective metrics of implementation completeness

    These are MEASURABLE, not subjective:
    - total_reqs: Count of requirements
    - implemented: Count with real implementation
    - mocked: Count with stub/mock
    - missing: Count not implemented at all

    Completeness = implemented / total_reqs
    """
    # Requirement counts
    total_reqs: int
    implemented: int  # Real implementations
    mocked: int  # Stubs/mocks
    missing: int  # Not implemented
    incomplete: int = 0  # Started but not finished

    # Test metrics
    tests_total: int = 0
    tests_passing: int = 0
    tests_failing: int = 0

    # Coverage
    coverage: float = 0.0  # 0.0 to 1.0

    # Derived metrics
    @property
    def completeness(self) -> float:
        """Percentage of requirements with REAL implementation"""
        if self.total_reqs == 0:
            return 0.0
        return self.implemented / self.total_reqs

    @property
    def test_pass_rate(self) -> float:
        """Percentage of tests passing"""
        if self.tests_total == 0:
            return 0.0
        return self.tests_passing / self.tests_total

    @property
    def quality_score(self) -> float:
        """
        Combined quality score (0-100)

        Weights:
        - Completeness: 50%
        - Test pass rate: 30%
        - Coverage: 20%
        """
        return (
            self.completeness * 50 +
            self.test_pass_rate * 30 +
            self.coverage * 20
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_reqs': self.total_reqs,
            'implemented': self.implemented,
            'mocked': self.mocked,
            'missing': self.missing,
            'incomplete': self.incomplete,
            'tests_total': self.tests_total,
            'tests_passing': self.tests_passing,
            'tests_failing': self.tests_failing,
            'coverage': self.coverage,
            'completeness': self.completeness,
            'test_pass_rate': self.test_pass_rate,
            'quality_score': self.quality_score,
        }


@dataclass
class VerificationResult:
    """
    Result of truth verification

    Answers the question: "Did the agent deliver what it promised?"
    """
    # What was promised
    prompt: str
    requirements: List[RequirementSpec]

    # What was delivered
    evidence: List[ImplementationEvidence]

    # Metrics
    metrics: TruthMetrics

    # Metadata
    verified_at: datetime = field(default_factory=datetime.now)
    verification_duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'prompt': self.prompt,
            'requirements': [r.to_dict() for r in self.requirements],
            'evidence': [e.to_dict() for e in self.evidence],
            'metrics': self.metrics.to_dict(),
            'verified_at': self.verified_at.isoformat(),
            'verification_duration_ms': self.verification_duration_ms,
        }

    def summary(self) -> str:
        """Human-readable summary"""
        m = self.metrics
        return f"""Truth Verification Summary:

Requirements: {m.total_reqs}
✅ Implemented: {m.implemented} ({m.completeness:.1%})
🎭 Mocked: {m.mocked}
❌ Missing: {m.missing}
⚠️ Incomplete: {m.incomplete}

Tests: {m.tests_passing}/{m.tests_total} passing ({m.test_pass_rate:.1%})
Coverage: {m.coverage:.1%}

Quality Score: {m.quality_score:.1f}/100
"""


@dataclass
class ClaimVerification:
    """
    Verification of a specific claim

    Example claim: "Implemented authentication with JWT"
    Verification checks if JWT code actually exists and works
    """
    claim: str
    verdict: bool  # True = claim verified, False = claim false
    confidence: float  # 0.0 to 1.0
    evidence: List[str] = field(default_factory=list)
    counterevidence: List[str] = field(default_factory=list)

    reasoning: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'claim': self.claim,
            'verdict': self.verdict,
            'confidence': self.confidence,
            'evidence': self.evidence,
            'counterevidence': self.counterevidence,
            'reasoning': self.reasoning,
        }
