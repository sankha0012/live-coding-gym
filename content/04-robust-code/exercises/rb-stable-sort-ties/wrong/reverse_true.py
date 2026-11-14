def rank(records):
    return sorted(records, key=lambda r: (r["score"] is None, r["score"] or 0, r["id"]), reverse=True)
