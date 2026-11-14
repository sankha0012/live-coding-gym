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
    z = (math.log(row["amount"]) - stats["mean"]) / stats["std"]
    category = (row.get("category") or "unknown").strip().lower()
    return {"amount_z": z, "category": category}
