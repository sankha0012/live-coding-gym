def fill_features(row: dict, defaults: dict) -> tuple[dict, list[str]]:
    out = dict(row)
    filled = []
    for name, default in defaults.items():
        if not row.get(name):
            out[name] = default
            filled.append(name)
    return out, sorted(filled)
