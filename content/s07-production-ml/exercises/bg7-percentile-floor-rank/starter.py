def percentiles(latencies):
    s = sorted(latencies)
    n = len(s)
    if n == 0:
        return {"p50": None, "p95": None, "p99": None}
    return {f"p{p}": s[min(int(p / 100 * n), n - 1)] for p in (50, 95, 99)}
