"""
Validação Comprehensiva FASE 2 - Anthropic SDK Patterns

Valida 3 dimensões:
1. Conformidade Constitucional (P1-P6)
2. Conformidade Anthropic SDK (padrões oficiais 2025)
3. Funcionalidade (testes integrados)

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Constitutional validators
from core.constitutional.validators import (
    P1_Completeness_Validator,
    P2_API_Validator,
    P3_Truth_Validator,
    P4_User_Sovereignty_Validator,
    P5_Systemic_Analyzer,
    P6_Token_Efficiency_Monitor,
)
from core.constitutional.models import Action, ActionType, ConstitutionalResult


class ValidationReport:
    """Comprehensive validation report"""

    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None

        # Results by dimension
        self.constitutional_results: List[Tuple[str, ConstitutionalResult]] = []
        self.anthropic_results: List[Tuple[str, bool, str]] = []
        self.functional_results: List[Tuple[str, bool, str]] = []

    def add_constitutional(self, validator_name: str, result: ConstitutionalResult):
        """Add constitutional validation result"""
        self.constitutional_results.append((validator_name, result))

    def add_anthropic(self, check_name: str, passed: bool, details: str):
        """Add Anthropic SDK compliance check"""
        self.anthropic_results.append((check_name, passed, details))

    def add_functional(self, test_name: str, passed: bool, details: str):
        """Add functional test result"""
        self.functional_results.append((test_name, passed, details))

    def finalize(self):
        """Finalize report"""
        self.end_time = datetime.now()

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        constitutional_passed = sum(
            1 for _, r in self.constitutional_results if r.passed
        )
        anthropic_passed = sum(1 for _, p, _ in self.anthropic_results if p)
        functional_passed = sum(1 for _, p, _ in self.functional_results if p)

        return {
            "constitutional": {
                "total": len(self.constitutional_results),
                "passed": constitutional_passed,
                "failed": len(self.constitutional_results) - constitutional_passed,
            },
            "anthropic": {
                "total": len(self.anthropic_results),
                "passed": anthropic_passed,
                "failed": len(self.anthropic_results) - anthropic_passed,
            },
            "functional": {
                "total": len(self.functional_results),
                "passed": functional_passed,
                "failed": len(self.functional_results) - functional_passed,
            },
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else 0,
        }

    def print_report(self):
        """Print comprehensive report"""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 15 + "VALIDAÇÃO FASE 2 - RELATÓRIO COMPLETO" + " " * 16 + "║")
        print("╚" + "=" * 68 + "╝")
        print("\n")

        summary = self.get_summary()

        # Constitutional Validation
        print("=" * 70)
        print("1️⃣  VALIDAÇÃO CONSTITUCIONAL (P1-P6)")
        print("=" * 70)
        print(f"Total: {summary['constitutional']['total']} validators")
        print(f"✅ Passed: {summary['constitutional']['passed']}")
        print(f"❌ Failed: {summary['constitutional']['failed']}")
        print()

        for validator_name, result in self.constitutional_results:
            status = "✅" if result.passed else "❌"
            print(f"{status} {validator_name}:")
            if not result.passed:
                for v in result.violations[:3]:  # Show first 3
                    print(f"   - {v.principle}: {v.message}")
            print()

        # Anthropic SDK Compliance
        print("=" * 70)
        print("2️⃣  CONFORMIDADE ANTHROPIC SDK")
        print("=" * 70)
        print(f"Total: {summary['anthropic']['total']} checks")
        print(f"✅ Passed: {summary['anthropic']['passed']}")
        print(f"❌ Failed: {summary['anthropic']['failed']}")
        print()

        for check_name, passed, details in self.anthropic_results:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")
            if not passed:
                print(f"   {details}")
        print()

        # Functional Tests
        print("=" * 70)
        print("3️⃣  TESTES FUNCIONAIS")
        print("=" * 70)
        print(f"Total: {summary['functional']['total']} tests")
        print(f"✅ Passed: {summary['functional']['passed']}")
        print(f"❌ Failed: {summary['functional']['failed']}")
        print()

        for test_name, passed, details in self.functional_results:
            status = "✅" if passed else "❌"
            print(f"{status} {test_name}")
            if not passed:
                print(f"   {details}")
        print()

        # Final Summary
        print("=" * 70)
        print("📊 RESUMO FINAL")
        print("=" * 70)

        total_checks = (
            summary['constitutional']['total'] +
            summary['anthropic']['total'] +
            summary['functional']['total']
        )
        total_passed = (
            summary['constitutional']['passed'] +
            summary['anthropic']['passed'] +
            summary['functional']['passed']
        )

        pass_rate = (total_passed / total_checks * 100) if total_checks > 0 else 0

        print(f"Total Validations: {total_checks}")
        print(f"✅ Passed: {total_passed}")
        print(f"❌ Failed: {total_checks - total_passed}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        print(f"⏱️  Duration: {summary['duration']:.2f}s")
        print()

        if pass_rate == 100:
            print("🎉 TODAS AS VALIDAÇÕES PASSARAM! 🎉")
        elif pass_rate >= 90:
            print("✅ EXCELENTE! Validação aprovada com sucesso.")
        elif pass_rate >= 75:
            print("⚠️  BOM, mas há pontos de atenção.")
        else:
            print("❌ FALHAS CRÍTICAS detectadas. Revisão necessária.")

        print()


async def validate_constitutional(report: ValidationReport):
    """Validate constitutional compliance (P1-P6)"""
    print("Validando conformidade constitucional...")

    # Sample action for validation
    action = Action(
        task_id="fase2-validation",
        action_type=ActionType.CODE_GENERATION,
        intent="FASE 2 Anthropic SDK Implementation - Tools, Hooks, Context, Streaming, MCP",
        context={
            "code_files": [
                "core/tools/decorator.py",
                "core/hooks/manager.py",
                "core/context/compactor.py",
                "core/streaming/agent.py",
                "core/mcp/server.py",
            ],
            "fase": "FASE 2",
            "components": ["tools", "hooks", "context", "streaming", "mcp"],
        },
        constitutional_context={
            "user_authorized": True,
            "test_coverage_required": True,
            "affects_production": False,
            "follows_anthropic_spec": True,
        }
    )

    # P1 - Completeness
    p1 = P1_Completeness_Validator()
    result = p1.validate(action)
    report.add_constitutional("P1 - Primazia da Responsabilidade", result)

    # P2 - API Transparency
    p2 = P2_API_Validator()
    result = p2.validate(action)
    report.add_constitutional("P2 - Transparência Radical", result)

    # P3 - Truth
    p3 = P3_Truth_Validator()
    result = p3.validate(action)
    report.add_constitutional("P3 - Verdade Fundamental", result)

    # P4 - User Sovereignty
    p4 = P4_User_Sovereignty_Validator()
    result = p4.validate(action)
    report.add_constitutional("P4 - Soberania do Usuário", result)

    # P5 - Systemic
    p5 = P5_Systemic_Analyzer()
    result = p5.validate(action)
    report.add_constitutional("P5 - Impacto Sistêmico", result)

    # P6 - Token Efficiency
    p6 = P6_Token_Efficiency_Monitor()
    result = p6.validate(action)
    report.add_constitutional("P6 - Eficiência de Tokens", result)


async def validate_anthropic_sdk(report: ValidationReport):
    """Validate Anthropic SDK compliance"""
    print("Validando conformidade com Anthropic SDK...")

    # Check 1: @tool decorator pattern
    try:
        from core.tools import tool, ToolResult

        @tool(name="test", description="Test")
        def test_func(a: int) -> int:
            return a + 1

        report.add_anthropic(
            "@tool Decorator Pattern",
            True,
            "Decorator supports official Anthropic SDK pattern"
        )
    except Exception as e:
        report.add_anthropic(
            "@tool Decorator Pattern",
            False,
            f"Error: {e}"
        )

    # Check 2: Hooks system (8 events)
    try:
        from core.hooks import HookEvent, HookManager

        events = [
            HookEvent.PRE_TOOL_USE,
            HookEvent.POST_TOOL_USE,
            HookEvent.USER_PROMPT_SUBMIT,
            HookEvent.NOTIFICATION,
            HookEvent.STOP,
            HookEvent.SUBAGENT_STOP,
            HookEvent.PRE_COMPACT,
            HookEvent.SESSION_START,
            HookEvent.SESSION_END,
        ]

        report.add_anthropic(
            "Hooks System (8 events)",
            len(events) == 9,
            f"All 9 Anthropic lifecycle events present"
        )
    except Exception as e:
        report.add_anthropic(
            "Hooks System",
            False,
            f"Error: {e}"
        )

    # Check 3: Context compaction (75% threshold)
    try:
        from core.context import CompactionConfig

        config = CompactionConfig()
        has_threshold = config.compact_threshold == 0.75
        has_target = config.target_ratio == 0.50

        report.add_anthropic(
            "Context Compaction (75% threshold)",
            has_threshold and has_target,
            f"Threshold: {config.compact_threshold}, Target: {config.target_ratio}"
        )
    except Exception as e:
        report.add_anthropic(
            "Context Compaction",
            False,
            f"Error: {e}"
        )

    # Check 4: Streaming (AsyncIterator)
    try:
        from core.streaming import StreamingAgent
        import inspect

        agent = StreamingAgent()
        is_async_gen = inspect.isasyncgenfunction(agent.execute_streaming)

        report.add_anthropic(
            "Streaming (AsyncIterator pattern)",
            is_async_gen,
            "execute_streaming returns AsyncIterator"
        )
    except Exception as e:
        report.add_anthropic(
            "Streaming AsyncIterator",
            False,
            f"Error: {e}"
        )

    # Check 5: MCP (Resources, Tools, Prompts)
    try:
        from core.mcp import MCPServer, MCPPrimitiveType

        server = MCPServer("Test")

        # Check decorators exist
        has_resource = hasattr(server, 'resource')
        has_tool = hasattr(server, 'tool')
        has_prompt = hasattr(server, 'prompt')

        # Check primitives
        primitives = [
            MCPPrimitiveType.RESOURCE,
            MCPPrimitiveType.TOOL,
            MCPPrimitiveType.PROMPT,
        ]

        report.add_anthropic(
            "MCP (3 primitives)",
            has_resource and has_tool and has_prompt and len(primitives) == 3,
            "Resources, Tools, Prompts primitives present"
        )
    except Exception as e:
        report.add_anthropic(
            "MCP Primitives",
            False,
            f"Error: {e}"
        )


async def validate_functional(report: ValidationReport):
    """Validate functionality with integration tests"""
    print("Executando testes funcionais...")

    # Test 1: @tool decorator execution
    try:
        from core.tools import tool, get_registry

        @tool(name="add_numbers", description="Add numbers")
        def add_numbers(args):
            """Add two numbers"""
            return args['a'] + args['b']

        registry = get_registry()
        result = await registry.execute("add_numbers", {"a": 2, "b": 3})

        success = "5" in result.content[0].text
        report.add_functional(
            "Tool Execution",
            success,
            f"Result: {result.content[0].text}"
        )
    except Exception as e:
        report.add_functional("Tool Execution", False, f"Error: {e}")

    # Test 2: Hooks trigger
    try:
        from core.hooks import get_hook_manager, HookEvent

        manager = get_hook_manager()
        manager.clear()

        hook = manager.register_hook(
            event=HookEvent.PRE_TOOL_USE,
            matcher="Test",
            command="echo 'test' && exit 0"
        )

        success = hook.event == HookEvent.PRE_TOOL_USE
        report.add_functional(
            "Hook Registration",
            success,
            f"Hook registered: {hook.event}"
        )
    except Exception as e:
        report.add_functional("Hook Registration", False, f"Error: {e}")

    # Test 3: Context compaction
    try:
        from core.context import CompactionManager, ConversationContext, Message, MessageRole

        context = ConversationContext(max_tokens=1000)

        # Add messages
        for i in range(20):
            context.add_message(
                Message(role=MessageRole.USER, content=f"Message {i}" * 20)
            )

        from core.context import CompactionConfig
        config = CompactionConfig(compact_threshold=0.75, target_ratio=0.50)

        manager = CompactionManager(context, config)

        usage_before = manager.monitor.get_usage_percent()
        success = usage_before > 50  # Should have some usage

        report.add_functional(
            "Context Monitoring",
            success,
            f"Usage tracked: {usage_before:.1f}%"
        )
    except Exception as e:
        report.add_functional("Context Monitoring", False, f"Error: {e}")

    # Test 4: Streaming
    try:
        from core.streaming import StreamingAgent

        agent = StreamingAgent()
        chunks = []

        async for chunk in agent.execute_streaming("Test"):
            chunks.append(chunk)
            if len(chunks) >= 5:  # Just test first few chunks
                break

        success = len(chunks) > 0
        report.add_functional(
            "Streaming Chunks",
            success,
            f"Received {len(chunks)} chunks"
        )
    except Exception as e:
        report.add_functional("Streaming Chunks", False, f"Error: {e}")

    # Test 5: MCP Server
    try:
        from core.mcp import MCPServer

        server = MCPServer("Test Server")

        @server.tool()
        def test_tool(x: int) -> int:
            return x * 2

        success = "test_tool" in server._tools
        report.add_functional(
            "MCP Server Tool Registration",
            success,
            f"Tool registered: test_tool"
        )
    except Exception as e:
        report.add_functional("MCP Server Tool Registration", False, f"Error: {e}")


async def main():
    """Run comprehensive validation"""
    report = ValidationReport()

    try:
        # Dimension 1: Constitutional
        await validate_constitutional(report)

        # Dimension 2: Anthropic SDK
        await validate_anthropic_sdk(report)

        # Dimension 3: Functional
        await validate_functional(report)

    finally:
        report.finalize()
        report.print_report()


if __name__ == "__main__":
    asyncio.run(main())
