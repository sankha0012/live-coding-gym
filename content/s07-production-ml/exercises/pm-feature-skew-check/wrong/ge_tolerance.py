def _is_null(v):
    return v is None or (isinstance(v, float) and v != v)


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def find_skew(online: dict, offline: dict, tolerance: float = 1e-6) -> dict:
    out = {}
    for name in sorted(set(online) | set(offline)):
        if name not in online:
            out[name] = "missing_online"
            continue
        if name not in offline:
            out[name] = "missing_offline"
            continue
        a, b = online[name], offline[name]
        if _is_null(a) or _is_null(b):
            if not (_is_null(a) and _is_null(b)):
                out[name] = "diff"
        elif _is_num(a) and _is_num(b):
            if abs(a - b) >= tolerance:
                out[name] = "diff"
        elif a != b:
            out[name] = "diff"
    return out
