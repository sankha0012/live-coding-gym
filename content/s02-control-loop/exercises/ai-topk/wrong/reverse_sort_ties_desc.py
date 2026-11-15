import math
def top_k(query, docs, k):
    n=lambda v: math.sqrt(sum(x*x for x in v))
    qn=n(query); sc=[]
    for i,v in docs.items():
        dn=n(v)
        if dn==0 or qn==0: continue
        sc.append((sum(a*b for a,b in zip(query,v))/(qn*dn), i))
    sc.sort(reverse=True)
    return [i for _,i in sc[:k]]
