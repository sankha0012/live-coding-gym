import hashlib

def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()):
        raise ValueError("bad")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("bad")
    h = int.from_bytes(hashlib.sha256(f"{experiment}:{user_id}".encode()).digest(), "big")
    bucket = h % 100
    acc = 0
    last = None
    for name, w in weights.items():
        if w == 0:
            continue
        acc += int(w / total * 100)
        last = name
        if bucket < acc:
            return name
    return last
