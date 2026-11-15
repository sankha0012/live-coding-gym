def predict_with_fallback(model, x, fallback, deadline_s, clock):
    start = clock()
    result = model(x)
    if clock() - start > deadline_s:
        return fallback, "timeout"
    return result, "model"
