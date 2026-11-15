def second_highest(values):
    s = sorted(values, reverse=True)
    return s[1] if len(s) >= 2 else None
