from statistics import mean, pstdev


def drift_alarm(reference, live, k=3.0):
    if not reference or not live:
        return {"alarm": False, "reasons": ["no_data"]}
    rs = pstdev(reference)
    reasons = []
    if abs(mean(live) - mean(reference)) > k * rs:
        reasons.append("mean")
    if pstdev(live) - rs > k * rs:
        reasons.append("std")
    return {"alarm": bool(reasons), "reasons": reasons}
