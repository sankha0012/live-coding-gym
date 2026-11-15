def fill_features(row: dict, defaults: dict, empty_is_missing: bool = False) -> tuple[dict, list[str]]:
    out = dict(row)
    filled = []
    for name, default in defaults.items():
        value = row.get(name)
        if value is None or (empty_is_missing and isinstance(value, str) and value == ""):
            out[name] = default
            filled.append(name)
    return out, sorted(filled)
