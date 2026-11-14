```python
import hashlib


def bucket(user_id, experiment, buckets=10_000):
    """Map a user to a stable bucket in [0, buckets) for one experiment."""
    key = f"{experiment}:{user_id}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    return int.from_bytes(digest[:8], "big") % buckets


def assign(user_id, experiment, variants, buckets=10_000):
    """Pick a variant. `variants` is a list of (name, weight) with weights summing to 1."""
    point = bucket(user_id, experiment, buckets)
    upper = 0.0
    for name, weight in variants:
        upper += weight * buckets
        if point < upper:
            return name
    return variants[-1][0]


if __name__ == "__main__":
    variants = [("control", 0.5), ("treatment", 0.5)]
    print(assign("u1", "checkout-v2", variants))
    print(assign("u1", "checkout-v2", variants))
    counts = {"control": 0, "treatment": 0}
    for i in range(20000):
        counts[assign(f"user{i}", "checkout-v2", variants)] += 1
    print(counts)
    shift = 0
    for i in range(2000):
        a = assign(f"user{i}", "exp-a", variants)
        b = assign(f"user{i}", "exp-b", variants)
        shift += a != b
    print("differ across experiments:", shift)
    three = [("a", 0.3), ("b", 0.3), ("c", 0.4)]
    print(assign("u9", "x", three))
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
