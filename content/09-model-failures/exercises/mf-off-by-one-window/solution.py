def rolling_mean(values: list[float], window: int) -> list[float | None]:
    """Rolling mean feature.

    Output i is the mean of the `window` values that end at index i, including
    values[i]. The first window - 1 outputs have no full window and are None.
    The output has the same length as the input. window < 1 raises ValueError.
    """
    if window < 1:
        raise ValueError("window must be at least 1")
    out: list[float | None] = []
    for i in range(len(values)):
        if i < window - 1:
            out.append(None)
            continue
        out.append(sum(values[i - window + 1 : i + 1]) / window)
    return out
