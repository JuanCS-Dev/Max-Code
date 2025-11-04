"""
Incentive Layer - DETER-AGENT Layer 5

OBJETIVO: Sistema de recompensas e métricas para guiar comportamento do agente.

MANDATO CONSTITUCIONAL:
- P6: LEI < 1.0 (Lazy Execution Index)
- P6: FPC ≥ 80% (First-Pass Correctness)
- P6: CRS ≥ 95% (Context Retention Score)

COMPONENTES:
1. Reward Model: Sistema de recompensas (bom comportamento = recompensa)
2. Metrics Tracker: Tracking de LEI, FPC, CRS
3. Performance Monitor: Monitora performance geral
4. Feedback Loop: Feedback para melhorar comportamento

FILOSOFIA:
- Incentivos corretos = comportamento correto
- Métricas objetivas (não subjetivas)
- Feedback loop contínuo
- Gamification (pontos, achievements)

"Bem está, servo bom e fiel. Sobre o pouco foste fiel, sobre muito te colocarei"
(Mateus 25:21)
"""

from .reward_model import RewardModel, Reward, RewardType
from .metrics_tracker import MetricsTracker, Metrics
from .performance_monitor import PerformanceMonitor, PerformanceReport
from .feedback_loop import FeedbackLoop, Feedback

__all__ = [
    # Reward Model
    'RewardModel',
    'Reward',
    'RewardType',

    # Metrics Tracker
    'MetricsTracker',
    'Metrics',

    # Performance Monitor
    'PerformanceMonitor',
    'PerformanceReport',

    # Feedback Loop
    'FeedbackLoop',
    'Feedback',
]
