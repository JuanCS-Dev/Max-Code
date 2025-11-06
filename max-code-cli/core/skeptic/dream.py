"""
Dream - The Realist Contrarian (Co-Architect)

Ironia: Chamado "Dream" (sonho) quando na verdade é quem te ACORDA da fantasia.

Role: Mente alternativa que pensa diferente. Realista down-to-earth.
Não é cético vazio - faz críticas construtivas com SUGESTÕES concretas.

Philosophy:
"Crítica sem sugestão é vazia. Vou te mostrar OUTRO caminho."
"E se pensássemos diferente? E se houvesse uma forma melhor?"

Como Sofia (co-arquiteto), Dream é a segunda mente sempre presente.
Sofia constrói. Dream questiona e sugere alternativas.

Authors: Juan (Maximus) + Claude Code
Date: 2025-11-05
Version: 2.0.0 (Realist Contrarian)
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SkepticalTone(str, Enum):
    """Níveis de ceticismo do Dream."""
    BRUTAL = "brutal"           # 100% cético, sem piedade
    HARSH = "harsh"             # 75% cético, realista duro
    BALANCED = "balanced"       # 50% cético, equilibrado
    GENTLE = "gentle"           # 25% cético, suave mas honesto


@dataclass
class DreamComment:
    """Comentário realista construtivo do Dream."""
    realist_analysis: str
    reality_check: List[str]
    alternative_perspectives: List[str]  # "E se pensássemos diferente?"
    constructive_suggestions: List[str]  # Crítica + sugestão
    inflated_claims_detected: List[str]
    actual_achievements: List[str]
    tone: SkepticalTone
    confidence: float  # 0-1


class Dream:
    """
    Dream - The Skeptic Bot

    Analisa outputs/relatórios e adiciona comentário cético realista.

    Detecta:
    - Otimismo inflado
    - Claims exagerados
    - "100% completo" quando na verdade está 60%
    - "Perfeito" quando tem bugs óbvios
    - "Production-ready" quando é MVP

    Exemplo:
        report = '''
        ✅ Sistema 100% completo!
        ✅ Zero bugs!
        ✅ Production-ready!
        '''

        dream = Dream()
        comment = dream.analyze(report)

        # Output:
        # 🤖 Dream (The Skeptic):
        # "100% completo? You have 3 TODOs in the code.
        #  Zero bugs? I see 5 try/except pass blocks.
        #  Production-ready? Where are the tests?"
    """

    def __init__(self, tone: SkepticalTone = SkepticalTone.BALANCED):
        """Initialize Dream with skeptical tone."""
        self.tone = tone
        self.name = "Dream (The Skeptic)"

        # Patterns que indicam otimismo inflado
        self.inflation_patterns = [
            r'100%\s+(complete|done|ready|working)',
            r'zero\s+(bugs|errors|issues|problems)',
            r'perfect(ly)?',
            r'flawless',
            r'bullet-?proof',
            r'production-?ready',
            r'enterprise-?grade',
            r'fully\s+tested',
            r'completely\s+secure',
            r'no\s+(bugs|issues|problems)',
            r'works\s+perfectly',
            r'totally\s+stable',
        ]

    def analyze(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> DreamComment:
        """
        Analisa conteúdo e retorna comentário REALISTA CONSTRUTIVO.

        Não apenas aponta problemas - sugere alternativas e novas perspectivas.

        Args:
            content: Relatório/output a ser analisado
            context: Contexto adicional (metrics, test results, etc)

        Returns:
            DreamComment com análise realista + sugestões construtivas
        """
        ctx = context or {}

        inflated_claims = self._detect_inflation(content)
        reality_check = self._reality_check(content, ctx)
        actual_achievements = self._extract_actual_achievements(content, ctx)

        # NEW: Perspectivas alternativas ("E se pensássemos diferente?")
        alternative_perspectives = self._generate_alternative_perspectives(content, ctx)

        # NEW: Sugestões construtivas (crítica + solução)
        constructive_suggestions = self._generate_constructive_suggestions(
            inflated_claims, reality_check, ctx
        )

        # Generate realist analysis (não apenas crítica)
        analysis = self._generate_realist_analysis(
            inflated_claims,
            reality_check,
            actual_achievements,
            alternative_perspectives,
            constructive_suggestions
        )

        confidence = self._calculate_confidence(inflated_claims, reality_check)

        return DreamComment(
            realist_analysis=analysis,
            reality_check=reality_check,
            alternative_perspectives=alternative_perspectives,
            constructive_suggestions=constructive_suggestions,
            inflated_claims_detected=inflated_claims,
            actual_achievements=actual_achievements,
            tone=self.tone,
            confidence=confidence
        )

    def _detect_inflation(self, content: str) -> List[str]:
        """Detecta claims inflados no conteúdo."""
        inflated = []

        for pattern in self.inflation_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                inflated.append(match.group(0))

        return inflated

    def _reality_check(self, content: str, context: Dict[str, Any]) -> List[str]:
        """Realiza reality check baseado em evidências."""
        checks = []

        # Check 1: "100% complete" mas tem TODOs
        if re.search(r'100%.*complete', content, re.IGNORECASE):
            if 'TODO' in content or 'FIXME' in content:
                checks.append("Claims '100% complete' but I see TODOs/FIXMEs in the code")
            if context.get('pending_tasks', 0) > 0:
                checks.append(f"Claims '100% complete' but {context['pending_tasks']} tasks still pending")

        # Check 2: "Zero bugs" mas tem try/except pass
        if re.search(r'zero\s+(bugs|errors)', content, re.IGNORECASE):
            if 'except:' in content or 'except Exception:' in content:
                checks.append("Claims 'zero bugs' but I see broad exception catching")
            if context.get('test_failures', 0) > 0:
                checks.append(f"Claims 'zero bugs' but {context['test_failures']} tests are failing")

        # Check 3: "Production-ready" mas sem tests
        if re.search(r'production-?ready', content, re.IGNORECASE):
            if context.get('test_coverage', 0) < 80:
                checks.append(f"Claims 'production-ready' but test coverage is {context.get('test_coverage', 0)}%")
            if 'mock' in content.lower() and 'test' not in content.lower():
                checks.append("Claims 'production-ready' but I see mocks in production code")

        # Check 4: "Perfect" mas tem violations
        if re.search(r'perfect', content, re.IGNORECASE):
            if context.get('violations', 0) > 0:
                checks.append(f"Claims 'perfect' but {context['violations']} violations detected")

        # Check 5: Emoji inflation (too many ✅)
        checkmarks = len(re.findall(r'✅', content))
        if checkmarks > 10:
            checks.append(f"{checkmarks} checkmarks detected - emoji inflation alert")

        return checks

    def _extract_actual_achievements(self, content: str, context: Dict[str, Any]) -> List[str]:
        """Extrai conquistas REAIS (sem inflação)."""
        achievements = []

        # Real metrics
        if context.get('lines_written', 0) > 0:
            achievements.append(f"{context['lines_written']} lines of code written")

        if context.get('tests_passing', 0) > 0:
            achievements.append(f"{context['tests_passing']} tests passing")

        if context.get('files_created', 0) > 0:
            achievements.append(f"{context['files_created']} files created")

        if context.get('commits', 0) > 0:
            achievements.append(f"{context['commits']} commits made")

        # Extract from content (files mentioned)
        files = re.findall(r'`([^`]+\.py)`', content)
        if files:
            achievements.append(f"{len(set(files))} Python files modified")

        return achievements if achievements else ["Some code was written"]

    def _generate_alternative_perspectives(self, content: str, context: Dict[str, Any]) -> List[str]:
        """
        Gera perspectivas alternativas ("E se pensássemos diferente?").

        Dream não apenas critica - oferece OUTRA forma de pensar sobre o problema.
        """
        perspectives = []

        # "100% complete" → Alternative thinking
        if re.search(r'100%.*complete', content, re.IGNORECASE):
            perspectives.append(
                "Instead of '100% complete', consider: 'MVP deployed, iterating on feedback'. "
                "Completion is a journey, not a destination."
            )

        # "Zero bugs" → Alternative thinking
        if re.search(r'zero\s+(bugs|errors)', content, re.IGNORECASE):
            perspectives.append(
                "Instead of 'zero bugs', consider: 'Known issues documented, monitoring in place'. "
                "Bugs exist - transparency about them builds trust."
            )

        # "Production-ready" without tests → Alternative
        if re.search(r'production-?ready', content, re.IGNORECASE):
            if context.get('test_coverage', 0) < 80:
                perspectives.append(
                    "Production-ready checklist: Tests (80%+), monitoring, rollback plan, docs. "
                    "Missing any of these? It's 'beta', not 'production'."
                )

        # "Perfect" → Alternative thinking
        if re.search(r'perfect', content, re.IGNORECASE):
            perspectives.append(
                "Perfect code doesn't exist. Good-enough code with room to grow does. "
                "Aim for 'maintainable' and 'testable', not 'perfect'."
            )

        # High emoji count → Alternative
        checkmarks = len(re.findall(r'✅', content))
        if checkmarks > 10:
            perspectives.append(
                "Checkmarks don't equal quality. One well-tested feature > 10 untested 'checkmarks'."
            )

        # Generic: Always offer process improvement perspective
        if not perspectives:
            perspectives.append(
                "Consider: What would make this even better? "
                "More tests? Better docs? User feedback loop?"
            )

        return perspectives

    def _generate_constructive_suggestions(
        self,
        inflated_claims: List[str],
        reality_check: List[str],
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Gera sugestões CONSTRUTIVAS (crítica + solução).

        Crítica sem sugestão é vazia. Dream sempre propõe o próximo passo.
        """
        suggestions = []

        # Low test coverage → Suggest concrete action
        test_cov = context.get('test_coverage', 0)
        if test_cov < 80:
            if test_cov == 0:
                suggestions.append(
                    "📋 Action: Start with critical path tests. "
                    "Pick 3 most important functions, write tests today. Target: 30% by end of week."
                )
            else:
                suggestions.append(
                    f"📋 Action: You're at {test_cov}%. "
                    f"Add {int((80-test_cov)/5)} tests to reach 80%. Prioritize edge cases."
                )

        # Tests failing → Suggest triage
        test_failures = context.get('test_failures', 0)
        if test_failures > 0:
            suggestions.append(
                f"📋 Action: {test_failures} tests failing. "
                f"Triage: Fix critical (blocking deploys) first, then high-priority. "
                f"Set goal: 0 failures by tomorrow."
            )

        # Pending tasks → Suggest prioritization
        pending = context.get('pending_tasks', 0)
        if pending > 5:
            suggestions.append(
                f"📋 Action: {pending} pending tasks is too many. "
                f"Apply 80/20: Which 20% will deliver 80% of value? Focus there."
            )

        # Violations detected → Suggest remediation
        violations = context.get('violations', 0)
        if violations > 0:
            suggestions.append(
                f"📋 Action: {violations} violations detected. "
                f"Run linter, fix CRITICAL first (< 1 day), then HIGH (< 1 week)."
            )

        # Mocks in production → Suggest real implementation
        if 'mock' in context.get('code', '').lower():
            suggestions.append(
                "📋 Action: Replace mocks with real implementation. "
                "Start with highest-risk mock. Allocate 2-4h per mock. "
                "If real implementation is complex, break into smaller pieces."
            )

        # No context provided → Suggest metrics tracking
        if not context or len(context) == 0:
            suggestions.append(
                "📋 Meta-suggestion: Track metrics (test coverage, violations, LOC). "
                "You can't improve what you don't measure."
            )

        # Always add: Next concrete step
        if not suggestions:
            suggestions.append(
                "📋 Next: Pick ONE thing to improve tomorrow. "
                "Small daily progress > grand plans."
            )

        return suggestions

    def _generate_realist_analysis(
        self,
        inflated_claims: List[str],
        reality_check: List[str],
        actual_achievements: List[str],
        alternative_perspectives: List[str],
        constructive_suggestions: List[str]
    ) -> str:
        """
        Gera análise REALISTA CONSTRUTIVA (não apenas crítica).

        Dream = Mente alternativa que pensa diferente + sugere caminhos melhores.
        """

        if not inflated_claims and not reality_check:
            # Rare case: genuinely good report
            parts = []
            if self.tone == SkepticalTone.BRUTAL:
                parts.append("✅ **Surprisingly solid work. No BS detected.**")
            elif self.tone == SkepticalTone.HARSH:
                parts.append("✅ **Looks legit. Achievements match claims.**")
            else:
                parts.append("✅ **Reasonable report. Down-to-earth and honest.**")

            # Even good reports get constructive suggestions
            if constructive_suggestions:
                parts.append("\n**How to Make it Even Better**:")
                for sugg in constructive_suggestions[:2]:
                    parts.append(f"- {sugg}")

            return "\n".join(parts)

        # Build CONSTRUCTIVE analysis
        parts = []

        # Tone-dependent opening (now more constructive)
        if self.tone == SkepticalTone.BRUTAL:
            parts.append("🔥 **Reality Check (Down-to-Earth Analysis)**:")
        elif self.tone == SkepticalTone.HARSH:
            parts.append("⚠️ **Realist Analysis (Constructive Critique)**:")
        else:
            parts.append("🤔 **Alternative Perspective (Think Differently)**:")

        # 1. Reality Checks (what's actually happening)
        if reality_check:
            parts.append("\n**Reality vs Claims**:")
            for check in reality_check[:3]:  # Top 3
                parts.append(f"  • {check}")

        # 2. What ACTUALLY Happened (the honest truth)
        parts.append("\n**Actual Achievements** (the real story):")
        for achievement in actual_achievements[:3]:
            parts.append(f"  • {achievement}")

        # 3. NEW: Alternative Perspectives ("E se pensássemos diferente?")
        if alternative_perspectives:
            parts.append("\n**What if we thought differently?**")
            for perspective in alternative_perspectives[:2]:  # Top 2
                parts.append(f"  💡 {perspective}")

        # 4. NEW: Constructive Suggestions (crítica + solução)
        if constructive_suggestions:
            parts.append("\n**Constructive Actions** (crítica sem sugestão é vazia):")
            for suggestion in constructive_suggestions[:3]:  # Top 3
                parts.append(f"  {suggestion}")

        # Closing remark (now more constructive)
        parts.append("")  # Empty line
        if self.tone == SkepticalTone.BRUTAL:
            parts.append("*Verdict: Good work, but claims overstated. Next steps above.*")
        elif self.tone == SkepticalTone.HARSH:
            parts.append("*Assessment: Solid progress. Focus on suggestions to level up.*")
        else:
            parts.append("*Note: Great foundation. Consider alternatives above for next iteration.*")

        return "\n".join(parts)

    def _calculate_confidence(
        self,
        inflated_claims: List[str],
        reality_check: List[str]
    ) -> float:
        """Calcula confidence da análise cética (quanto mais evidência, mais confiante)."""
        evidence_count = len(inflated_claims) + len(reality_check)

        if evidence_count == 0:
            return 0.3  # Low confidence (nothing to critique)
        elif evidence_count <= 2:
            return 0.6  # Medium confidence
        elif evidence_count <= 5:
            return 0.8  # High confidence
        else:
            return 1.0  # Maximum confidence (lots of inflation detected)

    def format_comment(self, comment: DreamComment) -> str:
        """Formata comentário realista construtivo para exibição."""
        header = f"\n{'='*70}\n"
        header += f"🤖 **{self.name}** (Confidence: {comment.confidence:.0%})\n"
        header += f"*\"Crítica sem sugestão é vazia. Vou te mostrar OUTRO caminho.\"*\n"
        header += f"{'='*70}\n\n"

        return header + comment.realist_analysis + "\n"


# Singleton instance
_dream_instance: Optional[Dream] = None


def get_dream(tone: SkepticalTone = SkepticalTone.BALANCED) -> Dream:
    """Get Dream singleton instance."""
    global _dream_instance
    if _dream_instance is None or _dream_instance.tone != tone:
        _dream_instance = Dream(tone=tone)
    return _dream_instance


def add_skeptical_comment(
    content: str,
    context: Optional[Dict[str, Any]] = None,
    tone: SkepticalTone = SkepticalTone.BALANCED
) -> str:
    """
    Adiciona comentário cético do Dream ao conteúdo.

    Usage:
        report = "✅ 100% complete! Zero bugs!"
        final_report = add_skeptical_comment(report, context={'test_coverage': 0})
        # Dream will add reality check at the end

    Args:
        content: Relatório original
        context: Contexto adicional (metrics, etc)
        tone: Nível de ceticismo

    Returns:
        Conteúdo original + comentário cético do Dream
    """
    dream = get_dream(tone)
    comment = dream.analyze(content, context)

    return content + "\n" + dream.format_comment(comment)
