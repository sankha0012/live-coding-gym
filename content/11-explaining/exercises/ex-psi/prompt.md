```python
import math


def psi(expected, actual, bins=10, eps=1e-4):
    """Population Stability Index of `actual` against `expected`."""
    if not expected or not actual:
        raise ValueError("both samples must be non-empty")
    ordered = sorted(expected)
    n = len(ordered)
    edges = [ordered[min(n - 1, i * n // bins)] for i in range(1, bins)]
    edges = sorted(set(edges))

    def shares(values):
        counts = [0] * (len(edges) + 1)
        for v in values:
            idx = sum(v > e for e in edges)
            counts[idx] += 1
        total = len(values)
        return [max(c / total, eps) for c in counts]

    e = shares(expected)
    a = shares(actual)
    return sum((ai - ei) * math.log(ai / ei) for ei, ai in zip(e, a))


if __name__ == "__main__":
    base = [i / 100 for i in range(1000)]
    same = [i / 100 + 0.005 for i in range(1000)]
    shifted = [i / 100 + 3 for i in range(1000)]
    print(round(psi(base, same), 4))
    print(round(psi(base, shifted), 4))
    print(round(psi([1, 1, 1, 1, 2], [1, 2, 2, 2, 2], bins=4), 4))
    try:
        psi([], [1])
    except ValueError as err:
        print("error:", err)
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
