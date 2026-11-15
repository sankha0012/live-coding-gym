def rank(records):
    for r in records:
        r["_k"] = (r["score"] is None, -(r["score"] or 0), r["id"])
    return sorted(records, key=lambda r: r["_k"])
