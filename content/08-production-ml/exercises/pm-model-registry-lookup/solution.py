def _parse(version: str):
    if not isinstance(version, str):
        return None
    pieces = version.split(".")
    if not all(p.isascii() and p.isdigit() for p in pieces):
        return None
    parts = [int(p) for p in pieces]
    while parts and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def latest_version(records: list[dict], name: str, stage: str) -> dict:
    best, best_key = None, None
    for rec in records:
        if rec.get("name") != name or rec.get("stage") != stage:
            continue
        parts = _parse(rec.get("version"))
        if parts is None:
            continue
        key = parts
        if best is None or key > best_key:
            best, best_key = rec, key
    if best is None:
        raise LookupError(f"no {stage} version of {name}")
    return best
