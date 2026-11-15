def latest_version(records: list[dict], name: str, stage: str) -> dict:
    found = [r for r in records if r["name"] == name and r["stage"] == stage]
    if not found:
        return None
    return max(found, key=lambda r: tuple(int(p) for p in r["version"].split(".")))
