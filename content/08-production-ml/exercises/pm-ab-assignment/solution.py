import hashlib


def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()):
        raise ValueError("weights must be non-empty and non-negative")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must sum to more than 0")
    digest = hashlib.sha256(f"{experiment}:{user_id}".encode()).digest()
    point = int.from_bytes(digest[:8], "big") / 2**64 * total
    acc = 0.0
    last = None
    for name, w in weights.items():
        if w == 0:
            continue
        acc += w
        last = name
        if point < acc:
            return name
    return last
