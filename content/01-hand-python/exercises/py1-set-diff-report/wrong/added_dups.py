def set_diff_report(old, new) -> dict:
    return {
        "added": [x for x in sorted(new) if x not in old],
        "removed": sorted(set(old) - set(new)),
        "kept": sorted(set(old) & set(new)),
    }
