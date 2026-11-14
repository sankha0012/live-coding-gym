import random


def assign(user_id: str, experiment: str, weights: dict) -> str:
    if not weights or any(w < 0 for w in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("bad")
    return random.choices(list(weights), weights=list(weights.values()))[0]
