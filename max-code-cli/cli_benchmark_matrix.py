"""
Matriz de funcionalidades dos CLIs líderes
Baseado em documentação pública, papers e experiência prática
Padrão: Pagani + Científico
"""
import json
from typing import Dict, List


class CLIBenchmark:
    """Benchmark de funcionalidades dos CLIs líderes"""
    
    def __init__(self):
        self.clis = {
            "claude_code": self.get_claude_code_features(),
            "github_copilot_cli": self.get_copilot_cli_features(),
            "gemini_cli": self.get_gemini_cli_features(),
            "cursor": self.get_cursor_features()
        }
    
    def get_claude_code_features(self) -> Dict:
        """Funcionalidades do Claude Code (Anthropic)"""
        return {
            "name": "Claude Code",
            "provider": "Anthropic",
            "release_date": "2024",
            "core_features": {
                # === PROMPT UNDERSTANDING ===
                "natural_language_understanding": 10,  # Excelente
                "multi_step_decomposition": 10,  # Automático e inteligente
                "context_retention": 9,  # 200K tokens
                "ambiguity_resolution": 9,  # Pede clarification
                "intent_extraction": 10,  # Forte
                
                # === PLANNING ===
                "automatic_planning": 10,  # Cria plano completo
                "dependency_resolution": 9,  # DAG implícito
                "task_prioritization": 8,  # Baseado em dependências
                "plan_visualization": 7,  # Mostra steps
                
                # === EXECUTION ===
                "code_generation": 10,  # State-of-the-art
                "file_editing": 10,  # Multi-file simultâneo
                "command_execution": 10,  # Bash/shell
                "multi_file_changes": 10,  # Coordenado
                "parallel_execution": 7,  # Limitado
                
                # === TOOLS ===
                "file_operations": 10,  # Read/write/edit
                "search_capabilities": 9,  # Grep/ripgrep
                "git_integration": 8,  # Básico
                "terminal_integration": 10,  # Completo
                "code_analysis": 9,  # AST parsing
                
                # === INTELLIGENCE ===
                "error_detection": 9,  # Durante execução
                "auto_correction": 8,  # Retry with fix
                "learning_from_errors": 7,  # Dentro da sessão
                "adaptive_behavior": 8,  # Ajusta estratégia
                "self_reflection": 9,  # Pensa sobre abordagem
                
                # === CONTEXT ===
                "project_awareness": 9,  # Entende estrutura
                "conversation_memory": 9,  # Mantém histórico
                "cross_file_context": 9,  # Navegação inteligente
                "code_understanding": 10,  # Compreende semântica
                
                # === UX ===
                "streaming_output": 10,  # Thinking + action
                "progress_indicators": 9,  # Mostra progresso
                "interactive_confirmation": 8,  # Pergunta antes de ações perigosas
                "undo_capability": 7,  # Git-based
                "diff_preview": 9,  # Mostra mudanças
                
                # === ROBUSTNESS ===
                "retry_logic": 8,
                "fallback_strategies": 7,
                "graceful_degradation": 8,
                "error_recovery": 8
            },
            "strengths": [
                "Entendimento excepcional de prompts complexos",
                "Decomposição automática de tarefas multi-step",
                "Execução coordenada de mudanças em múltiplos arquivos",
                "Contexto de projeto completo (200K tokens)",
                "Auto-correção inteligente com retry",
                "Thinking process transparente"
            ],
            "limitations": [
                "Requer API key Anthropic (pago)",
                "Execução sequencial (não paralela)",
                "Undo limitado a git",
                "Sem custom tools (tools fixos)"
            ],
            "typical_workflow": [
                "1. User: complex prompt",
                "2. Claude: Decomposes into subtasks",
                "3. Claude: Shows plan",
                "4. Claude: Executes step-by-step with thinking",
                "5. Claude: Validates each step",
                "6. Claude: Auto-corrects errors",
                "7. Claude: Reports completion"
            ]
        }
    
    def get_copilot_cli_features(self) -> Dict:
        """Funcionalidades do GitHub Copilot CLI"""
        return {
            "name": "GitHub Copilot CLI",
            "provider": "GitHub/OpenAI",
            "release_date": "2023",
            "core_features": {
                "natural_language_understanding": 9,
                "multi_step_decomposition": 8,
                "context_retention": 8,
                "ambiguity_resolution": 8,
                "intent_extraction": 9,
                
                "automatic_planning": 8,
                "dependency_resolution": 7,
                "task_prioritization": 7,
                "plan_visualization": 6,
                
                "code_generation": 9,
                "file_editing": 9,
                "command_execution": 9,
                "multi_file_changes": 8,
                "parallel_execution": 6,
                
                "file_operations": 9,
                "search_capabilities": 8,
                "git_integration": 10,  # Native GitHub
                "terminal_integration": 9,
                "code_analysis": 8,
                
                "error_detection": 8,
                "auto_correction": 7,
                "learning_from_errors": 6,
                "adaptive_behavior": 7,
                "self_reflection": 7,
                
                "project_awareness": 8,
                "conversation_memory": 8,
                "cross_file_context": 8,
                "code_understanding": 9,
                
                "streaming_output": 9,
                "progress_indicators": 8,
                "interactive_confirmation": 7,
                "undo_capability": 6,
                "diff_preview": 8,
                
                "retry_logic": 7,
                "fallback_strategies": 6,
                "graceful_degradation": 7,
                "error_recovery": 7
            },
            "strengths": [
                "Integração nativa com GitHub",
                "Forte em geração de código",
                "Boa experiência de usuário",
                "Suporte a múltiplas linguagens",
                "Command suggestions (gh, git)"
            ],
            "limitations": [
                "Planejamento menos sofisticado que Claude",
                "Auto-correção limitada",
                "Requer GitHub Copilot subscription",
                "Contexto menor que Claude"
            ],
            "typical_workflow": [
                "1. User: prompt or question",
                "2. Copilot: Suggests command or code",
                "3. User: Confirms",
                "4. Copilot: Executes",
                "5. Copilot: Reports result"
            ]
        }
    
    def get_gemini_cli_features(self) -> Dict:
        """Funcionalidades do Gemini CLI (Google)"""
        return {
            "name": "Gemini CLI",
            "provider": "Google",
            "release_date": "2024",
            "core_features": {
                "natural_language_understanding": 9,
                "multi_step_decomposition": 9,
                "context_retention": 9,  # 1M tokens context
                "ambiguity_resolution": 8,
                "intent_extraction": 9,
                
                "automatic_planning": 9,
                "dependency_resolution": 8,
                "task_prioritization": 8,
                "plan_visualization": 7,
                
                "code_generation": 9,
                "file_editing": 9,
                "command_execution": 9,
                "multi_file_changes": 9,
                "parallel_execution": 7,
                
                "file_operations": 9,
                "search_capabilities": 9,
                "git_integration": 7,
                "terminal_integration": 9,
                "code_analysis": 8,
                
                "error_detection": 8,
                "auto_correction": 8,
                "learning_from_errors": 7,
                "adaptive_behavior": 8,
                "self_reflection": 8,
                
                "project_awareness": 9,
                "conversation_memory": 9,
                "cross_file_context": 9,
                "code_understanding": 9,
                
                "streaming_output": 10,  # Excelente UX
                "progress_indicators": 9,
                "interactive_confirmation": 8,
                "undo_capability": 7,
                "diff_preview": 9,
                
                "retry_logic": 8,
                "fallback_strategies": 7,
                "graceful_degradation": 8,
                "error_recovery": 8
            },
            "strengths": [
                "Contexto massivo (1M tokens)",
                "Excelente UX com streaming",
                "Forte entendimento de contexto",
                "Boa decomposição de tarefas",
                "Integração com Google Cloud"
            ],
            "limitations": [
                "Menos maduro que Claude/Copilot",
                "Documentação limitada",
                "Ecossistema em desenvolvimento",
                "Git integration básico"
            ],
            "typical_workflow": [
                "1. User: complex prompt",
                "2. Gemini: Thinking stream",
                "3. Gemini: Proposes plan",
                "4. Gemini: Executes with progress",
                "5. Gemini: Validates",
                "6. Gemini: Reports with suggestions"
            ]
        }
    
    def get_cursor_features(self) -> Dict:
        """Funcionalidades do Cursor (IDE AI)"""
        return {
            "name": "Cursor",
            "provider": "Cursor",
            "release_date": "2023",
            "core_features": {
                "natural_language_understanding": 9,
                "multi_step_decomposition": 8,
                "context_retention": 9,
                "ambiguity_resolution": 8,
                "intent_extraction": 9,
                
                "automatic_planning": 7,
                "dependency_resolution": 6,
                "task_prioritization": 6,
                "plan_visualization": 8,  # Visual no IDE
                
                "code_generation": 10,  # Inline excelente
                "file_editing": 10,  # Editor integrado
                "command_execution": 8,
                "multi_file_changes": 9,
                "parallel_execution": 5,
                
                "file_operations": 10,  # IDE nativo
                "search_capabilities": 9,
                "git_integration": 9,  # VSCode-based
                "terminal_integration": 9,
                "code_analysis": 10,  # LSP integration
                
                "error_detection": 9,
                "auto_correction": 7,
                "learning_from_errors": 6,
                "adaptive_behavior": 7,
                "self_reflection": 6,
                
                "project_awareness": 10,  # IDE awareness
                "conversation_memory": 8,
                "cross_file_context": 10,  # IDE symbols
                "code_understanding": 10,  # AST + LSP
                
                "streaming_output": 8,
                "progress_indicators": 7,
                "interactive_confirmation": 6,
                "undo_capability": 10,  # Editor undo
                "diff_preview": 10,  # Visual diff
                
                "retry_logic": 6,
                "fallback_strategies": 5,
                "graceful_degradation": 6,
                "error_recovery": 6
            },
            "strengths": [
                "IDE integration perfeita",
                "Inline code generation excelente",
                "Undo/redo nativo",
                "Visual diff",
                "Project awareness completo",
                "LSP integration"
            ],
            "limitations": [
                "Menos autônomo que Claude",
                "Planejamento básico",
                "Requer interação humana frequente",
                "Não é CLI (é IDE)"
            ],
            "typical_workflow": [
                "1. User: Cmd+K with prompt",
                "2. Cursor: Generates code inline",
                "3. User: Reviews diff",
                "4. User: Accepts/rejects",
                "5. Cursor: Applies changes"
            ]
        }
    
    def calculate_average_scores(self) -> Dict:
        """Calcula score médio por categoria"""
        categories = set()
        for cli_data in self.clis.values():
            categories.update(cli_data["core_features"].keys())
        
        averages = {}
        for category in categories:
            scores = []
            for cli_data in self.clis.values():
                if category in cli_data["core_features"]:
                    scores.append(cli_data["core_features"][category])
            averages[category] = sum(scores) / len(scores) if scores else 0
        
        return averages
    
    def get_leader_board(self) -> Dict:
        """Identifica líder em cada categoria"""
        categories = set()
        for cli_data in self.clis.values():
            categories.update(cli_data["core_features"].keys())
        
        leaders = {}
        for category in categories:
            best_cli = None
            best_score = 0
            
            for cli_name, cli_data in self.clis.items():
                score = cli_data["core_features"].get(category, 0)
                if score > best_score:
                    best_score = score
                    best_cli = cli_name
            
            leaders[category] = {
                "cli": best_cli,
                "score": best_score
            }
        
        return leaders
    
    def generate_comparison_matrix(self) -> str:
        """Gera matriz de comparação formatada"""
        lines = []
        lines.append("="*130)
        lines.append("CLI FEATURE COMPARISON MATRIX - SCIENTIFIC BENCHMARK")
        lines.append("="*130)
        lines.append("")
        
        # Header
        cli_names = list(self.clis.keys())
        header = f"{'Feature':<40} | " + " | ".join(f"{name:<22}" for name in cli_names) + " | Avg"
        lines.append(header)
        lines.append("-"*130)
        
        # Get all features
        all_features = set()
        for cli_data in self.clis.values():
            all_features.update(cli_data["core_features"].keys())
        
        # Sort features by category
        feature_order = sorted(list(all_features))
        
        # Calculate category averages
        averages = self.calculate_average_scores()
        
        # Print features
        for feature in feature_order:
            if feature in all_features:
                row = f"{feature.replace('_', ' ').title():<40} | "
                
                scores = []
                for cli_name in cli_names:
                    score = self.clis[cli_name]["core_features"].get(feature, 0)
                    scores.append(score)
                    
                    # Color coding
                    if score >= 9:
                        row += f"🟢 {score:2d}                | "
                    elif score >= 7:
                        row += f"🟡 {score:2d}                | "
                    elif score >= 5:
                        row += f"🟠 {score:2d}                | "
                    else:
                        row += f"🔴 {score:2d}                | "
                
                # Add average
                avg = averages.get(feature, 0)
                row += f"{avg:.1f}"
                
                lines.append(row.rstrip(" |"))
        
        lines.append("="*130)
        
        # Overall Averages
        lines.append("\nOVERALL AVERAGE SCORES:")
        cli_averages = {}
        for cli_name in cli_names:
            scores = list(self.clis[cli_name]["core_features"].values())
            avg = sum(scores) / len(scores)
            cli_averages[cli_name] = avg
            lines.append(f"  {cli_name:<25}: {avg:.1f}/10")
        
        lines.append("")
        
        # Rankings
        lines.append("RANKINGS BY OVERALL SCORE:")
        sorted_clis = sorted(cli_averages.items(), key=lambda x: x[1], reverse=True)
        for i, (cli_name, score) in enumerate(sorted_clis, 1):
            medal = ["🥇", "🥈", "🥉", "  "][min(i-1, 3)]
            lines.append(f"  {medal} {i}. {cli_name:<25}: {score:.1f}/10")
        
        lines.append("")
        lines.append("="*130)
        
        return "\n".join(lines)
    
    def identify_gaps_for_max_code(self, max_code_analysis: Dict) -> Dict:
        """Identifica gaps do max-code comparado aos líderes"""
        
        # Calculate target (average of top 2 CLIs)
        cli_averages = {}
        for cli_name, cli_data in self.clis.items():
            scores = list(cli_data["core_features"].values())
            cli_averages[cli_name] = sum(scores) / len(scores)
        
        top_2 = sorted(cli_averages.items(), key=lambda x: x[1], reverse=True)[:2]
        
        gaps = {
            "critical_missing": [],  # Score 0-3 vs leader 8-10
            "major_gaps": [],        # Score 4-6 vs leader 8-10
            "minor_gaps": [],        # Score 7-8 vs leader 9-10
            "on_par": [],            # Score 9-10
            "target_baseline": {},
            "top_2_clis": [cli[0] for cli in top_2],
            "target_average": sum(cli[1] for cli in top_2) / 2
        }
        
        # Define target baseline (average of top 2)
        for feature in self.clis[top_2[0][0]]["core_features"].keys():
            scores = []
            for cli_name, _ in top_2:
                scores.append(self.clis[cli_name]["core_features"][feature])
            gaps["target_baseline"][feature] = sum(scores) / len(scores)
        
        # Estimate max-code scores
        max_code_score_map = self._estimate_max_code_scores(max_code_analysis)
        
        for feature, target_score in gaps["target_baseline"].items():
            max_score = max_code_score_map.get(feature, 0)
            diff = target_score - max_score
            
            if max_score <= 3 and target_score >= 8:
                gaps["critical_missing"].append({
                    "feature": feature,
                    "current": max_score,
                    "target": target_score,
                    "gap": diff
                })
            elif max_score <= 6 and target_score >= 8:
                gaps["major_gaps"].append({
                    "feature": feature,
                    "current": max_score,
                    "target": target_score,
                    "gap": diff
                })
            elif max_score <= 8 and target_score >= 9:
                gaps["minor_gaps"].append({
                    "feature": feature,
                    "current": max_score,
                    "target": target_score,
                    "gap": diff
                })
            elif max_score >= 9:
                gaps["on_par"].append({
                    "feature": feature,
                    "current": max_score,
                    "target": target_score
                })
        
        return gaps
    
    def _estimate_max_code_scores(self, analysis: Dict) -> Dict:
        """
        Estima scores do max-code baseado na análise
        Heurística científica baseada em capabilities detectadas
        """
        scores = {}
        
        # === PROMPT UNDERSTANDING ===
        # Natural language understanding (via LLM)
        if analysis.get("llm_integration", {}).get("has_anthropic"):
            scores["natural_language_understanding"] = 8  # Claude SDK
        else:
            scores["natural_language_understanding"] = 5
        
        # Multi-step decomposition
        if analysis.get("planning", {}).get("has_task_decomposition"):
            scores["multi_step_decomposition"] = 7
        else:
            scores["multi_step_decomposition"] = 3
        
        # Context retention
        if analysis.get("context_management", {}).get("has_context_module"):
            scores["context_retention"] = 6
        else:
            scores["context_retention"] = 3
        
        # Ambiguity resolution (requires explicit handling)
        scores["ambiguity_resolution"] = 4
        
        # Intent extraction (via LLM)
        if analysis.get("llm_integration", {}).get("has_anthropic"):
            scores["intent_extraction"] = 7
        else:
            scores["intent_extraction"] = 4
        
        # === PLANNING ===
        if analysis.get("planning", {}).get("has_task_planner"):
            scores["automatic_planning"] = 7
        else:
            scores["automatic_planning"] = 2
        
        if analysis.get("planning", {}).get("has_dependency_management"):
            scores["dependency_resolution"] = 7
        else:
            scores["dependency_resolution"] = 2
        
        scores["task_prioritization"] = 3
        scores["plan_visualization"] = 4
        
        # === EXECUTION ===
        if analysis.get("agents", {}).get("has_code_agent"):
            scores["code_generation"] = 8  # Com Claude
        else:
            scores["code_generation"] = 4
        
        if analysis.get("execution", {}).get("can_edit_files"):
            scores["file_editing"] = 8
        else:
            scores["file_editing"] = 3
        
        if analysis.get("execution", {}).get("can_run_commands"):
            scores["command_execution"] = 7
        else:
            scores["command_execution"] = 2
        
        if analysis.get("multi_step", {}).get("has_workflow"):
            scores["multi_file_changes"] = 7
        else:
            scores["multi_file_changes"] = 3
        
        scores["parallel_execution"] = 2  # Não detectado
        
        # === TOOLS ===
        if analysis.get("tools", {}).get("has_file_tools"):
            scores["file_operations"] = 8
        else:
            scores["file_operations"] = 4
        
        if analysis.get("tools", {}).get("has_grep"):
            scores["search_capabilities"] = 7
        else:
            scores["search_capabilities"] = 4
        
        scores["git_integration"] = 5  # Básico via subprocess
        
        if analysis.get("execution", {}).get("has_executor_bridge"):
            scores["terminal_integration"] = 7
        else:
            scores["terminal_integration"] = 4
        
        scores["code_analysis"] = 6  # Via tools + LLM
        
        # === INTELLIGENCE ===
        if analysis.get("error_handling", {}).get("try_except_count") > 100:
            scores["error_detection"] = 7
        else:
            scores["error_detection"] = 4
        
        if analysis.get("self_correction", {}).get("has_auto_fix"):
            scores["auto_correction"] = 6
        else:
            scores["auto_correction"] = 2
        
        scores["learning_from_errors"] = 3  # Não detectado claramente
        
        if analysis.get("error_handling", {}).get("has_retry_logic"):
            scores["adaptive_behavior"] = 5
        else:
            scores["adaptive_behavior"] = 3
        
        scores["self_reflection"] = 4  # Via LLM mas não explícito
        
        # === CONTEXT ===
        if analysis.get("context_management", {}).get("has_context_module"):
            scores["project_awareness"] = 6
        else:
            scores["project_awareness"] = 3
        
        if analysis.get("context_management", {}).get("has_history"):
            scores["conversation_memory"] = 6
        else:
            scores["conversation_memory"] = 3
        
        scores["cross_file_context"] = 5
        
        if analysis.get("agents", {}).get("has_code_agent"):
            scores["code_understanding"] = 8  # Via Claude
        else:
            scores["code_understanding"] = 4
        
        # === UX ===
        if analysis.get("llm_integration", {}).get("has_streaming"):
            scores["streaming_output"] = 8
        else:
            scores["streaming_output"] = 4
        
        scores["progress_indicators"] = 5  # Parcial
        scores["interactive_confirmation"] = 4  # Não claro
        scores["undo_capability"] = 3  # Limitado
        scores["diff_preview"] = 5  # Via file_editor
        
        # === ROBUSTNESS ===
        if analysis.get("error_handling", {}).get("has_retry_logic"):
            scores["retry_logic"] = 7
        else:
            scores["retry_logic"] = 3
        
        if analysis.get("error_handling", {}).get("has_fallback"):
            scores["fallback_strategies"] = 6
        else:
            scores["fallback_strategies"] = 3
        
        scores["graceful_degradation"] = 5
        
        if analysis.get("self_correction", {}).get("has_fix_agent"):
            scores["error_recovery"] = 6
        else:
            scores["error_recovery"] = 3
        
        return scores


# Execute benchmark
if __name__ == "__main__":
    benchmark = CLIBenchmark()
    
    # Print comparison matrix
    matrix = benchmark.generate_comparison_matrix()
    print(matrix)
    
    # Save to file
    with open("cli_benchmark.json", "w") as f:
        json.dump(benchmark.clis, f, indent=2)
    
    # Print leader board
    print("\n\n")
    print("="*80)
    print("LEADER BOARD BY CATEGORY")
    print("="*80)
    leaders = benchmark.get_leader_board()
    for feature, info in sorted(leaders.items()):
        print(f"{feature:<40}: {info['cli']:<25} ({info['score']}/10)")
    
    print("\n✅ Benchmark saved to: cli_benchmark.json")
