def top_k(query, docs, k):
    sc=[(sum(a*b for a,b in zip(query,v)), i) for i,v in docs.items() if any(v)]
    sc.sort(key=lambda t:(-t[0],t[1]))
    return [i for _,i in sc[:k]]
