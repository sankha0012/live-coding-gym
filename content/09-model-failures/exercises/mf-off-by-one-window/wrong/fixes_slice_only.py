def rolling_mean(values, window):
    if window < 1:
        raise ValueError("window must be at least 1")
    out = []
    for i in range(len(values)):
        if i < window:
            out.append(None)
            continue
        out.append(sum(values[i - window + 1 : i + 1]) / window)
    return out
