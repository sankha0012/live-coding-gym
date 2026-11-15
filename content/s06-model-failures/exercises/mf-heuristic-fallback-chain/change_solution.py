def predict_with_fallback(features, model, rule, default, valid=None):
    for stage, fn in (("model", model), ("rule", rule)):
        try:
            value = fn(features)
        except Exception:
            continue
        if value is None:
            continue
        if valid is not None and not valid(value):
            continue
        return value, stage
    return default, "default"
