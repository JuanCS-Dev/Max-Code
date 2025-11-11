#!/usr/bin/env python3
"""
Validação de imports - CONFIANÇA ZERO
Verifica se todos imports funcionam
"""
import sys
import importlib
from pathlib import Path


def validate_imports():
    """Valida todos imports"""
    base_path = "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"
    sys.path.insert(0, base_path)
    
    print("="*80)
    print("FASE 3: VALIDAÇÃO DE IMPORTS")
    print("="*80)
    print()
    
    modules_to_test = [
        # FASE 1
        ("ui.streaming", ["StreamingDisplay"]),
        ("core.risk_classifier", ["RiskClassifier", "RiskLevel"]),
        ("ui.confirmation", ["ConfirmationUI"]),
        ("core.plan_visualizer", ["PlanVisualizer"]),
        
        # FASE 2
        ("core.task_models", ["Task", "EnhancedExecutionPlan", "TaskStatus", "TaskType"]),
        ("core.task_graph", ["TaskGraph"]),
        ("core.task_decomposer", ["TaskDecomposer", "TaskDecomposerFactory"]),
        ("core.dependency_resolver", ["DependencyResolver"]),
        ("prompts.decomposition_prompts", ["DecompositionPrompts"]),
        ("core.tools.tool_metadata", ["EnhancedToolMetadata", "ToolCategory"]),
        ("core.tools.enhanced_registry", ["EnhancedToolRegistry"]),
        ("core.tools.tool_selector", ["ToolSelector"]),
        ("core.tools.decorator", ["enhanced_tool"]),
        ("core.tool_integration", ["ToolIntegration"]),
        ("core.execution_engine", ["ExecutionEngine", "RetryStrategy"]),
        ("ui.execution_display", ["ExecutionDisplay"]),
    ]
    
    total = 0
    passed = 0
    failed = 0
    errors = []
    
    for module_name, expected_items in modules_to_test:
        total += 1
        
        try:
            # Import module
            module = importlib.import_module(module_name)
            
            # Check expected items exist
            missing = []
            for item in expected_items:
                if not hasattr(module, item):
                    missing.append(item)
            
            if missing:
                failed += 1
                error_msg = f"{module_name}: Missing items: {', '.join(missing)}"
                errors.append(error_msg)
                print(f"❌ {module_name}")
                print(f"   Missing: {', '.join(missing)}")
            else:
                passed += 1
                print(f"✅ {module_name}")
                for item in expected_items:
                    print(f"   ✓ {item}")
        
        except ImportError as e:
            failed += 1
            error_msg = f"{module_name}: ImportError: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {module_name}")
            print(f"   ImportError: {str(e)}")
        
        except Exception as e:
            failed += 1
            error_msg = f"{module_name}: {type(e).__name__}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {module_name}")
            print(f"   {type(e).__name__}: {str(e)}")
        
        print()
    
    print("="*80)
    print("SUMMARY - FASE 3")
    print("="*80)
    print(f"Total modules:  {total}")
    print(f"Passed:         {passed}")
    print(f"Failed:         {failed}")
    print()
    
    if failed > 0:
        print("ERRORS:")
        for error in errors:
            print(f"  - {error}")
        print()
        print("="*80)
        print(f"❌ FASE 3 FAILED: {failed} modules have import errors")
        print("="*80)
        return False
    else:
        print("="*80)
        print("✅ FASE 3 PASSED: All imports work correctly")
        print("="*80)
        return True


if __name__ == "__main__":
    success = validate_imports()
    sys.exit(0 if success else 1)
