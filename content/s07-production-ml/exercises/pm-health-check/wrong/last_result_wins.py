def check_health(checks: list) -> dict:
    status = "ok"
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
        status = result
    return {"status": status, "reasons": reasons}
