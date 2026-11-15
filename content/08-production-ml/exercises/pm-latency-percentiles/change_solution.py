def percentiles(latencies: list, ps=(50, 95, 99)) -> dict:
    ordered = sorted(latencies)
    n = len(ordered)
    out = {}
    for p in ps:
        if n == 0:
            out[f"p{p}"] = None
        else:
            rank = -(-p * n // 100)  # integer ceil(p * n / 100)
            out[f"p{p}"] = ordered[rank - 1]
    return out
