import math
def _c(xs,ys):
    n=len(xs)
    if n==0: return 0.0
    mx,my=sum(xs)/n,sum(ys)/n
    sxx=sum((x-mx)**2 for x in xs); syy=sum((y-my)**2 for y in ys)
    if sxx==0 or syy==0: return 0.0
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/math.sqrt(sxx*syy)
def find_leaky_features(features, labels, threshold=0.95):
    s=[]
    for k,v in features.items():
        if len(v)>len(labels): raise ValueError
        c=abs(_c(v,labels))
        if c>threshold: s.append((-c,k))
    return [k for _,k in sorted(s)]
