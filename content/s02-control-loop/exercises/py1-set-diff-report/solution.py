def set_diff_report(old, new) -> dict:
    o, n = set(old), set(new)
    return {
        "added": sorted(n - o),
        "removed": sorted(o - n),
        "kept": sorted(o & n),
    }
