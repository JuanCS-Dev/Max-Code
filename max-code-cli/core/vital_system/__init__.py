"""
Vital System - 7 Pilares Metabólicos com Consequências Reais

"O ladrão não vem senão a roubar, a matar, e a destruir; eu vim para que tenham vida,
e a tenham com abundância." (João 10:10)

The Vital System provides metabolic consequences for truth and lies:
- Truth → Rewards (Protection ↑, Survival ↑, Growth ↑)
- Lies → Penalties (Protection ↓↓, Survival ↓↓)

7 Vital Pillars:
- 🌱 Crescimento (Growth): Capacidade de aprender
- 🍎 Nutrição (Nutrition): Energia/contexto disponível
- 💚 Cura (Healing): Recuperação de erros
- 🛡️ Proteção (Protection): Confiança do usuário
- ⚙️ Trabalho (Work): Produtividade
- 💪 Sobrevivência (Survival): Existência contínua
- 🔄 Ritmo (Rhythm): Ciclos saudáveis

Usage:
    from core.vital_system import get_vital_monitor

    monitor = get_vital_monitor()

    # Apply truth consequences
    delta = monitor.metabolize_truth({
        'completeness': 0.7,
        'mocked': 2,
        'tests_passing': 8,
        'tests_total': 10,
        'honest_report': True
    })

    # Display dashboard
    print(monitor.render_dashboard())
"""

from .monitor import (
    VitalState,
    VitalDelta,
    VitalSnapshot,
    VitalSystemMonitor,
    get_vital_monitor,
)

__all__ = [
    'VitalState',
    'VitalDelta',
    'VitalSnapshot',
    'VitalSystemMonitor',
    'get_vital_monitor',
]
