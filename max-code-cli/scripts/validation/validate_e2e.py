#!/usr/bin/env python3
"""
Validação end-to-end com casos reais - CONFIANÇA ZERO
"""
import asyncio
import sys
import time
from pathlib import Path

# Add to path
sys.path.insert(0, "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli")


class E2EValidator:
    """Validador end-to-end"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    async def test_case_1_task_models_basic(self):
        """Caso 1: Task models básicos"""
        print("\n" + "="*80)
        print("CASO 1: Task Models Básicos")
        print("="*80)
        
        try:
            from core.task_models import Task, TaskType, TaskStatus, EnhancedExecutionPlan
            
            start = time.time()
            
            # Criar task
            task = Task(
                id="test1",
                description="Test task",
                type=TaskType.THINK
            )
            
            # Validar
            assert task.id == "test1", "ID incorrect"
            assert task.status == TaskStatus.PENDING, "Initial status incorrect"
            assert task.type == TaskType.THINK, "Type incorrect"
            
            # Criar plan
            plan = EnhancedExecutionPlan(
                goal="Test goal",
                tasks=[task]
            )
            
            assert len(plan.tasks) == 1, "Task count incorrect"
            assert plan.goal == "Test goal", "Goal incorrect"
            
            elapsed = time.time() - start
            
            print(f"✅ Task models working")
            print(f"   Task created: {task.id}")
            print(f"   Plan created: {len(plan.tasks)} tasks")
            print(f"   Time: {elapsed:.3f}s")
            
            self.passed += 1
            return True
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
            self.failed += 1
            return False
    
    async def test_case_2_task_graph(self):
        """Caso 2: Task graph com dependências"""
        print("\n" + "="*80)
        print("CASO 2: Task Graph com Dependências")
        print("="*80)
        
        try:
            from core.task_models import Task, TaskType
            from core.task_graph import TaskGraph
            
            start = time.time()
            
            # Criar tasks com dependências
            task1 = Task(id="t1", description="Task 1", type=TaskType.THINK)
            task2 = Task(id="t2", description="Task 2", type=TaskType.THINK, depends_on=["t1"])
            task3 = Task(id="t3", description="Task 3", type=TaskType.THINK, depends_on=["t1"])
            task4 = Task(id="t4", description="Task 4", type=TaskType.THINK, depends_on=["t2", "t3"])
            
            # Criar grafo
            graph = TaskGraph([task1, task2, task3, task4])
            
            # Validar DAG
            is_valid, errors = graph.is_valid_dag()
            assert is_valid, f"Invalid DAG: {errors}"
            
            # Parallel batches (API existente)
            batches = graph.get_parallel_batches()
            assert len(batches) > 0, "No batches generated"
            
            elapsed = time.time() - start
            
            print(f"✅ Task graph working")
            print(f"   Tasks: {len(graph.tasks)}")
            print(f"   Valid DAG: {is_valid}")
            print(f"   Batches: {len(batches)}")
            print(f"   Time: {elapsed:.3f}s")
            
            self.passed += 1
            return True
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
            self.failed += 1
            return False
    
    async def test_case_3_tool_metadata(self):
        """Caso 3: Tool metadata e registry"""
        print("\n" + "="*80)
        print("CASO 3: Tool Metadata e Registry")
        print("="*80)
        
        try:
            from core.tools.enhanced_registry import get_enhanced_registry
            from core.tools.tool_metadata import ToolCategory
            
            start = time.time()
            
            # Get singleton registry (já inicializado)
            registry = get_enhanced_registry()
            
            # Validar
            assert len(registry.list_tools()) > 0, "No tools registered"
            
            # Buscar tool por nome
            file_reader = registry.get_tool("file_reader")
            assert file_reader is not None, "file_reader not found"
            
            # Listar todas tools
            all_tools = registry.list_tools()
            
            elapsed = time.time() - start
            
            print(f"✅ Tool registry working")
            print(f"   Tools registered: {len(all_tools)}")
            print(f"   file_reader found: {file_reader is not None}")
            print(f"   Time: {elapsed:.3f}s")
            
            self.passed += 1
            return True
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
            self.failed += 1
            return False
    
    async def test_case_4_tool_selector(self):
        """Caso 4: Tool selector"""
        print("\n" + "="*80)
        print("CASO 4: Tool Selector - Básico")
        print("="*80)
        
        try:
            from core.tools.tool_selector import ToolSelector
            from core.tools.enhanced_registry import get_enhanced_registry
            
            start = time.time()
            
            # Criar selector (sem LLM)
            selector = ToolSelector(use_llm_selection=False)
            
            # Testar get_all_tools
            all_tools = selector.get_all_tools()
            assert len(all_tools) > 0, "No tools available"
            
            # Validar que registry tem tools
            registry = get_enhanced_registry()
            registry_tools = registry.list_tools()
            assert len(registry_tools) > 0, "Registry empty"
            
            elapsed = time.time() - start
            
            print(f"✅ Tool selector working")
            print(f"   Total tools in selector: {len(all_tools)}")
            print(f"   Tools in registry: {len(registry_tools)}")
            print(f"   Time: {elapsed:.3f}s")
            
            self.passed += 1
            return True
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
            self.failed += 1
            return False
    
    async def test_case_5_execution_engine_basic(self):
        """Caso 5: Execution engine básico"""
        print("\n" + "="*80)
        print("CASO 5: Execution Engine Básico")
        print("="*80)
        
        try:
            from core.execution_engine import ExecutionEngine
            from core.task_models import Task, EnhancedExecutionPlan, TaskType
            
            start = time.time()
            
            # Criar plano simples
            task1 = Task(id="e1", description="Think step 1", type=TaskType.THINK)
            task2 = Task(id="e2", description="Think step 2", type=TaskType.THINK, depends_on=["e1"])
            
            plan = EnhancedExecutionPlan(
                goal="Simple execution test",
                tasks=[task1, task2]
            )
            
            # Executar (sem display)
            engine = ExecutionEngine(enable_parallel=False)
            result = await engine.execute_plan(plan, display=None)
            
            # Validar
            assert result is not None, "No result returned"
            assert "success" in result, "No success field"
            assert "total_tasks" in result, "No total_tasks field"
            
            elapsed = time.time() - start
            
            print(f"✅ Execution engine working")
            print(f"   Total tasks: {result['total_tasks']}")
            print(f"   Success: {result['success']}")
            print(f"   Time: {elapsed:.3f}s")
            
            self.passed += 1
            return True
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
            self.failed += 1
            return False
    
    async def run_all(self):
        """Executar todos casos de teste"""
        print("="*80)
        print("FASE 5: VALIDAÇÃO END-TO-END - CASOS REAIS")
        print("="*80)
        
        test_cases = [
            self.test_case_1_task_models_basic,
            self.test_case_2_task_graph,
            self.test_case_3_tool_metadata,
            self.test_case_4_tool_selector,
            self.test_case_5_execution_engine_basic,
        ]
        
        for test_case in test_cases:
            await test_case()
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY - FASE 5")
        print("="*80)
        print(f"Total cases:  {self.passed + self.failed}")
        print(f"Passed:       {self.passed}")
        print(f"Failed:       {self.failed}")
        print()
        
        if self.failed > 0:
            print("="*80)
            print(f"❌ FASE 5 FAILED: {self.failed} test cases failed")
            print("="*80)
            return False
        else:
            print("="*80)
            print("✅ FASE 5 PASSED: All end-to-end tests passed")
            print("="*80)
            return True


async def main():
    validator = E2EValidator()
    success = await validator.run_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
