def set_diff_report(old, new) -> dict:
    o, n = set(old), set(new)
    return {"added": list(n - o), "removed": list(o - n), "kept": list(o & n)}
