def flatten(lists: list) -> list:
    out = lists.pop(0) if lists else []
    for inner in lists:
        out.extend(inner)
    return out
