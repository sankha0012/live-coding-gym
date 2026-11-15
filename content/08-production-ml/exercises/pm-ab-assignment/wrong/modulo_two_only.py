import hashlib

def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()):
        raise ValueError("bad")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("bad")
    h = int.from_bytes(hashlib.md5(f"{experiment}:{user_id}".encode()).digest(), "big")
    names = [n for n, w in weights.items() if w > 0]
    return names[h % len(names)]
