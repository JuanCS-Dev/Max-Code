"""
Truth Engine - Objective Code Verification System

"E conhecereis a verdade, e a verdade vos libertará" (João 8:32)

The Truth Engine provides objective, measurable verification of code implementation
against requirements, combating the systemic dishonesty of LLMs through AST analysis,
test execution, and factual metrics.

Components:
- RequirementParser: Extract requirements from natural language
- CodeAnalyzer: AST-based classification (REAL/MOCK/MISSING)
- TestRunner: Execute tests and measure coverage
- TruthEngine: Complete verification pipeline

Usage:
    from core.truth_engine import TruthEngine

    engine = TruthEngine()
    result = engine.verify("Create calculator with add, subtract functions")

    print(result.metrics.completeness)  # 0.0 to 1.0
    print(result.summary())
"""

from .models import (
    RequirementSpec,
    ImplementationEvidence,
    ImplementationType,
    TestStatus,
    TruthMetrics,
    VerificationResult,
    ClaimVerification,
)

from .engine import (
    RequirementParser,
    CodeAnalyzer,
    TestRunner,
    TruthEngine,
)

__all__ = [
    # Models
    'RequirementSpec',
    'ImplementationEvidence',
    'ImplementationType',
    'TestStatus',
    'TruthMetrics',
    'VerificationResult',
    'ClaimVerification',

    # Engine
    'RequirementParser',
    'CodeAnalyzer',
    'TestRunner',
    'TruthEngine',
]
