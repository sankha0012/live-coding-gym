def compare_shadow(live, shadow, inputs, tolerance=0.1, top=3) -> dict:
    total = 0
    errors = 0
    cases = []
    for x in inputs:
        total += 1
        a = live(x)
        try:
            b = shadow(x)
        except Exception:
            errors += 1
            continue
        diff = a - b
        if abs(diff) > tolerance:
            cases.append({"input": x, "live": a, "shadow": b, "diff": diff})
    compared = total - errors
    cases.sort(key=lambda c: -abs(c["diff"]))
    return {
        "total": total,
        "shadow_errors": errors,
        "disagreements": len(cases),
        "rate": len(cases) / compared if compared else 0.0,
        "worst": cases[:top],
    }
