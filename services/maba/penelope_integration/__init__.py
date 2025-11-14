"""PENELOPE Integration Package.

Day 5: Integrating MABA browser automation with PENELOPE intelligence.

PENELOPE (nome da filha do criador) é o cérebro que une browser automation
com inteligência artificial, trazendo:
- Análise inteligente de páginas web
- Vision capabilities para screenshots
- Auto-healing quando ações falham
- Navegação inteligente baseada em contexto
- Reasoning sobre estrutura de páginas

"A sabedoria de PENELOPE guia o navegador através da web."

Author: Vértice Platform Team
License: Proprietary
"""
from .client import PenelopeClient
from .analyzer import PageAnalyzer
from .auto_healing import AutoHealer

__all__ = [
    "PenelopeClient",
    "PageAnalyzer",
    "AutoHealer",
]
