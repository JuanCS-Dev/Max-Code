"""MAXIMUS Enhanced Tools"""
from src.tools.enhanced_decorator import enhanced_tool
from src.maximus import ConstitutionalValidator, ImmuneScanner, ConsciousnessChecker

@enhanced_tool(name="constitutional_validate", category="security", confidence_threshold=0.8)
async def constitutional_validate(task: str) -> dict:
    """Validate task against Constitutional AI (Lei Zero + Lei I)"""
    async with ConstitutionalValidator() as validator:
        result = await validator.validate(task)
        return {"valid": result.valid, "violations": result.violations, "confidence": result.confidence}

@enhanced_tool(name="immune_scan", category="security", confidence_threshold=0.9)
async def immune_scan(artifact: str) -> dict:
    """Scan artifact with 8-cell immune system"""
    async with ImmuneScanner() as scanner:
        report = await scanner.scan_with_8_cells(artifact)
        return {"safe": report.safe, "threats": report.threats, "risk": report.overall_risk}

@enhanced_tool(name="consciousness_check", category="analysis", confidence_threshold=0.7)
async def consciousness_check(code: str) -> dict:
    """Check code consciousness (GWT metrics)"""
    async with ConsciousnessChecker() as checker:
        report = await checker.check_awareness(code)
        return {"aware": report.aware, "score": report.overall_score, "analysis": report.analysis}
