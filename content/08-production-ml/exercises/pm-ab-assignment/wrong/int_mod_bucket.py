import hashlib

def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()):
        raise ValueError("bad")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("bad")
    h = int.from_bytes(hashlib.sha256(f"{experiment}:{user_id}".encode()).digest(), "big")
    point = h % int(total)
    acc = 0
    for name, w in weights.items():
        acc += w
        if w > 0 and point < acc:
            return name
    return [n for n, w in weights.items() if w > 0][-1]
