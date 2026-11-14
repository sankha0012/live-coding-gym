def clip_probs(probs: list[float]) -> tuple[list[float], int]:
    clipped = [min(max(p, 0.0), 1.0) for p in probs]
    n_out = sum(1 for p in probs if p <= 0.0 or p >= 1.0)
    return clipped, n_out
