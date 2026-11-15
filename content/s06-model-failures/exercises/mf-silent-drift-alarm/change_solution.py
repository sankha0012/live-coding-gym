from statistics import mean, pstdev


def drift_alarm(reference: list[float], live: list[float], k: float = 3.0, min_live: int = 1) -> dict:
    if not reference or len(live) < min_live or not live:
        return {"alarm": False, "reasons": ["no_data"]}
    rs = pstdev(reference)
    limit = k * rs
    reasons = []
    if abs(mean(live) - mean(reference)) > limit:
        reasons.append("mean")
    if abs(pstdev(live) - rs) > limit:
        reasons.append("std")
    return {"alarm": bool(reasons), "reasons": reasons}
