def predict_with_fallback(model, x, fallback, deadline_s, clock):
    start = clock()
    try:
        result = model(x)
    except Exception:
        return fallback, "error"
    if not result or clock() - start > deadline_s:
        return fallback, "timeout"
    return result, "model"
