#!/usr/bin/env python3
"""
Validação sintática completa - CONFIANÇA ZERO
"""
import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class SyntaxValidator:
    """Valida sintaxe e estrutura de arquivos Python"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.stats = {
            "files_checked": 0,
            "files_valid": 0,
            "files_invalid": 0,
            "total_classes": 0,
            "total_functions": 0,
            "total_lines": 0
        }
    
    def validate_file(self, filepath: Path) -> Tuple[bool, List[str]]:
        """Valida um arquivo Python"""
        errors = []
        
        try:
            # Ler arquivo
            content = filepath.read_text()
            self.stats["total_lines"] += content.count("\n")
            
            # Parse AST
            tree = ast.parse(content, filename=str(filepath))
            
            # Contar classes e funções
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.stats["total_classes"] += 1
                elif isinstance(node, ast.FunctionDef):
                    self.stats["total_functions"] += 1
            
            # Verificar placeholders
            placeholder_errors = self._check_placeholders(content, filepath)
            errors.extend(placeholder_errors)
            
            self.stats["files_checked"] += 1
            
            if errors:
                self.stats["files_invalid"] += 1
                return (False, errors)
            else:
                self.stats["files_valid"] += 1
                return (True, [])
        
        except SyntaxError as e:
            error_msg = f"Syntax error: {e.msg} at line {e.lineno}"
            errors.append(error_msg)
            self.stats["files_checked"] += 1
            self.stats["files_invalid"] += 1
            return (False, errors)
        
        except Exception as e:
            error_msg = f"Failed to parse: {str(e)}"
            errors.append(error_msg)
            self.stats["files_checked"] += 1
            self.stats["files_invalid"] += 1
            return (False, errors)
    
    def _check_placeholders(self, content: str, filepath: Path) -> List[str]:
        """Verifica placeholders críticos"""
        errors = []
        
        critical_placeholders = [
            "# TODO: Implement",
            "# FIXME:",
            "pass  # TODO",
            "raise NotImplementedError",
        ]
        
        for placeholder in critical_placeholders:
            if placeholder in content:
                # Contar ocorrências
                count = content.count(placeholder)
                errors.append(f"Found {count} critical placeholder(s): {placeholder}")
        
        return errors
    
    def validate_all(self, files: List[Path]) -> Dict:
        """Valida todos arquivos"""
        results = {}
        
        for filepath in files:
            try:
                relative_path = filepath.relative_to(self.base_path)
            except ValueError:
                relative_path = filepath
                
            is_valid, errors = self.validate_file(filepath)
            
            results[str(relative_path)] = {
                "valid": is_valid,
                "errors": errors
            }
            
            if errors:
                self.errors.append({
                    "file": str(relative_path),
                    "errors": errors
                })
        
        return results
    
    def print_report(self):
        """Imprime relatório"""
        print("="*80)
        print("FASE 2: VALIDAÇÃO SINTÁTICA")
        print("="*80)
        print()
        
        print(f"Files checked:    {self.stats['files_checked']}")
        print(f"Files valid:      {self.stats['files_valid']}")
        print(f"Files invalid:    {self.stats['files_invalid']}")
        print(f"Total classes:    {self.stats['total_classes']}")
        print(f"Total functions:  {self.stats['total_functions']}")
        print(f"Total lines:      {self.stats['total_lines']}")
        print()
        
        if self.errors:
            print("ERRORS FOUND:")
            print("-"*80)
            for error in self.errors:
                print(f"\n❌ {error['file']}:")
                for err in error['errors']:
                    print(f"   {err}")
            print()
            print("="*80)
            print(f"❌ FASE 2 FAILED: {len(self.errors)} files with errors")
            print("="*80)
            return False
        else:
            print("="*80)
            print("✅ FASE 2 PASSED: All files syntactically valid")
            print("="*80)
            return True


def main():
    base_path = "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"
    
    # Lista de arquivos para validar
    files_to_check = [
        # FASE 1
        "ui/streaming.py",
        "core/risk_classifier.py",
        "ui/confirmation.py",
        "core/plan_visualizer.py",
        # FASE 2
        "core/task_models.py",
        "core/task_graph.py",
        "core/task_decomposer.py",
        "core/dependency_resolver.py",
        "prompts/decomposition_prompts.py",
        "core/tools/tool_metadata.py",
        "core/tools/enhanced_registry.py",
        "core/tools/tool_selector.py",
        "core/tools/decorator.py",
        "core/tool_integration.py",
        "core/execution_engine.py",
        "ui/execution_display.py",
        # Testes
        "tests/test_streaming_thinking.py",
        "tests/test_confirmation.py",
        "tests/test_task_decomposition.py",
        "tests/test_tool_selection_system.py",
        "tests/test_execution_engine.py",
    ]
    
    validator = SyntaxValidator(base_path)
    
    # Converter para Path objects
    files = [Path(base_path) / f for f in files_to_check]
    
    # Validar apenas arquivos que existem
    existing_files = [f for f in files if f.exists()]
    
    if len(existing_files) < len(files):
        print(f"⚠️  Warning: {len(files) - len(existing_files)} files not found")
    
    # Validar
    results = validator.validate_all(existing_files)
    
    # Relatório
    success = validator.print_report()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
