def latest_version(records: list[dict], name: str, stage: str) -> dict:
    found = [r for r in records if r["name"] == name]
    if not found:
        raise LookupError("not found")
    return max(found, key=lambda r: tuple(int(p) for p in r["version"].split(".")))
