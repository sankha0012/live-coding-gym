def percentiles(latencies: list) -> dict:
    ordered = sorted(latencies)
    n = len(ordered)
    out = {}
    for p in (50, 95, 99):
        if n == 0:
            out[f"p{p}"] = None
        else:
            rank = -(-p * n // 100)  # integer ceil(p * n / 100)
            out[f"p{p}"] = ordered[rank - 1]
    return out
