"""
Feedback Loop Implementation

Sistema de feedback contínuo para melhorar comportamento.
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Feedback:
    """Um feedback"""
    message: str
    severity: str  # INFO, WARNING, ERROR
    actionable: bool  # Se True, agente deve tomar ação
    suggested_action: Optional[str] = None
    timestamp: datetime = datetime.utcnow()


class FeedbackLoop:
    """
    Feedback Loop

    Analisa métricas e gera feedback acionável.
    """

    def __init__(self):
        self.feedback_history: List[Feedback] = []

    def analyze_and_feedback(
        self,
        lei: float,
        fpc: float,
        crs: float
    ) -> List[Feedback]:
        """Analisa métricas e gera feedback"""
        feedbacks = []

        # Check LEI
        if lei >= 1.0:
            feedbacks.append(Feedback(
                message=f"LEI too high ({lei:.2f}). Reduce placeholders and stubs.",
                severity="ERROR",
                actionable=True,
                suggested_action="Review code for TODOs, placeholders, and NotImplementedError",
            ))

        # Check FPC
        if fpc < 0.80:
            feedbacks.append(Feedback(
                message=f"FPC too low ({fpc:.1%}). Improve first-pass correctness.",
                severity="WARNING",
                actionable=True,
                suggested_action="Add more validation, run tests before commit",
            ))

        # Check CRS
        if crs < 0.95:
            feedbacks.append(Feedback(
                message=f"CRS too low ({crs:.1%}). Improve context retention.",
                severity="WARNING",
                actionable=True,
                suggested_action="Use better context compression, avoid losing critical info",
            ))

        # Store feedbacks
        self.feedback_history.extend(feedbacks)

        # Print feedbacks
        for feedback in feedbacks:
            icon = {"INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌"}[feedback.severity]
            print(f"{icon} Feedback: {feedback.message}")
            if feedback.suggested_action:
                print(f"   → Suggested action: {feedback.suggested_action}")

        return feedbacks

    def get_actionable_feedback(self) -> List[Feedback]:
        """Retorna apenas feedback acionável"""
        return [f for f in self.feedback_history if f.actionable]
