import math


def find_leaky_features(features, labels, threshold=0.95):
    scored = []
    for name, values in features.items():
        if len(values) != len(labels):
            raise ValueError(name)
        n = len(values)
        mx, my = sum(values) / n, sum(labels) / n
        sxy = sum((x - mx) * (y - my) for x, y in zip(values, labels))
        sxx = sum((x - mx) ** 2 for x in values)
        syy = sum((y - my) ** 2 for y in labels)
        c = abs(sxy / math.sqrt(sxx * syy))
        if c > threshold:
            scored.append((-c, name))
    return [name for _, name in sorted(scored)]
