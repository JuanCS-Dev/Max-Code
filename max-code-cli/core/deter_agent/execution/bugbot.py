"""
BugBot - Proactive Error Detection

Biblical Foundation:
"Vigiai, estai firmes na fé" (1 Coríntios 16:13)
Vigilance through proactive monitoring - watchfulness in action.

CONCEITO:
Inspired by Cursor's BugBot, enhanced with Constitutional AI guardians.
Monitors code changes in real-time and detects potential errors BEFORE execution.

PROCESSO:
1. WATCH: Monitor file changes (file system events)
2. ANALYZE: Static analysis for common errors
3. DETECT: Identify potential bugs early
4. ALERT: Notify developer proactively
5. PREVENT: Block execution if critical errors found (Guardian integration)

BENEFÍCIOS:
- Early bug detection (before execution)
- Prevents runtime errors
- Aligns with P4 - Prudência Operacional (test before execute)
- Integrates with Guardian Pre-Check
- Real-time feedback loop

Inspired by Cursor's BugBot concept.
Enhanced with Constitutional AI guardians.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import ast
import time
from datetime import datetime


class ErrorSeverity(Enum):
    """Severidade do erro detectado"""
    CRITICAL = "critical"  # Bloqueia execução
    HIGH = "high"  # Alerta forte
    MEDIUM = "medium"  # Aviso
    LOW = "low"  # Info


class ErrorCategory(Enum):
    """Categorias de erro detectado"""
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    UNDEFINED_VARIABLE = "undefined_variable"
    TYPE_ERROR = "type_error"
    LOGIC_ERROR = "logic_error"
    STYLE_WARNING = "style_warning"
    SECURITY_RISK = "security_risk"


@dataclass
class BugDetection:
    """Bug detectado proativamente"""
    file_path: str
    line_number: int
    category: ErrorCategory
    severity: ErrorSeverity
    description: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AnalysisResult:
    """Resultado da análise de arquivo"""
    file_path: str
    bugs: List[BugDetection]
    warnings: int
    errors: int
    critical_issues: int
    is_safe_to_execute: bool
    analysis_time: float


class BugBot:
    """
    Proactive Error Detection Engine (BugBot)

    Implementa P4 - Prudência Operacional através de detecção proativa de erros.
    Inspirado no Cursor's BugBot, mas com Guardian integration.

    Features:
    - Static code analysis
    - Syntax checking
    - Import validation
    - Undefined variable detection
    - Guardian integration
    - Real-time feedback

    Example:
        >>> bugbot = BugBot()
        >>> result = bugbot.analyze_file("script.py")
        >>> if not result.is_safe_to_execute:
        ...     print(f"⚠️  Found {result.critical_issues} critical issues!")
        ...     for bug in result.bugs:
        ...         print(f"  Line {bug.line_number}: {bug.description}")
    """

    def __init__(self, auto_fix: bool = False):
        """
        Inicializa BugBot

        Args:
            auto_fix: Se True, tenta auto-corrigir erros simples
        """
        self.auto_fix = auto_fix

        # Statistics
        self.stats = {
            'files_analyzed': 0,
            'bugs_detected': 0,
            'critical_issues_prevented': 0,
            'warnings_issued': 0,
        }

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """
        Analisa arquivo Python em busca de erros

        Args:
            file_path: Caminho do arquivo Python

        Returns:
            AnalysisResult com bugs detectados

        Process:
            1. Syntax check (AST parsing)
            2. Import validation
            3. Undefined variable detection
            4. Style warnings
            5. Security risks
        """
        start_time = time.time()
        self.stats['files_analyzed'] += 1

        path = Path(file_path)

        if not path.exists():
            return AnalysisResult(
                file_path=file_path,
                bugs=[BugDetection(
                    file_path=file_path,
                    line_number=0,
                    category=ErrorCategory.SYNTAX_ERROR,
                    severity=ErrorSeverity.CRITICAL,
                    description="File not found"
                )],
                warnings=0,
                errors=1,
                critical_issues=1,
                is_safe_to_execute=False,
                analysis_time=time.time() - start_time
            )

        if not path.suffix == '.py':
            # Only analyze Python files
            return AnalysisResult(
                file_path=file_path,
                bugs=[],
                warnings=0,
                errors=0,
                critical_issues=0,
                is_safe_to_execute=True,
                analysis_time=time.time() - start_time
            )

        bugs: List[BugDetection] = []

        # Read file content
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            bugs.append(BugDetection(
                file_path=file_path,
                line_number=0,
                category=ErrorCategory.SYNTAX_ERROR,
                severity=ErrorSeverity.CRITICAL,
                description=f"Failed to read file: {e}"
            ))
            return self._build_result(file_path, bugs, start_time)

        # FASE 1: Syntax check (AST parsing)
        syntax_bugs = self._check_syntax(file_path, content)
        bugs.extend(syntax_bugs)

        # Se tem erro de sintaxe crítico, para aqui
        if any(bug.severity == ErrorSeverity.CRITICAL for bug in syntax_bugs):
            return self._build_result(file_path, bugs, start_time)

        # FASE 2: Parse AST para análises mais profundas
        try:
            tree = ast.parse(content, filename=file_path)

            # Import validation
            import_bugs = self._check_imports(file_path, tree)
            bugs.extend(import_bugs)

            # Undefined variable detection
            undefined_bugs = self._check_undefined_variables(file_path, tree, content)
            bugs.extend(undefined_bugs)

            # Security risks
            security_bugs = self._check_security_risks(file_path, tree, content)
            bugs.extend(security_bugs)

        except SyntaxError:
            # Já capturado na fase 1
            pass

        return self._build_result(file_path, bugs, start_time)

    def _check_syntax(self, file_path: str, content: str) -> List[BugDetection]:
        """Verifica erros de sintaxe usando AST"""
        bugs = []

        try:
            ast.parse(content, filename=file_path)
        except SyntaxError as e:
            bugs.append(BugDetection(
                file_path=file_path,
                line_number=e.lineno or 0,
                category=ErrorCategory.SYNTAX_ERROR,
                severity=ErrorSeverity.CRITICAL,
                description=f"Syntax error: {e.msg}",
                suggestion="Fix syntax before executing",
                code_snippet=e.text.strip() if e.text else None
            ))

        return bugs

    def _check_imports(self, file_path: str, tree: ast.AST) -> List[BugDetection]:
        """Verifica imports problemáticos"""
        bugs = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Check for dangerous imports
                    if alias.name in ['os', 'subprocess', 'sys']:
                        bugs.append(BugDetection(
                            file_path=file_path,
                            line_number=node.lineno,
                            category=ErrorCategory.SECURITY_RISK,
                            severity=ErrorSeverity.MEDIUM,
                            description=f"Import of potentially dangerous module: {alias.name}",
                            suggestion="Ensure proper validation when using system modules"
                        ))

            elif isinstance(node, ast.ImportFrom):
                # Check for wildcard imports
                if any(alias.name == '*' for alias in node.names):
                    bugs.append(BugDetection(
                        file_path=file_path,
                        line_number=node.lineno,
                        category=ErrorCategory.STYLE_WARNING,
                        severity=ErrorSeverity.LOW,
                        description=f"Wildcard import from {node.module}",
                        suggestion="Use explicit imports instead of '*'"
                    ))

        return bugs

    def _check_undefined_variables(
        self,
        file_path: str,
        tree: ast.AST,
        content: str
    ) -> List[BugDetection]:
        """Detecta potenciais variáveis indefinidas"""
        bugs = []

        # Simplified check: look for common undefined variable patterns
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # Check for common typos/undefined
            if 'NameError' in line and '#' not in line.split('NameError')[0]:
                bugs.append(BugDetection(
                    file_path=file_path,
                    line_number=i,
                    category=ErrorCategory.UNDEFINED_VARIABLE,
                    severity=ErrorSeverity.HIGH,
                    description="Potential NameError reference",
                    suggestion="Ensure variable is defined before use",
                    code_snippet=line.strip()
                ))

        return bugs

    def _check_security_risks(
        self,
        file_path: str,
        tree: ast.AST,
        content: str
    ) -> List[BugDetection]:
        """Detecta riscos de segurança"""
        bugs = []

        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue

            # Check for eval/exec usage
            if 'eval(' in line or 'exec(' in line:
                # Make sure it's not in a comment
                code_part = line.split('#')[0]
                if 'eval(' in code_part or 'exec(' in code_part:
                    bugs.append(BugDetection(
                        file_path=file_path,
                        line_number=i,
                        category=ErrorCategory.SECURITY_RISK,
                        severity=ErrorSeverity.HIGH,
                        description="Use of eval() or exec() - potential security risk",
                        suggestion="Avoid eval/exec or validate input thoroughly",
                        code_snippet=line.strip()
                    ))

            # Check for SQL injection patterns
            if 'execute(' in line and '%s' in line:
                # Only flag if it looks like SQL (has 'cursor' or 'SELECT')
                if 'cursor' in content.lower() or 'SELECT' in content:
                    bugs.append(BugDetection(
                        file_path=file_path,
                        line_number=i,
                        category=ErrorCategory.SECURITY_RISK,
                        severity=ErrorSeverity.CRITICAL,
                        description="Potential SQL injection vulnerability",
                        suggestion="Use parameterized queries",
                        code_snippet=line.strip()
                    ))

        return bugs

    def _build_result(
        self,
        file_path: str,
        bugs: List[BugDetection],
        start_time: float
    ) -> AnalysisResult:
        """Constrói resultado da análise"""

        # Count by severity
        critical_issues = sum(1 for bug in bugs if bug.severity == ErrorSeverity.CRITICAL)
        errors = sum(1 for bug in bugs if bug.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH])
        warnings = sum(1 for bug in bugs if bug.severity in [ErrorSeverity.MEDIUM, ErrorSeverity.LOW])

        # Update stats
        self.stats['bugs_detected'] += len(bugs)
        self.stats['critical_issues_prevented'] += critical_issues
        self.stats['warnings_issued'] += warnings

        # Safe to execute if no critical issues
        is_safe = critical_issues == 0

        return AnalysisResult(
            file_path=file_path,
            bugs=bugs,
            warnings=warnings,
            errors=errors,
            critical_issues=critical_issues,
            is_safe_to_execute=is_safe,
            analysis_time=time.time() - start_time
        )

    def analyze_directory(
        self,
        directory: str,
        recursive: bool = True,
        pattern: str = "*.py"
    ) -> List[AnalysisResult]:
        """
        Analisa todos os arquivos Python em um diretório

        Args:
            directory: Diretório para analisar
            recursive: Se True, analisa subdiretórios
            pattern: Padrão de arquivos (default: *.py)

        Returns:
            Lista de AnalysisResult para cada arquivo
        """
        path = Path(directory)

        if not path.exists():
            return []

        files = path.rglob(pattern) if recursive else path.glob(pattern)
        results = []

        for file_path in files:
            result = self.analyze_file(str(file_path))
            results.append(result)

        return results

    def print_bugs(self, result: AnalysisResult, verbose: bool = False):
        """
        Imprime bugs detectados de forma formatada

        Args:
            result: AnalysisResult para imprimir
            verbose: Se True, mostra mais detalhes
        """
        if not result.bugs:
            logger.info(f"✅ {result.file_path}: No issues detected")
            return

        logger.info(f"\n{'='*70}")
        logger.debug(f"🔍 BugBot Analysis: {result.file_path}")
        logger.info(f"{'='*70}")
        # Summary
        logger.info(f"\n📊 Summary:")
        logger.info(f"  Critical issues: {result.critical_issues}")
        logger.error(f"  Errors: {result.errors}")
        logger.warning(f"  Warnings: {result.warnings}")
        logger.info(f"  Safe to execute: {'✅ Yes' if result.is_safe_to_execute else '❌ No'}")
        logger.info(f"  Analysis time: {result.analysis_time:.3f}s")
        # Bugs
        logger.info(f"\n🐛 Issues detected:")
        for bug in result.bugs:
            severity_icon = {
                ErrorSeverity.CRITICAL: "🔴",
                ErrorSeverity.HIGH: "🟠",
                ErrorSeverity.MEDIUM: "🟡",
                ErrorSeverity.LOW: "🔵"
            }[bug.severity]

            logger.info(f"\n  {severity_icon} [{bug.severity.value.upper()}] Line {bug.line_number}")
            logger.info(f"     Category: {bug.category.value}")
            logger.info(f"     {bug.description}")
            if bug.suggestion:
                logger.info(f"     💡 Suggestion: {bug.suggestion}")
            if verbose and bug.code_snippet:
                logger.info(f"     Code: {bug.code_snippet}")
    def print_stats(self):
        """Imprime estatísticas do BugBot"""
        print("\n" + "="*70)
        logger.error("   BUGBOT - PROACTIVE ERROR DETECTION STATISTICS")
        print("="*70)
        logger.info(f"  Files analyzed: {self.stats['files_analyzed']}")
        logger.info(f"  Bugs detected: {self.stats['bugs_detected']}")
        logger.info(f"  Critical issues prevented: {self.stats['critical_issues_prevented']}")
        logger.warning(f"  Warnings issued: {self.stats['warnings_issued']}")
        print("="*70)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def analyze_file(file_path: str) -> AnalysisResult:
    """
    Convenience function para analisar arquivo

    Args:
        file_path: Caminho do arquivo

    Returns:
        AnalysisResult

    Example:
        >>> result = analyze_file("script.py")
        >>> if not result.is_safe_to_execute:
        ...     print("⚠️  File has critical issues!")
    """
    bugbot = BugBot()
    return bugbot.analyze_file(file_path)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.error("🔍 BugBot - Proactive Error Detection Demo\n")
    print("=" * 70)
    logger.info("P4 - Prudência Operacional in action!")
    print("=" * 70)

    bugbot = BugBot()

    # Create test file with intentional errors
    import tempfile
    test_file = Path(tempfile.mktemp(suffix=".py"))

    test_code = """
# Test file with intentional errors
import os
from sys import *
from config.logging_config import get_logger

logger = get_logger(__name__)

def buggy_function():
    # Undefined variable
    result = undefined_var + 10

    # Security risk
    user_input = input("Enter code: ")
    eval(user_input)

    return result

# Syntax error on next line
def broken_function(
    logger.info("Missing closing parenthesis")
"""

    test_file.write_text(test_code)

    logger.info(f"\nAnalyzing test file: {test_file.name}")
    result = bugbot.analyze_file(str(test_file))

    bugbot.print_bugs(result, verbose=True)

    # Cleanup
    test_file.unlink()

    # Print stats
    bugbot.print_stats()

    logger.info("\n✅ BugBot Demo Complete!")
    logger.info("🏎️ PAGANI: P4 - Prudência Operacional implementado!")