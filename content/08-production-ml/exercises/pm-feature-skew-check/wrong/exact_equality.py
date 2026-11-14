def find_skew(online: dict, offline: dict, tolerance: float = 1e-6) -> dict:
    out = {}
    for name in sorted(set(online) | set(offline)):
        if name not in online:
            out[name] = "missing_online"
        elif name not in offline:
            out[name] = "missing_offline"
        elif online[name] != offline[name]:
            out[name] = "diff"
    return out
