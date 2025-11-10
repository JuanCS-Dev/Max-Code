"""
Análise científica de capacidades do max-code-cli
Padrão: Pagani + Científico
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Set
import json


class CapabilityAnalyzer:
    """Analisa capacidades do max-code-cli"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.capabilities = {}
        # Excluir maximus_services_reference da análise
        self.exclude_paths = ['maximus_services_reference', '.git', '__pycache__', 'htmlcov']
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        return any(exclude in str(path) for exclude in self.exclude_paths)
    
    def analyze_all(self) -> Dict:
        """Análise completa"""
        return {
            "project_stats": self.analyze_project_stats(),
            "commands": self.analyze_commands(),
            "agents": self.analyze_agents(),
            "tools": self.analyze_tools(),
            "llm_integration": self.analyze_llm_integration(),
            "planning": self.analyze_planning_capability(),
            "execution": self.analyze_execution_capability(),
            "context_management": self.analyze_context_management(),
            "error_handling": self.analyze_error_handling(),
            "multi_step": self.analyze_multi_step(),
            "self_correction": self.analyze_self_correction(),
            "deter_agent": self.analyze_deter_agent_framework()
        }
    
    def analyze_project_stats(self) -> Dict:
        """Estatísticas do projeto"""
        py_files = [f for f in self.base_path.rglob("*.py") if not self._should_exclude(f)]
        
        total_lines = 0
        for py_file in py_files:
            try:
                total_lines += len(py_file.read_text(errors="ignore").splitlines())
            except:
                pass
        
        return {
            "total_python_files": len(py_files),
            "total_lines_of_code": total_lines,
            "commands_count": len(list((self.base_path / "cli").glob("*_command.py"))),
            "agents_count": len(list((self.base_path / "agents").glob("*_agent.py"))),
            "has_core_module": (self.base_path / "core").exists(),
            "has_sdk": (self.base_path / "sdk").exists()
        }
    
    def analyze_commands(self) -> Dict:
        """Analisa comandos disponíveis"""
        commands = set()
        
        cli_path = self.base_path / "cli"
        if cli_path.exists():
            for py_file in cli_path.glob("*.py"):
                content = py_file.read_text(errors="ignore")
                
                # Click commands
                click_matches = re.findall(r'@click\.command\(["\']?name=["\'](\w+)["\']?\)', content)
                commands.update(click_matches)
                
                # Command from filename
                if py_file.name.endswith("_command.py"):
                    cmd_name = py_file.stem.replace("_command", "")
                    commands.add(cmd_name)
        
        return {
            "count": len(commands),
            "commands": sorted(list(commands)),
            "has_basic_commands": any(c in commands for c in ["code", "edit", "fix", "test"]),
            "has_analyze": "analyze" in commands,
            "has_health": "health" in commands,
            "has_logs": "logs" in commands
        }
    
    def analyze_agents(self) -> Dict:
        """Analisa agentes implementados"""
        agents = []
        
        agents_path = self.base_path / "agents"
        if agents_path.exists():
            for py_file in agents_path.glob("*_agent.py"):
                content = py_file.read_text(errors="ignore")
                
                # Encontrar classes de agente
                agent_classes = re.findall(r'^class (\w+Agent)\(', content, re.MULTILINE)
                
                for agent_class in agent_classes:
                    # Analisar métodos
                    methods = re.findall(r'    def (\w+)\(', content)
                    
                    agents.append({
                        "name": agent_class,
                        "file": py_file.name,
                        "methods": methods,
                        "lines": content.count("\n")
                    })
        
        return {
            "count": len(agents),
            "agents": agents,
            "has_code_agent": any("code" in a["name"].lower() for a in agents),
            "has_planning_agent": any("plan" in a["name"].lower() for a in agents),
            "has_architect_agent": any("architect" in a["name"].lower() for a in agents),
            "has_fix_agent": any("fix" in a["name"].lower() for a in agents),
            "has_test_agent": any("test" in a["name"].lower() for a in agents)
        }
    
    def analyze_tools(self) -> Dict:
        """Analisa ferramentas disponíveis"""
        tools = []
        
        tools_path = self.base_path / "core" / "tools"
        if tools_path.exists():
            for py_file in tools_path.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                
                content = py_file.read_text(errors="ignore")
                
                # Funções que parecem ferramentas
                tool_functions = re.findall(r'^def (\w+)\(', content, re.MULTILINE)
                tool_classes = re.findall(r'^class (\w+):', content, re.MULTILINE)
                
                tools.append({
                    "file": py_file.name,
                    "functions": tool_functions,
                    "classes": tool_classes,
                    "count": len(tool_functions) + len(tool_classes)
                })
        
        total_tools = sum(t["count"] for t in tools)
        
        return {
            "count": total_tools,
            "tool_files": len(tools),
            "tools": tools,
            "has_file_tools": any("file" in str(t).lower() for t in tools),
            "has_exec_tools": any("exec" in str(t).lower() or "executor" in str(t).lower() for t in tools),
            "has_grep": any("grep" in str(t).lower() for t in tools),
            "has_editor": any("editor" in str(t).lower() for t in tools)
        }
    
    def analyze_llm_integration(self) -> Dict:
        """Analisa integração com LLMs"""
        llm_info = {
            "has_anthropic": False,
            "has_openai": False,
            "has_streaming": False,
            "has_function_calling": False,
            "llm_files": []
        }
        
        llm_path = self.base_path / "core" / "llm"
        if llm_path.exists():
            llm_files = list(llm_path.glob("*.py"))
            llm_info["llm_files"] = [f.name for f in llm_files]
            
            for py_file in llm_files:
                content = py_file.read_text(errors="ignore")
                
                if "anthropic" in content or "claude" in content.lower():
                    llm_info["has_anthropic"] = True
                
                if "openai" in content or "gpt" in content.lower():
                    llm_info["has_openai"] = True
                
                if "stream" in content.lower():
                    llm_info["has_streaming"] = True
                
                if "function_call" in content or "tool_call" in content or "tools=" in content:
                    llm_info["has_function_calling"] = True
        
        return llm_info
    
    def analyze_planning_capability(self) -> Dict:
        """Analisa capacidade de planejamento"""
        planning_indicators = {
            "has_planning_module": False,
            "has_task_planner": False,
            "has_task_decomposition": False,
            "has_dependency_management": False,
            "planning_keywords_count": 0,
            "planning_files": []
        }
        
        # Check for task_planner.py
        task_planner = self.base_path / "core" / "task_planner.py"
        if task_planner.exists():
            planning_indicators["has_task_planner"] = True
            planning_indicators["planning_files"].append("task_planner.py")
            
            content = task_planner.read_text(errors="ignore")
            
            if "decompose" in content.lower():
                planning_indicators["has_task_decomposition"] = True
            
            if "dependency" in content.lower() or "depends" in content.lower():
                planning_indicators["has_dependency_management"] = True
        
        # Check for PlanAgent
        plan_agent = self.base_path / "agents" / "plan_agent.py"
        if plan_agent.exists():
            planning_indicators["has_planning_module"] = True
            planning_indicators["planning_files"].append("plan_agent.py")
        
        # Count keywords across all files
        keywords = ["plan", "decompose", "break down", "subtask", "dependency", "sequence", "workflow"]
        
        for py_file in self.base_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            
            try:
                content = py_file.read_text(errors="ignore").lower()
                for keyword in keywords:
                    planning_indicators["planning_keywords_count"] += content.count(keyword)
            except:
                pass
        
        return planning_indicators
    
    def analyze_execution_capability(self) -> Dict:
        """Analisa capacidade de execução"""
        exec_info = {
            "can_execute_code": False,
            "can_edit_files": False,
            "can_run_commands": False,
            "has_sandbox": False,
            "has_executor_bridge": False
        }
        
        # Check for executor_bridge
        executor_bridge = self.base_path / "core" / "tools" / "executor_bridge.py"
        if executor_bridge.exists():
            exec_info["has_executor_bridge"] = True
        
        for py_file in self.base_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            
            try:
                content = py_file.read_text(errors="ignore")
                
                if "subprocess" in content or "exec(" in content:
                    exec_info["can_execute_code"] = True
                
                if "write_file" in content or "create_file" in content or ("open(" in content and '"w"' in content):
                    exec_info["can_edit_files"] = True
                
                if "subprocess.run" in content or "os.system" in content:
                    exec_info["can_run_commands"] = True
                
                if "docker" in content.lower() or "sandbox" in content.lower():
                    exec_info["has_sandbox"] = True
            except:
                pass
        
        return exec_info
    
    def analyze_context_management(self) -> Dict:
        """Analisa gerenciamento de contexto"""
        context_info = {
            "has_context_module": False,
            "has_history": False,
            "has_memory": False,
            "context_size_limit": None,
            "context_files": []
        }
        
        # Check for context directory
        context_path = self.base_path / "core" / "context"
        if context_path.exists():
            context_info["has_context_module"] = True
            context_info["context_files"] = [f.name for f in context_path.glob("*.py")]
        
        for py_file in self.base_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            
            try:
                content = py_file.read_text(errors="ignore").lower()
                
                if "history" in content:
                    context_info["has_history"] = True
                
                if "memory" in content:
                    context_info["has_memory"] = True
                
                # Procurar limites de contexto
                limit_match = re.search(r'context.*(?:limit|size|max).*?(\d+)', content)
                if limit_match:
                    context_info["context_size_limit"] = int(limit_match.group(1))
            except:
                pass
        
        return context_info
    
    def analyze_error_handling(self) -> Dict:
        """Analisa tratamento de erros"""
        error_info = {
            "try_except_count": 0,
            "has_retry_logic": False,
            "has_fallback": False,
            "error_recovery_count": 0
        }
        
        for py_file in self.base_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            
            try:
                content = py_file.read_text(errors="ignore")
                
                error_info["try_except_count"] += content.count("try:") + content.count("except ")
                
                if "retry" in content.lower() or "attempt" in content.lower():
                    error_info["has_retry_logic"] = True
                
                if "fallback" in content.lower() or "alternative" in content.lower():
                    error_info["has_fallback"] = True
                
                error_info["error_recovery_count"] += content.lower().count("recover") + content.lower().count("fix error")
            except:
                pass
        
        return error_info
    
    def analyze_multi_step(self) -> Dict:
        """Analisa capacidade multi-step"""
        multi_step_info = {
            "has_workflow": False,
            "has_pipeline": False,
            "has_chaining": False,
            "step_keywords_count": 0,
            "workflow_files": []
        }
        
        keywords = ["step", "workflow", "pipeline", "chain", "sequence", "orchestrat"]
        
        for py_file in self.base_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            
            try:
                content = py_file.read_text(errors="ignore").lower()
                
                if "workflow" in content:
                    multi_step_info["has_workflow"] = True
                    if "workflow" in py_file.name.lower():
                        multi_step_info["workflow_files"].append(py_file.name)
                
                if "pipeline" in content:
                    multi_step_info["has_pipeline"] = True
                
                if "chain" in content:
                    multi_step_info["has_chaining"] = True
                
                for keyword in keywords:
                    multi_step_info["step_keywords_count"] += content.count(keyword)
            except:
                pass
        
        return multi_step_info
    
    def analyze_self_correction(self) -> Dict:
        """Analisa capacidade de auto-correção"""
        self_correction_info = {
            "has_self_correction": False,
            "has_validation": False,
            "has_auto_fix": False,
            "correction_keywords_count": 0,
            "has_fix_agent": False
        }
        
        # Check for FixAgent
        fix_agent = self.base_path / "agents" / "fix_agent.py"
        if fix_agent.exists():
            self_correction_info["has_fix_agent"] = True
        
        keywords = ["self correct", "auto fix", "validate", "verify", "check result", "fix error"]
        
        for py_file in self.base_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            
            try:
                content = py_file.read_text(errors="ignore").lower()
                
                if "self" in content and "correct" in content:
                    self_correction_info["has_self_correction"] = True
                
                if "validate" in content or "verify" in content:
                    self_correction_info["has_validation"] = True
                
                if "auto" in content and "fix" in content:
                    self_correction_info["has_auto_fix"] = True
                
                for keyword in keywords:
                    self_correction_info["correction_keywords_count"] += content.count(keyword)
            except:
                pass
        
        return self_correction_info
    
    def analyze_deter_agent_framework(self) -> Dict:
        """Analisa framework DETER-AGENT"""
        deter_info = {
            "has_deter_agent": False,
            "has_constitutional": False,
            "deter_files": [],
            "constitutional_files": []
        }
        
        # Check for DETER-AGENT framework
        deter_path = self.base_path / "core" / "deter_agent"
        if deter_path.exists():
            deter_info["has_deter_agent"] = True
            deter_info["deter_files"] = [f.name for f in deter_path.rglob("*.py")]
        
        # Check for Constitutional framework
        constitutional_path = self.base_path / "core" / "constitutional"
        if constitutional_path.exists():
            deter_info["has_constitutional"] = True
            deter_info["constitutional_files"] = [f.name for f in constitutional_path.rglob("*.py")]
        
        return deter_info
    
    def generate_report(self) -> str:
        """Gera relatório formatado"""
        analysis = self.analyze_all()
        
        report = []
        report.append("="*80)
        report.append("MAX-CODE-CLI CAPABILITY ANALYSIS")
        report.append("="*80)
        report.append("")
        
        # Project Stats
        stats = analysis["project_stats"]
        report.append("📊 PROJECT STATISTICS")
        report.append(f"  Python files: {stats['total_python_files']}")
        report.append(f"  Lines of code: {stats['total_lines_of_code']:,}")
        report.append(f"  Commands: {stats['commands_count']}")
        report.append(f"  Agents: {stats['agents_count']}")
        report.append(f"  Has core module: {stats['has_core_module']}")
        report.append(f"  Has SDK: {stats['has_sdk']}")
        report.append("")
        
        # Commands
        report.append("📋 COMMANDS")
        report.append(f"  Total: {analysis['commands']['count']}")
        report.append(f"  Has basic commands: {analysis['commands']['has_basic_commands']}")
        report.append(f"  Commands: {', '.join(analysis['commands']['commands'][:15])}")
        report.append("")
        
        # Agents
        report.append("🤖 AGENTS")
        report.append(f"  Total: {analysis['agents']['count']}")
        report.append(f"  Has code agent: {analysis['agents']['has_code_agent']}")
        report.append(f"  Has planning agent: {analysis['agents']['has_planning_agent']}")
        report.append(f"  Has architect agent: {analysis['agents']['has_architect_agent']}")
        report.append(f"  Has fix agent: {analysis['agents']['has_fix_agent']}")
        report.append(f"  Has test agent: {analysis['agents']['has_test_agent']}")
        report.append("")
        
        # Tools
        report.append("🔧 TOOLS")
        report.append(f"  Total: {analysis['tools']['count']}")
        report.append(f"  Tool files: {analysis['tools']['tool_files']}")
        report.append(f"  Has file tools: {analysis['tools']['has_file_tools']}")
        report.append(f"  Has exec tools: {analysis['tools']['has_exec_tools']}")
        report.append(f"  Has grep: {analysis['tools']['has_grep']}")
        report.append(f"  Has editor: {analysis['tools']['has_editor']}")
        report.append("")
        
        # LLM Integration
        report.append("🧠 LLM INTEGRATION")
        for key, value in analysis['llm_integration'].items():
            if key != 'llm_files':
                report.append(f"  {key}: {value}")
        report.append("")
        
        # Planning
        report.append("📐 PLANNING CAPABILITY")
        for key, value in analysis['planning'].items():
            if key != 'planning_files':
                report.append(f"  {key}: {value}")
        report.append("")
        
        # Execution
        report.append("⚙️ EXECUTION CAPABILITY")
        for key, value in analysis['execution'].items():
            report.append(f"  {key}: {value}")
        report.append("")
        
        # Context
        report.append("💭 CONTEXT MANAGEMENT")
        for key, value in analysis['context_management'].items():
            if key != 'context_files':
                report.append(f"  {key}: {value}")
        report.append("")
        
        # Error Handling
        report.append("🛡️ ERROR HANDLING")
        for key, value in analysis['error_handling'].items():
            report.append(f"  {key}: {value}")
        report.append("")
        
        # Multi-step
        report.append("🔄 MULTI-STEP CAPABILITY")
        for key, value in analysis['multi_step'].items():
            if key != 'workflow_files':
                report.append(f"  {key}: {value}")
        report.append("")
        
        # Self-correction
        report.append("🔍 SELF-CORRECTION")
        for key, value in analysis['self_correction'].items():
            report.append(f"  {key}: {value}")
        report.append("")
        
        # DETER-AGENT
        report.append("🏛️ DETER-AGENT FRAMEWORK")
        for key, value in analysis['deter_agent'].items():
            if not isinstance(value, list):
                report.append(f"  {key}: {value}")
        report.append("")
        
        report.append("="*80)
        
        return "\n".join(report)


# Executar análise
if __name__ == "__main__":
    analyzer = CapabilityAnalyzer("/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli")
    
    # Gerar relatório
    report = analyzer.generate_report()
    print(report)
    
    # Salvar JSON
    analysis = analyzer.analyze_all()
    with open("max_code_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    print("\n✅ Analysis saved to: max_code_analysis.json")
