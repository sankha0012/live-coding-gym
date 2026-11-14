def check_health(checks: list) -> dict:
    for name, fn in checks:
        try:
            result = fn()
        except Exception as exc:
            return {"status": "down", "reasons": [f"{name}: down (raised {type(exc).__name__})"]}
        if result not in ("ok", "degraded", "down"):
            return {"status": "down", "reasons": [f"{name}: down (invalid result)"]}
        if result != "ok":
            return {"status": result, "reasons": [f"{name}: {result}"]}
    return {"status": "ok", "reasons": []}
