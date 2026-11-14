import math

def top_k(query, docs, k):
    # 1. cosine(a, b) = dot(a, b) / (|a| * |b|)
    # 2. score every doc, skip zero vectors
    # 3. sort by (-score, id), take k
    pass
