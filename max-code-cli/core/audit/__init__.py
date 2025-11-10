"""
Audit Module - Independent Verification System

"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)

The Audit module provides meta-level verification of agent outputs,
operating independently to ensure truth and protect users.

Key Principle:
NO SYSTEM CAN AUDIT ITSELF HONESTLY.

The Independent Auditor is NOT part of the agent hierarchy - it operates
at meta-level, like an immune system operating independently of the brain.

Components:
- IndependentAuditor: Meta-level verification system
- Task: Task definition for execution
- AgentResult: Result from agent execution
- AuditReport: Complete audit with truth metrics
- CriticalVitalFailure: Exception for critical state

Usage:
    from core.audit import get_auditor, Task, AgentResult

    auditor = get_auditor()
    task = Task(prompt="Create calculator with add, subtract")
    result = AgentResult(success=True, output="...", files_changed=[...])

    report = await auditor.audit_execution(task, result)
    print(report.honest_report)
"""

from .independent_auditor import (
    IndependentAuditor,
    Task,
    AgentResult,
    AuditReport,
    CriticalVitalFailure,
    get_auditor,
)

__all__ = [
    'IndependentAuditor',
    'Task',
    'AgentResult',
    'AuditReport',
    'CriticalVitalFailure',
    'get_auditor',
]
