def set_diff_report(old, new) -> dict:
    return {
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "kept": sorted(x for x in old if x in new),
    }
