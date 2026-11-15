def predict_with_fallback(model, x, fallback, deadline_s, clock):
    try:
        result = model(x)
    except Exception:
        return fallback, "error"
    start = clock()
    if clock() - start > deadline_s:
        return fallback, "timeout"
    return result, "model"
