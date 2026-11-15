from statistics import mean, stdev


def drift_alarm(reference, live, k=3.0):
    if len(reference) < 2 or len(live) < 2:
        return {"alarm": False, "reasons": ["no_data"]}
    rs = stdev(reference)
    limit = k * rs
    reasons = []
    if abs(mean(live) - mean(reference)) > limit:
        reasons.append("mean")
    if abs(stdev(live) - rs) > limit:
        reasons.append("std")
    return {"alarm": bool(reasons), "reasons": reasons}
