def unique(items: list) -> list:
    out = []
    for x in reversed(items):
        if x not in out:
            out.append(x)
    return out[::-1]
