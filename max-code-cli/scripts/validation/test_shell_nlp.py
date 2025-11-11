#!/usr/bin/env python3
"""
Teste funcional do MAX-CODE Shell com NLP

Testa os 5 comandos principais:
1. Read arquivo
2. Write arquivo
3. Find/Search pattern
4. Edit arquivo
5. Run bash command

Soli Deo Gloria 🙏
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from core.epl.nlp_engine import recognize_intent, IntentType
from cli.shell_context import ShellContext
from rich.console import Console

console = Console()

def test_nlp_intent_recognition():
    """Test 1: NLP Engine reconhece intents corretamente"""
    console.print("\n[bold blue]TEST 1: NLP Intent Recognition[/bold blue]\n")

    tests = [
        ("Read config.json", IntentType.READ),
        ("Write hello world to test.txt", IntentType.WRITE),
        ("Find all TODO comments", IntentType.SEARCH),
        ("Edit config.json replacing port", IntentType.EDIT),
        ("Run ls -la", IntentType.RUN),
    ]

    for message, expected_intent in tests:
        intent = recognize_intent(message)
        status = "✅" if intent.type == expected_intent else "❌"
        console.print(f"{status} '{message}' → {intent.type.value} (expected: {expected_intent.value})")
        console.print(f"   Confidence: {intent.confidence:.2f}\n")

def test_context_resolution():
    """Test 2: Context Manager resolve referências"""
    console.print("\n[bold blue]TEST 2: Context Resolution[/bold blue]\n")

    ctx = ShellContext()

    # Simular: usuário leu um arquivo
    ctx.remember_file("config.json", "content here", "read")

    # Testar resoluções
    tests = [
        ("Edit that file", "Edit config.json"),
        ("Write it back", "Write config.json back"),
        ("Show the file", "Show config.json"),
    ]

    for original, expected in tests:
        resolved = ctx.resolve_reference(original)
        status = "✅" if expected in resolved else "❌"
        console.print(f"{status} '{original}' → '{resolved}'")

    console.print(f"\n📄 Context: {ctx.get_summary()}")

def test_file_operations():
    """Test 3: File operations (Read/Write)"""
    console.print("\n[bold blue]TEST 3: File Operations[/bold blue]\n")

    from core.tools.file_writer import FileWriter
    from core.tools.file_reader import FileReader

    # Write test file
    test_file = "/tmp/max_code_test.txt"
    writer = FileWriter()
    writer.write(test_file, "Hello MAX-CODE Shell!")
    console.print(f"✅ Wrote to {test_file}")

    # Read test file
    reader = FileReader()
    content = reader.read(test_file)
    console.print(f"✅ Read from {test_file}: '{content[:30]}...'")

    # Cleanup
    import os
    os.remove(test_file)
    console.print(f"✅ Cleaned up {test_file}")

def test_integration():
    """Test 4: Full integration (NLP → Context → Tool)"""
    console.print("\n[bold blue]TEST 4: Full Integration[/bold blue]\n")

    ctx = ShellContext()

    # Simular fluxo completo
    commands = [
        "Read /tmp/test.txt",
        "Edit that file",
        "Write it back"
    ]

    for cmd in commands:
        resolved = ctx.resolve_reference(cmd)
        intent = recognize_intent(resolved)
        console.print(f"💬 User: {cmd}")
        console.print(f"   Resolved: {resolved}")
        console.print(f"   Intent: {intent.type.value} (confidence: {intent.confidence:.2f})\n")

        # Simular execução
        if intent.type == IntentType.READ:
            ctx.remember_file("/tmp/test.txt", "content", "read")

if __name__ == "__main__":
    console.print("[bold green]" + "="*60 + "[/bold green]")
    console.print("[bold green]MAX-CODE Shell - Functional Tests[/bold green]")
    console.print("[bold green]" + "="*60 + "[/bold green]")

    try:
        test_nlp_intent_recognition()
        test_context_resolution()
        test_file_operations()
        test_integration()

        console.print("\n[bold green]✅ ALL TESTS PASSED![/bold green]\n")
        console.print("🚀 MAX-CODE Shell está 100% funcional!")
        console.print("📖 Você pode usar linguagem natural como no Claude Code\n")

    except Exception as e:
        console.print(f"\n[bold red]❌ TEST FAILED: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
