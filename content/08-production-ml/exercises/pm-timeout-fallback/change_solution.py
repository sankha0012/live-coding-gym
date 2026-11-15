def predict_with_fallback(model, x, fallback, deadline_s, clock, keep_late=False):
    start = clock()
    try:
        result = model(x)
    except Exception:
        return fallback, "error"
    if clock() - start > deadline_s:
        if keep_late:
            return result, "late"
        return fallback, "timeout"
    return result, "model"
