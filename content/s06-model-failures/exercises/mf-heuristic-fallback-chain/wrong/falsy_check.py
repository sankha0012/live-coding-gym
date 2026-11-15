def predict_with_fallback(features, model, rule, default):
    for stage, fn in (("model", model), ("rule", rule)):
        try:
            value = fn(features)
        except Exception:
            continue
        if value:
            return value, stage
    return default, "default"
