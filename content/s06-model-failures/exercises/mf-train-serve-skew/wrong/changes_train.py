import math


def train_features(rows, stats):
    out = []
    for row in rows:
        z = (math.log(row["amount"]) - stats["mean"]) / stats["std"]
        out.append({"amount_z": z, "category": row["category"]})
    return out


def serve_features(row, stats):
    return train_features([row], stats)[0]
