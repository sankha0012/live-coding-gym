import math


def train_features(rows, stats):
    out = []
    for row in rows:
        amount = row.get("amount")
        if amount is None:
            amount = 0.0
        z = (math.log1p(amount) - stats["mean"]) / stats["std"]
        category = (row.get("category") or "unknown").strip().lower()
        out.append({"amount_z": z, "category": category})
    return out


def serve_features(row, stats):
    amount = row.get("amount") or 0.0
    z = (math.log1p(amount) - stats["mean"]) / stats["std"]
    return {"amount_z": z, "category": row["category"]}
