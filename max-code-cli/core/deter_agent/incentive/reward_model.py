"""
Reward Model Implementation

Sistema de recompensas para guiar comportamento do agente.

"Bem está, servo bom e fiel..." (Mateus 25:21)
"""

from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class RewardType(Enum):
    """Tipo de recompensa"""
    POSITIVE = "positive"  # Comportamento bom
    NEGATIVE = "negative"  # Comportamento ruim
    NEUTRAL = "neutral"


@dataclass
class Reward:
    """Uma recompensa"""
    type: RewardType
    points: float
    reason: str
    timestamp: datetime = datetime.utcnow()


class RewardModel:
    """
    Reward Model

    RECOMPENSAS POSITIVAS:
    - FPC alto (+10 points)
    - LEI baixo (+10 points)
    - Tests passando (+5 points)
    - TDD seguido (+15 points)

    RECOMPENSAS NEGATIVAS:
    - FPC baixo (-10 points)
    - LEI alto (-10 points)
    - Tests falhando (-5 points)
    - TDD violado (-15 points)
    """

    def __init__(self):
        self.total_points = 0
        self.rewards_history = []

    def reward(self, reward: Reward):
        """Aplica recompensa"""
        self.total_points += reward.points
        self.rewards_history.append(reward)
        print(f"🎁 Reward: {reward.points:+.1f} points - {reward.reason}")

    def get_total_points(self) -> float:
        return self.total_points
