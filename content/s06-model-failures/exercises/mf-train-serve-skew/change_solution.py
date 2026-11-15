import math


def train_features(rows: list[dict], stats: dict) -> list[dict]:
    """Reference implementation used at training time. Do not change it.

    amount: a missing amount (None) counts as 0.0. Then log1p, then
    standardise with stats["mean"] and stats["std"].
    category: strip spaces and lowercase. A missing category is "unknown".
    """
    out = []
    for row in rows:
        amount = row.get("amount")
        if amount is None:
            amount = 0.0
        z = (math.log1p(amount) - stats["mean"]) / stats["std"]
        category = (row.get("category") or "unknown").strip().lower()
        out.append({"amount_z": z, "category": category})
    return out


def serve_features(row: dict, stats: dict, clip: float | None = None) -> dict:
    """Online version for one row. Must return exactly what train_features
    returns for the same row and stats."""
    out = train_features([row], stats)[0]
    if clip is not None:
        out["amount_z"] = max(-clip, min(clip, out["amount_z"]))
    return out
