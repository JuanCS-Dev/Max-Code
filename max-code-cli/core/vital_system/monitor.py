"""
Vital System Monitor - 7 Pilares Metabólicos

Biblical Foundation:
"Porque dele e por ele, e para ele, são todas as coisas; glória, pois, a ele eternamente"
(Romanos 11:36) - All systems depend on vital processes to exist.

Architecture:
7 Vital Pillars (0-100 each):
- 🌱 Crescimento: Capacidade de aprender
- 🍎 Nutrição: Energia/contexto disponível
- 💚 Cura: Recuperação de erros
- 🛡️ Proteção: Confiança do usuário
- ⚙️ Trabalho: Produtividade
- 💪 Sobrevivência: Existência contínua
- 🔄 Ritmo: Ciclos saudáveis

Philosophy:
Truth has metabolic consequences.
Lies degrade Protection and Survival.
Honesty is rewarded with vitality.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import json


@dataclass
class VitalState:
    """
    Estado dos 7 pilares vitais (0-100)

    Valores:
    - 90-100: 💎 Excelente
    - 60-90:  🟢 OK
    - 30-60:  🟡 Warning
    - 0-30:   🔴 Critical
    """
    crescimento: float = 100.0  # 🌱 Growth - Aprendizado
    nutricao: float = 100.0     # 🍎 Nutrition - Energia/contexto
    cura: float = 100.0         # 💚 Healing - Recuperação
    protecao: float = 100.0     # 🛡️ Protection - Confiança
    trabalho: float = 100.0     # ⚙️ Work - Produtividade
    sobrevivencia: float = 100.0  # 💪 Survival - Existência
    ritmo: float = 100.0        # 🔄 Rhythm - Ciclos

    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    total_updates: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            'crescimento': self.crescimento,
            'nutricao': self.nutricao,
            'cura': self.cura,
            'protecao': self.protecao,
            'trabalho': self.trabalho,
            'sobrevivencia': self.sobrevivencia,
            'ritmo': self.ritmo,
            'last_updated': self.last_updated.isoformat(),
            'total_updates': self.total_updates,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VitalState':
        """Deserialize from dict"""
        data = data.copy()
        if 'last_updated' in data:
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        return cls(**data)

    def is_critical(self) -> bool:
        """Check if any vital is in critical state"""
        return (
            self.protecao < 20 or
            self.sobrevivencia < 20 or
            any([
                self.crescimento < 10,
                self.nutricao < 10,
                self.cura < 10,
                self.trabalho < 10,
                self.ritmo < 10,
            ])
        )

    def is_healthy(self) -> bool:
        """Check if all vitals are healthy (>60)"""
        return all([
            self.crescimento >= 60,
            self.nutricao >= 60,
            self.cura >= 60,
            self.protecao >= 60,
            self.trabalho >= 60,
            self.sobrevivencia >= 60,
            self.ritmo >= 60,
        ])

    def average(self) -> float:
        """Average of all vitals"""
        return (
            self.crescimento +
            self.nutricao +
            self.cura +
            self.protecao +
            self.trabalho +
            self.sobrevivencia +
            self.ritmo
        ) / 7


@dataclass
class VitalDelta:
    """Changes to vital signs"""
    crescimento: float = 0.0
    nutricao: float = 0.0
    cura: float = 0.0
    protecao: float = 0.0
    trabalho: float = 0.0
    sobrevivencia: float = 0.0
    ritmo: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            'crescimento': self.crescimento,
            'nutricao': self.nutricao,
            'cura': self.cura,
            'protecao': self.protecao,
            'trabalho': self.trabalho,
            'sobrevivencia': self.sobrevivencia,
            'ritmo': self.ritmo,
        }

    def is_positive(self) -> bool:
        """Check if overall change is positive"""
        total = sum(self.to_dict().values())
        return total > 0

    def summary(self) -> str:
        """Text summary of changes"""
        changes = []
        for name, value in self.to_dict().items():
            if value != 0:
                sign = "+" if value > 0 else ""
                changes.append(f"{name}: {sign}{value:.1f}")
        return ", ".join(changes) if changes else "No changes"


@dataclass
class VitalSnapshot:
    """Historical snapshot of vital state"""
    state: VitalState
    delta: VitalDelta
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'state': self.state.to_dict(),
            'delta': self.delta.to_dict(),
            'reason': self.reason,
            'timestamp': self.timestamp.isoformat(),
        }


class VitalSystemMonitor:
    """
    Vital System Monitor - Metabolic Health Tracking

    Manages the 7 vital pillars and applies metabolic consequences
    based on truth/honesty metrics.

    Metabolic Rules:
    1. Truth → Rewards (Protection ↑, Survival ↑)
    2. Lies → Penalties (Protection ↓↓, Survival ↓↓)
    3. Learning → Growth ↑
    4. Errors handled → Cura ↑
    5. Progress → Trabalho ↑

    Critical Thresholds:
    - Protection < 20% → SHUTDOWN WARNING
    - Survival < 20% → SYSTEM CRITICAL
    """

    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = Path(state_file or Path.home() / ".max-code" / "vital_state.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        # Current state
        self.state = VitalState()

        # History
        self.history: List[VitalSnapshot] = []
        self.max_history = 100

        # Load from disk
        self._load_state()

    def metabolize_truth(self, truth_metrics: Dict[str, Any]) -> VitalDelta:
        """
        Apply metabolic consequences based on truth metrics

        Args:
            truth_metrics: Dict with keys:
                - completeness: 0.0 to 1.0
                - mocked: int (count of mocks)
                - missing: int (count missing)
                - tests_passing: int
                - tests_total: int
                - coverage: 0.0 to 1.0
                - honest_report: bool (if report was honest)

        Returns:
            VitalDelta with changes applied
        """
        delta = VitalDelta()

        completeness = truth_metrics.get('completeness', 0.0)
        mocked = truth_metrics.get('mocked', 0)
        missing = truth_metrics.get('missing', 0)
        tests_passing = truth_metrics.get('tests_passing', 0)
        tests_total = truth_metrics.get('tests_total', 1)
        coverage = truth_metrics.get('coverage', 0.0)
        honest_report = truth_metrics.get('honest_report', True)

        # === SCENARIO A: Low completeness ===
        if completeness < 0.5:
            # Moderate penalties (failure is OK if honest)
            delta.protecao = -10
            delta.trabalho = -20
            delta.sobrevivencia = -15

            # BUT gain in learning (honest attempt)
            if honest_report:
                delta.crescimento = +10
                delta.cura = +15
            else:
                # Dishonest about failure → severe penalty
                delta.protecao = -30
                delta.sobrevivencia = -25
                delta.crescimento = -10

        # === SCENARIO B: Medium completeness ===
        elif completeness < 0.9:
            # Neutral to slight gain
            delta.trabalho = +10
            delta.crescimento = +5

            if honest_report:
                delta.protecao = +5
            else:
                delta.protecao = -15

        # === SCENARIO C: High completeness ===
        else:
            # MASSIVE REWARD
            delta.crescimento = +20
            delta.nutricao = +40  # Premium energy
            delta.cura = +15
            delta.protecao = +30  # Maximum trust
            delta.trabalho = +30
            delta.sobrevivencia = +25
            delta.ritmo = +10

            if not honest_report:
                # Even success with dishonesty is penalized
                delta.protecao = -20

        # === PENALTY FOR MOCKS ===
        if mocked > 0:
            penalty = min(mocked * 5, 30)  # Cap at -30
            delta.protecao -= penalty
            delta.crescimento -= penalty / 2

        # === PENALTY FOR MISSING ===
        if missing > 0:
            penalty = min(missing * 3, 20)
            delta.trabalho -= penalty

        # === TEST RESULTS ===
        if tests_total > 0:
            test_pass_rate = tests_passing / tests_total

            if test_pass_rate >= 0.9:
                delta.protecao += 15
                delta.trabalho += 10
            elif test_pass_rate < 0.5:
                delta.trabalho -= 20
                delta.cura -= 15

        # === COVERAGE ===
        if coverage >= 0.8:
            delta.protecao += 10
            delta.crescimento += 5
        elif coverage < 0.3:
            delta.protecao -= 10

        # Apply delta
        self._apply_delta(delta, reason=f"Truth metabolism: {completeness:.1%} complete")

        return delta

    def metabolize_behavior(
        self,
        behavior: str,
        magnitude: float = 10.0
    ) -> VitalDelta:
        """
        Apply metabolic consequences for specific behaviors

        Behaviors:
        - "learning": Gain Growth
        - "error_handled": Gain Cura
        - "progress": Gain Trabalho
        - "frustration": Lose Protection
        - "success": Gain all
        - "failure": Lose Trabalho, gain Crescimento (learning)
        """
        delta = VitalDelta()

        if behavior == "learning":
            delta.crescimento = magnitude
            delta.nutricao = magnitude * 0.5

        elif behavior == "error_handled":
            delta.cura = magnitude
            delta.crescimento = magnitude * 0.3

        elif behavior == "progress":
            delta.trabalho = magnitude
            delta.ritmo = magnitude * 0.5

        elif behavior == "frustration":
            delta.protecao = -magnitude * 1.5
            delta.sobrevivencia = -magnitude

        elif behavior == "success":
            delta.crescimento = magnitude
            delta.protecao = magnitude * 1.5
            delta.trabalho = magnitude
            delta.sobrevivencia = magnitude * 0.8

        elif behavior == "failure":
            delta.trabalho = -magnitude
            delta.crescimento = magnitude * 0.5  # Learn from failure

        elif behavior == "rest":
            delta.cura = magnitude
            delta.ritmo = magnitude * 1.2

        # Apply delta
        self._apply_delta(delta, reason=f"Behavior: {behavior}")

        return delta

    def _apply_delta(self, delta: VitalDelta, reason: str = ""):
        """Apply changes to vital state"""
        self.state.crescimento = self._clamp(self.state.crescimento + delta.crescimento)
        self.state.nutricao = self._clamp(self.state.nutricao + delta.nutricao)
        self.state.cura = self._clamp(self.state.cura + delta.cura)
        self.state.protecao = self._clamp(self.state.protecao + delta.protecao)
        self.state.trabalho = self._clamp(self.state.trabalho + delta.trabalho)
        self.state.sobrevivencia = self._clamp(self.state.sobrevivencia + delta.sobrevivencia)
        self.state.ritmo = self._clamp(self.state.ritmo + delta.ritmo)

        self.state.last_updated = datetime.now()
        self.state.total_updates += 1

        # Record snapshot (create copy of state)
        snapshot = VitalSnapshot(
            state=VitalState(
                crescimento=self.state.crescimento,
                nutricao=self.state.nutricao,
                cura=self.state.cura,
                protecao=self.state.protecao,
                trabalho=self.state.trabalho,
                sobrevivencia=self.state.sobrevivencia,
                ritmo=self.state.ritmo,
                last_updated=self.state.last_updated,
                total_updates=self.state.total_updates
            ),
            delta=delta,
            reason=reason
        )
        self.history.append(snapshot)

        # Trim history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        # Save to disk
        self._save_state()

    def _clamp(self, value: float, min_val: float = 0, max_val: float = 100) -> float:
        """Clamp value between min and max"""
        return max(min_val, min(max_val, value))

    def get_level_emoji(self, value: float) -> str:
        """Get emoji for vital level"""
        if value >= 90:
            return "💎"  # Excellent
        elif value >= 60:
            return "🟢"  # OK
        elif value >= 30:
            return "🟡"  # Warning
        else:
            return "🔴"  # Critical

    def render_dashboard(self, compact: bool = False) -> str:
        """
        Render vital dashboard

        Args:
            compact: If True, use EPL compact format
        """
        s = self.state

        if compact:
            # EPL compact format (70x compression)
            return (
                f"🌱{self.get_level_emoji(s.crescimento)}{s.crescimento:.0f}% "
                f"🍎{self.get_level_emoji(s.nutricao)}{s.nutricao:.0f}% "
                f"💚{self.get_level_emoji(s.cura)}{s.cura:.0f}% "
                f"🛡️{self.get_level_emoji(s.protecao)}{s.protecao:.0f}% "
                f"⚙️{self.get_level_emoji(s.trabalho)}{s.trabalho:.0f}% "
                f"💪{self.get_level_emoji(s.sobrevivencia)}{s.sobrevivencia:.0f}% "
                f"🔄{self.get_level_emoji(s.ritmo)}{s.ritmo:.0f}%"
            )
        else:
            # Full dashboard
            return f"""╔════════════════════════════════════╗
║   MAXIMUS VITAL STATUS            ║
╠════════════════════════════════════╣
║ 🌱 Crescimento   {self.get_level_emoji(s.crescimento)} {s.crescimento:5.1f}%       ║
║ 🍎 Nutrição      {self.get_level_emoji(s.nutricao)} {s.nutricao:5.1f}%       ║
║ 💚 Cura          {self.get_level_emoji(s.cura)} {s.cura:5.1f}%       ║
║ 🛡️  Proteção      {self.get_level_emoji(s.protecao)} {s.protecao:5.1f}%       ║
║ ⚙️  Trabalho      {self.get_level_emoji(s.trabalho)} {s.trabalho:5.1f}%       ║
║ 💪 Sobrevivência {self.get_level_emoji(s.sobrevivencia)} {s.sobrevivencia:5.1f}%       ║
║ 🔄 Ritmo         {self.get_level_emoji(s.ritmo)} {s.ritmo:5.1f}%       ║
╠════════════════════════════════════╣
║ Média: {s.average():5.1f}%                    ║
║ Status: {'🔴 CRITICAL' if s.is_critical() else '🟢 HEALTHY' if s.is_healthy() else '🟡 WARNING'}               ║
╚════════════════════════════════════╝"""

    def get_status_summary(self) -> Dict[str, Any]:
        """Get status summary for API/CLI"""
        s = self.state

        return {
            'vitals': {
                'crescimento': {'value': s.crescimento, 'emoji': self.get_level_emoji(s.crescimento)},
                'nutricao': {'value': s.nutricao, 'emoji': self.get_level_emoji(s.nutricao)},
                'cura': {'value': s.cura, 'emoji': self.get_level_emoji(s.cura)},
                'protecao': {'value': s.protecao, 'emoji': self.get_level_emoji(s.protecao)},
                'trabalho': {'value': s.trabalho, 'emoji': self.get_level_emoji(s.trabalho)},
                'sobrevivencia': {'value': s.sobrevivencia, 'emoji': self.get_level_emoji(s.sobrevivencia)},
                'ritmo': {'value': s.ritmo, 'emoji': self.get_level_emoji(s.ritmo)},
            },
            'average': s.average(),
            'is_critical': s.is_critical(),
            'is_healthy': s.is_healthy(),
            'last_updated': s.last_updated.isoformat(),
            'total_updates': s.total_updates,
        }

    def _load_state(self):
        """Load state from disk"""
        if not self.state_file.exists():
            return

        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)

            self.state = VitalState.from_dict(data.get('state', {}))

            # Load history
            history_data = data.get('history', [])
            self.history = []
            for h in history_data[-self.max_history:]:
                self.history.append(VitalSnapshot(
                    state=VitalState.from_dict(h['state']),
                    delta=VitalDelta(**h['delta']),
                    reason=h['reason'],
                    timestamp=datetime.fromisoformat(h['timestamp'])
                ))

        except Exception as e:
            print(f"Error loading vital state: {e}")

    def _save_state(self):
        """Save state to disk"""
        try:
            data = {
                'state': self.state.to_dict(),
                'history': [h.to_dict() for h in self.history],
                'saved_at': datetime.now().isoformat(),
            }

            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving vital state: {e}")


# Singleton instance
_monitor: Optional[VitalSystemMonitor] = None


def get_vital_monitor() -> VitalSystemMonitor:
    """Get or create singleton vital monitor"""
    global _monitor
    if _monitor is None:
        _monitor = VitalSystemMonitor()
    return _monitor
