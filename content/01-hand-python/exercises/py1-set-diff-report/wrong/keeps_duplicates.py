def set_diff_report(old, new) -> dict:
    return {
        "added": sorted(x for x in new if x not in old),
        "removed": sorted(x for x in old if x not in new),
        "kept": sorted(x for x in old if x in new),
    }
