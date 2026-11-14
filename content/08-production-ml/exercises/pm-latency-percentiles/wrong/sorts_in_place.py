def percentiles(latencies):
    latencies.sort()
    n = len(latencies)
    if n == 0:
        return {"p50": None, "p95": None, "p99": None}
    return {f"p{p}": latencies[-(-p * n // 100) - 1] for p in (50, 95, 99)}
