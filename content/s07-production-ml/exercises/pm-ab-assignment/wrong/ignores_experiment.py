import hashlib


def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()):
        raise ValueError("bad")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("bad")
    digest = hashlib.sha256(user_id.encode()).digest()
    point = int.from_bytes(digest[:8], "big") / 2**64 * total
    acc = 0.0
    for name, w in weights.items():
        acc += w
        if point < acc:
            return name
    return name
