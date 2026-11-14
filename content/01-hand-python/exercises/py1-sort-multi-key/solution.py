def rank(records):
    return sorted(records, key=lambda r: (-r["score"], r["name"]))
