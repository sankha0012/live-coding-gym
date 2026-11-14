from statistics import mean, pstdev


def drift_alarm(reference, live, k=3.0):
    rs = pstdev(reference)
    limit = k * rs
    reasons = []
    if abs(mean(live) - mean(reference)) > limit:
        reasons.append("mean")
    if abs(pstdev(live) - rs) > limit:
        reasons.append("std")
    return {"alarm": bool(reasons), "reasons": reasons}
