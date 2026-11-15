def flatten(lists: list) -> list:
    out = []
    for inner in lists:
        for x in inner:
            if x not in out:
                out.append(x)
    return out
