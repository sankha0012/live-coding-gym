import math

def predict_batch(rows, model, fallback):
    good, bad = [], []
    for row in rows:
        try:
            pred = model(row)
            ok = pred is not None and math.isfinite(pred)
        except Exception:
            ok = False
        if ok:
            good.append({"id": row["id"], "pred": pred, "status": "ok"})
        else:
            bad.append({"id": row["id"], "pred": fallback, "status": "fallback"})
    rate = len(bad) / len(rows) if rows else 0.0
    return good + bad, rate
