import math

def predict_batch(rows, model, fallback):
    results, n_ok = [], 0
    for row in rows:
        try:
            pred = model(row)
            ok = pred is not None and math.isfinite(pred)
        except Exception:
            ok = False
        if not ok:
            pred = fallback
        else:
            n_ok += 1
        results.append({"id": row["id"], "pred": pred, "status": "ok" if ok else "fallback"})
    return results, (n_ok / len(rows) if rows else 0.0)
