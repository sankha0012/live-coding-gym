import math


def _corr(xs, ys):
    n = len(xs)
    if n == 0:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return 0.0
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy)


def find_leaky_features(features: dict[str, list[float]], labels: list[float],
                        threshold: float = 0.95) -> list[str]:
    scored = []
    for name, values in features.items():
        if len(values) != len(labels):
            raise ValueError(f"length mismatch for {name}")
        c = abs(_corr(values, labels))
        if c > threshold:
            scored.append((-c, name))
    return [name for _, name in sorted(scored)]
