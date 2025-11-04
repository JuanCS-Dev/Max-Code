"""
Max-Code CLI UI Benchmarking Suite

Comprehensive performance benchmarks for all UI components.

Targets (from ui/constants.py PERFORMANCE_TARGETS):
- Banner display: <50ms
- Table rendering: <100ms
- Live updates: >10 FPS
- Import time: <45ms
- Memory overhead: <50MB

Usage:
    python benchmarks/ui_benchmarks.py
    python benchmarks/ui_benchmarks.py --verbose
    python benchmarks/ui_benchmarks.py --save results.json
"""

import time
import sys
import json
import argparse
from io import StringIO
from datetime import datetime
from typing import Dict, List, Any
import tracemalloc

# Add parent directory to path
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')


class BenchmarkResult:
    """Single benchmark result."""

    def __init__(self, name: str, duration_ms: float, memory_mb: float = 0.0):
        self.name = name
        self.duration_ms = duration_ms
        self.memory_mb = memory_mb
        self.passed = True
        self.target_ms = None

    def set_target(self, target_ms: float):
        """Set performance target and check if passed."""
        self.target_ms = target_ms
        self.passed = self.duration_ms <= target_ms

    def __repr__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        if self.target_ms:
            return f"{self.name}: {self.duration_ms:.2f}ms (target: {self.target_ms}ms) {status}"
        return f"{self.name}: {self.duration_ms:.2f}ms"


class UIBenchmarkSuite:
    """Comprehensive UI benchmarking suite."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[BenchmarkResult] = []

    def run_all(self) -> Dict[str, Any]:
        """Run all benchmarks."""
        print("=" * 80)
        print("MAX-CODE CLI UI PERFORMANCE BENCHMARKS")
        print("=" * 80)
        print()

        # Import benchmarks
        print("1. Import Performance:")
        self.benchmark_imports()
        print()

        # Banner benchmarks
        print("2. Banner Display:")
        self.benchmark_banner_display()
        print()

        # Table rendering benchmarks
        print("3. Table Rendering:")
        self.benchmark_table_rendering()
        print()

        # Live updates
        print("4. Live Updates:")
        self.benchmark_live_updates()
        print()

        # Memory usage
        print("5. Memory Usage:")
        self.benchmark_memory_usage()
        print()

        # Component creation
        print("6. Component Creation:")
        self.benchmark_component_creation()
        print()

        # Summary
        self.print_summary()

        return self.get_results_dict()

    # ========================================================================
    # IMPORT BENCHMARKS
    # ========================================================================

    def benchmark_imports(self):
        """Benchmark module import times."""
        import importlib
        import sys

        modules = [
            'ui.banner',
            'ui.formatter',
            'ui.progress',
            'ui.agents',
            'ui.menus',
            'ui.tree_of_thoughts',
            'ui.streaming',
            'ui.base',
            'ui.constants',
            'ui.types',
        ]

        total_time = 0

        for module in modules:
            # Remove from cache if present
            if module in sys.modules:
                del sys.modules[module]

            start = time.perf_counter()
            importlib.import_module(module)
            elapsed = (time.perf_counter() - start) * 1000

            total_time += elapsed

            result = BenchmarkResult(f"Import {module}", elapsed)
            self.results.append(result)

            if self.verbose:
                print(f"  {result}")

        # Total import time
        result = BenchmarkResult("Total import time", total_time)
        result.set_target(45)  # Target: <45ms
        self.results.append(result)
        print(f"  {result}")

    # ========================================================================
    # BANNER BENCHMARKS
    # ========================================================================

    def benchmark_banner_display(self):
        """Benchmark banner display performance."""
        from ui.banner import MaxCodeBanner
        from rich.console import Console

        # Capture output
        console = Console(file=StringIO(), force_terminal=True)
        banner = MaxCodeBanner(console=console)

        # Warm-up
        banner.show(version="3.0", style='default')

        # Benchmark
        start = time.perf_counter()
        banner.show(version="3.0", style='default')
        elapsed = (time.perf_counter() - start) * 1000

        result = BenchmarkResult("Banner display (PyFiglet)", elapsed)
        result.set_target(50)  # Target: <50ms
        self.results.append(result)
        print(f"  {result}")

        # Test vCLI-Go style
        from ui.banner_vcli_style import show_banner

        start = time.perf_counter()
        show_banner(version="3.0", console=console)
        elapsed = (time.perf_counter() - start) * 1000

        result = BenchmarkResult("Banner display (vCLI-Go)", elapsed)
        result.set_target(50)  # Target: <50ms
        self.results.append(result)
        print(f"  {result}")

    # ========================================================================
    # TABLE RENDERING BENCHMARKS
    # ========================================================================

    def benchmark_table_rendering(self):
        """Benchmark table rendering with various row counts."""
        from ui.agents import AgentDisplay, Agent, AgentStatus
        from rich.console import Console

        console = Console(file=StringIO(), force_terminal=True)
        display = AgentDisplay(console=console)

        row_counts = [10, 50, 100, 500]

        for count in row_counts:
            # Generate test data
            agents = [
                Agent(
                    f"Agent{i}",
                    f"Role{i}",
                    AgentStatus.ACTIVE,
                    f"Task {i}",
                    50.0,
                    10.0,
                    20.0,
                    100.0
                )
                for i in range(count)
            ]

            # Benchmark
            start = time.perf_counter()
            display.show_dashboard(agents, title=f"Test {count} rows")
            elapsed = (time.perf_counter() - start) * 1000

            result = BenchmarkResult(f"Table render ({count} rows)", elapsed)
            if count == 100:
                result.set_target(100)  # Target: <100ms for 100 rows
            self.results.append(result)
            print(f"  {result}")

    # ========================================================================
    # LIVE UPDATE BENCHMARKS
    # ========================================================================

    def benchmark_live_updates(self):
        """Benchmark live update performance (FPS)."""
        from ui.streaming import ProgressStream, StreamUpdate
        from rich.console import Console

        console = Console(file=StringIO(), force_terminal=True)
        stream = ProgressStream(console=console)

        # Generate updates
        def update_generator():
            for i in range(100):
                yield StreamUpdate("test", "Testing", i, 100, "active")

        # Benchmark
        start = time.perf_counter()
        stream.stream_progress(update_generator(), title="FPS Test")
        elapsed = (time.perf_counter() - start) * 1000

        fps = 100 / (elapsed / 1000)

        result = BenchmarkResult("Live updates (100 frames)", elapsed)
        self.results.append(result)
        print(f"  {result}")
        print(f"  FPS: {fps:.1f} (target: >10 FPS) {'✓ PASS' if fps >= 10 else '✗ FAIL'}")

    # ========================================================================
    # MEMORY BENCHMARKS
    # ========================================================================

    def benchmark_memory_usage(self):
        """Benchmark memory usage of UI components."""
        import gc

        # Force garbage collection
        gc.collect()

        # Start memory tracking
        tracemalloc.start()

        # Import all UI modules
        from ui import (
            get_banner, get_formatter, get_progress,
            get_agent_display, get_thought_tree, get_streaming_display
        )

        # Create instances
        banner = get_banner()
        formatter = get_formatter()
        progress = get_progress()
        agents = get_agent_display()
        tot = get_thought_tree()
        stream = get_streaming_display()

        # Get memory snapshot
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory_mb = peak / (1024 * 1024)

        result = BenchmarkResult("Memory overhead", 0, memory_mb)
        self.results.append(result)
        print(f"  Memory usage: {memory_mb:.2f} MB (target: <50 MB) {'✓ PASS' if memory_mb < 50 else '✗ FAIL'}")

    # ========================================================================
    # COMPONENT CREATION BENCHMARKS
    # ========================================================================

    def benchmark_component_creation(self):
        """Benchmark component instantiation time."""
        components = [
            ('MaxCodeBanner', 'from ui.banner import MaxCodeBanner', 'MaxCodeBanner()'),
            ('MaxCodeFormatter', 'from ui.formatter import MaxCodeFormatter', 'MaxCodeFormatter()'),
            ('MaxCodeProgress', 'from ui.progress import MaxCodeProgress', 'MaxCodeProgress()'),
            ('AgentDisplay', 'from ui.agents import AgentDisplay', 'AgentDisplay()'),
            ('SelectionMenu', 'from ui.menus import SelectionMenu', 'SelectionMenu()'),
            ('ThoughtTree', 'from ui.tree_of_thoughts import ThoughtTree', 'ThoughtTree()'),
            ('StreamingDisplay', 'from ui.streaming import StreamingDisplay', 'StreamingDisplay()'),
        ]

        for name, import_stmt, create_stmt in components:
            exec(import_stmt)

            start = time.perf_counter()
            for _ in range(100):
                eval(create_stmt)
            elapsed = (time.perf_counter() - start) * 1000 / 100  # Average per creation

            result = BenchmarkResult(f"Create {name}", elapsed)
            self.results.append(result)

            if self.verbose:
                print(f"  {result}")

        print(f"  ✓ All components benchmarked")

    # ========================================================================
    # RESULTS
    # ========================================================================

    def print_summary(self):
        """Print benchmark summary."""
        print("=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)
        print()

        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"Total benchmarks: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print()

        if failed > 0:
            print("Failed benchmarks:")
            for result in self.results:
                if not result.passed:
                    print(f"  ✗ {result.name}: {result.duration_ms:.2f}ms (target: {result.target_ms}ms)")
            print()

        print("Status: " + ("✅ ALL PASS" if failed == 0 else "❌ SOME FAILURES"))
        print()

    def get_results_dict(self) -> Dict[str, Any]:
        """Get results as dictionary."""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_benchmarks': len(self.results),
            'passed': sum(1 for r in self.results if r.passed),
            'failed': sum(1 for r in self.results if not r.passed),
            'results': [
                {
                    'name': r.name,
                    'duration_ms': r.duration_ms,
                    'memory_mb': r.memory_mb,
                    'target_ms': r.target_ms,
                    'passed': r.passed,
                }
                for r in self.results
            ]
        }


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(description='Max-Code CLI UI Benchmarks')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--save', '-s', type=str, help='Save results to JSON file')
    args = parser.parse_args()

    suite = UIBenchmarkSuite(verbose=args.verbose)
    results = suite.run_all()

    if args.save:
        with open(args.save, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.save}")


if __name__ == '__main__':
    main()
