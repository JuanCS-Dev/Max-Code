"""
Integration Test Suite
Constitutional AI v3.0 - FASE 2

Tests integration between components (Tools, Agents, CLI).
Following Anthropic best practices: Real integration, not mocks.

Structure:
- test_agent_tool_integration.py - Agents using Tools
- test_cli_commands.py - CLI command execution
- test_e2e_flows.py - End-to-end workflows
"""

__all__ = [
    'test_agent_tool_integration',
    'test_cli_commands',
    'test_e2e_flows',
]
