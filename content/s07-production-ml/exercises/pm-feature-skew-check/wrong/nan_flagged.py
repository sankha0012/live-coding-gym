def find_skew(online: dict, offline: dict, tolerance: float = 1e-6) -> dict:
    out = {}
    for name in sorted(set(online) | set(offline)):
        if name not in online:
            out[name] = "missing_online"
        elif name not in offline:
            out[name] = "missing_offline"
        else:
            a, b = online[name], offline[name]
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a is not None and b is not None:
                if not abs(a - b) <= tolerance:
                    out[name] = "diff"
            elif a != b:
                out[name] = "diff"
    return out
