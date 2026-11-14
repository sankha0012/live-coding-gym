def predict_with_fallback(model, x, fallback, deadline_s, clock):
    try:
        return model(x), "model"
    except Exception:
        return fallback, "error"
