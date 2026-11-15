import math

def check_batch(values, ref_mean, ref_std, max_null_rate=0.05, z=3.0):
    if not values:
        return ["empty"]
    valid = [v for v in values if v is not None and not math.isnan(v)]
    alerts = []
    if 1 - len(valid) / len(values) > max_null_rate:
        alerts.append("null_rate")
    if valid:
        mean = sum(valid) / len(valid)
        if (mean - ref_mean) > z * ref_std / math.sqrt(len(valid)):
            alerts.append("mean_shift")
    return sorted(alerts)
