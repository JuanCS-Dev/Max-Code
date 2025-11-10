# Max-Code CLI Performance Profiling Report

Generated: 2025-11-06 18:23:18

## Summary

- **Targets Met:** 5/5
- **Pass Rate:** 100.0%

## Detailed Results

### python cli/main.py --help

- **Description:** Help command (cold start)
- **Latency:** 112.94ms (target: 150ms)
- **Status:** ✅ PASS

### python cli/main.py --version

- **Description:** Version command
- **Latency:** 107.78ms (target: 150ms)
- **Status:** ✅ PASS

### python cli/main.py health

- **Description:** Health check (fast fail)
- **Latency:** 107.40ms (target: 500ms)
- **Status:** ✅ PASS

### python cli/main.py predict --mode fast

- **Description:** Fast predict (first token)
- **Latency:** 110.07ms (target: 1000ms)
- **Status:** ✅ PASS

### python cli/main.py config

- **Description:** Config command
- **Latency:** 109.61ms (target: 150ms)
- **Status:** ✅ PASS

## Performance Recommendations

All commands meet performance targets! 🎉
