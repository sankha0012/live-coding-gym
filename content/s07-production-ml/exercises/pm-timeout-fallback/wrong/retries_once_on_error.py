def predict_with_fallback(model, x, fallback, deadline_s, clock):
    start = clock()
    for attempt in range(2):
        try:
            result = model(x)
            break
        except Exception:
            if attempt == 1:
                return fallback, "error"
    if clock() - start > deadline_s:
        return fallback, "timeout"
    return result, "model"
