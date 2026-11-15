def score_batch(rows, score_fn):
    scores = [score_fn(row) for row in rows]
    return {"scores": scores, "errors": []}
