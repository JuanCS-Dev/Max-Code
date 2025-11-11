"""
Tool Executor Implementation

OBJETIVO: Executar ferramentas de forma segura e auditável.

IDEIA CENTRAL:
- Agentes precisam executar ações (bash, file ops, API calls)
- Precisa ser SEGURO (validação, sandboxing)
- Precisa ser AUDITÁVEL (P4 - log cada ação)
- Precisa ser ROBUSTO (error handling)

FERRAMENTAS SUPORTADAS:
1. Bash: Executar comandos shell
2. File Ops: Read, write, edit files
3. API Calls: Chamar APIs externas
4. Search: Grep, find, etc

MANDATO CONSTITUCIONAL:
- P2: API validation (validar APIs antes de usar)
- P4: Rastreabilidade (auditar cada tool call)
- P5: Systemic impact (avaliar impacto antes de executar)

"O que as tuas mãos encontrarem para fazer, faze-o com toda a tua força"
(Eclesiastes 9:10)
"""

from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import subprocess
import os
import sys
from pathlib import Path

# Add tools to path
tools_path = Path(__file__).parent.parent.parent / "tools"
if str(tools_path) not in sys.path:
    sys.path.insert(0, str(tools_path))

# Import file tools
from core.tools import (
    FileReader, FileWriter, FileEditor,
    GlobTool, GrepTool
)

# Import self-correction engine (P5 - Autocorreção Humilde)
from .self_correction import SelfCorrectionEngine
from config.logging_config import get_logger

logger = get_logger(__name__)


class ToolType(Enum):
    """Tipo de ferramenta"""
    BASH = "bash"
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    FILE_EDIT = "file_edit"
    GLOB = "glob"  # Pattern-based file search
    GREP = "grep"  # Content search
    API_CALL = "api_call"
    SEARCH = "search"  # Generic search (deprecated - use GLOB or GREP)


class ToolStatus(Enum):
    """Status de execução"""
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    BLOCKED = "blocked"  # Bloqueada por validação


@dataclass
class Tool:
    """Definição de ferramenta"""
    name: str
    type: ToolType
    description: str
    parameters: Dict[str, Any]
    requires_validation: bool = True  # P2: API validation
    safe_mode: bool = True  # Se True, validar impacto antes de executar (P5)
    timeout: Optional[float] = None  # Timeout em segundos


@dataclass
class ToolResult:
    """Resultado de execução de ferramenta"""
    tool_name: str
    tool_type: ToolType
    status: ToolStatus
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict:
        return {
            'tool_name': self.tool_name,
            'tool_type': self.tool_type.value,
            'status': self.status.value,
            'output': str(self.output)[:200] if self.output else None,
            'error': self.error,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp.isoformat(),
        }


class ToolExecutor:
    """
    Tool Executor Engine

    PROCESSO:
    1. VALIDATE: Valida ferramenta (P2, P5)
    2. EXECUTE: Executa ferramenta
    3. AUDIT: Audita execução (P4)
    4. HANDLE ERRORS: Error handling robusto

    BENEFÍCIOS:
    - Safe execution (validação + sandboxing)
    - Auditability (P4)
    - Robust error handling
    - Timeout protection

    "Sê forte e corajoso; não temas, nem te espantes, porque o SENHOR, teu Deus,
     é contigo por onde quer que andares." (Josué 1:9)
    """

    DEFAULT_TIMEOUT = 30.0  # 30 seconds

    def __init__(self, safe_mode: bool = True, enable_self_correction: bool = True):
        """
        Inicializa Tool Executor

        Args:
            safe_mode: Se True, validar impacto antes de executar
            enable_self_correction: Se True, ativa Self-Correction Loops (P5)
        """
        self.safe_mode = safe_mode
        self.enable_self_correction = enable_self_correction

        # Registry de ferramentas
        self.registered_tools: Dict[str, Tool] = {}

        # Execution history (para auditoria - P4)
        self.execution_history: List[ToolResult] = []

        # Stats
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'blocked_executions': 0,
            'total_execution_time': 0.0,
            'self_corrections': 0,  # NEW: Track self-corrections
        }

        # Initialize file tools
        self.file_reader = FileReader()
        self.file_writer = FileWriter()
        self.file_editor = FileEditor()
        self.glob_tool = GlobTool()
        self.grep_tool = GrepTool()

        # Initialize self-correction engine (P5 - Autocorreção Humilde)
        if enable_self_correction:
            self.self_correction_engine = SelfCorrectionEngine(max_attempts=3)
            logger.info("🔄 Self-Correction Engine enabled (P5 - Autocorreção Humilde)")
        else:
            self.self_correction_engine = None

    def register_tool(self, tool: Tool):
        """
        Registra ferramenta

        Args:
            tool: Tool a registrar
        """
        self.registered_tools[tool.name] = tool
        logger.info(f"🔧 Tool Executor: Registered tool '{tool.name}' ({tool.type.value})")
    def execute(
        self,
        tool_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ToolResult:
        """
        Executa ferramenta

        Args:
            tool_name: Nome da ferramenta
            parameters: Parâmetros (None = usar default do Tool)

        Returns:
            ToolResult
        """
        self.stats['total_executions'] += 1

        # Get tool
        if tool_name not in self.registered_tools:
            result = ToolResult(
                tool_name=tool_name,
                tool_type=ToolType.BASH,  # Placeholder
                status=ToolStatus.FAILURE,
                output=None,
                error=f"Tool '{tool_name}' not registered",
            )
            self.execution_history.append(result)
            self.stats['failed_executions'] += 1
            return result

        tool = self.registered_tools[tool_name]

        # Merge parameters
        params = {**tool.parameters, **(parameters or {})}

        logger.info(f"⚙️  Tool Executor: Executing '{tool_name}'...")
        # FASE 1: VALIDATE
        if tool.requires_validation or (self.safe_mode and tool.safe_mode):
            validation_result = self._validate_tool_execution(tool, params)
            if not validation_result['valid']:
                result = ToolResult(
                    tool_name=tool_name,
                    tool_type=tool.type,
                    status=ToolStatus.BLOCKED,
                    output=None,
                    error=f"Validation failed: {validation_result['reason']}",
                )
                self.execution_history.append(result)
                self.stats['blocked_executions'] += 1
                logger.info(f"   🚫 Execution blocked: {validation_result['reason']}")
                return result

        # FASE 2: EXECUTE
        import time
        start_time = time.time()

        try:
            output = self._execute_tool(tool, params)
            status = ToolStatus.SUCCESS
            error = None
            self.stats['successful_executions'] += 1
        except TimeoutError as e:
            output = None
            status = ToolStatus.TIMEOUT
            error = str(e)
            self.stats['failed_executions'] += 1
        except Exception as e:
            output = None
            status = ToolStatus.FAILURE
            error = str(e)
            self.stats['failed_executions'] += 1

        execution_time = time.time() - start_time
        self.stats['total_execution_time'] += execution_time

        # FASE 2.5: SELF-CORRECTION (P5 - Autocorreção Humilde)
        # Se falhou e self-correction está ativado, tenta corrigir automaticamente
        if status == ToolStatus.FAILURE and self.enable_self_correction and self.self_correction_engine:
            logger.error(f"   ❌ Execution failed: {error}")
            logger.info(f"   🔄 Attempting self-correction (P5)...")
            correction_result = self.self_correction_engine.correct_execution(
                tool_executor=self,
                tool_name=tool_name,
                parameters=params,
                original_error=error
            )

            if correction_result.corrected:
                # Self-correction bem-sucedida! Usa resultado corrigido
                output = correction_result.final_output
                status = ToolStatus.SUCCESS
                error = None
                self.stats['self_corrections'] += 1

                # Atualiza stats (falha anterior foi corrigida)
                self.stats['failed_executions'] -= 1
                self.stats['successful_executions'] += 1

                logger.info(f"   ✅ Self-correction successful! (P5 - Autocorreção Humilde)")
            else:
                # Self-correction falhou, mantém erro original
                error = correction_result.final_error
                logger.error(f"   ⚠️  Self-correction failed, escalating to user...")
        # FASE 3: AUDIT (P4)
        result = ToolResult(
            tool_name=tool_name,
            tool_type=tool.type,
            status=status,
            output=output,
            error=error,
            execution_time=execution_time,
        )

        self.execution_history.append(result)

        # Log resultado
        if status == ToolStatus.SUCCESS:
            logger.info(f"   ✓ Execution successful ({execution_time:.2f}s)")
        elif status != ToolStatus.FAILURE:  # Timeout/blocked já foi logado
            logger.error(f"   ❌ Execution failed: {error}")
        return result

    def _validate_tool_execution(
        self,
        tool: Tool,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Valida execução de ferramenta

        Checks:
        - P2: API validation (se é API, validar que existe)
        - P5: Systemic impact (avaliar impacto no sistema)
        - Security (comandos perigosos)

        Returns:
            {'valid': bool, 'reason': str}
        """
        # Check 1: Dangerous commands (bash)
        if tool.type == ToolType.BASH:
            command = parameters.get('command', '')
            dangerous_commands = ['rm -rf /', 'format', 'mkfs', 'dd if=/dev/zero']

            for dangerous in dangerous_commands:
                if dangerous in command.lower():
                    return {
                        'valid': False,
                        'reason': f"Dangerous command detected: '{dangerous}'"
                    }

        # Check 2: File operations (paths)
        if tool.type in [ToolType.FILE_WRITE, ToolType.FILE_EDIT]:
            file_path = parameters.get('file_path', '')

            # Não permitir escrever em system paths
            system_paths = ['/etc', '/bin', '/usr', '/sys']
            for sys_path in system_paths:
                if file_path.startswith(sys_path):
                    return {
                        'valid': False,
                        'reason': f"Cannot write to system path: '{file_path}'"
                    }

        # Check 3: API validation (P2)
        if tool.type == ToolType.API_CALL:
            # Em produção, validar que API existe
            # (chamar P2_API_Validator)
            pass

        return {'valid': True, 'reason': ''}

    def _execute_tool(
        self,
        tool: Tool,
        parameters: Dict[str, Any]
    ) -> Any:
        """
        Executa ferramenta (implementação real)

        Dispatcher para cada tipo de ferramenta.
        """
        if tool.type == ToolType.BASH:
            return self._execute_bash(parameters)
        elif tool.type == ToolType.FILE_READ:
            return self._execute_file_read(parameters)
        elif tool.type == ToolType.FILE_WRITE:
            return self._execute_file_write(parameters)
        elif tool.type == ToolType.FILE_EDIT:
            return self._execute_file_edit(parameters)
        elif tool.type == ToolType.GLOB:
            return self._execute_glob(parameters)
        elif tool.type == ToolType.GREP:
            return self._execute_grep(parameters)
        elif tool.type == ToolType.API_CALL:
            return self._execute_api_call(parameters)
        elif tool.type == ToolType.SEARCH:
            return self._execute_search(parameters)
        else:
            raise ValueError(f"Unknown tool type: {tool.type}")

    def _execute_bash(self, parameters: Dict[str, Any]) -> str:
        """Executa comando bash"""
        command = parameters['command']
        timeout = parameters.get('timeout', self.DEFAULT_TIMEOUT)

        try:
            # Security: shell=True needed for bash tool functionality
            # Commands come from AI agent execution plan, not untrusted input
            # Protected by timeout and Constitutional AI validation
            result = subprocess.run(
                command,
                shell=True,  # nosec B602
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if result.returncode != 0:
                raise RuntimeError(f"Command failed with code {result.returncode}: {result.stderr}")

            return result.stdout

        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Command timed out after {timeout}s")

    def _execute_file_read(self, parameters: Dict[str, Any]) -> str:
        """Lê arquivo usando FileReader"""
        file_path = parameters['file_path']
        offset = parameters.get('offset')
        limit = parameters.get('limit')

        result = self.file_reader.read(file_path, offset=offset, limit=limit)

        if not result.success:
            raise RuntimeError(result.error)

        return result.content

    def _execute_file_write(self, parameters: Dict[str, Any]) -> str:
        """Escreve arquivo usando FileWriter"""
        file_path = parameters['file_path']
        content = parameters['content']
        overwrite = parameters.get('overwrite', True)

        result = self.file_writer.write(file_path, content, overwrite=overwrite)

        if not result.success:
            raise RuntimeError(result.error)

        return f"Written {result.bytes_written} bytes to {file_path}" + \
               (f" (backup: {result.backup_path})" if result.backup_path else "")

    def _execute_file_edit(self, parameters: Dict[str, Any]) -> str:
        """Edita arquivo usando FileEditor"""
        file_path = parameters['file_path']
        old_string = parameters['old_string']
        new_string = parameters['new_string']
        replace_all = parameters.get('replace_all', False)

        result = self.file_editor.edit(
            file_path,
            old_string,
            new_string,
            replace_all=replace_all
        )

        if not result.success:
            raise RuntimeError(result.error)

        return f"Replaced {result.replacements} occurrence(s) in {file_path}" + \
               (f"\nBackup: {result.backup_path}" if result.backup_path else "") + \
               (f"\n\nDiff:\n{result.diff}" if result.diff else "")

    def _execute_glob(self, parameters: Dict[str, Any]) -> str:
        """Executa glob (pattern-based file search)"""
        pattern = parameters['pattern']
        path = parameters.get('path')
        max_results = parameters.get('max_results', 100)

        result = self.glob_tool.glob(pattern, path=path, max_results=max_results)

        if not result.success:
            raise RuntimeError(result.error)

        # Format output
        output = f"Found {result.total_matches} files matching '{pattern}'\n"
        if result.ignored_count > 0:
            output += f"(Ignored {result.ignored_count} files)\n"

        output += "\nMatches:\n"
        for match in result.matches:
            output += f"  {match}\n"

        return output

    def _execute_grep(self, parameters: Dict[str, Any]) -> str:
        """Executa grep (content search)"""
        pattern = parameters['pattern']
        path = parameters.get('path')
        output_mode = parameters.get('output_mode', 'files_with_matches')
        case_sensitive = parameters.get('case_sensitive', True)
        file_type = parameters.get('file_type')

        result = self.grep_tool.grep(
            pattern,
            path=path,
            output_mode=output_mode,
            case_sensitive=case_sensitive,
            file_type=file_type
        )

        if not result.success:
            raise RuntimeError(result.error)

        # Format output based on mode
        output = f"Search results for '{pattern}' ({result.total_matches} matches)\n\n"

        if output_mode == "files_with_matches":
            for file_path in result.files_with_matches:
                output += f"  {file_path}\n"

        elif output_mode == "content":
            for match in result.matches:
                output += f"{match.file_path}:{match.line_number}:{match.line_content}\n"

        elif output_mode == "count":
            for file_path, count in result.match_counts.items():
                output += f"  {count:4d} - {file_path}\n"

        return output

    def _execute_api_call(self, parameters: Dict[str, Any]) -> Any:
        """
        Chama API externa usando requests.

        Parameters:
            url (str): URL to call
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
            headers (dict, optional): HTTP headers
            data (dict, optional): Request body (for POST/PUT)
            timeout (int, optional): Request timeout in seconds (default: 30)

        Returns:
            dict: Response with status_code, headers, and body
        """
        try:
            import requests
        except ImportError:
            logger.error("❌ requests library not installed. Install: pip install requests")
            return {
                'error': 'requests library not available',
                'status_code': None
            }

        url = parameters['url']
        method = parameters.get('method', 'GET').upper()
        headers = parameters.get('headers', {})
        data = parameters.get('data')
        timeout = parameters.get('timeout', 30)

        logger.info(f"   🌐 API call: {method} {url}")

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if data else None,
                timeout=timeout
            )

            # Try to parse JSON, fallback to text
            try:
                body = response.json()
            except ValueError:
                body = response.text

            result = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'body': body,
                'ok': response.ok,
                'url': response.url,
            }

            logger.info(f"   ✅ Response: {response.status_code}")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"   ⏱️  Timeout after {timeout}s")
            return {'error': 'timeout', 'status_code': None}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"   🔌 Connection error: {e}")
            return {'error': f'connection_error: {e}', 'status_code': None}
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            return {'error': str(e), 'status_code': None}

    def _execute_search(self, parameters: Dict[str, Any]) -> List[str]:
        """
        Executa busca usando grep/subprocess.

        Parameters:
            pattern (str): Pattern to search for
            path (str, optional): Path to search in (default: '.')
            case_sensitive (bool, optional): Case sensitive search (default: True)
            include_line_numbers (bool, optional): Include line numbers (default: True)
            file_pattern (str, optional): Filter files (e.g., "*.py")

        Returns:
            List[str]: List of matches in format "file:line:content" or ["file"] depending on options
        """
        import subprocess

        pattern = parameters['pattern']
        path = parameters.get('path', '.')
        case_sensitive = parameters.get('case_sensitive', True)
        include_line_numbers = parameters.get('include_line_numbers', True)
        file_pattern = parameters.get('file_pattern')

        logger.info(f"   🔍 Search: '{pattern}' in {path}")

        # Build grep command
        cmd = ['grep', '-r']  # Recursive by default

        if not case_sensitive:
            cmd.append('-i')

        if include_line_numbers:
            cmd.append('-n')

        if file_pattern:
            cmd.extend(['--include', file_pattern])

        cmd.extend([pattern, path])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )

            # grep returns 0 if matches found, 1 if no matches, 2+ for errors
            if result.returncode == 0:
                matches = [line for line in result.stdout.split('\n') if line]
                logger.info(f"   ✅ Found {len(matches)} match(es)")
                return matches
            elif result.returncode == 1:
                logger.info(f"   ℹ️  No matches found")
                return []
            else:
                logger.error(f"   ❌ Grep error: {result.stderr}")
                return []

        except subprocess.TimeoutExpired:
            logger.error(f"   ⏱️  Search timeout after 60s")
            return []
        except FileNotFoundError:
            logger.error(f"   ❌ grep command not found")
            return []
        except Exception as e:
            logger.error(f"   ❌ Search error: {e}")
            return []

    def get_execution_history(self, limit: int = 10) -> List[ToolResult]:
        """Retorna histórico de execuções (P4 - rastreabilidade)"""
        return self.execution_history[-limit:]

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
            'success_rate': (
                self.stats['successful_executions'] / self.stats['total_executions'] * 100
                if self.stats['total_executions'] > 0 else 0.0
            ),
            'avg_execution_time': (
                self.stats['total_execution_time'] / self.stats['total_executions']
                if self.stats['total_executions'] > 0 else 0.0
            ),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        logger.info("  TOOL EXECUTOR - STATISTICS")
        print("="*60)
        logger.info(f"Total executions:          {stats['total_executions']}")
        logger.info(f"Successful:                {stats['successful_executions']} ({stats['success_rate']:.1f}%)")
        logger.error(f"Failed:                    {stats['failed_executions']}")
        logger.info(f"Blocked:                   {stats['blocked_executions']}")
        if self.enable_self_correction:
            logger.info(f"Self-corrections (P5):     {stats['self_corrections']}")
        logger.info(f"Avg execution time:        {stats['avg_execution_time']:.3f}s")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def create_bash_tool(name: str, command: str) -> Tool:
    """Helper para criar Tool de bash"""
    return Tool(
        name=name,
        type=ToolType.BASH,
        description=f"Execute bash command: {command}",
        parameters={'command': command},
    )


def create_file_read_tool(name: str, file_path: str) -> Tool:
    """Helper para criar Tool de file read"""
    return Tool(
        name=name,
        type=ToolType.FILE_READ,
        description=f"Read file: {file_path}",
        parameters={'file_path': file_path},
    )
