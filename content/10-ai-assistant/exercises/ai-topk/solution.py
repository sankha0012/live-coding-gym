import math

def top_k(query, docs, k):
    def norm(v):
        return math.sqrt(sum(x * x for x in v))
    qn = norm(query)
    scored = []
    for doc_id, vec in docs.items():
        dn = norm(vec)
        if dn == 0 or qn == 0:
            continue
        cos = sum(x * y for x, y in zip(query, vec)) / (qn * dn)
        scored.append((cos, doc_id))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [doc_id for _, doc_id in scored[:k]]
