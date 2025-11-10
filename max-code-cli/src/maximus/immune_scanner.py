"""Immune System Scanner - 8 cells parallel (OpenAI)"""
import asyncio, logging
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum
from .backend_client import MaximusClient

logger = logging.getLogger(__name__)

class CellType(Enum):
    T_CELL = "t-cell"
    B_CELL = "b-cell"
    NK_CELL = "nk-cell"
    MACROPHAGE = "macrophage"
    DENDRITIC = "dendritic"
    NEUTROPHIL = "neutrophil"
    EOSINOPHIL = "eosinophil"
    BASOPHIL = "basophil"

@dataclass
class SecurityReport:
    safe: bool
    threats: List[str]
    cell_results: Dict[str, Dict]
    overall_risk: str
    confidence: float

class ImmuneScanner:
    """8-cell biomimetic security (parallel with OpenAI)"""
    def __init__(self, client=None):
        self.client = client or MaximusClient()
        self._owns_client = client is None
    
    async def scan_with_8_cells(self, artifact: str) -> SecurityReport:
        """Parallel scan with 8 immune cells"""
        tasks = [self._scan_cell(cell, artifact) for cell in CellType]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        cell_results = {cell.value: (r if not isinstance(r, Exception) else {"error": str(r)}) for cell, r in zip(CellType, results)}
        threats = [t for r in cell_results.values() if isinstance(r, dict) for t in r.get("threats", [])]
        return SecurityReport(
            safe=len(threats) == 0,
            threats=threats,
            cell_results=cell_results,
            overall_risk="low" if len(threats) == 0 else ("medium" if len(threats) < 3 else "high"),
            confidence=0.9
        )
    
    async def _scan_cell(self, cell: CellType, artifact: str) -> Dict:
        service = f"immune-{cell.value}"
        return await self.client.call_service(service, {"artifact": artifact})
    
    async def close(self):
        if self._owns_client: await self.client.close()
