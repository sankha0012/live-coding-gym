from statistics import mean, pstdev
def drift_alarm(reference, live, k=3.0):
    if not reference or not live: return {"alarm": False, "reasons": ["no_data"]}
    rs=pstdev(reference); lim=k*rs; r=[]
    if abs(mean(live)-mean(reference))>3*rs: r.append("mean")
    if abs(pstdev(live)-rs)>lim: r.append("std")
    return {"alarm": bool(r), "reasons": r}
