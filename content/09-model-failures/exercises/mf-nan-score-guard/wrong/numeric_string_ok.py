import math
def guard_scores(scores, fallback=0.5):
    out=[]; bad=0
    for s in scores:
        try:
            if isinstance(s,bool): raise TypeError
            v=float(s)
            if not math.isfinite(v): raise ValueError
            out.append(s if not isinstance(s,str) else v)
        except (TypeError,ValueError):
            out.append(fallback); bad+=1
    return out,bad
