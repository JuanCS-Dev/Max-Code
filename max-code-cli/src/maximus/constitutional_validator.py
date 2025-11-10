"""Constitutional AI Validator - Lei Zero + Lei I"""
import logging
from dataclasses import dataclass
from typing import List, Optional
from .backend_client import MaximusClient

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    valid: bool
    violations: List[str]
    lei_zero_compliant: bool
    lei_i_compliant: bool
    vulnerable_populations_impact: Optional[str]
    confidence: float

class ConstitutionalValidator:
    """Validate against VÉRTICE Constitution (Claude Extended Thinking)"""
    def __init__(self, client: Optional[MaximusClient] = None):
        self.client = client or MaximusClient()
        self._owns_client = client is None
    
    async def validate_against_lei_zero(self, task: str) -> bool:
        """Lei Zero: Imago Dei + Dignidade humana"""
        result = await self.client.call_service("constitutional-ai", {
            "task": task, "lei": "zero", "extended_thinking": True
        })
        return result.get("compliant", False)
    
    async def validate_against_lei_i(self, task: str) -> bool:
        """Lei I: Subordinação à Lei Zero"""
        result = await self.client.call_service("constitutional-ai", {
            "task": task, "lei": "i", "extended_thinking": True
        })
        return result.get("compliant", False)
    
    async def check_vulnerable_populations(self, task: str) -> Optional[str]:
        """Check impact on vulnerable populations"""
        result = await self.client.call_service("constitutional-ai", {
            "task": task, "check": "vulnerable_populations"
        })
        return result.get("impact")
    
    async def validate(self, task: str) -> ValidationResult:
        """Full constitutional validation"""
        lei_zero = await self.validate_against_lei_zero(task)
        lei_i = await self.validate_against_lei_i(task)
        vulnerable = await self.check_vulnerable_populations(task)
        violations = []
        if not lei_zero: violations.append("Lei Zero violation")
        if not lei_i: violations.append("Lei I violation")
        return ValidationResult(
            valid=lei_zero and lei_i,
            violations=violations,
            lei_zero_compliant=lei_zero,
            lei_i_compliant=lei_i,
            vulnerable_populations_impact=vulnerable,
            confidence=0.95 if lei_zero and lei_i else 0.6
        )
    
    async def close(self):
        if self._owns_client: await self.client.close()
