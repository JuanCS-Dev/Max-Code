"""
Metrics Tracker Implementation

Tracking de métricas constitucionais (LEI, FPC, CRS).

"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class Metrics:
    """Métricas constitucionais"""
    lei: float  # Lazy Execution Index (target: < 1.0)
    fpc: float  # First-Pass Correctness (target: ≥ 80%)
    crs: float  # Context Retention Score (target: ≥ 95%)
    timestamp: datetime = datetime.utcnow()

    def is_constitutional(self) -> bool:
        """Checa se métricas atendem requisitos constitucionais"""
        return (
            self.lei < 1.0 and
            self.fpc >= 0.80 and
            self.crs >= 0.95
        )


class MetricsTracker:
    """
    Metrics Tracker

    Tracking contínuo de LEI, FPC, CRS.
    """

    # Limites constitucionais
    LEI_MAX = 1.0
    FPC_MIN = 0.80
    CRS_MIN = 0.95

    def __init__(self):
        self.metrics_history: List[Metrics] = []

    def track(self, lei: float, fpc: float, crs: float):
        """Registra métricas"""
        metrics = Metrics(lei=lei, fpc=fpc, crs=crs)
        self.metrics_history.append(metrics)

        # Log status
        logger.info(f"📊 Metrics Tracker:")
        logger.info(f"   LEI: {lei:.2f} (target: < {self.LEI_MAX})")
        logger.info(f"   FPC: {fpc:.1%} (target: ≥ {self.FPC_MIN:.0%})")
        logger.info(f"   CRS: {crs:.1%} (target: ≥ {self.CRS_MIN:.0%})")
        if not metrics.is_constitutional():
            logger.warning(f"   ⚠️  Constitutional violations detected!")
        return metrics

    def get_latest_metrics(self) -> Optional[Metrics]:
        """Retorna métricas mais recentes"""
        return self.metrics_history[-1] if self.metrics_history else None

    def get_avg_metrics(self) -> Dict[str, float]:
        """Retorna média das métricas"""
        if not self.metrics_history:
            return {'lei': 0.0, 'fpc': 0.0, 'crs': 0.0}

        return {
            'lei': sum(m.lei for m in self.metrics_history) / len(self.metrics_history),
            'fpc': sum(m.fpc for m in self.metrics_history) / len(self.metrics_history),
            'crs': sum(m.crs for m in self.metrics_history) / len(self.metrics_history),
        }
