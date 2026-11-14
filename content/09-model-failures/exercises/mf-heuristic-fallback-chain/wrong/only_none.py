def predict_with_fallback(features, model, rule, default):
    for stage, fn in (("model", model), ("rule", rule)):
        value = fn(features)
        if value is not None:
            return value, stage
    return default, "default"
