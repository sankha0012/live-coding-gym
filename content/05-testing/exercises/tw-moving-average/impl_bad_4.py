def moving_average(values, window):
    if window < 1:
        return []
    return [sum(values[i:i + window]) / window for i in range(len(values) - window + 1)]
