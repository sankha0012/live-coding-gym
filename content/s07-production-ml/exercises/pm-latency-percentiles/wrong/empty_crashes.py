def percentiles(latencies):
    s = sorted(latencies)
    n = len(s)
    return {f"p{p}": s[-(-p * n // 100) - 1] for p in (50, 95, 99)}
