def _parse(v):
    try:
        parts = [int(x) for x in v.split(".")]
    except (ValueError, AttributeError):
        return None
    while parts and parts[-1] == 0:
        parts.pop()
    return tuple(parts)

def latest_version(records, name, stage):
    best, best_key = None, None
    for rec in records:
        if rec.get("name") != name or rec.get("stage") != stage:
            continue
        key = _parse(rec.get("version"))
        if key is None:
            continue
        if best is None or key > best_key:
            best, best_key = rec, key
    if best is None:
        raise LookupError("none")
    return best
