def compare_shadow(live, shadow, inputs, tolerance=0.1, top=3) -> dict:
    cases = []
    total = 0
    for x in inputs:
        total += 1
        a, b = live(x), shadow(x)
        if abs(a - b) > tolerance:
            cases.append({"input": x, "live": a, "shadow": b, "diff": abs(a - b)})
    cases.sort(key=lambda c: -c["diff"])
    return {"total": total, "shadow_errors": 0, "disagreements": len(cases),
            "rate": len(cases) / total if total else 0.0, "worst": cases[:top]}
