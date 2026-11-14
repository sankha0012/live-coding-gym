def _null(v):
    return v is None or (isinstance(v, float) and v != v)


def find_skew(online: dict, offline: dict, tolerance: float = 1e-6) -> dict:
    out = {}
    for name in sorted(offline):
        if name not in online:
            out[name] = "missing_online"
            continue
        a, b = online[name], offline[name]
        if _null(a) or _null(b):
            if not (_null(a) and _null(b)):
                out[name] = "diff"
        elif isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
            if abs(a - b) > tolerance:
                out[name] = "diff"
        elif a != b:
            out[name] = "diff"
    return out
