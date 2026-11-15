def avg_by_customer(rows):
    out = {}
    for c, v in rows:
        if c not in out: out[c] = None
        if v is not None:
            out[c] = v if out[c] is None else (out[c] + v) / 2
    return out
