def rank(records):
    records.sort(key=lambda r: (r["score"] is None, -(r["score"] or 0), r["id"]))
    return records
