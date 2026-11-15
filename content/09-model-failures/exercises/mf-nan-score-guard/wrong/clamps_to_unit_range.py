import math
def guard_scores(scores, fallback=0.5):
    out=[]; bad=0
    for s in scores:
        if isinstance(s,(int,float)) and not isinstance(s,bool) and math.isfinite(s) and 0<=s<=1:
            out.append(s)
        else:
            out.append(fallback); bad+=1
    return out,bad
