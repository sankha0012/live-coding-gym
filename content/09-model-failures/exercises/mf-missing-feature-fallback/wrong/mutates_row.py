def fill_features(row: dict, defaults: dict) -> tuple[dict, list[str]]:
    filled = []
    for name, default in defaults.items():
        if row.get(name) is None:
            row[name] = default
            filled.append(name)
    return row, sorted(filled)
