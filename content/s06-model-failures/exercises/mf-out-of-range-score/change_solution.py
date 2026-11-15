def clip_probs(probs: list[float], hi: float = 1.0) -> tuple[list[float], int]:
    clipped = [min(max(p, 0.0), float(hi)) for p in probs]
    n_out = sum(1 for p in probs if p < 0.0 or p > hi)
    return clipped, n_out
