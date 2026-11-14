def fit_stump(xs, ys):
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None]
    if not pairs:
        raise ValueError("no usable x values")
    fallback = 1 if 2 * sum(ys) > len(ys) else 0
    values = sorted({x for x, _ in pairs})
    candidates = [values[0] - 1] + values  # the first one lets the stump predict one class everywhere
    best = (-1, candidates[0], 1)
    for t in candidates:
        for sign in (1, -1):
            correct = sum((1 if sign * (x - t) > 0 else 0) == y for x, y in pairs)
            if correct > best[0]:
                best = (correct, t, sign)
    return {"threshold": best[1], "sign": best[2], "fallback": fallback}


def predict(model, x):
    if x is None:
        return model["fallback"]
    return 1 if model["sign"] * (x - model["threshold"]) > 0 else 0
