Trap: a prediction of 0.0 is valid, so don't write 'if not pred'. Check 'pred is None or not math.isfinite(pred)' (isfinite is False for NaN and infinity).
