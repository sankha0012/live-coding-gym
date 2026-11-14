def group_by_length(words: list) -> dict:
    out = {}
    for w in words:
        out.setdefault(len(w), []).append(w)
    return out
