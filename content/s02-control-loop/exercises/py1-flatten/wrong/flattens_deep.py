def flatten(lists: list) -> list:
    out = []
    for x in lists:
        if isinstance(x, list):
            out.extend(flatten(x))
        else:
            out.append(x)
    return out
