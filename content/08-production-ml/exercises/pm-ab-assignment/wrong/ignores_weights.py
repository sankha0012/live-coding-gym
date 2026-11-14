import hashlib


def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("bad")
    names = list(weights)
    digest = hashlib.sha256(f"{experiment}:{user_id}".encode()).digest()
    return names[int.from_bytes(digest[:8], "big") % len(names)]
