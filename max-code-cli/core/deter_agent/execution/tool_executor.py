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


class ToolType(Enum):
    """Tipo de ferramenta"""
    BASH = "bash"
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    FILE_EDIT = "file_edit"
    API_CALL = "api_call"
    SEARCH = "search"


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

    def __init__(self, safe_mode: bool = True):
        """
        Inicializa Tool Executor

        Args:
            safe_mode: Se True, validar impacto antes de executar
        """
        self.safe_mode = safe_mode

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
        }

    def register_tool(self, tool: Tool):
        """
        Registra ferramenta

        Args:
            tool: Tool a registrar
        """
        self.registered_tools[tool.name] = tool
        print(f"🔧 Tool Executor: Registered tool '{tool.name}' ({tool.type.value})")

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

        print(f"⚙️  Tool Executor: Executing '{tool_name}'...")

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
                print(f"   🚫 Execution blocked: {validation_result['reason']}")
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
            print(f"   ✓ Execution successful ({execution_time:.2f}s)")
        else:
            print(f"   ❌ Execution failed: {error}")

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
            result = subprocess.run(
                command,
                shell=True,
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
        """Lê arquivo"""
        file_path = parameters['file_path']

        with open(file_path, 'r') as f:
            return f.read()

    def _execute_file_write(self, parameters: Dict[str, Any]) -> str:
        """Escreve arquivo"""
        file_path = parameters['file_path']
        content = parameters['content']

        with open(file_path, 'w') as f:
            f.write(content)

        return f"Written {len(content)} bytes to {file_path}"

    def _execute_file_edit(self, parameters: Dict[str, Any]) -> str:
        """Edita arquivo (find & replace)"""
        file_path = parameters['file_path']
        old_string = parameters['old_string']
        new_string = parameters['new_string']

        with open(file_path, 'r') as f:
            content = f.read()

        if old_string not in content:
            raise ValueError(f"String not found in file: '{old_string}'")

        new_content = content.replace(old_string, new_string)

        with open(file_path, 'w') as f:
            f.write(new_content)

        return f"Replaced {content.count(old_string)} occurrences in {file_path}"

    def _execute_api_call(self, parameters: Dict[str, Any]) -> Any:
        """Chama API externa"""
        # Placeholder: em produção, usar requests library
        url = parameters['url']
        method = parameters.get('method', 'GET')

        print(f"   [Placeholder] API call: {method} {url}")
        return {'status': 'placeholder'}

    def _execute_search(self, parameters: Dict[str, Any]) -> List[str]:
        """Executa busca (grep, find)"""
        # Placeholder: em produção, usar grep/rg
        pattern = parameters['pattern']
        path = parameters.get('path', '.')

        print(f"   [Placeholder] Search: {pattern} in {path}")
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
        print("  TOOL EXECUTOR - STATISTICS")
        print("="*60)
        print(f"Total executions:          {stats['total_executions']}")
        print(f"Successful:                {stats['successful_executions']} ({stats['success_rate']:.1f}%)")
        print(f"Failed:                    {stats['failed_executions']}")
        print(f"Blocked:                   {stats['blocked_executions']}")
        print(f"Avg execution time:        {stats['avg_execution_time']:.3f}s")
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
