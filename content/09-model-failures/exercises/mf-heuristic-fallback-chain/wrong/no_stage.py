def predict_with_fallback(features, model, rule, default):
    for fn in (model, rule):
        try:
            value = fn(features)
        except Exception:
            continue
        if value is not None:
            return value, "model"
    return default, "default"
