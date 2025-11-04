"""
Demo: Auto-Protection System

Este exemplo demonstra como os Guardians protegem o Max-Code AUTOMATICAMENTE,
SEM intervenção manual.

Os Guardians são a DEFESA PERMANENTE contra violações doutrinárias.
Eles previnem falhas deliberadas 24/7.

"Porque ele dará ordens aos seus anjos a teu respeito, para te guardarem em todos os teus caminhos."
(Salmos 91:11)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.constitutional.engine import Action, ActionType
from core.constitutional.guardians.auto_protection import (
    enable_auto_protection,
    EnforcementLevel,
    AutoProtectionMode,
    AutoCorrectionStrategy,
)


def simulate_code_generation(action: Action) -> str:
    """
    Simula geração de código

    Em produção, isso seria chamada à API do Claude
    """
    # Para demo, retornar o código do payload
    return action.payload.get('code', '')


def demo_auto_protection():
    """Demonstração do Auto-Protection System"""

    print("\n" + "="*80)
    print("  MAX-CODE AUTO-PROTECTION SYSTEM DEMO")
    print("  Os Guardians protegem AUTOMATICAMENTE contra violações")
    print("="*80 + "\n")

    # ==================== HABILITAR AUTO-PROTEÇÃO ====================
    print("📋 Step 1: Enabling Auto-Protection (ALWAYS_ON mode)...\n")

    auto_protection = enable_auto_protection(
        enforcement_level=EnforcementLevel.STRICT
    )

    print()

    # ==================== TESTE 1: CÓDIGO COM PLACEHOLDER (VIOLAÇÃO P1) ====================
    print("="*80)
    print("TEST 1: Code with TODO placeholder (P1 VIOLATION)")
    print("="*80 + "\n")

    action_bad = Action(
        type=ActionType.CODE_GENERATION,
        payload={
            'code': '''
def calculate_sum(arr):
    # TODO: implement this function
    pass
''',
            'language': 'python',
        },
        task_id='test_1_todo_placeholder'
    )

    print("📝 Code to validate:")
    print(action_bad.payload['code'])
    print()

    # Auto-Protection AUTOMATICAMENTE protege
    report_1 = auto_protection.protect_action(action_bad, simulate_code_generation)

    print("\n🛡️ Auto-Protection Result:")
    print(f"   Overall Passed: {report_1.overall_passed}")
    print(f"   Pre-execution:  {report_1.pre_execution_verdict.decision.value}")
    print(f"   Violations:     {report_1.total_violations}")
    print()

    if not report_1.overall_passed:
        print("✅ PROTECTION WORKED! Code with placeholder was REJECTED automatically.")
    else:
        print("❌ Protection FAILED (this should not happen)")

    print()

    # ==================== TESTE 2: CÓDIGO COM PREMISSA FALSA (VIOLAÇÃO P3) ====================
    print("="*80)
    print("TEST 2: Bubble sort with O(n log n) claim (P3 VIOLATION)")
    print("="*80 + "\n")

    action_wrong_complexity = Action(
        type=ActionType.CODE_GENERATION,
        payload={
            'code': '''
def bubble_sort(arr):
    """Bubble sort - O(n log n) complexity"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
''',
            'language': 'python',
            'user_prompt': 'Implement bubble sort in O(n log n)',
        },
        task_id='test_2_wrong_complexity'
    )

    print("📝 User prompt: 'Implement bubble sort in O(n log n)'")
    print()

    # Auto-Protection AUTOMATICAMENTE detecta premissa falsa
    report_2 = auto_protection.protect_action(action_wrong_complexity, simulate_code_generation)

    print("\n🛡️ Auto-Protection Result:")
    print(f"   Overall Passed: {report_2.overall_passed}")
    print(f"   Pre-execution:  {report_2.pre_execution_verdict.decision.value}")

    if report_2.pre_execution_verdict.constitutional_result.violations:
        print(f"   Violations detected:")
        for v in report_2.pre_execution_verdict.constitutional_result.violations:
            if v.principle == 'P3':
                print(f"     - [P3] {v.message}")

    print()

    if not report_2.overall_passed:
        print("✅ PROTECTION WORKED! False assumption (bubble sort O(n log n)) was CHALLENGED.")
    else:
        print("⚠️ Warning detected but execution allowed (based on enforcement level)")

    print()

    # ==================== TESTE 3: CÓDIGO INSEGURO (VIOLAÇÃO P2) ====================
    print("="*80)
    print("TEST 3: Code with eval() (P2/P3 SECURITY VIOLATION)")
    print("="*80 + "\n")

    action_insecure = Action(
        type=ActionType.CODE_GENERATION,
        payload={
            'code': '''
def execute_user_code(user_input):
    """Execute user-provided code"""
    result = eval(user_input)
    return result
''',
            'language': 'python',
        },
        task_id='test_3_eval_security'
    )

    print("📝 Code with eval() (code injection vulnerability):")
    print(action_insecure.payload['code'])
    print()

    # Auto-Protection AUTOMATICAMENTE detecta vulnerabilidade
    report_3 = auto_protection.protect_action(action_insecure, simulate_code_generation)

    print("\n🛡️ Auto-Protection Result:")
    print(f"   Overall Passed: {report_3.overall_passed}")

    if report_3.post_execution_verdict:
        print(f"   Post-execution: {report_3.post_execution_verdict.quality.value}")
        print(f"   Security violations: {report_3.post_execution_verdict.metrics.critical_violations}")

    print()

    if not report_3.overall_passed:
        print("✅ PROTECTION WORKED! Insecure code (eval) was REJECTED automatically.")

    print()

    # ==================== TESTE 4: CÓDIGO PERFEITO (SEM VIOLAÇÕES) ====================
    print("="*80)
    print("TEST 4: Perfect code (NO VIOLATIONS)")
    print("="*80 + "\n")

    action_perfect = Action(
        type=ActionType.CODE_GENERATION,
        payload={
            'code': '''
def merge_sort(arr):
    """
    Merge sort implementation
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result
''',
            'language': 'python',
        },
        task_id='test_4_perfect_code',
        metadata={
            'sources': [
                {
                    'type': 'official_docs',
                    'ref': 'https://en.wikipedia.org/wiki/Merge_sort',
                    'description': 'Merge sort algorithm from Wikipedia'
                }
            ]
        }
    )

    print("📝 Perfect merge sort implementation (O(n log n)):")
    print(action_perfect.payload['code'][:200] + "...")
    print()

    # Auto-Protection valida e APROVA
    report_4 = auto_protection.protect_action(action_perfect, simulate_code_generation)

    print("\n🛡️ Auto-Protection Result:")
    print(f"   Overall Passed: {report_4.overall_passed}")
    print(f"   Pre-execution:  {report_4.pre_execution_verdict.decision.value}")

    if report_4.post_execution_verdict:
        print(f"   Post-execution: {report_4.post_execution_verdict.quality.value}")
        print(f"   LEI:           {report_4.post_execution_verdict.metrics.lei:.2f}")
        print(f"   Violations:    {report_4.total_violations}")

    print()

    if report_4.overall_passed:
        print("✅ APPROVED! Perfect code passed all Guardian checks.")

    print()

    # ==================== RELATÓRIO FINAL ====================
    print("="*80)
    print("FINAL PROTECTION REPORT")
    print("="*80 + "\n")

    auto_protection.print_protection_report()

    print("\n" + "="*80)
    print("  CONCLUSÃO")
    print("="*80)
    print("""
Os Guardians protegem o Max-Code AUTOMATICAMENTE:

✅ Bloqueiam código com placeholders/TODOs (P1)
✅ Desafiam premissas falsas (P3)
✅ Detectam vulnerabilidades de segurança (P2/P3)
✅ Aprovam código perfeito e constitucional

NENHUMA intervenção manual necessária.
Os Guardians são a DEFESA PERMANENTE 24/7.

"Porque ele dará ordens aos seus anjos a teu respeito,
 para te guardarem em todos os teus caminhos."
(Salmos 91:11)
""")
    print("="*80 + "\n")


if __name__ == '__main__':
    demo_auto_protection()
