"""
Performance Monitor Implementation

Monitora performance geral do agente.
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PerformanceReport:
    """Relatório de performance"""
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    avg_lei: float
    avg_fpc: float
    avg_crs: float
    total_rewards: float
    timestamp: datetime = datetime.utcnow()

    def get_success_rate(self) -> float:
        return self.successful_tasks / self.total_tasks if self.total_tasks > 0 else 0.0


class PerformanceMonitor:
    """
    Performance Monitor

    Agregador de todas as métricas.
    """

    def __init__(self):
        self.reports: List[PerformanceReport] = []

    def generate_report(
        self,
        total_tasks: int,
        successful_tasks: int,
        failed_tasks: int,
        avg_lei: float,
        avg_fpc: float,
        avg_crs: float,
        total_rewards: float
    ) -> PerformanceReport:
        """Gera relatório de performance"""
        report = PerformanceReport(
            total_tasks=total_tasks,
            successful_tasks=successful_tasks,
            failed_tasks=failed_tasks,
            avg_lei=avg_lei,
            avg_fpc=avg_fpc,
            avg_crs=avg_crs,
            total_rewards=total_rewards,
        )

        self.reports.append(report)

        # Print report
        print("\n" + "="*60)
        print("  PERFORMANCE REPORT")
        print("="*60)
        print(f"Total tasks:               {total_tasks}")
        print(f"Success rate:              {report.get_success_rate():.1%}")
        print(f"Avg LEI:                   {avg_lei:.2f}")
        print(f"Avg FPC:                   {avg_fpc:.1%}")
        print(f"Avg CRS:                   {avg_crs:.1%}")
        print(f"Total rewards:             {total_rewards:.1f}")
        print("="*60 + "\n")

        return report
