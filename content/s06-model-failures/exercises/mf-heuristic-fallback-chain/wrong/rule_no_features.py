def predict_with_fallback(features, model, rule, default):
    try:
        v = model(features)
        if v is not None: return v, "model"
    except Exception: pass
    try:
        v = rule()
        if v is not None: return v, "rule"
    except Exception: pass
    return default, "default"
