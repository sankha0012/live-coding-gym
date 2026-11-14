def clip_probs(probs: list[float]) -> tuple[list[float], int]:
    good = [p for p in probs if 0.0 <= p <= 1.0]
    return good, len(probs) - len(good)
