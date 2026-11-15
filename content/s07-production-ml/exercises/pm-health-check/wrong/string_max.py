def check_health(checks: list) -> dict:
    rank = {"ok": 0, "degraded": 1, "down": 2}
    worst = "ok"
    reasons = []
    for name, fn in checks:
        try:
            result = fn()
        except Exception as exc:
            result = "down"
            reasons.append(f"{name}: down (raised {type(exc).__name__})")
        else:
            if result not in ("ok", "degraded", "down"):
                result = "down"
                reasons.append(f"{name}: down (invalid result)")
            elif result != "ok":
                reasons.append(f"{name}: {result}")
        if result > worst:
            worst = result
    return {"status": worst, "reasons": reasons}
