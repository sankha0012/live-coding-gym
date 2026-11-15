def _parse(v):
    if not isinstance(v, str) or not all(x.isdigit() for x in v.split(".")):
        return None
    parts = [int(x) for x in v.split(".")][:3]
    parts += [0] * (3 - len(parts))
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
