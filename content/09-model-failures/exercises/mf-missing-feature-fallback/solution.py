def fill_features(row: dict, defaults: dict) -> tuple[dict, list[str]]:
    out = dict(row)
    filled = []
    for name, default in defaults.items():
        if row.get(name) is None:
            out[name] = default
            filled.append(name)
    return out, sorted(filled)
