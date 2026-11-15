from statistics import mean, pstdev


def drift_alarm(reference, live, k=3.0):
    if not reference or not live:
        return {"alarm": False, "reasons": ["no_data"]}
    reasons = []
    if abs(mean(live) - mean(reference)) > k * pstdev(reference):
        reasons.append("mean")
    return {"alarm": bool(reasons), "reasons": reasons}
