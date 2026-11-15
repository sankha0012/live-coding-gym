def predict_with_fallback(features, model, rule, default):
    for stage, fn in (("model", model), ("rule", rule)):
        try:
            v = fn(features)
        except (RuntimeError, ValueError):
            continue
        if v is not None:
            return v, stage
    return default, "default"
