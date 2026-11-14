def unique(items: list) -> list:
    seen = ____()
    out = []
    for x in items:
        if x ____ in seen:
            seen.add(x)
            out.append(x)
    return out
