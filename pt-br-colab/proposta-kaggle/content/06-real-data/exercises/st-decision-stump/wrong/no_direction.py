def fit_stump(xs, ys):
    if len(xs) != len(ys):
        raise ValueError
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None]
    if not pairs:
        raise ValueError
    best = (-1, 0)
    for t in sorted({x for x, _ in pairs}):
        correct = sum((1 if x > t else 0) == y for x, y in pairs)
        if correct > best[0]:
            best = (correct, t)
    return {"threshold": best[1], "sign": 1, "fallback": 0}


def predict(model, x):
    if x is None:
        return model["fallback"]
    return 1 if x > model["threshold"] else 0
