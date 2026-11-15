import math

def predict_batch(rows, model, fallback):
    results, n_fallback = [], 0
    for row in rows:
        try:
            pred = model(row)
            ok = pred is not None and math.isfinite(pred)
        except ValueError:
            ok = False
        if not ok:
            pred, n_fallback = fallback, n_fallback + 1
        results.append({"id": row["id"], "pred": pred, "status": "ok" if ok else "fallback"})
    rate = n_fallback / len(rows) if rows else 0.0
    return results, rate
