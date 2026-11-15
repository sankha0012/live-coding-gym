def score_batch(rows, score_fn):
    scores, errors = [], []
    for i, row in enumerate(rows):
        try:
            scores.append(score_fn(row))
        except Exception as e:
            errors.append({"index": i, "reason": f"{type(e).__name__}: {e}"})
    return {"scores": scores, "errors": errors}
