def rank(records):
    return sorted(records, key=lambda r: (r["name"], -r["score"]))
