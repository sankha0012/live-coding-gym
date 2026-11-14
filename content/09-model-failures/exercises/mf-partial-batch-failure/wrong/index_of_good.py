def score_batch(rows, score_fn):
    scores, errors = [], []
    for row in rows:
        try:
            scores.append(score_fn(row))
        except Exception as e:
            scores.append(None)
            errors.append({"index": len(scores) - 1 - len(errors), "reason": f"{type(e).__name__}: {e}"})
    return {"scores": scores, "errors": errors}
