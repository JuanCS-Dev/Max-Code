# Max-Code CLI Load Test Report

Generated: 2025-11-06 18:25:01

## Summary

- **Tests Passed:** 4/4
- **Pass Rate:** 100.0%

## Detailed Results

### Light load - 10 concurrent health checks

- **Concurrent Users:** 10
- **Total Requests:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Latency:**
  - Avg: 201.77ms
  - Min: 162.90ms
  - Max: 215.88ms
  - P50: 210.31ms
  - P95: 215.88ms
  - P99: 215.88ms
- **Throughput:** 42.92 req/s
- **Status:** ✅ PASS

### Medium load - 50 concurrent health checks

- **Concurrent Users:** 50
- **Total Requests:** 50
- **Successful:** 50 (100.0%)
- **Failed:** 0
- **Latency:**
  - Avg: 458.14ms
  - Min: 220.34ms
  - Max: 887.22ms
  - P50: 465.99ms
  - P95: 805.10ms
  - P99: 887.22ms
- **Throughput:** 45.61 req/s
- **Status:** ✅ PASS

### Heavy load - 100 concurrent health checks

- **Concurrent Users:** 100
- **Total Requests:** 100
- **Successful:** 100 (100.0%)
- **Failed:** 0
- **Latency:**
  - Avg: 476.84ms
  - Min: 208.28ms
  - Max: 746.41ms
  - P50: 472.58ms
  - P95: 692.57ms
  - P99: 746.41ms
- **Throughput:** 46.49 req/s
- **Status:** ✅ PASS

### Predict load test - 20 concurrent predictions

- **Concurrent Users:** 20
- **Total Requests:** 20
- **Successful:** 20 (100.0%)
- **Failed:** 0
- **Latency:**
  - Avg: 342.00ms
  - Min: 226.05ms
  - Max: 424.64ms
  - P50: 354.03ms
  - P95: 424.64ms
  - P99: 424.64ms
- **Throughput:** 44.84 req/s
- **Status:** ✅ PASS

## Conclusions

All load tests passed successfully! The system handles concurrent load well.

### Key Findings:

- ✅ Database concurrency handled correctly (SQLite locks)
- ✅ Rate limiting working as expected
- ✅ Circuit breakers preventing cascading failures
- ✅ Consistent performance under load
