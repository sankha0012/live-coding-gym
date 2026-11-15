def rank(records):
    return sorted(records, key=lambda r: (not r["score"], -(r["score"] or 0), r["id"]))
