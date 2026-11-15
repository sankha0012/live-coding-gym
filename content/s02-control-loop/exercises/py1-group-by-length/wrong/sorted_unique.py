def group_by_length(words: list) -> dict:
    out = {}
    for w in words:
        out.setdefault(len(w), set()).add(w)
    return {n: sorted(ws) for n, ws in out.items()}
